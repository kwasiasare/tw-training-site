---
course: cloud-security-engineer
title: Risk-Based Automated Device Isolation
month: 2
monthTitle: Modern Endpoint Security & Threat Protection
lesson: 3
summary: 'This is the heart of Project 1: a fully closed, human-free containment loop. You will connect
  three controls so they react to each other automatically. Microsoft Defender for Endpoint detects malicious
  activity and raises a device''s machine risk level; an Intune compliance policy that requires the threat
  level to be at most Medium then flips that device to noncompliant; and a Conditional Access policy requiring
  a compliant device immediately blocks the device from Exchange Online, SharePoint, and SaaS apps. You
  will configure every link, then layer on MDE''s manual and automated device isolation and ''restrict
  app execution'' actions for deeper containment.'
objectives:
- Trace the end-to-end risk-based isolation loop from MDE detection to Conditional Access block.
- Configure the Intune compliance rule that maps the MDE machine risk level to a noncompliant state.
- Build the Conditional Access policy that enforces 'require compliant device' on the right apps.
- Tune the loop's timing so containment happens in seconds without human intervention.
- Trigger and reverse MDE device isolation and 'restrict app execution' actions.
- Validate the whole loop with a controlled test detection and document the evidence for a portfolio.
video: cse-m2-l03-risk-based-automated-device-isolation.mp4
quiz:
- q: In the automated isolation loop, what is the correct order of cause and effect?
  options:
  - Conditional Access blocks -> Intune marks noncompliant -> MDE detects
  - MDE raises machine risk -> Intune marks device noncompliant -> Conditional Access blocks access
  - Intune detects malware -> MDE blocks -> Conditional Access notifies
  - Conditional Access raises risk -> MDE isolates -> Intune reports
  answer: 1
  why: Defender for Endpoint detects and raises the machine risk level, Intune's compliance policy flips
    the device to noncompliant based on that risk, and Conditional Access then denies access because the
    device is no longer compliant.
- q: Which exact Intune compliance setting is the linchpin that connects MDE risk to compliance?
  options:
  - Require BitLocker
  - Require the device to be at or under the machine risk score
  - Minimum OS version
  - Require firewall
  answer: 1
  why: Setting 'Require the device to be at or under the machine risk score' to a threshold like Medium
    means a High-risk device reported by MDE automatically fails compliance.
