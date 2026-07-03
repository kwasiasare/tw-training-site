'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, makeContainer, authUser } = require('./harness');

function progressHandler(container) {
  return loadHandler('progress', 'progress', { cosmosContainer: container });
}

test('progress: anonymous GET returns 401', async () => {
  const res = await progressHandler(makeContainer())(
    makeRequest({ method: 'GET' }),
    makeContext(),
  );
  assert.equal(res.status, 401);
});

test('progress: GET returns the user records', async () => {
  const records = [{ id: 'user-123:c:l', userId: 'user-123', type: 'progress', status: 'completed' }];
  const container = makeContainer({ queryResult: records });
  const res = await progressHandler(container)(
    makeRequest({ method: 'GET', user: authUser() }),
    makeContext(),
  );
  assert.deepEqual(res.jsonBody.items, records);
  // Query is scoped to the user id.
  assert.equal(container._calls.queries[0].parameters[0].value, 'user-123');
});

test('progress: POST without course/lesson returns 400', async () => {
  const res = await progressHandler(makeContainer())(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'c' } }),
    makeContext(),
  );
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'course_and_lesson_required');
});

test('progress: POST rejects a non-slug lesson (injection guard) with 400', async () => {
  const container = makeContainer();
  const res = await progressHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'demo-course', lesson: '<script>alert(1)</script>' } }),
    makeContext(),
  );
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'invalid_course_or_lesson');
  assert.equal(container._calls.upserts.length, 0, 'must not store an invalid lesson');
});

test('progress: POST upserts a progress record with a deterministic id', async () => {
  const container = makeContainer();
  const res = await progressHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'demo-course', lesson: 'l1' } }),
    makeContext(),
  );
  assert.equal(res.jsonBody.ok, true);
  const doc = container._calls.upserts[0];
  assert.equal(doc.id, 'user-123:demo-course:l1');
  assert.equal(doc.type, 'progress');
  assert.equal(doc.status, 'completed', 'defaults status to completed');
});

test('progress: POST merges a quiz score onto an existing record without clobbering status', async () => {
  const existing = {
    id: 'user-123:demo-course:l1', userId: 'user-123', type: 'progress',
    course: 'demo-course', lesson: 'l1', status: 'completed',
  };
  const container = makeContainer({ seed: [existing] });
  await progressHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'demo-course', lesson: 'l1', quizScore: 90 } }),
    makeContext(),
  );
  const doc = container._calls.upserts[0];
  assert.equal(doc.status, 'completed', 'keeps prior status when not supplied');
  assert.equal(doc.quizScore, 90, 'records the new quiz score');
});

test('progress: POST preserves an existing quiz score when only marking complete', async () => {
  const existing = {
    id: 'user-123:demo-course:l1', userId: 'user-123', type: 'progress',
    course: 'demo-course', lesson: 'l1', status: 'in-progress', quizScore: 75,
  };
  const container = makeContainer({ seed: [existing] });
  await progressHandler(container)(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'demo-course', lesson: 'l1', status: 'completed' } }),
    makeContext(),
  );
  const doc = container._calls.upserts[0];
  assert.equal(doc.status, 'completed');
  assert.equal(doc.quizScore, 75, 'preserves prior quiz score');
});

test('progress: POST rejects a lesson missing from the lesson index (certificate-forging guard)', async () => {
  const container = makeContainer();
  const handler = loadHandler('progress', 'progress', {
    cosmosContainer: container,
    lessons: { getLesson: () => null },
  });
  const res = await handler(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'demo-course', lesson: 'x1' } }),
    makeContext(),
  );
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'unknown_lesson');
  assert.equal(container._calls.upserts.length, 0, 'must not store an unknown lesson');
});

test('progress: POST rejects a real lesson claimed against the wrong course', async () => {
  const container = makeContainer();
  const handler = loadHandler('progress', 'progress', {
    cosmosContainer: container,
    lessons: { getLesson: () => ({ course: 'another-course' }) },
  });
  const res = await handler(
    makeRequest({ method: 'POST', user: authUser(), body: { course: 'demo-course', lesson: 'l1' } }),
    makeContext(),
  );
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'unknown_lesson');
  assert.equal(container._calls.upserts.length, 0, 'must not store a cross-course lesson');
});

test('progress: the real lesson index resolves a genuine catalog slug (integration)', () => {
  // Unstubbed shared/lessons against the committed lessons.generated.json — fails
  // loudly if a regenerated index drops or mis-labels a course, which would make
  // the forging guard reject legitimate progress writes for that whole course.
  // The harness leaves a stub for shared/lessons in require.cache — evict it so
  // this test exercises the real module.
  const lessonsId = require.resolve('../src/shared/lessons');
  delete require.cache[lessonsId];
  const real = require(lessonsId);
  const meta = real.getLesson('age-m1-l01-calling-llm-apis-in-python-completions-chat-and-');
  assert.ok(meta, 'known catalog slug must resolve');
  assert.equal(meta.course, 'agentic-ai-engineer');
  assert.ok(real.countLessons('agentic-ai-engineer') >= 20);
});
