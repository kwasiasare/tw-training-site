---
course: vdi-engineer
title: 'FSLogix Deep Dive: Profile Containers, Cloud Cache, and Storage'
month: 5
monthTitle: User Environments & App Delivery
lesson: 1
summary: FSLogix is the profile layer that makes non-persistent AVD and Windows 365 desktops feel personal.
  This lesson goes deep on the two container types, the critical VHDLocations-vs-Cloud-Cache decision,
  how to wire Azure Files to Entra-joined hosts with Microsoft Entra Kerberos, sizing and exclusion tuning,
  and how to read FSLogix's status/reason/error codes when a profile won't attach.
objectives:
- Explain the difference between a Profile Container and an Office Container (ODFC) and when to use each
- Choose between VHDLocations and Cloud Cache for profile storage and explain why the two are mutually
  exclusive
- Configure Azure Files as FSLogix profile storage using Microsoft Entra Kerberos authentication for Entra-joined
  session hosts
- Apply sizing, exclusion, and performance best practices for profile containers at scale
- Diagnose common FSLogix failure modes, including locked VHDX files, using FSLogix status, reason, and
  error codes
- Decide between per-machine and per-user FSLogix agent installation for a given host pool design
quiz:
- q: What is the primary difference between a Profile Container and an Office Container (ODFC) in FSLogix?
  options:
  - ODFC is the only container type that supports Azure Files; Profile Container requires local disk
  - Profile Container is deprecated in favor of ODFC for all new deployments
  - ODFC stores registry hives while Profile Container stores only documents
  - Profile Container holds the entire user profile (NTUSER.DAT, AppData, etc.); ODFC optionally splits
    out just the Office/OneDrive cache data into a second VHD(X)
  answer: 3
  why: Profile Container is the primary, full-profile container (registry hive, AppData, desktop, etc.).
    ODFC is an optional, separate container that isolates Outlook/OneDrive cache data — useful when you
    want Office data on faster or differently-sized storage, or when combining with other profile solutions.
    Both can attach to the same or different storage locations.
- q: Which two settings are mutually exclusive in an FSLogix profile configuration?
  options:
  - VHDLocations and Cloud Cache — a configuration uses one or the other, not both
  - SizeInMBs and IsDynamic — you must pick a fixed or dynamic disk, never configure size
  - ODFC and Outlook — you cannot use FSLogix with Outlook at all
  - Profile Container and folder redirection — folder redirection is required with FSLogix
  answer: 0
  why: VHDLocations points FSLogix at one or more plain storage paths in priority order, while Cloud Cache
    is a separate replication engine that asynchronously mirrors the profile across up to four locations
    for high availability and DR. An FSLogix configuration uses one mechanism or the other, not both simultaneously.
- q: Your session hosts are Microsoft Entra joined only (no on-premises Active Directory, no Microsoft
    Entra Domain Services). Which authentication method lets them mount an FSLogix profile share on Azure
    Files without line-of-sight to a domain controller at logon time?
  options:
  - NTLM authentication with a local storage account admin
  - Microsoft Entra Kerberos authentication for Azure Files
  - Azure AD Domain Services joined to the same VNet
  - Anonymous SMB access with share-level permissions only
  answer: 1
  why: Microsoft Entra Kerberos lets Microsoft Entra ID issue the Kerberos tickets an Entra-joined (or
    hybrid-joined) session host needs for SMB access to an Azure Files share — no domain controller or
    Microsoft Entra Domain Services required for the sign-in path. You still need one system with AD line-of-sight
    once to assign the share-level RBAC and NTFS permissions, but session hosts themselves don't need
    it at runtime.
- q: A user's FSLogix log shows the profile failed to attach with a Windows system error 0x00000020 (ERROR_SHARING_VIOLATION)
    on the VHDX file. What is the most likely cause?
  options:
  - The storage account has run out of capacity
  - The user's Microsoft Entra token has expired
  - The user's VHDX is already open — an active or orphaned session elsewhere still holds a lock on the
    file
  - The VHDX file format is corrupted beyond repair
  answer: 2
  why: 'ERROR_SHARING_VIOLATION (0x00000020 / decimal 32) is the classic Windows error for ''file in use
    by another process'' — in FSLogix terms, another session (active, disconnected-but-not-cleaned-up,
    or on a different host) still has the VHDX mounted. First checks: look for the user''s other active
    sessions across the host pool, then check for stale locks.'
