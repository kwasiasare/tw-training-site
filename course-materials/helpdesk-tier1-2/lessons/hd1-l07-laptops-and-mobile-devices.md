---
course: helpdesk-tier1-2
title: Laptops & mobile devices
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 7
summary: Learn how laptops differ from desktops, identify the parts that make them portable, and understand
  power, batteries, docking, and the common faults you will support on a helpdesk.
objectives:
- Explain the trade-offs between laptops and desktops (portability, power, repairability)
- 'Identify laptop-specific parts: Li-ion battery, SODIMM RAM, M.2 storage, integrated display, Fn keys,
  touchpad'
- Describe how laptops are powered and charged, including AC adapters and USB-C Power Delivery
- Explain what a docking station does and when to use one
- 'Compare mobile device types: smartphones, tablets, and 2-in-1s'
- Diagnose common laptop issues such as overheating, won't charge, and a dim screen
video: hd1-l07-laptops-and-mobile-devices.mp4
quiz:
- q: Which RAM form factor is designed for laptops because it is physically smaller than a desktop module?
  options:
  - SODIMM
  - DIMM
  - DDR socket
  - Riser card
  answer: 0
  why: SODIMM (Small Outline DIMM) is the compact memory module used in laptops; full-size DIMMs are used
    in desktops and would not fit a laptop's tight chassis.
- q: A user's laptop is plugged in but the battery says "plugged in, not charging" and the device feels
    very hot. What is the most likely first thing to check?
  options:
  - Reinstall the operating system
  - Airflow and vents — overheating can pause charging, and blocked vents cause it
  - Replace the motherboard
  - Buy a new monitor
  answer: 1
  why: Heat and blocked vents are common, cheap-to-fix causes; dust-clogged fans and vents make a laptop
    run hot and can stop the battery charging. Always check the simple, physical things first.
- q: What does USB-C Power Delivery (PD) let a laptop do?
  options:
  - Only transfer files, never power
  - Increase the CPU clock speed
  - Charge over the same USB-C cable that also carries data and video
  - Replace the battery entirely
  answer: 2
  why: USB-C PD negotiates higher voltages and currents so a single USB-C cable can charge the laptop
    while also moving data and video, which is why many modern laptops charge from a USB-C dock or phone
    charger.
- q: Why are laptops generally harder to repair and upgrade than desktops?
  options:
  - They use no real components
  - They run a different operating system
  - They have no storage
  - Parts are smaller, tightly packed, and often soldered to the board
  answer: 3
  why: To stay thin and light, laptops pack components tightly and increasingly solder RAM and storage
    to the motherboard, so upgrades and repairs are limited compared with a roomy, modular desktop.
- q: What does the Fn (Function) key on a laptop keyboard do?
  answer: It is a modifier key that, when held with another key (often the F1-F12 row), triggers a secondary
    action such as adjusting screen brightness, volume, Wi-Fi, or the external display.
  why: Laptops cram many controls onto few keys, so Fn unlocks a second layer of hardware shortcuts printed
    on the keys, like brightness, volume, and toggling the touchpad or wireless.
- q: Name one thing a user can do to look after a Li-ion laptop battery's long-term health.
  answer: Avoid keeping it at extreme charge or heat — for example don't leave it constantly at 100% in
    a hot place; keeping it cool and roughly between 20% and 80% helps it last longer.
  why: Lithium-ion batteries age faster under high heat and when held at very high or very low charge
    for long periods, so moderate charge levels and good cooling extend their useful life.
resources:
- label: CompTIA A+ Certification (220-1201 / 220-1202)
  url: https://www.comptia.org/certifications/a
- label: Microsoft Learn — powercfg command-line options
  url: https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/powercfg-command-line-options
- label: Wikipedia — Lithium-ion battery
  url: https://en.wikipedia.org/wiki/Lithium-ion_battery
- label: Wikipedia — SO-DIMM
  url: https://en.wikipedia.org/wiki/SO-DIMM
---

## Laptop vs desktop: the trade-offs

A **laptop** packs a whole computer — screen, keyboard, trackpad, battery, and all the internals — into one portable shell. A **desktop** spreads those parts across a roomy case with separate monitor and keyboard. The difference is all about trade-offs.

- **Portability:** laptops win — you can carry them anywhere and run on battery.
- **Power & cooling:** desktops win — bigger cases mean faster parts and better airflow.
- **Repairability & upgrades:** desktops win — parts are modular and easy to swap, while laptops are tightly packed and increasingly have RAM and storage **soldered** to the board.

On a helpdesk you will support far more laptops than you might expect, so knowing their quirks matters.

## Laptop-specific parts

Laptops use shrunk-down versions of familiar components:

- **Battery** — a rechargeable **Lithium-ion (Li-ion)** pack that powers the laptop unplugged.
- **SODIMM RAM** — a **Small Outline DIMM**, the compact memory stick laptops use instead of full-size desktop DIMMs.
- **M.2 storage** — a small stick-shaped SSD that plugs flat onto the board, replacing bulky 2.5-inch drives.
- **Integrated display** — the screen is built in and connected by a delicate ribbon cable.
- **Function (Fn) key** — a modifier that unlocks a second layer of shortcuts (brightness, volume, Wi-Fi) printed on the keys.
- **Touchpad** — the built-in pointing surface that replaces a mouse.

## Power & charging

Most laptops charge from an **AC adapter** (the "power brick") that converts wall power to low-voltage DC. Each adapter supplies a specific wattage — too weak an adapter may run the laptop but not charge it.

Modern laptops increasingly charge over **USB-C Power Delivery (USB-C PD)**, where a single USB-C cable carries power, data, and video at once. That is why one charger can power a phone, tablet, or laptop.

A **docking station** turns a laptop into a desk setup: connect one cable and you instantly get power, monitors, wired network, and USB devices. Great for staff who roam but want a full workstation at their desk.

## Mobile devices

Beyond laptops you will support:

- **Smartphones** — pocket computers with cellular data and touchscreens.
- **Tablets** — larger touchscreens, often with optional keyboards.
- **2-in-1s** — laptops whose screens detach or fold back to act as a tablet.

These share laptop concerns: Li-ion batteries, limited repairability, and wireless connectivity.

## Battery health & common issues

Li-ion batteries age with **heat** and with sitting at very high or very low charge. Keep devices cool and avoid leaving them pinned at 100% in hot spots. Windows can produce a detailed battery report:

```powershell
powercfg /batteryreport
```

That saves an HTML file showing design capacity versus current full-charge capacity — a great way to prove a battery is worn out. You can also query the battery quickly:

```powershell
Get-CimInstance Win32_Battery
```

Common faults to recognise:

- **Overheating** — dust-clogged fans and vents; clean airflow and check it isn't on a soft surface.
- **Won't charge** — try a known-good adapter and cable, check the port for debris, and confirm it isn't simply too hot.
- **Dim screen** — check the brightness Fn keys first, then the power plan and display ribbon.

## Your task

On a Windows laptop, open PowerShell and run `powercfg /batteryreport`. Open the saved HTML file and find the **design capacity** and the **full charge capacity**. Write down both numbers and work out roughly how much battery health has been lost. Then run `Get-CimInstance Win32_Battery` and note the battery status.
