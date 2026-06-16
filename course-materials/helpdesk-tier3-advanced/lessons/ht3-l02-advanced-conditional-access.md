---
course: helpdesk-tier3-advanced
title: Advanced Conditional Access and risk-based policies
month: 3
monthTitle: Advanced Endpoint Security & Identity
lesson: 2
summary: Design layered Conditional Access policies that combine identity, device and risk signals, then
  enforce them with authentication strengths, session controls and Identity Protection risk-based policies.
  You will roll changes out safely with report-only mode and protect break-glass accounts from lockout.
objectives:
- Break a Conditional Access policy into its assignments and access controls and explain what each lever
  does
- Design a layered set of policies rather than one monolithic rule, and reason about policy intersection
- Distinguish sign-in risk from user risk and map each to the correct Identity Protection policy
- Require phishing-resistant authentication using authentication strengths instead of the legacy MFA toggle
- Apply session controls — sign-in frequency, persistent browser, app-enforced restrictions and CAE
- Roll policies out safely with report-only mode and exclude break-glass emergency access accounts
video: ht3-l02-advanced-conditional-access.mp4
quiz:
- q: A Conditional Access policy is structured as assignments and access controls. Which item is an ASSIGNMENT
    rather than an access control?
  options:
  - Target resources (cloud apps or actions)
  - Require multifactor authentication
  - Require device to be marked as compliant
  - Require app protection policy
  answer: 0
  why: Assignments define WHO and WHAT a policy targets — users/groups, target resources, and conditions.
    Grant requirements like MFA, compliant device or app protection policy are access controls that fire
    once the assignment matches.
- q: What is the key difference between sign-in risk and user risk in Microsoft Entra Identity Protection?
  options:
  - Sign-in risk is about the account being compromised over time; user risk is about a single authentication
  - Sign-in risk reflects the probability that a specific authentication is not the legitimate owner;
    user risk reflects the probability the account itself is compromised
  - They are identical and used interchangeably
  - User risk only applies to guest accounts
  answer: 1
  why: Sign-in risk is real-time and per-authentication (impossible travel, anonymous IP, unfamiliar properties),
    so the right remediation is MFA. User risk is a cumulative judgement that the identity is compromised
    (leaked credentials, confirmed-compromise patterns), so the right remediation is a secure password
    change.
- q: You want to require phishing-resistant authentication for admins. What is the correct modern mechanism?
  options:
  - The legacy 'Require multifactor authentication' grant control
  - Blocking legacy authentication only
  - An authentication strength that allows only phishing-resistant methods (FIDO2, Windows Hello for Business,
    certificate-based)
  - Enabling the per-user MFA toggle in the legacy portal
  answer: 2
  why: Authentication strengths let you require a specific set of methods. The built-in phishing-resistant
    strength permits only FIDO2 security keys, Windows Hello for Business and certificate-based authentication
    — stronger and more precise than the generic MFA grant.
- q: Which session control causes the browser session to be re-evaluated and revoked in near real time
    when critical events occur, rather than waiting for token expiry?
  options:
  - Persistent browser session
  - Sign-in frequency
  - Continuous access evaluation (CAE)
  - App-enforced restrictions
  answer: 2
  why: Continuous access evaluation lets resource providers honour near-real-time revocation events (account
    disable, password reset, elevated risk). Sign-in frequency forces periodic reauthentication but is
    not real-time; persistent browser and app-enforced restrictions serve different purposes.
- q: Explain why break-glass (emergency access) accounts must be excluded from Conditional Access policies,
    and one safeguard you apply instead.
  answer: A misconfigured or dependency-broken policy (for example one requiring a compliant device, a
    specific MFA provider, or a location you cannot reach) can lock every admin out of the tenant. Two
    cloud-only break-glass accounts excluded from all policies guarantee you can still sign in to fix
    it. Safeguards include long random passphrases, phishing-resistant MFA where possible, tight sign-in
    alerting/monitoring, and periodic credential testing.
  why: Excluding break-glass accounts prevents a single bad policy or a downed MFA/identity dependency
    from permanently locking administrators out, while monitoring and strong credentials limit the risk
    those highly privileged exclusions create.
- q: In one or two sentences, describe how report-only mode supports a safe Conditional Access rollout
    and what you inspect before enabling.
  answer: Report-only mode evaluates the policy against real sign-ins and records what WOULD have happened
    without actually enforcing grant or block, so you can detect unintended impact. You inspect the sign-in
    logs and the Conditional Access Insights workbook to see which users, apps and sessions would have
    been affected, confirm break-glass accounts are excluded, then flip to On.
  why: Report-only surfaces the real-world blast radius — including surprises like service accounts or
    legacy clients — before enforcement, which is the safest way to avoid mass lockouts when a new policy
    goes live.
