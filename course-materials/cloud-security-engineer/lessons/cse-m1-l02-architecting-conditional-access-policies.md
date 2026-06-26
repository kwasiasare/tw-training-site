---
course: cloud-security-engineer
title: Architecting Conditional Access Policies
month: 1
monthTitle: Zero Trust Identity & Entra ID Governance
lesson: 2
summary: 'Conditional Access is the Zero Trust policy engine for identity — the place where signals become
  real-time allow, block, or limit decisions. This lesson breaks a policy into its parts: assignments
  (who and what), conditions/signals (risk, device, location, app), grant controls (require MFA, compliant
  device, phishing-resistant MFA), and session controls (sign-in frequency, app-enforced restrictions).
  You''ll learn the safe-rollout discipline of report-only mode, why every tenant needs excluded break-glass
  accounts, and how to assemble a layered baseline. The lesson includes a realistic policy expressed as
  Microsoft Graph JSON.'
objectives:
- Describe Conditional Access as the policy decision point that enforces Zero Trust 'verify explicitly'
- Decompose a policy into assignments, conditions, grant controls, and session controls
- Select the correct signals — sign-in risk, user risk, device compliance, location, client app — for
  a given scenario
- Choose appropriate grant controls including require MFA, require compliant device, and require phishing-resistant
  MFA
- Apply report-only mode and a phased rollout to deploy policies without locking users out
- Design break-glass emergency accounts and exclude them from blocking policies
- Assemble a layered Conditional Access baseline expressed as Microsoft Graph JSON
video: cse-m1-l02-architecting-conditional-access-policies.mp4
quiz:
- q: In Zero Trust terms, what role does Conditional Access play?
  options:
  - It is the data classification engine for files and email
  - It is the policy decision point that evaluates signals and enforces access decisions in real time
  - It is the endpoint EDR sensor that detects malware
  - It is the SIEM that stores and queries long-term logs
  answer: 1
  why: 'Conditional Access is the identity policy engine: at sign-in it gathers signals (user, risk, device,
    location, app) and outputs a decision — allow, block, or allow-with-controls. That real-time enforcement
    is exactly ''verify explicitly''. Classification is Purview, EDR is Defender for Endpoint, and the
    SIEM is Sentinel.'
- q: A Conditional Access policy is built from assignments and access controls. Which option lists the
    assignment (the 'if') components correctly?
  options:
  - Users/groups, target resources (apps/actions), and conditions (risk, device, location, client app)
  - Sensitivity labels, retention policies, and DLP rules
  - Antivirus signatures, firewall rules, and IP allow-lists only
  - Mailbox permissions, license SKUs, and group memberships only
  answer: 0
  why: 'Assignments define WHO and WHAT a policy applies to: users and groups (with exclusions), target
    resources such as cloud apps or user actions, and conditions like sign-in risk, user risk, device
    platform/state, locations, and client apps. The access controls (grant and session) then define the
    THEN.'
- q: Which grant control gives the strongest protection against real-time phishing and adversary-in-the-middle
    token theft?
  options:
  - Require multifactor authentication using SMS text messages
  - Require a password change every 30 days
  - Require phishing-resistant MFA (FIDO2 security key, passkey, or Windows Hello for Business)
  - Require security questions in addition to a password
  answer: 2
  why: Phishing-resistant MFA — FIDO2/passkeys, Windows Hello for Business, or certificate-based authentication
    — binds the credential to the legitimate site and device, defeating adversary-in-the-middle proxies
    that can relay SMS or push approvals. SMS and security questions are phishable; password rotation
    does nothing against token theft.
- q: Why should you deploy a new blocking Conditional Access policy in report-only mode first?
  options:
  - Report-only mode encrypts the sign-in logs
  - Report-only evaluates the policy and logs what WOULD happen without enforcing it, so you can find
    impact before locking users out
  - Report-only mode automatically excludes all guests
  - It is required before you can assign any users
  answer: 1
  why: Report-only mode runs the policy logic against real sign-ins and records the result (would grant
    / would block / would require control) in the sign-in logs and the What If tool, without affecting
    users. This lets you validate scope and catch unintended impact — like blocking a service account
    — before turning the policy On.
