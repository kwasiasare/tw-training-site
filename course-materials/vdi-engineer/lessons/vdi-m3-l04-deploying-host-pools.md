---
course: vdi-engineer
title: 'Deploying Host Pools: Portal, Bicep, Registration Tokens, and Session Host Update'
month: 3
monthTitle: 'Azure Virtual Desktop Infrastructure: Plan, Deploy & Scale'
lesson: 4
summary: This lesson turns the architecture, networking, and image decisions from earlier in the module
  into an actual deployed AVD environment. You'll walk the Azure portal deployment flow field by field,
  then deploy the same host pool, application group, and workspace as Bicep resources (with a note on
  the Terraform azurerm equivalent), issue and manage registration tokens with Az.DesktopVirtualization
  PowerShell cmdlets, wire in Azure Virtual Desktop Insights at deploy time, and understand exactly where
  the session host update (preview) feature stands today versus the classic scripted replace pattern.
objectives:
- Walk the Azure portal host pool creation flow and map each field to the architecture decisions from
  Lesson 1
- Author a minimal, correct Bicep deployment for a host pool, application group, and workspace
- Issue and retrieve AVD host pool registration tokens using Az.DesktopVirtualization PowerShell cmdlets
- Enable Azure Virtual Desktop Insights diagnostic settings as part of initial deployment rather than
  as an afterthought
- Explain the current (preview) state of the session host update feature and how it relates to the classic
  scripted replace pattern
quiz:
- q: In the Azure portal's host pool creation wizard, what does the 'Workspace' step actually accomplish?
  options:
  - It sets the Azure region the host pool deploys into
  - It associates the host pool's application group(s) with a workspace, which is what makes the published
    desktop or apps appear in a user's client feed
  - It configures the VNet and subnet for session hosts
  - It enables Azure Virtual Desktop Insights automatically
  answer: 1
  why: A host pool with session hosts and an application group but no workspace association publishes
    nothing a user can see — the workspace step in the wizard is what associates the application group
    to a workspace so it appears in the user's feed, exactly the object relationship covered in Lesson
    1.
