---
course: ai-product-manager
title: 'Designing Eval Frameworks: From Golden Sets to Rubrics'
month: 3
monthTitle: Building, Evaluating, and Prompting AI Features
lesson: 2
summary: 'Learn to design a practical evaluation framework for AI features: build golden sets, write scoring
  rubrics, and set acceptance thresholds so you can ship with confidence and catch regressions.'
objectives:
- Explain why AI features need systematic evals beyond manual spot-checks
- Construct a representative golden set with edge cases and clear labels
- Write scoring rubrics (binary, scaled, and dimensional) that produce consistent judgments
- Define acceptance thresholds and ship/no-ship gates tied to product risk
- Choose between human, automated, and LLM-as-judge scoring methods
- Operationalize evals into a repeatable plan integrated with releases
video: apm-m3-l02-designing-eval-frameworks-from-golden-sets-to-ru.mp4
quiz:
- q: What is the primary purpose of a golden set in an eval framework?
  options:
  - To store all production logs indefinitely
  - A curated, representative set of test cases used as a quality benchmark
  - A list of prompts that always pass
  - The model's training data
  answer: 1
  why: A golden set is a curated, versioned collection of representative and edge-case test cases used
    to benchmark feature quality over time.
- q: Which scoring approach is best for enforcing a hard 'output must be valid JSON' constraint?
  options:
  - LLM-as-judge
  - Scaled 1-5 human rating
  - Programmatic/deterministic checks
  - Ignoring it until launch
  answer: 2
  why: Format and schema constraints are objective and reliably enforced with programmatic checks rather
    than subjective scoring.
- q: Why should acceptance thresholds be tied to a baseline rather than an absolute ideal?
  options:
  - Baselines are easier to fake
  - To ensure the feature is at least as good as current production/human performance and to detect regressions
  - Absolute ideals are illegal
  - It removes the need for a golden set
  answer: 1
  why: Comparing against a baseline shows real improvement or regression relative to what users already
    experience, which is the meaningful decision criterion.
- q: When using LLM-as-judge for scoring, what critical step keeps it trustworthy?
  options:
  - Using the largest model available
  - Validating its judgments against human labels and checking for bias
  - Running it only once
  - Removing all programmatic checks
  answer: 1
  why: LLM-as-judge scales scoring but can be biased or inconsistent, so it must be periodically validated
    against human-labeled cases.
- q: Name one type of input you should deliberately include in a golden set beyond common, representative
    cases.
  answer: Edge cases such as adversarial, ambiguous, empty, or out-of-scope inputs
  why: Edge and adversarial cases reveal failure modes that representative-only sets miss, making the
    eval a stronger safety and quality net.
- q: In one phrase, what is the key advantage of a dimensional rubric over a single overall score?
  answer: It makes failures diagnosable by separating axes like accuracy, tone, and safety
  why: Scoring independent dimensions lets you see exactly where quality breaks down rather than getting
    one ambiguous number.
resources:
- label: OpenAI Evals framework (GitHub)
  url: https://github.com/openai/evals
- label: 'Anthropic: Building evaluations for your use case'
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests
- label: Hugging Face Evaluate library
  url: https://huggingface.co/docs/evaluate
- label: 'Google PAIR: Guidebook on Human-Centered AI evaluation'
  url: https://pair.withgoogle.com/guidebook/
---

## Why Evals Matter for AI PMs

AI features are probabilistic, not deterministic. The same prompt can yield different answers, and a model upgrade can silently break behavior that worked yesterday. As an AI PM, you cannot rely on "it looked good in the demo." You need a repeatable measurement system that tells you whether a feature meets quality bars before launch and whether it stays there over time.

An **eval framework** is the product spec for quality. It answers: What does good look like? How do we measure it? What score is good enough to ship?

## The Three Pillars

1. **Golden set** — a curated collection of test cases (inputs and, where possible, expected outputs or reference answers).
2. **Scoring rubric** — the rules for judging an output's quality.
3. **Acceptance thresholds** — the numeric bar a feature must clear to ship or stay live.

## Building a Golden Set

A golden set is your benchmark. Quality beats quantity early on; 50–200 well-chosen cases often outperform thousands of random ones.

**Principles:**
- **Representative:** mirror real user distribution (common intents, languages, formats).
- **Edge cases:** include adversarial, ambiguous, empty, and out-of-scope inputs.
- **Stratified:** tag cases by category, difficulty, and risk so you can analyze by slice.
- **Versioned:** store as data (CSV/JSON) under version control; freeze a set per release.
- **Sourced honestly:** pull from real logs (anonymized), support tickets, and known failure modes — not just inputs you know the model handles well.

Each case should capture: `input`, `context`, `expected_output` or `reference`, `category`, `difficulty`, and any `must_not` constraints (e.g., never reveal PII).

## Writing Scoring Rubrics

A rubric converts fuzzy "quality" into a measurable judgment. Pick the simplest type that captures what matters.

- **Binary (pass/fail):** "Did it correctly answer the question? Y/N." Easy to aggregate, great for correctness-critical tasks.
- **Scaled (1–5):** captures degrees of quality (e.g., helpfulness). Define each point on the scale to reduce subjectivity.
- **Dimensional:** score multiple independent axes — e.g., **accuracy**, **completeness**, **tone**, **safety**, **format compliance** — then combine with weights.

**Rubric best practices:**
- Anchor every score with concrete descriptions and examples.
- Separate *correctness* (factual) from *style* (tone/format) so failures are diagnosable.
- Include hard constraints as gating checks (safety violation = automatic fail regardless of other scores).
- Calibrate: have two people score the same 20 cases and measure agreement; refine until consistent.

## Choosing a Scoring Method

| Method | Best for | Tradeoffs |
|---|---|---|
| Exact/deterministic match | Structured output, classification | Cheap, fast; brittle for free text |
| Programmatic checks | Format, JSON schema, keyword presence | Reliable for constraints; can't judge nuance |
| Human review | Subjective quality, high-stakes | Gold standard; slow, expensive |
| LLM-as-judge | Scaling subjective scoring | Fast and cheap; needs validation against human labels, watch for bias |

A common pattern: programmatic checks for hard constraints + LLM-as-judge for quality, periodically audited by humans.

## Setting Acceptance Thresholds

Thresholds turn scores into decisions. Tie them to **product risk** and **baseline**.

- Define the **metric** (e.g., % passing, mean rubric score) and the **bar** (e.g., ≥90% pass on correctness, zero safety failures).
- Use **ship gates**: must-pass (safety, no regressions) vs. nice-to-have (helpfulness improvement).
- Compare against a **baseline** (current production or human performance), not an absolute ideal.
- Account for **statistical confidence** — small golden sets have noisy estimates; report ranges.
- Treat **regressions** explicitly: a new model can't drop any critical slice below its prior level.

## Operationalizing the Plan

- Run evals automatically on every prompt change, model upgrade, or release candidate.
- Track results over time in a dashboard; alert on regressions.
- Grow the golden set continuously by mining production failures.
- Review and recalibrate rubrics quarterly as the product and user expectations evolve.

The deliverable is a one-page **eval plan**: feature, golden set location, rubric, scoring method, thresholds, and owner.
