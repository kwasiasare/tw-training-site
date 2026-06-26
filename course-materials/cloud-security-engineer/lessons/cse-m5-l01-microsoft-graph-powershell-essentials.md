---
course: cloud-security-engineer
title: Microsoft Graph PowerShell SDK Essentials
month: 5
monthTitle: Security Automation with PowerShell, Graph API & Logic Apps
lesson: 1
summary: Microsoft Graph is the single REST API that fronts almost every M365 and Microsoft Entra ID workload,
  and the Microsoft Graph PowerShell SDK is the supported way to drive it from scripts. This lesson explains
  why Graph replaced the retired MSOnline and AzureAD modules, how to connect with least-privilege scopes,
  and the difference between delegated and application permissions. You will register an app, create a
  service principal, and authenticate unattended with a certificate or client secret. Finally you will
  learn to discover cmdlets with Find-MgGraphCommand, map permissions with Find-MgGraphPermission, and
  read users, groups, and sign-ins while handling pagination and throttling.
objectives:
- Explain why Microsoft Graph is the unified API for M365 and Microsoft Entra ID and why the SDK replaced
  MSOnline/AzureAD
- Connect interactively with Connect-MgGraph using least-privilege scopes and review consent
- Distinguish delegated from application permissions and choose the right one for a scenario
- Register an app, create a service principal, and authenticate unattended with a certificate or client
  secret
- Discover cmdlets and required permissions with Find-MgGraphCommand and Find-MgGraphPermission
- Read users, groups, and sign-in logs while handling pagination with -All and Graph throttling
video: cse-m5-l01-microsoft-graph-powershell-essentials.mp4
quiz:
- q: Why is the Microsoft Graph PowerShell SDK the recommended tool for M365 and Entra automation in 2026?
  options:
  - It is the only module that can run on Windows PowerShell 5.1
  - It wraps the unified Microsoft Graph API after the legacy MSOnline and AzureAD modules were retired
  - It stores credentials in plain text so scripts never need to re-authenticate
  - It bypasses Conditional Access policies for administrators
  answer: 1
  why: Microsoft Graph is the single API surface for Entra ID, Exchange, Teams, Intune and more. The MSOnline
    and AzureAD PowerShell modules were deprecated and retired, so the Graph SDK is the supported successor
    and the SDK simply wraps Graph REST calls as cmdlets.
- q: You are building an unattended Azure Automation runbook that reads all users nightly. Which permission
    type should the app use?
  options:
  - Delegated permissions, because a signed-in admin is always present
  - Application permissions, because the app runs without a signed-in user
  - No permissions, because runbooks inherit tenant admin rights automatically
  - Both delegated and application permissions are required together
  answer: 1
  why: Application permissions grant the app its own identity and access without a signed-in user, which
    is exactly what an unattended runbook needs. Delegated permissions act on behalf of a signed-in user
    and are unsuitable for headless automation.
- q: Which command tells you which Graph cmdlet backs a given REST API call such as GET /users?
  options:
  - Get-Help GET-users
  - Find-MgGraphCommand -Uri '/users' -Method GET
  - Resolve-MgGraphEndpoint /users
  - Search-MgGraphApi users
  answer: 1
  why: Find-MgGraphCommand maps Graph REST URIs and methods to SDK cmdlets and also lists the permissions
    each cmdlet requires, making it the primary discovery tool when you know the API but not the cmdlet
    name.
- q: What does the -All switch do on a cmdlet like Get-MgUser?
  options:
  - It returns every property of each object including hidden ones
  - It automatically follows @odata.nextLink paging to return the full result set
  - It elevates the session to Global Administrator
  - It disables throttling so the request never gets a 429
  answer: 1
  why: Graph returns results in pages with an @odata.nextLink. The -All switch makes the SDK follow those
    links and return the complete collection instead of just the first page, which is essential for tenant-wide
    reporting.
- q: When a script sends many Graph requests rapidly and receives HTTP 429 responses, what is the correct
    handling?
  options:
  - Immediately retry in a tight loop until it succeeds
  - Stop the script permanently because the tenant is blocked
  - Honor the Retry-After header and back off before retrying
  - Switch from application to delegated permissions
  answer: 2
  why: HTTP 429 means the request was throttled. Graph returns a Retry-After header telling you how long
    to wait; well-behaved automation backs off for that duration (the SDK does this automatically) rather
    than hammering the service, which would only extend the throttling.
- q: In two to four sentences, explain the difference between delegated and application permissions in
    Microsoft Graph and give one concrete example of when you would choose each.
  answer: Delegated permissions let an application act on behalf of a signed-in user, so the effective
    access is the intersection of the app's granted scopes and that user's own privileges; you would use
    them for an interactive admin tool where a human signs in and operates within their own rights. Application
    permissions give the app its own identity and a fixed set of rights with no signed-in user, so they
    are appropriate for unattended automation such as a nightly Azure Automation runbook that audits every
    user in the tenant. The key trade-off is that application permissions are powerful and not bounded
    by a user's rights, so they must be granted sparingly and protected with a certificate-based credential.
  why: Delegated permissions are user-context and bounded by the user's own rights; application permissions
    are app-context, unbounded by any user, and meant for headless scenarios. Choosing correctly is the
    foundation of least-privilege Graph automation.
resources:
- label: Get started with the Microsoft Graph PowerShell SDK
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/get-started
- label: Use app-only authentication with the Microsoft Graph PowerShell SDK
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/app-only
- label: Find Microsoft Graph PowerShell permissions for a command
  url: https://learn.microsoft.com/en-us/powershell/microsoftgraph/find-mg-graph-command
