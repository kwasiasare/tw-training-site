---
course: helpdesk-tier1-2
title: Configuration profiles and compliance policies
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 5
summary: Understand how Intune configuration profiles push settings to devices while compliance policies
  evaluate devices against rules, and how compliance feeds Conditional Access to protect company resources.
objectives:
- Explain the difference between a configuration profile (sets settings) and a compliance policy (checks
  rules)
- Create a configuration profile using the settings catalog or a template
- Describe administrative templates as the cloud answer to Group Policy
- Build a compliance policy with rules such as BitLocker required and minimum OS version
- Explain how compliance status feeds Conditional Access to allow or block access
- Configure actions for noncompliance and a grace period
video: hd5-l05-configuration-and-compliance-policies.mp4
quiz:
- q: What does a configuration profile do?
  options:
  - Evaluates a device against rules and marks it compliant
  - Pushes and enforces specific settings onto a device
  - Packages an app into a .intunewin file
  - Enrolls a device into Microsoft Entra
  answer: 1
  why: A configuration profile sets and enforces settings such as Wi-Fi, VPN, or a screen-lock timeout;
    it configures rather than merely checks.
- q: A compliance policy finds a device without BitLocker enabled. What is its direct effect?
  options:
  - It silently enables BitLocker
  - It marks the device non-compliant
  - It uninstalls noncompliant apps
  - It re-enrolls the device
  answer: 1
  why: Compliance policies evaluate and report; they mark the device non-compliant and trigger configured
    actions, but they do not change the setting themselves.
- q: Which Intune feature is the cloud-based successor to on-premises Group Policy settings?
  options:
  - Administrative templates
  - Detection rules
  - Company Portal
  - Autopilot
  answer: 0
  why: Administrative templates (and the broader settings catalog) bring familiar ADMX-style Group Policy
    settings into Intune for cloud-managed devices.
- q: How does compliance most commonly protect company resources?
  options:
  - By encrypting all email at rest
  - By feeding device compliance state into Conditional Access
  - By blocking the Microsoft Store
  - By forcing a daily password change
  answer: 1
  why: Conditional Access can require a device to be marked compliant before granting access to apps like
    Exchange or SharePoint, so a non-compliant device is blocked.
- q: In the Intune admin center, under which workload do you create configuration profiles and compliance
    policies, and what menu separates them?
  answer: 'Both live under Devices in the Intune admin center: configuration profiles under Devices >
    Configuration (or Manage devices > Configuration), and compliance policies under Devices > Compliance.'
  why: Devices is the workload for managing device state; Configuration handles settings you push while
    Compliance handles rules you evaluate.
- q: What is a grace period in a compliance policy, and why is it useful?
  answer: A grace period delays marking a device non-compliant (or delays the resulting action) for a
    set number of days after it first fails a rule, giving the user time to fix the issue before losing
    access.
  why: It prevents abrupt lockouts and gives end users a window to remediate, reducing helpdesk tickets
    while still enforcing policy.
resources:
- label: Apply features and settings with device configuration profiles
  url: https://learn.microsoft.com/en-us/mem/intune/configuration/device-profiles
- label: Use the settings catalog to configure settings
  url: https://learn.microsoft.com/en-us/mem/intune/configuration/settings-catalog
- label: Get started with device compliance policies in Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/device-compliance-get-started
- label: 'Exam MD-102: Endpoint Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
---

## Two jobs: setting versus checking

The single most important idea in this lesson is the difference between **configuration** and **compliance**. A **configuration profile** *sets* something on a device: it pushes and enforces settings like a Wi-Fi profile, a VPN connection, or a screen-lock timeout. A **compliance policy** *checks* something: it evaluates a device against rules and reports whether the device is **compliant** or **non-compliant**. Configuration changes the device; compliance only judges it. Keeping that distinction clear will save you on the MD-102 exam and on the job.

## Configuration profiles

When you need a setting applied everywhere, you create a **configuration profile**. Intune offers a few ways to author them:

- **Settings catalog** — a searchable list of thousands of individual settings you pick from; this is the modern, preferred approach.
- **Templates** — pre-grouped profiles for common scenarios like VPN, Wi-Fi, email, or endpoint protection.
- **Administrative templates** — the cloud answer to on-premises **Group Policy**, exposing familiar ADMX-style settings for admins coming from Active Directory.

```text
Intune admin center (intune.microsoft.com)
  > Devices > Configuration > + Create > New Policy
  > pick platform (Windows) and Settings catalog or Templates
  > add settings > Assignments > choose groups
```

The profile is then assigned to **Microsoft Entra groups** of users or devices, just like apps.

## Compliance policies

A **compliance policy** is a set of rules a device must satisfy. Typical rules include **BitLocker required**, a **minimum OS version**, **password required**, and Microsoft Defender being healthy. Intune evaluates the device against these rules on a schedule and stamps it **Compliant** or **Not compliant**. Crucially, compliance does *not* fix anything; it reports. If you want BitLocker actually turned on, that is a *configuration* job.

```text
Intune admin center (intune.microsoft.com)
  > Devices > Compliance > + Create policy
  > choose platform > define rules (BitLocker, min OS, password)
  > Actions for noncompliance > set grace period
  > Assignments > choose groups
```

## Actions and grace periods

Under **Actions for noncompliance** you decide what happens when a device fails. Options include sending the user an email, marking the device non-compliant after a delay, or remotely locking it. A **grace period** delays the non-compliant mark for a number of days, giving the user time to remediate before they lose access. This softens enforcement and cuts down on sudden lockout tickets.

## Compliance meets Conditional Access

Compliance becomes powerful when it feeds **Conditional Access**. A Conditional Access policy in Microsoft Entra can require that a device be **marked compliant** before it is allowed to reach resources like Exchange Online or SharePoint. So if a laptop fails its compliance policy, Conditional Access can **block** it from corporate email until it is fixed. This is how the two halves connect: compliance produces a verdict, and Conditional Access acts on it.

## Putting it together

In practice you usually pair them: a configuration profile *enables* BitLocker and sets a password policy, while a compliance policy *verifies* those same controls and reports to Conditional Access. One enforces, the other audits, and together they keep only healthy devices on the network.

## Your task

In a test tenant, create a Windows **configuration profile** using the settings catalog that sets a screen-lock timeout, and assign it to a test group. Then create a **compliance policy** that requires BitLocker and a minimum OS version, configure an action for noncompliance with a short **grace period**, assign it, and describe in one or two sentences how a Conditional Access policy could use that compliance state to block a non-compliant device from email.
