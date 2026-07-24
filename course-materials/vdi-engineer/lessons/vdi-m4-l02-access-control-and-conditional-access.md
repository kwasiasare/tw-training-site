---
course: vdi-engineer
title: Access Control and Conditional Access for AVD
month: 4
monthTitle: Identity & Security for Virtual Desktops
lesson: 2
summary: 'RBAC decides who can manage the AVD control plane; Conditional Access decides who even gets
  in. This lesson separates the two and shows how they interlock: the built-in Desktop Virtualization
  roles from Contributor down to User Session Operator, the data-plane Desktop Virtualization User role
  that actually grants app group access, and the Conditional Access cloud apps — Azure Virtual Desktop
  and Windows Cloud Login — that must both be targeted once single sign-on is enabled. You''ll also cover
  MFA licensing, sign-in frequency behavior per app, the one app you must never add to an MFA policy,
  and the extra step Microsoft Entra joined session hosts need.'
objectives:
- Map each built-in Desktop Virtualization RBAC role to the operational tier it serves, from full control-plane
  management to helpdesk session operations
- Distinguish control-plane RBAC roles from the data-plane Desktop Virtualization User role that grants
  app group access
- Configure a Conditional Access policy that correctly targets both the Azure Virtual Desktop and Windows
  Cloud Login cloud apps
- Explain why the Azure Virtual Desktop Azure Resource Manager Provider app must be excluded from MFA-enforcing
  Conditional Access policies
- Configure sign-in frequency per app and apply the extra Conditional Access step required for Microsoft
  Entra joined session hosts
quiz:
- q: Which built-in role lets a helpdesk operator send messages, disconnect, and log off user sessions
    without any host pool or session host management rights?
  options:
  - Desktop Virtualization User Session Operator
  - Desktop Virtualization Contributor
  - Desktop Virtualization Session Host Operator
  - Desktop Virtualization Host Pool Contributor
  answer: 0
  why: User Session Operator allows sending messages, disconnecting sessions, and logging users off, but
    doesn't allow host pool or session host management such as removing hosts or changing drain mode.
- q: A user is assigned Desktop Virtualization Contributor at the subscription scope but still can't assign
    users to an application group. What's missing?
  options:
  - They need Desktop Virtualization Reader in addition
  - They also need the User Access Administrator role
  - They need to be a Global Administrator
  - Nothing — Contributor should already allow this
  answer: 1
  why: Desktop Virtualization Contributor manages AVD resources but explicitly does not grant user or
    group assignment; that requires the User Access Administrator role (or equivalent) in addition.
- q: Which Conditional Access cloud app enforces reauthentication for the session host sign-in specifically,
    when single sign-on is enabled?
  options:
  - Azure Virtual Desktop
  - Microsoft Remote Desktop
  - Windows Cloud Login
  - Azure Virtual Desktop Azure Resource Manager Provider
  answer: 2
  why: With SSO enabled, the Windows Cloud Login app governs the session host sign-in event and its own
    sign-in frequency; the Azure Virtual Desktop app governs subscription, feed refresh, and the gateway
    connection.
- q: Which app should you deliberately exclude from an MFA-enforcing Conditional Access policy for AVD?
  options:
  - Windows Cloud Login
  - Azure Virtual Desktop
  - Microsoft Remote Desktop
  - Azure Virtual Desktop Azure Resource Manager Provider
  answer: 3
  why: The Azure Virtual Desktop Azure Resource Manager Provider app (app ID 50e95039-b200-4007-bc97-8d5790743a63)
    is used only to retrieve the user's resource feed and shouldn't have multifactor authentication applied,
    or feed discovery breaks.
- q: A user has been granted the Desktop Virtualization User role, scoped to a single application group,
    with no other RBAC assignment. What can they do?
  options:
  - Use the applications or desktop published through that application group as a non-administrative user
  - Manage the host pool that backs the application group
  - View all AVD resources in the subscription
  - Assign other users to the application group
  answer: 0
  why: Desktop Virtualization User is a data-plane role granting only the useApplications action — it
    lets the assigned user consume the published resource, nothing administrative.
