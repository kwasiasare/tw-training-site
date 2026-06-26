---
course: mlops-engineer
title: 'Capstone: Build and Operate a Production LLM Serving System'
month: 5
monthTitle: LLMOps & GPU Serving
lesson: 5
summary: This capstone ties the whole LLMOps module together into one deployed system. You'll serve an
  open LLM with vLLM, optimize it with quantization, scale it on Kubernetes with KServe and GPU-aware
  scheduling, observe it with token- and latency-aware telemetry, gate every change with an evaluation
  suite, guard it with safety rails, and operate it inside an explicit cost budget — a portfolio-ready
  demonstration of end-to-end LLM serving ownership.
objectives:
- Architect a production LLM serving system that connects serving, optimization, scaling, observability,
  evaluation, and cost control
- Serve a quantized open model with vLLM behind an OpenAI-compatible API and define latency/throughput SLOs
- Deploy and autoscale the endpoint on Kubernetes with KServe, GPU scheduling, and scale-to-zero
- Instrument token-, latency-, and cost-aware observability and gate deploys with an offline eval suite
- Add guardrails and operate the system within a cost budget, then document it for a portfolio
video: mlo-m5-l05-capstone-production-llm-serving-system.mp4
quiz:
- q: Which metric pair best captures interactive LLM latency for your SLOs?
  options:
  - Disk IOPS and CPU temperature
  - TTFT (time to first token) and TPOT (time per output token)
  - Image pull time and pod count
  - Model file size and host RAM
  answer: 1
  why: TTFT measures responsiveness (prefill and queue time) and TPOT measures streaming speed (the decode
    loop); together they define the interactive latency SLOs for an LLM endpoint.
- q: What should the evaluation gate do before a new model or prompt is promoted in the capstone?
  options:
  - Automatically promote it to save time
  - Run an offline eval/regression suite (e.g., RAGAS plus LLM-as-judge) and block promotion if quality
    regresses against the baseline
  - Only check that the container builds
  - Increase the GPU memory utilization
  answer: 1
  why: The gate runs the eval suite and blocks promotion when quality regresses, preventing silent quality
    drops — the LLM analogue of the classic model-metric promotion gate from Module 4.
- q: Which KServe setting lets an idle LLM endpoint cost nothing when there is no traffic?
  options:
  - maxReplicas set very high
  - minReplicas; 0, enabling scale-to-zero via Knative
  - A physically larger GPU
  - Disabling the readiness probe
  answer: 1
  why: minReplicas of 0 lets KServe/Knative scale the deployment to zero pods when idle, eliminating GPU
    cost during no-traffic periods, at the cost of a cold start on the next request.
- q: You must serve a 70B model that does not fit on a single GPU. What is the right approach?
  options:
  - Lower the sampling temperature
  - Shard it across GPUs with tensor (and optionally pipeline) parallelism, e.g., KServe workerSpec or
    vLLM --tensor-parallel-size
  - Reduce max_tokens
  - Move inference to the CPU
  answer: 1
  why: A model larger than one GPU's memory must be split across GPUs with tensor and optionally pipeline
    parallelism; KServe's workerSpec or vLLM's --tensor-parallel-size configures this.
- q: Name two cost levers from this module you would combine to keep a production LLM endpoint within budget.
  answer: Any two of — continuous batching, weight or KV-cache quantization, prompt/KV caching, autoscaling
    with scale-to-zero, and spot/preemptible GPUs.
  why: These levers stack across the model, system, and application layers; combining several (for example
    quantization plus continuous batching plus scale-to-zero) can cut inference cost well over half.
- q: Besides latency and error rate, name one LLM-specific signal your capstone dashboard must track.
  answer: Token usage / cost-per-1k-tokens (also acceptable; TTFT, TPOT, GPU or KV-cache utilization, or
    an eval/faithfulness score).
  why: LLM endpoints add token-economics and decode-latency signals that classic infra dashboards miss but
    that directly drive both user experience and spend.
resources:
- label: vLLM Documentation
  url: https://docs.vllm.ai/en/latest/
- label: KServe — Generative Inference (Multi-node / LLM serving)
  url: https://kserve.github.io/website/docs/model-serving/generative-inference/multi-node
- label: Ragas — LLM Evaluation
  url: https://docs.ragas.io/
- label: OpenTelemetry — GenAI Semantic Conventions
  url: https://opentelemetry.io/docs/specs/semconv/gen-ai/
---

## Capstone Overview

This is the integration lesson for the LLMOps module. The individual pieces from Lessons 1–4 — efficient serving with vLLM, quantization and compiled runtimes, Kubernetes/KServe scaling, and production observability/evaluation/cost — come together into a single deployed system. The goal is not a new tool but to demonstrate **end-to-end ownership** of an LLM in production: from a model checkpoint to a monitored, evaluated, cost-bounded endpoint that can be safely updated.

It extends the Module 4 capstone (an end-to-end classic-ML system) to large language models. Treat it as a portfolio project: hiring managers want to see that you can connect serving, scaling, observability, evaluation, and cost trade-offs — and operate the result after deployment.

## Reference Architecture

A production LLM serving system has five planes that mirror the module:

1. **Serving runtime** — an open model served by **vLLM** (PagedAttention + continuous batching) behind an OpenAI-compatible API.
2. **Optimization** — a **quantized** checkpoint (e.g., AWQ/FP8) and, where latency is critical, a compiled runtime (Triton + TensorRT-LLM).
3. **Scaling plane** — **Kubernetes + KServe** with GPU-aware scheduling, request-based autoscaling, scale-to-zero, and tensor/pipeline parallelism for large models.
4. **Observability & evaluation** — token-, latency-, and cost-aware telemetry (OpenTelemetry GenAI + Prometheus/Grafana) plus an offline **eval suite** that gates every change.
5. **Governance** — guardrails, drift monitoring, and an explicit **cost budget** with alerting.

The planes connect through artifacts: the model/quantized checkpoint, the container image and KServe `InferenceService`, the dashboards, and the eval report that gates promotion.

## Step 1 — Scope and SLOs

Pick a realistic use case (a support assistant, a RAG Q&A service, a summarizer). Define:

- The model and task, and a **quality bar** measured by your eval suite (e.g., RAGAS faithfulness ≥ target, no regression vs. baseline).
- **Latency SLOs** in LLM terms: p95 **TTFT** (e.g., < 1s) and p95 **TPOT** (e.g., < 100ms), plus a throughput target in tokens/sec.
- A **cost budget**: a target `cost_per_1k_tokens` and a monthly ceiling.
- "Production-ready" means: endpoint live and autoscaling, dashboards showing token/latency/cost, eval gate wired into CI, guardrails active, and alerts configured.

## Step 2 — Serve with vLLM

Serve a quantized open model behind the OpenAI-compatible server. Quantization (Lesson 2) shrinks memory and raises throughput; validate quality loss before committing to it.

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --quantization awq \
  --kv-cache-dtype fp8 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.90
# OpenAI-compatible endpoints on :8000 — /v1/chat/completions, /metrics
```

Expose `/health` (liveness) and `/ready` (readiness) so the orchestrator only routes traffic once weights are loaded — the same probe convention used throughout Modules 3–5.

## Step 3 — Deploy and Scale on KServe

Wrap the runtime in a KServe `InferenceService`. Use `minReplicas: 0` for scale-to-zero on idle, autoscale on request concurrency, and shard large models with a `workerSpec`.

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llm-capstone
spec:
  predictor:
    minReplicas: 0          # scale-to-zero when idle
    maxReplicas: 8
    scaleMetric: concurrency
    scaleTarget: 10
    model:
      modelFormat:
        name: huggingface
      storageUri: hf://meta-llama/Llama-3.1-8B-Instruct
      resources:
        limits:
          nvidia.com/gpu: "1"   # GPUs only in limits; request == limit
```

For a model that does not fit one GPU, add a `workerSpec` (sibling of `model`) with `tensorParallelSize`/`pipelineParallelSize`, and schedule onto GPU nodes with taints/tolerations and `nvidia.com/gpu.product` affinity.

## Step 4 — Observability

Instrument the system with the **OpenTelemetry GenAI** conventions (`gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.request.model`) and scrape vLLM's Prometheus metrics. Build a Grafana board with the LLM-specific signals next to classic latency/error/throughput.

```promql
# p95 TTFT and inter-token latency (TPOT)
histogram_quantile(0.95, sum(rate(vllm:time_to_first_token_seconds_bucket[5m])) by (le))
histogram_quantile(0.95, sum(rate(vllm:inter_token_latency_seconds_bucket[5m])) by (le))
# output throughput (tokens/sec)
sum(rate(vllm:generation_tokens_total[1m]))
```

Trace requests end-to-end into an LLM observability tool (Langfuse or Phoenix, both OTLP-native) so you can inspect prompts, token counts, and per-request cost.

## Step 5 — The Evaluation Gate

This is what makes the system safe to change. Maintain a versioned offline eval set and run it in CI on every model or prompt change. Promote only if quality holds against the baseline.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

result = evaluate(eval_dataset, metrics=[faithfulness, answer_relevancy])
if result["faithfulness"] < BASELINE["faithfulness"]:
    raise SystemExit("Eval regression — blocking promotion")
```

Combine deterministic checks with **LLM-as-judge** scoring for open-ended quality, and treat the eval report as the promotion artifact — the LLM analogue of Module 4's model-metric gate.

## Step 6 — Guardrails and Drift

Add input/output **guardrails** (e.g., NeMo Guardrails, or Llama Guard as a safety classifier) to block prompt injection, unsafe content, and PII leakage. Monitor **prompt/response drift** (embedding-distribution shift, refusal rate, output-length spikes) to catch silent degradation without ground-truth labels.

## Step 7 — Operate Within a Cost Budget

Treat cost as an SLO. Track `cost_per_1k_tokens` as a Grafana panel and alert when it breaches budget, just like latency. Pull the stacked levers from the module: continuous batching, quantization, prompt/KV caching, autoscaling with scale-to-zero, and spot/preemptible GPUs. Document the before/after cost so the trade-offs are explicit.

## Step 8 — Document for Your Portfolio

A strong README includes: the architecture diagram, how to deploy (ideally one command), the SLOs and whether they were met, dashboard screenshots (TTFT, TPOT, tokens, cost), the eval report gating deploys, and a trade-offs/"what I'd improve" section. Reproducibility is what separates a great capstone from an average one.

## Common Pitfalls

- Optimizing for throughput while blowing the **TTFT** SLO — interactive UX needs both tracked.
- Quantizing without an eval check, shipping a quietly worse model.
- No evaluation gate, so a prompt tweak silently regresses quality.
- Forgetting `minReplicas: 0`, paying for idle GPUs around the clock.
- Dashboards that track only infra metrics and ignore tokens, cost, and decode latency.
- Guardrails bolted on after launch instead of designed in.
