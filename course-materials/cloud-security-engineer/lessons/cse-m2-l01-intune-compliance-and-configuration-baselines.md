---
course: cloud-security-engineer
title: Intune Compliance Policies and Configuration Baselines
month: 2
monthTitle: Modern Endpoint Security & Threat Protection
lesson: 1
summary: This lesson builds the device-trust foundation that the rest of Module 2 depends on. You will
  enroll devices into Microsoft Intune, then author compliance policies that evaluate OS version, BitLocker/disk
  encryption, firewall state, Defender real-time protection, and the device threat level reported by Microsoft
  Defender for Endpoint. You will then push hardened configuration profiles and security baselines from
  the settings catalog to actively enforce BitLocker, Microsoft Defender Firewall, and Attack Surface
  Reduction. Finally you will see how the resulting compliant/noncompliant state becomes a first-class
  signal for Conditional Access, complete with 'mark device noncompliant' actions and grace periods.
objectives:
- Compare device enrollment models (Windows Autopilot, Automatic Enrollment, BYOD/MAM) and pick the right
  one per scenario.
- Author an Intune compliance policy that checks OS version, BitLocker, firewall, Defender real-time protection,
  and device threat level.
- Deploy configuration profiles and a settings-catalog security baseline that enforce BitLocker, firewall,
  and ASR.
- Configure compliance actions for noncompliance, including 'mark device noncompliant' with a grace period
  and end-user notifications.
- Explain how compliance state flows into Conditional Access as the 'require compliant device' grant control.
- Validate compliance and configuration results from the Intune admin center and on the endpoint.
video: cse-m2-l01-intune-compliance-and-configuration-baselines.mp4
quiz:
- q: Which Intune compliance setting turns a Defender for Endpoint machine-risk score into a pass/fail
    compliance result?
  options:
  - Require BitLocker
  - Require the device to be at or under the machine risk score (device threat level)
  - Minimum OS version
  - Require Secure Boot
  answer: 1
  why: The 'Require the device to be at or under the machine risk score' setting maps the MDE-reported
    threat level (Clear/Low/Medium/High) onto compliance, which is the hinge for the automated isolation
    loop later in the module.
- q: What is the difference between a configuration profile and a compliance policy in Intune?
  options:
  - They are the same feature with different names
  - A configuration profile enforces/sets settings on the device; a compliance policy only evaluates and
    reports a state
  - A compliance policy enforces settings; a configuration profile only reports
  - Configuration profiles only apply to iOS
  answer: 1
  why: Configuration profiles and security baselines actively push and enforce settings (e.g., turn BitLocker
    on). Compliance policies evaluate the device against rules and produce a compliant/noncompliant state
    used by Conditional Access.
- q: A compliance policy's action for noncompliance is set to 'Mark device noncompliant' with a schedule
    of 1 day. What happens?
  options:
  - The device is immediately wiped
  - The device is given a one-day grace period before its state flips to noncompliant
  - The user is blocked from sign-in for one day
  - Nothing until an admin manually approves
  answer: 1
  why: 'Setting the schedule to 1 day creates a grace period: the device is treated as compliant for one
    day after first failing, giving the user time to remediate before the state flips and Conditional
    Access reacts.'
- q: Where in Intune would you most efficiently configure dozens of granular Windows hardening settings
    (firewall, ASR, BitLocker) from a single searchable surface?
  options:
  - Templates > Administrative Templates only
  - The Settings Catalog
  - Compliance policies
  - Enrollment restrictions
  answer: 1
  why: The Settings Catalog exposes the full library of Windows CSP settings in one searchable place,
    and is the modern recommended way to build configuration profiles and security baselines.
- q: For an unmanaged personal phone accessing only Outlook and Teams, which enrollment approach is most
    appropriate?
  options:
  - Windows Autopilot
  - App protection policies / MAM without device enrollment
  - Microsoft Entra hybrid join
  - Group Policy
  answer: 1
  why: MAM (app protection policies) protects corporate data inside managed apps without enrolling or
    fully managing the personal device, which is the right fit for BYOD where you only need to govern
    app data.
- q: In 2-4 sentences, explain why deploying a compliance policy alone does not actually block a noncompliant
    device from reaching corporate resources, and what you must add.
  answer: A compliance policy only evaluates the device and stamps it compliant or noncompliant in Entra
    ID; by itself it changes nothing about access. To enforce access decisions you must pair it with a
    Conditional Access policy that uses the 'Require device to be marked as compliant' grant control.
    Only then does a noncompliant state actually block sign-in to apps like Exchange Online or SharePoint.
resources:
- label: Device compliance policies in Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/device-compliance-get-started
- label: Use the settings catalog to configure settings
  url: https://learn.microsoft.com/en-us/mem/intune/configuration/settings-catalog
