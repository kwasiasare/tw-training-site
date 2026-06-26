---
course: helpdesk-tier1-2
title: Building Your IT Support Portfolio
month: 7
monthTitle: Capstone & Career Launch
lesson: 2
summary: You have a lab and a folder of resolved-ticket write-ups; now you turn them into a portfolio
  a recruiter can find and trust. This lesson shows how to publish your work as a clean GitHub repository
  or a simple portfolio site, organize the knowledge-base articles, present good screenshots, and record
  one or two short screen demos that show a fix working end to end. You will also package an automation
  sample, a short PowerShell script or an RMM automation, so the portfolio proves you can save time at
  scale, not just click through one fix. The deliverable is a public, professional portfolio link you
  can paste into a resume, a LinkedIn Featured section, and every application.
objectives:
- Structure your lab and KB articles into a clean public GitHub repo or portfolio site
- Write a strong README that frames the portfolio with a one-line pitch and a project index
- Capture clear, redacted screenshots that make each write-up easy to scan
- Record one or two short screen demos that show a fix working end to end
- Package an automation sample (PowerShell or an RMM automation) with comments and a result
- Produce a single shareable portfolio link to use on your resume, LinkedIn, and applications
video: hd7-l02-building-your-it-support-portfolio.mp4
quiz:
- q: What is the single most important thing a portfolio README should do?
  options:
  - Frame who you are in one line and index the projects so a reviewer can navigate in seconds
  - List every command you have ever typed
  - Hide the projects until after an interview
  - Contain only a photo and no text
  answer: 0
  why: A reviewer spends seconds before deciding to read on. A README that opens with a one-line pitch
    (who you are and what you do) and a clear index of projects lets them navigate immediately, which
    is what converts a glance into a real read.
- q: Why is GitHub (or a simple portfolio site) a good home for helpdesk portfolio work?
  options:
  - Because it is only for software developers
  - Because it gives you a free, public, linkable home for your runbooks, scripts, and screenshots that
    recruiters can open instantly
  - Because it automatically gets you a job
  - Because it hides your work from search engines
  answer: 1
  why: GitHub (with GitHub Pages) or a lightweight site gives you a free, public, shareable URL where
    your markdown runbooks, commented scripts, and screenshots live together. A recruiter can open it
    in one click, which is far more persuasive than claims on a resume.
- q: What makes a screen demo effective for an IT support portfolio?
  options:
  - It is 30 minutes long with no narration
  - It only shows the final success screen
  - It is short (2-4 minutes), shows the problem, the fix, and the verification, with a calm spoken walkthrough
  - It includes real user passwords on screen
  answer: 2
  why: Recruiters and hiring managers watch short demos. A 2-4 minute clip that states the problem, shows
    you fixing it, and verifies the result, narrated calmly, proves both the technical skill and the communication
    skill the role needs, without wasting their time or exposing secrets.
- q: Why include an automation sample (a PowerShell script or an RMM automation) in the portfolio?
  options:
  - To prove you can write a novel
  - To make the repo larger
  - Because scripts are required to use a computer
  - To show you can save time at scale, not just fix one machine by hand
  answer: 3
  why: A single manual fix shows competence; an automation that applies a fix across many devices shows
    leverage. Including a commented script or RMM automation, with a note on what it does and the result,
    signals you think in terms of efficiency, which is a Tier 2 trait employers pay for.
- q: Which is the best practice when adding screenshots to your portfolio?
  options:
  - Post raw screenshots that include real usernames, emails, and any visible secrets
  - Crop to the relevant area, annotate the key part, and redact names, emails, and anything sensitive
  - Use only blurry photos taken with a phone
  - Never use screenshots at all
  answer: 1
  why: Good screenshots are cropped to what matters, lightly annotated to point at the key setting, and
    redacted so no real personal data or secrets leak. This is both more readable and a sign you understand
    data handling, which itself reassures a security-conscious employer.
- q: In two or three sentences, describe how you would structure a GitHub repo so a recruiter can navigate
    your helpdesk portfolio quickly.
  answer: I would put a README at the top with a one-line pitch and an index linking to each project,
    then one folder per area (for example active-directory, intune-m365, automation), each containing
    the runbook markdown plus a screenshots subfolder. Scripts live in an automation folder with comments
    and a short note on what each does and the result, and the demo videos are linked from the README.
    That way a reviewer reads the pitch, scans the index, and opens any project in one or two clicks.
  why: A clear top-level README plus consistent per-project folders (write-up, screenshots, scripts) and
    linked demos lets a reviewer move from pitch to evidence in seconds, which is exactly what turns a
    portfolio glance into an interview.
resources:
- label: GitHub (free public repositories to host your portfolio)
  url: https://github.com
- label: GitHub Pages (publish a simple portfolio site from a repo)
  url: https://pages.github.com/
- label: NinjaOne documentation (RMM automations and scripting reference)
  url: https://www.ninjaone.com/docs/
- label: Microsoft Learn training catalog (free, role-based learning to keep extending projects)
  url: https://learn.microsoft.com/en-us/training/
---

## From a Folder of Files to a Portfolio

In the last lesson you built a lab and wrote up five to ten resolved tickets. Right now they live in a folder on your machine, where no employer will ever see them. This lesson makes them public, professional, and linkable. The goal is a single URL you can paste into your resume, your LinkedIn Featured section, and every application, a URL that, in under a minute, convinces a reviewer you can do the work. Think of it as building a clean interface over the work you already did.

