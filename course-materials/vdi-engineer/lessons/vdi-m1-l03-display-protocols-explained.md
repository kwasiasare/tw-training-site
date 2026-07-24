---
course: vdi-engineer
title: 'Display Protocols Explained: RDP, HDX, Blast Extreme, and Legacy PCoIP'
month: 1
monthTitle: VDI & EUC Foundations
lesson: 3
summary: The display protocol is the single biggest factor in whether a virtual desktop feels instant
  or feels like a bad video call. This lesson breaks down the four protocols you'll encounter as an EUC
  engineer — Microsoft's RDP with RDP Shortpath, Citrix HDX built on the ICA protocol, Omnissa's Blast
  Extreme, and the now-legacy PCoIP — covering how each moves pixels, why TCP-only transport hurts real-time
  interactivity, what codecs like H.264 and HEVC trade off, and the latency and bandwidth budgets that
  separate a usable session from an unusable one.
objectives:
- Explain what a display protocol actually does and why it dominates perceived VDI performance
- Compare RDP with RDP Shortpath, Citrix HDX/ICA, and Omnissa Blast Extreme by transport and codec approach
- Explain why UDP-based transport improves interactivity compared to pure TCP
- State the current status of PCoIP and what it means for platform selection in 2026
- Describe the latency and bandwidth factors that determine whether a session feels usable
- Identify which protocol characteristics matter most for a given workload (task work vs. graphics-heavy)
quiz:
- q: Why does a pure TCP-based connection generally feel worse for interactive VDI sessions than a UDP-based
    one?
  options:
  - TCP cannot carry encrypted traffic
  - TCP only works on wired networks
  - TCP's reliable, in-order delivery and congestion control introduce retransmission delay that shows
    up as input lag under network loss or jitter, while UDP-based transports can tolerate some loss and
    prioritize timeliness over perfect delivery
  - TCP cannot be used at all for remote desktop protocols
  answer: 2
  why: TCP guarantees ordered, reliable delivery, which is great for file transfer but means a single
    lost packet stalls everything behind it until it's retransmitted. Real-time interactive protocols
    favor UDP-based transports (RDP Shortpath, Citrix EDT/HDX, Blast Extreme over UDP) that can drop or
    adapt around loss without stalling the whole stream, keeping input and screen updates feeling responsive.
- q: What is RDP Shortpath's function within Azure Virtual Desktop and Windows 365?
  options:
  - It replaces RDP entirely with a new protocol
  - It is a VPN product sold separately from AVD
  - It only works for RemoteApp, not full desktops
  - It establishes a UDP-based transport between the client and session host (via managed network or public
    network STUN/TURN) to reduce latency, falling back to TCP-based reverse connect if it cannot be established
  answer: 3
  why: RDP Shortpath adds a UDP-based transport option on top of standard RDP. It tries a direct or STUN/TURN-relayed
    UDP path first for better latency and throughput, and falls back to the TCP-based reverse connect
    transport when a UDP path can't be established — it doesn't replace RDP, it augments it.
- q: Citrix HDX is built on top of which underlying remoting protocol?
  options:
  - ICA (Independent Computing Architecture)
  - RDP
  - PCoIP
  - Blast Extreme
  answer: 0
  why: HDX is Citrix's marketing and technology umbrella built on top of ICA, the Independent Computing
    Architecture protocol. HDX adds intelligent redirection, adaptive compression, and (via Enlightened
    Data Transport, EDT) UDP-based adaptive transport on top of the core ICA remoting protocol.
- q: As of 2026, what is the status of the PCoIP protocol and its main commercial product line?
  options:
  - PCoIP is being aggressively expanded as HP's flagship remote desktop protocol
  - HP announced it will stop selling HP Anyware (its PCoIP-based product) and Trusted Zero Clients from
    May 2026, with support ending in October 2026 (legacy Teradici Desktop Access contracts run to 2029),
    and Omnissa is also ending PCoIP support in Horizon — PCoIP should be treated as legacy
  - PCoIP was renamed Blast Extreme in 2024
  - PCoIP is now the default protocol for Azure Virtual Desktop
  answer: 1
  why: In April 2026, HP announced it would stop selling HP Anyware and PCoIP-based Trusted Zero Clients
    from May 7, 2026, with support for those products ending on October 31, 2026 — only legacy Teradici
    Desktop Access customers retain support until October 31, 2029. Omnissa has also moved to end PCoIP
    support within Horizon. Any 2026-current architecture should treat PCoIP as a legacy protocol being
    phased out, not a forward-looking choice.
