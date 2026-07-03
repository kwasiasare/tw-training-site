---
course: helpdesk-tier1-2
title: 'How a computer works: hardware, software & the boot process'
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 1
summary: 'See the big picture of a computer: how hardware and software work together, and exactly what
  happens from the moment you press the power button until the desktop appears.'
objectives:
- Explain the difference between hardware and software in plain terms
- Describe the input-process-output-storage model every computer follows
- List the main stages of the boot process in order
- Identify the role of the BIOS/UEFI firmware and the operating system
- Recognise the four core hardware components and what each one does
- Use the right vocabulary to describe a computer to a customer or colleague
video: hd1-l01-how-a-computer-works.mp4
quiz:
- q: Which statement best describes the difference between hardware and software?
  options:
  - Hardware is the programs; software is the physical parts
  - Hardware is the physical parts you can touch; software is the instructions that run on it
  - They are two words for the same thing
  - Hardware only exists on laptops; software only on desktops
  answer: 1
  why: Hardware is the physical equipment (CPU, RAM, drives, screen). Software is the coded instructions,
    such as the operating system and apps, that tell the hardware what to do.
- q: What is the first piece of code that runs when you press the power button?
  options:
  - The operating system
  - Your web browser
  - The firmware (BIOS/UEFI) stored on the motherboard
  - The antivirus program
  answer: 2
  why: Before any operating system loads, the motherboard's firmware (BIOS or modern UEFI) runs first.
    It performs the POST and then locates and hands off to the boot device.
- q: 'The simple model that describes what every computer does is best summarised as:'
  options:
  - Input, process, output, storage
  - Download, upload, refresh
  - Compile, link, execute
  - Open, save, close
  answer: 0
  why: Computers take input, process it with the CPU, produce output, and keep data in storage. This four-part
    model fits everything from a calculator to a server.
- q: What does POST check during boot?
  options:
  - Your internet speed
  - That essential hardware like RAM and the CPU is present and working
  - Which websites you visited last
  - The price of the components
  answer: 1
  why: POST stands for Power-On Self-Test. The firmware quickly checks core hardware before loading the
    operating system; failures are often signalled by beep codes or on-screen errors.
- q: In your own words, what is the role of the operating system once the computer has booted?
  answer: The operating system manages the hardware and resources and provides a platform so the user
    and applications can run, giving you a desktop, files, and a way to launch programs.
  why: 'After firmware hands off, the OS (Windows, macOS, Linux) takes control: it manages memory, the
    CPU, storage, devices, and presents the interface you actually use.'
- q: Name the four core hardware components found in nearly every computer.
  answer: CPU (processor), RAM (memory), storage (drive), and the motherboard, usually powered by a power
    supply.
  why: 'These are the essentials: the CPU does the work, RAM holds active data, storage keeps data when
    powered off, and the motherboard connects everything together.'
resources:
- label: CompTIA A+ Certification (220-1201 & 220-1202) overview
  url: https://www.comptia.org/certifications/a
- label: Microsoft Learn — How does a computer work?
  url: https://learn.microsoft.com/en-us/training/
- label: Wikipedia — Booting
  url: https://en.wikipedia.org/wiki/Booting
- label: Wikipedia — UEFI (Unified Extensible Firmware Interface)
  url: https://en.wikipedia.org/wiki/UEFI
---

## Hardware vs software

Every computer is two things working together. **Hardware** is the physical equipment you can touch: the processor, memory, drives, screen, keyboard, and the board that links them. **Software** is the set of coded instructions that tells the hardware what to do — the **operating system** and the apps you run.

A useful way to remember it: hardware is the *body*, software is the *thoughts and instructions*. Neither is useful without the other. As a helpdesk technician, half your job is deciding whether a problem is hardware or software, so this distinction matters from day one.

## The model behind every computer

No matter how big or small, a computer follows the same loop: **input → process → output → storage**.

- **Input**: data comes in (keyboard, mouse, microphone, network).
- **Process**: the **CPU** does the calculations and decisions.
- **Output**: results go out (screen, speakers, printer).
- **Storage**: data is kept for later (drive) or held briefly while in use (**RAM**).

A calculator, a phone, and a data-centre server all follow this exact pattern.

## The four core components

Nearly every machine has four essentials:

- **CPU** (the processor) — does the actual work.
- **RAM** (memory) — fast, temporary workspace for whatever is running right now.
- **Storage** (HDD or SSD) — keeps your files when the power is off.
- **Motherboard** — the main board that connects everything, fed by the **power supply**.

We will open each of these up in later lessons. For now, just learn the names.

## The boot process, step by step

When you press the power button, a precise sequence runs:

1. **Power** flows from the power supply to the motherboard.
2. The motherboard **firmware** (**BIOS** on older PCs, **UEFI** on modern ones) starts first.
3. Firmware runs **POST** (Power-On Self-Test) to confirm RAM, CPU and other essentials are present and healthy.
4. Firmware finds the **boot device** (usually the main drive) and loads the **bootloader**.
5. The bootloader starts the **operating system**.
6. The OS loads drivers and shows you the **login screen** and **desktop**.

If POST fails, you may hear **beep codes** or see an error before any OS appears — a strong clue the problem is hardware.

## BIOS/UEFI and the operating system

Think of **firmware** as the building's caretaker who unlocks the doors and checks the lights work, then hands the keys to the **operating system** — the manager who actually runs the place. You can usually enter firmware settings by tapping a key like **Del**, **F2**, or **F10** right after powering on.

You can confirm key system facts from inside Windows once it boots:

```powershell
systeminfo | findstr /B /C:"OS Name" /C:"System Type" /C:"BIOS Version"
```

## Your task

Watch a computer boot and narrate the stages out loud. Power on a PC and tap the firmware key (often **Del** or **F2**) to peek at the BIOS/UEFI screen, then exit without changing anything. Once Windows loads, open PowerShell, run the `systeminfo` command above, and write down the OS name, system type, and BIOS version. In two sentences, describe what happened between pressing power and seeing the desktop.
