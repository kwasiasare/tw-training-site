---
course: cloud-security-engineer
title: 'Capstone: Automated Zero-Trust Endpoint Isolation System'
month: 6
monthTitle: Capstone Projects & Career Launch
lesson: 1
summary: This capstone wires three Microsoft security services into a single closed-loop control that
  contains a compromised endpoint in seconds, with no human in the path. When Defender for Endpoint raises
  a device's risk to High, an Intune compliance policy flips the device to noncompliant, and a Conditional
  Access policy that requires a compliant device instantly cuts the user off from Exchange, SharePoint,
  and federated SaaS such as an AWS app. You will build and test every link end to end, simulate a detonation
  safely in an evaluation tenant, and prove the chain fires. By the end you have a portfolio-grade Zero
  Trust signal-sharing project with diagrams, policy exports, and a demo video. It draws directly on Modules
  1 and 2.
objectives:
- Explain the Zero Trust signal-sharing loop that connects Defender for Endpoint, Intune compliance, and
  Conditional Access
- Configure an Intune compliance policy that maps the Microsoft Defender for Endpoint machine risk score
  to a device compliance state
- Build a Conditional Access policy that requires a compliant or Intune-managed device to grant access
- Verify the connector between Microsoft Intune and Microsoft Defender for Endpoint is enabled and exchanging
  signals
- Safely simulate a high-severity detection and validate that access is revoked end to end
- Assemble the architecture diagram, policy exports, and demo video that make this a hireable portfolio
  artifact
video: cse-m6-l01-capstone-zero-trust-endpoint-isolation.mp4
quiz:
- q: In this system, what is the direct trigger that causes Intune to mark the laptop noncompliant?
  options:
  - A user manually reports the device as lost
  - Defender for Endpoint raises the machine risk score above the threshold set in the compliance policy
  - Conditional Access blocks the sign-in first, which tells Intune to act
  - The antivirus signature file becomes more than 24 hours old
  answer: 1
  why: The compliance policy contains a rule 'Require the device to be at or under the machine risk score'.
    When Defender for Endpoint elevates the machine risk to High (above the allowed Medium), Intune evaluates
    the device as noncompliant. That is the signal that the rest of the chain depends on.
- q: Why does Conditional Access, not Intune, perform the actual access revocation to Exchange and SharePoint?
  options:
  - Intune cannot see cloud applications at all
  - Conditional Access is the policy decision point at the identity layer that gates access to apps based
    on the device compliance signal
  - Exchange and SharePoint ignore Intune entirely
  - Conditional Access is faster because it runs on the device
  answer: 1
  why: 'Intune only computes and stores the compliance state of the device. Conditional Access is the
    enforcement point in Entra ID: its grant control ''Require device to be marked as compliant'' reads
    that state at sign-in and token refresh, so a noncompliant device fails the grant and loses access
    to every app in scope, including federated SaaS.'
- q: A federated AWS application is in scope of the Conditional Access policy. Why does isolating the
    Windows laptop also cut off that AWS app?
  options:
  - Defender for Endpoint installs an agent inside AWS
  - Because Entra ID is the identity provider issuing the SAML/OIDC token, and Conditional Access evaluates
    device compliance before that token is issued
  - AWS polls Intune directly every minute
  - The laptop's local firewall blocks the AWS endpoints
  answer: 1
  why: When AWS uses Entra ID as its identity provider, every sign-in flows through Entra. Conditional
    Access evaluates the compliant-device grant before issuing the federation token, so a noncompliant
    device cannot obtain a token for the AWS app even though the workload lives in another cloud. This
    is the power of centralizing identity.
- q: What prerequisite makes the Defender for Endpoint risk score visible to Intune in the first place?
  options:
  - A manually exported CSV uploaded to Intune each morning
  - The Microsoft Defender for Endpoint connector in Intune must be turned On, with device compliance
    evaluation enabled
  - A third-party MDM bridge running on each laptop
  - A Logic App copying alerts between portals
  answer: 1
  why: Under Endpoint security or Connectors and tokens, the Microsoft Defender for Endpoint connector
    must be enabled and set to connect Windows devices and share signals for compliance. Without that
    connector the machine risk score never reaches Intune, and the compliance rule has nothing to evaluate.
