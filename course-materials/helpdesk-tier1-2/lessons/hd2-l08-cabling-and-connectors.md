---
course: helpdesk-tier1-2
title: Cabling and connectors
month: 2
monthTitle: Networking Foundations (Network+)
lesson: 8
summary: 'Get hands-on with the physical layer: copper and fibre cables, the connectors that terminate
  them, twisted-pair categories, and how to spot a cabling fault.'
objectives:
- Identify copper twisted-pair, coaxial, and fibre-optic cable types
- Match Ethernet categories (Cat5e, Cat6, Cat6a) to their speeds
- Recognise common connectors like RJ45, LC and SC
- Explain the difference between single-mode and multimode fibre
- Describe maximum cable lengths and why they matter
- Diagnose physical-layer faults such as a bad cable or run length
video: hd2-l08-cabling-and-connectors.mp4
quiz:
- q: What connector is used on standard Ethernet twisted-pair cabling?
  options:
  - RJ11
  - RJ45
  - BNC
  - LC
  answer: 1
  why: RJ45 is the 8-pin connector used to terminate twisted-pair Ethernet cables; RJ11 is the smaller
    phone connector.
- q: What is the maximum recommended length for a copper Ethernet run?
  options:
  - 10 metres
  - 55 metres
  - 100 metres
  - 500 metres
  answer: 2
  why: Twisted-pair Ethernet is rated to 100 metres (about 328 feet); beyond that, signal degrades and
    you need fibre or a repeater/switch.
- q: Which cable category is required for reliable 10 Gigabit Ethernet over 100 m?
  options:
  - Cat3
  - Cat5
  - Cat5e
  - Cat6a
  answer: 3
  why: Cat6a supports 10 Gigabit Ethernet over the full 100 metres; Cat6 manages 10G only over shorter
    runs, and Cat5e tops out at 1 Gigabit.
- q: What is the key advantage of fibre-optic cable over copper?
  options:
  - It is cheaper
  - It carries data as light over much longer distances and is immune to electromagnetic interference
  - It needs no connectors
  - It only works indoors
  answer: 1
  why: Fibre transmits light, so it travels far greater distances, supports higher speeds, and is immune
    to the electromagnetic interference that affects copper.
- q: Name the fibre type used for long-distance runs with a laser light source.
  answer: Single-mode fibre
  why: Single-mode fibre has a tiny core and uses laser light to travel very long distances, while multimode
    uses LED/VCSEL light over shorter runs.
- q: In one sentence, how would you quickly test whether a dead network port is a cable fault?
  answer: Swap the suspect cable for a known-good one, or plug the device into a known-good port, to isolate
    whether the cable or the port is the problem.
  why: Substituting a known-good cable or port is the fastest way to confirm or rule out a physical-layer
    fault at the bottom of the OSI model.
resources:
- label: Wikipedia — Twisted pair (Cat5e/Cat6/Cat6a)
  url: https://en.wikipedia.org/wiki/Twisted_pair
- label: Wikipedia — Optical fiber connector
  url: https://en.wikipedia.org/wiki/Optical_fiber_connector
- label: Cloudflare Learning Center — What is fiber optics?
  url: https://www.cloudflare.com/learning/network-layer/what-is-fiber-optics/
- label: Cisco — Ethernet cabling basics
  url: https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/networking-basics.html
---

## The physical layer is real

Everything we have discussed rides on **Layer 1** — actual cables and connectors. A surprising share of helpdesk tickets are pure physical faults: a damaged cable, a loose connector, or a run that is simply too long. Knowing the cable types lets you fix these fast instead of chasing ghosts higher up the stack.

## Copper twisted-pair

The workhorse of office networking is **twisted-pair** copper cable, terminated with an **RJ45** connector. The twists cancel out electrical interference. Cables come in **categories** that determine speed:

```text
Cat5e   1 Gbps    up to 100 m
Cat6    1 Gbps (10 Gbps over short runs)   100 m
Cat6a   10 Gbps   up to 100 m
```

The golden rule: a copper Ethernet run maxes out at **100 metres**. Beyond that, the signal weakens and the link fails or runs slowly — a classic cause of "the far office is always dropping." You will also meet **UTP** (unshielded) and **STP** (shielded) variants, where shielding helps in electrically noisy environments.

## Coaxial cable

**Coaxial** cable has a single copper core inside shielding and was common in older networks and cable TV/broadband. It uses **BNC** or **F-type** connectors. You will rarely cable a new LAN with coax, but you will see F-type where a cable ISP enters the building.

## Fibre-optic cable

**Fibre** carries data as pulses of **light** instead of electricity. That gives it three big wins: far greater **distance**, much higher **speed**, and complete **immunity to electromagnetic interference**. There are two types:

- **Single-mode** — tiny core, laser light, very long distances (between buildings, across campuses).
- **Multimode** — larger core, LED/VCSEL light, shorter distances (within a building or data centre).

Fibre uses small connectors like **LC** and **SC**. Fibre is more fragile and pricier to terminate, so it is used for backbones and long runs rather than to every desk.

## Diagnosing physical faults

Physical faults sit at the bottom of the OSI model, so check them first. Symptoms include no **link light**, intermittent drops, or very slow speeds. The fastest test is **substitution**: swap in a known-good cable, or move the device to a known-good port. A **cable tester** confirms continuity and correct wiring. Always check the obvious before anything clever:

```text
[ ] Is the cable fully seated and clicked in at both ends?
[ ] Is there a link light on the switch port and the NIC?
[ ] Is the run under 100 m?
[ ] Does a known-good cable fix it?
```

## Your task

Find an Ethernet cable near you and read the printing along its jacket — it usually states the **category** (e.g. "CAT6"). Note it down. Then inspect the **RJ45** connector and the **link lights** where it plugs into your PC or switch. Finally, write down the substitution steps you would use to prove whether a dead port is caused by a faulty cable.
