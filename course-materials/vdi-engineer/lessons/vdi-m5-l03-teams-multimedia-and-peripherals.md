---
course: vdi-engineer
title: Teams, Multimedia, and Peripherals on Virtual Desktops
month: 5
monthTitle: User Environments & App Delivery
lesson: 3
summary: Real-time media and peripherals are where VDI user experience is won or lost. This lesson covers
  how Microsoft Teams media optimization works on AVD in 2026 — SlimCore versus the older WebRTC Redirector
  Service — plus multimedia redirection, camera and audio redirection, cloud-based printing with Universal
  Print, and scanner/USB handling, closing with a pre-go-live test checklist.
objectives:
- Explain how Teams calling and meeting media is redirected to the local device on Azure Virtual Desktop
- Distinguish SlimCore from the WebRTC Redirector Service and know when each applies to Classic Teams
  vs new Teams
- Configure the registry keys and client prerequisites required for Teams media optimization
- Choose the right approach for printing, scanning, and USB peripherals in a virtual desktop session
- Build a pre-go-live test checklist covering multimedia, audio/video devices, and peripherals
quiz:
- q: By default, how does a Teams call behave in an Azure Virtual Desktop session if media optimization
    is NOT configured?
  options:
  - The call is automatically blocked until optimization is enabled
  - Audio and video are decoded and rendered on the session host itself, then that already-encoded output
    streams down to the client — adding server load and end-to-end latency
  - Teams falls back to a phone-only audio bridge
  - The session host redirects the call to the client with zero configuration required
  answer: 1
  why: 'Without media optimization, Teams runs entirely on the session host: it decodes and renders audio/video
    there, then that output has to be re-encoded into the remote display protocol and streamed to the
    client — doubling encode/decode work and adding latency. Media optimization instead redirects the
    actual call handling to the local client device.'
