---
course: helpdesk-tier1-2
title: Defender for Office 365 and threat protection
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 6
summary: Learn how Exchange Online Protection and Defender for Office 365 layer up to stop phishing, spoofing,
  and malware, then walk the Tier-2 workflow for triaging a reported phishing email and a user who clicked
  a bad link.
objectives:
- Explain the difference between Exchange Online Protection (EOP) and Defender for Office 365 Plan 1 and
  Plan 2
- Describe how Safe Attachments detonation and Safe Links time-of-click protection work
- Configure and reason about anti-phishing, anti-spam, and anti-malware policies
- Manage quarantined messages and handle end-user release requests
- Use Threat Explorer and reports to investigate a reported message
- Run the Tier-2 triage workflow when a user reports phishing or clicks a malicious link
video: hd6-l06-defender-for-office-365.mp4
quiz:
- q: Which capability is part of Defender for Office 365 rather than the baseline Exchange Online Protection?
  options:
  - Anti-spam filtering
  - Connection filtering by IP
  - Safe Attachments detonation in a sandbox
  - Basic anti-malware scanning
  answer: 2
  why: EOP gives every Exchange Online mailbox anti-spam, anti-malware, and connection filtering. Safe
    Attachments (sandbox detonation) and Safe Links are Defender for Office 365 add-on features.
- q: What does Safe Links protect against that a one-time scan at delivery cannot?
  options:
  - A link that is weaponised after the email is delivered
  - Spelling mistakes in the subject line
  - Oversized attachments
  - Mailbox storage limits
  answer: 0
  why: Safe Links rewrites URLs and checks them at time-of-click, so a link that was clean at delivery
    but later points to a malicious site is still blocked when the user clicks it.
- q: A user says a legitimate newsletter keeps landing in quarantine. As Tier 2, what is the cleanest
    fix?
  options:
  - Disable anti-spam for the whole tenant
  - Turn off Defender for Office 365
  - Release it and tune the anti-spam or anti-phishing policy (allow the sender)
  - Tell the user to create an inbox rule
  answer: 2
  why: Release the message so the user gets it, then reduce future false positives by allowing the sender
    or adjusting the policy. Disabling protection tenant-wide is never the answer.
- q: Where in the Microsoft Defender portal would a Tier-2 tech investigate all messages matching a reported
    phishing campaign?
  options:
  - Azure AD Connect
  - Threat Explorer (Explorer)
  - The Teams admin center
  - Windows Update for Business
  answer: 1
  why: Threat Explorer (Explorer / Real-time detections) lets you search messages by sender, subject,
    URL, or detection and see who else received the same campaign.
- q: In one sentence, what is the difference between EOP and Defender for Office 365 Plan 2?
  answer: EOP is the baseline anti-spam, anti-malware, and anti-phishing filtering included with Exchange
    Online, while Defender for Office 365 Plan 2 adds Safe Attachments, Safe Links, automated investigation
    and response (AIR), attack simulation training, and advanced hunting on top of Plan 1.
  why: Knowing the layering — EOP, then Plan 1, then Plan 2 — tells you which features a tenant actually
    has before you promise a customer a capability they may not be licensed for.
- q: A user reports they clicked a link in a suspicious email. List the first Tier-2 triage steps.
  answer: Confirm what they clicked and whether they entered credentials; use the built-in Report phishing
    data and Threat Explorer to find the message and anyone else who got it; check Safe Links / URL click
    verdicts; if credentials were entered, reset the password and revoke sessions, then purge the message
    tenant-wide and escalate if needed.
  why: Triage is contain first (credentials/sessions), then scope the blast radius (who else received
    it), then remediate (purge) — a repeatable Tier-2 incident pattern, not guesswork.
resources:
- label: Microsoft Learn — Microsoft Defender for Office 365 overview
  url: https://learn.microsoft.com/en-us/defender-office-365/mdo-about
- label: Microsoft Learn — Safe Attachments in Defender for Office 365
  url: https://learn.microsoft.com/en-us/defender-office-365/safe-attachments-about
