---
course: helpdesk-tier3-advanced
title: Monitoring and observability for endpoints
month: 4
monthTitle: AIOps, Monitoring & Agentic Automation
lesson: 2
summary: 'Move beyond threshold monitoring to true observability: the three pillars of telemetry, how
  to instrument the endpoint fleet, and how to define SLIs and SLOs that make AIOps decisions meaningful.'
objectives:
- Distinguish monitoring from observability and explain why observability is the prerequisite for AIOps
- Describe the three pillars — logs, metrics, and traces — in an endpoint context
- Route endpoint telemetry into a Log Analytics workspace and validate ingestion
- Define SLIs, SLOs and error budgets for endpoint health and support operations
- Design alerts that minimise noise and feed clean signal into AI correlation
- Apply guardrails so dashboards and AI summaries never expose excessive or unvalidated data
video: ht4-l02-monitoring-and-observability.mp4
quiz:
- q: What is the core difference between monitoring and observability?
  options:
  - Observability only works in the cloud
  - Monitoring answers known questions with predefined checks; observability lets you ask new questions
    of rich telemetry after the fact
  - They are the same thing with different names
  - Observability removes the need to collect logs
  answer: 1
  why: Monitoring is built around questions you anticipated; observability gives you enough high-cardinality
    telemetry to investigate problems you did not predict — which is exactly what AI correlation needs.
- q: Which set correctly names the three pillars of observability?
  options:
  - Logs, metrics, traces
  - Alerts, dashboards, reports
  - CPU, memory, disk
  - Users, devices, apps
  answer: 0
  why: The three pillars are logs (discrete events), metrics (numeric time series), and traces (the path
    of a request or operation across components).
- q: What is an error budget?
  options:
  - The money spent on monitoring tools
  - The allowable amount of unreliability before an SLO is breached, derived from the SLO target
  - The number of alerts per day
  - A budget for buying new endpoints
  answer: 1
  why: If your SLO is 99.9% success, the 0.1% allowable failure is your error budget; spending it triggers
    a change in priorities, and AIOps can track its burn rate.
- q: Why are noisy, low-signal alerts especially harmful when feeding an AIOps pipeline?
  options:
  - They cost extra storage only
  - They make dashboards look colourful
  - They drown real signal, train humans to ignore alerts, and pollute the correlation the AI reasons
    over
  - They have no effect on AI
  answer: 2
  why: Alert noise causes fatigue and degrades the very correlation AIOps depends on; tuning alerts to
    high-signal events is a prerequisite, not a nicety.
- q: Define an SLI and an SLO in one sentence each, using an endpoint example.
  answer: An SLI (Service Level Indicator) is a measured quantity such as the percentage of devices reporting
    healthy in the last hour; an SLO (Service Level Objective) is the target for that indicator, such
    as 'at least 98% of devices healthy over a rolling 24 hours'.
  why: The SLI is what you measure, the SLO is the target you commit to; together they make 'is the fleet
    healthy?' an objective, AI-trackable question.
- q: Give one guardrail you would apply when an AI generates a dashboard summary for a wide audience,
    and why.
  answer: Scope the underlying query and the summary to least privilege and non-sensitive fields (for
    example exclude usernames, device serials or security-incident detail), so an AI summary shown broadly
    cannot leak data the viewer is not entitled to see.
  why: AI summaries can inadvertently surface sensitive telemetry; constraining the query inputs and audience
    enforces least privilege at the data layer.
resources:
- label: Microsoft Learn — Log Analytics workspace overview
  url: https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview
- label: Microsoft Learn — Azure Monitor overview
  url: https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview
- label: Microsoft Learn — What is endpoint analytics?
  url: https://learn.microsoft.com/en-us/mem/analytics/overview
- label: Microsoft Learn — Service level objectives (SLOs) guidance
  url: https://learn.microsoft.com/en-us/azure/well-architected/reliability/metrics
---

## Monitoring vs observability

**Monitoring** answers questions you already knew to ask: is CPU above 90%, is the device compliant, did the agent check in. You wire up a check, you get an alert. **Observability** is broader — it means collecting telemetry rich enough that you can ask *new* questions after an incident, including questions you never anticipated. That distinction matters for AIOps because AI correlation is exactly the act of asking novel questions of your data. Without observability, the model has nothing interesting to reason over.

## The three pillars on endpoints

Observability rests on three pillars.

```text
Logs    -> discrete events: 'WindowsUpdate failed 0x80070002 on DEVICE-123'
Metrics -> numeric time series: boot time, % healthy, app crash rate
Traces  -> the path of an operation across components (enrol -> policy -> app)
```

For endpoints, **logs** are your Event Log, Defender events, and Intune diagnostics. **Metrics** are things like startup performance, compliance percentage, or crash counts from **endpoint analytics**. **Traces** are less common on devices but appear when you follow a multi-step operation — say, enrolment through policy application to app install — end to end.

## Getting telemetry into Log Analytics

The correlation engine for this module is a **Log Analytics workspace**. Route device and security telemetry into it, then prove it actually arrived before trusting any AI built on top.

```kql
// Sanity check: are devices reporting in the last hour?
DeviceInfo
| where TimeGenerated > ago(1h)
| summarize devices = dcount(DeviceId)
```

If that count is far below your fleet size, fix ingestion before anything else. **Validating ingestion is a guardrail**, not housekeeping — an AI summary built on half your fleet is worse than no summary, because it looks authoritative.

## SLIs, SLOs and error budgets

To make fleet health an objective question, define indicators and targets. An **SLI** (Service Level Indicator) is a measured quantity; an **SLO** (Service Level Objective) is the target for it; the gap between the target and 100% is your **error budget**.

```kql
// SLI: percentage of devices healthy in the last 24h
DeviceHealth
| where TimeGenerated > ago(24h)
| summarize healthy = countif(Status == "Healthy"), total = count()
| extend sli_pct = round(100.0 * healthy / total, 2)
```

If your SLO is *98% healthy over 24h* and the SLI drops to 96%, you are burning error budget — a concrete, AI-trackable trigger for action.

## Designing alerts that feed clean signal

AIOps reasons over your alert stream, so noise is poison. Alert on **symptoms users feel** and on **error-budget burn**, not on every transient blip. Each alert should be actionable, deduplicated, and carry enough context for both a human and an AI to triage. Tune aggressively: fewer, higher-signal alerts produce better correlation and stop your team learning to ignore the pager.

## Guardrails for dashboards and AI summaries

When an AI summarises telemetry for a wide audience, apply **least privilege at the data layer**: scope queries to exclude usernames, serials, or security-incident detail unless the viewer is entitled to them. A broadly shared AI summary must never leak data the reader could not query themselves.

## Your task

In your Log Analytics workspace, run the ingestion sanity check against your real fleet size. Then define one SLI and one SLO for endpoint health, write the KQL that computes the SLI, and state the error budget. Note one alert you currently have that is too noisy and how you would tune it.
