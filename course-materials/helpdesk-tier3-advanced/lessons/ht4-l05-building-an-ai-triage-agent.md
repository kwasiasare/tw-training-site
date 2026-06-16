---
course: helpdesk-tier3-advanced
title: Building an AI agent for endpoint triage
month: 4
monthTitle: AIOps, Monitoring & Agentic Automation
lesson: 5
summary: Design an AI triage agent that ingests an alert, gathers telemetry through tightly-scoped read-only
  tools, reasons about likely cause, and produces a verified recommendation — without ever taking a consequential
  action itself.
objectives:
- 'Explain the agent pattern: a reasoning loop of plan, call tool, observe, repeat'
- Define read-only tools with least-privilege scopes for an endpoint triage agent
- Write a system prompt that constrains the agent's role, tools, and output format
- Ground the agent in telemetry so its conclusions are evidence-based, not invented
- Design the agent to stop at a recommendation and hand off to a human for action
- 'Apply guardrails: tool allow-lists, output schemas, confidence reporting, and audit logging'
video: ht4-l05-building-an-ai-triage-agent.mp4
quiz:
- q: What fundamentally distinguishes an AI 'agent' from a single LLM prompt?
  options:
  - An agent runs a loop where it can call tools, observe results, and decide its next step toward a goal
  - An agent uses a bigger model
  - An agent never uses a language model
  - An agent always acts without tools
  answer: 0
  why: An agent is an LLM in a control loop that can invoke tools, read their outputs, and choose subsequent
    steps — turning a one-shot answer into a multi-step, goal-directed process.
- q: For an endpoint TRIAGE agent, what scope should its tools have by default?
  options:
  - Full read-write admin over Intune and Defender
  - Read-only access scoped to exactly the telemetry triage needs
  - No access at all
  - Write access to remediate immediately
  answer: 1
  why: A triage agent investigates and recommends; it needs read-only, least-privilege access to relevant
    telemetry and must not hold write/remediation permissions — those belong to a separate, human-gated
    path.
- q: Why should a triage agent return a structured output (e.g., JSON with cause, evidence, confidence,
    recommendation) rather than free text?
  options:
  - It looks nicer
  - It uses fewer tokens always
  - Structured output is verifiable, auditable, machine-checkable, and forces the agent to cite evidence
    and confidence rather than rambling
  - Free text is impossible to generate
  answer: 2
  why: A schema makes the agent's reasoning inspectable and its claims checkable, and lets downstream
    systems and humans validate evidence and confidence before any action.
- q: An engineer gives the triage agent a tool that can isolate a device, to 'save a step'. What guardrail
    does this violate?
  options:
  - Output formatting
  - Least privilege / separation of investigation from consequential action
  - Time-window filtering
  - Prompt length limits
  answer: 1
  why: Granting a consequential, write-capable tool to an investigation agent removes the human gate and
    violates least privilege; isolation must remain a separate, approved action.
- q: Write a one-paragraph system prompt for an endpoint triage agent that constrains its role, its tools,
    and its required output.
  answer: 'You are an endpoint triage assistant. Your job is to investigate a single alert and produce
    a recommendation; you must never take any action that changes a device. Use only the provided read-only
    tools (query_telemetry, get_device_state, get_compliance_status) and never request other capabilities.
    Base every conclusion on evidence returned by those tools and cite it. Respond only as JSON with keys:
    likely_cause, evidence (list), confidence (low|medium|high), recommended_action, and requires_human_approval
    (always true). If evidence is insufficient, say so rather than guessing.'
  why: A strong system prompt fixes the role (triage, not action), restricts tools to read-only, mandates
    evidence-grounded conclusions, and enforces a verifiable JSON output with an always-on human gate.
