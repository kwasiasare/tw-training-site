---
course: cloud-security-engineer
title: 'Capstone: Pre-AI Deployment Data Security Audit (Purview)'
month: 6
monthTitle: Capstone Projects & Career Launch
lesson: 2
summary: An organization wants Microsoft 365 Copilot but is terrified of data leakage and oversharing.
  In this capstone you act as the security architect who makes the tenant safe for AI by deploying Microsoft
  Purview as a control layer in front of Copilot. You will build auto-labeling and classification to find
  and tag proprietary IP and sensitive financial data, DLP policies that stop labeled content from leaving
  or being pasted into unapproved public AI tools, and oversharing remediation plus restricted search
  so Copilot cannot surface what it should not. You will validate the controls with seeded test data,
  measure Copilot readiness, and package it as a portfolio-grade project. It draws directly on Module
  3.
objectives:
- Explain why Copilot inherits a tenant's existing permissions and why oversharing is the core AI data-security
  risk
- Design a sensitivity label taxonomy and auto-labeling rules that classify proprietary IP and sensitive
  financial data at scale
- Author DLP policies that block sharing of labeled data externally and to unapproved generative AI applications
- Apply oversharing remediation, restricted SharePoint search, and the Copilot data-protection controls
  in Purview
- Validate the controls with seeded test data and measure tenant readiness before enabling Copilot
- Assemble the audit report, policy exports, and before/after evidence that make this a hireable portfolio
  artifact
video: cse-m6-l02-capstone-pre-ai-data-security-audit.mp4
quiz:
- q: Why is oversharing the central risk when deploying Microsoft 365 Copilot?
  options:
  - Copilot uploads tenant data to the public internet by default
  - Copilot respects existing permissions, so any content a user can already access can be surfaced and
    summarized by Copilot, amplifying pre-existing oversharing
  - Copilot ignores sensitivity labels entirely
  - Copilot creates new permissions on every file it reads
  answer: 1
  why: Copilot enforces the user's existing Microsoft 365 permissions, it does not grant new access. The
    danger is that years of 'shared with everyone' SharePoint sites and over-permissive links mean a user
    can already reach far more than anyone realized, and Copilot makes that latent oversharing instantly
    discoverable through natural-language search and summarization.
- q: What is the role of auto-labeling in this capstone?
  options:
  - It encrypts every email in the tenant regardless of content
  - It automatically applies sensitivity labels to content matching classifiers (e.g., financial data,
    IP) so downstream DLP and protection can act on it at scale
  - It deletes any file older than 90 days
  - It replaces the need for DLP policies completely
  answer: 1
  why: Auto-labeling uses sensitive information types, trainable classifiers, and keyword/EDM rules to
    apply sensitivity labels across SharePoint and OneDrive without relying on users. Those labels become
    the hook that DLP, encryption, and Copilot controls use to enforce protection consistently at scale.
- q: Which DLP capability most directly addresses the fear of staff pasting proprietary data into an unapproved
    public AI tool?
  options:
  - Exchange mail-flow rules only
  - Purview DLP for the browser/endpoint with controls that detect and block paste or upload of sensitive
    content to unapproved generative AI sites
  - A firewall rule that blocks all internet access
  - Renaming the files so the AI cannot read them
  answer: 1
  why: Purview Endpoint DLP (with the browser integration) can detect sensitive content being pasted or
    uploaded into generative AI sites and either warn or block it. Combined with the broader sensitive
    AI-site controls, this targets the exact exfiltration path the business fears without blocking the
    entire internet.
- q: Why apply restricted SharePoint search or SharePoint Advanced Management as part of Copilot readiness?
  options:
  - To make SharePoint search faster for everyone
  - To temporarily constrain what Copilot and enterprise search can return while you remediate oversharing,
    so Copilot cannot surface unsecured content during rollout
  - To delete unlabeled documents automatically
  - To disable SharePoint entirely during the audit
  answer: 1
  why: Restricted SharePoint Search lets you allow-list a curated set of sites for Copilot and enterprise
    search while you fix oversharing elsewhere, acting as a guardrail during rollout. SharePoint Advanced
    Management adds data-access governance reports and site lifecycle controls to find and reduce oversharing
    systematically.
