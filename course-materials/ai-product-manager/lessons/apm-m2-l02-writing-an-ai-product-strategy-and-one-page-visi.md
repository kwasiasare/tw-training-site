---
course: ai-product-manager
title: Writing an AI Product Strategy and One-Page Vision
month: 2
monthTitle: AI Product Strategy and Roadmapping
lesson: 2
summary: Learn to write a defensible AI product strategy and a one-page vision document that aligns stakeholders,
  clarifies positioning and differentiation, and connects AI capabilities to real customer and business
  value.
objectives:
- Articulate a clear AI product vision narrative that motivates teams and stakeholders
- Define positioning and differentiation grounded in defensible AI advantages (data, workflow, distribution)
- Translate strategy into measurable outcomes and a prioritized set of bets
- Distinguish genuine AI moats from commodity capabilities and feature parity
- Produce a one-page vision document that fits on a single page and survives executive review
video: apm-m2-l02-writing-an-ai-product-strategy-and-one-page-visi.mp4
quiz:
- q: Which of the following is most likely to be a durable moat for an AI product?
  options:
  - Access to a general-purpose LLM API
  - A compounding proprietary data flywheel
  - A well-crafted prompt template
  - A clean chat interface
  answer: 1
  why: General API access, prompts, and chat UIs are easily replicated commodities. A proprietary data
    flywheel compounds with usage and is hard for competitors to copy.
- q: What is the primary purpose of the "What we are NOT doing" section in a one-page vision?
  options:
  - To pad the document to a full page
  - To impose the discipline of saying no and sharpen strategic choices
  - To list competitor weaknesses
  - To document technical limitations of the model
  answer: 1
  why: Explicit non-goals force real trade-offs, which is what separates a focused strategy from a wish
    list of features.
- q: Which question best pressure-tests an AI product's defensibility?
  options:
  - Does the model use the latest architecture?
  - If a competitor had the same model API tomorrow, what would they still lack?
  - How many parameters does the model have?
  - Is the UI better than competitors'?
  answer: 1
  why: This question isolates what is truly hard to copy — data, workflow, distribution, domain depth
    — versus commodity model access.
- q: In the Today–Tension–Future–Bridge narrative structure, what does the 'Bridge' represent?
  options:
  - The painful current state
  - The capability that makes the future state possible
  - The competitive landscape
  - The pricing model
  answer: 1
  why: The Bridge is the enabling capability that connects the painful Today to the aspirational Future
    the product creates.
- q: Name one AI-specific guardrail metric (beyond a growth north-star) that an AI product strategy should
    track.
  answer: Quality/accuracy, trust and safety, cost-per-inference, or latency
  why: AI strategies must guard against degrading quality, safety, or unit economics; any of these guardrails
    prevents optimizing growth at the expense of the product's integrity.
- q: Why is a strong 'why now' statement especially important for AI products?
  answer: It names the specific enabling shift (cheaper inference, new model capabilities, data availability,
    regulation) that makes the timing credible
  why: AI timing depends on recent enabling shifts; naming them makes the opportunity believable rather
    than speculative hype.
resources:
- label: 'Good Strategy Bad Strategy by Richard Rumelt (kernel of strategy: diagnosis, guiding policy,
    coherent action)'
  url: https://www.goodstrategybadstrategy.com/
- label: a16z — The Economics of AI and Where Moats Come From
  url: https://a16z.com/ai/
- label: Amazon's Working Backwards / PR-FAQ method for vision documents
  url: https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes
- label: Lenny's Newsletter — Product strategy and positioning frameworks
  url: https://www.lennysnewsletter.com/
---

## Why AI Product Strategy Is Different

AI products carry uncertainty that traditional software does not: model behavior is probabilistic, data is a first-class asset, and capabilities can be rapidly commoditized by foundation-model providers. A strong AI product strategy answers a deceptively simple question: **why will this product win, and why will it keep winning?** It cannot rest on "we use AI" — that is table stakes. It must rest on a defensible advantage and a clear connection to customer value.

Strategy is a set of choices about where to play and how to win. The one-page vision is the artifact that communicates those choices crisply enough that any stakeholder — an engineer, an executive, a sales rep — can repeat it.

## The Core Components of an AI Product Strategy

1. **Customer and problem** — Who hurts, how badly, and how often? AI is expensive and uncertain, so the problem must justify it. Prefer problems where current solutions are slow, costly, or impossible without intelligence.
2. **Vision narrative** — A short story of the future state your product creates. It should be aspirational but believable.
3. **Positioning** — The category you compete in and the reference point in the customer's mind ("the X for Y").
4. **Differentiation and moat** — What makes you hard to copy. For AI this typically comes from proprietary or compounding data, deep workflow integration, distribution, or a system of models tuned to a specific domain — *not* the base model itself.
5. **Strategic bets** — The 3-5 things you are betting on, and the assumptions behind each.
6. **Outcomes and metrics** — How you will measure progress (north-star metric plus guardrails like quality, cost-per-inference, and trust/safety metrics).

## Defensibility: Real Moats vs. Commodity Capabilities

Ask: if a competitor had the same model API tomorrow, what would they still lack? Durable AI advantages include:

- **Data flywheel** — usage generates proprietary data that improves the product, which attracts more usage.
- **Workflow lock-in** — the product is embedded in how work gets done, with switching costs.
- **Distribution** — existing channels, integrations, or an installed base.
- **Domain depth** — evaluation sets, fine-tuning, guardrails, and tacit knowledge competitors lack.

Commodity (not moats by themselves): access to a general LLM, a clever prompt, a chat UI, generic embeddings. These are easily replicated.

## Writing the Vision Narrative

Good vision narratives are concrete and customer-anchored. Use the structure: **Today** (the painful status quo), **Tension** (why it persists / why now), **Future** (the world your product enables), **Bridge** (the capability that makes it possible). Keep it to a paragraph or two. Avoid hype words; describe observable outcomes ("a claims adjuster resolves a case in minutes, not days").

"Why now?" is critical for AI — name the specific enabling shift (cheaper inference, multimodal models, regulatory change, data availability) so the timing is credible.

## The One-Page Vision Template

Fit all of this on a single page:

- **Vision statement** (1-2 sentences)
- **Target customer & problem** (who, pain, frequency)
- **Why now** (the enabling shift)
- **How we win** (positioning + differentiation/moat)
- **Strategic bets** (3-5 bullets with key assumption each)
- **Success metrics** (north star + 2-3 guardrails including a quality/trust metric)
- **What we are NOT doing** (explicit non-goals)

The non-goals section is what separates strategy from a wish list. Saying no is the discipline that makes the document defensible.

## Common Pitfalls

- **Tech-first framing** — leading with the model instead of the customer outcome.
- **No defensibility** — a vision any competitor with an API key could execute.
- **Vague metrics** — "improve engagement" without a target or guardrail.
- **Ignoring trust and risk** — AI strategies must address quality, safety, and failure modes as part of the value proposition.
- **Too long** — if it doesn't fit on one page, the choices aren't sharp enough.

## Putting It Together

Draft the narrative first to get conviction, then compress into the one-pager, then pressure-test defensibility with the "same API tomorrow" question. Socialize it, capture objections, and iterate. The one-pager becomes the anchor for your roadmap — every initiative should trace back to a strategic bet on the page.
