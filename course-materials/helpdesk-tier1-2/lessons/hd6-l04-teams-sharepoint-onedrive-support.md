---
course: helpdesk-tier1-2
title: Teams, SharePoint and OneDrive support
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 4
summary: 'Learn how Teams, SharePoint and OneDrive are wired together in Microsoft 365, then support the
  everyday tickets: file sync errors, lost files, sharing problems, and guest access.'
objectives:
- Explain how a Team is backed by a Microsoft 365 group and a SharePoint site, and where Teams files actually
  live
- Navigate the Teams admin center to find policies, meeting policies, and external/guest access settings
- Manage SharePoint sites, document libraries, and internal versus external sharing links
- 'Support OneDrive for Business: the sync client, Known Folder Move, and storage quotas'
- 'Resolve common tickets: file sync errors, restoring a lost file, and access problems'
- Recognise retention and orphaned-site issues that follow when a Team or group is deleted
video: hd6-l04-teams-sharepoint-onedrive-support.mp4
quiz:
- q: Where do files shared in a Microsoft Teams channel actually get stored?
  options:
  - In the Teams app database
  - In a SharePoint document library on the team's site
  - On the local PC only
  - In Exchange Online mailboxes
  answer: 1
  why: Each standard channel maps to a folder in the **Documents** library of the team's backing SharePoint
    site, so Teams files are really SharePoint files.
- q: When you create a new Team, what is automatically created alongside it?
  options:
  - A Microsoft 365 group and a SharePoint site
  - A new Azure subscription
  - A shared mailbox only
  - A separate Microsoft 365 tenant
  answer: 0
  why: A Team is backed by a **Microsoft 365 group**, which provisions a SharePoint site, a group mailbox,
    a calendar, and a Planner — delete the group and all of these go with it.
- q: A user deleted a file from a SharePoint document library yesterday. Where do you look first to restore
    it?
  options:
  - The Exchange recoverable items folder
  - The Teams chat history
  - The site Recycle Bin
  - The Azure recovery vault
  answer: 2
  why: Deleted items go to the **site Recycle Bin** for 93 days; if it was emptied there, the **second-stage
    Recycle Bin** is the next stop before any tenant-level recovery.
- q: Which feature automatically redirects a user's Desktop, Documents, and Pictures folders into OneDrive?
  options:
  - BitLocker
  - Known Folder Move
  - Conditional Access
  - Files On-Demand
  answer: 1
  why: '**Known Folder Move (KFM)** redirects the Windows known folders into OneDrive so they sync and
    survive a device loss; Files On-Demand is separate and controls local availability.'
- q: An external partner cannot open a file a colleague 'shared' with them. List two settings you would
    check.
  answer: Check the SharePoint/OneDrive external sharing level for the tenant and that specific site (it
    may be set to internal-only), and check the sharing link type used (a 'People in your organisation'
    link will not work for guests — they need a 'Specific people' or 'Anyone' link).
  why: Sharing fails most often because the site or tenant external-sharing policy blocks it, or because
    the wrong **link type** was chosen — both must allow the external recipient.
- q: Why can deleting a Team or its Microsoft 365 group cause an 'orphaned' SharePoint site, and what
    is the retention concern?
  answer: Deleting the group deletes its connected SharePoint site, mailbox, and Teams content together;
    if a retention policy is applied, content may be preserved in a hidden/preservation state even after
    deletion, and admins can restore the group (and its site) within the 30-day soft-delete window.
  why: Group-connected resources share a lifecycle, so **retention** and the **30-day soft delete** window
    govern whether content can be recovered before it is permanently purged.
resources:
- label: Microsoft Learn — Microsoft Teams admin documentation
  url: https://learn.microsoft.com/en-us/microsoftteams/manage-teams-in-modern-portal
- label: Microsoft Learn — Manage sharing settings for SharePoint and OneDrive
  url: https://learn.microsoft.com/en-us/sharepoint/turn-external-sharing-on-or-off
