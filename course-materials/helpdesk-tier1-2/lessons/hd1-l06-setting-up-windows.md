---
course: helpdesk-tier1-2
title: Setting up and navigating Windows
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 6
summary: 'Get comfortable moving around Windows: the desktop, File Explorer, Settings, user accounts,
  Task Manager, and the keyboard shortcuts that make a helpdesk technician fast.'
objectives:
- 'Navigate the Windows desktop: Start menu, taskbar, system tray, and search'
- Tell the difference between Settings and the classic Control Panel
- 'Open File Explorer and find the C: drive, This PC, and your user profile'
- Explain local vs Microsoft accounts and standard vs administrator users
- Open Task Manager and use it to end a frozen program
- Use essential keyboard shortcuts and check for Windows Update
video: hd1-l06-setting-up-windows.mp4
quiz:
- q: Which keyboard shortcut opens File Explorer instantly?
  options:
  - Ctrl+E
  - Win+E
  - Alt+E
  - Win+F
  answer: 1
  why: Win+E (the Windows key plus E) opens File Explorer from anywhere in Windows. Win+F opens the Feedback
    Hub, so it is a tempting but wrong choice.
- q: What is the fastest way to open Task Manager directly?
  options:
  - Ctrl+Alt+Del
  - Ctrl+Shift+Esc
  - Win+T
  - Alt+F4
  answer: 1
  why: Ctrl+Shift+Esc opens Task Manager directly. Ctrl+Alt+Del works too, but it shows a menu first,
    so it is one extra step.
- q: Where are a user's personal Documents, Downloads, and Desktop folders stored by default?
  options:
  - In C:\Windows
  - In C:\Program Files
  - In the user profile under C:\Users
  - On the recovery partition
  answer: 2
  why: Each account gets a profile folder at C:\Users\<name> that holds their Documents, Downloads, Desktop,
    and settings. Windows system files live in C:\Windows.
- q: Which type of account can install software and change system-wide settings?
  options:
  - Administrator
  - Standard user
  - Guest
  - Child account
  answer: 0
  why: An administrator can install programs and change settings for the whole machine. Standard users
    are limited for safety, which is why helpdesk often elevates a task rather than handing out admin
    rights.
- q: Name the Run command that displays the exact Windows version and build number.
  answer: winver
  why: Press Win+R, type winver, and press Enter. A small box shows the Windows edition, version, and
    build, which is the first thing to confirm when troubleshooting.
- q: In one sentence, what is the difference between Settings and Control Panel?
  answer: Settings is the modern Windows app for most everyday options, while Control Panel is the older
    classic interface that still holds some advanced or legacy tools.
  why: Microsoft is slowly moving everything into Settings, but technicians still open Control Panel for
    items that have not moved yet, such as some device and account tools.
resources:
- label: Microsoft Support — Getting started with Windows
  url: https://support.microsoft.com/en-us/windows
- label: Microsoft Support — Search for things in File Explorer
  url: https://support.microsoft.com/en-us/windows/find-and-open-file-explorer-ef370130-1cca-9dc5-e0df-2f7416fe1cb1
- label: Microsoft Learn — Windows client documentation
  url: https://learn.microsoft.com/en-us/windows/
- label: CompTIA A+ Certification
  url: https://www.comptia.org/certifications/a
---

## The Windows desktop

When Windows finishes loading you land on the **desktop**. Along the bottom is the **taskbar**. On the left of the taskbar is the **Start menu** button — click it (or press the **Windows key**) to find apps, settings, and a search box. Type anything into **Search** and Windows will look for apps, files, and settings at once; this is often the fastest way to open something.

At the right end of the taskbar is the **system tray** (also called the notification area). It holds small icons for things running in the background — network, volume, battery, and updates. Click the little upward arrow to see hidden icons.

## Settings vs Control Panel

Windows has **two** places to change things. **Settings** is the modern app you open from Start; it covers most everyday options like display, network, accounts, and updates. **Control Panel** is the older, classic interface. Microsoft is slowly moving everything into Settings, but some advanced tools still live only in Control Panel.

Open Control Panel quickly from the Run box:

```text
Win+R  ->  type: control  ->  Enter
```

As a technician you will use both, so get comfortable switching between them.

## File Explorer and folders

**File Explorer** is how you browse files and folders. Open it with **Win+E**. In the left pane, click **This PC** to see your drives. The main drive is the **C: drive** ("C colon"), where Windows itself is installed.

Two folders matter most:

- `C:\Windows` — Windows system files. Do not delete things here.
- `C:\Users\<your name>` — your **user profile**, holding your Documents, Downloads, and Desktop.

## User accounts

Every person who signs in has an **account**. A **local account** lives only on that PC. A **Microsoft account** signs in with an email and syncs settings across devices.

Accounts also have a permission level. A **standard user** can run apps but cannot change system-wide settings. An **administrator** can install software and change anything. For safety, most people should be standard users; admin rights are used only when needed.

## Task Manager and shortcuts

When a program freezes, open **Task Manager** with **Ctrl+Shift+Esc**. Select the stuck app and click **End task** to force it closed.

Learn these shortcuts — they make you fast:

```text
Win+E      open File Explorer
Win+R      open the Run box
Win+L      lock the screen
Alt+Tab    switch between open windows
```

From the Run box you can launch tools directly:

```powershell
winver   # shows the exact Windows version and build
cmd      # opens the Command Prompt
control  # opens Control Panel
```

## Windows Update

Keeping Windows patched closes security holes and fixes bugs. Open **Settings**, choose **Windows Update**, and click **Check for updates**. On a helpdesk, "have you installed the latest updates?" is one of your first questions.

## Your task

Open File Explorer with **Win+E** and navigate to `C:\Users` and find your own profile folder. Then press **Win+R**, type `winver`, and write down your exact Windows edition and build number. Finally, open **Settings**, go to **Windows Update**, and note whether your PC is up to date.
