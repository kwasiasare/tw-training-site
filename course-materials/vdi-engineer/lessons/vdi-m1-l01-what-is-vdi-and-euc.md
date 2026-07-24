---
course: vdi-engineer
title: What Is VDI and End-User Computing?
month: 1
monthTitle: VDI & EUC Foundations
lesson: 1
summary: This opening lesson builds the vocabulary the rest of the course depends on. You'll learn how
  VDI, session-based computing (RDS), application virtualization, and DaaS are actually different from
  each other despite being used loosely as synonyms, trace the short history from Citrix WinFrame through
  Terminal Services to today's cloud-native platforms, and understand the concrete 2026 business drivers
  — hybrid work, data-egress control, contractor and BYOD access, regulated industries, and GPU/AI workstations
  — that make VDI and End-User Computing (EUC) one of the fastest-growing specializations inside IT operations.
objectives:
- Distinguish VDI, session-based/RDS, application virtualization, and DaaS by what actually runs where
- Trace the lineage from Citrix WinFrame through Windows Terminal Services to modern cloud DaaS in broad
  eras
- Explain at least three concrete 2026 business drivers for adopting VDI or EUC
- Identify which delivery model fits a given scenario based on isolation, cost, and compliance needs
- Describe why regulated industries treat VDI as a data-control strategy, not just a remote-access convenience
quiz:
- q: What is the defining architectural difference between VDI and session-based computing (RDS/Terminal
    Services)?
  options:
  - VDI gives each user their own OS instance (a VM); RDS gives many users a shared OS instance on one
    server
  - VDI runs locally on the user's device; RDS always runs in the cloud
  - VDI is only for Windows; RDS is only for Linux
  - There is no real difference — they are marketing terms for the same technology
  answer: 0
  why: In VDI, every user is assigned an isolated virtual machine running its own OS kernel. In session-based/RDS
    computing, many users share sessions on a single shared Windows Server OS instance. That isolation
    boundary is the reason VDI costs more per user but tolerates a wider range of applications and compliance
    requirements.
- q: Which statement best describes application virtualization as distinct from VDI or RDS?
  options:
  - It delivers an entire virtual desktop OS to the user
  - It packages and streams individual applications to a user's existing device or session, without delivering
    a full desktop
  - It is a synonym for DaaS
  - It only works with browser-based applications
  answer: 1
  why: Application virtualization (historically App-V, today mostly MSIX app attach and RemoteApp/published
    apps) isolates and delivers individual applications rather than a whole desktop. It's often layered
    on top of VDI or RDS rather than being a competing delivery model.
- q: What makes a platform 'DaaS' (Desktop-as-a-Service) rather than traditional on-premises VDI?
  options:
  - DaaS desktops are always free of charge
  - DaaS removes local applications entirely
  - DaaS is cloud-hosted and consumed as a managed subscription service, with the vendor or cloud provider
    owning most of the underlying infrastructure
  - DaaS only supports Linux desktops
  answer: 2
  why: DaaS (Windows 365, Citrix DaaS, Omnissa Horizon Cloud) shifts infrastructure ownership and operational
    burden to a cloud provider or vendor, billed as a subscription — versus classic on-prem VDI, where
    the customer owns and operates the hypervisor, storage, and broker themselves.
- q: Windows Terminal Server, the ancestor of today's Remote Desktop Services, was built using multi-user
    technology originally licensed from which company?
  options:
  - Novell
  - VMware
  - IBM
  - Citrix (its MultiWin technology)
  answer: 3
  why: Citrix's WinFrame (1995) added multi-user session capability to Windows NT through its MultiWin
    technology. Microsoft licensed MultiWin and shipped it as Windows NT 4.0 Terminal Server Edition in
    1998, which evolved into today's Remote Desktop Services (RDS).
