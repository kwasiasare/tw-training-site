---
course: helpdesk-tier1-2
title: Windows Autopilot deployment
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 3
summary: Learn how Windows Autopilot turns a factory-fresh device into a fully configured, user-ready
  PC with zero imaging, and how registration, deployment profiles, and the Enrollment Status Page make
  it happen.
objectives:
- Explain what Windows Autopilot is and how it removes the need for imaging
- Describe how a device is registered using its hardware hash
- Configure and assign a Windows Autopilot deployment profile
- Compare user-driven and self-deploying deployment modes
- Explain the purpose of the Enrollment Status Page (ESP) during OOBE
- Walk through the Autopilot screens in the Intune admin center
video: hd5-l03-windows-autopilot.mp4
quiz:
- q: What is the main benefit of Windows Autopilot for a helpdesk team?
  options:
  - It replaces antivirus on the device
  - It removes the need to build and apply custom images
  - It encrypts the network traffic
  - It backs up the device to tape
  answer: 1
  why: Autopilot provisions devices from the factory OS using cloud configuration, so technicians no longer
    build, store, and apply custom Windows images.
- q: What uniquely identifies a device so it can be registered for Autopilot?
  options:
  - The MAC address
  - The Wi-Fi SSID
  - The hardware hash (hardware ID)
  - The user's password
  answer: 2
  why: Autopilot registration uses the device's hardware hash (a hardware ID derived from the device),
    often supplied by the OEM or collected with a script.
- q: Which deployment mode requires NO user to sign in during setup and is used for kiosks or shared devices?
  options:
  - User-driven mode
  - Hybrid join mode
  - Co-management mode
  - Self-deploying mode
  answer: 3
  why: Self-deploying mode provisions the device with no user credentials, making it ideal for kiosks,
    digital signage, and shared devices.
- q: What does the Enrollment Status Page (ESP) do during the out-of-box experience?
  options:
  - Shows setup progress and blocks use until apps and policies are applied
  - Resets the local administrator password
  - Wipes the device
  - Captures the hardware hash
  answer: 0
  why: The ESP shows provisioning progress and can prevent the user from reaching the desktop until required
    apps, certificates, and policies are installed.
- q: Where in the Intune admin center do you find and manage Autopilot devices and profiles?
  answer: Intune admin center > Devices > Enrollment > Windows (under Windows Autopilot), where you manage
    Devices, Deployment profiles, and the Enrollment Status Page.
  why: Autopilot registration, profiles, and the ESP all live under the Windows enrollment area of the
    Intune admin center.
- q: In one sentence, explain the difference between user-driven and self-deploying Autopilot modes.
  answer: User-driven mode has the end user sign in with their work account so the device is set up and
    joined for that user, while self-deploying mode provisions the device with no user sign-in for kiosk
    or shared use.
  why: 'The key difference is whether a user authenticates during OOBE: user-driven requires it, self-deploying
    does not.'
resources:
- label: Overview of Windows Autopilot
  url: https://learn.microsoft.com/en-us/autopilot/overview
- label: Register devices to Windows Autopilot
  url: https://learn.microsoft.com/en-us/autopilot/add-devices
- label: Windows Autopilot Enrollment Status Page
  url: https://learn.microsoft.com/en-us/autopilot/enrollment-status
- label: 'MD-102: Endpoint Administrator exam'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
---

## What Windows Autopilot is

**Windows Autopilot** is a cloud-driven way to set up and configure brand-new Windows devices. The goal is **zero-touch provisioning**: a device ships from the factory with a standard Windows install, and when the user turns it on and connects to the internet, it automatically becomes a fully configured, corporate-ready PC - joined to **Entra ID**, enrolled in **Intune**, with policies and apps applied. The technician never touches the box.

The big win for helpdesk teams is the end of **imaging**. Traditionally you built a custom Windows image, stored it, and applied it to every machine - slow, version-sensitive work. With Autopilot you start from the OEM's factory OS and let the cloud do the configuration. Less time per device, fewer images to maintain, and devices can be drop-shipped straight to users.

## Registering a device (hardware hash)

For Autopilot to recognize a device, that device must be **registered** to your tenant. Registration is keyed on the **hardware hash** (also called the hardware ID) - a value derived from the device's hardware. There are three common ways it gets registered:

- The **OEM or reseller** registers it at purchase (the smoothest path).
- You **collect the hash** from an existing device and import it.
- A **distributor** uploads it on your behalf.

To collect the hash yourself from a device:

```powershell
# Run in an elevated PowerShell session
Install-Script -Name Get-WindowsAutopilotInfo -Force
Get-WindowsAutopilotInfo -OutputFile C:\HWID\AutopilotHWID.csv
```

You then import that CSV into Intune so the device shows up as an Autopilot device.

## Deployment profiles

A **deployment profile** is the set of rules that tells Autopilot how to configure a device: which **join type** (Entra joined or hybrid joined), what the out-of-box experience should hide or show, the naming convention, and which mode to use. You build the profile once and **assign** it to a group; any registered device in that group picks it up automatically.

## User-driven vs self-deploying modes

There are two main modes:

- **User-driven** - the end user signs in with their **work account** during setup. The device is provisioned and assigned to that user. This is the common choice for normal staff laptops.
- **Self-deploying** - **no user signs in**. The device provisions itself end-to-end. This is for **kiosks, digital signage, and shared devices** where there is no single owner.

## OOBE and the Enrollment Status Page

When the device first boots, the user sees the **Out-of-Box Experience (OOBE)** - the standard Windows setup screens. Autopilot customizes OOBE based on the profile, then hands off to the **Enrollment Status Page (ESP)**. The ESP shows provisioning **progress** and can **block** the user from reaching the desktop until required apps, certificates, and policies are installed - so users don't start working on a half-configured machine.

```text
Intune admin center (intune.microsoft.com)
> Devices > Enrollment > Windows
> Windows Autopilot:  Devices  |  Deployment profiles  |  Enrollment Status Page
```

From here you confirm a device is registered, create or edit a deployment profile, assign it to a group, and configure the ESP behavior.

## Your task

In the Intune admin center, navigate to Devices > Enrollment > Windows and open the Windows Autopilot area. Review the Devices, Deployment profiles, and Enrollment Status Page sections. Then describe, in three to four sentences, how you would take a brand-new laptop from its box to a user's hands using Autopilot - name the hardware hash registration step, the deployment profile, the mode you would choose (user-driven), and the role the ESP plays during OOBE.
