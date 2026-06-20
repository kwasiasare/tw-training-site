---
course: ai-app-developer-2026
title: 'Project: Autonomous Research Agent'
month: 3
monthTitle: Agents, Tools, and APIs
lesson: 4
summary: In this capstone-style project lesson, you build an autonomous research agent that takes a topic,
  plans a research strategy, calls web search and page-reading tools, synthesizes findings across sources,
  and produces a structured, citation-backed report. You'll design the agent loop, define tool schemas,
  add guardrails for cost and reliability, and validate output structure.
objectives:
- Design an agent loop (plan → act → observe → synthesize) for autonomous research
- Define and register web tools (search and fetch) with clear JSON schemas
- Implement source synthesis that aggregates and deduplicates findings with citations
- Generate a structured report using a validated output schema
- Add guardrails for iteration limits, cost control, and error handling
- Evaluate the agent's output for accuracy, coverage, and citation quality
video: aad-m3-l04-project-autonomous-research-agent.mp4
quiz:
- q: What distinguishes an agent from a single LLM call?
  options:
  - It uses a larger model
  - It iterates through a plan-act-observe loop using tools
  - It always produces JSON
  - It runs faster
  answer: 1
  why: An agent's defining feature is the iterative loop where it reasons, calls tools, observes results,
    and decides next steps — unlike a one-shot LLM call.
- q: Why do tools require a JSON parameter schema?
  options:
  - To make the code shorter
  - So the model knows how to invoke them correctly
  - To encrypt the arguments
  - To avoid using the network
  answer: 1
  why: The schema and description tell the model what arguments the tool expects and how to call it properly.
- q: Which is the best practice for the final research report?
  options:
  - Free-form prose with no structure
  - A validated schema where claims map to source URLs
  - Only a list of links
  - A single sentence summary
  answer: 1
  why: A validated structured schema ensures every claim is traceable to a source and that downstream
    code can parse the output reliably.
- q: What is the purpose of an iteration cap (max_iters) in the agent loop?
  options:
  - To improve writing quality
  - To prevent infinite loops and runaway cost
  - To increase the number of sources
  - To disable tools
  answer: 1
  why: An iteration cap is a guardrail that stops the loop from running indefinitely, controlling both
    reliability and cost.
- q: In one sentence, name the five stages of the ReAct-style research loop.
  answer: Plan, Act, Observe, Repeat (until stopping), and Synthesize.
  why: The agent plans research questions, acts by calling a tool, observes the result, repeats until
    a stopping condition, then synthesizes the report.
- q: 'Short answer: Give one reason citation quality is critical when evaluating the agent.'
  answer: It lets you verify claims are actually supported by real, relevant sources (accuracy and trustworthiness).
  why: Citations make the report verifiable; without accurate, relevant sources the findings can't be
    trusted or fact-checked.
resources:
- label: 'ReAct: Synergizing Reasoning and Acting in Language Models (paper)'
  url: https://arxiv.org/abs/2210.03629
- label: OpenAI Function/Tool Calling Guide
  url: https://platform.openai.com/docs/guides/function-calling
- label: 'Pydantic: Data Validation for Python'
  url: https://docs.pydantic.dev/
- label: LangChain Agents Documentation
  url: https://python.langchain.com/docs/concepts/agents/
---

## What You're Building

An **autonomous research agent** accepts a topic, decides what to look up, uses web tools to gather evidence, and writes a structured report with citations. Unlike a single LLM call, the agent runs an iterative loop: it plans, takes an action (calls a tool), observes the result, and decides the next step until it has enough information.

## The Agent Loop

The core pattern is **ReAct** (Reason + Act):

1. **Plan** — break the topic into research questions.
2. **Act** — call a tool (e.g., `web_search`, `fetch_page`).
3. **Observe** — read the tool output and update working notes.
4. **Repeat** until a stopping condition is met (enough coverage, max iterations, or budget exhausted).
5. **Synthesize** — combine notes into a final structured report.

Keep an explicit *scratchpad* (the running message history with tool calls and results) so the model can reason over what it has already found.

## Defining Tools

Tools are functions the model can call. Each needs a name, description, and a JSON parameter schema so the LLM knows how to invoke it.

```python
tools = [
  {
    "type": "function",
    "function": {
      "name": "web_search",
      "description": "Search the web and return ranked results with titles, URLs, and snippets.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {"type": "string"},
          "num_results": {"type": "integer", "default": 5}
        },
        "required": ["query"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_page",
      "description": "Fetch and return cleaned text content from a URL.",
      "parameters": {
        "type": "object",
        "properties": {"url": {"type": "string"}},
        "required": ["url"]
      }
    }
  }
]
```

Implement the actual functions separately and dispatch based on the name the model returns.

## The Orchestration Loop

```python
def run_agent(topic, max_iters=8):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Research this topic: {topic}"}
    ]
    for _ in range(max_iters):
        resp = client.chat.completions.create(
            model="gpt-4o", messages=messages, tools=tools
        )
        msg = resp.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            break  # model is done, ready to synthesize
        for call in msg.tool_calls:
            result = dispatch(call.function.name,
                              json.loads(call.function.arguments))
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result)
            })
    return synthesize_report(messages)
```

## Structured Output

Don't let the report be free-form. Define a schema and validate it. A useful report structure:

```json
{
  "topic": "string",
  "summary": "string",
  "key_findings": [{"claim": "string", "sources": ["url"]}],
  "open_questions": ["string"],
  "sources": [{"title": "string", "url": "string"}]
}
```

Use the model's structured-output / JSON mode and parse with a validator (e.g., Pydantic) so downstream code can rely on the shape. Every key finding should map to at least one source URL.

## Guardrails

- **Iteration cap**: stop after `max_iters` to avoid infinite loops.
- **Budget cap**: track token/tool spend; abort if exceeded.
- **Tool error handling**: wrap tool calls in try/except and return an error string the model can react to (e.g., retry with a different query).
- **Deduplication**: collapse repeated URLs before synthesis.
- **Timeouts**: enforce per-request timeouts on `fetch_page`.

## Synthesis Best Practices

When synthesizing, instruct the model to: cite sources for each claim, flag conflicting information, separate well-supported findings from speculation, and list open questions. Quality of citations is as important as the prose.

## Evaluation

Assess your agent on: **accuracy** (are claims supported by the cited source?), **coverage** (did it address the key sub-questions?), **citation quality** (real, relevant URLs), and **efficiency** (iterations and cost). Spot-check by opening cited URLs.
