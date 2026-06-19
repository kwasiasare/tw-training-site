---
course: agentic-ai-engineer
title: Observability, Tracing, and Debugging Agent Failures
month: 4
monthTitle: Evaluation, Deployment, and Capstone
lesson: 2
summary: Learn to instrument LLM agents with structured tracing, spans, and logging so you can diagnose
  loops, bad tool calls, and reasoning errors in production. Covers the anatomy of an agent trace, common
  failure modes, and a practical debugging workflow.
objectives:
- Explain why observability is essential for non-deterministic LLM agents and how it differs from traditional
  app monitoring
- Instrument an agent with spans, traces, and structured logs capturing prompts, tool calls, and token
  usage
- 'Identify common agent failure modes: infinite loops, malformed tool calls, hallucinated arguments,
  and reasoning drift'
- Use trace data and evaluation metrics to localize and reproduce a failure
- Apply a systematic debugging workflow and add guardrails to prevent recurrence
video: age-m4-l02-observability-tracing-and-debugging-agent-failur.mp4
quiz:
- q: What is the single most valuable artifact to capture on an LLM call span when debugging reasoning
    errors?
  options:
  - The CPU usage during the call
  - The raw prompt and model completion
  - The number of active threads
  - The server hostname
  answer: 1
  why: Reasoning lives in the text. Seeing the exact prompt sent and the exact completion returned lets
    you tell whether the input was wrong or the model reasoned incorrectly.
- q: In a trace, what is a 'span'?
  options:
  - A single timed unit of work with status and attributes
  - The total cost of a request
  - A type of LLM model
  - A database connection pool
  answer: 0
  why: A span represents one timed operation (e.g., an LLM call or tool call) with a name, start/end time,
    status, and attributes; spans nest to form a trace.
- q: An agent calls the same tool with identical arguments five times in a row. Which failure mode is
    this?
  options:
  - Hallucinated arguments
  - Reasoning drift
  - Infinite/long loop
  - Silent tool failure
  answer: 2
  why: Repeated identical tool calls with climbing step count is the classic signature of a loop, often
    because the model ignores results or there's no progress check.
- q: Which guardrail most directly prevents runaway loops?
  options:
  - Higher temperature
  - Max-step and max-token budgets
  - Larger context window
  - More verbose logging
  answer: 1
  why: Hard budgets on steps and tokens cap how far an agent can run, terminating loops before they consume
    excessive cost or time.
- q: Name one reason traditional stack-trace debugging is insufficient for LLM agents.
  answer: Agent logic lives in non-deterministic prompts and model outputs rather than in code paths,
    so there's no deterministic stack trace to read; you need recorded traces of prompts, completions,
    and tool calls.
  why: Agents are non-deterministic and their behavior is determined by text generation, so you must observe
    the actual recorded inputs/outputs of each step.
- q: In the debugging workflow, what step ensures a fixed bug does not silently return?
  answer: Adding a regression evaluation/test case for the failure to your eval suite.
  why: Capturing the failing scenario as an eval case means future changes are checked against it, preventing
    silent regressions.
resources:
- label: OpenTelemetry Documentation
  url: https://opentelemetry.io/docs/
- label: 'LangSmith: Tracing and Observability for LLM Apps'
  url: https://docs.smith.langchain.com/
- label: 'Langfuse: Open-Source LLM Engineering Platform'
  url: https://langfuse.com/docs
- label: 'Arize Phoenix: LLM Tracing and Evaluation'
  url: https://docs.arize.com/phoenix
---

## Why Observability Matters for Agents

LLM agents are non-deterministic, multi-step systems. A single user request can fan out into dozens of LLM calls, tool invocations, and retries. When something goes wrong in production you cannot just re-read a stack trace — the 'logic' lives in prompts, model outputs, and tool responses. **Observability** gives you the data to answer: *what did the agent actually do, and why?*

Three pillars apply, adapted for agents:
- **Traces**: the end-to-end record of one request, broken into spans.
- **Logs**: structured events (prompt sent, tool called, error raised).
- **Metrics**: aggregates like latency, token cost, tool error rate, loop frequency.

## Anatomy of an Agent Trace

A trace is a tree of **spans**. Each span has a name, start/end time, status, and attributes. For an agent, model the hierarchy like this:

```
Trace: user_request (id=abc123)
├─ span: agent_run
│  ├─ span: llm_call (planning)        attrs: model, prompt, completion, tokens
│  ├─ span: tool_call search_db        attrs: args, result, latency, error
│  ├─ span: llm_call (reasoning)
│  └─ span: tool_call send_email        attrs: args, result
```

Capture these attributes on every span:
- Inputs: the full prompt or messages (or a hash + sample if PII-sensitive).
- Outputs: raw model completion, parsed tool call.
- Metadata: model name, temperature, token counts, cost, latency.
- Status: success / error, with the exception message.
- Correlation IDs: `trace_id`, `session_id`, `user_id` to stitch multi-turn conversations.

## Instrumenting in Practice

Use a tracing library (OpenTelemetry, LangSmith, Langfuse, Arize Phoenix) rather than print statements. Most agent frameworks have auto-instrumentation, but you'll still add custom spans.

```python
from opentelemetry import trace
tracer = trace.get_tracer("agent")

def call_tool(name, args):
    with tracer.start_as_current_span(f"tool.{name}") as span:
        span.set_attribute("tool.name", name)
        span.set_attribute("tool.args", json.dumps(args))
        try:
            result = TOOLS[name](**args)
            span.set_attribute("tool.result", str(result)[:2000])
            return result
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.StatusCode.ERROR)
            raise
```

Log the raw LLM request/response on the span — this is the single most valuable artifact when debugging reasoning errors.

## Common Agent Failure Modes

| Failure | Symptom in trace | Likely cause |
|---|---|---|
| Infinite/long loop | Same tool called repeatedly, step count climbs | No progress check, model ignores results |
| Malformed tool call | JSON parse error span, retries | Schema unclear, model hallucinates fields |
| Hallucinated arguments | Tool succeeds but with wrong/fake values | Missing context, over-confident model |
| Reasoning drift | Final answer ignores tool output | Context window overflow, poor prompt |
| Silent tool failure | Tool returns error string, agent treats as success | No status checking |

## A Debugging Workflow

1. **Reproduce**: find the failing `trace_id`; replay with the same inputs and seed/temperature if possible.
2. **Localize**: walk the span tree to the first anomalous span — where did expected behavior diverge?
3. **Inspect**: read the exact prompt and completion at that step. Was the input correct? Was the output malformed or wrong?
4. **Classify**: map to a failure mode (loop, bad tool call, reasoning error).
5. **Fix**: tighten the prompt/tool schema, add validation, or add a guardrail.
6. **Prevent**: add an eval case to your regression suite so the bug can't silently return.

## Guardrails That Prevent Recurrence

- **Max-step / max-token budgets** to kill runaway loops.
- **Loop detection**: hash recent (tool, args) tuples; halt or escalate on repeats.
- **Schema validation** on tool args before execution (Pydantic / JSON Schema).
- **Tool result validation** and explicit status checks.
- **Cost/latency alerts** wired to your metrics backend.

Observability is not a one-time setup — treat traces as the primary feedback loop driving prompt and tool improvements.
