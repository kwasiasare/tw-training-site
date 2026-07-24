'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { isBedrockKbConfigured, answerViaBedrockKb } = require('../src/shared/bedrockkb');

const ENV_KEYS = ['BEDROCK_KB_ID', 'BEDROCK_KB_REGION', 'BEDROCK_KB_K', 'BEDROCK_TIMEOUT_MS', 'BEDROCK_CHAT_MODEL'];

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

// Build a fake agentClient whose RetrieveCommand handling is controlled by
// `impl` — either a canned result object or a function(command, opts) that
// returns/throws/hangs as needed.
function fakeAgentClient(impl) {
  return {
    send: async (command, opts) => {
      if (typeof impl === 'function') return impl(command, opts);
      return impl;
    },
  };
}

function fakeRuntimeClient(impl) {
  return {
    send: async (command, opts) => {
      if (typeof impl === 'function') return impl(command, opts);
      return impl;
    },
  };
}

function retrieveResult(results) {
  return { retrievalResults: results };
}

function converseResult(text) {
  return { output: { message: { content: [{ text }] } } };
}

// --- isBedrockKbConfigured ---

test('isBedrockKbConfigured: false when BEDROCK_KB_ID is missing', () => {
  const restore = snapshotEnv();
  try {
    delete process.env.BEDROCK_KB_ID;
    assert.equal(isBedrockKbConfigured(), false);
  } finally {
    restore();
  }
});

test('isBedrockKbConfigured: false when BEDROCK_KB_ID is empty string', () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = '';
    assert.equal(isBedrockKbConfigured(), false);
  } finally {
    restore();
  }
});

test('isBedrockKbConfigured: true when BEDROCK_KB_ID is set', () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-abc123';
    assert.equal(isBedrockKbConfigured(), true);
  } finally {
    restore();
  }
});

// --- answerViaBedrockKb: success ---

test('answerViaBedrockKb: success sends correct KB id/k/model and returns trimmed reply + sourcePaths', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';
    delete process.env.BEDROCK_KB_K; // default k
    delete process.env.BEDROCK_CHAT_MODEL; // default model

    let seenRetrieveInput;
    let seenConverseInput;
    const agentClient = fakeAgentClient((command) => {
      seenRetrieveInput = command.input;
      return retrieveResult([
        { content: { text: 'Excerpt one text.' }, location: { s3Location: { uri: 's3://bucket/kwasi-GenAI/lessons/g2-l01-embeddings.md' } } },
        { content: { text: 'Excerpt two text.' }, location: { s3Location: { uri: 's3://bucket/kwasi-GenAI/lessons/g2-l02-vectors.md' } } },
      ]);
    });
    const runtimeClient = fakeRuntimeClient((command) => {
      seenConverseInput = command.input;
      return converseResult('  This is the grounded answer.  ');
    });

    const messages = [{ role: 'user', content: 'What are embeddings?' }];
    const { reply, sourcePaths } = await answerViaBedrockKb({ messages, clients: { agentClient, runtimeClient } });

    assert.equal(reply, 'This is the grounded answer.');
    assert.deepEqual(sourcePaths, [
      's3://bucket/kwasi-GenAI/lessons/g2-l01-embeddings.md',
      's3://bucket/kwasi-GenAI/lessons/g2-l02-vectors.md',
    ]);

    assert.equal(seenRetrieveInput.knowledgeBaseId, 'kb-xyz');
    assert.equal(seenRetrieveInput.retrievalQuery.text, 'What are embeddings?');
    assert.equal(seenRetrieveInput.retrievalConfiguration.vectorSearchConfiguration.numberOfResults, 5);

    assert.equal(seenConverseInput.modelId, 'us.anthropic.claude-haiku-4-5-20251001-v1:0');
    assert.equal(seenConverseInput.messages[0].role, 'user');
    const prompt = seenConverseInput.messages[0].content[0].text;
    assert.match(prompt, /\[Source 1\]/);
    assert.match(prompt, /Excerpt one text\./);
    assert.match(prompt, /\[Source 2\]/);
    assert.match(prompt, /Excerpt two text\./);
    assert.match(prompt, /Student: What are embeddings\?/);
    assert.equal(seenConverseInput.inferenceConfig.maxTokens, 800);
  } finally {
    restore();
  }
});

