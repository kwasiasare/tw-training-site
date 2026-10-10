'use strict';

// Single place that decides HOW we reach Claude and WHICH models we use (TW-140).
//
// Preferred: Microsoft Foundry (@anthropic-ai/foundry-sdk). Selected when an
// endpoint (ANTHROPIC_FOUNDRY_RESOURCE or ANTHROPIC_FOUNDRY_BASE_URL) AND
// ANTHROPIC_FOUNDRY_API_KEY are both set. Fallback: direct Anthropic API via
// ANTHROPIC_API_KEY. Neither configured -> a clear config error that never
// includes any configured value.
//
// On Foundry, the `model` request field is the DEPLOYMENT name. Our deployments
// are named after the model id, so the defaults below work unchanged; override
// the CLAUDE_MODEL_* settings if a deployment is named differently.

const Anthropic = require('@anthropic-ai/sdk');
const AnthropicFoundry = require('@anthropic-ai/foundry-sdk');

let client;

function envStr(name) {
  const v = process.env[name];
  return typeof v === 'string' && v.trim() ? v.trim() : '';
}

// 'foundry' | 'direct' | null — which backend the current env selects.
function claudeProvider() {
  const hasEndpoint = envStr('ANTHROPIC_FOUNDRY_RESOURCE') || envStr('ANTHROPIC_FOUNDRY_BASE_URL');
  if (hasEndpoint && envStr('ANTHROPIC_FOUNDRY_API_KEY')) return 'foundry';
  if (envStr('ANTHROPIC_API_KEY')) return 'direct';
  return null;
}

function getClaudeClient() {
  if (client) return client;
  const provider = claudeProvider();
  if (provider === 'foundry') {
    const opts = { apiKey: envStr('ANTHROPIC_FOUNDRY_API_KEY') };
    const baseURL = envStr('ANTHROPIC_FOUNDRY_BASE_URL');
    if (baseURL) opts.baseURL = baseURL;
    else opts.resource = envStr('ANTHROPIC_FOUNDRY_RESOURCE');
    client = new AnthropicFoundry(opts);
  } else if (provider === 'direct') {
    client = new Anthropic({ apiKey: envStr('ANTHROPIC_API_KEY') });
  } else {
    throw new Error(
      'Claude is not configured: set ANTHROPIC_FOUNDRY_RESOURCE (or ANTHROPIC_FOUNDRY_BASE_URL) ' +
      'and ANTHROPIC_FOUNDRY_API_KEY for Microsoft Foundry, or ANTHROPIC_API_KEY for the direct API',
    );
  }
  return client;
}

// Read at call time (not module load) so app-setting changes and tests apply.
const selectModel = () => envStr('CLAUDE_MODEL_SELECT') || 'claude-haiku-4-5'; // chat Stage 1
const answerModel = () => envStr('CLAUDE_MODEL_ANSWER') || 'claude-sonnet-5'; // chat Stage 2
const tutorModel = () => envStr('CLAUDE_MODEL_TUTOR') || 'claude-opus-4-8'; // tutor, advisor, grader

module.exports = { getClaudeClient, claudeProvider, selectModel, answerModel, tutorModel };
