---
course: ai-product-manager
title: 'Capstone: Ship an AI Product Case Study'
month: 5
monthTitle: Capstone & Career Launch
lesson: 1
summary: In Module 4 you pitched a forward-looking AI product plan; this capstone turns that thinking
  into a finished, retrospective case study you can hand a hiring manager. You will produce one complete
  AI-product case study that walks from problem and PRD through a metrics tree, an eval plan, a go-to-market,
  and an honest launch retrospective, written as a single narrative arc rather than a folder of documents.
  The lesson gives you a concrete six-part structure, a scoring rubric, and a clear definition of what
  'done' means so you can self-assess before you publish. The deliverable is the single strongest piece
  of evidence in an experience-led field where AI PM hiring rewards demonstrated judgment over credentials.
  Treat it as the artifact every later lesson in this module will package, link, and sell.
objectives:
- Assemble a complete AI-product case study spanning problem, PRD, metrics tree, eval plan, GTM, and launch
  retro
- Write the case study as one narrative arc that shows product judgment, not a disconnected document dump
- Build a metric tree that connects a north-star metric to the inputs your AI feature actually moves
- Specify an eval plan with offline golden sets, online tests, and acceptance thresholds set before launch
- Write an honest launch retrospective that names what you learned, what you would change, and what you
  cut
- Self-assess the case study against a portfolio rubric and a clear definition of done before publishing
video: apm-m5-l01-capstone-ship-an-ai-product-case-study.mp4
quiz:
- q: What distinguishes a portfolio-grade AI case study from a folder of PM documents?
  options:
  - It contains the largest possible number of artifacts and screenshots
  - It reads as one narrative arc — problem, decision, evidence, outcome, and what you learned — that
    demonstrates judgment
  - It hides any metrics that did not improve
  - It omits the PRD so reviewers focus on the pitch
  answer: 1
  why: Hiring managers evaluate judgment, not volume. A case study that connects a real problem to the
    decisions you made, the evidence behind them, the measured outcome, and your honest reflection proves
    you can lead an AI product end to end. A loose folder of documents makes the reviewer do the work
    of finding the story.
- q: In a metric tree for an AI feature, how should the north-star metric relate to the inputs below it?
  options:
  - The north star should be a model metric like token accuracy
  - The inputs should be unrelated vanity metrics that look impressive
  - The north star expresses durable user value, and the input metrics are the levers your feature can
    actually move toward it
  - There should be only one metric and no inputs at all
  answer: 2
  why: A metric tree decomposes a single north-star metric that captures durable user value into the input
    metrics that drive it. A good tree shows that your AI feature plausibly moves specific inputs (e.g.,
    task completion rate, time-to-first-draft) which in turn move the north star, making the impact mechanism
    explicit and testable.
- q: When should the acceptance thresholds in your eval plan be defined?
  options:
  - Before launch, as part of the eval plan, so they form an objective go/no-go gate
  - After launch, once you see how users react
  - Only if leadership asks for them
  - They are unnecessary because AI output is subjective
  answer: 0
  why: Defining acceptance thresholds before launch prevents moving the goalposts and creates an objective
    go/no-go gate. Setting them after the fact lets a weak result be rationalized as success, which is
    exactly the discipline a case study should demonstrate.
- q: What makes a launch retrospective section credible rather than self-promotional?
  options:
  - It claims every metric improved and no trade-offs were made
  - It names what you cut, what surprised you, what you would change, and the limits of your evidence
  - It blames engineering for anything that went wrong
  - It removes all numbers so nothing can be questioned
  answer: 1
  why: Honest reflection is a senior signal. A retro that names scope you cut, results that surprised
    you, decisions you would revisit, and the limits of your data reads as someone who learns from shipping.
    Uniformly positive retros read as marketing and erode trust.
