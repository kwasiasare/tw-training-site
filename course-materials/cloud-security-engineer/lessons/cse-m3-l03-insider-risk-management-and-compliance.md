---
course: cloud-security-engineer
title: Insider Risk Management and Communication Compliance
month: 3
monthTitle: Data Security & AI Governance with Microsoft Purview
lesson: 3
summary: Not every threat comes from outside. Microsoft Purview Insider Risk Management detects risky
  activity by people who already have legitimate access, the departing employee mass-downloading files,
  the user emailing data to a personal account, the policy violator. This lesson covers risk indicators
  and policy templates, sequence detection that strings activities into a story, and cumulative exfiltration
  anomalies that catch unusual data aggregation and mass downloads by high-risk users. You will learn
  how pseudonymization and privacy-by-design protect investigated users, how triage and case management
  work, and why role-based access enforces separation of duties. A short introduction to Communication
  Compliance rounds out the human side of data governance.
objectives:
- Explain the insider risk problem and how Purview Insider Risk Management addresses it
- Map risk indicators to policy templates such as data theft by departing users and data leaks
- Describe sequence detection and cumulative exfiltration / mass-download anomaly detection
- Explain pseudonymization and privacy-by-design and why they are on by default
- Walk the alert triage, investigation, and case management lifecycle
- Apply role-based access for separation of duties and summarize Communication Compliance
video: cse-m3-l03-insider-risk-management-and-compliance.mp4
quiz:
- q: What core problem does Insider Risk Management address that perimeter and DLP controls do not fully
    solve?
  options:
  - External hackers brute-forcing passwords
  - Risky actions taken by people who already hold legitimate access to the data
  - Misconfigured firewalls
  - Expired TLS certificates
  answer: 1
  why: Insider Risk Management focuses on trusted insiders, employees, contractors, partners, who already
    have valid access. DLP can block a specific action, but it does not by itself build a risk picture
    of a person over time. IRM correlates many signals to surface users whose behaviour suggests data
    theft, leakage, or policy violation.
- q: A user resigns, and over the next two weeks downloads large volumes of SharePoint files and copies
    them to USB. Which Insider Risk policy template is the best fit?
  options:
  - General data leaks only
  - Data theft by departing (or leaving) users, which can use HR connector signals to weight activity
    around the resignation date
  - Security policy violations by priority users
  - Communication Compliance
  answer: 1
  why: 'The ''data theft by departing users'' template is purpose-built for this: it can ingest a resignation
    or termination date (often via the HR connector) and raise the weighting of exfiltration activity
    around that date, exactly the departing-employee mass-download scenario.'
- q: What does sequence detection add over evaluating individual activities in isolation?
  options:
  - It encrypts the user's mailbox
  - It links related activities into an ordered story, such as download then rename then exfiltrate, that
    is riskier than any single step
  - It deletes the risky files automatically
  - It disables the user's account immediately
  answer: 1
  why: Sequence detection connects a chain of related actions (for example collect, obfuscate or rename,
    then exfiltrate) into a single narrative. The sequence as a whole signals intent and risk far more
    strongly than any isolated event, helping analysts see the full exfiltration path.
- q: What is cumulative exfiltration detection designed to catch?
  options:
  - A single large file shared once
  - Unusual aggregation where many smaller exfiltration activities across channels add up to anomalous
    data movement over time by a user
  - Failed sign-in attempts
  - Expired sensitivity labels
  answer: 1
  why: Cumulative exfiltration detection looks at the total volume of exfiltration activity a user accumulates
    across channels and time, surfacing anomalous aggregation and mass downloads that would each look
    minor in isolation but together indicate elevated risk.
- q: Why is pseudonymization enabled by default in Insider Risk Management, and what does it do?
  options:
  - It speeds up alert generation by caching results
  - It replaces usernames with anonymized identifiers in the investigation experience so analysts assess
    behaviour without bias, supporting privacy-by-design
  - It encrypts the SharePoint sites involved
  - It permanently deletes user identity from logs
  answer: 1
  why: Pseudonymization masks user identities (names, emails) with anonymized aliases in the IRM UI so
    investigators triage based on the activity, not the person, reducing bias and protecting privacy.
    Identities can be revealed only through a controlled, role-gated action, embodying privacy-by-design.
- q: Explain, in two to four sentences, how role-based access in Insider Risk Management enforces separation
    of duties, and why that matters for a program's credibility.
  answer: Insider Risk Management ships role groups such as Insider Risk Management Analysts, who can
    triage and investigate alerts but see pseudonymized data, and Investigators, who can view real identities
    and manage cases, plus an Admin role that configures policies but does not investigate. Separating
    policy configuration from investigation from identity reveal means no single person can both define
    what is monitored and unilaterally act on a named individual. This separation of duties protects employees
    from misuse of the system, satisfies privacy and works-council requirements, and gives the program
    legal and ethical credibility. Without it, an insider risk tool could itself become a tool for surveillance
    abuse.
  why: A strong answer names the distinct IRM roles, explains that configuration, triage, and identity
    reveal are split across them, and connects that split to abuse prevention, privacy compliance, and
    program legitimacy.
resources:
- label: Learn about insider risk management
  url: https://learn.microsoft.com/en-us/purview/insider-risk-management
- label: Insider risk management policy templates
  url: https://learn.microsoft.com/en-us/purview/insider-risk-management-policies
