'use strict';

// Test harness for the SWA managed Azure Functions.
//
// Each function module registers its handler at require-time via
// `app.http(name, { handler })` from '@azure/functions', and pulls Cosmos/R2
// access from the shared modules. To unit/integration-test a handler in
// isolation we:
//   1. Inject a stub '@azure/functions' whose `app.http` captures the handler.
//   2. Inject stub '../shared/cosmos' and '../shared/r2' so no live Azure/R2
//      access happens (and tests control the fakes).
//   3. Use the REAL '../shared/principal' (pure header decoding) so auth is
//      exercised end-to-end from the x-ms-client-principal header.
// No production code is modified to support this (besides a test-only export on
// video.js for the free-preview sync check).

const path = require('path');

const API_ROOT = path.resolve(__dirname, '..');
const FUNCTIONS_DIR = path.join(API_ROOT, 'src', 'functions');
const SHARED_DIR = path.join(API_ROOT, 'src', 'shared');

function setCache(absId, exports) {
  require.cache[absId] = {
    id: absId,
    filename: absId,
    loaded: true,
    exports,
    children: [],
    paths: [],
  };
}

// Load a function module in isolation. Returns { handlers, exports } where
// `handlers` maps each registered name to its options object (incl. handler),
// and `exports` is the module's own exports (used by the sync test).
function loadFunction(name, { cosmosContainer, r2 } = {}) {
  const azFuncId = require.resolve('@azure/functions', { paths: [FUNCTIONS_DIR] });
  const cosmosId = path.join(SHARED_DIR, 'cosmos.js');
  const r2Id = path.join(SHARED_DIR, 'r2.js');
  const principalId = path.join(SHARED_DIR, 'principal.js');
  const fnId = path.join(FUNCTIONS_DIR, name + '.js');

  const handlers = {};
  setCache(azFuncId, { app: { http: (n, opts) => { handlers[n] = opts; } } });

  setCache(cosmosId, {
    getContainer: () => {
      if (!cosmosContainer) throw new Error('cosmos container not provided to loadFunction');
      return cosmosContainer;
    },
  });

  setCache(r2Id, {
    getSignedVideoUrl: r2 || (async () => { throw new Error('r2 not stubbed for this test'); }),
  });

  // Real principal + fresh function module each load.
  delete require.cache[principalId];
  delete require.cache[fnId];
  const exports = require(fnId);

  return { handlers, exports };
}

// Convenience: load and return a single handler by registered name.
function loadHandler(moduleName, registeredName, opts) {
  const { handlers } = loadFunction(moduleName, opts);
  const reg = handlers[registeredName];
  if (!reg) throw new Error(`function '${registeredName}' was not registered by ${moduleName}.js`);
  return reg.handler;
}

// Build a fake Azure Functions HttpRequest. `user`, when given, is base64-encoded
// into the x-ms-client-principal header exactly as SWA injects it.
function makeRequest({ method = 'GET', headers = {}, query = {}, body, user } = {}) {
  const h = new Map(Object.entries(headers).map(([k, v]) => [k.toLowerCase(), v]));
  if (user) {
    h.set('x-ms-client-principal', Buffer.from(JSON.stringify(user)).toString('base64'));
  }
  const q = new Map(Object.entries(query));
  const hasBody = body !== undefined;
  return {
    method,
    headers: { get: (k) => (h.has(String(k).toLowerCase()) ? h.get(String(k).toLowerCase()) : null) },
    query: { get: (k) => (q.has(k) ? q.get(k) : null) },
    json: async () => {
      if (!hasBody) throw new Error('no JSON body');
      return body;
    },
  };
}

// Silent context (handlers call context.error on failures).
function makeContext() {
  return { error: () => {}, log: () => {}, warn: () => {} };
}

// SWA client-principal shapes for the common cases.
const anonUser = undefined;
function authUser(overrides = {}) {
  return { userId: 'user-123', userDetails: 'alice@example.com', userRoles: ['authenticated'], ...overrides };
}
function adminUser(overrides = {}) {
  return { userId: 'admin-1', userDetails: 'kasare@spreadcomgh.com', userRoles: ['authenticated', 'administrator'], ...overrides };
}

// In-memory fake of the Cosmos container surface the handlers use:
//   items.upsert(doc) -> { resource }
//   items.query(spec).fetchAll() -> { resources }
//   item(id, pk).read() -> { resource } | throws (missing)
// `queryResult` lets a test fix what query().fetchAll() returns; otherwise it
// returns all upserted docs (optionally filtered by a provided predicate).
function makeContainer({ seed = [], queryResult } = {}) {
  const store = new Map(seed.map((d) => [d.id, d]));
  const calls = { upserts: [], queries: [] };
  return {
    _store: store,
    _calls: calls,
    items: {
      upsert: async (doc) => {
        calls.upserts.push(doc);
        store.set(doc.id, doc);
        return { resource: doc };
      },
      query: (spec) => {
        calls.queries.push(spec);
        return {
          fetchAll: async () => {
            if (typeof queryResult === 'function') return { resources: queryResult(spec, [...store.values()]) };
            if (Array.isArray(queryResult)) return { resources: queryResult };
            return { resources: [...store.values()] };
          },
        };
      },
    },
    item: (id) => ({
      read: async () => {
        if (!store.has(id)) {
          const err = new Error('NotFound');
          err.code = 404;
          throw err;
        }
        return { resource: store.get(id) };
      },
    }),
  };
}

module.exports = {
  API_ROOT,
  loadFunction,
  loadHandler,
  makeRequest,
  makeContext,
  makeContainer,
  anonUser,
  authUser,
  adminUser,
};
