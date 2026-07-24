---
course: vdi-engineer
title: 'Troubleshooting VDI: A Connection-Chain Triage Method'
month: 6
monthTitle: Monitoring, Operations & Troubleshooting
lesson: 3
summary: '"AVD is broken" is not a diagnosis, it''s a starting point. This lesson gives you a repeatable
  triage method that walks the connection chain in order — client, feed, authentication, gateway, session
  host, profile, in-session experience — so you can localize a failure to a specific hop instead of guessing.
  For each hop you''ll get the exact tool or Log Analytics table to check, a walkthrough of FSLogix-specific
  triage, a comparison of AVD''s own tooling against Citrix Director and the Omnissa Horizon Help Desk
  Tool, and a clear rule for when to self-resolve versus escalate to Microsoft or a platform vendor.'
objectives:
- Walk the AVD connection chain end to end and name the failure domain at each hop
- Match each failure bucket to the specific tool, log, or Log Analytics table used to diagnose it
- Triage the most common FSLogix profile-attach failures using the official logging locations
- Compare Citrix Director and the Omnissa Horizon Help Desk Tool to AVD's own Insights-based tooling
- Decide when to self-resolve, when to open a Microsoft support case, and when to escalate to platform
  vendor support
quiz:
- q: A user reports they can't even see their desktop or app icons in the Remote Desktop client or web
    feed. Which hop in the connection chain does this point to?
  options:
  - Session host performance
  - FSLogix profile attach
  - Feed/subscription
  - In-session graphics quality
  answer: 2
  why: If the icons never appear, the failure is upstream of authentication into a session — it's in workspace/app-group
    subscription (feed). Check WVDFeeds and WVDCheckpoints before assuming the session host or profile
    layer is involved.
- q: Which table specifically records whether a session host successfully registered with the Azure Virtual
    Desktop service?
  options:
  - WVDConnections
  - WVDCheckpoints
  - WVDManagement
  - WVDHostRegistrations
  answer: 3
  why: WVDHostRegistrations logs host-registration activity, including SessionHostName and CorrelationId,
    distinct from WVDConnections (user connection activity) and WVDManagement (admin/API activity).
- q: A user gets past sign-in but is stuck on a black screen right after entering credentials, correlating
    with FSLogix errors in the Windows Event Log. Which failure domain does this map to?
  options:
  - Profile attach
  - Gateway routing
  - Authentication (identity provider)
  - Network transport codec negotiation
  answer: 0
  why: Credentials already succeeded (auth passed), so the failure is downstream of that — a profile container
    failing to attach or mount is a classic black-screen-after-login cause, and FSLogix event log correlation
    confirms it.
- q: What is Citrix Director's rough functional equivalent when troubleshooting an AVD environment?
  options:
  - Azure Compute Gallery
  - Azure Virtual Desktop Insights combined with the WVD Log Analytics tables
  - Microsoft Intune compliance policies
  - Microsoft Entra Conditional Access
  answer: 1
  why: Citrix Director is a real-time and historical monitoring/helpdesk console for a Citrix site. In
    the Microsoft stack, that same 'see live session state, diagnose, and support end users' role is filled
    by AVD Insights plus direct KQL queries against the WVD tables, not by a single named product.
- q: In WVDErrors, a specific reproducible failure shows ServiceError == true. What should you do?
  options:
  - Ignore it — the field is cosmetic and doesn't affect anything
  - Immediately rebuild the golden image, regardless of the error's source
  - Escalate to Microsoft support, including the CorrelationId for that event
  - Disable diagnostic settings so the error stops appearing
  answer: 2
  why: ServiceError == true means the error originates on Microsoft's service side rather than being admin-actionable.
    The documented path is to escalate to Microsoft support and supply the CorrelationId so they can trace
    the exact event server-side.
