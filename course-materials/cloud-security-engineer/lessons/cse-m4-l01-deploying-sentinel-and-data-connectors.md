---
course: cloud-security-engineer
title: Deploying Microsoft Sentinel and Data Connectors
month: 4
monthTitle: Cloud SIEM & SOAR Operations with Microsoft Sentinel
lesson: 1
summary: 'Microsoft Sentinel is a cloud-native SIEM and SOAR that runs on top of an Azure Monitor Log
  Analytics workspace, so every design decision starts with the workspace. In this lesson you design the
  workspace (single vs. multi-workspace, RBAC, retention and archive, table plans and commitment tiers)
  and weigh the cost levers that make or break a SOC budget. You then enable Sentinel, install Content
  hub solutions, and wire up the core data connectors you need for the rest of the module: Microsoft Entra
  ID, Microsoft 365, Azure Activity, Microsoft Defender XDR, and third-party firewalls via CEF/Syslog
  over AMA or the Codeless Connector Platform. Finally you meet the unified Microsoft Defender portal
  experience and ASIM normalization. By the end you can stand up a Sentinel workspace ingesting M365,
  Entra, Azure Activity, and firewall logs, the exact telemetry Capstone 3 depends on.'
objectives:
- Explain how Microsoft Sentinel layers SIEM and SOAR on a Log Analytics workspace and what that means
  for design
- Design workspace topology, RBAC, retention/archive, and table plans to balance visibility against ingestion
  cost
- Enable Microsoft Sentinel and install the right solutions from the Content hub
- Connect Microsoft Entra ID, Microsoft 365, Azure Activity, and Defender XDR data connectors
- Ingest third-party firewall logs using CEF/Syslog via the Azure Monitor Agent or the Codeless Connector
  Platform
- Describe the unified Microsoft Defender portal experience and the role of ASIM normalization
video: cse-m4-l01-deploying-sentinel-and-data-connectors.mp4
quiz:
- q: Microsoft Sentinel stores and queries its data using which underlying Azure service?
  options:
  - An Azure SQL managed instance dedicated to Sentinel
  - An Azure Monitor Log Analytics workspace
  - An Azure Storage account with blob containers
  - A Cosmos DB graph database
  answer: 1
  why: Sentinel is a solution that runs on top of an Azure Monitor Log Analytics workspace. All ingested
    logs land in tables in that workspace and are queried with KQL, which is why workspace design (region,
    RBAC, retention, table plans) is the foundation of every Sentinel deployment.
- q: A SOC ingests roughly 250 GB of logs per day. Which pricing choice typically lowers cost the most?
  options:
  - Stay on Pay-As-You-Go because it is always cheapest
  - Move the workspace to a cheaper Azure region
  - Switch to a Commitment Tier (capacity reservation) sized at or below daily volume
  - Disable the workspace overnight to avoid ingestion
  answer: 2
  why: At steady, predictable volume a Commitment Tier (capacity reservation, e.g. 100/200/300 GB/day)
    gives a meaningful discount over Pay-As-You-Go. You commit to a daily tier and any overage is billed
    at the effective tier rate, so sizing the tier near your true daily ingestion is the main cost lever.
- q: Which table plan is the cheapest to ingest but is intended for high-volume, lower-fidelity logs and
    is queried with a limited KQL experience?
  options:
  - Analytics (interactive) plan
  - Basic / Auxiliary logs plan
  - Archive tier
  - Commitment tier
  answer: 1
  why: The Basic and Auxiliary logs plans cost far less to ingest than the Analytics plan but support
    only a subset of KQL and a short interactive retention, making them suitable for verbose, low-value-per-record
    sources (like raw firewall or network logs) you mostly need for occasional investigation rather than
    real-time analytics.
- q: What is the recommended way to ingest CEF and Syslog from a third-party firewall into Sentinel today?
  options:
  - Install the legacy Log Analytics agent (MMA) directly on the firewall
  - Forward events to a Linux log forwarder running the Azure Monitor Agent with a Data Collection Rule
  - Upload firewall logs manually as CSV each morning
  - Point the firewall at the Sentinel REST API with no collector
  answer: 1
  why: Firewalls send CEF/Syslog over the network to a Linux log forwarder VM running the Azure Monitor
    Agent (AMA). A Data Collection Rule (DCR) tells AMA which facilities/severities to collect and routes
    them into the CommonSecurityLog or Syslog tables. The legacy MMA agent is retired, and many appliances
    now also have Codeless Connector Platform connectors.
