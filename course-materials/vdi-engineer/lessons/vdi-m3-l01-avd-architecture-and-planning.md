---
course: vdi-engineer
title: 'AVD Architecture and Planning: Control Plane, Host Pools, and App Groups'
month: 3
monthTitle: 'Azure Virtual Desktop Infrastructure: Plan, Deploy & Scale'
lesson: 1
summary: This lesson builds the architectural mental model for everything else in this module. You'll
  learn exactly what Microsoft manages versus what you manage in Azure Virtual Desktop, why reverse connect
  means you never open an inbound port to a session host, and how host pools, application groups, and
  workspaces fit together to publish desktops and apps to users. You'll also learn the personal-vs-pooled
  decision, validation vs production host pools, and the practical service limits that shape how you design
  at scale — the foundation for AZ-140 Domain 1.
objectives:
- Draw the line between the Microsoft-managed AVD control plane and the customer-managed session host
  layer
- Explain reverse connect and why AVD requires no inbound firewall ports to session hosts
- Differentiate personal and pooled host pools and choose the correct load-balancing algorithm for a pooled
  pool
- Explain how host pools, application groups (Desktop vs RemoteApp), and workspaces relate and how they
  publish resources to users
- Justify when to use a validation host pool versus a production host pool
- Identify the practical service limits and planning constraints that shape host pool design at scale
quiz:
- q: Which statement correctly describes the Azure Virtual Desktop control plane?
  options:
  - The customer deploys and patches the broker, web, and gateway services in their own subscription
  - The control plane and session hosts are both fully managed by Microsoft with no customer configuration
  - Microsoft hosts and manages the broker, web, and gateway/diagnostics services; the customer owns the
    session host VMs and the resources they access
  - The control plane runs inside the customer's virtual network alongside the session hosts
  answer: 2
  why: 'AVD is a managed service: Microsoft operates the connection broker, web access/feed, gateway,
    and diagnostics components at global scale. The customer''s responsibility is the session host VMs
    (compute, OS, image, network) and everything those VMs can reach — that split is the first thing to
    internalize about AVD architecture.'
