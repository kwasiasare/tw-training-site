---
course: kwasi-GenAI
title: How LLMs behave
month: 1
monthTitle: LLM Foundations & API Fluency
lesson: 1
summary: 'Understand what a large language model actually does: it splits text into tokens, predicts the
  next token from a context window, and samples from those predictions using temperature and top-p.'
objectives:
- Explain how text is split into tokens and why token count matters
- Describe the context window and what happens when you exceed it
- Explain next-token prediction as the core mechanism behind every response
- Adjust temperature and top-p to control randomness in a deliberate way
- Predict how a given setting will make outputs more focused or more varied
- Connect token budgets to cost and latency in a production system
video: g1-l01-how-llms-behave.mp4
quiz:
- q: What is a token, as an LLM sees it?
  options:
  - A single character
  - A chunk of text — often a word or word-piece — mapped to a number
  - A full sentence
  - A line of code
  answer: 1
  why: Models operate on tokens, which are sub-word chunks (roughly 3-4 characters of English on average),
    each mapped to an integer the model can process.
- q: What does the context window define?
  options:
  - The model's training cutoff date
  - The maximum tokens of input plus output the model can attend to at once
  - The number of GPUs used
  - The temperature setting
  answer: 1
  why: The context window is the total token budget the model can see in one request — prompt plus the
    response it generates — and exceeding it forces truncation or an error.
- q: How does an LLM actually produce text?
  options:
  - It looks the answer up in a database
  - It predicts one token at a time, each conditioned on everything before it
  - It compiles your prompt into a program
  - It searches the web by default
  answer: 1
  why: 'Generation is autoregressive: the model repeatedly predicts a probability distribution over the
    next token, picks one, appends it, and repeats.'
- q: What does raising the temperature do?
  options:
  - Speeds up the model
  - Flattens the probabilities so less-likely tokens get picked more often, increasing variety
  - Shrinks the context window
  - Forces JSON output
  answer: 1
  why: Higher temperature flattens the next-token distribution, making sampling more random and outputs
    more varied; lower temperature sharpens it toward the most likely tokens.
- q: In one sentence, what does top-p (nucleus) sampling do?
  answer: It keeps only the smallest set of most-likely tokens whose probabilities add up to p, then samples
    from that set, trimming the long tail of unlikely tokens.
  why: Top-p caps the candidate pool by cumulative probability rather than by a fixed count, so the model
    never picks from the implausible tail.
- q: Why should a DevOps engineer care about token counts in production?
  answer: Because tokens drive both cost (you pay per input and output token) and latency (longer context
    and longer output take more time), so token budgets are a real operational constraint.
  why: Token count maps directly to spend and response time, which makes it a capacity-planning concern
    just like CPU or memory.
resources:
- label: Anthropic — Context windows
  url: https://platform.claude.com/docs/en/build-with-claude/context-windows
- label: Anthropic — Token counting
  url: https://platform.claude.com/docs/en/build-with-claude/token-counting
- label: Anthropic — Models overview
  url: https://platform.claude.com/docs/en/about-claude/models/overview
- label: Hugging Face — Summary of the tokenizers
  url: https://huggingface.co/docs/transformers/tokenizer_summary
---

## A model that only predicts the next token

A large language model does one thing astonishingly well: given some text, it predicts what token comes next. Everything else — answering questions, writing code, summarising a document — is that single trick repeated thousands of times. There is no database lookup, no hidden search engine. The model holds a learned sense of "what usually follows what" and uses it one step at a time.

This matters because it reframes how you think about prompting. You are not issuing a command to a program; you are giving the model a starting context and letting it continue in the most probable way. Good prompts shape that probability.

## Tokens: the unit the model actually sees

Models do not read characters or words directly. They read **tokens** — chunks of text mapped to integers. A token is often a whole common word, but longer or rarer words get split into word-pieces. As a rough rule for English, one token is about 3 to 4 characters, or roughly three-quarters of a word.

This is why `cat` might be one token but `unbelievability` is several, and why code or non-English text can tokenise very differently. You will count tokens often, because they drive cost and fit.

## The context window

The **context window** is the total number of tokens the model can attend to in a single request — your prompt *and* the response it generates, combined. Current Claude models such as Opus `claude-opus-4-8` and Sonnet `claude-sonnet-4-6` offer very large windows, but every model has a limit.

If you push past it, the model cannot see the overflow: older content gets truncated or the request is rejected. Treat the window as a budget. Long documents, long chat histories, and large tool outputs all compete for the same space.

## Next-token sampling: temperature and top-p

At each step the model produces a probability distribution over every possible next token. How you *pick* from that distribution decides how the text feels.

- **Temperature** reshapes the distribution. Low temperature sharpens it toward the single most likely token, giving focused, repeatable output. High temperature flattens it, so less likely tokens get a chance and the text becomes more varied — and more surprising.
- **Top-p** (nucleus sampling) trims the candidate pool. It keeps only the smallest set of tokens whose probabilities sum to `p` (say 0.9) and samples from those, discarding the long tail of implausible options.

Use low temperature for extraction, classification, and anything you need to be deterministic-ish. Use higher temperature for brainstorming or creative drafts.

```bash
# Conceptually, per request you tune:
temperature = 0.0   # focused, near-deterministic
temperature = 1.0   # varied, creative
top_p       = 0.9   # ignore the unlikely tail
```

A note for later: some current Claude models remove `temperature` and `top_p` entirely and steer behaviour through prompting and effort instead. The *concept* still explains how any LLM turns predictions into words — and that intuition transfers to every provider you will meet, including the models you can run on Amazon Bedrock or Azure.

## Why this is foundational

Once you internalise "tokenise, predict, sample, repeat," the rest of the course clicks into place. Hallucination, cost, latency, and the value of structure all follow from this one loop.

## Your task

Take a short paragraph of your own writing and estimate its token count (about words divided by 0.75). Then write one sentence describing what you would expect a low-temperature versus a high-temperature continuation of that paragraph to look like.
