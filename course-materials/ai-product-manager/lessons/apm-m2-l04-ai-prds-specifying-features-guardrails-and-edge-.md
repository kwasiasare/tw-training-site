---
course: ai-product-manager
title: 'AI PRDs: Specifying Features, Guardrails, and Edge Cases'
month: 2
monthTitle: AI Product Strategy and Roadmapping
lesson: 4
summary: Learn how to write a complete AI Product Requirements Document (PRD) that goes beyond traditional
  specs by defining intended model behavior, fallback flows, and safety guardrails for the messy, probabilistic
  edge cases AI products inevitably hit.
objectives:
- Explain how an AI PRD differs from a traditional software PRD and why probabilistic behavior changes
  the spec
- Specify desired model behavior using clear input/output contracts, examples, and acceptance criteria
- Design fallback flows for low-confidence, failure, and unsupported-input scenarios
- Define safety guardrails covering harmful content, privacy, bias, and misuse
- Enumerate and document edge cases systematically using a structured method
- Write measurable success metrics and evaluation criteria for AI features
video: apm-m2-l04-ai-prds-specifying-features-guardrails-and-edge-.mp4
quiz:
- q: What is the primary reason an AI PRD must differ from a traditional software PRD?
  options:
  - AI features are always more expensive to build
  - AI behavior is probabilistic and can be confidently wrong
  - AI requires more engineers than traditional software
  - Traditional PRDs don't include success metrics
  answer: 1
  why: AI is probabilistic — the same input can produce varying, sometimes confidently incorrect outputs
    — so the PRD must specify behavior under uncertainty, failure, and hard boundaries rather than a single
    deterministic output.
- q: Which acceptance criterion is best for an AI summarization feature?
  options:
  - Summaries should be accurate and helpful
  - Use GPT-4 at temperature 0.3
  - ≥90% of summaries are factually consistent with the source per human eval
  - Summaries must be short
  answer: 2
  why: Good acceptance criteria are measurable and tie to an eval. 'Accurate and helpful' is vague, specifying
    the model/temperature is implementation, and 'short' isn't tied to a measurable target or eval.
- q: When the model returns a low-confidence answer in a high-stakes context, what is an appropriate fallback?
  options:
  - Always return the answer anyway to avoid friction
  - Ask a clarifying question, show uncertainty, or route to a human
  - Silently retry until confidence is high
  - Block the user from the feature permanently
  answer: 1
  why: Below a confidence threshold the system should degrade gracefully — clarify, signal uncertainty,
    or escalate to a human — rather than letting a confident-sounding wrong answer through.
- q: For each safety guardrail, which two things should the PRD specify?
  options:
  - The model provider and the cost
  - The detection mechanism and the response
  - The launch date and the owner
  - The UI color and the copy
  answer: 1
  why: Every guardrail needs a way to detect violations (classifier, rule, deny list) and a defined response
    (block, refuse, redact, log).
- q: In one or two sentences, name three input dimensions you would use to enumerate edge cases for an
    AI feature.
  answer: 'Examples include: empty inputs, very long inputs, adversarial/malicious inputs, wrong-language
    inputs, ambiguous or off-topic inputs. Any three of these structured input dimensions are correct.'
  why: A structured method covers input dimensions like empty, oversized, adversarial, wrong-language,
    and ambiguous inputs so edge cases aren't left to imagination.
- q: Why should an AI PRD specify behavior rather than implementation (e.g., a specific model and temperature)?
  answer: Specifying behavior (e.g., required output quality and determinism) keeps the spec stable and
    testable while letting engineering choose and swap the best implementation; locking in a model or
    temperature couples the requirement to a transient technical choice.
  why: Behavior specs are measurable and durable; implementation details change and shouldn't be hard-coded
    into requirements, giving engineering flexibility to meet the contract.
resources:
- label: Google People + AI Guidebook (PAIR)
  url: https://pair.withgoogle.com/guidebook/
- label: Microsoft Responsible AI Standard & HAX Toolkit
  url: https://www.microsoft.com/en-us/haxtoolkit/
