---
course: helpdesk-tier1-2
title: Modern management and an intro to Microsoft Intune
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 1
summary: See how endpoint management moved from on-prem domain joins and imaging to cloud-based management,
  then tour Microsoft Intune and the admin center you will use every day.
objectives:
- Contrast traditional management (AD + Group Policy + imaging) with modern cloud management
- Describe what Microsoft Intune is and where it fits in Microsoft Intune Suite and Microsoft 365
- Navigate the Microsoft Intune admin center and find devices, apps, and policies
- Explain the role of the Intune MDM and how a device 'enrolls'
- Identify the difference between MDM and MAM at a high level
- Know what an Endpoint Administrator does and how MD-102 maps to the job
video: hd5-l01-modern-management-and-intune.mp4
quiz:
- q: What is the biggest shift that 'modern management' represents compared with traditional management?
  options:
  - Devices are managed from the cloud instead of requiring an on-prem domain and Group Policy
  - All devices must run Linux
  - Users can no longer install any apps
  - Imaging every device by hand becomes mandatory
  answer: 0
  why: Modern management uses cloud services like Intune and Entra ID so a device can be configured and
    secured over the internet, without needing a line of sight to an on-prem domain controller or hand-built
    images.
- q: Which portal is the primary place an Endpoint Administrator works in day to day?
  options:
  - Azure Storage Explorer
  - The Microsoft Intune admin center
  - Windows Disk Management
  - The BIOS setup screen
  answer: 1
  why: The Microsoft Intune admin center (intune.microsoft.com) is the unified console for devices, apps,
    configuration, compliance, and security policies.
- q: What does MDM stand for, and what does it manage?
  options:
  - Managed Data Migration — it moves files
  - Mobile Device Management — it manages the whole device
  - Multi-Domain Mapping — it links domains
  - Memory Defragment Manager — it tunes RAM
  answer: 1
  why: 'MDM (Mobile Device Management) enrolls and manages an entire device: its settings, compliance,
    apps, and security posture from the cloud.'
- q: How does MAM differ from MDM?
  options:
  - MAM encrypts the hard drive only
  - MAM manages company app data without managing the whole device
  - MAM is only for servers
  - MAM disables the network
  answer: 1
  why: MAM (Mobile Application Management) protects corporate data inside specific apps (like Outlook)
    without taking management control of the entire personal device.
- q: In one sentence, what is device 'enrollment'?
  answer: Enrollment is the process where a device registers with Intune so it can receive and report
    on policies, apps, and compliance.
  why: Until a device is enrolled, Intune has no management relationship with it, so it cannot push configuration
    or read compliance state.
- q: Name one real benefit of cloud management for a remote or hybrid workforce.
  answer: Devices can be configured, secured, and supported over the internet without needing to be on
    the corporate network or VPN.
  why: Cloud management removes the on-prem line-of-sight requirement, which is essential when staff work
    from anywhere.
resources:
- label: Microsoft Learn — Microsoft Intune overview
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/what-is-intune
- label: 'Microsoft Learn — Tutorial: Walkthrough Microsoft Intune admin center'
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/tutorial-walkthrough-intune-portal
- label: 'Microsoft — Exam MD-102: Microsoft 365 Endpoint Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
- label: Microsoft Learn — Microsoft Intune Suite
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/intune-add-ons
---

## From the old world to the cloud

If you have worked Tier 1, you have probably met **traditional management**: a Windows PC joined to an on-premises **Active Directory** domain, pushed settings via **Group Policy**, and built from a hand-crafted **image**. It works, but it assumes the device is on the corporate network and that someone built that image by hand.

**Modern management** flips this. The device is managed from the **cloud**, over the internet, from anywhere. Settings, apps, and security all flow down from a cloud service. This matters enormously for a hybrid and remote workforce — the PC at someone's kitchen table is just as manageable as the one in the office.

## What is Microsoft Intune?

**Microsoft Intune** is Microsoft's cloud service for managing devices and apps. It is the engine of modern management. Intune can manage Windows, macOS, iOS/iPadOS, and Android, and it sits inside the broader **Microsoft 365** and **Microsoft Intune Suite** family alongside Entra ID and Defender.

Intune does the jobs you used to do by hand or with Group Policy: deploy apps, push **configuration profiles**, enforce **compliance**, and apply security baselines — all from one console.

## MDM vs MAM

Two terms you will hear constantly:

- **MDM (Mobile Device Management)** manages the *whole device*. Think company-owned laptops fully enrolled into Intune.
- **MAM (Mobile Application Management)** protects company *data inside apps* without managing the whole device. Think a personal phone where only the Outlook work account is protected.

Knowing which one applies tells you how much control you have and what you can troubleshoot.

## A tour of the admin center

The console you will live in is the **Microsoft Intune admin center**.

```text
1. Go to https://intune.microsoft.com
2. Sign in with an admin account
3. Left menu, explore the key blades:
   - Devices  -> enrolled devices and their state
   - Apps     -> what you deploy to devices
   - Endpoint security -> baselines, antivirus, Defender
   - Reports  -> compliance and deployment status
   - Tenant administration -> connectors and roles
```

Spend time here. Click **Devices**, pick one, and look at its hardware, compliance, and the policies applied to it. This single device blade answers most Tier 2 questions.

## Enrollment in one sentence

**Enrollment** is the moment a device registers with Intune so it can receive policies and report back. No enrollment, no management relationship — so when a policy 'isn't applying', the first question is often: *is the device actually enrolled and checking in?*

## The role and the exam

The job title is **Endpoint Administrator**, and the certification that maps to it is **MD-102**. As you move from Tier 1 to Tier 2, you stop just resetting passwords and start owning device configuration, app delivery, and compliance. This month builds exactly those skills.

## Your task

Sign in to the Microsoft Intune admin center, open the **Devices** blade, pick any enrolled device, and write down three facts about it: its compliance state, its operating system version, and one policy applied to it.
