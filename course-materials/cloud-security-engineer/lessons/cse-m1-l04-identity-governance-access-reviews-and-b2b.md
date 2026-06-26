---
course: cloud-security-engineer
title: 'Identity Governance: Access Reviews, Entitlement Management, and B2B'
month: 1
monthTitle: Zero Trust Identity & Entra ID Governance
lesson: 4
summary: 'PIM governs admin elevation; this lesson governs the whole identity lifecycle for everyone —
  employees, partners, and guests. You''ll learn the Microsoft Entra Identity Governance suite: entitlement
  management with access packages, catalogs, and lifecycle policies that auto-expire access; access reviews
  for groups, apps, and guests; and lifecycle workflows that automate joiner, mover, and leaver events.
  You''ll then secure external collaboration with B2B, cross-tenant access settings, and cross-tenant
  synchronization, and use guest access reviews to stop guest sprawl. Every control ties back to least
  privilege and Zero Trust.'
objectives:
- Describe the Microsoft Entra Identity Governance suite and the problem each component solves
- Design entitlement management with access packages, catalogs, and lifecycle policies that automatically
  expire access
- Configure access reviews for groups, applications, and guest users with sensible recurrence and auto-removal
- Automate joiner/mover/leaver events with lifecycle workflows
- Secure external collaboration using B2B and cross-tenant access settings (inbound/outbound trust)
- Explain cross-tenant synchronization and when to use it instead of guest invitations
- Use guest access reviews to prevent guest sprawl and enforce least privilege
video: cse-m1-l04-identity-governance-access-reviews-and-b2b.mp4
quiz:
- q: What core problem does entitlement management (access packages) solve?
  options:
  - It encrypts files shared with external users
  - It bundles the resources a role needs (groups, apps, SharePoint sites) into a requestable package
    with approval and automatic expiration, so access is governed end-to-end
  - It replaces Conditional Access for guest sign-ins
  - It stores admin passwords in a vault
  answer: 1
  why: An access package bundles related resources (security/M365 groups, enterprise apps, SharePoint
    sites) plus the policy for who can request them, who approves, and when they expire. Users request
    access in one place, approvers grant it, and lifecycle policies auto-expire it — governing the full
    request-to-removal lifecycle instead of manual one-off grants.
- q: In entitlement management, what is the role of a catalog?
  options:
  - It is a list of blocked applications
  - It is a container that groups the resources and access packages for delegated administration, so non-admins
    can own packages for their own apps/groups
  - It is the audit log of all sign-ins
  - It is a Conditional Access policy set
  answer: 1
  why: 'A catalog is a container of resources (groups, apps, sites) and the access packages built from
    them. It enables delegation: a department lead can be made a catalog owner and manage access packages
    for their own resources without being a tenant-wide admin — a least-privilege, self-service governance
    model.'
- q: Which scenario is the best fit for a lifecycle workflow?
  options:
  - Encrypting an email with a sensitivity label
  - Automatically running joiner tasks (enable account, add to groups, send welcome) a set number of days
    before a new hire's start date, and leaver tasks at termination
  - Blocking legacy authentication tenant-wide
  - Activating a PIM role for four hours
  answer: 1
  why: Lifecycle workflows automate joiner/mover/leaver (JML) events based on attributes like employeeHireDate
    and employeeLeaveDateTime — provisioning access before day one and, critically, deprovisioning it
    at departure so access doesn't linger. That automation is the operational backbone of least privilege
    across the user lifecycle.
- q: What do cross-tenant access settings control in B2B collaboration?
  options:
  - The color theme of the guest sign-in page
  - Inbound and outbound trust between your tenant and specific partner tenants — which users/apps are
    allowed, and whether you trust their MFA and device compliance claims
  - The amount of storage guests can use in SharePoint
  - Whether guests can change their own passwords
  answer: 1
  why: Cross-tenant access settings define, per partner tenant (or as a default), which inbound external
    users and outbound internal users may collaborate, which apps are in scope, and whether you trust
    the partner's MFA and device-compliance claims so guests don't have to re-satisfy MFA. This is how
    you make B2B both usable and Zero-Trust-aligned.
