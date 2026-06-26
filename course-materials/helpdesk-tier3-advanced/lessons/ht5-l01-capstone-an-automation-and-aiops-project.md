---
course: helpdesk-tier3-advanced
title: 'Capstone: Build an Automation and AIOps Project'
month: 5
monthTitle: Capstone & Career Launch
lesson: 1
summary: 'This is the project that proves you are a systems engineer, not a ticket-closer. You will scope
  and build one portfolio-grade capstone drawn straight from the course: either a PowerShell and Microsoft
  Graph automation that operates at fleet scale, or a monitoring and agentic remediation runbook that
  detects, triages, gates, and fixes a real endpoint problem. You will work to an explicit rubric and
  a clear ''done'' bar so the result is reviewable evidence, not a half-finished script. The deliverable
  is a public repository with safe, idempotent, least-privilege code, a design document that justifies
  every guardrail, and quantified results you can put on a resume. Finish this and you have the single
  artifact that anchors every interview in the rest of the module.'
objectives:
- Scope a capstone with a real problem statement, a measurable outcome, and a defined blast radius
- Choose between a Graph-at-scale automation track and a monitoring/agentic remediation track and justify
  the choice
- Architect the solution as detect, decide, act, verify, and report stages with a guardrail on every action
- 'Apply the safety pattern: ShouldProcess dry runs, idempotency, retry with backoff, least-privilege
  scopes, ring rollout'
- Define the 'done' bar against an explicit rubric covering correctness, safety, documentation, and measurable
  impact
- Capture baseline and after metrics (MTTR, hours saved, devices at scale) that become quantified resume
  bullets
video: ht5-l01-capstone-an-automation-and-aiops-project.mp4
quiz:
- q: What separates a portfolio-grade capstone from a throwaway script a hiring manager will ignore?
  options:
  - It uses the largest possible number of Graph endpoints
  - It states a real problem, ships safe and idempotent code, justifies every guardrail in a design doc,
    and reports a measurable outcome
  - It runs only once on a single device with no documentation
  - It is written in as few lines as possible to look clever
  answer: 1
  why: Reviewers buy judgment and outcomes. A capstone that names the business problem, ships safe least-privilege
    code, explains why each control exists, and quantifies the result demonstrates exactly the engineering
    maturity a Tier 3 or systems engineering role requires, where raw line count or endpoint count proves
    nothing.
- q: You pick the Graph-at-scale automation track. Which problem is the strongest capstone candidate?
  options:
  - Manually renaming three devices in the Intune portal
  - Disabling all Conditional Access policies to see what breaks
  - A one-off query that prints every user to the screen
  - An unattended runbook that finds non-compliant or stale Windows devices across the fleet, remediates
    them idempotently behind an approval/pilot gate, and reports results to a dashboard
  answer: 3
  why: A strong automation capstone operates at fleet scale, makes a safe and idempotent change behind
    a gate, and produces a report. A manual portal action or a single read query shows no engineering,
    and disabling controls is reckless rather than a demonstration of judgment.
- q: Which sequence correctly orders the stages your capstone should follow?
  options:
  - Act on the whole fleet, then collect telemetry, then decide if it worked
  - Detect (read-only) -> decide (the rule) -> act (scoped, gated) -> verify/rollback -> report and audit
  - Report first, then detect, then never act
  - Decide, act everywhere, then delete the logs
  answer: 1
  why: Professional automation flows from read-only detection, through an explicit decision rule, into
    a scoped and gated action, followed by verification with rollback, and ends in a report and audit
    trail. Acting before you detect or verify is how a single bad run becomes a fleet-wide incident.
- q: Why must every state-changing action in the capstone be idempotent and run behind ShouldProcess with
    a pilot ring?
  options:
  - Because a -WhatIf dry run and a small pilot prove the logic while the blast radius is tiny, and idempotency
    means a re-run cannot duplicate or compound damage
  - Because Microsoft Graph refuses to run otherwise
  - Because it makes the script run faster
  - Because it removes the need for any logging
  answer: 0
  why: Endpoint automation has high blast radius. Previewing with -WhatIf and piloting on a small ring
    catches mistakes while impact is contained, and idempotency guarantees that re-running the same job
    leaves an already-healthy device unchanged rather than creating duplicates or errors.
