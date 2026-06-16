---
course: helpdesk-tier1-2
title: Exchange Online and email support
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 3
summary: Learn how Exchange Online delivers cloud email, the mailbox types and permissions you manage,
  and the day-to-day tickets you will fix with the Exchange admin center, message trace, and PowerShell.
objectives:
- 'Describe Exchange Online and the main mailbox types: user, shared, and resource/room'
- Grant shared mailbox access and explain Full Access, Send As, and Send on Behalf
- Choose between a distribution group and a Microsoft 365 group for a given need
- 'Explain mail flow basics: connectors and transport (mail flow) rules'
- Run a message trace to answer 'did my email arrive?' tickets and check quarantine
- 'Triage common email tickets: can''t send/receive, out of office, mailbox full, calendar sharing'
video: hd6-l03-exchange-online-and-email-support.mp4
quiz:
- q: A team wants a no-license inbox like info@contoso.com that several agents read and reply from. Which
    mailbox type fits best?
  options:
  - A resource mailbox
  - A shared mailbox
  - A second user mailbox with a paid license
  - A distribution group
  answer: 1
  why: A shared mailbox has no license requirement (under 50 GB) and lets multiple users open it and send
    from the shared address, which is exactly the info@ scenario.
- q: You add a user with Full Access to a shared mailbox, but they complain their replies still come from
    their own address. What else do they need?
  options:
  - A new Outlook profile
  - Send As or Send on Behalf permission
  - A mailbox license
  - Owner role on a distribution group
  answer: 1
  why: Full Access only lets a user open and read the mailbox. To send from the shared address they also
    need Send As (appears purely as the mailbox) or Send on Behalf permission.
- q: Which statement best distinguishes a distribution group from a Microsoft 365 group?
  options:
  - A distribution group includes a shared SharePoint site and Teams
  - A Microsoft 365 group is email-only with no shared resources
  - A distribution group just forwards mail to members; a Microsoft 365 group adds shared mailbox, calendar,
    SharePoint and Teams
  - They are identical and interchangeable
  answer: 2
  why: A distribution group is for one-way email distribution to members; a Microsoft 365 group is a collaboration
    identity with a shared inbox, calendar, SharePoint site and Teams integration.
- q: A user says 'I sent an email an hour ago but they never got it.' Which tool answers what actually
    happened to that message?
  options:
  - Message trace in the Exchange admin center
  - Connection filter policy
  - A mail flow (transport) rule
  - Outlook's Focused Inbox
  answer: 0
  why: Message trace follows a specific message through Exchange Online and shows its status (Delivered,
    Pending, Failed, Quarantined), which is the fastest way to confirm whether and where it arrived.
- q: In one sentence, what is the difference between Send As and Send on Behalf?
  answer: Send As makes the message appear to come purely from the shared mailbox, while Send on Behalf
    shows 'Sender on behalf of Mailbox' so the recipient can see who actually sent it.
  why: Both let a delegate send from another address, but Send on Behalf preserves the real sender's identity
    in the From line, which matters for transparency and auditing.
- q: A ticket says 'my mailbox is full and I can't receive new mail.' Name two things you would check
    or do.
  answer: Check the mailbox storage quota and current size (Get-Mailbox / Get-MailboxStatistics), then
    have the user clear large items and empty Deleted Items, or raise the quota / archive policy if appropriate.
  why: Mailbox-full tickets are about quota versus usage; you confirm the limit, see how much is used,
    and either free space (delete/archive) or adjust the quota and enable archiving.
resources:
- label: Microsoft Learn — Exchange Online overview
  url: https://learn.microsoft.com/en-us/exchange/exchange-online
- label: Microsoft Learn — About shared mailboxes
  url: https://learn.microsoft.com/en-us/microsoft-365/admin/email/about-shared-mailboxes
- label: Microsoft Learn — Mail flow rules (transport rules) in Exchange Online
  url: https://learn.microsoft.com/en-us/exchange/security-and-compliance/mail-flow-rules/mail-flow-rules
- label: 'Microsoft Learn — Exam MS-102: Microsoft 365 Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## Exchange Online: cloud email, managed centrally

**Exchange Online** is the hosted email service inside Microsoft 365. Instead of running an on-premises Exchange server, mailboxes live in Microsoft's cloud and you administer them from the **Exchange admin center (EAC)** at `admin.exchange.microsoft.com` or from **Exchange Online PowerShell**. As a Tier 2 tech, this is where most email tickets land, so knowing the moving parts pays off fast.

Connect to PowerShell once and you can do almost anything the portal can, faster:

```powershell
Connect-ExchangeOnline -UserPrincipalName admin@contoso.com
Get-Mailbox -ResultSize 50 | Format-Table DisplayName,RecipientTypeDetails,PrimarySmtpAddress
```

## Mailbox types you will manage

There are three types you meet daily. A **user mailbox** belongs to a licensed person. A **shared mailbox** (think `info@` or `support@`) needs no license under 50 GB and lets several people read and send from one address. A **resource mailbox** represents a **room** or **equipment** you book in Outlook calendars.

```powershell
New-Mailbox -Shared -Name "Support" -PrimarySmtpAddress support@contoso.com
New-Mailbox -Room -Name "Boardroom"
```

## Shared mailbox access and permissions

Three permissions cover almost every shared-mailbox request. **Full Access** lets someone open and read the mailbox. **Send As** makes their messages appear to come purely from the shared address. **Send on Behalf** shows "User on behalf of Mailbox". A common ticket: a user has Full Access but replies still show their own name — they are missing Send As.

```powershell
Add-MailboxPermission -Identity support@contoso.com -User joe@contoso.com -AccessRights FullAccess -AutoMapping $true
Add-RecipientPermission -Identity support@contoso.com -Trustee joe@contoso.com -AccessRights SendAs
```

## Groups: distribution vs Microsoft 365

A **distribution group** simply forwards mail to its members — one address in, many copies out. A **Microsoft 365 group** is a collaboration identity: a shared inbox, calendar, **SharePoint** site and **Teams** all under one membership. Rule of thumb: announcements only -> distribution group; a team that also needs shared files and chat -> Microsoft 365 group.

## Mail flow, message trace, and quarantine

**Mail flow** is how messages move in and out. **Connectors** define routing to or from partner systems, and **mail flow rules** (transport rules) apply conditions and actions — for example, add a disclaimer or block an attachment type. When a user asks "did my email arrive?", run a **message trace**:

```powershell
Get-MessageTrace -SenderAddress joe@contoso.com -StartDate (Get-Date).AddHours(-4) -EndDate (Get-Date)
```

Statuses like **Delivered**, **Pending**, **Failed**, or **Quarantined** tell you the next step. If it is **Quarantined**, check the quarantine in the Microsoft Defender portal and release it if it is a false positive.

```text
Exchange admin center -> Mail flow -> Message trace -> set sender/recipient + time range -> Search
```

## Your task

In a test tenant, create a shared mailbox `helpdesk@yourdomain`, grant a colleague **Full Access** and **Send As**, then send a test message and run a **message trace** to confirm it was Delivered. Note where you would look if the status came back Quarantined instead.
