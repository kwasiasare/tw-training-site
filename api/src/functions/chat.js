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

    function trace(response) {
      context.log(JSON.stringify({
        event: 'chat_query',
        outcome,
        courses,
        lessonIds,
        turns,
        qLen,
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

      // Tracks whether the gateway was attempted and failed, so a subsequent
      // Anthropic success can be logged as a measurably-degraded outcome
      // rather than indistinguishable from the pure-Anthropic path.
      let gatewayFellBack = false;

      // Prefer the self-hosted local LLM gateway (RAG over ingested course
      // content) when configured, with automatic fallback to the existing
      // two-stage Anthropic pipeline on ANY gateway failure — a flaky or
      // unreachable gateway must never surface as a student-facing error, only
      // a slightly slower reply from the path we already trust.
      const { isGatewayConfigured, answerViaGateway } = require('../shared/localllm');
      if (isGatewayConfigured()) {
        try {
          const gatewayResult = await answerViaGateway({ messages: convo });

          // The gateway's answer is grounded in its own retrieval, so prefer
          // lesson links derived from its sources over the Stage-1 selection
          // — those citations can otherwise misrepresent what the answer is
          // actually based on. Each source's metadata.source is a relative
          // path (e.g. 'kwasi-GenAI/lessons/g2-l01-embeddings.md'); its
          // basename minus the .md extension is a candidate lesson id.
          const seenIds = new Set();
          const gatewayLessons = [];
          for (const source of gatewayResult.sources) {
            const relPath = source && source.metadata && source.metadata.source;
            if (typeof relPath !== 'string' || !relPath) continue;
            const base = relPath.split('/').pop();
            const id = base.endsWith('.md') ? base.slice(0, -3) : base;
            if (!id || seenIds.has(id)) continue;
            const lesson = getLesson(id);
            if (!lesson) continue;
            seenIds.add(id);
            const course = courseList.find((c) => c.slug === lesson.course);
            gatewayLessons.push({ id, title: lesson.title, course: lesson.course, courseTitle: (course && course.title) || lesson.course });
          }

          const responseLessons = gatewayLessons.length
            ? gatewayLessons.map((l) => ({ id: l.id, title: l.title, course: l.course }))
            : mappedLessons;

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
          gatewayFellBack = true;
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

      outcome = gatewayFellBack ? 'answered_after_gateway_fallback' : 'answered';
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
