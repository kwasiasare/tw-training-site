---
course: vdi-engineer
title: 'Securing AVD Session Hosts: Intune, Defender, and Egress Control'
month: 4
monthTitle: Identity & Security for Virtual Desktops
lesson: 3
summary: Session hosts are shared, frequently rebuilt, multi-user machines, and they take different hardening
  tooling than a single-user laptop. This lesson covers what Intune actually supports on Windows 11 Enterprise
  multi-session — device versus user configuration, the settings-catalog-only rule, and the enrollment
  gotchas that break it — how to onboard ephemeral pooled hosts to Microsoft Defender for Endpoint without
  flooding the console with duplicate devices, screen capture protection and watermarking for data-loss
  scenarios, locking down RDP device and clipboard redirection, and using Azure Firewall to control egress
  from session hosts that need surprisingly little outbound access.
objectives:
- Distinguish device-based from user-based Intune configuration on Windows 11 Enterprise multi-session
  and identify which profile types are supported
- Enroll Microsoft Entra joined and Microsoft Entra hybrid joined multi-session hosts in Intune without
  hitting the cloned-image or auto-enrollment pitfalls
- Onboard pooled, frequently redeployed session hosts to Microsoft Defender for Endpoint using the single-entry-per-virtual-desktop
  method
- Configure screen capture protection and watermarking to reduce data exfiltration risk on session hosts
- Lock down RDP device and clipboard redirection and scope session host egress with Azure Firewall
quiz:
- q: Which configuration profile templates are supported for Windows Enterprise multi-session in Intune,
    beyond the Settings Catalog?
  options:
  - All templates, identical to a single-session Windows 11 device
  - Trusted certificate, SCEP certificate, PKCS certificate, and Device Tunnel VPN only
  - Only Windows Update ring templates
  - No templates are supported; only PowerShell scripts
  answer: 1
  why: Only Trusted certificate, SCEP certificate, PKCS certificate (device or user scoped), and Device
    Tunnel VPN templates are supported for multi-session; everything else must go through the Settings
    Catalog, and unsupported templates report as Not applicable.
- q: An organization enrolls a Microsoft Entra hybrid joined multi-session host in Intune using group
    policy auto-enrollment configured for user credentials. Enrollment fails. Why?
  options:
  - Hybrid joined hosts can never enroll in Intune
  - The Azure Virtual Desktop agent doesn't support Intune
  - Multi-session hosts must be enrolled using device credentials, not user credentials
  - Only Microsoft Entra joined hosts can enroll
  answer: 2
  why: Auto-enrollment for Windows Enterprise multi-session VMs must be configured to use device credentials;
    user-credential auto-enrollment is a documented cause of enrollment failure.
- q: Why does Microsoft recommend onboarding pooled, frequently redeployed AVD hosts to Defender for Endpoint
    using a single entry per virtual desktop, rather than a new entry per VM instance?
  options:
  - It's required to enable tamper protection
  - It reduces Microsoft Defender for Endpoint licensing costs
  - It's the only method that supports Windows 11 multi-session at all
  - It prevents duplicate device objects in the Defender portal for hosts that are deleted and rebuilt
    often, keeping investigation in the context of one device
  answer: 3
  why: Organizations that frequently delete and redeploy AVD hosts should use the single-entry method
    so multiple objects for what is conceptually the same machine aren't created, which would otherwise
    confuse incident investigation.
- q: What's the functional difference between 'Block screen capture on client' and 'Block screen capture
    on client and server' in AVD screen capture protection?
  options:
  - Client-and-server blocking additionally requires Windows 11 version 22H2 or later on the session host
  - There is no difference — they're aliases for the same setting
  - Client-only blocking requires Windows Server 2022
  - Client-and-server blocking only works with third-party clients
  answer: 0
  why: Block screen capture on client is available with a supported version of Windows 10 or 11; blocking
    on client and server additionally requires Windows 11 version 22H2 or later on the session host side.
- q: A security team wants to be able to trace which session a leaked screenshot came from. Which AVD
    feature is designed for this?
  options:
  - Screen capture protection alone
  - Watermarking, using the QR code's embedded Connection ID or Device ID
  - RDP clipboard redirection lockdown
  - Microsoft Defender for Endpoint tamper protection
  answer: 1
  why: Watermarking overlays a QR code containing the Connection ID or Device ID of the remote session,
    letting admins trace a captured image or photo back to the specific session it came from.
