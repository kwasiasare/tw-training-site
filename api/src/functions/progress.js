const { app } = require('@azure/functions');
const { getUser } = require('../shared/principal');
const { getContainer } = require('../shared/cosmos');

// Course/lesson are slugs (e.g. "kwasi-GenAI", "m1-l01-how-python-runs"). Validate
// to that shape so untrusted free-text can't be stored (data pollution + injection
// when rendered downstream, e.g. the admin dashboard).
const SLUG_RE = /^[a-z0-9-]+$/i;
const isSlug = (s) => typeof s === 'string' && s.length > 0 && s.length <= 80 && SLUG_RE.test(s);

// GET  /api/progress           -> all progress records for the signed-in user
// POST /api/progress {course,lesson,status,quizScore} -> upsert one record
app.http('progress', {
  methods: ['GET', 'POST'],
  authLevel: 'anonymous', // SWA enforces auth at the route level (staticwebapp.config.json)
  route: 'progress',
  handler: async (request, context) => {
    const user = getUser(request);
    if (!user) return { status: 401, jsonBody: { error: 'not_authenticated' } };

    try {
      const container = getContainer();

      if (request.method === 'GET') {
        const { resources } = await container.items
          .query({
            query: 'SELECT * FROM c WHERE c.userId = @u',
            parameters: [{ name: '@u', value: user.userId }],
          })
          .fetchAll();
        return { jsonBody: { items: resources } };
      }

      const body = await request.json().catch(() => ({}));
      const { course, lesson, status, quizScore } = body;
      if (!course || !lesson) {
        return { status: 400, jsonBody: { error: 'course_and_lesson_required' } };
      }
      if (!isSlug(course) || !isSlug(lesson)) {
        return { status: 400, jsonBody: { error: 'invalid_course_or_lesson' } };
      }
      // The lesson must exist in the bundled index and belong to the claimed
      // course. Slug-shape alone isn't enough: the certificate endpoint counts
      // distinct completed lessons per course, so accepting arbitrary slugs
      // would let a user mint a certificate from fabricated lesson ids.
      const { getLesson } = require('../shared/lessons');
      const known = getLesson(lesson);
      if (!known || known.course !== course) {
        return { status: 400, jsonBody: { error: 'unknown_lesson' } };
      }
      const id = `${user.userId}:${course}:${lesson}`;
      // Merge into any existing record so marking complete and saving a quiz
      // score (separate actions) don't overwrite each other.
      let existing = null;
      try {
        existing = (await container.item(id, user.userId).read()).resource;
      } catch {
        existing = null;
      }
      const doc = {
        id,
        userId: user.userId,
        userDetails: user.userDetails,
        type: 'progress',
        course,
        lesson,
        status: status || (existing && existing.status) || 'completed',
        updatedAt: new Date().toISOString(),
      };
      const score = typeof quizScore === 'number' ? quizScore : existing && existing.quizScore;
      if (typeof score === 'number') doc.quizScore = score;

      const { resource } = await container.items.upsert(doc);
      return { jsonBody: { ok: true, item: resource } };
    } catch (err) {
      context.error('progress error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});
