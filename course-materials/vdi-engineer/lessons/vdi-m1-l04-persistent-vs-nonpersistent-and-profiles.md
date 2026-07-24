---
course: vdi-engineer
title: Persistent vs. Non-Persistent Desktops and the Profile Layer
month: 1
monthTitle: VDI & EUC Foundations
lesson: 4
summary: 'Whether a virtual desktop is persistent or non-persistent is one of the first and most consequential
  decisions in any VDI design — it drives storage cost, patching strategy, and how badly you need profile
  tooling. This lesson defines pooled vs. personal/dedicated desktops, explains why non-persistent pools
  are unusable without a profile solution, and surveys the three tools you''ll actually deploy: Microsoft
  FSLogix, Citrix Profile Management, and Omnissa Dynamic Environment Manager (DEM) — including the difference
  between legacy folder redirection and modern container-based profiles.'
objectives:
- Define pooled/non-persistent and personal/dedicated desktop models and their trade-offs
- Explain why non-persistent desktops require a dedicated profile management tool
- Identify FSLogix, Citrix Profile Management, and Omnissa DEM as the three category tools and what each
  belongs to
- Compare folder redirection with container-based profile solutions
- Explain the storage and licensing implications of profile container placement
- Recognize common profile failure symptoms so you know when this layer is the root cause
quiz:
- q: What best distinguishes a pooled (non-persistent) desktop from a personal (persistent) desktop?
  options:
  - Pooled desktops use a different display protocol
  - Personal desktops cannot use FSLogix
  - Pooled desktops require more storage per user than personal desktops
  - In a pooled desktop, the user gets any available VM from a shared pool and changes are typically discarded
    on logoff/reset; a personal desktop is a dedicated VM that retains its state between sessions
  answer: 3
  why: The defining trait is state persistence at the machine level. Pooled/non-persistent hosts are interchangeable
    and reset to a clean state, which is what makes patching and image management dramatically simpler
    at scale. Personal/persistent desktops keep their own disk state between sessions, more like a traditional
    PC, at higher per-user storage cost.
- q: Why is a dedicated profile management tool considered mandatory (not optional) for non-persistent
    pooled desktops?
  options:
  - Because without it, any changes a user makes — documents, settings, browser data — are discarded the
    moment their session ends and they land on a different VM next time, so nothing feels 'theirs'
  - Because Windows cannot boot without one
  - Because it is required to enable RDP Shortpath
  - Because pooled desktops cannot join Active Directory otherwise
  answer: 0
  why: Non-persistent hosts are reset to a clean golden-image state on logoff, and the next session might
    land on an entirely different VM. Without a profile layer that reattaches the user's data and settings
    at logon, users would lose everything every session — profile management is what makes disposable,
    identical hosts usable in practice.
- q: Which statement correctly categorizes the three named profile tools?
  options:
  - FSLogix only works with Citrix DaaS
  - FSLogix is Microsoft's tool, Citrix Profile Management is Citrix's tool, and Omnissa DEM (Dynamic
    Environment Manager) is Omnissa's tool — all serve the same category of problem on their respective
    platforms
  - Omnissa DEM is a display protocol, not a profile tool
  - Citrix Profile Management requires FSLogix to function
  answer: 1
  why: 'FSLogix (Microsoft, bundled with qualifying M365/Windows Enterprise/AVD licenses), Citrix Profile
    Management (part of Citrix Virtual Apps and Desktops), and Omnissa Dynamic Environment Manager (part
    of the Horizon ecosystem) are the three vendor-aligned tools that solve the same underlying problem:
    making user profiles and settings portable across disposable or shared session hosts.'
- q: What is the key limitation of legacy folder redirection compared to modern container-based profile
    solutions?
  options:
  - Folder redirection only redirects the Documents folder and nothing else
  - Container-based solutions cannot be used with Active Directory
  - Folder redirection redirects specific folders to network storage but leaves most of the registry-based
    profile (app settings, personalization) unmanaged, while container-based solutions mount a single
    virtual disk holding the full profile, redirecting the whole user experience more completely and often
    faster
  - There is no real difference between the two approaches
  answer: 2
  why: Folder redirection (a Group Policy-era technique) moves specific known folders to a network share,
    but application settings stored in the registry or in AppData outside the redirected folders are not
    covered, leading to inconsistent experiences. Container-based tools like FSLogix mount a VHD/VHDX
    holding the entire profile at logon, covering far more of the user experience with generally better
    performance than copying files over the network.
