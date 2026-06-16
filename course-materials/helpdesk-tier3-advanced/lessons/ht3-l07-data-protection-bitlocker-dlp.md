---
course: helpdesk-tier3-advanced
title: 'Data protection: BitLocker, DLP and Purview'
month: 3
monthTitle: Advanced Endpoint Security & Identity
lesson: 7
summary: Protect data across its full lifecycle - at rest, in use and in transit - by combining BitLocker
  drive encryption with Microsoft Purview classification, sensitivity labels and endpoint Data Loss Prevention.
  You will manage encryption from the command line and design controls that block leaks without crippling
  productivity.
objectives:
- Describe how data must be protected at rest, in use and in transit, and which control covers each
- 'Explain BitLocker key concepts: TPM, TPM+PIN, XTS-AES, used-space versus full encryption and recovery
  key escrow'
- Manage and audit BitLocker using manage-bde and the Get-BitLockerVolume cmdlet
- Recover a BitLocker-protected drive using a recovery key escrowed to Entra ID or Active Directory
- Apply Microsoft Purview sensitivity labels and classification to enforce protection that travels with
  the data
- Design endpoint DLP policies that block or audit risky egress while balancing security against user
  productivity
video: ht3-l07-data-protection-bitlocker-dlp.mp4
quiz:
- q: A device uses BitLocker with TPM-only protection. What threat does adding a startup PIN specifically
    mitigate?
  options:
  - A remote attacker brute-forcing the user's domain password
  - An attacker with physical access using cold-boot or DMA attacks to extract keys before the OS loads
  - Malware encrypting files for ransom while the user is logged on
  - An administrator reading the recovery key from Entra ID
  answer: 1
  why: TPM-only unlocks transparently at boot, so a stolen device can be attacked at the pre-boot stage.
    A TPM+PIN requires a secret the attacker does not have, defeating pre-boot key-extraction attacks
    such as cold-boot and certain DMA attacks.
- q: You enable BitLocker on a brand-new laptop and choose 'used disk space only' encryption. What is
    the key trade-off versus full-disk encryption?
  options:
  - Used-space only is faster initially but data previously written to now-free sectors may remain unencrypted
  - Used-space only is unrecoverable if the TPM fails
  - Full encryption does not support XTS-AES
  - Used-space only disables recovery key escrow
  answer: 0
  why: Used-space-only encrypts current data quickly and is ideal for new drives, but on a drive that
    previously held data, blocks marked free may still contain readable remnants. Full encryption is the
    safe choice for any drive that has already been used.
- q: An endpoint DLP policy should stop highly sensitive files leaving via USB but must not block the
    finance team's legitimate exports during month-end close. Which approach best balances this?
  options:
  - Block all USB writes for every user with no exceptions
  - Disable DLP during month-end so exports succeed
  - Start in audit mode, scope by sensitivity label and group, then move to block with override-and-justify
    for the finance group
  - Remove the sensitivity labels from finance files
  answer: 2
  why: Mature DLP rollouts begin in audit to understand real behaviour, target high-value data by label
    and scope to groups, then enforce with a user override that captures business justification - protecting
    data while preserving legitimate work.
- q: Which Microsoft Purview capability classifies content automatically by recognising patterns like
    credit-card numbers, and which learns from examples to recognise categories such as contracts?
  options:
  - Sensitivity labels and retention labels respectively
  - Conditional Access and Intune compliance respectively
  - Sensitive information types and trainable classifiers respectively
  - BitLocker and EFS respectively
  answer: 2
  why: Sensitive information types (SITs) detect known patterns such as card or passport numbers using
    regex and checksums, while trainable classifiers are machine-learning models trained on sample content
    to recognise less structured categories like contracts or source code.
- q: Name the two manage-bde commands you would run to (a) check the encryption status and protection
    state of a volume and (b) list the key protectors on the C drive.
  answer: 'manage-bde -status (optionally with the drive letter, e.g. manage-bde -status C:) for the encryption
    and protection state, and manage-bde -protectors -get C: to list the key protectors on the C drive.'
  why: manage-bde -status reports percentage encrypted, method (XTS-AES) and whether protection is on
    or off; manage-bde -protectors -get enumerates protectors such as TPM, numerical recovery password
    and recovery key, which you need for auditing and recovery.
