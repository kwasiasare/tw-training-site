---
course: ai-product-manager
title: Running Evals and Interpreting Results to Improve Quality
month: 3
monthTitle: Building, Evaluating, and Prompting AI Features
lesson: 3
summary: A practical lesson on running evaluations against prompt variants, analyzing failure modes systematically,
  and translating results into a data-driven eval report that drives quality improvements for AI features.
objectives:
- Set up and execute an eval run across multiple prompt variants using a representative dataset
- Choose appropriate metrics (exact-match, rubric scoring, LLM-as-judge) for the task
- Categorize and prioritize failure modes from eval results
- Interpret aggregate and per-segment scores to compare variants confidently
- Document findings and recommended changes in a structured eval report
video: apm-m3-l03-running-evals-and-interpreting-results-to-improv.mp4
quiz:
- q: Why should an eval report include the distribution of scores, not just the average?
  options:
  - Averages are harder to compute
  - A high average can hide a cluster of catastrophic low scores
  - Distributions are required by regulators
  - It makes the report longer
  answer: 1
  why: An average like 4.2 can mask a subset of severe failures (1s) that may be dealbreakers; the distribution
    reveals them.
- q: When using LLM-as-judge for scoring, what is the most important safeguard?
  options:
  - Use the cheapest possible model
  - Validate judge scores against human labels and pin the judge prompt/model
  - Run the judge at high temperature
  - Score only the best outputs
  answer: 1
  why: LLM judges can be biased or inconsistent, so you must validate them against human labels and fix
    the judge model and prompt for reproducibility.
- q: You're comparing two prompt variants on a 60-example set; B scores 2% higher overall. What's the
    best next step?
  options:
  - Ship B immediately
  - Look at per-example wins/losses and segments to check if the difference is real
  - Delete variant A
  - Double the temperature and rerun
  answer: 1
  why: A 2% gap on a small set may be within noise; paired per-example analysis and segmentation tell
    you whether the difference is meaningful.
- q: Why keep a held-out set you never iterate against?
  options:
  - To reduce API costs
  - To avoid overfitting your prompts to the eval examples
  - Because models require it
  - To increase dataset size automatically
  answer: 1
  why: If you tune prompts against every example, you risk overfitting; a held-out set gives an honest
    measure of generalization.
- q: List three failure-mode buckets you might use when analyzing eval results.
  answer: Examples include hallucination/factual error, format or schema violation, refusal/over-caution,
    missing context handling, and tone/style mismatch.
  why: Bucketing failures into named categories lets you count them and map each to a specific cause and
    candidate fix.
- q: Besides quality scores, name two product constraints an eval report should weigh when recommending
    a variant.
  answer: Cost and latency.
  why: A higher-quality variant may be too slow or expensive to ship, so cost and latency must be balanced
    against quality.
resources:
- label: OpenAI Evals framework (GitHub)
  url: https://github.com/openai/evals
- label: 'Anthropic: Building evals and test sets'
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests
- label: Hugging Face Evaluate library
  url: https://huggingface.co/docs/evaluate
- label: 'Eugene Yan: Patterns for Building LLM-based Systems & Products (evals section)'
  url: https://eugeneyan.com/writing/llm-patterns/
---

## Why Evals Matter

Shipping an AI feature without evals is like deploying code with no tests. Evals give you a repeatable, quantitative way to answer one question: *did this change make the product better or worse?* As an AI PM, you own the definition of "better" and the discipline of measuring it.

## The Eval Loop

1. **Define quality** — translate the user outcome into measurable criteria.
2. **Build a dataset** — collect representative inputs plus expected outputs or rubrics.
3. **Run variants** — execute each prompt/model variant against the same dataset.
4. **Score** — apply metrics automatically and/or with human review.
5. **Analyze** — segment results, find failure modes, form hypotheses.
6. **Document & decide** — write the report, pick a winner, plan the next iteration.

## Choosing Metrics

- **Exact / fuzzy match**: good for classification, extraction, or short factual answers.
- **Rubric scoring (1-5)**: for open-ended outputs scored by humans or an LLM judge against explicit criteria (accuracy, completeness, tone, safety).
- **LLM-as-judge**: scalable and cheap, but must be validated against human labels and can carry bias. Pin the judge model and prompt.
- **Programmatic checks**: JSON validity, length limits, forbidden phrases, citation presence.

Always report both an **aggregate score** and the **distribution** — an average of 4.2 can hide a cluster of catastrophic 1s.

## Building a Good Eval Set

- Aim for 50-200 examples to start; enough to detect meaningful differences.
- Cover **happy paths, edge cases, and known-failure cases**.
- Add **segments/tags** (language, query type, difficulty, user persona) so you can slice results.
- Keep a held-out set you don't iterate against to avoid overfitting your prompts.

## Running Variants Fairly

- Change one thing at a time when possible, or run a clean A/B with everything else fixed.
- Fix temperature, model version, and seed where you can for reproducibility.
- Record metadata: model, prompt hash, date, cost, latency.

## Analyzing Failure Modes

Don't stop at the score. Read the failures and bucket them:

- **Hallucination / factual error**
- **Format / schema violation**
- **Refusal or over-caution**
- **Missing context handling**
- **Tone / style mismatch**

Count each bucket. A variant that scores slightly lower overall but eliminates a dangerous failure mode may still be the better ship decision. Tie each bucket to a hypothesized cause and a candidate fix (prompt instruction, few-shot example, retrieval change, model swap).

## Interpreting Results

- Compare variants on the **same examples** (paired comparison) for sensitivity.
- Watch for **noise**: with small sets, a 2% difference may be within margin of error. Look at per-example wins/losses, not just the mean.
- Segment: variant B may win overall but lose on the Spanish-language slice.
- Balance quality against **cost and latency** — these are real product constraints.

## The Eval Report

A good report is decision-ready and includes:

- **Goal & question** being tested
- **Dataset** description and size
- **Variants** compared (with prompt diffs)
- **Metrics & results table** (aggregate + by segment)
- **Top failure modes** with examples and counts
- **Recommendation** and next steps

Keep it short, link to raw data, and make the recommendation explicit so stakeholders can act.
