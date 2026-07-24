---
course: vdi-engineer
title: AZ-140 Exam Logistics and Your Multi-Platform Certification Roadmap
month: 7
monthTitle: Capstone Projects & Career Launch
lesson: 4
summary: 'Three capstones prove you can do the work; a certification proves it to someone who''s never
  seen your GitHub. This lesson maps AZ-140, Microsoft Certified: Azure Virtual Desktop Specialty, directly
  onto Modules 3 through 6 of this course, walks through the verified 2026 exam logistics, and is honest
  about what Microsoft does and doesn''t publish. Then it builds your wider certification roadmap across
  CCA-V, OCA-H, and adjacent credentials like MD-102, so you leave with a sequenced plan rather than a
  pile of exam codes.'
objectives:
- Map AZ-140's four skills-measured domains to the specific modules of this course that prepared you for
  each
- State the verified 2026 AZ-140 exam logistics and distinguish them from unverified third-party claims
- Build a study plan that closes gaps rather than re-studying material you've already mastered
- Compare the current Citrix (CCA-V) and Omnissa (OCA-H) administrator certifications and know when each
  is the right next step
- Sequence a multi-platform certification roadmap based on target role and target employer's platform
quiz:
- q: Which of these AZ-140 domain-to-module mappings is correct?
  options:
  - Plan and implement identity and security maps to Module 6
  - Monitor and maintain an Azure Virtual Desktop infrastructure maps to Module 2
  - Plan and implement user environments and apps maps to Module 1
  - Plan and implement an Azure Virtual Desktop infrastructure (40–45%) maps to Module 3
  answer: 3
  why: AZ-140's largest domain, planning and implementing the AVD infrastructure itself (host pools, images,
    networking, scaling), is a 1:1 match with Module 3 of this course. Identity and security maps to Module
    4, user environments and apps to Module 5, and monitoring and maintenance to Module 6.
- q: According to the current Microsoft Learn certification page, how long do you have to complete the
    AZ-140 exam?
  options:
  - 100 minutes
  - 45 minutes
  - 180 minutes
  - Microsoft does not set a time limit
  answer: 0
  why: Microsoft Learn's official AZ-140 certification page states candidates have 100 minutes to complete
    the assessment, and that the exam is proctored and may include interactive components.
- q: Why should you be skeptical of a third-party 'exam dump' site that confidently states AZ-140 has
    exactly 47 questions and a passing score of 700 out of 1000?
  options:
  - Those numbers are always accurate for every Microsoft exam
  - Microsoft does not publish an exact question count or a numeric passing score on its official certification
    page, so specific numbers from unofficial sites are unverifiable, may be outdated or platform-dependent,
    and referencing 'exam dump' content may violate Microsoft's exam policies
  - The passing score is always exactly 50%
  - Question counts are irrelevant to exam preparation
  answer: 1
  why: The official Microsoft Learn AZ-140 page gives the time limit and the domains but does not publish
    a fixed question count or numeric passing score, because scoring is adaptive and varies by exam form.
    Treat specific numbers from unofficial 'dump' sites as unverified, and be aware that engaging with
    literal exam-dump content can itself violate Microsoft's certification policies.
- q: A candidate wants a Citrix credential specifically for administering Citrix Virtual Apps and Desktops
    day to day. Which current certification fits?
  options:
  - VCP-DTM
  - OCA-H
  - CCA-V (Citrix Certified Associate – Virtualization)
  - AZ-104
  answer: 2
  why: CCA-V is the current Citrix Certified Associate – Virtualization credential, validating hands-on
    administration skills for Citrix Virtual Apps and Desktops (Delivery Controllers, Cloud Connectors,
    StoreFront, Director, Profile Management). VCP-DTM is a legacy VMware credential no longer issued;
    OCA-H is Omnissa's Horizon-specific credential, a different platform.
