const { app } = require('@azure/functions');

// POST /api/grade (TW-68) — AI grading of an open-ended quiz answer.
// Auth-gated by the /api/* route rule (re-checked here). The learner sends
// { lesson, qIndex, answer }; the backend looks up the lesson's quiz server-side
// (the reference answer is never trusted from the client) and asks Claude to grade
// the learner's answer against it. Only open-ended questions (no options) are
// gradable — MCQs are scored client-side already.

const SLUG_RE = /^[a-z0-9-]+$/i;
const MAX_ANSWER = 4000;

app.http('grade', {
  methods: ['POST'],
  authLevel: 'anonymous', // SWA enforces auth at the route level
  route: 'grade',
  handler: async (request, context) => {
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    // 403 (not 401) so SWA's global 401 -> /signin redirect doesn't turn the
    // client's fetch into the sign-in HTML page (same reason as video.js).
    if (!user) return { status: 403, jsonBody: { error: 'login_required' } };

    try {
      const body = await request.json().catch(() => ({}));
      const lessonId = typeof body.lesson === 'string' ? body.lesson.trim() : '';
      const qIndex = Number.isInteger(body.qIndex) ? body.qIndex : -1;
      const answer = typeof body.answer === 'string' ? body.answer.trim() : '';

      if (!lessonId || lessonId.length > 80 || !SLUG_RE.test(lessonId)) {
        return { status: 400, jsonBody: { error: 'bad_lesson' } };
      }
      if (qIndex < 0) return { status: 400, jsonBody: { error: 'bad_question' } };
      if (!answer) return { status: 400, jsonBody: { error: 'answer_required' } };

      const { getLesson } = require('../shared/lessons');
      const lesson = getLesson(lessonId);
      if (!lesson) return { status: 404, jsonBody: { error: 'unknown_lesson' } };

      const q = (lesson.quiz || [])[qIndex];
      if (!q) return { status: 404, jsonBody: { error: 'unknown_question' } };
      if (q.options) return { status: 400, jsonBody: { error: 'not_gradable' } }; // MCQ

      const { gradeAnswer } = require('../shared/grader');
      let result;
      try {
        result = await gradeAnswer({
          question: q.q,
          referenceAnswer: typeof q.answer === 'string' ? q.answer : String(q.answer ?? ''),
          why: q.why,
          learnerAnswer: answer.slice(0, MAX_ANSWER),
        });
      } catch (err) {
        if (err && err.code === 'refusal') return { status: 422, jsonBody: { error: 'cannot_grade' } };
        throw err;
      }

      return {
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: result,
      };
    } catch (err) {
      context.error('grade error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});
