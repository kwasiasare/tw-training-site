---
course: helpdesk-tier3-advanced
title: Proactive and predictive support with AI
month: 4
monthTitle: AIOps, Monitoring & Agentic Automation
lesson: 7
summary: 'Shift from reactive ticket-handling to proactive operations: detect anomalies and trends in
  endpoint telemetry, forecast failures before users feel them, and act early within the same guardrails.'
objectives:
- Contrast reactive, proactive, and predictive support and explain the value of moving left
- Detect anomalies and trends in endpoint telemetry using KQL series functions
- Identify leading indicators (disk health, battery wear, crash rate, update failures) that precede incidents
- Forecast capacity and failure risk to schedule maintenance before users are impacted
- Frame predictive outputs as risk scores that humans prioritise, not automatic actions
- Guard against false positives, alert fatigue, and acting on low-confidence predictions
video: ht4-l07-proactive-predictive-support.mp4
quiz:
- q: What best describes the shift from proactive to PREDICTIVE support?
  options:
  - Predictive support waits for the user to call
  - Proactive acts on current symptoms before users complain; predictive uses trends/forecasts to act
    before symptoms even appear
  - They are identical
  - Predictive support disables monitoring
  answer: 1
  why: Proactive responds to early but present signals; predictive forecasts future failures from trends
    and acts ahead of any symptom — moving the response even further 'left'.
- q: Which KQL function pair is most directly suited to building and analysing a time series for anomaly
    detection?
  options:
  - parse and split
  - project and take
  - make-series and series_decompose_anomalies
  - distinct and count
  answer: 2
  why: make-series builds a regular time series and series_decompose_anomalies (and related series_* functions)
    flag points that deviate from the expected pattern.
- q: Which is a genuine leading indicator that a laptop fleet may see incidents soon?
  options:
  - The number of tickets already closed last year
  - A rising trend in SMART disk-health warnings and growing application crash rates
  - The colour of the device chassis
  - The office floor number
  answer: 1
  why: Leading indicators like deteriorating disk health, battery wear, and rising crash/update-failure
    rates precede user-visible failures, enabling action before impact.
- q: How should a predictive failure-risk model's output be used in a safe AIOps design?
  options:
  - As an automatic trigger to wipe at-risk devices
  - As a reason to ignore monitoring
  - As a guaranteed prediction that never needs review
  - As a prioritised risk score that humans use to schedule proactive maintenance, still behind the usual
    approval gates
  answer: 3
  why: Predictions are probabilistic; they should rank and prioritise human-scheduled maintenance, not
    auto-trigger consequential action, and they remain subject to validation and approval.
- q: Name two leading indicators you would track to predict endpoint failures, and explain what incident
    each foreshadows.
  answer: Rising SMART disk-health/error counts foreshadow drive failure and data loss, so the device
    can be proactively re-provisioned or the disk replaced before it dies; increasing application or OS
    crash rates (or repeated update failures) foreshadow instability and user downtime, prompting investigation
    or a clean configuration push before users are blocked.
  why: Good leading indicators map to a specific future incident and a specific proactive action, which
    is the essence of predictive support.
- q: Why is guarding against false positives especially important in predictive support, and what is one
    mitigation?
  answer: Because predictions act before any symptom exists, a false positive can trigger unnecessary
    maintenance, cost, and disruption to a perfectly healthy device, and a stream of them causes alert
    fatigue that erodes trust in the system. One mitigation is to require a minimum confidence threshold
    plus corroborating indicators (multiple leading signals agreeing) before a prediction is surfaced
    or actioned.
  why: Predictive systems act with less direct evidence, so confidence thresholds and corroboration are
    needed to keep precision high and trust intact.
resources:
- label: Microsoft Learn — series_decompose_anomalies in KQL
  url: https://learn.microsoft.com/en-us/kusto/query/series-decompose-anomalies-function
- label: Microsoft Learn — make-series operator in KQL
  url: https://learn.microsoft.com/en-us/kusto/query/make-series-operator
- label: Microsoft Learn — What is endpoint analytics?
  url: https://learn.microsoft.com/en-us/mem/analytics/overview
- label: Microsoft Learn — Azure OpenAI Service documentation
  url: https://learn.microsoft.com/en-us/azure/ai-services/openai/overview
---

## Moving left: reactive to proactive to predictive

Most support is **reactive**: a user reports a problem, you fix it. **Proactive** support acts on early but present signals before the user complains — a device is already throwing errors, you intervene first. **Predictive** support goes further left still: it uses **trends and forecasts** to act before any symptom appears at all. Every step left reduces user impact and cost. AIOps is the engine that makes the leftward shift practical at fleet scale.

```text
Reactive   : user reports problem        -> you react   (highest impact)
Proactive  : early symptom appears        -> you act now
Predictive : trend forecasts future fault -> you act ahead (lowest impact)
```

## Detecting anomalies in telemetry

Predictive work starts with seeing the shape of normal, then spotting deviations. KQL's series functions do this directly.

```kql
// Build a per-hour crash series, then flag anomalies automatically
DeviceEvents
| where TimeGenerated > ago(14d)
| where ActionType == "ProcessCrash"
| make-series crashes = count() default=0 on TimeGenerated step 1h
| extend (anomalies, score, baseline) = series_decompose_anomalies(crashes)
```

`make-series` builds an evenly spaced series; `series_decompose_anomalies` flags the points that break the expected pattern. Those flags are your early warnings.

## Leading indicators that precede incidents

The art is choosing **leading indicators** — signals that move *before* the user-visible failure. On endpoints these include: rising **SMART disk-health** warnings (foreshadow drive failure), growing **battery wear** (foreshadow sudden shutdowns), increasing **crash rates**, and repeated **update failures** (foreshadow instability and blocked users). Each indicator maps to a specific future incident and a specific proactive action.

## Forecasting to schedule ahead

With trends in hand you can **forecast** — estimate when a metric will cross a danger line — and schedule maintenance before it does.

```kql
// Project storage growth and estimate when free space runs out
DeviceDisk
| where TimeGenerated > ago(30d)
| make-series freeGB = avg(FreeSpaceGB) default=0 on TimeGenerated step 1d
| extend forecast = series_decompose_forecast(freeGB, 7)
```

A forecast that free space hits zero in nine days is a maintenance ticket you schedule today, not an outage you handle next week.

## Predictions are risk scores, not triggers

Here is the guardrail that defines safe predictive support: a prediction is a **probabilistic risk score for humans to prioritise**, not an automatic trigger. You feed the score into the same pipeline as before — it raises a *recommendation*, a human reviews it, and any consequential action still passes the **approval gate** from lesson six. Prediction moves the response earlier; it does not remove the human.

```text
Prediction -> risk score -> ranked worklist for a human
           -> (if action needed) -> approval gate -> scoped, verified action
```

## Guarding against false positives and fatigue

Predictive systems act with *less* direct evidence than reactive ones, so precision matters more. Require a **minimum confidence threshold** and **corroboration** — several leading indicators agreeing — before surfacing or actioning a prediction. A flood of false alarms is worse than none: it burns budget on healthy devices and trains your team to distrust the system. Tune for high precision first, recall second.

## Your task

Choose one leading indicator in your fleet (disk health, battery wear, crash rate, or update failures). Write a `make-series` query over 14-30 days and apply `series_decompose_anomalies` or `series_decompose_forecast`. Define the confidence threshold and corroborating signal you would require before raising a proactive ticket, and state which proactive action the prediction would recommend (and why it still passes the approval gate).
