---
course: kwasi-GenAI
title: Human-in-the-loop, approval gates, and the Module 3 deliverable
month: 3
monthTitle: Agents & Orchestration
lesson: 7
summary: 'Add approval gates to an agent the same way CI/CD tiers gate a deploy, then build the Module
  3 deliverable: a multi-step agent that chains tools to complete a real task.'
objectives:
- Explain human-in-the-loop as approval gates on risky, hard-to-reverse actions
- Map agent approval tiers onto the CI/CD tiered approvals you already use
- Implement a confirmation step in the manual agent loop before a side-effecting tool runs
- Classify tools as auto-run versus approval-required by reversibility
- 'Assemble the Module 3 deliverable: a multi-step, tool-chaining agent'
- Apply the module's guardrails — bounds, logging, and gates — to that deliverable
video: g3-l07-human-in-the-loop-and-deliverable.mp4
quiz:
- q: What is the core idea of human-in-the-loop for agents?
  options:
  - A human writes every model response
  - The agent pauses for human approval before taking risky or hard-to-reverse actions
  - The model is disabled
  - Humans replace the tools
  answer: 1
  why: Human-in-the-loop inserts an approval gate so a person confirms consequential actions before the
    agent executes them.
- q: Which CI/CD concept is the closest parallel to an agent approval gate?
  options:
  - A linter
  - A required manual approval before a production deploy
  - A code formatter
  - A git clone
  answer: 1
  why: A tiered pipeline that auto-runs tests but requires a human to approve the prod deploy is exactly
    the auto-run vs approval-required split for agent tools.
- q: Which property best decides whether a tool needs an approval gate?
  options:
  - Its name length
  - Its reversibility — hard-to-reverse or destructive actions need a gate
  - Whether it is written in Python
  - How fast it runs
  answer: 1
  why: Read-only and easily reversible actions can auto-run; deletes, sends, and external writes are hard
    to reverse and should require approval.
- q: In one sentence, where in the manual loop do you place an approval gate?
  answer: Between detecting a side-effecting tool_use block and actually executing it, you pause and require
    confirmation before running that tool.
  why: The manual loop gives you the exact seam — after Claude requests the tool, before your code runs
    it — to insert a human decision.
- q: For the Module 3 deliverable, what defines it as an agent rather than a single call?
  answer: It runs a loop that chains multiple tool calls — each step's result feeding the next — until
    the task is complete.
  why: Chaining tools across loop iterations to finish a task is precisely the plan-act-observe-repeat
    behaviour that makes it an agent.
- q: Which guardrails from this module should the deliverable include?
  answer: An iteration cap, per-turn logging of calls and tokens, and an approval gate on any side-effecting
    tool.
  why: Bounding the loop, logging for visibility, and gating risky actions are the safety rails every
    shippable agent needs.
resources:
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/research/building-effective-agents
- label: Claude Docs — Tool use (manual agentic loop)
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: Claude Docs — Implement tool use
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
- label: Claude Docs — Tool use examples
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
---

## Approval gates you already understand

**Human-in-the-loop** sounds like new AI vocabulary, but you've shipped it for years. Your pipelines auto-run the linter and the tests, then *stop* and wait for a human to click approve before the production deploy. That tiered approval — cheap, reversible steps run automatically; expensive, irreversible steps need a person — is exactly the pattern an agent needs. The only new thing is applying it to tool calls.

The deciding property is **reversibility**. A read-only `get_weather` can auto-run; nobody needs to approve a lookup. A `send_email`, `delete_record`, or `terraform apply` is hard to undo — that gets a gate. Classify every tool this way and the design falls out.

## The gate lives in the manual loop

Remember why we wrote the manual loop instead of letting the SDK's tool runner hide it: *this is the seam you needed it for*. Between Claude emitting a `tool_use` block and your code executing it, you insert a decision.

```python
APPROVAL_REQUIRED = {"send_email", "delete_record", "apply_changes"}

for block in response.content:
    if block.type != "tool_use":
        continue
    if block.name in APPROVAL_REQUIRED:
        ok = ask_human(f"Run {block.name} with {block.input}? [y/N] ")
        if not ok:
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": "User denied this action.", "is_error": True})
            continue
    results.append({"type": "tool_result", "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input)})
```

Notice the denied path returns a `tool_result` with `is_error` true. The agent isn't crashed — it's *told* the action was refused, and it can adapt, exactly like a deploy that's rejected and sent back for changes.

## Building the Module 3 deliverable

Now we assemble everything into the module deliverable: **a multi-step agent that chains tools to complete a task.** Let's make it concrete with an *incident triage assistant* — given an alert, it looks up the affected service, fetches recent logs, and drafts a summary, asking approval before it posts anything. Five steps:

**1. Define the tools.** Three of them, classified by reversibility:

```python
tools = [
  {"name": "get_service", "description": "Look up the service owning an alert id. Call this first.",
   "input_schema": {"type": "object", "properties": {"alert_id": {"type": "string"}}, "required": ["alert_id"]}},
  {"name": "get_recent_logs", "description": "Fetch recent logs for a service. Read-only.",
   "input_schema": {"type": "object", "properties": {"service": {"type": "string"}}, "required": ["service"]}},
  {"name": "post_summary", "description": "Post an incident summary to the channel. Call only after the user approves.",
   "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}},
]
APPROVAL_REQUIRED = {"post_summary"}   # the only irreversible action
```

**2. Run the bounded, logged loop.** Use the manual loop from Lesson 1 with the Lesson 5 guards baked in:

```python
messages = [{"role": "user", "content": "Triage alert ALRT-91 and draft a summary."}]
for i in range(10):                                  # iteration cap (L5)
    r = client.messages.create(model="claude-opus-4-8", max_tokens=1024,
                               tools=tools, messages=messages)
    log(i, r.stop_reason, r.usage)                   # per-turn logging (L5)
    if r.stop_reason != "tool_use":
        break
    messages.append({"role": "assistant", "content": r.content})
    messages.append({"role": "user", "content": run_with_gates(r.content)})  # gates (L7)
```

**3. Chain the tools (Lesson 2).** Claude calls `get_service("ALRT-91")`, then uses the returned service name to call `get_recent_logs(service)`, then reasons over the logs to draft a summary. Each result feeds the next — that's the chain.

**4. Gate the risky step (this lesson).** When Claude finally calls `post_summary`, the gate fires and a human approves or denies. Everything before that auto-runs because it's read-only.

**5. Manage state and stop cleanly (Lesson 6).** The scratchpad carries the service name and logs across iterations; the loop ends on `end_turn` once the summary is posted or the cap is hit.

That single agent uses every idea in the module: the loop, chained tools, a framework-free clear implementation, MCP-style tool boundaries, the failure-mode guards, scratchpad state, and an approval gate.

## Your task

Build the incident triage agent (or one for your own domain). Implement the three tools with stubbed bodies, the bounded logged loop, tool chaining, and an approval gate on the one side-effecting tool. Run it end to end and confirm the gate fires before the irreversible action — then you've completed the Module 3 deliverable.
