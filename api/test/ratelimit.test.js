'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { makeContainer } = require('./harness');
const { checkLimit } = require('../src/shared/ratelimit');

// --- checkLimit (pure, container injected directly) ---

test('checkLimit: allows requests under the max', async () => {
  const container = makeContainer();
  const r1 = await checkLimit(container, 'rl:chat:u:alice', { max: 3, windowMs: 60000, now: 1000 });
  assert.equal(r1.allowed, true);
  const r2 = await checkLimit(container, 'rl:chat:u:alice', { max: 3, windowMs: 60000, now: 2000 });
  assert.equal(r2.allowed, true);
});

test('checkLimit: blocks at max+1 with a correct retryAfterSeconds', async () => {
  const container = makeContainer();
  await checkLimit(container, 'rl:chat:u:bob', { max: 2, windowMs: 60000, now: 1000 });
  await checkLimit(container, 'rl:chat:u:bob', { max: 2, windowMs: 60000, now: 2000 });
  const blocked = await checkLimit(container, 'rl:chat:u:bob', { max: 2, windowMs: 60000, now: 3000 });
  assert.equal(blocked.allowed, false);
  // oldest hit at t=1000, window 60000ms -> resets at t=61000; now=3000 -> 58s left.
  assert.equal(blocked.retryAfterSeconds, 58);
});

test('checkLimit: window slides — expired hits fall out and admit new requests', async () => {
  const container = makeContainer();
  await checkLimit(container, 'rl:chat:u:carol', { max: 2, windowMs: 1000, now: 0 });
  await checkLimit(container, 'rl:chat:u:carol', { max: 2, windowMs: 1000, now: 100 });
  const blocked = await checkLimit(container, 'rl:chat:u:carol', { max: 2, windowMs: 1000, now: 200 });
  assert.equal(blocked.allowed, false);

  // Advance past the window: both earlier hits (t=0, t=100) should have expired.
  const allowed = await checkLimit(container, 'rl:chat:u:carol', { max: 2, windowMs: 1000, now: 1300 });
  assert.equal(allowed.allowed, true);
});

test('checkLimit: prunes hits older than the window from the persisted doc', async () => {
  const container = makeContainer();
  await checkLimit(container, 'rl:chat:u:dave', { max: 5, windowMs: 1000, now: 0 });
  await checkLimit(container, 'rl:chat:u:dave', { max: 5, windowMs: 1000, now: 2000 });
  const doc = container._store.get('rl:chat:u:dave');
  assert.deepEqual(doc.hits, [2000], 'the t=0 hit should have been pruned from storage');
});

test('checkLimit: a blocked check does not record a new hit (so the doc does not grow unbounded)', async () => {
  const container = makeContainer();
  await checkLimit(container, 'rl:chat:u:frank', { max: 1, windowMs: 60000, now: 1000 });
  await checkLimit(container, 'rl:chat:u:frank', { max: 1, windowMs: 60000, now: 1001 }); // blocked
  await checkLimit(container, 'rl:chat:u:frank', { max: 1, windowMs: 60000, now: 1002 }); // blocked
  const doc = container._store.get('rl:chat:u:frank');
  assert.deepEqual(doc.hits, [1000]);
});

test('checkLimit: different keys (e.g. a user bucket and an IP bucket) are independent', async () => {
  const container = makeContainer();
  for (let i = 0; i < 3; i++) {
    await checkLimit(container, 'rl:chat:u:erin', { max: 3, windowMs: 60000, now: i * 10 });
  }
  const userBlocked = await checkLimit(container, 'rl:chat:u:erin', { max: 3, windowMs: 60000, now: 100 });
  assert.equal(userBlocked.allowed, false);

  const ipAllowed = await checkLimit(container, 'rl:chat:ip:abc123', { max: 3, windowMs: 60000, now: 100 });
  assert.equal(ipAllowed.allowed, true);
});

