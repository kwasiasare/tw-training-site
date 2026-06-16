---
course: helpdesk-tier3-advanced
title: Configuration as code for endpoints
month: 2
monthTitle: 'Automation: PowerShell & Microsoft Graph at Scale'
lesson: 5
summary: 'Treat endpoint configuration as versioned, reviewable code: define policies as JSON, store them
  in Git, and deploy them to Intune through Graph with idempotent import scripts.'
objectives:
- Explain why endpoint configuration should be declarative, versioned code
- Export an existing Intune policy as JSON via Graph
- Store policy definitions in Git and review changes through pull requests
- Write an idempotent import that creates or updates a policy by name
- Separate environment-specific values from policy templates
- Understand the IntuneCM / community tooling landscape for config as code
video: ht2-l05-configuration-as-code.mp4
quiz:
- q: What is the core principle of configuration as code for endpoints?
  options:
  - Click through the portal faster
  - Store passwords in scripts
  - Avoid using Git
  - Define configuration declaratively in versioned files and deploy it through automation
  answer: 3
  why: Config as code means the desired state lives in declarative, version-controlled files that are
    deployed by automation, giving you review, history, rollback, and repeatability.
- q: Why export Intune policies to JSON and keep them in Git?
  options:
  - JSON runs faster than the portal
  - You get change history, peer review via pull requests, and reliable rollback
  - Git encrypts the policies automatically
  - Graph requires it
  answer: 1
  why: Versioning policy JSON in Git gives you a diffable audit trail, code review through pull requests,
    and the ability to roll back to a known-good state.
- q: What makes an import script idempotent when applying a policy?
  options:
  - It checks whether a policy of that name exists and updates it, otherwise creates it
  - It always creates a new policy each run
  - It deletes everything first
  - It only runs once per tenant
  answer: 0
  why: 'An idempotent import is safe to re-run: it looks up the policy by a stable key (like displayName),
    updating if present and creating if absent, so repeated runs converge on the same state.'
- q: How should environment-specific values (tenant, group ids) be handled in config as code?
  options:
  - Hard-code them in each policy file
  - Email them to yourself
  - Keep them in separate parameter/variable files and inject at deploy time
  - Store them inside the policy displayName
  answer: 2
  why: Separating environment values from policy templates lets the same template deploy to dev and prod
    by swapping a parameter file, avoiding copy-paste drift.
- q: Name one Graph endpoint family you would call to manage Intune device configuration profiles as code.
  answer: deviceManagement/deviceConfigurations (or the settings-catalog configurationPolicies and deviceCompliancePolicies
    endpoints) under https://graph.microsoft.com.
  why: These endpoints expose Intune configuration and compliance policies as resources you can GET to
    export and POST/PATCH to import, which is what config-as-code tooling drives.
- q: In one sentence, why is a pull request review valuable for an Intune policy change?
  answer: A reviewer can see the exact JSON diff before it reaches devices, catching mistakes like an
    over-broad assignment or a wrong setting before they affect the fleet.
  why: Policy changes are high blast-radius; reviewing the diff in a pull request applies the same safety
    net to configuration that teams already apply to code.
resources:
- label: Microsoft Learn — deviceConfiguration resource type (Graph)
  url: https://learn.microsoft.com/en-us/graph/api/resources/intune-deviceconfig-deviceconfiguration
- label: Microsoft Learn — Intune configuration profiles overview
  url: https://learn.microsoft.com/en-us/mem/intune/configuration/device-profiles
- label: Microsoft Learn — Settings catalog configurationPolicies (Graph)
  url: https://learn.microsoft.com/en-us/graph/api/resources/intune-deviceconfigv2-devicemanagementconfigurationpolicy
- label: Microsoft Learn — Microsoft Graph PowerShell SDK overview
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/overview
---

## Why configuration should be code

Clicking through the Intune portal works for one device, once. It does not scale, it leaves no history, and a wrong click can hit thousands of endpoints. **Configuration as code** treats your **desired state** as declarative files — JSON policy definitions — kept in **Git** and deployed by automation. You gain a diffable **audit trail**, **peer review** through pull requests, and **rollback** to any prior commit.

The mental model: the repo is the source of truth, and Intune is just the runtime that the repo deploys to.

## Export what you already have

Start by capturing your current state. Graph exposes configuration profiles as resources you can `GET` and serialise to JSON.

```powershell
Connect-MgGraph -Scopes 'DeviceManagementConfiguration.Read.All'

$policies = Invoke-MgGraphRequest -Method GET `
    -Uri 'https://graph.microsoft.com/beta/deviceManagement/configurationPolicies' |
    Select-Object -ExpandProperty value

foreach ($p in $policies) {
    $safe = $p.name -replace '[^\w\-]', '_'
    $p | ConvertTo-Json -Depth 20 | Set-Content ".\policies\$safe.json" -Encoding UTF8
}
```

Commit that `policies` folder to Git. You now have a baseline you can diff against forever.

## Idempotent import: create or update by name

The heart of config as code is an import that is **safe to re-run**. It looks the policy up by a stable key — usually `displayName` or `name` — then **updates** it if it exists and **creates** it if it does not.

```powershell
function Import-IntunePolicy {
    [CmdletBinding(SupportsShouldProcess)]
    param([Parameter(Mandatory)][string]$Path)

    $def  = Get-Content $Path -Raw | ConvertFrom-Json
    $base = 'https://graph.microsoft.com/beta/deviceManagement/configurationPolicies'

    $existing = (Invoke-MgGraphRequest -Method GET `
        -Uri "$base?`$filter=name eq '$($def.name)'").value

    if ($existing) {
        if ($PSCmdlet.ShouldProcess($def.name, 'Update policy')) {
            Invoke-MgGraphRequest -Method PATCH `
                -Uri "$base/$($existing[0].id)" -Body ($def | ConvertTo-Json -Depth 20)
        }
    }
    else {
        if ($PSCmdlet.ShouldProcess($def.name, 'Create policy')) {
            Invoke-MgGraphRequest -Method POST `
                -Uri $base -Body ($def | ConvertTo-Json -Depth 20)
        }
    }
}
```

Run it twice; the second run changes nothing. That is the property you want.

## Separate templates from environment values

Never hard-code tenant or group ids inside a policy template. Keep them in a **parameter file** per environment and inject at deploy time, so the *same* template promotes from **dev** to **prod** by swapping one file.

```powershell
$env = Get-Content '.\envs\prod.json' -Raw | ConvertFrom-Json
$template = (Get-Content '.\templates\baseline.json' -Raw) `
    -replace '{{TargetGroupId}}', $env.TargetGroupId
```

## The tooling landscape

You can write your own importer, or stand on community tooling. Projects like the **IntuneCM** family and Microsoft's own samples wrap this export/import/assign loop with backup and reporting. Whatever you use, the principles are identical: declarative files, Git review, idempotent deploy.

## Your task

Build a minimal config-as-code pipeline by hand. Export at least two Intune **configurationPolicies** to JSON and commit them. Write an idempotent `Import-IntunePolicy` function (create-or-update by name, with `SupportsShouldProcess`). Move one environment-specific value — a target group id — out of the template into a per-environment JSON file and inject it at deploy time. Demonstrate a re-run that reports *no changes* the second time, and capture the `-WhatIf` output as proof of a safe dry run.
