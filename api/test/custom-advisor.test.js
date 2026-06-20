'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { loadHandler, makeRequest, makeContext, makeContainer, authUser } = require('./harness');

const PDF_B64 = Buffer.from('%PDF-1.4\nfake résumé content\n%%EOF').toString('base64');

// analysis the Claude wrapper would return
function analysisFor(role, skills) {
  return {
    summary: 's', currentSkills: ['x'], gaps: ['y'],
    targetRoles: [{ role, timeToHire: '4-7 months', why: 'w', leverage: 'l' }],
    recommendedRole: role, recommendedSkills: skills,
  };
}

function advisorHandler({ container, advisor, resumes, notify } = {}) {
  return loadHandler('custom-advisor', 'custom-advisor', {
    cosmosContainer: container || makeContainer(),
    advisor: advisor || (async () => analysisFor('AI Application Developer', ['python', 'rag', 'llm apps'])),
    resumes,
    notify,
  });
}

function body(overrides = {}) {
  return {
    method: 'POST',
    user: authUser(),
    body: {
      consent: true,
      questionnaire: { targetOutcome: 'AI developer job', hoursPerWeek: 10 },
      resumeBase64: PDF_B64,
      ...overrides,
    },
  };
}

test('custom-advisor: anonymous request returns 401', async () => {
  const res = await advisorHandler()(makeRequest({ method: 'POST', body: {} }), makeContext());
  assert.equal(res.status, 401);
});

