const { app } = require('@azure/functions');

// POST /api/chat (TW-117) — cross-course Q&A chatbot, Phase 1 / Tier A (public
// course content only, no live student data). Runs alongside tutor.js as a
// distinct, complementary feature: tutor.js stays single-lesson; this endpoint
// answers catalog-wide "which course / which lesson" and general course-topic
// questions from a global, every-page widget.
//
// Auth-gated by the /api/chat route rule in staticwebapp.config.json (and
// re-checked here, same 403-not-401 pattern as tutor.js so SWA's global 401 ->
// /signin redirect doesn't turn the client's fetch into the sign-in HTML page).
// The client sends only { messages }; the backend looks up any relevant lesson
// text server-side, so — like tutor.js — this endpoint can't be used as a free,
// ungrounded Claude proxy. Lazy-requires shared modules inside the handler (the
// pattern that reliably registers on SWA).

// Map engine-reported source paths (the gateway's relpaths, e.g.
// 'kwasi-GenAI/lessons/g2-l01-embeddings.md', or Bedrock's s3:// URIs, e.g.
// 's3://bucket/kwasi-GenAI/lessons/g2-l01-embeddings.md') to lesson records,
// deduped by lesson id. Only the basename matters for either source shape, so
// one helper covers both engines. `getLesson` is injected (rather than
// required here) so this stays a pure function of its inputs.
function mapSourcePathsToLessons(paths, getLesson) {
  const seenIds = new Set();
  const mapped = [];
  for (const raw of paths || []) {
    if (typeof raw !== 'string' || !raw) continue;
    const base = raw.split('/').pop();
    const id = base.endsWith('.md') ? base.slice(0, -3) : base;
    if (!id || seenIds.has(id)) continue;
    const lesson = getLesson(id);
    if (!lesson) continue;
    seenIds.add(id);
    mapped.push({ id, title: lesson.title, course: lesson.course });
  }
  return mapped;
}

const OFF_TOPIC_REPLY =
  "I can help with questions about our courses and how the site works — for example " +
  "'Which course covers Kubernetes?', 'What's the difference between the ML Engineer and " +
  "MLOps tracks?', or 'How do certificates work?'. For anything else, please contact support.";

const NO_MATCH_REPLY =
  "I couldn't find that in our current course material. You can browse all courses on the " +
  'home page — and if you think we should cover it, let us know.';

