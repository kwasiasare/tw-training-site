---
course: cloud-security-engineer
title: Automating Tenant Security Audits and Compliance Reports
month: 5
monthTitle: Security Automation with PowerShell, Graph API & Logic Apps
lesson: 2
summary: Manual tenant audits do not scale and they go stale the moment they finish. In this lesson you
  turn the Microsoft Graph PowerShell SDK into a repeatable audit engine that finds users without strong
  authentication, stale and inactive accounts, the full guest inventory, risky users, privileged role
  assignments, and your Conditional Access posture. You will generate clean CSV and HTML compliance reports
  that auditors can read. Finally you will schedule the whole thing as an Azure Automation runbook authenticating
  with a managed identity, so the report runs itself every night with no stored secrets.
objectives:
- Script a bulk audit of users lacking strong authentication using authentication method registration
  data
- Identify stale and inactive accounts from signInActivity.lastSignInDateTime
- Inventory guest accounts, risky users, and privileged directory role assignments
- Export Conditional Access policies for review and drift detection
- Generate readable CSV and HTML compliance reports from collected findings
- Schedule the audit as an Azure Automation runbook using a managed identity with least privilege
video: cse-m5-l02-automating-tenant-security-audits.mp4
quiz:
- q: Which Graph endpoint or report is the most reliable source for whether a user has registered strong
    authentication methods?
  options:
  - The user's StrongAuthenticationMethods property from the old MSOnline module
  - reports/authenticationMethods/userRegistrationDetails (Get-MgReportAuthenticationMethodUserRegistrationDetail)
  - The accountEnabled property on the user object
  - The user's lastPasswordChangeDateTime
  answer: 1
  why: The authentication methods registration report (userRegistrationDetails) reports per user whether
    they are registered and capable of MFA and passwordless. The legacy StrongAuthenticationMethods property
    came from the retired MSOnline module and is no longer the supported source.
- q: To detect stale accounts, which property must you request and what permission does it require?
  options:
  - lastPasswordChangeDateTime, requiring Directory.Read.All
  - signInActivity (lastSignInDateTime), requiring AuditLog.Read.All
  - createdDateTime, requiring User.Read
  - accountEnabled, requiring no special permission
  answer: 1
  why: signInActivity.lastSignInDateTime tells you when a user last actually signed in, which is the basis
    for staleness. It is not returned by default and requires the AuditLog.Read.All permission plus explicit
    selection in the -Property list.
- q: How do you identify guest (external) accounts in a Graph user query?
  options:
  - Filter where accountEnabled eq false
  - Filter where userType eq 'Guest'
  - Filter where displayName contains '#EXT#'
  - Guests cannot be queried via Graph
  answer: 1
  why: 'Guest accounts have userType equal to ''Guest'' (their UPN typically contains #EXT# but userType
    is the reliable filter). You can pass -Filter "userType eq ''Guest''" to Get-MgUser to enumerate the
    guest inventory.'
- q: Why is a managed identity preferred over a stored client secret for an Azure Automation audit runbook?
  options:
  - Managed identities run faster than secret-based auth
  - There is no credential to store, rotate, or leak; Azure manages it
  - Managed identities automatically grant Global Administrator
  - Client secrets cannot be used with Graph at all
  answer: 1
  why: A managed identity has no secret or certificate for you to store, rotate, or accidentally commit
    to source control. Azure issues and rotates the credential automatically, so the runbook connects
    with Connect-MgGraph -Identity and you simply assign the identity least-privilege Graph application
    permissions.
- q: When exporting findings, why convert objects with ConvertTo-Csv/Export-Csv using -NoTypeInformation
    (or modern PowerShell defaults) and selected properties?
  options:
  - It encrypts the CSV file
  - It produces a clean, flat report with only the columns auditors need and no PowerShell type header
  - It is the only way to write a file in Azure Automation
  - It prevents the script from being throttled
  answer: 1
  why: Selecting explicit properties and exporting without the type-information header yields a flat,
    readable CSV with exactly the columns an auditor expects. Dumping raw Graph objects produces nested,
    noisy output that is hard to consume.
