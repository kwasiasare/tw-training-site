---
course: vdi-engineer
title: 'AVD Networking: VNets, Required Endpoints, RDP Shortpath, and Private Link'
month: 3
monthTitle: 'Azure Virtual Desktop Infrastructure: Plan, Deploy & Scale'
lesson: 2
summary: Session hosts live in your virtual network, so networking design decisions directly shape user
  experience and security posture. This lesson covers how to design a VNet and subnet for AVD, the exact
  outbound connectivity a session host needs (service tags and required FQDNs), how RDP Shortpath establishes
  a direct UDP path for managed and public networks, when to use Private Link instead of public endpoints,
  and how to plan bandwidth and hybrid connectivity for real workloads.
objectives:
- Design a VNet and subnet layout for AVD session hosts that supports growth and hybrid connectivity
- List the outbound connectivity AVD session hosts require, using the WindowsVirtualDesktop service tag
  and required FQDNs
- Explain how RDP Shortpath for managed networks differs from RDP Shortpath for public networks
- Explain when and why to deploy Azure Private Link for AVD instead of relying on public service endpoints
- Estimate per-user bandwidth needs for different workload types and plan hybrid connectivity accordingly
quiz:
- q: Which Azure networking construct lets you allow AVD traffic through an NSG or Azure Firewall without
    maintaining a list of Microsoft's changing IP ranges yourself?
  options:
  - A user-defined route pointing to 0.0.0.0/0
  - A private endpoint on the session host's NIC
  - An application security group scoped to the session host subnet
  - The WindowsVirtualDesktop service tag (and matching FQDN tag on Azure Firewall)
  answer: 3
  why: Azure publishes AVD's required endpoints as the WindowsVirtualDesktop service tag for NSGs/UDRs
    and the matching FQDN tag for Azure Firewall, so you reference the tag in your rule instead of hardcoding
    IP ranges that Microsoft manages and changes over time.
- q: A session host's NSG blocks outbound access to *.blob.core.windows.net and *.servicebus.windows.net,
    but allows the WindowsVirtualDesktop service tag. What is the likely result?
  options:
  - Users will experience broken agent registration or session functionality, because those storage/service-bus
    endpoints carry diagnostics, agent updates, and other required traffic not covered by the service
    tag alone
  - No impact — the service tag alone covers all AVD requirements
  - The host will fail to boot
  - RDP Shortpath will silently fall back to TCP with no other effect
  answer: 0
  why: The WindowsVirtualDesktop service tag covers the core static AVD endpoints, but Microsoft's required-FQDN
    guidance calls out that you must still separately allow specific storage and Service Bus endpoints
    used for agent communication and diagnostics. Blocking them breaks functionality even with the service
    tag allowed.
- q: What is the key architectural difference between RDP Shortpath for managed networks and RDP Shortpath
    for public networks?
  options:
  - Managed networks always use TCP; public networks always use UDP
  - Managed networks establish a direct UDP connection over a private network path (like VPN or ExpressRoute)
    and can use a listener on the host; public networks establish a direct UDP connection over the public
    internet using ICE/STUN, with TURN as a relay fallback when a direct path can't be negotiated
  - Public networks require Azure Front Door; managed networks do not
  - There is no difference — 'managed' and 'public' are marketing terms for the same underlying protocol
  answer: 1
  why: RDP Shortpath for managed networks uses a private connection (ExpressRoute private peering or VPN)
    and can use a direct UDP listener on the session host. RDP Shortpath for public networks negotiates
    a direct UDP path across the internet using ICE/STUN; when a direct path is blocked by NAT or firewalls,
    it can fall back to a relayed connection via TURN so the session still gets a UDP transport instead
    of dropping to TCP.
- q: Why would an organization deploy Azure Private Link for Azure Virtual Desktop rather than relying
    on the default public endpoints?
  options:
  - Private Link is required before you can create any host pool
  - Private Link replaces the need for RDP Shortpath entirely
  - It routes the AVD control-plane traffic (feed discovery, feed download, and/or session connections,
    depending on configuration) over private endpoints in the customer's VNet instead of the public internet,
    supporting stricter network isolation requirements
  - Private Link is only relevant for personal host pools
  answer: 2
  why: Private Link for AVD lets you route parts of the AVD connection sequence over a private endpoint
    inside your VNet, which matters for organizations with strict network isolation or compliance requirements
    that prohibit public internet exposure. Note that public-network RDP Shortpath (STUN/TURN) is not
    supported when Private Link is in use for the session connection — you use RDP Shortpath for managed
    networks instead.
