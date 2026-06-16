---
course: helpdesk-tier3-advanced
title: 'Automating remediation with AI: guardrails and approvals'
month: 4
monthTitle: AIOps, Monitoring & Agentic Automation
lesson: 6
summary: 'Cross from recommendation into action safely: design approval gates, blast-radius limits, staged
  rollout, and rollback so AI-assisted remediation never causes a fleet-wide incident.'
objectives:
- Separate the recommendation path from the action path with an explicit human approval gate
- Classify remediations by risk and reversibility to decide what may ever be automated
- Limit blast radius with ring-based rollout, canaries, and per-action quotas
- Run remediation under least privilege using scoped, time-bound, audited credentials
- Build automatic verification and rollback so failed changes self-correct or stop
- Maintain a complete audit trail linking alert, evidence, approval, action, and outcome
video: ht4-l06-automating-remediation-with-ai.mp4
quiz:
- q: Where must the human approval gate sit in an AI-assisted remediation pipeline?
  options:
  - Between the AI's recommendation and any consequential change to devices
  - After the action has run
  - Only at the end of the month in a report
  - It is optional if the model is accurate
  answer: 0
  why: The gate must sit before the consequential action so a wrong recommendation is caught before it
    executes; approving after the fact defeats the purpose.
- q: Which remediation is the strongest candidate for fuller automation (with approval) and which should
    stay tightly gated?
  options:
  - Re-imaging fleet-wide is safe; clearing a temp cache is dangerous
  - Clearing a known-safe temp cache is low-risk/reversible; bulk credential rotation or wipe is high-risk/irreversible
    and must stay tightly gated
  - Both are equally safe to fully automate
  - Neither should ever be automated under any circumstances
  answer: 1
  why: 'Risk and reversibility drive automation eligibility: low-risk reversible actions can be more automated;
    high-risk or irreversible actions require strong gates and may never be fully autonomous.'
- q: What is the purpose of ring-based (canary) rollout for an automated remediation?
  options:
  - To make the change faster
  - To avoid needing approval
  - To limit blast radius by applying the change to a small ring first and verifying before expanding
  - To bypass audit logging
  answer: 2
  why: 'Ring/canary rollout contains the blast radius: if the action harms the small first ring, you stop
    before it reaches the whole fleet.'
- q: Why must automated remediation run under scoped, time-bound credentials rather than a standing admin
    account?
  options:
  - To save licensing costs
  - 'Least privilege: limiting permissions and lifetime caps the damage of a flawed or compromised action
    and shrinks the attack surface'
  - Because admin accounts are slower
  - It is a cosmetic preference
  answer: 1
  why: Scoped, just-in-time, time-bound credentials enforce least privilege so a buggy or abused automation
    cannot exceed its intended reach or persist beyond its task.
- q: Describe the minimum elements an audit trail for an AI-assisted remediation should capture, and why.
  answer: It should link the originating alert, the evidence the AI used, the AI's recommendation and
    confidence, who approved it (and when), the exact action taken with its scope, and the verified outcome
    (success/failure/rollback). This end-to-end record makes every automated change explainable, reviewable,
    and reversible, and supports incident analysis and compliance.
  why: A complete chain from alert to outcome is what makes AI-assisted action accountable and lets you
    reconstruct or roll back any change.
- q: Explain the role of automatic verification and rollback in a remediation pipeline, with an example.
  answer: After an action runs, the pipeline checks whether the intended healthy state was achieved (for
    example, re-querying compliance after pushing a config); if verification fails or health worsens,
    it halts the rollout and rolls back the change (reverting the config and flagging for a human). This
    turns a single bad action into a contained, self-correcting event instead of a spreading outage.
  why: Verify-then-rollback closes the loop so failures are caught and undone automatically rather than
    propagating across the fleet.
resources:
- label: Microsoft Learn — Use Scripts and remediations in Intune
  url: https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations
- label: Microsoft Learn — Create a deployment ring strategy (rings)
  url: https://learn.microsoft.com/en-us/windows/deployment/update/waas-deployment-rings-windows-updates
- label: Microsoft Learn — Azure RBAC and least privilege best practices
  url: https://learn.microsoft.com/en-us/azure/role-based-access-control/best-practices
- label: Microsoft Learn — What is Microsoft Security Copilot?
  url: https://learn.microsoft.com/en-us/copilot/security/microsoft-security-copilot
---

## The line between recommend and act

Everything so far has been read-only and safe. This lesson crosses the line into **action** — the one stage that can cause real harm. The non-negotiable rule from lesson one returns here as architecture: a **human approval gate** sits *between* the AI's recommendation and any consequential change. Approving after the action has run is not a gate; it is a post-mortem.

```text
[Alert] -> [AI triage: evidence + recommendation + confidence]
        -> [HUMAN APPROVAL GATE]   <-- the change happens only past here
        -> [Scoped action] -> [Verify] -> [Rollback if failed]
```

## Classify by risk and reversibility

Not all remediations are equal. Sort every candidate action on two axes: **risk** (how bad if wrong) and **reversibility** (can you undo it). Low-risk, reversible actions — clearing a known-safe temp cache, restarting a stuck service — can be more automated, still behind approval. High-risk or irreversible actions — bulk credential rotation, wipe, re-image — stay tightly gated and may never be fully autonomous. *Reversibility is the deciding factor: if you cannot undo it, a human owns it.*

## Limit the blast radius

Even an approved action should not hit the whole fleet at once. Use **ring-based (canary) rollout**: apply to a small first ring, verify, then expand.

```text
Ring 0: 5 pilot devices    -> verify healthy -> proceed
Ring 1: 5% of fleet        -> verify healthy -> proceed
Ring 2: 50% -> Ring 3: 100%  (halt instantly on regression)
```

Add **per-action quotas** ('never touch more than N devices per hour') so a runaway automation trips a limit instead of cascading.

## Run under least privilege

Automated remediation must never use a standing admin account. Use **scoped, time-bound, just-in-time** credentials: the minimum permissions, granted for the duration of the task, and revoked after.

```python
# Conceptual: request a narrow, expiring grant for one task
grant = request_jit_access(
    scope="intune:device.config.write",   # nothing wider
    devices=ring_0_device_ids,             # only this ring
    ttl_minutes=15,                        # expires fast
    reason=approval_ticket_id,             # tied to the approval
)
```

## Verify, then roll back

An action is not done when it runs — it is done when it is **verified**. After each step, re-check the intended healthy state; if it failed or health worsened, **halt and roll back** automatically.

```kql
// Verify: did the pushed config actually make the ring compliant?
DeviceInfo
| where DeviceId in (ring_0_device_ids)
| where TimeGenerated > ago(15m)
| summarize compliant = countif(ComplianceState == "Compliant"), total = count()
```

If `compliant` is not `total`, the pipeline stops, reverts, and flags a human. A single bad action becomes a contained event, not a spreading outage.

## The audit trail ties it together

Every automated change must be reconstructable end to end: the **alert**, the **evidence**, the **AI recommendation and confidence**, **who approved it and when**, the **exact scoped action**, and the **verified outcome**. This chain makes AI-assisted action accountable, reviewable, and reversible — and it is what your security and compliance teams will rightly demand.

## Your task

Take one recommendation from your lesson-5 triage agent. Design its full action path: write the approval gate, classify the action by risk and reversibility, define a ring rollout and a per-action quota, specify the scoped just-in-time credential it needs, and write the KQL verification check plus the rollback trigger. List the six fields your audit trail will record.