test('answerViaBedrockKb: honors BEDROCK_CHAT_MODEL override', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';
    process.env.BEDROCK_CHAT_MODEL = 'us.anthropic.claude-opus-4-8-v1:0';

    let seenConverseInput;
    const agentClient = fakeAgentClient(() => retrieveResult([]));
    const runtimeClient = fakeRuntimeClient((command) => {
      seenConverseInput = command.input;
      return converseResult('answer');
    });

    await answerViaBedrockKb({
      messages: [{ role: 'user', content: 'hi' }],
      clients: { agentClient, runtimeClient },
    });

    assert.equal(seenConverseInput.modelId, 'us.anthropic.claude-opus-4-8-v1:0');
  } finally {
    restore();
  }
});

test('answerViaBedrockKb: last 6 messages rendered as Student:/Assistant: lines', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';

    let seenConverseInput;
    const agentClient = fakeAgentClient(() => retrieveResult([]));
    const runtimeClient = fakeRuntimeClient((command) => {
      seenConverseInput = command.input;
      return converseResult('answer');
    });

    const messages = [
      { role: 'user', content: 'turn 1' },
      { role: 'assistant', content: 'reply 1' },
      { role: 'user', content: 'turn 2' },
      { role: 'assistant', content: 'reply 2' },
      { role: 'user', content: 'turn 3' },
      { role: 'assistant', content: 'reply 3' },
      { role: 'user', content: 'turn 4 (latest)' },
    ];

    await answerViaBedrockKb({ messages, clients: { agentClient, runtimeClient } });

    const prompt = seenConverseInput.messages[0].content[0].text;
    // Only the last 6 messages should appear — 'turn 1' (message 0) is dropped.
    assert.doesNotMatch(prompt, /turn 1(?!.)/);
    assert.match(prompt, /Assistant: reply 1/);
    assert.match(prompt, /Student: turn 2/);
    assert.match(prompt, /Student: turn 4 \(latest\)/);
  } finally {
    restore();
  }
});

// --- answerViaBedrockKb: errors ---

test('answerViaBedrockKb: Retrieve rejection throws with code "bedrock_retrieve"', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';
    const agentClient = { send: async () => { throw new Error('AccessDeniedException'); } };
    const runtimeClient = fakeRuntimeClient(() => converseResult('unused'));

    await assert.rejects(
      answerViaBedrockKb({ messages: [{ role: 'user', content: 'hi' }], clients: { agentClient, runtimeClient } }),
      (err) => {
        assert.equal(err.code, 'bedrock_retrieve');
        assert.doesNotMatch(err.message, /hi\b/);
        return true;
      },
    );
  } finally {
    restore();
  }
});

test('answerViaBedrockKb: Converse rejection throws with code "bedrock_generate"', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';
    const agentClient = fakeAgentClient(() => retrieveResult([]));
    const runtimeClient = { send: async () => { throw new Error('ThrottlingException'); } };

    await assert.rejects(
      answerViaBedrockKb({ messages: [{ role: 'user', content: 'hi' }], clients: { agentClient, runtimeClient } }),
      (err) => {
        assert.equal(err.code, 'bedrock_generate');
        return true;
      },
    );
  } finally {
    restore();
  }
});

test('answerViaBedrockKb: empty reply text throws with code "bedrock_bad_reply"', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';
    const agentClient = fakeAgentClient(() => retrieveResult([]));
    const runtimeClient = fakeRuntimeClient(() => converseResult('   '));

    await assert.rejects(
      answerViaBedrockKb({ messages: [{ role: 'user', content: 'hi' }], clients: { agentClient, runtimeClient } }),
      (err) => err.code === 'bedrock_bad_reply',
    );
  } finally {
    restore();
  }
});

