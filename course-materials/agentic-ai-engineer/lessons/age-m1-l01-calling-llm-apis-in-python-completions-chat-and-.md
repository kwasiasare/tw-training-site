---
course: agentic-ai-engineer
title: 'Calling LLM APIs in Python: Completions, Chat, and Structured Output'
month: 1
monthTitle: LLM Foundations and Tool-Using Agents
lesson: 1
summary: A hands-on lesson on calling LLM APIs from Python. You'll set up a clean environment, make your
  first chat completion request, understand the difference between legacy completions and the chat API,
  and learn to force reliable, schema-validated JSON output using structured output and Pydantic.
objectives:
- Set up a Python environment with API keys managed securely via environment variables
- Distinguish between legacy text completions and the modern chat completions API
- Make chat completion requests and control behavior with parameters like temperature and max_tokens
- Generate structured JSON output and validate it against a schema using Pydantic
- Implement basic error handling and retries for robust production calls
video: age-m1-l01-calling-llm-apis-in-python-completions-chat-and-.mp4
quiz:
- q: Which API should you use for modern instruction-tuned models?
  options:
  - The legacy completions API
  - The chat completions API
  - The embeddings API
  - The fine-tuning API
  answer: 1
  why: The chat completions API uses role-based messages and is the standard for modern models; legacy
    completions is largely deprecated.
- q: What is the best way to store your API key?
  options:
  - Hard-coded in the script
  - In a .env file loaded as an environment variable
  - In a public GitHub repo
  - Passed as a command-line argument every time
  answer: 1
  why: Storing keys in a gitignored .env file and loading them as environment variables keeps secrets
    out of source code.
- q: What does passing a Pydantic model as response_format give you?
  options:
  - A raw text string
  - Valid JSON syntax but an unknown shape
  - An already-validated Python object matching your schema
  - Faster inference
  answer: 2
  why: Schema-enforced structured output returns a parsed, validated instance of your model with exactly
    the fields you defined.
- q: Which temperature setting is most appropriate for reliable structured output?
  options:
  - A low value near 0
  - A high value near 2
  - It has no effect on structure
  - Always exactly 1.0
  answer: 0
  why: Low temperature makes output more deterministic and consistent, which is preferable for structured,
    parseable tasks.
- q: Name the strategy you should wrap API calls in to handle rate limits and transient failures.
  answer: Exponential backoff with retries
  why: Retrying with exponentially increasing wait times handles rate limits and transient errors gracefully
    before failing loudly.
- q: What does Pydantic's model_validate_json raise when data does not match the schema?
  answer: ValidationError
  why: It raises a ValidationError, which you can catch to retry or repair instead of letting bad data
    flow downstream silently.
resources:
- label: OpenAI Python SDK documentation
  url: https://github.com/openai/openai-python
- label: OpenAI Structured Outputs guide
  url: https://platform.openai.com/docs/guides/structured-outputs
- label: Pydantic documentation
  url: https://docs.pydantic.dev/latest/
- label: python-dotenv documentation
  url: https://pypi.org/project/python-dotenv/
---

## Why API calls are the foundation of agents

Every LLM agent, no matter how sophisticated, ultimately rests on one operation: sending a request to a model and parsing its response. Before you build tool-using loops or multi-agent systems, you must be able to call an LLM reliably and get back data your code can trust. This lesson focuses on that primitive.

## Setting up your environment

Isolate dependencies in a virtual environment and never hard-code secrets.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install openai pydantic python-dotenv
```

Store your key in a `.env` file (and add `.env` to `.gitignore`):

```
OPENAI_API_KEY=sk-...
```

Load it in Python:

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()  # reads OPENAI_API_KEY from the environment
```

## Completions vs. chat

The **legacy completions** API takes a single text prompt and returns a continuation. It is largely deprecated. The **chat completions** API takes a list of messages with roles (`system`, `user`, `assistant`) and is the standard for modern instruction-tuned models. Always prefer chat.

```python
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Name three uses of vector databases."},
    ],
    temperature=0.2,
)
print(resp.choices[0].message.content)
```

### Key parameters
- **model**: which model to call.
- **messages**: the conversation history; the `system` message sets behavior.
- **temperature**: 0 = deterministic, higher = more creative. Use low values for structured tasks.
- **max_tokens**: cap on the response length.

## Getting reliable structured output

Free-form text is hard for code to consume. For agents you usually want JSON. Three escalating techniques:

1. **Prompt for JSON** — ask the model to reply in JSON. Cheap but unreliable.
2. **JSON mode** — pass `response_format={"type": "json_object"}` to guarantee valid JSON syntax (but not a specific shape).
3. **Schema-enforced structured output** — supply a JSON schema (or a Pydantic model) so the model conforms to your exact fields.

```python
from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    year: int
    genres: list[str]

resp = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Give details for the film Inception."}],
    response_format=Movie,
)
movie = resp.choices[0].message.parsed  # already a validated Movie instance
print(movie.year)  # 2010
```

## Validating output yourself

Even when you only get a JSON string, validate before trusting it. Pydantic turns malformed data into a catchable error instead of a silent bug downstream.

```python
import json
from pydantic import ValidationError

try:
    data = Movie.model_validate_json(raw_json_string)
except ValidationError as e:
    # log, retry, or repair
    print(e)
```

## Error handling and retries

Network calls fail. Wrap requests to handle rate limits and transient errors with exponential backoff.

```python
import time
from openai import RateLimitError, APIError

def call_with_retry(**kwargs):
    for attempt in range(5):
        try:
            return client.chat.completions.create(**kwargs)
        except (RateLimitError, APIError):
            time.sleep(2 ** attempt)
    raise RuntimeError("LLM call failed after retries")
```

## Putting it together

A production-grade call: load secrets from env, use the chat API with a low temperature, request schema-validated output, wrap in retry logic, and validate the parsed object before using it. This pattern is the reliable building block every agent in later lessons depends on.
