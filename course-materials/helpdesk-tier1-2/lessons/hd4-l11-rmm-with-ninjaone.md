---
course: helpdesk-tier1-2
title: 'RMM with NinjaOne: managing the whole fleet'
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 11
summary: Meet Remote Monitoring and Management (RMM) — the platform support teams use to monitor, patch,
  automate and remote into an entire fleet of devices — using NinjaOne as a worked example.
objectives:
- Explain what an RMM platform is and the role of the agent
- Contrast proactive RMM with reactive one-to-one remote support
- 'List the core RMM capabilities: monitoring, alerting, patching, scripting, remote access, reporting'
- Describe how a Tier 1/2 technician uses NinjaOne day to day
- Explain why RMM access is a security-sensitive, high-privilege target
- Name common RMM alternatives and how the concepts transfer
video: hd4-l11-rmm-with-ninjaone.mp4
quiz:
- q: What does RMM stand for, and what is its core purpose?
  options:
  - Remote Machine Maintenance — to image PCs
  - Remote Monitoring and Management — to monitor and manage a fleet of devices from one console
  - Rapid Malware Mitigation — to remove viruses
  - Resource Metering Module — to bill customers
  answer: 1
  why: 'RMM = Remote Monitoring and Management: agent-based monitoring, patching, automation and remote
    access across many devices from a single console.'
- q: How does an RMM differ from a remote-support tool like Quick Assist?
  options:
  - It is the same thing with a different name
  - RMM agents are always on and proactive across the whole fleet; remote support is reactive, one machine
    at a time
  - RMM only works on servers
  - Remote support can patch; RMM cannot
  answer: 1
  why: Remote support is ad-hoc remote control of a single machine on request; RMM runs always-on agents
    to monitor and manage the entire fleet proactively.
- q: Which of these is a typical RMM capability?
  options:
  - Designing the office network cabling
  - Patch management across the fleet
  - Replacing a failed motherboard
  - Negotiating the SLA contract
  answer: 1
  why: Patch management — approving and deploying updates across many devices on a schedule — is a core
    RMM feature.
- q: Why is the RMM console a high-value target for attackers?
  options:
  - It stores customer credit cards
  - Its agents run with high privilege on every endpoint, so it can push code to the whole fleet
  - It is always offline
  - It cannot use MFA
  answer: 1
  why: RMM agents are high-privilege on every device; abusing the console lets an attacker push malware
    fleet-wide — which is why MFA and least privilege are essential.
- q: Name two things a Tier 1/2 technician would do in an RMM console on a typical day.
  answer: Triage dashboard alerts (e.g. low disk, failed backup) and act on a device — run an automation/script,
    approve patches, or remote in to fix an issue.
  why: 'Daily RMM work is alert triage plus acting on devices: scripts/automations, patching, and remote
    access, with tickets kept in sync.'
- q: Name two RMM platforms other than NinjaOne.
  answer: 'Any two of: Datto RMM, ConnectWise Automate, Atera, Kaseya (Microsoft Intune overlaps for cloud
    device management).'
  why: The market has several RMMs; the concepts transfer, so learning one prepares you for the rest.
resources:
- label: NinjaOne — What is RMM? (guide)
  url: https://www.ninjaone.com/what-is-rmm/
- label: NinjaOne documentation
  url: https://www.ninjaone.com/docs/
- label: CISA — Protecting against malicious use of remote monitoring and management software
  url: https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-025a
- label: Atera — RMM explained (vendor-neutral primer)
  url: https://www.atera.com/blog/what-is-rmm/
---

## What RMM actually is

A **Remote Monitoring and Management** tool — RMM for short — is the platform IT teams use to look after *every* computer they are responsible for, all from one screen. You install a small background program called an **agent** on each device, and from then on the RMM can see the machine's health, alert you when something is wrong, install updates, run scripts, and let you remote in — across hundreds or thousands of devices at once.

This is the day-to-day cockpit for support teams in managed service providers (MSPs) and in-house IT departments alike. **NinjaOne** is one of the most popular modern RMM platforms, and it is a great example to learn the concepts on.

## RMM vs. the remote-support tools you already met

In the remote-support lesson you learned to connect *into one machine* when a user asks for help — that is reactive and one-at-a-time. RMM is different: the agents are **always on**, so the platform is **proactive**. It watches the whole fleet and tells you a disk is nearly full *before* the user calls. Remote control is just one feature inside an RMM, not the whole point.

## The core capabilities

- **Monitoring & alerting** — device health, disk space, CPU, memory, services, and custom conditions; you get an alert (or a ticket) when something crosses a threshold.
- **Patch management** — approve and deploy Windows and third-party updates across the fleet on a schedule.
- **Automation & scripting** — run a PowerShell script or a built-in automation against one device or a whole group (e.g. clear temp files, restart a service).
- **Software deployment** — push or update applications remotely.
- **Remote access** — jump onto a device (NinjaOne integrates remote control) without interrupting the user.
- **Inventory & reporting** — a live asset list and reports for audits and reviews.

## A day in NinjaOne for a Tier 1/2 tech

You start at the **dashboard**: red and amber alerts at the top. You triage them — a failed backup here, a low-disk warning there. You open a device, check its health and recent activity, run an automation to free space, and confirm the alert clears. A patch policy flags machines missing this month's updates, so you approve the rollout. Throughout, NinjaOne can raise and update **tickets** automatically, and it integrates with the ticketing systems from the earlier lesson so monitoring and your queue stay in sync.

## Why security matters here

An RMM agent runs with **high privilege** on every endpoint, so the RMM console is a powerful — and attractive — target. Real-world attacks have abused RMM tools to push malware to whole fleets. Treat access seriously: enforce **multi-factor authentication**, give each technician the least privilege they need, and review who can run scripts. The same power that helps you fix 500 machines can harm 500 machines.

## Where it fits among the alternatives

NinjaOne sits alongside tools like **Datto RMM, ConnectWise Automate, Atera and Kaseya**. Microsoft **Intune** (covered next module) overlaps for cloud device management. The concepts transfer: learn one RMM well and you can pick up any of them.

## Your task

Sign up for a free NinjaOne trial or watch a product demo. Find and name these five panels: the **dashboard/alerts**, a **device's health page**, **patch management**, **automations/scripts**, and **remote access**. Write one sentence on how an RMM differs from the remote-support tool you used earlier.
