---
course: helpdesk-tier1-2
title: 'Tier 2 capstone: end-to-end incident handling'
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 9
summary: Work one realistic account-compromise incident from first report to post-incident notes, pulling
  together everything you learned across the course. You will rule out an outage, investigate sign-ins,
  contain the account, clean up attacker persistence, and document the root cause.
objectives:
- Triage a user report and rule out a service outage before assuming compromise
- Investigate suspicious sign-ins in Microsoft Entra ID and confirm scope
- Contain a compromised account by resetting credentials and revoking active sessions
- Find and remove attacker persistence such as inbox rules and mail forwarding
- Use message trace, quarantine, and Defender to assess spread and remediate
- Communicate, escalate, and write clear root-cause and post-incident notes in the ticket
video: hd6-l09-tier2-capstone.mp4
quiz:
- q: A user reports they cannot send email and that colleagues received strange messages from their address.
    What should you check FIRST before assuming the account is compromised?
  options:
  - Microsoft 365 Service health to rule out a wider outage
  - Immediately delete the user's mailbox
  - Buy the user a new laptop
  - Reinstall Outlook on every device in the office
  answer: 0
  why: Service health tells you whether the symptoms come from a known Microsoft outage. Confirming scope
    first stops you from chasing a compromise that is really a platform incident — and vice versa.
- q: In Microsoft Entra ID, which signal most strongly suggests an account was compromised rather than
    the user simply travelling?
  options:
  - A single successful sign-in from the user's usual city
  - Successful sign-ins from an unfamiliar country plus impossible-travel and legacy-auth attempts
  - The user changing their display name
  - A failed sign-in once on Monday morning
  answer: 1
  why: Impossible travel, an unfamiliar location, and legacy or basic-auth sign-ins together are classic
    compromise indicators. One normal sign-in or a single typo'd password is not.
- q: After confirming compromise, what is the correct CONTAINMENT order for the account?
  options:
  - Tell the user to ignore it and monitor for a week
  - Revoke sessions only and leave the old password active
  - Reset the password, then revoke active sessions, then re-confirm MFA
  - Delete the account permanently with no investigation
  answer: 2
  why: Resetting the password stops new sign-ins with the stolen credential, revoking sessions kills tokens
    the attacker already holds, and re-confirming MFA restores trusted access. Skipping the revoke leaves
    live tokens working.
- q: Why must you check the mailbox for inbox rules and mail forwarding after a compromise?
  options:
  - Rules make Outlook load faster
  - Forwarding is required for MFA to work
  - Inbox rules store the user's password
  - Attackers plant rules to hide replies or auto-forward mail, giving them persistence after the password
    change
  answer: 3
  why: A planted rule that deletes or forwards security mail lets the attacker keep reading messages and
    hide their tracks even after you reset the password. Removing persistence is part of remediation,
    not optional.
- q: Name the Exchange Online tool you would use to see whether messages were actually sent from the mailbox
    and where they were delivered.
  answer: Message trace (Get-MessageTrace in PowerShell, or the message trace report in the Exchange admin
    center / Defender portal).
  why: Message trace shows the path and status of individual messages, so you can confirm what the attacker
    sent, to whom, and whether it was delivered or blocked.
- q: In one or two sentences, what belongs in your post-incident / root-cause note once the account is
    secured?
  answer: A short timeline of what happened, the likely root cause (e.g. phishing link harvested the credential),
    the actions you took to contain and remediate, and any follow-ups such as user security awareness
    or tightening conditional access.
  why: Good post-incident notes let the next tech understand the incident at a glance, support escalation
    or audit, and feed prevention so the same compromise does not recur.
resources:
- label: Microsoft Learn — Respond to a compromised account in Microsoft 365
  url: https://learn.microsoft.com/en-us/defender-office-365/responding-to-a-compromised-email-account
- label: Microsoft Learn — Investigate risk with Microsoft Entra ID Protection
  url: https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-investigate-risk
- label: Microsoft Learn — Run a message trace in Exchange Online
  url: https://learn.microsoft.com/en-us/exchange/monitoring/trace-an-email-message/run-a-message-trace-and-view-results
- label: 'Microsoft Learn — Exam MS-102: Microsoft 365 Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## The ticket lands

A user, Priya, raises a ticket: she **can't send email**, and two colleagues have asked her why she emailed them a strange "shared invoice" link. This is your capstone. Everything you learned this course — hardware and OS basics, networking, identity, email, security, and Microsoft 365 admin — comes together in one incident. You will work it end to end like a real **Tier 2** tech.

Don't jump to a fix. Start with **triage**: when did it start, what exactly does "can't send" look like (a bounce? a block?), and has anything changed. Log it in the ticket as you go.

## Rule out an outage first

Before you assume compromise, confirm scope. Open the Microsoft 365 admin center and check **Service health**.

```text
Microsoft 365 admin center > Health > Service health > Exchange Online
```

If there's an active advisory affecting send/receive, this may be a platform incident, not Priya. No advisory, and only Priya is affected with odd outbound mail? That points at an **account compromise** — likely the aftermath of a phishing link that harvested her password.

## Investigate the sign-ins

Go to **Microsoft Entra ID** and review Priya's sign-in logs. You're looking for **impossible travel**, sign-ins from an unfamiliar country, and **legacy authentication** attempts.

```powershell
Connect-MgGraph -Scopes "AuditLog.Read.All","User.ReadWrite.All"
Get-MgAuditLogSignIn -Filter "userPrincipalName eq 'priya@contoso.com'" -Top 25 |
  Select-Object createdDateTime, ipAddress, @{n='City';e={$_.Location.City}}, status
```

A successful sign-in from another continent minutes after a normal one confirms it. Note the timeline in the ticket.

## Contain the account

Now stop the bleeding, in order. **Reset the password**, then **revoke active sessions** so any tokens the attacker already holds stop working, then re-confirm **MFA**.

```powershell
# Disable sign-in while you work, then revoke live tokens
Update-MgUser -UserId priya@contoso.com -AccountEnabled:$false
Revoke-MgUserSignInSession -UserId priya@contoso.com
```

Reset the password in the admin center, re-enable the account, and confirm MFA is registered. The stolen credential is now useless.

## Remove persistence and assess spread

A password reset alone is not enough. Attackers plant **inbox rules** and **mail forwarding** to keep reading mail and hide replies. Connect to Exchange Online and check.

```powershell
Connect-ExchangeOnline
Get-InboxRule -Mailbox priya@contoso.com | Format-List Name, Description, ForwardTo, DeleteMessage
Get-Mailbox priya@contoso.com | Format-List ForwardingSmtpAddress
```

Delete any rule you didn't expect. Then run a **message trace** to see what actually went out and to whom, and check **quarantine** and **Microsoft Defender for Office 365** for the phishing message and its blast radius.

```powershell
Get-MessageTrace -SenderAddress priya@contoso.com -StartDate (Get-Date).AddDays(-2) -EndDate (Get-Date)
```

## Communicate, escalate, document

Tell Priya what happened in plain language and that her account is secure. Warn the colleagues who received the link **not to click it**. If the spread is wide or other accounts look affected, **escalate** to Tier 3 / security. Finally, write the **root-cause and post-incident note** in the ticket: timeline, likely cause (phishing), actions taken, and follow-ups such as security-awareness training and tighter conditional access.

## Your task

Write the full incident up as a single ticket: triage notes, the outage check, the sign-in evidence, your containment steps, the persistence you removed, the message-trace findings, and a three-line root-cause note. Treat it as the write-up you'd hand to a hiring manager.
