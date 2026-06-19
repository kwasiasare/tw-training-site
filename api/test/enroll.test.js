'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, makeContainer, authUser } = require('./harness');

function enrollHandler(container) {
  return loadHandler('enroll', 'enroll', { cosmosContainer: container });
}

test('enroll: anonymous request returns 401', async () => {
  const res = await enrollHandler(makeContainer())(
    makeRequest({ method: 'POST', body: { course: 'dami-ai-career' } }),
    makeContext(),
  );
  assert.equal(res.status, 401);
  assert.equal(res.jsonBody.error, 'not_authenticated');
});

test('enroll: missing course returns 400', async () => {
  const res = await enrollHandler(makeContainer())(
    makeRequest({ method: 'POST', user: authUser(), body: {} }),
    makeContext(),
  );
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'course_required');
});

test('enroll: rejects a non-slug course (injection guard) with 400', async () => {
  const container = makeContainer();
  const res = await enrollHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: '<img src=x onerror=alert(1)>' } }),
    makeContext(),
  );
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'invalid_course');
  assert.equal(container._calls.upserts.length, 0, 'must not store an invalid course');
});

test('enroll: accepts a mixed-case slug (e.g. kwasi-GenAI)', async () => {
  const container = makeContainer();
  const res = await enrollHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'kwasi-GenAI' } }),
    makeContext(),
  );
  assert.equal(res.jsonBody.ok, true);
  assert.equal(container._calls.upserts[0].course, 'kwasi-GenAI');
});

test('enroll: records an enrollment for the signed-in user', async () => {
  const container = makeContainer();
  const res = await enrollHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'dami-ai-career' } }),
    makeContext(),
  );
  assert.equal(res.jsonBody.ok, true);
  const doc = container._calls.upserts[0];
  assert.equal(doc.id, 'user-123:enroll:dami-ai-career');
  assert.equal(doc.userId, 'user-123');
  assert.equal(doc.type, 'enrollment');
  assert.equal(doc.course, 'dami-ai-career');
  assert.ok(doc.enrolledAt, 'stamps enrolledAt');
});

test('enroll: a Cosmos failure surfaces as 500', async () => {
  const container = makeContainer();
  container.items.upsert = async () => { throw new Error('cosmos down'); };
  const res = await enrollHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'x' } }),
    makeContext(),
  );
  assert.equal(res.status, 500);
  assert.equal(res.jsonBody.error, 'server_error');
});
