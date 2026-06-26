---
course: cloud-security-engineer
title: Microsoft Defender for Cloud and Cloud Security Posture Management
month: 4
monthTitle: Cloud SIEM & SOAR Operations with Microsoft Sentinel
lesson: 4
summary: 'Microsoft Defender for Cloud is the posture-and-protection plane for your multicloud estate:
  it tells you how secure your Azure, AWS, and GCP resources are, and it actively defends workloads. This
  lesson separates the two halves of the product, free foundational Cloud Security Posture Management
  versus the paid Defender CSPM plan, and shows how Secure Score, recommendations, and the Microsoft Cloud
  Security Benchmark drive measurable improvement. You will connect AWS and GCP with multicloud connectors,
  use agentless scanning, attack path analysis, and the cloud security graph to find the toxic combinations
  attackers exploit, and turn on Defender workload plans for servers, storage, SQL, containers, and Key
  Vault. Finally you export Defender recommendations and alerts into Microsoft Sentinel so posture and
  detection live in one SOC. The throughline is multicloud posture management and benchmark-driven remediation.'
objectives:
- Distinguish foundational (free) CSPM from the paid Defender CSPM plan and what each adds
- Interpret Secure Score and prioritize recommendations to improve posture measurably
- Use the Microsoft Cloud Security Benchmark and the regulatory compliance dashboard
- Enable Defender workload plans for servers, storage, SQL, containers, and Key Vault
- Connect AWS and GCP with multicloud connectors and apply agentless scanning
- Use attack path analysis and the cloud security graph to find toxic combinations
- Remediate recommendations and export findings/alerts to Microsoft Sentinel
video: cse-m4-l04-defender-for-cloud-and-cspm.mp4
quiz:
- q: What capability is included in foundational (free) CSPM but requires the paid Defender CSPM plan
    to unlock?
  options:
  - Secure Score and basic security recommendations are free; attack path analysis and the cloud security
    graph require Defender CSPM
  - Everything in Defender for Cloud is free; there is no paid CSPM tier
  - Secure Score requires Defender CSPM; recommendations are free
  - Agentless scanning is free; Secure Score is paid
  answer: 0
  why: Foundational CSPM is free and provides Secure Score, asset inventory, and core MCSB recommendations
    across connected clouds. The paid Defender CSPM plan adds advanced capabilities such as attack path
    analysis, the cloud security graph (security explorer), agentless scanning enhancements, and more,
    for prioritized, risk-based remediation.
- q: What does Secure Score represent in Microsoft Defender for Cloud?
  options:
  - The number of resources you have deployed
  - A measure of your security posture, calculated from the recommendations you have and have not remediated
  - Your monthly Azure spend on security tooling
  - The count of active alerts in the last 24 hours
  answer: 1
  why: 'Secure Score aggregates your security recommendations into a single percentage that reflects posture:
    remediating recommendations (which are grouped into security controls) raises the score. It gives
    leadership a trendable KPI and helps teams prioritize the changes that most improve security.'
- q: What is the Microsoft Cloud Security Benchmark (MCSB)?
  options:
  - A performance benchmark for VM sizing
  - The default set of security best-practice controls Defender for Cloud assesses resources against
  - A billing optimization tool
  - A penetration-testing framework
  answer: 1
  why: The MCSB is Microsoft's canonical set of cloud security best-practice controls (mapped to standards
    like CIS and NIST). It is the default initiative Defender for Cloud uses to generate recommendations
    and Secure Score, and it spans Azure, AWS, and GCP so posture is assessed consistently across clouds.
- q: How does Defender for Cloud assess AWS and GCP workloads?
  options:
  - It cannot; it only supports Azure
  - You install the Azure portal on each AWS/GCP account
  - You create multicloud connectors that link the AWS account or GCP project for posture and optional
    workload protection
  - You manually upload CSV exports of AWS/GCP config each day
  answer: 2
  why: Multicloud connectors onboard AWS accounts and GCP projects into Defender for Cloud, pulling configuration
    for CSPM (recommendations, Secure Score, MCSB) and optionally enabling workload protection plans,
    so a single pane assesses and protects all three clouds consistently.
