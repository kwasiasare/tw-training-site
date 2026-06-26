---
course: helpdesk-tier3-advanced
title: Building Your Systems Engineering Portfolio
month: 5
monthTitle: Capstone & Career Launch
lesson: 2
summary: 'One capstone proves you can engineer; a portfolio proves it was not a fluke. This lesson turns
  your work into two or three self-contained automation projects a hiring manager can verify in minutes:
  Microsoft Graph scripts, an Autopilot or provisioning workflow, and an AIOps dashboard or gated remediation
  runbook. For each, you will assemble the four artifacts that separate an engineer from a button-clicker,
  a public repository with clean code and a README, an architecture diagram, a short demo video, and a
  one-page design doc that justifies the decisions. You will frame all of them under one story so a reviewer
  sees a systems engineer, not a collection of labs. The deliverable is a pinned, linkable portfolio you
  can drop into a resume, a LinkedIn Featured section, and an interview.'
objectives:
- Select two or three projects that together cover automation, provisioning, and AIOps/observability
- 'Build the four artifacts per project: a clean repo, an architecture diagram, a demo video, and a design
  doc'
- Write a README that states the problem, architecture, how to deploy, how to test, and the results
- 'Keep repositories safe and reviewable: no secrets, pinned module versions, least-privilege documented'
- Frame the projects under one narrative so reviewers see a coherent systems engineer
- Publish a pinned, linkable portfolio ready for a resume, LinkedIn Featured, and interviews
video: ht5-l02-building-your-systems-engineering-portfolio.mp4
quiz:
- q: What is the strongest set of projects for a Tier 3 / systems engineering portfolio?
  options:
  - Two or three projects that together span automation (Graph scripts), provisioning (Autopilot/config),
    and AIOps (a dashboard or gated remediation)
  - Three near-identical scripts that each rename a device
  - A single screenshot of the Intune portal
  - As many tiny repos as possible with no documentation
  answer: 0
  why: 'A portfolio should demonstrate breadth across the role: automation, provisioning, and observability/AIOps.
    Two or three coherent projects covering those areas prove range and depth, whereas duplicate scripts
    or undocumented fragments show neither.'
- q: Which four artifacts make a single portfolio project persuasive?
  options:
  - A long screenshot gallery with no narrative
  - A clean public repo with a README, an architecture diagram, a short demo video, and a one-page design
    doc
  - Only the certification badge
  - A private repo no one can open and a promise it works
  answer: 1
  why: 'The four artifacts let a reviewer verify capability fast: the repo and README show the code and
    how to run it, the diagram shows the design, the demo proves it works, and the design doc explains
    the decisions and trade-offs. That package is what separates an engineer from a button-clicker.'
- q: What belongs in a strong project README?
  options:
  - Just the project title
  - A list of every command you ran, in order, with no context
  - The problem, the architecture, how to deploy, how to test, and the measurable results
  - Your full life story and unrelated hobbies
  answer: 2
  why: A README is the front door to the repo. Stating the problem, the architecture, deploy and test
    instructions, and the results lets a reviewer understand and trust the work in under a minute, which
    is the entire point of publishing it.
- q: Why must portfolio repositories contain no secrets and pin their module versions?
  options:
  - It makes the repo look longer
  - Hardcoded secrets are a security failure that disqualifies you, and pinned versions make the project
    reproducible and trustworthy to a reviewer
  - GitHub deletes repos that have READMEs
  - Pinning versions makes the code run faster
  answer: 1
  why: A leaked secret in a public repo signals exactly the wrong judgment for a security-adjacent role,
    and unpinned dependencies make a project unreproducible. Clean, secret-free, version-pinned repositories
    demonstrate the operational discipline the role demands.
