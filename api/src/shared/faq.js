'use strict';

// Curated site-help FAQ loader (TW-118 Phase 2, Tier B — non-personal "how the
// site works" questions). Reads the hand-authored api/src/shared/faq.json.
//
// Unlike lessons.generated.json, faq.json is NOT build output — it's authored
// content, edited by hand in normal PRs and reviewed like any other content
// change. To add or edit an entry: append/edit an object with a unique
// kebab-case `id`, a short `topic`, the `question` it answers, and an `answer`
// written in the same plain-conversational register the chat widget renders
// (**bold**, `inline code`, and hyphen bullets only — no headings, tables, or
// links, since chat-panel.ts's renderer only supports that subset). Never add
// an entry that names or implies a specific student's data — every answer must
// stay generic ("your Account page shows...", never an actual value).
//
// Deliberately has no dependency on ./cosmos or any other live data source —
// this file must stay pure static-JSON grounding (see TW-118's zero-Cosmos
// tripwire).

let data;
function load() {
  if (!data) data = require('./faq.json');
  return data;
}

// Stable JSON string of the full FAQ, built once and reused across calls so
// the ephemeral cache_control block on it (Stage 2, shared/chat.js) hits
// Anthropic's prompt cache.
let faqJson;
function getFaqJson() {
  if (!faqJson) faqJson = JSON.stringify(load());
  return faqJson;
}

// Compact {id, topic, question} list (no answers) for the Stage-1 system
// context — same shape convention as lessons.js's listLessonMeta().
let topics;
function listFaqTopics() {
  if (!topics) {
    topics = load().map((e) => ({ id: e.id, topic: e.topic, question: e.question }));
  }
  return topics;
}

module.exports = { getFaqJson, listFaqTopics };
