---
course: agentic-ai-engineer
title: 'Capstone: Ship a Multi-Agent System'
month: 5
monthTitle: Capstone & Career Launch
lesson: 1
summary: 'This is the flagship piece you will show employers: a multi-agent system you designed, built,
  evaluated, and can defend. Earlier in the course you deployed a working app; here you raise it to portfolio-grade
  by holding it to an explicit rubric. You will architect a LangGraph orchestration over specialized agents
  with real tools and memory, build an evaluation harness with a versioned test set, and capture traces
  that prove how the system behaves. The deliverable is not a notebook but a reproducible repo with a
  design doc, quantified eval results, and a short demo a hiring manager can run and trust.'
objectives:
- Scope a multi-agent problem that genuinely needs orchestration and write it up as a design doc with
  user stories and an architecture diagram
- Implement a LangGraph system of 2-4 specialized agents with typed state, tool calls, and a supervisor
  or pipeline topology
- Wire in RAG over a real corpus and both session and persistent memory with bounded growth
- Build an evaluation harness with a versioned test set, outcome and trajectory metrics, and an LLM-as-judge
  rubric
- 'Capture end-to-end traces and report quantified results: task success rate, tool-call accuracy, latency,
  and cost per run'
- Self-assess the project against a portfolio-grade rubric and package it as a reproducible, demoable
  repo
video: age-m5-l01-capstone-ship-a-multi-agent-system.mp4
quiz:
- q: What is the single clearest signal that a capstone is 'portfolio-grade' rather than a demo?
  options:
  - It uses the largest available model
  - 'It is reproducible and evaluated: a hiring manager can run it from a README and see quantified eval
    results and traces'
  - It has the most agents possible
  - It runs only in the author's notebook with no setup notes
  answer: 1
  why: Portfolio-grade means another engineer can clone the repo, run it from documented commands, and
    verify your claims through eval numbers and traces. Reproducibility and evidence, not model size or
    agent count, are what convert a project into proof of skill.
- q: Why capture full execution traces for the capstone, not just final answers?
  options:
  - Traces make the model respond faster
  - Traces let you debug failures, measure tool-call accuracy and cost, and prove how the system actually
    behaved
  - Traces are required to call any LLM API
  - Traces replace the need for an evaluation set
  answer: 1
  why: A trace records every node, tool call, argument, token, and latency for a run. That is what makes
    failures debuggable and lets you report process metrics like tool-call accuracy and cost per run —
    evidence a final answer alone can never give.
- q: Which LangGraph topology is the safest default for a capstone you must explain and debug?
  options:
  - A fully autonomous peer-to-peer swarm
  - A single mega-prompt with no graph
  - A supervisor delegating to a small set of specialist nodes with explicit edges
  - Randomized agent hand-offs
  answer: 2
  why: A supervisor-over-specialists graph has explicit, inspectable control flow, which makes it predictable,
    debuggable, and easy to narrate in an interview. Swarms and randomized hand-offs are powerful but
    far harder to evaluate and explain.
- q: What belongs in the capstone's versioned evaluation set?
  options:
  - Only the single happy-path example that always works
  - 20-50 curated cases covering typical inputs, edge cases, and known failure modes, each with acceptance
    criteria
  - Thousands of unlabeled prompts with no expected behavior
  - Whatever the model generated last, unreviewed
  answer: 1
  why: 'A useful eval set is curated and versioned: a few dozen cases spanning normal use, edge cases,
    and past failures, each with a checkable acceptance criterion. That makes the suite a regression guard
    you can rerun on every change.'
- q: Why does the rubric reward a written 'known limitations and next steps' section?
  options:
  - It hides weaknesses from reviewers
  - It pads the README length
  - It demonstrates engineering judgment — you understand your system's failure modes and have a plan
  - It is required by LangGraph
  answer: 2
  why: 'Honestly naming limitations and a roadmap signals maturity: it shows you evaluated your own system
    critically and understand its boundaries. Reviewers trust a candidate who can articulate weaknesses
    far more than one who claims perfection.'
