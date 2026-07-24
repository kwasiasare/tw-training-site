const { app } = require('@azure/functions');

// GET /api/video?lesson=<slug> -> { url, expiresIn }
// Mints a short-lived (1h) presigned R2 URL for a lesson's video, enforcing the
// same hybrid access gate as the lesson pages: the first two lessons of each
// course are open to anyone; every other lesson requires an authenticated user.
//
// The object key is derived authoritatively from the lesson slug (`<slug>.mp4`,
// the project-wide naming convention) — the client never supplies a file path,
// so there is no way to request another lesson's video by tampering with input.
//
// Route is declared `anonymous` in staticwebapp.config.json so preview videos
// work signed-out; authorization for gated lessons is enforced here.

// First two lessons of each course — mirrors the free-preview route rules in
// staticwebapp.config.json. Keep these two lists in sync.
const FREE_PREVIEW = new Set([
  'aad-m1-l01-python-essentials-for-ai-developers',
  'aad-m1-l02-calling-your-first-llm-api',
  'age-m1-l01-calling-llm-apis-in-python-completions-chat-and-',
  'age-m1-l02-prompt-engineering-and-system-design-for-agent-b',
  'apm-m1-l01-how-modern-ai-works-a-no-math-mental-model-for-p',
  'apm-m1-l02-inside-llms-tokens-context-windows-and-how-they-',
  'cse-m1-l01-zero-trust-foundations-and-the-security-stack',
  'cse-m1-l02-architecting-conditional-access-policies',
  'dm-m1-l01-the-digital-marketing-landscape-the-assistant-ro',
  'dm-m1-l02-copywriting-that-converts-for-social-and-ads',
  'dsc-m1-l01-python-essentials-for-data-work',
  'dsc-m1-l02-loading-and-cleaning-data-with-pandas',
  'g1-l01-how-llms-behave',
  'g1-l02-where-llms-fail',
  'hd1-l01-how-a-computer-works',
  'hd1-l02-inside-the-pc',
  'ht1-l01-the-tier3-mindset-and-rca',
  'ht1-l02-advanced-windows-internals',
  'mle-m1-l01-python-for-ml-numpy-pandas-and-clean-code',
  'mle-m1-l02-linear-algebra-in-action-with-numpy',
  'mlo-m1-l01-setting-up-your-mlops-toolchain-and-workflow',
  'mlo-m1-l02-containerizing-a-machine-learning-model-with-doc',
  'vdi-m1-l01-what-is-vdi-and-euc',
  'vdi-m1-l02-vdi-architecture-building-blocks',
]);

const SLUG_RE = /^[a-z0-9-]+$/i;
const URL_TTL_SECONDS = 3600; // 1 hour

app.http('video', {
  methods: ['GET'],
  authLevel: 'anonymous',
  route: 'video',
  handler: async (request, context) => {
    const lesson = (request.query.get('lesson') || '').trim();
    if (!lesson || lesson.length > 80 || !SLUG_RE.test(lesson)) {
      return { status: 400, jsonBody: { error: 'bad_request' } };
    }

    // Gated lessons require a signed-in user. Return 403 (not 401) so the global
    // 401 -> /signin redirect override doesn't turn the player's fetch into HTML.
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    if (!FREE_PREVIEW.has(lesson) && !user) {
      return { status: 403, jsonBody: { error: 'login_required' } };
    }

    try {
      const { getSignedVideoUrl } = require('../shared/r2');
      const url = await getSignedVideoUrl(`${lesson}.mp4`, URL_TTL_SECONDS);
      return {
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: { url, expiresIn: URL_TTL_SECONDS },
      };
    } catch (err) {
      context.error('video sign error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});

// Exported for tests (kept in sync with the free-preview routes in
// staticwebapp.config.json — see free-preview-sync.test.js).
module.exports = { FREE_PREVIEW };