test('custom-advisor: missing consent returns 400', async () => {
  const res = await advisorHandler()(makeRequest(body({ consent: false })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'consent_required');
});

test('custom-advisor: incomplete questionnaire returns 400', async () => {
  const res = await advisorHandler()(makeRequest(body({ questionnaire: {} })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'questionnaire_incomplete');
});

test('custom-advisor: missing résumé returns 400', async () => {
  const res = await advisorHandler()(makeRequest(body({ resumeBase64: '' })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'resume_required');
});

test('custom-advisor: a non-PDF upload is rejected', async () => {
  const notPdf = Buffer.from('<html>not a pdf</html>').toString('base64');
  const res = await advisorHandler()(makeRequest(body({ resumeBase64: notPdf })), makeContext());
  assert.equal(res.status, 400);
  assert.equal(res.jsonBody.error, 'resume_not_pdf');
});

test('custom-advisor: matched path enrolls and persists the advisor doc', async () => {
  const container = makeContainer();
  const stored = [];
  const res = await advisorHandler({
    container,
    advisor: async () => analysisFor('AI Application Developer', ['python', 'rag', 'llm apps']),
    resumes: { putResume: async (uid, buf) => { stored.push(buf); return { bucket: 'tw-resumes', key: `${uid}/r.pdf` }; } },
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.outcome.type, 'matched');
  assert.equal(res.jsonBody.outcome.courseSlug, 'ai-app-developer-2026');
  assert.equal(stored.length, 1, 'résumé was stored before analysis');
  const ids = container._calls.upserts.map((d) => d.id);
  assert.ok(ids.includes('user-123:enroll:ai-app-developer-2026'), 'enrollment created');
  assert.ok(ids.includes('user-123:advisor'), 'advisor doc persisted');
  const advisorDoc = container._calls.upserts.find((d) => d.type === 'advisor');
  assert.equal(advisorDoc.consent, true);
  assert.equal(advisorDoc.resumeRef.bucket, 'tw-resumes');
});

test('custom-advisor: no match enqueues a generation request', async () => {
  const container = makeContainer();
  const res = await advisorHandler({
    container,
    advisor: async () => analysisFor('Quantum Hardware Technician', ['cryogenics', 'qubits']),
  })(makeRequest(body()), makeContext());

  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.outcome.type, 'generating');
  const gen = container._calls.upserts.find((d) => d.type === 'generationRequest');
  assert.ok(gen, 'generation request enqueued');
  assert.equal(gen.status, 'queued');
  assert.equal(gen.targetRole, 'Quantum Hardware Technician');
});

test('custom-advisor: GET returns the saved analysis + generation status', async () => {
  const container = makeContainer({ seed: [
    { id: 'user-123:advisor', userId: 'user-123', type: 'advisor', outcome: { type: 'generating' } },
    { id: 'gen:user-123', userId: 'user-123', type: 'generationRequest', status: 'queued', targetRole: 'X' },
  ] });
  const handler = loadHandler('custom-advisor', 'custom-advisor', { cosmosContainer: container });
  const res = await handler(makeRequest({ method: 'GET', user: authUser() }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.advisor.outcome.type, 'generating');
  assert.equal(res.jsonBody.generation.status, 'queued');
});

test('custom-advisor: POST notifies the admin on a course request (generating path)', async () => {
  const notified = [];
  const res = await advisorHandler({
    advisor: async () => analysisFor('Quantum Hardware Technician', ['cryogenics', 'qubits']),
    notify: async (payload) => { notified.push(payload); return { sent: true }; },
  })(makeRequest(body()), makeContext());
  assert.equal(res.jsonBody.outcome.type, 'generating');
  assert.equal(notified.length, 1, 'admin notified once');
  assert.equal(notified[0].targetRole, 'Quantum Hardware Technician');
  assert.equal(notified[0].userEmail, 'alice@example.com');
});

test('custom-advisor: a matched request does NOT notify', async () => {
  const notified = [];
  await advisorHandler({
    advisor: async () => analysisFor('AI Application Developer', ['python', 'rag', 'llm apps']),
    notify: async (p) => { notified.push(p); },
  })(makeRequest(body()), makeContext());
  assert.equal(notified.length, 0);
});

test('custom-advisor: GET auto-delivers a now-published course (enroll + matched + clears request)', async () => {
  const container = makeContainer({ seed: [
    { id: 'user-123:advisor', userId: 'user-123', type: 'advisor', outcome: { type: 'generating' },
      analysis: { recommendedRole: 'AI Application Developer', recommendedSkills: ['python', 'rag', 'llm apps'] } },
    { id: 'gen:user-123', userId: 'user-123', type: 'generationRequest', status: 'queued' },
  ] });
  const handler = loadHandler('custom-advisor', 'custom-advisor', { cosmosContainer: container });
  const res = await handler(makeRequest({ method: 'GET', user: authUser() }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.advisor.outcome.type, 'matched');
  assert.equal(res.jsonBody.advisor.outcome.courseSlug, 'ai-app-developer-2026');
  assert.equal(res.jsonBody.advisor.outcome.delivered, 'generated');
  assert.equal(res.jsonBody.generation, null, 'request cleared');
  assert.ok(container._calls.upserts.some((d) => d.id === 'user-123:enroll:ai-app-developer-2026'), 'enrolled');
  assert.ok(container._calls.deletes.includes('gen:user-123'), 'request deleted');
});

test('custom-advisor: GET returns nulls when the user has no plan yet', async () => {
  const handler = loadHandler('custom-advisor', 'custom-advisor', { cosmosContainer: makeContainer() });
  const res = await handler(makeRequest({ method: 'GET', user: authUser() }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.advisor, null);
  assert.equal(res.jsonBody.generation, null);
});

test('custom-advisor: DELETE removes the résumé object + advisor/generation docs', async () => {
  const container = makeContainer({ seed: [
    { id: 'user-123:advisor', userId: 'user-123', type: 'advisor', resumeRef: { bucket: 'tw-resumes', key: 'user-123/r.pdf' } },
    { id: 'gen:user-123', userId: 'user-123', type: 'generationRequest', status: 'queued' },
  ] });
  const deleted = [];
  const handler = loadHandler('custom-advisor', 'custom-advisor', {
    cosmosContainer: container,
    resumes: { putResume: async () => ({}), deleteResume: async (key) => { deleted.push(key); } },
  });
  const res = await handler(makeRequest({ method: 'DELETE', user: authUser() }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.ok, true);
  assert.deepEqual(deleted, ['user-123/r.pdf'], 'résumé object deleted from R2');
  assert.ok(container._calls.deletes.includes('user-123:advisor'), 'advisor doc deleted');
  assert.ok(container._calls.deletes.includes('gen:user-123'), 'generation request deleted');
});

test('custom-advisor: DELETE is a no-op (200) when there is nothing to remove', async () => {
  const handler = loadHandler('custom-advisor', 'custom-advisor', { cosmosContainer: makeContainer() });
  const res = await handler(makeRequest({ method: 'DELETE', user: authUser() }), makeContext());
  assert.equal(res.status, 200);
  assert.equal(res.jsonBody.ok, true);
});

test('custom-advisor: a model refusal returns 422', async () => {
  const res = await advisorHandler({
    advisor: async () => { const e = new Error('refused'); e.code = 'refusal'; throw e; },
  })(makeRequest(body()), makeContext());
  assert.equal(res.status, 422);
  assert.equal(res.jsonBody.error, 'cannot_analyze');
});
