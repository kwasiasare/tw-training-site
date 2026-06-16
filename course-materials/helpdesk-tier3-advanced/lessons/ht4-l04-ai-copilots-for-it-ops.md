---
course: helpdesk-tier3-advanced
title: AI copilots for IT operations
month: 4
monthTitle: AIOps, Monitoring & Agentic Automation
lesson: 4
summary: Use AI copilots — Microsoft Security Copilot and Copilot in Intune — to accelerate investigation
  and reporting, and learn to prompt them precisely while validating every answer against ground truth.
objectives:
- Describe what Security Copilot and Copilot in Intune do and where their data comes from
- Write precise, scoped prompts that produce reliable, verifiable operational answers
- Use copilots to summarise incidents, explain device non-compliance, and draft KQL
- Recognise and mitigate hallucination, stale context, and over-broad responses
- Apply least privilege and data-handling guardrails when using copilots on real telemetry
- Always validate copilot output against ground-truth telemetry before acting on it
video: ht4-l04-ai-copilots-for-it-ops.mp4
quiz:
- q: What primarily grounds Microsoft Security Copilot's answers about your environment?
  options:
  - A generic model with no access to your data
  - Your connected security and device data via plugins/connectors, combined with a large language model
  - Only public threat-intelligence blogs
  - A static spreadsheet you upload once
  answer: 1
  why: Security Copilot combines an LLM with connectors to your own data (Defender, Sentinel, Intune signals),
    so answers are grounded in your environment — but the LLM layer can still err, so verification remains
    essential.
- q: Which prompt is most likely to yield a reliable, verifiable operational answer?
  options:
  - '''Fix all my security problems.'''
  - '''Tell me everything about my tenant.'''
  - '''Summarise the 3 highest-severity Defender incidents in the last 24 hours, listing affected device
    names and the triggering alert for each.'''
  - '''Is my environment safe?'''
  answer: 2
  why: Precise prompts that specify scope, time window, and required fields produce answers you can verify
    against telemetry; vague prompts invite broad, unverifiable, or hallucinated responses.
- q: An admin asks Copilot in Intune why a device is non-compliant and acts on the answer without checking.
    What guardrail did they skip?
  options:
  - Least privilege
  - Validating AI output against ground-truth telemetry before acting
  - Multi-factor authentication
  - Network segmentation
  answer: 1
  why: Copilot explanations are a strong starting hypothesis, not verified fact; the skipped guardrail
    is confirming the explanation against the actual compliance policy and device state before acting.
- q: What is the safest way to treat a copilot's confident-sounding claim that you cannot immediately
    verify?
  options:
  - Accept it because the tool is paid for
  - Treat it as a hypothesis to confirm with a direct query or check before relying on it
  - Forward it to management as fact
  - Delete the device it mentions
  answer: 1
  why: Confidence is not correctness; unverifiable claims are hypotheses that must be confirmed with ground-truth
    data before they drive any decision or action.
- q: Give an example of a scoped, least-privilege prompt you would use with Copilot in Intune, and say
    why its scope matters.
  answer: '''List the Windows devices in the Finance group that failed the BitLocker compliance policy
    in the last 7 days, showing device name and last check-in.'' The scope (one policy, one group, a 7-day
    window, specific fields) keeps the query bounded, returns only what the task needs, and avoids pulling
    data about devices or users outside the investigation.'
  why: A bounded, group-scoped, field-limited prompt enforces least privilege at the prompt layer and
    produces a verifiable, relevant answer.
- q: Name two failure modes of AI copilots you must actively watch for, and how you mitigate each.
  answer: Hallucination — the model states something plausible but false; mitigate by verifying against
    telemetry. Stale or partial context — the copilot reasons over data that is out of date or incompletely
    connected; mitigate by confirming data freshness/coverage and re-running the underlying query directly.
  why: Hallucination and stale/partial grounding are the two most common ways copilots mislead operators;
    both are caught by independent verification.
resources:
- label: Microsoft Learn — What is Microsoft Security Copilot?
  url: https://learn.microsoft.com/en-us/copilot/security/microsoft-security-copilot
- label: Microsoft Learn — Copilot in Intune overview
  url: https://learn.microsoft.com/en-us/mem/intune/copilot/copilot-intune-overview
- label: Microsoft Learn — Prompting tips for Security Copilot
  url: https://learn.microsoft.com/en-us/copilot/security/prompting-tips
- label: Microsoft Learn — Azure OpenAI Service documentation
  url: https://learn.microsoft.com/en-us/azure/ai-services/openai/overview
---

## What a copilot is — and is not

An **AI copilot** is a large language model wired to your data through connectors. **Microsoft Security Copilot** grounds its answers in your Defender, Sentinel, and identity signals; **Copilot in Intune** reasons over your device, configuration, and compliance data. The copilot is an *accelerator* for investigation and reporting — it is not an oracle and not an autonomous actor. It speeds up the *observe, correlate, decide* stages from lesson one. The *act* stage stays yours.

The core mental model: a copilot turns a fuzzy question into a grounded draft answer fast. Your job is to ask precisely and to verify before you trust.

## Prompting for verifiable answers

Vague prompts produce vague, unverifiable, sometimes invented answers. Scoped prompts produce answers you can check. Specify the **time window**, the **scope** (group, policy, severity), and the **fields** you need.

```text
Weak:   "Is my environment safe?"
Strong: "Summarise the 3 highest-severity Defender incidents in the
         last 24h. For each, list affected device names and the
         triggering alert."
```

A good prompt is itself a least-privilege boundary: it tells the copilot to read only what the task needs.

## What copilots do well on endpoints

Three everyday wins. **Incident summarisation**: collapse a sprawling alert timeline into a readable narrative for an escalation. **Explaining non-compliance**: ask Copilot in Intune *why* a device failed a policy, getting a starting hypothesis in seconds. **Drafting KQL**: describe the question in English and get a query you then validate (lesson three) before running.

```text
Prompt to Copilot in Intune:
"List Windows devices in the Finance group that failed the BitLocker
 compliance policy in the last 7 days. Show device name and last check-in."
```

## The failure modes you must watch for

Three things go wrong. **Hallucination** — a confident, plausible, false statement. **Stale or partial context** — the copilot reasons over data that is out of date or only partly connected, so its answer is right about the wrong world. **Over-broad responses** — an answer that pulls or reveals more than the task warranted.

None of these are exotic; all three are caught the same way — by independent verification.

## The non-negotiable guardrail: validate against ground truth

Treat every copilot answer as a **hypothesis**, never a verified fact. Before acting:

```text
1. Re-run the underlying query directly (KQL) and compare.
2. Confirm data freshness and coverage — is the signal current and complete?
3. Check the claim against the authoritative source (the actual policy,
   the actual device state).
4. Only then decide. The act stage still requires human approval.
```

Confidence is not correctness. A copilot that is right 95% of the time is dangerous precisely because the 5% sounds identical to the 95%.

## Data handling and least privilege

Copilots operate on real, often sensitive telemetry. Scope prompts to the minimum data needed, respect the role-based access of the operator running them, and never paste secrets or wide data exports into a prompt. The copilot inherits your responsibility for the data it touches.

## Your task

Pick one real investigation. Write a weak prompt and a strong, scoped version of the same question. Run the strong one against Security Copilot or Copilot in Intune, then verify its key claim with a direct KQL query. Write three sentences: what the copilot said, what your verification found, and whether they agreed.