- label: OpenAI Safety Best Practices & Usage Policies
  url: https://platform.openai.com/docs/guides/safety-best-practices
- label: 'Lenny''s Newsletter: Writing PRDs for AI products'
  url: https://www.lennysnewsletter.com/
---

## Why AI PRDs Are Different

A traditional PRD specifies deterministic behavior: given input X, the system always returns output Y. AI features are **probabilistic** — the same input can yield different outputs, quality varies, and the system can be confidently wrong. Your PRD must therefore specify not just the happy path, but the *distribution* of behavior, what happens when the model is uncertain, and the boundaries the system must never cross.

An AI PRD answers three core questions traditional PRDs don't:
- What should the model do, and how good is good enough?
- What happens when the model fails or is unsure?
- What must the model *never* do, regardless of input?

## Anatomy of an AI PRD

A complete AI PRD typically includes:

1. **Problem & user need** — the job-to-be-done and why AI is the right tool (not every problem needs ML).
2. **Scope & non-goals** — what's explicitly out of bounds for v1.
3. **Model behavior spec** — input/output contract, tone, format, examples.
4. **Success metrics** — offline (eval sets) and online (product KPIs).
5. **Fallback flows** — behavior under low confidence or failure.
6. **Safety guardrails** — content, privacy, bias, misuse constraints.
7. **Edge cases** — enumerated unusual inputs and expected handling.
8. **Dependencies & constraints** — latency, cost, data, model provider.

## Specifying Model Behavior

Define an **input/output contract**. Be concrete:
- **Inputs:** types, formats, max length, languages supported.
- **Outputs:** structure (JSON schema, prose, citations), length limits, tone, reading level.
- **Examples:** include 5–10 gold-standard input/output pairs. Examples are clearer than prose for engineers and labelers.
- **Acceptance criteria:** e.g., "≥90% of summaries are factually consistent with source per human eval" rather than "summaries should be accurate."

Specify behavior, not implementation. Don't say "use GPT-4 with temperature 0.3" — say "responses must be deterministic enough that the same query returns substantively equivalent answers."

## Designing Fallback Flows

AI will be uncertain or wrong. Plan for it:
- **Confidence thresholds:** below a threshold, degrade gracefully (ask a clarifying question, show "I'm not sure," route to a human, or return a non-AI default).
- **Failure modes:** timeout, API error, empty/malformed output — define the user-facing behavior for each.
- **Human-in-the-loop:** when to escalate, and how the handoff preserves context.
- **Transparency:** tell users when AI is uncertain or when content is AI-generated.

A good rule: *never let a confident-sounding wrong answer reach the user in a high-stakes context without a guardrail.*

## Safety Guardrails

Guardrails are non-negotiable boundaries. Categories to cover:
- **Harmful content:** violence, self-harm, illegal instructions, hate speech.
- **Privacy:** PII handling, data retention, what's logged.
- **Bias & fairness:** test across demographic slices; define acceptable disparity.
- **Misuse & jailbreaks:** prompt injection, attempts to bypass restrictions.
- **Hallucination control:** require citations, restrict to retrieved context, or flag low-grounding answers.

For each guardrail, specify the **detection mechanism** (classifier, rules, allow/deny list) and the **response** (block, refuse with explanation, redact, log for review).

## Enumerating Edge Cases

Use a structured method so you don't rely on imagination alone:
- **Input dimensions:** empty, very long, adversarial, wrong language, off-topic, ambiguous.
- **User intent:** malicious, confused, edge demographics.
- **Context failures:** no relevant data retrieved, conflicting sources, stale data.
- **Operational:** degraded model, rate limits, downstream outages.

For each edge case, document: trigger, expected behavior, and how to test it. Build these into your eval set so regressions get caught.

## Putting It Together

The PRD is a living contract between PM, engineering, design, and safety/legal. Pair every behavior claim with a **measurable acceptance criterion** and a **test**. If you can't measure it, you can't ship confidently against it.
