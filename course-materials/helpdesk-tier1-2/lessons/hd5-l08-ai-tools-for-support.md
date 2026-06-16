---
course: helpdesk-tier1-2
title: 'AI tools for support: Copilot and AI ticket triage'
month: 5
monthTitle: Modern Endpoint Management with AI (MD-102)
lesson: 8
summary: Meet Microsoft Copilot and its support-focused variants, and learn how to use AI to triage, summarize,
  prioritize, and reply to tickets faster while always verifying the output before you trust it.
objectives:
- Describe Microsoft Copilot and its key variants (Copilot chat, Copilot in Intune, Microsoft Security
  Copilot)
- Use AI to summarize long ticket threads and turn vague user reports into structured troubleshooting
  steps
- Write prompts that classify, prioritize, and route tickets and suggest likely causes and KB articles
- Draft clear, professional user-facing replies with AI and edit them for accuracy and tone
- Use Copilot in Intune to ask natural-language questions about your tenant's devices and policies
- 'Apply a verify-before-trust discipline: check facts, protect PII, and never send AI replies blindly'
video: hd5-l08-ai-tools-for-support.mp4
quiz:
- q: Which Copilot variant is designed specifically to answer natural-language questions about your tenant's
    devices, policies, and apps?
  options:
  - Copilot in Intune
  - Copilot in Excel
  - GitHub Copilot
  - A generic public chatbot
  answer: 0
  why: Copilot in Intune is embedded in the Intune admin center and can answer questions about your managed
    devices, configuration, and policies using your tenant's own data.
- q: 'A user files a vague ticket: ''My laptop is broken.'' What is a good first use of AI here?'
  options:
  - Immediately email them a fix you guessed
  - Close the ticket as 'no detail'
  - Ask AI to turn the report into structured clarifying questions and likely troubleshooting steps
  - Escalate straight to Tier 3
  answer: 2
  why: AI is excellent at converting a vague report into a structured set of clarifying questions and
    a ranked list of likely causes, which speeds up triage without guessing.
- q: Why should you never send an AI-drafted reply to a user without reviewing it?
  options:
  - AI replies are always too short
  - It might contain inaccurate facts, the wrong tone, or leaked details, and AI can hallucinate
  - Email systems block AI text
  - Users prefer no replies
  answer: 1
  why: AI can hallucinate facts, miss context, use the wrong tone, or echo sensitive data. You are accountable
    for what you send, so always read and correct it first.
- q: Which is the security-operations focused Copilot used by SOC and security teams?
  options:
  - Copilot in Word
  - Microsoft Security Copilot
  - Copilot in Teams
  - Bing image creator
  answer: 1
  why: Microsoft Security Copilot is the generative AI security product that helps analysts investigate
    incidents, summarize alerts, and respond to threats.
- q: Give one example of sensitive information you must NOT paste into a public LLM when triaging a ticket.
  answer: Passwords, access tokens, customer PII, or internal IP addresses and secrets.
  why: Public LLMs may log or train on input, so credentials, PII, and confidential tenant data must never
    be pasted into them.
- q: In one sentence, how does AI help you prioritize a flood of tickets?
  answer: AI can classify each ticket by category and urgency and suggest a priority and routing queue,
    so you triage faster, but you confirm the calls yourself.
  why: Classification and prioritization are pattern tasks AI does well, but the human owns the final
    routing and priority decision.
resources:
- label: Microsoft Copilot — documentation hub
  url: https://learn.microsoft.com/en-us/copilot/
- label: Microsoft — Copilot in Intune overview
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/copilot-intune-overview
- label: Microsoft Security Copilot — documentation
  url: https://learn.microsoft.com/en-us/copilot/security/
- label: 'Microsoft — Exam MD-102: Microsoft 365 Endpoint Administrator'
  url: https://learn.microsoft.com/en-us/credentials/certifications/exams/md-102/
---

## What is Microsoft Copilot?

**Microsoft Copilot** is Microsoft's family of generative AI assistants built into the tools you already use. For a support tech, three variants matter most. **Copilot chat** (the general assistant in Microsoft 365, Edge, and Windows) helps you summarize, draft, and reason in plain language. **Copilot in Intune** is embedded in the Intune admin center and can answer natural-language questions about *your tenant's own* devices, policies, and apps. **Microsoft Security Copilot** is the security-operations assistant that helps SOC teams investigate incidents and alerts.

You will also meet general LLM assistants (the public chatbots). They are powerful for drafting and explaining, but they do **not** see your tenant data and they carry real privacy and accuracy risks.

## Triage: from chaos to a sorted queue

Tier 1 lives in the ticket queue. AI shines at the boring-but-critical triage work: reading a long thread, pulling out what matters, and suggesting where the ticket should go. Use it to **summarize** a 40-message email chain into three lines, **classify** a ticket by category, and **suggest a priority** and routing queue.

```text
Summarize this ticket thread in 4 bullets: the user's core problem,
what has already been tried, the current state, and the single most
likely next step. Then suggest a category (hardware / network /
identity / app) and a priority (P1-P4) with a one-line reason.
[paste thread]
```

## Turning a vague report into structured steps

Users rarely write good tickets. "My laptop is broken" is a starting point, not a diagnosis. Ask AI to convert the vague report into structured clarifying questions and a ranked list of likely causes plus the first diagnostic step for each.

```text
A user reports: "Outlook keeps asking me to sign in and then fails."
List the 5 most likely causes ranked by probability for a Microsoft
365 / Entra ID managed device, the one question I should ask the user
for each, and the first thing I should check. Keep it concise.
```

## Drafting replies and finding KB articles

AI is great at drafting a **clear, friendly, professional reply** at the right reading level. It can also suggest which **KB articles** likely apply. But you are accountable for what you send.

```text
Draft a short, friendly reply telling the user we have reset their
password, they must change it at next sign-in, and to call us if MFA
fails. Plain English, no jargon, under 80 words.
```

## Copilot in Intune: ask your tenant

Inside the Intune admin center you can ask Copilot questions about real devices.

```text
1. Go to https://intune.microsoft.com
2. Open a device or a policy blade
3. Open the Copilot pane
4. Ask: "Why is this device showing as non-compliant?"
   or "Which policies are assigned to this device?"
```

This grounds the answer in *your* data rather than the open internet, which makes it far more trustworthy than a public chatbot for tenant questions.

## Verify before you trust

This is the rule that separates a pro from a liability. **AI can hallucinate** — it can invent facts, KB numbers, and error-code meanings with total confidence. So: never send an AI reply blindly; read every line and confirm the facts. Watch for **PII and secrets** — never paste passwords, tokens, customer data, or internal IPs into a public LLM. Cross-check any technical claim against **official Microsoft docs**. AI gives you a faster first draft and a set of hypotheses, not the final word.

## Your task

Take one real (or realistic) messy ticket thread. Use an AI assistant to (1) summarize it in four bullets, (2) suggest a category and priority, and (3) draft a user reply. Then edit the reply for accuracy and tone, and write one sentence on what you had to correct.
