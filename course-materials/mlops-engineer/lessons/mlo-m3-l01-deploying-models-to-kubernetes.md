---
course: mlops-engineer
title: Deploying Models to Kubernetes
month: 3
monthTitle: Orchestration, CI/CD & Infrastructure as Code
lesson: 1
summary: 'Learn how to deploy a containerized model API to a Kubernetes cluster using core objects: Pods,
  Deployments, and Services. This lesson covers writing manifests, exposing your API, applying probes
  and resource limits, and verifying rollouts with kubectl.'
objectives:
- Explain the role of Pods, Deployments, and Services in running a model API on Kubernetes
- Write and apply YAML manifests to deploy a containerized model API
- Expose the model API internally and externally using Service types
- Configure liveness/readiness probes and resource requests/limits for reliability
- Verify, scale, and roll out updates to a deployment using kubectl
video: mlo-m3-l01-deploying-models-to-kubernetes.mp4
quiz:
- q: Which Kubernetes object should you create to run a stateless model API with self-healing and rolling
    updates?
  options:
  - A bare Pod
  - A Deployment
  - A Service
  - A ConfigMap
  answer: 1
  why: A Deployment manages a ReplicaSet of identical Pods and provides scaling, self-healing, and rolling
    updates. You rarely create bare Pods directly.
- q: What is the primary purpose of a Service in Kubernetes?
  options:
  - To store configuration values
  - To provide a stable network endpoint that load-balances across matching Pods
  - To build container images
  - To schedule Pods onto nodes
  answer: 1
  why: Pods are ephemeral and get new IPs; a Service provides a stable virtual IP/DNS name and load-balances
    traffic to Pods matched by its label selector.
- q: Which probe prevents traffic from reaching a Pod whose model weights are still loading?
  options:
  - Liveness probe
  - Startup probe only
  - Readiness probe
  - Resource limit
  answer: 2
  why: The readiness probe signals when a Pod is ready to receive traffic. Until it passes, the Service
    won't route requests to that Pod.
- q: Why should you avoid using the 'latest' image tag in production deployments?
  options:
  - It is slower to pull
  - It makes rollouts and rollbacks unpredictable
  - Kubernetes rejects it
  - It uses more memory
  answer: 1
  why: With 'latest' you can't reliably know which version is running, and rollbacks become unpredictable.
    Pin specific, immutable tags instead.
- q: In a Service manifest, what do 'port' and 'targetPort' refer to respectively?
  answer: port is the port clients use to reach the Service; targetPort is the port the container is listening
    on.
  why: Clients connect to the Service on 'port', which forwards traffic to the Pod's 'targetPort' (the
    containerPort).
- q: Which kubectl command reverts a Deployment to its previous version after a bad release?
  options:
  - kubectl scale deployment model-api --replicas=0
  - kubectl rollout undo deployment/model-api
  - kubectl delete deployment model-api
  - kubectl apply -f old.yaml
  answer: 1
  why: kubectl rollout undo reverts the Deployment to the prior ReplicaSet revision, enabling a quick
    rollback without manually editing manifests.
resources:
- label: Kubernetes Deployments (official docs)
  url: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- label: Kubernetes Services (official docs)
  url: https://kubernetes.io/docs/concepts/services-networking/service/
- label: Configure Liveness, Readiness and Startup Probes
  url: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- label: kubectl Cheat Sheet
  url: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
---

## Why Kubernetes for Model Serving

Once your model API is containerized, you need a way to run it reliably, scale it, and recover from failures. Kubernetes (k8s) is the de-facto orchestrator for this. It schedules containers across a cluster, restarts crashed processes, balances traffic, and enables zero-downtime updates.

For an MLOps engineer, the key insight is that you describe the **desired state** in declarative manifests, and Kubernetes continuously reconciles the cluster to match that state.

## Core Objects

- **Pod**: the smallest deployable unit — one (or a few tightly-coupled) containers sharing network and storage. You rarely create Pods directly.
- **Deployment**: manages a set of identical Pods via a ReplicaSet. Handles scaling, rolling updates, and self-healing. This is what you use for a stateless model API.
- **Service**: a stable network endpoint (virtual IP + DNS name) that load-balances traffic across the Pods matched by a label selector. Pods are ephemeral and get new IPs; a Service gives you a fixed address.

## A Deployment Manifest

A Deployment wraps a Pod template. The `selector` must match the Pod `labels`. Always pin a specific image tag (avoid `latest` in production).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-api
  labels:
    app: model-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: model-api
  template:
    metadata:
      labels:
        app: model-api
    spec:
      containers:
        - name: model-api
          image: registry.example.com/model-api:1.2.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1"
              memory: "1Gi"
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 20
            periodSeconds: 10
```

## Exposing the API with a Service

A Service selects Pods by label and routes traffic to them. Common types:

- **ClusterIP** (default): reachable only inside the cluster — good for internal microservices.
- **NodePort**: opens a port on every node — useful for quick testing.
- **LoadBalancer**: provisions an external load balancer (on cloud providers) — typical for public endpoints.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: model-api
spec:
  type: ClusterIP
  selector:
    app: model-api
  ports:
    - port: 80
      targetPort: 8080
```

Here `port` is the Service port clients hit, and `targetPort` is the container port. For external HTTP traffic you typically front a ClusterIP Service with an **Ingress** controller.

## Probes and Resources Matter

- **Readiness probe**: tells Kubernetes when a Pod can receive traffic. Model APIs often need time to load weights — a readiness probe prevents requests hitting a not-yet-ready Pod.
- **Liveness probe**: restarts a Pod that has hung or deadlocked.
- **Resource requests** drive scheduling; **limits** cap usage. Models can be memory-hungry, so set realistic values to avoid OOM kills and noisy-neighbor problems.

## Applying and Verifying

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

kubectl get pods -l app=model-api
kubectl get deployment model-api
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Test locally without external exposure
kubectl port-forward svc/model-api 8080:80
```

## Scaling and Rolling Updates

```bash
# Scale
kubectl scale deployment model-api --replicas=5

# Update image (triggers a rolling update)
kubectl set image deployment/model-api model-api=registry.example.com/model-api:1.3.0
kubectl rollout status deployment/model-api

# Roll back if something breaks
kubectl rollout undo deployment/model-api
```

Deployments perform rolling updates by default, spinning up new Pods before terminating old ones, giving you zero-downtime releases when probes are configured correctly.

## Common Pitfalls

- Selector labels not matching Pod template labels → Deployment manages nothing.
- Using `latest` tag → unpredictable rollouts and broken rollbacks.
- No readiness probe → traffic sent to Pods still loading models.
- No resource requests → poor scheduling and OOM kills.
