---
course: vdi-engineer
title: 'Day-2 Operations: Capacity, Cost, and Digital Employee Experience'
month: 6
monthTitle: Monitoring, Operations & Troubleshooting
lesson: 4
summary: 'Getting a VDI platform live is day one. Running it well for the next three years is day two,
  and it''s a completely different discipline: recurring capacity and cost reviews, a category of tooling
  called digital employee experience (DEX) that measures what users actually feel rather than what infrastructure
  reports, runbooks that don''t depend on one person''s memory, and service-level objectives that give
  you an honest answer to "is the platform healthy." This closing lesson of Module 6 ties infrastructure
  monitoring, image lifecycle, and troubleshooting from the rest of the module into an operating rhythm
  you can actually run.'
objectives:
- Run a recurring capacity and cost review cadence for an AVD estate
- Define the digital employee experience (DEX) tooling category and name current category-leading products
- Distinguish infrastructure health metrics from genuine user-experience metrics
- Draft service-level objectives for session availability and logon time
- Build a lightweight runbook and on-call structure for VDI day-2 operations
quiz:
- q: What does "DEX" stand for in the context of VDI and end-user computing operations?
  options:
  - Data Export
  - Desktop Extension
  - Device Enrollment eXchange
  - Digital Employee Experience
  answer: 3
  why: DEX (Digital Employee Experience) is the tooling category focused on measuring and improving how
    employees actually experience their digital workplace, distinct from raw infrastructure telemetry.
- q: Which of these is a real, current example of a digital employee experience (DEX) platform relevant
    to an EUC/VDI estate?
  options:
  - ControlUp
  - Azure Compute Gallery
  - Azure Firewall
  - FSLogix
  answer: 0
  why: ControlUp, Nexthink, and Omnissa Intelligence are current, named DEX-category products as of 2026
    — Nexthink and Omnissa were both named Leaders in the 2026 Gartner Magic Quadrant for Digital Employee
    Experience Management Tools, and ControlUp is a widely deployed platform in the same category. Azure
    Compute Gallery, Azure Firewall, and FSLogix are infrastructure and profile-management tools, not
    DEX platforms.
- q: Which of these is a genuine user-experience metric rather than a pure infrastructure metric?
  options:
  - Host pool average vCPU utilization
  - Logon duration as actually experienced by the end user
  - Storage account IOPS consumption
  - Number of VM boots per day
  answer: 1
  why: vCPU utilization, storage IOPS, and boot counts describe the state of the infrastructure. Logon
    duration as experienced by the user is a direct measure of what the employee actually felt, which
    is what DEX tooling and end-to-end logon metrics are built to capture.
- q: Why should cost and capacity reviews for an AVD estate be recurring rather than a one-time sizing
    exercise done at go-live?
  options:
  - Costs never change once autoscale is configured, so reviews are only symbolic
  - Cost reviews are only useful before go-live and add no value afterward
  - Usage patterns, licensing terms, and Azure pricing all shift over time, so right-sizing is an ongoing
    activity
  - Reserved Instances and Savings Plans make ongoing reviews unnecessary forever
  answer: 2
  why: User counts, session patterns, license mix, and Azure pricing all change after go-live. A sizing
    decision that was correct at launch drifts out of date, which is exactly why Module 3's autoscale
    and cost-optimization work needs a recurring review cadence, not a single decision.
- q: Which of these is the best candidate service-level objective (SLO) for a VDI platform team?
  options:
  - 100% of support tickets closed the same day they're opened
  - Zero support tickets filed per month
  - Session hosts are never rebooted
  - 95th-percentile logon time under a defined threshold, measured over a rolling window
  answer: 3
  why: A good SLO is measurable, tied to what users actually experience, and realistic over a rolling
    window — a percentile-based logon time target is exactly that. The other options are either unrealistic
    absolutes or not meaningful measures of platform health.
- q: Your VDI platform currently has no runbooks, and the on-call engineer is 'whoever remembers how it
    works.' Describe what a minimal but useful VDI runbook should contain, and give one SLO you'd track
    alongside it.
  answer: 'A minimal VDI runbook should document: how to check current host pool and session host health
    (which dashboard or KQL query to run), the steps to drain and replace an unhealthy session host, how
    to check for FSLogix/profile failures, who or what to escalate to for a platform-level Microsoft or
    vendor outage, and rollback steps for a bad image rollout or a bad scaling-plan change. Alongside
    it you''d track an SLO such as 95th-percentile logon time under a defined target (for example, under
    30-45 seconds) measured over a rolling 30-day window, or session availability (the percentage of connection
    attempts that succeed) against a target like 99.5%.'
  why: This connects the runbook content directly to the connection-chain triage method from Lesson 3
    and the SLO framing taught in this lesson — a runbook without a matching SLO has no way to prove it's
    working.
resources:
- label: Omnissa Intelligence
  url: https://www.omnissa.com/products/omnissa-intelligence/
- label: Nexthink
  url: https://www.nexthink.com/
- label: ControlUp
  url: https://www.controlup.com/
- label: Autoscale scaling plans and example scenarios (AVD)
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scenarios
- label: Enable Insights to monitor Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/insights
---

## Day One Ends, Day Two Never Does