- q: In two to four sentences, describe the least-privilege application permissions you would assign to
    an unattended runbook that reports users without MFA, stale accounts, and the guest inventory, and
    explain why each is read-only.
  answer: The runbook needs User.Read.All to enumerate users and their properties, AuditLog.Read.All to
    read signInActivity for staleness detection, and either UserAuthenticationMethod.Read.All or the AuthenticationMethods
    report permission (Reports.Read.All / Policy.Read.All depending on the exact API) to read registration
    details, plus Directory.Read.All if it also reports role assignments. Every one of these is a .Read
    permission because an audit only inspects state and never changes it, so granting write scopes would
    needlessly expand the blast radius if the identity were compromised. Keeping the runbook read-only
    also means it can never accidentally disable an account or alter a policy, which keeps the audit safe
    to run on a schedule.
  why: An audit is a read-only operation, so it should hold only read scopes scoped to the data it inspects.
    This minimizes blast radius and aligns with least privilege, the core principle of secure automation.
resources:
- label: authenticationMethods userRegistrationDetails report
  url: https://learn.microsoft.com/en-us/graph/api/authenticationmethodsroot-list-userregistrationdetails
- label: Manage inactive user accounts in Microsoft Entra ID (signInActivity)
  url: https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-manage-inactive-user-accounts
- label: Use a managed identity with Azure Automation
  url: https://learn.microsoft.com/en-us/azure/automation/enable-managed-identity-for-automation
- label: List Conditional Access policies (Graph)
  url: https://learn.microsoft.com/en-us/graph/api/conditionalaccessroot-list-policies
---

## Why Automate Audits

A security posture review you run by hand in the portal is out of date the moment you close the browser, and it cannot be diffed, scheduled, or trusted to be consistent. **Automated audits** turn posture into data: a script collects the same evidence every time, on a schedule, and emits a report you can compare week over week to spot drift. In this lesson we build that engine on the Graph PowerShell SDK and ship it as a nightly Azure Automation runbook.

The permissions are all **read-only**, because an audit only inspects state. A typical scope set: `User.Read.All`, `AuditLog.Read.All`, `Policy.Read.All`, and `Directory.Read.All`.

## Finding Users Without Strong Authentication

The single highest-value audit is *who can sign in without MFA*. Do **not** use the retired MSOnline `StrongAuthenticationMethods` property. The supported source is the **authentication methods registration report**, which reports per user whether they are MFA-capable and registered.

```powershell
# Requires AuditLog.Read.All (and Policy.Read.All / Reports.Read.All)
$reg = Get-MgReportAuthenticationMethodUserRegistrationDetail -All

$noMfa = $reg | Where-Object { -not $_.IsMfaRegistered } |
    Select-Object UserPrincipalName, UserDisplayName,
                  IsMfaRegistered, IsMfaCapable, IsAdmin

"$($noMfa.Count) users are NOT registered for MFA"
$noMfa | Export-Csv .\users-without-mfa.csv -NoTypeInformation
```

Flagging `IsAdmin` users without MFA first is the right triage order: an unprotected privileged account is the highest risk in the tenant.

## Detecting Stale and Inactive Accounts

Stale accounts are unused attack surface. The authoritative signal is **`signInActivity.lastSignInDateTime`**, which needs `AuditLog.Read.All` and must be requested explicitly.

```powershell
$cutoff = (Get-Date).AddDays(-90)

$stale = Get-MgUser -All -Property "displayName,userPrincipalName,accountEnabled,signInActivity" |
    Select-Object DisplayName, UserPrincipalName, AccountEnabled,
        @{N='LastSignIn'; E={ $_.SignInActivity.LastSignInDateTime }} |
    Where-Object {
        $_.LastSignIn -and [datetime]$_.LastSignIn -lt $cutoff
    }

$stale | Sort-Object LastSignIn |
    Export-Csv .\stale-accounts.csv -NoTypeInformation
```

