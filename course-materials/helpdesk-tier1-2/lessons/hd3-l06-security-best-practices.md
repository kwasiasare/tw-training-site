---
course: helpdesk-tier1-2
title: 'Security best practices: passwords, MFA & encryption'
month: 3
monthTitle: Windows, OS Support & Security (A+ Core 2)
lesson: 6
summary: 'Learn the everyday security controls a Tier 1 technician enforces: strong password and account
  policies, multi-factor authentication, and full-disk encryption with BitLocker.'
objectives:
- Explain why length and uniqueness beat complexity in modern password policy
- Configure local account and lockout policies from the command line
- Describe how multi-factor authentication stops stolen-password attacks
- Enable and check BitLocker full-disk encryption with manage-bde
- Save and use a BitLocker recovery key during a lockout
- Apply the principle of least privilege to user accounts
video: hd3-l06-security-best-practices.mp4
quiz:
- q: Which password policy gives the best real-world protection against guessing and reuse attacks?
  options:
  - Force a change every 30 days with three special characters
  - Require long, unique passphrases and screen against known-breached passwords
  - Require exactly eight characters with one capital letter
  - Disable lockout so users never get blocked
  answer: 1
  why: Modern guidance (NIST and Microsoft) favours length and uniqueness over forced rotation and arbitrary
    complexity, and blocking known-breached passwords stops reuse attacks.
- q: A user's password was phished. What single control would most likely have stopped the attacker from
    logging in?
  options:
  - Multi-factor authentication
  - A longer password
  - Disk encryption
  - A faster antivirus scan
  answer: 0
  why: MFA requires a second factor the attacker does not have, so a stolen password alone is not enough
    to sign in.
- q: What does BitLocker protect against?
  options:
  - Phishing emails
  - Weak network passwords
  - Data being read from a lost or stolen drive
  - Browser pop-ups
  answer: 2
  why: BitLocker provides full-disk encryption, so data on a lost or stolen drive cannot be read without
    the key or recovery key.
- q: Which command shows the encryption status of all drives on a Windows machine?
  options:
  - 'manage-bde -lock C:'
  - gpupdate /force
  - manage-bde -status
  - net user
  answer: 2
  why: manage-bde -status reports protection status, encryption percentage and method for each volume;
    the other commands lock, refresh policy, or list users.
- q: In one sentence, define the principle of least privilege and give one example.
  answer: Least privilege means giving each user only the access they need to do their job and nothing
    more — for example, making a normal user a standard account instead of a local administrator.
  why: Limiting privileges shrinks the damage an attacker or mistake can cause, which is why standard
    accounts are the default and admin rights are granted only when needed.
- q: Why should you save the BitLocker recovery key somewhere other than the encrypted machine itself?
  answer: If you are locked out (for example after a TPM or firmware change) you need the recovery key
    to unlock the drive, and it is useless if it is stored only on the drive you cannot access.
  why: The recovery key is the fallback when normal unlock fails, so it must live somewhere independent
    — a Microsoft account, Azure AD, a printout, or a USB key kept elsewhere.
resources:
- label: Microsoft Learn — BitLocker overview
  url: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/
- label: Microsoft Support — How to use multi-factor authentication
  url: https://support.microsoft.com/en-us/account-billing/how-to-use-the-microsoft-authenticator-app-9783c865-0308-42fb-a519-8cf666fe0acc
- label: Microsoft Learn — manage-bde command reference
  url: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/manage-bde
- label: CompTIA — A+ certification
  url: https://www.comptia.org/certifications/a
---

## Why security is a Tier 1 job

Most breaches do not start with a clever hacker; they start with a weak password, a reused password, or a laptop left on a train. As a helpdesk technician you are the person who actually turns the controls on. Three controls cover the majority of real risk: strong **authentication**, **multi-factor authentication (MFA)**, and **encryption**. Learn these and you protect both the user and the business.

## Passwords and account policy

Forget the old advice about swapping letters for symbols every month. Modern guidance favours **length and uniqueness**: a long **passphrase** is both stronger and easier to remember than `P@ss1!`. You also want an **account lockout** so attackers cannot guess endlessly, and you want to follow **least privilege** — give users a standard account, not local administrator, unless they genuinely need it.

You can inspect and set local policy from the command line:

```cmd
net accounts
:: Lockout threshold: Never  -> set it
net accounts /lockoutthreshold:5 /lockoutduration:15

:: List local users and check who is an admin
net user
net localgroup administrators
```

Sample output:

```cmd
Lockout threshold:                 5
Lockout duration (minutes):        15
```

## Multi-factor authentication

A password is **something you know**. MFA adds **something you have** (a phone or token) or **something you are** (a fingerprint). Even if a password is phished, the attacker cannot complete the login without the second factor. As a technician you will help users enrol in an authenticator app, generate **backup codes**, and recover when a device is lost. The key teaching point for users: approve a prompt **only** when you are the one signing in.

## Full-disk encryption with BitLocker

**BitLocker** encrypts the whole drive so a lost or stolen laptop is just an expensive paperweight, not a data leak. On business machines it usually relies on the **TPM** chip to release the key automatically at boot. Check and enable it with `manage-bde`:

```powershell
# Check status of every drive
manage-bde -status

# Turn BitLocker on for C: and save the recovery key to a file
manage-bde -on C: -recoverypassword
```

Sample output:

```powershell
Volume C: [OSDisk]
    Conversion Status:    Used Space Only Encrypted
    Percentage Encrypted: 100.0%
    Protection Status:    Protection On
```

## Recovery keys — do not skip this

If the TPM, firmware, or boot configuration changes, BitLocker demands the **recovery key**. Save it somewhere off the machine: a Microsoft account, Azure AD/Entra, a printout, or a USB stick stored elsewhere. A recovery key locked inside the drive you cannot open is worthless.

```powershell
# Show the numeric recovery password / key protectors
manage-bde -protectors -get C:
```

## Your task

On a test or virtual machine: run `net accounts` and set a lockout threshold of 5 attempts; confirm the change. Then run `manage-bde -status` to record the encryption state of C:. If BitLocker is available, capture the recovery key with `manage-bde -protectors -get C:` and write where you would store it safely. Summarise in three bullet points how passwords, MFA and encryption each protect a different stage of an attack.