- q: In three to four sentences, explain the difference between assigning a user the Desktop Virtualization
    User role on an application group and adding that user to the group targeted by a Conditional Access
    policy on the Azure Virtual Desktop app. What does each control decide?
  answer: The Desktop Virtualization User role is an Azure RBAC data-plane assignment that decides authorization
    — whether a signed-in, already-authenticated user is allowed to use a specific application group's
    published desktop or apps. Conditional Access targeting the Azure Virtual Desktop app decides authentication
    — the conditions such as MFA, device compliance, location, and sign-in frequency a user must satisfy
    before Microsoft Entra ID issues them a token to reach the AVD service at all. A user can pass Conditional
    Access and still be denied by RBAC if they're not assigned to the app group, and conversely can be
    correctly RBAC-assigned but blocked entirely if they fail the Conditional Access policy.
  why: RBAC (Desktop Virtualization User) governs authorization to specific AVD resources; Conditional
    Access governs the authentication conditions required to reach the service and session host at all.
    They are complementary, independent layers that both must pass.
resources:
- label: Built-in Azure RBAC roles for Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/rbac
- label: Enforce Microsoft Entra multifactor authentication for Azure Virtual Desktop using Conditional
    Access
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa
- label: Azure Virtual Desktop identities and authentication
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/authentication
- label: Understand scope for Azure RBAC
  url: https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview
video: vdi-m4-l02-access-control-and-conditional-access.mp4
---

## Two Different Questions, Two Different Systems

"Can this admin manage the host pool?" and "can this user even reach AVD right now?" are answered by two completely separate systems. Azure role-based access control (RBAC) answers the first: it's authorization for the control plane and, in one special case, the data plane. Microsoft Entra Conditional Access answers the second: it's authentication policy, evaluated on every sign-in, regardless of what RBAC role someone holds. Confusing the two is the single most common AVD access-control mistake — teams lock down RBAC tightly and leave Conditional Access wide open, or vice versa, and wonder why access still isn't behaving as expected.

## The Desktop Virtualization Role Family

AVD doesn't have its own Owner role — you use the standard Azure Owner role for that — but it ships a deliberately granular set of built-in roles so you can separate host pool management from application group management from session operations:

| Role | Scope of control | Typical assignee |
|---|---|---|
| **Desktop Virtualization Contributor** | Manage all AVD resources except user/group assignment | Platform team |
| **Desktop Virtualization Reader** | View all AVD resources, no changes | Auditors, read-only ops |
| **Desktop Virtualization Host Pool Contributor** | Manage all aspects of a host pool | Host pool owners |
| **Desktop Virtualization Application Group Contributor** | Manage an application group, except user/group assignment | App owners |
| **Desktop Virtualization Workspace Contributor** | Manage workspaces | Platform team |
| **Desktop Virtualization Session Host Operator** | View and remove session hosts, change drain mode | Operations engineers |
| **Desktop Virtualization User Session Operator** | Message, disconnect, and log off user sessions only | Helpdesk / Tier 1-2 |
| **Desktop Virtualization Virtual Machine Contributor** | Create, delete, start, stop VMs for the AVD resource provider | Automation identities |
| **Desktop Virtualization User** | Data-plane: use published apps/desktop | End users |

Notice the deliberate gap: Contributor roles manage resources but never grant user or group assignment. If you want an admin to both build a host pool and assign users to its app groups, you pair the relevant Contributor role with **User Access Administrator**. This separation exists so that platform engineers who provision infrastructure don't automatically also control who gets access to it — a genuine least-privilege boundary, not an accident.

For day-to-day operations, the two roles you'll assign most after initial build-out are **Desktop Virtualization Session Host Operator** (drain mode, host removal — your operations rotation) and **Desktop Virtualization User Session Operator** (message, disconnect, log off — your helpdesk tier, deliberately unable to touch host pool configuration).

## Data Plane vs Control Plane: The User Role Is Different

