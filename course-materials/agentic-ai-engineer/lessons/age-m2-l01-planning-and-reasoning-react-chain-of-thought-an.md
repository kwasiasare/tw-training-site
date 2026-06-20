---
course: agentic-ai-engineer
title: 'Planning and Reasoning: ReAct, Chain-of-Thought, and Decomposition'
month: 2
monthTitle: Reasoning, Memory, and Retrieval
lesson: 1
summary: 'This lesson teaches the core reasoning strategies that turn an LLM into a goal-directed agent:
  Chain-of-Thought for explicit step-by-step thinking, ReAct for interleaving reasoning with tool calls,
  and task decomposition for breaking large goals into ordered, executable subtasks. You will learn when
  to use each pattern, how to implement them in production code, and how to keep reasoning reliable, observable,
  and cost-aware.'
objectives:
- Explain the differences between Chain-of-Thought, ReAct, and explicit decomposition, and choose the
  right pattern for a given task.
- Implement a ReAct loop that interleaves Thought, Action, and Observation steps with tool calls.
- Decompose a complex goal into an ordered, dependency-aware subtask plan an agent can execute.
- Apply guardrails—step limits, validation, and structured output—to keep reasoning reliable and bounded.
- Add observability and cost controls so reasoning traces can be debugged and monitored in production.
video: age-m2-l01-planning-and-reasoning-react-chain-of-thought-an.mp4
quiz:
- q: What three components make up each cycle of a ReAct loop?
  options:
  - Prompt, Completion, Reward
  - Thought, Action, Observation
  - Plan, Execute, Verify
  - Input, Hidden, Output
  answer: 1
  why: ReAct interleaves a Thought (reasoning about what to do), an Action (a tool call), and an Observation
    (the tool's result), repeating until a final answer.
- q: Which pattern is best for a pure math problem that needs no external data or tools?
  options:
  - ReAct
  - Plan-and-execute
  - Chain-of-Thought
  - Interleaved replanning
  answer: 2
  why: Chain-of-Thought provides step-by-step internal reasoning and is cheap and fast for self-contained
    logic and math, with no need for tools.
- q: Why is setting a maximum step limit important in a ReAct agent?
  options:
  - It improves model accuracy
  - It prevents infinite loops and bounds cost
  - It increases the context window
  - It removes the need for tools
  answer: 1
  why: A step limit stops runaway loops and caps token/tool cost, ensuring the agent terminates even if
    it never reaches a clean final answer.
- q: What is the main advantage of plan-and-execute over fully interleaved replanning?
  options:
  - It is more adaptive to surprises
  - It is more predictable and cheaper
  - It never needs tools
  - It eliminates hallucination
  answer: 1
  why: Generating the full plan up front is cheaper and more predictable, though less adaptive than re-planning
    after every observation.
- q: In one sentence, why does ReAct reduce hallucination compared to plain Chain-of-Thought?
  answer: Because it feeds real tool observations back into the reasoning, grounding the model's assumptions
    in actual external results instead of guessed facts.
  why: ReAct checks each reasoning step against concrete observations from tools, so the model corrects
    course rather than inventing unverified information.
- q: Name one observability practice you should apply to a production reasoning agent.
  answer: 'Log/trace each step''s thought, action, arguments, observation, latency, and cost (also acceptable:
    detect repeated actions, validate outputs against a schema).'
  why: Per-step tracing is the primary way to debug agent behavior and monitor cost and reliability in
    production.
resources:
- label: 'ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)'
  url: https://arxiv.org/abs/2210.03629
- label: Chain-of-Thought Prompting Elicits Reasoning in LLMs (Wei et al., 2022)
  url: https://arxiv.org/abs/2201.11903
- label: 'LangGraph: Planning and Agent Execution Patterns'
  url: https://langchain-ai.github.io/langgraph/
- label: Plan-and-Solve Prompting (Wang et al., 2023)
  url: https://arxiv.org/abs/2305.04091
---

## Why Planning and Reasoning Matter

A raw LLM answers in one shot. An *agent* must pursue a goal that spans multiple steps, calls tools, and adapts when reality differs from expectations. Planning and reasoning patterns are the scaffolding that turns a single prediction into a controllable, multi-step process.

