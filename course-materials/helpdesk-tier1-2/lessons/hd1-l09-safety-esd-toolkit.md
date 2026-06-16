---
course: helpdesk-tier1-2
title: Safety, ESD and the technician's toolkit
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 9
summary: 'Learn how to protect both yourself and the hardware: control static electricity, work safely
  around electricity, dispose of components responsibly, and build the toolkit every helpdesk technician
  carries.'
objectives:
- Explain what electrostatic discharge is and why tiny static charges destroy components
- Apply ESD prevention using an anti-static wrist strap, ESD mat, and anti-static bags
- Identify electrical hazards and explain why a PSU and CRT monitor must never be opened
- Apply personal and environmental safety practices for lifting, fire, fumes, and cables
- Explain how to dispose of batteries, toner, and e-waste safely using SDS sheets
- Identify the core tools in a technician's toolkit and what each one is for
video: hd1-l09-safety-esd-toolkit.mp4
quiz:
- q: Why can a static shock you cannot even feel still destroy a computer component?
  options:
  - Components are too cheap to survive any handling
  - Sensitive chips can be damaged by far less voltage than a human can feel
  - Static only damages the case, never the chips
  - Modern parts are immune to static
  answer: 1
  why: You typically only feel static above about three thousand volts, but sensitive electronics can
    be damaged by under a hundred volts, so harmful ESD happens invisibly.
- q: Why should you never open a power supply unit or a CRT monitor?
  options:
  - The screws are glued in permanently
  - They contain capacitors that hold a dangerous charge even when unplugged
  - It voids the software licence
  - They are too heavy to open safely
  answer: 1
  why: PSUs and CRTs hold large capacitors that can store a lethal charge for a long time after being
    unplugged, so they are non-serviceable for a helpdesk technician.
- q: What is the correct way to store a spare RAM stick or expansion card?
  options:
  - In an anti-static bag
  - Loose in your trouser pocket
  - On a wool blanket
  - Taped to the side of the tower
  answer: 0
  why: Anti-static bags are designed to safely shield components from static build-up; pockets, wool,
    and carpets all generate static that can damage parts.
- q: Which practice reduces ESD risk while you work inside a PC?
  options:
  - Working on a thick carpet in socks
  - Wearing an anti-static wrist strap clipped to the chassis
  - Rubbing the parts to remove dust
  - Wearing wool gloves
  answer: 1
  why: An anti-static wrist strap bonds you to the same electrical potential as the chassis (equipotential
    bonding) so charge cannot build up and jump to a component.
- q: In one sentence, what does an SDS (Safety Data Sheet) tell a technician?
  answer: An SDS explains the hazards of a material such as toner or a battery and how to handle, store,
    and dispose of it safely.
  why: SDS sheets (formerly called MSDS) are the standard reference for handling and disposal of potentially
    hazardous materials in the workplace.
- q: Name two tools you would expect in a basic technician's toolkit and say what each is for.
  answer: 'Examples: a screwdriver set for removing case and component screws, an anti-static wrist strap
    to prevent ESD, a spudger for prying clips without scratching, a flashlight to see inside the case,
    or compressed air to clear dust.'
  why: A helpdesk toolkit mixes mechanical tools (screwdrivers, spudger), safety gear (wrist strap), and
    diagnostic tools (multimeter, cable tester) plus cleaning supplies.
resources:
- label: CompTIA — A+ Certification (Core 1 220-1101)
  url: https://www.comptia.org/certifications/a
- label: OSHA — Occupational Safety and Health Administration
  url: https://www.osha.gov
- label: Wikipedia — Electrostatic discharge
  url: https://en.wikipedia.org/wiki/Electrostatic_discharge
- label: Wikipedia — Antistatic wrist strap
  url: https://en.wikipedia.org/wiki/Antistatic_wrist_strap
---

## What is ESD and why does it matter

**Electrostatic discharge (ESD)** is the sudden flow of electricity between two objects at different charges — the tiny zap you feel touching a door handle. You only *feel* static above about **3,000 volts**, but sensitive chips inside a PC can be damaged by **less than 100 volts**. That means you can quietly destroy a part — or weaken it so it fails weeks later — without ever feeling a thing. This is why ESD is the number one hazard to the *hardware* you touch.

## Preventing ESD

The goal is to keep you and the equipment at the **same electrical potential** so no charge can jump. This is called **equipotential bonding**.

```text
ESD prevention checklist
[ ] Wear an anti-static wrist strap, clipped to bare metal on the chassis
[ ] Work on an ESD (anti-static) mat, not a carpet
[ ] Touch the metal case before handling any component
[ ] Hold cards by the edges, never the gold contacts or chips
[ ] Keep spare parts inside anti-static bags until needed
[ ] Avoid wool jumpers and shuffling on carpet in socks
```

An **anti-static wrist strap** connects your skin to the chassis through a resistor. An **ESD mat** does the same for your work surface. Together they drain static harmlessly instead of letting it build up and discharge into a chip.

## Electrical safety

Protect yourself, not just the parts. **Always power down properly and unplug the device before opening it.** Two components must **never** be opened by a helpdesk technician: the **power supply unit (PSU)** and a **CRT monitor**. Both contain large **capacitors** that store a dangerous — potentially lethal — charge for a long time *even after being unplugged*. These are non-serviceable: if one fails, you replace the whole unit.

## Personal and environmental safety

- **Lifting:** bend at the knees, keep your back straight, and get help with heavy servers or monitors.
- **Fire:** for electrical fires use a **CO2 extinguisher** (or another rated for electrical fires) — never water.
- **Fumes:** work in a ventilated space; some cleaning chemicals and overheated parts give off harmful fumes.
- **Trip hazards:** keep cables tidy and routed away from walkways. Good **cable management** is a safety measure, not just neatness.

## Proper disposal

Many IT items are hazardous waste and must **never** go in normal bins:

- **Batteries** (including the small CMOS coin cell) — recycle at proper collection points.
- **Toner and ink** — return cartridges through recycling schemes; toner powder is harmful to breathe.
- **E-waste** (old PCs, monitors, cables) — use a certified electronics recycler.

When in doubt, check the **SDS (Safety Data Sheet)**, formerly called an **MSDS**. It lists a material's hazards and how to handle, store, and dispose of it safely.

## The technician's toolkit

A good kit mixes mechanical, safety, and diagnostic tools:

- **Screwdriver set** (Phillips/flat, magnetic tip) — open cases and fasten components.
- **Spudger** — safely pry plastic clips without scratching boards.
- **Anti-static wrist strap** — your ESD protection.
- **Multimeter** — check voltages and continuity.
- **Cable tester** — confirm network cables are wired correctly.
- **Flashlight** — see inside dark cases.
- **Compressed air** — blow dust out of fans and heatsinks.
- **Thermal paste** — reapply between a CPU and its cooler.

## Your task

Write your own ESD and safety checklist (you can copy the one above and add to it). Then look around your own desk: identify at least three trip hazards or cable-management problems and note how you would fix each. Finally, list which everyday IT items in your home — old batteries, a dead phone, an ink cartridge — should be recycled as e-waste rather than thrown in the bin.
