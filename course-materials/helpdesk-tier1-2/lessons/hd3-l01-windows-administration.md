---
course: helpdesk-tier1-2
title: 'Windows administration: Settings, Control Panel & Task Manager'
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 1
summary: Learn where Windows hides its admin tools and how to move confidently between Settings, Control
  Panel and Task Manager. By the end you can find any setting, diagnose a slow PC and kill a stuck process
  like a tier 1 tech.
objectives:
- 'Choose the right tool: Settings, Control Panel or an MMC console'
- Use Task Manager to find what is eating CPU, memory and disk
- End a frozen process and manage startup apps safely
- Open admin consoles fast with Run commands and the Win+X menu
- Read basic system info to confirm edition, build and resources
- Explain when a task needs elevated (administrator) rights
video: hd3-l01-windows-administration.mp4
quiz:
- q: A user says their laptop is 'really slow today'. Which tab in Task Manager tells you fastest which
    app is the culprit?
  options:
  - Users
  - Services
  - Performance
  - Processes
  answer: 3
  why: The Processes tab sorts running apps by CPU, Memory, Disk and Network, so clicking a column header
    instantly reveals the resource hog. Performance shows totals but not which app is responsible.
- q: Which Run command opens the System Configuration utility used to manage boot options and startup?
  options:
  - msconfig
  - regedit
  - services.msc
  - dxdiag
  answer: 0
  why: msconfig launches System Configuration, where you control boot mode (including Safe Boot) and see
    services. Startup apps themselves were moved to Task Manager in Windows 8 and later.
- q: A setting exists in both modern Settings and the legacy Control Panel. For a CompTIA A+ tech, what
    is the safest general guidance?
  options:
  - Only Control Panel is ever correct
  - Settings is for phones only
  - Use modern Settings first; drop to Control Panel for legacy or advanced options
  - Never use either — edit the registry
  answer: 2
  why: Microsoft is steadily migrating options into Settings, so start there. Control Panel still holds
    deeper/legacy items (e.g. some device and admin tools), so know how to reach both.
- q: You need to disable a program that launches automatically at sign-in and slows boot. Where do you
    do this in modern Windows?
  options:
  - Control Panel > Programs
  - Task Manager > Startup apps tab
  - Device Manager
  - Disk Cleanup
  answer: 1
  why: The Startup apps tab in Task Manager lists auto-start programs with a Startup impact rating and
    a Disable button — the correct, supported place to manage them.
- q: Name the keyboard shortcut that opens Task Manager directly, without any menu.
  answer: Ctrl + Shift + Esc
  why: Ctrl+Shift+Esc opens Task Manager immediately. Ctrl+Alt+Del opens a security screen first, so the
    three-key Shift shortcut is faster on a frozen machine.
- q: In one sentence, what does it mean to run a tool 'as administrator' and when do you need it?
  answer: Running as administrator launches the tool with elevated privileges so it can change system-wide
    settings; you need it for tasks like editing services, system files or other users' settings.
  why: Windows uses User Account Control (UAC) to keep apps at standard rights by default; elevation grants
    the higher token only when a task genuinely needs system-level access.
resources:
- label: Microsoft Support — Open Task Manager
  url: https://support.microsoft.com/en-us/windows/what-is-task-manager-a7c50f4c-0d5a-4f74-9b50-32a4a1d5c5d5
- label: Microsoft Learn — Windows administrative tools
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands
- label: Microsoft Support — User Account Control settings
  url: https://support.microsoft.com/en-us/windows/user-account-control-settings-d5b2046b-dcb8-54eb-f732-059f321afe18
- label: CompTIA — A+ Core 2 (220-1202) exam objectives
  url: https://www.comptia.org/certifications/a
---

## The three places Windows keeps its controls

As a tier 1 tech you will jump between three surfaces all day. **Settings** is the modern, touch-friendly app (Win+I) where Microsoft now puts most options. **Control Panel** is the older surface that still holds legacy and advanced items. And the **MMC consoles** — small focused tools like Device Manager and Services — handle deeper administration. The rule of thumb: start in **Settings**, fall back to **Control Panel** for legacy items, and reach for a specific console when you need fine control.

Don't hunt through menus. Press **Win+R** to open the **Run** box and type the tool name directly:

```cmd
control            REM opens Control Panel
appwiz.cpl         REM Programs and Features (uninstall)
devmgmt.msc        REM Device Manager
services.msc       REM Services console
msconfig           REM System Configuration
```

The **Win+X** menu (right-click the Start button) is another fast launcher for Device Manager, Disk Management, Terminal and more.

## Task Manager: your first diagnostic stop

When a user reports a slow or frozen PC, open **Task Manager** with **Ctrl+Shift+Esc**. The **Processes** tab lists every app and background task. Click the **CPU**, **Memory** or **Disk** column header to sort, and the resource hog jumps to the top.

To kill a frozen app, select it and click **End task** (or use the command line):

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, CPU, WS

Name        CPU       WS
----        ---       --
chrome   842.31  1543200000
Teams    310.05   612000000
```

The **Performance** tab gives live graphs for CPU, memory, disk and network — useful to confirm whether the whole machine is stressed or just one app.

## Managing startup and boot

A slow boot is often caused by too many auto-start apps. Open the **Startup apps** tab in Task Manager, check the **Startup impact** column, and **Disable** the heavy ones you don't need. For boot-level changes — like enabling **Safe Boot** for troubleshooting — use **msconfig** (System Configuration), not the registry.

## Confirming the system you're working on

Before you change anything, confirm what you're looking at: edition, version and build. Right-click Start > **System**, or run:

```powershell
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

OS Name:    Microsoft Windows 11 Pro
OS Version: 10.0.22631 N/A Build 22631
```

This matters because fixes and update paths differ between editions (Home vs Pro) and builds.

## Standard vs administrator rights

Windows runs apps with **standard** rights by default. System-wide changes — editing services, touching protected files, changing another user's settings — need **elevation**. When you right-click a tool and choose **Run as administrator**, **User Account Control (UAC)** prompts you to confirm. If a setting is greyed out, the usual cause is that you didn't launch the tool elevated.

## Your task

On your own PC: open Task Manager with Ctrl+Shift+Esc, sort the Processes tab by Memory and note the top app. Switch to the Startup apps tab and disable one non-essential auto-start program. Then open the Run box, launch `msconfig`, and screenshot the Boot tab (do not change it). Finally, run `systeminfo` in a terminal and record your exact Windows edition and build. Write a 3-line note summarising what you found.
