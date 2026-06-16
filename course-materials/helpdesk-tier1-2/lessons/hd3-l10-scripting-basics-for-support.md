---
course: helpdesk-tier1-2
title: Scripting basics for support technicians
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 10
summary: 'Learn just enough scripting to automate repetitive helpdesk tasks: read input, loop over items,
  make decisions with if/else, and run a script safely in PowerShell and Bash.'
objectives:
- Explain why automating repetitive tasks reduces errors and saves time
- Store and use values in variables in PowerShell and Bash
- Loop over a list of items with foreach / for
- Make decisions in a script with if/else
- Read a file line by line and act on each line
- Run scripts safely and understand basic execution policy and permissions
video: hd3-l10-scripting-basics-for-support.mp4
quiz:
- q: What is the main reason a support technician writes scripts?
  options:
  - To make the computer run faster
  - To automate repetitive tasks consistently and avoid manual mistakes
  - To replace the operating system
  - To encrypt the hard drive
  answer: 1
  why: Scripting automates repetitive work so it runs the same way every time, which saves time and removes
    the human errors that creep into manual steps.
- q: Which PowerShell loop runs a block of code once for each item in a list?
  options:
  - foreach
  - Get-Help
  - Stop-Process
  - Set-Location
  answer: 0
  why: foreach iterates over a collection, running its block once per item; the others show help, stop
    a process, or change directory.
- q: What does an if/else statement let a script do?
  options:
  - Run faster
  - Choose between actions based on whether a condition is true
  - Delete files automatically
  - Connect to the internet
  answer: 1
  why: 'if/else branches the script: it runs one block when a condition is true and another when it is
    false, letting the script make decisions.'
- q: In PowerShell, which command reads the contents of a text file?
  options:
  - Write-Host
  - Remove-Item
  - Get-Content
  - Start-Service
  answer: 2
  why: Get-Content reads a file and returns its lines, which you can then loop over; the others print
    text, delete items, or start a service.
- q: In one sentence, what is a variable and why is it useful in a script?
  answer: A variable is a named container that stores a value (like a name, number or path) so you can
    reuse it and change it in one place instead of repeating the value throughout the script.
  why: 'Variables make scripts readable and maintainable: change the value once and every use updates,
    which avoids errors from repeating the same literal everywhere.'
- q: Why might a PowerShell script refuse to run, and how do you check the relevant setting?
  answer: The execution policy may block unsigned scripts; you check it with Get-ExecutionPolicy and,
    if appropriate and permitted, adjust it (for example to RemoteSigned) with Set-ExecutionPolicy.
  why: PowerShell's execution policy is a safety control against running untrusted scripts, so a blocked
    script usually means the policy needs checking with Get-ExecutionPolicy.
resources:
- label: Microsoft Learn — PowerShell scripting overview
  url: https://learn.microsoft.com/en-us/powershell/scripting/overview
- label: Microsoft Learn — about_Execution_Policies
  url: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies
- label: Ubuntu — The Linux command line for beginners
  url: https://ubuntu.com/tutorials/command-line-for-beginners
- label: CompTIA — A+ certification
  url: https://www.comptia.org/certifications/a
---

## Why technicians script

When you have done the same five-step fix forty times, you are not learning — you are wasting time and inviting mistakes. **Scripting** is the cure. A script is just a saved list of commands the computer runs for you, the same way every time. You do not need to be a programmer; four small ideas — **variables**, **loops**, **conditionals**, and reading **input** — cover most of the automation a Tier 1 technician needs. The two languages you will meet are **PowerShell** on Windows and **Bash** on Linux/macOS.

## Variables: name your values

A **variable** is a named box that holds a value, so you set it once and reuse it.

```powershell
$name = "Kwasi"
$logPath = "C:\Logs\app.log"
Write-Host "Checking log for $name at $logPath"
```

In Bash the same idea looks like this (note: no spaces around `=`):

```bash
name="Kwasi"
logPath="/var/log/syslog"
echo "Checking log for $name at $logPath"
```

## Loops: do it for every item

A **loop** repeats an action for each item in a list — perfect for "do this to every user" or "every file".

```powershell
$services = "Spooler", "W32Time", "BITS"
foreach ($svc in $services) {
    $state = (Get-Service $svc).Status
    Write-Host "$svc is $state"
}
```

Sample output:

```powershell
Spooler is Running
W32Time is Running
BITS is Stopped
```

## Conditionals: make decisions

An **if/else** lets the script decide. Here we restart a service only if it is stopped:

```powershell
foreach ($svc in $services) {
    if ((Get-Service $svc).Status -eq "Stopped") {
        Write-Host "$svc is stopped - starting it"
        Start-Service $svc
    } else {
        Write-Host "$svc is fine"
    }
}
```

The Bash equivalent uses `if ... then ... else ... fi` and tools like `systemctl is-active`.

## Reading input from a file

Real automation often reads a list — say, computer names — from a file. In PowerShell, **Get-Content** reads it and you loop over the lines:

```powershell
Get-Content ".\computers.txt" | foreach {
    Write-Host "Pinging $_"
    Test-Connection -ComputerName $_ -Count 1 -Quiet
}
```

The `$_` means "the current line". In Bash you would use `while read line; do ...; done < file`.

PowerShell guards against untrusted scripts with an **execution policy**. If a script refuses to run, check it:

```powershell
Get-ExecutionPolicy
# Restricted
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

On Linux you make a script runnable with `chmod +x script.sh` and run it as `./script.sh`. Always read a script before you run it, and test on a non-production machine first.

## Your task

Write a short PowerShell script that defines a list of three service names, loops over them with `foreach`, and uses `if/else` to print whether each is Running or Stopped (use `Get-Service`). Save it as `check-services.ps1` and run it; if it is blocked, check `Get-ExecutionPolicy` and note what you would change. Bonus: create a `computers.txt` file with three names, then use `Get-Content` and a loop to print each line. Write two sentences on one repetitive helpdesk task you could automate this way.