- q: A hospital wants clinicians to access patient records from personal tablets without any patient data
    ever being stored on the device. Which 2026 VDI driver does this scenario primarily illustrate?
  options:
  - Data-egress control for a regulated industry
  - GPU/AI workstation demand
  - Contractor onboarding speed
  - Reducing Windows licensing costs
  answer: 0
  why: Keeping data inside the datacenter and streaming only pixels to an unmanaged device is the core
    data-egress control use case that drives VDI adoption in healthcare, finance, and government — regardless
    of what device the clinician owns.
- q: In two to four sentences, explain why VDI/DaaS is often the fastest way to onboard short-term contractors
    compared to shipping them a managed laptop, and name one specific EUC platform capability that makes
    this possible.
  answer: 'With VDI or DaaS, an admin can assign a contractor a virtual desktop or Cloud PC in minutes
    through an existing provisioning workflow, without procuring, imaging, shipping, or eventually recovering
    physical hardware — the contractor connects from whatever device they already have. A capability that
    makes this safe is that the desktop itself is centrally managed and disposable: for example, a non-persistent
    pooled host pool or a Windows 365 Cloud PC can be deprovisioned or reset the moment the engagement
    ends, instantly revoking access without a hardware return process.'
  why: Speed of provisioning and speed of clean revocation are the two operational reasons VDI/DaaS beats
    physical-device onboarding for short-term and third-party access, and both rely on the desktop being
    centrally hosted rather than physically shipped.
