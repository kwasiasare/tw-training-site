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

test('GetRoles: grants administrator when userDetails matches an admin email', async () => {
  const res = await rolesHandler()(
    makeRequest({ method: 'POST', body: { userDetails: 'kasare@spreadcomgh.com' } }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, ['administrator']);
});

test('GetRoles: is case-insensitive on the email', async () => {
  const res = await rolesHandler()(
    makeRequest({ method: 'POST', body: { userDetails: 'KAsare@SpreadcomGH.com' } }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, ['administrator']);
});

test('GetRoles: matches an admin email found in claims', async () => {
  const res = await rolesHandler()(
    makeRequest({ method: 'POST', body: { claims: [{ typ: 'preferred_username', val: 'boss@example.com' }] } }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, ['administrator']);
});

test('GetRoles: returns no roles for a non-admin user', async () => {
  const res = await rolesHandler()(
    makeRequest({ method: 'POST', body: { userDetails: 'random@example.com' } }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.roles, []);
});

test('GetRoles: tolerates a missing/empty body', async () => {
  const res = await rolesHandler()(makeRequest({ method: 'POST' }), makeContext());
  assert.deepEqual(res.jsonBody.roles, []);
});
