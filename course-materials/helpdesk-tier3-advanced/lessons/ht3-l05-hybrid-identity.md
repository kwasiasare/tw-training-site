---
course: helpdesk-tier3-advanced
title: 'Hybrid identity: Entra Connect and on-prem Active Directory'
month: 3
monthTitle: Advanced Endpoint Security & Identity
lesson: 5
summary: Bridge on-premises Active Directory with Microsoft Entra ID using Entra Connect Sync, choosing
  the right sign-in method and understanding how a device earns a cloud identity through hybrid join.
  You will learn to operate, monitor and troubleshoot the sync engine like an engineer, not a button-pusher.
objectives:
- Explain what hybrid identity is and why organisations run on-prem AD alongside Entra ID
- 'Describe the Entra Connect Sync architecture: connector spaces, metaverse and the sync engine'
- Compare Password Hash Sync, Pass-through Authentication and Federation and choose the right one
- Operate the sync scheduler and trigger delta and initial sync cycles from PowerShell
- Explain source anchor / immutableID, soft and hard matching, and UPN considerations
- Diagnose Entra hybrid join state with dsregcmd and monitor health with Connect Health
video: ht3-l05-hybrid-identity.mp4
quiz:
- q: In the Entra Connect Sync engine, what is the role of the metaverse?
  options:
  - It stores the encrypted password hashes before they leave the server
  - It is the central aggregated view that joins objects from each connector space before export
  - It is the staging server's read-only replica of Entra ID
  - It is the cloud-side directory that Conditional Access reads from
  answer: 1
  why: The metaverse is the consolidated in-engine view. Objects flow from each connected directory into
    its connector space, then inbound sync rules project and join them into the metaverse, and outbound
    rules export the result to the target connector space.
- q: An organisation needs sign-in to keep working at the cloud even if all on-prem infrastructure is
    offline, with the lowest operational overhead. Which sign-in method best fits?
  options:
  - Federation with AD FS
  - Pass-through Authentication
  - Password Hash Sync
  - Certificate-based authentication only
  answer: 2
  why: Password Hash Sync synchronises a hash-of-the-hash to Entra ID, so authentication happens entirely
    in the cloud and survives a complete on-prem outage with minimal infrastructure. PTA and AD FS both
    depend on on-prem components being reachable to validate sign-ins.
- q: Which attribute does Entra Connect use by default as the source anchor (immutableID) for objects
    synced from on-prem AD?
  options:
  - sAMAccountName
  - userPrincipalName
  - ms-DS-ConsistencyGuid
  - objectGUID converted, with ms-DS-ConsistencyGuid as the modern default
  answer: 3
  why: Newer Entra Connect builds use ms-DS-ConsistencyGuid as the source anchor by default (populating
    it from objectGUID if empty). This makes the anchor writable and portable, which is what allows safe
    forest migrations and rebuilds without orphaning cloud objects.
- q: A user reports a change made in on-prem AD has not appeared in Entra ID after a few minutes. Which
    command lets you trigger an immediate incremental synchronisation?
  options:
  - Start-ADSyncSyncCycle -PolicyType Delta
  - Start-ADSyncSyncCycle -PolicyType Initial
  - Get-ADSyncScheduler -RunNow
  - Invoke-ADSyncExport -Full
  answer: 0
  why: Start-ADSyncSyncCycle -PolicyType Delta runs an incremental cycle that processes only changes since
    the last run. Initial (full) reprocesses everything and reimports rules, which is heavier and reserved
    for rule or configuration changes.
- q: When an on-prem account is matched to an existing cloud account, explain the difference between soft
    match and hard match.
  answer: Soft match links an on-prem object to a cloud object automatically when their primary SMTP /
    proxyAddresses or userPrincipalName align, with no manual action. Hard match is when you explicitly
    set the cloud object's immutableID to equal the Base64 of the on-prem source anchor so the next sync
    binds them deliberately. Soft match is convenient for clean mail attributes; hard match is the reliable
    fix when soft match fails or anchors must be repaired.
  why: Both stop the engine creating a duplicate cloud object. Soft match relies on matching mail/UPN
    attributes; hard match forces the link by aligning the immutableID, and is the controlled tool when
    soft matching cannot find or trust the attributes.
- q: 'On a Windows 11 device that should be Entra hybrid joined, dsregcmd /status shows AzureAdJoined
    : NO and DomainJoined : YES. In one or two sentences, what does this tell you and where would you
    look first?'
  answer: The device is domain-joined to on-prem AD but has not yet completed its cloud registration,
    so it is not hybrid joined. Check that the SCP (service connection point) points at the right tenant,
    that the device can reach Entra endpoints, that the computer object is syncing via Entra Connect,
    and review the Diagnostic Data / dsregcmd /status output and the User State section for join errors.
  why: 'Hybrid join requires both DomainJoined : YES and AzureAdJoined : YES. AzureAdJoined : NO means
    the automatic device registration has not succeeded — typically an SCP, connectivity, or sync (the
    computer object reaching Entra) problem.'
