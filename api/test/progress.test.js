'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, makeContainer, authUser } = require('./harness');

function progressHandler(container) {
  return loadHandler('progress', 'progress', { cosmosContainer: container });
}

test('progress: anonymous GET returns 401', async () => {
  const res = await progressHandler(makeContainer())(
    makeRequest({ method: 'GET' }),
    makeContext(),
  );
  assert.equal(res.status, 401);
});

test('progress: GET returns the user records', async () => {
  const records = [{ id: 'user-123:c:l', userId: 'user-123', type: 'progress', status: 'completed' }];
  const container = makeContainer({ queryResult: records });
  const res = await progressHandler(container)(
    makeRequest({ method: 'GET', user: authUser() }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.items, records);
  // Query is scoped to the user id.
  assert.equal(container._calls.queries[0].parameters[0].value, 'user-123');
});

test('progress: POST without course/lesson returns 400', async () => {
  const res = await progressHandler(makeContainer())(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'c' } }),
    makeContext(),
  );
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'course_and_lesson_required');
});

test('progress: POST upserts a progress record with a deterministic id', async () => {
  const container = makeContainer();
  const res = await progressHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'c1', lesson: 'l1' } }),
    makeContext(),
  );
  assert.equal(res.jsonBody.ok, true);
  const doc = container._calls.upserts[0];
  assert.equal(doc.id, 'user-123:c1:l1');
  assert.equal(doc.type, 'progress');
  assert.equal(doc.status, 'completed', 'defaults status to completed');
});

test('progress: POST merges a quiz score onto an existing record without clobbering status', async () => {
  const existing = {
    id: 'user-123:c1:l1', userId: 'user-123', type: 'progress',
    course: 'c1', lesson: 'l1', status: 'completed',
  };
  const container = makeContainer({ seed: [existing] });
  await progressHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'c1', lesson: 'l1', quizScore: 90 } }),
    makeContext(),
  );
  const doc = container._calls.upserts[0];
  assert.equal(doc.status, 'completed', 'keeps prior status when not supplied');
  assert.equal(doc.quizScore, 90, 'records the new quiz score');
});

test('progress: POST preserves an existing quiz score when only marking complete', async () => {
  const existing = {
    id: 'user-123:c1:l1', userId: 'user-123', type: 'progress',
    course: 'c1', lesson: 'l1', status: 'in-progress', quizScore: 75,
  };
  const container = makeContainer({ seed: [existing] });
  await progressHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'c1', lesson: 'l1', status: 'completed' } }),
    makeContext(),
  );
  const doc = container._calls.upserts[0];
  assert.equal(doc.status, 'completed');
  assert.equal(doc.quizScore, 75, 'preserves prior quiz score');
});
