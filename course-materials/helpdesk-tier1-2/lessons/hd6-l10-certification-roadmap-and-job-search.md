---
course: helpdesk-tier1-2
title: Certification roadmap and job-search playbook
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 10
summary: Map the certification ladder from CompTIA A+ to Microsoft MS-102 and choose what to chase next,
  then turn your skills into a resume, portfolio, and interview answers that get you hired.
objectives:
- Order the core certifications and explain which goal each one serves
- Choose your next certification based on the role you want
- Write quantified, tailored resume bullets that map to a job description
- Build a portfolio from your home lab and the projects in this course
- Answer behavioral questions with the STAR method
- Talk confidently about your troubleshooting methodology in an interview
video: hd6-l10-certification-roadmap-and-job-search.mp4
quiz:
- q: Which certification is the best fit for a tech whose target role is administering Microsoft 365 tenants
    — users, licensing, Exchange Online, and security?
  options:
  - CompTIA A+
  - Microsoft MS-102
  - Microsoft AI-900
  - CompTIA Network+
  answer: 1
  why: MS-102 (Microsoft 365 Administrator) is purpose-built for managing M365 tenants — identity, licensing,
    Exchange Online, and security and compliance — which is exactly the role described.
- q: You are brand new with no IT experience. Which certification is the recommended foundation to start
    with?
  options:
  - CompTIA A+
  - Microsoft MS-102
  - Microsoft MD-102
  - Microsoft AI-900
  answer: 0
  why: CompTIA A+ is the entry-level foundation covering hardware, operating systems, and core troubleshooting
    — it is the standard starting point before more specialised exams.
- q: Which certification best validates managing and securing physical and virtual Windows devices with
    Intune (endpoint/device administration)?
  options:
  - CompTIA Network+
  - Microsoft AI-900
  - Microsoft MD-102
  - CompTIA A+
  answer: 2
  why: MD-102 (Endpoint Administrator) focuses on deploying, configuring, and securing Windows endpoints
    with Microsoft Intune — the device-admin specialisation.
- q: A candidate wants a low-effort credential that signals AI literacy as a differentiator, not a deep
    specialism. Which fits best?
  options:
  - Microsoft MS-102
  - CompTIA Network+
  - CompTIA A+
  - Microsoft AI-900
  answer: 3
  why: AI-900 (Azure AI Fundamentals) is a fundamentals-level exam that demonstrates AI literacy — a quick,
    modern differentiator on a helpdesk or admin resume.
- q: Why should you tailor your resume to each job description rather than sending one generic version?
  answer: Because mirroring the job description's key skills and keywords shows you fit the specific role,
    helps you pass automated applicant-tracking-system (ATS) filters, and lets the hiring manager see
    your most relevant experience first.
  why: Generic resumes get filtered out by ATS keyword matching and fail to highlight the experience that
    matters for that particular role; tailoring directly raises your callback rate.
- q: What does the STAR method stand for, and why is it useful in interviews?
  answer: STAR stands for Situation, Task, Action, Result. It is useful because it structures a behavioral
    answer into a clear story — the context, what you needed to do, what you specifically did, and the
    measurable outcome — so the interviewer can follow your thinking and see your impact.
  why: Behavioral questions ('Tell me about a time...') reward concrete, structured stories; STAR keeps
    you from rambling and ensures you end on a result that proves your value.
resources:
- label: CompTIA A+ — official certification page
  url: https://www.comptia.org/certifications/a
- label: Microsoft MD-102 — Endpoint Administrator
  url: https://learn.microsoft.com/en-us/credentials/certifications/modern-desktop/
- label: Microsoft MS-102 — Microsoft 365 Administrator exam
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
- label: Microsoft AI-900 — Azure AI Fundamentals
  url: https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/
---

## The certification ladder, and why order matters

Certifications are not a checklist — they are a **ladder** that signals a story to employers. Each rung proves a capability the next role expects. The trick is to climb in an order that matches the job you actually want, not to collect badges for their own sake.

Here is the ladder this course points you toward:

```text
  AI-900  (AI literacy differentiator — bolt on anytime)
     ^
  MS-102  (Microsoft 365 Administrator)  <-- your current target
     ^
  MD-102  (Endpoint / device admin with Intune)
     ^
  Network+  (networking foundations)
     ^
  A+  (hardware, OS, core troubleshooting — the base)
```

## Which cert to chase, and when

**CompTIA A+** is the foundation. If you are brand new, start here: hardware, operating systems, and the troubleshooting mindset every helpdesk role assumes. The current exam series is **220-1201 (Core 1) and 220-1202 (Core 2)** — book those codes; the older 220-1101/1102 series retired in September 2025. **CompTIA Network+** (current exam **N10-009**) is the natural second step — DNS, DHCP, subnets, and the network knowledge that turns "it's broken" into "it's a DNS issue."

From there you specialise. **Microsoft MD-102 (Endpoint Administrator)** validates deploying and securing Windows devices with **Intune** — ideal if you want a device-management or modern-desktop role. **Microsoft MS-102 (Microsoft 365 Administrator)** is your current target: tenant identity, licensing, Exchange Online, and security and compliance. It maps directly to the Tier 2 / M365 admin work you have practiced all month.

**Microsoft AI-900 (Azure AI Fundamentals)** is the differentiator. It is a fundamentals exam, not a deep specialism, but on a 2026 resume it signals **AI literacy** — and it is a quick win you can bolt on at any point.

## Resume and CV: prove it, don't claim it

A resume that says "good at troubleshooting" is invisible. A resume that **quantifies** is hired. Tailor every application to the **job description (JD)**: mirror its keywords so you pass the **applicant-tracking system (ATS)**, and list your certifications near the top.

Use this bullet template:

```text
[Action verb] + [what you did] + [tool/tech] + [measurable result]

Examples:
- Resolved 40+ Tier 1 tickets per week in Microsoft 365,
  maintaining a 96% first-contact-resolution rate.
- Migrated 120 mailboxes to Exchange Online with zero data loss.
- Cut onboarding time 30% by automating user setup in Intune.
```

## Build a portfolio that backs it up

Certs say you can pass an exam; a **portfolio** shows you can do the work. Build a **home lab** — a Microsoft 365 trial tenant (or a 30-day Microsoft 365 Business Premium/Enterprise trial — the free developer sandbox is now restricted to eligible accounts), a couple of test users, an Intune policy or two. Document each project: the problem, your steps, screenshots, the result. The labs and tickets from this course are portfolio pieces already — write them up. A simple repo or one-page site that says "here is what I built and how" beats a wall of buzzwords.

## Interview prep: methodology over memorisation

Expect two flavours of question. **Behavioral** questions ("Tell me about a time a user was frustrated") want a story — answer with **STAR**: Situation, Task, Action, Result, ending on a measurable outcome. **Technical** questions ("A user can't reach a network share — walk me through it") want your **troubleshooting methodology**: gather information, establish a theory, test it, fix, verify, document. They care less about the single right answer and more about how you *think*.

Practice saying out loud: "First I'd reproduce it, then check what changed, then isolate the layer — user, device, network, or service." That sentence wins interviews.

## Your task

Three steps. First, **pick your next certification** and write one sentence on why it fits your target role. Second, **draft three quantified resume bullets** using the template above, drawn from real work or your course labs. Third, **outline a portfolio** — list three projects you could document this month, each with a one-line problem statement.