- q: 'In the Bicep snippet from this lesson, what does the `registrationInfo.registrationTokenOperation:
    ''Update''` property do?'
  options:
  - It permanently disables new session hosts from joining the pool
  - It updates the host pool's load-balancing algorithm
  - It rotates/generates a fresh registration token on that deployment rather than reusing a stale or
    previously issued one
  - It triggers the session host update (preview) feature
  answer: 2
  why: Setting registrationTokenOperation to 'Update' on the hostPool resource's registrationInfo tells
    Azure to issue a new registration token (honoring the given expirationTime) as part of that deployment,
    which is the IaC-native way to keep a fresh, short-lived token available for provisioning new session
    hosts.
- q: Which Az.DesktopVirtualization PowerShell cmdlet retrieves the current registration token for a host
    pool without minting a new one?
  options:
  - New-AzWvdRegistrationInfo
  - Update-AzWvdHostPool
  - Remove-AzWvdRegistrationInfo
  - Get-AzWvdHostPoolRegistrationToken
  answer: 3
  why: Get-AzWvdHostPoolRegistrationToken reads the RegistrationTokens currently associated with the host
    pool. New-AzWvdRegistrationInfo is the cmdlet that issues (creates or rotates) a token; the two serve
    different purposes in the same workflow.
- q: Why does this lesson recommend enabling Azure Virtual Desktop Insights diagnostic settings during
    initial deployment rather than after go-live?
  options:
  - Diagnostic data only starts flowing to Log Analytics from the point it's enabled, so enabling it from
    day one avoids a monitoring gap during the most fragile early-adoption period
  - Insights cannot be enabled after a host pool already has session hosts
  - Insights requires a separate Azure subscription if enabled later
  - It's a hard prerequisite for RDP Shortpath
  answer: 0
  why: Diagnostic settings only capture data going forward from when they're enabled — there's no retroactive
    backfill. Wiring diagnostics into the same Bicep deployment that creates the host pool means Module
    6's monitoring and troubleshooting workflows have real data from the first day of the pilot, rather
    than a blind spot during early adoption when issues are most likely to surface.
- q: As of 2026, what is the accurate way to describe the 'session host update' capability for AVD host
    pools?
  options:
  - It is generally available and has fully replaced the need to ever manually replace session hosts
  - It is a preview capability, built on a session host configuration and a session host management policy,
    that automates the deallocate/replace pattern engineers previously scripted by hand; the manual scripted
    replace approach remains fully supported
  - It does not exist in any form and hosts must always be patched in place
  - It only works for personal host pools, never pooled
  answer: 1
  why: Session host update is currently documented as a preview feature. It automates a deallocate-and-recreate
    pattern against a defined session host configuration and management policy — the same outcome engineers
    have long achieved by scripting new-host-provision plus old-host-drain-and-remove themselves. Because
    it's preview, production environments should pilot it in a validation host pool rather than depend
    on it exclusively.
- q: In two to four sentences, explain the classic (non-preview) pattern for refreshing session hosts
    to a new golden image version, and why an engineer might still choose it over the session host update
    preview feature today.
  answer: 'The classic pattern is a self-orchestrated blue/green replacement: provision a batch of new
    session hosts from the latest Azure Compute Gallery image version, put them into service, then set
    the old session hosts to drain mode so no new sessions land on them, wait for existing sessions to
    log off (or force them per a change window), and remove the old hosts from the host pool. An engineer
    might still choose this today because the session host update feature that automates the same outcome
    is in preview, and a team that needs predictable, fully-supported behavior for a production cutover
    — with full control over batch sequencing, validation gates between batches, and rollback — may prefer
    the scripted approach until session host update reaches general availability.'
  why: Understanding the manual pattern matters because it's what session host update automates under
    the hood, and because preview features carry a different support and stability bar than GA capabilities
    — a distinction AZ-140 candidates and production engineers both need to reason about correctly.
resources:
- label: Deploy Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/deploy-azure-virtual-desktop
- label: Microsoft.DesktopVirtualization/hostPools (Bicep, ARM template reference)
  url: https://learn.microsoft.com/en-us/azure/templates/microsoft.desktopvirtualization/hostpools
- label: Az.DesktopVirtualization PowerShell module reference
  url: https://learn.microsoft.com/en-us/powershell/module/az.desktopvirtualization/
- label: Session host update (preview) - Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/session-host-update
- label: Azure Virtual Desktop Insights
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/insights
video: vdi-m3-l04-deploying-host-pools.mp4
---

## From Design to a Working Host Pool

The previous three lessons gave you the architecture, the network, and the image. This lesson turns that into an actual deployed environment — first the portal walkthrough so you understand every field the wizard is setting on your behalf, then the infrastructure-as-code approach you'll actually use for anything beyond a proof of concept, and finally how to keep session hosts current once they're running.

## The Portal Deployment Walkthrough

Creating a host pool through the Azure portal's "Create a host pool" wizard walks you through exactly the decisions covered in Lesson 1 and Lesson 3, in order:

1. **Basics**: resource group, host pool name, location, host pool type (Personal/Pooled), and for pooled pools the load-balancing algorithm and max session limit.
2. **Virtual machines**: whether to add session hosts now or later, the resource group and image source (marketplace or your Azure Compute Gallery version), VM size, number of VMs, and network/domain-join configuration (Microsoft Entra ID join, Microsoft Entra hybrid join, or Active Directory Domain Services — covered fully in Module 4).
3. **Workspace**: create a new workspace or add to an existing one, which is what makes the host pool's desktop or apps show up in a user's feed at all.
4. **Advanced / diagnostics**: this is where you can enable the **Azure Virtual Desktop Insights** workbook at deployment time by pointing session host diagnostic settings at a Log Analytics workspace — doing this during initial deployment saves you from retrofitting monitoring after users are already on the platform, and it directly sets up the KQL-based monitoring you'll build on in Module 6.

The portal wizard is a legitimate way to learn the resource model and to stand up a small pilot quickly. It is not how you run a production environment past a handful of host pools — that's what infrastructure as code is for.

## Infrastructure as Code: Bicep as the Primary Path

For anything you intend to keep, redeploy, or scale, define your host pool, application groups, and workspace as **Bicep** resources under source control. Bicep is the primary IaC language this course uses because it's Microsoft's own first-party authoring layer over ARM, with the freshest AVD resource-type support and no third-party provider lag. A minimal but real example, using the verified `Microsoft.DesktopVirtualization` resource types:

```bicep
resource hostPool 'Microsoft.DesktopVirtualization/hostPools@2024-04-03' = {
  name: hostPoolName
  location: location
  properties: {
    hostPoolType: 'Pooled'
    loadBalancerType: 'BreadthFirst'
    preferredAppGroupType: 'Desktop'
    maxSessionLimit: 6
    startVMOnConnect: true
    validationEnvironment: false
    registrationInfo: {
      expirationTime: registrationTokenExpiration
      registrationTokenOperation: 'Update'
    }
  }
}

resource desktopAppGroup 'Microsoft.DesktopVirtualization/applicationGroups@2024-04-03' = {
  name: '${hostPoolName}-dag'
  location: location
  properties: {
    hostPoolArmPath: hostPool.id
    applicationGroupType: 'Desktop'
  }
}

