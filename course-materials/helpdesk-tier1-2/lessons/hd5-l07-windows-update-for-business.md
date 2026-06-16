---
course: helpdesk-tier1-2
title: Windows Update for Business and patching
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 7
summary: Learn how modern patching works without WSUS, using Windows Update for Business policies in Intune.
  Configure update rings with deferral, deadlines and active hours, tell feature updates from quality
  updates, expedite zero-day fixes, and monitor update compliance, with Windows Autopatch as the managed-service
  option.
objectives:
- Explain how Windows Update for Business patches devices without WSUS
- Configure update rings in Intune using deferral, deadline and active hours settings
- Distinguish feature updates from quality updates and manage each
- Describe how to expedite an update for a zero-day or critical fix
- Pause, resume, and roll back updates when a patch causes problems
- Monitor update compliance using Intune reports, and explain Windows Autopatch at a high level
video: hd5-l07-windows-update-for-business.mp4
quiz:
- q: How does Windows Update for Business get patches to devices?
  options:
  - Devices download updates directly from Microsoft's cloud, with policy controlling timing
  - An on-prem WSUS server stores and approves every update
  - An admin copies update files to each PC by USB
  - Updates only install when the user buys them
  answer: 0
  why: Windows Update for Business has devices pull updates straight from Microsoft, while Intune policy
    controls when and how they install, with no on-prem WSUS server required.
- q: What is the main difference between a quality update and a feature update?
  options:
  - Quality updates are paid; feature updates are free
  - Quality updates are monthly security and bug fixes; feature updates are the larger annual OS version
    upgrades
  - Feature updates only change the wallpaper
  - There is no difference, they are the same thing
  answer: 1
  why: Quality updates are the smaller monthly cumulative security and reliability fixes, while feature
    updates are the larger upgrades that move the device to a new Windows version, like 23H2 to 24H2.
- q: In an update ring, what does a DEADLINE setting do?
  options:
  - It blocks the device from ever updating
  - It deletes old updates
  - It forces installation and restart after a set number of days, even if the user keeps postponing
  - It changes the device name
  answer: 2
  why: A deadline gives users a grace period to install on their own terms, but once it passes the update
    is forced and the device will restart, so patches don't drift unpatched forever.
- q: Why would you EXPEDITE an update?
  options:
  - To slow a rollout down
  - To push a critical or zero-day fix quickly, bypassing the normal deferral period
  - To uninstall the latest update
  - To rename an update ring
  answer: 1
  why: Expedited updates let you rush an urgent security fix to devices fast, overriding the configured
    deferral so a zero-day gets patched within hours rather than waiting for the ring schedule.
- q: In one or two sentences, why do deferral periods and a ring strategy reduce risk and disruption?
  answer: Deferral lets a small pilot ring receive an update first so problems are caught before the wider
    fleet gets it, while staggered rings and active hours mean restarts happen at safe times, reducing
    both the blast radius of a bad patch and disruption to users.
  why: Rings with deferral catch bad updates early and spread the impact out, balancing security (devices
    still get patched) against stability (a flawed patch doesn't hit everyone at once).
- q: What is Windows Autopatch, in one sentence?
  answer: Windows Autopatch is a managed Microsoft service that automatically groups devices into rings
    and handles Windows, Office, Edge and driver updates for you, reducing the manual work of running
    update rings.
  why: Autopatch automates ring creation and update orchestration as a service, so smaller teams can get
    a well-run patching strategy without building and babysitting every ring by hand.
resources:
- label: Microsoft Learn — Manage Windows Updates with Windows Update for Business
  url: https://learn.microsoft.com/en-us/windows/deployment/update/waas-manage-updates-wufb
- label: Microsoft Learn — Manage Windows software updates in Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/windows-update-for-business-configure
- label: Microsoft Learn — Windows Autopatch overview
  url: https://learn.microsoft.com/en-us/windows/deployment/windows-autopatch/overview/windows-autopatch-overview
- label: 'Microsoft — Exam MD-102: Microsoft 365 Endpoint Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
---

## Patching without WSUS

In the old world, patches flowed through an on-prem **WSUS** server: you stored updates locally, approved each one, and pushed them to domain-joined PCs. Modern management does it differently. With **Windows Update for Business (WUfB)**, devices download updates *directly from Microsoft's cloud*, and you simply set **policy** in Intune to control *when* and *how* they install. No WSUS server, no approvals queue, and it works for the remote laptop just as well as the office desktop.

## Update rings

The core tool is the **update ring**. A ring is a policy you target at a group of devices that controls update timing. The key settings:

- **Deferral** — how many days to wait after Microsoft releases an update before this group installs it.
- **Deadline** — the point after which the update is forced and the device will restart, even if the user keeps postponing.
- **Active hours** — the daily window when restarts are *not* allowed, so a reboot never interrupts someone mid-meeting.

```text
1. Go to https://intune.microsoft.com
2. Devices -> Windows -> Update rings for Windows 10 and later
3. Create policy, set deferral, deadline, active hours
4. Assign it to a device group (start with a pilot ring)
```

A typical strategy uses several rings: a small **pilot** ring with short deferral, then **broad** and **critical** rings with longer deferral. If a patch breaks the pilot, you find out before it reaches everyone.

## Feature updates vs quality updates

Two kinds of update, managed separately:

- **Quality updates** — the smaller, monthly **cumulative** security and reliability fixes (the classic "Patch Tuesday").
- **Feature updates** — the larger, roughly annual upgrades that move a device to a new Windows version (for example 23H2 to 24H2). In Intune you create a **Feature updates** policy to pin or advance the target version, so you decide when the big jump happens.

## Why deferral and deadlines reduce risk

It is a balancing act. Patch too fast and a flawed update can take out your whole fleet; patch too slowly and you leave known vulnerabilities open. **Deferral** plus a **ring strategy** lets a pilot group absorb the risk first, while **deadlines** guarantee devices don't drift unpatched forever and **active hours** keep restarts out of the working day. Security and stability, both protected.

## Expedite, pause and roll back

Sometimes the normal schedule is too slow. For a **zero-day** or critical fix you can **expedite** an update, pushing it within hours and bypassing the configured deferral. Conversely, if a patch causes problems you can **pause** updates for a ring to stop the bleeding, and for quality updates you can **roll back** (uninstall) the latest update while you investigate.

## Monitoring and Windows Autopatch

Deploying isn't enough, you must confirm devices actually patched. Intune provides **Windows update reports** showing compliance, failures, and which version each device is on, your evidence that the fleet is current. For teams that want this run *for* them, **Windows Autopatch** is a managed Microsoft service that automatically groups devices into rings and orchestrates Windows, Office, Edge, and driver updates, a hands-off option built on the same WUfB foundations.

## Your task

In the Intune admin center, go to **Devices > Windows > Update rings**. Open (or create) an update ring and write down its **deferral**, **deadline**, and **active hours** values. Then, in your own words, explain how those three settings together protect both security and the user experience.
