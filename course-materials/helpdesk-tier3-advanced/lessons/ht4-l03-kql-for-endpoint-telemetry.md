---
course: helpdesk-tier3-advanced
title: KQL for endpoint telemetry
month: 4
monthTitle: AIOps, Monitoring & Agentic Automation
lesson: 3
summary: Learn the KQL patterns that turn raw endpoint and security telemetry into investigation-ready
  answers — filtering, summarising, joining, and time-series analysis — and how to validate AI-generated
  queries before you trust them.
objectives:
- 'Read and write core KQL operators: where, project, summarize, extend, sort, top'
- Aggregate endpoint telemetry by device, time bin, and category to find patterns
- Join across tables to correlate device state with security events
- Use time-series functions to detect anomalies and trends across the fleet
- Build reusable, parameterised queries that feed dashboards and AI triage
- Validate AI-generated KQL for correctness, scope, and least privilege before running it
video: ht4-l03-kql-for-endpoint-telemetry.mp4
quiz:
- q: Which KQL operator reduces a table to summary rows using aggregation functions like count() and avg()?
  options:
  - project
  - where
  - summarize
  - extend
  answer: 2
  why: summarize aggregates rows into groups using functions such as count(), dcount(), avg() and percentile();
    project selects columns and extend adds computed columns.
- q: To bucket events into hourly windows for a time-series, which expression is correct inside summarize
    ... by?
  options:
  - bin(TimeGenerated, 1h)
  - round(TimeGenerated, 1h)
  - floor(TimeGenerated)
  - hour(TimeGenerated, 1)
  answer: 0
  why: bin(TimeGenerated, 1h) rounds each timestamp down to the start of its hour, the standard way to
    build evenly spaced time buckets for trend and anomaly analysis.
- q: When correlating device inventory with security alerts across two tables, which operator combines
    rows matching on a key?
  options:
  - union
  - join
  - mv-expand
  - parse
  answer: 1
  why: join matches rows from two tables on a shared key (for example DeviceId); union stacks rows from
    multiple tables without matching keys.
- q: An AI assistant hands you a KQL query that uses search * across all tables with no time filter. What
    is the correct first action?
  options:
  - Run it immediately to save time
  - 'Reject or rewrite it: add a time window and scope to specific tables before running, because unbounded
    queries are slow, costly, and over-broad'
  - Schedule it to run nightly
  - Email it to the whole team
  answer: 1
  why: Unbounded search * with no time filter violates least privilege and performance hygiene; validating
    and constraining AI-generated KQL before execution is a core guardrail.
- q: Write a KQL query that returns the top 5 devices by count of failed sign-in events in the last 24
    hours (assume a SigninLogs table with DeviceId and ResultType, where ResultType != 0 means failure).
  answer: SigninLogs | where TimeGenerated > ago(24h) | where ResultType != 0 | summarize failures = count()
    by DeviceId | top 5 by failures desc
  why: The pattern is filter by time, filter to failures, summarize a count per device, then top N by
    that count — the everyday shape of investigation KQL.
- q: Why should you validate the SCOPE of an AI-generated KQL query, not just its syntax, before running
    it?
  answer: Because a syntactically valid query can still pull far more data than needed — too long a time
    range, too many tables, or sensitive columns — which wastes resources and can expose data beyond least
    privilege; checking scope ensures the query only reads what the task and the operator's permissions
    justify.
  why: Correct syntax does not imply correct or safe scope; least privilege applies to queries as much
    as to actions.
resources:
- label: Microsoft Learn — KQL quick reference
  url: https://learn.microsoft.com/en-us/azure/data-explorer/kql-quick-reference
- label: Microsoft Learn — Get started with KQL queries (Log Analytics)
  url: https://learn.microsoft.com/en-us/azure/azure-monitor/logs/get-started-queries
- label: Microsoft Learn — Aggregation functions in KQL (summarize)
  url: https://learn.microsoft.com/en-us/kusto/query/summarize-operator
- label: Microsoft Learn — join operator in KQL
  url: https://learn.microsoft.com/en-us/kusto/query/join-operator
---

## Why KQL is the language of endpoint AIOps

**KQL** — Kusto Query Language — is how you ask questions of telemetry in **Log Analytics**, **Microsoft Sentinel**, **Defender**, and **endpoint analytics**. Every AI assist layer this month either generates KQL for you or reasons over its results, so fluency here is non-negotiable. The good news: KQL reads top to bottom like a pipeline. Data flows left to right through operators separated by the pipe `|`.

## The core operators

Five operators cover most investigations.

```kql
DeviceEvents
| where TimeGenerated > ago(24h)          // filter rows
| where ActionType == "AntivirusDetection" // narrow further
| project TimeGenerated, DeviceName, ActionType, FileName  // pick columns
| sort by TimeGenerated desc               // order
| take 50                                  // limit
```

`where` filters, `project` selects columns, `extend` adds computed columns, `sort` orders, and `take`/`top` limit. Always lead with a **time filter** — it is the cheapest way to keep queries fast and scoped.

## Aggregating to find patterns

Raw events are noise until you **summarize** them. Group by device, category, or time bucket to see shape.

```kql
// Crash counts per device, last 7 days, worst first
DeviceEvents
| where TimeGenerated > ago(7d)
| where ActionType == "ProcessCrash"
| summarize crashes = count() by DeviceName
| top 10 by crashes desc
```

For trends over time, bucket with `bin()`:

```kql
DeviceEvents
| where TimeGenerated > ago(7d)
| summarize events = count() by bin(TimeGenerated, 1h)
| render timechart
```

## Joining to correlate

The real power of AIOps is **correlation** — connecting device state to security events. `join` matches rows from two tables on a key.

```kql
// Devices that are non-compliant AND have a recent security alert
DeviceInfo
| where TimeGenerated > ago(1d)
| where ComplianceState == "NonCompliant"
| project DeviceId, DeviceName
| join kind=inner (
    SecurityAlert
    | where TimeGenerated > ago(1d)
    | project DeviceId, AlertName, Severity
) on DeviceId
```

This single query is exactly the kind of correlated signal you will later hand to an AI for triage.

## Detecting anomalies

For predictive work, KQL has built-in series functions. A spike in failed sign-ins, for instance, jumps out when you compare each hour to the baseline.

```kql
SigninLogs
| where TimeGenerated > ago(7d)
| where ResultType != 0
| summarize failures = count() by bin(TimeGenerated, 1h)
| sort by TimeGenerated asc
```

## Guardrails: validate AI-generated KQL before you run it

Copilot and triage agents will write KQL for you. Treat every generated query as untrusted until checked. Confirm three things: a **bounded time window** (never `search *` with no `ago()`), the **right tables** (not every table in the workspace), and **least-privilege columns** (no sensitive fields the task does not need). A syntactically perfect query can still over-read. Validating scope is as important as validating syntax.

## Your task

In your workspace, write three queries: a top-10 devices-by-error summary using `summarize` and `top`; a one-hour `bin()` time-series rendered as a timechart; and a `join` that correlates non-compliant devices with recent alerts. Then take any AI-generated KQL, and write two sentences on how you validated its time window and scope before running it.
