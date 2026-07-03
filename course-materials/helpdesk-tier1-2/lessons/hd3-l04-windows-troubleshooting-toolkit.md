---
course: helpdesk-tier1-2
title: The Windows troubleshooting toolkit
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 4
summary: Build a mental toolbox of the core Windows repair tools and learn when to reach for each one.
  By the end you can read Event Viewer, repair system files, check disks and memory, and boot into Safe
  Mode with confidence.
objectives:
- Apply a logical troubleshooting order instead of guessing
- Use Event Viewer to find the error behind a vague symptom
- Repair corrupt system files with sfc and DISM
- Check disks and memory with chkdsk and Windows Memory Diagnostic
- Use Safe Mode and System Restore to recover a broken PC
- Document the cause and fix so the next tech benefits
video: hd3-l04-windows-troubleshooting-toolkit.mp4
quiz:
- q: A PC shows random crashes. Where do you look first to find the underlying error messages logged by
    Windows?
  options:
  - Disk Cleanup
  - Event Viewer
  - Snipping Tool
  - Calculator
  answer: 1
  why: Event Viewer records System, Application and Security logs. Filtering for Errors and Critical events
    around the crash time usually reveals the offending component or driver.
- q: You suspect corrupt protected system files are causing instability. Which command scans and repairs
    them?
  options:
  - chkdsk /f
  - ipconfig /all
  - sfc /scannow
  - tasklist
  answer: 2
  why: sfc /scannow (System File Checker) scans protected system files and restores correct versions.
    If sfc can't fix the underlying component store, you then run DISM.
- q: sfc reports it could not repair some files. What is the correct next step before re-running sfc?
  options:
  - Reinstall Windows immediately
  - Run DISM /Online /Cleanup-Image /RestoreHealth to repair the component store
  - Run chkdsk to format the disk
  - Disable the antivirus permanently
  answer: 1
  why: DISM repairs the underlying Windows image / component store that sfc draws from. After DISM completes,
    re-running sfc /scannow can then succeed.
- q: A user reports the PC won't start normally after installing a bad driver. Which startup option loads
    Windows with a minimal set of drivers so you can remove it?
  options:
  - Full Screen Mode
  - Sleep Mode
  - Safe Mode
  - Airplane Mode
  answer: 2
  why: Safe Mode boots Windows with only essential drivers and services, letting you uninstall the bad
    driver or run repairs without the faulty component loading.
- q: In one sentence, what does chkdsk /f do and why might it ask to run at next restart?
  answer: chkdsk /f checks the disk for file-system errors and fixes them; it schedules itself for restart
    when the volume is in use (such as the system drive) because it needs exclusive access to repair it.
  why: A volume that is currently in use can't be locked, so chkdsk defers to the next boot when it can
    get exclusive access to the drive.
- q: In one sentence, why should you document the root cause and fix at the end of a troubleshooting job?
  answer: So the resolution is searchable for the next technician and the same problem can be recognised
    and fixed faster, or prevented entirely.
  why: Documentation closes the loop in the troubleshooting methodology and turns one solved ticket into
    reusable knowledge for the whole team.
resources:
- label: Microsoft Learn — Use the System File Checker tool (sfc)
  url: https://learn.microsoft.com/en-us/troubleshoot/windows-server/deployment/system-file-checker
- label: Microsoft Learn — Repair a Windows image with DISM
  url: https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/repair-a-windows-image
- label: Microsoft Support — Start your PC in Safe Mode in Windows
  url: https://support.microsoft.com/en-us/windows/start-your-pc-in-safe-mode-in-windows-92c27cff-db89-8644-1ce4-b3e5e56fe234
- label: CompTIA — A+ Core 2 (220-1202) exam objectives
  url: https://www.comptia.org/certifications/a
---

## Troubleshoot in order, don't guess

Good techs don't randomly try fixes — they follow a method. Identify the **problem** and gather symptoms, form a **theory** of the likely cause, **test** the theory, fix it, **verify** full functionality, and finally **document** what you did. The tools below slot into that flow: most begin with *finding the evidence* before changing anything.

A quick triage habit: ask what changed. New driver, new update, new app, or new hardware right before the problem started is your strongest lead.

## Event Viewer: find the real error

Vague symptoms ("it just crashes") hide specific errors in the logs. Open **Event Viewer** (`eventvwr.msc`) and look under **Windows Logs > System** and **Application**. Filter for **Error** and **Critical** around the time of the fault.

```powershell
Get-EventLog -LogName System -EntryType Error -Newest 5
# Get-EventLog exists only in Windows PowerShell 5.1. In PowerShell 7 use:
# Get-WinEvent -FilterHashtable @{ LogName='System'; Level=2 } -MaxEvents 5

Index Time          Source        Message
----- ----          ------        -------
 4821 Jun 16 09:14  disk          The device has a bad block.
 4810 Jun 16 09:02  Service Ctrl  A service terminated unexpectedly.
```

That "bad block" line instantly points you at the disk — now your testing is targeted, not guesswork.

## Repairing system files: sfc then DISM

When Windows itself behaves oddly, suspect corrupt **system files**. Run **System File Checker** from an elevated terminal:

```cmd
sfc /scannow

Verification 100% complete.
Windows Resource Protection found corrupt files and successfully repaired them.
```

If sfc reports it *couldn't* repair everything, the underlying component store is damaged. Repair it with **DISM**, then run sfc again:

```cmd
DISM /Online /Cleanup-Image /RestoreHealth
```

## Disk and memory checks

For file-system errors or a failing drive, run **chkdsk**. With `/f` it fixes errors; on the system drive it schedules itself for the next restart because it needs exclusive access.

```cmd
chkdsk C: /f
```

For random crashes that smell like bad RAM, run **Windows Memory Diagnostic**:

```cmd
mdsched
```

It restarts the PC and tests memory before Windows loads, then reports results after boot.

## Recovery: Safe Mode and System Restore

When Windows won't start normally — often after a bad driver — boot into **Safe Mode**, which loads only essential drivers so you can remove the culprit. You reach it from `msconfig` (Boot tab > Safe boot) or the recovery menu. If a recent change broke things, **System Restore** rolls protected system files and settings back to an earlier **restore point** without touching personal files.

The last step of the method is **documentation**. Note the symptom, the root cause, and the exact fix. One solved ticket then becomes searchable knowledge that helps the whole team solve the next one faster.

## Your task

On a test PC, open Event Viewer and find one Error or Warning in the System log — note its Source and time. Open an elevated terminal and run `sfc /scannow`, then record the result line. (Do not run chkdsk /f on your only drive unless you can reboot.) Finally, open `msconfig`, look at the Boot tab and confirm where you would enable Safe boot — then write a short 'troubleshooting note' documenting an imaginary crash: symptom, the log evidence you'd look for, and the tool you'd use to fix it.