- q: Why is VCP-DTM the wrong certification to present as 'the current path' for someone targeting Horizon
    administration in 2026?
  options:
  - VCP-DTM was never a real certification
  - VCP-DTM and OCA-H are the same certification under different names
  - VCP-DTM now covers Citrix instead of Horizon
  - VCP-DTM is a legacy VMware credential that is no longer issued (existing holders' certifications are
    still honored); the current path for Horizon administration is Omnissa's OCA-H
  answer: 3
  why: Following the VMware End-User Computing spin-out under Broadcom into Omnissa, VCP-DTM is a legacy
    credential no longer issued to new candidates, even though people who already hold it keep it. The
    current, active administrator credential for Horizon is Omnissa's OCA-H, and that's the one to recommend
    to someone starting today.
- q: In two to four sentences, describe a sensible certification sequencing plan for someone finishing
    this course who doesn't yet know which employer's platform they'll land on.
  answer: Take AZ-140 first, because its depth matches this course directly and Azure Virtual Desktop
    skills transfer broadly regardless of which platform a future employer runs. After that, hold off
    on committing to a second, platform-specific certification like CCA-V or OCA-H until you know (or
    have a strong signal about) which vendor's platform your target employer or role actually uses, since
    studying the wrong vendor's exam wastes time that could go toward interview prep or portfolio work.
    If the target role leans heavily on Windows 365 and Intune-managed Cloud PCs specifically, MD-102
    is a reasonable adjacent credential to add regardless of which VDI vendor is in play.
  why: A strong answer sequences AZ-140 first because it matches the course's depth and transfers broadly,
    treats the platform-specific certs (CCA-V/OCA-H) as conditional on the target employer's stack rather
    than default next steps, and correctly places MD-102 as orthogonal (device/Windows 365 management)
    rather than a VDI platform choice.
resources:
- label: 'Microsoft Certified: Azure Virtual Desktop Specialty (AZ-140 certification page)'
  url: https://learn.microsoft.com/en-us/credentials/certifications/azure-virtual-desktop-specialty/
- label: AZ-140 study guide
  url: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-140
- label: Citrix training and certifications (CCA-V)
  url: https://www.citrix.com/training-and-certifications/
- label: Omnissa Certified Administrator – Horizon (OCA-H) exam guide
  url: https://www.omnissa.com/oca-horizon-exam-guide/
video: vdi-m7-l04-az-140-and-cert-roadmap.mp4
---

## Why Certify

Three capstones prove you can do the work to anyone who reads your portfolio closely. A certification proves it, faster, to a recruiter or an applicant tracking system that will never read your GitHub README in full. They're not substitutes for each other — the capstones give you something to talk about in an interview, and the certification gets you into that interview in the first place. This lesson builds your certification plan around AZ-140, the credential that matches this course's Azure depth, and then extends it to the multi-platform reality of the EUC job market.

## AZ-140 at a Glance

**Microsoft Certified: Azure Virtual Desktop Specialty** is scored at Microsoft's Intermediate level under the Administrator role, and renews every 12 months. Its four skills-measured domains map directly onto four modules of this course, because this course was built to that mapping from the start:

| AZ-140 domain | Weight | Maps to |
|---|---|---|
| Plan and implement an Azure Virtual Desktop infrastructure | 40–45% | Module 3 |
| Plan and implement identity and security | 15–20% | Module 4 |
| Plan and implement user environments and apps | 20–25% | Module 5 |
| Monitor and maintain an Azure Virtual Desktop infrastructure | 10–15% | Module 6 |

If you've worked through Modules 3 through 6 and this capstone module, you've already covered the exam's scope hands-on — the study plan below is about closing specific gaps and getting comfortable with the exam format, not learning the material for the first time.

## Exam Logistics — What's Actually Verified

