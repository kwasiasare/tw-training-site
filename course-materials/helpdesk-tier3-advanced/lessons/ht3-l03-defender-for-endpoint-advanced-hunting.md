---
course: helpdesk-tier3-advanced
title: Microsoft Defender for Endpoint and advanced hunting
month: 3
monthTitle: Advanced Endpoint Security & Identity
lesson: 3
summary: Tour the full Defender for Endpoint platform — next-gen AV, EDR, attack surface reduction and
  threat & vulnerability management — then learn to query its raw telemetry with KQL advanced hunting
  and turn a query into a custom detection rule.
objectives:
- 'Describe the core Defender for Endpoint capabilities: next-gen AV, EDR, ASR rules, network protection
  and TVM'
- Compare onboarding methods and explain what telemetry an onboarded device emits
- Navigate the advanced hunting data model and identify the key Device* schema tables
- Write KQL using where, project, summarize, parse and join across DeviceProcessEvents, DeviceNetworkEvents
  and DeviceLogonEvents
- Promote a validated hunting query into a custom detection rule and map findings to MITRE ATT&CK
- Use the device timeline and live response for hands-on investigation and remediation
video: ht3-l03-defender-for-endpoint-advanced-hunting.mp4
quiz:
- q: Which Defender for Endpoint capability proactively reduces the available attack surface by blocking
    risky behaviours such as Office apps spawning child processes?
  options:
  - Attack surface reduction (ASR) rules
  - Threat & vulnerability management
  - Automated investigation and remediation
  - Network protection
  answer: 0
  why: ASR rules are configurable controls that block or audit risky behaviours (Office child processes,
    obfuscated scripts, credential theft from LSASS), shrinking the attack surface before an exploit can
    run.
- q: In advanced hunting, which KQL operator is correct for selecting only the columns you want to keep
    in the result set?
  options:
  - select
  - filter
  - project
  - extract
  answer: 2
  why: project chooses and reshapes the columns returned; where filters rows. KQL has no select keyword,
    and parse/extract pull substrings out of a single field.
- q: You want to correlate a suspicious process with the network connections it made. Which two schema
    tables and join key are most appropriate?
  options:
  - DeviceFileEvents joined on SHA256
  - DeviceProcessEvents and DeviceNetworkEvents joined on DeviceId and InitiatingProcessId
  - DeviceLogonEvents joined on AccountSid
  - DeviceRegistryEvents joined on RegistryKey
  answer: 1
  why: Process-to-network correlation joins DeviceProcessEvents and DeviceNetworkEvents; the network table
    records the InitiatingProcess* fields, so you match on DeviceId plus the initiating process identity
    to tie a connection back to its parent process.
- q: What is the effect of promoting a validated advanced hunting query into a custom detection rule?
  options:
  - It deletes the underlying telemetry to save storage
  - It runs the query on a schedule and generates alerts plus optional automated response actions
  - It exports the query to a CSV once and stops
  - It disables the built-in Microsoft detections
  answer: 1
  why: A custom detection rule runs your KQL on a recurring frequency, raises an alert when rows return,
    and can trigger response actions such as isolating the device or collecting an investigation package.
- q: Name the advanced hunting schema table you would query to investigate interactive and remote sign-in
    activity on a device, and one field you would use to spot anomalous logons.
  answer: DeviceLogonEvents. Useful fields include LogonType (for example Interactive, Network, RemoteInteractive),
    AccountName, RemoteIP and ActionType (LogonSuccess or LogonFailed) to spot brute force or unusual
    remote logons.
  why: DeviceLogonEvents records authentication on the device; LogonType plus failed/success ActionType
    and source RemoteIP reveal lateral movement, password spraying and unexpected RemoteInteractive (RDP)
    sessions.
- q: In one sentence, explain why mapping a hunting finding to MITRE ATT&CK is valuable during an investigation.
  answer: Mapping to ATT&CK tactics and techniques gives the behaviour a shared, standard name so you
    can communicate it clearly, find related detections, anticipate the attacker's next likely step and
    measure your coverage gaps.
  why: ATT&CK provides a common taxonomy of adversary tactics and techniques; framing findings against
    it turns isolated observations into an understandable kill-chain and drives consistent, comparable
    detection engineering.
resources:
- label: Microsoft Learn — Microsoft Defender for Endpoint overview
  url: https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint
- label: Microsoft Learn — Advanced hunting overview
  url: https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-overview
- label: Microsoft Learn — Kusto Query Language (KQL) overview
  url: https://learn.microsoft.com/en-us/kusto/query/
