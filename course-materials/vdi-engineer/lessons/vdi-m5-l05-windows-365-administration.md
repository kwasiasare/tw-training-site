---
course: vdi-engineer
title: 'Windows 365 Administration: Provisioning, Networking, and Cloud PC Lifecycle'
month: 5
monthTitle: User Environments & App Delivery
lesson: 5
summary: Windows 365 trades AVD's infrastructure control for a fixed-price, Intune-first Cloud PC. This
  lesson covers provisioning policies, the choice between Microsoft-hosted network and Azure network connections,
  day-to-day Cloud PC lifecycle operations (restore points, resize), the current state of Windows 365
  Boot, Switch, and Frontline, and when a customer should actually be on Windows 365 instead of AVD.
objectives:
- Build a Windows 365 provisioning policy and explain what each configuration choice controls
- Choose between Microsoft-hosted network and an Azure network connection (ANC) for a given customer scenario
- 'Perform core Cloud PC lifecycle operations: restore points, resizing, and reprovisioning'
- Describe the current purpose and state of Windows 365 Boot, Switch, and Frontline
- Apply the Module 2 platform decision framework specifically to a Windows 365 vs. AVD choice
quiz:
- q: What does a Windows 365 provisioning policy actually control?
  options:
  - Only the billing and licensing assignment for Cloud PCs
  - Only the join type, with network and image configured elsewhere
  - Nothing user-facing — it only controls backend Azure subscription settings
  - The rules the Windows 365 service uses to build and configure Cloud PCs for assigned users, including
    the network, the image, and the Microsoft Entra user group that receives them
  answer: 3
  why: 'A provisioning policy is the central configuration object for Windows 365: it ties together the
    network configuration (Microsoft-hosted or an Azure network connection), the image used to build each
    Cloud PC, the join type, and the Microsoft Entra user group whose members will receive Cloud PCs built
    from that policy.'
- q: What is the key difference between the two Azure network connection (ANC) join types available for
    Windows 365?
  options:
  - Microsoft Entra join doesn't require connectivity to a Windows Server AD domain, while Hybrid Microsoft
    Entra join does
  - Microsoft Entra join is only for Frontline licenses; Hybrid join is only for Enterprise licenses
  - Both join types are functionally identical; the name is the only difference
  - Hybrid Microsoft Entra join is being retired in 2026 with no replacement
  answer: 0
  why: Both ANC join types let you place Cloud PCs into your own Azure virtual network and manage traffic,
    but Microsoft Entra join has no dependency on Windows Server AD domain connectivity, while Hybrid
    Microsoft Entra join specifically requires it, which affects your network design and where domain
    controllers need to be reachable from.
- q: Which network deployment model does Microsoft recommend as the default for Windows 365, where Microsoft
    fully provides and manages the underlying Azure connectivity on the customer's behalf?
  options:
  - Azure network connection with Hybrid Microsoft Entra join
  - Microsoft-hosted network
  - A customer-managed ExpressRoute circuit is mandatory for all deployments
  - Windows 365 has no default; every deployment must choose an ANC
  answer: 1
  why: 'Microsoft-hosted network is Microsoft''s recommended default deployment model for Windows 365:
    Microsoft fully provisions and manages the underlying Azure networking, so there''s no ANC, no customer-owned
    VNet, and no customer network configuration required at all — a genuine SaaS experience. A single
    tenant can run Microsoft-hosted network and ANC side by side for different user populations.'
- q: What does Windows 365 Boot let a user do on a supported Windows 11 physical device?
  options:
  - Run their Cloud PC and local desktop simultaneously as two Cloud PCs merged into one interface
  - Automatically resize their Cloud PC based on device battery level
  - Sign in directly to their Cloud PC from the physical device's Windows login screen, making the Cloud
    PC the primary experience with no extra steps
  - Convert any Windows 10 device into a Frontline Cloud PC license
  answer: 2
  why: Windows 365 Boot configures a Windows 11 physical device so the sign-in screen itself takes the
    user directly into their Cloud PC — effectively turning the device into a dedicated thin client to
    that user's Cloud PC, letting multiple users share one physical device by each landing on their own
    Cloud PC after their own sign-in.