- q: Describe, in order, the client-to-in-session triage chain a helpdesk engineer should mentally walk
    through when a user says "AVD is broken," and name one tool or data source you'd check at three different
    hops.
  answer: 'The chain runs roughly: client app/feed (does the user see the workspace and app tiles? check
    the Remote Desktop client logs and the WVDFeeds/WVDCheckpoints tables) then authentication (did sign-in
    and Conditional Access succeed? check Microsoft Entra ID sign-in logs) then gateway/connection broker
    (did the service accept and route the connection? check WVDConnections and WVDErrors) then session
    host (is the VM healthy and registered? check WVDHostRegistrations and WVDAgentHealthStatus) then
    profile (did FSLogix attach correctly? check the FSLogix logs under C:\\ProgramData\\FSLogix\\Logs)
    then in-session experience (is performance, graphics, or redirection the problem? check WVDConnectionNetworkData
    round-trip time and session host performance counters). Naming any three consecutive or non-consecutive
    hops together with their matching tool is an acceptable answer.'
  why: 'This restates the ordered triage model taught in the lesson: localize the failure to a specific
    hop before you start changing configuration, and use the tool that actually reports on that hop rather
    than the one that''s most familiar.'
resources:
- label: Azure Virtual Desktop troubleshooting overview
  url: https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-set-up-overview
- label: FSLogix troubleshooting with logging and diagnostics
  url: https://learn.microsoft.com/en-us/fslogix/troubleshooting-events-logs-diagnostics
- label: FSLogix known issues
  url: https://learn.microsoft.com/en-us/fslogix/troubleshooting-known-issues
- label: Citrix Director overview
  url: https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/director.html
- label: Using the Omnissa Horizon Help Desk Tool
  url: https://docs.omnissa.com/bundle/Horizon-AdministrationV2406/page/UsingHorizonHelpDeskToolinHorizonConsole.html
---

## "It's Broken" Is Not a Diagnosis

Every VDI helpdesk engineer has taken the ticket that just says "AVD is broken" or "Citrix is down." That sentence tells you nothing actionable, because a virtual desktop connection is actually a chain of six or seven distinct systems, any one of which can fail independently while the rest work perfectly. The skill this lesson teaches isn't a list of fixes — it's a **method**: walk the chain in order, from the client outward to the in-session experience, and stop at the first hop that's actually broken. Everything downstream of a working hop is a waste of your time to investigate.

## The Connection Chain, Hop by Hop

**1. Client / feed.** Does the user even see their workspace and app tiles in the Remote Desktop client or the web client? If not, the failure is upstream of authentication into a session entirely — it's a **subscription/feed** problem. Check the Remote Desktop client's own logs (Windows client: `%LocalAppData%\rdclientwpf`), and on the service side the `WVDFeeds` and `WVDCheckpoints` tables, which record whether the user's device successfully subscribed to the workspace.

