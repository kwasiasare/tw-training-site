---
course: helpdesk-tier1-2
title: Backup, recovery and imaging
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 7
summary: Learn the backup strategies a technician relies on, how to restore user data with File History
  and recover a system with wbadmin, and how imaging lets you rebuild a machine fast.
objectives:
- Explain the 3-2-1 backup rule and why it matters
- Tell the difference between a file backup, a system image, and a recovery point
- Restore user files with File History
- Create and restore a system image backup with wbadmin
- Describe how disk imaging speeds up rebuilding many machines
- Decide which recovery method fits a given failure
video: hd3-l07-backup-recovery-imaging.mp4
quiz:
- q: What does the 3-2-1 backup rule recommend?
  options:
  - 3 passwords, 2 admins, 1 firewall
  - 3 copies of data, on 2 different media, with 1 copy off-site
  - 3 backups per day on 1 drive
  - 3 antivirus scans before every backup
  answer: 1
  why: 3-2-1 means keep three copies of your data, on two different types of media, with at least one
    copy stored off-site, so a single failure or disaster can't wipe everything.
- q: A user deleted a single document yesterday and needs it back. Which is the quickest appropriate tool
    on Windows?
  options:
  - A full system image restore
  - Reinstalling Windows
  - File History
  - Repartitioning the disk
  answer: 2
  why: File History keeps versioned copies of user files, so a single deleted or changed document can
    be restored quickly without touching the rest of the system.
- q: What is the main advantage of a system image over a file-only backup?
  options:
  - It is smaller and faster to create
  - It restores the whole OS, apps and settings as one unit
  - It only saves documents
  - It runs without any storage
  answer: 1
  why: A system image is a block-level snapshot of the whole drive, so restoring it brings back the operating
    system, installed applications and settings together — ideal after a disk failure.
- q: Which command creates a system image backup on Windows?
  options:
  - wbadmin start backup
  - sfc /scannow
  - chkdsk /f
  - diskpart clean
  answer: 0
  why: wbadmin start backup creates a backup including a system image; the others repair files, check
    the disk, or wipe a disk respectively.
- q: In one sentence, explain why imaging is useful when setting up many identical computers.
  answer: You configure one machine perfectly, capture it as an image, and deploy that single image to
    many computers so they all start identical without repeating the setup each time.
  why: Imaging captures a known-good build once and clones it to many devices, saving hours and guaranteeing
    consistency across a fleet.
- q: Why should at least one backup copy be kept off-site or offline?
  answer: So that a local disaster such as fire, theft, or ransomware that encrypts everything reachable
    on the network cannot destroy every copy of the data at once.
  why: An off-site or offline copy is isolated from local failures and online threats, which is the whole
    point of the '1' in the 3-2-1 rule.
resources:
- label: Microsoft Support — Back up and restore with File History
  url: https://support.microsoft.com/en-us/windows/back-up-your-windows-pc-87a81f8a-78fa-456e-b521-ac0560e32338
- label: Microsoft Learn — wbadmin command reference
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin
- label: Microsoft Learn — Recovery options in Windows
  url: https://learn.microsoft.com/en-us/windows/client-management/system-failure-recovery-options
- label: CompTIA — A+ certification
  url: https://www.comptia.org/certifications/a
---

## Backups exist for the bad day

Nobody appreciates a backup until a disk dies, a laptop is stolen, or ransomware locks every file. As a technician your job is to make sure that bad day is survivable. That means knowing the difference between backing up **files**, backing up a whole **system image**, and being able to **recover** when something fails. Get this right and a catastrophic failure becomes an inconvenience.

## The 3-2-1 rule

The industry shorthand is **3-2-1**: keep **3 copies** of your data, on **2 different media** (for example an internal disk and an external drive or cloud), with at least **1 copy off-site or offline**. The off-site copy is what saves you from fire, theft, or ransomware that encrypts everything it can reach on the network. A backup that sits next to the original on the same machine is barely a backup at all.

## File backups vs system images

There are two flavours you must keep straight. A **file backup** copies documents, photos and settings — small, frequent, easy to restore one item from. A **system image** is a block-level snapshot of the entire drive: operating system, installed apps and settings as one unit. You restore a file backup to get a document back; you restore an image to rebuild a whole machine after a disk failure.

On Windows, **File History** handles versioned file backups:

```powershell
# File History is configured in Settings, but you can drive the engine
FileHistory
# Check status from PowerShell
Get-WindowsFeature -Name FS-Data-Deduplication | Format-Table -AutoSize
```

To restore a single file, open **File History** from Control Panel, browse to the file, pick a version, and click the green restore button.

## System image with wbadmin

For a full image, `wbadmin` is the built-in command-line tool. Run it from an **elevated** prompt:

```cmd
:: Create a system image of C: onto drive E:
wbadmin start backup -backupTarget:E: -include:C: -allCritical -quiet

:: List the backups you have
wbadmin get versions
```

Sample output:

```cmd
Backup time: 16/06/2026 09:14
Backup target: Fixed Disk labelled E:
Version identifier: 06/16/2026-08:14
Can recover: Volume(s), File(s), Application(s), Bare Metal Recovery, System State
```

To recover a whole system, boot into the **Windows Recovery Environment** and choose **System Image Recovery**, pointing it at the image you created.

## Imaging for fleets

**Imaging** takes the system-image idea and scales it. You configure one machine perfectly — the **gold image** — capture it, then deploy that single image to many computers so they all start identical. Tools like DISM capture and apply Windows images (`.wim` files):

```powershell
DISM /Capture-Image /ImageFile:D:\gold.wim /CaptureDir:C:\ /Name:"Gold build"
```

This is how IT departments rebuild a broken laptop in twenty minutes instead of a day.

## Your task

On a test or virtual machine: turn on **File History** to an external or second drive, create a test document, then delete it and restore the previous version. Next, from an elevated prompt run `wbadmin get versions` to inspect any system backups present (or create one with `wbadmin start backup` if you have a spare target). Finally, write two or three sentences mapping each of these failures to the right recovery method: a single deleted file, a dead boot drive, and rebuilding ten identical machines.
