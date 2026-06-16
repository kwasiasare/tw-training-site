---
course: helpdesk-tier1-2
title: 'Inside the PC: CPU, RAM, motherboard & power supply'
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 2
summary: 'Open up the computer and meet the four parts that make it run: the CPU that does the thinking,
  the RAM that holds work in progress, the motherboard that connects everything, and the power supply
  that feeds it all.'
objectives:
- Explain what the CPU does, including cores, clock speed, and sockets
- Describe RAM as volatile memory and identify DIMM versus SODIMM modules
- Identify the motherboard's chipset, slots, connectors, and form factors
- Explain power supply wattage, common connectors, and PSU safety rules
- View your own CPU and RAM details from the Windows command line
- Match each component to the job it does in a working PC
video: hd1-l02-inside-the-pc.mp4
quiz:
- q: What is the main job of the CPU?
  options:
  - Store files permanently when the power is off
  - Carry out the instructions that make programs run
  - Supply electricity to the other parts
  - Display the picture on the monitor
  answer: 1
  why: 'The CPU (Central Processing Unit) is the ''brain'': it executes the instructions of every program.
    Permanent storage is the drive''s job, electricity is the PSU''s job, and the picture comes from the
    GPU.'
- q: Why is RAM described as 'volatile' memory?
  options:
  - It can catch fire easily
  - It loses everything it holds when power is removed
  - It can only be read, never written
  - It is the fastest storage in the PC and keeps data forever
  answer: 1
  why: Volatile means RAM only holds data while it is powered. Switch the PC off and RAM is wiped, which
    is why unsaved work is lost in a power cut.
- q: Which motherboard form factor is the larger, full-size standard?
  options:
  - Mini-ITX
  - Micro-ATX
  - ATX
  - SODIMM
  answer: 2
  why: ATX is the full-size standard board with the most slots and ports. Micro-ATX is smaller, Mini-ITX
    is the smallest, and SODIMM is a type of RAM module, not a board size.
- q: What does the wattage rating on a power supply (PSU) tell you?
  options:
  - The maximum power it can deliver to the components
  - How fast the CPU can run
  - How much storage the drive has
  - The screen resolution it supports
  answer: 0
  why: Wattage is the total power the PSU can supply. A build with a power-hungry CPU and GPU needs a
    higher-wattage PSU so it does not run short.
- q: Name the type of RAM module used in laptops (the smaller form factor).
  answer: SODIMM
  why: SODIMM (Small Outline DIMM) is the compact RAM module used in laptops and small PCs, while full-size
    desktops use DIMM modules.
- q: Give one safety reason you should never open or repair a power supply unit.
  answer: PSUs contain capacitors that can store a dangerous high-voltage charge even after the unit is
    unplugged, so opening one risks a serious electric shock.
  why: Technicians replace a faulty PSU as a whole sealed unit; they never open it. The stored charge
    in its capacitors can injure or kill even when the PC is off and unplugged.
resources:
- label: CompTIA — A+ Certification (Core 1 & Core 2)
  url: https://www.comptia.org/certifications/a
- label: Crucial — What is RAM and how does it work?
  url: https://www.crucial.com/articles/about-memory/support-what-does-computer-memory-do
- label: Intel — What is a CPU and what does it do?
  url: https://www.intel.com/content/www/us/en/products/docs/processors/what-is-a-cpu.html
- label: Wikipedia — Motherboard form factor
  url: https://en.wikipedia.org/wiki/Computer_form_factor
---

## The four parts that make a PC "go"

Open any desktop computer and, past the cables, you will always find the same core team working together. The **CPU** does the thinking, the **RAM** holds the work you are doing right now, the **motherboard** connects everything, and the **power supply** feeds the whole machine. Learn these four and the inside of a PC stops being a mystery.

## The CPU: the brain

The **CPU** (Central Processing Unit) carries out the instructions that make programs run. Three words describe it on a spec sheet. **Cores** are independent workers inside one chip; a 4-core CPU can juggle four jobs at once, so more cores help with multitasking. **Clock speed**, measured in **gigahertz (GHz)**, is how many cycles of work it does per second, so higher is generally faster. The **socket** is the shaped slot on the motherboard the CPU drops into. The socket must match the CPU exactly — an Intel chip will not fit an AMD socket, and vice versa.

The CPU runs hot, so it always sits under a **heatsink and fan** (or a liquid cooler). Never run a PC with that cooler removed.

## RAM: the desk you work on

**RAM** (Random Access Memory) is fast, short-term memory. Think of it as your desk: the bigger the desk, the more papers (programs and files) you can have open at once. RAM is **volatile**, which means it is wiped the moment power is lost — that is why unsaved work vanishes in a crash. **Capacity** is measured in **gigabytes (GB)**; 8 GB is a sensible minimum and 16 GB is comfortable today. Desktop RAM comes on **DIMM** modules; laptops use the smaller **SODIMM**. Installing modules in matched pairs enables **dual-channel**, which lets the CPU reach memory faster.

## The motherboard: the connector of everything

The **motherboard** is the big circuit board everything else plugs into. Its **chipset** manages the traffic between the CPU, memory, and devices. It carries **slots** (the CPU socket, RAM slots, and **PCIe** slots for cards like a graphics card) and **connectors** (for storage, USB, and front-panel buttons). Boards come in **form factors** — sizes that decide how much fits and which case they need. **ATX** is the full-size standard, **Micro-ATX** is smaller, and **Mini-ITX (mITX)** is the tiny one.

## The power supply: feed it safely

The **power supply unit (PSU)** converts wall power into the steady low voltages the parts need. Its **wattage** rating (for example 550 W) is the most power it can deliver — a gaming PC with a hungry CPU and GPU needs more than an office PC. The PSU connects with a large **24-pin** plug to the board, a **CPU power** plug, and **SATA/PCIe** plugs for drives and cards. **Safety rule: never open a PSU.** Its capacitors can hold a dangerous charge even when unplugged. A faulty PSU is replaced as a whole sealed unit, never repaired.

## See your own hardware

You do not need to open the case to read your specs. Open **PowerShell** and ask Windows directly:

```powershell
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, MaxClockSpeed
Get-CimInstance Win32_PhysicalMemory | Select-Object Capacity, Speed
```

Or use the classic one-liner that prints a full system report:

```text
systeminfo
```

## Your task

On your own PC, run the two `Get-CimInstance` commands above. Write down your CPU name, its number of cores, its clock speed in GHz, and your total RAM in GB. Then state in one sentence whether your machine uses DIMM or SODIMM memory and how you can tell (desktop versus laptop).
