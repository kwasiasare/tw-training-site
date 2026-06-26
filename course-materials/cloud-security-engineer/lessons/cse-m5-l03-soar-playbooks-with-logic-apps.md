---
course: cloud-security-engineer
title: SOAR Playbooks with Logic Apps
month: 5
monthTitle: Security Automation with PowerShell, Graph API & Logic Apps
lesson: 3
summary: Security Orchestration, Automation and Response (SOAR) is how a SOC responds at machine speed.
  In Microsoft Sentinel a playbook is an Azure Logic App triggered by the Microsoft Sentinel connector
  when an incident or alert fires. This lesson shows how automation rules bind analytic rules to playbooks,
  how to perform real response actions like disabling a compromised user, revoking sessions, and isolating
  a device, and how to add a human-in-the-loop approval. You will give the playbook a managed identity
  with least-privilege roles and walk through the account-disable playbook that underpins Capstone 3.
objectives:
- Explain SOAR and how Sentinel playbooks map to Azure Logic Apps
- Use the Microsoft Sentinel incident/alert trigger and read entities from the incident
- Bind analytic rules to playbooks with automation rules
- 'Implement response actions: disable/confirm-compromised a user, revoke sessions, isolate a device'
- Add a human-in-the-loop approval step versus fully automated response
- Assign the playbook a managed identity with least-privilege roles instead of stored credentials
video: cse-m5-l03-soar-playbooks-with-logic-apps.mp4
quiz:
- q: In Microsoft Sentinel, what technology actually implements a playbook?
  options:
  - A PowerShell runbook in Azure Automation
  - An Azure Logic App
  - A Power Automate desktop flow
  - A Kusto (KQL) saved function
  answer: 1
  why: A Sentinel playbook is an Azure Logic App built on the Microsoft Sentinel connector. The Logic
    App's trigger fires on a Sentinel incident or alert and its actions carry out the response, which
    is why playbook authoring is really Logic Apps workflow design.
- q: What is the role of an automation rule in Sentinel?
  options:
  - It writes the KQL detection logic for an analytic rule
  - It binds analytic rules (or incident conditions) to one or more playbooks and can set status/owner
  - It stores the playbook's credentials
  - It replaces the need for the Microsoft Sentinel connector
  answer: 1
  why: 'An automation rule is the glue: it watches for incidents (optionally filtered by analytic rule,
    severity, or tactics) and triggers playbooks, and can also change status, assign an owner, or add
    tags. The analytic rule detects; the automation rule routes the response.'
- q: Which trigger should a playbook use so it receives the full incident with all its entities?
  options:
  - The recurrence (schedule) trigger
  - The 'When a HTTP request is received' trigger
  - The Microsoft Sentinel 'When an incident is created/updated' (incident) trigger
  - The Microsoft Sentinel alert trigger only
  answer: 2
  why: The Microsoft Sentinel incident trigger passes the whole incident including grouped alerts and
    entities (accounts, IPs, hosts), so the playbook can act on every entity. The alert trigger fires
    per alert and is used for alert-level automation rather than incident-level orchestration.
- q: What is the recommended identity for a playbook to call Microsoft Graph or Defender APIs?
  options:
  - A stored client secret in the Logic App parameters
  - The personal account of the SOC analyst who created it
  - A managed identity on the Logic App granted least-privilege roles/app permissions
  - Anonymous access with no identity
  answer: 2
  why: A managed identity removes stored secrets entirely; you enable it on the Logic App and grant it
    only the specific Graph application permissions or Azure roles the playbook needs (for example User.ReadWrite.All
    to disable an account). This is the least-privilege, secret-free pattern.
- q: Why add a human-in-the-loop approval (for example a Teams adaptive card or email approval) before
    disabling an account?
  options:
  - Because Logic Apps cannot disable accounts automatically
  - To prevent a false-positive detection from locking out a legitimate user without oversight
  - Because Graph requires a second administrator for every write
  - To make the playbook run faster
  answer: 1
  why: 'Fully automated containment is fast but risky: a false positive could disable a CEO mid-presentation.
    A human-in-the-loop approval gate lets an analyst confirm before a disruptive action runs, trading
    a few minutes of latency for safety. High-confidence detections may skip the gate; ambiguous ones
    should not.'
