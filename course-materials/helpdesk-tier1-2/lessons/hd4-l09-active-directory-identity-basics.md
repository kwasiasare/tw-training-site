---
course: helpdesk-tier1-2
title: Active Directory and identity basics
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 9
summary: 'Understand Active Directory and the identity tasks that fill a helpdesk day: resetting passwords,
  unlocking accounts, managing group membership, and doing it all securely.'
objectives:
- Explain what Active Directory is and the role of a domain
- Describe users, groups, and organizational units (OUs)
- Reset a password and unlock an account the correct way
- Use group membership to grant access instead of per-user permissions
- Verify a caller's identity before making account changes
- Handle a realistic account-related ticket end to end
video: hd4-l09-active-directory-identity-basics.mp4
quiz:
- q: What is Active Directory (AD)?
  options:
  - A web browser
  - Microsoft's directory service that stores and manages users, computers, and access on a network
  - A type of firewall
  - A spreadsheet program
  answer: 1
  why: Active Directory is Microsoft's directory service for Windows networks; it centrally stores accounts
    and controls authentication and access.
- q: What is the difference between unlocking an account and resetting a password?
  options:
  - Unlocking re-enables an account locked by failed logins; resetting changes the password itself
  - They are identical
  - Unlocking deletes the account
  - Resetting is only for admins
  answer: 0
  why: An account locks after too many bad attempts and just needs unlocking; a reset is needed when the
    user has actually forgotten or must change their password.
- q: Why is granting access through group membership preferred over per-user permissions?
  options:
  - It looks tidier only
  - It is required by Windows
  - 'It scales: you manage access by adding/removing users from groups instead of editing each resource'
  - It makes passwords stronger
  answer: 2
  why: Role-based groups make access manageable and auditable; you change one membership rather than editing
    permissions on many resources for each person.
- q: What must you always do before changing someone's account?
  options:
  - Nothing
  - Reboot the domain controller
  - Email everyone
  - Verify the caller's identity according to policy
  answer: 3
  why: Identity verification stops attackers using the helpdesk to hijack accounts; following the verification
    policy is a critical security control.
- q: What is an Organizational Unit (OU) used for in Active Directory?
  answer: An OU is a container used to organise users, groups, and computers, often to apply policies
    or delegate administration to a department or location.
  why: OUs structure the directory so settings (like Group Policy) and admin rights can be targeted at
    the right set of objects.
- q: Why is identity verification on a password-reset call a security control, not just a formality?
  answer: Attackers commonly phone the helpdesk pretending to be a user to get a password reset; verifying
    identity prevents this social-engineering attack from succeeding.
  why: The helpdesk is a frequent social-engineering target, so verification protects accounts and the
    whole organisation from compromise.
resources:
- label: Microsoft Learn — Active Directory Domain Services overview
  url: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview
- label: Microsoft Learn — Manage users and groups in Active Directory
  url: https://learn.microsoft.com/en-us/training/
- label: Microsoft Learn — Reset a user password and unlock accounts
  url: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/
- label: CompTIA — A+ security and operational procedures
  url: https://www.comptia.org/certifications/a
---

## Why identity is the helpdesk's bread and butter

A huge share of helpdesk tickets are about **identity**: "I can't log in," "my account's locked," "I need access to the shared folder." Behind most of these in a Windows environment sits **Active Directory**. Understanding it turns these tickets from mysteries into routine, confident fixes.

## What Active Directory is

**Active Directory (AD)** is Microsoft's **directory service** — a central database of every **user**, **computer**, and **resource** on a Windows network, plus the rules about who can access what. A network managed this way is called a **domain**. When a user logs into their work PC, the PC asks a **domain controller** (a server running AD) to confirm the password. That single sign-in then governs their access across the network.

## Users, groups, and OUs

Three objects matter most to you:

- A **user account** represents a person and holds their sign-in name and settings.
- A **group** is a collection of users; you grant access to the *group*, and membership grants it to each person.
- An **organizational unit (OU)** is a container that organises users and computers, often by department or site, so policies and admin can be targeted.

```text
Domain: contoso.local
  OU: Finance
    User: sam.patel
    Group: Finance-Share-RW  (members get write access to S:)
```

## Use groups, not per-user permissions

The golden rule of access: **grant through groups**, not to individuals. If Sam needs the finance drive, you add Sam to the **Finance-Share-RW** group — you do *not* edit the drive's permissions for Sam personally. When Sam later moves teams, you remove one group membership and all the right access changes at once. This is **role-based** thinking, and it scales.

## The two everyday fixes

Most identity tickets are one of two things, and they are *not* the same:

- **Account locked** — too many wrong passwords triggered a lockout. The fix is to **unlock** it; the password is fine.
- **Forgotten / expired password** — the fix is a **password reset**, after which the user usually sets a new one at next sign-in.

Diagnosing which one you are dealing with saves time and avoids unnecessary resets.

## Verify identity first — every time

The helpdesk is a favourite target for **social engineering**: an attacker phones pretending to be an employee to get a password reset and seize the account. So before *any* account change, **verify the caller's identity** using your organisation's policy — a callback number, employee ID, security questions, or a manager's confirmation.

```text
"Before I reset that, I need to verify your identity per policy.
Can you confirm your employee ID and the answer to your
security question, please?"
```

This is not bureaucracy. It is one of the most important security controls you personally operate.

## Your task

Write out how you would handle this ticket end to end: "Hi, I'm locked out of my computer and I have a meeting in ten minutes — can you reset my password?" In order, write: the identity-verification step (what you ask and why), how you decide whether it is a lockout or a true password reset, the action you take, and your closing line confirming the fix and any next step for the user.
