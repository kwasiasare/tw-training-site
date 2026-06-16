---
course: dami-ai-career
title: 'How LLMs work: tokens, context, sampling'
month: 3
monthTitle: LLM Application Skills
lesson: 1
summary: Understand how a large language model turns text into tokens, predicts the next one, and how
  context and sampling shape its output.
objectives:
- Explain what a token is and why models work in tokens, not words
- Describe next-token prediction as the core mechanism of an LLM
- Understand the context window and why it is a hard limit
- Explain how temperature and top-p sampling control randomness
- Connect tokens to cost, latency, and the max_tokens setting
- Make a basic call to the Claude Messages API in Python
video: m3-l01-how-llms-work.mp4
quiz:
- q: What is a token, roughly?
  options:
  - A single character
  - A common chunk of text, often part of a word
  - Always one whole word
  - A sentence
  answer: 1
  why: Tokens are sub-word chunks. A word like "unhappiness" may split into several tokens, while a common
    word is usually one.
- q: At its core, what does a language model actually do?
  options:
  - Look answers up in a database
  - Predict the next token given the previous ones
  - Translate words into numbers and stop
  - Run a search engine query
  answer: 1
  why: An LLM is a next-token predictor. It repeatedly picks the most likely next token, then feeds it
    back in to continue.
- q: What does the context window limit?
  answer: The total number of tokens (input plus output) the model can consider at once.
  why: Everything you send plus everything the model generates must fit inside the context window; older
    tokens beyond it are not seen.
- q: What happens to randomness as you lower the temperature toward 0?
  options:
  - Output becomes more random
  - Output becomes more deterministic and focused
  - The model refuses to answer
  - Tokens get longer
  answer: 1
  why: Low temperature sharpens the probability distribution, so the model almost always picks the most
    likely token, giving stable, repetitive output.
- q: Why does token count matter in a real application?
  answer: Tokens drive cost and latency, and both input and output count toward the context window and
    pricing.
  why: APIs bill per token and longer prompts take longer to process, so counting tokens helps you control
    cost and stay within limits.
- q: In the Claude Messages API, what does max_tokens control?
  options:
  - The size of the input prompt
  - The maximum number of tokens the model may generate in its reply
  - The temperature
  - The number of messages
  answer: 1
  why: max_tokens caps the length of the model's response only; it does not limit the input you send.
resources:
- label: Anthropic — Messages API reference
  url: https://docs.anthropic.com/en/api/messages
- label: OpenAI — Tokenizer (interactive tool to see tokens)
  url: https://platform.openai.com/tokenizer
- label: Jay Alammar — The Illustrated Transformer
  url: https://jalammar.github.io/illustrated-transformer/
- label: Anthropic — Token counting guide
  url: https://docs.anthropic.com/en/docs/build-with-claude/token-counting
---

## Tokens: the model's units

A **large language model** does not read words the way you do. It reads **tokens** — common chunks of text. A token might be a whole short word, a piece of a longer word, a space, or a punctuation mark. As a rough rule, one token is about four characters of English, or roughly three quarters of a word.

The text is converted into tokens by a *tokenizer*, and each token maps to a number the model can do maths on. So before any prediction happens, your sentence becomes a list of integers.

## Next-token prediction

At its heart, an LLM does one thing: given the tokens so far, it predicts a **probability for every possible next token**. It then picks one, appends it, and repeats. That loop — predict, append, predict again — is how a whole paragraph gets generated, one token at a time.

This is why models sometimes "drift": each new token depends only on what came before, so a small early choice can steer the rest of the answer.

## The context window

The **context window** is the maximum number of tokens the model can hold in mind at once. Crucially, this budget covers **both** your input (the prompt) **and** the output it generates. If a conversation grows too long, the oldest tokens fall outside the window and the model simply cannot see them.

Think of it like working memory: large, but finite. Modern models have very large windows, but you still design prompts to fit.

## Sampling: temperature and top-p

The model gives a *distribution* over next tokens. **Sampling** decides how we pick from it.

- **Temperature** scales how sharp or flat the distribution is. Low temperature (near 0) makes output focused and near-deterministic; high temperature adds variety and surprise.
- **Top-p** (nucleus sampling) keeps only the smallest set of tokens whose probabilities add up to *p*, then samples from those.

Low temperature for facts and code; higher for brainstorming and creative writing.

## Tokens, cost, and latency

Because work scales with tokens, **tokens are money and time**. APIs bill per input token and per output token, and longer prompts take longer to process. Counting tokens before sending helps you predict cost and stay inside the window.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

count = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "How do tokens work?"}],
)
print(count.input_tokens)
```

## Your first Claude call

Here is a minimal call to the Claude Messages API. Note `max_tokens`: it caps the length of the **reply**, not your input.

```python
import os
from anthropic import Anthropic

client = Anthropic()

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain a token in one sentence."}],
)
print(msg.content[0].text)
```

Keep your API key in an environment variable (`ANTHROPIC_API_KEY`) — never hard-code it.

## Your task

Paste a sentence into a tokenizer tool and count the tokens. Then make the basic Claude call above and read the response.
