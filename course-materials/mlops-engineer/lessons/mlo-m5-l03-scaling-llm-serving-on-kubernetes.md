---
course: mlops-engineer
title: Scaling LLM Serving on Kubernetes
month: 5
monthTitle: LLMOps & GPU Serving
lesson: 3
summary: Learn how to schedule and scale large language model workloads on Kubernetes GPUs. This lesson
  covers requesting GPUs with nvidia.com/gpu, the NVIDIA device plugin and GPU Operator, taints/tolerations
  and node affinity, GPU sharing via time-slicing and MPS, deploying an LLM behind a KServe InferenceService
  with autoscaling and scale-to-zero, autoscaling on GPU or queue/concurrency metrics, and multi-GPU
  scheduling for tensor- and pipeline-parallel models.
objectives:
- Schedule GPU pods using nvidia.com/gpu resource requests, the NVIDIA device plugin/GPU Operator, and
  taints, tolerations, and node affinity
- Share a single GPU across smaller LLM workloads using time-slicing and MPS, and explain their trade-offs
  versus MIG
- Deploy an LLM behind a KServe InferenceService with request-based autoscaling and scale-to-zero
- Configure autoscaling driven by GPU utilization or queue/concurrency metrics using KEDA, the Prometheus
  Adapter, or Knative concurrency
- Compare KServe, BentoML, and Ray Serve and select the right stack for tensor/pipeline-parallel multi-GPU
  models
video: mlo-m5-l03-scaling-llm-serving-on-kubernetes.mp4
quiz:
- q: How do you request a GPU for a pod in Kubernetes?
  options:
  - Add nvidia.com/gpu under resources.requests only
  - Add nvidia.com/gpu under resources.limits (requests defaults to the same value)
  - Set a GPU=true environment variable on the container
  - Label the pod with accelerator=gpu
  answer: 1
  why: GPUs are an extended resource and may only be set in limits. If you omit requests, Kubernetes copies
    the limit into requests; you cannot oversubscribe a whole GPU, so request always equals limit.
- q: How does GPU time-slicing differ from Multi-Instance GPU (MIG)?
  options:
  - Time-slicing gives each replica hardware memory and fault isolation
  - Time-slicing physically partitions the GPU into separate instances
  - Time-slicing oversubscribes one GPU with no memory or fault isolation between replicas
  - Time-slicing needs no device plugin or GPU Operator
  answer: 2
  why: Time-slicing interleaves workloads on an oversubscribed GPU with no memory or fault isolation between
    replicas, unlike MIG which physically partitions the GPU into isolated instances with dedicated memory.
- q: How do you enable scale-to-zero for a KServe InferenceService serving on GPUs?
  options:
  - Set replicas: 0 on the underlying Deployment
  - Set minReplicas: 0 so Knative scales pods to zero when idle
  - Manually delete the InferenceService when traffic stops
  - Move the model to a CPU-only node pool
  answer: 1
  why: With minReplicas set to 0, KServe's Knative-backed autoscaler scales the InferenceService down to
    zero pods when there is no traffic and cold-starts a GPU pod on the next request, freeing expensive GPUs.
- q: 'A model is deployed with tensorParallelSize: 2 and pipelineParallelSize: 2. How many GPUs does one
    replica need?'
  options:
  - '2'
  - '4'
  - '8'
  - '1'
  answer: 1
  why: Total GPUs per replica equals tensorParallelSize multiplied by pipelineParallelSize, so 2 x 2 =
    4 GPUs, which must be schedulable together (ideally on one node or across nodes with fast interconnect).
- q: Why is plain GPU utilization often a poor autoscaling signal for an LLM server, and what works better?
  answer: A single in-flight request can pin GPU utilization near 100% while the server still has spare
    batching capacity, so utilization hides real load. Queue/concurrency signals (number of waiting/running
    requests, KV-cache utilization, or in-flight concurrency) reflect saturation far better and are exposed
    by vLLM and consumed by KEDA, the Prometheus Adapter, or Knative concurrency.
  why: LLM servers batch continuously, so utilization saturates early; scaling on waiting requests, KV-cache
    usage, or concurrency tracks actual capacity and latency much more accurately.
- q: When would you pick Ray Serve over KServe or BentoML for LLM serving?
  answer: Choose Ray Serve when you need programmatic, Python-native composition of multi-stage pipelines
    (e.g., RAG with retrieval + rerank + generation), fractional/multi-GPU scheduling, or multi-node tensor/pipeline
    parallelism orchestrated by the Ray cluster. Pick KServe for a declarative, Kubernetes-native InferenceService
    with built-in Knative scale-to-zero, and BentoML/OpenLLM when you want to package a Bento and deploy
    it as a container or to BentoCloud with minimal infra.
  why: Each tool targets a different need. KServe is declarative and Kubernetes-native with scale-to-zero,
    BentoML is packaging-first, and Ray Serve is a programmable framework strong at composition and distributed
    multi-GPU serving.
