'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, makeContainer, authUser, adminUser } = require('./harness');

function statsHandler(container) {
  return loadHandler('stats', 'stats', { cosmosContainer: container });
}

test('stats: anonymous request returns 401', async () => {
  const res = await statsHandler(makeContainer())(makeRequest({ method: 'GET' }), makeContext());
  assert.equal(res.status, 401);
});

test('stats: a non-admin authenticated user is forbidden (403)', async () => {
  const res = await statsHandler(makeContainer())(
    makeRequest({ method: 'GET', user: authUser() }),
    makeContext(),
  );
  assert.equal(res.status, 403);
  assert.equal(res.jsonBody.error, 'forbidden');
});

test('stats: an administrator receives aggregated analytics', async () => {
  const rows = [
    { type: 'progress', userId: 'u1', userDetails: 'u1@x', course: 'c1', lesson: 'l1', status: 'completed', quizScore: 80, updatedAt: '2026-01-02T00:00:00Z' },
    { type: 'progress', userId: 'u1', userDetails: 'u1@x', course: 'c1', lesson: 'l2', status: 'completed', quizScore: 100, updatedAt: '2026-01-03T00:00:00Z' },
    { type: 'progress', userId: 'u2', userDetails: 'u2@x', course: 'c1', lesson: 'l1', status: 'completed', updatedAt: '2026-01-04T00:00:00Z' },
    { type: 'progress', userId: 'u2', userDetails: 'u2@x', course: 'c2', lesson: 'l1', status: 'in-progress', updatedAt: '2026-01-05T00:00:00Z' },
    { type: 'enrollment', userId: 'u2', course: 'c2' },
  ];
  const container = makeContainer({ queryResult: rows });
  const res = await statsHandler(container)(
    makeRequest({ method: 'GET', user: adminUser() }),
    makeContext(),
  );
  const b = res.jsonBody;
  assert.equal(b.totals.users, 2);
  assert.equal(b.totals.enrollments, 1);
  assert.equal(b.totals.completions, 3);
  assert.equal(b.totals.avgQuiz, 90, 'averages only the scored completions');
  assert.equal(b.byCourse.c1, 3);
  // Most-completed lesson is c1/l1 (2 completions).
  assert.equal(b.topLessons[0].lesson, 'c1 / l1');
  assert.equal(b.topLessons[0].count, 2);
  // Recent is newest-first.
  assert.equal(b.recent[0].updatedAt, '2026-01-05T00:00:00Z');
});
