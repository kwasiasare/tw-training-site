---
course: ai-product-manager
title: 'Capstone: Pitch a Complete AI Product Plan'
month: 4
monthTitle: Stakeholders, Metrics, and Launch Capstone
lesson: 4
summary: This capstone lesson guides aspiring AI Product Managers to synthesize everything learned across
  the course—strategy, roadmap, PRD, evaluation plans, and success metrics—into a single portfolio-ready
  AI product proposal. Learners then deliver it as a mock leadership pitch, practicing the storytelling,
  prioritization, and risk-framing skills that distinguish strong AI PMs.
objectives:
- Synthesize strategy, roadmap, PRD, eval plans, and metrics into a single coherent AI product proposal
- Structure a compelling executive pitch narrative that ties user problem to business value
- Define both product success metrics and AI-specific quality/eval metrics with clear targets
- Articulate AI-specific risks (data, model, safety, cost) and concrete mitigations
- Anticipate and answer tough leadership questions about ROI, feasibility, and trade-offs
- Self-assess the proposal against a portfolio-ready rubric
video: apm-m4-l04-capstone-pitch-a-complete-ai-product-plan.mp4
quiz:
- q: Why should an AI product pitch translate '95% precision' into business terms like hours saved?
  options:
  - Because precision is not a real metric
  - Executives fund outcomes, not raw benchmark numbers
  - It makes the model more accurate
  - Business terms are always more impressive
  answer: 1
  why: Leadership cares about business impact. Translating model metrics into dollars or hours makes the
    value concrete and fundable, whereas a raw benchmark figure is hard to act on.
- q: Which pair correctly separates product metrics from model metrics?
  options:
  - Adoption & retention vs. hallucination rate & latency
  - Precision vs. recall
  - Cost per query vs. inference cost
  - Roadmap phases vs. PRD sections
  answer: 0
  why: Product metrics (adoption, retention, task success) measure user/business outcomes; model metrics
    (hallucination rate, latency, precision) measure system quality. Keeping them separate clarifies what
    success means.
- q: When should acceptance thresholds for model quality be defined?
  options:
  - After launch, based on user complaints
  - Before launch, as part of the eval plan
  - Only if the model underperforms
  - Never — AI is probabilistic
  answer: 1
  why: Defining acceptance thresholds before launch prevents moving the goalposts and creates an objective
    go/no-go gate, which de-risks the bet.
- q: What makes a roadmap phase strong in an AI product plan?
  options:
  - It lists as many features as possible
  - It is tied to a learning milestone, not just features
  - It avoids mentioning risks
  - It hides the cost model
  answer: 1
  why: Crawl-walk-run phases should be organized around what you need to learn or validate, so each phase
    reduces uncertainty before scaling investment.
- q: Name one AI-specific risk an executive will likely ask about, and a mitigation you would pair with
    it.
  answer: 'Example: Cost overruns from inference at scale — mitigation: model a cost-per-query budget,
    cache results, and set a usage-based guardrail with an owner. (Other valid risks: model drift with
    monitoring/retraining; bias/safety with eval audits; data quality with validation pipelines.)'
  why: AI introduces risks beyond traditional products. Pairing each named risk with a concrete mitigation
    and an owner shows leadership the bet is managed, not hopeful.
- q: In the pitch narrative arc, what should come immediately after the 'Hook'?
  options:
  - The detailed cost model
  - The Insight — why it's solvable now with AI
  - The full PRD
  - The team org chart
  answer: 1
  why: After hooking with the problem, the Insight explains why this is newly solvable with AI, setting
    up the credibility for your solution before proof and the ask.
resources:
- label: Lenny's Newsletter — How to write a compelling product strategy & pitch
  url: https://www.lennysnewsletter.com/
- label: Google PAIR — People + AI Guidebook (metrics, evals, UX patterns)
  url: https://pair.withgoogle.com/guidebook/
- label: OpenAI — Evals best practices for LLM products
  url: https://platform.openai.com/docs/guides/evals
- label: Amazon Working Backwards / PR-FAQ template
  url: https://www.workingbackwards.com/
---

## Capstone Overview

This is where it all comes together. Across this course you learned to identify AI opportunities, write PRDs, design evaluation plans, choose metrics, and manage stakeholders. The capstone asks you to **package all of that into one cohesive proposal and pitch it** as if you were seeking executive funding and headcount.

The deliverable is two things: (1) a written **AI Product Plan** (your portfolio artifact) and (2) a **10-minute mock leadership pitch** with Q&A.

## The AI Product Plan: Required Sections

A strong plan reads as a tight story, not a data dump. Include:

1. **Problem & Opportunity** — Who is the user, what painful job are they doing, and how big is the prize? Quantify with TAM/usage data where possible.
2. **Why AI, Why Now** — Justify that AI is the right tool (vs. rules/heuristics). Name the capability unlock (e.g., unstructured text understanding) and the enabling shift (cheaper inference, better models).
3. **Solution & Strategy** — Your product concept, the wedge, and the moat. One crisp sentence of positioning.
4. **Roadmap** — Phased plan: crawl (validate), walk (scale), run (differentiate). Tie phases to learning milestones, not just features.
5. **PRD Highlights** — Core user stories, the happy path, and the human-in-the-loop design. Include what is explicitly out of scope.
6. **Evaluation Plan** — How you measure model quality offline (golden datasets, rubrics, LLM-as-judge) and online (A/B, shadow mode). Define acceptance thresholds before launch.
7. **Metrics & Targets** — Separate **product metrics** (adoption, retention, task success, time saved) from **model metrics** (accuracy, precision/recall, hallucination rate, latency, cost per query). Always name a North Star and guardrail metrics.
8. **Risks & Mitigations** — Data quality, model drift, safety/bias, cost overruns, regulatory exposure. Pair each risk with a mitigation and an owner.
9. **Ask** — The decision you want: budget, headcount, timeline, and the go/no-go gate.

## Crafting the Pitch Narrative

Leadership pitches reward clarity over completeness. Use a simple arc:

- **Hook** (problem framed as money or pain) →
- **Insight** (why this is solvable now with AI) →
- **Solution** (your product) →
- **Proof** (eval results, prototype, or comparable benchmarks) →
- **Plan & Ask** (roadmap, metrics, what you need).

Lead with the conclusion. Executives are busy—state the ask early, then support it. Use one chart per idea. Pre-empt objections by addressing the biggest risk yourself.

## AI-Specific Pitch Tips

- **Be honest about uncertainty.** AI outcomes are probabilistic. Show how your eval plan de-risks the bet rather than pretending the model is perfect.
- **Frame metrics in business terms.** "95% precision" means little; "fewer than 1 wrong escalation per 100, saving 200 agent-hours/month" lands.
- **Show the cost model.** Inference cost per query × volume is a real P&L line. Executives will ask.
- **Define the guardrail.** What's the safety/quality floor below which you would not ship?

## Anticipating Tough Questions

Prepare answers for: *What if the model isn't accurate enough? How much does this cost at scale? What's the build vs. buy decision? How do we measure success in 90 days? What's the biggest reason this fails?* Strong PMs rehearse these.

## Self-Assessment Rubric

Score your plan 1-5 on: problem clarity, AI justification, eval rigor, metric quality (leading + guardrail), risk realism, and pitch storytelling. Anything scoring ≤3 is your revision priority before adding it to your portfolio.
