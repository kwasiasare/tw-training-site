---
course: helpdesk-tier3-advanced
title: Microsoft Graph API and the PowerShell SDK
month: 2
monthTitle: 'Automation: PowerShell & Microsoft Graph at Scale'
lesson: 2
summary: Understand what Microsoft Graph is, how it exposes Microsoft 365 and Intune as one REST API,
  and how to drive it from PowerShell with the Microsoft Graph SDK.
objectives:
- Describe Microsoft Graph as a single REST endpoint over Entra, Intune, and M365
- Install the Microsoft Graph PowerShell SDK and its sub-modules
- Authenticate with Connect-MgGraph using the right delegated scopes
- Map a Graph REST endpoint to the equivalent Get-Mg* SDK cmdlet
- Page through large result sets with -All instead of truncated pages
- Call endpoints the SDK has no cmdlet for using Invoke-MgGraphRequest
video: ht2-l02-microsoft-graph-and-sdk.mp4
quiz:
- q: What is Microsoft Graph?
  options:
  - A single REST API and endpoint that unifies Entra ID, Intune, and Microsoft 365 data
  - A charting library for reports
  - A replacement for PowerShell
  - A local database on each device
  answer: 0
  why: Microsoft Graph is the unified REST API at graph.microsoft.com that exposes users, devices, Intune,
    mail, and more behind one consistent endpoint and permission model.
- q: Which cmdlet authenticates a session and requests permission scopes for the Graph SDK?
  options:
  - Login-AzAccount
  - Connect-MgGraph -Scopes ...
  - Enable-MgSession
  - Start-MgGraph
  answer: 1
  why: Connect-MgGraph establishes the session; the -Scopes parameter requests the delegated permissions
    your subsequent calls require, following least privilege.
- q: By default a Graph list call returns a limited page of results. How do you retrieve every item with
    an SDK cmdlet?
  options:
  - Run the cmdlet repeatedly until it errors
  - Set -Top 100000
  - Pass the -All switch so the SDK follows the nextLink automatically
  - There is no way; Graph caps results
  answer: 2
  why: Graph paginates with an @odata.nextLink; the SDK's -All switch follows those links for you so you
    get the complete collection rather than just the first page.
- q: When should you reach for Invoke-MgGraphRequest instead of a Get-Mg* cmdlet?
  options:
  - Never, the cmdlets cover everything
  - When you need a beta endpoint or one with no dedicated cmdlet, or full control over the raw request
  - Only for authentication
  - Only on PowerShell 5.1
  answer: 1
  why: Invoke-MgGraphRequest sends raw authenticated requests to any Graph URI, which is essential for
    beta endpoints, new features, or actions the typed cmdlets do not yet expose.
- q: Name the command that lists which scopes (permissions) your current Graph session actually holds.
  answer: (Get-MgContext).Scopes — Get-MgContext returns the active connection context including the granted
    Scopes, account, and tenant.
  why: 'Checking Get-MgContext before troubleshooting saves time: a 403 is very often a missing scope
    rather than a code bug.'
- q: In one sentence, why request the narrowest set of scopes your script needs rather than broad ones?
  answer: Least privilege limits the blast radius if credentials are misused and is required for security
    reviews and admin consent, so you ask only for the specific scopes the script's calls require.
  why: Scopes are the permission model; requesting only what you need keeps consent prompts honest and
    reduces risk if the session or app is compromised.
resources:
- label: Microsoft Learn — Microsoft Graph PowerShell SDK overview
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/overview
- label: Microsoft Learn — Install the Microsoft Graph PowerShell SDK
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/installation
- label: Microsoft Learn — Microsoft Graph REST API v1.0 reference
  url: https://learn.microsoft.com/en-us/graph/api/overview
- label: Microsoft Learn — Use Invoke-MgGraphRequest
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/navigating?view=graph-powershell-1.0
---

## One API over your whole tenant

**Microsoft Graph** is a single REST API, served from `https://graph.microsoft.com`, that exposes almost everything in your Microsoft cloud: **Entra ID** users and groups, **Intune** managed devices and policies, mail, Teams, and more. Instead of one module per product, you learn one endpoint, one permission model, and one query language (**OData**).

Everything is a resource at a URL. Users live at `/users`, managed devices at `/deviceManagement/managedDevices`, groups at `/groups`. Learn the URL pattern once and the whole API opens up.

## Installing and connecting the SDK

The **Microsoft Graph PowerShell SDK** is a family of modules. Install the meta-module, or just the sub-modules you need to keep load times short.

```powershell
# Install once, for the current user
Install-Module Microsoft.Graph -Scope CurrentUser

# Or targeted sub-modules only
Install-Module Microsoft.Graph.Authentication -Scope CurrentUser
Install-Module Microsoft.Graph.DeviceManagement -Scope CurrentUser
```

Authentication is **scope-based**. You ask only for the **delegated scopes** your script actually uses — this is least privilege, and reviewers will check it.

```powershell
Connect-MgGraph -Scopes 'DeviceManagementManagedDevices.Read.All','User.Read.All'

# Confirm who you are and what you can do
(Get-MgContext).Scopes
```

If a call later returns **403 Forbidden**, your first suspect is a missing scope — check `Get-MgContext` before you blame your code.

## From REST endpoint to Get-Mg cmdlet

Every Graph endpoint maps to a typed cmdlet. The pattern is predictable: `GET /deviceManagement/managedDevices` becomes `Get-MgDeviceManagementManagedDevice`.

```powershell
# Get every managed device, following pagination automatically
$devices = Get-MgDeviceManagementManagedDevice -All

$devices |
    Where-Object { $_.OperatingSystem -eq 'Windows' } |
    Select-Object DeviceName, OsVersion, LastSyncDateTime
```

The **`-All`** switch matters. Without it, Graph returns just the first page and silently follows an `@odata.nextLink` for the rest; `-All` walks every page so you do not miss devices.

## OData query options keep payloads small

Do not pull whole objects and filter in PowerShell when Graph can do it server-side. Use `-Filter`, `-Select`, and `-Top`.

```powershell
Get-MgDeviceManagementManagedDevice -All `
    -Filter "operatingSystem eq 'Windows'" `
    -Property 'deviceName,osVersion,complianceState' |
    Select-Object DeviceName, OsVersion, ComplianceState
```

Server-side filtering means less data over the wire and fewer throttling problems on big tenants.

## Invoke-MgGraphRequest for anything the cmdlets miss

New features land in the **beta** endpoint first, and not every action has a typed cmdlet. **`Invoke-MgGraphRequest`** sends a raw authenticated request to any Graph URI and reuses your existing token.

```powershell
$uri = 'https://graph.microsoft.com/beta/deviceManagement/managedDevices?$top=5'
$response = Invoke-MgGraphRequest -Method GET -Uri $uri
$response.value | Select-Object deviceName, osVersion

# It also works for actions:
Invoke-MgGraphRequest -Method POST `
    -Uri 'https://graph.microsoft.com/v1.0/deviceManagement/managedDevices/{id}/rebootNow'
```

This is your escape hatch — when the SDK has no cmdlet, the REST call always works.

## Your task

Connect to Graph with the minimum scopes needed to read managed devices. Write a function `Get-IntuneDeviceInventory` that retrieves **all** managed devices with `-All`, uses server-side `-Filter` and `-Property` to return only Windows devices and only the `deviceName`, `osVersion`, and `lastSyncDateTime` fields, and exports the result to CSV. Then re-implement the same read using `Invoke-MgGraphRequest` against the v1.0 endpoint and confirm the two approaches return the same count.