- label: Microsoft Learn — Safe Links in Defender for Office 365
  url: https://learn.microsoft.com/en-us/defender-office-365/safe-links-about
- label: 'Microsoft Learn — MS-102: Microsoft 365 Administrator exam'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## The threat landscape and why layers matter

Most attacks against an organisation arrive by email: **phishing** (tricking a user into giving up credentials), **spoofing** (forging a trusted sender), **malware** (a weaponised attachment or link), and **business email compromise** (a convincing message from a "CEO" asking for a wire transfer). No single filter stops all of these, so Microsoft 365 stacks protection in layers.

The baseline layer is **Exchange Online Protection (EOP)** — every Exchange Online mailbox gets it. EOP handles **anti-spam**, **anti-malware**, **anti-phishing** (spoof intelligence), and **connection filtering**. On top of EOP you can license **Microsoft Defender for Office 365**, sold as **Plan 1** (Safe Attachments, Safe Links, real-time detections) and **Plan 2** (everything in Plan 1 plus automated investigation and response, attack simulation training, and advanced hunting).

## Safe Attachments and Safe Links

**Safe Attachments** opens attachments in an isolated sandbox and watches their behaviour — this is called **detonation**. If the file does something malicious, it never reaches the inbox. **Safe Links** rewrites every URL and re-checks it at the moment the user clicks — **time-of-click** protection. This matters because attackers often send a clean link, then weaponise the destination after delivery, defeating a one-time scan.

```text
Microsoft Defender portal > Email & collaboration > Policies & rules
  > Threat policies > Safe Attachments  (and Safe Links)
```

## Anti-phishing, anti-spam, and anti-malware policies

Policies decide what happens to suspect mail. **Anti-phishing** policies add impersonation and mailbox-intelligence protection; **anti-spam** policies set spam actions and allow/block lists; **anti-malware** policies control the common-attachments filter. You can read them in **Exchange Online PowerShell**.

```powershell
Connect-ExchangeOnline
Get-AntiPhishPolicy | Format-List Name,Enabled,EnableMailboxIntelligence
Get-HostedContentFilterPolicy | Format-List Name,SpamAction,BulkThreshold
```

## Quarantine and end-user release

Messages that policies block land in **quarantine**. As Tier 2 you review them, **release** false positives, and decide whether end users may request release themselves (governed by **quarantine policies**).

```text
Microsoft Defender portal > Email & collaboration
  > Review > Quarantine
```

```powershell
Get-QuarantineMessage -RecipientAddress user@contoso.com
Release-QuarantineMessage -Identity <messageId> -ReleaseToAll
```

When a user emails "why didn't I get this newsletter?", the cleanest fix is to release the message and then allow the sender or tune the policy — never disable protection tenant-wide.

## Threat Explorer, reporting, and the report buttons

**Threat Explorer** (Explorer / Real-time detections) lets you search all mail by sender, subject, URL, or detection verdict, so you can see who else received a campaign. Users help you by clicking the built-in **Report phishing** / **Report message** button in Outlook, which feeds submissions you triage under **Submissions**.

## The Tier-2 triage workflow

When a user reports a suspicious email or admits they clicked a bad link, work a repeatable pattern: **contain**, then **scope**, then **remediate**.

```text
1. Contain: did they enter credentials? Reset password + revoke sessions.
2. Scope: use Threat Explorer to find everyone who got the same message.
3. Check Safe Links click verdicts to confirm what was blocked or allowed.
4. Remediate: purge the message tenant-wide; block sender/URL.
5. Document and escalate to security if the blast radius is wide.
```

## Your task

In the Microsoft Defender portal, open Threat policies and read your tenant's Safe Links, Safe Attachments, and anti-phishing policies. Then connect to Exchange Online PowerShell and run `Get-AntiPhishPolicy` and `Get-QuarantineMessage`, and write a short five-step triage note for a user who clicked a phishing link.