- q: A pooled AVD host pool is using FSLogix Profile Containers stored on Azure Files. Which statement
    about this design is accurate?
  options:
  - The profile container must be duplicated on every session host's local disk
  - FSLogix cannot be used with Azure Files, only with local disks
  - Profile containers eliminate the need for a golden image
  - The profile VHDX is mounted from network storage (such as Azure Files) at logon over the network,
    so storage performance and availability directly affect logon time and session reliability
  answer: 3
  why: FSLogix Profile Containers are VHD/VHDX files mounted at logon from a network storage location
    such as Azure Files (with Entra Kerberos) or Azure NetApp Files. Because the profile is mounted live
    over the network for the duration of the session, the performance, availability, and correct sizing
    of that storage tier directly determines logon speed and in-session reliability.
- q: In three to five sentences, explain the trade-off an EUC engineer makes when choosing pooled/non-persistent
    desktops over personal/persistent ones, and describe what has to be true about the profile layer for
    that choice to work well in production.
  answer: Choosing pooled/non-persistent desktops trades away per-user machine state — nothing a user
    changes on the OS itself survives logoff — in exchange for dramatically simpler patching, cheaper
    storage, and easier scaling, since every host in the pool is identical and can be rebuilt from a single
    golden image. For that trade to actually work for end users, the profile layer has to reliably and
    quickly reattach a consistent set of documents, application settings, and personalization at every
    logon regardless of which physical host in the pool they land on, which means the profile storage
    tier needs to be fast, highly available, and sized for concurrent I/O across the whole pool. If the
    profile layer is slow, unreliable, or misconfigured, users experience the downside of non-persistence
    (nothing feels like their own machine) without ever getting a working substitute.
  why: The core trade-off is machine-level statelessness in exchange for operational simplicity, and the
    profile layer is the load-bearing piece that has to compensate for that statelessness — its reliability
    and performance are non-negotiable prerequisites for a non-persistent design to succeed.
