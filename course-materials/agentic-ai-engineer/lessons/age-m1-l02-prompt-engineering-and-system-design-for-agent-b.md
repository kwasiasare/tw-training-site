---
course: agentic-ai-engineer
title: Prompt Engineering and System Design for Agent Behavior
month: 1
monthTitle: LLM Foundations and Tool-Using Agents
lesson: 2
summary: Learn to design system prompts and few-shot patterns that reliably steer LLM agent behavior,
  control tone, enforce output formats, and reduce hallucinations in production agent workflows.
objectives:
- Write structured system prompts that define an agent's role, constraints, and success criteria
- Apply few-shot and exemplar patterns to shape output format, tone, and reasoning style
- Implement guardrails and grounding techniques to reduce hallucinations
- Design prompts that integrate cleanly with tool-calling and multi-step agent loops
- Evaluate and iterate on prompts using measurable behavioral criteria
video: age-m1-l02-prompt-engineering-and-system-design-for-agent-b.mp4
quiz:
- q: Which prompt instruction is most likely to be followed reliably by a model?
  options:
  - '"Don''t make the response too long or complicated"'
  - '"Respond in valid JSON matching the provided schema"'
  - '"Try to be helpful and accurate when you can"'
  - '"Avoid being unclear in your answers"'
  answer: 1
  why: Models follow concrete, positive, and specific instructions—like an explicit output format—far
    better than vague negative phrasing.
- q: What is a primary technique for reducing hallucinations in a grounded agent?
  options:
  - Increasing the temperature setting
  - Instructing the agent to answer only from retrieved context and cite sources
  - Removing all examples from the prompt
  - Forbidding the agent from ever saying 'I don't know'
  answer: 1
  why: Grounding answers in provided context and requiring citations keeps the model from inventing facts,
    while allowing uncertainty also helps.
- q: Why should an agent's system prompt include an explicit stopping condition?
  options:
  - To make the prompt longer
  - Because agents run in loops and need to know when the task is complete to avoid redundant or infinite
    cycles
  - To increase token usage
  - To replace the need for tools
  answer: 1
  why: Agents iterate over reasoning and tool calls, so a clear stopping condition prevents endless loops
    and tells the agent when to return the final answer.
- q: How many few-shot examples are generally recommended, and what should they include?
  options:
  - Ten or more identical examples
  - Zero examples in all cases
  - 2-4 diverse examples including a tricky case and a refusal
  - One example covering only the easiest case
  answer: 2
  why: A small set of 2-4 diverse, high-quality examples—covering an edge case and a refusal—teaches format
    and behavior without wasting context budget.
- q: In one or two sentences, why is allowing an agent to say 'I don't know' an effective anti-hallucination
    measure?
  answer: Because prompts that implicitly demand an answer push the model to fabricate one; giving it
    an explicit uncertainty or escalation path lets it decline rather than invent unsupported facts.
  why: Permitting uncertainty removes the implicit pressure to always produce an answer, which is a common
    driver of hallucination.
- q: Name one reason to treat prompts like versioned code with an evaluation set.
  answer: So you can measure behavioral metrics, change one variable at a time, and catch regressions
    when improving one behavior breaks another.
  why: Systematic versioning and evals make prompt iteration measurable and prevent silent regressions.
resources:
- label: OpenAI Prompt Engineering Guide
  url: https://platform.openai.com/docs/guides/prompt-engineering
- label: Anthropic Prompt Engineering Documentation
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- label: DAIR.AI Prompt Engineering Guide
  url: https://www.promptingguide.ai/
- label: 'ReAct: Synergizing Reasoning and Acting in Language Models'
  url: https://arxiv.org/abs/2210.03629
---

## Why Prompt Design Matters for Agents

In agentic systems, the system prompt is the agent's *operating contract*. Unlike a one-off chat, an agent runs in a loop—reasoning, calling tools, and acting on results—so small ambiguities compound across turns. A well-engineered prompt is the cheapest, fastest lever you have to control reliability before reaching for fine-tuning or complex orchestration.

## Anatomy of an Effective System Prompt

A production system prompt typically has these components, in roughly this order:

1. **Role & identity** — who the agent is and its domain of competence.
2. **Objective** — the single primary goal it optimizes for.
3. **Constraints & policies** — what it must never do, safety rules, scope limits.
4. **Tools & capabilities** — what actions are available and when to use them.
5. **Output contract** — exact format expected (JSON schema, structure, length).
6. **Reasoning guidance** — how to think (step-by-step, verify before answering).
7. **Tone & persona** — voice, formality, audience.

Keep each section terse and unambiguous. Models follow concrete, positive instructions ("respond in valid JSON") better than vague negatives ("don't be too verbose").

## Few-Shot and Exemplar Patterns

Few-shot examples teach by demonstration. Use them when:

- The desired **output format** is hard to describe but easy to show.
- You want a consistent **reasoning trace** or tone.
- Edge cases need explicit handling.

Best practices:

- Show 2-4 high-quality, diverse examples—including at least one tricky case.
- Make examples mirror the *exact* format you expect at inference time.
- Include a counter-example showing how to refuse or escalate when appropriate.
- Keep examples short to save context budget; quality beats quantity.

## Reducing Hallucinations

Hallucinations drop sharply when you:

- **Ground the model**: provide retrieved context and instruct it to answer *only* from that context.
- **Permit uncertainty**: explicitly allow "I don't know" or escalation. Models hallucinate partly because prompts implicitly demand an answer.
- **Cite sources**: require the agent to reference which document/tool result supports each claim.
- **Separate retrieval from generation**: don't let the model invent facts it should look up via a tool.
- **Verify before finalizing**: add a self-check step ("List assumptions and confirm each is supported").

## Designing for the Agent Loop

Agents reason, call tools, and observe results repeatedly. Your prompt should:

- Define a clear **stopping condition** ("Stop and return the final answer once the user's request is fully satisfied").
- Specify **how to handle tool errors** (retry once, then report).
- Discourage redundant tool calls and infinite loops.
- Reserve the output contract for the *final* answer, keeping intermediate reasoning separate.

## Iterating and Evaluating

Treat prompts like code: version them, and test against a fixed set of cases.

- Define **behavioral metrics**: format adherence, factual accuracy, refusal correctness, tone.
- Build a small **eval set** of representative and adversarial inputs.
- Change one variable at a time; measure before and after.
- Watch for regressions—improving one behavior can break another.

## Quick Reference: Do / Don't

- **Do** use positive, concrete instructions and explicit output schemas.
- **Do** allow uncertainty and escalation paths.
- **Don't** stack contradictory rules or bury critical constraints mid-paragraph.
- **Don't** rely on a clever prompt to fix a problem that needs a tool or retrieval.
