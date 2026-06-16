---
course: helpdesk-tier3-advanced
title: Zero Trust architecture for endpoints
month: 3
monthTitle: Advanced Endpoint Security & Identity
lesson: 1
summary: Apply the Zero Trust model to endpoints, treating device identity, health and signal as first-class
  inputs to every access decision. You will map the Microsoft Zero Trust pillars to concrete endpoint
  controls you can deploy today.
objectives:
- Explain the three Zero Trust principles and why implicit trust by network location is obsolete
- 'Map the Zero Trust pillars to endpoint controls: identity, device, app, data, network'
- Describe how device compliance state becomes a signal in an access decision
- Differentiate authentication, authorization and continuous access evaluation at the endpoint
- Design a high-level Zero Trust enforcement flow for a managed Windows device
- Identify the telemetry sources that feed endpoint trust decisions
video: ht3-l01-zero-trust-for-endpoints.mp4
quiz:
- q: Which statement best captures the core assumption of Zero Trust?
  options:
  - Devices inside the corporate network are trusted by default
  - Assume breach and verify every request explicitly regardless of network location
  - VPN-connected devices need no further checks
  - Trust is granted once at logon and never re-evaluated
  answer: 1
  why: Zero Trust replaces the perimeter model with explicit, per-request verification under an assume-breach
    posture, so network location alone never confers trust.
- q: In a Zero Trust access decision for an endpoint, which is treated as a primary signal alongside user
    identity?
  options:
  - The device's compliance and health state
  - The colour of the desktop wallpaper
  - The number of installed fonts
  - The screen resolution
  answer: 0
  why: Device compliance and health (managed, encrypted, patched, not flagged by EDR) are first-class
    signals that Conditional Access and the access broker evaluate before granting access.
- q: What does the principle of 'least privilege' add to endpoint Zero Trust?
  options:
  - It grants admin rights to all users for convenience
  - It limits access with just-in-time and just-enough-access and risk-based adaptive policies
  - It disables all auditing to reduce noise
  - It removes the need for MFA
  answer: 1
  why: Least privilege means scoping access tightly using JIT/JEA and adaptive, risk-based policies so
    a compromised endpoint or account has minimal blast radius.
- q: Why is Continuous Access Evaluation (CAE) important in a Zero Trust endpoint design?
  options:
  - It caches tokens forever to improve speed
  - It lets revocation and risk changes take effect near real time instead of waiting for token expiry
  - It disables Conditional Access
  - It replaces the need for device compliance
  answer: 1
  why: CAE allows critical events such as account disable, password reset or elevated risk to revoke access
    in near real time rather than waiting up to an hour for token lifetime to lapse.
- q: Name the five core Microsoft Zero Trust pillars that an endpoint design touches.
  answer: Identity, Devices (endpoints), Applications, Data, and Network (with Infrastructure often added
    as a sixth).
  why: Microsoft's Zero Trust model spans Identity, Endpoints/Devices, Apps, Data, Network and Infrastructure;
    an endpoint strategy must consider how the device interacts with each.
- q: In one sentence, explain why 'assume breach' changes how you design endpoint controls.
  answer: Because you design as though an attacker is already present, you segment access, verify continuously,
    encrypt data and minimise privilege so a single compromised endpoint cannot move laterally or exfiltrate
    freely.
  why: Assume breach shifts focus from keeping attackers out to limiting damage, driving micro-segmentation,
    least privilege, encryption and rich telemetry on every endpoint.
resources:
- label: Microsoft Learn — Zero Trust security model overview
  url: https://learn.microsoft.com/en-us/security/zero-trust/zero-trust-overview
- label: Microsoft Learn — Secure endpoints with Zero Trust
  url: https://learn.microsoft.com/en-us/security/zero-trust/deploy/endpoints
- label: Microsoft Learn — Continuous access evaluation
  url: https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation
- label: Microsoft Learn — Zero Trust deployment for technology pillars
  url: https://learn.microsoft.com/en-us/security/zero-trust/deploy/overview
---

## The perimeter is gone

For decades security assumed a hard shell and a soft centre: get past the firewall or onto the VPN, and you were trusted. Cloud apps, remote work and BYOD destroyed that model. **Zero Trust** replaces it with three principles: **verify explicitly**, use **least-privilege access**, and **assume breach**. Network location is no longer a trust signal. Every request — including from a device sitting in your own office — must be authenticated, authorized and validated against current signals.

For an endpoint engineer this is a mindset shift. The device stops being a passive client and becomes an active participant whose **health and compliance state** feed directly into whether access is granted.

## The pillars and how endpoints touch each

Microsoft's Zero Trust model spans **Identity, Devices, Applications, Data, Network** and Infrastructure. An endpoint sits at the intersection:

- **Identity** — the user and the device both have identities (the device identity comes from Entra join or hybrid join).
- **Devices** — compliance policy decides if the endpoint is healthy: encrypted, patched, EDR-onboarded, not jailbroken.
- **Applications** — app protection policies and managed app access.
- **Data** — encryption at rest (BitLocker) and labelling/DLP in transit.
- **Network** — segmentation so a compromised endpoint cannot roam.

## Compliance state as a signal

The heart of endpoint Zero Trust is that **device compliance becomes an input to authorization**. Intune evaluates a device against policy and stamps it compliant or non-compliant. **Conditional Access** then consumes that state. A simplified decision flow looks like this:

```text
User + device request access to resource
  -> Authenticate user (MFA / passwordless)
  -> Evaluate signals: user risk, sign-in risk, device compliance, location, app
  -> Decision: Grant / Grant with controls / Block
  -> Continuously re-evaluate (CAE) for revocation & risk change
```

Notice authorization is **not** a one-time gate. With **Continuous Access Evaluation (CAE)** a disabled account, a password reset or a sudden risk spike can revoke a live session in near real time, instead of waiting for a token to expire.

## Least privilege at the endpoint

Assume breach means scoping access tightly. On the endpoint that translates to removing standing local-admin rights, using **just-in-time** elevation, and applying **just-enough-access**. You can confirm a user is not a standing admin:

```powershell
# List members of the local Administrators group
Get-LocalGroupMember -Group 'Administrators' |
  Select-Object Name, PrincipalSource, ObjectClass
```

Every account that does not strictly need elevation is removed. A compromised standard user is far less useful to an attacker than a compromised admin.

## Telemetry feeds the decision

Zero Trust only works if the signals are trustworthy and current. Endpoint telemetry — sign-in logs, **Defender for Endpoint** alerts, Intune compliance, and device risk scores — flows into the policy engine. The richer and fresher the signal, the better the decision. This is why EDR onboarding and compliance reporting are not optional extras; they are the sensory system of your access control.

## Your task

For one managed Windows device in a test tenant, document its full Zero Trust posture: device join type, compliance policy result, BitLocker and EDR onboarding state, and the local Administrators membership. Then draw the access-decision flow for that device reaching a sensitive app, naming every signal Conditional Access would evaluate and where CAE would intervene on a revocation event.
