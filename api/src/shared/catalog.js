'use strict';

// Course library used by the Custom Training Advisor (TW-61).
//
// Each entry carries a `targetProfile` (role + level + the key skills the course
// teaches) used by the matcher (matcher.js) to decide whether an analysed user
// can be served an existing course vs. having a new one generated. The built-in
// courses are seeded here; AI-generated courses are appended at publish time
// (TW-66) with the same shape. `summary` is compact context passed to Claude.

const BUILTIN_COURSES = [
  {
    slug: 'dami-ai-career',
    title: 'Beginner → AI Application Developer',
    summary:
      'Project-based path from little/no coding to a first AI Application Developer role: Python, data & SQL, LLM apps and RAG, agents, deployment, portfolio + interview prep.',
    targetProfile: {
      role: 'AI Application Developer',
      level: 'entry',
      skills: ['python', 'sql', 'data', 'llm apps', 'rag', 'agents', 'apis', 'deployment', 'portfolio'],
    },
  },
  {
    slug: 'kwasi-GenAI',
    title: 'Cloud Engineer → Applied GenAI Engineer',
    summary:
      'For someone with cloud/DevOps/security skills moving into applied GenAI: direct API fluency, retrieval-augmented generation, agents & orchestration, production engineering.',
    targetProfile: {
      role: 'Applied GenAI Engineer',
      level: 'mid',
      skills: ['cloud', 'devops', 'security', 'llm apis', 'rag', 'agents', 'orchestration', 'production engineering'],
    },
  },
  {
    slug: 'helpdesk-tier1-2',
    title: 'Helpdesk: No Experience → Tier 2',
    summary:
      'Zero PC experience to a job-ready IT support technician: CompTIA A+, Network+, MD-102/MS-102, PC hardware, networking, Windows support, ticketing/ITIL, endpoint management.',
    targetProfile: {
      role: 'IT Support / Helpdesk Tier 2',
      level: 'entry',
      skills: ['pc hardware', 'networking', 'windows', 'comptia a+', 'network+', 'ticketing', 'itil', 'endpoint management', 'm365'],
    },
  },
  {
    slug: 'helpdesk-tier3-advanced',
    title: 'Helpdesk Tier 3: Advanced Endpoint Engineering',
    summary:
      'Tier 2 → senior escalation / endpoint engineering: deep root-cause analysis, PowerShell & Microsoft Graph automation, advanced endpoint security & identity, AIOps.',
    targetProfile: {
      role: 'Tier 3 / Endpoint Engineer',
      level: 'advanced',
      skills: ['root cause analysis', 'powershell', 'microsoft graph', 'automation', 'endpoint security', 'identity', 'aiops'],
    },
  },
];

// Compact catalog text handed to Claude so recommendations map to real courses.
function catalogSummary(courses = BUILTIN_COURSES) {
  return courses
    .map((c) => `- ${c.slug} — ${c.title} (target: ${c.targetProfile.role}). ${c.summary}`)
    .join('\n');
}

module.exports = { BUILTIN_COURSES, catalogSummary };
