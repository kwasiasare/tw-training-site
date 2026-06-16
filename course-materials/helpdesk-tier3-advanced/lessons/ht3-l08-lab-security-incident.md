---
course: helpdesk-tier3-advanced
title: 'Lab: handling a security incident end to end'
month: 3
monthTitle: Advanced Endpoint Security & Identity
lesson: 8
summary: 'Work a realistic incident from first alert to lessons learned: a phishing-driven credential
  theft and suspicious PowerShell on a managed endpoint. You will triage in Defender XDR, scope with advanced
  hunting, contain, eradicate, recover and harden, integrating everything from this month.'
objectives:
- Triage a multi-stage Defender XDR incident by correlating identity and endpoint alerts into one timeline
- Scope the blast radius with an advanced hunting KQL query joining sign-in and device process telemetry
- Contain the threat by isolating the device, revoking sessions and disabling the account, leaning on
  Conditional Access and CAE
- Eradicate persistence and rotate credentials and secrets the attacker may have touched
- Recover the endpoint and user safely while verifying BitLocker and compliance state
- Run a post-incident review and close the root-cause gap with a new Conditional Access policy or ASR
  rule
video: ht3-l08-lab-security-incident.mp4
quiz:
- q: A Defender XDR incident links a risky sign-in from an impossible-travel location to a 'Suspicious
    PowerShell download' alert on a managed laptop. What is the single best first action during triage?
  options:
  - Open the incident, read the correlated alert story and build a timeline before acting
  - Immediately re-image the laptop before looking at anything else
  - Email the user to ask if they ran PowerShell
  - Delete the user's mailbox to stop data loss
  answer: 0
  why: Defender XDR already correlates identity and endpoint alerts into one incident with an attack story;
    reading that timeline first prevents premature, destructive actions and tells you exactly what to
    contain. Re-imaging or deleting data first destroys evidence and may not even address the root cause.
- q: You want to scope how far the compromised account spread. Which advanced hunting approach is most
    effective?
  options:
  - Search only DeviceProcessEvents on the one known device
  - Join identity sign-in events with device process and network events across the tenant by account and
    time window
  - Query AlertInfo alone and trust the alert count
  - Run a full antivirus scan and read the log
  answer: 1
  why: Scoping means following the account and indicators across all telemetry. Joining sign-in logs (AADSignInEventsBeta
    / SigninLogs) with DeviceProcessEvents and DeviceNetworkEvents by the compromised UPN and time window
    reveals other devices, IPs and processes the attacker touched — far more than a single-device or single-table
    query.
- q: During containment you isolate the device in Defender for Endpoint and disable the account in Entra.
    Why also explicitly revoke the user's sessions?
  options:
  - Disabling an account instantly kills all existing tokens everywhere
  - Session revocation re-images the device
  - Existing access and refresh tokens can remain valid until expiry unless revoked; revocation plus CAE
    forces re-auth in near real time
  - Revoking sessions restores the deleted files
  answer: 2
  why: Disabling the account stops new sign-ins, but already-issued tokens may stay valid up to their
    lifetime. Revoking sessions invalidates refresh tokens, and Continuous Access Evaluation propagates
    the change to resources in near real time, closing the window an attacker could keep using a live
    session.
- q: After eradication you are ready to recover. Which check confirms the endpoint is safe to release
    from isolation and return to the user?
  options:
  - The user says the laptop 'feels fine'
  - The device pings the gateway
  - The antivirus definitions are up to date
  - No active EDR detections, persistence removed, credentials rotated, and the device reports compliant
    and BitLocker-protected
  answer: 3
  why: 'Recovery is gated on verified clean state: no live detections, removed persistence, rotated secrets,
    and a confirmed compliant, encrypted device. Subjective impressions or a single signal like AV definitions
    are not sufficient evidence that the threat is gone.'
- q: In your own words, why is correlating the identity signal (risky sign-in) with the endpoint signal
    (suspicious process) more powerful than treating each alert alone?
  answer: Alone, a risky sign-in might look like a false positive and a suspicious process might look
    like benign admin activity; correlated, they form a clear attack story — stolen credentials being
    used to run malicious code on a real device — which raises confidence, defines scope, and tells you
    to contain both the identity and the endpoint together.
  why: XDR's value is breadth across domains. Correlation turns two ambiguous low-confidence signals into
    one high-confidence incident, drives the right containment on both the account and the device, and
    reveals lateral movement a single-domain view would miss.
- q: Name one root-cause hardening control you would add in the post-incident review for a phishing-to-token-theft
    incident, and say which principle it enforces.
  answer: Add a Conditional Access policy requiring phishing-resistant MFA and a compliant device for
    the affected app, optionally with token protection / sign-in frequency; this enforces 'verify explicitly'
    and least privilege so stolen passwords alone cannot grant access. An ASR rule blocking script-launched
    executables or credential theft from LSASS is an equally valid endpoint-side answer.
  why: Post-incident hardening must close the gap the attacker used. Phishing-resistant MFA plus device
    compliance defeats password-only and many token-replay attacks, while ASR rules cut off the script-based
    execution chain — both directly map to Zero Trust principles taught this month.
