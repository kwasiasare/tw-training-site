---
course: vdi-engineer
title: 'Session Hosts and Golden Images: Sizing, Building, and Versioning'
month: 3
monthTitle: 'Azure Virtual Desktop Infrastructure: Plan, Deploy & Scale'
lesson: 3
summary: 'This lesson covers the two things that determine whether your session hosts are fast, secure,
  and maintainable: how you size the VM, and how you build and version the image it boots from. You''ll
  learn to size VMs by workload class, choose between Windows 11 Enterprise multi-session and single-session
  editions, build a golden image the right way, version it through Azure Compute Gallery, automate the
  build with Azure Image Builder, and make informed choices about Trusted Launch and disk type.'
objectives:
- Size session host VM SKUs appropriately for light, medium, and heavy workload classes
- Choose between Windows 11 Enterprise multi-session and single-session editions for a given host pool
  type
- Describe the golden image workflow and why you build once and version rather than patch every host individually
- Explain how Azure Compute Gallery versions and replicates images for use across host pools and regions
- Explain what Azure Image Builder automates and when to use it instead of a manual golden image process
- Decide between Trusted Launch and standard VMs, and between ephemeral and managed OS disks, for a given
  scenario
quiz:
- q: A pooled host pool runs Windows 11 Enterprise multi-session for general office productivity users,
    roughly 6 users per host. Which sizing approach is correct?
  options:
  - Size the VM's vCPU, memory, and disk IOPS around the expected concurrent session count and workload
    class (light/medium/heavy), then validate with a pilot before committing to the fleet-wide SKU
  - Pick the cheapest available SKU regardless of vCPU-to-user ratio, since AVD automatically compensates
    for undersized VMs
  - Always use GPU-enabled VM SKUs for any multi-session pooled host pool
  - Match the VM size to the single heaviest individual user's laptop specification
  answer: 0
  why: There's no single 'correct' SKU — sizing is a function of concurrent sessions per host and the
    workload class those sessions represent (light task work vs. heavy engineering/design work). The practical
    approach is to size against Microsoft's workload-class guidance and your expected density, then validate
    against a real pilot before locking in the fleet-wide VM size.
- q: Why would a pooled host pool use Windows 11 Enterprise multi-session instead of a standard single-session
    edition?
  options:
  - Multi-session is required for FSLogix to function at all
  - Multi-session allows several concurrent users to share one VM's Windows OS instance, improving compute
    density and cost efficiency for shared, non-persistent pooled desktops
  - Multi-session is only available for personal host pools
  - Multi-session removes the need for a host pool entirely
  answer: 1
  why: Windows 11 Enterprise multi-session is licensed and engineered specifically to let multiple users
    run concurrent interactive sessions on the same VM, which is what makes pooled host pools cost-efficient
    at scale. Personal host pools, by contrast, typically use single-session editions since each VM is
    dedicated to one user.
- q: What is the core benefit of the 'golden image' approach compared to configuring each session host
    individually after deployment?
  options:
  - It removes the need for any patching after deployment forever
  - It is required by Microsoft licensing for all host pools
  - You build and validate the OS, applications, and configuration once, then roll that consistent, tested
    image out to every new or replaced session host — eliminating configuration drift and manual per-host
    setup
  - It automatically enables RDP Shortpath
  answer: 2
  why: The golden image approach bakes the OS, apps, agents, and configuration into a single tested artifact.
    Every session host — new or replaced — boots from that same consistent image, eliminating drift between
    hosts and manual configuration work that would otherwise happen one machine at a time.
- q: What role does Azure Compute Gallery play in the golden image workflow?
  options:
  - It replaces the need for Azure Image Builder
  - It is only used for marketplace images, not custom images
  - It automatically patches running session hosts in place
  - It stores, versions, and replicates your image definitions across regions and subscriptions, so session
    host deployments (portal, PowerShell, or Bicep) reference a specific image version by ID
  answer: 3
  why: 'Azure Compute Gallery (formerly Shared Image Gallery) is the versioning and distribution layer
    for your golden images: each build becomes a new image version under an image definition, can be replicated
    to the regions where you deploy session hosts, and is referenced by ID when you provision new hosts
    — giving you rollback and staged-rollout capability that a single unversioned managed image doesn''t.'
