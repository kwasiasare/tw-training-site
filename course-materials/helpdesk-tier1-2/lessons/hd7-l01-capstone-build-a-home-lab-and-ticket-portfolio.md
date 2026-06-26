---
course: helpdesk-tier1-2
title: 'Capstone: Build a Home Lab and Ticket Portfolio'
month: 7
monthTitle: Capstone & Career Launch
lesson: 1
summary: 'This capstone turns six months of study into evidence you can show an employer. You will build
  a small but real home lab: a Windows client and a domain controller running Active Directory inside
  free virtual machines, plus a Microsoft 365 / Microsoft Entra tenant with Intune so you can practice
  modern, cloud-joined management. You will then work a set of realistic tickets end to end and write
  each one up as a runbook or knowledge-base article. The deliverable is a documented lab and five to
  ten resolved-ticket write-ups that prove, with screenshots and clear steps, that you can do Tier 1 and
  Tier 2 work. A simple rubric tells you when each piece is portfolio ready.'
objectives:
- Stand up a free home lab with a Windows client and an Active Directory domain controller in virtual
  machines
- Provision a Microsoft 365 / Entra tenant with Intune and enrol a test device for modern management
- Work realistic Tier 1 and Tier 2 tickets end to end and capture each fix as you go
- Write resolved tickets as runbooks and knowledge-base articles with clear, repeatable steps
- Capture clean screenshots and document the problem, steps, and verification for each task
- Judge your own work against a portfolio rubric so every artifact is interview ready
video: hd7-l01-capstone-build-a-home-lab-and-ticket-portfolio.mp4
quiz:
- q: Why does a documented home lab help a career-changer with no paid experience get hired?
  options:
  - It replaces the need for any certifications
  - It is demonstrable, hands-on proof you can do the work, which an employer can verify in minutes
  - It guarantees a specific salary
  - It lets you skip the interview entirely
  answer: 1
  why: For someone moving into a first IT role, a self-built, documented lab is legitimate, verifiable
    experience. It shows you can actually stand up and support real systems, not just pass a multiple-choice
    exam, which is exactly what a hiring manager needs to see.
- q: What is the most accurate statement about getting a free Microsoft 365 developer tenant in 2026?
  options:
  - Anyone can still get a free E5 developer sandbox with no conditions
  - Microsoft 365 cannot be tried at all without buying licenses
  - The free E5 developer sandbox is now restricted (for example to Visual Studio Professional/Enterprise
    subscribers or partner-program orgs), so a 30-day Microsoft 365 / Intune trial is the reliable free
    alternative
  - You must run Microsoft 365 on your own servers
  answer: 2
  why: Since January 2024 Microsoft restricted the free Microsoft 365 E5 developer sandbox to eligible
    groups such as Visual Studio Professional/Enterprise subscribers and certain partners. If you do not
    qualify, a 30-day Microsoft 365 Business Premium or Enterprise trial gives you a real Entra tenant
    and Intune to practice in.
- q: In this lab, what is the simplest free way to practice on-premises Active Directory?
  options:
  - Install Windows Server and Windows client evaluation editions as virtual machines and promote the
    server to a domain controller
  - Buy a rack of physical servers
  - Active Directory cannot be run outside a real company
  - Use a public website that pretends to be a domain
  answer: 0
  why: Microsoft provides free time-limited evaluation ISOs for Windows Server and Windows. Running them
    as VMs (Hyper-V, VirtualBox, or VMware Workstation) and promoting the server with the AD DS role gives
    you a real domain controller to practice users, groups, and Group Policy at no cost.
- q: What turns a fixed ticket into a useful portfolio artifact?
  options:
  - A single screenshot with no words
  - A long story with no steps anyone could repeat
  - Only the final 'resolved' status
  - A write-up with the problem, the environment, the numbered steps you took, the verification, and the
    result
  answer: 3
  why: A runbook or KB article is valuable because someone else could follow it. Stating the problem,
    the environment, the exact steps, how you verified the fix, and the outcome makes the work repeatable
    and shows your troubleshooting method, which is what employers and teammates rely on.
