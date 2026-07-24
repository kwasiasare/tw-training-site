---
course: vdi-engineer
title: 'Zero Trust Across VDI Platforms: AVD, Citrix, and Omnissa'
month: 4
monthTitle: Identity & Security for Virtual Desktops
lesson: 4
summary: 'The controls from Lessons 1 through 3 are Azure-specific implementations of something bigger:
  Zero Trust applied to end-user computing. This lesson steps back to the vendor-neutral picture — the
  same identity, endpoint, session/app, data, network, and infrastructure pillars used throughout this
  site''s security content, now mapped across AVD, Citrix DaaS, and Omnissa Horizon. You''ll see Citrix
  Workspace App Protection and Omnissa''s Unified Access Gateway as the platform-specific equivalents
  of AVD''s screen capture protection and Conditional Access, learn where session recording fits on each
  platform, and leave with a single cross-platform Zero Trust checklist you can apply to any VDI estate,
  not just the one you happen to run today.'
objectives:
- Apply the Zero Trust principles — verify explicitly, least-privilege access, assume breach — and six
  pillars to a VDI/EUC context specifically
- Map AVD's identity, endpoint, session, and data controls from Lessons 1-3 onto the Zero Trust pillar
  each one defends
- Identify the Citrix DaaS equivalent controls, including Workspace App Protection and Citrix Cloud identity
  federation, for the same pillars
- Identify the Omnissa Horizon equivalent controls, including Unified Access Gateway hardening and Horizon
  Console RBAC, for the same pillars
- Evaluate a VDI platform's security posture using a single vendor-neutral Zero Trust checklist regardless
  of which platform it runs on
quiz:
- q: In the Zero Trust EUC mapping, which pillar do Microsoft Entra Conditional Access, Citrix Cloud identity
    federation, and a Horizon identity broker integration all primarily serve?
  options:
  - Network
  - Data
  - Identity
  - Infrastructure
  answer: 2
  why: All three are policy decision points that verify who is signing in and under what conditions before
    granting access — the core function of the identity pillar, regardless of vendor.
- q: Which Citrix Workspace app feature is the closest functional equivalent to AVD's screen capture protection?
  options:
  - Delivery Groups
  - Machine Creation Services
  - StoreFront
  - App Protection's anti-screen-capture and anti-keylogging controls
  answer: 3
  why: App Protection filters the OS-level APIs used to capture screens or keystrokes, blocking screenshots,
    screen recording, and keylogging — the same session-layer data-exfiltration risk that AVD's screen
    capture protection and watermarking address.
- q: Which Omnissa component is the closest equivalent to hardening an AVD Conditional Access-protected
    gateway or an AVD Private Link endpoint?
  options:
  - Unified Access Gateway (UAG), through its TLS/cipher hardening and edge-facing posture
  - App Volumes
  - Dynamic Environment Manager
  - Instant Clones
  answer: 0
  why: Unified Access Gateway is Horizon's edge-facing access point; hardening its TLS configuration and
    cipher suites is the Horizon-side equivalent of hardening the network/gateway posture that AVD achieves
    through Conditional Access and Private Link.
- q: A learner argues that because AVD has no single built-in session-recording feature comparable to
    Citrix Session Recording, AVD can't satisfy the 'assume breach' Zero Trust principle for session-layer
    visibility. What's the strongest counter-argument?
  options:
  - AVD doesn't need assume-breach controls because Microsoft manages the control plane
  - Assume-breach visibility on AVD comes from a different toolset — Microsoft Defender for Endpoint,
    Azure Virtual Desktop Insights, and Log Analytics — not a single recording feature; the principle
    is satisfied by the outcome, not by matching a specific competitor feature
  - Watermarking makes session recording unnecessary in every scenario
  - Screen capture protection replaces the need for any session visibility
  answer: 1
  why: Zero Trust principles are about outcomes — verify, minimize privilege, detect and respond — not
    feature parity with a specific competitor. AVD achieves session-layer visibility through a different
    combination of tools, which is a valid way to satisfy assume breach.