- q: When would you choose an ephemeral OS disk over a managed OS disk for a pooled, non-persistent session
    host?
  options:
  - When you want lower storage cost and faster VM reimage/redeploy for non-persistent pooled hosts, accepting
    that the OS disk is stored on the host's local VM cache/temp storage and is lost on deallocation
  - Never — ephemeral disks are not supported for AVD session hosts
  - When the session host needs to retain user profile data on the OS disk between reboots
  - Only for personal host pools, never for pooled host pools
  answer: 0
  why: Ephemeral OS disks are created on the local VM storage (cache or temp disk) instead of remote managed
    disk storage, which reduces cost and speeds up reimaging — a natural fit for non-persistent pooled
    session hosts that are expected to be stateless and disposable. Because the disk doesn't persist independently
    of the VM, it's the wrong choice whenever you need the OS disk to survive deallocation or hold persistent
    state, which is why personal host pools and any host expected to retain local state typically use
    managed disks instead.
- q: In two to four sentences, explain what Azure Image Builder automates in the golden-image workflow
    and why a platform team would prefer it over a manual 'build a VM, install apps, sysprep, capture'
    process.
  answer: 'Azure Image Builder (AIB) automates the golden-image pipeline end to end: given a base image,
    a set of customization steps (PowerShell scripts, Windows Update, restart handling, app installers)
    and a distribution target, it provisions a temporary build VM, applies the customizations, and publishes
    the resulting image as a new version directly into Azure Compute Gallery — without an engineer manually
    creating a VM, RDPing in, installing software, and running sysprep by hand. A platform team prefers
    this because the build becomes a repeatable, source-controlled, auditable definition (an ARM/Bicep
    template) that can be re-run on a schedule or triggered by a pipeline, which is essential once you''re
    maintaining monthly image refreshes across many host pools rather than a single manually-built image.'
  why: AIB turns image building from a manual, error-prone, one-off task into a repeatable automated pipeline
    that integrates with Azure Compute Gallery versioning — the difference between an image process that
    scales to dozens of host pools and one that doesn't.
resources:
- label: Overview of Azure Compute Gallery
  url: https://learn.microsoft.com/en-us/azure/virtual-machines/azure-compute-gallery
- label: Azure VM Image Builder overview
  url: https://learn.microsoft.com/en-us/azure/virtual-machines/image-builder-overview
- label: Prepare and customize a master VHD image for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-golden-image
- label: Trusted launch for Azure virtual machines
  url: https://learn.microsoft.com/en-us/azure/virtual-machines/trusted-launch
- label: Supported virtual machine sizes for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites
---

## Two Decisions That Shape Everything Else

Once your networking is sorted, the two decisions that most determine session host cost, performance, and manageability are: what VM SKU you size for each workload class, and what image that VM boots from. Get sizing wrong and users complain about lag no amount of RDP Shortpath tuning will fix. Get the image process wrong and every patch cycle becomes a manual, error-prone slog across dozens or hundreds of hosts. This lesson covers both properly.

## Sizing Session Hosts by Workload Class

There is no single "right" VM size for AVD — sizing is a function of **workload class** and **density** (sessions per host for pooled pools):

- **Light / task workers**: data entry, basic office apps, a handful of browser tabs. These tolerate higher density — more concurrent sessions per vCPU — and do well on general-purpose burstable or standard VM SKUs with modest vCPU-to-user ratios.
- **Medium / knowledge workers**: full Office suite, multiple browser tabs, occasional video calls, moderate multitasking. This is the most common profile and needs a meaningfully lower sessions-per-vCPU ratio than light workers to keep the experience responsive.
- **Heavy / power users and engineers**: CAD, development workloads, data analysis, sustained video conferencing, multiple high-resolution monitors. These often need dedicated or near-dedicated vCPU allocation per user, more memory per session, and sometimes a GPU-enabled SKU (covered from the vendor-neutral angle in Module 2, and revisited for AVD specifically as NV-series VMs when a workload needs hardware-accelerated graphics).

The practical workflow: start from Microsoft's published workload-class sizing guidance as a baseline, translate that into a target sessions-per-host number for pooled pools, and then **validate against a real pilot group** doing real work before you commit to the SKU for the full fleet. Disk IOPS and throughput matter as much as vCPU and memory — an undersized managed disk can bottleneck a session host that otherwise has plenty of compute headroom, especially during a FSLogix profile load or a boot storm at 9am.

## Choosing the OS: Windows 11 Enterprise Multi-Session

