---
course: helpdesk-tier1-2
title: Endpoint security and Microsoft Defender
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 6
summary: Tour the Endpoint security node in Intune and learn how security baselines, Microsoft Defender
  Antivirus, firewall, BitLocker, and attack surface reduction rules harden a device. Then see how Microsoft
  Defender for Endpoint adds EDR and feeds device risk back into Intune compliance.
objectives:
- Navigate the Endpoint security node in the Microsoft Intune admin center
- Explain what a security baseline is and why it speeds up secure configuration
- Configure Microsoft Defender Antivirus, firewall, and BitLocker disk encryption policies
- Describe attack surface reduction (ASR) rules and what they block
- Explain the difference between antivirus (prevention) and EDR (detection and response)
- Connect Intune with Microsoft Defender for Endpoint so device risk drives compliance
video: hd5-l06-endpoint-security-and-defender.mp4
quiz:
- q: What is a security baseline in Intune?
  options:
  - A pre-configured set of recommended security settings you can deploy as a starting point
  - A backup of every device on the network
  - A report of failed login attempts
  - A list of blocked IP addresses
  answer: 0
  why: A security baseline is a Microsoft-recommended group of pre-configured settings (for Windows, Defender,
    Edge, and more) that gives you a hardened starting point instead of configuring hundreds of settings
    by hand.
- q: Which technology focuses on DETECTING and RESPONDING to threats that get past prevention, rather
    than just blocking known malware?
  options:
  - BitLocker
  - A firewall rule
  - Microsoft Defender for Endpoint (EDR)
  - An update ring
  answer: 2
  why: 'Microsoft Defender for Endpoint provides EDR (Endpoint Detection and Response): it watches behaviour,
    surfaces alerts and incidents, and lets you respond, going beyond antivirus prevention of known malware.'
- q: Where does an Endpoint Administrator review security alerts, incidents, and device risk levels?
  options:
  - The BIOS setup screen
  - The Microsoft Defender portal at security.microsoft.com
  - Windows Disk Management
  - The router admin page
  answer: 1
  why: The Microsoft Defender portal (security.microsoft.com) is where you triage alerts and incidents,
    see device risk, and run response actions for Defender for Endpoint.
- q: What do attack surface reduction (ASR) rules do?
  options:
  - Encrypt the system drive
  - Block common attack behaviours, such as Office apps spawning child processes or running untrusted
    scripts
  - Defragment the disk
  - Schedule Windows updates
  answer: 1
  why: ASR rules reduce the ways malware can get a foothold by blocking risky behaviours, like Office
    launching executables or running obfuscated scripts, that legitimate apps rarely need.
- q: In one sentence, what is the difference between Defender Antivirus and Defender for Endpoint?
  answer: Defender Antivirus prevents and removes known malware on the device, while Defender for Endpoint
    adds EDR, detecting suspicious behaviour, raising alerts and incidents, and enabling investigation
    and response across the fleet.
  why: Antivirus is prevention of known threats; EDR is detection, investigation, and response for the
    threats that evade prevention, and the two work together.
- q: Why would you connect Intune to Microsoft Defender for Endpoint?
  answer: So a device's Defender risk score flows into Intune, letting a compliance policy mark a high-risk
    device as non-compliant and trigger Conditional Access to block it until it is clean.
  why: The connection lets risk drive compliance and access decisions automatically, instead of an admin
    manually checking each device.
resources:
- label: Microsoft Learn — Manage endpoint security in Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/endpoint-security
- label: Microsoft Learn — Use security baselines to configure Windows devices in Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/security-baselines
- label: Microsoft Learn — Attack surface reduction rules overview
  url: https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction
- label: 'Microsoft — Exam MD-102: Microsoft 365 Endpoint Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
---

## The Endpoint security node

Inside the **Microsoft Intune admin center** there is a section built just for hardening devices: the **Endpoint security** node. This is where an Endpoint Administrator lives when the job is *security* rather than general configuration. From here you deploy **security baselines**, antivirus policy, firewall rules, disk encryption, and **attack surface reduction** rules, and you connect to Microsoft Defender.

```text
1. Go to https://intune.microsoft.com
2. Left menu -> Endpoint security
3. Browse the categories:
   - Security baselines
   - Antivirus
   - Disk encryption (BitLocker)
   - Firewall
   - Attack surface reduction
   - Endpoint detection and response
```

## Security baselines

There are hundreds of security settings in Windows. A **security baseline** is a Microsoft-recommended, pre-configured *group* of those settings, so instead of choosing each one by hand you deploy a hardened starting point and then tweak. Baselines exist for Windows, Microsoft Edge, and Defender for Endpoint. Deploy one to a pilot group first, review what it changes, then widen the rollout.

## Defender Antivirus, firewall and BitLocker

Three everyday protections you configure here:

- **Microsoft Defender Antivirus** — real-time protection, cloud-delivered protection, and scheduled scans. This is built into Windows; you are tuning policy, not installing software.
- **Firewall** — control inbound and outbound traffic per profile (domain, private, public).
- **Disk encryption (BitLocker)** — encrypt the system drive so a lost laptop does not leak data, with recovery keys escrowed to Entra ID.

These map directly to common Tier 2 tickets: "why is this site blocked", "where is my BitLocker recovery key", "why did a scan quarantine a file".

## Attack surface reduction

**Attack surface reduction (ASR)** rules block the *behaviours* attackers rely on, things legitimate software rarely needs. Examples: stopping Office apps from spawning child processes, blocking untrusted or unsigned scripts, and blocking credential theft from LSASS. You can run a rule in **audit** mode first to see what it *would* block before enforcing it, which avoids breaking a line-of-business app.

## Antivirus versus EDR

This distinction matters for the exam and the job. **Antivirus** is *prevention*: it stops and removes *known* malware. **Microsoft Defender for Endpoint** adds **EDR** — *Endpoint Detection and Response* — which watches device behaviour, raises **alerts** and groups them into **incidents**, and lets you investigate and respond (isolate a device, collect a forensic package). Prevention catches the known; EDR catches the sneaky and the new.

You review all of this in the **Microsoft Defender portal** at **security.microsoft.com**: the incident queue, device risk levels, and recommended actions.

## Connecting Intune and Defender for Endpoint

The two services are stronger together. When you wire up the **Microsoft Defender for Endpoint connector** in Intune, each device's **risk score** flows back into Intune. A **compliance policy** can then say "a device at high risk is non-compliant", and **Conditional Access** can block that device from company data until it is cleaned up, no manual checking required.

## Your task

Open **Endpoint security** in the Intune admin center. Open the **Security baselines** category and note which baselines are available. Then open **Attack surface reduction** and write down two ASR rules and, in your own words, what behaviour each one blocks.
