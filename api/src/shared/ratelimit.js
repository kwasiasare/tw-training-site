'use strict';

// Cosmos-backed sliding-window rate limiter for the chatbot (TW-117). Reuses the
// EXISTING `progress` container (db `training`, partition key /userId) — zero new
// Azure resources. No etag/optimistic-concurrency retry loop: slight over-admission
// under heavy parallel requests from the same key is acceptable for abuse control,
// not worth the complexity for v1.

const crypto = require('crypto');

// Pure logic, unit-testable: reads the doc, prunes hits older than windowMs,
// checks the count against max, and — only when still under the limit — appends
// `now` and upserts. A blocked check does NOT record a new hit (so a client
// hammering the endpoint past the limit doesn't keep pushing its own reset time
// out); the pruned list is still persisted either way so the doc never grows
// unbounded. `key` doubles as both the Cosmos item id and (since the container's
// partition key is /userId) the partition key value.
async function checkLimit(container, key, { max, windowMs, now = Date.now() }) {
  let doc = null;
  try {
    doc = (await container.item(key, key).read()).resource;
  } catch {
    doc = null; // not found (or any read error) — treat as no prior hits
  }

  const prevHits = doc && Array.isArray(doc.hits) ? doc.hits : [];
  const pruned = prevHits.filter((t) => now - t < windowMs);

  if (pruned.length >= max) {
    const oldest = Math.min(...pruned);
    const retryAfterSeconds = Math.max(1, Math.ceil((oldest + windowMs - now) / 1000));
    await container.items.upsert({
      id: key,
      userId: key,
      type: 'ratelimit',
      hits: pruned,
      updatedAt: new Date(now).toISOString(),
      ttl: 86400,
    });
    return { allowed: false, retryAfterSeconds };
  }

  const hits = [...pruned, now];
  await container.items.upsert({
    id: key,
    userId: key,
    type: 'ratelimit',
    hits,
    updatedAt: new Date(now).toISOString(),
    ttl: 86400,
  });
  return { allowed: true, retryAfterSeconds: 0 };
}

// Read a limit's max/window from env vars at call time (not module-load time),
// so tests can set process.env.* right before calling checkChatLimits with no
// need to bust the require cache. Defaults: 10/5min per user, 30/5min per IP.
function readLimits() {
  return {
    userMax: Number(process.env.CHAT_RL_USER_MAX) || 10,
    userWindowMs: Number(process.env.CHAT_RL_USER_WINDOW_MS) || 300000,
    ipMax: Number(process.env.CHAT_RL_IP_MAX) || 30,
    ipWindowMs: Number(process.env.CHAT_RL_IP_WINDOW_MS) || 300000,
  };
}

function userKey(userId) {
  return `rl:chat:u:${userId}`;
}

// IP extraction: first entry of a (possibly comma-separated) x-forwarded-for
// header, strip any :port suffix, lowercase. Returns null if there's nothing
// usable, so callers can skip the IP check entirely (fail-open by design — the
// per-user limit still applies, and this endpoint requires auth anyway).
function extractIp(rawHeader) {
  if (!rawHeader) return null;
  const first = String(rawHeader).split(',')[0].trim();
  if (!first) return null;
  return first.replace(/:\d+$/, '').toLowerCase();
}

// Store only a truncated sha256 hash of the IP — never raw IPs at rest.
function ipKey(rawHeader) {
  const ip = extractIp(rawHeader);
  if (!ip) return null;
  const hash = crypto.createHash('sha256').update(ip).digest('hex').slice(0, 32);
  return `rl:chat:ip:${hash}`;
}

// Same IP hashing as ipKey, but a distinct key prefix so the complaint form's
// bucket (TW-133) never collides with the chatbot's.
function feedbackIpKey(rawHeader) {
  const ip = extractIp(rawHeader);
  if (!ip) return null;
  const hash = crypto.createHash('sha256').update(ip).digest('hex').slice(0, 32);
  return `rl:feedback:ip:${hash}`;
}

function readFeedbackLimits() {
  return {
    ipMax: Number(process.env.FEEDBACK_RL_IP_MAX) || 5,
    ipWindowMs: Number(process.env.FEEDBACK_RL_IP_WINDOW_MS) || 3600000,
  };
}

// IP-only limiter for the anonymous complaints/suggestions endpoint (TW-133) —
// there is no logged-in user to key on. Fails open on any Cosmos error, same
// posture as checkChatLimits.
async function checkFeedbackLimit({ ip, now = Date.now() } = {}) {
  const ipK = ip ? feedbackIpKey(ip) : null;
  if (!ipK) return { allowed: true };

  const { ipMax, ipWindowMs } = readFeedbackLimits();

  let container;
  try {
    const { getContainer } = require('./cosmos');
    container = getContainer();
  } catch (err) {
    console.error('ratelimit: cosmos unavailable, failing open', err);
    return { allowed: true };
  }

  try {
    const result = await checkLimit(container, ipK, { max: ipMax, windowMs: ipWindowMs, now });
    if (!result.allowed) return { allowed: false, retryAfterSeconds: result.retryAfterSeconds };
    return { allowed: true };
  } catch (err) {
    console.error('ratelimit: cosmos call failed, failing open', err);
    return { allowed: true };
  }
}

// Composite: checks the per-user limit AND the per-IP limit, returns the first
// violation found ({allowed:false, scope:'user'|'ip', retryAfterSeconds}).
// `now` is optional and only meant for test injection of a fixed clock.
async function checkChatLimits({ userId, ip, now = Date.now() } = {}) {
  const { userMax, userWindowMs, ipMax, ipWindowMs } = readLimits();

  let container;
  try {
    // Lazy-require so a missing COSMOS_CONNECTION_STRING (or any load-time
    // failure) is caught right here rather than crashing module load.
    const { getContainer } = require('./cosmos');
    container = getContainer();
  } catch (err) {
    console.error('ratelimit: cosmos unavailable, failing open', err);
    return { allowed: true };
  }

  try {
    if (userId) {
      const result = await checkLimit(container, userKey(userId), { max: userMax, windowMs: userWindowMs, now });
      if (!result.allowed) return { allowed: false, scope: 'user', retryAfterSeconds: result.retryAfterSeconds };
    }
    const ipK = ip ? ipKey(ip) : null;
    if (ipK) {
      const result = await checkLimit(container, ipK, { max: ipMax, windowMs: ipWindowMs, now });
      if (!result.allowed) return { allowed: false, scope: 'ip', retryAfterSeconds: result.retryAfterSeconds };
    }
    return { allowed: true };
  } catch (err) {
    // Availability over strictness, matching this codebase's existing posture
    // (e.g. progress.js's best-effort reads) — a Cosmos hiccup should never be
    // the reason a legitimate student can't ask a question.
    console.error('ratelimit: cosmos call failed, failing open', err);
    return { allowed: true };
  }
}

module.exports = { checkLimit, checkChatLimits, checkFeedbackLimit };