app.http('chat', {
  methods: ['POST'],
  authLevel: 'anonymous', // SWA enforces auth at the route level
  route: 'chat',
  handler: async (request, context) => {
    const start = Date.now();
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    // 403 (not 401) so SWA's global 401 -> /signin redirect doesn't turn the
    // client's fetch into the sign-in HTML page (same reason as tutor.js/video.js).
    if (!user) {
      context.log(JSON.stringify({ event: 'chat_query', outcome: 'unauthenticated', ms: Date.now() - start }));
      return { status: 403, jsonBody: { error: 'login_required' } };
    }

    // Structured trace state, filled in as the handler proceeds and logged once
    // at every exit point via trace() below. NEVER log the actual question text.
    let outcome = 'error';
    let courses = [];
    let lessonIds = [];
    let turns = 0;
    let qLen = 0;
    // Which configured engines did not produce the answer — failed, or were
    // skipped to protect the time budget — in attempt order, e.g.
    // ['bedrock_kb'] or ['bedrock_kb', 'local_gateway']. Empty when nothing
    // fell back, including when an engine was never configured at all.
    const fellBack = [];

    function trace(response) {
      context.log(JSON.stringify({
        event: 'chat_query',
        outcome,
        courses,
        lessonIds,
        turns,
        qLen,
        fellBack,
        ms: Date.now() - start,
      }));
      return response;
    }

    try {
      const { normalizeMessages } = require('../shared/tutor');
      const body = await request.json().catch(() => ({}));
      const convo = normalizeMessages(body.messages);
      turns = convo.length;
      if (!convo.length || convo[convo.length - 1].role !== 'user') {
        outcome = 'bad_request';
        return trace({ status: 400, jsonBody: { error: 'no_question' } });
      }
      qLen = convo[convo.length - 1].content.length;

      // Rate limit check BEFORE any Claude call, so a limited request never
      // spends a Stage-1/Stage-2 call.
      const { checkChatLimits } = require('../shared/ratelimit');
      const ip = request.headers.get('x-forwarded-for');
      const rl = await checkChatLimits({ userId: user.userId, ip });
      if (!rl.allowed) {
        outcome = rl.scope === 'ip' ? 'rate_limited_ip' : 'rate_limited_user';
        return trace({
          status: 429,
          jsonBody: { error: 'rate_limited', retryAfterSeconds: rl.retryAfterSeconds },
        });
      }

      const { selectLessons, answerCourseQuestion, answerSiteHelpQuestion } = require('../shared/chat');
      const selection = await selectLessons({ messages: convo });

      if (selection.status === 'off_topic') {
        outcome = 'refused_offtopic';
        return trace({
          status: 200,
          headers: { 'cache-control': 'private, no-store' },
          jsonBody: { reply: OFF_TOPIC_REPLY, lessons: [] },
        });
      }
      if (selection.status === 'clarify') {
        outcome = 'clarify';
        return trace({
          status: 200,
          headers: { 'cache-control': 'private, no-store' },
          jsonBody: { reply: selection.message, lessons: [] },
        });
      }
      if (selection.status === 'site_help') {
        let siteResult;
        try {
          siteResult = await answerSiteHelpQuestion({ messages: convo });
        } catch (err) {
          if (err && err.code === 'refusal') {
            outcome = 'refused_model_sitehelp';
            return trace({ status: 422, jsonBody: { error: 'cannot_answer' } });
          }
          throw err;
        }
        outcome = 'site_help';
        return trace({
          status: 200,
          headers: { 'cache-control': 'private, no-store' },
          jsonBody: { reply: siteResult.reply, lessons: [] },
        });
      }

      // 'no_match', or 'ok' with no (valid) lesson ids surviving validation —
      // treat both as no_match rather than calling Stage 2 with nothing to
      // ground on.
      if (selection.status !== 'ok' || !selection.lessonIds.length) {
        outcome = 'no_match';
        return trace({
          status: 200,
          headers: { 'cache-control': 'private, no-store' },
          jsonBody: { reply: NO_MATCH_REPLY, lessons: [] },
        });
      }

      const { getLesson } = require('../shared/lessons');
      const { allCourses } = require('../shared/catalog');
      const courseList = allCourses();
      const lessons = selection.lessonIds
        .map((id) => {
          const lesson = getLesson(id);
          if (!lesson) return null;
          const course = courseList.find((c) => c.slug === lesson.course);
          return {
            id,
            course: lesson.course,
            courseTitle: (course && course.title) || lesson.course,
            title: lesson.title,
            objectives: lesson.objectives,
            body: lesson.body,
          };
        })
        .filter(Boolean);

      if (!lessons.length) {
        outcome = 'no_match';
        return trace({
          status: 200,
          headers: { 'cache-control': 'private, no-store' },
          jsonBody: { reply: NO_MATCH_REPLY, lessons: [] },
        });
      }

      courses = [...new Set(lessons.map((l) => l.course))];
      lessonIds = lessons.map((l) => l.id);

      const mappedLessons = lessons.map((l) => ({ id: l.id, title: l.title, course: l.course }));

      // Prefer AWS Bedrock Knowledge Base (managed RAG over ingested course
      // content) when configured — the PRIMARY engine, ahead of the
      // self-hosted local LLM gateway and the existing two-stage Anthropic
      // pipeline. Same fallback-first contract as the gateway below: ANY
      // Bedrock failure falls through to the next engine rather than
      // surfacing as a student-facing error.
      const { isBedrockKbConfigured, answerViaBedrockKb } = require('../shared/bedrockkb');
      if (isBedrockKbConfigured()) {
        try {
          const bedrockResult = await answerViaBedrockKb({ messages: convo });

          // The Knowledge Base's answer is grounded in its own retrieval, so
          // prefer lesson links derived from its sources over the Stage-1
          // selection, same reasoning as the gateway path below.
          const bedrockLessons = mapSourcePathsToLessons(bedrockResult.sourcePaths, getLesson);
          const responseLessons = bedrockLessons.length ? bedrockLessons : mappedLessons;

          if (bedrockLessons.length) {
            courses = [...new Set(bedrockLessons.map((l) => l.course))];
            lessonIds = bedrockLessons.map((l) => l.id);
          }

          outcome = 'answered_bedrock';
          return trace({
            status: 200,
            headers: { 'cache-control': 'private, no-store' },
            jsonBody: { reply: bedrockResult.reply, lessons: responseLessons },
          });
        } catch (err) {
          // NEVER log the question text or AWS credentials — only the
          // classifying error code/message — then fall through to the gateway.
          context.log(JSON.stringify({
            event: 'chat_bedrock_fallback',
            code: (err && err.code) || 'unknown',
            message: err && err.message,
          }));
          fellBack.push('bedrock_kb');
        }
      }

      // Prefer the self-hosted local LLM gateway (RAG over ingested course
      // content) when configured, with automatic fallback to the existing
      // two-stage Anthropic pipeline on ANY gateway failure — a flaky or
      // unreachable gateway must never surface as a student-facing error, only
      // a slightly slower reply from the path we already trust.
      const { isGatewayConfigured, answerViaGateway } = require('../shared/localllm');
      // Skip the gateway attempt entirely when the request is already deep
      // into Azure SWA's ~45s ceiling (Stage-1 plus a timed-out Bedrock
      // attempt can consume ~15s): a further 15s gateway timeout would leave
      // the Anthropic fallback no room to answer, turning a recoverable
      // engine failure into a student-facing 500.
      const GATEWAY_SKIP_AFTER_MS = 20000;
      if (isGatewayConfigured() && Date.now() - start > GATEWAY_SKIP_AFTER_MS) {
        context.log(JSON.stringify({
          event: 'chat_gateway_fallback',
          code: 'skipped_time_budget',
          message: `gateway skipped after ${Date.now() - start}ms elapsed`,
        }));
        fellBack.push('local_gateway');
      } else if (isGatewayConfigured()) {
        try {
          const gatewayResult = await answerViaGateway({ messages: convo });

          // The gateway's answer is grounded in its own retrieval, so prefer
          // lesson links derived from its sources over the Stage-1 selection
          // — those citations can otherwise misrepresent what the answer is
          // actually based on. Each source's metadata.source is a relative
          // path (e.g. 'kwasi-GenAI/lessons/g2-l01-embeddings.md'); its
          // basename minus the .md extension is a candidate lesson id.
          const gatewaySourcePaths = (gatewayResult.sources || [])
            .map((source) => source && source.metadata && source.metadata.source)
            .filter((p) => typeof p === 'string' && p);
          const gatewayLessons = mapSourcePathsToLessons(gatewaySourcePaths, getLesson);
          const responseLessons = gatewayLessons.length ? gatewayLessons : mappedLessons;

          if (gatewayLessons.length) {
            courses = [...new Set(gatewayLessons.map((l) => l.course))];
            lessonIds = gatewayLessons.map((l) => l.id);
          }

          outcome = 'answered_gateway';
          return trace({
            status: 200,
            headers: { 'cache-control': 'private, no-store' },
            jsonBody: { reply: gatewayResult.reply, lessons: responseLessons },
          });
        } catch (err) {
          // NEVER log the question text or the gateway key — only the
          // classifying error code/message — then fall through to Anthropic.
          context.log(JSON.stringify({
            event: 'chat_gateway_fallback',
            code: (err && err.code) || 'unknown',
            message: err && err.message,
          }));
          fellBack.push('local_gateway');
        }
      }

      let result;
      try {
        result = await answerCourseQuestion({ lessons, messages: convo });
      } catch (err) {
        if (err && err.code === 'refusal') {
          outcome = 'refused_model';
          return trace({ status: 422, jsonBody: { error: 'cannot_answer' } });
        }
        throw err;
      }

      outcome = fellBack.length ? 'answered_after_fallback' : 'answered';
      return trace({
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: {
          reply: result.reply,
          lessons: mappedLessons,
        },
      });
    } catch (err) {
      context.error('chat error', err);
      outcome = 'error';
      return trace({ status: 500, jsonBody: { error: 'server_error' } });
    }
  },
});
