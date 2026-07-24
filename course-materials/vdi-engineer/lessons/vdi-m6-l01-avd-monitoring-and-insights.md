---
course: vdi-engineer
title: 'AVD Monitoring and Insights: Log Analytics, Workbooks, and KQL'
month: 6
monthTitle: Monitoring, Operations & Troubleshooting
lesson: 1
summary: 'Before you can operate an Azure Virtual Desktop estate at scale you need eyes on it, and that
  starts with Azure Virtual Desktop Insights. This lesson walks through the full monitoring data path:
  enabling diagnostic settings on host pools and workspaces, wiring session hosts to a Log Analytics workspace
  through the Azure Monitor Agent and a data collection rule, and understanding the family of WVD-prefixed
  tables that carry connection, error, checkpoint, host-registration, agent-health, and network telemetry.
  You''ll write real KQL queries against verified table and column names to find connection failures,
  track round-trip time, and calculate session duration, then set up log alerts so problems surface before
  users complain.'
objectives:
- Explain what Azure Virtual Desktop Insights is built on and what data sources feed it
- Enable AVD diagnostic settings on host pools and workspaces and identify the supported diagnostic categories
- Configure the Azure Monitor Agent data collection path for session hosts using a data collection rule
- Identify the core WVD Log Analytics tables and the columns each one actually contains
- Write KQL queries to find connection failures, round-trip time trends, and per-user session duration
- Configure an Azure Monitor log alert against AVD telemetry
quiz:
- q: Azure Virtual Desktop Insights is a dashboard built on top of which Azure Monitor feature?
  options:
  - Azure Monitor Workbooks
  - A standalone Log Analytics workspace with no other dependency
  - Azure Data Explorer clusters
  - Application Insights availability tests
  answer: 0
  why: Microsoft Learn describes Azure Virtual Desktop Insights as 'a dashboard built on Azure Monitor
    Workbooks.' It reads from a Log Analytics workspace, but the dashboard layer itself is Workbooks.
- q: Which agent does Microsoft require today to collect performance counters and Windows Event Logs from
    AVD session hosts for Insights?
  options:
  - The legacy Log Analytics agent (MMA)
  - The Azure Monitor Agent (AMA), associated to hosts via a Data Collection Rule
  - The Dependency agent only
  - No agent is needed; diagnostic settings cover everything
  answer: 1
  why: Current AVD Insights setup requires the Azure Monitor Agent plus a Data Collection Rule on each
    session host. The legacy Log Analytics (MMA) agent was deprecated August 31, 2024, and its backend
    services stop entirely on March 2, 2026 — do not design new monitoring on it.
- q: Which table would you query to see the estimated round-trip time for a user's connection?
  options:
  - WVDConnections
  - WVDCheckpoints
  - WVDConnectionNetworkData
  - WVDAgentHealthStatus
  answer: 2
  why: WVDConnectionNetworkData carries EstRoundTripTimeInMs and EstAvailableBandwidthKBps, keyed by CorrelationId
    and TimeGenerated. WVDConnections has connection metadata and state, not network quality metrics.
- q: In the WVDErrors table, which column tells you whether an error is a Microsoft service-side problem
    you must escalate, versus one you can likely resolve yourself?
  options:
  - CodeSymbolic
  - Source
  - ActivityType
  - ServiceError
  answer: 3
  why: ServiceError is a boolean. When it's true, escalate to Microsoft support and supply the CorrelationId.
    When it's false, the error is something an admin task can typically resolve.
- q: Which host pool diagnostic category and table pair correctly reports whether the AVD agent on a session
    host is currently healthy?
  options:
  - AgentHealthStatus -> WVDAgentHealthStatus
  - Checkpoints -> WVDCheckpoints
  - Feed -> WVDFeeds
  - Errors -> WVDErrors
  answer: 0
  why: The AgentHealthStatus diagnostic category writes to the WVDAgentHealthStatus table, which includes
    Status, LastHeartBeat, ActiveSessions, and AgentVersion per session host.