resource workspace 'Microsoft.DesktopVirtualization/workspaces@2024-04-03' = {
  name: workspaceName
  location: location
  properties: {
    applicationGroupReferences: [
      desktopAppGroup.id
    ]
  }
}
```

A few details worth calling out in that snippet: `hostPoolType`, `loadBalancerType`, and `preferredAppGroupType` are the same three planning decisions from Lesson 1, now expressed as resource properties. `registrationInfo` is how you issue a **registration token** — the credential a new session host's AVD agent uses during setup to join itself to this specific host pool; tokens have an `expirationTime` you control, and `registrationTokenOperation: 'Update'` rotates the token on each deployment rather than reusing a stale one indefinitely. The `applicationGroups` resource references the host pool by `hostPoolArmPath`, and the `workspaces` resource pulls the application groups together into the feed users see — exactly the object relationships from Lesson 1, now as deployable resources.

**Terraform note**: if your organization standardizes on Terraform instead, the `azurerm` provider has first-class resources for AVD (`azurerm_virtual_desktop_host_pool`, `azurerm_virtual_desktop_application_group`, `azurerm_virtual_desktop_workspace`, and session-host-related resources) that map onto the same underlying `Microsoft.DesktopVirtualization` resource provider. The planning decisions are identical either way — Bicep versus Terraform is a tooling choice, not an architecture choice — but this course authors examples in Bicep because it tracks new AVD API versions fastest.

## Registration Keys and Tokens in Practice

Whether you provision through the portal, Bicep, or PowerShell, every new session host needs a **registration token** to join a host pool. In PowerShell, `New-AzWvdRegistrationInfo` issues a fresh token with a chosen expiration time, and `Get-AzWvdHostPoolRegistrationToken` retrieves the current one associated with a host pool without minting a new one:

```powershell
# Issue a registration token valid for 24 hours
New-AzWvdRegistrationInfo `
  -ResourceGroupName "rg-avd-prod" `
  -HostPoolName "hp-avd-prod-pooled01" `
  -ExpirationTime (Get-Date).ToUniversalTime().AddHours(24).ToString("yyyy-MM-ddTHH:mm:ss.fffffffZ")

# Retrieve the current token for automation to consume
Get-AzWvdHostPoolRegistrationToken `
  -ResourceGroupName "rg-avd-prod" `
  -HostPoolName "hp-avd-prod-pooled01"
```

Treat registration tokens as short-lived secrets: mint them close to the deployment window that consumes them, never hardcode one into a golden image, and let your Bicep or Terraform pipeline handle rotation as part of the deployment rather than a human copy-pasting a token from the portal.

## Enabling Insights at Deploy Time

The **Azure Virtual Desktop Insights** workbook depends on diagnostic settings being enabled on the host pool, workspace, and application group resources, sending data to a Log Analytics workspace. Enabling this during your initial Bicep deployment — rather than as a follow-up task — means every session host you add from day one is already contributing connection, error, and performance data to the workbook, so Module 6's monitoring lessons have real historical data to work with instead of a monitoring gap during your most fragile early-adoption period.

## Session Host Update: Where the Feature Stands Today

Historically, keeping session hosts current meant a manual or scripted pattern: build a new image version, provision new session hosts from it, drain and remove old ones — effectively a blue/green replacement you orchestrated yourself with PowerShell or your pipeline of choice. That pattern remains fully supported and is still the right mental model to teach.

As of 2026, Microsoft also offers **session host update** as a **preview** capability layered on top of a host pool. You define a **session host configuration** (a sub-resource of the host pool specifying the target image, VM properties, and network settings) and a **session host management** policy (specifying batch size — how many hosts are replaced concurrently — and scheduling), and Azure Virtual Desktop then deallocates or deletes existing session hosts and creates replacements that match the configuration automatically, rather than you scripting the replacement loop yourself. Because this is explicitly a **preview** feature at the time of writing, treat it as something to pilot in a validation host pool and track for GA, not something to depend on for a production cutover today — the underlying replace-and-reprovision pattern it automates is exactly what you'd otherwise orchestrate by hand.

## Putting the Deployment Together

A production-grade host pool deployment, in order: Bicep templates define the host pool, application groups, and workspace with diagnostic settings wired in from the start; a pipeline mints a short-lived registration token and provisions session hosts from a specific Azure Compute Gallery image version; Insights starts collecting data immediately; and session host refreshes follow either your own scripted replace pattern or the session host update preview feature, depending on how much you're willing to depend on a preview capability for your environment's maturity level.
