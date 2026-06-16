---
course: helpdesk-tier3-advanced
title: 'Lab: automate a real Tier 3 workflow end to end'
month: 2
monthTitle: 'Automation: PowerShell & Microsoft Graph at Scale'
lesson: 8
summary: 'Bring the whole month together: design and build an end-to-end automation that detects a real
  Tier 3 issue, remediates it, reports it, and runs unattended on a schedule.'
objectives:
- Decompose a real Tier 3 workflow into detect, decide, act, and report stages
- Combine the module, Graph calls, remediation logic, and a runbook into one solution
- Make every action safe with ShouldProcess, retry, and idempotency
- Produce a machine-readable report and a human-readable summary
- Authenticate the unattended path with a managed identity and least privilege
- Define success criteria and a rollback plan for the automation
video: ht2-l08-lab-automate-a-tier3-workflow.mp4
quiz:
- q: What is the right first step when automating a Tier 3 workflow end to end?
  options:
  - 'Decompose the workflow into clear stages: detect, decide, act, report'
  - Write the remediation first and test in production
  - Grant the broadest permissions to avoid errors
  - Skip dry runs to save time
  answer: 0
  why: Breaking the workflow into detect, decide, act, and report stages lets you build and test each
    piece, add safety at the act stage, and reason about failure before touching the fleet.
- q: Why run the act stage behind ShouldProcess with a pilot ring before fleet-wide rollout?
  options:
  - It is faster
  - Graph requires a pilot
  - It removes the need for logging
  - A dry run and small pilot prove the logic and limit blast radius before scaling
  answer: 3
  why: Previewing with -WhatIf and piloting on a small group catches mistakes while the impact is tiny,
    which is essential for high blast-radius endpoint automation.
- q: In the end-to-end design, what authenticates the scheduled, unattended run?
  options:
  - A password in the runbook
  - The Automation account's managed identity with least-privilege application permissions
  - An interactive login each night
  - A shared service desk account
  answer: 1
  why: Unattended runs use the managed identity granted only the Graph application permissions the workflow
    needs, removing stored secrets and limiting scope.
- q: Why produce both a machine-readable report (JSON/CSV) and a human-readable summary?
  options:
  - To use more storage
  - JSON is required by Intune
  - The machine format feeds dashboards and tickets while the summary lets a human triage at a glance
  - Humans cannot read JSON at all
  answer: 2
  why: Structured output integrates with downstream systems, and a concise summary makes the run immediately
    understandable to an on-call engineer, serving two different consumers.
- q: Name two safety mechanisms from this month that your end-to-end automation should include.
  answer: 'Any two of: ShouldProcess/-WhatIf dry runs, idempotent actions, try/catch error handling, retry
    with exponential backoff and Retry-After handling, least-privilege scopes, and a pilot ring before
    fleet rollout.'
  why: Production endpoint automation must be previewable, idempotent, resilient to throttling/transient
    errors, least-privilege, and rolled out gradually — these were the recurring themes of the month.
- q: In one sentence, what should your rollback plan cover for an automation that changes device or group
    state?
  answer: It should define how to stop the schedule, reverse the change (for example remove added group
    members or restore the prior policy), and confirm devices returned to the known-good baseline you
    exported beforehand.
  why: Because changes have blast radius, a tested rollback — disable schedule, reverse the action, verify
    against the exported baseline — turns a bad run from an incident into a non-event.
resources:
- label: Microsoft Learn — Manage runbooks in Azure Automation
  url: https://learn.microsoft.com/en-us/azure/automation/manage-runbooks
- label: Microsoft Learn — Remediations in Intune
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations
- label: Microsoft Learn — Microsoft Graph PowerShell SDK overview
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/overview
- label: Microsoft Learn — Microsoft Graph throttling guidance
  url: https://learn.microsoft.com/en-us/graph/throttling
---

## The brief

