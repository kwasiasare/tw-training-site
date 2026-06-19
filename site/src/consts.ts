// Central site configuration + course catalog + data-driven curriculum helpers.
// Lesson slugs match the Markdown file ids in course-materials/<course>/lessons.

export const SITE = {
  title: 'AI Career Courses',
  tagline: 'Project-based courses that take you to your first AI role.',
  // Where instructor videos are served from in production (Cloudflare R2).
  // Override at build time with PUBLIC_VIDEO_CDN_BASE. Falls back to local /videos in dev.
  videoCdnBase: import.meta.env.PUBLIC_VIDEO_CDN_BASE ?? '/videos',
};

// Authentication (Entra External ID) is gated behind a build-time flag so the
// sign-in UI only appears once the provider is wired. Set PUBLIC_AUTH_ENABLED=true
// (a GitHub Actions variable) to turn it on.
export const AUTH_ENABLED = import.meta.env.PUBLIC_AUTH_ENABLED === 'true';

// Application Insights (TW-42). Client telemetry loads only when a connection
// string is provided at build time via the PUBLIC_APPINSIGHTS_CONNECTION_STRING
// GitHub Actions variable. The ingestion key it contains is write-only and is
// intentionally embeddable in client pages. Empty in local dev → telemetry off.
export const APPINSIGHTS_CONNECTION_STRING =
  import.meta.env.PUBLIC_APPINSIGHTS_CONNECTION_STRING ?? '';

// Custom Training Advisor (TW-61). Gated behind a build-time flag so the feature
// stays hidden until its backend (résumé bucket + ANTHROPIC_API_KEY) is wired in
// the target environment. Set PUBLIC_CUSTOM_ADVISOR_ENABLED=true to turn it on.
export const CUSTOM_ADVISOR_ENABLED =
  import.meta.env.PUBLIC_CUSTOM_ADVISOR_ENABLED === 'true';

// Course-level catalog metadata. The per-module/lesson tree is derived from the
// lessons themselves (see courseModules / courseOrder below) so it never drifts.
export type Course = {
  slug: string;
  title: string;
  tagline: string;
  blurb: string;
  sample: string; // a representative lesson slug
  accent: string;
};

export const COURSES: Course[] = [
  {
    slug: 'dami-ai-career',
    title: 'Beginner → AI Application Developer',
    tagline: 'From beginner to your first AI Application Developer role in six months.',
    blurb:
      'A project-based, self-study path for a beginner with little coding: Python, data & SQL, LLM apps and RAG, portfolio projects, deployment, and interview prep.',
    sample: 'm1-l06-functions',
    accent: '#4f46e5',
  },
  {
    slug: 'kwasi-GenAI',
    title: 'Cloud Engineer → Applied GenAI Engineer',
    tagline: 'Turn cloud, DevOps & security skills into an applied GenAI role.',
    blurb:
      'A deliverable-driven roadmap: direct API fluency, retrieval-augmented generation, agents & orchestration, and production engineering — leaning into your security edge.',
    sample: 'g1-l01-how-llms-behave',
    accent: '#0ea5e9',
  },
  {
    slug: 'helpdesk-tier1-2',
    title: 'Helpdesk: No Experience → Tier 2',
    tagline: 'From zero PC experience to a job-ready IT support technician in six months.',
    blurb:
      'A hands-on, 60-lesson path built around CompTIA A+, Network+, Microsoft MD-102 and MS-102: PC hardware, networking, Windows support, the helpdesk craft (ITIL & ticketing), modern endpoint management, and AI tools for resolving real endpoint problems.',
    sample: 'hd4-l04-troubleshooting-methodology',
    accent: '#16a34a',
  },
  {
    slug: 'helpdesk-tier3-advanced',
    title: 'Helpdesk Tier 3: Advanced Endpoint Engineering',
    tagline: 'Step up from Tier 2 to senior escalation and endpoint engineering.',
    blurb:
      'An advanced follow-on for working technicians: deep root-cause analysis, PowerShell & Microsoft Graph automation at scale, advanced endpoint security & identity, and AIOps with agentic automation for modern endpoint operations.',
    sample: 'ht4-l05-building-an-ai-triage-agent',
    accent: '#db2777',
  },
  {
    slug: 'cx-validation-test',
    title: 'AI Application Developer: Building Production-Ready LLM Apps with RAG',
    tagline: 'Aspiring AI Application Developers with basic programming exposure who want to build and ship real LLM-powered applications.',
    blurb: 'A hands-on, project-based course that takes you from Python fundamentals to deploying retrieval-augmented generation (RAG) applications powered by large language models. You\'ll build a portfolio-ready AI app that answers questions over custom documents using embeddings, a vector store, and an LLM, while applying best practices in prompt design, evaluation, and deployment.',
    sample: 'vt1-m1-l01-capstone-build-and-deploy-a-document-q-a-rag-app',
    accent: '#7c3aed',
  },
];

export function getCourse(slug: string): Course | undefined {
  return COURSES.find((c) => c.slug === slug);
}

// Minimal shape we need from a content-collection entry.
export type LessonEntry = {
  id: string;
  data: { course: string; month: number; monthTitle: string; lesson: number; title: string };
};

export type Module = {
  month: number;
  monthTitle: string;
  lessons: LessonEntry[];
};

// Group a course's lessons into ordered modules (by month, then lesson number).
export function courseModules(all: LessonEntry[], courseSlug: string): Module[] {
  const byMonth = new Map<number, Module>();
  for (const t of all) {
    if (t.data.course !== courseSlug) continue;
    let m = byMonth.get(t.data.month);
    if (!m) {
      m = { month: t.data.month, monthTitle: t.data.monthTitle, lessons: [] };
      byMonth.set(t.data.month, m);
    }
    m.lessons.push(t);
  }
  const modules = [...byMonth.values()].sort((a, b) => a.month - b.month);
  for (const m of modules) m.lessons.sort((a, b) => a.data.lesson - b.data.lesson);
  return modules;
}

// Flat, ordered list of a course's lesson slugs (for prev/next navigation).
export function courseOrder(all: LessonEntry[], courseSlug: string): string[] {
  return courseModules(all, courseSlug).flatMap((m) => m.lessons.map((l) => l.id));
}

export function courseLessonCount(all: LessonEntry[], courseSlug: string): number {
  return all.filter((t) => t.data.course === courseSlug).length;
}

export function videoUrl(file?: string): string | undefined {
  if (!file) return undefined;
  if (file.startsWith('http')) return file;
  return `${SITE.videoCdnBase}/${file}`;
}