- q: In two to four sentences, walk through the trigger-to-actions flow of a playbook that disables a
    compromised user account, and name the specific response actions involved.
  answer: The playbook is triggered by the Microsoft Sentinel incident trigger when an analytic rule (for
    example impossible-travel or a confirmed risky sign-in) creates an incident, and an automation rule
    routes that incident to the playbook. The playbook parses the Account entity to get the user's object
    ID or UPN, optionally posts a Teams adaptive card or email for analyst approval, and on approval calls
    Microsoft Graph to set accountEnabled to false (disable the account) and to revoke the user's refresh
    tokens via revokeSignInSessions so existing sessions are killed. It can also confirm the user as compromised
    in Entra ID Protection and isolate any associated device through the Microsoft Defender for Endpoint
    action, then comment back on the incident and set its status to closed or active. The playbook authenticates
    with its managed identity holding least-privilege permissions such as User.ReadWrite.All.
  why: The flow is trigger (Sentinel incident) to entity extraction (Account) to optional approval to
    containment actions (disable account, revoke sessions, confirm compromised, isolate device) to incident
    update, all under a least-privilege managed identity. This is the core SOAR containment pattern and
    the basis of Capstone 3.
resources:
- label: Automate threat response with playbooks in Microsoft Sentinel
  url: https://learn.microsoft.com/en-us/azure/sentinel/automation/automate-responses-with-playbooks
- label: Create and use Microsoft Sentinel automation rules
  url: https://learn.microsoft.com/en-us/azure/sentinel/create-manage-use-automation-rules
- label: Authenticate playbooks to Microsoft Sentinel (managed identity)
  url: https://learn.microsoft.com/en-us/azure/sentinel/authenticate-playbooks-to-sentinel
- label: 'Microsoft Graph user: revokeSignInSessions'
  url: https://learn.microsoft.com/en-us/graph/api/user-revokesigninsessions
---

## What SOAR Is and Why It Matters

A SOC analyst who manually disables a compromised account is racing the attacker, and losing. **SOAR**, Security Orchestration, Automation and Response, lets the platform respond at machine speed: detect, decide, contain, all in seconds. In Microsoft Sentinel the response unit is a **playbook**, and a playbook is nothing more than an **Azure Logic App** built on the **Microsoft Sentinel connector**. If you can design a Logic App workflow, you can build a SOAR playbook.

The value is consistency and speed. The same containment steps run identically every time, day or night, with a full audit trail, instead of depending on which analyst is on shift.

## The Sentinel Trigger

A playbook starts with a **trigger**. For incident-level orchestration use the Microsoft Sentinel **"When an incident is created or updated"** trigger. It hands the playbook the whole incident, including the grouped alerts and, crucially, the **entities**, accounts, IP addresses, hosts, URLs, that the response will act on.

```
Trigger: Microsoft Sentinel incident
  -> incident.properties.title, severity, status
  -> incident.properties.relatedEntities[] (Account, Ip, Host ...)
```

There is also an **alert trigger** that fires per alert; use it for alert-scoped automation. For full containment of a multi-alert incident, the incident trigger is the right choice because it exposes every entity at once.

## Automation Rules: Binding Detections to Playbooks

An analytic rule **detects**; it does not run a playbook by itself. The glue is an **automation rule**. It watches incidents, optionally filtered by analytic rule name, severity, or MITRE tactic, and triggers one or more playbooks. It can also set status, assign an owner, and add tags.

```
Automation rule: "Contain confirmed account compromise"
  Trigger:   When incident is created
  Conditions: Analytic rule name contains 'Risky sign-in'
              AND Severity = High
  Actions:   Run playbook 'PB-Disable-CompromisedUser'
             Change status -> Active, assign owner -> SOC Tier 2
```

This separation is deliberate: detection logic (KQL) and response routing (automation rules) evolve independently, so you can re-point a detection at a different playbook without touching the query.

## Common Response Actions

Once triggered, a playbook orchestrates **actions**, each typically a Graph or Defender API call. The most common containment actions:

