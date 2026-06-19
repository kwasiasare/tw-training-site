'use strict';

// Guards the invariant called out in video.js: the FREE_PREVIEW slug set (which
// gates /api/video) must match the anonymous /topics/<slug>* route rules in
// staticwebapp.config.json. If they drift, a lesson page is public but its video
// 403s (or vice-versa). This test fails loudly when one side is edited alone.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const { loadFunction } = require('./harness');

const CONFIG_PATH = path.resolve(
  __dirname, '..', '..', 'site', 'public', 'staticwebapp.config.json',
);

function freePreviewSlugsFromConfig() {
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  const slugs = new Set();
  for (const r of config.routes || []) {
    const m = /^\/topics\/(.+)\*$/.exec(r.route || '');
    if (!m) continue;
    const slug = m[1];
    if (slug === '' || slug.includes('*')) continue; // skip the catch-all /topics/*
    if ((r.allowedRoles || []).includes('anonymous')) slugs.add(slug);
  }
  return slugs;
}

test('FREE_PREVIEW in video.js matches the anonymous /topics routes in staticwebapp.config.json', () => {
  const { exports } = loadFunction('video', { r2: async () => 'x' });
  const fromCode = exports.FREE_PREVIEW;
  assert.ok(fromCode instanceof Set, 'video.js should export FREE_PREVIEW as a Set');

  const fromConfig = freePreviewSlugsFromConfig();
  assert.ok(fromConfig.size >= 2, 'expected at least a couple of free-preview routes in the config');

  const codeArr = [...fromCode].sort();
  const configArr = [...fromConfig].sort();
  assert.deepEqual(
    codeArr, configArr,
    `FREE_PREVIEW (video.js) and staticwebapp.config.json have drifted.\n` +
    `  only in video.js: ${codeArr.filter((s) => !fromConfig.has(s)).join(', ') || '(none)'}\n` +
    `  only in config:   ${configArr.filter((s) => !fromCode.has(s)).join(', ') || '(none)'}`,
  );
});