resources:
- label: Microsoft Learn — What is Microsoft Entra Connect Sync?
  url: https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-whatis
- label: Microsoft Learn — Choose the right authentication method for hybrid identity
  url: https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/choose-ad-authn
- label: Microsoft Learn — Plan your Microsoft Entra hybrid join implementation
  url: https://learn.microsoft.com/en-us/entra/identity/devices/how-to-hybrid-join
- label: 'Microsoft Learn — Microsoft Entra Connect Sync: Scheduler'
  url: https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-feature-scheduler
---

## Why hybrid identity exists

Most enterprises did not start in the cloud. They have years of investment in on-premises **Active Directory** (AD) — group policy, file shares, line-of-business apps that authenticate against domain controllers. They also need Microsoft 365, Intune and Conditional Access, which live in **Microsoft Entra ID**. **Hybrid identity** bridges the two so a user has one identity, one password and one sign-on experience whether they hit an on-prem file share or a cloud app.

The bridge is **Microsoft Entra Connect** (the sync client) running **Entra Connect Sync**. It reads objects from AD, transforms them, and provisions matching objects into Entra ID, keeping them in step.

## The sync engine architecture

The engine is not a simple copy. Each connected directory has a **connector space** — a staging area holding a snapshot of that directory's objects. Inbound sync rules project objects into a central **metaverse**, the consolidated view that joins the on-prem user and the cloud user into one record. Outbound rules then export from the metaverse into the Entra ID connector space.

```text
On-prem AD ──import──> AD connector space
                              │ inbound sync rules
                              ▼
                         METAVERSE  (joined view)
                              │ outbound sync rules
                              ▼
               Entra ID connector space ──export──> Entra ID
```

Understanding this pipeline is what lets you reason about *why* an attribute did or did not flow.

## Choosing a sign-in method

Three options decide where the password is actually validated:

- **Password Hash Sync (PHS)** — a hash of the AD password hash is synced to Entra ID. Authentication happens in the cloud, survives a full on-prem outage, and is the lowest-overhead choice. Recommended default.
- **Pass-through Authentication (PTA)** — the password is validated against on-prem AD in real time by a lightweight agent. No password material in the cloud, but it depends on the agent and DCs being reachable.
- **Federation (AD FS)** — sign-in is redirected to an on-prem federation farm. Most control and most infrastructure; reserve it for specific requirements like third-party MFA or smart-card-only auth.

**Seamless single sign-on (SSO)** can sit on top of PHS or PTA to give Kerberos-style silent sign-in on domain-joined devices.

## The sync cycle and scheduler

By default the scheduler runs a **delta (incremental)** sync every 30 minutes, processing only changes. A full **initial** sync reimports everything and is triggered when you change rules. Operate it from PowerShell on the Connect server:

```powershell
# See the current schedule and whether sync is enabled
Get-ADSyncScheduler

# Force an immediate incremental (delta) run
Start-ADSyncSyncCycle -PolicyType Delta

# Force a full reimport + reprocess (heavier; after rule changes)
Start-ADSyncSyncCycle -PolicyType Initial
```

## Anchors, matching and devices

Every object needs a stable **source anchor** (the **immutableID**). Modern Connect uses **ms-DS-ConsistencyGuid**, a writable attribute that makes forest migrations safe. When an on-prem object meets an existing cloud object, the engine performs a **soft match** on mail/UPN attributes; if that fails you perform a **hard match** by setting the cloud object's immutableID to the Base64 of the source anchor. Watch the **UPN**: the on-prem UPN suffix should be a verified domain in the tenant, or users end up with an `.onmicrosoft.com` UPN.

A device gets its cloud identity through **Entra hybrid join**: the domain-joined computer is registered with Entra ID (its object syncs up via Connect), so it appears as a hybrid-joined device and can satisfy Conditional Access. Verify it on the endpoint:

```text
C:\> dsregcmd /status

+----------------------------------------------------------------------+
| Device State                                                         |
+----------------------------------------------------------------------+
             AzureAdJoined : YES
          EnterpriseJoined : NO
              DomainJoined : YES
               Virtual Desktop : NOT SET
                  DeviceId : 2b8c...e91
```

Both `AzureAdJoined : YES` and `DomainJoined : YES` confirm a successful hybrid join. Use **Entra Connect Health** to monitor sync status, errors and latency, and run a **staging server** — a second Connect instance importing but not exporting — for high availability and safe upgrades.

## Your task

On a test Connect server, run `Get-ADSyncScheduler` and record the current sync interval and whether sync is enabled. Change a user's attribute (e.g. department) in on-prem AD, force a delta cycle with `Start-ADSyncSyncCycle -PolicyType Delta`, and confirm it lands in Entra ID. Then on a hybrid-joined Windows device run `dsregcmd /status`, capture the Device State and SSO State sections, and write a short note explaining which sign-in method your tenant uses and why it is the correct choice for that environment.
