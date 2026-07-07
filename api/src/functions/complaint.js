const { app } = require('@azure/functions');

// POST /api/complaint (TW-133) — public complaints/suggestions form. Anonymous
// by design (no login required to send feedback); if a signed-in user submits
// it, we capture them for the log/email context but never require it. Lazy-
// requires shared modules inside the handler (the pattern that reliably
// registers on SWA — see chat.js/custom-advisor.js for the same convention).

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const VALID_KINDS = new Set(['complaint', 'suggestion']);

app.http('complaint', {
  methods: ['POST'],
  authLevel: 'anonymous',
  route: 'complaint',
  handler: async (request, context) => {
    const start = Date.now();
    const { getUser } = require('../shared/principal');
    const user = getUser(request); // present only if the submitter happens to be signed in

    let outcome = 'error';
    let kind = 'complaint';
    let hasEmail = false;
    let msgLen = 0;

    function trace(response) {
      context.log(JSON.stringify({
        event: 'complaint_submit',
        outcome,
        kind,
        hasEmail,
        msgLen,
        signedIn: !!user,
        ms: Date.now() - start,
      }));
      return response;
    }

    try {
      const body = await request.json().catch(() => ({}));

      // Honeypot: real users never populate this hidden field. Bots that fill
      // every field will — silently accept without sending anything.
      const website = typeof body.website === 'string' ? body.website.trim() : '';
      if (website) {
        outcome = 'honeypot';
        return trace({ status: 200, headers: { 'cache-control': 'private, no-store' }, jsonBody: { ok: true } });
      }

      kind = body.kind === 'suggestion' ? 'suggestion' : 'complaint';
      if (body.kind !== undefined && !VALID_KINDS.has(body.kind)) {
        outcome = 'invalid';
        return trace({ status: 400, jsonBody: { error: 'invalid', field: 'kind' } });
      }

      const name = typeof body.name === 'string' ? body.name.trim() : '';
      if (name.length > 100) {
        outcome = 'invalid';
        return trace({ status: 400, jsonBody: { error: 'invalid', field: 'name' } });
      }

      const email = typeof body.email === 'string' ? body.email.trim() : '';
      if (email) {
        if (email.length > 200 || !EMAIL_RE.test(email)) {
          outcome = 'invalid';
          return trace({ status: 400, jsonBody: { error: 'invalid', field: 'email' } });
        }
      }
      hasEmail = !!email;

      const message = typeof body.message === 'string' ? body.message.trim() : '';
      msgLen = message.length;
      if (message.length < 10 || message.length > 5000) {
        outcome = 'invalid';
        return trace({ status: 400, jsonBody: { error: 'invalid', field: 'message' } });
      }

      const { checkFeedbackLimit } = require('../shared/ratelimit');
      const ip = request.headers.get('x-forwarded-for');
      const rl = await checkFeedbackLimit({ ip });
      if (!rl.allowed) {
        outcome = 'rate_limited';
        return trace({
          status: 429,
          jsonBody: { error: 'rate_limited', retryAfterSeconds: rl.retryAfterSeconds },
        });
      }

      // Best-effort notify — a send failure must never turn into a 500 for the
      // submitter (same posture as custom-advisor.js's notifyCourseRequest use).
      let queued = true;
      try {
        const { notifyFeedback } = require('../shared/notify');
        const result = await notifyFeedback({ kind, name, email, message });
        if (result && result.sent === false) {
          queued = false;
          outcome = 'notify_skipped';
        } else {
          outcome = 'sent';
        }
      } catch (err) {
        queued = false;
        outcome = 'notify_failed';
        context.error('complaint notify failed', err);
      }

      return trace({
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: queued ? { ok: true } : { ok: true, queued: false },
      });
    } catch (err) {
      context.error('complaint error', err);
      outcome = 'error';
      return trace({ status: 500, jsonBody: { error: 'server_error' } });
    }
  },
});
