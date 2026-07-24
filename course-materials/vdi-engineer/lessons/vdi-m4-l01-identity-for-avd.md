---
course: vdi-engineer
title: 'Identity for AVD: Entra Join Types, FSLogix Kerberos, and SSO'
month: 4
monthTitle: Identity & Security for Virtual Desktops
lesson: 1
summary: 'Every AVD security decision starts with one question: what identity backs your session hosts?
  This lesson maps the three supported join types — Microsoft Entra joined, Microsoft Entra hybrid joined,
  and Microsoft Entra Domain Services — to what they unlock and what they block, especially single sign-on.
  You''ll learn why on-premises-only identities are never supported, how hybrid UPN/SID mismatches break
  sign-in, and how to wire FSLogix profile containers to Azure Files using Microsoft Entra Kerberos so
  profiles load without a domain controller in sight. You''ll finish by enabling Microsoft Entra authentication
  for RDP — the mechanism behind AVD''s recommended single sign-on experience — and know the licensing
  you need before you start.'
objectives:
- Differentiate Microsoft Entra joined, Microsoft Entra hybrid joined, and Microsoft Entra Domain Services
  session hosts and identify which support Microsoft Entra single sign-on
- Explain why AVD requires every user identity to be discoverable in Microsoft Entra ID, and apply the
  UPN/SID matching rule for hybrid identities
- Configure FSLogix profile containers on Azure Files using Microsoft Entra Kerberos for hybrid, cloud-only,
  or external identities
- List the licensing prerequisites for AVD access and Conditional Access-driven identity scenarios
- Enable Microsoft Entra authentication for RDP and describe the five tasks required to turn on single
  sign-on for a host pool
quiz:
- q: Which session host join types are supported for Microsoft Entra single sign-on (SSO) to the session
    host itself?
  options:
  - Microsoft Entra Domain Services joined only
  - Active Directory Domain Services joined only, with no Microsoft Entra ID presence
  - Any join type, including standalone AD DS
  - Microsoft Entra joined or Microsoft Entra hybrid joined only
  answer: 3
  why: Session hosts must be Microsoft Entra joined or Microsoft Entra hybrid joined to use Entra SSO
    for RDP. Hosts joined only to Microsoft Entra Domain Services or only to AD DS aren't supported for
    this feature.
- q: A hybrid AVD user's on-premises AD account is user@contoso.local, but their Microsoft Entra ID account
    is user@contoso.com. Under what condition does AVD support this configuration?
  options:
  - Only if either the UPN or the SID (ObjectSID / OnPremisesSecurityIdentifier) matches between the AD
    and Microsoft Entra ID accounts
  - It's never supported — UPNs must be identical across AD and Microsoft Entra ID
  - Only if the organization disables Microsoft Entra Connect synchronization
  - Only if the session host is Microsoft Entra Domain Services joined
  answer: 0
  why: AVD only supports mismatched UPNs when either the UPN or the SID for both the AD and Microsoft
    Entra ID accounts match — SID meaning the AD ObjectSID property matches the Microsoft Entra ID OnPremisesSecurityIdentifier
    property.
- q: You're configuring Azure Files with Microsoft Entra Kerberos to host FSLogix profiles. What's true
    about the storage account's authentication method?
  options:
  - The storage account can authenticate with both Microsoft Entra ID and AD DS simultaneously for redundancy
  - The storage account can only use one authentication method at a time — Microsoft Entra ID, AD DS,
    or Microsoft Entra Domain Services, never two
  - Authentication method doesn't matter for FSLogix, only NTFS permissions do
  - Microsoft Entra Kerberos requires AD DS to also be enabled on the same account
  answer: 1
  why: An Azure Storage account can't authenticate with both Microsoft Entra ID and a second method like
    AD DS or Microsoft Entra Domain Services — only one authentication method can be active at a time.
- q: Which Microsoft Entra application must have isRemoteDesktopProtocolEnabled set to true to enable
    Microsoft Entra authentication for RDP?
  options:
  - Azure Virtual Desktop
  - Microsoft Remote Desktop
  - Windows Cloud Login
  - Azure Virtual Desktop Azure Resource Manager Provider
  answer: 2
  why: You enable Microsoft Entra authentication for RDP by setting isRemoteDesktopProtocolEnabled to
    true on the Windows Cloud Login service principal (app ID 270efc09-cd0d-444b-a71f-39af4910ec45).
