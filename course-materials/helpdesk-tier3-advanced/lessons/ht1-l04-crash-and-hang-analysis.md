---
course: helpdesk-tier3-advanced
title: 'Crash and hang analysis: BSODs, dumps & WinDbg basics'
month: 1
monthTitle: Advanced Troubleshooting & Root Cause Analysis
lesson: 4
summary: Turn a blue screen or a frozen application into a named root cause by reading crash dumps in
  WinDbg. Configure dump capture, resolve symbols, and run the analysis commands that point at the faulting
  module.
objectives:
- Configure Windows to capture the right dump type for kernel and user crashes
- Resolve symbols correctly so WinDbg can name modules and functions
- Run !analyze -v and interpret the bugcheck code and faulting module
- Distinguish a hang from a crash and capture a manual dump of a frozen process
- Read a basic call stack to attribute a fault to a specific driver or DLL
- Decide when a crash is a driver defect versus corrupted state versus hardware
video: ht1-l04-crash-and-hang-analysis.mp4
quiz:
- q: A machine bugchecks intermittently and you need stack and driver detail but disk space is limited.
    Which dump type is the best default for kernel crashes?
  options:
  - Complete (full) memory dump
  - Active memory dump of user pages only
  - Kernel memory dump (or Automatic)
  - No dump — rely on the event log
  answer: 2
  why: A kernel memory dump captures kernel-mode memory — enough to name the faulting driver and read
    the stack — without the size of a complete dump. Automatic dump is the modern default and sizes the
    page file accordingly.
- q: 'WinDbg shows ''*** ERROR: Module load completed but symbols could not be loaded''. What is the correct
    fix?'
  options:
  - Reinstall Windows
  - Set the symbol path to the Microsoft symbol server and reload
  - Ignore it — symbols are optional
  - Switch to a 32-bit debugger
  answer: 1
  why: Without symbols WinDbg cannot map addresses to function names. Setting .sympath to the public symbol
    server (srv*) and running .reload resolves the stack to readable names.
- q: '!analyze -v reports a bugcheck and names a third-party driver in MODULE_NAME and IMAGE_NAME. What
    is the most defensible next conclusion?'
  options:
  - The CPU is failing
  - That driver is the prime suspect for the proximate cause; verify its version and known issues
  - Windows itself is corrupt
  - The user caused it
  answer: 1
  why: MODULE_NAME/IMAGE_NAME point to the code executing at the fault. It is the prime proximate suspect
    — but a Tier 3 engineer still verifies version, signing, and known issues before declaring root cause,
    since a driver can fault on corrupted state it did not create.
- q: An application is frozen but not crashed. How do you get a dump for analysis?
  options:
  - Wait for it to crash on its own
  - Capture a user-mode dump of the live process with ProcDump or Task Manager 'Create dump file'
  - Reboot immediately
  - Delete the application
  answer: 1
  why: A hang produces no crash dump on its own. You capture the live process state — ProcDump (e.g. procdump
    -ma) or Task Manager's Create dump file — then analyse the threads and locks to see what it is waiting
    on.
- q: In one sentence, what does the bugcheck code (e.g. 0xD1 DRIVER_IRQL_NOT_LESS_OR_EQUAL) tell you?
  answer: It classifies the kind of illegal operation the kernel detected (here, a driver accessed pageable
    memory at too high an IRQL), which narrows the failure mode and often points directly at a driver
    category before you even read the stack.
  why: The bugcheck code is the kernel's classification of what rule was violated, giving you a head start
    on the failure mode and likely culprit class.
- q: Why might a crash that names a Microsoft driver still NOT be a Microsoft bug?
  answer: A faulting Microsoft driver may simply be the code that finally tripped over memory already
    corrupted by a different third-party driver upstream; the visible faulting module is the victim, so
    you read the full stack and check for other recently loaded or unsigned drivers before assigning blame.
  why: The faulting frame is where the crash surfaced, not necessarily where the corruption originated,
    so attribution requires reading the stack and surrounding context, not just MODULE_NAME.
