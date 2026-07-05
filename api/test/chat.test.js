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

// --- listLessonMeta() (api/src/shared/lessons.js, TW-117) ---

test('listLessonMeta: returns all 391 real lessons with id/course/title', () => {
  const meta = listLessonMeta();
  assert.equal(meta.length, 391);
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