- q: What is the purpose of break-glass (emergency access) accounts, and how should they relate to Conditional
    Access?
  options:
  - They are everyday admin accounts that should be in every MFA policy
  - They are highly-protected, monitored emergency accounts that are EXCLUDED from blocking CA policies
    so a misconfigured policy or MFA outage can't lock everyone out
  - They are guest accounts used for vendor access
  - They are disabled accounts kept for auditing only
  answer: 1
  why: Break-glass accounts are a small number of cloud-only, highly-protected accounts excluded from
    policies that could otherwise cause a tenant-wide lockout (for example if an MFA provider fails or
    a CA policy is misconfigured). They use long, unique credentials, are tightly monitored with alerts
    on every sign-in, and are used only in emergencies.
- q: In three to five sentences, design a minimal but layered Conditional Access baseline for a mid-sized
    tenant and explain what each layer enforces and why the order/exclusions matter.
  answer: Layer one blocks legacy authentication protocols for all users, because legacy auth cannot do
    MFA and is the most common path for password-spray attacks. Layer two requires MFA (ideally phishing-resistant)
    for all users accessing all cloud apps, establishing the 'verify explicitly' baseline. Layer three
    requires a compliant or hybrid-joined device for sensitive or admin applications, tying access to
    endpoint health from Intune. Layer four uses Identity Protection signals so that high sign-in risk
    is blocked and high user risk forces a secure password change. Across all of these, a small set of
    break-glass accounts is excluded so a misconfiguration or MFA outage cannot lock administrators out
    of the tenant.
  why: A good baseline layers controls from broad hygiene (block legacy auth, require MFA) to targeted
    hardening (compliant device for sensitive apps) to adaptive risk response (Identity Protection), always
    with break-glass exclusions to preserve recoverability.
resources:
- label: What is Conditional Access?
  url: https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
- label: Conditional Access policy components
  url: https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-policies
- label: Manage emergency access (break-glass) accounts
  url: https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access
- label: Plan a Conditional Access deployment
  url: https://learn.microsoft.com/en-us/entra/identity/conditional-access/plan-conditional-access
---

## Conditional Access Is the Policy Engine

In Lesson 1 we said Zero Trust has a central policy engine that turns signals into decisions. In Microsoft Entra ID, that engine is **Conditional Access (CA)**. Think of it as an `if-then` statement evaluated on **every sign-in**: *IF* a particular user, accessing a particular resource, under particular conditions (risk, device, location, app), *THEN* allow, block, or allow only with extra controls.

CA is where 'verify explicitly' becomes real. It does not replace authentication — it sits *after* the first factor and decides what else is required before a token is issued. Because tokens gate access to every Microsoft 365 and integrated app, CA is the single most important identity control you will design. Get it right and a stolen password is nearly useless; get it wrong and you either lock out your company or leave the door open.

## Anatomy of a Policy: Assignments vs. Access Controls

Every CA policy has two halves.

**Assignments (the IF):**
- **Users and groups** — who the policy targets, with **exclusions** (this is where break-glass accounts go).
- **Target resources** — cloud apps, user actions (e.g., *register security info*), or authentication context.
- **Conditions / signals** — the contextual inputs: sign-in risk, user risk, device platforms, device state (compliant/hybrid-joined), locations, and client apps (browser, mobile/desktop, legacy).

**Access controls (the THEN):**
- **Grant controls** — block access, or grant *only if* controls are met: require MFA, require **phishing-resistant** MFA, require a **compliant device**, require hybrid-joined device, require approved client app, require app protection policy. Combine with *require all* or *require one*.
- **Session controls** — shape the session even after access is granted: **sign-in frequency**, **persistent browser**, **app-enforced restrictions** (e.g., limited web-only access to Exchange/SharePoint), and Conditional Access App Control via Defender for Cloud Apps.

## The Signals That Drive Decisions

CA is only as smart as the signals it can read. The key ones:

