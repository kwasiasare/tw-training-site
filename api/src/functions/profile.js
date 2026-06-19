const { app } = require('@azure/functions');

// GET  /api/profile -> { email, displayName, enrolledCourses:[{course,completed}] }
// POST /api/profile { displayName } -> upsert the user's profile (display name)
// Route is gated to 'authenticated' in staticwebapp.config.json. Lazy-requires
// shared modules inside the handler (the pattern that reliably registers on SWA).
app.http('profile', {
  methods: ['GET', 'POST'],
  authLevel: 'anonymous',
  route: 'profile',
  handler: async (request, context) => {
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    if (!user) return { status: 401, jsonBody: { error: 'not_authenticated' } };

    try {
      const { getContainer } = require('../shared/cosmos');
      const container = getContainer();
      const profileId = `${user.userId}:profile`;

      if (request.method === 'POST') {
        const body = await request.json().catch(() => ({}));
        let displayName = typeof body.displayName === 'string' ? body.displayName.trim() : '';
        if (displayName.length > 60) displayName = displayName.slice(0, 60);
        const doc = {
          id: profileId,
          userId: user.userId,
          type: 'profile',
          displayName,
          email: user.userDetails,
          updatedAt: new Date().toISOString(),
        };
        const { resource } = await container.items.upsert(doc);
        return { jsonBody: { ok: true, displayName: resource.displayName } };
      }

      // GET — read profile doc + derive enrolled courses from progress/enrollment.
      let profile = null;
      try {
        profile = (await container.item(profileId, user.userId).read()).resource;
      } catch {
        profile = null;
      }
      const { resources } = await container.items
        .query({
          query: 'SELECT c.course, c.type, c.status FROM c WHERE c.userId = @u',
          parameters: [{ name: '@u', value: user.userId }],
        })
        .fetchAll();

      const byCourse = {};
      resources.forEach((r) => {
        if ((r.type === 'progress' || r.type === 'enrollment') && r.course) {
          byCourse[r.course] = byCourse[r.course] || { course: r.course, completed: 0 };
          if (r.type === 'progress' && r.status === 'completed') byCourse[r.course].completed += 1;
        }
      });
      const enrolledCourses = Object.keys(byCourse)
        .map((k) => byCourse[k])
        .sort((a, b) => b.completed - a.completed);

      return {
        jsonBody: {
          email: user.userDetails,
          displayName: (profile && profile.displayName) || '',
          enrolledCourses,
        },
      };
    } catch (err) {
      context.error('profile error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});
