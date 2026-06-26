---
course: cloud-security-engineer
title: 'Securing Microsoft 365 Copilot: Pre-AI Data Readiness'
month: 3
monthTitle: Data Security & AI Governance with Microsoft Purview
lesson: 4
summary: 'Microsoft 365 Copilot does not get its own special access to your data; it reads exactly what
  the signed-in user can already read. That single fact means every oversharing problem you have ever
  ignored becomes an instant data-exposure problem the moment Copilot is enabled. This lesson is the data-readiness
  foundation for Capstone Project 2: you will fix oversharing with SharePoint Advanced Management and
  site access reviews, constrain reach with Restricted SharePoint Search, ensure sensitivity labels and
  their encryption travel into Copilot responses, apply DLP for Copilot, exclude sensitive content, audit
  Copilot interactions in Purview, and block users from pasting corporate secrets into unapproved public
  AI tools. Get the data house in order before, not after, you turn Copilot on.'
objectives:
- Explain why Copilot inherits user permissions and how oversharing becomes data exposure
- Remediate oversharing using SharePoint Advanced Management, site access reviews, and Restricted SharePoint
  Search
- Describe how sensitivity labels and encryption control what Copilot can surface and what it inherits
  onto outputs
- Configure DLP for Microsoft 365 Copilot and exclude labeled or sensitive content from grounding
- Audit Copilot interactions and prompts using Purview Audit, eDiscovery, and Communication Compliance
- Reduce shadow-AI risk by blocking sensitive data from being pasted into unapproved public AI tools
video: cse-m3-l04-securing-microsoft-365-copilot.mp4
quiz:
- q: What is the single most important security fact about Microsoft 365 Copilot's data access?
  options:
  - Copilot has elevated admin access to all tenant data
  - Copilot reads only what the signed-in user already has permission to read
  - Copilot can only read public internet data, never tenant data
  - Copilot ignores SharePoint permissions entirely
  answer: 1
  why: 'Copilot grounds its answers in the user''s accessible Microsoft Graph content, honouring existing
    permissions: it reads what the user can read, nothing more. This is reassuring in principle but means
    any existing oversharing immediately becomes a Copilot data-exposure path, which is why pre-deployment
    readiness is essential.'
- q: A site labeled 'Everyone except external users' contains a salary spreadsheet nobody realized was
    broadly shared. Why is this now urgent once Copilot is enabled?
  options:
  - Copilot will delete the spreadsheet
  - Any user can now surface that salary data through a natural-language Copilot prompt because they always
    technically had access
  - Copilot encrypts the file so no one can read it
  - It is not urgent; Copilot cannot read spreadsheets
  answer: 1
  why: 'Before Copilot, the oversharing was latent: users could technically access the file but rarely
    stumbled onto it. Copilot makes that latent access trivially discoverable through plain-language prompts,
    so a permissions problem that sat dormant for years becomes an active exposure overnight.'
