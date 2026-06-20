'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, authUser } = require('./harness');

function handler(opts) {
  return loadHandler('grade', 'grade', opts);
}

function body(overrides = {}) {
  return {
    method: 'POST',
    user: authUser(),
    body: { lesson: 'demo-lesson', qIndex: 0, answer: 'my attempt at the answer', ...overrides },
  };
}

test('grade: anonymous request returns 401', async () => {
  const res = await handler()(makeRequest({ method: 'POST', body: {} }), makeContext());
  assert.equal(res.status, 401);
});

test('grade: malformed lesson slug returns 400', async () => {
  const res = await handler()(makeRequest(body({ lesson: 'bad slug!' })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'bad_lesson');
});

test('grade: missing answer returns 400', async () => {
  const res = await handler()(makeRequest(body({ answer: '   ' })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'answer_required');
});

test('grade: a non-integer/negative qIndex returns 400', async () => {
  const res = await handler()(makeRequest(body({ qIndex: -1 })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'bad_question');
});

test('grade: unknown lesson returns 404', async () => {
  const res = await handler({ lessons: { getLesson: () => null } })(makeRequest(body()), makeContext());
  assert.equal(res.status, 404);
  assert.equal(res.jsonBody.error, 'unknown_lesson');
});

test('grade: a qIndex past the quiz returns 404', async () => {
  const res = await handler()(makeRequest(body({ qIndex: 99 })), makeContext());
  assert.equal(res.status, 404);
  assert.equal(res.jsonBody.error, 'unknown_question');
});

test('grade: grading an MCQ (has options) is rejected as not gradable', async () => {
  const res = await handler()(makeRequest(body({ qIndex: 1 })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'not_gradable');
});

test('grade: grades an open answer against the server-side reference', async () => {
  let seen;
  const res = await handler({
    grader: async (args) => { seen = args; return { verdict: 'partial', score: 60, feedback: 'Close.' }; },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.verdict, 'partial');
  assert.equal(res.jsonBody.score, 60);
  // The reference answer must come from the server-side lesson, not the client.
  assert.equal(seen.referenceAnswer, 'the reference answer');
  assert.equal(seen.learnerAnswer, 'my attempt at the answer');
});

test('grade: a model refusal returns 422', async () => {
  const res = await handler({
    grader: async () => { const e = new Error('no'); e.code = 'refusal'; throw e; },
  })(makeRequest(body()), makeContext());
  assert.equal(res.status, 422);
  assert.equal(res.jsonBody.error, 'cannot_grade');
});