- q: What is the primary value of attack path analysis and the cloud security graph?
  options:
  - They lower ingestion cost in Log Analytics
  - They surface exploitable chains of risks (toxic combinations) that together expose a critical asset,
    so you fix what matters most
  - They automatically patch all vulnerabilities
  - They replace the need for Defender workload plans
  answer: 1
  why: The cloud security graph models resources, their relationships, exposures, and vulnerabilities;
    attack path analysis traverses it to show concrete chains, for example an internet-exposed VM with
    a critical CVE and a managed identity that can reach sensitive storage, so you remediate the few combinations
    that actually lead to breach rather than chasing thousands of isolated findings.
- q: In 3-4 sentences, explain why exporting Defender for Cloud recommendations and alerts into Microsoft
    Sentinel strengthens a SOC, and name one mechanism used to do it.
  answer: Exporting brings posture findings and workload-protection alerts from Defender for Cloud into
    the same Sentinel workspace where identity, endpoint, and network telemetry already live, so analysts
    correlate a weak posture (for example an exposed, unpatched VM) with active attack signals in one
    incident queue instead of switching consoles. It lets you write analytics rules, hunts, and automation
    that combine posture and detection, and it preserves the multicloud context across Azure, AWS, and
    GCP. One mechanism is the Microsoft Defender for Cloud (or Tenant-based) data connector in Sentinel,
    which streams Defender for Cloud alerts (and recommendations via continuous export) into the workspace.
    This unifies posture management and threat detection under a single SOC workflow.
  why: Centralizing Defender for Cloud alerts and recommendations in Sentinel lets the SOC correlate posture
    weaknesses with live threats and automate response; the Defender for Cloud connector plus continuous
    export is the standard mechanism.
resources:
- label: Microsoft Defender for Cloud overview
  url: https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction
- label: Secure Score in Defender for Cloud
  url: https://learn.microsoft.com/en-us/azure/defender-for-cloud/secure-score-security-controls
- label: Identify and remediate attack paths
  url: https://learn.microsoft.com/en-us/azure/defender-for-cloud/how-to-manage-attack-path
- label: Connect AWS accounts to Defender for Cloud
  url: https://learn.microsoft.com/en-us/azure/defender-for-cloud/quickstart-onboard-aws
---

## Two Jobs: Posture and Protection

Microsoft Defender for Cloud (DfC) does two distinct jobs, and senior engineers keep them separate in their heads:

1. **Cloud Security Posture Management (CSPM)** — *Are my resources configured securely?* This is continuous assessment of configuration against best practices, producing **recommendations** and a **Secure Score** across Azure, AWS, and GCP.
2. **Cloud Workload Protection (CWPP)** — *Is anything actively attacking my workloads?* This is the **Defender plans** (servers, storage, SQL, containers, Key Vault, and more) that generate runtime security **alerts**, which we feed into Sentinel.

Posture reduces the attack surface *before* an incident; protection detects and responds *during* one. You need both.

## Foundational CSPM vs. Defender CSPM

CSPM comes in two tiers:

- **Foundational CSPM (free)** — on by default for any connected cloud. Gives you **asset inventory**, **Secure Score**, and core **recommendations** based on the **Microsoft Cloud Security Benchmark**. This alone is enormously valuable and costs nothing.
- **Defender CSPM (paid plan)** — adds the advanced, risk-based capabilities: **attack path analysis**, the **cloud security graph / security explorer**, broader **agentless scanning** (machine vulnerabilities, secrets, sensitive-data awareness), **governance rules** for assigning and tracking remediation, and code-to-cloud context. This is what turns thousands of findings into the *handful that actually matter*.

The pattern: start free to get visibility and Secure Score, then enable Defender CSPM where you need risk prioritization.

## Secure Score and Recommendations

**Secure Score** is a single percentage summarizing posture. Recommendations are grouped into **security controls**, each worth points; remediating the resources under a control raises the score. Treat Secure Score as a **trendable KPI** for leadership and a **prioritization engine** for engineers.

How to work it:

- Sort recommendations by **potential score increase** and by **risk level** (Defender CSPM adds risk-based prioritization that considers exploitability and blast radius, which is far better than raw count).
- Use the **Fix** button where DfC offers one-click remediation, or the **automated remediation / Logic App** for bulk fixes.
- Track improvement over time; a rising Secure Score is concrete evidence your hardening is working.

## The Microsoft Cloud Security Benchmark and Compliance Dashboard