- q: Why doesn't Azure Virtual Desktop require an inbound firewall rule or a public IP on the session
    host VM for users to connect?
  options:
  - Because session hosts only accept connections from the same virtual network
  - Because RDP traffic is tunneled through Microsoft Entra ID by default
  - Because Azure Bastion is automatically deployed with every host pool
  - Because the AVD agent on the session host establishes an outbound, persistent connection ('reverse
    connect') to the AVD service, which then relays the user's session over that channel
  answer: 3
  why: The AVD agent on each session host initiates an outbound connection to the Azure Virtual Desktop
    service (reverse connect). User sessions are relayed over that already-established outbound channel,
    so you never need an inbound port open, a public IP, or a VPN just to allow users to reach the host
    — you only need outbound access to the required AVD endpoints.
- q: A pooled host pool needs to keep placing new sessions on the least-loaded host until the pool is
    close to full, then even it out over time. Which load-balancing algorithm fits, and which host pool
    type does NOT use load balancing at all?
  options:
  - Breadth-first fits the requirement; personal host pools don't use load balancing because each user
    has a dedicated, assigned host
  - Depth-first fits the requirement; pooled host pools don't use load balancing
  - Breadth-first fits the requirement; pooled host pools don't use load balancing
  - Depth-first fits the requirement; personal host pools use breadth-first by default
  answer: 0
  why: Breadth-first spreads new sessions evenly across all available session hosts, maximizing performance
    per user — the description in the question. Depth-first instead fills one host to its session limit
    before moving to the next, which is better for cost-driven consolidation. Personal host pools assign
    each user a specific, dedicated VM, so there's no pool of interchangeable hosts to balance across.
- q: What is the relationship between an application group and a host pool in Azure Virtual Desktop?
  options:
  - An application group can span multiple host pools to aggregate resources for a single user base
  - An application group is a logical grouping of desktops or apps published from the session hosts of
    exactly one host pool, and it cannot exist without that host pool
  - An application group replaces the need for a workspace
  - An application group defines the VNet and subnet the session hosts use
  answer: 1
  why: Every application group (Desktop or RemoteApp type) is tied to a single host pool and publishes
    resources from that pool's session hosts. Workspaces sit a layer above and aggregate one or more application
    groups so users see a single feed; a host pool with no application group publishes nothing to users.
- q: Why would you deploy a small validation host pool alongside your production host pools?
  options:
  - Validation host pools are required by Microsoft licensing before any production pool can be created
  - Validation host pools automatically mirror production pool capacity for disaster recovery
  - A validation pool lets you receive new AVD service updates and agent changes early, on a small blast
    radius, before they roll out broadly to production so you can catch regressions
  - Validation host pools are the only pool type that supports RemoteApp publishing
  answer: 2
  why: Marking a host pool as a validation environment opts it into early exposure to AVD service-side
    changes and agent updates. Running a small validation pool with a subset of test users lets you catch
    a regression before it reaches your production fleet — the same 'canary ring' idea used across Azure
    services.
- q: In two to four sentences, explain what the Azure portal's practical create-flow cap of 500 session
    hosts per host pool means for planning a 3,000-user pooled deployment, and describe one way an engineer
    works around it.
  answer: The Azure portal's host pool creation wizard caps how many session hosts you can add in a single
    create operation at 500, which is a UI/workflow limit rather than a hard architectural ceiling on
    the host pool resource itself. For a 3,000-user pooled deployment you plan capacity in batches — provisioning
    and registering session hosts to the same host pool across multiple deployment runs (portal, PowerShell/Az.DesktopVirtualization,
    or Bicep pipelines), or splitting the user base across multiple host pools with a shared workspace
    so no single deployment operation has to add more hosts than the tooling supports at once. Either
    way, the design decision is made at the automation/pipeline level, not by trying to force one enormous
    single-shot deployment.
  why: Real AVD deployments at scale are always built incrementally — through IaC pipelines that add session
    hosts in batches or by partitioning users across several host pools — rather than in one operation,
    and engineers need to plan vCPU quota, availability-set, and deployment-tooling limits alongside the
    host pool's own configuration.
resources:
- label: What is Azure Virtual Desktop?
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/overview
- label: Azure Virtual Desktop terminology
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/terminology
- label: Configure host pool load balancing in Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-host-pool-load-balancing
- label: Preferred application group type behavior for pooled host pools
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/preferred-application-group-type
- label: Azure Virtual Desktop FAQ
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/faq
video: vdi-m3-l01-avd-architecture-and-planning.mp4
---

## Why This Lesson Exists

AZ-140's biggest domain — planning and implementing an AVD infrastructure — is worth 40 to 45% of the exam, and every task in it assumes you already have the architectural picture in your head. Before you touch a Bicep template or an autoscale plan, you need to know exactly what Microsoft runs for you, what you run yourself, and how the building blocks — host pools, application groups, workspaces — snap together. Get this model right and every later lesson in this module is just filling in detail. Get it wrong and you'll misdiagnose problems for the rest of your AVD career.

## The Control Plane vs. The Session Host Layer

Azure Virtual Desktop is a **managed desktop and app virtualization service** with a hard architectural split:

- **Microsoft-managed control plane**: the connection broker (matches a user to an available session), the web/feed service (what shows up in the client), the gateway (relays session traffic), diagnostics, and the global load-balancing infrastructure. You never patch this, never see a VM for it, and never pay compute for it directly — it's part of the AVD service, available at no additional licensing cost beyond your eligible Windows/Microsoft 365 or per-user access rights.
- **Customer-managed session host layer**: the actual Windows 11 Enterprise multi-session (or single-session) VMs that run in *your* subscription, *your* virtual network, with *your* image, *your* patching cadence, and *your* cost. This is the layer this entire module teaches you to design, deploy, and scale.

This split matters practically: when a user can't log in, the first triage question is always "is this a control-plane problem (feed, broker, auth) or a session-host problem (VM unreachable, agent unhealthy, image broken)?" You'll build that triage skill fully in Module 6, but the architecture split is where it starts.

## Reverse Connect: No Inbound Ports, Ever

A question every AVD newcomer asks: "what inbound NSG rule do I need so users can RDP into my session hosts?" The answer is **none**. AVD uses **reverse connect**: the AVD agent installed on each session host initiates an *outbound* TLS connection to the Azure Virtual Desktop service the moment the VM boots and the agent registers. That connection stays open. When a user connects, their session is relayed to the host over that already-established outbound channel — the session host never has to accept an inbound connection from the internet or even from inside your VNet.

The practical consequence: your session host subnet's NSG needs **outbound** access to the required AVD service endpoints (and to package/patch sources, and anything the user's apps need) — but no inbound rule for RDP is required for the AVD connection itself, and you should not open one. You'll cover the exact required outbound URLs and service tags in the next lesson on AVD networking.