- q: Why is a strong case study especially valuable for breaking into AI product management?
  options:
  - Because a single certification guarantees an AI PM offer
  - Because PM hiring is experience- and portfolio-led, so demonstrated end-to-end judgment substitutes
    for the on-the-job track record a career-changer lacks
  - Because case studies replace the need to interview
  - Because hiring managers never read written work
  answer: 1
  why: Product management is hired on demonstrated judgment, and AI PM roles add the expectation that
    you can reason about models, evals, and risk. A complete case study lets a career-changer prove that
    end-to-end capability concretely, which is why it is the centerpiece artifact the rest of this module
    promotes.
- q: In two to four sentences, describe the six sections your AI product case study must include and why
    each earns its place.
  answer: 'The case study moves through problem and opportunity (who hurts and how big the prize is),
    a PRD with the behavior spec and guardrails (what you decided to build and why), a metric tree (how
    you connect a north star to the inputs your feature moves), an eval plan with pre-set thresholds (how
    you proved quality before shipping), a go-to-market plan (how you rolled it out and to whom), and
    a launch retrospective (what happened, what you learned, and what you would change). Each section
    earns its place because together they show the full arc of product judgment: framing, specifying,
    measuring, validating, launching, and learning. Dropping any one leaves a visible gap in the story
    a reviewer is trying to verify.'
  why: A complete answer names all six sections and explains that they form a coherent arc from problem
    framing to reflection. The point is that the sections are not a checklist but a narrative that proves
    end-to-end judgment, and each one closes a specific gap a reviewer would otherwise probe.
resources:
- label: Amazon Working Backwards / PR-FAQ template
  url: https://www.workingbackwards.com/
- label: Amplitude — The North Star Playbook (metric trees and inputs)
  url: https://amplitude.com/north-star
- label: Google PAIR — People + AI Guidebook (metrics, evals, UX patterns)
  url: https://pair.withgoogle.com/guidebook/
- label: Ragas — open-source evaluation framework for LLM products (golden sets, faithfulness, LLM-as-judge)
  url: https://docs.ragas.io/en/stable/
---

## From Pitch to Proof

In Module 4 you pitched a complete AI product plan: a forward-looking case for funding. This capstone asks for something different and, for a job search, more valuable. You will write a **retrospective case study** of an AI product or feature, real, simulated, or a redesign of something you use, that walks a reader from the original problem all the way to an honest reflection on what shipping taught you. Where the pitch sells a bet, the case study proves you can think and operate across the whole lifecycle. It is the single artifact the rest of this module will package into a portfolio, a resume, and a LinkedIn profile, so it is worth getting right.

The reason this matters is structural. Product management is hired on demonstrated judgment, not credentials, and AI PM roles add the expectation that you can reason about models, evaluation, and risk. A career-changer rarely has a shipped-at-scale track record to point to. A complete, well-told case study is the closest substitute: it lets a hiring manager watch you make decisions and see the evidence behind them.

## Choosing What to Write About

The best subject is a problem you understand deeply where AI plausibly helps. You have three honest options, in rough order of strength. First, **real work**, a feature you shipped or shaped, anonymized to respect confidentiality. Second, a **redesign of a product you use daily**, where you can speak credibly about the user and propose an AI feature with a clear job-to-be-done. Third, a fully **simulated product** built around a domain you know. All three are legitimate as long as you label them honestly; an interviewer cares far more about the rigor of your reasoning than whether the thing reached production. Avoid generic 'AI for everything' concepts and pick a narrow, sharp use case: a support-ticket summarizer, a drafting assistant for a specific role, a triage classifier. A tight scope lets you go deep, and depth is what reads as senior.

## The Six-Part Structure

A strong case study reads as one story with six sections. Each section closes a gap a skeptical reviewer would otherwise probe.

