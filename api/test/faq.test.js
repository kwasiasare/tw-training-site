'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { getFaqJson, listFaqTopics } = require('../src/shared/faq');
const faqData = require('../src/shared/faq.json');

test('faq.json: every entry has a unique non-empty id and non-empty topic/question/answer strings', () => {
  assert.ok(Array.isArray(faqData) && faqData.length > 0);
  const seenIds = new Set();
  for (const entry of faqData) {
    assert.equal(typeof entry.id, 'string');
    assert.ok(entry.id.length > 0);
    assert.match(entry.id, /^[a-z0-9-]+$/, `id "${entry.id}" should be kebab-case`);
    assert.ok(!seenIds.has(entry.id), `duplicate FAQ id: ${entry.id}`);
    seenIds.add(entry.id);

    for (const field of ['topic', 'question', 'answer']) {
      assert.equal(typeof entry[field], 'string', `${entry.id}.${field} should be a string`);
      assert.ok(entry[field].trim().length > 0, `${entry.id}.${field} should not be empty`);
    }
  }
});

test('faq.json: no entry contains or implies per-student data (no personal-looking placeholders beyond generic phrasing)', () => {
  // A loose guard, not a full PII scanner: this content is hand-authored and
  // reviewed like any PR, but a quick check catches an obvious slip (e.g.
  // someone pasting a real name/email into an answer while drafting).
  const emailPattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/i;
  for (const entry of faqData) {
    assert.equal(emailPattern.test(entry.answer), false, `${entry.id}: answer should not contain an email address`);
  }
});

test('getFaqJson: returns a stable JSON string matching the full faq.json content', () => {
  const json = getFaqJson();
  assert.equal(typeof json, 'string');
  assert.deepEqual(JSON.parse(json), faqData);
  assert.equal(getFaqJson(), json, 'must be cached/stable across calls (so the cache_control block stays byte-identical)');
});

test('listFaqTopics: returns {id, topic, question} only — no answers — for every entry', () => {
  const topics = listFaqTopics();
  assert.equal(topics.length, faqData.length);
  for (const t of topics) {
    assert.equal(typeof t.id, 'string');
    assert.equal(typeof t.topic, 'string');
    assert.equal(typeof t.question, 'string');
    assert.equal('answer' in t, false, 'topic list must not leak answers into the Stage-1 prompt');
  }
});
