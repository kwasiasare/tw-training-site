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

function advisorHandler({ container, advisor, resumes } = {}) {
  return loadHandler('custom-advisor', 'custom-advisor', {
    cosmosContainer: container || makeContainer(),
    advisor: advisor || (async () => analysisFor('AI Application Developer', ['python', 'rag', 'llm apps'])),
    resumes,
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
  assert.equal(res.jsonBody.outcome.courseSlug, 'dami-ai-career');
  assert.equal(stored.length, 1, 'résumé was stored before analysis');
  const ids = container._calls.upserts.map((d) => d.id);
  assert.ok(ids.includes('user-123:enroll:dami-ai-career'), 'enrollment created');
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

test('custom-advisor: a model refusal returns 422', async () => {
  const res = await advisorHandler({
    advisor: async () => { const e = new Error('refused'); e.code = 'refusal'; throw e; },
  })(makeRequest(body()), makeContext());
  assert.equal(res.status, 422);
  assert.equal(res.jsonBody.error, 'cannot_analyze');
});
