---
course: helpdesk-tier1-2
title: Microsoft 365 tenant overview
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 1
summary: Understand what a Microsoft 365 tenant actually is, how its admin centers and licensing fit together,
  and where you go to support users as a Tier 2 cloud admin.
objectives:
- Explain what a Microsoft 365 tenant is and how it maps to a single organisation
- Navigate the Microsoft 365 admin center and the specialist admin centers
- Describe how licensing and subscriptions assign capabilities to users
- Identify where domains, DNS, and Microsoft Entra ID fit into a tenant
- Use admin roles to control who can change tenant settings
- Locate the tenant ID and key settings needed to support and audit a tenant
video: hd6-l01-m365-tenant-overview.mp4
quiz:
- q: What is a Microsoft 365 tenant?
  options:
  - A single licensed user account
  - A dedicated, isolated instance of Microsoft 365 services for one organisation
  - A physical server in a Microsoft data centre
  - A backup copy of a mailbox
  answer: 1
  why: A tenant is the dedicated, logically isolated instance of Microsoft 365 (Entra ID, Exchange, Teams,
    SharePoint, etc.) that belongs to one organisation and is identified by a unique tenant ID and default
    *.onmicrosoft.com domain.
- q: Which admin center is the central starting point for managing users, licences, and other admin centers?
  options:
  - The Exchange admin center
  - The Microsoft 365 admin center
  - The Azure portal
  - The Teams admin center
  answer: 1
  why: 'The Microsoft 365 admin center (admin.microsoft.com) is the hub: it manages users, groups, licences,
    and service health, and links out to the specialist admin centers.'
- q: What controls which Microsoft 365 capabilities a specific user can access?
  options:
  - The user's password length
  - The licences (subscription plans) assigned to that user
  - The number of devices they own
  - Their job title in Active Directory
  answer: 1
  why: Capabilities such as Exchange Online, Teams, and Copilot are unlocked per user by the licences
    assigned to them; a user with no licence has no access to those services.
- q: Where are user identities and sign-in stored for a Microsoft 365 tenant?
  options:
  - In Microsoft Entra ID
  - In the Exchange mailbox database
  - In SharePoint document libraries
  - In the local device registry
  answer: 0
  why: Microsoft Entra ID (formerly Azure AD) is the identity and access layer for the tenant; it holds
    user accounts, groups, and the sign-in/authentication that all M365 services rely on.
- q: Name the default domain every new Microsoft 365 tenant receives, and why an organisation usually
    adds a custom one.
  answer: Every tenant gets a default domain in the form yourcompany.onmicrosoft.com; organisations add
    a custom domain (like contoso.com) so user sign-in and email addresses look professional and match
    their brand.
  why: The onmicrosoft.com domain always works as a fallback, but custom domains require verifying DNS
    records and are what users actually sign in and send mail with.
- q: In one sentence, why should you avoid handing out the Global Administrator role to everyone who needs
    to make a change?
  answer: Global Administrator can change anything in the tenant, so granting it widely is a major security
    risk; you should assign the least-privileged role that lets each admin do their specific job.
  why: Least privilege limits blast radius — if a Help Desk admin only needs to reset passwords, give
    them the Helpdesk Administrator role, not full Global Admin.
resources:
- label: Microsoft Learn — Overview of the Microsoft 365 admin center
  url: https://learn.microsoft.com/en-us/microsoft-365/admin/admin-overview/admin-center-overview
- label: Microsoft Learn — Microsoft Entra ID documentation
  url: https://learn.microsoft.com/en-us/entra/fundamentals/whatis
- label: Microsoft Learn — About admin roles in the Microsoft 365 admin center
  url: https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/about-admin-roles
- label: 'Microsoft Learn — MS-102: Microsoft 365 Administrator exam page'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## What a tenant really is

When an organisation buys Microsoft 365, Microsoft creates a **tenant** for them: a dedicated, logically isolated instance of all the cloud services — identity, email, Teams, SharePoint, security tooling — that belongs only to that organisation. Your company's tenant is separate from every other company's, even though they all run on the same Microsoft cloud.

Every tenant has a unique **tenant ID** (a GUID) and a default domain in the form `yourcompany.onmicrosoft.com`. As a Tier 2 admin, the tenant is the boundary you work inside all day.

## The admin centers

You manage the tenant through a set of web portals. The hub is the **Microsoft 365 admin center** at `admin.microsoft.com`, where you handle users, groups, licences, and service health, and from which you jump to the specialist portals.

```text
Microsoft 365 admin center (admin.microsoft.com)
  +-- Exchange admin center        (email)
  +-- Teams admin center           (meetings, calling)
  +-- SharePoint admin center      (sites, OneDrive)
  +-- Microsoft Entra admin center (identity)
  +-- Microsoft Purview            (compliance)
  +-- Microsoft Defender portal    (security)
```

Knowing which portal owns which job is half the battle when a ticket lands.

## Identity and domains

Underneath everything sits **Microsoft Entra ID** (formerly Azure AD). It stores user accounts, groups, and the **authentication** that every service trusts. When a user signs in to Outlook, Teams, or SharePoint, Entra ID is what verifies them.

Most organisations add a **custom domain** like `contoso.com` so that sign-in names and email addresses look professional. Adding a domain means verifying ownership through DNS records — typically a TXT record to prove control, then MX and other records so mail flows.

## Licensing: what unlocks what

A tenant subscribes to one or more **plans** (for example Microsoft 365 Business Premium or E3/E5). Each plan is a bundle of **licences** that unlock specific services. You assign licences **per user** — a user with no Exchange licence has no mailbox; a user with no Copilot licence cannot use Copilot.

When a user reports "I can't get to Teams" your first reflex should be to check their assigned licences in the admin center before you touch anything else.

## Roles and least privilege

Not every admin needs full power. **Admin roles** decide who can change what. The **Global Administrator** role can do everything — which is exactly why you give it to very few people. For day-to-day support, narrower roles like **Helpdesk Administrator** (reset passwords) or **User Administrator** (manage users) follow the principle of **least privilege**: grant the smallest role that does the job.

```text
Admin center > Roles > Role assignments
  - Find the role (e.g. Helpdesk Administrator)
  - Assign the specific user
  - Review assignments regularly
```

## Your task

Sign in to a Microsoft 365 admin center (use a free Microsoft 365 Developer tenant if you don't have one). Find and write down your tenant's default `.onmicrosoft.com` domain and tenant ID, list which specialist admin centers you can reach from the hub, and note which admin role you would assign to a Tier 1 colleague who only needs to reset passwords.
