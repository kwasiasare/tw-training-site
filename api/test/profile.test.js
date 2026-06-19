'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, makeContainer, authUser } = require('./harness');

function profileHandler(container) {
  return loadHandler('profile', 'profile', { cosmosContainer: container });
}

test('profile: anonymous request returns 401', async () => {
  const res = await profileHandler(makeContainer())(makeRequest({ method: 'GET' }), makeContext());
  assert.equal(res.status, 401);
});

test('profile: GET derives enrolled courses and completed counts', async () => {
  const rows = [
    { course: 'c1', type: 'progress', status: 'completed' },
    { course: 'c1', type: 'progress', status: 'completed' },
    { course: 'c1', type: 'progress', status: 'in-progress' },
    { course: 'c2', type: 'enrollment' },
  ];
  // GET issues a profile read() (missing -> null) then a query() for the rows.
  const container = makeContainer({ queryResult: rows });
  const res = await profileHandler(container)(
    makeRequest({ method: 'GET', user: authUser() }),
    makeContext(),
  );
  assert.equal(res.jsonBody.email, 'alice@example.com');
  assert.equal(res.jsonBody.displayName, '', 'no profile doc -> empty display name');
  const byCourse = Object.fromEntries(res.jsonBody.enrolledCourses.map((c) => [c.course, c.completed]));
  assert.deepEqual(byCourse, { c1: 2, c2: 0 });
});

test('profile: GET returns a saved display name', async () => {
  const profileDoc = { id: 'user-123:profile', userId: 'user-123', type: 'profile', displayName: 'Alice A' };
  const container = makeContainer({ seed: [profileDoc], queryResult: [] });
  const res = await profileHandler(container)(
    makeRequest({ method: 'GET', user: authUser() }),
    makeContext(),
  );
  assert.equal(res.jsonBody.displayName, 'Alice A');
});

test('profile: POST trims and upserts the display name', async () => {
  const container = makeContainer();
  const res = await profileHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { displayName: '  Alice  ' } }),
    makeContext(),
  );
  assert.equal(res.jsonBody.ok, true);
  assert.equal(res.jsonBody.displayName, 'Alice');
  assert.equal(container._calls.upserts[0].id, 'user-123:profile');
});

test('profile: POST caps display name at 60 characters', async () => {
  const container = makeContainer();
  const res = await profileHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { displayName: 'x'.repeat(100) } }),
    makeContext(),
  );
  assert.equal(res.jsonBody.displayName.length, 60);
});