- q: Which factor most directly determines whether typing and mouse movement in a VDI session feel instantaneous
    versus laggy?
  options:
  - The total storage capacity of the session host
  - The number of monitors connected to the session host
  - Round-trip network latency between client and session host, along with the protocol's ability to prioritize
    input/screen-update responsiveness over raw throughput
  - The Windows edition running on the golden image
  answer: 2
  why: Interactivity is dominated by round-trip latency and how well the protocol prioritizes responsiveness
    — high bandwidth alone doesn't fix a session that has to wait 300ms for every keystroke to round-trip.
    This is why protocol designers focus so heavily on transport (UDP-based paths) and adaptive prioritization
    rather than just raw compression ratio.
- q: In three to five sentences, explain why an EUC engineer designing for a graphics-intensive CAD workload
    would care about codec choice (H.264/AVC vs. HEVC) and give one concrete trade-off between the two.
  answer: Codec choice determines how efficiently the protocol compresses the screen content that has
    to be sent over the network every frame, which directly affects both bandwidth consumption and the
    visual quality a user perceives at a given bitrate — critical for CAD workloads with complex, fast-changing
    3D graphics. H.264/AVC is broadly compatible and has the widest hardware decode support across client
    devices, while HEVC (H.265) generally compresses more efficiently at the same visual quality, meaning
    lower bandwidth or better fidelity for the same link, but requires HEVC decode support on the client
    device and more encode overhead on the session host's GPU. An engineer sizing a GPU-backed host pool
    for CAD users would weigh HEVC's bandwidth savings against client device compatibility and the extra
    encode load on the host GPU.
  why: Codec selection is a direct trade-off between bandwidth efficiency, visual fidelity, client compatibility,
    and host-side encode cost, and it matters most precisely for graphics-heavy workloads like CAD where
    screen content changes constantly and at high detail.
