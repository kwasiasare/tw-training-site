'use strict';

// TW-140: Claude is served from Microsoft Foundry (direct API as fallback) with
// env-configurable models. All SDKs are replaced by fakes: no network, no keys.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const { loadHandler, makeRequest, makeContext, authUser } = require('./harness');

const SHARED_DIR = path.join(__dirname, '..', 'src', 'shared');
const ENV_KEYS = [
  'ANTHROPIC_API_KEY', 'ANTHROPIC_FOUNDRY_API_KEY', 'ANTHROPIC_FOUNDRY_RESOURCE',
  'ANTHROPIC_FOUNDRY_BASE_URL', 'CLAUDE_MODEL_SELECT', 'CLAUDE_MODEL_ANSWER', 'CLAUDE_MODEL_TUTOR',
];
const FRESH = ['claudeClient', 'chat', 'tutor', 'advisor', 'grader'].map((n) => path.join(SHARED_DIR, n + '.js'));

// Runs `run(ctx)` with fake direct + Foundry SDKs and a scrubbed env.
// ctx.calls = every messages.create() args; ctx.made = [{kind, opts}] constructions.
async function withFakes(env, createImpl, run) {
  const directId = require.resolve('@anthropic-ai/sdk', { paths: [SHARED_DIR] });
  const foundryId = require.resolve('@anthropic-ai/foundry-sdk', { paths: [SHARED_DIR] });
  const prevCache = new Map([directId, foundryId, ...FRESH].map((id) => [id, require.cache[id]]));
  const prevEnv = Object.fromEntries(ENV_KEYS.map((k) => [k, process.env[k]]));

  const ctx = { calls: [], made: [] };
  const make = (kind) => class {
    constructor(opts) {
      ctx.made.push({ kind, opts });
      this.messages = { create: async (args) => { ctx.calls.push({ kind, ...args }); return createImpl(args, kind); } };
    }
  };
  const put = (id, exports) => {
    require.cache[id] = { id, filename: id, loaded: true, exports, children: [], paths: [] };
  };
  put(directId, make('direct'));
  put(foundryId, make('foundry'));
  FRESH.forEach((id) => { delete require.cache[id]; });
  ENV_KEYS.forEach((k) => { delete process.env[k]; });
  Object.assign(process.env, env);

  try {
    return await run(ctx);
  } finally {
    for (const [id, mod] of prevCache) { if (mod) require.cache[id] = mod; else delete require.cache[id]; }
    FRESH.forEach((id) => { delete require.cache[id]; });
    ENV_KEYS.forEach((k) => { if (prevEnv[k] === undefined) delete process.env[k]; else process.env[k] = prevEnv[k]; });
  }
}

const text = (t) => ({ stop_reason: 'end_turn', content: [{ type: 'text', text: t }] });
const select = (status, ids = []) => text(JSON.stringify({ status, lesson_ids: ids, message: '' }));

// --- client selection ---

test('claudeClient: Foundry resource + key selects the Foundry client with resource and apiKey', async () => {
  await withFakes({ ANTHROPIC_FOUNDRY_RESOURCE: 'kasare-5989-resource', ANTHROPIC_FOUNDRY_API_KEY: 'k-f', ANTHROPIC_API_KEY: 'k-d' }, () => text('x'), (ctx) => {
    const cc = require(path.join(SHARED_DIR, 'claudeClient.js'));
    assert.equal(cc.claudeProvider(), 'foundry');
    const c1 = cc.getClaudeClient();
    assert.equal(cc.getClaudeClient(), c1, 'client is cached');
    assert.deepEqual(ctx.made, [{ kind: 'foundry', opts: { apiKey: 'k-f', resource: 'kasare-5989-resource' } }]);
  });
});

test('claudeClient: ANTHROPIC_FOUNDRY_BASE_URL is accepted instead of a resource name', async () => {
  await withFakes({ ANTHROPIC_FOUNDRY_BASE_URL: 'https://r.services.ai.azure.com/anthropic/', ANTHROPIC_FOUNDRY_API_KEY: 'k-f' }, () => text('x'), (ctx) => {
    require(path.join(SHARED_DIR, 'claudeClient.js')).getClaudeClient();
    assert.deepEqual(ctx.made, [{ kind: 'foundry', opts: { apiKey: 'k-f', baseURL: 'https://r.services.ai.azure.com/anthropic/' } }]);
  });
});

test('claudeClient: without Foundry config it falls back to the direct API key', async () => {
  await withFakes({ ANTHROPIC_API_KEY: 'k-d' }, () => text('x'), (ctx) => {
    const cc = require(path.join(SHARED_DIR, 'claudeClient.js'));
    assert.equal(cc.claudeProvider(), 'direct');
    cc.getClaudeClient();
    assert.deepEqual(ctx.made, [{ kind: 'direct', opts: { apiKey: 'k-d' } }]);
  });
});

