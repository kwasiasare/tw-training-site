// Central site configuration + course catalog + data-driven curriculum helpers.
// Lesson slugs match the Markdown file ids in course-materials/<course>/lessons.

export const SITE = {
  title: 'AI Career Courses',
  tagline: 'Project-based courses that take you to your first AI role.',
  // Where instructor videos are served from in production (Cloudflare R2).
  // Override at build time with PUBLIC_VIDEO_CDN_BASE. Falls back to local /videos in dev.
  videoCdnBase: import.meta.env.PUBLIC_VIDEO_CDN_BASE ?? '/videos',
};

// Operating company (TW-133). Used by the site footer and the contact/feedback
// page. Static — no build-time env override needed, unlike SITE above.
export const COMPANY = {
  name: 'Spreadcom LLC',
  website: 'https://www.spreadcomgh.com',
  email: 'kasare@spreadcomgh.com',
  phone: '+1 (774) 570-0034',
  phoneHref: 'tel:+17745700034',
  location: 'United States',
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

// Cross-course Q&A chatbot (TW-117, Phase 1 / Tier A). Gated behind a build-time
// flag so the global widget stays hidden until its backend (rate limiter +
// ANTHROPIC_API_KEY) is wired in the target environment. Set
// PUBLIC_CHATBOT_ENABLED=true to turn it on.
export const CHATBOT_ENABLED = import.meta.env.PUBLIC_CHATBOT_ENABLED === 'true';

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
    slug: 'data-scientist',
    title: 'Data Scientist Career Accelerator: From Python to Production Insights',
    tagline: 'Aspiring data scientists, analysts, or developers with basic computer literacy who want to transition into a data science role through hands-on, portfolio-building work.',
    blurb: 'A project-based course that takes you from programming and statistics fundamentals to building, evaluating, and communicating machine learning models. You\'ll work with real datasets to build a portfolio of analyses, dashboards, and end-to-end ML projects that prove you\'re ready for a data scientist role.',
    sample: 'dsc-m1-l01-python-essentials-for-data-work',
    accent: '#7c3aed',
  },
  {
    slug: 'ai-app-developer-2026',
    title: 'AI Application Developer: Build and Ship LLM-Powered Apps',
    tagline: 'Aspiring AI Application Developers with basic programming exposure who want to build and deploy real LLM-powered applications and land a job in the field.',
    blurb: 'A hands-on, project-based course that takes you from Python foundations to deploying production-ready AI applications using LLMs, RAG pipelines, autonomous agents, and vector databases. You\'ll build a portfolio of real apps culminating in a deployed capstone project.',
    sample: 'aad-m1-l01-python-essentials-for-ai-developers',
    accent: '#7c3aed',
  },
  {
    slug: 'ai-product-manager',
    title: 'AI Product Management: From Fundamentals to Shipping AI Products',
    tagline: 'Aspiring and transitioning product managers, technical PMs, founders, and analysts who want to lead AI/LLM products and need practical, portfolio-building experience to land an AI Product Manager role.',
    blurb: 'A hands-on, project-based course that prepares you to lead AI and LLM-powered products end to end. You\'ll build AI literacy, master LLM capabilities and limits, craft product strategy and roadmaps, design evaluation frameworks and prompts, manage cross-functional stakeholders, and define metrics that prove impact. By the end, you\'ll have a portfolio-ready AI product spec, roadmap, eval suite, and launch plan.',
    sample: 'apm-m1-l01-how-modern-ai-works-a-no-math-mental-model-for-p',
    accent: '#7c3aed',
  },
  {
    slug: 'ml-engineer',
    title: 'Machine Learning Engineer Bootcamp: From Fundamentals to Production',
    tagline: 'Aspiring Machine Learning Engineers with basic programming exposure who want to bridge résumé gaps and become job-ready for ML engineering roles.',
    blurb: 'A project-based course that builds the practical skills needed to land a Machine Learning Engineer role, covering Python, math foundations, ML algorithms, PyTorch, feature engineering, model training and evaluation, and production-ready data pipelines. Learners build a portfolio of hands-on projects culminating in an end-to-end ML system.',
    sample: 'mle-m1-l01-python-for-ml-numpy-pandas-and-clean-code',
    accent: '#7c3aed',
  },
  {
    slug: 'agentic-ai-engineer',
    title: 'Agentic AI Engineer: Building Production-Ready LLM Agents',
    tagline: 'Python developers and ML practitioners who want to transition into building, orchestrating, and deploying autonomous LLM-powered agents in production.',
    blurb: 'A hands-on, project-based course that takes you from Python-driven LLM API calls to deploying sophisticated multi-agent systems with planning, memory, RAG, and orchestration using LangGraph. You\'ll build a portfolio of working agents culminating in a deployed capstone application.',
    sample: 'age-m1-l01-calling-llm-apis-in-python-completions-chat-and-',
    accent: '#7c3aed',
  },
  {
    slug: 'mlops-engineer',
    title: 'MLOps Engineering: From Models to Production',
    tagline: 'Data scientists, software engineers, and DevOps practitioners who want to transition into an MLOps Engineer role and need practical skills in deploying, automating, and monitoring machine learning systems — including LLMs — in production.',
    blurb: 'A hands-on, project-based course that takes you from containerizing ML workloads to building fully automated, monitored, and cloud-deployed machine learning pipelines — including serving large language models efficiently on GPUs. You\'ll master Docker, Kubernetes, CI/CD, MLflow, infrastructure as code, production monitoring, and modern LLMOps (vLLM, quantization, KServe, GPU-aware scaling) while building a portfolio of deployable systems.',
    sample: 'mlo-m1-l01-setting-up-your-mlops-toolchain-and-workflow',
    accent: '#7c3aed',
  },
  {
    slug: 'junior-digital-marketing',
    title: 'Junior Digital Marketing & Social Media Assistant Bootcamp',
    tagline: 'Aspiring marketers, career changers, and recent graduates with little to no professional experience who want an entry-level digital marketing or social media role.',
    blurb: 'A hands-on, project-based course that builds the practical skills needed to launch a career as a digital marketing and social media assistant. Learners will run real ad campaigns, create engaging content, analyze performance data, and assemble a job-ready portfolio across paid ads, SEO, social media, and email marketing.',
    sample: 'dm-m1-l01-the-digital-marketing-landscape-the-assistant-ro',
    accent: '#7c3aed',
  },
  {
    slug: 'cloud-security-engineer',
    title: 'Cloud Security Engineer & M365 Security Architect: Zero Trust to SOC Automation',
    tagline: 'From M365 admin to senior security architect: Zero Trust, XDR, Purview, Sentinel & SOC automation.',
    blurb: 'A project-based course that bridges the gap between intermediate M365 administration (MD-102/MS-102) and senior security architecture (SC-500). You\'ll design Zero Trust identity perimeters with Entra ID, unify endpoint security with Intune and Defender for Endpoint, govern data and AI with Microsoft Purview, run a cloud SIEM/SOAR with Microsoft Sentinel and KQL, and automate it all with PowerShell, the Microsoft Graph API, and Logic Apps. You finish by building the three portfolio-grade projects hiring managers look for.',
    sample: 'cse-m1-l01-zero-trust-foundations-and-the-security-stack',
    accent: '#0891b2',
  },
  {
    slug: 'vdi-engineer',
    title: 'VDI & End-User Computing Engineer: Azure Virtual Desktop, Windows 365 & Multi-Platform VDI',
    tagline: 'IT professionals — sysadmins, helpdesk tier 2/3, M365/Azure administrators — who want to move into a VDI / End-User Computing Engineer role. Assumes basic Windows administration and some Azure familiarity; prepares you for AZ-140 (Microsoft Certified: Azure Virtual Desktop Specialty) and gives you the cross-platform grounding for Citrix CCA-V and Omnissa OCA-H paths.',
    blurb: 'A project-based course that takes working IT professionals from VDI fundamentals to production-grade virtual desktop engineering. You\'ll master the vendor-neutral core every EUC engineer needs — architecture, display protocols, profile management, licensing, and platform selection across Azure Virtual Desktop, Windows 365, Citrix DaaS, and Omnissa Horizon — then go deep on Azure Virtual Desktop mapped to all four AZ-140 exam domains: planning and deploying host pools, images, and autoscaling; securing access with Entra ID and Conditional Access; delivering user environments with FSLogix and app attach; and monitoring, maintaining, and troubleshooting at scale. You finish with portfolio-grade capstones: a full AVD design-and-build and a multi-platform migration assessment hiring managers actually ask for.',
    sample: 'vdi-m1-l01-what-is-vdi-and-euc',
    accent: '#4f46e5',
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
