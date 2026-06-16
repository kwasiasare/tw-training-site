---
course: helpdesk-tier3-advanced
title: Writing the RCA report and running a post-incident review
month: 1
monthTitle: Advanced Troubleshooting & Root Cause Analysis
lesson: 8
summary: Turn your investigation into a clear, blameless RCA report and run a post-incident review that
  produces tracked, preventive actions. Communicate evidence, impact, and follow-through that the whole
  organisation can act on.
objectives:
- Structure an RCA report so any reader gets impact, cause, and fix in seconds
- Build a precise incident timeline with detection, diagnosis, and resolution markers
- Separate the proximate cause from the root cause and the contributing factors in writing
- Write blameless language that targets systems, not individuals
- Define SMART, owned, tracked corrective actions that prevent recurrence
- Facilitate a post-incident review that surfaces lessons without assigning blame
video: ht1-l08-rca-report-and-post-incident-review.mp4
quiz:
- q: What belongs in the first section of a well-structured RCA report?
  options:
  - A full packet-by-packet trace
  - The list of every command you ran
  - 'A concise executive summary: what happened, the impact, the root cause, and the fix'
  - The names of who was on shift
  answer: 2
  why: Most readers need impact, cause, and fix in seconds. The detailed evidence belongs later; the report
    leads with a tight executive summary so leadership and other teams can act immediately.
- q: Why does an RCA timeline distinguish 'time to detect' from 'time to resolve'?
  options:
  - To make the report longer
  - Because a long detection gap points at monitoring weaknesses, while a long resolution gap points at
    process/tooling weaknesses — different corrective actions
  - They are the same metric
  - Only auditors care about timing
  answer: 1
  why: Splitting the timeline isolates where time was actually lost. A slow detection implicates monitoring/alerting;
    a slow resolution implicates runbooks, access, or tooling — guiding distinct improvements.
- q: Which corrective action is written correctly for an RCA report?
  options:
  - '''Be more careful with deployments.'''
  - '''Add pre-deploy config validation to the pipeline; owner: J. Okoye; due: 2026-07-15; tracked as
    TKT-4821.'''
  - '''Someone should look into monitoring.'''
  - '''Improve the process going forward.'''
  answer: 1
  why: 'A good action is SMART and accountable: specific, owned, dated, and tracked. Vague exhortations
    like ''be more careful'' are not actions and prevent nothing.'
- q: What is the core principle of a blameless post-incident review?
  options:
  - Identify who caused the incident so they can be retrained
  - Assume people acted reasonably with the information they had, and fix the systems that allowed the
    failure
  - Avoid writing anything down to reduce liability
  - Only senior staff may speak
  answer: 1
  why: Blameless review assumes good-faith actors and focuses on systemic causes. This surfaces honest
    information; blame culture hides it and guarantees the next recurrence.
- q: In one sentence, why must an RCA report state the impact in concrete, measurable terms?
  answer: Because measurable impact (users affected, duration, transactions or revenue lost) lets the
    organisation prioritise corrective work proportionately and judge whether the cost of prevention is
    justified, rather than reacting to vague severity.
  why: Quantified impact turns an incident into a prioritisable business decision and prevents both over-
    and under-investment in fixes.
- q: How should an RCA report handle a root cause you could not definitively prove?
  answer: State it honestly as the most-supported hypothesis with the evidence for and against, document
    the hypotheses you ruled out, record the monitored mitigation in place, and define what new data would
    confirm it — presenting a bounded, resumable unknown rather than a false certainty.
  why: Overstating certainty destroys credibility and leads to wrong fixes; an honest, bounded unknown
    preserves trust and keeps the investigation resumable.
resources:
- label: 'Google SRE Book — Postmortem Culture: Learning from Failure'
  url: https://sre.google/sre-book/postmortem-culture/
- label: Google SRE Workbook — Example postmortem and templates
  url: https://sre.google/workbook/postmortem-culture/
- label: Atlassian — Incident postmortem (blameless) guide
  url: https://www.atlassian.com/incident-management/postmortem
- label: Microsoft Learn — Azure post-incident review (PIR) practices
  url: https://learn.microsoft.com/en-us/azure/well-architected/reliability/monitoring-alerting-strategy
---

## The report is the deliverable

Your investigation only matters if others can act on it. The **RCA report** is the actual deliverable of Tier 3 work: it converts your evidence into a decision the organisation can make and a fix it can track. A brilliant diagnosis trapped in your head, or buried in 20 pages of raw logs, changes nothing.

## Structure for the reader, not the writer

Write top-down. The first thing any reader sees is a tight **executive summary**: what happened, the measurable impact, the root cause, and the fix — in seconds, not pages. Detail comes later for those who need it.

```text
RCA REPORT — INC-2026-0142
Summary   : 30 laptops lost VPN for 3h12m after the 06/14 client update.
Impact    : 30 users, ~96 user-hours lost; no data loss.
Root cause: Driver pushed without version pinning regressed the adapter.
Fix       : Pin driver version; add pre-deploy validation gate.
Status    : Mitigated 14/06; permanent fix tracked as TKT-4821.
```

State **impact in measurable terms** — users affected, duration, work or revenue lost. That is what lets leadership prioritise the fix proportionately.

## Timeline: separate detect from resolve

A good report includes a precise **timeline** with three markers: when the incident *began*, when it was *detected*, and when it was *resolved*. Splitting **time-to-detect** from **time-to-resolve** is diagnostic in itself: a long detection gap implicates your **monitoring**; a long resolution gap implicates your **runbooks, access, or tooling**. They lead to different corrective actions.

## Name the causes precisely

Use the vocabulary from this month. Separate the **proximate cause** (the immediate trigger), the **root cause** (the systemic condition), and any **contributing factors** (the other slices of cheese that aligned). If you could not prove the root cause, say so honestly: present the most-supported hypothesis with evidence for and against, the hypotheses you ruled out, the monitored mitigation, and what new data would confirm it. A **bounded unknown** preserves credibility; false certainty destroys it.

## Blameless language and SMART actions

Write **blamelessly**: assume people acted reasonably with the information they had, and target the *systems* that allowed the failure. "The tech forgot" becomes "the pipeline had no validation to catch a missing config." Blame culture hides information and guarantees recurrence.

Every report ends in **corrective actions** that are **SMART** — specific, measurable, owned, dated, and tracked:

```text
Action                              Owner       Due         Tracking
Add pre-deploy config validation    J. Okoye    2026-07-15  TKT-4821
Alert on >5 VPN drops/host/hour      S. Mensah   2026-07-08  TKT-4822
```

"Be more careful" is not an action and prevents nothing.

## Running the post-incident review

The **post-incident review (PIR)** is the meeting that turns the report into shared learning. Facilitate it **blamelessly**: walk the timeline, confirm the causes, and focus every minute on what systemic change prevents recurrence — not on who did what. Assign each action an owner and a date, and ensure they are tracked to closure. An incident with no closed actions is an incident you will have again.

## Your task

Take your most complete investigation from this month and write a one-page RCA report using the structure above: executive summary with measurable impact, a timeline that separates time-to-detect from time-to-resolve, a clear split of proximate cause / root cause / contributing factors (or an honest bounded unknown), and at least three SMART corrective actions with owner, due date, and a tracking ID. Rewrite any blame-laden sentence into blameless, systems-focused language. Finally, write a short agenda for a 30-minute post-incident review that would walk a team through it without assigning blame.
