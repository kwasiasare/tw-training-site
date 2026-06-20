const { app } = require('@azure/functions');

// GET /api/custom-requests (TW-66) — admin-only list of Custom Advisor submissions
// and any queued generation requests, for the /admin dashboard. Route is gated to
// 'authenticated' in staticwebapp.config; the 'administrator' role is enforced here
// (SWA returns 404 not 403 on an allowedRoles miss). Returns PII-minimal rows (no
// résumé text) — user email, target role, status, course.
app.http('custom-requests', {
  methods: ['GET'],
  authLevel: 'anonymous',
  route: 'custom-requests',
  handler: async (request, context) => {
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    if (!user) return { status: 401, jsonBody: { error: 'not_authenticated' } };
    if (!(user.roles || []).includes('administrator')) {
      return { status: 403, jsonBody: { error: 'forbidden' } };
    }

    try {
      const { getContainer } = require('../shared/cosmos');
      const { resources } = await getContainer().items
        .query({ query: "SELECT * FROM c WHERE c.type = 'advisor' OR c.type = 'generationRequest'" })
        .fetchAll();

      const gens = {};
      resources.filter((r) => r.type === 'generationRequest').forEach((g) => { gens[g.userId] = g; });

      const requests = resources
        .filter((r) => r.type === 'advisor')
        .map((a) => {
          const o = a.outcome || {};
          const gen = gens[a.userId];
          const status = o.type === 'matched'
            ? 'matched'
            : gen ? (gen.status || 'generating') : (o.type || 'unknown');
          return {
            user: a.userDetails || a.userId,
            createdAt: a.createdAt,
            targetOutcome: (a.questionnaire || {}).targetOutcome || '',
            recommendedRole: (a.analysis || {}).recommendedRole || '',
            targetRoles: ((a.analysis || {}).targetRoles || []).map((t) => t.role),
            status,
            course: o.courseSlug || '',
          };
        })
        .sort((x, y) => (y.createdAt || '').localeCompare(x.createdAt || ''));

      return {
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: { requests },
      };
    } catch (err) {
      context.error('custom-requests error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});
