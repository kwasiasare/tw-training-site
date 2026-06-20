---
course: ai-product-manager
title: Roadmapping AI Products Under Uncertainty
month: 2
monthTitle: AI Product Strategy and Roadmapping
lesson: 3
summary: Learn to build phased, hypothesis-driven roadmaps for AI products where outcomes are uncertain.
  This lesson shows how to balance research spikes, data acquisition, and shippable milestones using staged
  gates and clear success metrics.
objectives:
- Explain why traditional feature roadmaps fail for AI products and how uncertainty changes planning
- Structure an AI roadmap into discovery, validation, and scaling phases with explicit hypotheses
- Define entry and exit criteria (gates) that tie experiments to go/no-go decisions
- Sequence data acquisition, model experimentation, and shipping milestones to reduce risk early
- Communicate uncertainty and confidence levels to stakeholders without overcommitting on dates
- Apply metrics and kill criteria to keep an AI roadmap honest and adaptive
video: apm-m2-l03-roadmapping-ai-products-under-uncertainty.mp4
quiz:
- q: Why is a traditional feature roadmap risky for AI products?
  options:
  - AI features are always cheaper to build
  - Feasibility is uncertain until you experiment with data and models
  - Stakeholders never want dates
  - AI products don't need metrics
  answer: 1
  why: Unlike conventional software, you cannot assume an AI capability will reach its quality bar; feasibility
    must be validated through experimentation before you can promise outcomes.
- q: What is the primary output of the Discovery/Feasibility phase?
  options:
  - A production-ready product
  - A confidence signal about whether the capability is achievable
  - A finalized pricing model
  - A complete UI design
  answer: 1
  why: Discovery uses time-boxed spikes to produce evidence about feasibility—a confidence signal—not
    a shippable product.
- q: Which sequencing principle best reduces risk early in an AI roadmap?
  options:
  - Polish the UX before testing the model
  - Tackle the riskiest assumption first
  - Skip baselines and go straight to complex models
  - Delay data work until after launch
  answer: 1
  why: De-risking means addressing the biggest uncertainty first—usually data and feasibility—before investing
    in downstream work like UX.
- q: Why should kill criteria be defined in advance?
  options:
  - To guarantee the project never stops
  - To prevent sunk-cost momentum from sustaining a failing bet
  - Because investors require it legally
  - To avoid measuring anything
  answer: 1
  why: Pre-committed kill criteria give an objective basis to stop investing, countering the sunk-cost
    bias that keeps doomed projects alive.
- q: In one sentence, write a hypothesis-style roadmap item for an AI feature, including a measurable
    signal.
  answer: We believe an email-classification model will correctly route support tickets for SMB customers,
    and we'll know we're right when auto-routing accuracy exceeds 85% with under 5% misroute escalations.
  why: A good answer states the capability, the target outcome, the user segment, and a measurable signal
    that would confirm or falsify the bet.
- q: What is the benefit of presenting unproven AI work in 'Now / Next / Later' horizons?
  answer: It communicates direction and priority while honestly reflecting uncertainty, instead of committing
    to precise dates for work that hasn't been validated.
  why: Horizons avoid false precision on uncertain work and let the roadmap update as evidence arrives,
    keeping stakeholder expectations realistic.
resources:
- label: Marty Cagan, INSPIRED — product discovery and risk
  url: https://www.svpg.com/inspired-how-to-create-products-customers-love/
- label: Google People + AI Guidebook (PAIR)
  url: https://pair.withgoogle.com/guidebook/
- label: Now/Next/Later roadmap format (ProdPad)
  url: https://www.prodpad.com/blog/the-anatomy-of-the-perfect-product-roadmap/
- label: Emmanuel Ameisen, Building Machine Learning Powered Applications
  url: https://www.oreilly.com/library/view/building-machine-learning/9781492045106/
---

## Why AI Roadmaps Are Different

Traditional product roadmaps assume that if you build a feature correctly, it will work. AI products break that assumption: feasibility itself is uncertain until you experiment with data and models. You cannot promise an outcome (e.g., "95% accurate fraud detection") before you've validated it. Roadmapping under uncertainty means planning to *learn*, not just to *build*.

Key sources of uncertainty:
- **Feasibility**: Can a model actually reach the quality bar?
- **Data**: Do we have enough representative, labeled data?
- **Value**: Will users trust and adopt the AI output?
- **Cost/latency**: Is it economical and fast enough in production?

## Hypothesis-Driven Roadmapping

Frame each roadmap item as a testable hypothesis instead of a fixed deliverable:

> "We believe that [model/feature] will achieve [outcome] for [user segment]. We'll know we're right when [measurable signal]."

This reframes the roadmap from a list of promises into a sequence of bets, each with a way to be proven wrong cheaply.

## The Three-Phase Structure

1. **Discovery / Feasibility (spikes)** — Time-boxed experiments to test whether the core ML capability is achievable. Output: a confidence signal, not a product. Example: offline model evaluation on a sample dataset.
2. **Validation (thin slice)** — Ship a narrow, real version to a small audience. Test value and trust with real users (often with a human-in-the-loop fallback). Output: evidence of adoption and acceptable quality.
3. **Scaling / Hardening** — Improve reliability, reduce cost/latency, expand coverage, add monitoring and guardrails. Output: a production-grade product.

Each phase has **gates**: explicit entry and exit criteria. You only advance when evidence clears the gate; otherwise you iterate, pivot, or kill.

## Sequencing: Data and Experiments First

Reduce the biggest uncertainty earliest. Usually that means front-loading **data assessment** and **feasibility spikes** before committing UI or launch dates. A common anti-pattern is designing polished UX before knowing the model can perform.

Useful sequencing principles:
- Tackle the riskiest assumption first ("de-risking").
- Run a baseline (heuristic or simple model) before complex models.
- Treat data collection/labeling as a first-class roadmap item with its own timeline.
- Keep a manual or rules-based fallback so you can ship value while the model matures.

## Gates and Kill Criteria

Define in advance what success and failure look like. A gate might read: "Proceed to validation only if offline F1 ≥ 0.80 on the holdout set and labeling cost per item < $0.50." Equally important are **kill criteria** — the conditions under which you stop investing. Pre-committing to kill criteria prevents sunk-cost momentum.

## Communicating Uncertainty to Stakeholders

- Present the roadmap in **horizons** (Now / Next / Later) rather than precise quarterly dates for unproven work.
- Attach **confidence levels** to items (e.g., high/medium/low).
- Separate **committed** deliverables (low-uncertainty engineering) from **exploratory bets** (research spikes).
- Update the roadmap as evidence arrives; treat it as a living artifact tied to learning milestones.

## Putting It Together

A strong AI roadmap reads as a chain of de-risking decisions: identify the riskiest assumption, design the cheapest test, set a gate, and only then commit further resources. This keeps the team adaptive while still giving the business a credible path to shipping.