- q: When is cross-tenant synchronization (CTS) preferable to standard B2B guest invitations?
  options:
  - Never — CTS and B2B are identical
  - When a multi-tenant organization wants users from one tenant automatically provisioned and kept in
    sync as B2B members in another tenant, instead of inviting and managing them one by one
  - When you want to block all external access
  - When you only need to share a single SharePoint file with one person
  answer: 1
  why: Cross-tenant synchronization automatically creates, updates, and deprovisions B2B users across
    tenants in the same organization, keeping identities in sync without manual invitations. It's ideal
    for mergers or multi-tenant enterprises; one-off external sharing is still better served by a standard
    B2B guest invite.
- q: In three to five sentences, explain how access packages, access reviews, lifecycle workflows, and
    guest access reviews work together to enforce least privilege across the identity lifecycle, and why
    this matters for Zero Trust.
  answer: 'Lifecycle workflows handle the joiner and mover and leaver events automatically, so accounts
    are provisioned just before they''re needed and deprovisioned the moment someone leaves, eliminating
    orphaned access. Access packages govern in-life entitlements: users request bundled resources, approvers
    grant them, and lifecycle policies auto-expire the access so nothing is permanent by default. Access
    reviews periodically force attestation that each remaining group, app, and especially guest assignment
    is still justified, removing anything stale. Guest access reviews specifically curb guest sprawl,
    because external accounts otherwise accumulate silently and become forgotten attack surface. Together
    they keep the set of who-can-access-what minimal and current, which is exactly the least-privilege
    foundation Zero Trust depends on.'
  why: The four controls cover provisioning (lifecycle workflows), in-life entitlement (access packages
    with expiry), periodic recertification (access reviews), and external-account hygiene (guest reviews)
    — a closed loop that continuously drives toward least privilege, the core of Zero Trust identity.
resources:
- label: What is Microsoft Entra ID Governance?
  url: https://learn.microsoft.com/en-us/entra/id-governance/identity-governance-overview
- label: What is entitlement management?
  url: https://learn.microsoft.com/en-us/entra/id-governance/entitlement-management-overview
- label: What are lifecycle workflows?
  url: https://learn.microsoft.com/en-us/entra/id-governance/what-are-lifecycle-workflows
- label: Cross-tenant access overview (B2B)
  url: https://learn.microsoft.com/en-us/entra/external-id/cross-tenant-access-overview
---

## From Admin Elevation to the Whole Lifecycle

Lesson 3 governed *admin elevation* with PIM. But least privilege has to apply to **everyone, all the time** — the new hire on day one, the employee who changes departments, the contractor who finishes a project, and the partner guest who was invited two years ago and never removed. **Microsoft Entra Identity Governance** is the suite that automates this whole lifecycle so access is granted appropriately, reviewed regularly, and removed promptly — without an admin manually babysitting every change.

The suite has four workhorses we'll cover: **entitlement management** (how access is requested and granted), **access reviews** (how access is recertified), **lifecycle workflows** (how joiners/movers/leavers are automated), and **B2B / cross-tenant** controls (how external people collaborate safely). All four serve one goal: keep *who-can-access-what* minimal and current.

## Entitlement Management: Access Packages and Catalogs

Manually adding people to groups and apps doesn't scale and leaves no governance trail. **Entitlement management** fixes this with **access packages**.

- An **access package** bundles everything a role needs: security and Microsoft 365 groups, enterprise applications, and SharePoint sites — plus a **policy** describing *who can request it*, *who approves*, and *how long it lasts*.
- A **catalog** is the container that holds those resources and packages. Catalogs enable **delegation**: a department owner can manage packages for their own resources without being a tenant admin (least privilege for governance itself).
- **Lifecycle policies** on the package set **automatic expiration** — access lapses after N days or on a date unless the user re-requests and is re-approved. Nothing is permanent by default.