- label: Investigate insider risk management activities
  url: https://learn.microsoft.com/en-us/purview/insider-risk-management-activities
- label: Learn about communication compliance
  url: https://learn.microsoft.com/en-us/purview/communication-compliance
---

## The Threat From Inside

Firewalls, Conditional Access, and DLP are built largely to stop outsiders and to block specific risky actions. But the person most able to steal your data is someone who is *supposed* to have it: the engineer who downloads the codebase before joining a competitor, the salesperson who emails the client list to a personal account, the contractor who copies a project folder to USB on their last day. **Microsoft Purview Insider Risk Management (IRM)** exists to surface exactly these situations. Where DLP blocks one event, IRM builds a **risk picture of a person over time** by correlating many weak signals into a strong one, while carefully protecting the privacy of the people it observes.

## Risk Indicators and Policy Templates

IRM is driven by **indicators**, the signals it watches, and **policy templates**, pre-built scenarios that select relevant indicators and scoring.

**Indicators** include things like: downloading large numbers of files from SharePoint, copying files to USB or personal cloud, printing, emailing to external or personal domains, renaming files in a way that hides content, accessing sites the user does not normally touch, and Defender/endpoint security alerts. Some indicators are **HR-context** signals delivered via the **HR connector**, such as a resignation date or a performance improvement plan.

**Policy templates** assemble indicators into scenarios:

- **Data theft by departing users** - weights exfiltration around a resignation/termination date.
- **Data leaks** - general unauthorized sharing or exfiltration of sensitive data, optionally tied to DLP policy matches.
- **Security policy violations** - risky activity from users who trigger Defender alerts or violate security policy, including priority-user variants.
- Additional templates cover risky browser usage, risky AI usage, and patient data misuse in healthcare.

You choose a template, scope it to users or groups, set thresholds, and the policy begins scoring activity into **low / medium / high** risk.

## Sequence Detection: Telling the Story

A single download is rarely alarming. What matters is the **chain**. **Sequence detection** links related activities into an ordered narrative, for example:

```text
1. Collect    -> download 400 files from a SharePoint site
2. Obfuscate  -> rename / zip / change file extensions
3. Exfiltrate -> copy the archive to USB or upload to personal cloud
```

Seeing collect -> obfuscate -> exfiltrate as one sequence signals **intent** far more strongly than any single step, and it gives the analyst the full exfiltration path on a timeline rather than a pile of disconnected events.

## Cumulative Exfiltration and Mass-Download Anomalies

The other key analytic is **cumulative exfiltration detection**. Insiders often stay quiet per-event, ten files here, an email there, a small upload later, so that no single action trips a threshold. IRM aggregates exfiltration activity **across channels and over time** and flags **anomalous aggregation**: a user whose total data movement is abnormal compared to their own baseline and their peers. This is precisely how you catch the **mass download** and **unusual data aggregation** patterns of a high-risk user who is deliberately staying under per-action limits. Anomaly-based scoring compares a user against historical norms so that 'normal busy' does not generate noise but a genuine spike does.

## Privacy by Design: Pseudonymization

A tool that profiles employees must be built to **prevent its own abuse**. IRM applies **privacy-by-design**:

- **Pseudonymization is on by default** - usernames and emails are replaced with anonymized aliases throughout the investigation UI, so analysts triage **behaviour, not identity**, reducing bias.
- Revealing a real identity is a **separate, role-gated action** that is itself audited.
- Policies can be scoped, and many regions require works-council or privacy sign-off before deployment.

This is not a nice-to-have; it is what makes an insider risk program **legally and ethically defensible**.

## Triage, Investigation, and Case Management

The operational lifecycle moves an alert from noise to decision:

1. **Alerts** - the policy generates alerts when a user's scored activity crosses thresholds.
2. **Triage** - an analyst reviews the alert in the (pseudonymized) activity view, looking at the timeline, sequences, and contributing indicators, and marks it **confirmed**, **dismissed**, or needing escalation.
3. **Cases** - confirmed alerts are escalated into a **case**, a container for deeper investigation that aggregates all of a user's activity, supports notes, and integrates with **eDiscovery** and collaboration for legal/HR.
4. **Actions** - outcomes include user notifications, escalation to HR or legal, automatic creation of an eDiscovery case, or remediation. All steps are logged in the audit trail.

## Separation of Duties via RBAC

IRM ships distinct **role groups** so that no one person controls the whole pipeline:

- **Insider Risk Management Admins** configure policies but do not investigate.
- **Analysts** triage and investigate with **pseudonymized** data.
- **Investigators** can view real identities and manage cases.
- **Auditors** review the program's own activity.

Splitting *who defines monitoring* from *who investigates* from *who can unmask identities* enforces **separation of duties**, preventing the tool from becoming a surveillance weapon and satisfying privacy regulators.

## A Brief Look at Communication Compliance

Where IRM watches data movement, **Communication Compliance** watches **communications** for risky or non-compliant content across Exchange, Teams, Viva Engage, and connected third-party channels. It uses policies and classifiers to detect things like harassment, threats, regulatory violations, or potential leakage in messages, then routes flagged items to designated reviewers, again with pseudonymization and role-based access to protect privacy. Together, IRM and Communication Compliance cover the **human side** of data governance: not just what the data is, but how trusted people handle and discuss it.
