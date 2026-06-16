---
course: kwasi-GenAI
title: 'The capstone: integrating your four deliverables'
month: 6
monthTitle: Capstone & Career
lesson: 1
summary: Combine the four phase deliverables — a tool-using API client, a RAG system, a multi-step agent,
  and an eval-plus-guardrail layer — into one coherent portfolio system, and learn how the pieces actually
  connect.
objectives:
- Describe how the four phase deliverables fit into a single layered architecture
- Explain why RAG, tool use, and agency are complementary rather than competing patterns
- Position the eval and guardrail layer as a cross-cutting concern, not a fifth feature
- Define clean seams between components so each can be tested in isolation
- Map the integrated system onto the AWS or Azure infrastructure you already operate
- Plan a capstone build that a hiring manager could read in five minutes
video: g6-l01-capstone-integration.mp4
quiz:
- q: In the integrated capstone, what is the agent's role relative to the other three deliverables?
  options:
  - It replaces RAG and tool use entirely
  - It is the orchestration layer that decides when to retrieve, when to call a tool, and when to stop
  - It is only a user-interface concern
  - It runs after the eval layer has finished
  answer: 1
  why: The multi-step agent is the brain that plans the loop — it chooses when to retrieve context, when
    to invoke a tool, and when the task is complete; RAG and tool use are capabilities it draws on.
- q: Where do the eval suite and guardrails sit in the architecture?
  options:
  - Only at the very end, after the system ships
  - As a cross-cutting layer that wraps every model call and every tool result
  - Inside the RAG retriever only
  - They are optional and can be removed for the demo
  answer: 1
  why: 'Evals and guardrails are cross-cutting: input validation, output checks, and offline eval runs
    touch every component, which is exactly the safety-and-deploy story that sets you apart.'
- q: Why is RAG a better fit than fine-tuning for grounding the capstone in your own documents?
  options:
  - RAG is always more accurate than any model
  - RAG lets you update knowledge by changing data, not retraining, and gives you citations
  - Fine-tuning is impossible on Claude
  - RAG removes the need for a model
  answer: 1
  why: RAG grounds answers in retrieved passages you can cite and update independently of the model —
    far cheaper and more auditable than retraining for a portfolio project.
- q: Name one clean seam you should design between the agent and the tool layer.
  answer: A typed tool interface (JSON schema in, structured tool_result out) so the agent and the tools
    can each be tested and swapped independently.
  why: A well-defined tool contract lets you unit-test tools without the model and mock tools when testing
    the agent's planning loop.
- q: In one sentence, what makes the four deliverables 'one coherent system' rather than four demos?
  answer: They share a single request flow where the agent orchestrates retrieval and tools while the
    eval-and-guardrail layer wraps every step, so data flows end to end through one architecture.
  why: Coherence comes from a shared flow and shared infrastructure, not from four separate scripts living
    in the same repository.
- q: Which cloud building block would you naturally use to host the integrated capstone, given your background?
  options:
  - A spreadsheet
  - A containerised service behind your existing CI/CD, with secrets in a managed vault and logs/metrics
    wired in
  - A single laptop left running
  - A public pastebin
  answer: 1
  why: You already know how to ship containers through CI/CD with managed secrets and observability —
    that operational maturity is the differentiator, so reuse it for the capstone.
resources:
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/research/building-effective-agents
- label: Anthropic docs — Tool use overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: Anthropic docs — Reduce hallucinations (grounding & RAG patterns)
  url: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- label: AWS — Well-Architected Framework
  url: https://aws.amazon.com/architecture/well-architected/
- label: 'Microsoft — Azure Architecture Center: AI architecture design'
  url: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/
---

## From four exercises to one system

Over the last four phases you built four things: a **tool-using API client** that lets Claude call your functions, a **RAG system** that grounds answers in your own documents, a **multi-step agent** that plans and acts in a loop, and an **eval-plus-guardrail layer** that measures quality and blocks bad behaviour. Each was a good exercise on its own. The capstone asks a harder, more valuable question: how do they become **one coherent portfolio system**?

The answer is architecture. These four pieces are not four competing approaches — they are four layers of the same stack.

## The layered view

Think of it as a request flowing top to bottom and back up.

```text
        user request
             |
   [ guardrails: input validation ]
             |
   [ AGENT: plan the next step ]
        /          \
  [ RAG retrieve ]   [ tool call ]
        \          /
   [ model call (Claude) ]
             |
   [ guardrails: output checks ]
             |
   [ eval logging / offline eval ]
             |
        response
```

The **agent** is the orchestrator — the brain that decides what to do next. On each turn it may decide it needs **context** (so it calls the RAG retriever), or it needs to **act in the world** (so it calls a tool), or it has enough to answer (so it stops). RAG and tool use are *capabilities the agent reaches for*, not separate programs.

The **eval and guardrail layer is cross-cutting**. It is not a fifth feature bolted on the end; it wraps every model call and every tool result. Input guardrails validate the request, output guardrails check the response, and your eval harness records traces so you can measure quality offline. This is the safety-and-deploy story that, frankly, most applied AI engineers cannot tell — and you can.

## Why the pieces are complementary

- **RAG** answers "what does the model *know* about *my* world?" It grounds responses in retrieved passages you can cite and update by changing data, not by retraining.
- **Tool use** answers "what can the model *do*?" It lets Claude check inventory, send an email, or query a database through a typed interface.
- **The agent** answers "in what *order*, and when do we *stop*?" It runs the loop, interleaving retrieval and tools until the task is done.
- **Evals and guardrails** answer "is it *good*, and is it *safe*?" They turn a demo into something you would actually deploy.

A real assistant needs all four. Ground it (RAG), let it act (tools), let it plan (agent), and prove it works safely (evals + guardrails).

## Designing clean seams

The trick to making this testable is **clean seams** between components — exactly the interface discipline you already practise in software.

- **Agent ↔ tools:** a typed contract. JSON schema in, structured `tool_result` out. Now you can unit-test each tool with no model in the loop, and mock the tools when testing the agent's planning.
- **Agent ↔ retriever:** the retriever takes a query string and returns ranked passages with source IDs. Swap your vector store without touching the agent.
- **Everything ↔ guardrails:** guardrails take a payload and return pass/fail plus a reason. They sit at the boundaries, so they never need to know the internals.

When examples need a model id, default to the most capable current Claude — `claude-opus-4-8` via the Messages API (`messages.create`, roles `user`/`assistant`, a top-level `system`, `tool_use` and `tool_result` content blocks). The same patterns run on Amazon Bedrock and Azure (Microsoft Foundry) — the clouds you already operate in.

## Map it onto infrastructure you already run

This is where your DevOps and security background turns a project into a portfolio. Ship the integrated capstone as a **containerised service** behind your existing CI/CD. Put API keys in a **managed secrets vault** (AWS Secrets Manager or Azure Key Vault), not in code. Wire in **logs and metrics** so every agent run is observable. Add a human-in-the-loop approval gate on irreversible tool actions — that is just a CI/CD approval step applied to an agent.

Most applied AI engineers can prototype this. Far fewer can *secure and deploy* it. That gap is your differentiator.

## Your task

Sketch the architecture of your capstone on one page: the four deliverables as layers, the agent as the orchestrator, the seams between components, and where guardrails and evals wrap the flow. Then list the AWS or Azure services you'll use to host it, store secrets, and observe it. Aim for a diagram a hiring manager could understand in five minutes.
