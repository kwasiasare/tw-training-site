---
course: agentic-ai-engineer
title: 'Evaluating Agents: Metrics, Trajectories, and LLM-as-Judge'
month: 4
monthTitle: Evaluation, Deployment, and Capstone
lesson: 1
summary: Learn to build systematic evaluation harnesses for LLM agents, measuring not just final-answer
  accuracy but the quality of tool use, reasoning trajectories, and task completion. This lesson covers
  outcome and process metrics, trajectory evaluation, and the LLM-as-judge pattern with rubrics, calibration,
  and guardrails against bias.
objectives:
- Distinguish outcome metrics from process/trajectory metrics and explain when each matters
- Build a reusable evaluation dataset and harness that runs an agent over fixed test cases
- Measure tool-use correctness, trajectory quality, and task completion programmatically
- Design and calibrate an LLM-as-judge with explicit rubrics and structured outputs
- Identify and mitigate common judge biases (position, verbosity, self-preference)
- Wire evaluation into CI/CD to catch regressions before deployment
video: age-m4-l01-evaluating-agents-metrics-trajectories-and-llm-a.mp4
quiz:
- q: Why are process/trajectory metrics important even when outcome metrics look good?
  options:
  - They are cheaper to compute than outcome metrics
  - They reveal why failures happen and predict reliability when prompts or models change
  - They are required by all LLM providers
  - They replace the need for any outcome metrics
  answer: 1
  why: Outcome metrics show current usefulness, but process metrics explain failure causes and predict
    how the agent behaves under change — an agent can reach a right answer via a fragile path.
- q: Which trajectory matching strategy allows extra steps but enforces that required tools occur in the
    correct relative order?
  options:
  - Exact-order match
  - Set/subset match
  - In-order subset match
  - Argument-only match
  answer: 2
  why: In-order subset match checks that required tools appear in the right relative order while tolerating
    extra steps, balancing strictness and flexibility.
- q: Which practice most improves the reliability of an LLM-as-judge?
  options:
  - Asking for a vague 1-10 rating with no rubric
  - Using an explicit rubric with concrete levels and structured output, ideally reference-guided
  - Always using the same model that generated the answer
  - Hiding the reference answer from the judge
  answer: 1
  why: Explicit concrete rubrics, structured JSON output, and reference-guided grading substantially raise
    consistency and agreement with humans.
- q: Name one bias an LLM judge commonly exhibits and a way to mitigate it.
  answer: 'Position bias — mitigate by randomizing option order or averaging both orders; (also acceptable:
    verbosity bias — penalize padding in rubric; self-preference — use a different model family).'
  why: Judges show position, verbosity, and self-preference biases; randomizing order, rubric penalties
    for length, and cross-family grading mitigate them.
- q: In an evaluation harness, why should a reported production bug be added as a new test case?
  answer: So the specific failure is permanently covered and can never silently regress in future changes
    — treating eval cases like regression unit tests.
  why: Adding bugs as cases turns the eval suite into a growing regression guard, preventing previously-fixed
    failures from reappearing.
resources:
- label: LangSmith Evaluation documentation
  url: https://docs.smith.langchain.com/evaluation
- label: 'Arize Phoenix: LLM & Agent Evals'
  url: https://docs.arize.com/phoenix
- label: Zheng et al., 'Judging LLM-as-a-Judge' (MT-Bench / Chatbot Arena)
  url: https://arxiv.org/abs/2306.05685
- label: OpenAI Evals framework
  url: https://github.com/openai/evals
---

## Why Agent Evaluation Is Hard

Traditional ML evaluation compares a single prediction against a label. Agents are different: they take *multi-step trajectories*, call tools, maintain state, and can reach a correct answer through a wasteful or unsafe path — or reach a wrong answer through reasonable steps. Evaluation must therefore look at both **what** the agent produced (outcome) and **how** it got there (process).

