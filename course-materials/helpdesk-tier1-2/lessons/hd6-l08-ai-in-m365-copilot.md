---
course: helpdesk-tier1-2
title: 'AI in Microsoft 365: Copilot adoption and support'
month: 6
monthTitle: Microsoft 365 Administration (MS-102)
lesson: 8
summary: Learn what Microsoft 365 Copilot actually is, how it grounds answers in your org's own data through
  Microsoft Graph, and the Tier 2 admin work of licensing, securing, and supporting a Copilot rollout.
objectives:
- Explain what Microsoft 365 Copilot is and how it grounds responses in your organisation's data via Microsoft
  Graph
- 'List the prerequisites: eligible licences, supported apps, and Entra ID accounts'
- Describe how Copilot respects existing permissions and why SharePoint oversharing becomes a real risk
- Outline the data security and privacy boundary that protects your prompts and data
- Assign Microsoft 365 Copilot licences in the Microsoft 365 admin center
- Troubleshoot common Copilot tickets and support user adoption with better prompts
video: hd6-l08-ai-in-m365-copilot.mp4
quiz:
- q: How does Microsoft 365 Copilot decide what organisational data it can use to answer a user?
  options:
  - It can read everything in the tenant regardless of permissions
  - It only uses content the signed-in user already has permission to access
  - It uses a random sample of files for speed
  - It downloads the whole SharePoint library to a local cache
  answer: 1
  why: Copilot grounds answers through Microsoft Graph using the user's own identity, so it surfaces only
    content that user could already open themselves — it never elevates permissions.
- q: A user reports that the Copilot app does not appear in their Word and Teams. What should you check
    FIRST?
  options:
  - That their mailbox is over quota
  - That a Microsoft 365 Copilot licence is assigned to that user
  - That they cleared their browser cookies
  - That the tenant has DNS configured
  answer: 1
  why: Copilot is a paid add-on; if no Copilot licence is assigned to the user, the experience simply
    will not show up. Licence assignment is the first thing to verify.
- q: Why does enabling Copilot turn pre-existing SharePoint oversharing into a bigger problem?
  options:
  - Copilot deletes files it cannot read
  - Copilot changes the permissions on shared sites automatically
  - Copilot makes over-permissioned content far easier to discover and surface in answers
  - Copilot disables sharing links across the tenant
  answer: 2
  why: Copilot does not change permissions, but by searching across everything a user can access it makes
    loosely-permissioned content suddenly very easy to surface — so oversharing should be cleaned up before
    rollout.
- q: Where does a Tier 2 admin assign Microsoft 365 Copilot licences?
  options:
  - In the Microsoft 365 admin center under the user's Licenses and apps
  - In the Windows Control Panel
  - By editing the user's local registry
  - In the user's Outlook signature settings
  answer: 0
  why: Copilot licences are assigned per user in the Microsoft 365 admin center (Users, then the user,
    then Licenses and apps), the same place you manage other Microsoft 365 licences.
- q: A user complains that Copilot gave a confident but wrong answer. In one sentence, how do you coach
    them?
  answer: Explain that Copilot can sometimes hallucinate or misread context, so its output is a draft
    to be verified against the source documents, not a final authority.
  why: Copilot is a generative assistant; treating every answer as a starting draft and checking it against
    the grounded sources keeps users safe from acting on errors.
- q: In one sentence, what is the role of Microsoft Graph in Copilot?
  answer: Microsoft Graph is the layer that lets Copilot find and ground answers in the user's own emails,
    files, chats, and calendar that they already have access to.
  why: Grounding in Graph is what makes Copilot answers specific to your organisation rather than generic,
    while still honouring each user's existing permissions.
resources:
- label: Microsoft Learn — Microsoft 365 Copilot overview
  url: https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-overview
- label: Microsoft Learn — Set up Microsoft 365 Copilot
  url: https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-setup
- label: Microsoft Learn — Data, privacy, and security for Microsoft 365 Copilot
  url: https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy
- label: Microsoft Learn — MS-102 Microsoft 365 Administrator exam
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/ms-102/
---

## What Microsoft 365 Copilot actually is

**Microsoft 365 Copilot** is a large language model (an **LLM**) woven into the apps your users already live in — Word, Excel, PowerPoint, Outlook, and Teams. The thing that makes it useful at work is **grounding**: instead of answering from generic training data alone, Copilot pulls in your organisation's own content — emails, documents, chats, and calendar — through **Microsoft Graph**. Ask it to "summarise last week's project emails and draft a status update" and it reads the real threads the user can already see, then writes the draft.

The key Tier 2 mental model: Copilot is the model, **Microsoft Graph** is how it finds your data, and the user's **Entra ID** identity is what scopes what it may touch.

## Prerequisites before anyone can use it

Three things must line up. First, an eligible **Microsoft 365 Copilot licence** (a paid add-on) assigned to the user. Second, **supported app versions** — Copilot lives in current builds of the Microsoft 365 apps, so an out-of-date client simply will not show it. Third, a cloud **Entra ID** account, because Copilot uses that identity to decide what data it can reach.

## Permissions, and why oversharing is now a risk

This is the point examiners and security teams care about most. **Copilot never shows a user data they could not already access.** It honours the exact same permissions the user already has — it does not elevate anything.

The catch: many tenants have quietly **overshared** in SharePoint for years — "Everyone" links, wide site access, forgotten permissions. Before Copilot, that content was hard to stumble across. After Copilot, a single prompt like "what's our pricing strategy?" can surface it instantly. Copilot did not break permissions; it just made loose permissions visible. **Clean up oversharing before rollout.**

## The data protection boundary

Under **commercial data protection**, your prompts, the data Copilot retrieves through Graph, and the responses it generates are **not used to train the underlying foundation models**, and stay inside your Microsoft 365 service boundary. Copilot inherits your existing compliance controls — sensitivity labels, retention, and audit. Be ready to reassure nervous users and managers on this.

## Assigning Copilot licences

Licences are assigned per user in the **Microsoft 365 admin center**:

```text
Microsoft 365 admin center (admin.microsoft.com)
  > Users > Active users
  > select the user > Licenses and apps
  > tick "Microsoft 365 Copilot" > Save changes
```

For bulk assignment, group-based licensing or PowerShell scales better:

```powershell
# Microsoft Graph PowerShell SDK
Connect-MgGraph -Scopes "User.ReadWrite.All","Directory.ReadWrite.All"
# inspect a user's current licences
Get-MgUserLicenseDetail -UserId "jordan@contoso.com" | Select SkuPartNumber
```

## Common tickets and adoption support

"**Copilot isn't showing up**" — almost always no licence assigned, or an old app build; check both. **Expectation management** — users expect magic and get a helpful-but-imperfect assistant. **Hallucinations** — Copilot can sound confident and still be wrong, so coach users to treat every output as a draft and verify against the source. **Adoption** — better prompts get better results: give it a goal, context, and a desired format ("Draft a 3-bullet summary of this thread for my manager").

The Tier 2 role in a rollout: confirm prerequisites, assign and track licences, help remediate oversharing with the security team, and field the first wave of support tickets.

## Your task

In a test tenant, assign a Microsoft 365 Copilot licence to one user via the admin center, confirm Copilot appears in their Word and Teams, then write a one-page support note explaining the "Copilot isn't showing up" checklist and how to coach users on verifying outputs.
