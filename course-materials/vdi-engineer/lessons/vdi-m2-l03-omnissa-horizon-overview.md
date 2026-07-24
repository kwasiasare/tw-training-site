---
course: vdi-engineer
title: 'Omnissa Horizon: From VMware EUC to an Independent Platform'
month: 2
monthTitle: The 2026 VDI Platform Landscape
lesson: 3
summary: Omnissa is the independent company formed when Broadcom spun the former VMware End-User Computing
  business out on its own, and Horizon is its flagship on-prem-capable VDI platform. You'll learn Horizon
  8's core architecture — Connection Server, Unified Access Gateway, Instant Clones, App Volumes, and
  Dynamic Environment Manager (DEM) — how Horizon Cloud extends that architecture with cloud-hosted control,
  why the VMware-to-Omnissa transition matters for existing customers, and where the OCA-H certification
  (the current path, replacing the retired VCP-DTM) fits.
objectives:
- Explain who Omnissa is and why it exists as an independent company rather than under VMware/Broadcom
- Describe the function of Connection Server and Unified Access Gateway in a Horizon 8 deployment
- Explain what Instant Clones and App Volumes each solve for provisioning and application delivery
- Distinguish Horizon 8 (customer-managed pods) from Horizon Cloud (next-gen, cloud-hosted control)
- Summarize what the VMware-to-Omnissa transition means practically for an existing Horizon customer
- Identify OCA-H as the current Omnissa administrator certification and state why VCP-DTM is no longer
  the path
quiz:
- q: What is Omnissa?
  options:
  - A brand-new startup with no relation to VMware
  - A division that remains fully owned and operated by Broadcom
  - A rebrand of Citrix's EUC product line
  - The independent company formed when Broadcom spun the former VMware End-User Computing (EUC) business
    division out on its own
  answer: 3
  why: When Broadcom acquired VMware, it spun the End-User Computing division — including Horizon, Workspace
    ONE, and App Volumes — out as an independent company, Omnissa, rather than retaining it inside the
    Broadcom/VMware Cloud Foundation portfolio. Horizon is Omnissa's flagship product, not a Citrix product.
- q: In a Horizon 8 deployment, which component authenticates and brokers users to their entitled desktops
    and published applications?
  options:
  - Connection Server
  - Unified Access Gateway
  - App Volumes
  - Dynamic Environment Manager
  answer: 0
  why: Connection Server is Horizon's brokering component — it authenticates users and connects them to
    the desktop or application pool they're entitled to. Unified Access Gateway (UAG) provides the secure
    external access point (replacing the need for a VPN); it hands off to Connection Server rather than
    brokering sessions itself.
- q: What problem does Horizon's 'Instant Clones' technology solve?
  options:
  - It encrypts session traffic between the client and the desktop
  - It provisions large numbers of desktop VMs rapidly and just-in-time from a running parent image, minimizing
    storage and provisioning time compared to full clones
  - It manages user profile data across sessions
  - It replaces the need for Active Directory
  answer: 1
  why: Instant Clones create new desktop VMs almost instantly from a running parent VM's memory and disk
    state, dramatically reducing provisioning time and storage footprint compared to traditional full-clone
    VMs — the Horizon equivalent of the rapid, image-based provisioning AVD achieves with host pool VM
    templates and Citrix achieves with MCS.
- q: What is the key architectural difference between Horizon 8 and Horizon Cloud (next-gen)?
  options:
  - Horizon 8 only runs on physical hardware; Horizon Cloud is entirely software-free
  - There is no difference; they are the same product with different names
  - Horizon 8 is a customer-deployed and managed 'pod' architecture (Connection Servers, UAG, etc. that
    you run); Horizon Cloud shifts management to a cloud-hosted control plane, connected to your resources
    via an Edge Gateway, similar in spirit to Citrix Cloud
  - Horizon Cloud does not support Instant Clones
  answer: 2
  why: Horizon 8 uses a self-managed 'pod' model where the customer deploys and operates Connection Servers
    and UAG themselves. Horizon Cloud (next-gen) moves the control-plane management to Omnissa-hosted
    cloud services, with a Horizon Edge Gateway virtual appliance connecting a resource location back
    to that cloud control plane — architecturally similar in spirit to how Citrix DaaS relates to on-prem
    CVAD.