- q: Name two telemetry-grounding measures that reduce the chance a triage agent invents a conclusion,
    and why each helps.
  answer: Require the agent to cite specific tool results as evidence for each claim (so an unsupported
    conclusion is visibly missing evidence) and have it report a confidence level and explicitly flag
    insufficient data (so low-evidence cases surface for human judgement instead of being papered over
    with a confident guess).
  why: Evidence citation and explicit confidence/insufficiency reporting make ungrounded reasoning detectable
    and route uncertain cases to humans.
resources:
- label: Microsoft Learn — AI agents for beginners (concepts and patterns)
  url: https://learn.microsoft.com/en-us/shows/ai-agents-for-beginners/
- label: Microsoft Learn — Azure OpenAI Service documentation
  url: https://learn.microsoft.com/en-us/azure/ai-services/openai/overview
- label: Microsoft Learn — Function calling with Azure OpenAI
  url: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling
- label: Microsoft Learn — KQL quick reference (for tool queries)
  url: https://learn.microsoft.com/en-us/azure/data-explorer/kql-quick-reference
---

## What an agent actually is

A single prompt gives one answer. An **agent** is a language model running inside a **control loop**: it plans, calls a **tool**, observes the result, and decides its next step — repeating until it reaches its goal. That loop is what lets an agent investigate, not just respond.

```text
Loop:  reason about the goal
       -> choose a tool and arguments
       -> run the tool, read the result
       -> enough evidence?  yes -> answer   no -> loop again
```

For endpoint triage, the goal is fixed and modest: *given an alert, find the likely cause and recommend a fix* — and then stop.

## Tools: read-only and least privilege

An agent is only as safe as the tools you hand it. A **triage** agent investigates; it must never change a device. So every tool is **read-only** and **scoped** to exactly what triage needs.

```python
tools = [
  {"name": "query_telemetry",     "scope": "read",  "desc": "Run a bounded KQL query against Log Analytics"},
  {"name": "get_device_state",    "scope": "read",  "desc": "Fetch Intune state for one device"},
  {"name": "get_compliance",      "scope": "read",  "desc": "Fetch compliance status for one device"},
]
# Note: NO isolate, NO wipe, NO push_config. Those are not the agent's job.
```

The moment you add a write-capable tool 'to save a step', you have removed the human gate. Don't. Investigation and consequential action live on separate paths.

## The system prompt is the contract

The **system prompt** fixes the agent's role, its allowed tools, and the shape of its output. Treat it as a contract, not a suggestion.

```text
You are an endpoint triage assistant. Investigate ONE alert and produce a
recommendation. You must NEVER take any action that changes a device.
Use only the provided read-only tools. Base every conclusion on evidence the
tools return, and cite it. Respond ONLY as JSON:
  { likely_cause, evidence[], confidence(low|med|high),
    recommended_action, requires_human_approval (always true) }
If evidence is insufficient, say so rather than guessing.
```

## Grounding: evidence over invention

Left unconstrained, a model will fill gaps with plausible fiction. You prevent this by **grounding** every conclusion in tool output. Two measures do most of the work: require **cited evidence** for each claim, and require an explicit **confidence** level plus a flag for **insufficient data**. Now an ungrounded conclusion is visibly missing its evidence, and uncertain cases route to a human instead of hiding behind false confidence.

## Structured output you can verify

Free text is hard to check; **structured JSON** is not. A schema with `likely_cause`, `evidence`, `confidence`, `recommended_action`, and `requires_human_approval` makes the agent's reasoning inspectable, machine-checkable, and auditable. The agent proposes; a human disposes.

## Guardrails recap for agents

Four controls keep a triage agent safe: a **tool allow-list** (only read-only tools exist), an **output schema** (verifiable, evidence-bearing), **confidence reporting** (uncertainty is surfaced, not hidden), and **audit logging** (every tool call and recommendation is recorded). The agent never crosses into the act stage — that is lesson six.

## Your task

Design, on paper or in code, a triage agent for one real alert type in your environment. List its read-only tools and their scopes, write its system prompt, and define its output JSON schema. Then write three lines explaining how a human reviews its recommendation before any action is taken.
