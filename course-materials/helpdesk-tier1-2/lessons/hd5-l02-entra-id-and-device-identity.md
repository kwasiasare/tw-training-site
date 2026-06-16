---
course: helpdesk-tier1-2
title: Entra ID and device identity (join types)
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 2
summary: Learn what Microsoft Entra ID is and how the three device join types - Entra registered, Entra
  joined, and Entra hybrid joined - shape how a device is managed and what you can troubleshoot.
objectives:
- Explain what Microsoft Entra ID is and how it relates to the former Azure AD
- Describe the three device identity join types and when each is used
- Use dsregcmd /status on Windows to read a device's join state
- Locate and interpret device join type in the Entra admin center and Intune
- Explain at a high level what a Primary Refresh Token (PRT) is and why it matters
- Decide how join type affects sign-in, policy, and the tickets you can resolve
video: hd5-l02-entra-id-and-device-identity.mp4
quiz:
- q: A user brings their own personal laptop and adds their work account to access email. Which device
    identity type is this?
  options:
  - Entra hybrid joined
  - Entra registered
  - Entra joined
  - Domain joined only
  answer: 1
  why: Entra registered is for BYOD / personal devices where the user adds a work account but the device
    is not corporate-owned or fully managed.
- q: Which join type connects a device to BOTH on-premises Active Directory and Microsoft Entra ID?
  options:
  - Entra hybrid joined
  - Entra registered
  - Entra joined
  - Workgroup joined
  answer: 0
  why: Entra hybrid joined devices are joined to on-prem AD and registered in Entra ID, common during
    cloud migrations where Group Policy is still in use.
- q: What is the Primary Refresh Token (PRT) primarily used for?
  options:
  - Encrypting the device disk
  - Storing the local administrator password
  - Enabling single sign-on to Entra-protected resources
  - Backing up user files to OneDrive
  answer: 2
  why: The PRT is issued at sign-in and lets the device get tokens for apps and resources without re-prompting,
    powering seamless single sign-on (SSO).
- q: Which command on a Windows device shows whether it is Entra joined, hybrid joined, or registered?
  options:
  - gpresult /r
  - ipconfig /all
  - dsregcmd /status
  - whoami /all
  answer: 2
  why: dsregcmd /status reports AzureAdJoined, EnterpriseJoined, and DomainJoined states plus PRT and
    SSO details.
- q: In dsregcmd /status, which fields would you read to confirm a device is Entra joined (cloud-only)
    and not hybrid joined?
  answer: AzureAdJoined would show YES and DomainJoined would show NO. If DomainJoined also showed YES,
    the device would be Entra hybrid joined instead.
  why: Entra joined means cloud-only (no on-prem AD), so AzureAdJoined is YES while DomainJoined is NO.
- q: Why does it matter to know a device's join type before you start troubleshooting a sign-in or policy
    problem?
  answer: Join type determines where identity and policy come from - on-prem AD and Group Policy, Entra
    ID and Intune, or just a registered work account - so it tells you which console to check and which
    fixes are even possible.
  why: Knowing join type points you to the right management plane (Entra/Intune vs on-prem AD) and sets
    expectations for what you can change.
resources:
- label: What is a device identity in Microsoft Entra ID?
  url: https://learn.microsoft.com/en-us/entra/identity/devices/overview
- label: Plan your Microsoft Entra device deployment
  url: https://learn.microsoft.com/en-us/entra/identity/devices/plan-device-deployment
- label: Troubleshoot devices by using the dsregcmd command
  url: https://learn.microsoft.com/en-us/entra/identity/devices/troubleshoot-device-dsregcmd
- label: 'MD-102: Endpoint Administrator exam'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
---

## What Microsoft Entra ID is

**Microsoft Entra ID** is Microsoft's cloud identity and access management service - it is the product formerly called **Azure Active Directory (Azure AD)**. The rename is just branding; the tenant, accounts, groups, and tokens are the same. Entra ID is where user accounts live, where sign-ins are authenticated, and where **Conditional Access** policies decide whether a sign-in is allowed. For helpdesk work, the key shift from classic on-prem **Active Directory (AD)** is that identity now lives in the cloud and devices can register themselves with that cloud directory.

A **device identity** is simply a record of a device in Entra ID. Having that record lets you target the device with policy, see it in reports, and let **Conditional Access** require a managed or compliant device before granting access.

## The three join types

There are three ways a Windows device can have an identity in Entra ID:

- **Entra registered** - the device is personal (BYOD). The user adds their work account, but the device itself is owned by the person. Used for phones, home PCs, and contractor laptops. You get limited management.
- **Entra joined** - the device is corporate-owned and **cloud-only**. It is joined directly to Entra ID with no on-prem AD involvement. This is the modern target state, usually managed by **Intune**.
- **Entra hybrid joined** - the device is joined to **both** on-prem AD and Entra ID. This is common in organizations still migrating to the cloud that need **Group Policy** and on-prem resources while also using Entra and Intune.

A quick rule of thumb: personal = registered, cloud-only corporate = joined, still tied to on-prem AD = hybrid joined.

## The Primary Refresh Token (PRT)

When a user signs in on an Entra joined or hybrid joined device, Entra issues a **Primary Refresh Token (PRT)**. At a high level the PRT proves "this user, on this device," and lets the device silently get tokens for apps and websites without re-prompting. That is what powers **single sign-on (SSO)**. If SSO suddenly breaks across many apps, a broken or missing PRT is a prime suspect.

## Checking join type on the device

The fastest check on Windows is **dsregcmd**:

```text
Open a Command Prompt and run:
dsregcmd /status
```

```powershell
# Read the Device State section of the output:
# AzureAdJoined : YES   -> registered in Entra
# EnterpriseJoined : NO
# DomainJoined : YES    -> also joined to on-prem AD
# If AzureAdJoined=YES and DomainJoined=NO  -> Entra joined (cloud-only)
# If AzureAdJoined=YES and DomainJoined=YES -> Entra hybrid joined
# AzureAdPrt : YES      -> a Primary Refresh Token is present
```

## Checking join type in the portal

You can confirm the same thing from the cloud side:

```text
Entra admin center (entra.microsoft.com)
> Devices > All devices
> select the device
> read the "Join type" column / property: Entra registered, Entra joined, or Entra hybrid joined
```

The same devices appear in **Intune** under Devices, where you can also see compliance and assigned policies. Join type affects what you can fix: a **registered** BYOD device gives you little control, while an Entra **joined** device managed by Intune lets you push policy, wipe, or reset.

## Your task

On a Windows device, run `dsregcmd /status` and identify the join type from the AzureAdJoined and DomainJoined values, and confirm whether AzureAdPrt is YES. Then open the Entra admin center, go to Devices > All devices, find that same device, and confirm its Join type matches what the command reported. Write one sentence explaining how that join type would affect a sign-in troubleshooting ticket.