- q: How should a career-changer present self-directed projects on a portfolio?
  options:
  - Hide them, because only paid work counts as real experience
  - Only as a PDF emailed after the interview
  - As a single line that says 'did some projects'
  - 'As legitimate, demonstrable engineering: framed under one story, pinned on the profile, and linked
    from the resume and LinkedIn Featured section'
  answer: 3
  why: Self-directed, portfolio-grade projects are genuine, verifiable experience, especially when moving
    into a senior role. Framing them under one narrative and making them easy to find and open is exactly
    what converts a profile view into an interview.
- q: In two to four sentences, describe the one-sentence narrative you would use to frame your three projects,
    and name the project that anchors each theme.
  answer: 'My framing line is: I automate and operate modern Windows endpoints at scale, from provisioning
    to self-healing. The Graph automation project anchors the automation theme, showing fleet-wide remediation
    behind safe gates; the Autopilot and configuration-as-code project anchors provisioning, showing zero-touch
    device setup from a source of truth; and the AIOps dashboard with gated remediation anchors observability
    and reliability, showing telemetry turning into a verified fix. Together they tell one story of an
    engineer who designs, automates, and operates the endpoint lifecycle, rather than three unrelated
    labs.'
  why: A strong answer gives a single positioning line and maps each project to a distinct theme (automation,
    provisioning, AIOps), demonstrating that the portfolio is a coherent argument about one engineer rather
    than a pile of disconnected scripts.
resources:
- label: GitHub Docs - Managing your profile README
  url: https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
- label: Microsoft Learn - Overview of Windows Autopilot
  url: https://learn.microsoft.com/en-us/autopilot/overview
- label: Microsoft Learn - Microsoft Graph PowerShell SDK overview
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/overview
- label: Microsoft Learn - Remediations in Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations
---

## From one project to a body of work

The capstone proved you can engineer one solution. A portfolio proves it is repeatable, that you make safe, well-documented automation as a matter of habit. Two or three coherent projects do far more than one: they show **range** (you can provision, automate, and observe) and **depth** (each is built to a professional bar). This lesson is about packaging that work so a hiring manager, who will spend ninety seconds on your profile before deciding whether to keep reading, sees a systems engineer. The work is mostly done; what remains is presentation, and presentation is where most strong candidates quietly lose.

## Choose projects that span the role

Aim for two or three projects that together cover the territory of a Tier 3 / endpoint / systems engineering role. A strong, complementary set:

- **A Microsoft Graph automation.** Your capstone or a sibling of it: fleet-wide detection and idempotent, gated remediation driven by the Graph PowerShell SDK, packaged as an Azure Automation runbook with managed-identity auth. This anchors **automation at scale**.
- **A provisioning / Autopilot workflow.** Zero-touch device setup expressed as **configuration-as-code**: Autopilot deployment profiles or device-preparation policies, group-tag assignment, an Enrollment Status Page, and configuration profiles applied from a source of truth, ideally deployed by script so it is reproducible. This anchors **provisioning and modern management**.
- **An AIOps dashboard or gated remediation.** Endpoint telemetry pulled into Log Analytics or a workbook, KQL queries that surface reliability and risk, and either a dashboard a team could actually use or a runbook that turns a signal into a verified, gated fix. This anchors **observability and reliability**.

You do not need all three. Two that span automation and observability are plenty. The goal is breadth across the role plus depth in each, not quantity.

## The four artifacts per project

Treat every project as a self-contained case study with the same four artifacts. This is the single most important pattern in the lesson.

- **A clean public repository.** Code that is safe, idempotent, and least-privilege, with a clear structure. Include the runbook or scripts, any Bicep or configuration JSON, and a **README** (see below). Pin module versions. **No secrets, ever**, scrub tenant IDs, tokens, and connection strings; a leaked secret in a public repo disqualifies you for a security-adjacent role.
- **An architecture diagram.** One clean diagram per project in a consistent visual style, the detect-decide-act-verify-report flow, the provisioning pipeline, the telemetry-to-dashboard path. This is the first thing anyone looks at, so make it legible.
- **A short demo video.** Three to five minutes showing the project working end to end: the runbook firing, the device provisioning, the dashboard updating, the remediation gated and verified. Recruiters and hiring managers genuinely watch these, and a working demo defeats any doubt about whether the project is real.
- **A one-page design doc.** The business problem, the design and *why* you chose it, the trade-offs and limitations, and the measurable results. This is what separates an engineer from a button-clicker, because it shows judgment, not just output.