- q: Which statement correctly describes a vendor-neutral Zero Trust checklist item for the identity pillar
    that applies equally to AVD, Citrix DaaS, and Omnissa Horizon?
  options:
  - Every platform must use exactly the same Conditional Access app IDs
  - Every platform must be Microsoft Entra joined
  - Every platform's control plane must verify identity and enforce MFA and conditional policy before
    granting session access, regardless of which product implements the policy engine
  - Every platform must disable session recording
  answer: 2
  why: The vendor-neutral principle is the requirement itself — explicit verification and conditional
    policy enforcement before granting session access — not a specific vendor's implementation detail
    like an app ID.
- q: In three to four sentences, using the Zero Trust six-pillar model, describe how you would evaluate
    the security posture of a Citrix DaaS estate you've never seen before, without assuming it uses any
    AVD-specific tooling.
  answer: 'I''d walk the six pillars and ask what enforces each one on this specific estate: for identity,
    whether Citrix Cloud federates to Microsoft Entra ID or another identity provider with MFA and Conditional
    Access enforced at sign-in; for endpoint, whether the VDAs (session hosts) are enrolled in an endpoint
    management and EDR tool and kept patched; for apps/session, whether Workspace App Protection or an
    equivalent anti-capture and anti-keylogging control is enabled on sensitive Delivery Groups; for data,
    whether profile and file-share access is scoped and encrypted; for network, whether the Citrix Cloud
    Connectors and gateway are hardened without unnecessary inbound ports; and for infrastructure, whether
    the hypervisor or cloud resource layer has its own posture management. The point is to evaluate by
    function against each pillar rather than by searching for AVD-specific product names that won''t exist
    in a Citrix environment.'
  why: A vendor-neutral Zero Trust evaluation asks what control serves each pillar's function on the platform
    actually in front of you, rather than checking for the presence of a specific product from a different
    vendor.
