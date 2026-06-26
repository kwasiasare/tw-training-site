---
course: data-scientist
title: 'Calling LLM APIs from Python: The LLM as a Data Science Tool'
month: 5
monthTitle: Generative AI and LLM Foundations for Data Scientists
lesson: 1
summary: Learn to treat a large language model as another tool in your data science toolkit, called from
  Python with a few lines of code. This lesson covers the Messages API, steering output with system prompts
  and parameters, getting reliable structured (JSON) output, and choosing models by cost so you can add
  unstructured-text capabilities to workflows that classical ML handles poorly.
objectives:
- Explain where LLMs complement tabular models by handling unstructured text and few-shot tasks
- Call an LLM from Python using the Anthropic Messages API and read the response
- Steer output deterministically with system prompts, temperature, max_tokens, and stop sequences
- Produce structured JSON output and parse it safely without ever calling eval()
- Select a model by matching task difficulty and token cost to a cheap or frontier model
- Identify the points in a data science workflow where an LLM adds the most value
video: dsc-m5-l01-calling-llm-apis-from-python.mp4
quiz:
- q: You have 50,000 free-text customer reviews and almost no labels. Which approach fits an LLM best?
  options:
  - Train a logistic regression from scratch on the raw text
  - Compute the mean review length and threshold it
  - Use a few-shot LLM prompt to classify sentiment without labeled training data
  - Drop the reviews because there are no labels
  answer: 2
  why: LLMs excel at unstructured text and few-shot tasks where classical ML would need a large labeled
    training set. A few-shot prompt classifies each review with no model training required.
- q: In the Anthropic Messages API, how do you read the model's generated text from the response object
    `msg`?
  options:
  - msg.content[0].text
  - msg.choices[0].message.content
  - msg.text
  - msg.output
  answer: 0
  why: 'The Messages API returns a list of content blocks. The generated text is in the first block''s
    .text attribute: msg.content[0].text.'
- q: Which parameter should you set to make an extraction task as deterministic and repeatable as possible?
  options:
  - A high temperature like 1.0
  - A longer system prompt only
  - A larger max_tokens
  - A low temperature like 0.0
  answer: 3
  why: Temperature controls randomness. A low temperature (near 0.0) makes the model pick the most likely
    tokens, giving stable, repeatable output that is ideal for extraction and classification.
- q: After prompting a model to return JSON, what is the safe way to turn its text output into a Python
    object?
  options:
  - eval(text) so any Python literal is accepted
  - json.loads(text) inside a try/except, then validate the shape
  - Assume it is already a dict and index into it
  - Use a regex to pull out values one by one
  answer: 1
  why: Model output is untrusted text, so never use eval(). Parse with json.loads() inside try/except
    to handle malformed JSON, then validate that the expected keys and types are present. Tool use / structured
    outputs give a stronger guarantee.
- q: You must classify millions of short, simple snippets cheaply. Which model choice is most appropriate?
  options:
  - Always use the largest frontier model for every call
  - Avoid LLMs entirely because volume is high
  - Use a small, cheap model like claude-haiku-4-5 for the bulk simple work
  - Pick a model at random per request
  answer: 2
  why: Cost scales with tokens, so match the model to the task. A small, cheap model such as claude-haiku-4-5
    handles high-volume simple classification economically; reserve a frontier model for genuinely hard
    reasoning.
- q: In one or two sentences, explain why an LLM complements rather than replaces a tabular model like
    gradient boosting in a churn-prediction pipeline.
  answer: A tabular model is best for structured numeric and categorical features (usage counts, tenure,
    plan), where it is accurate, cheap, and interpretable. An LLM complements it by turning unstructured
    inputs the tabular model cannot use, such as free-text support tickets, into features or labels; you
    use each tool where it is strongest rather than swapping one for the other.
  why: 'The key idea is fit-for-purpose: tabular models own structured features and LLMs own unstructured
    text. Combining them beats forcing either to do the other''s job.'
resources:
- label: Anthropic Messages API Documentation
  url: https://docs.claude.com/en/api/messages
- label: Anthropic Python SDK (anthropics/anthropic-sdk-python)
  url: https://github.com/anthropics/anthropic-sdk-python
- label: Anthropic Prompt Engineering Overview
  url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- label: Anthropic Tool Use (Structured Outputs)
  url: https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
---

## Why LLMs Matter for a Data Scientist

Most of your work is **structured** data: rows and columns of numbers and categories, modeled with regression, gradient boosting, or clustering. Those tools are accurate, cheap, and interpretable, and nothing here replaces them. But a large fraction of real-world signal lives in **unstructured text** — support tickets, reviews, emails, notes. Classical ML struggles here unless you have a large, labeled training set.

