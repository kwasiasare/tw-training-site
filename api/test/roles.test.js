'use strict';

const { test, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext } = require('./harness');

const ORIGINAL = process.env.ADMIN_EMAILS;

beforeEach(() => { process.env.ADMIN_EMAILS = 'kasare@spreadcomgh.com, boss@example.com'; });
afterEach(() => {
  if (ORIGINAL === undefined) delete process.env.ADMIN_EMAILS;
  else process.env.ADMIN_EMAILS = ORIGINAL;
});

function rolesHandler() {
  return loadHandler('getroles', 'GetRoles');
}

// The shape SWA's rolesSource invocation always sends (TW-108: payloads
// missing this shape are treated as probes and get no roles).
function swaPayload(overrides = {}) {
  return {
    identityProvider: 'entraExternalId',
    userId: 'a1b2c3d4e5f60718293a4b5c6d7e8f90',
    userDetails: 'someone@example.com',
    claims: [],
    ...overrides,
  };
}

test('GetRoles: grants administrator when userDetails matches an admin email', async () => {
  const res = await rolesHandler()(
    makeRequest({ method: 'POST', body: swaPayload({ userDetails: 'kasare@spreadcomgh.com' }) }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, ['administrator']);
});

test('GetRoles: is case-insensitive on the email', async () => {
  const res = await rolesHandler()(
    makeRequest({ method: 'POST', body: swaPayload({ userDetails: 'KAsare@SpreadcomGH.com' }) }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, ['administrator']);
});

test('GetRoles: matches an admin email found in claims', async () => {
  const res = await rolesHandler()(
    makeRequest({
      method: 'POST',
      body: swaPayload({ claims: [{ typ: 'preferred_username', val: 'boss@example.com' }] }),
    }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, ['administrator']);
});

test('GetRoles: returns no roles for a non-admin user', async () => {
  const res = await rolesHandler()(
    makeRequest({ method: 'POST', body: swaPayload({ userDetails: 'random@example.com' }) }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, []);
});

test('GetRoles: tolerates a missing/empty body', async () => {
  const res = await rolesHandler()(makeRequest({ method: 'POST' }), makeContext());
  assert.deepEqual(res.jsonBody.roles, []);
});

test('GetRoles: a bare enumeration probe (email only, no SWA identity shape) gets no roles', async () => {
  // TW-108: an anonymous caller posting just an admin email must learn nothing.
  const res = await rolesHandler()(
    makeRequest({ method: 'POST', body: { userDetails: 'kasare@spreadcomgh.com' } }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, []);
});

test('GetRoles: probe with claims but no identityProvider/userId gets no roles', async () => {
  const res = await rolesHandler()(
    makeRequest({
      method: 'POST',
      body: { claims: [{ typ: 'preferred_username', val: 'boss@example.com' }] },
    }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, []);
});