- q: You need to size a VPN or ExpressRoute circuit for a group of 200 concurrent AVD users doing general
    knowledge-work (office apps, web, light video). What is the correct planning approach?
  options:
  - Assume zero bandwidth, since AVD traffic never leaves the session host's VNet
  - Always provision for the maximum theoretical bandwidth of the display protocol regardless of workload
  - Bandwidth planning is unnecessary because RDP Shortpath removes all bandwidth constraints
  - Use Microsoft's published RDP bandwidth requirement guidance per workload type as a starting per-user
    estimate, multiply by expected concurrent users, and validate with a pilot before finalizing circuit
    sizing
  answer: 3
  why: Microsoft publishes RDP bandwidth requirement guidance broken out by usage pattern (light office
    work vs. video-heavy workloads). The practical approach is to use that guidance as a per-user baseline,
    scale it to your expected concurrency, and then validate against a pilot group before committing to
    a circuit size — bandwidth needs vary significantly by real usage.
- q: In two to four sentences, describe the outbound-only connectivity model a session host subnet needs
    for AVD to function, and name one specific type of endpoint beyond the WindowsVirtualDesktop service
    tag that must also be explicitly allowed.
  answer: A session host subnet only needs outbound connectivity — no inbound rule is required for AVD
    connectivity itself because the AVD agent initiates an outbound connection to the service (reverse
    connect). The NSG or firewall should allow outbound access to the WindowsVirtualDesktop service tag
    (or FQDN tag on Azure Firewall) for the core control-plane endpoints. Beyond that, Microsoft's required-FQDN
    list calls out specific storage and messaging endpoints — for example *.blob.core.windows.net and
    *.servicebus.windows.net — that carry agent communication, diagnostics, and other required traffic
    and must be allowed separately, in addition to whatever endpoints the session host's applications
    and OS patching need.
  why: AVD's networking model is outbound-only by design (reverse connect), but the required connectivity
    is broader than the service tag alone — the storage and Service Bus endpoints used for agent telemetry
    and communication are a commonly missed piece that causes registration or session failures when locked
    down too aggressively.
resources:
- label: Required FQDNs and endpoints for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/required-fqdn-endpoint
- label: RDP Shortpath for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-shortpath
- label: Configure RDP Shortpath for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-rdp-shortpath
- label: Azure Private Link with Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview
- label: Remote Desktop Protocol (RDP) bandwidth requirements
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-bandwidth
video: vdi-m3-l02-avd-networking.mp4
---

## Why Networking Is Not an Afterthought

Because session hosts are customer-managed VMs sitting in your own virtual network, every networking decision you make — subnet sizing, firewall rules, transport protocol, hybrid connectivity — directly shows up as either a smooth remote desktop experience or a stream of "my session feels laggy" tickets. This lesson gives you the four pieces you need: how to lay out the VNet, what outbound connectivity is actually required, how RDP Shortpath gets you a fast UDP path instead of plain TCP, and when Private Link changes the picture.

## Designing the VNet and Subnet

Start with the basics that apply to any VM fleet, then layer AVD-specific concerns on top:

- **Dedicate a subnet (or subnets) to session hosts** rather than mixing them with other workloads, so NSG rules, route tables, and monitoring stay scoped and readable. Segregating personal-pool hosts from pooled-pool hosts in separate subnets is a common pattern when their security posture or DR treatment differs.
- **Size for growth, not just day one.** Host pools scale by adding more session hosts, and a subnet that's too small forces a re-IP exercise later. Plan address space for at least your two-year headcount projection plus autoscale burst capacity.
- **Region alignment matters for latency.** Deploy session hosts in the Azure region closest to the majority of your users, not necessarily the region where the rest of your estate happens to live — user experience is dominated by round-trip time between client and host.

Your session host subnet is **outbound-only** by design, thanks to reverse connect (Lesson 1). That simplifies the inbound story to almost nothing, but it raises the bar on getting outbound rules exactly right.

## Required Outbound Connectivity

Microsoft publishes a required-FQDN list for AVD, and the practical way to consume it is:

- Use the **WindowsVirtualDesktop service tag** in your NSG or route table rules (or the matching **FQDN tag** if you're using Azure Firewall) to cover the core static AVD service endpoints — the broker, diagnostics, and related control-plane traffic — without hand-maintaining IP ranges Microsoft controls and changes.
- **Separately allow specific storage and messaging endpoints** that the service tag does not fully cover — Microsoft calls out endpoints such as `*.blob.core.windows.net`, `*.servicebus.windows.net`, and `*.table.core.windows.net` scoped to the specific deployment URLs used for agent communication, diagnostics, and telemetry. Skipping these is one of the most common causes of "the host registers but sessions behave oddly" tickets.
- Allow whatever your **image and applications** independently need: Windows Update or WSUS/Configuration Manager endpoints, your package management service, line-of-business API endpoints, and identity endpoints for Microsoft Entra ID authentication.
- Microsoft explicitly does **not support** AVD deployments where required FQDNs are blocked — treat the required list as non-negotiable, not a starting point for further lockdown.

## RDP Shortpath: Two Different Mechanisms

RDP Shortpath establishes a **direct UDP-based transport** between the client and the session host instead of relaying everything through the TCP-based reverse connect path — UDP tolerates packet loss and jitter far better than TCP for real-time audio/video and input, which is exactly what a remote desktop session needs. There are two distinct variants, and mixing them up is a common exam trap:

- **RDP Shortpath for managed networks**: used when the client reaches the session host over a network you control end-to-end — a site-to-site VPN or ExpressRoute private peering. It can use a listener configured directly on the session host, or fall back to ICE/STUN-based discovery when the listener isn't enabled and inbound ports aren't opened, to find a usable direct UDP path across that private network.
- **RDP Shortpath for public networks**: used when the client connects over the general internet, with no private network in common. It uses **ICE/STUN** to attempt a direct UDP connection first. When NAT or firewall behavior prevents a direct path, it can fall back to a **relayed connection via TURN**, which still gets the session a UDP transport instead of dropping all the way back to plain TCP. This works automatically, with no extra configuration, as long as your session hosts, clients, and any firewalls in between allow the traffic and RDP transport settings remain at their defaults.

The practical takeaway: managed-network Shortpath is for organizations with private connectivity already in place (VPN/ExpressRoute); public-network Shortpath with its ICE/STUN/TURN fallback chain is what makes remote, unmanaged, internet-connected users get a good UDP-based experience without you having to build private connectivity to every home office.

## Private Link: Keeping Traffic Off the Public Internet

**Azure Private Link for Azure Virtual Desktop** lets you expose the AVD service's connection endpoints — feed discovery, feed download, and/or the session connection itself, depending on which Private Link scenario you enable — through a **private endpoint** inside your own VNet, instead of the public AVD service endpoints. This matters for organizations with strict network isolation requirements (regulated industries, government, or any environment where "no path to the internet" is a hard requirement) who still want to use the managed AVD service.

Two things to remember when you combine Private Link with the rest of this lesson: first, Private Link for session connections requires the **entire TCP dynamic port range (1–65535)** open to the private endpoint, because port mapping happens through a single private IP for all the global gateway instances behind it. Second, **RDP Shortpath for public networks (STUN/TURN) is not supported** alongside Private Link for the session connection — if you need a direct UDP path in a Private Link deployment, you use **RDP Shortpath for managed networks** instead, over your private connectivity.

## Bandwidth Planning and Hybrid Connectivity

Bandwidth needs vary enormously by workload type — a data-entry task worker on a single monitor uses a small fraction of the bandwidth of a user running multiple 4K monitors with heavy video conferencing through the session. Rather than guessing, use Microsoft's published **RDP bandwidth requirements** guidance as a per-user starting point, broken out by usage pattern, and then:

1. Multiply the relevant per-user figure by your expected **concurrent** (not total) user count for the workload type you're sizing.
2. Add headroom for Teams media traffic if you're not offloading it (Teams optimization is covered in Module 5).
3. Validate against a real **pilot group** before finalizing a VPN or ExpressRoute circuit size — published guidance is a baseline, not a guarantee for your specific application mix.
4. For **hybrid connectivity** (on-prem file shares, line-of-business systems, domain controllers for hybrid-joined hosts), size the VPN gateway SKU or ExpressRoute circuit for the combined AVD session traffic and the backend traffic those sessions will generate, not just one or the other.

Getting the VNet layout, required connectivity, Shortpath configuration, and bandwidth sizing right up front is what turns AVD from "technically working" into an experience users don't think about — which is the actual bar for a production EUC platform.