resources:
- label: Schedule GPUs (Kubernetes official docs)
  url: https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/
- label: Time-Slicing GPUs in Kubernetes (NVIDIA GPU Operator)
  url: https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html
- label: KServe Generative Inference (LLM serving)
  url: https://kserve.github.io/website/docs/model-serving/generative-inference/overview
- label: Ray Serve LLM APIs
  url: https://docs.ray.io/en/latest/serve/llm/index.html
---

## Why GPU-Aware Scaling Is Different

Earlier in this course you deployed CPU model APIs with Deployments, Services, HPA, and probes (Module 3), and in this module you served LLMs with vLLM (lesson 1) and squeezed them with quantization, Triton, and TensorRT-LLM (lesson 2). Scaling LLMs on a cluster adds a new constraint: **GPUs are scarce, expensive, and indivisible by default**. A single A100/H100 can cost more per hour than a rack of CPU nodes, and one large model may not even fit on one GPU. So the scheduling and scaling rules change.

This lesson is about getting LLM pods onto the right GPUs, sharing GPUs when models are small, scaling on signals that actually reflect LLM load, and splitting giant models across multiple GPUs.

## Scheduling GPU Pods

Kubernetes does not understand GPUs natively. A **device plugin** from the hardware vendor advertises GPUs as an *extended resource* named `nvidia.com/gpu`. In practice you install the **NVIDIA GPU Operator**, which deploys and manages the driver, container toolkit, device plugin, and DCGM metrics exporter for you, instead of wiring each component by hand.

Once GPUs are advertised, you request them like any resource — but with two rules: **GPUs may only appear in `limits`** (Kubernetes copies the limit into `requests`), and you **cannot oversubscribe a whole GPU**, so request always equals limit.

```yaml
resources:
  limits:
    nvidia.com/gpu: 1   # request == limit; whole GPUs only
    cpu: "4"
    memory: 24Gi
```

### Taints, Tolerations, and Affinity

GPU nodes are precious, so you keep CPU-only pods off them. The common pattern is to **taint** GPU nodes and have GPU pods **tolerate** that taint, then use **node affinity** to target a specific GPU type.

```yaml
spec:
  tolerations:
    - key: "nvidia.com/gpu"
      operator: "Exists"
      effect: "NoSchedule"
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: nvidia.com/gpu.product
                operator: In
                values: ["NVIDIA-H100-80GB-HBM3"]
```

Taints repel everything that does not tolerate them; affinity *attracts* the pod to the right hardware. Use both: the toleration earns entry to GPU nodes, and affinity pins the workload to GPUs with enough memory for the model.

## GPU Sharing: Time-Slicing and MPS

A 7B model in INT8 might use only a fraction of an 80 GB GPU. Running one pod per GPU wastes money. The GPU Operator lets you **oversubscribe** a GPU so several pods share it:

- **Time-slicing**: the GPU rapidly interleaves work from multiple replicas. You define how many replicas a GPU is split into; each is handed to a pod as a normal `nvidia.com/gpu` unit. There is **no memory or fault isolation** between replicas — one pod can OOM the GPU and affect neighbors.
- **MPS (Multi-Process Service)**: NVIDIA's CUDA MPS runs kernels from multiple processes concurrently, giving better throughput than pure time-slicing and optional memory limits per client.
- **MIG (Multi-Instance GPU)**: on A100/H100, physically partitions the GPU into isolated instances with dedicated memory and fault isolation — the strongest isolation, but fixed profiles.

Enable time-slicing by giving the GPU Operator a config map and labeling nodes. The node then advertises multiple GPU replicas and gets a `-SHARED` product suffix:

```yaml
# ConfigMap consumed by the GPU Operator / device plugin
sharing:
  timeSlicing:
    resources:
      - name: nvidia.com/gpu
        replicas: 4   # 1 physical GPU advertised as 4 schedulable units
```

Rule of thumb: **time-slicing/MPS for many small models that trust each other; MIG when you need hard isolation; a whole GPU (or several) for a large model.**

## Deploying an LLM with KServe

**KServe** turns a model into a declarative `InferenceService` (ISVC) and, in Knative mode, gives you request-based autoscaling and **scale-to-zero** for free. Its generative-inference runtime auto-maps the **vLLM** backend for Hugging Face LLM tasks, so you get continuous batching without writing a server.

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llama3-8b
spec:
  predictor:
    minReplicas: 0          # scale-to-zero when idle
    maxReplicas: 5
    scaleTarget: 10         # target concurrent requests per pod
    scaleMetric: concurrency
    model:
      modelFormat:
        name: huggingface   # served by the vLLM runtime
      storageUri: "hf://meta-llama/Meta-Llama-3-8B-Instruct"
      resources:
        limits:
          nvidia.com/gpu: "1"
          cpu: "4"
          memory: 24Gi
