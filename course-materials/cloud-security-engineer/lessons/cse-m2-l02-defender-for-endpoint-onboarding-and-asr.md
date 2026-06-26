---
course: cloud-security-engineer
title: 'Defender for Endpoint: Onboarding and Attack Surface Reduction'
month: 2
monthTitle: Modern Endpoint Security & Threat Protection
lesson: 2
summary: Here you connect endpoints to Microsoft Defender for Endpoint (MDE) and turn on its proactive
  hardening controls. You will establish the Intune-to-MDE connector, onboard Windows devices through
  an Intune EDR policy, and confirm devices appear in the Microsoft Defender portal. You will then roll
  out Attack Surface Reduction (ASR) rules using a disciplined audit-then-block strategy, naming real
  rules such as block credential stealing from LSASS and block Office child processes. Finally you will
  enable controlled folder access, network protection, tamper protection, and read your exposure score
  from Microsoft Defender Vulnerability Management.
objectives:
- Describe MDE's cloud-plus-sensor architecture and the role of the Intune connector.
- Onboard Windows devices to MDE through an Intune endpoint detection and response (EDR) policy.
- Deploy Attack Surface Reduction rules and run an audit-then-block rollout to avoid breaking business
  apps.
- Identify several real ASR rules by name and GUID and explain what each blocks.
- Enable controlled folder access, network protection, and tamper protection.
- Interpret the exposure score and security recommendations in Defender Vulnerability Management.
video: cse-m2-l02-defender-for-endpoint-onboarding-and-asr.mp4
quiz:
- q: What does the Intune connector to Microsoft Defender for Endpoint primarily enable?
  options:
  - It installs antivirus signatures
  - It establishes trust so MDE can share device risk with Intune and Intune can onboard/deploy EDR policy
  - It replaces Conditional Access
  - It encrypts the disk
  answer: 1
  why: The connector creates the service-to-service trust that lets Intune onboard devices to MDE and
    lets MDE report each device's risk level back to Intune for compliance evaluation.
- q: Why deploy ASR rules in audit mode before block mode?
  options:
  - Audit mode is required by licensing
  - Audit mode logs what would be blocked so you can find false positives before enforcing
  - Block mode does not generate any telemetry
  - Audit mode is faster to deploy
  answer: 1
  why: Audit mode records the events a rule would have blocked without actually blocking them, letting
    you discover legitimate business apps that would break and add exclusions before flipping to block.
- q: Which ASR rule specifically protects against credential theft tooling like Mimikatz reading the LSASS
    process?
  options:
  - Block executable content from email client and webmail
  - Block credential stealing from the Windows local security authority subsystem (lsass.exe)
  - Block Office applications from creating child processes
  - Use advanced protection against ransomware
  answer: 1
  why: The 'Block credential stealing from lsass.exe' rule (GUID 9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2)
    stops tools from dumping credentials out of the Local Security Authority Subsystem Service.
- q: What does Controlled Folder Access protect against?
  options:
  - Phishing emails
  - Ransomware modifying files in protected folders by only allowing trusted apps to write
  - Weak passwords
  - Outdated firmware
  answer: 1
  why: Controlled Folder Access guards designated folders so only trusted/allowed applications can modify
    their contents, blocking ransomware-style mass file encryption.
- q: Tamper protection in MDE primarily prevents what?
  options:
  - Users running Office macros
  - Malware or local admins from disabling Defender features such as real-time protection
  - Devices from enrolling in Intune
  - BitLocker from being enabled
  answer: 1
  why: Tamper protection locks critical Defender settings (real-time protection, cloud-delivered protection,
    security intelligence updates) so they cannot be turned off by malware, scripts, or even local administrators.
- q: In 2-4 sentences, outline a safe production rollout plan for a new ASR rule across a 5,000-device
    fleet.
  answer: Start by deploying the rule in audit mode to a small pilot ring and review the ASR audit events
    and the attack surface reduction report for legitimate apps that would be blocked. Add per-path or
    per-publisher exclusions for confirmed false positives, then expand audit to the full fleet for a
    week or two. Once telemetry is clean, flip the rule to block for the pilot ring, validate, and progressively
    roll block mode out ring by ring while monitoring the Action center and user reports.
resources:
- label: Onboard Windows devices to Defender for Endpoint using Intune
  url: https://learn.microsoft.com/en-us/defender-endpoint/configure-endpoints-mdm
- label: Attack surface reduction rules reference
  url: https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference
- label: Enable attack surface reduction rules
  url: https://learn.microsoft.com/en-us/defender-endpoint/enable-attack-surface-reduction