resources:
- label: Microsoft Learn — Get started with WinDbg (kernel-mode)
  url: https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/getting-started-with-windbg--kernel-mode-
- label: Microsoft Learn — !analyze extension command
  url: https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/-analyze
- label: Sysinternals — ProcDump
  url: https://learn.microsoft.com/en-us/sysinternals/downloads/procdump
- label: Microsoft Learn — Configure system crash dump files
  url: https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/memory-dump-file-options
---

## A crash is data, not a mystery

A blue screen — a **bugcheck** — is the kernel deliberately stopping because continuing would corrupt the system. That stop produces a **crash dump**: a snapshot of memory you can read after the fact. A frozen app produces no dump on its own, but you can force one. Either way, the crash is not a mystery; it is evidence waiting for a debugger.

## Capture the right dump

Before you can analyse, you must capture. For kernel crashes the **Kernel memory dump** (or the modern **Automatic** setting) is the right default: it holds enough kernel memory to name the faulting driver and read the stack, without the disk cost of a **Complete** dump.

```powershell
# Confirm the configured dump type (CrashDumpEnabled: 1=Complete,2=Kernel,7=Automatic)
Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\CrashControl' |
  Select-Object CrashDumpEnabled, DumpFile, AutoReboot
```

Kernel dumps land at `%SystemRoot%\MEMORY.DMP`. Minidumps go to `%SystemRoot%\Minidump`.

## Symbols first, always

WinDbg maps raw addresses to function names using **symbols**. Without them every frame is a hex address and the analysis is useless. Point WinDbg at the Microsoft public symbol server before anything else.

```text
.sympath srv*C:\symbols*https://msdl.microsoft.com/download/symbols
.reload /f
```

If you ever see *"symbols could not be loaded"*, fix the symbol path and `.reload` — do not interpret a stack until names resolve.

## !analyze -v: the first real command

The workhorse is `!analyze -v` ("analyze, dash v" for verbose). It decodes the **bugcheck code**, identifies the likely **faulting module**, and prints the stack at the point of failure.

```text
!analyze -v

*** look for these lines ***
BUGCHECK_CODE:  D1            (DRIVER_IRQL_NOT_LESS_OR_EQUAL)
MODULE_NAME:    somedriver
IMAGE_NAME:     somedriver.sys
FAILURE_BUCKET_ID: ...
```

The bugcheck code classifies *what rule was broken*. `MODULE_NAME`/`IMAGE_NAME` name the code executing at the fault — your prime proximate suspect. But stay disciplined: a faulting module can be the *victim* of corruption another driver caused upstream. Read the full stack with `k`, and check for recently loaded or unsigned drivers with `lm` before assigning root cause.

## Hangs: capture the frozen state

A hang never bugchecks, so you capture the live process. Use **ProcDump** or Task Manager's *Create dump file*.

```text
procdump -ma <pid-or-name> C:\evidence\hang.dmp
```

Open the user-mode dump, run `!analyze -v -hang`, and inspect threads with `~*k` to see what each is waiting on — a lock, a remote call, or a deadlock between two threads. Look for a thread blocked inside a critical section while another thread owns it: that ownership cycle is the signature of a classic deadlock, and the call stacks usually name the component responsible.

## Your task

On a test VM, confirm the configured dump type via the `CrashControl` registry key and set it to Automatic if it is not. Trigger or obtain a kernel dump (a test crash, or an existing MEMORY.DMP), open it in WinDbg, set the symbol path to the public server, and run `!analyze -v`. Record the bugcheck code, the named module, and the top of the stack from `k`. Then capture a user-mode dump of a deliberately hung process with ProcDump, run `~*k`, and write one sentence on what the main thread was waiting on. Conclude with whether your evidence points to a driver defect, corrupted state, or hardware.
