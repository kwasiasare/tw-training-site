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

// Return { course, title, objectives, body } for a lesson id, or null if unknown.
function getLesson(lessonId) {
  if (!lessonId) return null;
  const data = load()[lessonId];
  return data || null;
}

module.exports = { getLesson };