- q: When validating, why seed purpose-built test data rather than testing only on real documents?
  options:
  - Real documents cannot be labeled
  - Seeded test data with known sensitive patterns lets you prove the classifiers, labels, and DLP fire
    correctly and measure precision without risking real exposure
  - Microsoft requires synthetic data for all DLP
  - Test data automatically trains Copilot
  answer: 1
  why: Seeding documents that contain known fake credit-card numbers, fake account IDs, and clearly marked
    'PROPRIETARY' IP gives you ground truth. You can confirm auto-labeling tags them, DLP blocks the right
    actions, and Copilot cannot surface them, and you can measure false positives and negatives, which
    you cannot do reliably against messy real data alone.
- q: In two to four sentences, explain how labels, DLP, and oversharing remediation work together as layers
    to make a tenant safe for Copilot, rather than relying on any single control.
  answer: 'Sensitivity labels classify and can encrypt the data so protection travels with the file, giving
    every other control a consistent signal to act on. DLP then uses those labels (and content classifiers)
    to stop the data from leaving the trust boundary or being pasted into unapproved AI tools, controlling
    movement. Oversharing remediation and restricted search reduce who can reach the data in the first
    place, so even Copilot''s permission-respecting search cannot surface content the user should never
    have been able to open. Together they form defense in depth: classify, control movement, and minimize
    access, so no single failure exposes the crown jewels to AI.'
  why: A strong answer ties each layer to a distinct function, labels classify/protect, DLP controls movement,
    oversharing remediation minimizes access, and frames them as defense in depth that survives a single
    control failing.
resources:
- label: Microsoft Purview data security and compliance protections for Microsoft 365 Copilot
  url: https://learn.microsoft.com/en-us/purview/ai-microsoft-purview
- label: Learn about sensitivity labels
  url: https://learn.microsoft.com/en-us/purview/sensitivity-labels
- label: Learn about Data Loss Prevention
  url: https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp
- label: Restricted SharePoint Search
  url: https://learn.microsoft.com/en-us/sharepoint/restricted-sharepoint-search
---

## Scenario

Leadership wants **Microsoft 365 Copilot** rolled out to the whole company next quarter to boost productivity. Security is sounding the alarm: 'If we turn this on today, will Copilot expose salary spreadsheets, the unreleased product roadmap, and the M&A folder to half the company?' They are right to worry. Copilot does not invent new access, it **respects every existing Microsoft 365 permission**, which means a decade of over-permissive SharePoint sites and 'share with everyone' links becomes instantly discoverable through natural-language prompts. Your job as the security architect is to run a **pre-AI deployment data security audit** and stand up **Microsoft Purview** as the control layer that makes the tenant safe for AI.

This capstone is the marquee project for Module 3 (Data Security & AI Governance with Purview). It proves you can do the single most in-demand 2026 security task: get an organization Copilot-ready without leaking the crown jewels.

## Architecture

Think of Purview as three protective layers wrapped around Copilot, plus a readiness gate:

1. **Classification layer - Sensitivity labels + auto-labeling.** Define a label taxonomy (e.g., Public, Internal, Confidential, Highly Confidential\Financial, Highly Confidential\IP). Auto-labeling policies crawl **SharePoint Online and OneDrive**, using sensitive information types (SITs), exact data match (EDM), and trainable classifiers to tag proprietary IP and sensitive financial data automatically.
2. **Movement-control layer - DLP.** Data Loss Prevention policies use those labels and classifiers to **block external sharing** of labeled content and to **block paste/upload of sensitive data into unapproved generative AI tools** via Endpoint and browser DLP.
3. **Access-minimization layer - Oversharing remediation + Restricted Search.** Use **SharePoint Advanced Management** data-access governance reports to find oversharing, then remediate. Turn on **Restricted SharePoint Search** to allow-list a curated set of sites so Copilot and enterprise search cannot surface unsecured content during rollout.
4. **Copilot-aware controls.** Purview's **AI data-security** features (DSPM for AI / data protection for Copilot) let labels and DLP apply to Copilot interactions, and let you audit Copilot prompts and responses.

Diagram it as concentric rings: data at the center, then labels, then DLP, then access minimization, with Copilot reaching in through all three rings. That ring diagram is your portfolio centerpiece.