## Choose a Home: GitHub or a Simple Site

For an IT support portfolio, **GitHub** is the easiest professional home, and yes, it is for more than developers. A free public repository gives your markdown runbooks, your commented scripts, and your screenshots one shareable address. If you want something that looks more like a web page, turn on **GitHub Pages**, which publishes a repo as a simple site, or use any lightweight site builder. Either way the principles are the same: one clear front door, consistent structure, and evidence one click away.

Do not over-engineer this. A single well-organized repository beats a fancy site you never finish. You can always upgrade later.

## Structure the Repository

Reviewers skim. Structure for skimming:

- **README at the top.** This is your front door. Open with a one-line pitch, for example: *Aspiring IT Support / Desktop Support technician (CompTIA A+, Network+) - here are labs and runbooks I built supporting Windows, Active Directory, Microsoft 365, and Intune.* Then an index: a short list linking to each project with a one-line description.
- **One folder per area.** For example `active-directory/`, `intune-m365/`, `windows-troubleshooting/`, and `automation/`. Inside each, put the runbook markdown and a `screenshots/` subfolder.
- **Consistent file names.** `onboarding-new-user.md`, `shared-folder-access-denied.md`, and so on. Predictable names make the repo feel professional.
- **An automation folder.** Keep your scripts together, each with comments and a short note on what it does and the result.

The test: can a stranger land on your README and reach any piece of evidence in one or two clicks? If yes, the structure works.

## Make the Knowledge-Base Articles Shine

You already wrote the runbooks with five sections (problem, environment, steps, verification, outcome). Now polish them for a public audience. Add a one-line summary at the very top of each article so a reader knows instantly what it covers. Keep steps numbered and specific. Where a setting has an exact name, use it. Link related articles to each other. Read each one aloud once, if a step is unclear to you, it is unclear to a reviewer.

## Screenshots That Help, Not Hurt

Screenshots are powerful proof, but only when done well:

- **Crop** to the relevant area. Nobody needs your whole desktop.
- **Annotate** the key part with a box or arrow so the eye goes straight to the setting that matters.
- **Redact** every username, email, license key, and anything that even resembles a password or personal data. Use lab/test data wherever possible. Careful redaction is itself a signal that you handle data responsibly, which reassures a security-conscious employer.
- **Name files clearly** (`gpo-drive-map-applied.png`) so they are easy to reference from the markdown.

## Record One or Two Short Demos

A short screen demo is the highest-impact artifact you can add, because recruiters actually watch them and they prove communication skill at the same time as technical skill. Record one or two, no more, each **two to four minutes**, using any free screen recorder. A good demo:

1. States the problem in one sentence (the ticket).
2. Shows you working the fix in the lab, talking through what you are doing and why.
3. Verifies the result, the policy applied, the user signed in, the alert cleared.

Speak calmly and plainly, as if explaining to a colleague. Do not show any real credentials on screen. Upload unlisted to a video host and link the demo from the relevant README, so a reviewer can watch without hunting for it. One clean three-minute demo of an Intune profile deploying or a Group Policy drive-mapping applying is worth more than a page of claims.

## Package an Automation Sample

Manual fixes show competence; automation shows leverage, the Tier 2 mindset of fixing things at scale. Include one small, genuine automation sample:

- A short, **commented PowerShell script** that does something useful, clears temp files, checks disk space and reports, bulk-creates test users in AD, or audits a setting across machines.
- Or an **RMM automation** (for example in NinjaOne, from Module 4) that runs a script against a group of devices.

Whatever you choose, comment it well, explain at the top what problem it solves, and note the result (*ran against 5 lab VMs, freed an average of 2 GB each*). You do not need to be a developer; you need to show you reach for automation when a task repeats. That instinct is exactly what moves you from Tier 1 toward Tier 2.

## Tie It Together With One Link

The deliverable of this lesson is a single, shareable portfolio link. Once your repo or site is live:

- Put the link near the top of your **resume**, next to your contact details.
- Add it (and the demo videos) to your **LinkedIn Featured** section, which you will set up in lesson four.
- Paste it into applications wherever a website or portfolio field appears.

Double-check the link works in a private browser window (so you are sure it is public), that there are no broken images, and that no real personal data slipped through. Ask a friend to open it cold and tell you what they think you do, if their answer matches your pitch, the portfolio is working.

## Keep Improving It Over Time

A portfolio is not a one-time submission; it is a living asset that should grow while you job-hunt. Each week, add or improve one artifact, a new runbook, a cleaner screenshot, a second short demo, so a recruiter who revisits sees momentum. Commit your changes with clear messages (for example 'add Intune compliance remediation runbook'); a tidy commit history quietly signals that you work in an organized, professional way. Ask for feedback: share the link with a working technician or a mentor and act on whatever confuses them, because the first-time reader is exactly who you are optimizing for. Watch which projects draw questions in interviews and expand those. Keep accessibility in mind too, plain headings, alt text on images where the platform supports it, and readable contrast, so anyone can navigate it. Over a few weeks this compounds: the portfolio that earned your first interview becomes noticeably stronger by your fifth, which is exactly when it matters most.

## The Deliverable

By the end of this lesson you should have a public GitHub repo or portfolio site with a strong README and project index, your polished KB articles organized by area with clean redacted screenshots, one or two short demos linked in, and at least one commented automation sample. That single link is now the centerpiece of your job search, the thing that lets a recruiter believe your resume before they have even spoken to you.