- q: What is the right 'done' bar for the capstone before you call it portfolio-ready?
  options:
  - It compiled once on your laptop
  - It has more than 500 lines of code
  - Code is safe, idempotent, and least-privilege; a design doc justifies every guardrail; a second run
    changes nothing already healthy; and you have baseline-vs-after metrics
  - A colleague said it looked fine without running it
  answer: 2
  why: 'The ''done'' bar is evidence of engineering judgment: provably safe and idempotent code, documented
    guardrail justifications, a demonstrated idempotent re-run, and quantified impact. Line count or an
    unverified glance proves none of those things.'
- q: In two to four sentences, write the problem statement and measurable outcome for a capstone you would
    build, and name one guardrail you would justify.
  answer: 'Problem: across our 4,000-device Windows fleet, roughly 6 percent fall out of Intune compliance
    each month and are remediated by hand, costing the team about 20 hours and leaving devices non-compliant
    for days. Outcome: an unattended Graph runbook detects non-compliant devices daily, tags them into
    a pilot ring, runs an idempotent remediation behind an approval gate, and reports results, targeting
    a reduction in mean-time-to-remediate from days to under an hour and recovering roughly 18 hours a
    month. Guardrail: every action runs behind ShouldProcess with a pilot ring first, because the change
    touches device state at scale and a -WhatIf dry run plus a small ring contains any mistake before
    it reaches the whole fleet.'
  why: A strong answer pairs a quantified problem with a measurable outcome and names a guardrail with
    a one-line justification tied to blast radius. That problem-outcome-guardrail framing is exactly what
    turns a script into portfolio evidence and a resume bullet.
resources:
- label: Microsoft Learn - Microsoft Graph PowerShell SDK overview
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/overview
- label: Microsoft Learn - Remediations in Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations
- label: Microsoft Learn - Manage runbooks in Azure Automation
  url: https://learn.microsoft.com/en-us/azure/automation/manage-runbooks
- label: Microsoft Learn - Microsoft Graph throttling guidance
  url: https://learn.microsoft.com/en-us/graph/throttling
---

## The deliverable: one project that proves you can engineer

Everything in this course has been building toward a single artifact: a project a hiring manager can open, read, and believe. This capstone is not a tutorial to follow line by line. It is a brief. You will scope, build, and document **one** portfolio-grade automation or AIOps project that solves a real Tier 3 problem in your environment (or a realistic lab) end to end. Done well, it becomes the centre of your portfolio, the story you tell in interviews, and the source of two or three quantified resume bullets. Done poorly, it is another script in a folder no one will ever read. The difference is entirely in scoping, safety, and evidence.

## Choose your track

Pick the track that matches the role you are targeting and the skills you most want to prove.

**Track A - PowerShell and Graph at scale.** Build an unattended automation that operates across the whole fleet. Classic candidates: find every Windows device that has not synced with Intune in 30 days, tag it into a remediation group, trigger a sync, and report; or audit Entra ID for stale guest accounts, disabled-but-licensed users, or risky sign-ins and remediate on a schedule; or drive an Autopilot/provisioning workflow that assigns group tags and configuration profiles from a source of truth. This track proves **automation engineering**: Microsoft Graph, the PowerShell SDK, idempotency, error handling, and managed-identity runbooks.

**Track B - Monitoring and agentic remediation.** Build a runbook that closes the loop from signal to safe fix. Pull endpoint telemetry (Intune, Endpoint Analytics, or Log Analytics), correlate it with KQL, generate an evidence-grounded recommendation, route it through a **human approval gate**, then run a scoped, verified remediation and audit the whole chain. This track proves **AIOps and reliability engineering**: observability, KQL, gated automation, and guardrail design.

Either track is hireable. What is not hireable is a project with no problem statement, no safety, and no result. Choose one, go deep, and finish it.

## Scope it like an engineer

Before you write a line of code, write three sentences:

1. **The problem.** What hurts today, and how much? *"~6% of our 4,000 Windows devices fall out of compliance monthly and are fixed by hand, costing ~20 hours and leaving devices exposed for days."* Quantify it; the number becomes your baseline.
2. **The outcome.** What will be true when this works? *"Mean-time-to-remediate drops from days to under an hour; ~18 hours a month recovered; zero unapproved fleet changes."*
3. **The blast radius.** What is the worst this can touch, and how do you contain it? *"Writes to device group membership and triggers syncs; contained by a pilot ring and an approval gate."*

