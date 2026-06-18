const { app } = require('@azure/functions');
const { getUser } = require('../shared/principal');
const { getContainer } = require('../shared/cosmos');

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