- label: Protect security settings with tamper protection
  url: https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection
---

## MDE architecture in one picture

Microsoft Defender for Endpoint is a cloud service plus a sensor that is already built into Windows. The endpoint sensor streams behavioral telemetry to the **Microsoft Defender portal** (security.microsoft.com), where detections, the device inventory, vulnerability data, and automated investigation all live. There is no separate agent to install on modern Windows — you simply **onboard** the device (register its sensor with your tenant) and configure the antivirus/EDR engine. Onboarding plus the Intune connector is what makes a device both *protected* and *governable*.

## The Intune <-> MDE connector

First wire the two services together. In the **Microsoft Defender portal**: *Settings > Endpoints > Advanced features* and turn on **Microsoft Intune connection**. Then in the **Intune admin center**: *Endpoint security > Microsoft Defender for Endpoint* and confirm the connection status is *Available* with *Connect Windows devices...* set to **On**. This service-to-service trust does two jobs: it lets Intune onboard devices, and — crucially for Lesson 3 — it lets MDE report each device's **risk level** back to Intune so compliance can react to it.

## Onboarding through an Intune EDR policy

With the connector live, onboarding is a policy push. Go to **Endpoint security > Endpoint detection and response > Create policy** (platform Windows). Because the connector is on, Intune fills in the onboarding blob automatically; set *Sample sharing* and *Expedite telemetry reporting frequency* as desired, then assign to your device group. Confirm success two ways:

```powershell
# On an onboarded device, sense service should be running
Get-Service -Name Sense | Select-Object Name, Status, StartType

# Quick MDE protection state
Get-MpComputerStatus | Select-Object AMRunningMode, RealTimeProtectionEnabled, IsTamperProtected
```

Within ~10-15 minutes the device appears under *Assets > Devices* in the Defender portal.

## Attack Surface Reduction: audit, tune, then block

ASR rules block the behaviors attackers rely on. The golden rule is **never deploy straight to block** — start in **Audit**, watch what *would* have been blocked, add exclusions, then enforce. Configure rules in Intune under *Endpoint security > Attack surface reduction > Create policy > Attack Surface Reduction Rules*. Real rules worth knowing:

- **Block credential stealing from lsass.exe** — `9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2` (stops Mimikatz-style credential dumping).
- **Block all Office applications from creating child processes** — `d4f940ab-401b-4efc-aadc-ad5f3c50688a`.
- **Block executable content from email client and webmail** — `be9ba2d9-53ea-4cdc-84e5-9b1eeee46550`.
- **Block process creations originating from PSExec and WMI commands** — `d1e49aac-8f56-4280-b9ba-993a6d77406c`.
- **Block Win32 API calls from Office macros** — `92e97fa1-2edf-4476-bdd6-9dd0b4dddc7b`.
- **Use advanced protection against ransomware** — `c1db55ab-c21a-4637-bb3f-a12568109d35`.

Each rule's per-setting state is *Not configured / Audit / Block / Warn*. You can manage ASR audit/block centrally; on an endpoint you can confirm with PowerShell:

```powershell
# 1 = Block, 2 = Audit, 6 = Warn, 0 = Not configured
(Get-MpPreference).AttackSurfaceReductionRules_Ids
(Get-MpPreference).AttackSurfaceReductionRules_Actions
```

Review hits in the Defender portal's **attack surface reduction report**, add `AttackSurfaceReductionOnlyExclusions` for confirmed false positives, then flip to Block ring by ring.

## Controlled folder access and network protection

Two more proactive controls live in the same ASR policy family:

- **Controlled folder access** — anti-ransomware: only trusted apps may write to protected folders (Documents, Desktop, etc.). Roll it out in audit first too, because line-of-business apps often need to be explicitly allowed.
- **Network protection** — extends SmartScreen to all processes, blocking outbound connections to malicious domains/IPs and phishing sites. Also start in audit, then set to Block.

## Tamper protection and exposure score

**Tamper protection** locks Defender's own settings — real-time protection, cloud-delivered protection, and signature updates — so malware, scripts, or even local admins cannot switch them off. Enable it tenant-wide in the Defender portal (*Settings > Endpoints > Advanced features*) and/or via an Intune Antivirus/Security Experience policy.

Finally, **Microsoft Defender Vulnerability Management** continuously assesses every onboarded device and produces an **exposure score** and a prioritized list of **security recommendations** (missing patches, weak configurations, risky software). A lower exposure score means a smaller attack surface; treat the top recommendations as your hardening backlog. Together, ASR plus a falling exposure score plus tamper protection give you a measurably harder fleet — and a reliable risk signal to feed the automated loop next.