resources:
- label: Microsoft Learn — What is Conditional Access?
  url: https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
- label: Microsoft Learn — Risk-based access policies (Identity Protection)
  url: https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-policies
- label: Microsoft Learn — Conditional Access authentication strength
  url: https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-strengths
- label: Microsoft Learn — Manage emergency access (break-glass) accounts
  url: https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access
---

## Anatomy of a Conditional Access policy

Every Conditional Access policy is an if-then statement: **if** these assignments match, **then** apply these access controls. Master the anatomy and the rest follows.

- **Assignments** define the scope. They are **users** (or workload identities), **target resources** (cloud apps, user actions like registering security info, or authentication context), and **conditions** (sign-in risk, user risk, device platform, locations, client apps, device filters).
- **Access controls** define the outcome. **Grant** controls either block or grant with requirements such as **require MFA**, **require compliant device**, **require Intune-managed or hybrid-joined device**, **require app protection policy**, or **require authentication strength**. **Session** controls shape the resulting session.

A policy with no matching assignment never fires. A policy that matches always applies its controls — and **multiple matching policies combine**: all grant requirements are ANDed together, and any single block wins.

## Design layered, not monolithic

Resist the urge to cram everything into one rule. Build small, single-purpose policies so intersection is predictable and troubleshooting is sane:

```text
CA001  Block legacy authentication            (all users)
CA002  Require phishing-resistant MFA          (admin roles)
CA003  Require compliant device                (all users, M365 apps)
CA004  Require MFA on sign-in risk = medium+   (all users)
CA005  Require password change on user risk    (all users)
CA006  Sign-in frequency 12h + no persistence  (unmanaged devices)
CA000  EXCLUDE break-glass accounts            (every policy)
```

Each policy does one thing. Together they form a defence-in-depth mesh where the grant requirements stack.

## Sign-in risk versus user risk

**Identity Protection** produces two distinct risk signals and they need different remediation.

- **Sign-in risk** is the probability that a *single authentication* is not the legitimate owner — impossible travel, anonymous IP, unfamiliar properties. Remediate in real time by **requiring MFA**.
- **User risk** is the cumulative probability that the *account itself* is compromised — leaked credentials, confirmed-compromise patterns. Remediate by **requiring a secure password change** (self-service password reset with MFA), which also dismisses the risk.

You wire these in as conditions on Conditional Access grant controls:

```json
{
  "conditions": { "signInRiskLevels": ["high", "medium"] },
  "grantControls": {
    "operator": "OR",
    "builtInControls": ["mfa"]
  }
}
```

## Strengths, session controls and locations

Drop the legacy MFA toggle for privileged access. An **authentication strength** lets you demand specific methods; the built-in **phishing-resistant** strength permits only **FIDO2**, **Windows Hello for Business** and **certificate-based** authentication.

**Session controls** govern the session after grant: **sign-in frequency** forces periodic reauthentication; **persistent browser** controls staying signed in; **app-enforced restrictions** let Office and SharePoint limit downloads on unmanaged devices; and **continuous access evaluation (CAE)** revokes sessions in near real time on critical events. **Named locations** and **device filters** sharpen conditions — for example, treating a trusted country differently or excluding a kiosk by its device attributes.

Find risky sign-ins to validate your risk policies:

```kql
SigninLogs
| where TimeGenerated > ago(7d)
| where RiskLevelDuringSignIn in ("high", "medium")
| project TimeGenerated, UserPrincipalName, AppDisplayName,
          RiskLevelDuringSignIn, ConditionalAccessStatus, IPAddress
| order by TimeGenerated desc
```

## Roll out safely and avoid lockout

Never flip a new policy straight to On. Set it to **report-only**, let it observe real sign-ins, and read the **Conditional Access Insights** workbook and sign-in logs to see who *would* have been blocked. Surprises — service accounts, legacy clients, a forgotten region — show up here, not in a flood of help-desk tickets.

The non-negotiable safeguard: maintain two cloud-only **break-glass** accounts **excluded from every policy**, with long random passphrases, monitored sign-in alerts, and periodic testing. A policy that requires a compliant device or a downed MFA provider can otherwise lock out every admin — break-glass is your way back in.

## Your task

In a test tenant, design and document a layered set of at least five Conditional Access policies covering: block legacy auth, phishing-resistant strength for admins, compliant-device requirement, a sign-in-risk MFA policy and a user-risk password-change policy. Create each in **report-only** mode, confirm both break-glass accounts are excluded from all of them, run the Insights workbook for 48 hours, and write up the would-be impact (affected users, apps, sessions) plus any misconfiguration you caught before enabling enforcement.