- q: In two to four sentences, describe the minimum set of artifacts your capstone repo must contain to
    be portfolio-grade, and why each matters.
  answer: 'It must contain a design doc with an architecture diagram (so a reviewer understands the problem
    and your topology), the source for the LangGraph agents plus RAG and memory (the working system),
    an evaluation harness with a versioned test set and reported metrics (proof it works), captured traces
    or screenshots (evidence of behavior), and a README with one-command setup and known limitations (reproducibility
    and judgment). Each artifact answers a different reviewer question: what, how, does it work, prove
    it, and can I run it. Together they turn effort into verifiable proof of capability. A short demo
    video ties them together for someone skimming.'
  why: A strong answer lists the design doc/diagram, the agent source, the eval harness with quantified
    results, traces as evidence, and a reproducible README, and explains that each maps to a distinct
    reviewer question (what, how, does it work, proof, reproducibility).
resources:
- label: LangGraph documentation (state, nodes, multi-agent)
  url: https://langchain-ai.github.io/langgraph/
- label: 'LangSmith: tracing and evaluation'
  url: https://docs.smith.langchain.com/
- label: Model Context Protocol (MCP) — connect agents to tools and data
  url: https://modelcontextprotocol.io
- label: 'GitHub: managing your profile README'
  url: https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
---

## The Project That Gets You Hired

Agentic AI Engineer is an emerging, portfolio-led role. There is no dominant certification you can wave at a hiring manager, so your evidence is the work itself. This capstone is the centerpiece of that evidence: one multi-agent system you designed, built, evaluated, and can defend line by line. Earlier in the course you already deployed a working app and learned the mechanics of endpoints, containers, and auth. This lesson is different — it is about raising that work to a **portfolio-grade bar** by holding it to an explicit rubric, capturing evidence, and packaging it so a stranger can run it and believe you.

The difference between a demo and a portfolio piece is not the model or the agent count. It is reproducibility and proof. A demo runs once on your machine. A portfolio piece ships with a design doc, a clean repo, an evaluation harness with numbers, traces that show how it behaved, and a README that lets someone else reproduce all of it.

## Step 1 — Scope and Write the Design Doc

Start from a user outcome, not a framework. Pick a task that **genuinely needs multiple cooperating agents** — for example a research analyst that plans, retrieves, drafts, and critiques, or a support triage system that classifies, looks up context, and proposes a resolution. If one prompt and one tool would do, it is not a multi-agent problem.

Write a one-page design doc before any code: a problem statement, three to five concrete user stories, the agents and their roles, the tools each may call, the orchestration topology, and your stop conditions. Include a clean architecture diagram. This document is both your build plan and the first artifact a reviewer reads. It is also where you state the **trade-offs you chose** — the sentence "I used a supervisor rather than a peer-to-peer network because control flow stays inspectable" is exactly the judgment interviewers probe for.

## Step 2 — Build the LangGraph System

Implement the system in **LangGraph** with typed state, explicit nodes, and explicit edges. Keep it to **2-4 agents** — every additional agent multiplies the failure surface and the cost of every run. The supervisor (orchestrator-worker) topology is the safest default: a coordinator node delegates subtasks to specialists and decides when the work is done. A fixed sequential pipeline (retrieve, draft, critique, finalize) is even simpler and cheaper when the stages are known in advance.

Give each agent a tight contract: a clear role, a small set of allowed tools defined with function calling or exposed through an **MCP server**, structured outputs, and a stop condition. Tools are where agents touch the real world — a search API, a database query, a code runner — so validate their arguments and outputs. Resist the temptation to let agents call anything; least privilege applies to tools just as it does to access.

## Step 3 — RAG and Memory

