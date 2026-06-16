---
course: helpdesk-tier1-2
title: User accounts, groups and NTFS permissions
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 3
summary: Understand how Windows controls who can do what, from account types and groups to NTFS file permissions.
  By the end you can create accounts, place users in the right groups and fix 'access denied' problems.
objectives:
- Distinguish standard, administrator and guest account types
- Explain why groups make permissions manageable at scale
- Compare NTFS permissions with simpler share permissions
- Apply the principle of least privilege to everyday support
- Use net user and icacls to inspect and change access from the terminal
- Diagnose a common 'access denied' problem and explain the cause
video: hd3-l03-accounts-groups-ntfs-permissions.mp4
quiz:
- q: A user needs to install printer drivers but keeps getting blocked. Their account is the wrong type.
    Which account type can install most software and change system settings?
  options:
  - Guest
  - Standard user
  - Administrator
  - Service account
  answer: 2
  why: An Administrator account can install software and change system-wide settings. Standard users are
    deliberately limited for safety, and Guest is the most restricted of all.
- q: Why do organisations assign permissions to groups rather than to individual users?
  options:
  - Groups make files smaller
  - It is the only way Windows allows access
  - 'It scales: change one group instead of hundreds of users'
  - Groups encrypt the data automatically
  answer: 2
  why: Assigning rights to a group and then adding users to that group means you manage access in one
    place. When someone changes role you move them between groups instead of editing every file.
- q: A file is shared on the network. The share permission allows Full Control but the NTFS permission
    only allows Read. What can a remote user actually do?
  options:
  - Full Control — share wins
  - Read only — the most restrictive of the two applies
  - Nothing at all
  - Modify — Windows averages them
  answer: 1
  why: When share and NTFS permissions combine, the most restrictive effective permission wins. Read on
    NTFS caps the remote user at Read even though the share allows Full Control.
- q: Which command-line tool displays and changes NTFS permissions on files and folders?
  options:
  - icacls
  - net user
  - gpresult
  - tasklist
  answer: 0
  why: icacls views and modifies NTFS access control lists (ACLs). net user manages accounts, gpresult
    reports Group Policy, and tasklist lists processes.
- q: In one sentence, what is the principle of least privilege and why does it matter on a helpdesk?
  answer: Give each user only the access they need to do their job and no more, so a mistake or compromised
    account can do the least possible damage.
  why: 'Least privilege limits blast radius: standard users by default, elevation only when justified.
    It is a core security expectation in the A+ objectives.'
- q: In one sentence, what does the command 'net user jsmith /add' do, and what should you usually do
    next?
  answer: It creates a new local user account named jsmith; next you would set a password and add the
    account to the appropriate group with net localgroup.
  why: net user /add creates the account, but a new account needs a password and group membership before
    it is genuinely useful and secure.
resources:
- label: Microsoft Learn — icacls command reference
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls
- label: Microsoft Learn — net user command reference
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-user
- label: Microsoft Support — Create a local user or administrator account in Windows
  url: https://support.microsoft.com/en-us/windows/create-a-local-user-or-administrator-account-in-windows-20de74e0-ac7f-3502-a866-32915af2a34d
- label: CompTIA — A+ Core 2 (220-1102) exam objectives
  url: https://www.comptia.org/certifications/a
---

## Who are you? Account types

Every action in Windows happens under a **user account**, and the **account type** decides what that user may do. A **standard user** can run apps and change their own settings but cannot make system-wide changes. An **administrator** can install software, change system settings and manage other accounts. The **guest** account is heavily restricted and usually disabled. The safe default for everyday work is a **standard** account; elevate only when a task truly needs it.

You can inspect and create accounts from the terminal:

```powershell
net user                       # list local accounts
net user jsmith P@ssw0rd! /add # create an account
net localgroup Administrators jsmith /add
```

## Groups: permissions that scale

Imagine setting permissions on a thousand files for fifty users — then someone leaves. Painful. Instead, Windows uses **groups**. You grant access to a **group** (say *Accounting*), then add users to that group. Change a person's role and you simply move them between groups; the files never change. Common built-in groups include **Administrators**, **Users** and **Guests**.

```cmd
net localgroup Accounting /add
net localgroup Accounting jsmith /add
```

## NTFS vs share permissions

There are two permission systems and the A+ exam loves the difference. **Share permissions** apply only when a folder is reached *over the network*. **NTFS permissions** apply *always* — locally and remotely — and are far more granular (Read, Write, Modify, Full Control, and more).

The golden rule: when both apply, the **most restrictive** effective permission wins. If the share says Full Control but NTFS says Read, a remote user gets **Read**. Because NTFS always applies, it is the system you'll tune most.

```cmd
icacls C:\Reports
C:\Reports BUILTIN\Administrators:(F)
         CONTOSO\Accounting:(M)
         BUILTIN\Users:(R)
```

The letters mean Full control (F), Modify (M), Read (R), and Write (W).

## Changing access with icacls

When a user genuinely needs more access, grant it to the right group, not the individual, and only the level required:

```cmd
icacls C:\Reports /grant CONTOSO\Accounting:(OI)(CI)M
```

The `(OI)(CI)` flags mean the permission is inherited by files and subfolders inside the folder. Always prefer Modify over Full Control unless the user must change permissions themselves.

## Least privilege and 'access denied'

The **principle of least privilege** says: give each user only the access they need, and no more. It is the single most effective everyday security habit, because a mistake or a hijacked account can then do far less harm.

Most **access denied** tickets come down to one of three things: the user is in the wrong group, an NTFS permission is too restrictive, or they didn't run a tool **as administrator**. Check group membership first (`whoami /groups`), then the folder's NTFS permissions, then elevation.

## Your task

On a test PC (or a VM), open an elevated terminal. Run `net user` to list accounts and `whoami /groups` to see your own group memberships. Create a folder `C:\Lab`, then run `icacls C:\Lab` to read its current permissions and identify which groups have Read versus Modify. Write three lines explaining who can do what, and which single group you would add to give your imaginary 'Accounting' team Modify access without touching individual users.
