---
course: mlops-engineer
title: Provisioning Infrastructure as Code with Terraform
month: 3
monthTitle: Orchestration, CI/CD & Infrastructure as Code
lesson: 4
summary: Learn to provision reproducible cloud infrastructure for an ML platform using Terraform. This
  lesson covers the declarative workflow, state management, reusable modules, and practical patterns for
  building infrastructure as code that supports MLOps pipelines.
objectives:
- Explain the benefits of Infrastructure as Code (IaC) and Terraform's declarative model for ML platforms
- 'Describe the core Terraform workflow: init, plan, apply, and destroy'
- Manage Terraform state safely using remote backends and state locking
- Build reusable Terraform modules to provision common ML infrastructure components
- Apply best practices for variables, outputs, and environment separation in production
- Integrate Terraform into a CI/CD pipeline for automated infrastructure delivery
video: mlo-m3-l04-provisioning-infrastructure-as-code-with-terrafo.mp4
quiz:
- q: What does the `terraform plan` command do?
  options:
  - Permanently deletes all resources
  - Previews the changes Terraform will make without applying them
  - Downloads the required providers
  - Edits the state file directly
  answer: 1
  why: plan is a dry run that shows what will be added, changed, or destroyed, letting you review before
    applying.
- q: Why should you use a remote backend with state locking for team projects?
  options:
  - It makes Terraform run faster locally
  - It shares state and prevents concurrent applies from corrupting it
  - It removes the need to write HCL
  - It automatically writes your modules
  answer: 1
  why: A remote backend lets the team share state, and locking (e.g., via DynamoDB) prevents simultaneous
    applies that could corrupt the state file.
- q: Which statement about the Terraform state file is correct?
  options:
  - It should be committed to Git for version history
  - It can be safely edited by hand for quick fixes
  - It can contain secrets and should never be committed to Git
  - It is only needed for the destroy command
  answer: 2
  why: State can contain sensitive data, so it must never be committed to version control and should not
    be hand-edited.
- q: What is the main purpose of a Terraform module?
  options:
  - To store credentials securely
  - To package reusable infrastructure that can be instantiated across environments
  - To replace the plan command
  - To encrypt the state file
  answer: 1
  why: Modules are reusable, self-contained packages of configuration that you build once and reuse with
    different inputs across environments.
- q: Name one CI step that should run on a pull request before applying Terraform changes.
  answer: terraform plan (or fmt/validate, or a security scan like tfsec)
  why: Running plan, format checks, validate, and security scanners in CI lets reviewers see and approve
    infrastructure changes before they are applied.
- q: Is Terraform declarative or imperative, and what does that mean in one sentence?
  answer: Declarative — you describe the desired end state and Terraform determines the API calls needed
    to reach it.
  why: Terraform reconciles real infrastructure against your declared desired state rather than executing
    step-by-step commands.
resources:
- label: Terraform Official Documentation
  url: https://developer.hashicorp.com/terraform/docs
- label: 'Terraform: Up & Running (book by Yevgeniy Brikman)'
  url: https://www.terraformupandrunning.com/
- label: HashiCorp Terraform Best Practices
  url: https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices
- label: tfsec — security scanner for Terraform
  url: https://github.com/aquasecurity/tfsec
---

## Why Infrastructure as Code?

Manually clicking through a cloud console to set up GPU instances, buckets, networks, and IAM roles is error-prone and impossible to reproduce. **Infrastructure as Code (IaC)** lets you define your entire ML platform in version-controlled files, so environments are reproducible, auditable, and reviewable like any other code.

Key benefits for MLOps:

- **Reproducibility** – spin up identical dev, staging, and prod environments.
- **Version control** – track every infrastructure change in Git, with PR reviews.
- **Disaster recovery** – rebuild the platform from code if something breaks.
- **Collaboration** – teams share modules instead of tribal knowledge.

## Why Terraform?

Terraform by HashiCorp is a **cloud-agnostic, declarative** IaC tool. You describe the *desired end state* and Terraform figures out the API calls needed to reach it. It supports AWS, GCP, Azure, Kubernetes, and hundreds of providers through a single workflow.

Declarative vs. imperative: you write *what* you want (an S3 bucket, a GKE cluster), not the step-by-step commands. Terraform builds a dependency graph and reconciles reality against your configuration.

## The Core Workflow

Terraform's lifecycle is four commands:

```bash
terraform init     # download providers, configure backend
terraform plan     # preview changes (dry run)
terraform apply    # create/update resources
terraform destroy  # tear down resources
```

Always read the `plan` output before applying — it shows what will be **added, changed, or destroyed**. In production, `plan` runs in CI and a human approves the `apply`.

A minimal configuration:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "model_artifacts" {
  bucket = "my-ml-model-artifacts"
}
```

## State Management

Terraform records what it created in a **state file** (`terraform.tfstate`). State maps your config to real-world resources and stores metadata. **Never edit it by hand**, and **never commit it to Git** — it can contain secrets.

For teams, use a **remote backend** so state is shared and locked:

```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "ml-platform/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"   # state locking
    encrypt        = true
  }
}
```

**State locking** (via DynamoDB here) prevents two engineers from applying at the same time and corrupting state. Always enable encryption for state at rest.

## Variables, Outputs, and Modules

**Variables** parameterize configurations; **outputs** expose values to other systems or modules.

```hcl
variable "instance_type" {
  type    = string
  default = "ml.m5.large"
}

output "bucket_name" {
  value = aws_s3_bucket.model_artifacts.bucket
}
```

**Modules** are reusable, self-contained packages of Terraform configuration. Build a module once (e.g., a training cluster, a feature store bucket) and reuse it across environments:

```hcl
module "training_cluster" {
  source        = "./modules/training-cluster"
  instance_type = "ml.p3.2xlarge"
  node_count    = 3
  environment   = "prod"
}
```

## Environment Separation

Keep dev, staging, and prod isolated. Common patterns:

- **Directory per environment** with shared modules — explicit and easy to reason about.
- **Terraform workspaces** — one config, multiple state files (use cautiously; less explicit).

Use separate state files and ideally separate cloud accounts/projects for blast-radius isolation.

## Terraform in CI/CD

Automate infrastructure delivery just like application code:

1. Engineer opens a PR changing `.tf` files.
2. CI runs `terraform fmt -check`, `terraform validate`, and `terraform plan`.
3. The plan is posted to the PR for review.
4. On merge to main, CI runs `terraform apply` (often with manual approval for prod).

Use tools like **tflint**, **checkov**, or **tfsec** to scan for misconfigurations and security issues before apply. Store cloud credentials as CI secrets or use OIDC federation — never hardcode them.

## Best Practices Recap

- Pin provider and module versions.
- Remote, encrypted, locked state.
- Small, composable modules.
- Never commit state or secrets.
- Always review `plan` before `apply`.
- Run static analysis in CI.