Accounts that have **never** signed in show a null `LastSignIn`; treat those separately, they are often unused service or test accounts.

## Guests, Risky Users, and Role Assignments

Three more high-value inventories. **Guests** are external identities (`userType eq 'Guest'`). **Risky users** come from Entra ID Protection. **Privileged role assignments** reveal who holds directory roles like Global Administrator.

```powershell
# Guest inventory
Get-MgUser -All -Filter "userType eq 'Guest'" `
    -Property "displayName,userPrincipalName,createdDateTime,externalUserState" |
    Export-Csv .\guest-inventory.csv -NoTypeInformation

# Risky users (needs IdentityRiskyUser.Read.All)
Get-MgRiskyUser -All |
    Where-Object { $_.RiskState -eq 'atRisk' } |
    Select-Object UserPrincipalName, RiskLevel, RiskLastUpdatedDateTime

# Who holds privileged directory roles
Get-MgDirectoryRole -All | ForEach-Object {
    $role = $_
    Get-MgDirectoryRoleMember -DirectoryRoleId $role.Id -All |
        ForEach-Object {
            [pscustomobject]@{ Role = $role.DisplayName; MemberId = $_.Id }
        }
}
```

## Exporting Conditional Access as Evidence

Your **Conditional Access (CA)** policies are the backbone of Zero Trust enforcement. Exporting them gives you both an audit artifact and a baseline for drift detection (we automate redeployment of CA as code in lesson 4).

```powershell
# Needs Policy.Read.All
$ca = Get-MgIdentityConditionalAccessPolicy -All

$ca | Select-Object DisplayName, State,
    @{N='Users';   E={ $_.Conditions.Users.IncludeUsers -join ';' }},
    @{N='Apps';    E={ $_.Conditions.Applications.IncludeApplications -join ';' }},
    @{N='Controls';E={ $_.GrantControls.BuiltInControls -join ';' }} |
    Export-Csv .\ca-policies.csv -NoTypeInformation

# Keep the full JSON as the source-of-truth snapshot
$ca | ConvertTo-Json -Depth 10 | Set-Content .\ca-policies.json
```

## Generating CSV and HTML Reports

CSV is great for diffing and pivot tables; **HTML** is what a manager or auditor actually reads. `ConvertTo-Html` turns any object collection into a styled table you can email.

```powershell
$style = "<style>table{border-collapse:collapse}td,th{border:1px solid #ccc;padding:6px}th{background:#0078d4;color:#fff}</style>"

$noMfa | ConvertTo-Html -Title "Users Without MFA" -PreContent "<h2>Users Without MFA - $(Get-Date -Format yyyy-MM-dd)</h2>" -Head $style |
    Out-File .\mfa-report.html
```

Bundle every finding (no-MFA, stale, guests, risky, roles) into one dated report folder so each run is a self-contained evidence package.

## Scheduling with Azure Automation and a Managed Identity

A report nobody runs is useless. Wrap the script in an **Azure Automation runbook** and let it run nightly. The best-practice credential is the Automation account's **system-assigned managed identity**, no secret to store, rotate, or leak. Assign that identity the read-only Graph application permissions, then connect with one line:

```powershell
# Inside the runbook - no stored credentials
Connect-MgGraph -Identity

# ... run all the audit blocks above ...
# Write outputs to an Azure Storage blob or email them via Graph sendMail

Disconnect-MgGraph
```

Grant the managed identity application permissions with a one-time admin script (assigning app role IDs on the service principal), schedule the runbook, and you have a hands-off compliance report that lands in the same place every morning. Because every scope is read-only, the runbook can audit the tenant but never change it, which is exactly what you want running unattended.
