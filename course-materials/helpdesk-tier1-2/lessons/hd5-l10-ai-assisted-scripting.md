---
course: helpdesk-tier1-2
title: AI-assisted scripting and automation
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 10
summary: Use AI to generate, explain, and refine PowerShell for endpoint tasks such as Microsoft Graph
  queries and Intune remediation scripts, then apply a strict verification workflow so you never run untested
  AI code in production.
objectives:
- Use AI to generate and explain PowerShell for endpoint tasks like Graph queries and bulk operations
- Write effective prompts that state the goal, environment, modules, constraints, and error handling
- Generate Intune remediation script pairs (detection + remediation) with AI as a starting point
- Always request -WhatIf, confirmation prompts, and safe defaults for any destructive operation
- 'Verify AI-generated scripts: read every line, check cmdlet and parameter names, and confirm Graph scopes'
- 'Apply safe practice: test on a pilot device, keep secrets out of prompts, and version-control and peer-review
  scripts'
video: hd5-l10-ai-assisted-scripting.mp4
quiz:
- q: What is the single most important rule before running an AI-generated PowerShell script against production?
  options:
  - Run it on every device at once to save time
  - Read every line, understand it, and test it on a pilot device first
  - Trust it because AI wrote it
  - Delete the comments to make it shorter
  answer: 1
  why: AI can hallucinate cmdlets, misuse parameters, or include destructive logic. You must read and
    understand every line and test on a single pilot device or group before any broad run.
- q: Which PowerShell SDK does AI commonly target for managing Intune and Entra objects programmatically?
  options:
  - The Microsoft Graph PowerShell SDK
  - The DOS batch toolkit
  - The VBScript engine
  - The Linux bash kernel
  answer: 0
  why: The Microsoft Graph PowerShell SDK is the standard way to query and manage Intune, devices, and
    Entra ID objects from PowerShell, so AI usually generates Graph SDK code for these tasks.
- q: An AI-generated script includes Remove-MgDeviceManagementManagedDevice with no confirmation. What
    should you add?
  options:
  - Nothing, run it immediately
  - More devices to the list
  - -WhatIf and/or a confirmation prompt before testing on one pilot device
  - A second copy of the line
  answer: 2
  why: Destructive cmdlets must be run with -WhatIf first and guarded by confirmation, then validated
    on a single pilot device, so you never bulk-delete by accident.
- q: Why must you check the Microsoft Graph permission scopes an AI-generated script requests?
  options:
  - Scopes change the font color
  - Scopes determine what the script is allowed to do; over-broad or wrong scopes are a security and reliability
    risk
  - Scopes are decorative
  - Scopes speed up the network
  answer: 1
  why: Graph scopes control authorization. The script may request scopes that are too broad (a security
    risk) or the wrong scopes (it will fail), so you verify them against least-privilege needs.
- q: Name two things you must NOT include in a prompt when asking an AI to generate a script.
  answer: Secrets such as client secrets or passwords, and real user or customer PII or tenant identifiers.
  why: Public LLMs may log or train on input, so credentials and PII must never be pasted into a prompt;
    use placeholders instead.
- q: In one sentence, give a good prompt pattern for generating a PowerShell script with AI.
  answer: State the goal, the environment and modules, the constraints and error handling, and require
    -WhatIf and comments explaining each step.
  why: A precise prompt that specifies goal, environment, constraints, safety, and explanation produces
    safer, more accurate, and reviewable code.
resources:
- label: Microsoft — PowerShell documentation
  url: https://learn.microsoft.com/en-us/powershell/
- label: Microsoft — Get started with the Microsoft Graph PowerShell SDK
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/get-started
- label: Microsoft — Intune remediations (detection + remediation scripts)
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations
- label: 'Microsoft — Exam MD-102: Microsoft 365 Endpoint Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
---

## Why AI is great at PowerShell (and where it bites)

PowerShell is the automation language of endpoint management, and AI is a genuinely strong pair-programmer for it. It can draft a **Microsoft Graph PowerShell SDK** query, scaffold a bulk device operation, write an Intune **remediation script pair**, or explain a script you inherited line by line. The catch: AI also **hallucinates cmdlet and parameter names**, invents Graph scopes, and will happily write destructive code with a straight face. Treated as a fast first draft you fully verify, it is a superpower. Treated as an oracle, it is a production incident waiting to happen.

## Prompt patterns that produce good scripts

Vague prompts produce vague, risky code. State the **goal**, the **environment and modules**, the **constraints**, and the **error handling** you expect.

```text
Write a PowerShell script using the Microsoft Graph PowerShell SDK
to list all Intune-managed Windows devices that haven't checked in
for 30+ days. Requirements: use Connect-MgGraph with least-privilege
scopes, add error handling, include -WhatIf-safe read-only calls,
comment every step, and tell me exactly which Graph scopes are
needed. Do not include any secrets; use placeholders.
```

Asking it to *name the required scopes* and *comment every step* turns the output into something you can actually review.

## A sample generated snippet

Here is the kind of read-only output you might get — and must still read carefully:

```powershell
# Requires: Microsoft.Graph module
# Scopes needed: DeviceManagementManagedDevices.Read.All
Connect-MgGraph -Scopes "DeviceManagementManagedDevices.Read.All"

$cutoff = (Get-Date).AddDays(-30)
Get-MgDeviceManagementManagedDevice -All |
  Where-Object { $_.LastSyncDateTime -lt $cutoff } |
  Select-Object DeviceName, UserPrincipalName, LastSyncDateTime |
  Sort-Object LastSyncDateTime
```

Before trusting it: does `Get-MgDeviceManagementManagedDevice` actually exist with those parameters? Is the property name `LastSyncDateTime` correct? Check the docs — do not assume.

## Remediation script pairs

Intune **remediations** use a **detection** script (exit 1 if the issue is present) plus a **remediation** script (the fix). AI is great for scaffolding both, but a remediation runs on real machines, so safety matters double.

```text
Generate an Intune remediation pair in PowerShell: detection checks
if a registry value HKLM:\...\Foo equals 1; remediation sets it to 1.
Follow Intune exit-code conventions, add error handling, log to a
file, and make the remediation idempotent. Comment every line.
```

## Verify before you run — non-negotiable

This is the most important section of the lesson. **Never run AI-generated scripts in production untested.** The rules:

- **Read every line** and understand what it does. If you can't explain it, you can't run it.
- **Check cmdlet and parameter names** against official docs — AI invents plausible-looking ones.
- **Run `-WhatIf` first** and add confirmation prompts on any destructive cmdlet (`Remove-*`, `Set-*`, `Disable-*`).
- **Test on one pilot device or a tiny pilot group**, never the whole fleet.
- **Verify Graph permission scopes** — least privilege, not the broadest scope the AI grabbed.
- **Review for destructive operations** hidden in the middle of innocent-looking code.
- **Keep secrets and PII out of prompts** — use placeholders for tenant IDs, UPNs, and never paste client secrets.
- **Version-control and peer-review** every script before it goes near production.

## Your task

Use an AI assistant to generate one read-only Microsoft Graph PowerShell script (for example: list devices not checked in for 30 days). Then audit it: confirm every cmdlet and parameter exists in the official docs, identify the Graph scopes it needs, and write two sentences on anything the AI got wrong or that you had to change before you would run it.
