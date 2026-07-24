---
course: vdi-engineer
title: 'VDI Architecture: The Universal Building Blocks'
month: 1
monthTitle: VDI & EUC Foundations
lesson: 2
summary: 'Strip away the vendor branding and every VDI or DaaS platform — Azure Virtual Desktop, Citrix
  DaaS, Omnissa Horizon, Windows 365 — is built from the same five parts: a control plane/broker, a gateway/access
  layer, session hosts, golden images, and a profile layer. This lesson walks the full connection flow
  from user click to desktop pixels, defines each building block in vendor-neutral terms, and explains
  the difference between agent-based and agentless host registration so you can recognize the same architecture
  no matter which product''s console you''re looking at.'
objectives:
- Name the five universal building blocks present in every VDI/DaaS platform
- Trace the full connection flow from user request to established session, step by step
- Explain what a connection broker does and why it's the decision-making core of the platform
- Distinguish the gateway/access layer's job from the broker's job
- Compare agent-based and agentless session host registration and state a trade-off for each
- Explain why golden images and the profile layer exist as separate concerns from the OS itself
quiz:
- q: What is the primary job of the connection broker in a VDI/DaaS architecture?
  options:
  - Encrypting network traffic between the client and the datacenter
  - Deciding which session host a user's request should be routed to, and brokering that connection
  - Storing the user's profile data
  - Rendering the desktop's graphics
  answer: 1
  why: 'The broker (control plane) is the decision-maker: it authenticates the request against entitlements,
    checks host pool state and load, and hands the client a route to a specific session host. It doesn''t
    move pixels or store profiles itself — that''s the gateway''s and profile layer''s job respectively.'
- q: Why do most modern cloud VDI platforms use a gateway/access layer instead of exposing session hosts
    directly to the internet?
  options:
  - Gateways make golden images smaller
  - Gateways are only needed for non-persistent desktops
  - Gateways allow the platform to avoid opening any inbound ports on session hosts by using reverse/outbound
    connections
  - Gateways replace the need for a broker entirely
  answer: 2
  why: 'The gateway/access layer is the front door: session hosts establish outbound (reverse) connections
    to the service, so no inbound ports need to be opened on the hosts themselves. This is why Azure Virtual
    Desktop, for example, requires no inbound firewall rules to session host VMs.'
- q: What is a golden image, and why is it a separate concept from the profile layer?
  options:
  - A golden image is the user's personal desktop background; the profile layer manages wallpaper settings
  - A golden image and the profile layer are two names for the same thing
  - A golden image is only used for personal/persistent desktops, never for pooled ones
  - A golden image is the standardized OS + apps template every session host is built from; the profile
    layer carries the user-specific data and settings on top of that shared template
  answer: 3
  why: The golden image is the common, versioned template (OS, patches, line-of-business apps) that every
    session host is provisioned from. The profile layer separately carries what makes a session feel personal
    to a user — documents, app settings, browser data — so that identical images can serve many different
    users.
- q: What is the key operational difference between agent-based and agentless session host registration?
  options:
  - Agent-based registration installs a platform-specific agent/service on each host that maintains a
    live connection to the broker; agentless approaches rely on the hypervisor or cloud platform's own
    APIs to track host state
  - Agent-based hosts don't need a golden image
  - Agentless hosts cannot join a domain
  - There is no meaningful difference; the terms are interchangeable
  answer: 0
  why: Agent-based platforms (Citrix VDA, Omnissa Horizon Agent, the AVD agent) run a service on every
    session host that reports health and availability to the broker. Agentless approaches lean more heavily
    on the underlying platform (hypervisor/cloud APIs) for host state, trading some flexibility for less
    on-host software to manage.
- q: 'Put these connection-flow steps in the correct order: (A) broker selects an available session host,
    (B) user authenticates to the control plane, (C) client establishes a session directly or via the
    gateway to the assigned host, (D) user opens the client and requests their desktop/app feed.'
  options:
  - B, D, A, C
  - D, B, A, C
  - A, B, D, C
  - D, A, B, C
  answer: 1
  why: The user opens the client and requests their feed (D), authenticates (B), the broker evaluates
    entitlements and picks a host (A), then the session is established to that host, typically via the
    gateway (C).
- q: In three to five sentences, walk through the full connection flow for a pooled desktop from the moment
    a user clicks 'Connect' to the moment they see their desktop, naming each building block involved.
  answer: The user opens their client and authenticates through the control plane's identity check, which
    validates their entitlement to a given desktop or app group. The broker then evaluates the available
    session hosts in the assigned host pool — checking health, load, and (for pooled/non-persistent hosts)
    whether the user already has an active session to reconnect to — and selects a target host. The client
    is handed a connection ticket and routed through the gateway/access layer, which relays or brokers
    the session so the host never needs an open inbound port. Once the session lands on the host, the
    profile layer mounts the user's profile container so their settings and data appear as if local, completing
    the connection.
  why: 'This traces all five building blocks in order: control plane/broker for authentication and host
    selection, session hosts as the compute target, the gateway/access layer for secure connectivity,
    and the profile layer for personalization — the same flow underlies AVD, Citrix DaaS, and Omnissa
    Horizon regardless of branding.'
resources:
- label: Azure Virtual Desktop network connectivity (reverse connect / gateway)
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity
- label: Azure Virtual Desktop host pools overview
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/host-pool-overview
- label: Citrix DaaS documentation
  url: https://docs.citrix.com/en-us/citrix-daas
- label: Omnissa Horizon 8 overview (TechZone)
  url: https://techzone.omnissa.com/resource/what-horizon-8
---

## One Architecture, Many Logos

