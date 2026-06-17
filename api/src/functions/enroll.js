const { app } = require('@azure/functions');
const { getUser } = require('../shared/principal');
const { getContainer } = require('../shared/cosmos');

// POST /api/enroll {course} -> record an enrollment for the signed-in user
app.http('enroll', {
  methods: ['POST'],
  authLevel: 'anonymous', // SWA enforces auth at the route level
  route: 'enroll',
  handler: async (request, context) => {
    const user = getUser(request);
    if (!user) return { status: 401, jsonBody: { error: 'not_authenticated' } };

    try {
      const body = await request.json().catch(() => ({}));
      const { course } = body;
      if (!course) return { status: 400, jsonBody: { error: 'course_required' } };

      const doc = {
        id: `${user.userId}:enroll:${course}`,
        userId: user.userId,
        type: 'enrollment',
        course,
        enrolledAt: new Date().toISOString(),
      };
      const { resource } = await getContainer().items.upsert(doc);
      return { jsonBody: { ok: true, item: resource } };
    } catch (err) {
      context.error('enroll error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});
