---
course: helpdesk-tier1-2
title: App deployment and management with Intune
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 4
summary: Learn how Microsoft Intune delivers and manages applications across Windows devices, from packaging
  Win32 apps to assigning them as Required or Available and troubleshooting why an install failed.
objectives:
- 'Identify the main app types Intune can deploy: Win32, line-of-business, Microsoft Store, web link,
  and Microsoft 365 apps'
- Package a Win32 application into the .intunewin format using the Microsoft Win32 Content Prep Tool
- Choose between Required, Available, and Uninstall assignment intents and explain each
- Decide when to assign apps to user groups versus device groups
- Explain how detection rules and the Company Portal report install status
- Troubleshoot a common reason an assigned app failed to install
video: hd5-l04-app-deployment-with-intune.mp4
quiz:
- q: Which tool packages a Win32 application into the .intunewin file Intune needs?
  options:
  - Microsoft Win32 Content Prep Tool
  - Windows Configuration Designer
  - Azure AD Connect
  - System Center Updates Publisher
  answer: 0
  why: The Microsoft Win32 Content Prep Tool (IntuneWinAppUtil.exe) wraps source files and the installer
    into a single .intunewin package for upload.
- q: A user wants an optional app they can install on demand from the Company Portal. Which assignment
    intent fits?
  options:
  - Required
  - Uninstall
  - Available for enrolled devices
  - Block
  answer: 2
  why: Available makes the app optional and visible in the Company Portal so the user can choose to install
    it; Required force-installs without user action.
- q: What is the primary purpose of a detection rule on a Win32 app?
  options:
  - To decide which group receives the app
  - To tell Intune whether the app is already installed
  - To encrypt the .intunewin file
  - To schedule a reboot after install
  answer: 1
  why: Detection rules (file, registry, MSI code, or script) let Intune determine current install state
    so it knows whether to install, skip, or report success.
- q: You must guarantee a security agent is installed on every laptop regardless of who logs in. What
    should you do?
  options:
  - Assign it as Available to a user group
  - Assign it as Required to a device group
  - Publish it as a web link
  - Assign Uninstall to all devices
  answer: 1
  why: Required assignment to a device group force-installs on the device itself, so it applies no matter
    which user signs in.
- q: Where in the Intune admin center do you upload and assign applications, and what app type is used
    to deploy custom EXE-based installers?
  answer: Go to the Intune admin center (intune.microsoft.com) > Apps, then add the app; custom EXE or
    script-based installers are deployed as Win32 apps using a .intunewin package.
  why: Apps is the dedicated workload for adding and assigning software, and Win32 app type handles EXE/MSI
    installers wrapped with the Content Prep Tool.
- q: An app assigned as Required shows 'Failed' for several devices. Name two things you would check first.
  answer: Check the detection rule (it may not correctly match the installed app) and verify the install
    command line, dependencies, and that the device is online and checked in; the Company Portal and device
    install status report give the error code.
  why: Most Required-install failures trace to a wrong detection rule, a bad command line or missing dependency,
    or a device that has not yet synced; the status reports and error codes pinpoint which.
resources:
- label: App management in Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/apps/app-management
- label: Win32 app management in Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-app-management
- label: Add apps to Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/apps/apps-add
- label: 'Exam MD-102: Endpoint Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
---

## Why app delivery matters

A huge slice of Tier 1 and Tier 2 work is getting the right software onto the right machine. With **Microsoft Intune** you stop walking USB sticks to desks and instead push apps from the cloud to enrolled Windows devices. Intune downloads the package, runs the installer silently, checks whether it worked, and reports status back to the admin center. Understanding this pipeline lets you move from "it won't install" tickets to confidently diagnosing the cause.

## App types in Intune

Intune supports several app types, each suited to a different source:

- **Win32 app** — your custom EXE, MSI, or script installers, packaged into a **.intunewin** file. This is the workhorse for in-house and third-party software.
- **Line-of-business (LOB) app** — a single MSI you upload directly, simpler but less flexible than Win32.
- **Microsoft Store app** — apps pulled from the new Microsoft Store integration; Intune handles updates automatically.
- **Web link** — a shortcut to a web app that appears in the Company Portal.
- **Microsoft 365 Apps** — a guided way to deploy Office (Word, Excel, Outlook) with channel and language options.

## Packaging a Win32 app

Win32 apps must be wrapped first. The **Microsoft Win32 Content Prep Tool** (`IntuneWinAppUtil.exe`) takes your source folder and setup file and produces one encrypted `.intunewin` package.

```powershell
IntuneWinAppUtil.exe -c C:\Source -s setup.exe -o C:\Output
```

You then upload that `.intunewin`, specify the silent **install and uninstall commands**, and define a **detection rule** so Intune knows when the app is present.

## Assigning apps

Adding an app does nothing until you assign it. There are three intents:

- **Required** — Intune force-installs the app automatically.
- **Available for enrolled devices** — the app appears in the **Company Portal** for users to install on demand.
- **Uninstall** — Intune removes the app from targeted devices.

You assign to **Microsoft Entra groups**. A key decision is **user groups versus device groups**: assign to a *user* group when the app should follow the person (Available apps usually target users); assign to a *device* group when the software must be on the machine no matter who logs in, such as a security agent.

```text
Intune admin center (intune.microsoft.com)
  > Apps > Windows > + Add
  > pick app type > upload package and set install/detect rules
  > Assignments > add group under Required / Available / Uninstall
```

## How status is reported

The **Company Portal** app is the user-facing storefront for Available apps and shows install progress. On the admin side, each app's **Device install status** and **User install status** pages report Installed, Failed, or Not applicable, along with an error code. The **detection rule** is what decides "Installed," so a mismatched rule is a frequent cause of phantom failures.

## Troubleshooting failures

When an app shows **Failed**, work through the basics: confirm the device has synced (it must check in to receive the assignment), verify the **install command line** is correct and silent, check for missing **dependencies**, and re-examine the **detection rule** to be sure it matches what the installer actually drops. Error codes from the status pages map to specific failures.

## Your task

In a test tenant, package a small free tool (for example, 7-Zip) into a `.intunewin` file with the Content Prep Tool, upload it as a Win32 app, set a detection rule, assign it as **Available** to a test user group, and confirm it appears in the Company Portal. Then add a second assignment as **Required** to a device group and verify the install status reports correctly.
