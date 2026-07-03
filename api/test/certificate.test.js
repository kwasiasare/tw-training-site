'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, makeContainer, authUser } = require('./harness');

function handler(container, lessons) {
  return loadHandler('certificate', 'certificate', { cosmosContainer: container || makeContainer(), lessons });
}

// Progress docs for `n` completed lessons of `course`, for user-123.
function completed(course, n) {
  return Array.from({ length: n }, (_, i) => ({
    id: `user-123:${course}:l${i}`, userId: 'user-123', type: 'progress',
    course, lesson: `l${i}`, status: 'completed',
  }));
}

test('certificate: anonymous request returns 403 (not 401, to dodge the SWA signin redirect)', async () => {
  const res = await handler()(makeRequest({ method: 'GET', query: { course: 'demo-course' } }), makeContext());
  assert.equal(res.status, 403);
  assert.equal(res.jsonBody.error, 'login_required');
});

test('certificate: a bad course slug returns 400', async () => {
  const res = await handler()(makeRequest({ method: 'GET', user: authUser(), query: { course: 'bad slug!' } }), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'bad_course');
});

test('certificate: a course with no lessons returns 404', async () => {
  const res = await handler(makeContainer(), { countLessons: () => 0 })(
    makeRequest({ method: 'GET', user: authUser(), query: { course: 'ghost' } }), makeContext());
  assert.equal(res.status, 404);
  assert.equal(res.jsonBody.error, 'unknown_course');
});

test('certificate: not yet eligible reports progress', async () => {
  const container = makeContainer({ queryResult: completed('demo-course', 2) }); // 2 of 3
  const res = await handler(container, { countLessons: () => 3 })(
    makeRequest({ method: 'GET', user: authUser(), query: { course: 'demo-course' } }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.eligible, false);
  assert.equal(res.jsonBody.completedLessons, 2);
  assert.equal(res.jsonBody.totalLessons, 3);
});

test('certificate: full completion issues and persists a certificate', async () => {
  const container = makeContainer({ queryResult: completed('demo-course', 3) }); // 3 of 3
  const res = await handler(container, { countLessons: () => 3 })(
    makeRequest({ method: 'GET', user: authUser(), query: { course: 'demo-course' } }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.eligible, true);
  assert.equal(res.jsonBody.completedLessons, 3);
  assert.ok(res.jsonBody.serial, 'a serial was issued');
  assert.ok(res.jsonBody.issuedAt, 'an issue date was set');
  // The certificate doc was persisted.
  const cert = container._calls.upserts.find((d) => d.type === 'certificate');
  assert.ok(cert, 'certificate persisted');
  assert.equal(cert.id, 'user-123:cert:demo-course');
});

test('certificate: duplicate lesson completions are de-duplicated (no false eligibility)', async () => {
  // Same lesson completed twice + one other = 2 distinct of 3 → not eligible.
  const dupes = [...completed('demo-course', 1), ...completed('demo-course', 1),
    { id: 'x', userId: 'user-123', type: 'progress', course: 'demo-course', lesson: 'other', status: 'completed' }];
  const container = makeContainer({ queryResult: dupes });
  const res = await handler(container, { countLessons: () => 3 })(
    makeRequest({ method: 'GET', user: authUser(), query: { course: 'demo-course' } }), makeContext());
  assert.equal(res.jsonBody.eligible, false);
  assert.equal(res.jsonBody.completedLessons, 2, 'distinct lessons only');
});

test('certificate: re-issue returns the SAME serial (stable certificate)', async () => {
  const seed = [{
    id: 'user-123:cert:demo-course', userId: 'user-123', type: 'certificate',
    course: 'demo-course', serial: 'ABCD1234', issuedAt: '2026-01-01T00:00:00Z',
  }];
  const container = makeContainer({ seed, queryResult: [...completed('demo-course', 3), ...seed] });
  const res = await handler(container, { countLessons: () => 3 })(
    makeRequest({ method: 'GET', user: authUser(), query: { course: 'demo-course' } }), makeContext());
  assert.equal(res.jsonBody.serial, 'ABCD1234', 'existing serial reused');
  assert.equal(res.jsonBody.issuedAt, '2026-01-01T00:00:00Z');
});

test('certificate: fabricated lesson slugs do not count toward completion', async () => {
  // Slug-shaped junk that was never a real lesson (e.g. stored before the
  // progress-write validation existed) must not add up to a certificate.
  const junk = [1, 2, 3].map((i) => ({
    id: `user-123:demo-course:x${i}`, userId: 'user-123', type: 'progress',
    course: 'demo-course', lesson: `x${i}`, status: 'completed',
  }));
  const container = makeContainer({ queryResult: junk });
  const res = await handler(container, {
    countLessons: () => 3,
    getLesson: (id) => (id.startsWith('l') ? { course: 'demo-course' } : null),
  })(makeRequest({ method: 'GET', user: authUser(), query: { course: 'demo-course' } }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.eligible, false);
  assert.equal(res.jsonBody.completedLessons, 0, 'junk lessons must not be counted');
  assert.equal(container._calls.upserts.length, 0, 'no certificate may be issued');
});

test('certificate: an issued certificate is grandfathered when the course later grows', async () => {
  // User completed all 3 lessons and was issued a cert; the course then grew
  // to 5 lessons. The persisted certificate must still be returned (TW-98
  // product decision) instead of flipping back to eligible:false.
  const seed = [{
    id: 'user-123:cert:demo-course', userId: 'user-123', type: 'certificate',
    course: 'demo-course', serial: 'GRNDFTHR', issuedAt: '2026-06-01T00:00:00Z',
  }];
  const container = makeContainer({ seed, queryResult: [...completed('demo-course', 3), ...seed] });
  const res = await handler(container, {
    countLessons: () => 5, // course grew after issuance
    getLesson: (id) => (id.startsWith('l') ? { course: 'demo-course' } : null),
  })(makeRequest({ method: 'GET', user: authUser(), query: { course: 'demo-course' } }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.eligible, true, 'issued cert must survive course growth');
  assert.equal(res.jsonBody.serial, 'GRNDFTHR', 'must return the original certificate');
  assert.equal(container._calls.upserts.length, 0, 'must not re-issue');
});