- q: When you test the chain, why might access NOT be revoked instantly even after the device shows noncompliant?
  options:
  - Conditional Access only runs once per week
  - Existing access tokens remain valid until they expire or Continuous Access Evaluation revokes them;
    sign-in re-evaluation or CAE drives the cut-off
  - Intune compliance never reaches Exchange
  - The device must be physically rebooted for any policy to apply
  answer: 1
  why: Conditional Access is evaluated at sign-in and token refresh. An already-issued access token can
    linger until expiry unless Continuous Access Evaluation (CAE) signals the resource to revoke it near-real-time.
    Understanding token lifetime and CAE is what separates a demo that 'eventually' blocks from one that
    contains the threat in seconds.
- q: In two to four sentences, justify the design choice of using device-compliance-based Conditional
    Access for containment rather than simply having an analyst manually disable the user account when
    an alert fires.
  answer: The automated compliance-to-Conditional-Access loop responds in seconds with no human in the
    path, which matters because ransomware spreads far faster than an analyst can triage and act. It also
    scopes the response to the affected device and its identity context rather than nuking the user everywhere,
    and it reverses automatically once the device is remediated and risk drops back to acceptable. Manual
    account disablement is slower, error-prone under pressure, and creates a recovery burden, whereas
    this design is consistent, auditable, and self-healing. It embodies the Zero Trust principle of assume
    breach and verify continuously using shared signals.
  why: The grading answer should connect speed of containment, blast-radius scoping, and self-healing
    reversibility to the Zero Trust 'assume breach' pillar, and contrast those with the latency and human
    error of manual response.
resources:
- label: Enforce compliance for Microsoft Defender for Endpoint with Conditional Access in Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/advanced-threat-protection
- label: Device compliance policies in Microsoft Intune
  url: https://learn.microsoft.com/en-us/mem/intune/protect/device-compliance-get-started
- label: 'Conditional Access: Require compliant or hybrid joined device'
  url: https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-all-users-device-compliance
- label: Microsoft Defender for Endpoint evaluation lab
  url: https://learn.microsoft.com/en-us/defender-endpoint/evaluation-lab
---

## Scenario

A finance manager's corporate laptop opens a malicious attachment and ransomware begins encrypting files and attempting lateral movement. In a traditional shop, a SOC analyst eventually sees an alert, opens a ticket, and starts manually pulling access, minutes or hours later. By then the blast radius is enormous. Your capstone removes the human from the critical path. The moment **Microsoft Defender for Endpoint** classifies the machine as high risk, the device is judged noncompliant by **Intune**, and **Conditional Access** in **Entra ID** revokes the user's access to Exchange Online, SharePoint Online, and a federated **AWS** application, all within seconds. This is Zero Trust signal sharing in action: the endpoint, the device-management plane, and the identity plane all speaking the same language.

This project is the showpiece for Modules 1 (Zero Trust Identity & Entra ID) and 2 (Modern Endpoint Security). It proves you can design a closed-loop, automated containment control, exactly what enterprise hiring managers mean when they say 'Zero Trust'.

## Architecture

The control loop has four moving parts and one connector that glues two of them together:

1. **Microsoft Defender for Endpoint (MDE)** runs on the laptop. On active malware it raises the **machine risk score** to High.
2. The **MDE-to-Intune connector** shares that risk signal into Intune.
3. An **Intune compliance policy** contains the rule *Require the device to be at or under the machine risk score = Medium*. A High score therefore makes the device **noncompliant**.
4. A **Conditional Access policy** with the grant control *Require device to be marked as compliant* gates Exchange, SharePoint, and the federated AWS app. A noncompliant device fails the grant.

Signal flow, in one line:

`MDE detects malware -> risk = High -> Intune compliance = Noncompliant -> Conditional Access grant fails -> tokens revoked (CAE) -> access denied to M365 + AWS`

Because **Entra ID** is the identity provider for the AWS app, cutting the identity off at the token-issuance point isolates the user across clouds, not just inside Microsoft 365. Draw this as a left-to-right diagram with the laptop on the left and the three protected workloads on the right; that single diagram is the centerpiece of your portfolio writeup.

