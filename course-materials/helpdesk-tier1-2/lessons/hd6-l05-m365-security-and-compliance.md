---
course: helpdesk-tier1-2
title: Microsoft 365 security and compliance basics
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 5
summary: 'Learn how security and compliance work in Microsoft 365: read and act on Secure Score, navigate
  Microsoft Purview, and understand DLP, sensitivity and retention labels, audit search, and eDiscovery
  as a Tier 2 tech.'
objectives:
- Explain the shared-responsibility model and why M365 security and compliance matter
- Read Microsoft Secure Score and act on a recommended improvement action
- Describe what Microsoft Purview is and the role of a DLP policy
- Tell the difference between sensitivity labels and retention labels/policies
- Run an audit log search to find who did what, and explain eDiscovery at a high level
- Recognise GDPR and other compliance frameworks at an awareness level
video: hd6-l05-m365-security-and-compliance.mp4
quiz:
- q: Under the shared-responsibility model for Microsoft 365 (SaaS), who is responsible for the data,
    accounts, and identities in the tenant?
  options:
  - The customer, while Microsoft secures the underlying platform
  - Microsoft handles everything, including your data
  - Only the internet service provider
  - Nobody — SaaS removes the need for security
  answer: 0
  why: In SaaS, Microsoft secures the physical datacentre and platform, but the customer always owns and
    must protect their own data, identities, and access — that's the part a helpdesk supports.
- q: What does Microsoft Secure Score give you?
  options:
  - A list of users who failed sign-in
  - A measurement of your security posture with prioritised improvement actions
  - A bill for your M365 licences
  - An automatic firewall configuration
  answer: 1
  why: Secure Score scores your current security configuration and recommends ranked improvement actions
    (like enabling MFA), so you can see posture and prioritise what to fix.
- q: A DLP (data loss prevention) policy is designed to do what?
  options:
  - Back up mailboxes nightly
  - Delete old emails automatically
  - Detect and stop sensitive data such as credit-card numbers from leaving the organisation
  - Reset user passwords on a schedule
  answer: 2
  why: DLP inspects content for sensitive information types (e.g. credit-card or national-ID numbers)
    and can warn, block, or restrict sharing so that data does not leak out.
- q: Which statement best describes the difference between sensitivity labels and retention labels?
  options:
  - They are the same feature with two names
  - Sensitivity labels delete data; retention labels encrypt it
  - Both only apply to Teams chats
  - Sensitivity labels classify and protect (encrypt/mark) data; retention labels control how long data
    is kept or when it is deleted
  answer: 3
  why: Sensitivity labels classify and protect content (encryption, watermarks, access limits); retention
    labels and policies govern lifecycle — how long items are retained and when they are deleted.
- q: What is the purpose of audit log search in Microsoft Purview, and where would a Tier 2 tech start
    it?
  answer: Audit log search records who did what across M365 (sign-ins, file access, sharing, admin changes).
    You start it in the Microsoft Purview portal under Audit, then filter by date, user, and activity
    to investigate an incident or answer a 'who did this' question.
  why: Auditing gives the accountability trail. A Tier 2 tech reads and reports on it — for example, confirming
    who deleted a file or shared a document externally — rather than authoring deep policy.
- q: In one or two sentences, explain what eDiscovery is and why GDPR awareness matters to a helpdesk
    role.
  answer: eDiscovery is the process of searching for, holding, and exporting electronic content (email,
    files, chats) for legal cases or investigations. GDPR awareness matters because it sets rules on protecting
    and handling personal data, and helpdesk staff routinely touch user data, so knowing the obligations
    helps avoid mishandling it.
  why: eDiscovery finds and preserves relevant content for legal/compliance needs; GDPR is a key data-protection
    framework, and front-line staff must handle personal data responsibly even if they don't own the policy.
resources:
- label: Microsoft Learn — Microsoft Secure Score
  url: https://learn.microsoft.com/en-us/defender-xdr/microsoft-secure-score
- label: Microsoft Learn — Learn about data loss prevention (DLP)
  url: https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp
- label: Microsoft Learn — Learn about sensitivity labels
  url: https://learn.microsoft.com/en-us/purview/sensitivity-labels
- label: 'Microsoft Learn — Exam MS-102: Microsoft 365 Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## Shared responsibility, and why this matters

Moving to Microsoft 365 does not move security off your plate. Under the **shared-responsibility model**, Microsoft secures the physical datacentres and the underlying platform, but the **customer always owns their data, identities, and access**. That is exactly the layer a helpdesk touches every day — accounts, sharing, and the content users create.

Security and compliance are two sides of the same coin. **Security** keeps attackers and accidents from harming data; **compliance** proves you are handling data according to rules like **GDPR**. As a Tier 2 tech you won't author deep policy, but you must read these tools, report what you find, and take simple corrective actions.

## Microsoft Secure Score

**Microsoft Secure Score** measures your tenant's security posture as a percentage and gives a ranked list of **improvement actions** — for example, enabling multi-factor authentication or blocking legacy authentication. Each action shows the points gained and the user impact.

```text
Microsoft 365 Defender portal (security.microsoft.com)
  > Secure Score
    > Recommended actions  (sort by points / status)
    > pick an action > Manage in integrations
```

Reading it is a skill: look at the highest-value, lowest-impact actions first, and report progress over time.

## Microsoft Purview: the compliance hub

**Microsoft Purview** (at `compliance.microsoft.com` / `purview.microsoft.com`) is where compliance lives — data classification, **data loss prevention**, labels, auditing, and eDiscovery all sit here.

**DLP policies** detect **sensitive information types** (credit-card numbers, passport or national-ID numbers) and can warn a user, block sharing, or restrict access when that data tries to leave.

```text
Microsoft Purview portal
  > Data loss prevention > Policies
    > review policy > Locations (Exchange, SharePoint, OneDrive, Teams)
    > Rules > conditions (sensitive info types) > actions (block / notify)
```

## Labels: classify, protect, and retain

Two label families do different jobs:

- **Sensitivity labels** *classify and protect* content — they can mark a document **Confidential**, add a watermark, or apply encryption that follows the file.
- **Retention labels** and **retention policies** *control lifecycle* — how long an item is kept and when it is deleted.

```text
Microsoft Purview portal
  > Information protection > Labels        (sensitivity)
  > Data lifecycle management > Retention policies   (retain / delete)
```

## Auditing and eDiscovery

The **audit log** answers "who did what" — sign-ins, file access, external sharing, admin changes. You search it, filter, and report.

```text
Microsoft Purview portal
  > Audit > Search
    > set date range, users, activities > Search > export results
```

You can also check audit status with PowerShell:

```powershell
Connect-ExchangeOnline
Get-AdminAuditLogConfig | Select UnifiedAuditLogIngestionEnabled
```

**eDiscovery** is the process of finding, holding, and exporting content (email, files, chats) for legal cases or investigations. At Tier 2 you should recognise the concept and where it lives in Purview, not run full legal cases.

## Compliance frameworks at a glance

**GDPR** is the headline data-protection framework: it governs how personal data is collected, stored, and handled. Others include **ISO 27001** and **HIPAA**. You don't need to memorise them — just know they drive the labels, DLP, and retention rules you support.

## Your task

Open Secure Score and write down your tenant's current score plus the top three recommended actions. Then in Microsoft Purview, find one DLP policy and note what sensitive information type it protects and what action it takes.
