---
course: ai-product-manager
title: 'Spotting AI Opportunities: Problem-First Use Case Discovery'
month: 2
monthTitle: AI Product Strategy and Roadmapping
lesson: 1
summary: This lesson teaches AI Product Managers how to discover high-value AI use cases by starting with
  real customer and business problems rather than chasing technology hype. You'll learn a repeatable problem-first
  framework, criteria for screening ideas, and how to assemble a prioritized opportunity list ready for
  roadmapping.
objectives:
- Apply a problem-first framework to surface AI use cases grounded in real user and business pain.
- Distinguish genuine AI-suitable problems from hype-driven 'AI for AI's sake' ideas.
- Evaluate opportunities against value, feasibility, data availability, and risk criteria.
- Use a scoring rubric to rank candidate use cases into a prioritized opportunity list.
- Communicate the rationale behind opportunity prioritization to stakeholders.
video: apm-m2-l01-spotting-ai-opportunities-problem-first-use-case.mp4
quiz:
- q: What is the core principle of problem-first AI discovery?
  options:
  - Choose the most advanced model first
  - Start with a quantified problem before deciding if AI fits
  - Prioritize ideas that demo well to executives
  - Build a chatbot for every workflow
  answer: 1
  why: Problem-first means articulating and quantifying a real pain before asking whether AI is the right
    tool — protecting against hype-driven work.
- q: Which of the following is a red flag suggesting an idea may be hype-driven?
  options:
  - The problem affects high-volume repetitive decisions
  - The task involves unstructured data humans process slowly
  - The idea names a technology before naming a problem
  - A prediction would change the decision being made
  answer: 2
  why: Leading with a technology rather than a measurable problem is a classic hype red flag; the other
    options are green flags for AI suitability.
- q: In the priority formula Priority = (Value × AI fit × Data readiness × Feasibility) / Effort, how
    is risk typically handled?
  options:
  - Added to the numerator
  - Ignored during discovery
  - Used as a gate that can reject an idea outright
  - Multiplied by effort
  answer: 2
  why: Risk is treated as a hard gate — a catastrophic, unmitigable risk disqualifies an idea regardless
    of its computed priority score.
- q: What is the intended deliverable of problem-first discovery?
  options:
  - A finished technical architecture
  - A detailed sprint plan
  - A prioritized, ranked shortlist of validated problems with owners
  - A trained model ready for production
  answer: 2
  why: Discovery produces a ranked opportunity list of validated problems with owners and rationale, not
    a build plan or model.
- q: In one or two sentences, write a problem statement using the recommended template for a support team
    drowning in repetitive tickets.
  answer: Support agents struggle to resolve high-volume repetitive tickets quickly because each requires
    manual lookup, which costs ~15 minutes per ticket and delays customer responses.
  why: A strong answer follows the 'who struggles to do what, because why, which costs what' format and
    includes a quantified impact rather than naming a solution.
- q: Name one green flag that indicates a problem is well-suited to AI.
  answer: High-volume repetitive decisions, unstructured data (text/images/audio) humans process slowly,
    or personalization at scale.
  why: These signal learnable patterns and scale where AI predictions or generation meaningfully improve
    outcomes over rules or manual work.
resources:
- label: Google PAIR — People + AI Guidebook (User Needs & Defining Success)
  url: https://pair.withgoogle.com/guidebook/
- label: a16z — AI Product Management and Opportunity Framing
  url: https://a16z.com/ai/
- label: 'Marty Cagan — INSPIRED: Product Discovery Principles'
  url: https://www.svpg.com/inspired-how-to-create-products-customers-love/
- label: Microsoft — Responsible AI Impact Assessment Template
  url: https://www.microsoft.com/en-us/ai/responsible-ai
---

## Why Problem-First Matters

The fastest way to waste an AI budget is to start with the technology: "We need to add a chatbot" or "Let's use GenAI somewhere." Problem-first discovery flips this. You begin with a clearly articulated problem, quantify its impact, and only then ask whether AI is the right tool. This protects you from hype-driven projects that demo well but never ship value.

AI is a means, not an end. A good AI opportunity exists when there is a painful, frequent, and measurable problem where prediction, generation, classification, or pattern-finding meaningfully changes the outcome.

## The Problem-First Framework

Work through five steps:

1. **Frame the problem** — Write it as a user/business pain statement, not a feature. Use the format: *"[Who] struggles to [do what] because [why], which costs [impact]."*
2. **Quantify the impact** — Attach numbers: frequency, time lost, revenue at risk, cost per occurrence. No number means no priority.
3. **Test for AI-suitability** — Ask: Is there a pattern in data? Is the task repetitive or judgment-based at scale? Would a prediction or generation change the decision? If a simple rule or better UX solves it, you don't need AI.
4. **Check data and feasibility** — Do we have (or can we get) representative data? Is the cost of errors tolerable? Is latency acceptable?
5. **Estimate value vs. effort** — Rough sizing of business value against build/operate cost and risk.

## Screening Out Hype

Use these red flags to reject or pause ideas:

- The idea names a technology before naming a problem.
- No measurable impact or owner can be identified.
- A deterministic rule, search, or UI fix would solve it more cheaply.
- Required data doesn't exist and can't be obtained ethically.
- The cost of a wrong answer is catastrophic and unmitigable.

Green flags include: high-volume repetitive decisions, unstructured data (text, images, audio) that humans process slowly, personalization at scale, and tasks where "good enough" predictions beat the status quo.

## Scoring and Prioritization

Score each surviving candidate on a simple 1–5 scale across dimensions, then combine:

- **Value** — business/user impact if solved well.
- **AI fit** — how much AI uniquely improves the outcome.
- **Data readiness** — availability and quality of training/eval data.
- **Feasibility** — technical and operational achievability.
- **Risk** — inverse of regulatory, safety, and reputational exposure.

A practical formula: `Priority = (Value × AI fit × Data readiness × Feasibility) / Effort`, with risk used as a gate. Rank candidates to produce your prioritized opportunity list — typically a table with problem statement, score, owner, and a one-line rationale.

## From List to Roadmap

The output of discovery is not a project plan — it's a ranked shortlist of validated problems with clear ownership. The top items become candidates for discovery spikes or proofs of concept. Revisit the list quarterly as data, costs, and model capabilities change.

## Common Pitfalls

- Letting a senior leader's pet idea skip the screening.
- Confusing 'interesting' with 'valuable'.
- Ignoring the operating cost and human-in-the-loop needs.
- Scoring in isolation rather than comparing across the portfolio.