Most useful agents need grounding. Add **RAG** over a real corpus: chunk the documents (roughly 500-1000 tokens with overlap), embed them, store them in a vector index, and retrieve top-k with a metadata filter or a reranker. Always carry **source citations** through to the answer — without them you cannot measure faithfulness, and grounded citations are also what make the output trustworthy to a reader.

Add **memory** in two layers. Short-term memory is the in-session scratchpad and conversation state that LangGraph already threads through your graph. Long-term memory is a persisted store of user facts and prior results, in a vector or key-value store, with a **summarization step** so it does not grow without bound. Be explicit in your design doc about what is remembered, for how long, and why.

## Step 4 — The Evaluation Harness

Do not ship on vibes. Build evaluation as a first-class part of the project, because for this role the eval harness itself is a portfolio asset that almost no junior candidate has.

- **Versioned test set.** Curate 20-50 cases covering typical inputs, edge cases, and known failure modes. Each case has an input and a checkable acceptance criterion.
- **Outcome metrics.** Task success rate against acceptance criteria, plus format and constraint compliance.
- **Trajectory metrics.** Tool-call accuracy (right tool, right arguments, right order), step efficiency, and error recovery.
- **LLM-as-judge.** For qualities with no cheap programmatic check — helpfulness, faithfulness — use a strong model as a grader with an explicit rubric and structured JSON output, ideally reference-guided. Defend against position, verbosity, and self-preference bias.
- **Regression discipline.** Treat cases like unit tests: when you find a failure, add it to the set so it can never silently regress.

Report the numbers in your README. "Task success 86% on a 40-case suite; tool-call accuracy 94%; p95 latency 7.2s; ~$0.04 per run" is the language of an engineer who measures.

## Step 5 — Capture Traces

Instrument the system with a tracing tool such as **LangSmith**, Langfuse, or OpenTelemetry so every run records each node, tool call, argument, observation, token count, latency, and cost. Traces serve three purposes: they make failures debuggable, they are the source of your process metrics, and they are **evidence**. A screenshot of a trace in your README or demo shows a reviewer exactly how the system reasoned — far more convincing than a final answer alone.

## Guardrails and Reliability

A portfolio-grade system also has to survive the messy real world, and reviewers notice whether you thought about it. Add the guardrails that keep an agent honest and affordable: **input and output validation** with schemas, **loop and budget limits** (a hard cap on steps, tokens, and wall-clock time so a stuck agent cannot run up a bill), **retries with backoff** and a graceful fallback that returns a best partial answer instead of crashing, and **structured tool outputs** so downstream nodes can rely on the shape. Call these out in your design doc and demonstrate one in a trace — for example, a run that hits the step cap and exits cleanly. Showing that you anticipated failure, rather than hoping it would not happen, is exactly the maturity that separates a production engineer from a hobbyist.

## The Portfolio-Grade Rubric

Score your own project honestly against this bar before you call it done:

- **Problem fit (genuinely needs multiple agents).**
- **Architecture clarity (diagram + design doc with stated trade-offs).**
- **Implementation quality (clean LangGraph, bounded tools, RAG with citations, bounded memory).**
- **Evaluation (versioned set, outcome + trajectory metrics, judge rubric, quantified results).**
- **Observability (traces captured and shown).**
- **Reproducibility (one-command setup, pinned deps, secrets via env).**
- **Communication (README, short demo, honest limitations and next steps).**

If any row is weak, that is your next commit. A project that scores well across all seven rows is the kind of artifact that ends an interview with "when can you start."

## Package and Demo

Close the loop by packaging for a reviewer who has ninety seconds. The README leads with the problem and the architecture diagram, then setup, then the eval results and a trace screenshot, then limitations. Record a three to five minute demo showing the system planning, calling tools, retrieving, and producing a grounded answer. Make it reproducible: one command to install, one to run, secrets injected through environment variables and never committed. This single project, defensible end to end, is the asset the rest of this module turns into interviews and offers.
