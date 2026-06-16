---
course: helpdesk-tier3-advanced
title: EDR and endpoint incident response
month: 3
monthTitle: Advanced Endpoint Security & Identity
lesson: 4
summary: Move beyond signature antivirus to behaviour-based EDR, and run a disciplined endpoint incident
  through the full NIST response lifecycle. You will triage alerts, isolate devices, preserve evidence
  and drive a containment-to-recovery workflow.
objectives:
- Contrast traditional signature antivirus with behaviour-based EDR and explain why telemetry and detections
  matter
- Walk an endpoint incident through the six NIST SP 800-61 phases from preparation to lessons learned
- Triage Defender for Endpoint alerts and incidents and pivot on indicators of compromise
- Choose between full and selective device isolation and collect an investigation package
- Use a live response session to gather artefacts and remediate while preserving evidence
- Explain Automated Investigation and Response and how chain of custody is maintained
video: ht3-l04-edr-and-incident-response.mp4
quiz:
- q: What is the fundamental difference between traditional signature antivirus and EDR?
  options:
  - EDR only scans files on a fixed schedule while AV runs continuously
  - EDR continuously records endpoint behaviour and detects suspicious activity, not just known file signatures
  - EDR replaces the need for any operating system patching
  - AV stores full process telemetry centrally while EDR does not
  answer: 1
  why: Signature AV matches files against a database of known bad hashes; EDR continuously collects process,
    network and behavioural telemetry and detects anomalous activity, enabling detection of novel and
    fileless attacks plus investigation and response.
- q: In the NIST SP 800-61 incident response lifecycle, which phase directly follows Containment?
  options:
  - Preparation
  - Detection and Analysis
  - Eradication
  - Post-Incident Activity
  answer: 2
  why: NIST orders the lifecycle as Preparation, Detection and Analysis, then Containment, Eradication
    and Recovery (often grouped), followed by Post-Incident Activity. Eradication removes the threat after
    the bleeding is stopped by containment.
- q: When should you choose selective isolation rather than full isolation of a device in Defender for
    Endpoint?
  options:
  - When you want to cut all network connectivity including the Defender connection
  - When you need to block the device's apps from the network while keeping the Defender for Endpoint
    connection for investigation
  - When the device is already offline
  - When you want to permanently remove the device from the tenant
  answer: 1
  why: Selective isolation restricts a limited set of processes or apps from network access while preserving
    the Defender for Endpoint service connection so analysts can keep investigating and running live response;
    full isolation cuts almost all connectivity except the Defender channel.
- q: What is the primary purpose of collecting an investigation package from a compromised endpoint?
  options:
  - To capture forensic artefacts such as autoruns, processes, network connections and event logs for
    analysis and evidence
  - To reinstall the operating system remotely
  - To deploy a new antivirus signature
  - To reset the user's password
  answer: 0
  why: The investigation package bundles forensic artefacts (autoruns, installed programs, network connections,
    prefetch, scheduled tasks, security event logs and more) so analysts can examine the device's state
    and preserve evidence without working live on the machine.
- q: List the six phases of the NIST SP 800-61 incident response lifecycle in order.
  answer: Preparation; Detection and Analysis; Containment; Eradication; Recovery; Post-Incident Activity
    (lessons learned). NIST groups Containment, Eradication and Recovery into one major phase, but they
    are distinct steps.
  why: 'Knowing the ordered lifecycle keeps responders disciplined: prepare first, detect and confirm,
    contain to stop spread, eradicate the threat, recover to normal operations, then learn so the next
    incident is handled faster.'
- q: In one sentence, explain why chain of custody matters when handling endpoint evidence.
  answer: Chain of custody documents who collected, accessed and transferred each artefact and when, so
    the evidence stays trustworthy and admissible and any tampering would be detectable.
  why: Without a documented, unbroken chain of custody, forensic artefacts can be challenged as altered
    or unreliable, undermining legal action, insurance claims and the credibility of the investigation's
    conclusions.
resources:
- label: Microsoft Learn — Investigate incidents in Microsoft Defender for Endpoint
  url: https://learn.microsoft.com/en-us/defender-endpoint/investigate-incidents