```

With `minReplicas: 0`, Knative drops the deployment to zero GPU pods when traffic stops and cold-starts one on the next request — the single biggest GPU cost saver for spiky workloads. The trade-off is cold-start latency: loading multi-GB weights takes time, so pair scale-to-zero with a generous **startup probe** (`/health`) so the pod is not killed mid-load, and keep **readiness** (`/ready`) gating traffic until weights are loaded — the same probe convention you used in Module 3.

## Autoscaling on the Right Signal

CPU and even GPU utilization are poor LLM scaling signals: a single in-flight request can pin a GPU near 100% while the server still has batching headroom, so utilization saturates long before the server is actually full. **Scale on load, not utilization.** Better signals:

- **Knative concurrency** — in-flight requests per pod (`scaleMetric: concurrency`), the simplest queue-based signal and the KServe default for generative inference.
- **vLLM queue metrics via KEDA** — KEDA scales on external metrics such as the number of **waiting requests** or **KV-cache utilization** that vLLM exports to Prometheus.
- **Prometheus Adapter** — exposes any Prometheus metric (e.g., `requests_per_second`, queue depth) as a Kubernetes custom metric an HPA can target.

```yaml
# KEDA: scale on vLLM's pending-request queue
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: llama3-scaler
spec:
  scaleTargetRef:
    name: llama3-8b-predictor
  minReplicaCount: 0
  maxReplicaCount: 8
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus.monitoring:9090
        query: sum(vllm:num_requests_waiting)
        threshold: "5"
```

Whatever signal you pick, tune scale-up to be fast and scale-down to be slow (stabilization windows) so GPU pods do not flap — a cold start is far more expensive than holding a warm pod a little longer.

## Multi-GPU Scheduling for Large Models

When a model is too big for one GPU, split it:

- **Tensor parallelism (TP)** shards each layer's matrices across GPUs — needs fast interconnect (NVLink) and is usually kept **within one node**.
- **Pipeline parallelism (PP)** splits the model into stages across GPUs/nodes — tolerates slower links between stages.

Total GPUs per replica = **TP x PP**. KServe expresses this with a `workerSpec` for multi-node/multi-GPU serving:

```yaml
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      storageUri: pvc://llama-70b-pvc/Meta-Llama-3-70B-Instruct
    workerSpec:                   # sibling of model, under predictor
      tensorParallelSize: 4       # 4 GPUs per node (NVLink)
      pipelineParallelSize: 2     # 2 nodes -> 8 GPUs total
```

The scheduler must place all TP shards on GPUs with fast interconnect; spreading a tensor-parallel group across nodes will cripple throughput. Ray Serve handles the same split with `engine_kwargs={"tensor_parallel_size": 4, "pipeline_parallel_size": 2}`, using Ray placement groups to co-locate workers.

## Choosing a Serving Stack

- **KServe** — declarative, Kubernetes-native `InferenceService`. Best when you want GitOps-style manifests, Knative scale-to-zero, and a managed vLLM runtime. Pick it as the default for k8s-centric platforms.
- **BentoML / OpenLLM** — packaging-first. You bundle code, weights, and dependencies into a **Bento**, containerize it, and run it anywhere (Kubernetes or BentoCloud). Best when you want a portable artifact and a simple Python service API.
- **Ray Serve** — a programmable Python framework. Best for **composing multi-stage pipelines** (RAG: retrieve, rerank, generate), **fractional GPUs** for many small models, and **distributed multi-GPU** serving orchestrated by the Ray cluster. Note fractional-GPU deployments work best with fixed replica counts rather than autoscaling.

You can also combine them — for example, package with BentoML and deploy onto KServe — but for a single LLM endpoint, start with KServe.

## Common Pitfalls

- Putting `nvidia.com/gpu` in `requests` instead of `limits`, or setting unequal values — the pod will fail to schedule.
- Missing tolerations on GPU pods, so they stay `Pending` while CPU pods squat on GPU nodes without affinity.
- Scale-to-zero with no startup probe — slow weight loading gets killed by the liveness probe before the model is ready.
- Autoscaling on CPU/GPU utilization instead of queue/concurrency, so the server saturates without ever triggering a scale-up.
- Spreading a tensor-parallel group across nodes without NVLink-class interconnect, tanking throughput.
- Forgetting the Cluster Autoscaler (or a warm GPU node pool), so HPA/KEDA scale-ups sit `Pending` with no GPU node to land on.