- q: An April 2026 Windows Server update changes a Kerberos default that can break FSLogix access to SMB
    file shares if they haven't been upgraded first. What is that change?
  options:
  - SMB 1.0 is removed entirely from Windows Server
  - Kerberos is replaced by certificate-only authentication
  - The default session ticket lifetime is reduced to 5 minutes
  - The default Kerberos encryption type changes from RC4 to AES-SHA1
  answer: 3
  why: Microsoft's FSLogix documentation flags that the April 2026 Windows Server update changes the default
    Kerberos encryption type from RC4 to AES-SHA1. File shares hosting FSLogix containers that haven't
    already been upgraded to AES-SHA1 can see access failures once that update lands, so it needs to be
    handled proactively, not reactively.
- q: In two to four sentences, explain when you would choose Cloud Cache over a single VHDLocations path
    on Azure Files with Zone-Redundant Storage (ZRS), and name one real trade-off of using Cloud Cache.
  answer: Cloud Cache is the right choice when you need multi-region or multi-provider redundancy and
    automatic session-host failover — for example, replicating a profile across an Azure Files share in
    one region and a file server share in another, or supporting active-active disaster recovery, since
    Cloud Cache can replicate to up to four locations and fail over automatically if the primary is unreachable.
    A single VHDLocations path with Azure Files ZRS is simpler and sufficient when you only need protection
    against a single datacenter/zone failure within one region. The trade-off with Cloud Cache is added
    complexity and local cache disk requirements on each session host (a local cache directory is needed
    for the asynchronous replication), plus more moving parts to monitor and troubleshoot than a single
    VHDLocations target.
  why: 'Cloud Cache trades simplicity for resilience: it''s the documented approach for FSLogix HA/DR
    beyond what a single storage target with platform-level redundancy (like Azure Files ZRS) can offer,
    but it requires local cache storage per host and adds operational complexity that a straightforward
    VHDLocations deployment doesn''t have.'
