'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const { match, score } = require(path.join(__dirname, '..', 'src', 'shared', 'matcher.js'));
const { BUILTIN_COURSES } = require(path.join(__dirname, '..', 'src', 'shared', 'catalog.js'));

test('match assigns an AI App Developer profile to dami-ai-career', () => {
  const m = match(
    { role: 'AI Application Developer', skills: ['python', 'rag', 'llm apps', 'apis'] },
    BUILTIN_COURSES,
  );
  assert.ok(m, 'expected a match');
  assert.equal(m.courseSlug, 'dami-ai-career');
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

test('match returns null when nothing meets the threshold', () => {
  const m = match(
    { role: 'Underwater Basket Weaver', skills: ['knitting', 'reeds'] },
    BUILTIN_COURSES,
  );
  assert.equal(m, null);
});

test('score weights role similarity above skill overlap', () => {
  const sameRole = score({ role: 'AI Application Developer', skills: [] }, BUILTIN_COURSES[0].targetProfile);
  const sameSkillsOnly = score({ role: 'Zzz', skills: ['python', 'rag'] }, BUILTIN_COURSES[0].targetProfile);
  assert.ok(sameRole > sameSkillsOnly);
});

test('threshold is tunable', () => {
  const profile = { role: 'Data Person', skills: ['sql', 'data'] };
  const loose = match(profile, BUILTIN_COURSES, 0.1);
  const strict = match(profile, BUILTIN_COURSES, 0.95);
  assert.ok(loose, 'loose threshold should match something');
  assert.equal(strict, null, 'strict threshold should reject a weak match');
});