- q: An organization holds a legacy VMware Certified Professional – Desktop and Mobility (VCP-DTM) credential
    and wants to know the current certification path for a newly hired Horizon administrator in 2026.
    What should they be told?
  options:
  - The new hire should pursue VCP-DTM as well, since it is still the primary active credential
  - Omnissa has no certification program at all
  - The new hire should pursue CCA-V instead, since Horizon and Citrix certifications are interchangeable
  - VCP-DTM is no longer issued; existing holders' credentials are still honored, but the current path
    for a new administrator is OCA-H (Omnissa Certified Administrator – Horizon)
  answer: 3
  why: VCP-DTM was VMware's legacy Horizon-track certification; it is no longer issued (existing holders
    keep their credential, but it cannot be newly earned). The current, active Omnissa administrator credential
    is OCA-H (Omnissa Certified Administrator – Horizon), and CCA-V is a separate, Citrix-specific credential,
    not interchangeable with Horizon skills.
- q: In two to four sentences, explain what App Volumes and Dynamic Environment Manager (DEM) each solve
    in a Horizon deployment, and why an administrator typically needs both rather than just one.
  answer: 'App Volumes solves application delivery: it packages applications into virtual disks that attach
    to a desktop at login or in real time, so IT can deliver and update applications without baking them
    into the golden image or installing them per-user. Dynamic Environment Manager (DEM) solves user personalization
    and policy: it manages user profile settings, environment configuration, and conditional policies
    (without needing a full profile container solution on its own) so users get a consistent, personalized
    experience across sessions and non-persistent desktops. An administrator typically needs both because
    one manages what applications a user has, and the other manages how the user''s environment and settings
    behave — application delivery and user personalization are separate problems that need separate tooling,
    mirroring the app-delivery-vs-profile-management split covered across this course''s Module 1 and
    Module 5 lessons.'
  why: 'This mirrors the general VDI pattern from Module 1: profile/personalization tooling and application
    delivery tooling solve different layers of the non-persistent desktop problem, and Horizon''s App
    Volumes plus DEM is the platform-specific instance of that pattern, comparable to Citrix''s App Layering
    plus WEM or AVD''s app attach plus FSLogix.'
resources:
- label: What Is Horizon 8? (Omnissa Tech Zone)
  url: https://techzone.omnissa.com/resource/what-horizon-8
- label: Horizon 8 architecture (Omnissa Tech Zone)
  url: https://techzone.omnissa.com/resource/horizon-8-architecture
- label: Omnissa Horizon 8 product page
  url: https://www.omnissa.com/products/horizon-8/
- label: Evaluation Guide for Horizon 8 (Omnissa Tech Zone)
  url: https://techzone.omnissa.com/resource/evaluation-guide-horizon-8
video: vdi-m2-l03-omnissa-horizon-overview.mp4
---

## From VMware EUC to Omnissa

For most of Horizon's history, it was "the VMware VDI product" — the natural pairing with vSphere and NSX for shops already deep in the VMware ecosystem. That changed with Broadcom's acquisition of VMware: rather than folding End-User Computing into the Broadcom/VMware Cloud Foundation portfolio, Broadcom divested the entire EUC division — **Horizon, Workspace ONE, App Volumes, and Dynamic Environment Manager** — to the investment firm KKR, which launched it in 2024 as an **independent company: Omnissa**.

