---
course: ml-engineer
title: Cloud Deployment and Serving at Scale
month: 6
monthTitle: Cloud Deployment, Scaling, and Monitoring
lesson: 1
summary: Move beyond running a container on your laptop and learn how to deploy a model to the cloud so
  it stays available, scales automatically, and rolls out safely. We cover managed ML endpoints, Kubernetes
  fundamentals for multi-replica serving, purpose-built serving runtimes like KServe and Triton, and how
  to choose between managed and self-managed approaches.
objectives:
- Explain why a single local container cannot meet production availability, autoscaling, and rollout needs
- Push a container image to a registry and deploy it to a managed ML endpoint (SageMaker, Vertex AI, or
  Azure ML)
- 'Describe the core Kubernetes objects for serving: pods, Deployments, Services, and horizontal autoscaling'
- Compare purpose-built serving runtimes (KServe, BentoML, Ray Serve, Triton) and what they add over a
  hand-rolled API
- Connect a model registry to deployment by pulling and serving an approved model version
- Choose between a managed endpoint and self-managed Kubernetes based on cost, control, and operational
  burden
video: mle-m6-l01-cloud-deployment-and-serving-at-scale.mp4
quiz:
- q: Why is running `docker run` on your laptop inadequate for a production model service?
  options:
  - Docker images are always too large to transfer over the network
  - Laptops are physically unable to execute Python code
  - A single machine offers no high availability, no autoscaling, and only manual, risky rollouts
  - Containers cannot expose network ports outside the host
  answer: 2
  why: One laptop is a single point of failure with fixed capacity. Production needs redundancy across
    machines, automatic scaling under load, and controlled rollouts — none of which a lone `docker run`
    provides.
- q: What is typically the first step when deploying a container image to a managed cloud ML service?
  options:
  - Push the built image to a container registry the service can pull from
  - Email the image file to the cloud provider's support team
  - Rewrite the model in the provider's proprietary serving language
  - Delete Docker and upload the raw Python source files instead
  answer: 0
  why: Managed services deploy from an image stored in a registry such as Amazon ECR, Google Artifact
    Registry, or Azure Container Registry. You push once, then point the endpoint at the image tag.
- q: In Kubernetes, which object manages a desired number of identical pod replicas and recreates them
    if they fail?
  options:
  - A ConfigMap
  - A Service
  - An Ingress
  - A Deployment
  answer: 3
  why: A Deployment declares the desired replica count and pod template; its controller continuously reconciles
    reality to that desired state, replacing crashed pods and enabling rolling updates.
- q: What do purpose-built serving runtimes like KServe, BentoML, Ray Serve, and Triton add over a hand-rolled
    FastAPI app?
  options:
  - Nothing useful; they are strictly slower than FastAPI in every case
  - Built-in capabilities such as autoscaling, request batching, multi-model serving, and GPU optimization
  - They remove the need to containerize the model at all
  - They only work for image-classification models and nothing else
  answer: 1
  why: 'These runtimes bake in concerns you would otherwise build by hand: dynamic batching, scale-to-zero/autoscaling,
    hosting many models per server, and efficient GPU utilization.'
- q: What is NVIDIA Triton Inference Server primarily optimized for?
  options:
  - Packaging Python applications into pip wheels for distribution
  - Provisioning and managing the underlying Kubernetes cluster nodes
  - High-throughput GPU inference with dynamic batching across multiple frameworks
  - Training large models from scratch on distributed clusters
  answer: 2
  why: Triton is an inference server focused on maximizing GPU throughput — it supports dynamic batching
    and concurrent model execution across backends like TensorRT, PyTorch, and ONNX. It does not train
    models.
- q: When would you choose a fully managed endpoint (SageMaker, Vertex AI, Azure ML) over self-managing
    Kubernetes yourself?
  answer: When you want lower operational burden — the provider handles infrastructure, scaling, patching,
    and uptime — and you are willing to trade some control and flexibility (and often higher per-hour
    cost) for speed and simplicity.
  why: Managed endpoints minimize ops work and are ideal for small teams or when time-to-production matters;
    self-managed Kubernetes offers more control and potentially lower cost at scale but requires real
    platform expertise.
resources:
- label: 'Amazon SageMaker: Deploy Models for Inference'
  url: https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html
- label: 'Kubernetes Docs: Deployments'
  url: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- label: 'KServe: Kubernetes-Native Model Serving'
  url: https://kserve.github.io/website/
- label: 'Google Cloud Run: Deploying Container Images'
  url: https://cloud.google.com/run/docs/deploying
---

## From `docker run` on Your Laptop to the Cloud

