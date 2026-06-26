---
course: mlops-engineer
title: Serving LLMs Efficiently with vLLM
month: 5
monthTitle: LLMOps & GPU Serving
lesson: 1
summary: Serving large language models is fundamentally different from serving the classic models in earlier
  modules. This lesson explains why LLM inference is memory-bound and autoregressive, how the KV cache
  dominates GPU memory, and how vLLM uses PagedAttention and continuous batching to serve many requests
  efficiently. You will launch an OpenAI-compatible vLLM server, call it, tune key flags, and reason about
  throughput-versus-latency trade-offs.
objectives:
- Explain why LLM inference is memory-bound and autoregressive and how it differs from serving classic
  ML models
- Describe how the KV cache dominates GPU memory and how PagedAttention manages it efficiently
- Contrast continuous (in-flight) batching with static batching and explain why it raises GPU utilization
- Launch an OpenAI-compatible vLLM server and call it with curl and the Python openai client
- Tune key vLLM flags and reason about throughput-versus-latency trade-offs using TTFT, TPOT, and tokens/s
video: mlo-m5-l01-serving-llms-efficiently-with-vllm.mp4
quiz:
- q: Why is autoregressive LLM decoding usually memory-bandwidth bound rather than compute bound?
  options:
  - Each generated token requires retraining the model
  - Each decode step reads the full weights and the KV cache to produce just one token, so it is limited
    by memory bandwidth, not raw FLOPs
  - GPUs have no tensor cores for attention
  - Tokenization dominates the runtime
  answer: 1
  why: During decode the model produces one token per step but must stream the entire weight matrix and
    the growing KV cache from GPU memory, so memory bandwidth—not arithmetic throughput—is the bottleneck.
- q: What does PagedAttention do?
  options:
  - Compresses the model weights with quantization
  - Stores the KV cache in fixed-size, non-contiguous blocks addressed through a block table, like OS virtual
    memory
  - Skips attention computation for long sequences
  - Encrypts the KV cache at rest
  answer: 1
  why: PagedAttention applies the idea of OS virtual memory to the KV cache, dividing it into fixed-size
    blocks mapped via a block table so memory need not be contiguous, which slashes fragmentation and waste.
- q: How does continuous (in-flight) batching differ from static batching?
  options:
  - It waits for every request in the batch to finish before admitting any new ones
  - It schedules at the iteration level, freeing finished sequences and admitting queued ones every step
    to keep the GPU saturated
  - It runs each request on a separate dedicated GPU
  - It disables the KV cache to save memory
  answer: 1
  why: Continuous batching makes scheduling decisions every forward pass — when a sequence finishes, its
    blocks are freed and a waiting request joins immediately, so the GPU is not idled by the slowest request.
- q: Which vLLM flag controls the fraction of GPU memory reserved for weights, activations, and the KV
    cache pool?
  options:
  - --max-model-len
  - --max-num-seqs
  - --gpu-memory-utilization
  - --tensor-parallel-size
  answer: 2
  why: --gpu-memory-utilization (default 0.90) sets the fraction of VRAM vLLM may use; after weights load,
    the remainder becomes the KV cache pool, so a higher value allows more concurrent sequences.
- q: A user says the chatbot feels slow to start answering but then streams quickly. Which latency metric
    is the problem, and name one lever to improve it?
  answer: Time to first token (TTFT) is high—the prefill/queueing stage. Lower it by reducing queue pressure
    (fewer concurrent requests or a smaller --max-model-len), giving the KV cache more memory, or adding
    tensor parallelism. TPOT/ITL (streaming speed) is fine here.
  why: TTFT measures time from request arrival to the first output token, dominated by prefill and queue
    wait; inter-token latency governs streaming speed, which the user reports as acceptable.
- q: Your 70B model does not fit in one GPU's memory. Which vLLM flag spreads it across multiple GPUs on
    a node, and what does it do?
  answer: --tensor-parallel-size N shards each layer's weight matrices (and the attention/KV computation)
    across N GPUs on one node so the model and its KV cache fit and compute in parallel.
  why: Tensor parallelism splits the large matrix multiplications across GPUs, distributing both the memory
    footprint and the compute; larger multi-node topologies are covered in later lessons.
