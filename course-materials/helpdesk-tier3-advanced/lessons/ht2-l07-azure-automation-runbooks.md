---
course: helpdesk-tier3-advanced
title: Scheduled automation and runbooks with Azure Automation
month: 2
monthTitle: 'Automation: PowerShell & Microsoft Graph at Scale'
lesson: 7
summary: 'Run your PowerShell unattended in the cloud with Azure Automation: runbooks, schedules, managed-identity
  authentication to Graph, and operational logging.'
objectives:
- Explain what Azure Automation runbooks are and when to use them over local scripts
- Authenticate a runbook to Graph using a managed identity instead of stored secrets
- Grant a managed identity the exact Graph application permissions it needs
- Import modules into the Automation account and pin versions
- Schedule a runbook and pass parameters at run time
- Capture output, errors, and verbose streams in job logs for operations
video: ht2-l07-azure-automation-runbooks.mp4
quiz:
- q: What is an Azure Automation runbook?
  options:
  - A local scheduled task on each device
  - A Graph permission scope
  - A PowerShell (or Python) script that runs unattended in the cloud on Azure's compute
  - A type of Intune policy
  answer: 2
  why: A runbook is a script hosted in an Azure Automation account that runs on managed cloud compute,
    on a schedule or trigger, with no local machine required.
- q: How should a runbook authenticate to Microsoft Graph in production?
  options:
  - A system-assigned managed identity granted the needed Graph app permissions
  - A username and password stored in the script
  - An interactive Connect-MgGraph prompt
  - A shared admin token pasted in a variable
  answer: 0
  why: A managed identity removes stored secrets entirely; Azure manages the credential, and you grant
    that identity the specific Graph application permissions it requires.
- q: Why pin module versions in the Automation account rather than always using latest?
  options:
  - Latest is never available
  - It makes runbooks run faster
  - Azure requires a fixed version
  - Pinning gives reproducible runs and prevents a new module version from silently breaking a runbook
  answer: 3
  why: Pinning the Microsoft.Graph module versions means a runbook behaves identically every run; an unexpected
    module update will not change behaviour or break a scheduled job overnight.
- q: When a runbook uses a managed identity, which Connect-MgGraph parameter do you use?
  options:
  - -Interactive
  - -Identity
  - -DeviceCode
  - -Credential
  answer: 1
  why: Connect-MgGraph -Identity authenticates using the Automation account's managed identity, with no
    secret stored or prompt shown.
- q: Name where you go to see what a runbook actually did, including errors and verbose output, after
    a scheduled run.
  answer: The job history / job logs for that runbook in the Automation account, which capture the Output,
    Error, Warning, and Verbose streams for each run.
  why: Unattended jobs have no console, so the per-job stream logs are your only window into success,
    failure, and diagnostics; design your runbook to write useful verbose/error output.
- q: In one sentence, why are application permissions (not delegated) usually right for an unattended
    runbook?
  answer: An unattended runbook has no signed-in user, so it needs application permissions granted to
    its identity with admin consent, scoped to only the operations it performs.
  why: Delegated permissions act on behalf of a signed-in user; a scheduled runbook runs as itself, so
    it uses application permissions consented by an admin and kept least-privilege.
resources:
- label: Microsoft Learn — Azure Automation overview
  url: https://learn.microsoft.com/en-us/azure/automation/overview
- label: Microsoft Learn — Manage runbooks in Azure Automation
  url: https://learn.microsoft.com/en-us/azure/automation/manage-runbooks
- label: Microsoft Learn — Use a managed identity for Azure Automation
  url: https://learn.microsoft.com/en-us/azure/automation/enable-managed-identity-for-automation
- label: Microsoft Learn — Use Microsoft Graph PowerShell with a managed identity
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/authentication-commands
---

## Why run automation in the cloud

A script that only works when *you* run it on *your* laptop is not automation — it is a chore with extra steps. **Azure Automation** hosts your PowerShell as **runbooks** that run unattended on Azure compute, on a **schedule** or trigger, with no machine to leave switched on and no one to remember to click run.

Use runbooks for anything recurring at fleet scale: nightly stale-device reports, scheduled group hygiene, off-hours remediation sweeps.

## Authenticate without secrets: managed identity

The worst thing you can do is paste a credential into a script. A **managed identity** is an Azure-managed credential attached to the Automation account; Azure rotates it and you never see it. The Graph SDK connects to it with one switch.

```powershell
# Inside the runbook — no secret, no prompt
Connect-MgGraph -Identity -NoWelcome

$context = Get-MgContext
Write-Output "Connected as $($context.AppName) in tenant $($context.TenantId)"
```

Because the runbook runs **as itself** with no signed-in user, it uses **application permissions**, not delegated ones.

## Grant the identity exactly what it needs

You grant the managed identity specific **Graph application permissions** (app roles) — and only those. This is least privilege at the identity level. The grant itself can be scripted.

```powershell
# Run once by an admin to grant the runbook's identity a Graph app role
$graphSp   = Get-MgServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"
$miSp      = Get-MgServicePrincipal -ServicePrincipalId $managedIdentityObjectId
$appRole   = $graphSp.AppRoles | Where-Object { $_.Value -eq 'DeviceManagementManagedDevices.Read.All' }

New-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $miSp.Id `
    -PrincipalId $miSp.Id -ResourceId $graphSp.Id -AppRoleId $appRole.Id
```

## Modules and version pinning

A runbook can only use modules **imported into the Automation account**. Import the Graph sub-modules you need and **pin their versions** so a surprise update never breaks a scheduled job at 2 a.m.

```powershell
# The runbook body declares what it expects; the account provides it
#Requires -Modules @{ ModuleName='Microsoft.Graph.Authentication'; ModuleVersion='2.0.0' }
#Requires -Modules @{ ModuleName='Microsoft.Graph.DeviceManagement'; ModuleVersion='2.0.0' }
```

Import modules via the portal, or programmatically with `New-AzAutomationModule`.

## Schedule, parameterise, and log

Attach a **schedule** (daily, weekly, or a recurring interval) and pass **parameters** at run time so one runbook serves many cases. Because there is no console, design for the **job log**: every `Write-Output`, `Write-Error`, and `Write-Verbose` is captured per job.

```powershell
param(
    [int]$StaleDays = 30,
    [string]$OutputContainerUrl
)
Connect-MgGraph -Identity -NoWelcome

$cutoff = (Get-Date).AddDays(-$StaleDays)
$stale  = Get-MgDeviceManagementManagedDevice -All |
    Where-Object { $_.LastSyncDateTime -lt $cutoff }

Write-Output "Found $($stale.Count) devices stale beyond $StaleDays days"
$stale | Select-Object DeviceName, LastSyncDateTime | ConvertTo-Json
```

Review the per-job streams in the Automation account's **job history** to confirm what ran and catch failures.

## Your task

Design (and where you have a sandbox, build) a runbook `Report-StaleDevices` that authenticates with `Connect-MgGraph -Identity`, accepts a `-StaleDays` parameter, lists every device stale beyond that window, and writes a JSON summary to `Write-Output`. List the **exact** Graph application permission its managed identity needs and why. Add `#Requires` lines pinning the Graph module versions, and attach a daily schedule. Describe where you would read the job log to verify the run and how you would alert on failure.
