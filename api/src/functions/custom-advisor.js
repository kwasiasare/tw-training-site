const { app } = require('@azure/functions');

// POST /api/custom-advisor (TW-64) — Custom Training Advisor intake.
// Auth-gated (SWA route rule + in-function check). Validates the questionnaire +
// consent + résumé PDF, stores the résumé in the private bucket, analyses it with
// Claude, then either MATCHES the user to an existing course (enrolls them) or
// ENQUEUES a course-generation request for the offline pipeline. Lazy-requires
// shared modules inside the handler (the pattern that reliably registers on SWA).

const MAX_RESUME_BYTES = 5 * 1024 * 1024; // 5 MB

app.http('custom-advisor', {
  methods: ['POST'],
  authLevel: 'anonymous', // SWA enforces auth at the route level
  route: 'custom-advisor',
  handler: async (request, context) => {
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    if (!user) return { status: 401, jsonBody: { error: 'not_authenticated' } };

    try {
      const body = await request.json().catch(() => ({}));
      const questionnaire = body.questionnaire || {};
      const consent = body.consent === true;
      const resumeBase64 = typeof body.resumeBase64 === 'string' ? body.resumeBase64 : '';

      if (!consent) return { status: 400, jsonBody: { error: 'consent_required' } };
      if (!questionnaire.targetOutcome) return { status: 400, jsonBody: { error: 'questionnaire_incomplete' } };
      if (!resumeBase64) return { status: 400, jsonBody: { error: 'resume_required' } };

      const buf = Buffer.from(resumeBase64, 'base64');
      if (buf.length < 5 || buf.length > MAX_RESUME_BYTES) {
        return { status: 400, jsonBody: { error: 'resume_size' } };
      }
      if (buf.slice(0, 5).toString('latin1') !== '%PDF-') {
        return { status: 400, jsonBody: { error: 'resume_not_pdf' } };
      }

      // Store the résumé (private bucket) before spending an AI call.
      const { putResume } = require('../shared/resumes');
      const resumeRef = await putResume(user.userId, buf);

      // Analyse with Claude.
      const { analyzeResume } = require('../shared/advisor');
      const { BUILTIN_COURSES, catalogSummary } = require('../shared/catalog');
      let analysis;
      try {
        analysis = await analyzeResume({ pdfBase64: resumeBase64, questionnaire, catalogText: catalogSummary() });
      } catch (err) {
        if (err && err.code === 'refusal') {
          return { status: 422, jsonBody: { error: 'cannot_analyze' } };
        }
        throw err;
      }

      // Match against the library, else enqueue a generation request.
      const { match } = require('../shared/matcher');
      const m = match(
        { role: analysis.recommendedRole, skills: analysis.recommendedSkills },
        BUILTIN_COURSES,
      );

      const { getContainer } = require('../shared/cosmos');
      const container = getContainer();
      const now = new Date().toISOString();

      let outcome;
      if (m) {
        outcome = { type: 'matched', courseSlug: m.courseSlug, score: m.score };
        await container.items.upsert({
          id: `${user.userId}:enroll:${m.courseSlug}`,
          userId: user.userId,
          type: 'enrollment',
          course: m.courseSlug,
          source: 'custom-advisor',
          enrolledAt: now,
        });
      } else {
        outcome = { type: 'generating' };
        await container.items.upsert({
          id: `gen:${user.userId}`,
          userId: user.userId,
          type: 'generationRequest',
          status: 'queued',
          targetRole: analysis.recommendedRole,
          targetSkills: analysis.recommendedSkills,
          requestedAt: now,
        });
      }

      await container.items.upsert({
        id: `${user.userId}:advisor`,
        userId: user.userId,
        type: 'advisor',
        createdAt: now,
        consent: true,
        resumeRef,
        questionnaire,
        analysis,
        outcome,
      });

      return {
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: { analysis, outcome },
      };
    } catch (err) {
      context.error('custom-advisor error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});