test('claudeClient: a Foundry resource without its key (or a key without an endpoint) does not select Foundry', async () => {
  await withFakes({ ANTHROPIC_FOUNDRY_RESOURCE: 'r', ANTHROPIC_API_KEY: 'k-d' }, () => text('x'), () => {
    assert.equal(require(path.join(SHARED_DIR, 'claudeClient.js')).claudeProvider(), 'direct');
  });
  await withFakes({ ANTHROPIC_FOUNDRY_API_KEY: 'k-f' }, () => text('x'), () => {
    assert.equal(require(path.join(SHARED_DIR, 'claudeClient.js')).claudeProvider(), null);
  });
});

test('claudeClient: init log names the provider and any missing Foundry setting, and leaks no values', async () => {
  const captured = [];
  const prevLog = console.log;
  const prevWarn = console.warn;
  console.log = (line) => captured.push(['log', line]);
  console.warn = (line) => captured.push(['warn', line]);
  try {
    // Fully configured Foundry: one info line, provider only.
    await withFakes({ ANTHROPIC_FOUNDRY_RESOURCE: 'kasare-5989-resource', ANTHROPIC_FOUNDRY_API_KEY: 'super-secret-value' }, () => text('x'), (ctx) => {
      const cc = require(path.join(SHARED_DIR, 'claudeClient.js'));
      cc.getClaudeClient();
      cc.getClaudeClient(); // cached: no second line
      assert.equal(captured.length, 1);
      assert.equal(captured[0][0], 'log');
      assert.deepEqual(JSON.parse(captured[0][1]), { event: 'claude_client_init', provider: 'foundry' });
    });
    captured.length = 0;
    // Half-configured Foundry (resource, no key) falling back to direct: a
    // warning naming the missing setting, with neither key value present.
    await withFakes({ ANTHROPIC_FOUNDRY_RESOURCE: 'kasare-5989-resource', ANTHROPIC_API_KEY: 'direct-secret-value' }, () => text('x'), () => {
      require(path.join(SHARED_DIR, 'claudeClient.js')).getClaudeClient();
      assert.equal(captured.length, 1);
      assert.equal(captured[0][0], 'warn');
      assert.deepEqual(JSON.parse(captured[0][1]), {
        event: 'claude_client_init', provider: 'direct', foundryMissing: ['ANTHROPIC_FOUNDRY_API_KEY'],
      });
      assert.doesNotMatch(captured[0][1], /secret-value/);
    });
  } finally {
    console.log = prevLog;
    console.warn = prevWarn;
  }
});

test('claudeClient: no configuration throws a clear error that leaks no values', async () => {
  await withFakes({ ANTHROPIC_FOUNDRY_API_KEY: 'super-secret-value' }, () => text('x'), () => {
    const { getClaudeClient } = require(path.join(SHARED_DIR, 'claudeClient.js'));
    assert.throws(getClaudeClient, (err) => {
      assert.match(err.message, /not configured/i);
      assert.match(err.message, /ANTHROPIC_FOUNDRY_RESOURCE/);
      assert.doesNotMatch(err.message, /super-secret-value/);
      return true;
    });
  });
});

// --- model resolution ---

test('claudeClient: model helpers default to today\'s models and honour env overrides', async () => {
  await withFakes({}, () => text('x'), () => {
    const cc = require(path.join(SHARED_DIR, 'claudeClient.js'));
    assert.equal(cc.selectModel(), 'claude-haiku-4-5');
    assert.equal(cc.answerModel(), 'claude-sonnet-5');
    assert.equal(cc.tutorModel(), 'claude-opus-4-8');
    process.env.CLAUDE_MODEL_SELECT = 'dep-select';
    process.env.CLAUDE_MODEL_ANSWER = 'dep-answer';
    process.env.CLAUDE_MODEL_TUTOR = 'dep-tutor';
    assert.equal(cc.selectModel(), 'dep-select');
    assert.equal(cc.answerModel(), 'dep-answer');
    assert.equal(cc.tutorModel(), 'dep-tutor');
  });
});