- label: Microsoft Graph throttling guidance
  url: https://learn.microsoft.com/en-us/graph/throttling
---

## Why Microsoft Graph Is the Unified API

For years, administering Microsoft 365 meant juggling a pile of single-purpose PowerShell modules: `MSOnline`, `AzureAD`, separate Exchange and Teams modules, each with its own auth and its own quirks. That era is over. **Microsoft Graph** is now the single REST API that fronts almost every workload, Microsoft Entra ID (users, groups, sign-ins, Conditional Access), Exchange Online, Teams, Intune, SharePoint, and security signals. The legacy `MSOnline` and `AzureAD` modules have been **deprecated and retired**, so new automation must target Graph.

The **Microsoft Graph PowerShell SDK** is the supported way to call Graph from scripts. It is a set of modules (`Microsoft.Graph.*`) generated directly from the Graph API definition, so each cmdlet is a thin wrapper over a REST endpoint. Install only what you need to keep sessions lean:

```powershell
Install-Module Microsoft.Graph.Authentication -Scope CurrentUser
Install-Module Microsoft.Graph.Users -Scope CurrentUser
Install-Module Microsoft.Graph.Identity.SignIns -Scope CurrentUser
```

## Connecting with Least-Privilege Scopes

Every Graph call is gated by **scopes** (permissions). The golden rule is least privilege: ask only for what the script truly needs, and read-only wherever possible. Interactive sign-in uses `Connect-MgGraph` with one or more scopes:

```powershell
Connect-MgGraph -Scopes "User.Read.All", "AuditLog.Read.All", "Group.Read.All"

# Inspect the current session, including the scopes you actually consented to
Get-MgContext | Select-Object Account, TenantId, AuthType, Scopes
```

The first time you request a scope, Entra ID shows a **consent** prompt. Note `.Read` vs `.ReadWrite`: a reporting script should never request write scopes. When you are done, `Disconnect-MgGraph` ends the session.

## Delegated vs Application Permissions

This is the single most important concept in Graph automation.

- **Delegated permissions** act *on behalf of a signed-in user*. The effective access is the **intersection** of the app's scopes and the user's own rights. Use them for interactive tools where a human signs in.
- **Application permissions** give the app *its own identity* with a fixed set of rights and **no signed-in user**. Use them for unattended automation, runbooks, scheduled jobs, Logic Apps.

Application permissions are powerful precisely because they are not bounded by any user's rights, so grant them sparingly and require admin consent.

## Unattended Auth: App Registration, Service Principal, Certificate

Headless automation needs an **app registration** in Entra ID, which creates a **service principal** (the identity) in your tenant. Grant it application permissions (for example `User.Read.All`) and **grant admin consent**. For credentials, prefer a **certificate** over a client secret because certificates are not a copyable shared string.

```powershell
# Create a self-signed cert for the app (store the public key on the app registration)
$cert = New-SelfSignedCertificate -Subject "CN=GraphAutomation" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -KeyExportPolicy Exportable -KeySpec Signature

# Connect unattended with app-only auth (no user prompt)
Connect-MgGraph -ClientId "00000000-1111-2222-3333-444444444444" `
    -TenantId  "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee" `
    -CertificateThumbprint $cert.Thumbprint
```

In Azure Automation or a Function, you can skip stored credentials entirely and use a **managed identity**: `Connect-MgGraph -Identity`. The managed identity's service principal still needs the application permissions assigned to it.

## Discovering Cmdlets and Permissions

The SDK has thousands of cmdlets. Two discovery commands save hours. `Find-MgGraphCommand` maps a REST URI to the cmdlet that calls it and lists the permissions it needs; `Find-MgGraphPermission` searches the permission catalog.

```powershell
# I know the REST call GET /users - which cmdlet and permissions?
Find-MgGraphCommand -Uri '/users' -Method GET |
    Select-Object Command, Permissions -First 1

# Find every permission related to sign-in audit logs
Find-MgGraphPermission auditlog -PermissionType Application
```

Use these to build a precise, least-privilege scope list instead of guessing.

## Reading Users, Groups, and Sign-Ins (Pagination and Throttling)

Graph returns large collections in **pages** linked by `@odata.nextLink`. The `-All` switch makes the SDK follow every page automatically. Always select only the properties you need, and request non-default properties like `signInActivity` explicitly (it is GA on the v1.0 endpoint but is not returned unless you select it, and it requires `AuditLog.Read.All`).

```powershell
# All members - note -All to page through the whole tenant
$users = Get-MgUser -All -Property "id,displayName,userPrincipalName,accountEnabled"

# Last interactive sign-in requires AuditLog.Read.All and the signInActivity property
Get-MgUser -All -Property "displayName,signInActivity" |
    Select-Object DisplayName,
        @{N='LastSignIn';E={ $_.SignInActivity.LastSignInDateTime }}

# Group membership
Get-MgGroup -Filter "displayName eq 'Finance'" |
    ForEach-Object { Get-MgGroupMember -GroupId $_.Id -All }
```

When you send many requests quickly, Graph may return **HTTP 429 (throttled)** with a `Retry-After` header. The SDK honors this and backs off automatically; in custom loops, respect `Retry-After` rather than retrying in a tight loop. Designing for pagination and throttling from the start is what separates a script that works on a 10-user lab from one that survives a 50,000-user tenant.
