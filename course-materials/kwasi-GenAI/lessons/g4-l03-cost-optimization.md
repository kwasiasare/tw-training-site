---
course: kwasi-GenAI
title: Cost optimization for LLM apps
month: 4
monthTitle: Production Engineering
lesson: 3
summary: Cut the bill without cutting quality using prompt caching, model routing from cheap to capable,
  and prompt compression — all grounded in how per-token pricing actually works.
objectives:
- 'Explain how LLM pricing works: separate rates for input and output tokens'
- Estimate the cost of a request from its input and output token counts
- Use prompt caching to stop paying full price for a repeated stable prefix
- Design a model-routing tier that tries a cheap model first and escalates
- Apply prompt compression and context trimming to shrink input tokens
- Measure cost per request and prove an optimization actually saved money
video: g4-l03-cost-optimization.mp4
quiz:
- q: How are LLM API calls priced?
  options:
  - A flat fee per request
  - Per token, with separate rates for input and output tokens
  - Per minute of compute
  - Per character of output only
  answer: 1
  why: You pay per token, and input (prompt) tokens and output (generated) tokens are billed at different
    rates — output is usually more expensive.
- q: What does prompt caching save you money on?
  options:
  - Output tokens
  - Re-processing a large, stable prompt prefix on repeated calls
  - Network bandwidth
  - Storage of logs
  answer: 1
  why: Caching stores a stable prefix (system prompt, tools, long context) so repeated calls read it at
    a large discount instead of paying full input price each time.
- q: What is the core idea of model routing?
  options:
  - Always use the biggest model
  - Try a cheap, fast model first and escalate to a stronger one only when needed
  - Route requests to the nearest server
  - Randomly pick a model
  answer: 1
  why: Routing handles the easy majority of requests on a cheap model and reserves the expensive model
    for the hard cases that actually need it.
- q: Which change reduces input tokens directly?
  options:
  - Raising max_tokens
  - Trimming irrelevant retrieved context and tightening the prompt
  - Adding more few-shot examples
  - Increasing temperature
  answer: 1
  why: Removing irrelevant context and compressing the prompt shrinks the input token count, which is
    billed on every call.
- q: In one sentence, why is output usually more expensive to control than input?
  answer: You can edit the input directly, but output length depends on the model's generation, so you
    control it indirectly by capping max_tokens and asking for concise answers.
  why: Input is yours to trim, while output cost is governed by how much the model generates, so you steer
    it with limits and instructions rather than editing it.
- q: In one sentence, how do you prove a cost optimization actually worked?
  answer: Log input and output token counts per request, convert to cost, and compare the average cost
    per request before and after the change on the same workload.
  why: Measuring real per-request token usage on a comparable workload turns a claimed saving into a verified
    one.
resources:
- label: Anthropic — Prompt caching
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- label: Anthropic — Pricing
  url: https://www.anthropic.com/pricing
- label: Anthropic — Reducing latency and cost
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/reduce-latency
- label: Anthropic — Token counting
  url: https://docs.anthropic.com/en/docs/build-with-claude/token-counting
- label: AWS — Prompt caching on Amazon Bedrock
  url: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
---

## You're billed per token, both ways

The single fact that drives every cost decision: LLM APIs charge **per token**, and **input tokens and output tokens are priced separately**. A token is roughly three-quarters of a word. Your input — system prompt, tools, retrieved context, the user's message — is billed at the input rate. The model's generated answer is billed at the output rate, which is typically several times higher. So a request that stuffs a huge document into context and asks for a long answer is expensive on both sides.

```python
def cost(in_tok, out_tok, in_rate, out_rate):
    # rates are dollars per million tokens
    return in_tok/1e6*in_rate + out_tok/1e6*out_rate
```

Once you can compute cost per request, optimization stops being guesswork. The three biggest levers are caching, routing, and compression.

## Lever 1: prompt caching

Many apps send the *same* large prefix every call — a long system prompt, tool definitions, a fixed knowledge document — and only the user's question changes. Paying full input price to re-process that identical prefix every time is waste. **Prompt caching** stores the stable prefix so repeated calls read it at a steep discount.

```python
msg = client.messages.create(
    model="claude-sonnet-4-6", max_tokens=512,
    system=[{"type": "text", "text": BIG_STABLE_PROMPT,
             "cache_control": {"type": "ephemeral"}}],
    messages=[{"role": "user", "content": question}])
```

Put the **stable** content first (system prompt, tools, long context) and the **variable** content last. There's a small premium to write the cache, so caching pays off when a prefix is reused within its lifetime — which is exactly the high-traffic case. The same feature exists on Amazon Bedrock, so the pattern carries into the cloud you already run.

## Lever 2: model routing

Not every request needs your most capable model. Most are easy. **Model routing** tries a cheap, fast model first — Haiku, `claude-haiku-4-5-20251001` — and escalates to a stronger one only when the cheap answer isn't good enough.

```python
def answer(q):
    draft = call("claude-haiku-4-5-20251001", q)
    if confident(draft):
        return draft
    return call("claude-opus-4-8", q)   # escalate hard cases
```

The escalation signal can be a confidence check, a validator, or a cheap classifier that labels the request's difficulty. If 80% of traffic is handled by the cheap model, your average cost drops sharply while hard cases still get the firepower they need. This is the same tiering you'd apply to compute: cheap instances for the baseline, burst to the expensive ones on demand.

## Lever 3: prompt compression

Every input token is billed on every call, so trim them. **Prompt compression** and context discipline mean: send only the retrieved chunks that are actually relevant (top-k, not everything), drop boilerplate, summarise long histories instead of replaying them verbatim, and keep the system prompt tight. For RAG especially, retrieving five sharp chunks instead of fifty mediocre ones cuts cost *and* often improves the answer by reducing distraction.

For output, cap `max_tokens` to a sane ceiling and instruct the model to be concise. You can't edit the output directly the way you edit input, so you control it with limits and instructions.

## Measure, don't assume

Every optimization here is a hypothesis until measured. Log `input_tokens` and `output_tokens` from each API response (they come back in the usage field), convert to cost, and compare the **average cost per request** before and after on the same workload. Watch quality at the same time — a cost win that tanks your eval scores from last lesson isn't a win. Cheaper *and* still good is the goal.

## Your task

Take a real prompt from your project. One: compute its cost per request from the token counts in the response usage field. Two: move the stable part into a cached prefix and re-measure. Three: write a two-tier router that tries Haiku and escalates to Opus when a validator fails. Report the average cost per request before and after, and confirm your eval score didn't drop.
