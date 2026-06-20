'use strict';

// Lesson-content lookup for the AI tutor (TW-67). Reads the committed index that
// build_lesson_index.py generates from course-materials/*/lessons/*.md (the API
// deployment can't see that folder at runtime, so the text is bundled). Loaded
// once and cached in module scope.

let index;
function load() {
  if (!index) index = require('./lessons.generated.json');
  return index;
}

// Return { course, title, objectives, body, quiz } for a lesson id, or null if unknown.
function getLesson(lessonId) {
  if (!lessonId) return null;
  const data = load()[lessonId];
  return data || null;
}

// Count how many lessons belong to a course slug (used for completion certificates).
let counts;
function countLessons(courseSlug) {
  if (!courseSlug) return 0;
  if (!counts) {
    counts = {};
    const idx = load();
    for (const id of Object.keys(idx)) {
      const c = idx[id].course;
      if (c) counts[c] = (counts[c] || 0) + 1;
    }
  }
  return counts[courseSlug] || 0;
}

module.exports = { getLesson, countLessons };