resources:
- label: vLLM Documentation
  url: https://docs.vllm.ai/en/stable/
- label: vLLM Optimization and Tuning
  url: https://docs.vllm.ai/en/stable/configuration/optimization/
- label: vLLM Production Metrics (TTFT, ITL)
  url: https://docs.vllm.ai/en/stable/design/metrics/
- label: 'PagedAttention: Efficient Memory Management for LLM Serving (SOSP 2023)'
  url: https://arxiv.org/abs/2309.06180
---

## Why Serving LLMs Is Different

In Modules 1–4 you containerized models with Docker, wrapped them in FastAPI, deployed to Kubernetes, tracked them with MLflow, and added monitoring. Those classic models — a gradient-boosted classifier, a small CNN — take a fixed-size input, run one forward pass, and return one output. Sizing them is easy: measure latency, set replicas, autoscale on CPU.

Large language models break that mental model. A single request is not one forward pass — it is *hundreds* of them, one per generated token. Memory, not CPU, is the scarce resource, and a naive deployment wastes most of the GPU. This module is about serving LLMs the way production teams actually do, starting with **vLLM**, the de-facto open-source inference engine.

## LLM Inference Is Memory-Bound and Autoregressive

LLMs generate text **autoregressively**: they produce one token, append it to the input, and feed the whole sequence back in to produce the next token. A 200-token answer means ~200 sequential forward passes.

Inference splits into two phases:

- **Prefill**: process the entire input prompt in one parallel pass and populate the cache. This is compute-heavy and drives **time to first token**.
- **Decode**: generate output tokens one at a time. Each step does very little math but must read the *entire* set of model weights plus a growing cache from GPU memory.

Decode is **memory-bandwidth bound**: the GPU's tensor cores sit mostly idle while waiting for data to stream from VRAM. This is the opposite of classic batch inference, and it changes everything about how we batch and size LLM servers.

## The KV Cache Dominates GPU Memory

To avoid recomputing attention over the whole sequence at every step, the model caches the **key** and **value** tensors for every previous token. This **KV cache** grows linearly with sequence length and with the number of concurrent requests:

```
kv_bytes ≈ 2 (K and V) × layers × kv_heads × head_dim × seq_len × dtype_bytes
```

For a 13B model at fp16, a single 2,000-token sequence can need on the order of a gigabyte of KV cache — and you want to serve *many* sequences at once. After the weights load, **whatever VRAM is left becomes the KV cache pool, and that pool caps how many requests you can serve concurrently.** KV cache, not weights, is usually what limits throughput.

Classic frameworks pre-allocated a contiguous chunk of memory per request sized for the maximum length, wasting huge amounts to internal fragmentation. vLLM's headline innovation fixes exactly this.

## PagedAttention

**PagedAttention** (UC Berkeley, SOSP 2023) applies the idea of **operating-system virtual memory** to the KV cache. Instead of one contiguous allocation per sequence, the cache is split into fixed-size **blocks** (16 tokens each by default). Each sequence keeps a **block table** mapping its logical positions to physical blocks, which may live anywhere in the pool.

The payoff:

- **Near-zero fragmentation** — blocks are allocated on demand as a sequence grows, not reserved up front for the worst case.
- **Higher concurrency** — the freed memory becomes room for more simultaneous requests.
- **Cheap sharing** — sequences with a common prefix (a shared system prompt, parallel samples) can point at the *same* physical blocks (copy-on-write), saving memory and prefill work.

PagedAttention is always on in vLLM; there is no flag to enable it.

## Continuous (In-Flight) Batching

Throughput on a GPU comes from batching. The old approach, **static batching**, collects N requests, runs them together, and waits for *all* of them to finish before starting the next batch. Because requests finish at different lengths, fast ones idle while the GPU grinds on the slowest — utilization tanks.

vLLM uses **continuous batching** (also called in-flight or iteration-level batching). Scheduling happens **every forward pass**: the moment a sequence emits its end-of-sequence token, its KV blocks are freed and a queued request is admitted into the running batch for the very next step. The GPU stays saturated, and average latency drops because requests no longer wait for a whole batch to drain. Continuous batching is on by default.

