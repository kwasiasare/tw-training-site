---
course: helpdesk-tier3-advanced
title: Performance analysis and bottleneck hunting
month: 1
monthTitle: Advanced Troubleshooting & Root Cause Analysis
lesson: 3
summary: Find the real bottleneck behind 'the machine is slow' by measuring CPU, memory, disk, and the
  often-missed resources. Capture and read an Event Tracing for Windows profile with WPR and WPA.
objectives:
- Decompose 'slow' into a measurable bottleneck across CPU, memory, disk, and GPU
- Use Performance Monitor counters to distinguish saturation from latency
- Identify hard page faults and committed-memory pressure versus working-set churn
- Capture a CPU and disk profile with Windows Performance Recorder (WPR)
- Open and read the trace in Windows Performance Analyzer (WPA) to find the hot stack
- Tell a genuine resource bottleneck apart from a scheduling or contention problem
video: ht1-l03-performance-analysis.mp4
quiz:
- q: A machine feels slow but CPU sits at 30%, RAM at 50%, and disk queue is low. Which resource is the
    most likely culprit you have NOT yet measured?
  options:
  - Page file size
  - Total installed RAM
  - Number of CPU cores
  - Disk latency / per-IO response time, or GPU and network waits
  answer: 3
  why: Low utilisation with poor responsiveness points to latency, not saturation — a disk that is idle
    but answering each IO slowly, or waits on GPU/network. Utilisation percentages alone never reveal
    latency.
- q: Which PerfMon counter best indicates memory pressure forcing the system to hit disk?
  options:
  - Memory\Available MBytes only
  - Memory\Pages/sec combined with hard faults (page reads/sec)
  - Processor\% Idle Time
  - System\Processes
  answer: 1
  why: Hard page faults — pages read from disk because they were paged out — are the real cost. Pages/sec
    alongside hard fault rate reveals the system thrashing; Available MBytes alone can look fine while
    paging hurts.
- q: What does Windows Performance Recorder (WPR) actually capture?
  options:
  - A static snapshot of running processes
  - A memory dump for WinDbg
  - Event Tracing for Windows (ETW) events including sampled CPU stacks and disk IO
  - Only network packets
  answer: 2
  why: WPR drives ETW providers to record a time-based trace — sampled CPU call stacks, context switches,
    disk and file IO, and more — which WPA then analyses. It is a trace, not a snapshot or a dump.
- q: In WPA, you see a thread spending most of its time in 'Ready' but not 'Running'. What does that indicate?
  options:
  - The thread is CPU-bound and saturating a core
  - The thread is runnable but waiting for a CPU — a scheduling/contention problem, not raw CPU shortage
  - The thread has crashed
  - The disk is the bottleneck
  answer: 1
  why: Time in Ready means the thread could run but no core was available to it — a contention or priority
    issue. That is a different fix from a thread genuinely burning CPU in Running state.
- q: Name one reason high CPU utilisation can still mean the CPU is NOT the bottleneck.
  answer: The CPU may be busy spinning on a lock, handling interrupts/DPCs from a misbehaving driver,
    or busy-waiting on slow IO — so it looks saturated while the real constraint is contention or a downstream
    device, not compute capacity.
  why: Utilisation measures busyness, not useful work; high CPU from lock contention, interrupt storms,
    or busy-waiting is a symptom of a different root cause.
- q: Why capture a timed WPR trace instead of just reading Task Manager?
  answer: Task Manager shows instantaneous, aggregated utilisation; a WPR/ETW trace records the actual
    call stacks, context switches, and IO over time, so you can see which module and which stack is consuming
    the resource and whether the cost is CPU, wait, or IO.
  why: Root cause needs the responsible stack and the wait analysis over time, which only a trace provides
    — Task Manager tells you something is busy, not what or why.
resources:
- label: Microsoft Learn — Windows Performance Recorder (WPR)
  url: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder
- label: Microsoft Learn — Windows Performance Analyzer (WPA)
  url: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer
- label: Microsoft Learn — Performance Monitor and counters
  url: https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/tools/perfmon
- label: Sysinternals — Process Explorer
  url: https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer
---

## 'Slow' is not a measurement

The word **slow** is a symptom, never a cause. Your first job is to turn it into a number: which resource is constrained, and is the problem **saturation** (the resource is maxed out) or **latency** (the resource is idle but answering slowly)? These have opposite fixes, and utilisation percentages alone cannot tell them apart. A disk at 5% busy that takes 40 ms per IO will make a machine feel terrible while every dashboard looks green.

## The four-resource sweep, plus the ones people miss

Start with the obvious four — **CPU, memory, disk, network** — but go beyond utilisation. For each, ask both *how busy* and *how slow per operation*.

```text
CPU     : % usage, but also queue length and DPC/interrupt time
Memory  : Available MB, AND hard page-fault rate (paging to disk)
Disk    : % busy, AND avg sec/transfer (latency per IO)
Network : throughput, AND round-trip latency and retransmits
```

Then check the ones people forget: **GPU** (compositor and rendering waits), **handle/thread leaks**, and **lock contention**. A process climbing in handles or threads over hours is a leak you will only see by trending.

## Counters that reveal the truth

Performance Monitor exposes the diagnostic counters Task Manager hides.

```powershell
# Sample the high-value counters once a second for 30 seconds
Get-Counter -Counter '\Processor(_Total)\% Processor Time',
  '\Memory\Available MBytes',
  '\Memory\Pages/sec',
  '\PhysicalDisk(_Total)\Avg. Disk sec/Transfer',
  '\System\Processor Queue Length' -SampleInterval 1 -MaxSamples 30
```

Memory pressure shows up as **hard page faults** (`Pages/sec` driven by reads from disk), not as low Available MB alone. A persistently non-zero `Processor Queue Length` means threads are waiting for a core — contention, not raw CPU shortage.

## Capturing a real profile with WPR

Utilisation tells you *something* is busy; a trace tells you *what* and *why*. **Windows Performance Recorder (WPR)** drives **Event Tracing for Windows (ETW)** to capture sampled CPU stacks, context switches, and disk IO over time.

```powershell
# Start a CPU + disk profile, reproduce the slowness, then stop
wpr -start CPU -start DiskIO
# ... reproduce the slow operation now ...
wpr -stop C:\evidence\slow.etl
```

## Reading it in WPA

Open the `.etl` in **Windows Performance Analyzer (WPA)**. In the CPU Usage (Sampled) graph, expand by process then by stack to find the **hot stack** — the call path consuming the most samples. Crucially, read the thread states: time in **Running** is real CPU work; time in **Ready** means the thread was runnable but starved of a core (contention); time in **Waiting** points at IO or a lock. A thread mostly in Ready is a scheduling problem, not a CPU-capacity problem — a completely different fix.

## Your task

Reproduce a slow scenario on a test machine (or run a CPU/IO-heavy workload). Capture 30 seconds of the PerfMon counters above with `Get-Counter` and decide whether you are seeing saturation or latency. Then capture a WPR trace covering the slow operation, open it in WPA, and identify the hot stack and the dominant thread state (Running, Ready, or Waiting). Write a two-paragraph finding: name the constrained resource, classify it as saturation vs latency vs contention, and state the responsible module from the stack.
