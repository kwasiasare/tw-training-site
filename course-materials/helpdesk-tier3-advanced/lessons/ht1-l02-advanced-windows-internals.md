---
course: helpdesk-tier3-advanced
title: 'Advanced Windows internals: boot, registry, services & drivers'
month: 1
monthTitle: Advanced Troubleshooting & Root Cause Analysis
lesson: 2
summary: Understand how Windows actually boots, loads drivers, and starts services so you can reason about
  failures instead of guessing. Map the registry control sets and service dependency chains that decide
  whether a machine reaches the desktop.
objectives:
- Trace the Windows boot sequence from firmware through Session Manager to the desktop
- Explain how the registry HKLM\SYSTEM control sets and LastKnownGood are selected
- Read a driver's Start type and ErrorControl and predict its effect on boot
- Map service dependency chains and diagnose a failed dependency
- Use Autoruns and the boot/setup event logs to find what runs at startup
- Distinguish a kernel-mode driver fault from a user-mode service failure
video: ht1-l02-advanced-windows-internals.mp4
quiz:
- q: A driver has Start type 0 (Boot) and ErrorControl 3 (Critical). What happens if it fails to load?
  options:
  - Windows logs a warning and continues to the desktop
  - The system bugchecks or rolls back to LastKnownGood — boot cannot proceed
  - The driver is silently disabled until next reboot
  - It is retried as a user-mode service
  answer: 1
  why: ErrorControl 3 (Critical) forces a bugcheck or LastKnownGood rollback if a load fails; Start 0
    means the driver is needed before the kernel finishes initialising, so the system cannot just continue.
- q: Where does Windows record the control set it actually booted from?
  options:
  - HKLM\SYSTEM\Select\Current
  - HKCU\Software\Microsoft\Boot
  - HKLM\SOFTWARE\Policies\Boot
  - HKLM\HARDWARE\Description\Boot
  answer: 0
  why: HKLM\SYSTEM\Select holds Current, Default, Failed, and LastKnownGood values that point to the numbered
    ControlSet the system booted, so you can confirm which configuration is live.
- q: Service A depends on Service B, which failed to start. Which tool most directly shows you that dependency
    chain?
  options:
  - Task Manager Performance tab
  - sc.exe qc and the service's DependOnService value
  - ipconfig /all
  - chkdsk
  answer: 1
  why: sc.exe qc dumps a service's configuration including DependOnService; the Service Control Manager
    refuses to start a service whose listed dependencies have not started.
- q: Which Sysinternals tool gives the most complete view of everything configured to run at boot and
    logon, including drivers, services, and scheduled tasks?
  options:
  - Process Explorer
  - Autoruns
  - TCPView
  - RAMMap
  answer: 1
  why: Autoruns enumerates every autostart location — drivers, services, Run keys, scheduled tasks, codecs,
    more — and can verify signatures, making it the canonical startup-audit tool.
- q: In one sentence, what does Session Manager (smss.exe) do early in boot?
  answer: Smss.exe is the first user-mode process the kernel starts; it initialises the registry, creates
    paging files and environment, runs autochk, and launches the session that brings up Winlogon and the
    user environment.
  why: Knowing smss is the bridge from kernel initialisation to user-mode sessions tells you where to
    look when a machine reaches the spinner but never the logon screen.
- q: Why does reading a driver's Start type help you predict boot impact?
  answer: Start type defines when the driver loads (0 Boot, 1 System, 2 Auto, 3 Demand, 4 Disabled); a
    fault in a Boot or System driver can prevent the machine from ever reaching the desktop, whereas a
    Demand-start driver fault usually only affects the feature that triggers it.
  why: The earlier in boot a driver loads, the more catastrophic its failure, so Start type tells you
    whether a driver fault is a no-boot or a feature-level problem.
resources:
- label: Sysinternals — Autoruns documentation
  url: https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns
- label: Microsoft Learn — Advanced startup and boot options
  url: https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/windows-boot-issues-troubleshooting
