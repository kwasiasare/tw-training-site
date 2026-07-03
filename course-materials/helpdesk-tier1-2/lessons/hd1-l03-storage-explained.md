---
course: helpdesk-tier1-2
title: 'Storage explained: HDD vs SSD, partitions & file systems'
month: 1
monthTitle: PC Hardware & How Computers Work (A+ Core 1)
lesson: 3
summary: 'Learn how computers store files for the long term: the difference between hard drives and solid-state
  drives, the shapes and connectors they come in, and how partitions and file systems turn a raw disk
  into usable drive letters.'
objectives:
- Explain the difference between an HDD and an SSD and when each is used
- Identify common drive form factors and connectors (2.5", M.2, SATA, NVMe)
- Describe what a partition is and tell GPT apart from MBR
- Match common file systems (NTFS, exFAT, FAT32, ext4) to the right job
- Explain what formatting does and how a drive becomes a drive letter
- View disks, volumes and partitions safely using built-in Windows tools
video: hd1-l03-storage-explained.mp4
quiz:
- q: Which statement best describes an SSD compared with a traditional HDD?
  options:
  - It uses spinning platters and a moving read/write head
  - It stores data in flash memory with no moving parts and is much faster
  - It is always cheaper per gigabyte than an HDD
  - It can only be used for the operating system, never for files
  answer: 1
  why: An SSD uses flash memory chips with no moving parts, so it is far faster and more shock-resistant
    than an HDD, which relies on spinning platters and a mechanical head.
- q: What does the RPM rating on a hard drive (HDD) tell you?
  options:
  - How fast the platters spin, which affects performance
  - How many gigabytes it holds
  - How many partitions it supports
  - The voltage it needs
  answer: 0
  why: RPM means revolutions per minute. Faster-spinning platters (e.g. 7200 RPM vs 5400 RPM) generally
    read and write data quicker on a mechanical HDD.
- q: 'An M.2 NVMe drive is faster than a 2.5" SATA SSD mainly because:'
  options:
  - It is physically larger
  - It connects over the PCI Express bus instead of the slower SATA bus
  - It uses spinning platters
  - It needs no power
  answer: 1
  why: NVMe drives talk to the system over the high-speed PCIe lanes, which carry far more data per second
    than the older SATA interface used by 2.5" SATA SSDs.
- q: Which partitioning scheme supports drives larger than 2 TB and more than four primary partitions?
  options:
  - MBR
  - FAT32
  - GPT
  - RAID
  answer: 2
  why: GPT (GUID Partition Table) is the modern scheme that handles drives over 2 TB and many partitions.
    The older MBR scheme is capped at 2 TB and four primary partitions.
- q: Name the default file system Windows uses for its system drive, and give one reason it is chosen.
  answer: NTFS, because it supports large files, security permissions, and journaling that helps recover
    from crashes.
  why: NTFS is the standard Windows file system; its permissions and journaling make it reliable and secure
    for the operating system and most internal drives.
- q: In one sentence, what does formatting a drive actually do, and why must you be careful?
  answer: Formatting writes a fresh, empty file system onto a partition, which erases the data that was
    there, so you must always confirm you have selected the correct disk.
  why: Formatting prepares a volume for use but wipes existing files, so picking the wrong disk in a tool
    like Disk Management or diskpart can destroy data permanently.
resources:
- label: CompTIA A+ Certification (220-1201 / 220-1202)
  url: https://www.comptia.org/certifications/a
- label: Microsoft Learn — Overview of Disk Management
  url: https://learn.microsoft.com/en-us/windows-server/storage/disk-management/overview-of-disk-management
- label: 'Crucial — SSD vs HDD: What''s the difference?'
  url: https://www.crucial.com/articles/about-ssd/ssd-vs-hdd
- label: Wikipedia — NTFS file system
  url: https://en.wikipedia.org/wiki/NTFS
---

## Why storage matters

Your computer has two kinds of memory. **RAM** is fast but forgets everything when the power goes off. **Storage** is the slower, permanent home for your operating system, programs, and files — it keeps your data even when the PC is switched off. On a helpdesk, you will swap drives, clone systems, and explain to users why their old PC "feels slow." Very often the answer is the drive.

## HDD vs SSD

A **hard disk drive (HDD)** stores data on spinning magnetic **platters**. A tiny mechanical arm with a read/write **head** moves across the platter to find your data. The platters spin at a fixed speed measured in **RPM** (revolutions per minute) — commonly 5400 or 7200. Because parts physically move, HDDs are slower, noisier, and more fragile, but they are **cheap and come in huge capacities**, which makes them great for bulk storage and backups.

A **solid-state drive (SSD)** stores data in **flash memory** chips. There are **no moving parts**, so it is dramatically faster, silent, cooler, and far more resistant to bumps. Swapping an old HDD for an SSD is the single biggest speed upgrade you can give most computers. The trade-off is a higher cost per gigabyte.

## Form factors and connectors

Drives come in different shapes (**form factors**) and use different connectors:

- **2.5\" SATA** — a small rectangular drive that connects with a **SATA** cable. Both HDDs and SSDs use this shape.
- **M.2** — a thin stick that plugs flat onto the motherboard. Pronounced "em dot two."
- **SATA vs NVMe** — the connector is only half the story. A 2.5\" SSD or some M.2 drives use the older **SATA** bus. Faster M.2 drives use **NVMe**, which runs over the high-speed **PCIe** lanes and is many times quicker.

## Partitions: GPT vs MBR

A raw drive is just empty space. A **partition** is a section of the drive treated as a separate unit. One physical disk can hold several partitions. The **partition table** records this layout, and there are two schemes:

- **MBR (Master Boot Record)** — older, limited to **2 TB** and four **primary** partitions.
- **GPT (GUID Partition Table)** — modern, supports huge drives and many partitions. Required for UEFI boot.

## File systems and formatting

A partition still needs a **file system** — the rulebook for how files are stored and named. Common ones:

- **NTFS** — Windows default; permissions, large files, journaling.
- **exFAT** — great for large external/USB drives shared between Windows and Mac.
- **FAT32** — old and simple; can't hold files over 4 GB.
- **ext4** — the common Linux file system.

**Formatting** writes a fresh, empty file system onto a partition — and erases what was there. Once formatted, Windows assigns a **drive letter** (like `C:` or `D:`) so you can use it.

## Viewing drives safely

You can inspect storage without changing anything. Open PowerShell and run these read-only commands:

```powershell
Get-Disk
Get-Volume
Get-Partition
```

You can also open **Disk Management** (`diskmgmt.msc`) for a visual map. The command-line tool **diskpart** can also list disks read-only:

```text
diskpart
list disk
list volume
exit
```

**Warning:** never run format, clean, or delete commands unless you are 100% sure of the disk number. Selecting the wrong disk wipes it permanently.

## Your task

Open PowerShell on your PC and run `Get-Disk`, then `Get-Volume`, then `Get-Partition`. Write down, for your main drive: is it an HDD or SSD, what file system does it use (look at the `Get-Volume` output), and what drive letter is it? Then open Disk Management (`diskmgmt.msc`) and confirm your findings visually — without changing anything.
