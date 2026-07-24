'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const { isGatewayConfigured, answerViaGateway } = require('../src/shared/localllm');

// Start a stub HTTP server on an ephemeral port that runs `onRequest` for every
// request. Returns { url, close } — tests MUST call close() so the server
// (and any pending connections) don't keep the test process alive.
function startStub(onRequest) {
  const server = http.createServer(onRequest);
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({
        url: `http://127.0.0.1:${port}`,
        close: () => new Promise((r) => server.close(r)),
      });
    });
  });
}

function readBody(req) {
  return new Promise((resolve) => {
    let data = '';
    req.on('data', (chunk) => { data += chunk; });
    req.on('end', () => resolve(data));
  });
}

const ENV_KEYS = ['LOCAL_LLM_GATEWAY_URL', 'LOCAL_LLM_GATEWAY_KEY', 'LOCAL_LLM_CHAT_COLLECTION', 'LOCAL_LLM_CHAT_TIER', 'LOCAL_LLM_TIMEOUT_MS'];

function snapshotEnv() {
  const saved = {};
  for (const k of ENV_KEYS) saved[k] = process.env[k];
  return () => {
    for (const k of ENV_KEYS) {
      if (saved[k] === undefined) delete process.env[k];
      else process.env[k] = saved[k];
    }
  };
}

// --- isGatewayConfigured ---

test('isGatewayConfigured: false when both env vars are missing', () => {
  const restore = snapshotEnv();
  try {
    delete process.env.LOCAL_LLM_GATEWAY_URL;
    delete process.env.LOCAL_LLM_GATEWAY_KEY;
    assert.equal(isGatewayConfigured(), false);
  } finally {
    restore();
  }
});

test('isGatewayConfigured: false when only the URL is set', () => {
  const restore = snapshotEnv();
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = 'http://127.0.0.1:9';
    delete process.env.LOCAL_LLM_GATEWAY_KEY;
    assert.equal(isGatewayConfigured(), false);
  } finally {
    restore();
  }
});

test('isGatewayConfigured: false when only the key is set', () => {
  const restore = snapshotEnv();
  try {
    delete process.env.LOCAL_LLM_GATEWAY_URL;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'secret';
    assert.equal(isGatewayConfigured(), false);
  } finally {
    restore();
  }
});

test('isGatewayConfigured: true when both env vars are non-empty', () => {
  const restore = snapshotEnv();
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = 'http://127.0.0.1:9';
    process.env.LOCAL_LLM_GATEWAY_KEY = 'secret';
    assert.equal(isGatewayConfigured(), true);
  } finally {
    restore();
  }
});

// --- answerViaGateway ---

test('answerViaGateway: success returns the trimmed reply and sends the correct body fields + auth header', async () => {
  const restore = snapshotEnv();
  let seenAuth;
  let seenBody;
  const stub = await startStub(async (req, res) => {
    seenAuth = req.headers.authorization;
    seenBody = JSON.parse(await readBody(req));
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ app: 'local-llm', reply: '  Kubernetes is covered in the MLOps track.  ', sources: [] }));
  });
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = stub.url;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'super-secret-key';
    delete process.env.LOCAL_LLM_CHAT_COLLECTION;
    delete process.env.LOCAL_LLM_CHAT_TIER;

    const messages = [{ role: 'user', content: 'Which course covers Kubernetes?' }];
    const { reply } = await answerViaGateway({ messages });

    assert.equal(reply, 'Kubernetes is covered in the MLOps track.');
    assert.equal(seenAuth, 'Bearer super-secret-key');
    assert.deepEqual(seenBody, {
      messages,
      collection: 'training-lesson-content',
      k: 5,
      tier: 'cloud',
    });
  } finally {
    await stub.close();
    restore();
  }
});

test('answerViaGateway: honors LOCAL_LLM_CHAT_COLLECTION / LOCAL_LLM_CHAT_TIER overrides', async () => {
  const restore = snapshotEnv();
  let seenBody;
  const stub = await startStub(async (req, res) => {
    seenBody = JSON.parse(await readBody(req));
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ app: 'local-llm', reply: 'ok', sources: [] }));
  });
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = `${stub.url}/`; // trailing slash — URL join must not double it
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';
    process.env.LOCAL_LLM_CHAT_COLLECTION = 'custom-collection';
    process.env.LOCAL_LLM_CHAT_TIER = 'edge';

    await answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] });
    assert.equal(seenBody.collection, 'custom-collection');
    assert.equal(seenBody.tier, 'edge');
  } finally {
    await stub.close();
    restore();
  }
});

