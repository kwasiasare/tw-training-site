---
course: mlops-engineer
title: 'Optimizing LLM Inference: Quantization and Compiled Runtimes'
month: 5
monthTitle: LLMOps & GPU Serving
lesson: 2
summary: Lesson 1 got a model serving on vLLM with PagedAttention and continuous batching. This lesson
  makes that serving cheaper and faster. You will learn numeric precision and quantization (FP16/BF16
  down to INT8, FP8, and weight-only AWQ/GPTQ), how to reason about accuracy/throughput/memory trade-offs,
  how to serve a quantized model in vLLM, and when NVIDIA Triton and TensorRT-LLM compiled engines earn
  their added complexity.
objectives:
- Distinguish numeric precision formats (FP16/BF16, INT8, FP8) and weight-only vs weight+activation quantization
- Apply AWQ, GPTQ, FP8, and KV-cache quantization, and reason about their memory and throughput effects
- Evaluate quantization quality loss with task metrics and perplexity before promoting a model
- Serve a quantized model in vLLM and a multi-backend stack in NVIDIA Triton Inference Server
- Decide between vLLM and a TensorRT-LLM compiled engine using a latency/throughput/cost framework
video: mlo-m5-l02-optimizing-llm-inference-with-quantization-and.mp4
quiz:
- q: Which statement best describes AWQ and GPTQ?
  options:
  - They quantize both weights and activations to INT8 at training time
  - They require full retraining of the model from scratch
  - They are weight-only post-training methods (e.g., W4A16) that leave activations in FP16/BF16
  - They only compress the KV cache and leave weights untouched
  answer: 2
  why: AWQ and GPTQ are post-training, weight-only methods. They pack weights to ~4 bits (W4A16) while
    activations stay in FP16/BF16, cutting weight memory and bandwidth without touching the activation path.
- q: For an FP8 model served in vLLM, what does "W8A8" mean?
  options:
  - Eight weight tensors and eight activation tensors per layer
  - Both weights and activations are represented in 8-bit (here, FP8)
  - 8-bit weights but 16-bit activations
  - The model must run across exactly 8 GPUs
  answer: 1
  why: W8A8 means weights AND activations are 8-bit. FP8 W8A8 is a weight+activation scheme that uses the
    GPU's FP8 tensor cores (e.g., Hopper/Blackwell), so the compute path itself runs in 8-bit, not just storage.
- q: Which command serves an AWQ-quantized model with vLLM?
  options:
  - vllm serve my-model --dtype awq
  - vllm serve my-model --quantization awq
  - vllm compile my-model --awq
  - vllm serve my-model --kv-cache-dtype awq
  answer: 1
  why: The `--quantization` flag selects the quantization method (e.g., `awq`, `fp8`, `gptqmodel`). `--dtype`
    sets the base compute dtype, and `--kv-cache-dtype` controls KV-cache precision, not weight quantization.
- q: When is a TensorRT-LLM compiled engine most likely to beat vLLM?
  options:
  - When you swap models frequently and need fast iteration
  - On a stable model and fixed NVIDIA GPU, where a pre-compiled, hardware-specific engine minimizes latency
  - When you must serve on CPU-only hosts
  - When you cannot afford any build/compile step
  answer: 1
  why: TensorRT-LLM compiles a GPU-, shape-, and batch-specific engine with fused kernels, typically winning
    15-30% on latency/throughput on H100-class GPUs. The cost is a long compile and rigidity, so it pays off
    for stable, high-volume models, not rapidly changing ones.
- q: Explain the accuracy/throughput/memory trade-off of weight-only INT4 quantization, and how you would
    evaluate the quality loss before shipping.
  answer: INT4 weight-only (e.g., AWQ/GPTQ W4A16) cuts weight memory roughly 4x versus FP16 and reduces
    memory-bandwidth pressure, which raises throughput and lets a model fit on smaller/fewer GPUs; activations
    stay FP16 so compute precision is largely preserved. The risk is accuracy degradation, especially on
    reasoning/long-context tasks. Evaluate it by measuring perplexity plus your real task metrics (e.g.,
    exact-match, pass@k, or an LLM-judge score) on a held-out set, comparing the quantized model against the
    FP16/BF16 baseline, and only promoting if the drop is within your tolerance.
  why: Quantization quality must be measured, not assumed. Perplexity is a cheap proxy but task-level metrics
    on representative prompts are what actually gate a release; the trade-off is memory/throughput gains versus
    a tolerable accuracy delta.
- q: When would you choose NVIDIA Triton Inference Server over running vLLM's standalone OpenAI-compatible
    server directly?
  answer: Choose Triton when you need to serve many models and/or mixed backends behind one server, with a
    managed model repository, versioning, concurrent model execution, and server-side dynamic batching. Triton
    can host a vLLM backend and a TensorRT-LLM backend (and non-LLM models) side by side with unified metrics,
    health, and deployment. If you are serving a single LLM and want the simplest path, vLLM's own server is
    lighter weight.
  why: vLLM's standalone server is ideal for one model with minimal overhead; Triton adds value as a
    multi-model, multi-backend platform with a model repository, versioning, and dynamic batching across
    heterogeneous models.
