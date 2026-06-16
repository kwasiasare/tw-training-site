---
course: helpdesk-tier3-advanced
title: Automating Intune and Entra with Graph
month: 2
monthTitle: 'Automation: PowerShell & Microsoft Graph at Scale'
lesson: 3
summary: 'Apply the Graph SDK to real endpoint operations: query and act on Intune devices, manage Entra
  users and groups, and drive bulk changes safely with WhatIf.'
objectives:
- Query Intune managed devices and trigger device actions through Graph
- Manage Entra ID users and group memberships programmatically
- Resolve a device or user object to its Graph id before acting on it
- Drive dynamic vs assigned group membership and understand the difference
- Add ShouldProcess so bulk scripts support -WhatIf and -Confirm
- Throttle-proof a bulk operation with batching and Retry-After handling
video: ht2-l03-automating-intune-and-entra.mp4
quiz:
- q: Before you can POST a device action like sync or wipe, what do you usually need first?
  options:
  - The device's Graph object id, obtained by querying managedDevices
  - The device's serial number only
  - Local admin on the device
  - The user's password
  answer: 0
  why: Graph actions target a resource by its id in the URL (for example /managedDevices/{id}/syncDevice),
    so you resolve the device to its id before calling the action.
- q: What is the practical difference between an Entra dynamic group and an assigned group?
  options:
  - Dynamic groups cannot hold devices
  - Assigned groups update faster
  - There is no difference, only the name
  - Dynamic group membership is evaluated automatically from a rule; assigned membership is set manually
  answer: 3
  why: Dynamic groups recalculate membership from a membership rule (e.g. device OS), while assigned groups
    require you to add and remove members explicitly via Graph or the portal.
- q: Which cmdlet triggers an Intune device sync action from the SDK?
  options:
  - Sync-MgDevice
  - Sync-MgDeviceManagementManagedDevice
  - Invoke-MgSyncDeviceManagementManagedDevice
  - Update-MgDeviceSync
  answer: 1
  why: Sync-MgDeviceManagementManagedDevice -ManagedDeviceId <id> issues the syncDevice action; many Intune
    actions also have an equivalent Invoke-MgGraphRequest POST.
- q: Why add SupportsShouldProcess and call ShouldProcess in a bulk-change function?
  options:
  - It makes the script run faster
  - It is required to connect to Graph
  - It gives the function free -WhatIf and -Confirm so callers can preview destructive changes
  - It encrypts the output
  answer: 2
  why: SupportsShouldProcess plus an if ($PSCmdlet.ShouldProcess(...)) guard lets users dry-run with -WhatIf
    and gate risky bulk actions with -Confirm before anything changes.
- q: When Graph returns HTTP 429, what header tells you how long to wait before retrying?
  answer: The Retry-After header; honour it by sleeping for that many seconds before retrying, ideally
    with exponential backoff.
  why: 429 Too Many Requests means you are throttled; respecting Retry-After (and backing off) is the
    correct, supported way to keep bulk jobs running without making throttling worse.
- q: In one sentence, why resolve a user to their object id rather than acting by userPrincipalName everywhere?
  answer: The object id is the stable, unique key Graph uses for relationship calls like group membership,
    and it does not change if the userPrincipalName is renamed.
  why: UPNs can be renamed and are not always accepted on relationship endpoints, so resolving to the
    immutable id first makes bulk scripts reliable.
resources:
- label: Microsoft Learn — Intune deviceManagement managedDevice API
  url: https://learn.microsoft.com/en-us/graph/api/resources/intune-devices-manageddevice
- label: Microsoft Learn — Working with groups in Microsoft Graph
  url: https://learn.microsoft.com/en-us/graph/api/resources/groups-overview
- label: Microsoft Learn — Microsoft Graph throttling guidance
  url: https://learn.microsoft.com/en-us/graph/throttling
- label: Microsoft Learn — about_Functions_CmdletBindingAttribute (ShouldProcess)
  url: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_cmdletbindingattribute
