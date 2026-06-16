---
course: helpdesk-tier1-2
title: 'Operating systems overview: Windows, macOS, Linux & mobile'
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 5
summary: 'Learn what an operating system actually does, then compare the four you will support every day
  on a helpdesk: Windows, macOS, Linux, and the mobile systems Android and iOS.'
objectives:
- Explain what an operating system does, including the kernel, drivers, and file management
- Compare a graphical user interface (GUI) with a command line interface (CLI)
- Identify the main desktop operating systems and where each is commonly used
- Compare Windows editions (Home vs Pro) and the NTFS file system
- Describe the difference between Android and iOS on mobile devices
- Check the operating system name and version from a terminal
video: hd1-l05-operating-systems-overview.mp4
quiz:
- q: What is the core part of an operating system that manages memory, the CPU, and hardware called?
  options:
  - The browser
  - The kernel
  - The driver
  - The desktop
  answer: 1
  why: The kernel is the central part of the OS that controls memory, the processor, and access to hardware.
    Drivers, the desktop, and the browser all sit above it.
- q: A small business runs accounting software, joins computers to a company network domain, and wants
    BitLocker drive encryption. Which Windows edition fits best?
  options:
  - Windows Pro
  - Windows Home
  - Windows Mobile
  - Windows RT
  answer: 0
  why: Windows Pro adds business features like domain join, Group Policy, and BitLocker encryption that
    Windows Home does not include.
- q: Which statement about Linux is correct?
  options:
  - It is made only by Apple for Apple hardware
  - It only runs on phones
  - It is open source, free to use, and common on servers
  - It cannot run a graphical desktop
  answer: 2
  why: Linux is open source and free, comes in many distributions such as Ubuntu, and is extremely common
    on servers. It can run with or without a graphical desktop.
- q: Which mobile operating system is closed source and runs only on Apple devices?
  options:
  - Android
  - Ubuntu Touch
  - Chrome OS
  - iOS
  answer: 3
  why: iOS (and iPadOS) is Apple's closed, controlled system that runs only on Apple hardware. Android
    is open source and used by many manufacturers.
- q: In one sentence, explain the difference between a GUI and a CLI.
  answer: A GUI (graphical user interface) lets you point and click on windows, icons, and menus, while
    a CLI (command line interface) lets you type text commands for the computer to run.
  why: Both control the same OS. The GUI is friendlier for everyday use; the CLI is faster and scriptable,
    which is why helpdesk and admin work often uses it.
- q: Why does it matter to a helpdesk technician that an operating system has reached end of support (end
    of life)?
  answer: An out-of-support OS no longer receives security updates, so it becomes a serious security risk
    and usually must be upgraded or replaced.
  why: Vendors set a support lifecycle. Once an OS is past end of life it stops getting patches, leaving
    known vulnerabilities open, so techs track these dates and plan upgrades.
resources:
- label: Microsoft Learn — Windows documentation
  url: https://learn.microsoft.com/en-us/windows/
- label: CompTIA — A+ certification
  url: https://www.comptia.org/certifications/a
- label: Apple Support — macOS User Guide
  url: https://support.apple.com/guide/mac-help/welcome/mac
- label: Ubuntu — Official desktop documentation
  url: https://ubuntu.com/desktop
---

## What an operating system actually does

An **operating system** (OS) is the master program that sits between you and the hardware. Without it, a PC is just metal and silicon. The OS does several big jobs at once: it manages memory and the **CPU**, talks to hardware through **drivers**, organises your files, and controls who is allowed to do what through **user accounts**.

The heart of the OS is the **kernel**. The kernel decides which program gets the processor, how memory is shared, and how requests reach the hardware. You never click on the kernel directly — everything else is built on top of it.

## GUI vs CLI, drivers, and files

You interact with an OS in two main ways. A **GUI** (graphical user interface) is the windows, icons, and menus you click. A **CLI** (command line interface) is a text prompt where you type commands. Both control the same machine; the CLI is faster for repetitive admin tasks and is a core helpdesk skill.

A **driver** is a small piece of software that teaches the OS how to talk to a specific device — a printer, a graphics card, a webcam. **File management** is how the OS stores and finds your data, using a **file system** to organise folders and permissions.

## Windows: the business standard

**Windows** is by far the most common OS in business, so you will support it most. Two editions matter for the exam:

- **Windows Home** — for everyday personal use.
- **Windows Pro** — adds business features: domain join, Group Policy, and **BitLocker** encryption.

Windows uses the **NTFS** file system, which supports large drives, permissions, and encryption. You can check the version in seconds:

```powershell
Get-ComputerInfo | Select-Object OsName, OsVersion
```

Or simply run `winver` to pop up a version window.

## macOS and Linux

**macOS** is Apple's desktop OS and runs only on **Apple hardware**. It is **Unix-based**, which means it shares a heritage with Linux and has a powerful built-in terminal. You will see it on designers' and executives' machines.

**Linux** is **open source** and **free**. Instead of one product, it comes in many **distributions** (distros) such as **Ubuntu**, Debian, and Fedora. Linux dominates **servers** and cloud computing because it is stable, lightweight, and free to deploy at scale.

## Mobile operating systems

Phones and tablets run their own systems. **Android** is **open source**, made by Google, and used by many manufacturers (Samsung, Google, and others). **iOS** (and **iPadOS** on tablets) is **closed source** and runs only on Apple devices, giving Apple tight control over the experience.

## Choosing an OS and the support lifecycle

There is no single "best" OS — you choose based on the job: Windows for business apps, macOS for Apple-centric creative work, Linux for servers and developers. Just as important is the **vendor lifecycle**: every OS reaches **end of support** (end of life), after which it stops receiving security updates. A technician must track these dates, because an unsupported OS is a security risk that needs upgrading or replacing.

## Your task

On the computer in front of you, open a terminal and find out exactly which OS and version you are running. On Windows, open **PowerShell** and run `Get-ComputerInfo | Select-Object OsName, OsVersion`, then also try `winver`. On macOS or Linux, open the terminal and run `uname -a`. Write down the OS name and version, then look up online whether that version is still in support — and note its end-of-life date if you can find it.
