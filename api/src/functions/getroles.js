const { app } = require('@azure/functions');

// SWA rolesSource: SWA POSTs the authenticated identity here after login and
// applies whatever custom roles we return. Grants 'administrator' to the emails
// listed in the ADMIN_EMAILS app setting (comma-separated).
app.http('GetRoles', {
  methods: ['POST'],
  authLevel: 'anonymous',
  route: 'GetRoles',
  handler: async (request) => {
    let body = {};
    try { body = await request.json(); } catch { body = {}; }

    const admins = (process.env.ADMIN_EMAILS || '')
      .toLowerCase().split(',').map((s) => s.trim()).filter(Boolean);

    const candidates = [];
    if (body.userDetails) candidates.push(String(body.userDetails).toLowerCase());
    if (Array.isArray(body.claims)) {
      body.claims.forEach((c) => {
        if (/email|preferred_username|upn|name/i.test(c.typ || '') && c.val) {
          candidates.push(String(c.val).toLowerCase());
        }
      });
    }

    const roles = candidates.some((e) => admins.includes(e)) ? ['administrator'] : [];
    return { jsonBody: { roles } };
  },
});