**2. Authentication.** Icons appear but sign-in fails, loops, or gets blocked. This is now an identity problem, not an AVD problem — check **Microsoft Entra ID sign-in logs** for Conditional Access denials, MFA failures, or risk-based blocks (this ties directly back to Module 4's identity and Conditional Access lessons).

**3. Gateway / broker.** Sign-in succeeds but the connection itself never establishes, times out, or errors immediately. Query `WVDConnections` for the `State` progression (`Started` → `Connected` → `Completed`) and `WVDErrors` for anything with a matching `CorrelationId`. A connection that never reaches `Connected` usually means a broker or network path problem, not a session host problem.

**4. Session host.** The connection reaches a host but the host itself is unhealthy — unregistered, agent not responding, or out of capacity. Check `WVDHostRegistrations` for registration failures and `WVDAgentHealthStatus` for `Status != "Healthy"` on the target host, plus basic VM health (is it even running, does it have free capacity, is it stuck mid-update from Lesson 2).

**5. Profile (FSLogix).** The user reaches a session host and authenticates into Windows, but hits a **black screen**, an extremely slow logon, or lands in a **temporary/local profile** instead of their real one. This is almost always a profile container attach failure — see the dedicated section below.

**6. In-session experience.** Everything above worked, but the session itself is laggy, pixelated, or drops audio/video. This is a **network and display protocol** problem — check `WVDConnectionNetworkData` for `EstRoundTripTimeInMs` and `EstAvailableBandwidthKBps`, session host performance counters (CPU, memory, disk queue length), and revisit the display protocol fundamentals from Module 1 (RDP Shortpath, codec choice, transport type in `WVDConnections.TransportType`).

The discipline is simple: **start at hop one and don't skip ahead.** A user who can't see their app tiles doesn't need you investigating session host CPU. A user who reaches a black screen after login almost certainly isn't a network problem, no matter how much the ticket description talks about "slowness."

## FSLogix Triage in Detail

Because profile-attach failures are one of the highest-volume ticket categories in any VDI environment, they deserve their own checklist:

- **Confirm FSLogix is actually enabled** — after install, none of its features (Profile Containers, ODFC) are active until you configure them. A fresh, unconfigured install looks identical to a broken one from the user's perspective.
- **Check storage reachability and capacity first.** FSLogix depends entirely on a remote storage provider (Azure Files or Azure NetApp Files). If the storage account is unreachable, throttled, or full, users fall back to a temporary or local profile — which looks like "my settings are gone" to the end user but is really a storage problem.
- **Check network/DNS from the session host.** A session host that can't resolve or reach the UNC path hosting the VHD(X) containers will fail to attach the container, even if storage itself is healthy.
- **Read the logs directly.** The primary log is `Profile_<timestamp>.log` under `C:\ProgramData\FSLogix\Logs\Profile` on the session host. For a structured collection, run the **FSLogix Support Tool** directly on the affected host and attach its output to any Microsoft support case.
- **Watch for the Kerberos encryption change.** An April 2026 Windows Server update shifts the default Kerberos encryption type from RC4 to AES-SHA1; file shares hosting FSLogix containers that haven't been upgraded to support AES-SHA1 can start failing attach operations after that update lands. If profile failures spike right after a patch cycle, this is a fast thing to rule in or out.

## AVD's Tooling vs. Citrix Director vs. the Omnissa Horizon Help Desk Tool

If you've supported Citrix or Horizon before, you'll instinctively look for a single console that shows live session state and lets you act on it. AVD doesn't ship one unified product with that name — the equivalent capability is **Azure Virtual Desktop Insights plus direct KQL queries** against the WVD tables from Lesson 1, which together give you the same live-plus-historical visibility.

- **Citrix Director** is a web-based console for Citrix DaaS/Virtual Apps and Desktops sites: a real-time dashboard of session and logon status, historical data from the monitoring database, and the ability to shadow a user's session directly through Windows Remote Assistance from within the tool.
- **Omnissa Horizon Help Desk Tool** (inside the Horizon Console) gives Horizon admins a comparable per-session view — session details, session processes, and guided troubleshooting actions for a specific user's desktop or app session.

The practical takeaway for a multi-platform EUC engineer: the *capability* (live session visibility, historical trend, and quick per-user drill-down) is universal across platforms, but where Citrix and Horizon bundle it into one purpose-built helpdesk console, on AVD you assemble the same picture from Insights workbooks and the KQL skills from Lesson 1.

## When to Self-Resolve vs. Escalate

Use this as a decision rule, not a guess: if `WVDErrors.ServiceError == false`, or the failure is clearly config/identity/storage-side (a Conditional Access policy, a full storage account, a mis-scoped RBAC role), it's yours to fix. If `ServiceError == true`, or you've isolated the failure to the AVD *service* itself (broker, gateway, feed) with no local misconfiguration to explain it, open a Microsoft support case and hand over the `CorrelationId` — that single field lets Microsoft trace the exact server-side event instead of reproducing your problem from scratch. For the vendor-neutral platforms, Citrix and Omnissa each have their own support paths gated by your subscription tier; know which path you're entitled to *before* an incident, not during one.

## What You'd Actually Do

When a ticket says "AVD is broken": ask what the user actually sees (no icons? stuck at login? black screen? slow?), map that answer to a hop in the chain above, pull the matching table or log for that hop only, and only widen the investigation if that hop turns out healthy. Keep the FSLogix checklist and the CorrelationId escalation habit as defaults — they resolve the majority of real-world tickets faster than jumping straight to "let's rebuild the image."