---

## Acting on Intune devices, not just reading them

Reading inventory is half the job. The other half is **taking action** — sync, restart, retire, or wipe a device. Graph actions target a resource by its **id** in the URL, so the workflow is always: resolve to id, then act.

```powershell
Connect-MgGraph -Scopes 'DeviceManagementManagedDevices.PrivilegedOperations.All','DeviceManagementManagedDevices.ReadWrite.All'

# Resolve the device to its Graph id
$device = Get-MgDeviceManagementManagedDevice -All `
    -Filter "deviceName eq 'LAP-0427'"

# Trigger a sync action against that id
Sync-MgDeviceManagementManagedDevice -ManagedDeviceId $device.Id
```

Privileged actions like wipe require a stronger scope (`PrivilegedOperations.All`). Request it only in scripts that genuinely need it.

## Managing Entra users and groups

The same SDK manages **Entra ID**. Users, groups, and the relationships between them are all Graph resources.

```powershell
# Resolve a user to their stable object id
$user = Get-MgUser -Filter "userPrincipalName eq 'jdoe@contoso.com'"

# Add that user to a group by id
New-MgGroupMember -GroupId $groupId -DirectoryObjectId $user.Id
```

Always act on the **object id**, not the `userPrincipalName`. UPNs get renamed; the id never changes and relationship endpoints expect it.

## Dynamic vs assigned groups

An **assigned group** is one you add and remove members from by hand (or by script). A **dynamic group** recalculates its membership from a **membership rule** — for example, all Windows devices. You manage assigned groups with `New-MgGroupMember`; you manage dynamic ones by editing the rule.

```powershell
# A dynamic device group: rule, not manual members
$params = @{
    DisplayName     = 'All Windows Devices'
    MailEnabled     = $false
    MailNickname    = 'allWinDevices'
    SecurityEnabled = $true
    GroupTypes      = @('DynamicMembership')
    MembershipRule  = '(device.deviceOSType -eq "Windows")'
    MembershipRuleProcessingState = 'On'
}
New-MgGroup @params
```

## Make bulk changes safe with ShouldProcess

A script that loops over hundreds of devices must support a **dry run**. Adding `SupportsShouldProcess` to `[CmdletBinding()]` gives your function free `-WhatIf` and `-Confirm`.

```powershell
function Invoke-DeviceSyncBulk {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
    param([Parameter(Mandatory)][object[]]$Devices)
    process {
        foreach ($d in $Devices) {
            if ($PSCmdlet.ShouldProcess($d.DeviceName, 'Sync device')) {
                Sync-MgDeviceManagementManagedDevice -ManagedDeviceId $d.Id
            }
        }
    }
}
# Preview first, then commit:
Invoke-DeviceSyncBulk -Devices $stale -WhatIf
```

## Surviving throttling at scale

Graph throttles aggressive callers with **HTTP 429**. The response carries a **`Retry-After`** header telling you how long to pause. Honour it, ideally with backoff.

```powershell
foreach ($d in $devices) {
    try {
        Sync-MgDeviceManagementManagedDevice -ManagedDeviceId $d.Id -ErrorAction Stop
    }
    catch {
        if ($_.Exception.Response.StatusCode -eq 429) {
            $wait = [int]($_.Exception.Response.Headers.RetryAfter.Delta.TotalSeconds)
            Start-Sleep -Seconds ($wait ? $wait : 10)
        }
        else { throw }
    }
}
```

## Your task

Write a function `Set-StaleDeviceGroup` that finds all managed devices whose `lastSyncDateTime` is older than 30 days, resolves each to its id, and adds them to a specified assigned Entra group. Support `-WhatIf` via `SupportsShouldProcess`, request only the scopes you need, and wrap the group-add call in a try/catch that honours `Retry-After` on a 429. Run it once with `-WhatIf` to prove the preview works before any change is made.
