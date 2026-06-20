const { app } = require('@azure/functions');

// POST /api/custom-advisor (TW-64) — Custom Training Advisor intake.
// Auth-gated (SWA route rule + in-function check). Validates the questionnaire +
// consent + résumé PDF, stores the résumé in the private bucket, analyses it with
// Claude, then either MATCHES the user to an existing course (enrolls them) or
// ENQUEUES a course-generation request for the offline pipeline. Lazy-requires
// shared modules inside the handler (the pattern that reliably registers on SWA).

const MAX_RESUME_BYTES = 5 * 1024 * 1024; // 5 MB

app.http('custom-advisor', {
  methods: ['GET', 'POST', 'DELETE'],
  authLevel: 'anonymous', // SWA enforces auth at the route level
  route: 'custom-advisor',
  handler: async (request, context) => {
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    if (!user) return { status: 401, jsonBody: { error: 'not_authenticated' } };

    // DELETE — right to be forgotten: remove the user's résumé + advisor data.
    if (request.method === 'DELETE') {
      try {
        const { getContainer } = require('../shared/cosmos');
        const container = getContainer();
        let advisor = null;
        try { advisor = (await container.item(`${user.userId}:advisor`, user.userId).read()).resource; } catch { advisor = null; }
        if (advisor && advisor.resumeRef && advisor.resumeRef.key) {
          try {
            const { deleteResume } = require('../shared/resumes');
            await deleteResume(advisor.resumeRef.key);
          } catch (e) { context.error('résumé object delete failed', e); }
        }
        for (const id of [`${user.userId}:advisor`, `gen:${user.userId}`]) {
          try { await container.item(id, user.userId).delete(); } catch { /* not present */ }
        }
        return { status: 200, jsonBody: { ok: true } };
      } catch (err) {
        context.error('custom-advisor DELETE error', err);
        return { status: 500, jsonBody: { error: 'server_error' } };
      }
    }

    // GET — the user's saved analysis + any pending generation request (for /account).
    if (request.method === 'GET') {
      try {
        const { getContainer } = require('../shared/cosmos');
        const container = getContainer();
        let advisor = null;
        let generation = null;
        try { advisor = (await container.item(`${user.userId}:advisor`, user.userId).read()).resource; } catch { advisor = null; }
        try { generation = (await container.item(`gen:${user.userId}`, user.userId).read()).resource; } catch { generation = null; }

        // Auto-delivery: if the user is awaiting a generated course and one now in
        // the library matches their stored profile (i.e. their requested course was
        // generated + published), enrol them and flip the status to "matched".
        if (generation && generation.status !== 'ready' && advisor && advisor.analysis) {
          const { allCourses } = require('../shared/catalog');
          const { match } = require('../shared/matcher');
          const m = match(
            { role: advisor.analysis.recommendedRole, skills: advisor.analysis.recommendedSkills },
            allCourses(),
          );
          if (m) {
            const now = new Date().toISOString();
            await container.items.upsert({
              id: `${user.userId}:enroll:${m.courseSlug}`,
              userId: user.userId,
              type: 'enrollment',
              course: m.courseSlug,
              source: 'custom-advisor',
              enrolledAt: now,
            });
            advisor.outcome = { type: 'matched', courseSlug: m.courseSlug, score: m.score, delivered: 'generated' };
            await container.items.upsert(advisor);
            try { await container.item(`gen:${user.userId}`, user.userId).delete(); } catch { /* already gone */ }
            generation = null;
          }
        }

        return { status: 200, headers: { 'cache-control': 'private, no-store' }, jsonBody: { advisor, generation } };
      } catch (err) {
        context.error('custom-advisor GET error', err);
        return { status: 500, jsonBody: { error: 'server_error' } };
      }
    }

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
      const { allCourses, catalogSummary } = require('../shared/catalog');
      const courses = allCourses(); // built-in + published AI-generated courses
      let analysis;
      try {
        analysis = await analyzeResume({ pdfBase64: resumeBase64, questionnaire, catalogText: catalogSummary(courses) });
      } catch (err) {
        if (err && err.code === 'refusal') {
          return { status: 422, jsonBody: { error: 'cannot_analyze' } };
        }
        throw err;
      }

      // Match against the whole reusable library. Consider EVERY role the analysis
      // surfaced (the recommended one + the alternatives), and prefer an existing
      // course over queuing a new-course generation — e.g. a user whose top goal is
      // off-catalog but whose 2nd-choice role we already train for gets matched.
      const { match } = require('../shared/matcher');
      const roleCandidates = [analysis.recommendedRole, ...(analysis.targetRoles || []).map((t) => t.role)]
        .filter(Boolean);
      let m = null;
      for (const role of roleCandidates) {
        const r = match({ role, skills: analysis.recommendedSkills }, courses);
        if (r && (!m || r.score > m.score)) m = r;
      }

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
        // Notify the admin so they can dispatch the generator (best-effort).
        try {
          const { notifyCourseRequest } = require('../shared/notify');
          await notifyCourseRequest({
            userEmail: user.userDetails,
            targetRole: analysis.recommendedRole,
            targetSkills: analysis.recommendedSkills,
          });
        } catch (e) {
          context.error('course-request notify failed', e);
        }
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
