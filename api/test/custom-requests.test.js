'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, makeContainer, authUser, adminUser } = require('./harness');

function handler(container) {
  return loadHandler('custom-requests', 'custom-requests', { cosmosContainer: container || makeContainer() });
}

test('custom-requests: anonymous request returns 401', async () => {
  const res = await handler()(makeRequest({ method: 'GET' }), makeContext());
  assert.equal(res.status, 401);
});

test('custom-requests: a non-admin authenticated user is forbidden (403)', async () => {
  const res = await handler()(makeRequest({ method: 'GET', user: authUser() }), makeContext());
  assert.equal(res.status, 403);
  assert.equal(res.jsonBody.error, 'forbidden');
});

test('custom-requests: admin gets the request list (newest first, status mapped)', async () => {
  const rows = [
    {
      type: 'advisor', userId: 'u1', userDetails: 'maame@x', createdAt: '2026-06-19T10:00:00Z',
      questionnaire: { targetOutcome: 'become a digital marketer' },
      analysis: { recommendedRole: 'Digital Marketer', targetRoles: [{ role: 'Digital Marketer' }] },
      outcome: { type: 'generating' },
    },
    { type: 'generationRequest', userId: 'u1', status: 'queued' },
    {
      type: 'advisor', userId: 'u2', userDetails: 'kwasi@x', createdAt: '2026-06-20T10:00:00Z',
      questionnaire: { targetOutcome: 'AI developer job' },
      analysis: { recommendedRole: 'AI Application Developer', targetRoles: [] },
      outcome: { type: 'matched', courseSlug: 'ai-app-developer-2026' },
    },
  ];
  const container = makeContainer({ queryResult: rows });
  const res = await handler(container)(makeRequest({ method: 'GET', user: adminUser() }), makeContext());

  assert.equal(res.status, 200);
  const reqs = res.jsonBody.requests;
  assert.equal(reqs.length, 2, 'one row per advisor submission');
  // Newest first.
  assert.equal(reqs[0].user, 'kwasi@x');
  assert.equal(reqs[0].status, 'matched');
  assert.equal(reqs[0].course, 'ai-app-developer-2026');
  // Queued generation status is surfaced from the generationRequest.
  assert.equal(reqs[1].user, 'maame@x');
  assert.equal(reqs[1].status, 'queued');
  assert.equal(reqs[1].recommendedRole, 'Digital Marketer');
});

test('custom-requests: falls back to the email from another doc when the advisor doc lacks it', async () => {
  const rows = [
    { type: 'advisor', userId: 'u9', createdAt: '2026-06-19T10:00:00Z', analysis: {}, outcome: { type: 'generating' } },
    { type: 'profile', userId: 'u9', email: 'legacy@example.com' },
  ];
  const container = makeContainer({ queryResult: rows });
  const res = await handler(container)(makeRequest({ method: 'GET', user: adminUser() }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.requests[0].user, 'legacy@example.com', 'email pulled from the profile doc');
});
