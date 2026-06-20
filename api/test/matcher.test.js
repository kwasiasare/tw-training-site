'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const { match, score } = require(path.join(__dirname, '..', 'src', 'shared', 'matcher.js'));
const { BUILTIN_COURSES } = require(path.join(__dirname, '..', 'src', 'shared', 'catalog.js'));

test('match assigns an Applied GenAI profile to kwasi-GenAI', () => {
  const m = match(
    { role: 'Applied GenAI Engineer', skills: ['rag', 'agents', 'llm apis', 'cloud'] },
    BUILTIN_COURSES,
  );
  assert.ok(m, 'expected a match');
  assert.equal(m.courseSlug, 'kwasi-GenAI');
  assert.ok(m.score >= 0.5);
});

test('match assigns a helpdesk profile to helpdesk-tier1-2', () => {
  const m = match(
    { role: 'IT Support Technician', skills: ['windows', 'networking', 'comptia a+', 'ticketing'] },
    BUILTIN_COURSES,
  );
  assert.ok(m);
  assert.equal(m.courseSlug, 'helpdesk-tier1-2');
});

test('match reuses a published generated course when it fits best', () => {
  const generated = {
    slug: 'cx-prompt-eng',
    title: 'Prompt Engineering Pro',
    summary: 'Custom generated course.',
    targetProfile: { role: 'Prompt Engineer', level: 'mid', skills: ['prompting', 'evals', 'rag'] },
  };
  const library = [...BUILTIN_COURSES, generated];
  const m = match({ role: 'Prompt Engineer', skills: ['prompting', 'evals'] }, library);
  assert.ok(m);
  assert.equal(m.courseSlug, 'cx-prompt-eng', 'generated course is reusable via the matcher');
});

test('match returns null when nothing meets the threshold', () => {
  const m = match(
    { role: 'Underwater Basket Weaver', skills: ['knitting', 'reeds'] },
    BUILTIN_COURSES,
  );
  assert.equal(m, null);
});

test('score weights role similarity above skill overlap', () => {
  const sameRole = score({ role: 'Applied GenAI Engineer', skills: [] }, BUILTIN_COURSES[0].targetProfile);
  const sameSkillsOnly = score({ role: 'Zzz', skills: ['rag', 'cloud'] }, BUILTIN_COURSES[0].targetProfile);
  assert.ok(sameRole > sameSkillsOnly);
});

test('threshold is tunable', () => {
  const profile = { role: 'Generalist', skills: ['windows', 'networking'] };
  const loose = match(profile, BUILTIN_COURSES, 0.1);
  const strict = match(profile, BUILTIN_COURSES, 0.95);
  assert.ok(loose, 'loose threshold should match something');
  assert.equal(strict, null, 'strict threshold should reject a weak match');
});
