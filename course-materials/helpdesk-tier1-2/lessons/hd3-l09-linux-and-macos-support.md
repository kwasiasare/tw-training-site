---
course: helpdesk-tier1-2
title: Linux and macOS support basics
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 9
summary: 'Get comfortable supporting the two non-Windows systems you will meet: navigate and manage a
  Linux box from the terminal, and handle common macOS tasks for Apple users.'
objectives:
- Navigate a Linux filesystem and inspect files from the terminal
- Use sudo and chmod to manage permissions safely
- Install and update software with a package manager like apt
- Check disk, memory and processes with df, top and ps
- Perform common macOS support tasks and manage software with Homebrew
- Know where logs and settings live on Linux and macOS
video: hd3-l09-linux-and-macos-support.mp4
quiz:
- q: Which command changes the permissions on a file in Linux?
  options:
  - chmod
  - chdir
  - chkdsk
  - chgenv
  answer: 0
  why: chmod (change mode) sets the read, write and execute permissions on a file or directory; the others
    change directory, check a Windows disk, or are not real commands.
- q: What does prefixing a command with sudo do?
  options:
  - Runs it silently
  - Runs it as the superuser (root) for that command
  - Schedules it for later
  - Sends it to another computer
  answer: 1
  why: sudo (superuser do) runs a single command with administrative/root privileges, which is the safe
    way to perform admin tasks without logging in as root.
- q: On a Debian/Ubuntu system, which command installs a package and its dependencies?
  options:
  - yum install
  - brew install
  - sudo apt install
  - Install-Package
  answer: 2
  why: On Debian and Ubuntu the apt package manager handles installs; sudo apt install <package> downloads
    and installs the package with its dependencies.
- q: A Mac user's application won't quit normally. What is the standard macOS way to force it to close?
  options:
  - Ctrl+Alt+Delete
  - Force Quit (Cmd+Option+Esc) or kill from Activity Monitor
  - Restart the router
  - Reinstall macOS
  answer: 1
  why: macOS uses Force Quit, reached with Command-Option-Escape or from Activity Monitor, to close an
    unresponsive app — there is no Ctrl+Alt+Delete on a Mac.
- q: In one sentence, explain what df and top tell you on a Linux machine.
  answer: df shows how much disk space is used and free on each filesystem, while top shows the running
    processes with their live CPU and memory usage.
  why: df is for storage capacity and top is for live performance and what's consuming CPU/RAM — two of
    the first things you check when a Linux box is slow or full.
- q: Where would you look first to investigate a problem on a Linux server?
  answer: In the system and application logs, typically under /var/log (for example /var/log/syslog or
    with the journalctl command on systemd systems).
  why: Linux records events and errors in /var/log and the systemd journal, so that's the first place
    a technician checks to see what actually went wrong.
resources:
- label: Ubuntu — The Linux command line for beginners
  url: https://ubuntu.com/tutorials/command-line-for-beginners
- label: man7.org — Linux manual pages (chmod, ps, df)
  url: https://man7.org/linux/man-pages/
- label: Apple Support — If an app freezes or quits unexpectedly on Mac
  url: https://support.apple.com/en-us/102254
- label: CompTIA — A+ certification
  url: https://www.comptia.org/certifications/a
---

## Why you need more than Windows

Not every machine on the helpdesk runs Windows. Developers, designers and servers run **Linux** and **macOS**, and a confident technician can support all three. The good news: both Linux and macOS share a **Unix** heritage, so the terminal skills you learn here work on both. Once you are comfortable at a shell, a strange-looking system stops being intimidating.

## Moving around Linux

Everything in Linux is a file, and you navigate from the terminal. The essentials:

```bash
pwd            # print working directory
ls -la         # list everything, long format, including hidden files
cd /var/log    # change directory
cat syslog     # show a file's contents
```

Sample output:

```bash
$ ls -la
drwxr-xr-x  2 root root 4096 Jun 16 09:01 .
-rw-r--r--  1 user user  220 Jun 16 08:55 notes.txt
```

That `drwxr-xr-x` string is the **permissions** — read, write, execute for the owner, group and everyone else.

## Permissions, sudo and packages

To change permissions you use **chmod**; to act as the administrator (**root**) for one command you prefix it with **sudo**. To install software on Debian/Ubuntu you use the **apt** package manager.

```bash
chmod +x script.sh           # make a script executable
sudo apt update              # refresh the package list
sudo apt install htop        # install a package and its dependencies
```

Using `sudo` for single commands — rather than logging in as root — is the safe Linux equivalent of least privilege.

## Checking health: disk, memory, processes

When a Linux box is slow or full, three commands answer most questions:

```bash
df -h          # disk space used/free, human-readable
top            # live processes by CPU/memory (press q to quit)
ps aux         # snapshot of all running processes
```

Sample output:

```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   42G  5.2G  90% /
```

Ninety percent full explains a lot. For deeper investigation, logs live in **/var/log** (or via `journalctl` on modern systems).

## Supporting macOS

macOS is Unix underneath, so the same terminal commands work in **Terminal.app**. Day to day you will also use the graphical tools: **Activity Monitor** (the Mac equivalent of Task Manager), **Force Quit** (Cmd+Option+Esc) for a frozen app, **Disk Utility** for drives, and **Time Machine** for backups. For installing developer tools, many Mac users rely on **Homebrew**:

```bash
brew update              # refresh Homebrew
brew install wget        # install a package
brew list                # what's installed
```

You can also read and change hidden settings with `defaults`:

```bash
defaults write com.apple.finder AppleShowAllFiles -bool true
killall Finder           # apply the change
```

## Your task

Get to a Linux shell (a VM, WSL on Windows, or a Raspberry Pi) and do the following: run `pwd`, `ls -la`, and `df -h`, and note your home directory and how full the disk is. Create a file, then use `chmod +x` to make it executable and confirm the permissions changed. Use `sudo apt update` (or your distro's package manager) to refresh the package list. If you have access to a Mac, open Activity Monitor, find the most CPU-hungry process, and write one sentence on what it is and whether it looks normal.