Everything up to this point in the course — architecture, networking, images, identity, FSLogix, monitoring, patching, troubleshooting — gets a platform live. **Day-2 operations** is the discipline of keeping it healthy, affordable, and trusted by users for the years after go-live, and it's where a lot of otherwise well-built VDI platforms quietly decay: capacity that was right-sized at launch drifts wrong, costs creep as autoscale plans go untouched, nobody notices logon times climbing until users start complaining loudly, and the one person who understood the environment leaves. This lesson closes Module 6 by turning infrastructure monitoring (Lesson 1), image lifecycle (Lesson 2), and troubleshooting (Lesson 3) into a recurring operating rhythm.

## Capacity and Cost Reviews Are Recurring, Not One-Time

Module 3 taught you to build autoscale scaling plans and reason about density and Reserved Instances at design time. Day-2 operations means revisiting those decisions on a cadence — monthly for cost, quarterly for capacity structure — because none of the inputs stay fixed: headcount changes, session patterns shift (more hybrid days, different peak hours), Azure pricing and available VM SKUs change, and your license mix evolves as the org migrates between M365 tiers. A useful monthly review pulls three things: actual peak concurrent sessions per host pool against your autoscale ramp-up/ramp-down schedule (is capacity arriving before users need it, or lagging?), cost per active user (total host pool spend divided by monthly active users, tracked as a trend, not a snapshot), and any host pools still running Reserved Instance or Savings Plan coverage that no longer matches actual usage. None of this requires new tooling beyond what Lesson 1 already wired up — Azure Cost Management plus the WVDConnections/WVDAgentHealthStatus data you're already collecting is enough to answer all three questions.

## Infrastructure Metrics vs. What Users Actually Feel

Here's the trap: a platform can look perfectly healthy on every infrastructure dashboard — low CPU, low disk queue length, autoscale behaving — while users are quietly miserable because logons take 90 seconds or app launches stutter. **Infrastructure metrics** (vCPU utilization, storage IOPS, VM boot counts, autoscale event counts) tell you about the machines. **User-experience metrics** (logon duration as actually measured end to end, session responsiveness, application launch time, self-reported satisfaction) tell you what the employee felt. Both matter, but they answer different questions, and a platform team that only watches infrastructure dashboards will consistently be the last to know about a real problem.

This is exactly the gap **digital employee experience (DEX)** tooling exists to close. DEX platforms aggregate telemetry across endpoints, sessions, and applications specifically to surface the user-experience layer, often correlating it back to the infrastructure cause. Three category-leading, currently active products worth knowing by name: **Omnissa Intelligence** (a cloud-native telemetry and automation service that aggregates data across Workspace ONE UEM, Horizon, and other sources into dashboards and automated remediation workflows), **Nexthink** (a DEX platform combining technical monitoring with employee sentiment data, recognized as a Leader in the 2026 Gartner Magic Quadrant for Digital Employee Experience Management Tools), and **ControlUp** (ControlUp ONE, which monitors and optimizes experience across VDI, physical endpoints, and cloud environments, a long-standing VDI-focused platform in the same category). You don't need all three, or even one, to run a healthy platform — but you do need *something* measuring the user-experience layer, whether it's a dedicated DEX product or logon-time telemetry you build yourself from the WVD tables in Lesson 1.

## Writing SLOs That Mean Something

A service-level objective (SLO) is only useful if it's measurable, tied to what users actually experience, and realistic over a defined window — not an aspirational absolute nobody can hit. Two SLOs worth adopting for almost any VDI platform:

- **Session availability**: the percentage of connection attempts that succeed end to end (reach `Connected` state in `WVDConnections` without a matching service error), targeted at something like 99.5% measured over a rolling 30-day window.
- **Logon time**: the 95th-percentile logon duration (from credential submission to a usable desktop), targeted at a threshold appropriate to your environment — often 30-45 seconds for a well-tuned FSLogix + golden image setup — again over a rolling window, not a single bad day.

Using the **95th percentile** rather than an average matters: an average hides the worst experiences behind a sea of fast logons, while the 95th percentile tells you what your unluckiest one-in-twenty users are actually enduring, which is usually where the real complaints come from.

## Runbooks and On-Call, Kept Lightweight

A runbook doesn't need to be exhaustive to be useful — it needs to cover the handful of situations that happen often enough to matter and are painful enough that improvising them live, at 2am, is a bad idea. A minimal but genuinely useful VDI runbook set covers: how to check current host pool/session host health (pointing directly at the Lesson 1 workbook and KQL queries), how to drain and replace an unhealthy session host (Lesson 2/3 material), a quick FSLogix triage checklist (Lesson 3), clear escalation criteria for when a problem is Microsoft's to fix versus yours (the `ServiceError` rule from Lesson 3), and rollback steps for a bad image rollout or a misbehaving autoscale plan change. Pair each runbook entry with the SLO it protects, so on-call has both **what to do** and **why it matters** in the same document.

## What You'd Actually Do

Set a monthly cost/capacity review and a quarterly deeper capacity-structure review, both using data you already have from Lesson 1. Pick at least one user-experience signal to track alongside infrastructure metrics — either a DEX platform or logon-time telemetry from `WVDConnections` — so you're not blind to what users actually feel. Write two SLOs (session availability, 95th-percentile logon time) and put them somewhere visible. Build a short runbook covering the handful of recurring situations from this module, and make sure it lives somewhere the whole team can find it, not in one engineer's memory. That combination — recurring reviews, a real experience signal, honest SLOs, and a lightweight runbook — is what separates a platform that was launched well from one that stays healthy for years.