- q: Which capability lets you limit Copilot and tenant-wide search to an approved set of SharePoint sites
    while you remediate oversharing?
  options:
  - Restricted SharePoint Search
  - Conditional Access
  - Azure Rights Management
  - Multi-Geo
  answer: 0
  why: Restricted SharePoint Search lets admins restrict organization-wide search and Copilot grounding
    to a curated allow-list of sites (and users' OneDrive), acting as a temporary guardrail that contains
    exposure while you do the deeper permissions cleanup with SharePoint Advanced Management.
- q: How does a sensitivity label with encryption affect what Copilot can do with a document?
  options:
  - It has no effect; Copilot bypasses encryption
  - If the user lacks usage rights (such as EXTRACT/VIEW) on the encrypted file, Copilot cannot use its
    content, and labels can be inherited onto generated output
  - It forces Copilot to share the file externally
  - It deletes the label when Copilot reads the file
  answer: 1
  why: 'Copilot respects label encryption: if the signed-in user does not have the rights to extract or
    view content, Copilot will not surface or summarize it. Additionally, when Copilot uses labeled content,
    the most restrictive sensitivity label can be inherited onto the generated output, so protection carries
    forward.'
- q: What is the purpose of DLP for Microsoft 365 Copilot?
  options:
  - To block users from signing in to Microsoft 365
  - To prevent Copilot from using or processing content that carries specified sensitivity labels as grounding
    data
  - To encrypt every Copilot prompt at rest
  - To replace the need for sensitivity labels
  answer: 1
  why: DLP for Microsoft 365 Copilot lets you author a policy that excludes content with specified sensitivity
    labels from being used by Copilot as grounding/reference data, so your most sensitive labeled material
    is kept out of Copilot responses even when the user technically has access.
- q: You are scoping pre-deployment readiness for Microsoft 365 Copilot. In three to five sentences, outline
    the key data-security steps you would complete before enabling Copilot, and explain why doing them
    first matters.
  answer: 'First, because Copilot reads whatever the user can read, I would tackle oversharing: use SharePoint
    Advanced Management with data access governance reports and site access reviews to find and fix sites
    and files shared too broadly, and apply Restricted SharePoint Search as an interim guardrail to limit
    grounding to vetted sites. Second, I would mature classification by ensuring sensitivity labels (with
    encryption where appropriate) are applied to sensitive content via auto-labeling, so Copilot honours
    those rights and inherits the most restrictive label onto its output. Third, I would configure DLP
    for Microsoft 365 Copilot to exclude the most sensitive labels from grounding, and turn on Purview
    auditing of Copilot interactions for accountability. Finally, I would reduce shadow-AI risk by using
    Endpoint DLP and browser controls to block pasting sensitive data into unapproved public AI tools.
    Doing this first matters because enabling Copilot over an unremediated estate instantly converts years
    of latent oversharing into active, easily discoverable data exposure.'
  why: A strong answer leads with the inherit-permissions principle, then sequences oversharing remediation,
    labeling, DLP for Copilot plus auditing, and shadow-AI blocking, and explicitly ties 'do it first'
    to the fact that Copilot makes latent oversharing instantly exploitable.
resources:
- label: Microsoft Purview data security and compliance protections for Microsoft 365 Copilot
  url: https://learn.microsoft.com/en-us/purview/ai-microsoft-purview
- label: Restricted SharePoint Search
  url: https://learn.microsoft.com/en-us/sharepoint/restricted-sharepoint-search
- label: Microsoft SharePoint Advanced Management overview
  url: https://learn.microsoft.com/en-us/sharepoint/advanced-management
- label: Use Microsoft Purview to manage data security and compliance for Microsoft 365 Copilot
  url: https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy
---

## The One Fact That Changes Everything

There is a single sentence you must internalize before deploying Microsoft 365 Copilot: **Copilot reads what the user can read.** It has no privileged backdoor and no elevated service identity into your content. When a user asks Copilot a question, it grounds the answer in that user's accessible Microsoft Graph data, files, emails, chats, meetings, honouring the **exact same permissions** the user already has. Microsoft built it this way deliberately, and on paper it sounds perfectly safe.

The problem is what that fact does to your **existing oversharing**. Every site shared with *Everyone except external users*, every *anyone* link, every forgotten folder a whole department can open, used to be a *latent* risk: technically accessible but rarely discovered. Copilot turns latent access into **instant, natural-language discoverability**. "Summarize what we pay our directors" or "find documents about the acquisition" will happily surface anything the user could have reached. **Oversharing becomes data exposure the moment Copilot is enabled.** This lesson is the data-readiness foundation for **Capstone Project 2**, and the whole job is to get the data house in order *before* you turn Copilot on.

## Find and Fix Oversharing

You cannot fix what you cannot see. **SharePoint Advanced Management (SAM)** provides the tooling:

- **Data Access Governance (DAG) reports** - surface sites with the most *anyone* links, *Everyone except external users* sharing, and sensitive-content-by-label, ranking your worst oversharing offenders.
- **Site access reviews** - delegate remediation to site owners: the admin flags risky sites, and owners attest to or correct who has access.
- **Restricted access control** and **conditional access policies for sites** - lock down high-value sites to specific groups.
- **Inactive site and sharing policies** - clean up the stale sprawl that accumulates over years.

The goal is **right-sized permissions**: people can reach what their role needs and nothing more, so Copilot grounding stays inside legitimate boundaries.

## Restricted SharePoint Search as a Guardrail

Remediating a large tenant takes time. **Restricted SharePoint Search (RSS)** is the interim guardrail. It lets admins restrict organization-wide search and **Copilot grounding** to an **allow-list of up to a few hundred curated, vetted sites** (plus users' own OneDrive and the files they own or recently used). While RSS is on, Copilot cannot reach the sprawling, unreviewed sites, so you contain exposure *during* cleanup. Treat RSS as a temporary blast-radius limiter, not a permanent fix, you still must remediate permissions, then expand or remove the restriction.

## Labels Travel Into Copilot

This is where Module 3 pays off. **Sensitivity labels** are not just for files at rest, they actively shape Copilot:

- **Encryption is enforced.** If a file carries a label whose encryption does not grant the signed-in user **EXTRACT/VIEW** usage rights, Copilot **cannot** use or summarize it, even if the user can see the file exists. Encryption is a hard boundary Copilot respects.
- **Labels are inherited onto output.** When Copilot generates content grounded in labeled source material, it applies the **most restrictive** sensitivity label from those sources to the new output, so protection carries forward into the document or message the user creates.
- **Citations honour labels**, so users see the sensitivity of what Copilot referenced.

This is exactly why robust auto-labeling (Lesson 1) is a Copilot prerequisite, not an afterthought.

## DLP for Copilot and Excluding Sensitive Content

Beyond label-borne encryption, you can author **DLP for Microsoft 365 Copilot**. This policy type lets you specify that content carrying certain **sensitivity labels is excluded from Copilot grounding**, Copilot will not use it as reference data, even when the user technically has access. Combined with auto-labeling your crown-jewel content (e.g. *Highly Confidential\\Board* material), DLP for Copilot gives you a clean, label-driven switch to keep the most sensitive material out of AI responses entirely, independent of every individual file's permission state.

## Audit Copilot Interactions in Purview

Governance requires evidence. Purview captures **Copilot interactions** so you can prove and investigate usage:

- **Audit (Standard/Premium)** logs Copilot prompts and responses as activities, who asked what, when, and which app.
- **eDiscovery** can collect Copilot interaction content for legal hold and investigation.
- **Communication Compliance** can review Copilot prompts and responses for risky or non-compliant content.
- **Activity explorer and Data Security Posture Management for AI (DSPM for AI)** give dashboards on AI usage and the sensitivity of data flowing through Copilot.

Turn auditing on **before** broad rollout so you have a baseline and an accountability trail from day one.

## Block Shadow AI: Don't Let Secrets Leak to Public Tools

Copilot is the *governed* path. The ungoverned path is a user pasting source code or a customer list into a random public chatbot, **shadow AI**. Close that door:

- **Endpoint DLP** and **Purview browser collaboration (Edge for Business)** can detect and **block pasting or uploading sensitive content into unapproved generative-AI sites**, using the same SIT and label conditions from Lesson 2.
- **DSPM for AI** discovers which AI apps users are visiting and what sensitive data is heading toward them.
- Pair technical controls with **acceptable-use policy** and education so people know which AI tools are sanctioned.

## Bringing It Together: The Readiness Checklist

Before you flip Copilot on:

```text
[ ] Inventory oversharing with SAM Data Access Governance reports
[ ] Run site access reviews; right-size the worst offenders
[ ] Turn on Restricted SharePoint Search as an interim guardrail
[ ] Auto-label sensitive content; apply encryption where needed
[ ] Configure DLP for Microsoft 365 Copilot to exclude top labels
[ ] Enable Purview Audit + DSPM for AI for accountability
[ ] Block sensitive data from unapproved public AI via Endpoint DLP
```

Every item traces back to the one fact: Copilot reads what the user can read. Fix *who can read what* first, label and exclude the sensitive material, watch the interactions, and block the shadow-AI side doors. That sequence is the backbone of Capstone Project 2 and the difference between an AI rollout that accelerates your business and one that leaks it.