- q: A customer needs users to share a small pool of Cloud PC licenses across shift workers who never
    use them concurrently, to control cost, and wants a physical kiosk-style device experience for that
    shared use. Which Windows 365 offerings together fit this scenario?
  options:
  - Windows 365 Enterprise with a dedicated per-user license and no Boot
  - Azure Virtual Desktop only, since Windows 365 has no shared-license model
  - Windows 365 Switch used as a standalone replacement for both
  - Windows 365 Frontline paired with Windows 365 Boot
  answer: 3
  why: Windows 365 Frontline is the shared-license, non-concurrent-use model built for shift/frontline
    workers, cost-optimized because it doesn't need one license per named user. Windows 365 Boot turns
    a shared physical device into a dedicated thin client straight into a Frontline Cloud PC, which is
    exactly the kiosk-style shared-device pattern described.
- q: In two to four sentences, using the Module 2 platform decision framework, describe one concrete scenario
    where you would recommend Windows 365 over Azure Virtual Desktop, and one where you would recommend
    AVD over Windows 365.
  answer: Windows 365 is the better fit for a mid-size professional services firm with predictable, one-user-per-license
    needs, a small IT team that wants Intune-first management with no infrastructure to size or patch,
    and a fixed, predictable per-user monthly cost — the SaaS simplicity outweighs the loss of infrastructure
    control. Azure Virtual Desktop is the better fit for an organization needing pooled multi-session
    hosts to control cost at scale, custom autoscaling tied to variable usage patterns, GPU-backed session
    hosts for specialized workloads, or infrastructure-level control (custom VNets, specific VM SKUs,
    granular scaling policies) that a fixed-price personal-only Cloud PC model can't provide.
  why: 'The decision hinges on the Module 2 framework: Windows 365 wins on simplicity, fixed pricing,
    and personal (1:1) desktops with minimal admin overhead; AVD wins when pooled multi-session economics,
    granular infrastructure control, or GPU/specialized workloads are required — the same variables from
    the original platform-choice lesson apply here with administrative depth added.'
resources:
- label: Create provisioning policies for Windows 365
  url: https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy
- label: Azure network connection overview
  url: https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections
- label: What is Windows 365 Boot?
  url: https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-boot-overview
- label: What is Windows 365 Frontline?
  url: https://learn.microsoft.com/en-us/windows-365/enterprise/introduction-windows-365-frontline
- label: What's new in Windows 365 Enterprise
  url: https://learn.microsoft.com/en-us/windows-365/enterprise/whats-new
---

## Administering a SaaS Desktop

Everything in Modules 3 and 4 assumed you own the infrastructure: you size the VMs, you patch the image, you scale the host pool. Windows 365 flips that model. It's Cloud PC as a **service** — Microsoft owns the underlying Azure infrastructure, you get a fixed per-user monthly price, and administration happens almost entirely through **Intune**, not the Azure portal. This lesson is about administering that model well, not about the architecture decision itself (that's Module 2's job — here we go deep on the how).

## Provisioning Policies: The Central Configuration Object

Every Cloud PC traces back to a **provisioning policy**. Created in the Intune admin center under **Devices → Windows 365 → Provisioning policies**, a policy ties together everything the service needs to build and hand out Cloud PCs: which **image** to use (a Microsoft-provided gallery image or your own custom image), which **network** configuration to place the Cloud PC on, the **join type**, and which **Microsoft Entra user group** should receive Cloud PCs from this policy. When the policy runs, the service creates a Cloud PC for each group member and, on an ANC deployment, places it into the correct Azure subnet based on the network configuration referenced by the policy. Multiple policies let you serve different user populations differently — a finance team on a locked-down ANC with a custom image, a contractor pool on Microsoft-hosted network with a lighter default image — from the same tenant.

## Network Options: Microsoft-Hosted vs. Azure Network Connection

This is the single most consequential choice in a Windows 365 deployment, and it's genuinely a spectrum from 'Microsoft manages everything' to 'you manage the network.'

**Microsoft-hosted network** is Microsoft's recommended default: Microsoft fully provisions and manages the underlying Azure networking on your behalf, in a Microsoft-owned subscription. There's no VNet to design, no subnet to size, no outbound connectivity to configure — genuinely the SaaS experience the product is built around. This is the right starting point for most net-new deployments unless you have a specific reason to need your own network.

**Azure network connection (ANC)** places Cloud PCs into a VNet in *your* Azure subscription, which you need when Cloud PCs must reach on-premises resources, sit behind your own network security controls, or route through existing hybrid connectivity (VPN/ExpressRoute). ANC comes in two join-type flavors:

- **Microsoft Entra join** — no dependency on Windows Server AD domain connectivity.
- **Hybrid Microsoft Entra join** — requires connectivity to a Windows Server AD domain, since the Cloud PC needs to complete a domain join in addition to registering with Entra ID.