resources:
- label: What is Azure Virtual Desktop? (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/overview
- label: What is Windows 365? (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/windows-365/overview
- label: Citrix DaaS documentation
  url: https://docs.citrix.com/en-us/citrix-daas
- label: Omnissa Horizon 8 overview (TechZone)
  url: https://techzone.omnissa.com/resource/what-horizon-8
- label: Cloud Software Group (Citrix parent company)
  url: https://en.wikipedia.org/wiki/Cloud_Software_Group
video: vdi-m1-l01-what-is-vdi-and-euc.mp4
---

## Four Words People Use Interchangeably (and Shouldn't)

Walk into any IT organization and you'll hear "VDI," "virtual desktops," "RDS," and "DaaS" used as if they're the same thing. They aren't, and the differences drive real decisions about cost, compliance, and user experience. This lesson gives you the vocabulary the rest of this course — and every conversation you'll have as an EUC engineer — depends on.

### VDI (Virtual Desktop Infrastructure)

In true VDI, **each user gets their own virtual machine**, running its own copy of a desktop OS (typically Windows 10 or Windows 11 Enterprise). That VM is isolated at the kernel level from every other user's VM. This isolation is expensive — you're paying for a full OS instance, patching, and compute per user — but it buys you application compatibility (anything that runs on a real desktop OS runs here) and a strong compliance boundary, because one user's process, malware, or crash cannot touch another user's session.

### Session-based computing (RDS / Terminal Services)

Here, **many users share a single Windows Server OS instance**, each getting an isolated *session* rather than an isolated *machine*. This is dramatically cheaper per user — a single server can host dozens of sessions — but application compatibility is narrower (apps must tolerate multi-user execution), and a resource-hungry or crashing process can degrade the experience for everyone sharing that host. Azure Virtual Desktop's signature move is **Windows 11 Enterprise multi-session** — the only place you can legally run a multi-user Windows 11 client OS, blending session-based economics with a client OS experience.

### Application virtualization

This delivers **individual applications**, not a whole desktop. The app is packaged, isolated from the underlying OS, and streamed or attached on demand — think MSIX app attach on Azure Virtual Desktop, or RemoteApp publishing. It's usually layered *on top of* VDI or RDS rather than competing with them: you might publish only Excel and a line-of-business app to a contractor instead of a full desktop.

### DaaS (Desktop-as-a-Service)

DaaS is not a different rendering technology — it's a **consumption and ownership model**. In classic on-premises VDI, you own and operate the hypervisor, the broker, the gateway, and the storage. In DaaS (Windows 365, Citrix DaaS, Omnissa Horizon Cloud), a vendor owns and operates most or all of that control plane, and you consume virtual desktops as a managed, often per-user-per-month subscription. Windows 365 pushes this furthest: it is genuinely SaaS, with fixed-price Cloud PCs and no infrastructure for you to size or patch.

| Model | Isolation unit | Who owns infrastructure | Typical use |
|---|---|---|---|
| VDI | Dedicated VM per user | Customer (or cloud IaaS) | Regulated/compliance workloads, power users |
| Session-based (RDS) | Shared OS, isolated session | Customer | Task workers, cost-sensitive fleets |
| App virtualization | Isolated app package | Customer or vendor | Legacy app delivery, app conflicts |
| DaaS | Dedicated or pooled VM | Vendor/cloud provider | Fast provisioning, low ops overhead |

## A Short History, in Eras

You don't need trivia dates memorized, but you do need the shape of the story, because it explains why today's products look the way they do.

1. **The multi-user era (mid-1990s).** Citrix WinFrame added multi-user session sharing to Windows NT through its MultiWin technology — the first practical way to put many users on one Windows server.
2. **The Microsoft licensing era (late 1990s–2000s).** Microsoft licensed that multi-user technology and shipped it as Windows Terminal Server, which became Terminal Services and eventually **Remote Desktop Services (RDS)** — a first-party Microsoft product that Citrix then added value on top of (protocol acceleration, profile management, provisioning).
3. **The hypervisor/VDI era (2000s–2010s).** VMware, and later Citrix XenDesktop, popularized *true* VDI: one VM per user, orchestrated by a connection broker, running on-premises hypervisors.
4. **The cloud DaaS era (2019–today).** Microsoft launched Windows Virtual Desktop (now **Azure Virtual Desktop**) in 2019, followed by **Windows 365** Cloud PCs in 2021. Citrix and the former VMware Horizon business (now **Omnissa**, spun out independently in 2024) both shipped cloud control planes — Citrix DaaS and Horizon Cloud — while keeping on-premises options alive for regulated and latency-sensitive customers.

The throughline: each era pushed more of the operational burden (hardware, patching, broker infrastructure) off the customer and onto a vendor or cloud platform, while the fundamental problem — deliver a secure, consistent desktop to a device you may not control — never changed.

## Why VDI and EUC Matter in 2026

The business case for VDI has shifted from "remote access convenience" to genuine strategic infrastructure. Five drivers show up in almost every real deployment you'll work on:

- **Hybrid and distributed work.** Employees expect to work from home, the office, or a client site interchangeably, on whatever device is nearest, without IT re-imaging a laptop for every scenario.
- **Security and data-egress control.** This is the big one for regulated industries. In VDI/DaaS, data never leaves the datacenter — only encrypted pixels, audio, and input events cross the network. A lost or compromised endpoint device exposes nothing, because nothing was ever stored on it. Financial services, healthcare, defense, and government all lean on this property specifically, not just remote access.
- **Contractors and BYOD.** Standing up a Cloud PC or a pooled desktop for a short-term contractor takes minutes and is trivially revocable, versus procuring, imaging, shipping, and eventually recovering a physical laptop.
- **Regulated industries and audit posture.** Centralizing desktops makes patching, logging, session recording, and access reviews consistent and auditable across the whole fleet, rather than trusting thousands of physically dispersed endpoints to stay compliant.
- **GPU and AI workstation demand.** A newer driver: CAD, media production, and AI/ML development increasingly need GPU-backed compute that's expensive to put in every employee's hands as a physical workstation. GPU-enabled VDI (Azure NV-series, NVIDIA vGPU) lets organizations centralize that expensive hardware and allocate it on demand.

As you move through this course, keep coming back to this list. Every platform choice, every architecture decision, and every security control in later modules exists to serve one or more of these five drivers — and a good EUC engineer can always explain *which one* a given design decision serves.