Three patterns dominate production systems:

1. **Chain-of-Thought (CoT)** — the model reasons step by step before answering.
2. **ReAct** — the model interleaves *reasoning* with *acting* (tool calls), observing results between steps.
3. **Decomposition / Planning** — the model (or a planner) splits a goal into ordered subtasks, then executes them.

## Chain-of-Thought (CoT)

CoT prompts the model to produce intermediate reasoning steps rather than jumping to a final answer. This improves accuracy on math, logic, and multi-constraint tasks.

- **Zero-shot CoT:** append a cue like *"Let's think step by step."*
- **Few-shot CoT:** show worked examples that include reasoning.
- **Production note:** keep the *visible* reasoning out of the user-facing response when not needed. Use structured output so the final answer is machine-parseable, and consider hiding raw chain-of-thought from end users for safety and cost reasons.

CoT is **internal** reasoning—no tools, no external state. It is cheap and fast but cannot fetch fresh information or act on the world.

## ReAct: Reason + Act

ReAct (Yao et al., 2022) interleaves reasoning traces with actions. Each cycle has three parts:

- **Thought** — what should I do next and why?
- **Action** — call a tool with concrete arguments.
- **Observation** — the tool's returned result, fed back into context.

The loop repeats until the model emits a final answer. ReAct grounds reasoning in real observations, reducing hallucination because the model checks its assumptions against tool output.

```text
Thought: I need the current weather in Paris.
Action: get_weather(city="Paris")
Observation: 14°C, light rain
Thought: I now have what I need.
Final Answer: It's 14°C and lightly raining in Paris.
```

### Implementing a ReAct loop

```python
def react_agent(goal, tools, llm, max_steps=8):
    history = []
    for step in range(max_steps):
        prompt = build_prompt(goal, tools, history)
        out = llm(prompt)  # returns Thought + Action OR Final Answer
        if out.is_final:
            return out.answer
        # parse and execute the chosen tool
        result = tools[out.action.name](**out.action.args)
        history.append((out.thought, out.action, result))
    return "Stopped: step limit reached"
```

Key production concerns:

- **Step limit** prevents infinite loops and runaway cost.
- **Structured tool calls** (use the provider's function/tool-calling API rather than parsing free text) make actions reliable.
- **Observation truncation** keeps the context window from exploding.

## Decomposition and Planning

For complex goals, ask the model to *plan first*: produce an ordered list of subtasks with dependencies, then execute them. This separates **planning** from **execution**, which makes the system easier to debug and parallelize.

Two common styles:

- **Plan-and-execute:** generate the full plan up front, then run each step. Cheaper and more predictable, but brittle if early assumptions break.
- **Interleaved (ReAct-style) planning:** re-plan after each observation. More adaptive, more expensive.

A practical hybrid: generate a coarse plan, execute, and allow **replanning** only when a step fails or an observation contradicts the plan.

```python
plan = llm_plan(goal)  # [{"id":1,"task":...,"depends_on":[]}, ...]
results = {}
for task in topological_order(plan):
    results[task.id] = execute(task, context=results)
    if failed(results[task.id]):
        plan = llm_replan(goal, plan, results)
```

### Good decomposition principles

- Each subtask should be **independently verifiable** and map to one tool or one clear action.
- Capture **dependencies** so steps run in the correct order.
- Keep subtasks **atomic**—if a step needs its own sub-steps, recurse.

## Choosing the Right Pattern

| Task | Pattern |
|------|---------|
| Pure logic/math, no external data | Chain-of-Thought |
| Needs live data or tools, adaptive | ReAct |
| Long multi-stage workflow | Plan-and-execute (+ replan) |

Many real agents combine all three: a planner decomposes the goal, and each subtask is solved by a ReAct loop whose internal steps use CoT.

## Reliability and Observability

- **Bound everything:** max steps, max tokens, timeouts per tool.
- **Validate outputs:** parse structured responses with a schema; retry on parse failure.
- **Trace every step:** log thought, action, args, observation, latency, and cost. These traces are your primary debugging tool.
- **Detect loops:** if the agent repeats the same action with the same args, break and escalate.
- **Fail gracefully:** return partial results and a clear reason when limits are hit.