resources:
- label: RDP Shortpath (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-shortpath
- label: Citrix HDX documentation
  url: https://docs.citrix.com/en-us/citrix-workspace-app-for-windows/hdx.html
- label: What is HDX? (Citrix glossary)
  url: https://www.citrix.com/glossary/what-is-hdx.html
- label: Omnissa Horizon Blast Extreme display protocol (TechZone)
  url: https://techzone.omnissa.com/resource/omnissa-horizon-blast-extreme-display-protocol
video: vdi-m1-l03-display-protocols-explained.mp4
---

## The Protocol Is the Product

Ask any long-time VDI admin what actually determines whether users complain, and the answer is almost never CPU or storage — it's the display protocol. Everything else in the stack can be perfectly sized and still produce a session that feels sluggish if the protocol is fighting a bad network path. This lesson covers the four protocols you need fluent working knowledge of: **RDP** (with RDP Shortpath), **Citrix HDX** (built on ICA), **Omnissa Blast Extreme**, and legacy **PCoIP** — plus the transport and codec concepts that explain why they behave the way they do.

## TCP vs. UDP: Why Transport Choice Comes First

Before comparing protocols, you need the transport-layer distinction underneath all of them.

- **TCP** guarantees reliable, in-order delivery. If a packet is lost, TCP stalls and retransmits before delivering anything after it. That's exactly right for a file download, and exactly wrong for real-time interactivity: on a lossy or high-latency link, that stall shows up to the user as the mouse pointer freezing or keystrokes lagging behind.
- **UDP** has no such guarantee — packets can arrive out of order or simply be dropped, with no automatic retransmission. On its own that sounds worse, but for real-time display protocols it's an advantage: the protocol can decide *which* frame to prioritize and simply skip a stale one rather than stalling the whole session waiting for a retransmit.

Every serious remote display protocol built in the last decade layers an adaptive, congestion-aware scheme on top of UDP to get reliability where it matters (input events, security handshakes) without full TCP-style stalling. That's exactly what RDP Shortpath, Citrix's Enlightened Data Transport (EDT), and Blast Extreme's UDP mode all do.

## RDP and RDP Shortpath

Standard RDP begins every connection as a TCP-based **reverse connect transport** — this is what lets Azure Virtual Desktop and Windows 365 avoid opening any inbound ports on session hosts, since the host and client both connect outward to the service. On top of that baseline, **RDP Shortpath** attempts to establish a parallel UDP-based path for better latency and throughput:

- **RDP Shortpath for managed networks** — a direct UDP connection over a private link such as ExpressRoute or a site-to-site VPN, either via a listener port (default UDP 3390) or via STUN if no inbound port is opened.
- **RDP Shortpath for public networks** — a direct UDP connection over the internet using STUN, falling back to a relayed connection via TURN if a direct path can't be established through NAT/firewalls.

If neither UDP path succeeds, the session simply continues over the original TCP reverse-connect transport — Shortpath is a performance upgrade, not a hard requirement, which is why it fails gracefully.

## Citrix HDX, Built on ICA

**ICA (Independent Computing Architecture)** is Citrix's original remoting protocol, dating back to WinFrame. **HDX** is the modern technology and marketing umbrella Citrix builds on top of ICA — it's not a separate protocol so much as ICA plus a large set of optimizations: intelligent redirection (deciding what to process locally vs. remotely, such as multimedia or browser content), adaptive compression, and data de-duplication. The transport-layer piece that matters most for interactivity is **Enlightened Data Transport (EDT)**, a UDP-based adaptive transport used for ICA connections — analogous in purpose to RDP Shortpath, giving Citrix sessions a responsive UDP path with a TCP-based fallback. Citrix also offers multiple encryption options for ICA traffic depending on deployment (Secure HDX/AES-256, HDX Direct with TLS/DTLS), which matters when you're designing for regulated environments.

## Omnissa Blast Extreme

**Blast Extreme** is Omnissa's protocol for Horizon, engineered to work well across a wide range of devices, networks, and media types. Its defining characteristics:

- Can run over **either TCP or UDP**, and will use UDP when available for better performance under adverse network conditions
- Uses **H.264/AVC by default** for video compression, with **HEVC (H.265)** available as an option for better compression efficiency where client hardware supports it
- Designed to scale across CPU cores efficiently and to take advantage of hardware encode/decode on both server and client where present

Blast Extreme is the protocol you'll configure for every Horizon deployment going forward — it fully superseded PCoIP as Omnissa's primary protocol, and PCoIP support is now being phased out of the platform entirely.

## PCoIP: Now a Legacy Protocol

PCoIP (PC-over-IP) was developed by Teradici (acquired by HP in 2021) and was historically the default protocol for VMware Horizon before Blast Extreme matured. As of 2026, treat PCoIP as **legacy, not a forward-looking option**: HP announced it will stop selling its PCoIP-based **HP Anyware** product and Trusted Zero Client hardware from May 7, 2026, with support for both ending on October 31, 2026 (only legacy Teradici Desktop Access contracts retain support through October 31, 2029). Omnissa has correspondingly moved to end PCoIP support within Horizon itself. If you inherit an environment still configured for PCoIP, your job is a migration plan to Blast Extreme (or another current protocol) on a timeline that respects the October 2026 support cutoff — not a reason to design new deployments around it.

## Codecs: What H.264 and HEVC Actually Trade Off

All of these protocols ultimately have to compress a constantly-changing screen image into a video-like stream, and the codec choice affects both bandwidth and visual quality:

- **H.264/AVC** is the universal baseline — broadly compatible, hardware-decodable on essentially every client device, a safe default.
- **HEVC (H.265)** generally compresses more efficiently at the same visual quality (or delivers better quality at the same bitrate), which matters for bandwidth-constrained links or high-resolution/high-frame-rate graphical workloads — but it requires HEVC decode support on the client and adds encode overhead on the host, usually offloaded to a GPU where available.

A general-purpose task-worker fleet is fine on H.264. A GPU-backed pool serving CAD or media professionals is exactly where the HEVC trade-off starts to matter.

## Latency and Bandwidth: What "Usable" Actually Means

Two numbers govern whether a session feels good:

- **Round-trip latency** is what interactivity actually depends on — every keystroke and mouse movement has to travel to the host and the resulting screen update has to come back. High latency (from long geographic distance, satellite links, or an overloaded network path) makes a session feel sluggish no matter how much bandwidth is available. As a rule of thumb, aim to keep round-trip latency low enough that input feels immediate; anything creeping toward a few hundred milliseconds becomes noticeably frustrating for interactive work.
- **Bandwidth** determines how much detail and motion the protocol can push through per second. A single office productivity session typically needs a modest, sub-megabit-to-low-single-digit-megabit budget; add video calls, multimedia redirection, or high-frame-rate 3D graphics and that budget climbs substantially — which is exactly why Module 3's networking lesson and Module 5's Teams/multimedia lesson both come back to bandwidth planning per workload type.

As an EUC engineer, your protocol decisions are never made in a vacuum — they're made against a specific network path and a specific workload. The rest of this course will keep returning to that pairing: protocol capability plus real network conditions equals the experience your users actually get.
