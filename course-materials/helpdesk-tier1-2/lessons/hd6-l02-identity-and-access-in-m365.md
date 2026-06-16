---
course: helpdesk-tier1-2
title: Identity and access management in Microsoft 365
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 2
summary: Microsoft Entra ID is the identity layer behind every Microsoft 365 sign-in. In this lesson you
  create and manage users and groups, license through groups, and protect accounts with MFA, Conditional
  Access, and self-service password reset.
objectives:
- Describe Microsoft Entra ID as the identity layer for Microsoft 365
- Tell the difference between cloud-only and synced (hybrid) identities via Entra Connect
- Create and manage users and choose between security and Microsoft 365 groups
- Assign licences efficiently with group-based licensing
- Enable multi-factor authentication and build a basic Conditional Access policy
- 'Resolve common Tier 2 tasks: password resets, account lockouts, and self-service password reset'
video: hd6-l02-identity-and-access-in-m365.mp4
quiz:
- q: What is Microsoft Entra ID in a Microsoft 365 tenant?
  options:
  - The email storage service
  - The cloud identity and access management service
  - A file-sharing platform
  - The Windows desktop login only
  answer: 1
  why: Entra ID (formerly Azure AD) is the cloud identity layer that authenticates users and controls
    access to Microsoft 365 and other apps.
- q: Which group type can be used to assign Microsoft 365 licences and grant access to resources?
  options:
  - Security group
  - Distribution list only
  - Mail-enabled contact
  - Shared mailbox
  answer: 0
  why: Security groups (and Microsoft 365 groups) support group-based licensing and resource access; distribution
    lists are for email only.
- q: In a Conditional Access policy, what are 'signals'?
  options:
  - The licences a user owns
  - The mailbox size
  - Conditions like user, device, location, and risk that the policy evaluates
  - Backup schedules
  answer: 2
  why: Conditional Access evaluates signals (who, what device, where, how risky) and then makes a decision
    such as require MFA or block.
- q: What does a synced (hybrid) identity rely on to copy on-premises accounts to the cloud?
  options:
  - Microsoft Entra Connect
  - Exchange Online only
  - SharePoint sync
  - OneDrive Files On-Demand
  answer: 0
  why: Entra Connect synchronises on-premises Active Directory objects into Entra ID, creating hybrid
    identities.
- q: A user is locked out after too many failed sign-ins and cannot reach you. How could self-service
    password reset help, and what must be in place first?
  answer: Self-service password reset (SSPR) lets the user reset or unlock their own account using registered
    authentication methods (such as phone or the Authenticator app). SSPR must be enabled for their group
    and the user must have registered methods beforehand.
  why: SSPR cuts password-reset tickets, but it only works if it is enabled and the user has pre-registered
    verification methods.
- q: Briefly, why is assigning licences to a group better than assigning them one user at a time?
  answer: Group-based licensing assigns the licence to a security group, so every member automatically
    gets it and loses it when they leave the group. It scales, reduces manual errors, and keeps licensing
    consistent.
  why: Manual per-user assignment does not scale and is easy to forget; group-based licensing automates
    joiner and leaver changes.
resources:
- label: Microsoft Learn — What is Microsoft Entra ID?
  url: https://learn.microsoft.com/en-us/entra/fundamentals/whatis
- label: Microsoft Learn — Add or delete users in Microsoft Entra ID
  url: https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users
- label: Microsoft Learn — What is Conditional Access?
  url: https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
- label: 'Microsoft Learn — Exam MS-102: Microsoft 365 Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## Entra ID: the identity layer behind Microsoft 365

Every time someone signs in to Outlook, Teams, or SharePoint, they authenticate against **Microsoft Entra ID** (formerly Azure Active Directory). Entra ID is the **identity and access management** service for the whole tenant. It stores users and groups, checks passwords and other factors, and decides what each person is allowed to reach. As a Tier 2 admin, most of your access tickets begin and end here.

You manage it from two main places: the **Microsoft 365 admin center** for everyday user and licence work, and the **Microsoft Entra admin center** (entra.microsoft.com) for deeper identity controls like Conditional Access.

## Cloud-only vs synced (hybrid) identities

There are two kinds of accounts. A **cloud-only identity** is created and lives entirely in Entra ID. A **synced (hybrid) identity** starts in an on-premises **Active Directory** and is copied up to the cloud by **Microsoft Entra Connect**.

The practical difference matters at the helpdesk: for a synced user, you usually edit the account (name, password, group membership) in on-premises AD, and the change flows up. For a cloud-only user, you edit it directly in the cloud. Always check which type you are dealing with before making changes.

## Users and groups

You create users in the admin center, or with **Microsoft Graph PowerShell**.

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All"
Get-MgUser -UserId "ada@contoso.com"
New-MgUser -DisplayName "Ada Lovelace" -UserPrincipalName "ada@contoso.com" -MailNickname "ada" -AccountEnabled -PasswordProfile @{ Password = "TempP@ssw0rd!"; ForceChangePasswordNextSignIn = $true }
```

Groups come in two flavours you must not confuse. A **security group** controls access to resources and supports licensing. A **Microsoft 365 group** adds shared collaboration: a mailbox, calendar, and Teams/SharePoint space. Use security groups for access and licensing; use Microsoft 365 groups for teams that collaborate.

## Licensing through groups

Assigning licences one user at a time does not scale. Instead use **group-based licensing**: assign the licence to a security group, and every member inherits it automatically.

```text
Microsoft 365 admin center > Billing > Licenses
  -> or Entra admin center > Groups > [group] > Licenses > Assignments
```

When someone joins the group they get the licence; when they leave, it is removed. Joiner and leaver changes become almost automatic.

## MFA and Conditional Access

A password alone is weak. **Multi-factor authentication (MFA)** adds a second factor — typically the **Microsoft Authenticator** app — so a stolen password is not enough.

The modern way to enforce it is **Conditional Access**. A policy reads **signals** (which user, which device, which location, how risky the sign-in) and then makes a **decision**: require MFA, require a compliant device, or block.

```text
Entra admin center > Protection > Conditional Access > Policies > New policy
  Assignments: Users/groups + target apps
  Conditions: locations, device platforms, sign-in risk
  Grant: Require multi-factor authentication
```

Start policies in **report-only** mode so you can see the impact before turning them on.

## Self-service password reset

**Self-service password reset (SSPR)** lets users reset or unlock their own accounts using registered methods like phone or the Authenticator app. Enable it for a group, make users register, and your password-reset ticket volume drops sharply. When SSPR is not available, resets and **account lockouts** are still classic Tier 2 jobs you handle directly in the admin center.

## Your task

In a test or trial tenant, create one cloud-only user, add them to a security group, assign a licence to that group, and build a report-only Conditional Access policy that requires MFA for that group.