- q: You want the average session duration for users over the last day, using the WVDConnections table
    you already have enabled. Describe, in your own words, the approach you'd take in KQL to compute it
    (exact syntax not required).
  answer: 'Filter WVDConnections to the last day, then use CorrelationId as the join key that ties together
    the rows for a single connection: the row where State == "Connected" gives the start time (its TimeGenerated),
    and the row where State == "Completed" for the same CorrelationId gives the end time. Join those two
    projections on CorrelationId, compute the time difference between the two TimeGenerated values as
    the session duration, and then summarize (e.g., average) that duration, optionally grouped by UserName
    or SessionHostName.'
  why: This mirrors the documented connection state machine (Started, Connected, Completed) and the CorrelationId-based
    self-join Microsoft's own sample query uses to compute session duration.
resources:
- label: Enable Insights to monitor Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/insights
- label: Send Azure Virtual Desktop diagnostics to Log Analytics
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics
- label: 'Azure Monitor Logs reference: WVDConnections table'
  url: https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/wvdconnections
- label: Azure Monitor Agent overview
  url: https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-overview
- label: Log alerts in Azure Monitor
  url: https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-log
---

## Why Monitoring Gets Its Own AZ-140 Domain

Everything you built in Modules 3 through 5 — host pools, networking, golden images, identity, FSLogix — eventually meets real users on a Tuesday morning, and something will go sideways. AZ-140's fourth domain, Monitor and maintain AVD infrastructure, exists because a platform you can't observe is a platform you can only guess about. This lesson builds the observability foundation the rest of Module 6 assumes: Azure Virtual Desktop Insights, the Log Analytics tables underneath it, and the KQL you'll actually run at 8am when the help desk queue starts filling up.

## What Azure Virtual Desktop Insights Actually Is

AVD Insights is not a separate monitoring product. It's a dashboard built on **Azure Monitor Workbooks**, reading data out of a Log Analytics workspace that you point at your AVD environment. Open it at `aka.ms/avdi` in the Azure portal, and the first thing you should do on a new environment is run its **Check Configuration** workbook — it audits whether the pieces below are actually wired up, and gives you one-click remediation when they aren't.

Two RBAC roles are the minimum to view it: **Desktop Virtualization Reader** on the resource group/subscription holding your host pools, and **Log Analytics Reader** on the workspace. Neither role lets you *change* anything — that still requires separate AVD admin permissions.

## The Data Path: Diagnostic Settings + Azure Monitor Agent

Insights needs two independent data feeds, and it's a common deployment mistake to set up only one:

1. **Resource diagnostic settings** on the AVD host pool and workspace objects (these are Azure Resource Manager objects, not VMs). You enable the diagnostic categories: **Management Activities, Feed, Connections, Errors, Checkpoints, HostRegistration, AgentHealthStatus** (host pool) and **Management Activities, Feed, Errors, Checkpoints** (workspace), each streamed to your designated Log Analytics workspace.
2. **Session host telemetry** via the **Azure Monitor Agent (AMA)**, associated to each session host through a **Data Collection Rule (DCR)** that defines which performance counters and Windows Event Logs to collect. This is a per-VM agent install, not a resource-level setting, and it's the part people forget after adding new hosts to a pool.

A critical, exam-relevant fact: the legacy **Log Analytics agent (MMA)** is not an option here. Microsoft deprecated it on **August 31, 2024**, data uploads were scheduled to briefly pause on **January 26, 2026** as a test, and the backend services shut down entirely on **March 2, 2026**. If you inherit an environment still running MMA for AVD monitoring, migrating it to AMA is not optional maintenance — it's a hard deadline that has now passed the point of safe delay.

## The WVD Table Family