A single tenant can run Microsoft-hosted network for one user population and an ANC for another, side by side — this isn't an all-or-nothing tenant-wide setting, so match the network model to each provisioning policy's actual requirement rather than defaulting the whole tenant to the more complex option 'just in case.' One 2026 operational note: for ANC deployments, VNets created after March 31, 2026 default to **private subnets** under Azure's broader default-outbound-access retirement — outbound internet access has to be explicitly configured on new VNets or Cloud PC provisioning will fail, a change worth checking before you stand up a new ANC.

## Cloud PC Lifecycle: Restore Points, Resize, Intune-First Management

Day-to-day Windows 365 administration happens through Intune rather than infrastructure tooling:

- **Restore points** are automatic, periodic snapshots of each Cloud PC (plus the ability to trigger one on demand) that let you or the end user roll a Cloud PC back to a known-good state — the closest Windows 365 equivalent to an AVD host pool's 'reset the pooled VM' pattern, except it's per-user since Cloud PCs are personal, not pooled.
- **Resize** lets you change a Cloud PC's compute/storage SKU after provisioning without reprovisioning from scratch, useful when a user's workload outgrows their original assignment.
- **Reprovision** rebuilds a Cloud PC from its policy's current image, which is how you push a refreshed base image to an existing user's Cloud PC rather than only new provisions picking it up.

All of this happens through the **Intune admin center** — there's no separate 'Windows 365 portal' distinct from where you already manage Intune-enrolled devices, which is deliberate: a Windows 365 Cloud PC is, from a management perspective, just another Intune-managed Windows device with a few Cloud-PC-specific actions layered on top.

## Boot, Switch, and Frontline

Four Windows 365 capabilities — three software features and one purpose-built device — extend the base personal-Cloud-PC model:

- **Windows 365 Boot** turns a physical **Windows 11** device into a dedicated thin client: the device's own sign-in screen takes the user straight into their Cloud PC, with no separate remote desktop client step. Because sign-in is per-user, multiple people can share the same physical device and each lands on their own Cloud PC — a strong fit for shared kiosks, front-desk terminals, or hot-desking hardware. Recent enhancements (through 2026) added the ability to switch back to the physical device's own local desktop from within the Cloud PC session without a full disconnect, and support for captive-portal Wi-Fi authentication before the Cloud PC sign-in even starts.
- **Windows 365 Link** is the hardware complement to Boot: Microsoft's first purpose-built Cloud PC thin client, generally available since 2025. It's a compact, fanless device with no local apps, no local data storage, and no local admin access — it signs the user straight into their Cloud PC in seconds and is managed through Intune like any other corporate endpoint.
- **Windows 365 Switch** lets a user move between their physical device's desktop and their Cloud PC using the same gesture Windows already uses for switching virtual desktops, rather than a separate remote desktop application window. Pairing Switch with **Frontline** Cloud PCs specifically now shows connection status and timeout information directly on the connection screen — a capability that reached general availability in 2026 after time in preview.
- **Windows 365 Frontline** is the shared-license model: instead of one license per named user, a smaller pool of licenses serves a larger population of shift or frontline workers who use their Cloud PC non-concurrently. **Intelligent pre-start** for Frontline's dedicated mode — which uses predictive signals to start a likely-needed Cloud PC in advance, cutting perceived boot time — reached general availability in 2026 as well.

Boot and Frontline are frequently paired in practice: a shared physical terminal (Boot) connecting shift workers into a cost-optimized shared license pool (Frontline) is one of the cleanest applied patterns in the whole Windows 365 catalog.

## Revisiting the Platform Decision, With Admin Depth

Module 2 gave you a first-pass framework for AVD vs. Windows 365: pooled multi-session cost efficiency and infrastructure control favor AVD; predictable per-user pricing and administrative simplicity favor Windows 365. Now that you've administered both in depth, sharpen that framework further. Windows 365 wins decisively when: the customer wants Intune to be the *only* management plane they touch, when desktops are genuinely personal (1:1) rather than pooled, when a small IT team can't take on infrastructure sizing and patching, or when Boot/Frontline's shared-device economics fit a frontline workforce. AVD wins decisively when: you need pooled multi-session hosts to drive down per-user cost at scale, GPU-backed session hosts for specialized workloads, granular autoscaling tied to variable demand, or infrastructure-level control (specific VM SKUs, custom VNets, Azure Compute Gallery versioning) that a fixed-price, personal-only Cloud PC model structurally can't offer. Many real customers end up running both, side by side, for different populations — which is exactly what the M7 migration-assessment capstone will ask you to design.