- **Disable a user** in Entra ID: set `accountEnabled = false`.
- **Revoke sign-in sessions**: invalidate refresh tokens so existing sessions die (`revokeSignInSessions`).
- **Confirm compromised**: mark the user compromised in Entra ID Protection so risk-based policies engage.
- **Isolate a device** via Microsoft Defender for Endpoint.
- **Add an entity to a watchlist** for ongoing correlation.
- **Notify / request approval** via Teams or email.

The Graph calls behind the two most important user actions:

```http
# Disable the account
PATCH https://graph.microsoft.com/v1.0/users/{userId}
Content-Type: application/json

{ "accountEnabled": false }

# Kill all existing sessions (revoke refresh tokens)
POST https://graph.microsoft.com/v1.0/users/{userId}/revokeSignInSessions
```

In a Logic App these are the **Microsoft Graph** HTTP actions (or the built-in Entra/Defender connector actions); the `{userId}` comes from the Account entity in the trigger.

## Reading Entities with Inline Expressions

The playbook must pull the target user out of the incident. Sentinel exposes an **Entities - Get Accounts** action, and you reference fields with Logic App **inline expressions** (the workflow definition language). For example, to grab the first account's AAD object ID:

```
@{triggerBody()?['object']?['properties']?['relatedEntities'][0]?['properties']?['aadUserId']}
```

Inside a "For each" loop over accounts you would instead use `@{items('For_each_account')?['properties']?['aadUserId']}`. These expressions are how data flows from the trigger into each action's parameters.

## Human-in-the-Loop vs Fully Automated

Speed is good; an automated mistake is not. Disabling an account on a **false positive** could lock out a CEO mid-board-meeting. The mitigation is a **human-in-the-loop** approval gate: before the disruptive action, post a **Teams adaptive card** or send an **email with approval options** and branch on the response.

```
Action: Post adaptive card and wait for a response (Teams)
  -> Buttons: [Approve disable]  [Reject]
Condition: if outcome == 'Approve disable'
  then  -> PATCH accountEnabled=false + revokeSignInSessions
  else  -> add comment 'Analyst rejected auto-containment', close as benign
```

The design rule: **high-confidence, low-blast-radius** detections (a confirmed-compromised risky user) can be fully automated; **ambiguous or high-impact** actions should pass through approval. Many SOCs run a tiered model, auto-contain commodity threats, gate anything touching a VIP or privileged account.

## Least-Privilege Identity for the Playbook

Never store a client secret in a Logic App. Enable a **managed identity** on the playbook and grant it only what it needs. To disable users and revoke sessions the identity needs the Graph **User.ReadWrite.All** application permission; to comment on incidents it needs the **Microsoft Sentinel Responder** (or Contributor) role on the workspace; to isolate devices it needs the appropriate Defender permission.

```powershell
# Grant the playbook's managed identity the Graph app role it needs (one-time)
$miSpId  = (Get-MgServicePrincipal -Filter "displayName eq 'PB-Disable-CompromisedUser'").Id
$graphSp = Get-MgServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"
$role    = $graphSp.AppRoles | Where-Object { $_.Value -eq 'User.ReadWrite.All' }

New-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $miSpId `
    -PrincipalId $miSpId -ResourceId $graphSp.Id -AppRoleId $role.Id
```

## Walkthrough: The Disable-Compromised-Account Playbook (Capstone 3)

Putting it together, here is the end-to-end flow that Capstone 3 asks you to build:

1. **Trigger** - Microsoft Sentinel incident trigger fires on a high-severity 'Risky sign-in' incident, routed by an **automation rule**.
2. **Extract entity** - Entities - Get Accounts; read `aadUserId` via inline expression.
3. **Approval (optional gate)** - post a Teams adaptive card to the SOC channel; wait for Approve/Reject.
4. **Contain** - on approval: Graph `PATCH accountEnabled=false`, then `POST revokeSignInSessions`; optionally confirm the user compromised in Entra ID Protection and isolate the device in Defender.
5. **Close the loop** - add a comment to the incident summarizing actions taken and set status to Active or Closed.
6. **Identity** - every API call runs under the playbook's **managed identity** holding only User.ReadWrite.All and the Sentinel Responder role.

The result: from detection to a disabled, session-revoked account in well under a minute, with an approval trail and no stored credentials. That is SOAR.