resources:
- label: FSLogix overview (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/fslogix/overview-what-is-fslogix
- label: Cloud Cache overview (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/fslogix/concepts-fslogix-cloud-cache
- label: High availability / container resiliency with Cloud Cache
  url: https://learn.microsoft.com/en-us/fslogix/concepts-container-high-availability
- label: FSLogix codes and what they mean
  url: https://learn.microsoft.com/en-us/fslogix/troubleshooting-error-codes
- label: Microsoft Entra Kerberos authentication for Azure Files
  url: https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable
---

## Why FSLogix Matters

Any non-persistent host pool — the pooled, multi-session model that makes AVD and Windows 365 Frontline cost-effective — has a hard problem: the operating system disk is thrown away or reset between sessions, but users expect their desktop, their pinned apps, their Outlook signature, and their browser bookmarks to follow them every time. FSLogix solves this by storing the user's profile in a virtual disk file that mounts at logon and detaches at logoff, so pooled hosts feel personal without ever persisting user data on the host itself. It's the single most consequential storage decision you'll make in a VDI deployment, and it's directly examined under AZ-140 Domain 3.

## Profile Container vs. Office Container (ODFC)

FSLogix ships two container types. The **Profile Container** is the primary one: it holds the entire user profile — the NTUSER.DAT registry hive, AppData, Desktop, Documents, Favorites, everything Windows considers 'the profile.' Most deployments need only this.

The **Office Container (ODFC — Office 365 Container)** is optional and narrower: it isolates just the Outlook OST cache and OneDrive data into a second VHD(X). You'd reach for ODFC when you want Office data to live on different, faster storage than the rest of the profile, when you're layering FSLogix with another profile tool that already manages the base profile, or when Outlook cache growth is large enough that you want to manage its lifecycle independently. In most modern AVD builds, a single Profile Container is sufficient — reach for ODFC only when you have a specific reason.

## VHDLocations vs. Cloud Cache — Pick One

This is the decision every AVD/Windows 365 architect has to make explicitly, and it's binary: **an FSLogix configuration uses either `VHDLocations` or Cloud Cache, never both.**

- **`VHDLocations`** is a simple, ordered list of one or more UNC paths. FSLogix tries each path in order until it finds (or creates) the user's container. Pair this with a storage backend that already provides redundancy — Azure Files configured for Zone-Redundant Storage (ZRS) is the standard 2026 pattern — and you get resilience against a zonal failure without any FSLogix-side complexity.
- **Cloud Cache** is a different engine entirely. It asynchronously replicates the profile across up to four storage locations simultaneously — for example, an Azure Files share in one region plus a file server share in another — and automatically fails a session host over to a healthy location if the primary becomes unreachable. Cloud Cache is the documented path for multi-region HA/DR scenarios that a single storage target can't cover on its own. The trade-off: Cloud Cache needs local cache disk on every session host for the asynchronous write-back layer, and it adds real operational surface area — more logs, more failure modes, more to monitor.

Rule of thumb for the exam and for production: if platform-level redundancy (ZRS, geo-redundant file server clustering) covers your resilience requirement within one region, use `VHDLocations`. If you need cross-region failover or multi-provider redundancy, use Cloud Cache.

## Storage Backends: Azure Files with Entra Kerberos, or Azure NetApp Files

Azure Files is the default recommendation for FSLogix storage — good cost-to-management ratio and it's compatible with both Active Directory Domain Services and Microsoft Entra ID identity models. For session hosts that are **Microsoft Entra joined only** (no domain controller, no Microsoft Entra Domain Services), enable **Microsoft Entra Kerberos authentication** on the storage account: go to the storage account, **File shares → Identity-based access**, and select **Microsoft Entra Kerberos**. This lets Microsoft Entra ID issue the Kerberos tickets your Entra-joined hosts need for SMB access — no domain controller line-of-sight required at sign-in. You still need one machine with AD line-of-sight once to grant the RBAC role (Storage File Data SMB Share Elevated Contributor or similar, scoped per user/group) and configure NTFS permissions on the share.

For customers with heavier IOPS/throughput needs or who are already invested in NetApp, **Azure NetApp Files** is the alternative — but note it currently requires session hosts to be joined to Active Directory Domain Services (or Microsoft Entra Domain Services), not Entra-joined-only.

One 2026 operational note worth flagging now and revisiting in Module 6: an April 2026 Windows Server update changes the **default Kerberos encryption type from RC4 to AES-SHA1**. File shares hosting FSLogix containers that haven't already been upgraded to AES-SHA1 can see logon-time access failures once that update rolls out — this is a proactive fix, not a wait-and-see one.

## Sizing, Exclusions, and Performance

Use **dynamically expanding** VHD(X) files (the FSLogix default) rather than fixed-size — they only consume as much storage as the profile actually uses. Set a generous `SizeInMBs` ceiling (30,000 MB / ~30 GB is a common starting point) since dynamic disks won't pre-allocate it. Exclude noisy, regenerable folders from the profile with the standard FSLogix exclusion list — browser caches, `%LocalAppData%\Microsoft\Teams`, `AppData\Local\Temp` — to keep container growth under control. Keep your FSLogix storage share in the **same Azure region** as your session hosts to minimize latency, and separate it from any App Attach file share (Module 5, Lesson 2) since the two workloads have different I/O patterns.

## Reading Failure Modes: Status, Reason, and Error Codes

FSLogix records three values per user session in the registry: a **Status** code (Normal or Error), a **Reason** code that explains a *Normal* status (for example, `REASON_LOCAL_PROFILE_EXISTS` or `REASON_WINDOWS_TEMP_PROFILE`), and a Windows **Error** code that explains why an operation failed — these are standard Windows System Error Codes, not FSLogix-invented numbers. The most common one you'll see in the field is `0x00000020` (`ERROR_SHARING_VIOLATION`, decimal 32) — the file is already open elsewhere, almost always because the user has another active or orphaned session holding the VHDX lock. Status code `12` (`ERROR_ATTACH_VHD`, "Can't attach to virtual disk") is the general attach-failure bucket you'll see wrapping that underlying error. Your first move on any attach failure is always the same: check the profile log at `C:\ProgramData\FSLogix\Logs\Profile\Profile_<user>.log` for the underlying Windows error, then check for other sessions/locks before touching permissions.

## Per-Machine vs. Per-User Install

FSLogix is installed per-machine (once per session host image, applied to all users) in the overwhelming majority of AVD and Windows 365 deployments — it needs to run before any user profile loads, which a per-user install can't guarantee. Bake the agent and its registry configuration into your golden image (Module 3) so every new session host is FSLogix-ready from first boot.