Every role above except one is a **control-plane** role — it grants permissions over the AVD resource objects themselves (host pools, application groups, workspaces) via Azure Resource Manager `actions`. **Desktop Virtualization User** is different: it's a **data-plane** role, granting only the `Microsoft.DesktopVirtualization/applicationGroups/useApplications/action` `dataAction`. This is the role — scoped to an application group — that actually determines which end users can see and launch a given desktop or RemoteApp. Assigning end users this role (directly or, more commonly, through a group) at the application group scope is how you populate a workspace's feed for them. Get the scope wrong — assign at the wrong application group, or forget the assignment for a new app group — and users authenticate fine but see nothing to connect to.

## Conditional Access: Which Apps Actually Govern AVD

Every AVD connection can, in principle, be authenticated to twice: once to the AVD **service** (subscribing to your feed, connecting to the gateway) and once to the **session host** (signing in to Windows), if single sign-on is enabled. Each phase is a different Microsoft Entra app in Conditional Access, so a policy targeting only one leaves the other phase unprotected:

- **Azure Virtual Desktop** (app ID `9cdead84-a844-4324-93f2-b2e6bb768d07`) — applies when a user subscribes, authenticates to the gateway during a connection, and when diagnostics are sent. This app was previously named *Windows Virtual Desktop*; if your resource provider was registered before the rename, you may still see the old name with the same app ID.
- **Windows Cloud Login** (app ID `270efc09-cd0d-444b-a71f-39af4910ec45`) — applies when the user authenticates to the session host, but only when SSO is enabled. Microsoft recommends matching your Conditional Access policy between this app and the Azure Virtual Desktop app, **except for sign-in frequency**, which behaves differently on each (see below).

If you enable SSO and only target the Azure Virtual Desktop app with your MFA policy, the session host sign-in phase goes unprotected — a real gap, not a theoretical one.

## The App You Must Never Put Behind MFA

There's a third app you'll encounter while searching the Conditional Access app picker: **Azure Virtual Desktop Azure Resource Manager Provider** (app ID `50e95039-b200-4007-bc97-8d5790743a63`). This app is used purely to retrieve the user's resource feed — it isn't a user-facing sign-in event — and Microsoft explicitly states it shouldn't have multifactor authentication applied. Adding it to an MFA-enforcing policy blocks feed discovery for your users. Know this app by name specifically so you don't select it by mistake when searching for "Azure Virtual" in the app picker.

## Sign-In Frequency: Two Apps, Two Behaviors

Sign-in frequency policies control how often a user must reauthenticate, and the two AVD apps behave differently under the same setting:

- On the **Azure Virtual Desktop** app, reauthentication is enforced when the user subscribes, manually refreshes their feed, or authenticates to the gateway. After the period expires, background feed refresh and diagnostics silently fail until the user's next interactive sign-in — there's no hard block, just a quiet feed staleness.
- On the **Windows Cloud Login** app, reauthentication is enforced when the user signs in to a session host with SSO enabled — and this is the only app where the **Every time** option is supported, prompting reauthentication roughly every 5 to 10 minutes after the last authentication, for scenarios that need very tight session control.

## Entra-Joined Session Hosts: The Extra Step

For Microsoft Entra joined session hosts specifically, there's a documented gotcha: for connections to succeed, you must either disable the legacy per-user MFA sign-in method, or — if you want to keep strong methods like Windows Hello for Business intact without loosening that — exclude the **Azure Windows VM Sign-In** app from your Conditional Access policy. Skipping this step is a common cause of "MFA works everywhere except my Entra-joined AVD hosts" tickets.

## Putting It Together: A Layered Access Design

A solid AVD access design layers, rather than merges, these controls: RBAC Contributor and Session Host/User Session Operator roles for admins and helpdesk at the control plane; Desktop Virtualization User assignments per application group for end users at the data plane; and a Conditional Access policy pair — one on Azure Virtual Desktop, one on Windows Cloud Login, both requiring MFA and a sensible sign-in frequency, deliberately excluding the ARM Provider app — governing authentication for everyone, regardless of their RBAC role. Lesson 3 builds on this by hardening the session hosts themselves once a user is actually connected.