- q: You're hardening a pooled, non-persistent AVD host pool used by contractors on unmanaged devices.
    In three to four sentences, describe the combination of controls from this lesson you'd apply, and
    why layering them matters more than picking just one.
  answer: 'I''d onboard the hosts to Microsoft Defender for Endpoint using the single-entry method, since
    pooled hosts are rebuilt often, with tamper protection enabled; apply an Intune device-scoped security
    baseline plus a compliance policy for antivirus and firewall state; enable screen capture protection
    with watermarking so any successful capture is traceable; and lock down clipboard and drive redirection
    via custom RDP properties so contractors can''t exfiltrate data through the session itself. Layering
    matters because each control covers a different failure mode: Defender and Intune address the endpoint
    being compromised, screen capture protection and watermarking address unauthorized data extraction
    from the display, and redirection lockdown addresses direct exfiltration through the RDP channel —
    losing any single layer leaves that specific path open.'
  why: Session host security for a high-risk, unmanaged-device pooled pool needs endpoint protection,
    display-level data controls, and channel-level redirection controls together; no single control from
    this lesson covers all three exfiltration paths on its own.
resources:
- label: Using Azure Virtual Desktop multi-session with Microsoft Intune
  url: https://learn.microsoft.com/en-us/intune/solutions/azure-virtual-desktop-multi-session
- label: Onboard Windows devices in Azure Virtual Desktop (Microsoft Defender for Endpoint)
  url: https://learn.microsoft.com/en-us/defender-endpoint/onboard-windows-multi-session-device
- label: Watermarking in Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/watermarking
- label: Screen capture protection in Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/screen-capture-protection
- label: Customize Remote Desktop Protocol (RDP) properties for a host pool
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/customize-rdp-properties
video: vdi-m4-l03-securing-session-hosts.mp4
---

## A Different Kind of Endpoint

A session host isn't a laptop. It's shared by multiple concurrent users, it's frequently deleted and rebuilt from a golden image, and in a pooled host pool it may have no persistent identity of its own beyond a few weeks. Every tool in this lesson — Intune, Microsoft Defender for Endpoint, screen capture protection, RDP redirection controls, Azure Firewall — has a session-host-specific wrinkle because of that, and missing the wrinkle is why "we followed the normal Windows 11 hardening checklist" so often fails on AVD.

## What Intune Actually Supports on Multi-Session

Device configuration support for Windows Enterprise multi-session in Intune is generally available, and so is user-scoped configuration — but multi-session is treated as its own OS edition with real limits, not a Windows 11 clone:

- Configuration must go through the **Settings Catalog**, filtered by the **OS edition == Enterprise multi-session** filter, to see what actually applies. Outside the Settings Catalog, only four template types are supported: Trusted certificate, SCEP certificate, PKCS certificate (device or user scoped), and Device Tunnel VPN. Everything else reports as **Not applicable**.
- **Device-scoped** policy and system-context apps apply when assigned to device groups; **user-scoped** policy (via Settings Catalog user-scope settings, user certificates, and user-context PowerShell scripts) applies when assigned to user groups. Mixing scopes — a device policy assigned to a user group — fails silently as Error or Not applicable.
- **Compliance policies** are limited to a specific subset: OS version bounds, password settings, and the Defender antimalware/firewall/antivirus signals. Everything else is Not applicable. Compliance policies must be device-targeted; user-targeted compliance isn't supported.
- **App deployment**: apps must install in system/device context, targeted to devices, with Required or Uninstall intent — Available isn't supported. RemoteApp and MSIX app attach aren't deployable through Intune at all; that's a host pool / AVD-native concern.
- **Windows Autopilot, Enrollment Status Page, and Fresh Start** aren't supported — multi-session skips the OOBE enrollment flow entirely.

## Enrollment: The Gotchas That Break It

Enrollment fails in a small number of predictable ways, and knowing them upfront saves a support cycle:

- Multi-session VMs must enroll using **device credentials**, not user credentials — a hybrid-joined host with group policy auto-enrollment configured for user credentials will fail.
- The AVD agent must be version **1.0.2944.1400 or later**.
- Multiple MDM providers on the same tenant isn't supported.
- **Never enroll from a cloned image.** Cloning an already-enrolled device (or VM) replicates its enrollment and identity tokens, which causes enrollment/sync failures for every clone — build your golden image before enrollment, or exclude enrollment state from the image entirely.
- Hosts joined only to **Microsoft Entra Domain Services** can't be managed by Intune at all — a hard exclusion, not a configuration gap.
- FSLogix and Intune don't coexist safely on token roaming by default: confirm you're running a supported FSLogix configuration with token roaming disabled (RoamIdentity settings), since Intune doesn't support token roaming between devices.

## Onboarding Pooled Hosts to Microsoft Defender for Endpoint

Pooled, non-persistent host pools present a specific onboarding problem: if every rebuilt VM instance registers as a brand-new device, the Defender for Endpoint console fills with duplicate, orphaned device entries for what is conceptually a single virtual desktop, and incident investigation becomes a guessing game about which "device" is actually the one a user was on. Microsoft's guidance is to onboard using a **single entry per virtual desktop** approach for organizations that frequently delete and redeploy hosts, keeping the investigation experience tied to the machine name rather than the ephemeral VM instance.

Once onboarded, you unlock endpoint security controls managed through Intune's endpoint security policies, including **tamper protection** for Windows 11 Enterprise (and Windows 11 Enterprise multi-session) session hosts — but onboarding to Defender for Endpoint has to happen *before* you apply a tamper protection policy, or the policy has nothing to attach to.

## Screen Capture Protection and Watermarking

Two AVD-native controls address the "authorized user, unauthorized data extraction" risk — a user who's legitimately signed in but tries to screenshot, screen-share, or photograph sensitive content:

- **Screen capture protection** blocks remote content from being captured in screenshots and screen sharing at the OS/API level. **Block screen capture on client** works with any supported Windows 10 or 11 client; **Block screen capture on client and server** additionally requires Windows 11 version 22H2 or later on the session host and blocks capture attempts made from the server side too.
- **Watermarking** overlays a QR code on the remote session containing the Connection ID or Device ID, so if content is captured by a method screen capture protection can't stop — a phone photo of the screen, for instance — admins can still trace the leak back to the specific session.

Both are configured through Intune (Settings Catalog) or Group Policy on the session host, and both are enforced by the Windows App or Remote Desktop client, so client version matters as much as host configuration.

## Locking Down RDP Redirection

Custom RDP properties on a host pool control which local resources get redirected into a session — and for regulated or contractor-facing pools, the default "allow everything" posture is usually wrong. The properties to review during hardening include clipboard redirection, drive/USB redirection, printer redirection, COM port redirection, and smart card redirection; each has a corresponding `redirect*` property you can set to disabled per host pool. This is configured the same way as any other RDP property customization — through the Azure portal host pool properties or PowerShell — and it's the layer that stops a legitimately-authenticated, legitimately-authorized user from simply copying data out through the clipboard or a mapped local drive.

## Azure Firewall for Egress Control

Session hosts need remarkably little outbound access once deployed: the AVD required URLs (service tags and specific FQDNs for the control plane, agent updates, and Windows activation), plus whatever your applications and Windows Update need. Rather than allowing broad outbound internet access, route session host subnets through **Azure Firewall** (or Azure Firewall Premium, if you need TLS inspection and IDPS on top of FQDN filtering) and combine it with network security groups to explicitly allow only the required AVD service tags and application FQDNs. This turns "session host got compromised, now what can it reach" from an open question into a short, auditable list.

## Layering It Together

None of these controls substitutes for another. Intune and Defender for Endpoint protect the endpoint itself; screen capture protection and watermarking protect the display layer; RDP redirection lockdown protects the data channel; Azure Firewall protects the network egress path. A session host hardened on only one of these axes still has three open doors. Lesson 4 zooms out from AVD specifically to show how this same layered thinking maps onto Citrix DaaS and Omnissa Horizon, so the pattern travels with you even if the platform doesn't.