## Write the README like a front door

The README is the most-read file in your portfolio. Give every project the same structure so reviewers know exactly where to look:

```text
# Project name - one-line description
## Problem        what hurts, quantified (the baseline)
## Architecture   the diagram + a short narration of the flow
## How to deploy   prerequisites, permissions (least privilege), steps
## How to test     a dry run, the pilot ring, how to prove idempotency
## Results         baseline vs after: MTTR, hours saved, devices at scale
## Safety          the guardrails and a one-line justification for each
```

A reviewer who opens this README understands the problem, the design, how to run it, and the impact in under a minute. That is the entire purpose of publishing the work.

## Keep it safe and reproducible

A portfolio is also a judgment test. The discipline you would apply in production applies here: **no secrets in source** (use a `.gitignore`, reference managed identities, and replace real identifiers with placeholders); **pinned dependencies** so the project is reproducible; **least privilege documented**, state the exact scopes or application permissions the automation needs and why; and a clear note on **how you piloted** (the `-WhatIf` dry run and the ring). Reviewers read these signals fast. A clean, safe, reproducible repo says *"I can be trusted with the fleet"* far more convincingly than any bullet point.

## Frame everything under one story

Do not present three unrelated labs; present one engineer. Write a single positioning line and let each project illustrate a facet of it. For example: *"I automate and operate modern Windows endpoints at scale, from provisioning to self-healing."* The Graph automation shows automation, the Autopilot workflow shows provisioning, the AIOps dashboard shows observability and reliability. Put that line at the top of your GitHub **profile README**, pin the project repositories beneath it, and link the demo videos. A reviewer who lands on your profile should grasp the narrative before they click anything. One story across three projects is what turns a list into an argument.

## Make it linkable everywhere

The portfolio is only useful if people can find it. Create a **GitHub profile README** (a repo named after your username) as a one-screen landing page: your positioning line, the pinned projects with one-line descriptions, and links to the demos. That single URL then goes into your resume header, your LinkedIn **Featured** section, and your outreach messages. One link, everything behind it, verifiable in minutes.

## Common portfolio mistakes to avoid

A few recurring mistakes quietly sink otherwise good portfolios. **Quantity over quality** is the most common: ten thin repos with no READMEs signal less than two polished projects, because a reviewer judges your bar by your *best public work* and your *worst public work* at the same time. **Private repos** are another: a project a hiring manager cannot open does not exist as far as the screen is concerned, so make the showcase work public and keep only genuinely sensitive material private. **Stale or broken demos** undermine trust, a video that no longer matches the repo, or a README whose steps fail, reads as carelessness, so re-record and re-test when you change the code. **Committed secrets** are disqualifying for a security-adjacent role and are easy to leak by accident, so scan your history and use placeholders. And **no narrative** leaves three good projects looking like three unrelated accidents; without the one-sentence framing line, the reviewer has to do the work of connecting them, and most will not bother. Treat the portfolio like a product you are shipping to one specific user, the hiring manager, and remove anything that makes their thirty-second skim harder.

## Your task

Build the portfolio. (1) Choose two or three projects that span automation, provisioning, and AIOps/observability. (2) For each, ship the four artifacts: a clean, secret-free public repo with a structured README, an architecture diagram, a three-to-five-minute demo video, and a one-page design doc with quantified results. (3) Pin module versions, document least-privilege scopes, and confirm no secrets are committed. (4) Write your one-sentence narrative and build a GitHub profile README that frames all the projects under it. (5) Produce the single portfolio link you will drop into your resume, LinkedIn Featured, and interviews. That link is the proof that everything in this course actually happened.