A good evaluation harness answers three questions:
1. Did the agent complete the task correctly? (outcome)
2. Did it use tools efficiently and correctly? (process)
3. Is the behaviour stable as we change prompts, models, or tools? (regression)

## Two Families of Metrics

### Outcome metrics
- **Task success rate**: fraction of tasks where the final output meets acceptance criteria.
- **Exact match / F1**: when there is a canonical answer (e.g. a number, an extracted field).
- **Constraint satisfaction**: did the output respect format, length, schema, or policy rules?

### Process / trajectory metrics
- **Tool-call accuracy**: correct tool selected, correct arguments, correct order.
- **Step efficiency**: number of steps or tokens vs. an optimal reference.
- **Recovery**: did the agent recover from a tool error instead of looping or giving up?
- **Groundedness**: are claims supported by retrieved/observed evidence?

Outcome metrics tell you if the system is useful today; process metrics tell you *why* it fails and predict reliability under change.

## Building the Harness

Start with a versioned **evaluation dataset**: a list of cases, each with an input, optional reference trajectory, and acceptance criteria.

```python
case = {
  "id": "refund-001",
  "input": "Refund order 4471, customer says item never arrived",
  "expected_tools": ["lookup_order", "issue_refund"],
  "success_check": lambda out: "refund issued" in out.lower(),
}
```

The harness loop is simple: run the agent, capture the full trajectory (every tool call, arg, observation, and the final answer), then apply scorers.

```python
def run_eval(agent, cases, scorers):
    results = []
    for c in cases:
        trace = agent.run(c["input"])  # returns steps + final
        scores = {name: fn(c, trace) for name, fn in scorers.items()}
        results.append({"id": c["id"], **scores})
    return results
```

Capture traces with a tracing tool (LangSmith, Phoenix, OpenTelemetry) so failures are debuggable, not just numbers.

## Evaluating Trajectories

Three common strategies:
- **Exact-order match**: trajectory must match a reference tool sequence. Strict, brittle, good for narrow tasks.
- **Set/subset match**: required tools all appear, order ignored. More forgiving.
- **In-order subset**: required tools appear in the right relative order, extra steps allowed.

Also score **argument correctness** separately — picking the right tool with the wrong arguments is still a failure.

## LLM-as-Judge

Many quality dimensions (helpfulness, coherence, groundedness) have no cheap programmatic check. Use a strong LLM as a grader. Keys to making it reliable:

- **Explicit rubric**: define each score level concretely. Avoid vague "rate 1-10".
- **Structured output**: force JSON with a `score` and `reasoning` field.
- **Reference-guided grading**: give the judge a gold answer when available — far more reliable than reference-free.
- **Pairwise comparison** when you only need to know which of two outputs is better; often more consistent than absolute scoring.

```python
JUDGE_PROMPT = '''You are grading an agent response.
Rubric:
- 0: wrong or unsafe
- 1: partially correct, missing key step
- 2: fully correct and grounded
Reference answer: {reference}
Agent answer: {answer}
Return JSON: {{"score": int, "reasoning": str}}'''
```

### Judge biases to defend against
- **Position bias**: prefers the first option in pairwise — randomize order, or run both orders and average.
- **Verbosity bias**: prefers longer answers — instruct the rubric to penalize padding.
- **Self-preference**: a model favours its own outputs — use a different model family as judge where possible.

### Calibrate your judge
Before trusting it, measure agreement with human labels on a held-out set (e.g. Cohen's kappa). If agreement is low, refine the rubric. The judge is itself a model you must evaluate.

## From Harness to CI/CD

Once metrics are stable, turn them into gates:
- Run the eval suite on every prompt/model change.
- Fail the build if task success drops below a threshold or a regression set breaks.
- Track metrics over time on a dashboard; watch for silent drift after a model provider updates.

Keep a small, fast **smoke set** for every commit and a larger nightly suite. Treat eval cases like unit tests: when a bug is reported in production, add it as a new case so it never regresses.