## Step-by-step build

**Step 0 - Prerequisites.** Use an M365 E5 / E5 Compliance evaluation tenant with Copilot licensing (or trial). Seed a test SharePoint site and a few OneDrive accounts with realistic but **synthetic** documents (see Validation). Confirm Purview roles are assigned.

**Step 1 - Build the label taxonomy.** In the Purview portal under **Information Protection > Labels**, create the labels above. For Highly Confidential\Financial and \IP, configure **encryption** and content marking. Publish them in a **label policy** scoped to your users.

**Step 2 - Auto-label at scale.** Create **auto-labeling policies** (service-side) for SharePoint/OneDrive: match the financial label on built-in financial SITs (credit card, bank account, plus a custom EDM for internal account IDs) and match the IP label on a trainable classifier or a keyword/document-property rule (e.g., documents containing 'PROPRIETARY - DO NOT DISTRIBUTE'). Run them first in **simulation mode** to preview matches before enforcing.

**Step 3 - Author DLP policies.** Create DLP policies that, for content carrying the Financial or IP labels: **block sharing with people outside the organization**; and via **Endpoint DLP + the Purview browser extension / network protection**, **block or warn on paste and upload to unapproved generative AI sites** while allowing the approved enterprise Copilot. Start with **Audit/Test with notifications**, then move to **Block**.

**Step 4 - Reduce oversharing.** Run **SharePoint Advanced Management** data-access governance reports to find sites with 'Everyone' / 'Everyone except external users' access and overshared links. Remediate the worst offenders. Enable **Restricted SharePoint Search** to allow-list vetted sites for Copilot/search while remediation continues.

**Step 5 - Turn on Copilot-aware protection.** In **DSPM for AI**, enable the data-protection and auditing controls so labels and DLP apply to Copilot, and so prompts/responses are auditable.

## Validation / Testing

Validate against **ground truth** using seeded synthetic data, never real secrets:

- **Seed test documents** with known fake patterns: fake credit-card and IBAN numbers (financial), a doc clearly marked 'PROPRIETARY - DO NOT DISTRIBUTE' (IP), and benign 'Public' docs as negative controls.
- **Classification test:** confirm auto-labeling applies the right labels (check the document's label and Content Explorer). Record precision: did any Public doc get mislabeled (false positive)? Did any sensitive doc get missed (false negative)?
- **DLP test:** attempt to share a labeled financial doc with an external address, expect a block and policy tip. Attempt to paste seeded IP text into an unapproved public AI site in the browser, expect a block/warn; confirm the approved Copilot still works.
- **Oversharing test:** as a low-privilege test user, run a Copilot prompt like 'summarize our latest financial results' or 'show me the product roadmap' before and after remediation. Before, Copilot may surface the seeded sensitive doc; after restricted search and remediation, it should not.
- **Readiness metrics:** report a simple scorecard, percentage of sensitive sites remediated, number of overshared links removed, classifier precision/recall on the seeded set, and number of DLP blocks observed. This turns 'it feels safer' into measurable readiness.

Keep a *Control | Test | Expected | Observed | Pass/Fail* table and capture screenshots of each block and label, these are gold in your portfolio.

## What to put in your portfolio

- **The concentric-ring architecture diagram** (data -> labels -> DLP -> access minimization -> Copilot).
- **A written audit report**: executive summary of the oversharing risk, the controls deployed, before/after readiness metrics, and a go/no-go recommendation for Copilot.
- **Policy exports**: label definitions, auto-labeling policy config, and DLP policy config (export via Graph/PowerShell where possible). Redact tenant specifics.
- **Before/after evidence**: screenshots of the Copilot prompt surfacing the seeded doc *before*, and being blocked *after*; DLP policy tips; Content Explorer showing labels applied.
- **A GitHub repo** with the diagram, exported configs, the seeded-data generator script, and a README framing the business value.

Resume bullet, impact-first: 'Led a pre-Copilot data security audit in Microsoft Purview, deployed auto-labeling, DLP, and oversharing remediation that reduced overshared sites by X% and blocked sensitive data from leaving to unapproved AI tools, clearing the tenant for safe Microsoft 365 Copilot rollout.'
