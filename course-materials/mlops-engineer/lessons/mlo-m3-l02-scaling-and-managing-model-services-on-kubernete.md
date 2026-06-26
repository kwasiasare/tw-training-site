---
course: mlops-engineer
title: Scaling and Managing Model Services on Kubernetes
month: 3
monthTitle: Orchestration, CI/CD & Infrastructure as Code
lesson: 2
summary: Learn how to run model serving workloads reliably on Kubernetes by configuring resource requests/limits,
  autoscaling with HPA, and safe rolling updates with health probes.
objectives:
- Set appropriate CPU/memory requests and limits for model serving pods
- Configure Horizontal Pod Autoscaler (HPA) to scale model services under load
- Perform safe rolling updates and rollbacks with zero downtime
- Use liveness, readiness, and startup probes to keep traffic flowing to healthy pods
- Apply PodDisruptionBudgets and node strategies to maintain availability
video: mlo-m3-l02-scaling-and-managing-model-services-on-kubernete.mp4
quiz:
- q: What happens when a container exceeds its memory limit?
  options:
  - It is CPU throttled
  - It is OOMKilled
  - It is removed from Service endpoints
  - Nothing, limits are advisory
  answer: 1
  why: Exceeding a memory limit triggers an OOMKill, unlike CPU which is throttled. This is why memory
    request should be close to the limit for model servers.
- q: Which probe is most important for a model with a slow weight-loading startup?
  options:
  - livenessProbe
  - readinessProbe
  - startupProbe
  - none
  answer: 2
  why: The startupProbe gives slow-starting containers time to initialize before liveness and readiness
    probes begin, preventing premature restarts.
- q: Why is CPU utilization often a poor scaling metric for inference services?
  options:
  - CPU is never used by models
  - HPA cannot read CPU
  - Request rate or queue depth better reflects real inference load
  - CPU metrics are not available in Kubernetes
  answer: 2
  why: Inference load correlates better with requests-per-second or queue depth than raw CPU, so custom
    metrics via Prometheus Adapter or KEDA scale more accurately.
- q: 'What does setting maxUnavailable: 0 in a rolling update achieve?'
  options:
  - Faster rollout by killing all pods at once
  - Full serving capacity is maintained throughout the rollout
  - Disables rollbacks
  - Prevents new pods from starting
  answer: 1
  why: 'maxUnavailable: 0 ensures no existing pods are removed until replacements are Ready, keeping full
    capacity during the update (requires surge room).'
- q: What is the role of a PodDisruptionBudget?
  answer: It guarantees a minimum number of healthy pods remain available during voluntary disruptions
    such as node drains or cluster upgrades.
  why: PDBs protect availability against voluntary disruptions, ensuring operations like node maintenance
    don't take down too many model serving pods at once.
- q: Which two Kubernetes components must work together so HPA scale-ups can actually run?
  answer: The Horizontal Pod Autoscaler (which adds pods) and the Cluster Autoscaler (which adds nodes
    for those pods to land on).
  why: HPA only creates pods; if no node has capacity they stay Pending, so the Cluster Autoscaler must
    add nodes to realize the scale-up.
resources:
- label: Kubernetes HorizontalPodAutoscaler docs
  url: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- label: Configure Liveness, Readiness and Startup Probes
  url: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- label: PodDisruptionBudget / Disruptions
  url: https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
- label: 'KEDA: Kubernetes Event-driven Autoscaling'
  url: https://keda.sh/docs/
---

## Why Kubernetes for Model Serving

Model services have unique traffic patterns: bursty inference loads, slow cold starts (loading large weights), and strict latency SLOs. Kubernetes gives us declarative scaling, self-healing, and rolling updates—but only if we configure resources, autoscaling, and health checks correctly.

## Resource Requests and Limits

Every container should declare `requests` (what the scheduler reserves) and `limits` (the hard ceiling).

- **requests** drive scheduling and HPA utilization math.
- **limits** prevent a noisy pod from starving neighbors. CPU over-limit is throttled; memory over-limit triggers an OOMKill.
- For model servers, profile real inference memory (weights + batch activations) and set memory request ≈ limit to avoid OOM surprises. Avoid setting a CPU limit far below request, or you'll throttle latency.

```yaml
resources:
  requests:
    cpu: "1"
    memory: "4Gi"
  limits:
    cpu: "2"
    memory: "4Gi"
```

For GPU models, request `nvidia.com/gpu: 1`; GPUs are not oversubscribed, so request == limit always.

## Health Probes

Three probe types keep traffic on healthy pods:

- **startupProbe**: gives slow-loading models time to load weights before other probes start. Critical for large models.
- **readinessProbe**: pod only receives traffic when ready; failing it removes the pod from the Service endpoints without killing it.
- **livenessProbe**: restarts a hung pod.

```yaml
startupProbe:
  httpGet: { path: /health, port: 8080 }
  failureThreshold: 30
  periodSeconds: 10
readinessProbe:
  httpGet: { path: /ready, port: 8080 }
  periodSeconds: 5
livenessProbe:
  httpGet: { path: /health, port: 8080 }
  periodSeconds: 10
```

## Horizontal Pod Autoscaler (HPA)

HPA adds/removes replicas based on metrics. CPU is the default, but for inference, custom metrics like requests-per-second or queue depth (via Prometheus Adapter / KEDA) are far better proxies for load.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: model-hpa }
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-server
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 60 }
```

Tune `behavior` to avoid flapping: scale up fast, scale down slowly with stabilization windows. HPA needs metrics-server installed and accurate `requests` to compute utilization.

## Rolling Updates and Rollbacks

Deployments default to `RollingUpdate`. Control disruption with `maxUnavailable` and `maxSurge`.

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```

- `maxUnavailable: 0` ensures full capacity during rollout (needs spare node room).
- Readiness probes gate the rollout—new pods must be Ready before old ones terminate.
- Roll back with `kubectl rollout undo deployment/model-server`.
- Use `minReadySeconds` to bake new pods before considering them stable.

## Availability: PDBs and Disruptions

A **PodDisruptionBudget** protects against voluntary disruptions (node drains, upgrades) by guaranteeing a minimum of healthy pods.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
spec:
  minAvailable: 2
  selector:
    matchLabels: { app: model-server }
```

Combine with `terminationGracePeriodSeconds` and a `preStop` hook so in-flight requests drain before shutdown.

## Putting It Together

A production-ready model service: 2+ minReplicas, profiled requests/limits, startup+readiness+liveness probes, HPA on a meaningful metric, zero-downtime rolling strategy, and a PDB. Add a Cluster Autoscaler so HPA scale-ups can actually land on new nodes.