## Launching an OpenAI-Compatible vLLM Server

vLLM ships an **OpenAI-compatible** HTTP server, so it is a drop-in replacement for the OpenAI API. Start it with the `vllm serve` CLI:

```bash
pip install vllm

# Serve a model; it downloads from Hugging Face on first run
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 --port 8000 \
  --gpu-memory-utilization 0.90 \
  --max-model-len 8192
```

By default it listens on port `8000` and exposes:

- `POST /v1/chat/completions` — chat-style requests
- `POST /v1/completions` — raw text completions
- `GET  /v1/models` — list served models
- `GET  /health` and `GET /metrics` — liveness and Prometheus metrics

The `/health` and `/metrics` endpoints plug straight into the Kubernetes probes and monitoring you set up in earlier modules.

## Calling the Server

Because the API is OpenAI-compatible, any OpenAI client works — just point it at your host and use any non-empty API key. With curl:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "Explain the KV cache in one sentence."}],
    "max_tokens": 128
  }'
```

Or with the Python `openai` client:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

resp = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Explain the KV cache in one sentence."}],
    max_tokens=128,
    stream=True,  # stream tokens as they are generated
)
for chunk in resp:
    print(chunk.choices[0].delta.content or "", end="")
```

## Key Tuning Flags

A handful of flags drive most of the performance:

- `--gpu-memory-utilization` (default `0.90`): fraction of VRAM vLLM may use. Whatever is left after weights becomes KV cache, so a higher value allows more concurrent sequences — raise it until you hit out-of-memory.
- `--max-model-len`: maximum context length (prompt + output) in tokens. Each token costs KV cache, so capping this frees memory for more parallel requests. Set it to the longest context you actually need.
- `--max-num-seqs`: the maximum number of sequences in a running batch. Larger values increase throughput under heavy load but can raise per-request latency.
- `--tensor-parallel-size`: number of GPUs to shard the model across on one node (see below).

## Throughput vs. Latency: TTFT, TPOT, Throughput

You cannot maximize everything at once; serving is a trade-off measured by three numbers:

- **TTFT (time to first token)**: how long until the first token appears. Dominated by prefill and queue wait — this is what makes a chat UI feel responsive.
- **TPOT / ITL (time per output token / inter-token latency)**: the average gap between successive tokens once generation starts — how fast text streams.
- **Throughput (tokens/second)**: total tokens the server emits across *all* requests per second — the cost-efficiency number.

Pushing batch size and `--max-num-seqs` up raises aggregate throughput (cheaper per token) but increases TTFT and TPOT for any individual user. An interactive chatbot optimizes for low TTFT; a nightly batch summarization job optimizes for raw throughput. Always state which one your SLO targets. vLLM exposes all three on `/metrics` for Prometheus.

## Tensor Parallelism for Multi-GPU

When a model is too large for one GPU — a 70B model needs well over a single 80 GB card's memory — use **tensor parallelism** to shard each layer's weight matrices across GPUs on the same node:

```bash
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 4
```

Each GPU holds a slice of every layer and the slices compute in parallel, communicating over fast NVLink. This distributes both the weights and the KV cache so a model that would not fit anywhere now runs. Larger pipeline/data-parallel and multi-node topologies build on this idea in later lessons.

## Common Pitfalls

- Setting `--max-model-len` far higher than needed → KV cache reserved per token starves concurrency.
- Pushing `--gpu-memory-utilization` to `1.0` → out-of-memory crashes; leave headroom for activations.
- Quoting a single TTFT number without load → latency degrades sharply as concurrency rises; always benchmark under realistic traffic.
- Treating an LLM pod like a classic CPU service in autoscaling → scale on GPU/KV-cache pressure and queue depth, not CPU.

> **Coming up in this module:** quantization and TensorRT-LLM/Triton for even faster kernels (lesson 2), serving on Kubernetes with KServe (lesson 3), and LLM observability and cost control (lesson 4). This lesson gave you the engine; the rest of the module operationalizes it.