## Host Pools: The Core Compute Object

A **host pool** is a collection of Azure VMs registered as session hosts to the same AVD deployment. Every host pool has a type, set at creation and immutable afterward:

- **Personal**: each user is assigned a specific, dedicated VM (either automatically or by an admin). State persists on that VM between sessions. No load balancing applies — there's nothing to balance, the user always lands on their own machine.
- **Pooled**: many users share a pool of interchangeable, typically non-persistent, multi-session hosts. The broker decides which host a given session lands on using a **load-balancing algorithm**:
    - **Breadth-first** — spreads new sessions across all available hosts to keep per-host load low and performance high. The default and right choice for most knowledge-worker pools.
    - **Depth-first** — fills one host to its `maxSessionLimit` before moving to the next, minimizing the number of running hosts. Pairs naturally with autoscale for cost-sensitive pools where you want to consolidate load onto as few running VMs as possible.

A pooled host pool also sets a **preferred application group type** (Desktop or RemoteApp), which governs default behavior when a user is assigned to both a Desktop and a RemoteApp application group on the same pool — one more reason the pool, not just the app group, is a planning-time decision.

**Validation vs. production**: any host pool — personal or pooled — can be flagged as a **validation environment**. Validation pools receive Azure Virtual Desktop service-side updates and agent changes ahead of production pools, so a small validation pool with a handful of pilot users acts as your canary ring for catching a regression (an agent bug, a broker behavior change) before it reaches the fleet everyone depends on. Plan for at least one validation pool per environment tier you support.

## Application Groups: What Gets Published

An **application group** is a logical container of resources published from a single host pool's session hosts. It comes in two flavors:

- **Desktop application group**: publishes the full desktop. A host pool can have at most one Desktop application group.
- **RemoteApp application group**: publishes one or more individual applications rather than the whole desktop. A host pool can have several RemoteApp application groups, each with a different set of apps assigned to different user groups.

An application group cannot exist independently of a host pool — it's always scoped to exactly one pool — and users are granted access by assigning a Microsoft Entra ID security group (never individual users, as a matter of practice) to the application group.

## Workspaces: What Users See

A **workspace** is the layer users actually experience: it's a logical grouping of one or more application groups, and it's what shows up as a single feed in the Remote Desktop client or web client. Without associating an application group to a workspace, users have access rights but see nothing in their feed — a classic "deployed correctly but nobody can find it" support ticket. A typical design associates several RemoteApp application groups (finance apps, engineering apps) and one Desktop application group into a single workspace per business unit or use case, so the user's feed reflects exactly what they're entitled to, from wherever they sign in.

## Service Limits Worth Planning Around

A few practical constraints shape how you design at scale rather than assume infinite elasticity:

- The Azure **portal's host pool creation wizard** caps a single create operation at 500 session hosts; larger fleets are built by adding hosts in batches through automation (PowerShell, Bicep/ARM, or CLI pipelines) across multiple runs, or by splitting users across multiple host pools sharing one workspace.
- **Availability sets** used for session hosts are capped like any other Azure availability set (200 VMs), which is one more reason large pools lean on availability zones (covered in the BCDR lesson) rather than a single oversized availability set.
- Regional **vCPU quota** is almost always the real bottleneck before any AVD-specific limit — request quota increases early in a rollout, not the week before go-live.
- Each **host pool registration token** used to join new session hosts has an expiration time you set (up to 30 days) — plan your automation to regenerate it rather than treating it as permanent.

## Putting It Together

When you plan an AVD environment, you're really answering four questions in order: which **host pool type** fits the user population (personal for 1:1 persistent desktops, pooled for shared knowledge-worker or task-worker capacity); which **load-balancing algorithm** fits the cost/performance trade-off for a pooled pool; what **application groups** need to be published (one desktop, or a curated set of RemoteApps, or both); and which **workspace** each user's application groups should land in so their feed is coherent. Everything else in this module — networking, images, deployment automation, autoscale, and BCDR — is built on top of the answers to those four questions.
