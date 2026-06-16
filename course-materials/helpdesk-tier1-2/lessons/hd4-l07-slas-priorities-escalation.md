---
course: helpdesk-tier1-2
title: SLAs, priorities and escalation
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 7
summary: Understand how SLAs, impact and urgency set a ticket's priority, and learn to escalate cleanly
  so the right people get the right tickets at the right time.
objectives:
- Explain what a Service Level Agreement (SLA) is and what it commits to
- Calculate priority from impact and urgency using a priority matrix
- Distinguish response time targets from resolution time targets
- Recognise a major incident and how it is handled differently
- Escalate functionally and hierarchically with a complete handover
- Prioritise a realistic mixed queue of tickets correctly
video: hd4-l07-slas-priorities-escalation.mp4
quiz:
- q: What is a Service Level Agreement (SLA)?
  options:
  - A list of broken computers
  - A documented commitment to respond and resolve within agreed timeframes
  - A type of password
  - A software licence
  answer: 1
  why: An SLA is an agreement between IT and the business defining target response and resolution times,
    often varying by priority.
- q: How is a ticket's priority normally determined?
  options:
  - By who shouts loudest
  - Alphabetically
  - By combining impact and urgency
  - By ticket number
  answer: 2
  why: Priority comes from a matrix of impact (how many/how critical) and urgency (how time-sensitive),
    giving a consistent, defensible ranking.
- q: Which scenario is most likely a P1 / major incident?
  options:
  - One user wants a larger monitor
  - A user forgot a password
  - Someone requests new software
  - The company email system is down for everyone
  answer: 3
  why: High impact (everyone) plus high urgency (core service down) makes an organisation-wide email outage
    a top-priority/major incident.
- q: What is the difference between functional and hierarchical escalation?
  options:
  - Functional sends it to a team with the right skills; hierarchical raises it to management for authority
    or attention
  - They are the same
  - Functional is faster
  - Hierarchical only happens at night
  answer: 0
  why: Functional escalation routes to specialists by skill; hierarchical escalation raises the ticket
    up the management chain, often for SLA breaches or major incidents.
- q: Explain the difference between an SLA response time and a resolution time.
  answer: Response time is how quickly someone must acknowledge or begin work on the ticket; resolution
    time is how long is allowed to actually fix it. Both are usually set per priority.
  why: Response and resolution are separate clocks; you can meet a response target but still breach the
    resolution target if the fix runs long.
- q: What information must you include when escalating a ticket to keep it clean?
  answer: The ticket reference, a clear summary of the issue, what you already tried and ruled out, the
    impact and priority, and the user's contact details, so the next team can continue without re-interviewing
    the user.
  why: A complete handover prevents wasted time and a frustrated user repeating themselves; incomplete
    escalations bounce back.
resources:
- label: Atlassian — What is an SLA? Service level agreements explained
  url: https://www.atlassian.com/itsm/service-request-management/slas
- label: ServiceNow Docs — Service Level Management (SLAs)
  url: https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/service-level-management/concept/c_ServiceLevelManagement.html
- label: Axelos — ITIL incident management and prioritisation
  url: https://www.axelos.com/certifications/itil-service-management/itil-4-foundation
- label: Zendesk — Defining and using SLA policies
  url: https://support.zendesk.com/hc/en-us/articles/4408821871386-Defining-SLA-policies
---

## What an SLA actually promises

A **Service Level Agreement (SLA)** is a documented promise between IT and the business about how fast tickets will be handled. It usually sets two separate clocks per priority: a **response time** (how quickly someone acknowledges and starts work) and a **resolution time** (how long is allowed to fix it). When a ticket exceeds its target, that is an **SLA breach** — something the desk works hard to avoid.

```text
Priority  Response target   Resolution target
P1        15 minutes        4 hours
P2        30 minutes        8 hours
P3        4 hours           2 business days
P4        1 business day    5 business days
```

The SLA is why you cannot just work tickets in the order they arrive — some have a much tighter clock than others.

## Priority = impact x urgency

Priority is not about who complains loudest. It is calculated from **impact** (how many people, how critical the service) and **urgency** (how time-sensitive). Most desks use a **priority matrix**:

```text
              Urgency High   Urgency Med   Urgency Low
Impact High      P1            P2            P3
Impact Med       P2            P3            P4
Impact Low       P3            P4            P4
```

A single user who forgot a password is high urgency *to them* but low impact, so it is not a P1. The whole sales floor losing email is high impact *and* high urgency — that is a **P1**.

## Major incidents

A **major incident** is the most severe class: a critical service down, many users affected, the business hurting. These get special handling — a **major incident manager**, a dedicated bridge call, frequent communications, and all-hands focus. As Tier 1, your role is often to **recognise** one early, log it correctly, and raise the alarm rather than quietly working it alone.

## Escalation done well

No single technician can fix everything, so **escalation** is a normal, healthy part of the job. There are two kinds:

- **Functional escalation** — sending the ticket to a team with the right **skills** (e.g. networking).
- **Hierarchical escalation** — raising it up the **management** chain for authority or attention, common on SLA breaches and major incidents.

A clean escalation is a complete **handover**. Bad escalations bounce back and waste everyone's time:

```text
Escalation note:
Ref: INC0048213 | Priority: P2
Summary: Finance shared mailbox not receiving external email since 08:30.
Tried: confirmed mailbox exists, internal mail arrives, checked rules
       (none blocking), verified user permissions OK.
Impact: 6 finance users, month-end deadline today.
Contact: Sam Patel, ext. 4471, available until 17:00.
Reason for escalation: needs mail-flow/transport rule review (Tier 2).
```

That handover lets the next team start immediately, without re-interviewing the user.

## Your task

You have these four tickets open at once. Assign each a priority (P1-P4) using impact and urgency, then list the order you would work them and write one sentence justifying each:

1. The entire warehouse cannot scan stock; shipping is halted.
2. One user's mouse scroll wheel is sticky.
3. A manager cannot open a report needed for a board meeting in one hour.
4. The shared printer on floor 2 is out of toner (a spare is in the cupboard).
