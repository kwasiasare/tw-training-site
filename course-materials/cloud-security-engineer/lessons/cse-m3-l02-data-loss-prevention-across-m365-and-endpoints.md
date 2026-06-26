---
course: cloud-security-engineer
title: Data Loss Prevention Across M365 and Endpoints
month: 3
monthTitle: Data Security & AI Governance with Microsoft Purview
lesson: 2
summary: 'Classification tells you what your sensitive data is; Data Loss Prevention decides what people
  are allowed to do with it. This lesson builds Microsoft Purview DLP policies that span Exchange, SharePoint,
  OneDrive, Teams, and managed devices through Endpoint DLP. You will learn to write conditions from Sensitive
  Information Types and sensitivity labels, choose actions from policy tips through block-with-override
  to encryption and Endpoint controls that restrict copying to USB, clipboard, and cloud upload. Two realistic
  policies anchor the lesson: blocking external sharing of credit-card data, and restricting labeled files
  from leaving managed devices on unmanaged USB. You will also use simulation mode, policy tips, alerts,
  and DLP analytics to roll out safely.'
objectives:
- Describe Purview DLP and the workloads it protects, including Endpoint DLP on managed devices
- Build DLP conditions from Sensitive Information Types and sensitivity labels with instance counts and
  confidence
- 'Select appropriate actions: policy tip, block, block with override, encrypt, and Endpoint restrictions'
- Configure Endpoint DLP to restrict copy to USB, clipboard, and cloud upload, plus print and network
  share
- Roll out a policy safely using simulation/test mode, policy tips, and user education before enforcement
- 'Author two realistic policies: block external credit-card sharing and restrict labeled files to unmanaged
  USB'
video: cse-m3-l02-data-loss-prevention-across-m365-and-endpoints.mp4
quiz:
- q: What is the relationship between data classification and DLP?
  options:
  - DLP replaces classification entirely
  - Classification identifies what the data is; DLP enforces what users may do with that identified data
  - DLP only works on unclassified data
  - Classification is only needed for email, DLP only for endpoints
  answer: 1
  why: 'DLP conditions are written against the things classification produces: Sensitive Information Types
    and sensitivity labels. Classification answers ''what is this data,'' and DLP answers ''what is allowed
    to happen to it.'' Without classification, a DLP policy has nothing reliable to match on.'
- q: Which set of locations does a single Purview DLP policy potentially cover?
  options:
  - Only Exchange email
  - Exchange, SharePoint, OneDrive, Teams chat and channel messages, and Endpoint (managed devices)
  - Only on-premises file servers
  - Only third-party SaaS apps
  answer: 1
  why: Purview DLP spans Exchange Online, SharePoint, OneDrive, Teams messages, and Endpoint DLP on Windows
    and macOS managed devices (plus options like on-premises repositories and Defender for Cloud Apps).
    A single policy can select multiple of these locations, giving consistent enforcement across the data
    estate.
- q: A policy uses 'Block with override.' What does this achieve compared to a plain block?
  options:
  - It silently allows the action with no record
  - It blocks the action but lets the user proceed after providing a business justification, which is
    logged
  - It always encrypts instead of blocking
  - It disables the policy for that user permanently
  answer: 1
  why: Block with override stops the risky action by default but allows the user to override, typically
    requiring a business justification or false-positive report, which is recorded. This balances protection
    with productivity and surfaces edge cases for tuning while keeping an audit trail.
- q: Endpoint DLP is configured to restrict 'copy to removable USB' for files carrying the Highly Confidential
    label. Which prerequisite makes this enforceable?
  options:
  - The device must be unmanaged and personal
  - The device must be onboarded to Purview/Defender endpoint management so Endpoint DLP can monitor egress
    actions
  - The user must be a global administrator
  - The file must be stored only in Exchange
  answer: 1
  why: Endpoint DLP only works on devices onboarded to Microsoft Purview / Microsoft Defender for Endpoint.
    Once onboarded, the endpoint agent can observe and restrict egress activities such as copying to USB,
    clipboard, cloud upload, printing, and network shares for labeled or SIT-matched files.
- q: Why should you run a new DLP policy in simulation (test) mode before enforcement?
  options:
  - Simulation mode encrypts all matching files immediately
  - It shows what the policy would match and which actions would fire, so you can gauge impact and false
    positives without disrupting users
  - It is required to license DLP
  - Simulation mode only works for Teams
  answer: 1
  why: Simulation (test) mode evaluates the policy and reports matches and would-be actions, optionally
    showing policy tips, without actually blocking anything. This lets you measure false positives, estimate
    user impact, and tune conditions before turning on enforcement, avoiding a disruptive big-bang rollout.
- q: Design a DLP policy, in two to four sentences, that blocks external sharing of credit-card data while
    remaining usable for staff who occasionally have a legitimate need. Name the location, condition,
    action, and rollout approach.
  answer: Create a DLP policy scoped to Exchange, SharePoint, OneDrive, and Teams with a condition that
    content contains the built-in Credit Card Number SIT at high confidence with a low instance threshold,
    and that the content is shared with people outside the organization. Use a 'Block with override' action
    so external sharing is stopped by default but a user with a genuine need can proceed with a logged
    business justification, and show a policy tip explaining the rule. Roll it out first in simulation
    mode with policy tips on to measure false positives, then enable enforcement once the match rate looks
    clean and generate alerts for any overrides. This protects regulated data while keeping a controlled
    escape hatch and an audit trail for legitimate cases.
  why: A strong answer ties together the correct location set, a label/SIT-based condition with a recipient-is-external
    check, a block-with-override action for the legitimate-need requirement, and a simulation-first rollout,
    which is exactly the safe, real-world DLP pattern.