resources:
- label: vLLM Quantization (official docs)
  url: https://docs.vllm.ai/en/latest/features/quantization/
- label: NVIDIA Triton Inference Server (official docs)
  url: https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html
- label: NVIDIA TensorRT-LLM Documentation
  url: https://nvidia.github.io/TensorRT-LLM/
- label: 'AWQ: Activation-aware Weight Quantization (paper)'
  url: https://arxiv.org/abs/2306.00978
---

## From "It Serves" to "It Serves Efficiently"

In Lesson 1 you stood up a model on vLLM with PagedAttention and continuous batching behind an OpenAI-compatible API. That gets you correct, scalable serving. This lesson is about the next question every LLMOps engineer hits: *how do I serve the same quality for less GPU memory, lower latency, and lower cost?* The two biggest levers are **quantization** (use fewer bits per number) and **compiled runtimes** (build a hardware-specific engine).

## Numeric Precision: The Baseline

LLM weights and activations are numbers, and the number format decides how much memory and bandwidth each one costs.

- **FP32** (32-bit float): training-grade precision, rarely used for inference.
- **FP16 / BF16** (16-bit): the standard inference baseline. BF16 has a wider exponent range (more training-stable); FP16 has more mantissa precision. Most published checkpoints serve in one of these.

Memory math is simple and worth internalizing: a 7B-parameter model needs roughly `params x bytes_per_param`. At FP16 (2 bytes) that is ~14 GB just for weights; at INT8 (~1 byte) ~7 GB; at INT4 (~0.5 byte) ~3.5 GB. Lower precision means the weights fit in less VRAM **and** move through memory bandwidth faster, which is often the real bottleneck in decoding.

## What Quantization Actually Does

Quantization maps high-precision values onto a smaller set of low-precision values using a **scale** (and sometimes a zero-point), usually per-group of weights to limit error. Two axes matter:

- **What is quantized?**
  - **Weight-only**: only the stored weights are low-bit; activations stay FP16/BF16. Cheap memory win, minimal compute-path change. AWQ and GPTQ are the popular INT4 weight-only methods (often written **W4A16** = 4-bit weights, 16-bit activations).
  - **Weight + activation**: both weights and activations are low-bit, so the matrix-multiply compute path itself runs low-bit on dedicated tensor cores. **FP8 W8A8** and **INT8 W8A8** are the common forms.
- **When is it computed?** Post-training quantization (PTQ) like AWQ/GPTQ/FP8 calibrates on a small dataset after training — no retraining. (Quantization-aware training exists but is out of scope here.)

### AWQ and GPTQ (weight-only, INT4)

- **GPTQ** quantizes weights layer-by-layer, using second-order (Hessian) information to minimize the output error introduced by rounding.
- **AWQ** (Activation-aware Weight Quantization) observes that a small fraction of weight channels are "salient" because they multiply large activations, and protects those channels so accuracy holds up at 4 bits.

Both deliver ~4x weight-memory reduction and strong throughput on memory-bound decoding, with usually small accuracy loss. In vLLM, AWQ is the default kernel for AWQ models, with optimized kernels (e.g., Marlin) available.

### FP8 and INT8 (weight + activation)

**FP8** (formats E4M3 and E5M2) is the modern sweet spot on Hopper (H100) and Blackwell GPUs: it quantizes weights *and* activations to 8-bit and runs on native FP8 tensor cores, giving strong throughput with very small quality loss — often the recommended default when your hardware supports it. **INT8 W8A8** is a similar weight+activation idea using integer math. Tooling such as **LLM Compressor** and **NVIDIA Model Optimizer** produces these checkpoints for vLLM.

### KV-Cache Quantization

