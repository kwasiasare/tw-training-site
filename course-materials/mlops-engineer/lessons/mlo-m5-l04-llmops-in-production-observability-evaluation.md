---
course: mlops-engineer
title: 'LLMOps in Production: Observability, Evaluation, and Cost'
month: 5
monthTitle: LLMOps & GPU Serving
lesson: 4
summary: This final lesson closes the loop on running LLMs in production. You'll learn the observability
  signals unique to LLM serving (latency decomposition into TTFT and TPOT, throughput, token usage, GPU
  metrics, and cost-per-token), how to trace requests with the OpenTelemetry GenAI conventions and a tool
  like Langfuse or Phoenix, how to evaluate quality with offline eval sets, LLM-as-judge, and RAG metrics,
  and how to model and cut cost using the batching, quantization, caching, and autoscaling levers from
  earlier in the module.
objectives:
- Decompose LLM latency into TTFT and TPOT and explain how token, throughput, and GPU metrics differ from
  the classic model monitoring of Module 4
- Instrument an LLM service with the OpenTelemetry GenAI semantic conventions and visualize traces in an
  LLM observability tool such as Langfuse or Arize Phoenix
- Build an evaluation strategy using offline eval datasets, LLM-as-judge regression suites, and RAG metrics
  with RAGAS
- Apply guardrails and prompt/response drift monitoring to keep a production LLM safe and on-distribution
- Model cost-per-token and combine batching, quantization, caching, autoscaling, and spot GPUs to hit a
  cost budget
video: mlo-m5-l04-llmops-in-production-observability-evaluation.mp4
quiz:
- q: In LLM serving, which metric measures inter-token latency during the decode phase — the model's "typing
    speed" after the first token has been produced?
  options:
  - Time to First Token (TTFT)
  - Time Per Output Token (TPOT)
  - Tokens-per-second throughput
  - End-to-end request latency
  answer: 1
  why: TPOT (also called inter-token latency) is the average time between successive output tokens during
    decode. TTFT measures the wait for the first token (prefill); throughput aggregates across requests.
- q: Which observability signal is specific to LLM serving and was NOT part of the classic model monitoring
    (latency, errors, throughput, drift) taught in Module 4?
  options:
  - Request error rate
  - p95 latency
  - Token usage and cost-per-token
  - Requests per second
  answer: 2
  why: Token counts (input/output) and the cost-per-1K-tokens derived from them are unique to generative
    models. Latency, errors, and throughput are shared operational signals already covered in Module 4.
- q: Following the OpenTelemetry GenAI semantic conventions, which attribute name records the number of
    output tokens a model generated?
  options:
  - llm.tokens.out
  - gen_ai.usage.output_tokens
  - response.token_count
  - openai.completion_tokens
  answer: 1
  why: The GenAI semconv standardizes names like gen_ai.request.model, gen_ai.usage.input_tokens, and
    gen_ai.usage.output_tokens so spans look identical across providers and frameworks.
- q: In RAGAS, what does the "faithfulness" metric measure?
  options:
  - Whether the answer is grounded in the retrieved context with no hallucinated claims
  - How quickly the retriever returns documents
  - Whether the model weights are correctly quantized
  - How fully the GPU is utilized during decode
  answer: 0
  why: Faithfulness (groundedness) breaks the answer into atomic claims and checks each against the retrieved
    context using an LLM judge; it is the primary defense against hallucination in RAG.
- q: Name one cost-optimization lever from earlier in this module and explain in one line why it lowers
    cost-per-token.
  answer: Continuous batching (it keeps the GPU saturated by inserting new requests as others finish, raising
    tokens/sec so the fixed GPU-hour cost is spread over far more tokens). Quantization, prefix/KV caching,
    autoscaling/scale-to-zero, and spot GPUs are also valid.
  why: Cost-per-token = GPU-hour price / tokens produced per hour. Levers either raise the denominator
    (batching, caching, quantization throughput) or cut the numerator (spot GPUs, scale-to-zero idle time).
- q: What is prompt/response drift, and why is it worth monitoring even before you have ground-truth labels
    or eval results?
  answer: It is a shift over time in the distribution of incoming prompts (input drift) or model outputs
    (response drift) relative to a reference window. It is an early, label-free warning that usage patterns
    or output quality are changing, letting you re-run evals or add guardrails before users are harmed.
  why: Like prediction drift in Module 4, it needs no labels — you compare distributions (embeddings, length,
    topic, refusal rate) against a baseline, giving a leading indicator of regressions.
resources:
- label: OpenTelemetry — GenAI Semantic Conventions
  url: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- label: Langfuse — LLM Observability Documentation
  url: https://langfuse.com/docs
- label: Ragas — RAG & LLM Evaluation Documentation
  url: https://docs.ragas.io/