- q: A session host is Microsoft Entra hybrid joined, and you're enabling Microsoft Entra SSO for RDP.
    What must you create first to avoid sign-in failures?
  options:
  - A second Azure Files share
  - A Windows Hello for Business certificate template
  - A Microsoft Entra Domain Services replica set
  - A Kerberos server object
  answer: 3
  why: Microsoft Entra hybrid joined session hosts need a Kerberos server object to complete authentication
    to a domain controller. Without it, connections may fail with a 'session doesn't exist' error or silently
    skip SSO.
- q: In three to four sentences, explain why a session host joined only to Microsoft Entra Domain Services
    can't use Microsoft Entra single sign-on for RDP, and what identity model you'd recommend for a brand-new,
    cloud-only organization with no on-premises Active Directory.
  answer: Microsoft Entra SSO for RDP depends on the session host itself having a Microsoft Entra device
    identity so it can receive an Entra-issued RDP access token; a host joined only to Microsoft Entra
    Domain Services is a member of a separate, Kerberos/NTLM-compatible managed domain and never establishes
    that Entra device identity, so the SSO token flow has nothing to attach to. For a greenfield, cloud-only
    organization, the recommended model is Microsoft Entra joined session hosts with cloud-only user identities,
    FSLogix profiles stored on Azure Files using Microsoft Entra Kerberos, and Microsoft Entra SSO enabled
    on the host pool — no AD DS or Microsoft Entra Domain Services required at all.
  why: SSO requires the session host to hold a Microsoft Entra device identity, which Entra Domain Services
    and standalone AD DS joins don't provide. A cloud-only organization avoids the problem entirely by
    going fully Microsoft Entra joined, which is also the simplest identity model to operate.