- label: Microsoft Learn — DeviceProcessEvents schema table
  url: https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table
---

## What Defender for Endpoint actually is

**Microsoft Defender for Endpoint (MDE)** is not a single antivirus product; it is a layered endpoint protection platform. The layers worth knowing: **next-generation antivirus** (cloud-backed, behaviour-based protection), **endpoint detection and response (EDR)** that records rich behavioural telemetry and raises alerts, **attack surface reduction (ASR) rules** that block risky behaviours like an Office app spawning a child process, **network protection** that blocks connections to malicious domains and IPs, and **threat & vulnerability management (TVM)** that inventories software and surfaces exploitable CVEs with remediation guidance.

The layer that makes MDE a hunting platform is EDR: every onboarded device continuously streams **behavioural telemetry** — process creations, network connections, file writes, logons, registry edits — into the cloud where you can query it.

## Onboarding and the data it produces

A device only contributes telemetry once it is **onboarded**. Common methods: **Intune** (the modern default for managed Windows), **Group Policy** or a local **onboarding script**, **Microsoft Configuration Manager**, and platform-native onboarding for macOS and Linux. Onboarding installs the sensor and connects the device to your tenant. From that moment its events flow into the **advanced hunting** schema.

## The advanced hunting data model

**Advanced hunting** is a query-based investigation tool over up to 30 days of raw event data, written in **KQL** (Kusto Query Language). The schema is organised into tables; the endpoint ones are prefixed `Device`:

- `DeviceProcessEvents` — process creations and command lines.
- `DeviceNetworkEvents` — outbound and inbound connections.
- `DeviceFileEvents` — file create, modify, rename, delete.
- `DeviceLogonEvents` — interactive, network and remote logons.
- `DeviceRegistryEvents`, `DeviceImageLoadEvents`, `DeviceEvents` — registry, DLL loads and miscellaneous sensor events.

Every row carries `DeviceId`, `Timestamp` and a set of `InitiatingProcess*` columns describing the parent process — these are the keys you join on.

## Writing KQL over the schema

KQL reads top to bottom, piping a table through operators. The core verbs are **where** (filter rows), **project** (choose columns), **summarize** (aggregate), **parse** (extract from a string) and **join** (correlate tables). Hunt for a script interpreter launched from Office:

```kql
DeviceProcessEvents
| where Timestamp > ago(7d)
| where InitiatingProcessFileName in~ ("winword.exe", "excel.exe", "outlook.exe")
| where FileName in~ ("powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe")
| project Timestamp, DeviceName, InitiatingProcessFileName, FileName, ProcessCommandLine
| sort by Timestamp desc
```

Now correlate suspicious processes with the connections they made by **joining** the process and network tables on the device and initiating process:

```kql
let suspect = DeviceProcessEvents
| where Timestamp > ago(1d)
| where FileName =~ "powershell.exe"
| where ProcessCommandLine has_any ("-enc", "DownloadString", "FromBase64String");
suspect
| join kind=inner (
    DeviceNetworkEvents
    | where Timestamp > ago(1d)
) on DeviceId, $left.ProcessId == $right.InitiatingProcessId
| summarize Connections = count() by DeviceName, RemoteUrl, RemoteIP, ProcessCommandLine
| sort by Connections desc
```

## From query to detection and investigation

A query that reliably finds bad behaviour should not stay manual. Use **Create detection rule** to schedule the KQL, raise an alert when rows return, and optionally trigger response actions. Each alert is mapped to **MITRE ATT&CK** tactics and techniques so the behaviour gets a shared name and a place in the kill chain.

For hands-on work, the **device timeline** shows a chronological event stream, and **live response** gives you a secure remote shell:

```text
live response session (analyst):
  connect <deviceId>
  getfile "C:\Users\Public\dropper.ps1"   # collect evidence
  processes                                  # list running processes
  remediate file <SHA1>                      # quarantine
  run TriageScript.ps1                        # run a library script
```

Isolation, package collection and file quarantine can all be driven from here or automated by the detection rule.

## Your task

In a test tenant's advanced hunting, write a query that hunts for likely lateral movement: find `DeviceLogonEvents` with `LogonType == "RemoteInteractive"` (RDP) where the same `RemoteIP` produced more than five `LogonFailed` events before a `LogonSuccess` within an hour. Use `summarize` with `count()` and time bucketing, `project` only the fields an analyst needs, then join back to `DeviceProcessEvents` to show what the successful session ran. Finally, describe how you would promote it to a custom detection rule and which ATT&CK technique it maps to.
