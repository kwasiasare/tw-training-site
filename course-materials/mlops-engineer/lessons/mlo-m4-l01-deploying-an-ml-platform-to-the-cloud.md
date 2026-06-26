---
course: mlops-engineer
title: Deploying an ML Platform to the Cloud
month: 4
monthTitle: Cloud Deployment, Monitoring & Capstone
lesson: 1
summary: Provision a managed Kubernetes cluster and supporting cloud services to host a production model
  serving stack, covering infrastructure-as-code, networking, autoscaling, and secure deployment.
objectives:
- Choose an appropriate managed Kubernetes service and supporting cloud resources for ML serving
- Provision a cluster and its dependencies reproducibly using infrastructure-as-code
- Deploy a containerized model serving stack with proper resource requests, autoscaling, and ingress
- Configure secure access, secrets management, and IAM for cloud-hosted workloads
- Validate the deployment and prepare it for monitoring and the capstone project
video: mlo-m4-l01-deploying-an-ml-platform-to-the-cloud.mp4
quiz:
- q: Why use infrastructure as code instead of the cloud console for production clusters?
  options:
  - It is faster to type
  - It makes infrastructure reproducible, version-controlled, and reviewable
  - It removes the need for IAM
  - It eliminates all cloud costs
  answer: 1
  why: IaC tools like Terraform give you reproducible, version-controlled, peer-reviewable infrastructure,
    which manual console clicking cannot.
- q: What is the primary purpose of a HorizontalPodAutoscaler?
  options:
  - To add more nodes to the cluster
  - To scale the number of pod replicas based on metrics
  - To manage secrets
  - To build container images
  answer: 1
  why: The HPA scales the number of pod replicas up or down based on CPU, memory, or custom metrics; node
    scaling is handled by the Cluster Autoscaler.
- q: Which approach is best for giving pods cloud permissions?
  options:
  - Bake access keys into the container image
  - Use workload identity (IRSA or Workload Identity) with scoped IAM roles
  - Share one root key across all pods
  - Disable IAM entirely
  answer: 1
  why: Workload identity lets pods assume scoped, short-lived IAM roles, avoiding long-lived static credentials
    embedded in images.
- q: Why separate GPU workloads into their own node pool with taints?
  options:
  - GPUs cannot run Kubernetes
  - To prevent non-GPU pods from consuming costly GPU nodes and allow scaling to zero
  - Taints make pods faster
  - It is required for TLS
  answer: 1
  why: A dedicated, tainted GPU pool ensures only GPU workloads land there and can scale to zero when
    idle, controlling cost.
- q: Name the Kubernetes resource that exposes external HTTPS traffic and routes it to a Service.
  answer: Ingress
  why: An Ingress (with an ingress controller) handles external routing and TLS termination, forwarding
    traffic to internal Services.
- q: What should you set on containers so the scheduler can pack pods and the autoscaler can react correctly?
  answer: Resource requests and limits
  why: CPU and memory requests and limits let the scheduler place pods efficiently and let the Cluster
    Autoscaler decide when to add nodes.
resources:
- label: Terraform AWS EKS Module
  url: https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest
- label: Kubernetes Horizontal Pod Autoscaler Docs
  url: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- label: GKE Workload Identity Guide
  url: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity
- label: Helm Documentation
  url: https://helm.sh/docs/
---

## Why Cloud Deployment for ML Platforms

Local or single-VM serving works for prototypes, but production model serving needs elastic compute, high availability, rolling updates, and integration with storage, logging, and identity systems. Managed Kubernetes (EKS, GKE, AKS) gives you a control plane that the cloud provider maintains, while you focus on workloads.

A typical ML platform on the cloud includes:

- **Compute**: a managed Kubernetes cluster with CPU and (optionally) GPU node pools.
- **Storage**: object storage (S3/GCS/Blob) for model artifacts and a managed database for metadata.
- **Networking**: a load balancer / ingress controller, DNS, and TLS.
- **Identity & secrets**: IAM roles for workloads and a secrets manager.
- **Registry**: a container registry for your serving images.

## Infrastructure as Code (IaC)

Never click your production infra into existence. Use **Terraform** (or Pulumi/CloudFormation) so the cluster is reproducible, version-controlled, and reviewable.

```hcl
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "ml-platform"
  cluster_version = "1.29"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  eks_managed_node_groups = {
    cpu = {
      instance_types = ["m6i.large"]
      min_size       = 2
      max_size       = 6
      desired_size   = 2
    }
  }
}
```

Keep state in a remote backend (e.g. an S3 bucket with locking) so a team can collaborate safely.

## Node Pools and Resource Planning

Separate node pools by workload type:

- A **CPU pool** for lightweight inference and platform services.
- A **GPU pool** (taints + tolerations) for heavy models, scaled to zero when idle to save cost.

Always set CPU/memory **requests and limits** so the scheduler can pack pods and the **Cluster Autoscaler** (or Karpenter) can add nodes when needed.

## Deploying the Serving Stack

Package deployment with Helm or Kustomize. A Deployment runs replicas of your model server, a Service exposes it internally, and an Ingress routes external traffic with TLS.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-server
spec:
  replicas: 2
  selector:
    matchLabels: { app: model-server }
  template:
    metadata:
      labels: { app: model-server }
    spec:
      containers:
        - name: server
          image: <registry>/model-server:1.2.0
          ports: [{ containerPort: 8080 }]
          resources:
            requests: { cpu: "500m", memory: "1Gi" }
            limits:   { cpu: "1",    memory: "2Gi" }
          readinessProbe:
            httpGet: { path: /ready, port: 8080 }
```

Add a **HorizontalPodAutoscaler** to scale replicas on CPU or custom latency metrics:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: model-server }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: model-server }
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
```

## Security and Access

- Use **workload identity** (IRSA on AWS, Workload Identity on GKE) so pods assume scoped IAM roles instead of long-lived keys.
- Store credentials in a **secrets manager** and mount them, never bake them into images.
- Lock down the cluster API endpoint, use private subnets for nodes, and apply **network policies**.
- Pull images from a private registry and scan them for vulnerabilities.

## Validation Checklist

Before declaring success: confirm `kubectl get pods` shows Ready, hit the ingress endpoint over HTTPS, send a real inference request, trigger load to verify the HPA scales, and check that artifacts load from object storage. This deployment becomes the foundation for the monitoring and observability work in the next lessons and your capstone.
