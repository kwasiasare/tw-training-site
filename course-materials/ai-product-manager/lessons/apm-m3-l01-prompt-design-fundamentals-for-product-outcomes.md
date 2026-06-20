---
course: ai-product-manager
title: Prompt Design Fundamentals for Product Outcomes
month: 3
monthTitle: Building, Evaluating, and Prompting AI Features
lesson: 1
summary: This lesson teaches AI Product Managers how to design and iterate on prompts that reliably meet
  product requirements. You'll learn the anatomy of a strong prompt, how to use structure, examples, and
  constraints to control model behavior, and how to build a reusable prompt library with versioning and
  lightweight evaluation tied to product outcomes.
objectives:
- Identify the core components of an effective prompt (role, task, context, constraints, output format)
  and explain how each maps to a product requirement
- Apply few-shot examples and explicit constraints to reduce variance and improve reliability of model
  outputs
- Translate fuzzy product requirements into testable prompt specifications and acceptance criteria
- Iterate on prompts systematically using a small evaluation set rather than one-off vibe checks
- Build and version a reusable prompt library that engineering can ship and maintain
video: apm-m3-l01-prompt-design-fundamentals-for-product-outcomes.mp4
quiz:
- q: Which of these best converts the requirement 'responses should be brief' into a usable prompt constraint?
  options:
  - '''Be concise and to the point'''
  - '''Keep it short, please'''
  - '''Respond in no more than 50 words'''
  - '''Avoid being too long'''
  answer: 2
  why: Measurable constraints like a word limit are testable and produce consistent behavior; the others
    are vague and leave the model to interpret 'brief'.
- q: What is the primary purpose of using an evaluation set of 15-30 inputs when iterating on a prompt?
  options:
  - To make the prompt longer
  - To replace opinion-based checks with repeatable evidence and catch regressions
  - To increase model temperature
  - To avoid using examples in the prompt
  answer: 1
  why: An eval set lets you measure changes objectively across representative and edge cases, and serves
    as a regression check when prompts or models change.
- q: Why should you separate instructions from user-supplied content using delimiters like XML tags?
  options:
  - It makes the model faster
  - It clarifies boundaries and reduces prompt-injection risk
  - It removes the need for an output format
  - It guarantees JSON output
  answer: 1
  why: Delimiters clearly mark which text is data versus instruction, improving reliability and lowering
    the chance that user content overrides your instructions.
- q: When iterating to improve a prompt's results, what is the recommended practice?
  options:
  - Change several variables at once to move faster
  - Change one variable at a time and re-run the eval set
  - Only test on the single example that failed
  - Trust your judgment after one good output
  answer: 1
  why: Changing one variable at a time isolates what caused the improvement; testing on the full eval
    set avoids overfitting to a single case.
- q: In one sentence, why are model choice and temperature considered part of a prompt spec?
  answer: Because the same prompt can produce different outputs depending on the model and temperature,
    so reproducing the validated behavior requires recording those settings.
  why: A prompt's results are inseparable from the model and settings used; documenting them ensures the
    tuned behavior is reproducible in production.
- q: Name one component of a well-structured prompt and the product requirement it typically maps to.
  answer: 'Output format maps to integration/parsing needs (or: constraints map to brand/safety; examples
    map to quality/edge cases; role maps to tone/domain).'
  why: Each prompt component is a knob that addresses a specific product requirement, which is why mapping
    them helps translate requirements into prompts.
resources:
- label: OpenAI Prompt Engineering Guide
  url: https://platform.openai.com/docs/guides/prompt-engineering
- label: Anthropic Prompt Engineering Documentation
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- label: Learn Prompting (open-source course)
  url: https://learnprompting.org/
- label: OpenAI Evals — building evaluation sets
  url: https://github.com/openai/evals
---

## Why prompt design is a PM skill

Prompts are the interface between a product requirement and a model's behavior. As an AI PM, you may not write every production prompt, but you must be able to specify what 'good' looks like, draft prompts to validate feasibility, and define the acceptance criteria engineering builds against. A well-designed prompt is the cheapest, fastest lever you have to change product behavior before reaching for fine-tuning or new models.

## The anatomy of a reliable prompt

Most effective prompts contain some combination of these building blocks:

- **Role / persona**: who the model is acting as ("You are a support triage assistant"). Sets tone and domain.
- **Task instruction**: the single, clear action to perform. Lead with the verb.
- **Context / inputs**: the data the model needs (user message, retrieved documents, customer tier).
- **Constraints**: length, tone, what NOT to do, safety boundaries, allowed values.
- **Output format**: the exact shape of the response (JSON schema, markdown, bullet list) so it's parseable downstream.
- **Examples (few-shot)**: 1-5 input/output pairs that demonstrate the pattern.

Think of these as knobs. Each maps to a product requirement: format maps to integration needs, constraints map to brand and safety, examples map to quality and edge cases.

## From product requirement to prompt spec

Fuzzy requirements like "summarize support tickets nicely" must become testable specs. Convert them:

- Requirement: *Summaries must be skimmable for agents.*
- Spec: *Output 3-5 bullets, each under 15 words, neutral tone, must include the customer's requested action.*
- Acceptance criteria: *On 20 sample tickets, 90%+ include the requested action and stay within bullet limits.*

If you can't write acceptance criteria, you don't yet have a prompt spec — you have a wish.

## Techniques that move reliability

- **Be explicit, not clever.** Ambiguity is the enemy of consistency. State edge-case handling directly: "If the ticket has no clear action, output: 'No action requested.'"
- **Structure the output.** Ask for JSON when downstream code parses it. Provide the schema in the prompt.
- **Use delimiters** (triple quotes, XML tags) to separate instructions from user-supplied content. This also reduces prompt-injection risk.
- **Few-shot for tricky patterns.** Examples teach format and tone faster than prose. Include at least one hard/edge case.
- **Decompose complex tasks.** Chain or break into steps rather than one giant prompt.
- **Constrain the failure mode.** Tell the model what to do when it's unsure rather than letting it hallucinate.

## Iterating systematically (not vibe-checking)

Good prompt iteration looks like lightweight evaluation:

1. Build a small **eval set** of 15-30 representative inputs, including edge cases and known-hard examples.
2. Define **pass/fail criteria** per output (format valid? action included? on-tone?).
3. Change **one variable at a time** and re-run the set.
4. Track results in a simple table; keep the winning version.

This turns prompt work from opinion into evidence, and gives you a regression check when models or prompts change.

## Building a prompt library

Treat prompts as product assets:

- **Version** each prompt (v1, v2) with a changelog and date.
- Store the **prompt, intended use, eval results, and owner**.
- Use **variables/templates** ({{customer_name}}, {{ticket_body}}) so prompts are reusable.
- Separate the **system prompt** (stable instructions) from **user content** (dynamic).
- Note **model + settings** (temperature, max tokens) the prompt was tuned for — they're part of the spec.

A shared library prevents teams from reinventing prompts, enables A/B testing, and makes handoff to engineering clean.

## Common pitfalls

- Overloading one prompt with too many tasks.
- Vague constraints ("be concise") instead of measurable ones ("under 50 words").
- No edge-case handling, so the model improvises.
- Iterating on a single example and overfitting.
- Forgetting that temperature and model choice are part of the result.
