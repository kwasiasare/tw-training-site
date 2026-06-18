const { app } = require('@azure/functions');

// TEMPORARY diagnostic: anonymous health check to confirm functions deploy,
// env vars are present, and Cosmos is reachable. Remove after debugging.
app.http('ping', {
  methods: ['GET'],
  authLevel: 'anonymous',
  route: 'ping',
  handler: async () => {
    let cosmos = 'untested';
    try {
      const { getContainer } = require('../shared/cosmos');
      const { resources } = await getContainer().items
        .query({ query: 'SELECT VALUE COUNT(1) FROM c' }).fetchAll();
      cosmos = 'ok count=' + JSON.stringify(resources);
    } catch (e) {
      cosmos = 'error: ' + String((e && e.message) || e);
    }
    return {
      jsonBody: {
        ok: true,
        node: process.version,
        hasCosmos: !!process.env.COSMOS_CONNECTION_STRING,
        hasAdminEmails: !!process.env.ADMIN_EMAILS,
        cosmos,
      },
    };
  },
});
