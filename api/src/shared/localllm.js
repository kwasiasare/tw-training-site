'use strict';

// Gateway client for the self-hosted "local LLM platform" (RAG over ingested
// course content, reachable over Tailscale). This is a FALLBACK-FIRST design:
// chat.js only calls answerViaGateway() when isGatewayConfigured() is true, and
// treats ANY failure here (bad config, network blip, timeout, malformed reply)
// as a signal to fall straight back to the existing Anthropic pipeline in
// shared/chat.js — so a flaky or unreachable gateway must never surface an
// error to the student, only a slightly slower/less-grounded reply. Never log
// LOCAL_LLM_GATEWAY_KEY or the student's question text from this module or its
// callers.
//
// Contract (server-side, already implemented on the gateway):
//   POST {LOCAL_LLM_GATEWAY_URL}/v1/chat
//   Authorization: Bearer {LOCAL_LLM_GATEWAY_KEY}
//   Body: { messages: [{role:'user'|'assistant', content}...], collection, k, tier }
//     (last message must be role 'user')
//   200 -> { app, reply, sources }
//   non-200 -> { detail }

const DEFAULT_COLLECTION = 'training-lesson-content';
const DEFAULT_TIER = 'cloud';
// Azure SWA managed functions have a hard 45s execution ceiling. This gateway
// call must leave enough headroom for the Anthropic fallback path to still
// complete within that ceiling if the gateway fails, so keep this well under
// 45s — 15s gateway + fallback Anthropic call fits comfortably.
const DEFAULT_TIMEOUT_MS = 15000;
const DEFAULT_K = 5;
const MIN_K = 1;
const MAX_K = 20;

// True only when both pieces of config needed to reach the gateway are present
// — callers use this to decide whether to attempt the gateway at all, so a
// half-configured environment (e.g. URL set, key forgotten) degrades to the
// existing Anthropic-only path rather than throwing.
function isGatewayConfigured() {
  return Boolean(process.env.LOCAL_LLM_GATEWAY_URL && process.env.LOCAL_LLM_GATEWAY_KEY);
}

// Join a base URL and a path with exactly one slash between them, regardless
// of whether the configured base already ends in '/'.
function joinUrl(base, path) {
  return `${base.replace(/\/+$/, '')}${path}`;
}

function gatewayError(message, code) {
  const err = new Error(message);
  err.code = code;
  return err;
}

// Resolve the retrieval `k` (number of chunks) to send to the gateway. Reads
// LOCAL_LLM_CHAT_K, clamped to [MIN_K, MAX_K]; missing/non-numeric values fall
// back to DEFAULT_K.
function resolveChatK() {
  const raw = process.env.LOCAL_LLM_CHAT_K;
  const n = Number(raw);
  if (!raw || !Number.isFinite(n)) return DEFAULT_K;
  return Math.min(MAX_K, Math.max(MIN_K, Math.trunc(n)));
}

// Answer a question via the local LLM gateway's RAG pipeline. `messages` is the
// already-normalized conversation (see shared/tutor.js normalizeMessages),
// ending on a 'user' turn. Returns { reply, sources } (sources is [] when the
// gateway didn't include any) or throws an Error with `.code` in
// {'gateway_timeout','gateway_http','gateway_bad_reply','gateway_network'} —
// callers should treat all of these as "fall back to Anthropic," never as a
// student-facing error.
async function answerViaGateway({ messages }) {
  const baseUrl = process.env.LOCAL_LLM_GATEWAY_URL;
  const key = process.env.LOCAL_LLM_GATEWAY_KEY;
  const url = joinUrl(baseUrl, '/v1/chat');
  const timeoutMs = Number(process.env.LOCAL_LLM_TIMEOUT_MS) || DEFAULT_TIMEOUT_MS;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  let res;
  let parsed;
  try {
    try {
      res = await fetch(url, {
        method: 'POST',
        headers: {
          authorization: `Bearer ${key}`,
          'content-type': 'application/json',
        },
        body: JSON.stringify({
          messages,
          collection: process.env.LOCAL_LLM_CHAT_COLLECTION || DEFAULT_COLLECTION,
          k: resolveChatK(),
          tier: process.env.LOCAL_LLM_CHAT_TIER || DEFAULT_TIER,
        }),
        signal: controller.signal,
      });
    } catch (err) {
      if (err && err.name === 'AbortError') {
        throw gatewayError(`local LLM gateway timed out after ${timeoutMs}ms`, 'gateway_timeout');
      }
      throw gatewayError(`local LLM gateway request failed: ${err && err.message}`, 'gateway_network');
    }

    if (!res.ok) {
      throw gatewayError(`local LLM gateway returned HTTP ${res.status}`, 'gateway_http');
    }

    try {
      parsed = await res.json();
    } catch (err) {
      if (err && err.name === 'AbortError') {
        throw gatewayError(`local LLM gateway timed out after ${timeoutMs}ms`, 'gateway_timeout');
      }
      throw gatewayError('local LLM gateway returned a non-JSON response', 'gateway_bad_reply');
    }
  } finally {
    // Stay armed until the body has been fully read — a gateway that returns
    // 200 headers then stalls the body must still be caught by the timeout,
    // so don't disarm the AbortController until res.json() has settled.
    clearTimeout(timer);
  }

  const reply = parsed && typeof parsed.reply === 'string' ? parsed.reply.trim() : '';
  if (!reply) {
    throw gatewayError('local LLM gateway returned an empty reply', 'gateway_bad_reply');
  }

  const sources = parsed && Array.isArray(parsed.sources) ? parsed.sources : [];

  return { reply, sources };
}

module.exports = { isGatewayConfigured, answerViaGateway };
