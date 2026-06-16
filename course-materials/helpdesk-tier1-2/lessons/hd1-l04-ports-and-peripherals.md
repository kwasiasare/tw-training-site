---
course: helpdesk-tier1-2
title: Ports, connectors & peripherals
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 4
summary: Learn to recognise the common ports on a PC by their shape, and understand the cables and peripherals
  that plug into them. This is bread-and-butter knowledge for any helpdesk technician.
objectives:
- Identify common ports (USB-A, USB-C, HDMI, DisplayPort, RJ45, 3.5mm) by their shape
- Explain the difference between USB versions and the speeds they offer
- 'Connect the right peripheral to the right port: keyboard, mouse, monitor, webcam, headset'
- Describe what a docking station does and when to use one
- Recognise legacy ports such as VGA, DVI and PS/2 when you meet older equipment
- List connected USB and PnP devices from Windows PowerShell
video: hd1-l04-ports-and-peripherals.mp4
quiz:
- q: Which port is small, oval, reversible (works either way up), and can carry power, video and data?
  options:
  - USB-A
  - USB-C
  - RJ45
  - HDMI
  answer: 1
  why: USB-C is the small oval reversible connector. Because it is reversible there is no wrong way up,
    and a single USB-C port can carry power, video and data at the same time.
- q: A user wants to plug a wired network cable into their laptop. Which port do they need?
  options:
  - 3.5mm jack
  - DisplayPort
  - RJ45 (Ethernet)
  - VGA
  answer: 2
  why: RJ45 is the square-ish 8-pin Ethernet port with a little clip. It is wider than a phone jack and
    is used for wired network connections.
- q: Which of these is a VIDEO connector commonly found on monitors and TVs?
  options:
  - HDMI
  - RJ45
  - PS/2
  - 3.5mm
  answer: 0
  why: HDMI carries digital video and audio and is the most common modern display connector. RJ45 is networking,
    PS/2 is legacy keyboard/mouse, and 3.5mm is analogue audio.
- q: Which connector is the older blue D-shaped video port with 15 pins that carries an analogue signal
    only?
  options:
  - USB-C
  - HDMI
  - DisplayPort
  - VGA
  answer: 3
  why: VGA is the legacy blue 15-pin D-shaped port. It carries analogue video only (no audio) and is being
    replaced by HDMI and DisplayPort.
- q: In one sentence, how can you tell USB-A apart from USB-C just by looking?
  answer: USB-A is the flat rectangular connector that only fits one way up, while USB-C is the small
    rounded oval connector that is reversible and fits either way.
  why: Shape is the fastest way to identify a port. USB-A is rectangular and one-way; USB-C is oval and
    reversible.
- q: What is a docking station and why is it useful on a helpdesk?
  answer: A docking station is a hub a laptop connects to (often by a single USB-C or Thunderbolt cable)
    that adds extra ports such as Ethernet, multiple monitors, USB and power, so a user can connect everything
    with one click.
  why: Docks let a user plug in once and instantly connect monitors, network, keyboard, mouse and power,
    which is why they are common on office desks and a frequent support topic.
resources:
- label: USB-IF — Official USB Implementers Forum (USB types & speeds)
  url: https://www.usb.org
- label: CompTIA A+ Certification (Core 1 220-1101)
  url: https://www.comptia.org/certifications/a
- label: Microsoft Learn — Get help with USB-C on Windows
  url: https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/
- label: Wikipedia — USB-C connector
  url: https://en.wikipedia.org/wiki/USB-C
---

## Why ports matter on a helpdesk

A huge share of helpdesk tickets are simply "my monitor won't display" or "my mouse stopped working". Nine times out of ten the fix is knowing **which cable goes in which hole**. If you can identify a port by its **shape**, you can solve these in seconds. Let's learn the common ones.

## USB: the universal connector

**USB** (Universal Serial Bus) is the most common port you'll meet. There are two shapes you must know:

- **USB-A** — the flat **rectangular** connector that only fits one way up (everyone flips it three times). Used for keyboards, mice, flash drives.
- **USB-C** — a small **oval, reversible** connector. No wrong way up. It can carry data, video and power all at once.

USB also comes in **versions** that set the speed. **USB 2.0** is slow (often a black plug). **USB 3.x** is faster (often a **blue** plug). **Thunderbolt** uses the USB-C shape but is even faster and can drive monitors and external drives. Tip: blue inside the port usually means it's a faster USB 3 port.

## Video ports: getting a picture on screen

When a monitor shows "No Signal", check the video cable. The common ones:

- **HDMI** — flat with slightly tapered corners; carries **video and audio**. Most common today.
- **DisplayPort** — similar size to HDMI but with one **squared-off** corner; great for high refresh rates.
- **VGA** — old **blue D-shaped** port with 15 pins; **analogue video only**, no sound.
- **DVI** — older white connector with many pins; a step between VGA and HDMI.

## Audio, networking, legacy and power

- **3.5mm jack** — the round headphone/microphone hole. Green is usually output, pink is microphone.
- **RJ45 (Ethernet)** — squarish 8-pin port with a clip, for **wired networking**. Looks like a fat phone socket.
- **PS/2** — round **purple (keyboard)** or **green (mouse)** legacy ports on older desktops.
- **Power** — desktops use a **barrel** plug or a power lead; many modern laptops charge over **USB-C**.

## Peripherals and docking stations

**Peripherals** are the devices users plug in: **keyboard**, **mouse**, **monitor**, **webcam**, **headset**. Most modern ones use USB-A, USB-C or wireless (Bluetooth/USB dongle).

A **docking station** lets a laptop connect to lots of things with **one cable**. The user plugs in a single USB-C or Thunderbolt lead and instantly gets Ethernet, two monitors, USB devices and charging. Docks are common on office desks and a frequent support topic.

## Listing devices in PowerShell

When a USB device misbehaves, you can list what Windows currently sees. Open **PowerShell** and run:

```powershell
Get-PnpDevice -PresentOnly | Where-Object Class -eq 'USB'
```

To see everything Windows detects (not just USB):

```powershell
Get-PnpDevice -PresentOnly | Select-Object Class, FriendlyName, Status
```

If a device shows a Status of `Error`, that's a strong clue where the problem is.

## Your task

Walk over to a PC (or use a photo of one). Identify and write down **at least five ports** by shape: USB-A, USB-C, HDMI, RJ45 and a 3.5mm jack. Then open PowerShell, run `Get-PnpDevice -PresentOnly | Where-Object Class -eq 'USB'`, and note one USB device it lists.