For a working EUC engineer, the practical upshot is: Horizon is no longer "a VMware product." It's Omnissa's flagship platform, developed and sold independently, though it still runs comfortably on vSphere and increasingly on other hypervisors (including public cloud and platforms like Nutanix AHV, reflecting Omnissa's push toward hypervisor flexibility post-spinout). If you inherit an existing "VMware Horizon" estate, expect licensing, support contracts, and documentation branding to be mid-transition — verify current contract ownership before assuming anything about renewal terms.

## Horizon 8 Core Architecture

Horizon 8 is the on-premises-capable, customer-managed "pod" architecture — you deploy and operate its components yourself, much like Citrix's classic CVAD model (Lesson 2):

- **Connection Server** — the brokering component. It authenticates users (against Active Directory, often paired with MFA/SAML) and connects them to their entitled desktop or application pool. This is Horizon's direct equivalent to Citrix's Delivery Controller function or AVD's managed broker.
- **Unified Access Gateway (UAG)** — the secure external access point. UAG terminates external connections, performs authentication pre-checks, and proxies traffic to Connection Server and session hosts, removing the need for a traditional VPN for remote access — functionally similar to Citrix's Gateway service or AVD's reverse-connect gateway.
- **Instant Clones** — Horizon's rapid provisioning technology. New desktop VMs are created almost instantly from a running parent VM's memory and disk state, rather than full disk clones, which sharply cuts both provisioning time and storage consumption. This is what makes large pooled, non-persistent Horizon desktop pools practical at scale — the Horizon-specific answer to the same golden-image provisioning problem MCS solves for Citrix and Compute Gallery solves for AVD.
- **App Volumes** — application delivery via virtual disks ("AppStacks"/writable volumes) attached to a desktop at login or dynamically, so applications don't need to be baked into the golden image or manually installed per user.
- **Dynamic Environment Manager (DEM)** — user personalization and policy management: profile settings, environment configuration, and conditional policy application, layered on top of (not replacing) a profile container strategy.

Together, Instant Clones solve provisioning, App Volumes solves application delivery, and DEM solves personalization — three separate layers of the same non-persistent-desktop problem you first met conceptually in Module 1 Lesson 4.

## Horizon Cloud: The Next-Gen, Cloud-Managed Model

Just as Citrix evolved from on-prem CVAD to cloud-managed DaaS, Omnissa offers **Horizon Cloud (next-gen)** — a cloud-hosted control plane that takes over the management functions Connection Server and UAG traditionally handled on-prem. A **Horizon Edge Gateway** virtual appliance connects a Horizon 8 pod (or a Horizon Cloud-native resource location) back to Horizon Cloud's control services, including subscription-based (rather than perpetual) licensing.

The architectural shape should feel familiar by now: a vendor-hosted control plane, a lightweight connector/gateway component bridging to customer-owned resources, and the customer choosing where those resources physically live. It's the same pattern as Citrix Cloud plus Cloud Connectors, and conceptually parallel to AVD's managed control plane plus customer-owned session hosts — three vendors converging on the same "cloud brain, customer body" architecture from different starting points.

## What the Transition Means for Existing Customers

If you support an organization with an existing VMware Horizon estate, three things matter practically: **support and licensing now route through Omnissa**, not VMware/Broadcom, for EUC products; **documentation and branding are actively migrating** (Omnissa Tech Zone is the current authoritative source, replacing VMware's old TechZone/docs properties); and **the underlying technology — Instant Clones, App Volumes, DEM, UAG — is unchanged in function**, so an administrator's existing Horizon skills transfer directly. Don't let the corporate restructuring create unnecessary anxiety about the product's technical direction; it hasn't materially changed.

## The Certification Path

The current, active administrator credential is **OCA-H (Omnissa Certified Administrator – Horizon)**. The legacy VMware credential, **VCP-DTM (VMware Certified Professional – Desktop and Mobility), is no longer issued** — existing holders retain it, but it is not an achievable path for a new administrator in 2026. If you see VCP-DTM listed as a target credential in a job posting or study plan, treat it as outdated and redirect toward OCA-H; Module 7's cert-roadmap lesson places OCA-H alongside AZ-140 and CCA-V in the full multi-platform picture.

## A Practical Naming Checklist

Because the VMware-to-Omnissa transition is recent enough that documentation, job postings, and legacy contracts lag behind reality, keep a quick mental checklist when you walk into an unfamiliar Horizon estate: confirm whether support is contracted through Omnissa directly or through a reseller still using older VMware paperwork; confirm which hypervisor the pod actually runs on (vSphere remains common, but Omnissa's post-spinout roadmap has pushed multi-hypervisor support, including Nutanix AHV, so don't assume vSphere by default); and confirm whether the deployment is Horizon 8 (self-managed pod) or Horizon Cloud (next-gen, cloud-managed) before you go looking for a Connection Server that might not exist. Getting these three answers early avoids a lot of wasted troubleshooting time, and it's exactly the kind of due-diligence question a hiring manager will expect a VDI engineer to ask on day one of a new Horizon engagement.

## What's Next

You've now covered the three major full-featured VDI/DaaS platforms: AVD/Windows 365, Citrix DaaS, and Omnissa Horizon. Lesson 4 turns to the specialized edge of the landscape — GPU-accelerated VDI for CAD, media, and AI/ML workloads — plus a survey of smaller players worth knowing by name.