resources:
- label: Microsoft Learn — Investigate incidents in Microsoft Defender XDR
  url: https://learn.microsoft.com/en-us/defender-xdr/investigate-incidents
- label: Microsoft Learn — Proactively hunt for threats with advanced hunting
  url: https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-overview
- label: Microsoft Learn — Take response actions on a device (including isolate device)
  url: https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts
- label: NIST SP 800-61 Rev. 2 — Computer Security Incident Handling Guide
  url: https://csrc.nist.gov/pubs/sp/800/61/r2/final
---

## The scenario

It is 09:14 on a Tuesday. A **Defender XDR** incident lights up your queue, severity High, correlating two alerts: a **risky sign-in** for `j.okafor@contoso.com` from an unfamiliar IP flagged *impossible travel*, and a *Suspicious PowerShell download activity* alert on her managed laptop `LT-OKAFOR-01`. The attack story writes itself: a **phishing** email harvested her credentials, the attacker signed in, and a **LOLBin** PowerShell one-liner pulled a payload onto the endpoint. This is your capstone — you will run the full **IR lifecycle** (NIST SP 800-61: *prepare, detect & analyse, contain, eradicate & recover, post-incident*) using every control from this month.

## Detect and analyse: read the story, then scope

Open the incident and read the correlated timeline **before touching anything**. XDR has already joined the identity and endpoint signals for you — confirm the **IOC**s: the source IP, the spawned process, any outbound C2 domain. Then scope the blast radius with **advanced hunting**. Do not trust a single device or single table; follow the account across the tenant:

```kql
let target = "j.okafor@contoso.com";
let window = 24h;
AADSignInEventsBeta
| where Timestamp > ago(window) and AccountUpn == target
| where RiskLevelDuringSignIn in ("high", "medium")
| project Timestamp, IPAddress, Country, DeviceName, Application
| join kind=leftouter (
    DeviceProcessEvents
    | where Timestamp > ago(window)
    | where InitiatingProcessFileName in~ ("powershell.exe", "cmd.exe", "mshta.exe")
    | where ProcessCommandLine has_any ("DownloadString", "-enc", "Invoke-WebRequest")
    | project Timestamp, DeviceName, AccountName, ProcessCommandLine, RemoteUrl=InitiatingProcessRemoteSessionDeviceName
) on DeviceName
| order by Timestamp asc
```

This tells you which **devices**, IPs and processes the one compromised identity touched — your true scope.

## Contain: cut access on both the identity and the endpoint

Containment is two-sided because this is an XDR incident. On the **endpoint**, isolate the device so it keeps its EDR link but loses everything else:

```powershell
# From a SOC workstation using the Defender for Endpoint API / portal action:
# 1) Device > Isolate device (Full)  -> severs network, keeps Defender comms
# 2) Identity side, in Entra / Graph PowerShell:
Update-MgUser -UserId "j.okafor@contoso.com" -AccountEnabled:$false
Revoke-MgUserSignInSession -UserId "j.okafor@contoso.com"
```

Disabling the account stops new sign-ins; **revoking sessions** invalidates refresh tokens; and because **Continuous Access Evaluation (CAE)** is on, those revocations propagate to resources in near real time rather than waiting for token expiry. Your existing **Conditional Access** posture is what made the device isolatable and the account governable in the first place.

## Eradicate and recover

**Eradicate** the foothold: remove the dropped payload and any **persistence** (scheduled task, Run key, new service), then rotate everything the attacker may have seen — reset the user's password, rotate any app secrets or keys cached on the device, and review **PKI** certificates that may need revoking. **Recover** only on verified-clean evidence: no live EDR detections, persistence gone, and the device reporting **compliant** with **BitLocker** protection healthy. Then release the device from isolation, re-enable the account behind a fresh **MFA** challenge, and restore access.

## Post-incident: close the gap

The incident is not over until the **root cause** is fixed. The attacker won with a phished password and password-only access. So harden: add a **Conditional Access** policy requiring **phishing-resistant MFA** and a compliant device for sensitive apps, and add an **ASR rule** to block script-launched executables. Write up the timeline, the dwell time, and what detection or control would have caught it sooner.

## Your task

In a test tenant, simulate this incident end to end. (1) Generate or locate a risky sign-in plus a suspicious PowerShell event so a correlated XDR incident appears. (2) Triage it and write a one-page timeline of the attack story. (3) Run an advanced hunting query (adapt the KQL above) to scope which devices and accounts were affected, and paste the results. (4) Contain: isolate the device, disable the account and revoke sessions, noting how CAE behaves. (5) Eradicate and recover: remove persistence, rotate the password, verify compliance and BitLocker, then release isolation. (6) Deliver a post-incident report naming one new Conditional Access policy AND one ASR rule you would deploy, and which Zero Trust principle each enforces.
