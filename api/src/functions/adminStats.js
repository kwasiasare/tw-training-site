const { app } = require('@azure/functions');
const { getUser } = require('../shared/principal');
const { getContainer } = require('../shared/cosmos');

// GET /api/admin/stats — platform analytics for admins. SWA restricts the route
// to the 'administrator' role; we re-check the role here as defence in depth.
app.http('adminStats', {
  methods: ['GET'],
  authLevel: 'anonymous',
  route: 'admin/stats',
  handler: async (request, context) => {
    const user = getUser(request);
    if (!user) return { status: 401, jsonBody: { error: 'not_authenticated' } };
    if (!(user.roles || []).includes('administrator')) {
      return { status: 403, jsonBody: { error: 'forbidden' } };
    }
    try {
      const container = getContainer();
      const { resources } = await container.items.query({ query: 'SELECT * FROM c' }).fetchAll();
      const progress = resources.filter((r) => r.type === 'progress');
      const enrollments = resources.filter((r) => r.type === 'enrollment');
      const completed = progress.filter((r) => r.status === 'completed');

      const byCourse = {};
      completed.forEach((r) => { byCourse[r.course] = (byCourse[r.course] || 0) + 1; });

      const lessonCounts = {};
      completed.forEach((r) => {
        const k = r.course + ' / ' + r.lesson;
        lessonCounts[k] = (lessonCounts[k] || 0) + 1;
      });
      const topLessons = Object.keys(lessonCounts)
        .map((k) => ({ lesson: k, count: lessonCounts[k] }))
        .sort((a, b) => b.count - a.count).slice(0, 10);

      const scores = completed.filter((r) => typeof r.quizScore === 'number').map((r) => r.quizScore);
      const avgQuiz = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;

      const userMap = {};
      progress.forEach((r) => {
        const u = (userMap[r.userId] = userMap[r.userId] || { user: r.userDetails || r.userId, completed: 0, last: '' });
        if (r.status === 'completed') u.completed += 1;
        if ((r.updatedAt || '') > u.last) u.last = r.updatedAt || '';
      });
      const users = Object.keys(userMap).map((k) => userMap[k]).sort((a, b) => b.completed - a.completed);

      const recent = progress.slice()
        .sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''))
        .slice(0, 15)
        .map((r) => ({ user: r.userDetails || r.userId, course: r.course, lesson: r.lesson, status: r.status, updatedAt: r.updatedAt }));

      return {
        jsonBody: {
          totals: { users: users.length, enrollments: enrollments.length, completions: completed.length, avgQuiz },
          byCourse, topLessons, users, recent,
        },
      };
    } catch (err) {
      context.error('adminStats error', err);
      return { status: 500, jsonBody: { error: 'server_error', detail: String((err && err.message) || err) } };
    }
  },
});