- q: What does the Advanced Security Information Model (ASIM) provide in Sentinel?
  options:
  - A billing model that caps ingestion cost automatically
  - A set of normalized schemas and parsers so queries work across many source products
  - A replacement for KQL with a graphical query builder
  - An automatic incident-response playbook engine
  answer: 1
  why: ASIM defines normalized schemas (for example for authentication, network sessions, process events)
    plus parsers that map vendor-specific tables into those schemas. A detection written against an ASIM
    schema (e.g. imNetworkSession) runs across many firewall and proxy products without rewriting the
    query for each vendor's raw table.
- q: In 3-4 sentences, explain why workspace topology (single vs. multi-workspace) and RBAC must be decided
    before you turn on connectors, and give one concrete trade-off of consolidating everything into a
    single workspace.
  answer: Topology and RBAC determine who can read which logs and where data physically lives, and connectors
    immediately begin writing billable data into whatever workspace you target, so changing the decision
    later means re-homing data, re-scoping roles, and re-pointing connectors. A single workspace simplifies
    cross-source KQL hunting and correlation because all tables sit together, and it is easier to manage
    and often cheaper. The trade-off is that table-level RBAC is coarser, so you may over-expose sensitive
    logs to analysts, and you can hit data-residency or delegated-administration limits when teams or
    regions must be isolated. Multi-workspace gives stronger isolation and residency control but fragments
    queries and can raise cost and management overhead.
  why: 'Workspace design is foundational: it sets data residency, the RBAC blast radius, query convenience,
    and cost. Because connectors write data the moment they are enabled, getting topology and access right
    up front avoids painful re-architecture.'
resources:
- label: Plan for Microsoft Sentinel workspace architecture
  url: https://learn.microsoft.com/en-us/azure/sentinel/best-practices-workspace-architecture
- label: Microsoft Sentinel data connectors reference
  url: https://learn.microsoft.com/en-us/azure/sentinel/data-connectors-reference
- label: Ingest CEF and Syslog with the Azure Monitor Agent
  url: https://learn.microsoft.com/en-us/azure/sentinel/connect-cef-syslog-ama
- label: Advanced Security Information Model (ASIM) overview
  url: https://learn.microsoft.com/en-us/azure/sentinel/normalization
---

## Sentinel Is a Solution on a Log Analytics Workspace

The single most important fact about Microsoft Sentinel is that it is **not a standalone database**. Sentinel is a SIEM (Security Information and Event Management) and SOAR (Security Orchestration, Automation, and Response) solution that you enable **on top of an Azure Monitor Log Analytics workspace**. Every log you ingest lands in a table in that workspace, and you query those tables with **KQL** (Kusto Query Language). Analytics rules, hunting, workbooks, and automation all read from the same workspace.

Because of this, **workspace design is security design**. The workspace decides where data physically lives (region / data residency), who can read it (RBAC), how long it is kept (retention and archive), and what you pay (table plans and commitment tiers). Get these wrong and you either blow the budget, lose the visibility you need to detect attacks, or expose sensitive logs to the wrong analysts. So we design the workspace first, then turn on connectors.

## Workspace Topology and RBAC

The first decision is **single workspace vs. multi-workspace**.

- **Single workspace** keeps all telemetry together. Cross-source hunting is trivial because `SigninLogs`, `SecurityEvent`, and `CommonSecurityLog` all sit side by side, so a single `union` or `join` correlates identity, endpoint, and network. It is simpler and usually cheaper to manage. The downside is coarser isolation: table-level RBAC helps, but it is easy to over-share sensitive data, and you may hit data-residency or delegated-admin needs you cannot satisfy in one region.
- **Multi-workspace** (often one per region, business unit, or tenant in MSSP scenarios) gives strong isolation and residency control but fragments your queries — you must use **cross-workspace queries** (`workspace("name").TableName`) and accept more management overhead.

For RBAC, prefer the **Sentinel-specific Azure roles** over broad workspace ownership:

- **Microsoft Sentinel Reader** — view data, incidents, workbooks.
- **Microsoft Sentinel Responder** — the above plus manage incidents (assign, change status, add comments).
- **Microsoft Sentinel Contributor** — create and edit analytics rules, workbooks, and other content.

Scope these at the resource group containing the workspace, and use **table-level RBAC** when a subset of analysts should see only certain tables.

## Retention, Archive, and Table Plans (the Cost Levers)

Ingestion and retention are where SOC budgets live or die. Three levers matter:

1. **Interactive retention** — how long data stays fully queryable with the normal interactive KQL experience. Defaults can be extended per-table; longer interactive retention costs more.
2. **Archive (long-term retention)** — after the interactive period, data can roll into a low-cost **archive tier** for up to several years. Archived data is cheap to store but you pay a small fee to run **search jobs** or **restore** it for investigation.
3. **Table plans** — each table has a plan:
   - **Analytics** plan: full KQL, real-time analytics rules, normal retention. Most expensive per GB. Use it for high-value security tables (sign-ins, audit, Defender alerts).
   - **Basic / Auxiliary logs** plan: much cheaper ingestion, limited KQL, short interactive retention. Use it for verbose, low-value-per-record sources you mostly need for occasional lookup (raw network/firewall noise).