The user experience: someone visits the **My Access** portal, requests the *'Finance App — Analyst'* package, the finance owner approves, and the right groups/apps/sites are granted automatically — then auto-removed at expiry. Request, approve, expire: governed end-to-end.

## Access Reviews for Groups, Apps, and Guests

Grants drift. People change roles, projects end, and yesterday's appropriate access becomes today's risk. **Access reviews** force periodic **attestation**:

- Scope a review to a **group**, an **application's** assigned users, a **privileged role** (from Lesson 3), or **guest users**.
- Choose **reviewers**: resource owners, managers, or the users themselves (self-attestation).
- Set **recurrence** (weekly/monthly/quarterly) and an **auto-apply** action: **remove access if denied or not reviewed**, so inaction defaults to least privilege rather than lingering rights.

For sensitive resources, require the reviewer to **provide a justification** and enable **decision helpers** (e.g., flag users who haven't signed in). Reviews are the recertification heartbeat of governance.

## Lifecycle Workflows: Joiner / Mover / Leaver

**Lifecycle workflows (LCW)** automate the **JML** events that historically caused the worst access hygiene problems — especially the **leaver**, where forgotten accounts become standing attack surface.

- **Joiner:** triggered relative to `employeeHireDate` — e.g., *2 days before start*, enable the account, add it to baseline groups, generate a temporary access pass, send a welcome email.
- **Mover:** on attribute change (department/job title) — adjust group memberships and entitlements.
- **Leaver:** triggered relative to `employeeLeaveDateTime` — disable the account, remove from all groups, revoke sessions/tokens, and reassign or remove access.

Workflows are built from configurable **tasks** and run on a schedule, with execution history for audit. Pairing LCW with HR-driven inbound provisioning means a person's access tracks their employment automatically.

## Secure B2B and Cross-Tenant Access Settings

External collaboration is essential and dangerous. **B2B collaboration** lets partners sign in with *their own* identity (no password for you to manage) as a **guest** in your tenant. **Cross-tenant access settings** make that Zero-Trust-aligned by defining trust **per partner tenant** (and a default):

- **Inbound** — which external users/groups and which of *your* apps they can reach.
- **Outbound** — which of *your* users can access *partner* tenants and apps.
- **Trust settings** — whether you **trust the partner's MFA and device-compliance claims**, so a guest who already did phishing-resistant MFA in their home tenant doesn't have to repeat it, and your Conditional Access can require a *compliant device* even for guests.

A hardened default blocks broad external access and explicitly allows named partner tenants and apps — external access by exception, not by default.

## Cross-Tenant Sync and Stopping Guest Sprawl

For organizations that span **multiple tenants** (mergers, multi-national subsidiaries), inviting guests one by one doesn't scale. **Cross-tenant synchronization (CTS)** automatically **provisions, updates, and deprovisions** B2B users from a source tenant into a target tenant and keeps them in sync — users appear and disappear automatically as their home tenant changes. Use CTS for *same-organization* multi-tenant scenarios; use ordinary B2B invitations for *one-off* external partners.

Whatever the mechanism, guests **accumulate silently** — invited for a project, never removed. That **guest sprawl** is forgotten attack surface. Counter it with **guest-focused access reviews**: recurring reviews of all guests (or guests in sensitive groups), with **remove-on-no-response**, plus inactivity decision helpers to catch guests who haven't signed in for months. 

Step back and see the loop: lifecycle workflows provision and deprovision, access packages grant and auto-expire, access reviews recertify, and guest reviews prune external accounts. Together they keep the identity estate minimal and current — the living embodiment of least privilege, and the identity foundation the rest of this course's Zero Trust architecture is built on.