- q: In one sentence, explain why a sensitivity label provides protection that an endpoint DLP policy
    alone cannot.
  answer: A sensitivity label embeds classification and optional encryption into the file itself, so the
    protection and rights travel with the document wherever it goes - even outside the managed endpoint
    - whereas endpoint DLP only enforces while the file is on a device the policy controls.
  why: Labels apply persistent, content-bound protection (encryption, rights, marking) that follows the
    data across devices and services, while DLP is a perimeter-style control that acts at egress points
    on managed endpoints; the two are complementary, not interchangeable.
resources:
- label: Microsoft Learn - BitLocker overview and requirements
  url: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/
- label: Microsoft Learn - manage-bde command-line reference
  url: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/operations-guide
- label: Microsoft Learn - Learn about sensitivity labels (Microsoft Purview)
  url: https://learn.microsoft.com/en-us/purview/sensitivity-labels
- label: Microsoft Learn - Learn about endpoint data loss prevention
  url: https://learn.microsoft.com/en-us/purview/endpoint-dlp-learn-about
---

## Three states, three controls

Data protection is not one job; it is three. Data is vulnerable **at rest** (sitting on a disk), **in use** (open on a screen, copied to a clipboard), and **in transit** (moving over a network or onto a USB stick). A complete strategy covers all three. **BitLocker** protects data at rest by encrypting the whole volume. **Microsoft Purview sensitivity labels** protect data in use and in transit by binding classification and encryption to the file itself. **Endpoint Data Loss Prevention (DLP)** controls risky egress - copy to USB, upload to cloud, clipboard, print. No single tool is enough; you layer them.

## BitLocker: encryption at rest

**BitLocker** encrypts the entire volume with **XTS-AES** (the modern, tamper-resistant mode, default 128-bit, optionally 256-bit). The encryption key is sealed to the **Trusted Platform Module (TPM)**, a hardware chip that releases the key only if boot integrity is intact. TPM-only unlocks transparently, but adding a **PIN** (TPM+PIN) defeats pre-boot key-extraction attacks against a stolen device.

Two enrolment choices matter. **Used-space-only** encryption is fast and fine for brand-new drives; **full** encryption is mandatory for any drive that has held data, because free sectors can hold readable remnants. Critically, you must **escrow the recovery key** to Entra ID or Active Directory so a locked-out user is never stranded.

In practice you set all of this with an **Intune disk encryption policy** for fleet-wide consistency, then verify on the box:

```powershell
# Quick status and protection state
manage-bde -status C:

# List the key protectors (TPM, numerical recovery password, etc.)
manage-bde -protectors -get C:

# The PowerShell-native equivalent, richer for scripting
Get-BitLockerVolume -MountPoint C: |
  Select-Object MountPoint, VolumeStatus, EncryptionMethod,
    ProtectionStatus, EncryptionPercentage
```

## BitLocker recovery

When the TPM measurements change - a firmware update, a BIOS change, a moved disk - BitLocker enters **recovery mode** and demands the 48-digit numerical password. Because you escrowed it, you retrieve it from Entra ID or AD and unlock:

```text
manage-bde -unlock C: -RecoveryPassword 123456-...-654321
manage-bde -protectors -disable C:   # suspend during planned firmware work
```

Suspend (not decrypt) protection before TPM-affecting maintenance so the device boots without prompting, then resume.

## Purview: classification and labels

Protection at rest is not enough once a file leaves the disk. **Microsoft Purview Information Protection** classifies content using **sensitive information types (SITs)** - pattern detectors for things like card or passport numbers - and **trainable classifiers**, machine-learning models trained on examples to spot fuzzy categories such as contracts. A **sensitivity label** (for example *Confidential*) then applies persistent encryption, rights and visual marking that **travel with the file** anywhere.

## Endpoint DLP and the productivity balance

**Endpoint DLP** enforces policy at egress points on managed devices: block or audit **copy to USB, upload to cloud, clipboard paste, and print**. Combined with labels, DLP can say "a *Confidential*-labelled file may not be written to removable media". The art is balance: blunt blocking breeds shadow IT and **insider risk**. Mature rollouts start in **audit**, scope by label and group, then enforce with a **block-with-override** that captures user justification - protecting **PII** without stopping legitimate work.

## Your task

In a test tenant, create an Intune disk encryption policy that enforces XTS-AES with TPM+PIN and escrows the recovery key to Entra ID. On an enrolled device, confirm the result with `manage-bde -status` and `Get-BitLockerVolume`, then deliberately trigger recovery (change a boot setting) and recover using the escrowed key. Finally, publish one sensitivity label and build an endpoint DLP policy in audit mode that flags that label being copied to USB; review the audit events and write a one-page plan for moving it to block-with-override without disrupting a named business workflow.
