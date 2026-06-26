---
course: cloud-security-engineer
title: Security as Code and Deployment Governance
month: 5
monthTitle: Security Automation with PowerShell, Graph API & Logic Apps
lesson: 4
summary: Click-ops security configuration drifts, cannot be reviewed, and cannot be rebuilt after an incident.
  Security as Code fixes this by expressing guardrails as version-controlled Bicep, Azure Policy, and
  Graph templates that deploy through a pipeline. This lesson covers Bicep for security resources, Azure
  Policy initiatives with deny and deployIfNotExists effects to enforce guardrails at scale, and exporting
  Sentinel analytics and Conditional Access policies as code. You will wire a GitHub Actions pipeline
  that authenticates to Azure with OIDC workload identity federation, so there are no stored secrets,
  and promote changes from dev to prod behind review gates.
objectives:
- Explain how configuration drift arises and how Security as Code eliminates it
- Author Bicep to deploy security resources idempotently
- Use Azure Policy initiatives with deny and deployIfNotExists to enforce guardrails at scale
- Export and redeploy Sentinel analytics and Conditional Access policies as code
- Authenticate a GitHub Actions pipeline to Azure using OIDC workload identity federation (no secrets)
- Promote changes dev to prod with environment review gates and approvals
video: cse-m5-l04-security-as-code-and-deployment-governance.mp4
quiz:
- q: What problem does Security as Code most directly solve?
  options:
  - It makes Azure resources cheaper to run
  - It eliminates configuration drift by making version-controlled, reviewable, redeployable definitions
    the source of truth
  - It removes the need for Conditional Access policies
  - It encrypts all data at rest automatically
  answer: 1
  why: Click-ops configuration drifts over time and cannot be reviewed or rebuilt reliably. Expressing
    security configuration as code in version control makes it auditable, peer-reviewable, and redeployable,
    so the declared state is the source of truth and drift is corrected by redeploying.
- q: Which Azure Policy effect automatically remediates a non-compliant resource by deploying the missing
    configuration?
  options:
  - deny
  - audit
  - deployIfNotExists
  - disabled
  answer: 2
  why: deployIfNotExists evaluates a resource and, if a required related resource or setting is missing,
    deploys it (via a remediation task with a managed identity). deny blocks non-compliant creation, and
    audit only flags it without changing anything.
- q: What is the main security advantage of OIDC workload identity federation for a GitHub Actions to
    Azure pipeline?
  options:
  - It runs the pipeline faster
  - There is no long-lived client secret to store or rotate; GitHub presents a short-lived federated token
    Azure trusts
  - It grants the pipeline Owner on every subscription
  - It removes the need for an app registration
  answer: 1
  why: With workload identity federation, the GitHub workflow gets a short-lived OIDC token that Azure's
    app registration is configured to trust for a specific repo/branch/environment. No client secret is
    stored in GitHub, eliminating the most common credential-leak vector in CI/CD.
- q: How are Conditional Access policies best managed as code?
  options:
  - They cannot be managed as code and must be clicked in the portal
  - Export them as JSON via Microsoft Graph and redeploy through Graph in the pipeline
  - Store screenshots of the portal in the repo
  - Recreate them by hand in each environment
  answer: 1
  why: Conditional Access policies are Graph objects; you can GET them as JSON and POST/PATCH them back
    through Microsoft Graph. Storing that JSON in version control and deploying it via the pipeline gives
    you reviewable, repeatable CA configuration across tenants/environments.
- q: Why use environment protection rules and a dev-to-prod promotion flow in the pipeline?
  options:
  - To make builds slower on purpose
  - To require review/approval before changes reach production and to validate them in dev first
  - Because Azure bills less for staged deployments
  - To avoid using Bicep entirely
  answer: 1
  why: Promotion from dev to prod lets you validate templates in a low-risk environment first, and environment
    protection rules (required reviewers) gate the production deployment behind human approval. Together
    they prevent an unreviewed change from hitting production guardrails.
- q: In two to four sentences, explain the difference between an Azure Policy 'deny' guardrail and a 'deployIfNotExists'
    guardrail, and give an example use of each in a security baseline.
  answer: 'A deny policy blocks a non-compliant resource from ever being created or updated, so it is
    a hard preventive guardrail, for example denying the creation of any storage account that allows public
    blob access or any NSG rule that opens RDP to the internet. A deployIfNotExists policy instead allows
    the resource but automatically deploys a missing required configuration onto it through a remediation
    task, for example enabling diagnostic settings to send logs to a Log Analytics workspace, or deploying
    the Defender for Cloud agent, whenever a VM is created without it. In short, deny prevents bad state
    up front while deployIfNotExists corrects or completes state after the fact, and a mature baseline
    uses both: deny for things that must never exist, deployIfNotExists for settings that must always
    be present.'
  why: deny is preventive and blocks creation; deployIfNotExists is corrective and remediates missing
    configuration via a managed-identity deployment. A strong baseline combines both, which is the heart
    of policy-as-code guardrails at scale.
resources:
- label: Bicep documentation
  url: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview
- label: Azure Policy effects (deny, deployIfNotExists, audit)
  url: https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-basics
- label: Configure GitHub Actions to authenticate to Azure with OIDC
  url: https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect
- label: Deploy Microsoft Sentinel analytics rules and content as code
  url: https://learn.microsoft.com/en-us/azure/sentinel/ci-cd
---

## The Drift Problem

Every security setting clicked into a portal is a future incident waiting to happen. **Configuration drift** is the slow divergence between what you *think* is configured and what actually is: someone disables a policy to debug an issue and forgets to re-enable it, two environments quietly diverge, and after an outage nobody can rebuild the exact tenant state. Click-ops is unreviewable, unrepeatable, and unauditable.

**Security as Code** is the cure. Express every guardrail, resources, policies, analytics, Conditional Access, as **version-controlled definitions** that deploy through a pipeline. The declared state becomes the single source of truth; drift is corrected simply by redeploying. Changes get a pull request, a peer review, and a history.

## Bicep for Security Resources

**Bicep** is Azure's domain-specific language for declarative, **idempotent** deployments, you describe the desired state and redeploying converges to it. Use it for security resources like Log Analytics workspaces, Defender plans, and storage with secure defaults.

```bicep
param location string = resourceGroup().location
param workspaceName string = 'law-soc-prod'

resource law 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: workspaceName
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 90
  }
}

resource secureStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'stsoclogs${uniqueString(resourceGroup().id)}'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}
```

Because the deployment is idempotent, running it again after someone toggles `allowBlobPublicAccess` to true silently corrects the drift.

## Azure Policy: Guardrails at Scale

Bicep deploys *your* resources; **Azure Policy** governs *everyone's*. Policies evaluate resources across a subscription or management group and apply an **effect**. The three that matter for guardrails:

- **deny** - block non-compliant creation outright (preventive).
- **deployIfNotExists (DINE)** - allow the resource but auto-deploy a missing required setting via a remediation task (corrective).
- **audit** - flag non-compliance without changing anything (visibility).

Group related policies into an **initiative** (policy set) and assign it once to a management group. A deny rule that forbids public blob storage:

```json
{
  "properties": {
    "displayName": "Deny storage accounts with public blob access",
    "policyRule": {
      "if": {
        "allOf": [
          { "field": "type", "equals": "Microsoft.Storage/storageAccounts" },
          { "field": "Microsoft.Storage/storageAccounts/allowBlobPublicAccess", "equals": true }
        ]
      },
      "then": { "effect": "deny" }
    }
  }
}
```

A **deployIfNotExists** policy would instead, for example, deploy diagnostic settings to your Log Analytics workspace whenever a resource is created without them, the remediation runs under a policy-assigned managed identity.

## Sentinel Analytics and Conditional Access as Code

Your detections and access policies are configuration too. **Sentinel analytics rules** can be exported as ARM/Bicep and redeployed, Microsoft's Sentinel CI/CD guidance and the `Microsoft.SecurityInsights/alertRules` resource type let you keep detections in a repo and deploy them per workspace.

**Conditional Access** policies are **Microsoft Graph** objects, so you manage them as code by exporting JSON and pushing it back through Graph:

```powershell
# Export every CA policy to JSON (source of truth in git)
Connect-MgGraph -Scopes 'Policy.Read.All'
Get-MgIdentityConditionalAccessPolicy -All |
    ConvertTo-Json -Depth 20 | Set-Content .\ca\policies.json

# Redeploy in the pipeline (Policy.ReadWrite.ConditionalAccess)
$body = Get-Content .\ca\require-mfa-admins.json -Raw
New-MgIdentityConditionalAccessPolicy -BodyParameter ($body | ConvertFrom-Json -AsHashtable)
```

Now the same MFA-for-admins policy can be reviewed in a PR and deployed identically to every tenant.

## CI/CD with OIDC Workload Identity Federation

The pipeline must authenticate to Azure, and the worst way is a stored client secret in GitHub. The modern way is **OIDC workload identity federation**: the GitHub workflow receives a short-lived OIDC token, and an Entra **app registration with a federated credential** trusts that token for a specific repo, branch, or environment. **No secret is ever stored.**

```yaml
name: deploy-security-baseline
on:
  push:
    branches: [ main ]
permissions:
  id-token: write   # required to request the OIDC token
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: prod   # gated by required reviewers
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      - name: Deploy Bicep baseline
        run: az deployment sub create --location uksouth --template-file ./infra/baseline.bicep
```

Note `id-token: write`, that permission lets the job mint the OIDC token `azure/login` exchanges for an Azure access token. The three values passed are public identifiers (client/tenant/subscription IDs), not secrets.

## Environment Promotion and Review Gates

Never let a change hit production unreviewed. Use a **dev to prod promotion** flow: deploy and validate in **dev** first, then promote to **prod**. GitHub **environment protection rules** (or Azure DevOps approvals) require named reviewers before the prod job runs, exactly the dev-test-approve-prod discipline.

```yaml
  deploy-dev:
    environment: dev
    # ... deploys on every push, fast feedback

  deploy-prod:
    needs: deploy-dev
    environment: prod   # required reviewers must approve here
    if: github.ref == 'refs/heads/main'
```

The `prod` environment's protection rule pauses the run until a reviewer approves. Combined with policy guardrails and OIDC, you get a pipeline where security configuration is reviewed, secret-free, validated in dev, approved, and deployed identically every time, drift eliminated by design.