test('answerViaBedrockKb: missing content block throws with code "bedrock_bad_reply"', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';
    const agentClient = fakeAgentClient(() => retrieveResult([]));
    const runtimeClient = fakeRuntimeClient(() => ({ output: { message: { content: [] } } }));

    await assert.rejects(
      answerViaBedrockKb({ messages: [{ role: 'user', content: 'hi' }], clients: { agentClient, runtimeClient } }),
      (err) => err.code === 'bedrock_bad_reply',
    );
  } finally {
    restore();
  }
});

test('answerViaBedrockKb: a fake that never resolves + BEDROCK_TIMEOUT_MS=50 rejects with code "bedrock_timeout" and does not hang', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';
    process.env.BEDROCK_TIMEOUT_MS = '50';

    // Never resolves/rejects on its own — only reacts to the abort signal.
    const agentClient = {
      send: (command, opts) => new Promise((resolve, reject) => {
        opts.abortSignal.addEventListener('abort', () => {
          const err = new Error('The operation was aborted');
          err.name = 'AbortError';
          reject(err);
        });
      }),
    };
    const runtimeClient = fakeRuntimeClient(() => converseResult('unused'));

    await assert.rejects(
      answerViaBedrockKb({ messages: [{ role: 'user', content: 'hi' }], clients: { agentClient, runtimeClient } }),
      (err) => err.code === 'bedrock_timeout',
    );
  } finally {
    restore();
  }
});

test('answerViaBedrockKb: a Converse call that never resolves + BEDROCK_TIMEOUT_MS=50 rejects with code "bedrock_timeout"', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';
    process.env.BEDROCK_TIMEOUT_MS = '50';

    const agentClient = fakeAgentClient(() => retrieveResult([]));
    const runtimeClient = {
      send: (command, opts) => new Promise((resolve, reject) => {
        opts.abortSignal.addEventListener('abort', () => {
          const err = new Error('The operation was aborted');
          err.name = 'AbortError';
          reject(err);
        });
      }),
    };

    await assert.rejects(
      answerViaBedrockKb({ messages: [{ role: 'user', content: 'hi' }], clients: { agentClient, runtimeClient } }),
      (err) => err.code === 'bedrock_timeout',
    );
  } finally {
    restore();
  }
});

// --- k clamping ---

test('answerViaBedrockKb: BEDROCK_KB_K is clamped to [1, 20]', async () => {
  const restore = snapshotEnv();
  try {
    process.env.BEDROCK_KB_ID = 'kb-xyz';

    async function kFor(rawK) {
      if (rawK === undefined) delete process.env.BEDROCK_KB_K;
      else process.env.BEDROCK_KB_K = rawK;
      let seenK;
      const agentClient = fakeAgentClient((command) => {
        seenK = command.input.retrievalConfiguration.vectorSearchConfiguration.numberOfResults;
        return retrieveResult([]);
      });
      const runtimeClient = fakeRuntimeClient(() => converseResult('answer'));
      await answerViaBedrockKb({ messages: [{ role: 'user', content: 'hi' }], clients: { agentClient, runtimeClient } });
      return seenK;
    }

    assert.equal(await kFor(undefined), 5, 'default when unset');
    assert.equal(await kFor('0'), 1, 'clamps below minimum up to 1');
    assert.equal(await kFor('-5'), 1, 'clamps negative up to 1');
    assert.equal(await kFor('3'), 3, 'in-range value passes through');
    assert.equal(await kFor('50'), 20, 'clamps above maximum down to 20');
    assert.equal(await kFor('not-a-number'), 5, 'non-numeric falls back to default');
  } finally {
    restore();
  }
});