- label: NVIDIA NeMo Guardrails Documentation
  url: https://docs.nvidia.com/nemo/guardrails/latest/about/overview.html
---

## Closing the Loop on Production LLMs

Across this module you stood up an LLM serving stack: high-throughput inference with vLLM (Lesson 1), quantization and compiled engines with Triton and TensorRT-LLM (Lesson 2), and elastic scaling on Kubernetes with KServe (Lesson 3). A serving system that is fast and scalable is still only half of LLMOps. This lesson adds the operational half: **observing** what the system does, **evaluating** whether its answers are good, keeping it **safe**, and running it inside a **cost budget**.

The classic monitoring from Module 4 — latency, errors, throughput, and PSI/KS drift — still applies. But LLMs add signals that a churn classifier never had: token usage, two-phase latency, GPU memory pressure, generation quality, and a per-request dollar cost. LLMOps is classic MLOps plus these new dimensions.

## LLM-Specific Observability

A single LLM request has **two latency phases**, so a single end-to-end number hides the real behavior:

- **TTFT (Time To First Token)** — the wait before the first token streams out. It is dominated by the *prefill* of the prompt (plus scheduler queueing). Long prompts and cold caches inflate it. For interactive UX, aim for p99 TTFT under ~1s.
- **TPOT (Time Per Output Token)** — the inter-token latency during *decode*, i.e. the model's typing speed. A common interactive target is p99 TPOT under ~100ms. Total latency ≈ `TTFT + TPOT × output_tokens`.

Throughput and usage metrics complete the picture:

- **Throughput**: aggregate **tokens/sec** across all in-flight requests, plus requests/sec. Continuous batching trades a little per-request latency for large throughput gains.
- **Token usage**: input and output tokens per request — the raw driver of both cost and decode latency.
- **GPU metrics**: utilization, memory used vs. total, and KV-cache occupancy. LLM serving is usually **memory-bound**; a full KV cache forces preemption and tanks throughput.
- **Cost-per-token**: derived from GPU-hour price and tokens/sec (see the cost section).

vLLM exposes these on a Prometheus `/metrics` endpoint, so the Prometheus + Grafana stack from Module 4 carries straight over — you are just scraping different series.

```promql
# p95 TTFT from the vLLM histogram
histogram_quantile(0.95, sum(rate(vllm:time_to_first_token_seconds_bucket[5m])) by (le))

# p95 inter-token latency (TPOT)
histogram_quantile(0.95, sum(rate(vllm:inter_token_latency_seconds_bucket[5m])) by (le))

# output token throughput (tokens/sec)
sum(rate(vllm:generation_tokens_total[1m]))
```

**How this differs from Module 4.** There you watched a fixed-shape prediction (a score or class) and computed PSI/KS on tabular features. Here the output is open-ended text, latency is two-phase, the bottleneck is GPU memory, and every request has a token-denominated cost. The *discipline* (expose metrics, scrape, alert, act) is identical; the *signals* are new.

## Tracing with OpenTelemetry GenAI Conventions

Metrics tell you *that* something is slow or expensive; **traces** tell you *why* — which prompt, which tool call, which retrieval step. The **OpenTelemetry GenAI semantic conventions** standardize how LLM spans are named so a trace looks the same whether it came from vLLM, LangChain, or a raw provider SDK. Standard attributes include:

- `gen_ai.request.model`, `gen_ai.request.temperature`, `gen_ai.request.max_tokens`
- `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`
- `gen_ai.response.finish_reasons`

As of mid-2026 most of these conventions are still marked **experimental** in the spec, but vendor and tool support is already broad. Capture a span per LLM call and attach the standard attributes:

```python
from opentelemetry import trace

tracer = trace.get_tracer("llm-service")

with tracer.start_as_current_span("chat") as span:
    span.set_attribute("gen_ai.request.model", "llama-3.1-8b-instruct")
    resp = client.chat.completions.create(model=..., messages=msgs)
    span.set_attribute("gen_ai.usage.input_tokens", resp.usage.prompt_tokens)
    span.set_attribute("gen_ai.usage.output_tokens", resp.usage.completion_tokens)
```

Point those traces at an **LLM observability tool**. Both leading open-source options are OTLP-native:

- **Langfuse** — open-source platform for tracing, prompt management, evals, and analytics; it can act as an OTLP backend at `/api/public/otel` and aims to follow the GenAI semconv. (Note: Langfuse was acquired by ClickHouse in January 2026 — validate hosting/licensing for your org.)
- **Arize Phoenix** — open-source observability and eval platform built on OpenTelemetry and **OpenInference** instrumentation; ships `phoenix.evals` and runs standalone (`phoenix serve`, ports 6006/4317).

## Evaluation: Is the Output Actually Good?

A model can be fast, cheap, and confidently wrong. **Evaluation** is the LLM analogue of model-quality monitoring — but generation has no single ground-truth label, so you combine methods:

