const { app } = require('@azure/functions');

// POST /api/tutor (TW-67) — in-lesson AI tutor.
// Auth-gated by the /api/* route rule in staticwebapp.config.json (and re-checked
// here). The learner sends { lesson, messages:[{role,content}] }; the backend looks
// up that lesson's authoritative text server-side (the client cannot supply lesson
// content, so the endpoint can't be used as a free, ungrounded Claude proxy) and
// asks Claude to answer grounded in that lesson only. Lazy-requires shared modules
// inside the handler (the pattern that reliably registers on SWA).

const SLUG_RE = /^[a-z0-9-]+$/i;

app.http('tutor', {
  methods: ['POST'],
  authLevel: 'anonymous', // SWA enforces auth at the route level
  route: 'tutor',
  handler: async (request, context) => {
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    if (!user) return { status: 401, jsonBody: { error: 'not_authenticated' } };

    try {
      const body = await request.json().catch(() => ({}));
      const lessonId = typeof body.lesson === 'string' ? body.lesson.trim() : '';
      if (!lessonId || lessonId.length > 80 || !SLUG_RE.test(lessonId)) {
        return { status: 400, jsonBody: { error: 'bad_lesson' } };
      }

      const { getLesson } = require('../shared/lessons');
      const lesson = getLesson(lessonId);
      if (!lesson) return { status: 404, jsonBody: { error: 'unknown_lesson' } };

      const { allCourses } = require('../shared/catalog');
      const course = allCourses().find((c) => c.slug === lesson.course);
      const courseTitle = (course && course.title) || lesson.course;

      const { answerLessonQuestion } = require('../shared/tutor');
      let result;
      try {
        result = await answerLessonQuestion({ lesson, courseTitle, messages: body.messages });
      } catch (err) {
        if (err && err.code === 'no_question') return { status: 400, jsonBody: { error: 'no_question' } };
        if (err && err.code === 'refusal') return { status: 422, jsonBody: { error: 'cannot_answer' } };
        throw err;
      }

      return {
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: { reply: result.reply },
      };
    } catch (err) {
      context.error('tutor error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});
