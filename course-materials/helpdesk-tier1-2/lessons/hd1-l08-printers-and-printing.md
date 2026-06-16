---
course: helpdesk-tier1-2
title: Printers and printing
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 8
summary: Learn the main printer types and how laser printing works, then connect, manage, and troubleshoot
  printers like a helpdesk technician using Windows tools and PowerShell.
objectives:
- Explain the differences between inkjet, laser, thermal, and 3D printers
- Describe the seven steps of the laser printing process at a high level
- Connect a printer over USB, network IP, wireless, or as a shared printer
- Explain the role of printer drivers and the Windows print spooler
- Troubleshoot common faults like paper jams, streaks, stuck spoolers, and offline printers
- 'Identify the right consumables: toner for laser, ink for inkjet'
video: hd1-l08-printers-and-printing.mp4
quiz:
- q: Which printer type uses a laser, a charged drum, and heat to fuse toner onto paper?
  options:
  - Inkjet printer
  - Thermal printer
  - Laser printer
  - Dot-matrix printer
  answer: 2
  why: A laser printer charges a drum, uses a laser to write the image, attracts powdered toner, then
    fuses it to the paper with heat and pressure. Inkjets spray liquid ink instead.
- q: A user reports their printer shows as 'Offline' even though it is powered on. What is a sensible
    FIRST check?
  options:
  - Replace the toner cartridge
  - Check the cable or network connection and that the printer is set as default
  - Reinstall Windows
  - Buy a new printer
  answer: 1
  why: Offline usually means Windows cannot reach the printer. Check the USB cable or network/Wi-Fi connection
    first before touching consumables or doing anything drastic.
- q: What does the Windows print spooler service do?
  options:
  - It fuses toner to the paper
  - It manages and queues print jobs being sent to printers
  - It refills the ink tanks
  - It scans documents into the computer
  answer: 1
  why: The spooler (Spooler service) accepts print jobs, queues them, and feeds them to the printer in
    order. If it gets stuck, restarting the service clears the jam.
- q: Which command lists the printers installed on a Windows machine?
  options:
  - Get-Printer
  - Show-Printers
  - List-Devices
  - Print-Status
  answer: 0
  why: Get-Printer is the PowerShell cmdlet that returns the installed printers and their status, a quick
    first step when diagnosing printing problems.
- q: In one sentence, what is the difference between toner and ink?
  answer: Toner is the dry powder used by laser printers and fused with heat, while ink is the liquid
    used by inkjet printers and sprayed onto the page.
  why: 'Knowing which consumable a printer uses tells you what to order and what causes faults: dry toner
    streaks versus wet ink smudges or clogged nozzles.'
- q: A print job is stuck in the queue and nothing prints. Name a PowerShell command that often fixes
    this.
  answer: Restart-Service -Name Spooler (after optionally clearing stuck jobs with Get-PrintJob / Remove-PrintJob).
  why: Restarting the Spooler service clears a hung queue so jobs can flow again; it is one of the most
    common helpdesk printing fixes.
resources:
- label: Microsoft Support — Fix printer connection and printing problems in Windows
  url: https://support.microsoft.com/en-us/windows/fix-printer-connection-and-printing-problems-in-windows-f6bed0d6-2356-3b9c-6fa6-b9a9b2db8c8e
- label: Microsoft Learn — Get-Printer (PrintManagement) PowerShell reference
  url: https://learn.microsoft.com/en-us/powershell/module/printmanagement/get-printer
- label: CompTIA A+ Certification
  url: https://www.comptia.org/certifications/a
- label: Wikipedia — Laser printing
  url: https://en.wikipedia.org/wiki/Laser_printing
---

## Printer types you'll meet on the helpdesk

Most printers fall into a few families. An **inkjet** printer sprays tiny droplets of liquid **ink** onto the page; they are cheap to buy, great for photos, but the ink can smudge and nozzles clog if unused. A **laser** printer uses a laser, a drum, and powdered **toner** fused with heat; they are fast, sharp for text, and cheaper per page in busy offices. A **thermal** printer uses heat to darken special paper or melt a ribbon and is common for **receipts, labels, and shipping**. A **3D** printer is a different beast entirely: it builds physical objects layer by layer from melted plastic filament. As a Tier 1 tech, you'll spend most of your time on laser and inkjet office printers.

## How a laser printer actually works

Laser printing follows **seven steps** in order. You don't need to memorise the physics, but knowing the sequence helps you locate a fault:

1. **Processing** — the printer receives the job and builds the page image in memory.
2. **Charging** — a uniform negative charge is applied to the rotating drum.
3. **Exposing** — the laser writes the image by discharging spots on the drum.
4. **Developing** — toner sticks to the discharged areas, forming the image.
5. **Transferring** — the toner image is moved onto the paper.
6. **Fusing** — heat and pressure melt the toner so it bonds permanently.
7. **Cleaning** — leftover toner and charge are wiped so the drum is ready again.

A repeating mark or **streak** down every page often points to a damaged drum or dirty fuser.

## Connecting printers

There are four common connection methods. **USB** is a direct cable to one PC — simplest, but only that PC can print. **Network / IP** printers sit on the LAN with their own **I P address**, so anyone on the network can reach them. **Wireless (Wi-Fi)** printers join the network without a cable. A **shared** printer is one PC's local printer that it shares out to others. For network printers, knowing the IP lets you browse to the printer's web page or add it directly.

## Drivers and the print spooler

Windows needs a **driver** — software that translates documents into the printer's language. The **print spooler** is a Windows service that accepts jobs, queues them, and feeds them to the printer one at a time. When printing breaks, these two are the usual suspects. List printers and the queue with PowerShell:

```powershell
Get-Printer
Get-PrintJob -PrinterName "Office-Laser"
```

## Common issues and quick fixes

**Paper jams** — power off, gently remove paper in the direction of travel, check for torn scraps. **Streaks or faded print** — low or faulty toner/ink, or a dirty drum. **Stuck spooler** — jobs pile up and nothing prints; clear the queue and restart the service. **Offline printer** — Windows can't reach it; check the cable, Wi-Fi, or IP, and confirm it's the default printer. To clear a hung queue:

```powershell
Get-PrintJob -PrinterName "Office-Laser" | Remove-PrintJob
Restart-Service -Name Spooler
```

## Consumables

Match the supply to the printer: **laser printers use toner cartridges** (dry powder), **inkjets use ink cartridges or tanks** (liquid). Ordering the wrong one is a common Tier 1 mistake. Always note the exact model number before ordering.

## Your task

On a Windows PC, open PowerShell and run `Get-Printer` to list the installed printers. Pick one, run `Get-PrintJob -PrinterName "<name>"` to view its queue, then practise restarting the spooler with `Restart-Service -Name Spooler`. Write down the printer's connection type (USB, network IP, or wireless) and whether it uses toner or ink.