- **Offline eval datasets**: a curated, version-controlled set of representative inputs with expected behavior. Run them in CI as a **regression suite** so a prompt tweak or model swap can't silently regress quality.
- **LLM-as-judge**: use a strong model to grade outputs against a rubric (correctness, helpfulness, tone) at scale where human review can't reach. Pin the judge model and prompt so scores are comparable over time; periodically calibrate against human labels.
- **RAG evaluation with RAGAS**: for retrieval-augmented systems, score retrieval (context precision/recall) and generation (faithfulness, answer relevancy). **Faithfulness** is the primary hallucination guard — it splits the answer into atomic claims and checks each against the retrieved context using an LLM judge.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

result = evaluate(
    dataset,  # question, answer, contexts, (optional) ground_truth
    metrics=[faithfulness, answer_relevancy, context_precision],
)
print(result)  # gate the deploy: fail CI if faithfulness < 0.85
```

Wire eval scores into the same promotion-gate pattern from the capstone: a new model or prompt ships only if it beats the production baseline on your eval suite.

## Guardrails, Safety, and Drift

Evaluation catches quality regressions offline; **guardrails** enforce safety online, on every request:

- **Input rails** screen prompts for jailbreaks and injection; **output rails** block unsafe or off-policy responses; **retrieval rails** filter RAG chunks.
- **NeMo Guardrails** (NVIDIA, Apache-2.0) is a programmable toolkit using the *Colang* language to model conversation flows and rails. **Llama Guard** is a dedicated content-safety classifier (input and output moderation). Production systems layer them — classifier plus programmable rails plus deterministic pattern checks — as defense in depth.

**Prompt/response drift** is the LLM version of the prediction drift from Module 4: compare the distribution of incoming prompts (length, topic, embedding clusters) and outputs (length, refusal rate, sentiment) against a reference window. Because it needs no labels, it is an **early warning** that usage has shifted or quality is slipping — a trigger to re-run evals or tighten guardrails before users feel it.

## Cost Modeling and Optimization

LLM inference is expensive enough that **cost is a first-class SLO**. Model it per token:

```
cost_per_1k_tokens = (GPU_hourly_price / tokens_per_second / 3600) * 1000
```

The denominator (throughput) and numerator (GPU price and idle time) are exactly what the earlier lessons gave you levers for:

- **Continuous batching** (Lesson 1) keeps the GPU saturated, lifting tokens/sec 2–3x+ over static batching — the single biggest win.
- **Quantization** (INT8/INT4/FP8, Lesson 2) shrinks the model and KV cache, fitting larger batches and cutting cost roughly in half while keeping ~95–99% of accuracy.
- **Prompt/prefix and KV caching** skip recomputing shared context (system prompts, RAG preambles), cutting prefill cost and TTFT.
- **Autoscaling and scale-to-zero** (Lesson 3, KServe) remove idle GPU spend for spiky or low-traffic endpoints.
- **Spot/preemptible GPUs** cut the hourly price for batch or interruption-tolerant workloads.

Stacking these across model, system, and application layers can cut inference cost by well over half. Track `cost_per_1k_tokens` as a Grafana panel next to TTFT and faithfulness, and **alert when it breaches budget** just like latency or error rate.

## Tie-In: Extending the Capstone to LLMs

This module extends the Module 4 capstone — your end-to-end MLOps system — to large language models. As an advanced project, take that same discipline and stand up a **production LLM serving system**: a vLLM (or Triton/TensorRT-LLM) backend, served and autoscaled on Kubernetes/KServe, **observed** with OpenTelemetry GenAI traces and Prometheus/Grafana dashboards (TTFT, TPOT, throughput, GPU, cost-per-token), **evaluated** by an offline RAGAS/LLM-as-judge regression suite gating each deploy, **guarded** by input/output rails, and run inside an explicit **cost budget** with batching, quantization, caching, and scale-to-zero. The MLOps discipline you learned for classic models — reproducible, monitored, gated, and operable — now extends end-to-end to LLMs.

## Key Takeaways

- LLM observability adds TTFT/TPOT latency decomposition, token usage, GPU/KV-cache pressure, and cost-per-token on top of the classic latency/error/throughput/drift signals.
- Trace with the OpenTelemetry GenAI conventions and visualize in Langfuse or Phoenix (both OTLP-native, open-source).
- Evaluate with versioned offline sets, LLM-as-judge regression suites, and RAGAS (faithfulness first) — and gate deploys on the results.
- Add guardrails (NeMo Guardrails, Llama Guard) and label-free prompt/response drift monitoring for safety and early warning.
- Treat cost as an SLO: model cost-per-token and pull the batching, quantization, caching, autoscaling, and spot-GPU levers to stay on budget.