Open the Azure portal, the Citrix Cloud console, and Omnissa Horizon Console side by side and they look nothing alike. But underneath, every one of them is solving the same problem with the same five parts: a **control plane/broker** that makes decisions, a **gateway/access layer** that moves traffic securely, **session hosts** that do the actual computing, **golden images** that define what those hosts look like, and a **profile layer** that makes a shared or disposable host feel personal to one user. Learn this shape once and you can read any vendor's documentation faster, because you're mapping their terminology onto a structure you already understand.

## Building Block 1: The Control Plane / Broker

The broker is the brain. When a user requests a desktop or app, the broker is what decides: *is this user entitled to this resource, and which specific session host should serve them right now?* Concretely, the broker:

- Validates the user's identity and checks their entitlement (are they a member of the group assigned to this desktop/app group?)
- Tracks the real-time state of every session host in a host pool — powered on or off, current session count, health
- For non-persistent/pooled desktops, decides whether to reconnect the user to an existing disconnected session or place them on a fresh host
- Issues a connection ticket that authorizes the client to connect to a specific host

In Azure Virtual Desktop, this is the AVD service's broker component (fully Microsoft-managed — you never see or patch it). In Citrix DaaS, this is the **Delivery Controller** function, exposed through Citrix Cloud. In Omnissa Horizon, this is the **Connection Server** role. Different names, identical job.

## Building Block 2: The Gateway / Access Layer

The gateway is the front door between the outside world and your session hosts. Its defining property in every modern cloud-delivered platform is **reverse connect**: the session host initiates an *outbound* connection to the service, so administrators never need to open an inbound port on the host itself. The client also connects outbound to the same gateway, and the service brokers the two together.

This matters operationally: a session host sitting in a private subnet with no public IP and no inbound firewall rule can still serve users anywhere in the world, because it reached out first. AVD's gateway is Microsoft-managed. Citrix uses **Citrix Gateway service** (cloud) or on-prem Citrix ADC/Gateway appliances. Omnissa Horizon uses the **Unified Access Gateway (UAG)**. Same job, three names.

## Building Block 3: Session Hosts

Session hosts are where the actual computing happens — the VM (or, in RDS-style deployments, the shared server) that runs the desktop OS and applications the user interacts with. They can be:

- **Personal/persistent** — one dedicated VM per user, state preserved between sessions
- **Pooled/non-persistent** — a shared pool of interchangeable VMs, any of which can serve any entitled user, typically reset to a clean state on logoff

Session hosts register themselves with the broker so it knows they exist and are healthy — which brings us to agent-based vs. agentless registration, covered below.

## Building Block 4: Golden Images

A golden image is the standardized template — OS version, patches, agents, line-of-business applications, security tooling — that every session host in a pool is built from. Instead of hand-configuring a thousand VMs, you build and validate one image, version it, and roll it out. This is what makes fleets of identical, disposable session hosts practical: when something's wrong, you don't troubleshoot the VM, you rebuild it from a known-good image. Azure Compute Gallery, Citrix Machine Creation Services (MCS) templates, and Omnissa's Instant Clone parent VMs are all implementations of this same idea — you'll go deep on image management in Module 3.

## Building Block 5: The Profile Layer

If golden images make every host identical, the profile layer is what makes each *session* feel personal despite that. It carries the user-specific state — documents, application settings, browser profile, taskbar pins — separately from the OS, typically as a mountable container attached at logon. This is what allows a genuinely stateless, disposable pooled host to still feel like 'my desktop' to the person using it. FSLogix (Microsoft), Citrix Profile Management, and Omnissa Dynamic Environment Manager (DEM) are the concrete tools here — Lesson 4 of this module is dedicated entirely to this layer.

## The Full Connection Flow

Putting the five blocks together, here is what happens end to end when a user connects to a pooled desktop:

1. **User opens the client** (native app, Windows App, or a browser) and requests their feed of available desktops/apps.
2. **Authentication** happens against the identity provider (Microsoft Entra ID, Active Directory, or a Citrix/Omnissa-integrated identity source).
3. **The broker evaluates entitlement and host pool state** — is this user allowed here, is there a disconnected session to reconnect to, which healthy host has capacity — and selects a target session host.
4. **A connection ticket is issued** to the client, authorizing a session to that specific host.
5. **The client connects through the gateway/access layer**, which relays the session so the host needs no inbound port open.
6. **The session lands on the session host**, and the **profile layer mounts the user's profile container**, so documents and settings appear as if local.
7. **The display protocol takes over** (Lesson 3 covers this in depth), streaming the desktop and carrying input back.

## Agent-Based vs. Agentless Registration

How does the broker know a session host exists and is healthy? Two models:

- **Agent-based**: a platform-specific service runs on every session host (the AVD agent, the Citrix Virtual Delivery Agent/VDA, the Omnissa Horizon Agent) and maintains a live heartbeat connection to the broker, reporting health, session count, and readiness. This is the dominant model today because it gives the broker rich, real-time state independent of the underlying hypervisor.
- **Agentless**: the platform instead leans on the hypervisor's or cloud provider's own APIs to infer host state (is the VM running, is it responding to health probes), without a dedicated agent service. This trades some richness of signal for a smaller footprint on the host.

In practice, almost every production VDI platform you'll operate — AVD, Citrix DaaS, Omnissa Horizon — uses agent-based registration for session hosts, because the agent is also what plumbs the display protocol, redirection channels, and management commands. Keep the term in mind, though: you'll see "agentless" architecture discussions come up when comparing lighter-weight or browser-only remote access tools against full VDI platforms.

Once these five blocks and this connection flow are second nature, every platform-specific lesson later in this course becomes a matter of learning what a vendor *calls* each part — not learning a new architecture from scratch.