- q: Which task best demonstrates Tier 2 (rather than Tier 1) capability in your lab?
  options:
  - Resetting a forgotten password for one user
  - Creating a Group Policy or Intune configuration profile to enforce a setting across all devices and
    confirming it applied
  - Plugging in a monitor
  - Reading a knowledge-base article
  answer: 1
  why: Tier 1 handles single-user, well-documented fixes like password resets. Tier 2 owns configuration
    and root-cause work, such as authoring a Group Policy Object or an Intune profile that affects many
    devices and verifying it deployed correctly, which is the deeper skill the rubric rewards.
- q: List the five sections every resolved-ticket write-up in your portfolio should contain.
  answer: Problem/symptom, environment (OS, AD or Intune, device), the numbered troubleshooting and resolution
    steps, verification (how you proved it was fixed), and the outcome/result, ideally with a screenshot
    or two and any preventive note.
  why: 'Those five sections turn a one-off fix into a repeatable runbook: they show the context, your
    method, proof of success, and the result, which is exactly the structure a hiring manager and a real
    service desk knowledge base expect.'
resources:
- label: Microsoft 365 Developer Program (sandbox eligibility and sign-up)
  url: https://developer.microsoft.com/en-us/microsoft-365/dev-program
- label: Set up a Microsoft 365 developer sandbox subscription (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/office/developer-program/microsoft-365-developer-program-get-started
- label: Microsoft Evaluation Center (free Windows and Windows Server evaluation ISOs)
  url: https://www.microsoft.com/en-us/evalcenter/
- label: Active Directory Domain Services overview (Microsoft Learn)
  url: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview
---

## Why a Capstone, and Why Now

You have learned hardware, networking, Windows, the helpdesk craft, Intune, and Microsoft 365. The problem every career-changer faces next is the same: employers ask for experience, and you are trying to get your first job. The fix is to manufacture real, demonstrable experience in a lab you control. This capstone has two deliverables: a documented home lab that mirrors a small business, and a set of five to ten resolved-ticket write-ups (runbooks and knowledge-base articles). Together they let a hiring manager verify, in a few minutes, that you can actually do Tier 1 and Tier 2 support, not just pass an exam.

## Part 1: Build the Lab

Your lab should cover both worlds a modern technician supports: traditional on-premises Active Directory and cloud-based Microsoft 365 with Intune. Everything here is free or trial-based.

**The on-prem side (virtual machines).** Install a hypervisor you already have access to: Hyper-V (built into Windows Pro), Oracle VirtualBox (free), or VMware Workstation. Download the free, time-limited evaluation ISOs from the Microsoft Evaluation Center: one Windows Server and one Windows 11 client. Build two VMs. On the server, add the Active Directory Domain Services role and promote it to a domain controller, creating a domain such as `lab.local`. Now you have the real thing: create organizational units, users, and security groups; write a Group Policy Object that, for example, sets a desktop background or enforces a password policy; then join the Windows 11 client to the domain and confirm a user can sign in and that the policy applied. This single exercise touches DNS, DHCP, authentication, and Group Policy, the backbone of countless Tier 2 tickets.

**The cloud side (Entra + Intune).** You want a real Microsoft Entra tenant with Intune. The cleanest option used to be the Microsoft 365 Developer Program sandbox, but since January 2024 the free E5 sandbox is restricted to eligible groups (for example Visual Studio Professional or Enterprise subscribers and certain Microsoft partners). If you qualify, use it. If you do not, sign up for a 30-day Microsoft 365 Business Premium or Enterprise trial, which still gives you Entra ID, the Microsoft 365 admin center, and Intune. In the tenant, create a few test users, assign licenses, build an Intune compliance policy and a configuration profile, and enrol a test Windows VM. If you can, try a simple Windows Autopilot or app-deployment flow. This mirrors how real organizations now manage cloud-joined devices.

**Keep it lightweight.** You do not need a huge environment. Two on-prem VMs and one cloud tenant with a couple of users is plenty to generate dozens of realistic tickets. Snapshot your VMs before big changes so you can break things safely and roll back.

## Part 2: Work Tickets End to End

A lab is only half the story; the portfolio comes from using it. Give yourself a backlog of realistic tickets and resolve each one properly. Good starter tickets, drawn from real Tier 1 and Tier 2 queues:

- A user is locked out / forgot their password (reset in AD and in Entra; explain the difference).
- New-hire onboarding: create the AD user, add to the right groups, assign an M365 license, and confirm sign-in.
- A shared folder shows access denied (diagnose NTFS vs. share permissions and group membership).
- A laptop is not getting this month's updates (check Windows Update for Business / Intune update rings).
- A device shows as non-compliant in Intune (find the failing setting and remediate).
- Outlook keeps prompting for a password (work through the standard mail-flow and identity checks).
- Map a network drive for a department via Group Policy and verify it applied.
- A printer is offline for one user but not others (isolate the layer).

For each, follow the troubleshooting methodology from Module 4: gather information, establish a probable cause, test, fix, verify, and document. The documentation step is what creates your portfolio, so capture it as you go, not from memory afterward.

## Part 3: Write It Up

Every resolved ticket becomes a runbook or knowledge-base article with the same five sections:

1. **Problem / symptom** in the user's words and the technical reality.
2. **Environment** (Windows 11 client, AD domain or Entra-joined, Intune-managed, etc.).
3. **Steps** you took, numbered, so someone else could repeat them.
4. **Verification**, how you proved it was actually fixed (the policy applied, the user signed in, the alert cleared).
5. **Outcome / result**, plus any preventive note (for example, add the group to onboarding).

Add one or two clean screenshots per article: the policy you created, the before/after state, the verification. Redact anything that even looks like a real password or personal data. Write in plain, confident language, the same way a real service desk KB reads, because clear writing is itself a Tier 2 skill employers value.

## The Rubric: When Is It Portfolio Ready?

Use this rubric to judge each artifact before you call it done:

- **Reproducible (40%)** Could a stranger follow your steps and get the same result? Numbered steps, exact setting names, real screenshots.
- **Correct and safe (25%)** Is the fix the right root-cause fix, not a guess, and did you avoid bad practice (no shared admin passwords, least privilege respected)?
- **Verified (15%)** Did you prove it worked, not just assume it?
- **Clear writing (10%)** Plain English, no jargon dumps, sensible structure.
- **Professional polish (10%)** Consistent format, redacted secrets, tidy screenshots, a one-line summary at the top.

Aim for five to ten write-ups that each score well, with at least two clearly demonstrating Tier 2 depth (a Group Policy Object or an Intune profile that affects many devices, with verification). Quality beats quantity: ten polished, repeatable articles outperform thirty rushed ones.

## Make It Resemble a Real Workplace

The more your lab mirrors a small business, the more transferable your evidence becomes. Give your test users realistic names and departments, sales, finance, operations, and build security groups that match (for example a Finance group that controls access to a finance share). Set a naming convention for devices, such as LAB-WS01, the way real fleets do. When you create a Group Policy or an Intune profile, write down the business reason in one line, not just the setting, because that is the thinking an interviewer probes. Snapshot your virtual machines before each major change so you can deliberately break something, watch it fail, and practice the fix, that failure-and-recovery cycle is where real troubleshooting skill is built. Revisit the lab every week or two as well: tenants and trials change and settings drift, so keeping it current means your screenshots and runbooks stay accurate when a hiring manager asks you to walk through one live.

## Your Deliverable

By the end of this lesson you should have a running lab (two on-prem VMs with AD plus a cloud tenant with Intune), a backlog you worked through, and a folder of five to ten resolved-ticket runbooks, each scored against the rubric. Keep the screenshots and the markdown files together, you will assemble them into a public portfolio in the next lesson. This is the single most persuasive thing you can show a hiring manager when you have no paid experience yet: proof, in your own words and your own screenshots, that you can already do the job.
