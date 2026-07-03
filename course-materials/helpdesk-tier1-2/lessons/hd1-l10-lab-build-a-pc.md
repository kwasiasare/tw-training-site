---
course: helpdesk-tier1-2
title: 'Hands-on lab: build, upgrade and tear down a PC'
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 10
summary: Bring together everything from Month 1 by assembling a working PC from parts, powering it on,
  installing the operating system, and then practising an upgrade and a safe tear-down.
objectives:
- Set up a safe, anti-static workspace using an ESD strap and the part manuals
- Install the CPU, cooler, RAM, motherboard, PSU and storage in the correct order
- Connect front-panel headers, power, data and the GPU cleanly with good cable management
- Power on, complete POST, enter UEFI and set the boot order
- Install the OS and verify every component with Device Manager and systeminfo
- Upgrade the machine by adding RAM or storage, then tear it down safely in reverse order
video: hd1-l10-lab-build-a-pc.mp4
quiz:
- q: Why should you wear an anti-static (ESD) strap clipped to the case while building?
  options:
  - It speeds up the CPU
  - It drains static charge from your body so a tiny spark doesn't damage components
  - It is required to enter UEFI
  - It keeps the cables tidy
  answer: 1
  why: Electrostatic discharge can silently kill chips. An ESD strap keeps you at the same electrical
    potential as the case so static drains away harmlessly instead of arcing into a component.
- q: What is the correct early step when fitting the CPU into the motherboard socket?
  options:
  - Press down hard until it clicks flat
  - Align the gold triangle / pin-1 marker and lower it in with zero force
  - Apply thermal paste to the socket first
  - Slide it in sideways
  answer: 1
  why: Modern CPUs are keyed. You align the pin-1 triangle, drop the chip in with zero insertion force,
    then close the retention arm. Forcing it bends pins and ruins the part.
- q: After the build, which Windows tool gives a quick text summary of the installed CPU, RAM and OS?
  options:
  - systeminfo
  - ipconfig
  - chkdsk
  - taskkill
  answer: 0
  why: Running systeminfo prints a full report including processor, installed physical memory and OS version,
    making it a fast way to confirm the hardware was detected.
- q: When you tear a PC down, what is the safest general approach?
  options:
  - Remove the motherboard first
  - Yank cables to save time
  - Reverse the build order and keep screws organised by step
  - Leave it plugged into the wall
  answer: 2
  why: 'Tear-down is the build in reverse: unplug from the wall, discharge, then remove parts in the opposite
    order you installed them, keeping screws labelled so reassembly is painless.'
- q: In one sentence, what does POST do when you first power on the PC?
  answer: POST (Power-On Self-Test) is the firmware check that runs at startup to confirm the CPU, RAM
    and core hardware are present and working before handing over to the boot device.
  why: If POST fails it usually beeps or shows an error/diagnostic LED, which tells you which component
    to re-seat before you ever reach the operating system.
- q: Name the small connectors you must wire up for the case power button, reset button and activity LEDs,
    and why their orientation can matter.
  answer: The front-panel headers (often labelled F_PANEL or System Panel); the LED connectors are polarised
    so positive and negative must match the motherboard pins or the LED simply won't light.
  why: Front-panel headers are tiny and easy to get wrong; the power and reset switches work either way,
    but the LEDs only light when the plus and minus pins are oriented correctly per the manual.
resources:
- label: CompTIA — A+ certification (Core 1 220-1201) overview
  url: https://www.comptia.org/certifications/a
- label: iFixit — Repair guides and teardown techniques
  url: https://www.ifixit.com
- label: Microsoft Learn — Create installation media for Windows
  url: https://learn.microsoft.com/en-us/windows/deployment/
- label: Wikipedia — Electrostatic discharge
  url: https://en.wikipedia.org/wiki/Electrostatic_discharge
---

## Prep and safety recap

This lab pulls together everything from Month 1. Before any part comes out of its bag, get the workspace right. Work on a hard, non-carpeted surface with room to lay parts out. Wear an **ESD strap** clipped to bare metal on the case so **static** drains away instead of zapping a chip. Unplug the power supply from the wall while you build. Keep the **motherboard, CPU and RAM manuals** open — they show exactly where each connector and slot lives.

## The build order, step by step

Do the fiddly bits outside the case first, then drop the board in. A reliable order:

```text
BUILD CHECKLIST
[ ] 1. Install CPU: align pin-1 triangle, zero force, close arm
[ ] 2. Thermal paste (pea-sized) + mount the cooler
[ ] 3. Seat RAM in the correct DIMM slots until both clips snap
[ ] 4. Fit standoffs, lay I/O shield, screw motherboard into case
[ ] 5. Install the PSU and route its cables
[ ] 6. Install M.2 SSD in its slot; mount any SATA drives
[ ] 7. Connect front-panel headers (power, reset, LEDs)
[ ] 8. Connect 24-pin board power and 8-pin CPU power
[ ] 9. Install the GPU in the top PCIe slot; add its power cable
[ ] 10. Double-check everything is seated before first power-on
```

The **CPU** drops into the socket with no force — let the keying and gravity do the work. A **pea-sized** dot of **thermal paste** is plenty; the cooler spreads it. Push **RAM** into the **DIMM slots** firmly until the clips click. Use **standoffs** so the board never touches the metal tray and short out.

## Cable management and first power-on

Good **cable management** is not just looks: tidy cables improve airflow and make future upgrades easy. Route cables behind the tray and use the case tie-points. Plug the **24-pin** main power and the **8-pin CPU** power firmly.

Now power on. The firmware runs **POST** (Power-On Self-Test). If it beeps or shows a diagnostic light, re-seat RAM or power before panicking. Tap the key shown on screen (often Del or F2) to enter **UEFI**. Confirm the CPU, RAM and storage are all detected, then set the **boot order** so your install media boots first.

## Installing the OS and verifying the build

Boot from your Windows USB and follow the installer. Once Windows is up, prove every part is working.

```powershell
# Quick full summary of the machine
systeminfo

# Confirm the CPU the way A+ techs do
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores
```

Open **Device Manager** and look for any yellow warning marks — those mean a driver is missing. A clean Device Manager plus a correct `systeminfo` report means the build is solid.

## Upgrading and tearing down

To **upgrade**, add a second RAM stick in the matching slot, or install another **M.2** or SATA drive — power off and unplug first every time. **Tear-down** is simply the build in reverse: shut down, unplug from the wall, hold the power button to discharge, then remove the GPU, cables, storage, board, cooler and CPU in the opposite order. Keep **screws organised** in labelled pots per step.

## Your task

Using a real or training PC, follow the build checklist end to end: assemble it, power on, enter UEFI and set the boot order, install Windows, then run `systeminfo` and check Device Manager for any warnings. Finally, add or move one RAM stick as a practice upgrade, confirm the new total in `systeminfo`, and write down the safe tear-down order in your own words.