- label: Security baselines for Windows in Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/security-baselines
- label: Use compliance policies with Conditional Access
  url: https://learn.microsoft.com/en-us/mem/intune/protect/device-compliance-get-started#use-conditional-access-with-your-compliance-policies
---

## Why device trust comes first

Zero Trust says *never trust, always verify* — and one of the strongest things you can verify is the health of the device making the request. In Microsoft Intune you build that verification in two halves: **configuration profiles / security baselines** that *enforce* a hardened state, and **compliance policies** that *evaluate* the device and stamp it compliant or noncompliant in Microsoft Entra ID. Conditional Access then consumes that stamp. Get this layer right and the automated isolation you build in Lesson 3 becomes almost free.

## Enrollment models: choose deliberately

Before a device can be governed it must be known to Intune. Pick the model that matches ownership and use case:

- **Windows Autopilot** — corporate Windows devices provisioned zero-touch from the OEM/reseller; the device joins Entra ID and enrolls automatically.
- **Automatic enrollment** — when a user Entra-joins a Windows device, MDM enrollment happens automatically (configured under *Devices > Enrollment*).
- **Hybrid Entra join** — on-prem AD-joined devices that also register in Entra; common in migration scenarios.
- **MAM / App protection (BYOD)** — personal phones where you protect *app data* (Outlook, Teams) without enrolling or fully managing the device.

Rule of thumb: full device management (and therefore compliance + configuration profiles) for corporate devices; MAM for unmanaged personal devices.

## Building a compliance policy

In the Intune admin center go to **Devices > Compliance > Create policy**, platform **Windows 10 and later**. Concrete settings to set:

- **Device Health**: Require BitLocker = *Require*; Require Secure Boot = *Require*; Code integrity = *Require*.
- **Device Properties**: Minimum OS version = e.g. `10.0.22631` (Windows 11 23H2 or later).
- **System Security**: Firewall = *Require*; Antivirus = *Require*; Microsoft Defender Antimalware real-time protection = *Require*; Encryption of data storage = *Require*.
- **Microsoft Defender for Endpoint**: *Require the device to be at or under the machine risk score* = **Medium**. This is the line that ties compliance to MDE's threat level — remember it for Lesson 3.

Assign the policy to a device or user group. A device that fails any rule will (after its action schedule) be marked noncompliant.

## Actions for noncompliance and grace periods

On the **Actions for noncompliance** tab you control the user experience and timing:

- **Mark device noncompliant** with *Schedule (days after noncompliance)* = `0` for immediate, or `1`–`3` to grant a **grace period** so users can self-remediate before access is cut.
- **Send email to end user** using a configured notification message template, optionally CC'ing the helpdesk.
- **Remotely lock** or **Retire the noncompliant device** for high-stakes scenarios.

Grace periods are a usability/security trade-off: too long and a risky device keeps access; `0` days gives the tightest containment, which is what you want for the threat-level rule.

## Enforcing settings with profiles and the settings catalog

Compliance *checks* but does not *fix*. Use **Devices > Configuration > Create > New policy > Settings catalog** to actively enforce. Search the catalog and add, for example:

- **BitLocker**: require encryption, XTS-AES 256, silent enablement, and escrow the recovery key to Entra ID.
- **Microsoft Defender Firewall**: enable Domain/Private/Public profiles, default inbound = block.
- **Attack Surface Reduction**: set ASR rules to *Block* (covered in depth in Lesson 2).

A simple way to read effective BitLocker state on an endpoint:

```powershell
# Confirm BitLocker is on and fully encrypted
Get-BitLockerVolume -MountPoint C: |
  Select-Object MountPoint, VolumeStatus, EncryptionPercentage, ProtectionStatus
```

## Security baselines as a fast hardening start

Instead of hand-picking hundreds of settings, deploy a **security baseline** (Devices > Security baselines) — Microsoft's recommended preconfigured set for Windows, Microsoft Defender for Endpoint, and Microsoft Edge. Treat the baseline as your starting point, then layer targeted settings-catalog profiles for anything the baseline doesn't cover. Watch for **conflicts**: when two profiles set the same setting differently, Intune reports the device as *Conflict* and applies neither, so keep ownership of each setting clear.

## Closing the loop into Conditional Access

None of this blocks anything yet. Compliance state is just metadata until a **Conditional Access** policy uses it. In Entra create a policy targeting your users and cloud apps, and under *Grant* select **Require device to be marked as compliant**. Now a noncompliant Windows device is denied at sign-in to Exchange Online, SharePoint, and your SaaS apps. Validate end-to-end: break a rule (e.g., disable the firewall), confirm the device flips to noncompliant in *Devices > All devices*, and confirm sign-in is blocked. That round trip is exactly what you will automate in Lesson 3.
