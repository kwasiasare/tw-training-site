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

      outcome = 'answered';
      return trace({
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: {
          reply: result.reply,
          lessons: lessons.map((l) => ({ id: l.id, title: l.title, course: l.course })),
        },
      });
    } catch (err) {
      context.error('chat error', err);
      outcome = 'error';
      return trace({ status: 500, jsonBody: { error: 'server_error' } });
    }
  },
});
