'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const { getUser } = require(path.join(__dirname, '..', 'src', 'shared', 'principal.js'));

function reqWithPrincipal(principal) {
  const value = principal === null
    ? null
    : Buffer.from(JSON.stringify(principal)).toString('base64');
  return { headers: { get: (k) => (k.toLowerCase() === 'x-ms-client-principal' ? value : null) } };
}

test('getUser returns null when the header is absent', () => {
  assert.equal(getUser(reqWithPrincipal(null)), null);
});

test('getUser decodes a valid client principal', () => {
  const user = getUser(reqWithPrincipal({
    userId: 'abc',
    userDetails: 'bob@example.com',
    userRoles: ['authenticated', 'administrator'],
  }));
  assert.deepEqual(user, {
    userId: 'abc',
    userDetails: 'bob@example.com',
    roles: ['authenticated', 'administrator'],
  });
});

test('getUser defaults roles to an empty array', () => {
  const user = getUser(reqWithPrincipal({ userId: 'abc', userDetails: 'x' }));
  assert.deepEqual(user.roles, []);
});

test('getUser returns null when userId is missing', () => {
  assert.equal(getUser(reqWithPrincipal({ userDetails: 'no-id' })), null);
});

test('getUser returns null on non-base64 / malformed header', () => {
  const req = { headers: { get: () => 'not!base64!json' } };
  assert.equal(getUser(req), null);
});