- label: Microsoft Learn — Take response actions on a device (isolation, investigation package)
  url: https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts
- label: Microsoft Learn — Investigate entities on devices using live response
  url: https://learn.microsoft.com/en-us/defender-endpoint/live-response
- label: NIST SP 800-61 Rev. 2 — Computer Security Incident Handling Guide
  url: https://csrc.nist.gov/pubs/sp/800/61/r2/final
---

## From signatures to behaviour

Traditional **antivirus** answers one question: does this file match a known-bad signature? That works for commodity malware but fails against fileless attacks, living-off-the-land techniques and novel payloads that have no signature yet. **Endpoint Detection and Response (EDR)** changes the question. An EDR agent continuously records endpoint behaviour — process creation, command lines, network connections, registry and file changes — and ships that telemetry to a cloud analytics engine. Detections fire on *behaviour*, not just file hashes, so an attacker abusing `powershell.exe` to download a payload is caught even when the file itself looks clean.

For an endpoint engineer the practical shift is this: the device is now a sensor, and your job is to triage what it reports and respond fast.

## The NIST incident response lifecycle

Discipline beats heroics. **NIST SP 800-61** defines a repeatable lifecycle that keeps responders calm and consistent:

```text
1. Preparation          build tooling, runbooks, contacts, baselines
2. Detection & Analysis confirm it is real, scope the blast radius
3. Containment          stop the spread (short-term + long-term)
4. Eradication          remove malware, accounts, persistence
5. Recovery             restore to known-good, monitor closely
6. Post-Incident        lessons learned, improve the runbook
```

NIST groups containment, eradication and recovery into one major phase, but treat them as distinct steps. The loop is iterative: lessons learned feed straight back into preparation.

## Triage and indicators of compromise

In **Defender for Endpoint**, related alerts are correlated into an **incident**. Start there, not at individual alerts. Read the attack story, identify the impacted assets, and pivot on **indicators of compromise (IOCs)** — file hashes, IP addresses, domains, registry keys. Hunt across the estate to find every device touched by the same IOC. A focused KQL query in advanced hunting confirms scope quickly:

```kql
DeviceProcessEvents
| where Timestamp > ago(24h)
| where SHA256 == "<suspect-hash>"
   or InitiatingProcessCommandLine has "Invoke-WebRequest"
| project Timestamp, DeviceName, AccountName, FileName, ProcessCommandLine
| order by Timestamp asc
```

Scope before you act: you cannot contain what you have not found.

## Containment: isolation and the investigation package

Defender gives you two **device isolation** modes. **Full isolation** cuts almost all connectivity, leaving only the Defender for Endpoint channel so you keep control. **Selective isolation** blocks a limited set of apps from the network while preserving more of the device — useful when you need the user partly working or want a lighter touch. Before you change anything, **collect the investigation package**: a bundle of autoruns, processes, network connections, scheduled tasks, prefetch and security event logs that preserves the device state as evidence.

## Live response and AIR

A **live response** session is a remote command shell into the isolated device for investigation and surgical remediation — all while the device stays contained.

```powershell
# Inside a live response session
getfile C:\Users\Public\suspicious.exe   # pull artefact to evidence store
processes                                # list running processes
connections                              # active network connections
remediate file C:\Users\Public\suspicious.exe
```

**Automated Investigation and Response (AIR)** can do much of this for you: when an alert fires, AIR investigates the alert tree, determines verdicts and applies approved remediation automatically, shrinking response time from hours to minutes. Always preserve **chain of custody** — record who collected each artefact, when, and where it is stored — so evidence stays trustworthy.

## Your task

In a test tenant, simulate a benign detection on one onboarded device. Walk it through the full lifecycle: triage the incident and note the IOCs, run an advanced hunting query to scope which devices share an IOC, collect the investigation package, place the device in selective isolation, open a live response session and pull one artefact to an evidence store, then write a one-page runbook entry documenting your containment decision, the chain of custody for that artefact, and the recovery and communication steps you would take.