You will build one automation that solves a real Tier 3 problem end to end: **find every Windows device that has not synced with Intune in 30 days, tag it into a remediation group, attempt a sync, and produce a report** — running unattended on a schedule. This lab ties together every skill from Month 2: the module, Graph, remediation thinking, safety, and runbooks.

Start by decomposing the workflow into four stages: **detect → decide → act → report**. Build and test each stage on its own before wiring them together.

## Stage 1 and 2 — detect and decide

Detection is read-only. Pull the fleet with `-All`, filter server-side, and apply your rule. The *decide* stage is just the predicate that separates healthy from unhealthy.

```powershell
Connect-MgGraph -Scopes 'DeviceManagementManagedDevices.ReadWrite.All','Group.ReadWrite.All'

function Get-StaleWindowsDevice {
    [CmdletBinding()]
    param([int]$StaleDays = 30)
    $cutoff = (Get-Date).AddDays(-$StaleDays)
    Get-MgDeviceManagementManagedDevice -All `
        -Filter "operatingSystem eq 'Windows'" |
        Where-Object { $_.LastSyncDateTime -lt $cutoff }
}
```

## Stage 3 — act, safely

Every action goes behind `ShouldProcess`, uses the retry helper from Lesson 6, and is **idempotent**. Add to the group, then trigger a sync; re-running must not create duplicates or errors.

```powershell
function Invoke-StaleDeviceRemediation {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory)][object[]]$Devices,
        [Parameter(Mandatory)][string]$RemediationGroupId
    )
    $results = foreach ($d in $Devices) {
        if ($PSCmdlet.ShouldProcess($d.DeviceName, 'Tag + sync stale device')) {
            try {
                Invoke-WithRetry {
                    New-MgGroupMember -GroupId $RemediationGroupId -DirectoryObjectId $d.AzureAdDeviceId -ErrorAction Stop
                    Sync-MgDeviceManagementManagedDevice -ManagedDeviceId $d.Id -ErrorAction Stop
                }
                [pscustomobject]@{ Device = $d.DeviceName; Action = 'Remediated'; Error = $null }
            }
            catch {
                [pscustomobject]@{ Device = $d.DeviceName; Action = 'Failed'; Error = $_.Exception.Message }
            }
        }
    }
    $results
}
```

## Stage 4 — report for two audiences

Produce a **machine-readable** artefact (JSON/CSV) for dashboards and tickets, and a **human-readable** one-line summary for the on-call engineer.

```powershell
$report = Invoke-StaleDeviceRemediation -Devices $stale -RemediationGroupId $groupId
$report | ConvertTo-Json -Depth 5 | Set-Content '.\stale-report.json' -Encoding UTF8

$ok  = ($report | Where-Object Action -eq 'Remediated').Count
$bad = ($report | Where-Object Action -eq 'Failed').Count
Write-Output "Stale-device run: $ok remediated, $bad failed, $($report.Count) total"
```

## Make it unattended

Wrap the whole flow in a runbook that authenticates with `Connect-MgGraph -Identity`, grant that managed identity only `DeviceManagementManagedDevices.ReadWrite.All` and `Group.ReadWrite.All` as **application** permissions, pin module versions, and attach a daily schedule. Pilot on a small ring with `-WhatIf` first.

## Your task

Deliver the complete solution as a single, reviewable package:

1. A **detect** function (`Get-StaleWindowsDevice`) and a **decide** rule, read-only.
2. An **act** function (`Invoke-StaleDeviceRemediation`) that uses `SupportsShouldProcess`, the `Invoke-WithRetry` helper, idempotent group-add + sync, and per-device result objects.
3. A **report** stage emitting both JSON and a one-line summary.
4. A **runbook** wrapper using managed-identity auth, pinned modules, and a schedule.
5. A short written **runbook of operations**: the exact least-privilege permissions, how you piloted with `-WhatIf`, your success criteria, and a tested **rollback plan** (disable schedule, remove added members, restore baseline). Prove a second run is idempotent — it should remediate nothing already healthy.