resources:
- label: Learn about data loss prevention
  url: https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp
- label: Learn about Endpoint data loss prevention
  url: https://learn.microsoft.com/en-us/purview/endpoint-dlp-learn-about
- label: Create and deploy a data loss prevention policy
  url: https://learn.microsoft.com/en-us/purview/dlp-create-deploy-policy
- label: Get started with DLP alerts and the DLP Alerts dashboard
  url: https://learn.microsoft.com/en-us/purview/dlp-alerts-dashboard-get-started
---

## From Knowing to Controlling

In the previous lesson you taught Purview to **identify** sensitive data with SITs, trainable classifiers, and labels. **Data Loss Prevention (DLP)** is the control that decides **what users are allowed to do** with that identified data. A DLP policy watches for sensitive content in motion, an email to an outside recipient, a file shared with an external guest, a document copied to a USB stick, and applies actions ranging from a gentle tip to a hard block. The two halves fit together: classification provides the *what*, DLP provides the *what's allowed*.

## Where DLP Applies: Locations

A single Purview DLP policy can protect multiple **locations**:

- **Exchange Online** - outbound and internal email.
- **SharePoint** and **OneDrive** - files at rest and when shared.
- **Teams** - chat and channel messages.
- **Endpoint (Devices)** - managed Windows and macOS devices via **Endpoint DLP**, controlling local egress like USB, clipboard, and cloud upload.
- Plus **on-premises repositories** and **Microsoft Defender for Cloud Apps** for broader SaaS coverage.

Choosing locations thoughtfully matters: an email-only policy will not stop a user dragging a file to a thumb drive. That gap is exactly what **Endpoint DLP** closes.

## Conditions: Built on Classification

A DLP rule's **conditions** describe what to match. The most common building blocks are:

- **Content contains** a **Sensitive Information Type** (e.g. *Credit Card Number*), with a **confidence level** and a **minimum instance count** (one card vs. fifty cards is very different risk).
- **Content contains** a **sensitivity label** (e.g. *Highly Confidential*) or a retention label.
- **Context** conditions: recipient is **external**, content is **shared with people outside the organization**, sender domain, attachment type, and more.

You combine conditions with AND/OR and group them. A typical rule reads: *content contains Credit Card Number (high confidence, 1+ instances) AND is shared with people outside my organization*.

## Actions: From Tips to Hard Blocks

Once a rule matches, **actions** decide the outcome. Common actions, roughly increasing in strictness:

- **Policy tip** - a non-blocking, educational message shown to the user in Outlook, Office, or Teams. Pure user education.
- **Notify** - email the user or admins; log an event.
- **Restrict access / encrypt** - apply rights protection or restrict who can access the shared content.
- **Block with override** - block by default but let the user proceed with a logged **business justification** or **false-positive report**.
- **Block** - hard stop, no override.

For Endpoint locations, additional **Endpoint actions** apply: **restrict copy to removable USB**, **restrict clipboard copy**, **restrict cloud / web upload**, **restrict print**, **restrict copy to network share**, and **restrict access by unallowed apps**, each settable to *Audit*, *Block with override*, or *Block*.

## Endpoint DLP in Depth

**Endpoint DLP** extends enforcement to the device itself, where users actually exfiltrate data. It only works on devices **onboarded** to Microsoft Purview / Microsoft Defender for Endpoint. Once onboarded, the endpoint agent observes egress activities and enforces your actions:

- Copying a labeled file to an **unmanaged USB** drive.
- Pasting sensitive content into a browser or chat via the **clipboard**.
- Uploading to **unsanctioned cloud apps** or personal web services.
- **Printing** or copying to a **network share**.

You can also define **printer groups**, **removable storage device groups**, and **network share groups** so that, for example, corporate-approved encrypted USB drives are allowed while all others are blocked.

## Two Realistic Policies

**Policy A - Block external sharing of credit-card data.**

```text
Locations:   Exchange, SharePoint, OneDrive, Teams
Condition:   Content contains SIT "Credit Card Number"
             (High confidence, 1+ instances)
             AND content is shared with people outside the org
Action:      Block with override (require business justification)
User:        Policy tip explaining the rule
Alerts:      High-severity alert on every override
```

**Policy B - Restrict labeled files from leaving managed devices on unmanaged USB.**

```text
Location:    Devices (Endpoint DLP, onboarded devices only)
Condition:   Content contains sensitivity label "Highly Confidential"
Endpoint actions:
             Copy to removable USB ......... Block
             (allow approved "Corporate USB" device group)
             Copy to clipboard ............. Block with override
             Upload to cloud / web ......... Block
             Print ......................... Audit
User:        Policy tip; override requires justification
```

Policy A keeps regulated card data inside the tenant with a controlled escape hatch. Policy B ensures your most sensitive labeled documents cannot trivially walk out on a personal thumb drive while still permitting approved hardware.

## Roll Out Safely, Then Monitor

Never flip a new DLP policy straight to enforce. Use this sequence:

1. **Simulation / test mode** - the policy evaluates and reports what it *would* match and which actions *would* fire, without disrupting anyone. Review the would-be matches to gauge false positives and impact.
2. **Test with policy tips** - turn tips on in test mode so users start seeing guidance and you collect feedback.
3. **Enforce** - once the match rate is clean, enable enforcement.

After go-live, run the operation from data: the **DLP Alerts dashboard** surfaces matches, overrides, and false-positive reports, and **DLP analytics / activity explorer** show trends so you can tune conditions, reduce noise, and prove control effectiveness to auditors. DLP is never 'set and forget'; it is a continuous loop of measure, tune, and educate.