If you cannot write those three sentences, you are not ready to build. This is the senior skill the whole course has been teaching: reason about failure *before* you touch the fleet.

## Architect every action with a guardrail

Whatever the track, the architecture is the same one-directional flow, and every arrow carries a guardrail:

```text
[Detect]    read-only: pull current state, filter server-side
   v
[Decide]    the explicit rule that separates healthy from unhealthy
   v
[Act]       scoped, idempotent, behind ShouldProcess + pilot ring
   v
[Verify]    confirm the fix; roll back on failure
   v
[Report]    machine-readable JSON for systems + one-line human summary
   +
[Audit]     signal -> evidence -> approval -> action -> outcome
```

The safety pattern that makes this professional is non-negotiable: **`SupportsShouldProcess`** so every change has a `-WhatIf` dry run; **idempotency** so a re-run on an already-healthy device does nothing; **retry with exponential backoff and `Retry-After` handling** so Graph throttling does not break the job; **least-privilege scopes** (grant only the exact application permissions the workflow needs, authenticate unattended runs with a **managed identity**, never a stored secret); and **ring rollout** so you pilot on a small group before the fleet. A senior engineer can attach a one-line justification to each control. *If you cannot justify a guardrail, you do not yet understand the risk it manages.*

## The rubric and the 'done' bar

Score your own capstone against this rubric before you publish it. Aim to satisfy every row.

```text
Correctness   Solves the stated problem; detect/decide logic is accurate
Safety        ShouldProcess, idempotent, retry/backoff, least privilege, ring rollout
Scale         Operates across the fleet, not one device; handles paging and throttling
Documentation Design doc: problem, architecture, guardrail justifications, how to run/test
Evidence      Baseline-vs-after metrics; a demo or screenshots proving it works
Reviewability Clean repo, README, pinned module versions, no secrets in source
```

The **'done' bar** is concrete and testable: the code runs safely end to end; a **second run changes nothing already healthy** (proving idempotency); a design doc justifies every guardrail; the repository is public, clean, and secret-free; and you have **before-and-after numbers**. When all of that is true, and not before, the capstone is portfolio-ready.

## Capture the metrics that become resume bullets

Measure twice: once before the automation exists (your baseline) and once after it runs (your result). The gap is your impact. Useful metrics by track: **mean-time-to-remediate** (days to minutes), **hours saved per month** (manual effort eliminated), **devices or users at scale** (the size of the fleet you operated on), **incident or non-compliance reduction** (percentage), and **automation safety** (percent of actions gated, rollback rate, zero unapproved changes). Even in a lab you can quantify these honestly. A number turns *"I wrote a script"* into *"I built an unattended runbook that cut compliance remediation from days to under an hour across 4,000 devices, recovering ~18 hours a month with zero unapproved changes."* Only the second sentence gets you the interview.

## Common ways the capstone fails the bar

Most capstones fail in predictable, avoidable ways, so check yourself against them before you publish. The first is **scope creep**: trying to automate five problems badly instead of one problem well. A single, deep, fully-guarded workflow beats a sprawling half-built toolkit every time, so resist the urge to add features and instead add evidence. The second is **acting without detecting**: a script that changes state before it has read and validated the current state, which is how a typo wipes a fleet. The third is **no dry run**: an action that cannot be previewed with `-WhatIf`, leaving you to test in production. The fourth is **hidden privilege**: a runbook authenticated with a stored secret or a god-mode app registration instead of a least-privilege managed identity. The fifth is **no numbers**: a project that works but never measured its baseline, so the impact is unprovable and the resume bullet is hollow. And the sixth is **an empty README**: code with no explanation of the problem, the design, or how to run it. Walk this list before you call the project done, fixing each gap is what turns a script into evidence a senior engineer would respect.

## Your task

Deliver the capstone as one reviewable package. (1) Write the three-sentence scope: problem with a baseline number, measurable outcome, and blast radius. (2) Choose Track A or Track B and justify it. (3) Build the detect -> decide -> act -> verify -> report pipeline with a guardrail on every action and the full safety pattern. (4) Write a one-page design doc that names each tool and attaches a one-line justification to every guardrail. (5) Prove the 'done' bar: run it safely, demonstrate an idempotent second run, and record baseline-vs-after metrics. Publish it to a clean public repository with a README. This single artifact is what the next four lessons turn into a portfolio, a resume, and a job.