- **User/group membership** — the baseline scope.
- **Sign-in risk** (from Microsoft Entra **Identity Protection**) — the probability *this specific sign-in* is not the legitimate user (impossible travel, anonymous IP, malware-linked IP).
- **User risk** (also Identity Protection) — the probability the *account itself* is compromised (leaked credentials found, atypical behavior over time).
- **Device compliance / state** — comes from **Microsoft Intune**: is the device enrolled, compliant with policy (encryption, OS version, defender healthy), or hybrid-joined? This is the bridge between the identity and endpoint pillars.
- **Location** — named locations / trusted IPs or country-based conditions.
- **Client app** — modern auth browser/desktop vs. **legacy authentication** (POP, IMAP, SMTP, older Office). Legacy auth can't do MFA and should be blocked outright.

## A Realistic Policy as Graph JSON

CA policies are objects you can read and deploy via Microsoft Graph. Below is a policy that **requires phishing-resistant MFA for all users on all apps**, in **report-only** mode, excluding break-glass accounts. Note `grantControls.authenticationStrength` referencing the built-in phishing-resistant strength.

```json
{
  "displayName": "CA001 - Require phishing-resistant MFA for all users",
  "state": "enabledForReportingButNotEnforced",
  "conditions": {
    "users": {
      "includeUsers": ["All"],
      "excludeUsers": [
        "<break-glass-1-objectId>",
        "<break-glass-2-objectId>"
      ]
    },
    "applications": {
      "includeApplications": ["All"]
    },
    "clientAppTypes": ["all"]
  },
  "grantControls": {
    "operator": "AND",
    "authenticationStrength": {
      "id": "00000000-0000-0000-0000-000000000004"
    }
  }
}
```

A second policy blocks **legacy authentication**, which cannot satisfy MFA at all:

```json
{
  "displayName": "CA002 - Block legacy authentication",
  "state": "enabledForReportingButNotEnforced",
  "conditions": {
    "users": { "includeUsers": ["All"], "excludeUsers": ["<break-glass-1-objectId>"] },
    "applications": { "includeApplications": ["All"] },
    "clientAppTypes": ["exchangeActiveSync", "other"]
  },
  "grantControls": { "operator": "OR", "builtInControls": ["block"] }
}
```

Deploy and inspect policies with Graph PowerShell, for example `Get-MgIdentityConditionalAccessPolicy` and `New-MgIdentityConditionalAccessPolicy -BodyParameter $json`.

## Safe Rollout: Report-Only, What If, and Phasing

Never flip a tenant-wide blocking policy straight to **On**. The discipline:

1. **Report-only mode** (`enabledForReportingButNotEnforced`) — the policy is evaluated on real sign-ins and the result is logged (would-grant / would-block / would-require-control) **without** affecting users. Watch the sign-in logs and the report-only workbook for days.
2. **What If tool** — simulate a specific user, app, and conditions to see which policies apply and why.
3. **Phased enforcement** — pilot on a small group, then ring out to the org; keep exclusion groups for users who need temporary relief.
4. **Monitor after enabling** — confirm no spike in failures or help-desk tickets before declaring success.

This is the difference between an architect and someone who locks out the CEO on a Friday afternoon.

## Break-Glass Accounts and the Layered Baseline

**Break-glass (emergency access) accounts** are your insurance against a CA mistake or an MFA-provider outage locking everyone out. Best practice: at least **two** cloud-only accounts (`*.onmicrosoft.com`), Global Administrator, with **long unique passphrases** stored offline, **excluded** from blocking CA policies, and wired to **alerts on every sign-in** so any real use is noticed immediately.

With that safety net, layer the baseline from broad hygiene to adaptive response:

1. **Block legacy authentication** (CA002 above) — kills the easiest password-spray path.
2. **Require MFA / phishing-resistant MFA for all users** (CA001) — the core 'verify explicitly' control.
3. **Require a compliant or hybrid-joined device for sensitive/admin apps** — ties access to Intune endpoint health.
4. **Identity Protection risk policies** — **high sign-in risk → block**; **high user risk → require secure password change** (self-remediation via MFA).

Each layer maps to a Zero Trust principle, and every layer carries the same break-glass exclusion. That is a defensible, portfolio-grade Conditional Access architecture.