test('models: chat Stage 1 / Stage 2 and tutor / advisor / grader send the env-configured deployment names via the Foundry client', async () => {
  const env = {
    ANTHROPIC_FOUNDRY_RESOURCE: 'r', ANTHROPIC_FOUNDRY_API_KEY: 'k',
    CLAUDE_MODEL_SELECT: 'dep-select', CLAUDE_MODEL_ANSWER: 'dep-answer', CLAUDE_MODEL_TUTOR: 'dep-tutor',
  };
  await withFakes(env, (args) => (args.system && String(args.system[0] && args.system[0].text).includes('retrieval step')
    ? select('ok', ['x']) : text('{"verdict":"ok"}')), async (ctx) => {
    const chat = require(path.join(SHARED_DIR, 'chat.js'));
    const msgs = [{ role: 'user', content: 'q' }];
    await chat.selectLessons({ messages: msgs });
    await chat.answerCourseQuestion({ lessons: [], messages: msgs });
    await chat.answerSiteHelpQuestion({ messages: msgs });
    await require(path.join(SHARED_DIR, 'tutor.js')).answerLessonQuestion({
      lesson: { title: 'T', objectives: [], body: 'b' }, courseTitle: 'C', messages: msgs,
    });
    assert.deepEqual(ctx.calls.map((c) => [c.kind, c.model]), [
      ['foundry', 'dep-select'], ['foundry', 'dep-answer'], ['foundry', 'dep-answer'], ['foundry', 'dep-tutor'],
    ]);
  });
});

// --- grounding is unchanged (real chat.js pipeline behind the real handler) ---

// The harness stubs shared/chat.js; drop that stub so the handler's lazy
// require() loads the REAL chat.js (against the harness's lessons stub and the
// fake SDKs). Everything below Stage 1 / Stage 2 is then production code.
function realChatHandler(lessonsById) {
  const h = loadHandler('chat', 'chat', {
    ratelimit: { checkChatLimits: async () => ({ allowed: true }) },
    lessons: { getLesson: (id) => lessonsById[id] || null },
  });
  delete require.cache[path.join(SHARED_DIR, 'chat.js')];
  return h;
}
const req = (content) => makeRequest({ method: 'POST', user: authUser(), body: { messages: [{ role: 'user', content }] } });

test('grounding: an off-topic question is declined after Stage 1 only, with no Stage 2 answer call', async () => {
  await withFakes({ ANTHROPIC_FOUNDRY_RESOURCE: 'r', ANTHROPIC_FOUNDRY_API_KEY: 'k' }, () => select('off_topic'), async (ctx) => {
    const res = await realChatHandler({})(req('Who won the football match last night?'), makeContext());
    assert.equal(res.status, 200);
    assert.match(res.jsonBody.reply, /questions about our courses/i);
    assert.deepEqual(res.jsonBody.lessons, []);
    assert.equal(ctx.calls.length, 1, 'only the Stage 1 classifier ran');
    assert.ok(!ctx.calls.some((c) => typeof c.system === 'string'), 'no Stage 2 (string-system) call was made');
  });
});

test('grounding: Stage 2 receives only the selected lesson text, never other lessons', async () => {
  const lessons = {
    'a-l01': { course: 'course-a', title: 'Kubernetes basics', objectives: ['pods'], body: 'ALPHA-BODY pods and nodes' },
    'b-l01': { course: 'course-b', title: 'Unrelated', objectives: [], body: 'BRAVO-BODY should never be sent' },
  };
  await withFakes({ ANTHROPIC_FOUNDRY_RESOURCE: 'r', ANTHROPIC_FOUNDRY_API_KEY: 'k' },
    (args) => (typeof args.system === 'string' ? text('Kubernetes is covered in course-a.') : select('ok', ['a-l01', 'ghost-id'])),
    async (ctx) => {
      const res = await realChatHandler(lessons)(req('Which course covers Kubernetes?'), makeContext());
      assert.equal(res.status, 200);
      assert.deepEqual(res.jsonBody.lessons, [{ id: 'a-l01', title: 'Kubernetes basics', course: 'course-a' }]);
      const stage2 = ctx.calls.filter((c) => typeof c.system === 'string');
      assert.equal(stage2.length, 1);
      assert.match(stage2[0].system, /ALPHA-BODY/);
      assert.doesNotMatch(stage2[0].system, /BRAVO-BODY/);
      assert.deepEqual(stage2[0].output_config, { effort: 'low' }, 'effort is preserved');
    });
});

test('grounding: a site_help question is answered from the FAQ block only, with no lesson material', async () => {
  await withFakes({ ANTHROPIC_FOUNDRY_RESOURCE: 'r', ANTHROPIC_FOUNDRY_API_KEY: 'k' },
    (args) => (Array.isArray(args.system) && args.system[0].text.includes('retrieval step')
      ? select('site_help') : text('Certificates are earned by completing every lesson.')),
    async (ctx) => {
      const res = await realChatHandler({ 'a-l01': { course: 'c', title: 't', objectives: [], body: 'ALPHA-BODY' } })(
        req('How do certificates work?'), makeContext());
      assert.equal(res.status, 200);
      assert.deepEqual(res.jsonBody.lessons, []);
      const answer = ctx.calls[1];
      const sys = JSON.stringify(answer.system);
      assert.match(sys, /FAQ/);
      assert.doesNotMatch(sys, /ALPHA-BODY/);
    });
});
