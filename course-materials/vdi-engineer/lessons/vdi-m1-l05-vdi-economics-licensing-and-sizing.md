---
course: vdi-engineer
title: 'VDI Economics: Cost Drivers, Licensing, and Sizing Basics'
month: 1
monthTitle: VDI & EUC Foundations
lesson: 5
summary: This closing lesson of Module 1 gives you the economic literacy every EUC engineer needs before
  touching a budget conversation. You'll learn the real cost drivers behind a VDI deployment (compute,
  storage, egress, licensing), how Windows and platform licensing actually works for VDI (per-user entitlements
  via Microsoft 365/Windows Enterprise E3+, Citrix and Omnissa subscription models), the density and sizing
  basics (vCPU-to-user ratios, RAM, IOPS) that determine how many users a host can serve, and how to frame
  an on-premises vs. cloud TCO conversation honestly.
objectives:
- List the four major cost drivers in a VDI deployment and explain what makes each one variable vs. fixed
- Explain the Windows per-user licensing requirement for VDI and which Microsoft entitlements satisfy
  it
- Describe how Citrix and Omnissa subscription licensing models generally work at a category level
- Explain vCPU-to-user density ratios and why they differ by workload persona
- Identify RAM and storage IOPS as sizing constraints distinct from vCPU count
- Frame an honest on-premises vs. cloud VDI TCO comparison, including hidden costs on both sides
quiz:
- q: Which of the following is a Windows licensing requirement that specifically applies to running Windows
    10/11 Enterprise virtual desktops for corporate users?
  options:
  - Users must be covered by a qualifying per-user entitlement — such as Microsoft 365 E3/E5, Windows
    Enterprise E3/E5, or an equivalent subscription — not merely a device-based license
  - No license is required beyond a standard Windows 11 Home key
  - Only a one-time perpetual license purchased per virtual machine is required
  - Licensing is only required if the VDI environment is hosted on-premises
  answer: 0
  why: Unlike a physical PC, which can be licensed per device, accessing Windows Enterprise virtual desktops
    for corporate use requires the accessing user to hold a qualifying per-user entitlement, most commonly
    through Microsoft 365 E3/E5 or standalone Windows Enterprise E3/E5 subscriptions. This user-based
    model is also what makes FSLogix and Azure Virtual Desktop access rights available at no extra cost
    under the same qualifying licenses.
- q: Which statement best characterizes how Citrix and Omnissa license their DaaS/VDI platforms compared
    to a simple one-time purchase?
  options:
  - Both are one-time perpetual licenses with no ongoing fee
  - Both are primarily consumed through subscription-based models (per-user or per-device, often tiered
    by feature edition), layered on top of the separate Windows and cloud infrastructure costs
  - Citrix and Omnissa provide their software entirely free of charge
  - Licensing for these platforms is bundled automatically into every Windows Enterprise subscription
  answer: 1
  why: Citrix DaaS and Omnissa Horizon (including Horizon Cloud) are both sold as ongoing subscriptions,
    typically per-user or per-device and often tiered across feature editions, separate from the Windows
    OS licensing and the underlying compute/storage infrastructure cost — three distinct cost lines that
    both a Citrix and an Omnissa deployment share the same shape for.
- q: Why do vCPU-to-user density ratios differ significantly between a task-worker persona and a power-user
    or graphics-intensive persona?
  options:
  - Density ratios never actually differ by persona
  - Power users always require personal (persistent) desktops by law
  - Task workers run lighter, less concurrent, less CPU-intensive workloads, so more of them can share
    a host's vCPUs; power users run heavier, more concurrent workloads that need more dedicated compute
    per person, lowering the safe density
  - Density ratios are determined entirely by the display protocol chosen
  answer: 2
  why: 'Density sizing is workload-driven: a task worker running a browser and light office apps needs
    far less sustained CPU than a power user running CAD, heavy multitasking, or data analysis tools.
    Sizing more users per host for task workers and fewer for power users is standard practice, and getting
    this ratio wrong in either direction wastes money or degrades user experience.'
- q: Besides vCPU count, which two additional resources most directly constrain how many users a session
    host can support?
  options:
  - Screen resolution and keyboard layout
  - The number of monitors and the color depth setting
  - The Windows edition name and build number
  - RAM (memory pressure per concurrent session) and storage IOPS (disk read/write throughput under concurrent
    load)
  answer: 3
  why: Even with ample vCPU headroom, a host can become unusable if it runs out of RAM under concurrent
    sessions (causing paging and slowdowns) or if storage can't sustain the IOPS demanded by many simultaneous
    logons, profile mounts, and application I/O — both are classic, easy-to-overlook sizing bottlenecks
    distinct from raw CPU count.
