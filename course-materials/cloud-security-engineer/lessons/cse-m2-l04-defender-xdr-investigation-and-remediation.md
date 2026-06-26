---
course: cloud-security-engineer
title: 'Defender XDR: Automated Investigation and Remediation'
month: 2
monthTitle: Modern Endpoint Security & Threat Protection
lesson: 4
summary: Module 2 closes by zooming out from a single endpoint to the unified Microsoft Defender XDR console.
  You will see how XDR correlates alerts across identity, endpoints, email, and cloud apps into a single
  incident with a full attack story. You will configure Automated Investigation and Remediation (AIR)
  and choose automation levels from semi- to fully automated, then use the Action center to approve or
  auto-approve remediation actions. You will get a first taste of advanced hunting across the XDR schema
  (the deep KQL lands in Module 4) and see how attack disruption and AIR slash analyst workload.
objectives:
- Navigate the Microsoft Defender XDR portal as the unified SOC console.
- Explain how XDR correlates cross-domain alerts into a single incident with an attack story.
- Configure Automated Investigation and Remediation and select an appropriate automation level.
- Use the Action center to review, approve, or auto-approve pending and completed remediation actions.
- Run a basic advanced hunting query across the XDR schema to pivot during an investigation.
- Describe automatic attack disruption and quantify how AIR reduces analyst load.
video: cse-m2-l04-defender-xdr-investigation-and-remediation.mp4
quiz:
- q: What is the primary value of an incident in Microsoft Defender XDR versus a single alert?
  options:
  - It is just a renamed alert
  - It correlates related alerts and evidence across identity, endpoint, email, and cloud apps into one
    attack story
  - It only shows endpoint alerts
  - It disables Conditional Access
  answer: 1
  why: An XDR incident stitches together related alerts and entities from multiple domains so an analyst
    sees the full scope and timeline of an attack instead of triaging disconnected signals.
- q: What does Automated Investigation and Remediation (AIR) do when an alert triggers it?
  options:
  - It only emails the analyst
  - It runs an automated playbook that investigates entities, determines a verdict, and proposes or takes
    remediation actions
  - It deletes the device from Intune
  - It rewrites Conditional Access policies
  answer: 1
  why: 'AIR mimics an analyst''s investigation steps automatically: it examines files, processes, and
    accounts, reaches a verdict, and either takes remediation actions or queues them for approval based
    on the automation level.'
- q: In a 'Semi - require approval' automation level, what happens to remediation actions?
  options:
  - They are applied immediately with no review
  - They are queued in the Action center for an analyst to approve before they run
  - They are silently discarded
  - They are emailed to the end user
  answer: 1
  why: Semi-automated levels investigate automatically but hold remediation actions in the Action center
    pending human approval, balancing speed with control.
- q: Where do analysts review, approve, or undo remediation actions taken or proposed by automation?
  options:
  - The Action center
  - The Intune compliance blade
  - The Entra sign-in logs
  - The BitLocker recovery portal
  answer: 0
  why: The Action center is the single pane for pending and completed remediation actions across Defender
    XDR, where analysts approve, reject, or undo them.
- q: What is automatic attack disruption in Defender XDR?
  options:
  - A manual quarterly review
  - A capability that uses high-confidence signals to automatically contain an in-progress attack, e.g.
    disabling an account or isolating a device
  - A reporting dashboard only
  - A licensing tier
  answer: 1
  why: Attack disruption acts on high-confidence XDR signals to automatically contain active attacks -
    such as suspending a compromised user or isolating a device - to limit blast radius before an analyst
    engages.
- q: In 2-4 sentences, explain the trade-off between fully automated and semi-automated AIR, and how you
    might phase adoption.
  answer: Fully automated AIR remediates threats fastest with no analyst wait, which is ideal for high-confidence,
    well-understood detections, but it carries more risk of acting on a false positive. Semi-automated
    AIR keeps a human approval gate, giving more control at the cost of speed and analyst time. A sensible
    phased approach is to start semi-automated, review the Action center to build trust in the verdicts,
    and then raise the automation level for device groups and detection types where the automation has
    proven reliable.
resources:
- label: Microsoft Defender XDR overview
  url: https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender
- label: Automated investigation and response in Microsoft Defender XDR
  url: https://learn.microsoft.com/en-us/defender-xdr/m365d-autoir