A large language model (LLM) fills exactly this gap:

- **Unstructured text** — it reads and reasons over free text directly.
- **Few-shot tasks** — it generalizes from a handful of in-prompt examples, with no model training.
- **Generation** — it writes summaries, rewrites, and explanations on demand.

Think of the LLM as a function you call from Python: text in, text out. It **complements** your tabular models — use gradient boosting on the numeric features, and an LLM to convert messy text into features or labels those models can consume.

## The Messages API: The Canonical Call

Every interaction is a single call to the Messages API. Install the SDK (`pip install anthropic`), set `ANTHROPIC_API_KEY` in your environment, and call `client.messages.create`. The same patterns apply to other providers, but we keep the examples concrete with the Anthropic SDK.

```python
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

msg = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    system="You are a precise data-labeling assistant.",
    messages=[{"role": "user", "content": "Classify the sentiment of: 'The app keeps crashing.'"}],
)

text = msg.content[0].text
print(text)
```

The response is a list of content blocks; the generated text lives in `msg.content[0].text`. The `messages` list is the conversation — each item has a `role` (`user` or `assistant`) and `content`.

## Steering the Output

A raw call gives you the model's default behavior. Four levers tighten it for data work:

- **`system`** — sets the persona and rules ("Reply with only one word: positive, negative, or neutral.").
- **`temperature`** — controls randomness from `0.0` (deterministic, best for extraction/classification) to `1.0` (creative).
- **`max_tokens`** — caps output length; keep it small for short labels to save cost and time.
- **`stop_sequences`** — strings that halt generation early once produced.

```python
msg = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=10,
    temperature=0.0,
    system="Reply with exactly one word: positive, negative, or neutral.",
    messages=[{"role": "user", "content": "I love the new dashboard."}],
)
print(msg.content[0].text.strip())  # -> positive
```

Low temperature plus a strict system prompt turns the LLM into a stable, repeatable labeling function.

## Structured (JSON) Output

For a pipeline you need machine-readable output, not prose. Instruct the model to return JSON, then **parse it safely**. Never call `eval()` on model output — it is untrusted text and `eval` would execute arbitrary code.

```python
import json

msg = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=256,
    temperature=0.0,
    system="Extract fields and return ONLY valid JSON with keys: sentiment, urgency (1-5).",
    messages=[{"role": "user", "content": "My subscription was charged twice and support won't reply!"}],
)

raw = msg.content[0].text
try:
    data = json.loads(raw)
    assert "sentiment" in data and "urgency" in data  # validate the shape
except (json.JSONDecodeError, AssertionError):
    data = None  # handle the bad response: retry, log, or skip

print(data)
```

Prompting-for-JSON works, but the model can still drift. For a stronger guarantee, use **tool use / structured outputs**, where you declare a JSON schema and the API enforces it — the model's response is constrained to match your shape, removing most parse failures.

## Model Selection and Cost

You pay per **token** (input and output), so cost scales with how much text flows through. Match the model to the task:

- **Cheap, small model** (e.g. `claude-haiku-4-5`) for high-volume, simple work: bulk classification, short extraction, tagging.
- **Frontier model** (e.g. `claude-opus-4-8`) for genuinely hard reasoning: multi-step analysis, nuanced judgment, tricky edge cases.

Never hard-pin one model as "the" model. Profile a sample, see which tier meets your quality bar, and route accordingly.

```python
def classify(text, hard=False):
    model = "claude-opus-4-8" if hard else "claude-haiku-4-5"
    msg = client.messages.create(
        model=model,
        max_tokens=20,
        temperature=0.0,
        system="Reply with one label: bug, billing, feature, or other.",
        messages=[{"role": "user", "content": text}],
    )
    return msg.content[0].text.strip()
```

Running the cheap model on the easy 95% and escalating only the hard cases is a common, large cost saving.

## Where LLMs Fit in a DS Workflow

LLMs slot into stages where text dominates:

- **Data prep** — clean, normalize, and de-duplicate messy free-text fields.
- **Feature engineering** — turn text into structured columns (sentiment, topic, urgency) that feed a tabular model.
- **Labeling** — produce few-shot labels to bootstrap a supervised dataset, then train a cheap classical model on them.
- **Communication** — draft summaries and plain-language explanations of results for stakeholders.

The LLM is one tool among many. The skill is knowing when text-shaped problems call for it and when a tabular model is still the right answer.