- q: What are the two components Azure Virtual Desktop uses to redirect Teams calling and meeting media
    to the local device, and how do they relate to Classic Teams vs new Teams?
  options:
  - SlimCore and RemoteFX — both are required together for any Teams call
  - Only the WebRTC Redirector Service; SlimCore is a Citrix-only feature
  - SlimCore and the WebRTC Redirector Service — new Teams can use either one, while Classic Teams uses
    only the WebRTC Redirector Service
  - Only SlimCore; the WebRTC Redirector Service was fully retired in 2025
  answer: 2
  why: New Teams can use either SlimCore or the older WebRTC Redirector Service (Microsoft recommends
    installing the WebRTC Redirector Service alongside SlimCore for new Teams as a fallback for users
    roaming to devices that don't yet support the new architecture), while Classic Teams is limited to
    the WebRTC Redirector Service only.
- q: How can you confirm Teams media optimization actually loaded during a live session?
  options:
  - Check Task Manager for a process named TeamsOptimized.exe
  - There is no way to verify this from within the Teams client
  - Run a PowerShell cmdlet Get-TeamsOptimizationStatus on the session host
  - Open Teams Settings > About Teams and check for a banner reading 'AVD SlimCore Media Optimized' or
    'AVD Media Optimized'
  answer: 3
  why: The Teams client itself surfaces optimization state under Settings > About Teams. A banner showing
    'AVD SlimCore Media Optimized' or 'AVD Media Optimized' confirms it loaded; a banner reading 'AVD
    Media not connected' means it didn't, and the standard fix is to quit and relaunch the Teams app in-session.
- q: Which of these is the current, cloud-based approach recommended for printing from Azure Virtual Desktop
    or Windows 365 sessions, replacing traditional on-premises print servers?
  options:
  - Universal Print
  - A locally installed print driver baked into the golden image for every possible printer model
  - RDP printer redirection is the only supported method and Universal Print does not apply to VDI
  - Print jobs must always be routed through a physical print server on-premises
  answer: 0
  why: Universal Print is Microsoft's cloud-based print service that removes the need for on-premises
    print servers and per-device driver installation, and it's the recommended modern approach to add
    to an AVD/Windows 365 image alongside (not necessarily instead of) client/RDP printer redirection
    depending on the scenario.
- q: Which registry key must be set on each session host to tell the Teams client it's running in an Azure
    Virtual Desktop environment, a prerequisite for media optimization to even attempt to load?
  options:
  - HKEY_CURRENT_USER\SOFTWARE\Teams\OptimizeForVDI set to true
  - HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Teams with a DWORD value IsWVDEnvironment set to 1
  - There is no registry requirement; optimization is automatic on any AVD host
  - HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Teams\EnableRedirect
  answer: 1
  why: Microsoft's documented setup step is creating the IsWVDEnvironment DWORD value under HKLM\SOFTWARE\Microsoft\Teams
    on each session host. Without this, the Teams client has no signal that it's running in a virtualized
    session and won't attempt to load media optimization at all.
- q: In two to four sentences, describe a pre-go-live test checklist item you would run specifically for
    Teams media optimization before rolling a new host pool image to production, and explain what a failed
    result would look like to the user.
  answer: 'One concrete checklist item: from a real session on the new image, join a live Teams test call
    and check Settings > About Teams for the optimization banner, then verify that local microphones,
    cameras, and speakers show up in the Teams device menu instead of a generic ''Remote audio'' entry.
    A failed result looks like a banner reading ''AVD Media not connected'' or the device menu only showing
    remote/virtual audio devices — meaning the call is actually running unoptimized on the session host,
    with visibly worse audio/video quality and added host CPU load, even though the meeting itself still
    connects and looks functional to a casual glance.'
  why: Optimization failures are easy to miss because the call still works — it just runs unoptimized
    on the server, which silently degrades quality and increases host load, so this has to be explicitly
    checked rather than assumed from 'the call connected.'
resources:
- label: Use Microsoft Teams on Azure Virtual Desktop
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/teams-on-avd
- label: Microsoft Teams for Virtualized Desktop Infrastructure (VDI)
  url: https://learn.microsoft.com/en-us/microsoftteams/teams-client-vdi-requirements-deploy
- label: Universal Print documentation
  url: https://learn.microsoft.com/en-us/universal-print/
- label: Customize RDP properties for a host pool
  url: https://learn.microsoft.com/en-us/azure/virtual-desktop/customize-rdp-properties
video: vdi-m5-l03-teams-multimedia-and-peripherals.mp4
---

## Why Real-Time Media Is a Special Case

Most applications in a virtual desktop don't care that they're remote — a spreadsheet renders the same whether it's local or streamed over RDP. Real-time audio and video are different. Without help, a Teams call runs entirely on the session host: the host decodes incoming audio/video, renders it, then that already-rendered output gets re-encoded into the remote display protocol and streamed down to the client. That's double work (server-side decode/encode, then protocol encode/decode again) and it adds real, user-visible latency and jitter — exactly what a live call can't tolerate. **Media optimization** exists to route the actual call handling to the local client device instead, so the host just carries signaling.

## SlimCore vs. the WebRTC Redirector Service

Azure Virtual Desktop uses one of two components to achieve this redirection, and which one applies depends on which Teams client you're running:

- **Classic Teams** uses the **WebRTC Redirector Service** only. Classic Teams (Windows-based endpoints) is on a retirement clock: end of support October 1, 2026, end of availability April 1, 2027 — after that you must be on new Teams.
- **New Teams** can use either **SlimCore** (the newer, purpose-built media engine) or the WebRTC Redirector Service. Microsoft's recommendation is to install the WebRTC Redirector Service alongside SlimCore even for new Teams — it acts as an automatic fallback if a user roams to a device or platform that doesn't yet support SlimCore.

SlimCore is the direction the platform is moving: it's the same media engine that powers the native Teams client, extended to virtualized scenarios, and its rollout has been expanding steadily through 2026 across Windows and macOS, with support reaching RemoteApp and Cloud App scenarios in the Windows App (not just full desktop sessions). Its required components ship bundled with new Teams and Windows App or the Remote Desktop client, so there's no separate SlimCore installer to manage the way there is for the WebRTC Redirector Service MSI.

## Setting It Up

Three things have to be true before media optimization can load in a session:

1. **The session host has to identify itself as a VDI environment.** Set the registry value `HKLM\SOFTWARE\Microsoft\Teams\IsWVDEnvironment` (DWORD) to `1` on every session host — bake this into your golden image.
2. **The WebRTC Redirector Service is installed** on session hosts that need the fallback path (effectively all of them, per Microsoft's guidance).
3. **The client meets minimum version requirements.** Windows App and the Remote Desktop client both have documented minimum versions for SlimCore support, and the Visual C++ Redistributable must be current on both client and host. If you use FSLogix and want new Teams, you also need a current-enough FSLogix build (2210 hotfix 3 or later) — an easy thing to miss if your golden image was built against an older FSLogix baseline.

After installing, verify optimization actually loaded from inside a live session: Teams **Settings → About Teams** shows a banner reading either **'AVD SlimCore Media Optimized'** or **'AVD Media Optimized.'** If it instead reads **'AVD Media not connected,'** quit and relaunch Teams in-session before escalating — that resolves the majority of first-time failures. You can cross-check by opening the device menu: optimized sessions enumerate the user's actual local microphones and cameras; an unoptimized session just shows a generic 'Remote audio' entry.

## Multimedia and Device Redirection Beyond Calling

Teams calling/meeting redirection is a special case built specifically for Teams. For general multimedia playback (a training video in a browser, for instance) and general audio/camera use outside of Teams, Azure Virtual Desktop's RDP properties give you separate controls: `audiocapturemode:i:1` enables microphone capture and redirects audio-capable apps, `audiomode:i:0` plays remote audio on the local device, and `camerastoredirect:s:*` redirects all local cameras into the session. Note that **when Teams media optimization is working, you don't need these device redirections just for Teams** — optimization already routes Teams' own audio/video locally. You'd still enable general redirection for other applications that need microphone or camera access outside of Teams.

## Printing: Universal Print

Printing is the peripheral scenario every VDI rollout underestimates. The legacy pattern — install every printer driver your org uses into the golden image, plus RDP client printer redirection for local/home printers — creates a driver-maintenance burden that scales badly and is a common source of print-spooler crashes on shared multi-session hosts. **Universal Print** replaces the on-premises print server model with a cloud-based print service: printers are registered once, access is controlled with Entra security groups, and clients print without installing a device-specific driver, which is exactly the driver-sprawl problem multi-session hosts are most exposed to. For scenarios where users genuinely need to print to a printer physically attached to their local machine, standard RDP printer redirection is still the right tool — the two aren't mutually exclusive, they cover different scenarios.

## Scanners and USB

Scanners and other USB peripherals typically rely on **RemoteFX USB redirection** or, more commonly today, client drive/device redirection built into the Windows App and Remote Desktop client. USB redirection has real bandwidth and latency costs and doesn't work uniformly across every client platform (mobile clients, for instance, have limited USB redirection support), so this is squarely a 'test with the actual device and the actual client the users will use' item, not something to assume from a spec sheet.

## What to Test Before Go-Live

Build a checklist specific to your user population's actual devices and workflows, but at minimum: a live Teams call with the optimization banner check described above; local microphone, speaker, and camera enumeration inside Teams; screen sharing both ways (presenting and receiving); printing to at least one Universal Print-registered device and one client-redirected device if your users need both; and, if relevant, a scanner or specialty USB device from an actual client machine, not just the session host. Test this on every client platform you support — Windows App on Windows behaves differently from Windows App on macOS or a thin client, and SlimCore's rollout across platforms hasn't been uniform through 2026, so don't assume parity without checking.