The **Microsoft Cloud Security Benchmark (MCSB)** is the **default standard** DfC assesses against. It is Microsoft's curated set of cloud security controls, mapped to industry frameworks (CIS, NIST, PCI DSS), and crucially it spans **Azure, AWS, and GCP**, so you get consistent recommendations everywhere.

The **regulatory compliance dashboard** layers additional standards on top. You assign initiatives like **CIS**, **NIST SP 800-53**, **PCI DSS**, or **ISO 27001**, and DfC continuously reports your pass/fail status per control, with drill-down to the failing resources. This turns audit prep from a quarterly fire drill into a live dashboard.

## Defender Workload Protection Plans

The paid **Defender plans** protect specific workload types. Enable the ones matching your estate:

- **Defender for Servers** — vulnerability assessment, just-in-time VM access, file integrity monitoring, and EDR via integration with Defender for Endpoint.
- **Defender for Storage** — detects malware uploads and suspicious access to blobs, with on-upload malware scanning.
- **Defender for SQL** (and open-source databases) — finds vulnerabilities and detects anomalous, potentially malicious database activity.
- **Defender for Containers** — image vulnerability scanning (registry and runtime), Kubernetes hardening, and runtime threat detection.
- **Defender for Key Vault** — alerts on unusual secret/key access that may indicate credential theft.

Each plan emits **alerts** in DfC; those alerts are what we export to Sentinel for SOC triage and automation.

## Multicloud: AWS and GCP Connectors, Agentless Scanning

Most enterprises are multicloud, and DfC is designed for it. You create a **multicloud connector** that onboards an **AWS account** or **GCP project** (via a CloudFormation template / Terraform or GCP equivalent that establishes the trust). Once connected, those resources flow into the **same** Secure Score, MCSB recommendations, and (optionally) workload protection.

**Agentless scanning** is the modern default: DfC takes point-in-time snapshots of VM disks (across Azure, AWS, and GCP) to assess **vulnerabilities, installed software, and exposed secrets without installing an agent** on every machine, eliminating coverage gaps from missing agents. Agent-based options remain for deeper, real-time signals where you need them.

## Attack Path Analysis and the Cloud Security Graph

The most powerful Defender CSPM feature. The **cloud security graph** models every resource, its relationships, network exposure, identities, and vulnerabilities as a graph. **Attack path analysis** traverses that graph to surface concrete **exploitable chains** — the *toxic combinations* attackers actually use.

Example path: *Internet-exposed VM → has a critical, exploitable CVE → carries a managed identity → that identity has read access to a storage account holding sensitive data.* No single recommendation captures that, but the chain is a real breach path. You fix it by breaking **any one link** (remove exposure, patch the CVE, or scope down the identity). The companion **cloud security explorer** lets you **query** the graph ("show internet-exposed VMs with high-severity CVEs that can reach sensitive data") to hunt for risk proactively. This is how you move from drowning in findings to fixing the few that prevent breach.

## Remediate and Export to Sentinel

Remediation paths: one-click **Fix**, **governance rules** (assign an owner and due date, with grace periods), and **workflow automation** via Logic Apps for bulk or recurring fixes.

Finally, unify posture and detection in the SOC by **exporting to Microsoft Sentinel**:

- Enable the **Microsoft Defender for Cloud / Tenant-based Microsoft Defender for Cloud** data connector in Sentinel to stream **DfC security alerts** into the workspace.
- Use **continuous export** to push **recommendations and Secure Score** data as well (to Log Analytics / Event Hub), so you can build workbooks and analytics rules on posture.

Once in Sentinel, alerts land in tables you can correlate with identity and endpoint data, and write detections against:

```kusto
// Defender for Cloud high-severity alerts in the last 24h, by affected resource
SecurityAlert
| where TimeGenerated > ago(24h)
| where ProductName has "Defender for Cloud"
| where AlertSeverity in ("High", "Medium")
| extend Resource = tostring(parse_json(ExtendedProperties)["Resource"])
| project TimeGenerated, AlertName, AlertSeverity, CompromisedEntity, Resource
| sort by TimeGenerated desc
```

Now posture weaknesses and active threats live in one place: the SOC can correlate an exposed, unpatched VM (posture) with an active brute-force alert against it (protection) in a single incident — across Azure, AWS, and GCP. That is the multicloud, benchmark-driven security operation this module set out to build.