resources:
- label: What is FSLogix (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/fslogix/overview-what-is-fslogix
- label: FSLogix prerequisites (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/fslogix/overview-prerequisites
- label: Azure Virtual Desktop host pool overview (personal vs. pooled)
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/host-pool-overview
- label: Omnissa Dynamic Environment Manager (DEM)
  url: https://www.omnissa.com/products/dynamic-environment-manager/
---

## The Decision That Shapes Everything Else

One of the very first decisions in any VDI design is whether a desktop is **persistent** or **non-persistent**. It sounds like a small technical toggle, but it cascades into storage cost, patching strategy, image management workload, and — critically — whether you need serious profile tooling at all. Get this decision and its consequences right, and everything downstream gets simpler.

## Pooled (Non-Persistent) Desktops

In a **pooled** host pool, users don't own a specific VM. When they connect, the broker assigns them *any* available, healthy host from the pool. On logoff (or on a schedule), the host is typically reset back to its clean golden-image state — often by simply discarding the disk changes and re-provisioning from the image. This is the model that makes VDI economical at scale:

- **Patching is trivial**: you patch and validate one golden image, then roll it out; you never patch a thousand individual machines by hand.
- **Storage is cheap**: hosts share a common OS disk pattern rather than each carrying a large, unique, ever-growing disk.
- **Compliance is strong**: a compromised or misconfigured session evaporates on reset rather than persisting as a foothold.

The cost is that **nothing the user does to the machine itself survives** — no locally installed apps, no local file saves, no OS-level personalization. That's a feature for security and manageability, but it's unusable for end users unless something else preserves *their* experience across that churn. That something is the profile layer, covered below.

## Personal (Persistent/Dedicated) Desktops

In a **personal** host pool, each user is permanently assigned their own VM, and it behaves like a traditional PC: changes persist, locally installed software stays installed, and the user reconnects to the exact same machine every time. This suits power users, developers, and anyone running specialized software that resists centralized packaging — but it brings back the operational burden VDI is often adopted to escape: every VM needs to be individually patched, monitored, and eventually right-sized or decommissioned, and per-user storage cost is meaningfully higher because each disk grows independently over time.

Most real deployments run **both models side by side** — pooled for task workers and call-center-style roles, personal for specialists — which is exactly why host pool types and app group assignment (covered in Module 3) exist as a first-class design surface, not an afterthought.

## Why Non-Persistent Desktops Need Profile Tooling

Here's the sharp edge: if you deploy a pooled, non-persistent host pool with no profile solution at all, every single logon is a brand-new machine as far as the user's *experience* is concerned. Desktop wallpaper, pinned taskbar apps, Outlook signature, browser bookmarks, saved documents on the desktop — gone, every time, because the user could land on a completely different physical VM than last time, and that VM was just reset to golden-image defaults anyway.

A profile management tool solves this by separating **user-specific state** from **machine state**, and reattaching that user-specific state at logon regardless of which host the user lands on. This is not an optional nice-to-have for pooled desktops — it is the feature that makes pooled desktops usable at all.

## The Three Tools You'll Actually Deploy

Every major platform has settled on essentially the same architecture (a mountable profile container) with its own product name:

| Tool | Vendor/Platform | Category |
|---|---|---|
| **FSLogix** | Microsoft — bundled with qualifying Microsoft 365 E3/E5, Windows Enterprise E3/E5, and Azure Virtual Desktop entitlements | Profile & Office container management |
| **Citrix Profile Management** | Citrix (Cloud Software Group) — part of Citrix Virtual Apps and Desktops/DaaS | User profile management |
| **Omnissa Dynamic Environment Manager (DEM)** | Omnissa — part of the Horizon ecosystem | Profile and policy/context-aware environment management |

FSLogix is the tool you'll use most in this course because of the AZ-140/AVD focus, and it comes **pre-installed on Windows Enterprise multi-session images**. Microsoft acquired FSLogix in 2018 and folded its licensing into existing Microsoft 365 and Windows Enterprise entitlements, so in most AVD deployments there's no separate FSLogix license to buy — just the storage it runs on. Citrix Profile Management and Omnissa DEM follow the same conceptual model on their respective platforms, and DEM additionally layers in **context-aware policy** (settings that change based on device, location, or network) beyond pure profile portability.

## Folder Redirection vs. Container-Based Profiles

Before container-based tools matured, the standard technique was **folder redirection**: a Group Policy setting that redirects specific known folders (Documents, Desktop, Pictures) to a network file share, so their contents survive even though the local profile itself doesn't. It's simple and has no special agent requirement, but it has real limits — application settings and personalization stored in the registry or in AppData folders outside the redirected set are not covered, and heavy file I/O over a plain network share (rather than a locally-mounted virtual disk) can be slow.

**Container-based profiles** (FSLogix Profile Containers, Citrix Profile Management's container mode, DEM's equivalent) instead package the *entire* user profile — registry hive included — into a single virtual disk (a VHD/VHDX for FSLogix), which is mounted directly onto the session host at logon as if it were a local disk. This covers far more of the actual user experience (application settings, not just files) and generally performs better than copying files over a share, because the OS treats the mounted container as local storage rather than performing granular network file operations for every read and write.

## Where the Container Actually Lives

For FSLogix specifically, the profile container needs a storage backend reachable by every session host in the pool — common choices are **Azure Files** (typically with Entra Kerberos authentication for cloud-native environments) or **Azure NetApp Files** for higher-performance requirements. Whatever the backend, remember: the container is mounted live, over the network, for the entire session. If that storage tier is slow, undersized for concurrent connections, or unavailable, logon times spike and sessions can fail outright — this is one of the most common real-world VDI troubleshooting scenarios, and Module 6 dedicates a full lesson to triaging it. As a preview: a corrupted or "stuck" profile container that fails to release its lock from a previous session is one of the single most common FSLogix support tickets you will ever see in production.

## Bringing It Together

The pattern to internalize: **persistence is a machine-level property, and the profile layer is what compensates when you deliberately give that property up.** Pooled, non-persistent desktops buy you operational simplicity at the cost of local state — and a properly sized, properly configured profile container is the tool that makes users never notice the trade was made at all. Get the profile layer wrong, and users will feel every non-persistent reset as data loss, even when the underlying architecture is working exactly as designed.
