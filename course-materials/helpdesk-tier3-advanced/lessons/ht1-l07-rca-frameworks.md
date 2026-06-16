---
course: helpdesk-tier3-advanced
title: Systematic RCA frameworks
month: 1
monthTitle: Advanced Troubleshooting & Root Cause Analysis
lesson: 7
summary: 'Replace ad-hoc guessing with repeatable root-cause methods: Five Whys, fault-tree thinking,
  and differential diagnosis. Learn when each framework fits and how to avoid stopping at the first plausible
  answer.'
objectives:
- Apply Five Whys without stopping at the first convenient cause
- Use a fault tree to enumerate and eliminate contributing conditions
- Run a differential diagnosis to rank competing hypotheses by evidence
- Apply the contributing-factors model to incidents with multiple causes
- Choose the right framework for the shape of the problem in front of you
- Recognise and counter the cognitive biases that derail systematic RCA
video: ht1-l07-rca-frameworks.mp4
quiz:
- q: A team runs Five Whys and concludes 'the technician forgot to apply the config.' Why is this usually
    a poor stopping point?
  options:
  - Five Whys should always have exactly five steps
  - It stops at human error instead of asking why the system allowed the error and let it reach production
    undetected
  - Human error is never a real cause
  - It should have used a fault tree instead
  answer: 1
  why: Stopping at 'human error' blames a person and ignores the systemic causes — no validation, no automation,
    no guardrail — that let the mistake happen and go undetected. Good Five Whys keeps asking why the
    system permitted it.
- q: When is a fault tree more appropriate than Five Whys?
  options:
  - When the incident has a single, linear cause chain
  - When you have no logs at all
  - When you want to assign blame quickly
  - When multiple conditions could each contribute and you need to enumerate and eliminate combinations
    systematically
  answer: 3
  why: Five Whys models a single linear chain. A fault tree is better when several conditions can combine
    (AND/OR logic) to produce the failure, letting you reason about and rule out combinations rather than
    one chain.
- q: In differential diagnosis, how do you decide which hypothesis to test next?
  options:
  - Test the one you find most interesting
  - Test the discriminating evidence that best separates the highest-ranked competing hypotheses
  - Always test the cheapest one regardless of value
  - Test them in alphabetical order
  answer: 1
  why: Differential diagnosis ranks hypotheses by current evidence, then seeks the test whose result most
    strongly discriminates between the leading contenders — maximising information gained per test.
- q: An incident is found to need a bad config AND a missing monitor AND a slow response to all coincide.
    Which model fits best?
  options:
  - Single root cause
  - A contributing-factors / Swiss-cheese model where several aligned conditions together produced the
    outcome
  - Five Whys with one chain
  - No model is needed
  answer: 1
  why: Many real incidents have no single root cause; multiple latent conditions align (Swiss-cheese).
    The contributing-factors model captures that several defences had to fail together, guiding fixes
    at multiple layers.
- q: In one sentence, what is the main danger of confirmation bias during RCA?
  answer: Confirmation bias leads you to seek and over-weight evidence that supports your initial theory
    while discounting evidence against it, so you stop investigating once the favourite hypothesis looks
    supported and miss the true cause.
  why: Because it prunes the hypothesis space prematurely around a hunch, confirmation bias is the most
    common way a systematic investigation quietly becomes a self-fulfilling one.
- q: Why should an RCA framework force you to state what evidence would disprove your leading hypothesis?
  answer: Requiring a disproving condition keeps the hypothesis falsifiable and forces you to actively
    look for contradicting evidence, which counters confirmation bias and prevents you from declaring
    root cause on a theory that merely fits the data you happened to collect.
  why: A hypothesis you cannot imagine disproving is not a conclusion you can defend; demanding the disproving
    test enforces rigour and guards against premature closure.
resources:
- label: Google SRE Workbook — Postmortem Culture and analysis
  url: https://sre.google/workbook/postmortem-culture/
- label: Google SRE Book — Effective Troubleshooting (hypothesis method)
  url: https://sre.google/sre-book/effective-troubleshooting/
- label: Microsoft Learn — Troubleshooting methodology
  url: https://learn.microsoft.com/en-us/troubleshoot/windows-client/welcome-windows-client
- label: NASA — Root Cause Analysis overview (Safety Center)
  url: https://sma.nasa.gov/sma-disciplines/root-cause-analysis
---

## Frameworks beat hunches

The difference between a senior engineer and a lucky one is **repeatability**. A framework forces you to enumerate hypotheses, test the right one next, and recognise when you have actually reached a cause rather than a convenient stopping point. No single method fits every problem — your skill is matching the framework to the *shape* of the incident.

## Five Whys: follow the chain, don't stop at the person

**Five Whys** repeatedly asks "why?" to walk from symptom to cause. It suits problems with a fairly **linear cause chain**. The classic failure is stopping at *human error* — "the tech forgot the config." That is a symptom of a systemic gap, not a root cause. Keep going:

```text
Symptom : VPN config missing on 30 machines
Why 1   : The deploy script skipped them        -> why?
Why 2   : They were offline at deploy time       -> why?
Why 3   : No retry for offline machines          -> why?
Why 4   : The tool has no state tracking         -> why?
Why 5   : No validation that config = intended   <- systemic root cause
```

The useful root cause is the **systemic gap** that let the error happen *and* go undetected — not the person.

## Fault trees: when causes combine

When several conditions can each contribute, a linear chain is the wrong model. A **fault tree** decomposes the top-level failure into contributing conditions joined by **AND/OR** logic, so you can enumerate and *eliminate* combinations rather than chase one thread.

```text
            [App fails to launch]
                   OR
      +-------------+-------------+
  [DLL missing]            [License check fails]
                                AND
                       +----------+----------+
                 [No network]        [Cache expired]
```

You then rule out branches with evidence until only a supported path remains. Fault trees shine for intermittent issues with multiple necessary conditions.

## Differential diagnosis: rank, then discriminate

Borrowed from medicine, **differential diagnosis** lists every plausible cause, ranks them by current evidence, and then chooses the test whose result best **discriminates** between the top contenders — maximising information per test. After each test you re-rank. This is the disciplined version of the "cheapest test that kills the most hypotheses" instinct from Lesson 1.

## Contributing factors: incidents rarely have one cause

Many real incidents have **no single root cause**. The **Swiss-cheese model** says several latent weaknesses had to align: a bad config *and* a missing monitor *and* a slow response. The **contributing-factors** approach captures all of them, so your fixes land at multiple layers rather than scapegoating one. If you only ever find one cause, you are probably stopping too early.

## Countering the biases

Every framework exists partly to defeat **cognitive bias**. **Confirmation bias** makes you over-weight evidence for your favourite theory; counter it by stating, up front, *what evidence would disprove* your leading hypothesis and then actively seeking it. **Anchoring** locks you to the first explanation you heard; **recency bias** makes the last incident feel like this one. Naming the bias is the first step to neutralising it.

## Your task

Take one of your investigations from Lessons 3-6. First, run a written Five Whys and deliberately push past any "human error" stopping point to a systemic gap. Then re-model the same incident as a fault tree with at least one AND and one OR node, and mark which branches your evidence eliminated. List your hypotheses as a ranked differential diagnosis, and for the top hypothesis write the single piece of evidence that would *disprove* it. Finish by stating whether the incident had one root cause or multiple contributing factors, and name one cognitive bias you caught yourself risking.