Earlier you containerized a model. Running `docker run -p 8000:8000 my-model` proves the image works — but it is not production. A single container on one machine has three fatal gaps:

- **No high availability:** if the process crashes or the machine reboots, the service is simply down.
- **No autoscaling:** fixed capacity means spikes cause timeouts while idle periods waste money.
- **No safe rollout:** shipping a new version means stopping the old one, with no gradual rollout or rollback.

The cloud solves these by running **many replicas across many machines**, behind a load balancer, managed by a control plane that restarts failures and scales on demand.

## Step 1: Push to a Registry, Run on a Managed Service

Cloud services deploy from an **image in a container registry**, not from your local Docker daemon. The flow is: build, tag, push, then point a managed endpoint at the image.

```bash
# Tag and push to a registry (Amazon ECR shown; GCP Artifact Registry / Azure ACR are analogous)
docker build -t my-model:1.0 .
docker tag my-model:1.0 123456789.dkr.ecr.us-east-1.amazonaws.com/my-model:1.0
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/my-model:1.0
```

Managed ML endpoints then take that image and run it for you with autoscaling, health checks, and HTTPS built in. The big-three options:

- **AWS SageMaker** — real-time and serverless inference endpoints.
- **Google Cloud Vertex AI** — online prediction endpoints from a custom container.
- **Azure Machine Learning** — managed online endpoints.

They differ in API, but the mental model is identical: *registry image in, scalable HTTPS endpoint out.*

## Kubernetes Basics for ML Serving

When you need more control than a managed endpoint, **Kubernetes (K8s)** is the standard. Four objects matter for serving:

- **Pod** — the smallest unit; one or more containers sharing a network namespace.
- **Deployment** — declares *how many* identical replicas you want and keeps them running, enabling rolling updates and rollback.
- **Service** — a stable DNS name that load-balances traffic across the pods.
- **HorizontalPodAutoscaler (HPA)** — adds or removes replicas based on CPU, memory, or custom metrics.

A minimal Deployment plus Service for our model:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-model
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-model
  template:
    metadata:
      labels:
        app: my-model
    spec:
      containers:
        - name: server
          image: 123456789.dkr.ecr.us-east-1.amazonaws.com/my-model:1.0
          ports:
            - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: my-model
spec:
  selector:
    app: my-model
  ports:
    - port: 80
      targetPort: 8000
```

With `replicas: 3` you immediately get redundancy and load spreading — the core reason to use K8s for multi-replica serving.

## Horizontal Autoscaling

Fixed replicas still waste money or fall over under load. An HPA scales the Deployment automatically:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-model
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-model
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

Now Kubernetes keeps average CPU near 70%, scaling between 2 and 10 pods as traffic changes.

## Purpose-Built Serving Runtimes

Hand-rolling FastAPI is fine for one model, but production serving has recurring needs. **Purpose-built runtimes** provide them out of the box:

- **KServe** — Kubernetes-native model serving with autoscaling (including scale-to-zero), canary rollout, and a standard inference protocol.
- **BentoML** — focuses on packaging and serving: bundle model, code, and dependencies into a deployable artifact with adaptive batching.
- **Ray Serve** — scalable Python-first serving; compose multiple models and scale across a Ray cluster.
- **NVIDIA Triton** — high-throughput GPU inference with **dynamic batching** and concurrent models across TensorRT, PyTorch, and ONNX backends.

The common wins over a bare API are **continuous/dynamic batching** (grouping concurrent requests to use the GPU efficiently), **multi-model hosting**, and **GPU-aware autoscaling** — work you would otherwise build yourself.

## From Model Registry to Deployment

A **model registry** (MLflow Registry, SageMaker Model Registry, Vertex Model Registry) is the handoff point between training and serving. Training produces and registers versions; deployment pulls the **approved** version and serves it.

```python
import mlflow

# Pull the version currently promoted to Production, not a hardcoded path
model = mlflow.pyfunc.load_model("models:/fraud-detector@champion")
prediction = model.predict(features)
```

This decouples *what* is deployed from *how*: the serving config references a version alias, so promoting a new model is a registry action and the same image serves whichever version the registry points to.

## Choosing an Approach

There is no single right answer — it is a trade-off:

- **Managed endpoint (SageMaker / Vertex AI / Azure ML):** lowest operational burden; the provider handles infra, scaling, and patching. Best for small teams and fast time-to-production. Trade-offs: less control and often higher per-hour cost.
- **Self-managed Kubernetes (+ KServe/Triton):** maximum control and flexibility, portable across clouds, potentially cheaper at large scale. Trade-off: you own the platform and need real K8s expertise.

Start managed when you can; reach for Kubernetes when scale, cost, custom hardware, or portability demands it.