test('answerViaGateway: non-200 throws with code "gateway_http" (message includes the status)', async () => {
  const restore = snapshotEnv();
  const stub = await startStub((req, res) => {
    res.writeHead(500, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ detail: 'internal error' }));
  });
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = stub.url;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';

    await assert.rejects(
      answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] }),
      (err) => {
        assert.equal(err.code, 'gateway_http');
        assert.match(err.message, /500/);
        assert.doesNotMatch(err.message, /key/i);
        return true;
      },
    );
  } finally {
    await stub.close();
    restore();
  }
});

test('answerViaGateway: empty reply throws with code "gateway_bad_reply"', async () => {
  const restore = snapshotEnv();
  const stub = await startStub((req, res) => {
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ app: 'local-llm', reply: '   ', sources: [] }));
  });
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = stub.url;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';

    await assert.rejects(
      answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] }),
      (err) => err.code === 'gateway_bad_reply',
    );
  } finally {
    await stub.close();
    restore();
  }
});

test('answerViaGateway: missing reply field throws with code "gateway_bad_reply"', async () => {
  const restore = snapshotEnv();
  const stub = await startStub((req, res) => {
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ app: 'local-llm', sources: [] }));
  });
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = stub.url;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';

    await assert.rejects(
      answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] }),
      (err) => err.code === 'gateway_bad_reply',
    );
  } finally {
    await stub.close();
    restore();
  }
});

test('answerViaGateway: a stub that never responds times out with code "gateway_timeout"', async () => {
  const restore = snapshotEnv();
  // Never call res.end() — the connection just hangs until our AbortController fires.
  const stub = await startStub(() => {});
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = stub.url;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';
    process.env.LOCAL_LLM_TIMEOUT_MS = '50';

    await assert.rejects(
      answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] }),
      (err) => err.code === 'gateway_timeout',
    );
  } finally {
    await stub.close();
    restore();
  }
});

test('answerViaGateway: unreachable host throws with code "gateway_network"', async () => {
  const restore = snapshotEnv();
  // Bind a server to grab a free port, close it immediately, then point the
  // client at that now-unoccupied port so the connection is refused.
  const probe = await startStub(() => {});
  const deadUrl = probe.url;
  await probe.close();
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = deadUrl;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';

    await assert.rejects(
      answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] }),
      (err) => err.code === 'gateway_network',
    );
  } finally {
    restore();
  }
});

test('answerViaGateway: 200 with a non-JSON body throws with code "gateway_bad_reply"', async () => {
  const restore = snapshotEnv();
  const stub = await startStub((req, res) => {
    res.writeHead(200, { 'content-type': 'text/plain' });
    res.end('not json at all');
  });
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = stub.url;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';

    await assert.rejects(
      answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] }),
      (err) => err.code === 'gateway_bad_reply',
    );
  } finally {
    await stub.close();
    restore();
  }
});

test('answerViaGateway: sources are passed through verbatim, and default to [] when absent', async () => {
  const restore = snapshotEnv();
  const wantSources = [{ metadata: { source: 'kwasi-GenAI/lessons/g2-l01-embeddings.md' } }];
  let call = 0;
  const stub = await startStub((req, res) => {
    call += 1;
    res.writeHead(200, { 'content-type': 'application/json' });
    if (call === 1) {
      res.end(JSON.stringify({ app: 'local-llm', reply: 'with sources', sources: wantSources }));
    } else {
      res.end(JSON.stringify({ app: 'local-llm', reply: 'without sources' }));
    }
  });
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = stub.url;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';

    const withSources = await answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] });
    assert.deepEqual(withSources.sources, wantSources);

    const withoutSources = await answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] });
    assert.deepEqual(withoutSources.sources, []);
  } finally {
    await stub.close();
    restore();
  }
});

test('answerViaGateway: a stalled body (200 headers, response never ends) times out with code "gateway_timeout"', async () => {
  const restore = snapshotEnv();
  const stub = await startStub((req, res) => {
    res.writeHead(200, { 'content-type': 'application/json' });
    // Write a partial JSON body and never call res.end() — the headers land
    // fine but the body read must still be caught by the abort timer.
    res.write('{"app":"local-llm","reply":"chun');
  });
  try {
    process.env.LOCAL_LLM_GATEWAY_URL = stub.url;
    process.env.LOCAL_LLM_GATEWAY_KEY = 'key';
    process.env.LOCAL_LLM_TIMEOUT_MS = '50';

    await assert.rejects(
      answerViaGateway({ messages: [{ role: 'user', content: 'hi' }] }),
      (err) => err.code === 'gateway_timeout',
    );
  } finally {
    await stub.close();
    restore();
  }
});
