---
course: kwasi-GenAI
title: Is the new prompt actually better?
month: 4
monthTitle: Production Engineering
lesson: 2
summary: Answer the question every team argues about — is the new prompt better? — with offline evaluation
  and online A/B testing instead of opinions.
objectives:
- Frame a prompt change as a measurable hypothesis with a target metric
- Run an offline A/B comparison of two prompts over a fixed eval set
- Design an online A/B test that splits live traffic between variants
- Distinguish a real improvement from noise using paired comparison and sample size
- 'Avoid common pitfalls: peeking, tiny samples, and changing two things at once'
- Promote, hold, or roll back a prompt based on the data
video: g4-l02-prompt-ab-testing.mp4
quiz:
- q: What is the core difference between offline and online evaluation of a prompt?
  options:
  - Offline uses the internet; online doesn't
  - Offline scores a fixed dataset; online splits real user traffic between variants
  - They are the same thing
  - Online is always cheaper
  answer: 1
  why: Offline eval grades a pinned golden set; online A/B testing routes live users to each variant and
    compares real outcomes.
- q: Why is a paired comparison (both prompts on the same inputs) stronger than testing each prompt on
    different inputs?
  options:
  - It uses fewer tokens
  - It removes input difficulty as a confounder, so the difference reflects the prompt
  - It is required by the API
  - It avoids the need for a metric
  answer: 1
  why: Running both prompts on the identical inputs cancels out the variation in question difficulty,
    isolating the effect of the prompt itself.
- q: What does 'peeking' mean and why is it a problem in an A/B test?
  options:
  - Reading the prompt aloud
  - Checking results repeatedly and stopping when they look good, which inflates false positives
  - Using a peek-token
  - Looking at the competitor's prompt
  answer: 1
  why: Repeatedly checking and stopping the moment a result looks significant dramatically raises the
    chance of a false win; decide the sample size up front.
- q: If you change the prompt wording AND switch the model at the same time, what's the issue?
  options:
  - Nothing, it's efficient
  - You can't attribute the result to either change
  - It violates the API terms
  - It doubles the cost only
  answer: 1
  why: Changing two variables at once means a score difference can't be attributed to the prompt or the
    model — change one thing per experiment.
- q: In one sentence, what should you define before running any prompt experiment?
  answer: A clear hypothesis and a single target metric — what you expect to improve and how you'll measure
    it — decided before you look at any results.
  why: Pre-registering the metric and hypothesis prevents you from rationalising whatever the data happens
    to show.
- q: In one sentence, when is offline eval enough and you can skip an online A/B test?
  answer: When your golden set faithfully represents production and the metric is something you can grade
    offline, a strong offline win is often enough to ship, with monitoring to confirm.
  why: Online tests cost real traffic and time; if offline eval is representative and conclusive, you
    can ship and verify with observability rather than a full A/B.
resources:
- label: Anthropic — Empirical prompt engineering and testing
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- label: Anthropic — Using the Evaluation tool to compare prompts
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool
- label: Microsoft Learn — How to evaluate and compare generative AI flows
  url: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-approach-gen-ai
- label: Evidently AI — A/B testing and online evaluation of LLM apps
  url: https://www.evidentlyai.com/llm-guide/llm-evaluation
- label: Microsoft Experimentation — Trustworthy online controlled experiments (KDD)
  url: https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/
---

## The argument every team has

Someone rewrites the system prompt, demos two cherry-picked examples, and declares it better. Someone else disagrees. The meeting goes in circles because nobody has a number. Last lesson you built the tools to end that argument: a golden dataset and scorers. This lesson is about *using* them to compare two prompts — first **offline**, cheaply, then **online** with real traffic when the stakes justify it. The mindset is the one you already apply to infrastructure changes: form a hypothesis, change one thing, measure, decide.

## Start with a hypothesis and one metric

Before touching the prompt, write down what you expect and how you'll judge it. "Adding a worked example will raise the faithfulness score" is a hypothesis with a metric. Decide the metric *before* you see results — otherwise you'll unconsciously pick whichever number makes your change look good. Change **one thing** per experiment. If you reword the prompt and swap the model in the same test, a score difference can't be attributed to either.

## Offline A/B: the paired comparison

The cheapest, fastest comparison runs both prompts over the **same** fixed eval set and grades each. Because both see identical inputs, question difficulty cancels out and the difference reflects the prompt.

```python
def run(prompt, dataset):
    return [generate(prompt, case["input"]) for case in dataset]

out_a = run(PROMPT_A, golden)
out_b = run(PROMPT_B, golden)

wins_b = sum(judge(c, a, b) == "B" for c, a, b in zip(golden, out_a, out_b))
print(f"B better on {wins_b}/{len(golden)} cases")
```

A pairwise judge — "which answer is better, A or B?" — is often more reliable than scoring each in isolation, because relative judgements are easier than absolute ones. Look at *where* B wins and loses, not just the total. A prompt that's better on average but worse on your critical edge cases may not be the one to ship.

## Online A/B: splitting real traffic

Offline eval is only as good as your golden set. When the change is risky or the set can't capture real behaviour, run an **online A/B test**: route a slice of live traffic to each variant and compare real outcomes — thumbs-up rate, task completion, escalation rate, latency.

```python
import hashlib

def variant(user_id):
    h = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    return "B" if h % 100 < 50 else "A"   # 50/50 split, stable per user
```

Hash the user id so each user consistently sees the same variant — flípping a user between prompts mid-session pollutes the data and confuses people. This is the same controlled-rollout instinct behind a canary deploy: small slice first, watch the metrics, expand if healthy.

## Telling signal from noise

LLM outputs are noisy, so a small lead can be luck. Two disciplines protect you. **Decide the sample size up front** and don't stop early just because B is winning — that's *peeking*, and it manufactures false wins. And prefer **paired** results, where you compare A and B on the same input, because that removes a huge source of variance. If the gap is tiny and the cost is real, "no meaningful difference" is a perfectly good, honest result.

## Promote, hold, or roll back

The outcome is one of three moves. **Promote** B if it wins clearly offline and holds up on a small online slice. **Hold** if it's a wash — keep the simpler prompt. **Roll back** instantly if the online metrics dip. Wire the decision to your existing release controls so a bad prompt is as easy to revert as a bad deploy.

## Your task

Take the golden set from last lesson and write a second prompt variant that changes exactly one thing. Run a paired offline comparison with a pairwise judge, record how many cases each wins. Then sketch (in code or pseudocode) an online split that assigns users to A or B stably by hashing their id, and name the live metric you'd watch. Write one sentence: ship, hold, or roll back — and why.
