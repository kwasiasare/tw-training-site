'use strict';

// Deterministic reuse/matching layer (TW-68). Given an analysed user target
// profile, pick the best library course above a confidence threshold, or null
// (→ the advisor enqueues a course-generation request). Pure + unit-testable;
// no model call (a Claude-judged matcher can be swapped in later behind match()).

const STOP = new Set(['a', 'an', 'the', 'and', 'or', 'of', 'to', 'for', '/', '-', '&', 'engineer', 'developer']);

function tokens(s) {
  return String(s == null ? '' : s)
    .toLowerCase()
    .replace(/[^a-z0-9+# ]+/g, ' ')
    .split(/\s+/)
    .filter((t) => t && !STOP.has(t));
}

function tokenSet(values) {
  const set = new Set();
  for (const v of [].concat(values || [])) for (const t of tokens(v)) set.add(t);
  return set;
}

function intersize(a, b) {
  let inter = 0;
  for (const t of a) if (b.has(t)) inter += 1;
  return inter;
}

// Overlap coefficient: how much the smaller set is contained in the larger.
// Used for the role so titles of different lengths still compare fairly.
function overlap(a, b) {
  const min = Math.min(a.size, b.size);
  return min === 0 ? 0 : intersize(a, b) / min;
}

// Coverage of the user's needs by the course: of the skills the user needs to
// learn, what fraction does this course teach? Doesn't penalize a broad course.
function coverage(need, has) {
  return need.size === 0 ? 0 : intersize(need, has) / need.size;
}

// Score a user profile against one course profile. Role similarity is weighted
// more heavily than skill coverage. Returns 0..1.
function score(userProfile, courseProfile) {
  const roleScore = overlap(tokenSet(userProfile.role), tokenSet(courseProfile.role));
  const skillScore = coverage(tokenSet(userProfile.skills), tokenSet(courseProfile.skills));
  return 0.6 * roleScore + 0.4 * skillScore;
}

// Best match across the catalog. Returns { courseSlug, score } when the best
// score meets `threshold`, else null. `userProfile` = { role, skills:[] }.
function match(userProfile, courses, threshold = 0.5) {
  let best = null;
  for (const c of courses || []) {
    const s = score(userProfile || {}, c.targetProfile || {});
    if (!best || s > best.score) best = { courseSlug: c.slug, score: s };
  }
  if (!best) return null;
  best.score = Math.round(best.score * 1000) / 1000;
  return best.score >= threshold ? best : null;
}

module.exports = { match, score, tokenSet, overlap, coverage };