resources:
- label: Azure Virtual Desktop identities and authentication (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/authentication
- label: Configure single sign-on for Azure Virtual Desktop using Microsoft Entra ID
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-single-sign-on
- label: Store FSLogix profile containers on Azure Files using Microsoft Entra ID
  url: https://learn.microsoft.com/en-us/fslogix/how-to-configure-profile-container-entra-id-hybrid
- label: Deploy Microsoft Entra joined VMs in Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/deploy-azure-ad-joined-vm
video: vdi-m4-l01-identity-for-avd.mp4
---

## Why Identity Comes Before Everything Else

Every AVD security decision in this module — RBAC, Conditional Access, session host hardening, Zero Trust — sits on top of one foundational choice: how are your session hosts and users identified? Get this wrong and you'll spend weeks debugging SSO failures, FSLogix profiles that won't mount, or Conditional Access policies that silently don't apply. Get it right and the rest of AVD security nearly falls into place.

## Three Ways to Join a Session Host

AVD supports three session host join configurations, and they aren't interchangeable:

| Join type | Cloud-only users | Hybrid users | Entra SSO for RDP | Needs DC line-of-sight |
|---|---|---|---|---|
| **Microsoft Entra joined** | Yes | Yes (can be assigned to app groups) | Yes | No, unless you also need Kerberos to on-prem resources |
| **Microsoft Entra hybrid joined** | No | Yes | Yes | Yes for Kerberos, unless using Entra Kerberos for Azure Files |
| **Microsoft Entra Domain Services joined** | No (requires password hash sync) | Yes | **No** | Depends on your Entra Domain Services topology |

A fourth configuration — session hosts joined only to standalone AD DS with no Microsoft Entra ID presence at all — isn't supported: users must be discoverable through Microsoft Entra ID to access AVD, full stop.

The practical decision: greenfield, cloud-first deployments go Microsoft Entra joined. Estates with an existing on-premises AD DS footprint that must be preserved — line-of-business apps that need Kerberos or NTLM, GPO-managed tooling — go Microsoft Entra hybrid joined. Microsoft Entra Domain Services is a narrower option, useful when you want a lightweight managed domain without operating your own domain controllers, but it explicitly does not support Entra SSO for RDP. Plan around that limitation if SSO is a hard requirement.

## The Rule AVD Never Breaks

Whatever join type you choose, one rule never changes: AVD requires user identities to be discoverable through Microsoft Entra ID. Standalone Active Directory deployments — even ones federated through AD FS with no synchronization to Microsoft Entra ID — aren't supported. If you're migrating a legacy RDS estate that has never touched Entra ID, standing up Microsoft Entra Connect (or moving straight to cloud-only accounts) is a prerequisite, not an optional step.

## Hybrid Identity's Sharp Edge: UPN and SID Matching

Hybrid identities are common, but they carry a gotcha every AVD engineer eventually hits: a mismatch between the AD UPN and the Microsoft Entra ID UPN. If your on-premises account is `user@contoso.local` and it syncs to Microsoft Entra ID as `user@contoso.com`, AVD only supports that configuration if either the UPN **or** the SID matches between the two directories — where SID means the AD `ObjectSID` property matching the Microsoft Entra ID `OnPremisesSecurityIdentifier` property. When neither matches, users can authenticate to the AVD service but fail to sign in to the session host itself. This is one of the most common "SSO works for the portal but not the desktop" support tickets — check UPN/SID alignment before you touch anything else.

## FSLogix Profiles Without a Domain Controller

Traditionally, FSLogix profile containers on Azure Files needed AD DS or Microsoft Entra Domain Services for Kerberos authentication to the SMB share, which meant session hosts needed network line-of-sight to a domain controller at every logon. Microsoft Entra Kerberos removes that requirement: Microsoft Entra ID itself issues the Kerberos tickets needed to access the file share over standard SMB, and hybrid-joined or Entra-joined session hosts don't need DC line-of-sight to load a profile (a system with DC line-of-sight is still needed once, to configure share permissions).

The setup, in order:

1. Create the storage account and file share. A storage account can authenticate with only one method at a time — Microsoft Entra ID, AD DS, or Microsoft Entra Domain Services, never two simultaneously.
2. Enable Microsoft Entra Kerberos authentication on the storage account, which creates the Entra ID app registration backing the share.
3. Assign share-level permissions, either through default share-level permissions or Azure RBAC roles, then set the recommended NTFS-level permissions for the FSLogix profile folder.
4. Grant admin consent to the storage account's new service principal, and disable multifactor authentication on that service principal specifically — profile mounting happens silently at logon with no UX to complete step-up authentication, so an MFA-enforcing Conditional Access policy that catches this app breaks every profile load.
5. On the session host, enable the Kerberos/CloudKerberosTicketRetrievalEnabled setting via Intune Settings Catalog (now supported for Windows Enterprise multi-session) or Group Policy, then point FSLogix's VHDLocations registry value at the file share's UNC path.
6. For cloud-only or external identities specifically, also add the kdc_enable_cloud_group_sids tag to the app manifest so Entra includes cloud-only group SIDs in the Kerberos ticket.

Cloud-only and external identity support for this path is available in the Azure public cloud; hybrid identity support additionally covers Azure Government and the Azure operated by 21Vianet cloud.

## Licensing You Need Before You Start

Two license tracks matter here, and they're often conflated:

- **AVD access rights** — a per-user entitlement most organizations already own through Microsoft 365 E3/E5, Microsoft 365 Business Premium, or Windows Enterprise E3/E5; standalone per-user AVD access licenses exist for anyone who doesn't already qualify.
- **Microsoft Entra ID P1 (or P2)** — required for Conditional Access, dynamic device groups (used to hide the SSO consent prompt), and MFA enforcement. Don't assume this is bundled — verify it explicitly during planning, because everything in Lesson 2 depends on it.

## Turning On Microsoft Entra SSO for RDP

Microsoft's recommended remote-session authentication mechanism is Microsoft Entra SSO: it lets the connection skip the session host credential prompt entirely and sign the user in to Windows with a Microsoft Entra ID token, unlocking passwordless authentication and third-party identity provider federation inside the session too. Enabling it is five tasks:

1. **Enable Microsoft Entra authentication for RDP** — set isRemoteDesktopProtocolEnabled to true on the Windows Cloud Login service principal (app ID 270efc09-cd0d-444b-a71f-39af4910ec45), via the Azure portal (Microsoft Entra ID → Devices → Remote connection configuration) or the Microsoft Graph PowerShell SDK.
2. **Hide the consent prompt** — without this step, users see a "Yes, allow this connection" dialog the first time they hit a new host. Target a dynamic device group of your session hosts on the Windows Cloud Login service principal to suppress it.
3. **Create a Kerberos server object** — required if hosts are Entra hybrid joined, or if they're Entra joined but the environment still has AD DS domain controllers users need to reach.
4. **Review Conditional Access policies** — SSO introduces a new sign-in event at the session host, which Lesson 2 covers in depth.
5. **Enable SSO on the host pool** — set the RDP property Microsoft Entra single sign-on to "Connections will use Microsoft Entra authentication to provide single sign-on" in the portal, or set enablerdsaadauth to 1 via PowerShell.

Session hosts need Windows 11 (or Windows 10) Enterprise single or multi-session with the 2022-10 cumulative update or later, or Windows Server 2022 with its 2022-10 update, and must be Entra joined or Entra hybrid joined — Entra Domain Services-only or AD DS-only hosts are excluded from this feature entirely.

With identity and SSO wired up, Lesson 2 builds the access control layer on top: who gets which AVD role, and which Conditional Access apps actually govern each authentication phase.