- label: Microsoft Learn — Registry control sets and LastKnownGood
  url: https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/use-last-known-good-control-set-restore-system
- label: Microsoft Learn — Services and the Service Control Manager
  url: https://learn.microsoft.com/en-us/windows/win32/services/service-control-manager
---

## The boot sequence, end to end

To diagnose a machine that never reaches the desktop, you must know the order things happen. **Firmware** (UEFI) hands off to the **Windows Boot Manager** (`bootmgr`), which reads the **BCD** store and starts the **Windows OS Loader** (`winload.efi`). The loader pulls in the kernel (`ntoskrnl.exe`), the HAL, and every **Boot-start driver**. The kernel initialises, then starts **Session Manager** (`smss.exe`) — the first user-mode process. Smss sets up the registry, paging files, and environment, runs autochk, then launches the session leading to **Winlogon** and the desktop.

If a machine hangs on the spinner, the fault is usually before smss (a Boot/System driver). If it reaches the logon screen and then fails, you are in user-mode service territory.

## Control sets and LastKnownGood

The live system configuration lives under `HKLM\SYSTEM`. Windows keeps multiple numbered **control sets** and records which is which under `HKLM\SYSTEM\Select`.

```text
HKLM\SYSTEM\Select\Current        -> e.g. 1  (the ControlSet booted now)
HKLM\SYSTEM\Select\LastKnownGood  -> e.g. 1  (last config that reached logon)
HKLM\SYSTEM\Select\Failed         -> e.g. 2
```

**LastKnownGood** is updated to the current set only after a *successful* interactive logon. That is why "Last Known Good Configuration" can recover a machine that a bad driver just broke — it rolls back to the set that last reached the desktop.

## Drivers: Start type and ErrorControl

Every driver and service has a **Start** type and an **ErrorControl** value under its `Services` key:

```powershell
# Inspect a driver's load behaviour
Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Services\disk' |
  Select-Object Start, Type, ErrorControl, ImagePath
```

**Start**: 0 = Boot, 1 = System, 2 = Auto, 3 = Demand, 4 = Disabled. **ErrorControl**: 0 = Ignore, 1 = Normal, 2 = Severe, 3 = Critical. A Boot-start driver (0) with Critical error control (3) that fails will bugcheck or force a LastKnownGood rollback. A Demand-start driver (3) that fails usually only breaks the feature that needed it. Reading these two numbers tells you whether a fault is a no-boot or a nuisance.

## Services and dependency chains

Services start in dependency order under the **Service Control Manager** (SCM). If service A lists B in `DependOnService` and B fails, SCM refuses to start A.

```powershell
# Dump a service's full config including its dependencies
sc.exe qc Netlogon

# List what depends on a given service
Get-Service -Name LanmanWorkstation -DependentServices
```

A single failed low-level service can cascade into a dozen downstream failures — always trace upstream to the first thing that broke, not the loudest error.

## Auditing what actually runs

**Autoruns** from Sysinternals enumerates every autostart location: drivers, services, Run keys, scheduled tasks, codecs, and more, with signature verification. Use it to spot an unsigned or unexpected driver loading early. Pair it with the boot performance and setup logs:

```powershell
Get-WinEvent -LogName 'Microsoft-Windows-Diagnostics-Performance/Operational' |
  Where-Object Id -in 100,101,102,103 |
  Select-Object TimeCreated, Id, Message -First 20
```

## Your task

On a test VM, read `HKLM\SYSTEM\Select` and record which control set is Current and which is LastKnownGood. Pick three drivers and use `Get-ItemProperty` to list their Start and ErrorControl values; for each, predict in writing what would happen on boot if it failed to load. Run Autoruns, export the list, and identify any unsigned autostart entry. Finally, pick a multi-dependency service (e.g. Netlogon), map its dependency chain with `sc.exe qc` and `Get-Service -DependentServices`, and draw the chain.