// --- checkChatLimits (composite: user + IP, reads Cosmos via shared/cosmos) ---
//
// checkChatLimits has no container param (it calls shared/cosmos.getContainer()
// internally), so these tests stub that module's require-cache entry directly —
// the same require-cache-injection technique harness.js uses for function tests,
// just applied to a shared module instead of a function module.

const cosmosId = require.resolve('../src/shared/cosmos');
const ratelimitId = require.resolve('../src/shared/ratelimit');

function freshRatelimit(getContainerImpl) {
  require.cache[cosmosId] = {
    id: cosmosId,
    filename: cosmosId,
    loaded: true,
    exports: { getContainer: getContainerImpl },
    children: [],
    paths: [],
  };
  delete require.cache[ratelimitId];
  return require('../src/shared/ratelimit');
}

test('checkChatLimits: missing IP header -> user-limit-only path still works', async () => {
  const container = makeContainer();
  const { checkChatLimits } = freshRatelimit(() => container);

  const r = await checkChatLimits({ userId: 'user-1', ip: undefined, now: 1000 });
  assert.equal(r.allowed, true);

  const ids = [...container._store.keys()];
  assert.ok(ids.some((id) => id.startsWith('rl:chat:u:')), 'expected a user-scoped doc');
  assert.ok(!ids.some((id) => id.startsWith('rl:chat:ip:')), 'no IP check should have run at all');
});

test('checkChatLimits: user and IP limits are independent of each other', async () => {
  const container = makeContainer();
  const { checkChatLimits } = freshRatelimit(() => container);
  process.env.CHAT_RL_USER_MAX = '1';
  process.env.CHAT_RL_IP_MAX = '5';
  try {
    const r1 = await checkChatLimits({ userId: 'user-2', ip: '203.0.113.7', now: 1000 });
    assert.equal(r1.allowed, true);
    // Second call from the SAME user but a DIFFERENT ip: user limit (max 1) trips.
    const r2 = await checkChatLimits({ userId: 'user-2', ip: '203.0.113.9', now: 1001 });
    assert.equal(r2.allowed, false);
    assert.equal(r2.scope, 'user');

    // A different user behind the SAME first ip is still allowed (independent
    // user bucket), and that ip's own bucket only has 1 hit so far (under its max of 5).
    const r3 = await checkChatLimits({ userId: 'user-3', ip: '203.0.113.7', now: 1002 });
    assert.equal(r3.allowed, true);
  } finally {
    delete process.env.CHAT_RL_USER_MAX;
    delete process.env.CHAT_RL_IP_MAX;
  }
});

test('checkChatLimits: x-forwarded-for with a port suffix and multiple hops uses only the first, stripped entry', async () => {
  const container = makeContainer();
  const { checkChatLimits } = freshRatelimit(() => container);
  process.env.CHAT_RL_IP_MAX = '1';
  try {
    await checkChatLimits({ userId: undefined, ip: '198.51.100.5:54321, 10.0.0.1', now: 1000 });
    const r2 = await checkChatLimits({ userId: undefined, ip: '198.51.100.5', now: 1001 });
    assert.equal(r2.allowed, false, 'the port-suffixed and bare forms should hash to the same IP key');
  } finally {
    delete process.env.CHAT_RL_IP_MAX;
  }
});

test('checkChatLimits: getContainer() throwing (Cosmos unreachable) fails open', async () => {
  const { checkChatLimits } = freshRatelimit(() => { throw new Error('cosmos unavailable'); });
  const r = await checkChatLimits({ userId: 'user-4', ip: '203.0.113.1', now: 1000 });
  assert.equal(r.allowed, true);
});

test('checkChatLimits: a Cosmos call failing mid-check fails open', async () => {
  const badContainer = {
    item: () => ({
      read: async () => { throw new Error('boom'); },
    }),
    items: {
      upsert: async () => { throw new Error('boom'); },
    },
  };
  const { checkChatLimits } = freshRatelimit(() => badContainer);
  const r = await checkChatLimits({ userId: 'user-5', ip: '203.0.113.2', now: 1000 });
  assert.equal(r.allowed, true);
});
