const { app } = require('@azure/functions');
const crypto = require('crypto');

// GET /api/certificate?course=<slug> (TW-69) — completion certificate.
// Auth-gated by the /api/* route rule (re-checked here). Reports whether the
// signed-in user has completed every lesson in the course (lesson totals come from
// the bundled lesson index; completions from their Cosmos progress records). On
// first eligibility it issues + persists a stable certificate (id + issue date) so
// the same certificate is returned on every later view.

const SLUG_RE = /^[a-z0-9-]+$/i;

app.http('certificate', {
  methods: ['GET'],
  authLevel: 'anonymous', // SWA enforces auth at the route level
  route: 'certificate',
  handler: async (request, context) => {
    const { getUser } = require('../shared/principal');
    const user = getUser(request);
    // 403 (not 401) so SWA's global 401 -> /signin redirect doesn't turn the
    // client's fetch into the sign-in HTML page (same reason as video.js).
    if (!user) return { status: 403, jsonBody: { error: 'login_required' } };

    const course = (request.query.get('course') || '').trim();
    if (!course || course.length > 80 || !SLUG_RE.test(course)) {
      return { status: 400, jsonBody: { error: 'bad_course' } };
    }

    try {
      const { countLessons, getLesson } = require('../shared/lessons');
      const totalLessons = countLessons(course);
      if (totalLessons === 0) return { status: 404, jsonBody: { error: 'unknown_course' } };

      const { getContainer } = require('../shared/cosmos');
      const container = getContainer();

      // Completed lessons for this course + the user's profile (for the name).
      const { resources } = await container.items
        .query({
          query: 'SELECT c.type, c.course, c.status, c.lesson, c.displayName FROM c WHERE c.userId = @u',
          parameters: [{ name: '@u', value: user.userId }],
        })
        .fetchAll();

      const completedSet = new Set();
      let displayName = '';
      resources.forEach((r) => {
        if (r.type === 'profile' && r.displayName) displayName = r.displayName;
        if (r.type === 'progress' && r.course === course && r.status === 'completed' && r.lesson) {
          // Count only lessons that really belong to this course. progress.js
          // validates on write, but this also disarms records stored before
          // that check existed (or after a lesson is renamed/removed).
          const meta = getLesson(r.lesson);
          if (meta && meta.course === course) completedSet.add(r.lesson);
        }
      });
      const completedLessons = completedSet.size;

      // Issued certificates are durable (TW-98 product decision, 2026-07-03):
      // a course may gain lessons or rename them after issuance, which would
      // drop the recomputed completion below 100%. An already-persisted
      // certificate therefore short-circuits the eligibility gate.
      const certId = `${user.userId}:cert:${course}`;
      let cert = null;
      try { cert = (await container.item(certId, user.userId).read()).resource; } catch { cert = null; }

      if (!cert && completedLessons < totalLessons) {
        return {
          status: 200,
          headers: { 'cache-control': 'private, no-store' },
          jsonBody: { eligible: false, completedLessons, totalLessons },
        };
      }

      const { allCourses } = require('../shared/catalog');
      const courseMeta = allCourses().find((c) => c.slug === course);
      const courseTitle = (courseMeta && courseMeta.title) || course;
      const learner = displayName || (user.userDetails || '').split('@')[0] || user.userDetails || 'Learner';

      // Issue once, then return the same certificate on every subsequent view.
      if (!cert) {
        cert = {
          id: certId,
          userId: user.userId,
          userDetails: user.userDetails,
          type: 'certificate',
          course,
          serial: crypto.randomUUID().slice(0, 8).toUpperCase(),
          issuedAt: new Date().toISOString(),
        };
        try { await container.items.upsert(cert); } catch (e) { context.error('cert persist failed', e); }
      }

      return {
        status: 200,
        headers: { 'cache-control': 'private, no-store' },
        jsonBody: {
          eligible: true,
          course,
          courseTitle,
          learner,
          completedLessons,
          totalLessons,
          serial: cert.serial,
          issuedAt: cert.issuedAt,
        },
      };
    } catch (err) {
      context.error('certificate error', err);
      return { status: 500, jsonBody: { error: 'server_error' } };
    }
  },
});