- label: The Action center
  url: https://learn.microsoft.com/en-us/defender-xdr/m365d-action-center
- label: Automatic attack disruption in Microsoft Defender XDR
  url: https://learn.microsoft.com/en-us/defender-xdr/automatic-attack-disruption
---

## One console for the whole attack

Until now we have lived on a single endpoint. **Microsoft Defender XDR** (security.microsoft.com) is the unified console that brings every signal together: **Defender for Endpoint** (devices), **Defender for Identity** (on-prem AD/identity), **Defender for Office 365** (email and collaboration), and **Defender for Cloud Apps** (SaaS). Instead of four tools and four queues, your SOC works one portal where alerts, the device/user/mailbox inventory, automated investigation, advanced hunting, and the Action center all live side by side.

## Incidents correlate the story

The core unit of work in XDR is the **incident**, not the alert. XDR's correlation engine groups related alerts and the entities they touch — a phishing email, the user who clicked, the device that ran the payload, the SaaS app the attacker reached — into a single incident with a coherent **attack story** and timeline. Open *Incidents & alerts > Incidents* and you will see scope, affected assets, an attack graph, and the MITRE ATT&CK techniques observed. This is what turns dozens of disconnected signals into one investigable case.

## Automated Investigation and Remediation (AIR)

When certain alerts fire, XDR can launch an **automated investigation** that mimics what a skilled analyst would do: walk the process tree, inspect files, query related devices and accounts, detonate suspicious artifacts, and reach a **verdict** (malicious / suspicious / clean). Based on that verdict it proposes or performs **remediation actions** — quarantine a file, stop a process, isolate a device, disable or force-sign-out a user, soft-delete a malicious email across all mailboxes. Investigations and their evidence are visible under each incident's *Investigations* tab.

## Automation levels

How far AIR goes on its own is governed by the **automation level**, set per device group in *Settings > Endpoints > Device groups*:

- **Full - remediate threats automatically** — actions are applied without waiting; fastest, best for high-confidence detections.
- **Semi - require approval for any/core/non-temp folders** — investigation runs automatically but remediation waits in the Action center for a human.
- **No automated response** — investigation only, nothing acted on (rare; reduces protection).

A common maturity path: start **semi-automated**, build trust by reviewing outcomes, then raise groups to **full** where automation has proven reliable.

## The Action center

The **Action center** (*Incidents & alerts > Action center*) is the single pane for everything automation did or wants to do, across the whole XDR suite. It has two tabs:

- **Pending** — actions waiting on approval (under semi-automated levels). Approve, reject, or approve in bulk.
- **History** — completed actions, who/what took them, and an **Undo** option for reversible actions like device isolation or app restriction.

You can also enable **auto-approval** for specific action types so trusted remediations flow without a click. The Action center is your audit trail and your control surface in one place.

## A first taste of advanced hunting

**Advanced hunting** lets you query the raw XDR data with **KQL** across a rich schema — `DeviceEvents`, `DeviceProcessEvents`, `EmailEvents`, `IdentityLogonEvents`, `AlertEvidence`, and more. We go deep on KQL in Module 4; for now, know that you can pivot from an incident straight into hunting to confirm scope. A simple example:

```kusto
// Recent process creations referencing a suspicious binary
DeviceProcessEvents
| where Timestamp > ago(24h)
| where FileName in~ ("powershell.exe", "cmd.exe")
| where ProcessCommandLine has_any ("Invoke-WebRequest", "DownloadString", "-enc")
| project Timestamp, DeviceName, AccountName, FileName, ProcessCommandLine
| order by Timestamp desc
```

Run it from *Hunting > Advanced hunting*; results can be turned into custom detection rules later.

## Attack disruption and the payoff

At the top of the stack, **automatic attack disruption** acts on very high-confidence, XDR-correlated signals (for example a confirmed human-operated ransomware or business-email-compromise pattern) to **contain an attack in progress** — suspending the compromised user in Entra ID and isolating involved devices — within minutes, before an analyst even opens the incident. Together, incident correlation, AIR, the Action center, and attack disruption collapse what used to be hours of manual triage into automated minutes: analysts review verdicts instead of assembling them, false-positive noise is auto-resolved, and the team's scarce attention goes to the genuinely hard cases. That is the modern SOC operating model you will automate further in Modules 4 and 5.