## Step-by-step build

**Step 0 - Prerequisites.** Use a Microsoft 365 E5 / Defender for Endpoint evaluation tenant. Onboard at least one Windows test device to MDE, enroll it in Intune, and confirm the user is licensed for Entra ID P1/P2.

**Step 1 - Enable the connector.** In the Intune admin center go to **Endpoint security > Microsoft Defender for Endpoint** (Connectors and tokens). Turn the connection **On** and enable *Connect Windows devices ... to Microsoft Defender for Endpoint* and *Allow Microsoft Defender for Endpoint to enforce Endpoint Security Configurations*. In the Defender portal, confirm the Intune connection shows **Enabled**. This bidirectional handshake is what carries the risk score.

**Step 2 - Build the compliance policy.** Create a Windows 10/11 compliance policy. Under **Microsoft Defender for Endpoint**, set *Require the device to be at or under the machine risk score* to **Medium**. Set the *Mark device noncompliant* action to **Immediately** (0 days) so there is no grace period during a real incident. Assign it to your test user group.

**Step 3 - Build the Conditional Access policy.** In Entra ID > **Conditional Access**, create a policy: Users = the test group; Target resources = Office 365 (Exchange + SharePoint) and the AWS enterprise application; Grant = **Require device to be marked as compliant** (and optionally *Require Microsoft Entra hybrid joined device*). Start in **Report-only** mode, then flip to **On** once you have validated it does not lock you out.

**Step 4 - Federate the AWS app (if not already).** Add AWS as an enterprise application using Entra ID as the SAML/OIDC IdP, and include it in the Conditional Access target resources so the same compliance grant governs it.

## Validation / Testing

Never detonate real ransomware on a production network. Use the **MDE evaluation lab**, which provisions isolated test VMs, or run a Microsoft-provided safe simulation. Two safe ways to drive the chain:

- **MDE Evaluation Lab + simulation:** spin up a lab device and run one of the bundled attack simulations (or the EICAR test file for AV). Watch the device's **risk level** climb in the Defender portal.
- **Tampering / controlled detection:** trigger a benign high-severity alert in the lab so MDE assigns a High risk score.

Then verify each link:

1. **Defender portal** > Device inventory: risk level shows **High**.
2. **Intune** > Device > Compliance: state flips to **Noncompliant** (may take a few minutes to sync).
3. **Sign-in logs** (Entra ID): a fresh sign-in to Outlook/SharePoint/AWS shows **Failure** with reason *device not compliant*; the Conditional Access tab names the policy that blocked it.
4. **Token revocation timing:** confirm **Continuous Access Evaluation** is shortening the cut-off for existing sessions. Note the realistic latency in your writeup, this honesty impresses interviewers.
5. **Remediation / self-heal:** clear the threat in the lab, watch risk drop to Medium or below, Intune returns to **Compliant**, and access is automatically restored. Demonstrating the loop closing both ways is the strongest part of the demo.

Keep a test plan table: *Link | How tested | Expected | Observed | Pass/Fail*. That table is a portfolio artifact in its own right.

## What to put in your portfolio

- **Architecture diagram** (the signal-flow diagram above) as a clean PNG/SVG.
- **Policy exports**: the Intune compliance policy JSON and the Conditional Access policy JSON (export via Graph or the portal). Redact tenant IDs.
- **A 3-5 minute demo video**: screen-record the detection, the compliance flip, the blocked sign-in, and the self-healing restore.
- **A one-page design doc**: the scenario, the threat it mitigates, design decisions (why CAE matters, why immediate noncompliance, blast-radius scoping), and known limitations.
- **A GitHub repo** with the exported policies, the diagram source, and a README that frames the business value: *contains a compromised endpoint in seconds, across M365 and federated SaaS, with zero analyst involvement*.

Frame the resume bullet around impact, for example: 'Designed and tested an automated Zero Trust endpoint-isolation control (Defender for Endpoint + Intune compliance + Conditional Access) that revokes access to M365 and federated AWS within seconds of a high-severity detection.'