For **pooled** host pools, **Windows 11 Enterprise multi-session** is the default choice: it's licensed and engineered to let several users run independent, concurrent interactive sessions on one VM, which is exactly what makes pooled compute cost-efficient. For **personal** host pools, where each VM is dedicated to a single user, a standard single-session edition of Windows 11 Enterprise is the more common choice, since there's no need for the multi-session capability when nobody is sharing the machine. Either way, the licensing prerequisite is the same family of eligible Microsoft 365 or Windows per-user entitlements you'll cover in Module 4's identity lesson.

## The Golden Image Workflow

A **golden image** is a single, tested VM image — OS plus applications, agents, and baseline configuration — that every session host in a pool (or family of pools) boots from. The alternative — configuring each host by hand after deployment — doesn't scale past a handful of machines and guarantees configuration drift. The golden image workflow looks like this:

1. **Build**: start from a supported base (a Windows 11 Enterprise multi-session marketplace image is the common starting point), install and configure your applications, apply baseline settings, and install the AVD agent components.
2. **Generalize**: run Sysprep (or let your automation tooling handle it) to remove machine-specific identifiers so the image can be deployed to many VMs.
3. **Capture**: publish the generalized image as a managed image or, preferably, directly as a new version in an **Azure Compute Gallery** image definition.
4. **Deploy**: point host pool session host provisioning (portal, PowerShell, or Bicep) at that specific image version.
5. **Refresh**: on a regular cadence, repeat the process, publish a new image version, and roll it out to new or replaced session hosts — this is where the deployment automation and session host update mechanisms from the next lesson come in.

## Azure Compute Gallery: Versioning and Distribution

**Azure Compute Gallery** (the current name for what was previously called Shared Image Gallery) is the layer that turns a one-off captured image into a manageable artifact. Each build becomes a new **image version** under an **image definition**, and Azure Compute Gallery lets you:

- **Replicate** a version to every Azure region where you deploy session hosts, so provisioning pulls the image from a nearby region instead of across the world.
- **Reference a specific version by ID** in your deployment automation, so you can pin a host pool to a known-good version, stage a new version to a validation host pool first, and roll it out to production deliberately rather than accidentally deploying "whatever the latest build happens to be."
- **Share** image definitions across subscriptions in the same tenant (or beyond, with the right RBAC), useful when a central platform team builds images consumed by multiple business-unit subscriptions.

This versioning discipline is what makes a **rollback** possible: if a new image version causes problems, you point deployments back at the prior known-good version instead of trying to hot-fix hosts that are already running.

## Automating the Build with Azure Image Builder

**Azure Image Builder (AIB)** automates the build-generalize-capture sequence itself. You define a template — base image, a list of customizers (PowerShell/shell scripts, Windows Update, restart handling, app installers), and a distribution target (typically an Azure Compute Gallery image definition) — and AIB provisions a temporary build VM, applies the customizations, captures the result, and publishes it as a new gallery version, then tears down the temporary VM. Because the template is just an ARM/Bicep resource, the entire image-build process becomes source-controlled and repeatable through a pipeline, rather than a manual "build a VM, RDP in, install everything, sysprep by hand" exercise that different engineers might do slightly differently each month. AIB also automatically applies **Trusted Launch** settings when the target image definition is configured to support it, keeping security posture consistent without an extra manual step.

## Trusted Launch and Disk Type

Two more decisions round out the session host build:

- **Trusted Launch** combines **Secure Boot** and a **virtual TPM (vTPM)** to protect against boot-level and kernel-level attacks (rootkits, bootkits, malicious code injection into Windows kernel-mode processes) and enables **Credential Guard**. AVD supports provisioning Trusted Launch VMs from custom images stored in Azure Compute Gallery, and it should be treated as a default-on baseline for new session host deployments rather than an optional extra, given there's no meaningful downside for typical AVD workloads.
- **Ephemeral vs. managed OS disks**: an ephemeral OS disk is created on the VM's own local (cache or temp) storage instead of remote managed disk storage. That makes reimaging faster and removes the managed-disk storage cost, which fits **non-persistent pooled session hosts** well — they're meant to be stateless and disposable, and losing the OS disk on deallocation is a non-issue since a fresh copy of the golden image is exactly what you want on the next boot. **Managed OS disks** remain the right choice for personal host pools or any host where the OS disk needs to persist independently of the VM lifecycle.

Put together, sizing and image strategy determine whether your AVD estate is fast and maintainable or a constant source of tickets — and both feed directly into the deployment automation you'll build in the next lesson.
