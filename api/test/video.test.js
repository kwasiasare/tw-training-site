'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, authUser } = require('./harness');

const FREE_SLUG = 'aad-m1-l01-python-essentials-for-ai-developers';
const GATED_SLUG = 'm3-l07-some-gated-lesson';

function videoHandler(signedUrl = 'https://signed.example/video.mp4?sig=abc') {
  const calls = [];
  const r2 = async (key, ttl) => { calls.push({ key, ttl }); return signedUrl; };
  const handler = loadHandler('video', 'video', { r2 });
  return { handler, calls };
}

test('video: rejects a missing lesson param with 400', async () => {
  const { handler } = videoHandler();
  const res = await handler(makeRequest({ query: {} }), makeContext());
  assert.equal(res.status, 400);
});

test('video: rejects an invalid slug with 400 (no signing)', async () => {
  const { handler, calls } = videoHandler();
  const res = await handler(makeRequest({ query: { lesson: '../../etc/passwd' } }), makeContext());
  assert.equal(res.status, 400);
  assert.equal(calls.length, 0);
});

test('video: rejects an over-long slug with 400', async () => {
  const { handler } = videoHandler();
  const res = await handler(makeRequest({ query: { lesson: 'a'.repeat(81) } }), makeContext());
  assert.equal(res.status, 400);
});

test('video: free-preview lesson is served to anonymous users', async () => {
  const { handler, calls } = videoHandler();
  const res = await handler(makeRequest({ query: { lesson: FREE_SLUG } }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.expiresIn, 3600);
  assert.match(res.jsonBody.url, /^https:\/\/signed\.example/);
  // Object key is derived server-side from the slug.
  assert.equal(calls[0].key, `${FREE_SLUG}.mp4`);
  assert.equal(calls[0].ttl, 3600);
  assert.equal(res.headers['cache-control'], 'private, no-store');
});

test('video: gated lesson returns 403 (not 401) for anonymous users', async () => {
  const { handler, calls } = videoHandler();
  const res = await handler(makeRequest({ query: { lesson: GATED_SLUG } }), makeContext());
  assert.equal(res.status, 403);
  assert.equal(res.jsonBody.error, 'login_required');
  assert.equal(calls.length, 0, 'must not sign a URL for a denied request');
});

test('video: gated lesson is served to an authenticated user', async () => {
  const { handler, calls } = videoHandler();
  const res = await handler(
    makeRequest({ query: { lesson: GATED_SLUG }, user: authUser() }),
    makeContext(),
  );
  assert.equal(res.status, 200);
  assert.equal(calls[0].key, `${GATED_SLUG}.mp4`);
});

test('video: signing failure surfaces as 500', async () => {
  const handler = loadHandler('video', 'video', { r2: async () => { throw new Error('boom'); } });
  const res = await handler(makeRequest({ query: { lesson: FREE_SLUG } }), makeContext());
  assert.equal(res.status, 500);
  assert.equal(res.jsonBody.error, 'server_error');
});
