---
course: helpdesk-tier1-2
title: Microsoft 365 troubleshooting and service health
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 7
summary: Learn a structured way to triage Microsoft 365 problems — is it one user, many users, or a Microsoft
  outage? — using the Service health dashboard, Message center, connectivity tests, and the Support and
  Recovery Assistant before you escalate.
objectives:
- 'Apply a scoping methodology: one user, many users, or a service-wide outage'
- Use the Service health dashboard and Message center to rule out a Microsoft-side incident before troubleshooting
  locally
- Run the Microsoft 365 connectivity test and admin diagnostics to confirm where a problem lives
- Use the Support and Recovery Assistant (SARA) for common Outlook and Office issues
- Check licences, MFA, and Conditional Access as common root causes
- Open a Microsoft support request with the right detail and document the escalation cleanly
video: hd6-l07-m365-troubleshooting-and-service-health.mp4
quiz:
- q: A user reports they cannot send mail in Outlook. Following a structured cloud troubleshooting method,
    what should you check FIRST?
  options:
  - Reinstall Office on the user's machine
  - Whether the problem affects only this user, many users, or is a Microsoft-side outage
  - Reset the user's password immediately
  - Open a Microsoft support request straight away
  answer: 1
  why: 'Scoping is the first move: confirm whether it is one user, many users, or a service outage. That
    single question tells you whether to look at the user, the tenant, or Microsoft''s own status before
    you waste hours.'
- q: Where in the Microsoft 365 admin center do you confirm whether Microsoft is currently reporting an
    active incident affecting your services?
  options:
  - Billing > Your products
  - Settings > Org settings
  - Health > Service health
  - Users > Active users
  answer: 2
  why: Health > Service health lists active incidents and advisories Microsoft has acknowledged. Checking
    it early prevents you from troubleshooting a problem that Microsoft is already fixing.
- q: What is the Message center primarily used for?
  options:
  - Reading planned changes, new features, and required actions from Microsoft
  - Resetting user passwords in bulk
  - Viewing real-time mail flow queues
  - Configuring Conditional Access policies
  answer: 0
  why: The Message center is Microsoft's communication channel for upcoming changes, new and retiring
    features, and actions you must take — distinct from Service health, which reports live incidents.
- q: Several users in one department suddenly cannot access SharePoint, but Service health is all green.
    What is the most likely category of root cause to investigate?
  options:
  - A global Microsoft datacentre failure
  - A configuration issue such as licensing, a group, or a Conditional Access policy scoped to that department
  - A faulty network cable at Microsoft
  - Expired root certificates on Microsoft's servers
  answer: 1
  why: When Microsoft reports healthy but a defined subset of users is affected, the cause is almost always
    local scoping — a licence, group membership, or a Conditional Access policy targeting that population.
- q: Name the Microsoft tool you would download and run to automatically diagnose and often fix common
    Outlook and Office sign-in or activation problems on a user's device.
  answer: The Support and Recovery Assistant (SARA).
  why: SARA runs guided automated diagnostics on the client for Outlook, Office activation, and Microsoft
    365 sign-in issues, and either fixes the problem or collects logs to attach to a support case.
- q: In one or two sentences, list what you should include when opening a Microsoft support request for
    a service issue.
  answer: A clear description of the impact, the scope (how many users and which ones), exact error messages,
    timestamps and time zone, affected service and region, steps already tried, and any diagnostic logs
    or connectivity test results.
  why: A well-scoped request with errors, timestamps, scope, and diagnostics lets Microsoft engineers
    reproduce and triage immediately instead of bouncing the ticket back for more information.
resources:
- label: Microsoft Learn — How to check Microsoft 365 service health
  url: https://learn.microsoft.com/en-us/microsoft-365/enterprise/view-service-health
- label: Microsoft Learn — Message center in the Microsoft 365 admin center
  url: https://learn.microsoft.com/en-us/microsoft-365/admin/manage/message-center
- label: Microsoft Learn — About the Microsoft Support and Recovery Assistant
  url: https://learn.microsoft.com/en-us/microsoft-365/troubleshoot/administration/microsoft-support-and-recovery-assistant
- label: 'Microsoft Learn — Exam MS-102: Microsoft 365 Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## Start by scoping the problem

The biggest time-waster in cloud support is fixing the wrong layer. Before you touch anything, answer one question: **is this one user, many users, or a service outage?** That single decision changes everything you do next.

- **One user** → look at *that* user: licence, mailbox, MFA registration, device, client.
- **Many users / a whole department** → look at *configuration*: a group, a policy, a **Conditional Access** rule, a licence pool.
- **Everyone, suddenly** → suspect a **Microsoft-side incident** before you suspect yourself.

Write the scope down at the top of your ticket. It is the most important line you will record.

## Rule out Microsoft first: Service health and Message center

If the scope smells like "everyone", check Microsoft's own status before you debug for hours.

```text
Microsoft 365 admin center (admin.microsoft.com)
  > Health > Service health   (active incidents & advisories)
  > Health > Message center   (planned changes & required actions)
```

**Service health** lists incidents Microsoft has acknowledged, the affected services, and an estimated time to resolution. If your symptom matches an active incident, your job switches from *fixing* to *communicating* — post status, link the incident ID, and wait. The **Message center** is different: it announces upcoming changes, new and retiring features, and actions you must take. A change announced there last week often explains "it stopped working" today.

## Confirm where the problem lives: client vs service

When Service health is green, the problem is on your side — but is it the **client** or the **service**? Test from a second device or a browser session. If Outlook on the web works but the desktop client fails, it is a **client** problem. Use the connectivity test and basic checks:

```powershell
# Reachability and DNS sanity from the user's machine
Test-Connection outlook.office365.com -Count 4
Resolve-DnsName outlook.office365.com
```

The **Microsoft 365 connectivity test** (connectivity.office.com) and the admin center's diagnostics run guided checks and surface known issues automatically.

## Check the usual cloud root causes

Most "can't access" tickets come down to a handful of causes. Verify them directly rather than guessing:

```powershell
# Verify the user's licence assignment and account state
Get-MgUser -UserId user@contoso.com -Property AssignedLicenses,AccountEnabled

# Verify mailbox exists and type is correct
Get-Mailbox user@contoso.com | Format-List Name,RecipientTypeDetails,LitigationHoldEnabled
```

The big three: a **missing or wrong licence**, an **MFA** registration problem, and a **Conditional Access** policy blocking the sign-in (check the Entra sign-in logs for the failure reason). These explain far more outages than broken software does.

## Use SARA for client-side Office issues

For Outlook, Office activation, and Microsoft 365 sign-in problems on a device, download and run the **Support and Recovery Assistant (SARA)**. It runs automated diagnostics, fixes many issues on the spot, and when it cannot, it collects logs you can attach to a support case — saving a round-trip with Microsoft.

## Escalate cleanly when it is genuinely Microsoft's

If you have confirmed it is a service issue and there is no published incident, open a support request from **Help & support** in the admin center. Include: impact, **scope** (who and how many), exact error text, **timestamps with time zone**, the affected service and region, what you have already tried, and diagnostic or connectivity-test output. Document the same in your ticket so the next tech is not starting from zero.

## Your task

Take a real or sample ticket and write out its troubleshooting trail: state the scope (one user / many / outage), record the Service health result, note client-vs-service, list the three root-cause checks you ran, and draft the support-request summary you would send Microsoft.
