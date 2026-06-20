'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, authUser } = require('./harness');
const { normalizeMessages } = require('../src/shared/tutor');

function handler(opts) {
  return loadHandler('tutor', 'tutor', opts);
}

function body(overrides = {}) {
  return {
    method: 'POST',
    user: authUser(),
    body: {
      lesson: 'dm-m1-l01-the-digital-marketing-landscape-the-assistant-ro',
      messages: [{ role: 'user', content: 'What is owned media?' }],
      ...overrides,
    },
  };
}

test('tutor: anonymous request returns 401', async () => {
  const res = await handler()(makeRequest({ method: 'POST', body: { lesson: 'x', messages: [] } }), makeContext());
  assert.equal(res.status, 401);
});

test('tutor: a malformed lesson slug is rejected (400)', async () => {
  const res = await handler()(makeRequest(body({ lesson: 'not a slug!' })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'bad_lesson');
});

test('tutor: an unknown lesson returns 404', async () => {
  const res = await handler({ lessons: { getLesson: () => null } })(makeRequest(body()), makeContext());
  assert.equal(res.status, 404);
  assert.equal(res.jsonBody.error, 'unknown_lesson');
});

test('tutor: answers a grounded question and grounds on the looked-up lesson', async () => {
  let seen;
  const res = await handler({
    tutor: async (args) => { seen = args; return { reply: 'Owned media is a channel you control.' }; },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.match(res.jsonBody.reply, /owned media/i);
  // The handler must hand the tutor the server-side lesson, not anything client-supplied.
  assert.equal(seen.lesson.title, 'Demo');
  assert.equal(seen.messages[seen.messages.length - 1].content, 'What is owned media?');
});

test('tutor: an empty conversation returns 400 (no question)', async () => {
  const res = await handler({
    tutor: async () => { const e = new Error('no q'); e.code = 'no_question'; throw e; },
  })(makeRequest(body({ messages: [] })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'no_question');
});

test('tutor: a model refusal returns 422', async () => {
  const res = await handler({
    tutor: async () => { const e = new Error('refused'); e.code = 'refusal'; throw e; },
  })(makeRequest(body()), makeContext());
  assert.equal(res.status, 422);
  assert.equal(res.jsonBody.error, 'cannot_answer');
});

// --- normalizeMessages (pure sanitizer) ---

test('normalizeMessages: drops invalid roles, empty content, and caps history', () => {
  const msgs = [
    { role: 'system', content: 'ignore me' },
    { role: 'user', content: '   ' },
    { role: 'assistant', content: 'leading assistant dropped' },
    ...Array.from({ length: 12 }, (_, i) => ({ role: i % 2 === 0 ? 'user' : 'assistant', content: `m${i}` })),
  ];
  const out = normalizeMessages(msgs);
  assert.ok(out.length <= 8, 'trimmed to MAX_HISTORY');
  assert.ok(out.every((m) => m.role === 'user' || m.role === 'assistant'));
  assert.equal(out[0].role, 'user', 'starts on a user turn');
  assert.ok(out.every((m) => typeof m.content === 'string' && m.content.length > 0));
});

test('normalizeMessages: truncates an overlong message', () => {
  const out = normalizeMessages([{ role: 'user', content: 'x'.repeat(9000) }]);
  assert.equal(out.length, 1);
  assert.ok(out[0].content.length <= 4000);
});