Pulled directly from Microsoft's official AZ-140 certification page (checked July 2026): you have **100 minutes** to complete the assessment. The exam is **proctored** and **may include interactive components** — meaning some questions can go beyond simple multiple choice, closer to scenario-based or hands-on-style items. It's currently offered in **English, German, Spanish, French, Japanese, Portuguese (Brazil), and Chinese (Simplified)**. If you fail, you can retake it **24 hours** after the first attempt; the wait for subsequent retakes is longer and detailed in Microsoft's retake policy.

Here's what's deliberately **not** stated above: an exact question count or a specific numeric passing score. Microsoft does not publish either of those on the official certification page, because scoring is adaptive and varies by exam form. You will find third-party sites confidently stating things like "40–60 questions" or "passing score 700/1000" — treat those as unverified folklore, not fact, and be cautious about any site that goes further and offers literal "exam dump" question banks, since using those can violate Microsoft's certification policies and puts your credential at risk even if you pass.

## Building Your Study Plan

Start from what you've already built, not from a study guide's table of contents. For each AZ-140 domain, ask honestly: did a lesson or a capstone actually make you *do* this, or only read about it? Host pool and networking design (Module 3, reinforced hard by Capstone 1) should feel solid. Identity and Conditional Access (Module 4) likewise. Monitoring (Module 6) is the domain most people under-practice, because it's the smallest weight — but it's also fast to close: spend a session running the KQL-style queries against Azure Virtual Desktop Insights and reading a few real alert configurations rather than only the docs. Use the official AZ-140 study guide to spot anything the course didn't cover in the exact form the exam expects, then take a practice assessment to find your actual gaps before you schedule the real thing.

## The Multi-Platform Roadmap

AZ-140 is the right first certification for this course's depth, but the EUC job market — as Module 2 covered — is not single-vendor. Depending on where you land, a second credential may be worth adding:

- **CCA-V (Citrix Certified Associate – Virtualization).** No prerequisites, built around the current Citrix Virtual Apps and Desktops Administration exam, and it validates the hands-on skills covered in Module 2's Citrix DaaS lesson: Delivery Controllers, Cloud Connectors, StoreFront, Director, and Profile Management. Worth pursuing if a target employer runs Citrix.
- **CC-VAD-CC**, Citrix's Cloud/DaaS-specific credential, is the next step up once you're specifically working in Citrix Cloud-managed environments rather than classic on-premises Citrix.
- **OCA-H (Omnissa Certified Administrator – Horizon).** The current administrator credential for Omnissa Horizon, covering Connection Server, Instant Clones, App Volumes, and DEM. Important: **VCP-DTM, the old VMware credential, is no longer issued** — existing holders keep it, but OCA-H is the active path for anyone starting today.
- **MD-102**, Microsoft's endpoint administrator exam, is worth adding if your target role leans heavily on Windows 365 and Intune-managed Cloud PCs specifically — it's orthogonal to the VDI-platform choice, not a competitor to AZ-140, CCA-V, or OCA-H.

## Sequencing It

Take **AZ-140 first** — it matches this course's depth directly, and Azure Virtual Desktop skills transfer broadly no matter which vendor a future employer ultimately runs. After that, don't default to studying a second platform-specific exam just to collect credentials; wait until you have a real signal about which vendor's platform your target role or employer actually uses, and study that one. Add MD-102 opportunistically if Windows 365 and device management show up repeatedly in the job descriptions you're targeting — Lesson 5 will show you exactly how to read those job descriptions for signals like this.

## Using the Practice Tools Before You Schedule

Microsoft's official AZ-140 certification page links two tools worth using before you pay for the real exam: a **practice assessment**, which gives you the style, wording, and difficulty of real questions and a readiness signal per domain rather than a single pass/fail guess; and an **exam sandbox**, which lets you experience the actual testing interface and interact with the different question types beforehand, so the format itself isn't a surprise on exam day. Run the practice assessment once early, to find your real gaps, and once again close to your scheduled date, to confirm those gaps closed — a single early attempt tells you what to study, and a second attempt closer to test day tells you whether you're actually ready, which is a more honest signal than confidence alone.