- label: Microsoft Learn — OneDrive guide for administrators
  url: https://learn.microsoft.com/en-us/sharepoint/onedrive-online-admin-center
- label: 'Microsoft Learn — Exam MS-102: Microsoft 365 Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## How Teams, SharePoint and OneDrive fit together

This is the single most important idea in the lesson: these three services are one connected system. When you create a **Team**, Microsoft 365 quietly provisions a **Microsoft 365 group** behind it. That group brings a **SharePoint site**, a group mailbox, a calendar, and a Planner. Every file someone drops into a Teams channel is actually stored in the **Documents** library of that SharePoint site — Teams is just a friendly front door to SharePoint.

**OneDrive for Business** is the personal version of the same SharePoint storage engine: each user gets their own site for private files. Files shared in a one-to-one or group **chat** (not a channel) live in the sender's OneDrive, not the team site. Knowing where a file physically lives tells you exactly which admin center to open when a ticket lands.

## The Teams admin center

Most Teams tickets are solved with **policies**. Open the Teams admin center to manage them.

```text
admin.teams.microsoft.com
  -> Teams -> Manage teams        (find and own a team)
  -> Meetings -> Meeting policies (recording, lobby, sharing)
  -> Users -> Guest access        (allow/block external guests)
  -> Org-wide settings -> External access
```

**External access** (federation) lets your users chat with people in other Microsoft 365 organisations. **Guest access** lets you add an outside person directly into a team as a guest. They are different switches, and tickets like "I can't add my client to the team" usually trace back to one of them being off.

## SharePoint sites, libraries and sharing

In the SharePoint admin center you manage every site, including the ones created by Teams. The key support concept is **sharing**.

```text
admin.microsoft.com -> SharePoint admin center
  -> Sites -> Active sites        (every site + storage used)
  -> Policies -> Sharing          (tenant external-sharing level)
```

Sharing has two layers. The **tenant** sets the maximum (for example, "Anyone", "New and existing guests", or "Only people in your organisation"), and each **site** can be set equal or more restrictive — never more permissive than the tenant. When someone clicks **Share**, the **link type** matters: a *People in your organisation* link will never work for an external guest. Sharing tickets are almost always a policy level or a wrong link type.

You can also drive this with the SharePoint Online Management Shell:

```powershell
Connect-SPOService -Url https://contoso-admin.sharepoint.com
Get-SPOSite -Limit All | Select Url, Owner, StorageUsageCurrent
Get-SPOSite -Identity https://contoso.sharepoint.com/sites/Sales | Select SharingCapability
```

## OneDrive and the sync client

The **OneDrive sync client** keeps files mirrored between the PC and the cloud. **Known Folder Move (KFM)** redirects the Desktop, Documents, and Pictures folders into OneDrive so they sync automatically and survive a lost laptop. **Files On-Demand** keeps files cloud-only until opened, saving disk space. When sync stalls, check the blue/grey cloud icons, look for a paused client, an over-quota account, or a filename with illegal characters.

## Common tickets and how you fix them

- **"I lost a file."** Check **version history** first (restore an earlier version), then the **site Recycle Bin** (93 days), then the second-stage Recycle Bin.
- **File sync error.** Reset or restart the sync client, confirm the user is signed in, check storage quota, and rename files with `\ / : * ? " < > |`.
- **Can't access a site or team.** Confirm group membership — access follows the **Microsoft 365 group**, not a one-off permission.
- **Sharing not working.** Check tenant and site external-sharing level, then the link type.
- **Orphaned sites and retention.** Deleting a Team deletes its group and SharePoint site together. A **retention policy** may preserve content even after deletion, and a deleted group can be restored within **30 days**.

## Your task

In a test tenant or lab, create a Team, find its backing SharePoint site in the SharePoint admin center, upload a file to a channel, delete it, and restore it from the site Recycle Bin. Then connect with `Connect-SPOService` and run `Get-SPOSite` to list your sites and their sharing capability.