Every AVD-related table in Log Analytics is prefixed `WVD` (a holdover from the service's original Windows Virtual Desktop name). The ones you'll use constantly:

| Table | What it holds | Key columns |
|---|---|---|
| `WVDConnections` | Connection lifecycle events (Started/Connected/Completed) | `CorrelationId`, `UserName`, `State`, `SessionHostName`, `ResourceAlias`, `TransportType`, `TimeGenerated` |
| `WVDErrors` | Errors across management, host registration, and feed activity | `CodeSymbolic`, `Code`, `Message`, `ServiceError`, `Source`, `CorrelationId`, `UserName` |
| `WVDCheckpoints` | Intermediate steps within an activity (e.g., app launches inside a desktop session) | `ActivityType`, `Name`, `CorrelationId`, `Parameters` |
| `WVDHostRegistrations` | Whether a session host successfully registered with the service | `SessionHostName`, `SessionHostIPAddress`, `CorrelationId` |
| `WVDAgentHealthStatus` | Live health/heartbeat of the AVD agent per host, roughly every 30 seconds | `SessionHostName`, `Status`, `AgentVersion`, `ActiveSessions`, `InactiveSessions`, `LastHeartBeat` |
| `WVDConnectionNetworkData` | Estimated network quality per connection | `CorrelationId`, `EstRoundTripTimeInMs`, `EstAvailableBandwidthKBps` |
| `WVDManagement` | Admin/API/PowerShell management activity | `CorrelationId`, `ActivityType` |
| `WVDFeeds` | Whether users could subscribe to a workspace's app feed | `CorrelationId`, `UserName` |

Note the exact casing and pluralization — `WVDHostRegistrations` and `WVDFeeds` are plural, `WVDManagement` is not `WVDManagementActivities`, and there is no `WVDErrors` alternate spelling. Typos here are the single most common reason a working query returns zero rows.

## Starter KQL Queries You'll Actually Run

**Connection failures in the last 24 hours, grouped by cause:**

```kusto
WVDErrors
| where TimeGenerated > ago(24h)
| where ServiceError == false
| summarize FailureCount = count() by CodeSymbolic, Source
| sort by FailureCount desc
```

Filtering `ServiceError == false` isolates admin-actionable errors first; flip it to `true` to see what you'd need to open a Microsoft support case for.

**Round-trip time trend over the last week:**

```kusto
WVDConnectionNetworkData
| where TimeGenerated > ago(7d)
| summarize AvgRoundTripMs = avg(EstRoundTripTimeInMs), AvgBandwidthKBps = avg(EstAvailableBandwidthKBps) by bin(TimeGenerated, 1h)
| render timechart
```

**Session duration by user, using the documented CorrelationId self-join pattern:**

```kusto
let Events = WVDConnections | where TimeGenerated > ago(1d);
Events
| where State == "Connected"
| project CorrelationId, UserName, SessionHostName, StartTime = TimeGenerated
| join kind=inner (
    Events
    | where State == "Completed"
    | project CorrelationId, EndTime = TimeGenerated
) on CorrelationId
| extend DurationMinutes = datetime_diff('minute', EndTime, StartTime)
| project UserName, SessionHostName, DurationMinutes
| sort by DurationMinutes desc
```

**Session hosts currently reporting unhealthy:**

```kusto
WVDAgentHealthStatus
| where TimeGenerated > ago(1h)
| summarize arg_max(TimeGenerated, *) by SessionHostName
| where Status != "Healthy"
| project SessionHostName, Status, AgentVersion, LastHeartBeat
```

`arg_max` here picks the most recent heartbeat row per host so you're not double-counting stale status snapshots.

## Alerting on What Matters

Dashboards you have to remember to open don't catch 2am problems. Wrap the queries above (or simpler thresholds) in **Azure Monitor log alerts**: an alert rule on a scheduled query, with an action group that pages your on-call or posts to a Teams channel. Reasonable first alerts for a production estate: a spike in `WVDErrors` with `ServiceError == false` over a short window (config/auth problems), any `WVDAgentHealthStatus` row reporting `Status != "Healthy"` for more than a few minutes, and a sustained rise in average `EstRoundTripTimeInMs`. Start with a small set of high-signal alerts — alert fatigue from noisy thresholds is what gets monitoring ignored six weeks after go-live.

## What You'd Actually Do

On a new AVD environment: create a dedicated Log Analytics workspace for AVD, run the Insights Check Configuration workbook, enable diagnostic settings on every host pool and workspace, deploy AMA plus a DCR to every session host (Azure Policy can auto-remediate this as hosts are added), confirm data is flowing with a quick `WVDConnections | take 10`, then build two or three log alerts before you call monitoring 'done.' Everything in the rest of this module — image lifecycle, troubleshooting, day-2 operations — assumes this pipeline is already live.
