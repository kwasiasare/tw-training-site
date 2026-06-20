---
course: ai-app-developer-2026
title: Prompt Engineering Fundamentals
month: 1
monthTitle: Python and LLM Foundations
lesson: 3
summary: 'A practical introduction to prompt engineering: how to write structured prompts, use few-shot
  examples, and enforce reliable output formats so LLMs behave predictably in real applications.'
objectives:
- Explain the anatomy of an effective prompt (role, task, context, constraints, output format)
- Apply zero-shot and few-shot prompting to improve accuracy and consistency
- Specify and enforce structured outputs such as JSON for downstream parsing
- Use system, user, and assistant message roles correctly in chat APIs
- Diagnose and fix common prompt failures through iterative refinement
video: aad-m1-l03-prompt-engineering-fundamentals.mp4
quiz:
- q: Which chat message role should hold persistent rules and the model's assigned role?
  options:
  - user
  - system
  - assistant
  - function
  answer: 1
  why: The system message sets persistent behavior and global constraints, making it the right place for
    the role and stable rules.
- q: When is few-shot prompting most useful?
  options:
  - When you want to save the most tokens
  - When the task format is hard to describe or the model repeats mistakes
  - Only for creative writing tasks
  - When you have no example inputs
  answer: 1
  why: Few-shot examples demonstrate the exact input-output mapping, which helps when a format is hard
    to describe in words or the model keeps making the same error.
- q: What is the best practice after asking an LLM to return JSON?
  options:
  - Trust the output and use it directly
  - Validate it in code and add a retry path for malformed output
  - Always increase temperature
  - Convert it to plain prose first
  answer: 1
  why: Models can produce malformed JSON, so you should validate (e.g., json.loads plus schema checks)
    and retry when parsing fails.
- q: Which temperature setting is most appropriate for a deterministic classification task?
  options:
  - Around 0 to 0.3
  - Around 0.7
  - Around 1.0
  - Above 1.5
  answer: 0
  why: Lower temperatures reduce randomness, producing more consistent and deterministic outputs suited
    to classification and extraction.
- q: List the five common components of a well-structured prompt.
  answer: Role, task, context, constraints, and output format.
  why: These five elements remove ambiguity and reliably steer the model toward the desired behavior and
    output shape.
- q: In one sentence, why should prompts be treated like code?
  answer: Because they directly determine output behavior and should be versioned, tested, and iteratively
    refined for reliability.
  why: Treating prompts as code emphasizes reproducibility, testing against real inputs, and controlled
    changes — essential for production reliability.
resources:
- label: OpenAI Prompt Engineering Guide
  url: https://platform.openai.com/docs/guides/prompt-engineering
- label: Anthropic Prompt Engineering Overview
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- label: Learn Prompting (open-source guide)
  url: https://learnprompting.org/
- label: OpenAI Structured Outputs Documentation
  url: https://platform.openai.com/docs/guides/structured-outputs
---

## Why Prompt Engineering Matters

An LLM is a powerful but literal collaborator: it does what your prompt implies, not what you secretly intended. Prompt engineering is the discipline of writing instructions that reliably steer model behavior for a specific task. For AI application developers, prompts are *code* — they should be versioned, tested, and made deterministic where possible.

## Anatomy of a Good Prompt

Strong prompts usually contain these components:

- **Role**: who the model should act as ("You are a senior support agent").
- **Task**: the precise instruction ("Classify the ticket into one of these categories").
- **Context**: relevant data, examples, or background the model needs.
- **Constraints**: tone, length, what to avoid, edge-case handling.
- **Output format**: the exact shape of the response (JSON keys, bullet list, etc.).

A vague prompt like "Summarize this" produces inconsistent output. A structured prompt removes ambiguity:

```
You are a concise technical editor.
Summarize the text below in exactly 3 bullet points.
Each bullet must be under 15 words.

Text: """{document}"""
```

## Chat Message Roles

Modern chat APIs separate messages into roles:

- **system**: sets persistent behavior and rules. Put your role and global constraints here.
- **user**: the task and input data.
- **assistant**: prior model responses (used for multi-turn context or few-shot examples).

Keep stable instructions in the system message and variable data in user messages so you can cache and reuse the system prompt.

## Zero-Shot vs Few-Shot

**Zero-shot** prompting just describes the task. It's fast and cheap and often enough for simple tasks.

**Few-shot** prompting includes labeled examples that demonstrate the desired input-output mapping. Use few-shot when:

- The task has a specific format you can't easily describe in words.
- The model keeps making the same mistake.
- You need consistent style or labeling.

```
Classify sentiment as positive, negative, or neutral.

Review: "Loved it, works great!" -> positive
Review: "Broke after one day." -> negative
Review: "It's okay, nothing special." -> neutral
Review: "{new_review}" ->
```

Keep examples diverse and representative of edge cases. 2–5 examples is a good starting range; more isn't always better and costs tokens.

## Enforcing Output Format

For app integration, you usually need machine-parseable output. Tactics:

- Ask explicitly for **JSON** and specify the schema and keys.
- Say "Respond with ONLY valid JSON, no markdown or prose."
- Provide a sample of the exact output.
- Use structured-output / JSON-mode features when the API offers them.

```
Return a JSON object with this exact shape:
{"category": string, "priority": "low"|"medium"|"high", "needs_human": boolean}
Do not include any text outside the JSON.
```

Always validate the output in code (e.g., `json.loads` plus schema checks) and add a retry path for malformed responses.

## Iterative Refinement

Prompt engineering is empirical. A practical loop:

1. Write a first prompt and run it on several real inputs.
2. Collect failures and categorize them (format errors, wrong content, hallucination).
3. Add a constraint, example, or clarification targeting that failure class.
4. Re-test against your input set to avoid regressions.

Keep a small evaluation set of representative inputs so you can measure whether a change actually helps.

## Common Pitfalls

- **Overstuffing**: too many instructions dilute focus. Be concise and ordered.
- **Conflicting rules**: contradictory constraints confuse the model.
- **Implicit assumptions**: spell out edge-case handling ("If unsure, return \"unknown\"").
- **Ignoring temperature**: lower temperature (0–0.3) for deterministic tasks like classification and extraction.