On top of plans sits the **pricing model**. **Pay-As-You-Go** bills per GB ingested. **Commitment Tiers** (capacity reservations such as 100, 200, 300+ GB/day) give a discount when you commit to a predictable daily volume; overage is billed at the tier's effective rate. At steady, predictable volume, sizing a commitment tier at or just below your true daily ingestion is the biggest single cost win.

> Rule of thumb: route security-critical, frequently-queried logs to the **Analytics** plan, push high-volume noise to **Basic/Auxiliary**, archive the rest, and right-size a **commitment tier** once your daily GB stabilizes.

## Enabling Sentinel and the Content Hub

Enabling Sentinel is quick: create (or select) a Log Analytics workspace, then add the **Microsoft Sentinel** resource onto it. The cost and capability all come from what you ingest afterward.

The **Content hub** is the marketplace for Sentinel content. Instead of wiring connectors one by one, you install **solutions** — packaged bundles that include data connectors, analytics rule templates, hunting queries, workbooks, parsers, and playbooks for a given product (for example the *Microsoft Entra ID*, *Azure Activity*, or *Palo Alto Networks* solutions). Installing a solution is the modern, supported way to light up a source end to end.

## The Core Data Connectors

For this module and for Capstone 3 you need four first-party sources plus firewalls:

- **Microsoft Entra ID** — sign-in and audit logs. This connector configures **diagnostic settings** on Entra ID to stream into the workspace, populating the `SigninLogs`, `AADNonInteractiveUserSignInLogs`, and `AuditLogs` tables (the backbone of identity threat hunting).
- **Microsoft 365 (Office 365)** — Exchange, SharePoint, and Teams activity into `OfficeActivity`.
- **Azure Activity** — control-plane operations across subscriptions into the `AzureActivity` table (who created/changed/deleted Azure resources).
- **Microsoft Defender XDR** — streams **alerts and raw advanced-hunting tables** (e.g. `DeviceProcessEvents`, `DeviceNetworkEvents`, `EmailEvents`, `IdentityLogonEvents`) from Defender for Endpoint/Identity/Office/Cloud Apps into Sentinel for unified correlation.

Most first-party connectors are configured with a click plus the right permissions (often Security Administrator or Global Administrator for the initial diagnostic-setting wiring).

## Third-Party Firewalls: CEF/Syslog via AMA and the Codeless Connector Platform

Non-Microsoft appliances (Palo Alto, Fortinet, Check Point, Cisco ASA, etc.) typically emit **CEF** (Common Event Format) or plain **Syslog** over the network. The supported pattern today:

1. Stand up a **Linux log-forwarder VM** running the **Azure Monitor Agent (AMA)**.
2. Point the firewalls' syslog output at that forwarder.
3. Attach a **Data Collection Rule (DCR)** that selects the facilities/severities to collect and routes them into the **`CommonSecurityLog`** table (CEF) or **`Syslog`** table (plain syslog).

The legacy Log Analytics agent (MMA) is retired — **AMA + DCR is the current method**. Increasingly, vendors also ship **Codeless Connector Platform (CCP)** connectors that pull logs directly via API with no collector VM, which you install straight from the Content hub.

```kusto
// Confirm firewall CEF events are landing and see top devices
CommonSecurityLog
| where TimeGenerated > ago(1h)
| summarize Events = count() by DeviceVendor, DeviceProduct, Computer
| sort by Events desc
```

## The Unified Defender Portal and ASIM

Microsoft has converged operations into the **unified Microsoft Defender portal** (security.microsoft.com), where Sentinel incidents, hunting, and Defender XDR investigation live in one place — when a workspace is onboarded, analysts triage Sentinel and XDR incidents together rather than switching consoles.

Finally, normalization. Different firewalls log to different schemas, which would force you to rewrite every detection per vendor. The **Advanced Security Information Model (ASIM)** solves this: it defines **normalized schemas** (authentication, network session, process events, DNS, and more) plus **parsers** that map each vendor's raw table into the common schema. Write a detection once against an ASIM schema and it runs across many products:

```kusto
// Normalized network-session query that works across many firewall/proxy vendors
imNetworkSession
| where TimeGenerated > ago(24h)
| where DstPortNumber == 3389
| summarize Sessions = count() by SrcIpAddr, DstIpAddr
| sort by Sessions desc
```

You now have the foundation: a cost-aware workspace ingesting Entra ID, M365, Azure Activity, Defender XDR, and firewall logs — exactly the telemetry the rest of the module (and Capstone 3) builds detections on.