- q: When comparing on-premises VDI TCO to cloud VDI TCO, what is a common mistake that makes the comparison
    dishonest?
  options:
  - Counting only the hardware purchase price on the on-prem side while including staffing, facilities,
    cooling, refresh cycles, and downtime risk only on the cloud side (or vice versa) — an apples-to-oranges
    comparison that favors whichever side got the narrower accounting
  - Including software licensing costs at all
  - Comparing costs at all, since VDI economics can never be estimated
  - Assuming cloud costs are usage-based
  answer: 0
  why: 'A fair TCO comparison has to include the full cost envelope on both sides: for on-prem, that means
    hardware refresh cycles, power and cooling, datacenter space, and the staff time to operate it, not
    just the initial purchase; for cloud, that means compute, storage, egress, and licensing at realistic
    utilization, not best-case list pricing. Leaving out operational costs on one side while counting
    them on the other systematically biases the outcome.'
- q: In three to five sentences, name the four major VDI cost drivers and explain why licensing is often
    the cost category new EUC engineers most underestimate.
  answer: The four major cost drivers are compute (session host vCPU/RAM), storage (OS disks, profile
    containers, golden image storage), egress/networking (data leaving the cloud region or datacenter),
    and licensing (Windows per-user entitlements plus any Citrix or Omnissa subscription). Licensing is
    the category most often underestimated because it isn't a line item on a compute cost calculator the
    way vCPU-hours are, and because per-user entitlement rules are easy to assume are 'already covered'
    by an existing Microsoft 365 plan when they may not actually qualify the way the team assumes. New
    engineers frequently size compute and storage carefully but forget to confirm that every user connecting
    has a qualifying Windows Enterprise/M365 license, discovering the gap only during a compliance review
    or renewal.
  why: Compute and storage are visible, metered, and easy to estimate from a pricing calculator, while
    licensing entitlement compliance requires cross-referencing user assignments against subscription
    SKUs — a step that's easy to skip early in a design and expensive to fix retroactively.
resources:
- label: Windows 365 licensing
  url: https://www.microsoft.com/licensing/product-licensing/windows-365
- label: Windows 365 plans and pricing
  url: https://www.microsoft.com/en-us/windows-365/enterprise/all-pricing
- label: Azure Virtual Desktop pricing
  url: https://azure.microsoft.com/en-us/pricing/details/virtual-desktop/