1. **Problem & Opportunity.** Who is the user, what painful job are they doing, and how big is the prize? Open with the user's pain in concrete terms and size the opportunity with whatever data you have, usage, market, or a defensible estimate. Justify *why AI, why now*: name the capability the model unlocks and the shift (cheaper inference, stronger models, better tooling) that makes it feasible today.
2. **PRD.** The product decision. Summarize the behavior spec, the input/output contract, the happy path, the human-in-the-loop design, the guardrails for harmful content, privacy, and misuse, and what you put explicitly out of scope. You do not paste the whole PRD; you show the decisions and link the full document.
3. **Metric Tree.** How you will know it worked. Pick one **north-star metric** that captures durable user value, then decompose it into the **input metrics** your feature can actually move. Show the mechanism: the feature improves an input, which moves the north star. Separate **product metrics** (adoption, retention, task success, time saved) from **model metrics** (precision, hallucination rate, latency, cost per query), and name your guardrail metrics, the floors you refuse to cross.
4. **Eval Plan.** How you proved quality before shipping. Describe the offline evaluation, golden datasets, rubrics, and where appropriate an LLM-as-judge, and the online evaluation, A/B tests or shadow mode. State your **acceptance thresholds before launch** so they form an objective go/no-go gate.
5. **Go-to-Market.** How you rolled it out. Cover the launch strategy (internal dogfood, then a percentage rollout, then general availability), the positioning and messaging, enablement for support and sales, pricing or cost implications, and the rollback plan if a guardrail trips.
6. **Launch Retrospective.** What actually happened and what you learned. Report the results against your pre-set thresholds, name what surprised you, what you cut and why, what you would change, and the limits of your evidence. This is the section that separates an operator from a planner.

## Make It a Narrative, Not a Dump

The most common failure is a folder of disconnected documents. The fix is to write transitions that carry a decision forward: the problem motivates the PRD, the PRD defines what the metric tree must measure, the metric tree tells the eval plan what 'good' means, the eval result gates the go-to-market, and the launch feeds the retro. When each section answers a question the previous one raised, the reader experiences your judgment rather than auditing your paperwork.

Lead with conclusions. Open the case study with a two-sentence summary, the problem, what you shipped, and the measured outcome, so a busy reviewer gets the gist in ten seconds and reads on for the depth. Use one diagram for the metric tree and one for the architecture or user flow; visuals are scanned first.

## Quantify Honestly

Even for a simulated product you can and should quantify. Translate model metrics into business terms: '95% precision' lands as 'fewer than one wrong escalation per hundred, saving roughly 200 agent-hours a month.' Where a number is an estimate, label it as one and show your assumptions. Inflated or unlabeled numbers are the fastest way to lose a credible reviewer; a clearly reasoned estimate is far stronger than a precise-looking fabrication.

## Common Failure Modes to Avoid

Four mistakes sink otherwise-promising case studies. The first is **solution-first framing**, opening with the AI feature before establishing the user pain, which signals you reach for technology before understanding the problem. The second is a **missing 'why AI'**, where the same outcome could be achieved with a rule or a form; always defend why a model is the right tool. The third is **evals as an afterthought**, mentioning accuracy in one line with no golden set, thresholds, or online plan; for an AI PM this is the most visible competence, so give it real space. The fourth is a **glossy retro** in which everything worked, which reads as marketing rather than reflection. If you catch any of these in your draft, fix them before you fix anything else, because each one undercuts the exact judgment the case study is meant to prove.

## What 'Done' Means

The case study is done when all six sections are present and connected, every quantified claim is either sourced or labeled an estimate, the metric tree visibly links a north star to movable inputs, the eval plan states thresholds set before launch, and the retro names at least two things you would change. If any section is missing or any claim is unsupported, it is not done, it is a draft.

## The Scoring Rubric

Before you publish, score the case study one to five on each dimension and revise anything at three or below:

- **Problem clarity** — is the user, the pain, and the prize unmistakable?
- **AI justification** — is 'why AI, why now' specific, not hand-waved?
- **Spec quality** — does the PRD show real decisions, guardrails, and non-goals?
- **Metric rigor** — does the tree connect a north star to movable inputs with named guardrails?
- **Eval discipline** — are there offline and online evals with pre-set thresholds?
- **GTM realism** — is the rollout phased, with enablement and a rollback plan?
- **Reflection honesty** — does the retro name trade-offs, surprises, and changes?
- **Narrative & polish** — does it read as one story a reviewer can skim and trust?

The deliverable of this lesson is a single, finished case study that scores at least a four on every dimension, the piece you will spend the rest of this module turning into a portfolio, a resume bullet, and a LinkedIn story.