During generation, the attention **KV cache** grows with batch size and sequence length and frequently dominates memory for long-context or high-concurrency serving. Quantizing the cache (e.g., FP8 via vLLM's `--kv-cache-dtype fp8`) is separate from weight quantization: it shrinks per-token cache footprint so you can hold more concurrent sequences or longer contexts on the same GPU. Watch for quality loss on very long contexts and validate.

## The Trade-Off Triangle: Accuracy, Throughput, Memory

There is no free lunch. Fewer bits buy memory and (usually) throughput, and the price is some accuracy. The job is to find the largest saving whose quality loss is within tolerance.

- **Memory**: INT4 ~4x smaller weights, INT8/FP8 ~2x, versus FP16.
- **Throughput**: decoding is often memory-bandwidth-bound, so smaller weights move faster; weight+activation (FP8/INT8) additionally speeds the compute path on supported tensor cores.
- **Accuracy**: typically FP8 < INT8 < INT4 in terms of risk, but it is model- and task-dependent.

### Evaluating Quality Loss

Never assume quantization is "fine." Measure it:

1. **Perplexity** on a held-out corpus — a cheap regression signal.
2. **Task metrics** that match your product: exact-match/F1, `pass@k` for code, accuracy on a domain benchmark, or an LLM-judge score on representative prompts.
3. **Compare against the FP16/BF16 baseline** and set a tolerance (e.g., "<1% drop on our eval set") as a release gate.

(Building full evaluation harnesses and continuous quality monitoring is Lesson 4 — here, just gate the swap.)

## Serving a Quantized Model in vLLM

vLLM consumes quantized checkpoints with one flag. Point it at a pre-quantized model and select the method:

```bash
# Serve a pre-quantized AWQ (INT4 weight-only) checkpoint
vllm serve TheModel/Llama-3.1-8B-Instruct-AWQ \
  --quantization awq \
  --max-model-len 8192

# Serve an FP8 (W8A8) checkpoint and quantize the KV cache to FP8 too
vllm serve meta-llama/Llama-3.1-8B-Instruct-FP8 \
  --quantization fp8 \
  --kv-cache-dtype fp8
```

Notes:
- `--quantization` accepts methods like `awq`, `gptqmodel`, and `fp8`. Many checkpoints embed their quant config, so vLLM can auto-detect, but setting it explicitly is clearer in production.
- `--dtype` is the base compute dtype and is distinct from `--quantization`.
- The server still exposes the same OpenAI-compatible `/v1/chat/completions` endpoint from Lesson 1 — quantization is transparent to clients.

## NVIDIA Triton Inference Server: Multi-Model, Multi-Backend

vLLM's own server is perfect for a single model. When you must serve **many models or mixed backends** behind one production endpoint, **NVIDIA Triton Inference Server** is the platform layer. Triton manages a **model repository** (versioned directory of models), runs models concurrently, exposes unified HTTP/gRPC and metrics, and performs **server-side dynamic batching**.

Triton is backend-pluggable. Relevant backends:
- **vLLM backend**: runs a vLLM engine inside Triton; its `model.json` maps to vLLM `EngineArgs` (e.g., `tensor_parallel_size`).
- **TensorRT-LLM backend**: serves compiled TensorRT-LLM engines with in-flight (continuous) batching and paged attention.
- Plus framework backends (PyTorch, ONNX, TensorRT) for non-LLM models in the same server.

A minimal model repository and dynamic-batching config:

```text
model_repository/
  llama3-vllm/
    config.pbtxt
    1/
      model.json        # vLLM EngineArgs: model, tensor_parallel_size, ...
```

```text
# config.pbtxt (excerpt) - server-side batching
dynamic_batching {
  preferred_batch_size: [ 8, 16 ]
  max_queue_delay_microseconds: 5000
}
```

**Dynamic batching** groups incoming requests server-side: Triton dispatches a batch when a preferred size is reached or `max_queue_delay_microseconds` expires, whichever comes first — raising GPU utilization for bursty, small requests. (Note: for LLMs, the vLLM/TensorRT-LLM backends also do their own continuous/in-flight batching at the token level, which is the bigger win covered in Lesson 1.)

## TensorRT-LLM: Compiled Engines

**TensorRT-LLM** takes a model plus a target GPU and **compiles a hardware-specific engine**: fused kernels, optimized attention, and quantization baked into a binary tuned for your GPU, batch size, and sequence lengths. Because the work is done ahead of time, the runtime extracts more out of the silicon than a general-purpose runtime can.

- **Upside**: on a stable model and fixed NVIDIA GPU, a well-built engine typically beats vLLM by ~15-30% on latency and peak throughput (H100-class).
- **Downside**: compilation is slow (tens of minutes) and the engine is rigid — tied to a specific GPU/shape config. Change the model, GPU, or parallelism and you recompile. It is more engineering overhead than `vllm serve`.

Serve the compiled engine via Triton's TensorRT-LLM backend for production endpoints.

## A Decision Framework

Choose your stack by the target you care about most:

- **Iterating fast / many models / changing weights** -> vLLM (standalone or via Triton's vLLM backend). Fastest to deploy, most flexible.
- **Need lowest latency on one stable, high-volume model on fixed NVIDIA GPUs** -> TensorRT-LLM compiled engine, served through Triton. Accept the compile cost for the speed.
- **One model, simplest ops** -> vLLM's standalone OpenAI-compatible server.
- **Many models / mixed LLM + non-LLM / heterogeneous backends behind one endpoint** -> Triton as the platform.

For precision, a practical default: start at **FP16/BF16** to establish a quality baseline, move to **FP8** if your GPUs support it (best quality-for-savings), and reach for **INT4 AWQ/GPTQ** when memory is the binding constraint — always gating the change on your eval metrics. Quantization and a compiled runtime are complementary: you can compile an FP8 or INT4 engine to stack both wins.

## Key Takeaways

- Lower precision trades accuracy for memory and throughput; FP8 (weight+activation) is the modern default on Hopper/Blackwell, AWQ/GPTQ (weight-only INT4) when memory is tight.
- Always measure quality loss (perplexity + task metrics) against the FP16 baseline before promoting a quantized model.
- vLLM serves quantized models with a single `--quantization` flag; KV-cache quantization is a separate, additive memory win.
- Triton is the multi-model/multi-backend platform with a model repository and dynamic batching; TensorRT-LLM compiled engines win on latency for stable, high-volume models at the cost of flexibility and build time.