- q: If you set the compliance threshold to 'Clear', what is the practical effect?
  options:
  - Only devices with no risk detections at all stay compliant; even Low risk fails
  - All devices are always compliant
  - Only High-risk devices fail
  - The setting is ignored
  answer: 0
  why: '''Clear'' is the strictest threshold: any nonzero risk level (Low, Medium, or High) makes the
    device noncompliant, so it should be used carefully to avoid blocking users on benign low-severity
    signals.'
- q: What does the MDE 'Isolate device' action do that the Conditional Access block does not?
  options:
  - Nothing different
  - It cuts the device off from network communication at the OS level while keeping the MDE connection
    for investigation
  - It deletes the device from Entra ID
  - It only sends an email
  answer: 1
  why: Device isolation severs the machine's network connectivity at the endpoint (except its link to
    the Defender service), containing lateral movement, whereas the Conditional Access block only denies
    access to cloud apps.
- q: Why is this loop considered 'containment in seconds without human intervention'?
  options:
  - Because an analyst must approve each step quickly
  - Because the three controls react to each other automatically via shared signals, with no ticket or
    manual action required
  - Because it only works during business hours
  - Because it disables the network card permanently
  answer: 1
  why: 'Each control consumes the previous control''s signal automatically: detection raises risk, risk
    fails compliance, noncompliance triggers the access block, all without a human in the loop.'
- q: In 2-4 sentences, describe how you would safely test this isolation loop end-to-end without using
    live malware.
  answer: Use a controlled, sanctioned test such as the EICAR antivirus test file or a Microsoft-provided
    MDE evaluation/simulation to trigger a detection on a dedicated pilot device. Watch the device's risk
    level rise in the Defender portal, confirm Intune flips it to noncompliant, and then attempt to reach
    Exchange Online or SharePoint to verify Conditional Access blocks it. Capture screenshots and timestamps
    at each stage as portfolio evidence, then resolve the alert and confirm the device returns to compliant
    and regains access.
resources:
- label: Enforce compliance for Defender for Endpoint with Conditional Access
  url: https://learn.microsoft.com/en-us/mem/intune/protect/advanced-threat-protection
- label: Take response actions on a device in Defender for Endpoint
  url: https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts
- label: 'Conditional Access: Require compliant device'
  url: https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-grant
- label: Device compliance policy settings for Windows
  url: https://learn.microsoft.com/en-us/mem/intune/protect/compliance-policy-create-windows
---

## The closed loop, end to end

Project 1's centerpiece is a containment loop with **no human in it**. Three controls you already met now talk to each other:

1. **Microsoft Defender for Endpoint** sees malicious behavior on a device and raises its **machine risk level** (Low -> Medium -> High).
2. **Intune compliance** has a rule: *require the device to be at or under the machine risk score = Medium*. A High-risk device instantly fails and is stamped **noncompliant** in Entra ID.
3. **Conditional Access** has a policy: *require device to be marked compliant*. The moment the device is noncompliant, sign-in to Exchange Online, SharePoint, Teams, and SaaS apps is **blocked**.

Detection to lockout takes seconds, and nobody opened a ticket. Your job in this lesson is to build and prove each link.

## Link 1: MDE produces the risk signal

This is already running from Lesson 2 — onboarded devices report risk, and the Intune connector carries that risk into Intune. Confirm the connector is **Available** (Intune > *Endpoint security > Microsoft Defender for Endpoint*) and that *Connect Windows devices...* is **On**. Without this trust, the risk level never reaches compliance and the loop is dead.

## Link 2: compliance converts risk into a state

Edit (or create) your Windows compliance policy and set the **Microsoft Defender for Endpoint** rule:

```text
Require the device to be at or under the machine risk score:  Medium
```

Threshold meanings:

- **Clear** — strictest; any detection (Low+) makes the device noncompliant.
- **Low** — Low is tolerated; Medium/High fail.
- **Medium** — Low/Medium tolerated; only **High** fails. A common production balance.
- **High** — most permissive; only the very worst flips the device.

Set the *Actions for noncompliance* schedule to **0 days** so the state flips immediately — a grace period here would defeat the purpose.

## Link 3: Conditional Access enforces the block

In Entra, *Protection > Conditional Access > New policy*:

- **Users**: your target population (exclude a break-glass account).
- **Target resources**: Office 365 (Exchange, SharePoint, Teams) and your SaaS apps.
- **Grant**: *Require device to be marked as compliant*.
- Enable in **Report-only** first, confirm in the *Conditional Access Insights* workbook, then set to **On**.

Now the loop is wired: risk -> noncompliant -> blocked.

## Tuning the timing

'Seconds' depends on a few knobs. MDE raises risk almost immediately on detection. Intune re-evaluates compliance on a sync, so the device check-in cadence matters; the noncompliance schedule should be **0 days**. Conditional Access evaluates at sign-in and via **Continuous Access Evaluation (CAE)**, which can revoke active sessions in near real time rather than waiting for token expiry. The net effect is containment that feels instantaneous to the attacker and invisible to your SOC queue.

## Deeper containment: isolate and restrict app execution

Conditional Access blocks *cloud* access, but a compromised device can still attack the *local network*. For that, use MDE response actions from the device page in the Defender portal (or via the API/automation):

- **Isolate device** — cuts the machine off from all network communication except its link back to the Defender service, stopping lateral movement while you investigate. Choose *Full* or *Selective* isolation.
- **Restrict app execution** — applies a code-integrity policy so only Microsoft-signed processes can run, neutering most malware without fully isolating the device.
- **Run antivirus scan**, **Collect investigation package**, and **Initiate automated investigation** for follow-up.

Both isolation and restriction are reversible with one click (*Release from isolation* / *Remove app restriction*) once the threat is handled. These can be triggered manually, by automation in Defender XDR (next lesson), or by your own Logic App / Graph automation (Module 5).

## Validate and capture evidence

Prove it safely. On a dedicated pilot device, trigger a benign detection (e.g., the **EICAR** test string or a Microsoft MDE simulation). Then watch the chain:

```powershell
# Generates a harmless EICAR detection to exercise the pipeline
$e = 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
Set-Content -Path "$env:TEMP\\eicar.com" -Value $e
```

Confirm: device risk rises in the Defender portal -> device shows **noncompliant** in Intune -> a browser sign-in to Outlook/SharePoint is blocked by Conditional Access. Screenshot each stage with timestamps. Resolve the alert, confirm the device returns to **compliant**, and verify access is restored. That documented round trip is the deliverable for Project 1.