resources:
- label: Zero Trust security overview (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/security/zero-trust/zero-trust-overview
- label: App Protection overview (Citrix Workspace app)
  url: https://docs.citrix.com/en-us/citrix-workspace-app/app-protection.html
- label: Omnissa Unified Access Gateway Security Guide
  url: https://docs.omnissa.com/bundle/UnifiedAccessGatewaySecurityGuideV2309/page/Aboutthisbook-UnifiedAccessGatewaySecurityGuide.html
- label: Azure Private Link with Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview
- label: Azure Virtual Desktop identities and authentication
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/authentication
video: vdi-m4-l04-zero-trust-across-vdi-platforms.mp4
---

## What the Last Three Lessons Were Really Teaching

Lessons 1 through 3 taught AVD-specific mechanics: join types, RBAC roles, Conditional Access app IDs, Intune enrollment rules. But step back and every one of those was an implementation of the same underlying model this site uses across its security content: Zero Trust, built on three principles — verify explicitly, use least-privilege access, and assume breach — applied across six pillars: identity, endpoints, apps, data, infrastructure, and network. AVD is one implementation of that model. Citrix DaaS and Omnissa Horizon are others. If you only know the AVD product names, you can't evaluate a Citrix or Horizon estate at all. If you know the pillars, you can evaluate any of them, including whatever replaces all three in five years.

## The Six Pillars, Mapped to EUC

Here's the vendor-neutral mapping, with the AVD-specific control from earlier lessons alongside its Citrix and Omnissa equivalents:

| Pillar | AVD (Lessons 1-3) | Citrix DaaS | Omnissa Horizon |
|---|---|---|---|
| **Identity** | Microsoft Entra ID join types, Conditional Access, SSO | Citrix Cloud identity, federated to Entra ID or another IdP | Horizon identity broker, federated to an IdP |
| **Endpoint** | Intune device management, Microsoft Defender for Endpoint | Citrix endpoint management / third-party MDM + EDR | Workspace ONE (or third-party) MDM + EDR |
| **Apps / Session** | Screen capture protection, watermarking, RDP redirection lockdown | Workspace App Protection (anti-capture, anti-keylogging) | Horizon session controls, clipboard/USB redirection policy |
| **Data** | FSLogix profile scoping, storage RBAC | Profile Management / App Volumes scoping | Dynamic Environment Manager, App Volumes scoping |
| **Network** | Conditional Access + Private Link, Azure Firewall egress | Cloud Connectors, gateway/StoreFront hardening | Unified Access Gateway (UAG) TLS/cipher hardening |
| **Infrastructure** | Trusted Launch, Compute Gallery image hygiene | Machine Creation Services image hygiene | Instant Clones image hygiene |

The point of this table isn't memorization — it's the habit of asking "what serves this pillar here?" on any platform, rather than looking for a specific product name you already know.

## Citrix DaaS: App Protection as the Session/Data Control

Where AVD uses screen capture protection and watermarking to stop unauthorized extraction from an authorized session, Citrix's equivalent is **App Protection** in the Citrix Workspace app: anti-screen-capture blocks screenshots, screen recording, mirroring, and app switching over a protected session, while anti-keylogging scrambles keystrokes at the kernel level before a keylogger can read them, for both physical and on-screen keyboards. Like AVD's controls, it can be applied contextually — **Contextual App Protection** lets you scope policies to specific users, devices, or network posture rather than applying one blanket rule everywhere, mirroring how you'd scope AVD's Conditional Access policies by group and device filter.

On identity, Citrix Cloud is the control plane, and it federates outward to Microsoft Entra ID or another identity provider — meaning MFA and Conditional Access enforcement for a Citrix estate is frequently still an Entra ID policy underneath, just fronted by Citrix Cloud rather than the AVD service directly. This is a useful fact when you're assessing an estate you don't own: the Zero Trust identity control might already exist, just not where you first looked.

## Omnissa Horizon: The Gateway as the Hardening Surface

Horizon's architecture puts more weight on a single edge component: **Unified Access Gateway (UAG)**. Where AVD achieves network-pillar Zero Trust through Conditional Access plus optional Azure Private Link (removing the need to expose the service to the public internet at all), Horizon's equivalent hardening surface is the UAG itself — its TLS configuration and cipher suite selection, which can be updated post-deployment through the UAG admin console or REST API, and its placement as the sole edge-facing component in front of Connection Servers and session hosts. A Horizon estate with a well-hardened UAG but a weak identity broker configuration is exactly the kind of imbalance the pillar model is built to catch — strong network pillar, weak identity pillar, still an overall gap.

## Session Recording: Where Each Platform Lands

Session recording is a good test case for the "assume breach" principle, because the three platforms implement it differently and none of them is wrong:

- **Citrix** ships a dedicated **Session Recording** component that captures and can play back ICA sessions for compliance and forensic review.
- **Omnissa Horizon** doesn't ship a first-party session-recording product in the same way; visibility instead comes through Helpdesk tooling and UAG/Connection Server logging, often paired with third-party session recording where compliance demands it.
- **AVD** has no single built-in session-recording feature either. Assume-breach visibility instead comes from a different combination — Microsoft Defender for Endpoint telemetry, Azure Virtual Desktop Insights, and Log Analytics KQL queries across connection and session events (the toolset Module 6 covers in depth).

The lesson isn't "Citrix wins because it has a dedicated feature." It's that assume breach is satisfied by the *outcome* — can you detect and reconstruct what happened after the fact — not by matching a specific competitor's product name. A platform without a "Session Recording" button can still fully satisfy the principle through other tooling, and a platform with one can still fail the principle if nobody reviews the recordings.

## A Cross-Platform Zero Trust Checklist

Whatever platform lands on your desk, walk the same six questions instead of hunting for AVD-specific settings that won't exist:

1. **Identity** — Is every sign-in verified against MFA and a conditional policy, and is that policy engine actually enforced, not just configured?
2. **Endpoint** — Are the session hosts/VDAs enrolled in device management and EDR, patched, and free of tamper-protection gaps?
3. **Apps/Session** — Is there an anti-capture, anti-keylogging, or equivalent control on sessions handling sensitive data, scoped contextually rather than blanket-applied?
4. **Data** — Are profiles, redirected folders, and file shares scoped to least privilege and encrypted in transit and at rest?
5. **Network** — Is the gateway/edge component hardened, and is inbound exposure minimized (Private Link, UAG hardening, or equivalent)?
6. **Infrastructure** — Is the golden image current, and is the underlying compute/hypervisor layer under its own posture management?

## Closing the Module

This module started with a single identity decision in Lesson 1 and ends with a checklist that works on a platform this course hasn't even named. That's the actual skill AZ-140 Domain 2 and the broader EUC-engineer role are testing for: not memorizing where a button lives, but knowing which Zero Trust pillar a problem belongs to, and being able to find that pillar's control on whatever platform you're handed. Module 5 picks the thread back up on the user-environment side — FSLogix in depth, app delivery, and Teams optimization — building on the identity and profile-storage foundation this module set.
