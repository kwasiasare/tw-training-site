---
course: helpdesk-tier1-2
title: The command line and PowerShell essentials
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 2
summary: Move beyond clicking and learn the core Command Prompt and PowerShell commands a helpdesk tech
  uses every day. By the end you can navigate the file system, check the network and run diagnostics from
  a terminal.
objectives:
- Tell the difference between Command Prompt and PowerShell, and when to use each
- Navigate folders and manage files from the terminal
- 'Run network diagnostics: ipconfig, ping and nslookup'
- Use PowerShell cmdlets in the Verb-Noun pattern with the pipeline
- Open an elevated terminal and explain why some commands need it
- Find help for any command without leaving the terminal
video: hd3-l02-command-line-and-powershell.mp4
quiz:
- q: A user can't reach an internal web app. Which command shows their PC's IP address, subnet mask and
    default gateway?
  options:
  - ipconfig
  - ping
  - tracert
  - netstat
  answer: 0
  why: ipconfig (use /all for full detail) reports the adapter's IP address, subnet mask, default gateway
    and DNS servers — the first thing to check when connectivity fails.
- q: PowerShell commands follow a consistent naming pattern. What is it?
  options:
  - Noun-Verb (e.g. Process-Get)
  - Verb-Noun (e.g. Get-Process)
  - all lowercase single words
  - Action.Target dotted names
  answer: 1
  why: PowerShell uses Verb-Noun, like Get-Process, Stop-Service or Get-ChildItem. The predictable pattern
    makes commands easy to guess and discover with Get-Command.
- q: You want to test whether a remote host is reachable and measure round-trip time. Which command do
    you use?
  options:
  - ping
  - dir
  - cls
  - whoami
  answer: 0
  why: ping sends ICMP echo requests and reports replies with round-trip times, confirming basic reachability
    between two hosts. tracert would show the path, but ping is the quick reachability test.
- q: Which command flushes the local DNS resolver cache, a common fix when a site resolves to the wrong
    address?
  options:
  - ipconfig /renew
  - ipconfig /release
  - ipconfig /flushdns
  - ipconfig /all
  answer: 2
  why: ipconfig /flushdns clears cached DNS records so the next lookup queries the DNS server fresh. /renew
    and /release deal with DHCP leases, not DNS caching.
- q: In one sentence, why might a command like 'sfc /scannow' fail unless you open the terminal a certain
    way?
  answer: Because it changes protected system files, it must be run from a terminal opened 'as administrator'
    (elevated); a standard terminal lacks the rights and the command will fail or be denied.
  why: Many repair and system commands need elevation. Right-click Terminal/Command Prompt and choose
    Run as administrator before running them.
- q: In one sentence, what does the pipe symbol ( | ) do in PowerShell?
  answer: It passes the output of one command as the input to the next, letting you chain commands such
    as Get-Process | Sort-Object CPU.
  why: PowerShell pipes objects (not just text) between cmdlets, so you can filter, sort and format results
    by chaining commands together.
resources:
- label: Microsoft Learn — Windows commands reference
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands
- label: Microsoft Learn — Discover PowerShell (Get-Help, Get-Command)
  url: https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/02-help-system
- label: Microsoft Learn — Understanding the PowerShell pipeline
  url: https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/04-pipelines
- label: CompTIA — A+ Core 2 (220-1202) exam objectives
  url: https://www.comptia.org/certifications/a
---

## Two terminals, one keyboard

Windows ships with two command-line tools and you should know both. **Command Prompt** (cmd.exe) is the classic shell that runs traditional commands like `ipconfig` and `chkdsk`. **PowerShell** is the modern, far more powerful shell built on objects, ideal for automation. The newer **Windows Terminal** app hosts both in tabs. For most helpdesk diagnostics, either works — but PowerShell can do everything cmd can and much more.

The single most important habit: when a command repairs the system, open the terminal **as administrator**. Right-click it and choose **Run as administrator**, or press Win+X and pick the admin option.

## Getting around the file system

The basics of navigation are nearly identical in both shells:

```cmd
cd C:\Users\Sam\Documents     REM change directory
dir                            REM list contents (cmd)
mkdir reports                  REM make a folder
del oldfile.txt                REM delete a file
cls                            REM clear the screen
```

In PowerShell the same ideas use cmdlets, though friendly aliases mean `dir`, `cd` and `cls` still work:

```powershell
Get-ChildItem C:\Logs            # list folder contents
Set-Location C:\Logs            # change directory
New-Item -ItemType Directory reports
```

## Network diagnostics you'll use daily

Most "I can't connect" tickets start with three commands. First confirm the PC's own addressing:

```cmd
ipconfig /all

   IPv4 Address. . . . . . . . . . . : 192.168.1.42
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.1.1
   DNS Servers . . . . . . . . . . . : 192.168.1.1
```

Then test reachability and name resolution:

```cmd
ping 8.8.8.8
Reply from 8.8.8.8: bytes=32 time=14ms TTL=117

nslookup learn.microsoft.com
```

If a site resolves wrong, clear the cache with `ipconfig /flushdns`. For DHCP problems, `ipconfig /release` then `ipconfig /renew` grabs a fresh lease.

## The PowerShell mindset: Verb-Noun and the pipeline

Every PowerShell command follows the **Verb-Noun** pattern — `Get-Process`, `Stop-Service`, `Get-ChildItem`. Once you know that, you can guess most commands. The real power is the **pipeline** (`|`), which passes the *objects* one command produces straight into the next:

```powershell
Get-Process | Where-Object CPU -gt 100 | Sort-Object CPU -Descending

Handles  CPU(s)    Id  ProcessName
-------  ------    --  -----------
   1842  842.31  9120  chrome
    910  310.05  4477  Teams
```

That one line finds every busy process, keeps the heavy ones, and sorts them — no scripting required.

## Never get stuck: built-in help

You don't have to memorise everything. PowerShell discovers and documents itself:

```powershell
Get-Command *service*        # find commands about services
Get-Help Get-Process -Examples
```

In Command Prompt, add `/?` to most commands (e.g. `ipconfig /?`) to see their switches.

## Your task

Open Windows Terminal. In a Command Prompt tab, run `ipconfig /all` and record your IP address, default gateway and DNS server. Run `ping` against your gateway and confirm replies. Then open a PowerShell tab and run `Get-Process | Sort-Object CPU -Descending | Select-Object -First 5` to list your five busiest processes. Finally, use `Get-Help Get-Service -Examples` and read one example. Note in two lines what each command told you.
