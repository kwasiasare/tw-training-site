'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, authUser } = require('./harness');
const { listLessonMeta } = require('../src/shared/lessons');

function handler(opts) {
  return loadHandler('chat', 'chat', opts);
}

function body(overrides = {}) {
  return {
    method: 'POST',
    user: authUser(),
    body: {
      messages: [{ role: 'user', content: 'Which course covers Kubernetes?' }],
      ...overrides,
    },
  };
}

test('chat: anonymous request returns 403 (not 401, to dodge the SWA signin redirect)', async () => {
  const res = await handler()(makeRequest({ method: 'POST', body: { messages: [] } }), makeContext());
  assert.equal(res.status, 403);
  assert.equal(res.jsonBody.error, 'login_required');
});

test('chat: empty messages returns 400 no_question', async () => {
  const res = await handler()(makeRequest(body({ messages: [] })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'no_question');
});

test('chat: a rate-limited request returns 429 and never spends a Claude call', async () => {
  let selectCalled = false;
  let answerCalled = false;
  const res = await handler({
    ratelimit: { checkChatLimits: async () => ({ allowed: false, scope: 'user', retryAfterSeconds: 42 }) },
    chat: {
      selectLessons: async () => { selectCalled = true; return { status: 'ok', lessonIds: [], message: '' }; },
      answerCourseQuestion: async () => { answerCalled = true; return { reply: 'x' }; },
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 429);
  assert.equal(res.jsonBody.error, 'rate_limited');
  assert.equal(res.jsonBody.retryAfterSeconds, 42);
  assert.equal(selectCalled, false, 'Stage 1 must not run once a rate limit is hit');
  assert.equal(answerCalled, false, 'Stage 2 must not run once a rate limit is hit');
});

// --- site_help routing (TW-118 Phase 2) ---

test('chat: a rate-limited request never spends a Claude call on the site_help path either', async () => {
  let siteHelpCalled = false;
  const res = await handler({
    ratelimit: { checkChatLimits: async () => ({ allowed: false, scope: 'ip', retryAfterSeconds: 10 }) },
    chat: {
      selectLessons: async () => ({ status: 'site_help', lessonIds: [], message: '' }),
      answerSiteHelpQuestion: async () => { siteHelpCalled = true; return { reply: 'x' }; },
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 429);
  assert.equal(siteHelpCalled, false, 'site-help Stage 2 must not run once a rate limit is hit');
});

test('chat: a site_help classification calls the FAQ-grounded Stage 2 and returns empty lessons', async () => {
  let seenMessages;
  const res = await handler({
    chat: {
      selectLessons: async () => ({ status: 'site_help', lessonIds: [], message: '' }),
      answerSiteHelpQuestion: async (args) => { seenMessages = args.messages; return { reply: 'Certificates are earned by completing every lesson in a course.' }; },
    },
  })(makeRequest(body({ messages: [{ role: 'user', content: 'How do certificates work?' }] })), makeContext());

  assert.equal(res.status, 200);
  assert.match(res.jsonBody.reply, /certificates/i);
  assert.deepEqual(res.jsonBody.lessons, []);
  assert.equal(seenMessages.length, 1);
  assert.equal(seenMessages[0].content, 'How do certificates work?');
});

test('chat: a site_help Stage 2 refusal returns 422 cannot_answer, same as the course path', async () => {
  const res = await handler({
    chat: {
      selectLessons: async () => ({ status: 'site_help', lessonIds: [], message: '' }),
      answerSiteHelpQuestion: async () => { const e = new Error('refused'); e.code = 'refusal'; throw e; },
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 422);
  assert.equal(res.jsonBody.error, 'cannot_answer');
});

test('chat: a mixed conversation (course question, then a site-help follow-up) routes each turn independently', async () => {
  const calls = [];
  const stubbedChat = {
    chat: {
      selectLessons: async ({ messages }) => {
        const last = messages[messages.length - 1].content;
        return /certificate/i.test(last)
          ? { status: 'site_help', lessonIds: [], message: '' }
          : { status: 'ok', lessonIds: ['demo-lesson'], message: '' };
      },
      answerCourseQuestion: async () => { calls.push('course'); return { reply: 'Kubernetes is covered in the MLOps track.' }; },
      answerSiteHelpQuestion: async () => { calls.push('site_help'); return { reply: 'Certificates are earned by completing every lesson.' }; },
    },
    lessons: {
      getLesson: (id) => (id === 'demo-lesson'
        ? { course: 'demo-course', title: 'Demo Lesson', objectives: [], body: 'demo body text' }
        : null),
    },
  };

  const res1 = await handler(stubbedChat)(makeRequest(body({ messages: [{ role: 'user', content: 'Which course covers Kubernetes?' }] })), makeContext());
  assert.equal(res1.status, 200);
  assert.match(res1.jsonBody.reply, /kubernetes/i);
  assert.equal(res1.jsonBody.lessons.length, 1);

  const res2 = await handler(stubbedChat)(makeRequest(body({ messages: [{ role: 'user', content: 'How do certificates work?' }] })), makeContext());
  assert.equal(res2.status, 200);
  assert.match(res2.jsonBody.reply, /certificates/i);
  assert.deepEqual(res2.jsonBody.lessons, []);

  assert.deepEqual(calls, ['course', 'site_help']);
});

test('chat: an off_topic classification returns the fixed reply without calling Stage 2', async () => {
  let answerCalled = false;
  const res = await handler({
    chat: {
      selectLessons: async () => ({ status: 'off_topic', lessonIds: [], message: '' }),
      answerCourseQuestion: async () => { answerCalled = true; return { reply: 'x' }; },
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.match(res.jsonBody.reply, /questions about our courses/i);
  assert.deepEqual(res.jsonBody.lessons, []);
  assert.equal(answerCalled, false, 'off_topic must short-circuit before Stage 2');
});

test('chat: a no_match classification returns the fixed reply without calling Stage 2', async () => {
  let answerCalled = false;
  const res = await handler({
    chat: {
      selectLessons: async () => ({ status: 'no_match', lessonIds: [], message: '' }),
      answerCourseQuestion: async () => { answerCalled = true; return { reply: 'x' }; },
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.match(res.jsonBody.reply, /couldn't find that/i);
  assert.equal(answerCalled, false);
});

test('chat: a clarify classification returns the selector\'s own message verbatim', async () => {
  const res = await handler({
    chat: {
      selectLessons: async () => ({ status: 'clarify', lessonIds: [], message: 'Which track — MLOps or ML Engineer?' }),
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.reply, 'Which track — MLOps or ML Engineer?');
});

test('chat: happy path grounds Stage 2 in the real server-fetched lesson, not client input', async () => {
  let seenLessons;
  const res = await handler({
    chat: {
      selectLessons: async () => ({ status: 'ok', lessonIds: ['demo-lesson'], message: '' }),
      answerCourseQuestion: async (args) => {
        seenLessons = args.lessons;
        return { reply: 'Kubernetes is covered in the MLOps track.' };
      },
    },
    lessons: {
      getLesson: (id) => (id === 'demo-lesson'
        ? { course: 'demo-course', title: 'Demo Lesson', objectives: ['obj1'], body: 'demo body text' }
        : null),
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.match(res.jsonBody.reply, /kubernetes/i);
  assert.deepEqual(res.jsonBody.lessons, [{ id: 'demo-lesson', title: 'Demo Lesson', course: 'demo-course' }]);
  // Stage 2 must have received the server-fetched lesson body/objectives — never
  // anything the client could have supplied (the client only ever sends `messages`).
  assert.equal(seenLessons.length, 1);
  assert.equal(seenLessons[0].title, 'Demo Lesson');
  assert.equal(seenLessons[0].body, 'demo body text');
});

test('chat: an "ok" classification whose lesson ids all fail validation falls back to no_match', async () => {
  const res = await handler({
    chat: {
      selectLessons: async () => ({ status: 'ok', lessonIds: [], message: '' }),
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.match(res.jsonBody.reply, /couldn't find that/i);
});

test('chat: a Stage 2 refusal returns 422 cannot_answer', async () => {
  const res = await handler({
    chat: {
      selectLessons: async () => ({ status: 'ok', lessonIds: ['demo-lesson'], message: '' }),
      answerCourseQuestion: async () => { const e = new Error('refused'); e.code = 'refusal'; throw e; },
    },
    lessons: {
      getLesson: () => ({ course: 'demo-course', title: 'Demo Lesson', objectives: [], body: 'demo body text' }),
    },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 422);
  assert.equal(res.jsonBody.error, 'cannot_answer');
});

// --- answerCourseQuestion() (api/src/shared/chat.js, TW-117) ---
//
// Stubs the '@anthropic-ai/sdk' module directly (same require.cache-swap
// technique harness.js uses for '@azure/functions') so this exercises the
// real Stage 2 logic in shared/chat.js rather than a test-side mock of it.

test('answerCourseQuestion: an empty/whitespace-only Stage 2 reply throws with err.code "refusal" (so the handler routes it to 422 cannot_answer, not a bare 500)', async () => {
  const path = require('path');
  const SHARED_DIR = path.join(__dirname, '..', 'src', 'shared');
  const chatSharedId = path.join(SHARED_DIR, 'chat.js');
  const sdkId = require.resolve('@anthropic-ai/sdk', { paths: [SHARED_DIR] });

  const prevSdkCache = require.cache[sdkId];
  const prevChatCache = require.cache[chatSharedId];
  const prevApiKey = process.env.ANTHROPIC_API_KEY;

  class FakeAnthropic {
    constructor() {
      this.messages = {
        create: async () => ({ stop_reason: 'end_turn', content: [{ type: 'text', text: '   ' }] }),
      };
    }
  }
  require.cache[sdkId] = {
    id: sdkId, filename: sdkId, loaded: true, exports: FakeAnthropic, children: [], paths: [],
  };
  delete require.cache[chatSharedId];
  process.env.ANTHROPIC_API_KEY = 'test-key';

  try {
    const { answerCourseQuestion } = require(chatSharedId);
    await assert.rejects(
      answerCourseQuestion({ lessons: [], messages: [{ role: 'user', content: 'hi' }] }),
      (err) => err.code === 'refusal',
    );
  } finally {
    if (prevSdkCache) require.cache[sdkId] = prevSdkCache; else delete require.cache[sdkId];
    if (prevChatCache) require.cache[chatSharedId] = prevChatCache; else delete require.cache[chatSharedId];
    if (prevApiKey === undefined) delete process.env.ANTHROPIC_API_KEY; else process.env.ANTHROPIC_API_KEY = prevApiKey;
  }
});

// --- answerSiteHelpQuestion() (api/src/shared/chat.js, TW-118 Phase 2) ---

function withFakeAnthropic(createImpl, run) {
  const path = require('path');
  const SHARED_DIR = path.join(__dirname, '..', 'src', 'shared');
  const chatSharedId = path.join(SHARED_DIR, 'chat.js');
  const sdkId = require.resolve('@anthropic-ai/sdk', { paths: [SHARED_DIR] });

  const prevSdkCache = require.cache[sdkId];
  const prevChatCache = require.cache[chatSharedId];
  const prevApiKey = process.env.ANTHROPIC_API_KEY;

  const seenCalls = [];
  class FakeAnthropic {
    constructor() {
      this.messages = { create: async (args) => { seenCalls.push(args); return createImpl(args); } };
    }
  }
  require.cache[sdkId] = {
    id: sdkId, filename: sdkId, loaded: true, exports: FakeAnthropic, children: [], paths: [],
  };
  delete require.cache[chatSharedId];
  process.env.ANTHROPIC_API_KEY = 'test-key';

  return Promise.resolve()
    .then(() => run(require(chatSharedId), seenCalls))
    .finally(() => {
      if (prevSdkCache) require.cache[sdkId] = prevSdkCache; else delete require.cache[sdkId];
      if (prevChatCache) require.cache[chatSharedId] = prevChatCache; else delete require.cache[chatSharedId];
      if (prevApiKey === undefined) delete process.env.ANTHROPIC_API_KEY; else process.env.ANTHROPIC_API_KEY = prevApiKey;
    });
}

test('answerSiteHelpQuestion: happy path grounds on the full FAQ via a cached system block and returns the trimmed reply', async () => {
  await withFakeAnthropic(
    () => ({ stop_reason: 'end_turn', content: [{ type: 'text', text: '  Certificates are earned by completing every lesson.  ' }] }),
    async (mod, seenCalls) => {
      const { reply } = await mod.answerSiteHelpQuestion({ messages: [{ role: 'user', content: 'How do certificates work?' }] });
      assert.equal(reply, 'Certificates are earned by completing every lesson.');
      assert.equal(seenCalls.length, 1);
      assert.equal(seenCalls[0].model, 'claude-sonnet-5');
      assert.deepEqual(seenCalls[0].output_config, { effort: 'low' });
      const systemBlocks = seenCalls[0].system;
      assert.ok(Array.isArray(systemBlocks) && systemBlocks.length === 2);
      const faqBlock = systemBlocks[1];
      assert.deepEqual(faqBlock.cache_control, { type: 'ephemeral' });
      const faqEntries = JSON.parse(faqBlock.text);
      assert.ok(Array.isArray(faqEntries) && faqEntries.length > 0);
      assert.ok(faqEntries.every((e) => e.id && e.topic && e.question && e.answer));
    },
  );
});

test('answerSiteHelpQuestion: an empty/whitespace-only reply throws with err.code "refusal"', async () => {
  await withFakeAnthropic(
    () => ({ stop_reason: 'end_turn', content: [{ type: 'text', text: '   ' }] }),
    async (mod) => {
      await assert.rejects(
        mod.answerSiteHelpQuestion({ messages: [{ role: 'user', content: 'hi' }] }),
        (err) => err.code === 'refusal',
      );
    },
  );
});

test('answerSiteHelpQuestion: a model refusal (stop_reason "refusal") throws with err.code "refusal"', async () => {
  await withFakeAnthropic(
    () => ({ stop_reason: 'refusal', content: [] }),
    async (mod) => {
      await assert.rejects(
        mod.answerSiteHelpQuestion({ messages: [{ role: 'user', content: 'hi' }] }),
        (err) => err.code === 'refusal',
      );
    },
  );
});

test('selectLessons: never sends output_config.effort — unsupported on the Haiku Stage-1 model and would break every classification call in production', async () => {
  await withFakeAnthropic(
    () => ({ content: [{ type: 'text', text: JSON.stringify({ status: 'no_match', lesson_ids: [], message: '' }) }] }),
    async (mod, seenCalls) => {
      await mod.selectLessons({ messages: [{ role: 'user', content: 'anything' }] });
      assert.equal(seenCalls.length, 1);
      assert.equal(seenCalls[0].model, 'claude-haiku-4-5');
      assert.equal(seenCalls[0].output_config && seenCalls[0].output_config.effort, undefined);
    },
  );
});

// --- selectLessons() site_help classification (api/src/shared/chat.js, TW-118 Phase 2) ---

test('selectLessons: a "site_help" status from the model is passed through with empty lessonIds', async () => {
  await withFakeAnthropic(
    () => ({ content: [{ type: 'text', text: JSON.stringify({ status: 'site_help', lesson_ids: [], message: '' }) }] }),
    async (mod) => {
      const result = await mod.selectLessons({ messages: [{ role: 'user', content: 'How do certificates work?' }] });
      assert.equal(result.status, 'site_help');
      assert.deepEqual(result.lessonIds, []);
    },
  );
});

test('selectLessons: a "site_help" status with (incorrectly) non-empty lesson_ids from the model still comes back with empty lessonIds', async () => {
  await withFakeAnthropic(
    () => ({ content: [{ type: 'text', text: JSON.stringify({ status: 'site_help', lesson_ids: ['some-lesson'], message: '' }) }] }),
    async (mod) => {
      const result = await mod.selectLessons({ messages: [{ role: 'user', content: 'How do certificates work?' }] });
      assert.equal(result.status, 'site_help');
      assert.deepEqual(result.lessonIds, [], 'site_help must never ground on lessons, regardless of what the model returned');
    },
  );
});

test('selectLessons: an unrecognized status string still degrades to no_match', async () => {
  await withFakeAnthropic(
    () => ({ content: [{ type: 'text', text: JSON.stringify({ status: 'not_a_real_status', lesson_ids: [], message: '' }) }] }),
    async (mod) => {
      const result = await mod.selectLessons({ messages: [{ role: 'user', content: 'anything' }] });
      assert.equal(result.status, 'no_match');
      assert.deepEqual(result.lessonIds, []);
    },
  );
});

test('selectLessons: the JSON-only fallback path (structured output rejected) still accepts "site_help"', async () => {
  await withFakeAnthropic(
    (args) => {
      if (args.output_config) {
        const e = new Error('output_config.format is not supported for this model');
        e.status = 400;
        throw e;
      }
      return { content: [{ type: 'text', text: JSON.stringify({ status: 'site_help', lesson_ids: [], message: '' }) }] };
    },
    async (mod, seenCalls) => {
      const result = await mod.selectLessons({ messages: [{ role: 'user', content: 'How do certificates work?' }] });
      assert.equal(result.status, 'site_help');
      assert.deepEqual(result.lessonIds, []);
      assert.equal(seenCalls.length, 2, 'structured-output attempt first, then the JSON-only fallback');
      assert.equal(seenCalls[1].output_config, undefined, 'fallback call must not resend output_config');
      assert.ok(
        seenCalls[1].system[0].text.includes('"status": "ok"|"site_help"'),
        'JSON-only suffix enum must include site_help',
      );
    },
  );
});

test('selectLessons: system prompt carries the lesson catalog and the FAQ topic list as two separate cached blocks', async () => {
  await withFakeAnthropic(
    () => ({ content: [{ type: 'text', text: JSON.stringify({ status: 'no_match', lesson_ids: [], message: '' }) }] }),
    async (mod, seenCalls) => {
      await mod.selectLessons({ messages: [{ role: 'user', content: 'anything' }] });
      const systemBlocks = seenCalls[0].system;
      assert.ok(Array.isArray(systemBlocks) && systemBlocks.length === 3, 'instructions + catalog block + FAQ topics block');
      const [, catalogBlock, faqTopicsBlock] = systemBlocks;
      assert.deepEqual(catalogBlock.cache_control, { type: 'ephemeral' });
      assert.deepEqual(faqTopicsBlock.cache_control, { type: 'ephemeral' });
      const topics = JSON.parse(faqTopicsBlock.text);
      assert.ok(Array.isArray(topics) && topics.length > 0);
      assert.ok(topics.every((t) => t.id && t.topic && t.question && !('answer' in t)), 'topic list must not carry answers');
    },
  );
});

// --- listLessonMeta() (api/src/shared/lessons.js, TW-117) ---

test('listLessonMeta: returns all 360 real lessons with id/course/title', () => {
  const meta = listLessonMeta();
  assert.equal(meta.length, 360);
  for (const m of meta) {
    assert.equal(typeof m.id, 'string');
    assert.equal(typeof m.course, 'string');
    assert.equal(typeof m.title, 'string');
    assert.ok(m.id.length > 0 && m.course.length > 0 && m.title.length > 0);
  }
  // Spot-check against the actual committed index rather than trusting the
  // derivation blindly.
  const idx = require('../src/shared/lessons.generated.json');
  assert.equal(Object.keys(idx).length, meta.length);
  const sampleId = Object.keys(idx)[0];
  const sampleMeta = meta.find((m) => m.id === sampleId);
  assert.ok(sampleMeta);
  assert.equal(sampleMeta.course, idx[sampleId].course);
  assert.equal(sampleMeta.title, idx[sampleId].title);
});
