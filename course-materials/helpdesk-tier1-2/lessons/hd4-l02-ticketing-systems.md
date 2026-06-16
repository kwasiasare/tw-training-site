---
course: helpdesk-tier1-2
title: 'Ticketing systems: ServiceNow, Jira & Zendesk'
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 2
summary: Learn how IT ticketing systems work and how to write a clean, complete ticket in the three platforms
  you are most likely to meet on the job.
objectives:
- Explain what a ticketing system is and why every service desk uses one
- Describe the lifecycle of a ticket from New to Closed
- Identify the core fields every ticket should contain
- Compare ServiceNow, Jira Service Management, and Zendesk at a high level
- Write a clear, well-structured ticket that another technician could pick up
- Use ticket categories, priority, and assignment correctly
video: hd4-l02-ticketing-systems.mp4
quiz:
- q: What is the primary purpose of a ticketing system?
  options:
  - To replace the IT team
  - To track, manage, and document every support request in one place
  - To send marketing emails
  - To monitor employee internet use
  answer: 1
  why: A ticketing system records each request, tracks its status, and keeps a complete history so nothing
    is lost and work can be measured and audited.
- q: Which sequence best represents a typical ticket lifecycle?
  options:
  - New > In Progress > Resolved > Closed
  - Closed > New > Open
  - Resolved > New > Pending
  - Open > Deleted > New
  answer: 0
  why: Tickets generally flow New, then In Progress (often via On Hold/Pending), to Resolved once fixed,
    and finally Closed after confirmation.
- q: Which platform is an IT service management suite most associated with large enterprises?
  options:
  - Zendesk
  - Notepad
  - ServiceNow
  - Slack
  answer: 2
  why: ServiceNow is a large, enterprise-focused ITSM platform; Zendesk leans toward customer support
    and Jira toward dev-aligned teams, though all three handle IT tickets.
- q: Why should you avoid a ticket subject like 'It's broken'?
  options:
  - It is too long
  - It uses the wrong font
  - Subjects are not allowed
  - It gives no information, so the ticket can't be triaged or searched
  answer: 3
  why: A vague subject can't be categorised, prioritised, or found later; a good subject names the system
    and the symptom, e.g. 'Outlook - password incorrect error'.
- q: List the core fields every well-formed ticket should contain.
  answer: Requester/user, contact details, a clear subject, a detailed description with symptoms and timing,
    category, priority, and the assignment or queue.
  why: These fields let any technician triage, prioritise, and pick up the ticket without having to chase
    the user for basics.
- q: In one sentence, why does good ticket hygiene matter to the whole team?
  answer: Clean, complete tickets mean any technician can pick up the work without re-interviewing the
    user, which speeds resolution and builds a searchable knowledge history.
  why: Tickets are shared records; sloppy ones create rework, while well-written ones become future knowledge-base
    material.
resources:
- label: ServiceNow Docs — Incident Management
  url: https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/incident-management/concept/c_IncidentManagement.html
- label: Atlassian — Jira Service Management documentation
  url: https://support.atlassian.com/jira-service-management-cloud/
- label: Zendesk — About ticket fields and the agent workspace
  url: https://support.zendesk.com/hc/en-us/articles/4408886797466-About-ticket-fields
- label: Atlassian — What is a ticketing system?
  url: https://www.atlassian.com/itsm/ticketing-system
---

## Why every service desk uses a ticketing system

A **ticketing system** is the shared workspace where every support request is logged, tracked, and documented. Without one, requests scatter across inboxes, sticky notes, and hallway conversations — and things get lost. With one, every contact becomes a **ticket** with an ID, a status, a history, and an owner. It is the source of truth for the whole team.

Ticketing systems also make work *measurable*. Because every request is recorded, the desk can report on volumes, response times, and recurring problems.

## The lifecycle of a ticket

Every ticket moves through **states**. The names vary slightly by platform, but the shape is the same:

```text
New  ->  In Progress  ->  (On Hold / Pending)  ->  Resolved  ->  Closed
```

- **New** — logged but not yet picked up.
- **In Progress** — a technician is actively working it.
- **On Hold / Pending** — waiting on the user, a vendor, or a part.
- **Resolved** — the fix is applied; awaiting confirmation.
- **Closed** — confirmed fixed and finished.

Never skip states. The status field tells everyone — including the user — exactly where things stand.

## The fields that make a ticket usable

A ticket another technician can pick up cold contains:

- **Requester** and **contact details**
- A specific **subject** naming the system and symptom
- A **description** with symptoms, error text, timing, and what changed
- **Category** (e.g. Email, Network, Hardware)
- **Priority**
- **Assignment** to a person or queue

Compare these two subjects:

```text
Bad:  It's broken
Good: Outlook 365 - "password incorrect" error since 09:00 today
```

The good subject can be triaged, searched, and understood in one glance.

## The three platforms you will meet

Three tools dominate the job market:

| Platform | Strength | Typical home |
|----------|----------|--------------|
| **ServiceNow** | Full enterprise ITSM, ITIL-aligned | Large organisations |
| **Jira Service Management** | Tight link to dev teams, flexible | Software-driven companies |
| **Zendesk** | Friendly, fast, omnichannel | Customer-support-heavy teams |

The good news: they all share the same core concepts. Learn the lifecycle and field discipline once, and you can move between them quickly. The buttons differ; the thinking does not.

## Writing the ticket

When you log a contact, capture the user's words *and* the technical facts. A clean description reads like a short report:

```text
User reports Outlook prompts "password incorrect" repeatedly
since ~09:00. Webmail login works with same password.
No recent password change reported. Laptop, Windows 11, on VPN.
Verified account is not locked in directory.
```

That description tells the next person what was tried and rules things out — it is half the troubleshooting already done.

## Your task

Write a complete ticket for this scenario: a user named Sam in Finance reports that the shared accounting drive 'S:' disappeared from their PC after a reboot this morning; other users can still see it. Include subject, category, priority, and a description with symptoms, timing, and what you have already verified. Aim for the quality of the 'Good' examples above.
