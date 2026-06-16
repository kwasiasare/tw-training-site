---
course: helpdesk-tier3-advanced
title: Log analysis at scale
month: 1
monthTitle: Advanced Troubleshooting & Root Cause Analysis
lesson: 6
summary: Move from reading one machine's Event Viewer to querying logs across a fleet to find patterns.
  Filter precisely with Get-WinEvent and FilterHashtable, then aggregate and correlate with KQL.
objectives:
- Query Windows event logs precisely with Get-WinEvent and FilterHashtable
- Build a cross-source timeline by correlating events on time and identifier
- Recognise the difference between a noisy symptom log and the originating event
- Aggregate events across many machines to separate a one-off from a fleet pattern
- Write KQL queries to summarise, bin by time, and rank failures
- Avoid the survivorship and selection biases that distort log-based conclusions
video: ht1-l06-log-analysis-at-scale.mp4
quiz:
- q: Why is Get-WinEvent with -FilterHashtable strongly preferred over piping Get-WinEvent to Where-Object
    for large logs?
  options:
  - It produces prettier output
  - FilterHashtable filters server-side in the event log engine, so it reads far fewer records and is
    dramatically faster
  - Where-Object cannot read event logs
  - It automatically uploads to the cloud
  answer: 1
  why: FilterHashtable pushes the filter down into the logging subsystem (XPath), so only matching records
    are materialised. Piping to Where-Object reads and deserialises every record first, which is orders
    of magnitude slower on big logs.
- q: You find thousands of 'service failed to start' errors after a patch. What is the disciplined next
    step before blaming the patch?
  options:
  - Roll back the patch immediately on the whole fleet
  - Build a timeline to find the FIRST originating event and check whether the errors precede or follow
    the patch install time
  - Delete the noisy log
  - Ignore it as expected noise
  answer: 1
  why: A flood of downstream errors is a symptom. You must establish the timeline and the originating
    event — confirming the errors started after the patch and identifying the first failure — before attributing
    cause; otherwise you may roll back something unrelated.
- q: In KQL, which operator summarises a count of events bucketed into 5-minute intervals?
  options:
  - summarize count() by bin(TimeGenerated, 5m)
  - project TimeGenerated
  - where count > 5
  - sort by TimeGenerated
  answer: 0
  why: summarize count() by bin(TimeGenerated, 5m) aggregates rows into 5-minute time buckets — the standard
    way to turn raw events into a rate over time so you can see spikes and trends.
- q: Forty machines show a crash; you investigate the three that were escalated and conclude it's a rare
    edge case. What bias has likely distorted this?
  options:
  - Confirmation bias only
  - Selection/survivorship bias — you analysed only the escalated subset, not the full population that
    experienced the issue
  - Recency bias
  - There is no bias
  answer: 1
  why: Looking only at escalated tickets samples a biased subset. To judge prevalence and pattern you
    must query the whole fleet's logs, not just the machines that happened to be reported.
- q: In one sentence, why correlate logs across multiple sources rather than trusting a single log?
  answer: Because a single log shows only its own component's view; correlating the System, Application,
    security, and network or device logs on a shared timeline reveals the causal chain — which event happened
    first and triggered the rest — that no single source can show.
  why: Root cause lives in the sequence across components; cross-source correlation on time is what exposes
    the originating event behind a cascade of symptoms.
- q: What does an Event Viewer error's 'symptom log' problem mean for RCA?
  answer: Many logs record the consequence of a failure (e.g. dozens of components reporting they lost
    a dependency) rather than its origin, so the loudest, most frequent error is usually a downstream
    symptom; RCA requires tracing back to the quieter, earlier originating event.
  why: The most frequent error is often the easiest to see but the furthest from the cause; disciplined
    analysis hunts the first event in the chain, not the loudest one.
resources:
- label: Microsoft Learn — Get-WinEvent reference
  url: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent
- label: Microsoft Learn — Creating Get-WinEvent queries with FilterHashtable
  url: https://learn.microsoft.com/en-us/powershell/scripting/samples/creating-get-winevent-queries-with-filterhashtable
- label: Microsoft Learn — Kusto Query Language (KQL) overview
  url: https://learn.microsoft.com/en-us/kusto/query/
- label: Microsoft Learn — summarize operator (KQL)
  url: https://learn.microsoft.com/en-us/kusto/query/summarize-operator
---

## One machine is an anecdote; the fleet is the evidence

At Tier 2 you read one machine's Event Viewer. At Tier 3 the question changes: *is this a one-off, or a pattern across the fleet?* A crash on one laptop is an anecdote. The same crash on forty laptops after the same patch is a root cause. Scaling your log analysis from one host to many is the core Tier 3 skill in this lesson.

## Filter precisely, and server-side

The most common performance mistake is filtering in PowerShell instead of in the log engine. Piping `Get-WinEvent` to `Where-Object` reads and deserialises *every* record first. **FilterHashtable** pushes the filter down into the logging subsystem, so only matching records are ever materialised — often orders of magnitude faster on a busy log.

```powershell
# Precise, fast, server-side filtering
Get-WinEvent -FilterHashtable @{
  LogName   = 'System'
  Id        = 7000,7001,7031,7034   # service control manager failures
  StartTime = (Get-Date).AddHours(-24)
} | Select-Object TimeCreated, Id, ProviderName, Message
```

## Find the originating event, not the loudest one

Logs are full of **symptom records**. When a low-level service dies, dozens of components log that they lost a dependency. The loudest, most frequent error is usually a *downstream symptom*. RCA means tracing back to the **first, quieter originating event** on the timeline.

Build a cross-source timeline by merging logs and sorting on time:

```powershell
$logs = foreach ($l in 'System','Application') {
  Get-WinEvent -FilterHashtable @{ LogName = $l; StartTime = (Get-Date).AddHours(-2) }
}
$logs | Sort-Object TimeCreated | Select-Object TimeCreated, LogName, Id, ProviderName
```

The event at the *top* of the cascade — the first failure — is your suspect.

## Aggregate across the fleet with KQL

When logs are centralised (e.g. in a log analytics workspace), **Kusto Query Language (KQL)** lets you separate a one-off from a fleet-wide pattern. The key move is to summarise and bin by time.

```text
Event
| where TimeGenerated > ago(24h)
| where EventID in (7031, 7034)
| summarize count() by Computer, bin(TimeGenerated, 5m)
| sort by count_ desc
```

Binning turns raw events into a **rate over time**, so a spike at a deployment window jumps out. Summarising by `Computer` tells you whether one host or forty are affected — the difference between an anecdote and a root cause.

## Beware the biases

Two biases wreck log-based RCA. **Selection/survivorship bias**: investigating only escalated tickets samples a skewed subset, making a common problem look rare. **Confirmation bias**: filtering for the events you already expect and never querying the rest. Always query the *whole population* and let the data tell you the prevalence.

## Your task

Using a real or lab fleet (or several machines), write a `FilterHashtable` query that pulls service-control failures (IDs 7000/7001/7031/7034) from the last 24 hours and confirm it runs faster than the `Where-Object` equivalent. Merge System and Application logs into one sorted timeline and identify the first originating event behind a cascade. If you have a log analytics workspace, write a KQL query that `summarize`s those failures by `Computer` and `bin(TimeGenerated, 5m)`; if not, replicate the aggregation in PowerShell with `Group-Object`. Write one paragraph stating whether the issue is a one-off or a fleet pattern, and which bias you actively guarded against.