- label: FSLogix prerequisites and licensing notes (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/fslogix/overview-prerequisites
---

## Why This Lesson Matters Beyond the Technology

Every lesson so far has been about how VDI works. This one is about what it *costs* — because the technically correct architecture that blows the budget doesn't ship. As an EUC engineer, you will be asked to justify sizing and licensing decisions in dollar terms more often than you'll be asked to explain a protocol handshake. This lesson gives you the vocabulary to have that conversation credibly.

## The Four Cost Drivers

Every VDI or DaaS deployment, regardless of platform, is paying for some mix of four things:

1. **Compute** — the vCPUs and RAM behind every session host, whether that's Azure VMs backing an AVD host pool, on-prem hypervisor capacity, or the fixed-size Cloud PC tier a Windows 365 user is assigned. This scales with the number of concurrent (not just total) users and the persona's resource needs.
2. **Storage** — OS disks for session hosts, golden image storage (Azure Compute Gallery, image repositories), and — often the most underestimated line item — profile container storage (FSLogix VHDX files on Azure Files or Azure NetApp Files), which grows with both user count and per-user data footprint.
3. **Egress and networking** — data leaving a cloud region or datacenter costs money and matters more than people expect once you factor in multimedia-heavy sessions, cross-region access, or hybrid connectivity (ExpressRoute/VPN) circuit costs.
4. **Licensing** — the Windows per-user entitlement plus any Citrix or Omnissa subscription layered on top. This is frequently the cost category new engineers underestimate, precisely because it doesn't show up on a compute pricing calculator the way vCPU-hours do.

A useful mental model: compute and storage are largely *usage-driven and visible*; licensing is *entitlement-driven and easy to silently get wrong* — you can be fully compliant on infrastructure spend while accidentally out of compliance on user licensing, and only discover it at renewal or audit time.

## Windows Licensing for VDI: The Per-User Rule

Here's the rule that trips up people coming from traditional desktop IT: **a physical Windows PC can be licensed per device, but accessing Windows 10/11 Enterprise virtual desktops for corporate use requires the connecting *user* to hold a qualifying per-user entitlement.** The most common qualifying licenses are:

- **Microsoft 365 E3 or E5** — the most common path in real deployments, since it also covers Microsoft 365 Apps, Entra ID P1/P2 features many designs already need, and FSLogix rights
- **Windows Enterprise E3 or E5** as a standalone subscription, for organizations that don't need the full Microsoft 365 suite
- **Windows 365** itself includes the required per-user Windows, Intune, and Entra ID P1 licensing bundled into its own subscription price for Cloud PC users specifically

This per-user entitlement is also what unlocks **FSLogix at no additional cost** — it isn't sold separately; it's included with the same qualifying subscriptions, along with Azure Virtual Desktop access rights. The practical lesson: before you finalize a host pool design, confirm every user who will connect actually holds one of these qualifying licenses. "We already have Microsoft 365" is not automatically the same as "every user connecting to this environment is licensed for VDI" — different M365 SKUs (Business plans vs. Enterprise plans, for example) carry different VDI entitlement rights.

## Citrix and Omnissa Subscription Models

Citrix DaaS and Omnissa Horizon (including Horizon Cloud) both layer their own **subscription licensing** on top of — not instead of — the Windows per-user licensing above and the underlying compute/storage cost. At a category level:

- Licensing is typically **per-user or per-device**, often tiered across feature editions (a baseline tier vs. a tier that unlocks advanced security, app delivery, or monitoring features)
- These subscriptions cover the vendor's control-plane software and premium capabilities (App Protection, advanced provisioning, analytics) — they do **not** replace the Windows OS licensing requirement, and in cloud deployments they don't replace the underlying infrastructure cost either
- Exact current pricing changes frequently and varies by contract, region, and negotiated agreement — treat published list pricing as directional, not a number to quote to a customer without verifying current rates

The pattern to remember for any platform: **infrastructure cost + Windows per-user licensing + platform/vendor subscription = total cost**, and skipping any one of the three produces a budget that will blow up later.

## Density and Sizing Basics

Once licensing is accounted for, the next question is: how many users can one session host actually support well? This is workload-driven, not a single universal number:

| Persona | Typical profile | Density implication |
|---|---|---|
| Task worker | Browser, light Office use, low concurrency of heavy apps | Higher density — more users share fewer vCPUs |
| Knowledge worker | Office suite, some multitasking, occasional video calls | Moderate density |
| Power user / developer | Heavy multitasking, IDEs, larger memory footprint | Lower density — fewer users per host |
| GPU/graphics workload | CAD, media, AI/ML dev | Lowest density — often 1:1 or small ratios, GPU-bound |

vCPU-to-user ratio is the number people quote first, but it is not the only constraint:

- **RAM** — memory pressure under concurrent sessions is often the first thing to fail before CPU does; undersized RAM shows up as sluggishness and paging well before CPU utilization looks alarming.
- **Storage IOPS** — logon storms (many users signing in around the same time, each mounting a profile container and launching apps) create a burst of read/write operations that a poorly sized storage tier simply cannot sustain, independent of how much CPU or RAM is available.

A sizing exercise that only looks at vCPU count and ignores RAM headroom and storage IOPS under concurrent load will look fine in testing with five users and fall over in production with five hundred.

## On-Premises vs. Cloud TCO: Keeping the Comparison Honest

When a customer asks "is it cheaper to run this ourselves or in the cloud," the honest answer requires counting the *same* categories on both sides:

- **On-premises** costs include hardware purchase and refresh cycles (typically every 3–5 years), power and cooling, datacenter/rack space, and the staff time to operate and patch the physical and virtualization layer — not just the sticker price of the servers.
- **Cloud** costs include compute, storage, egress, and the same Windows/platform licensing discussed above, at *realistic* utilization patterns (autoscale reduces idle spend, but poorly tuned autoscale can also leave capacity running unnecessarily) — not best-case list pricing assumptions.

The honest framing is rarely "cloud is always cheaper" or "on-prem is always cheaper" — it depends on utilization patterns, existing sunk investment, staffing model, and how much operational risk (patching, hardware failure, capacity planning) the organization wants to own directly versus transfer to a vendor. Module 2 picks this framing back up when comparing specific platforms, and Module 7's capstones will have you build an actual TCO sketch for a realistic scenario — the goal of this lesson is that when you get there, the categories won't be new to you.
