---
course: helpdesk-tier1-2
title: 'Lab: a day in the life of a helpdesk technician'
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 10
summary: 'Bring the whole month together in a simulated shift: triage a live queue, work tickets with
  method and empathy, escalate cleanly, and document as you go.'
objectives:
- Triage and prioritise a realistic mixed ticket queue under time pressure
- Classify each contact as incident, request, problem, or change
- Apply the six-step troubleshooting method to a live ticket
- Communicate with empathy and verify identity where required
- Escalate a ticket with a complete, professional handover
- Document a worked ticket to a knowledge-base standard
video: hd4-l10-lab-day-in-the-life.mp4
quiz:
- q: You arrive to a queue of five tickets. What do you do first?
  options:
  - Triage them by priority using impact and urgency
  - Work them in arrival order
  - Pick the easiest one
  - Escalate all of them
  answer: 0
  why: 'Triage first: assess impact and urgency to set priorities, so the most business-critical issues
    get worked before lower-impact ones.'
- q: A ticket reads 'Whole call centre lost phones 2 minutes ago.' How should you treat it?
  options:
  - P4, log and move on
  - Ignore until other tickets are done
  - 'As a likely major incident: raise it and alert the right people fast'
  - Ask them to email instead
  answer: 2
  why: A core service down for many users is high impact and urgency, a probable major incident requiring
    you to recognise and escalate it immediately.
- q: Mid-shift a user is rude and impatient. What is the professional response?
  options:
  - Match their tone
  - Hang up
  - Lower the ticket priority as punishment
  - Stay calm, acknowledge the frustration, and keep helping
  answer: 3
  why: Professionalism means not taking it personally; acknowledge the feeling, keep your tone steady,
    and focus on resolving the issue.
- q: Before closing a resolved ticket, what should you always do?
  options:
  - Nothing, just close it
  - Verify the fix with the user and document findings and actions
  - Reassign it to a colleague
  - Delete the notes
  answer: 1
  why: Confirm the user agrees it is fixed, then document the symptoms, cause, actions, and outcome so
    the ticket is complete and reusable.
- q: Describe, in order, how you would handle a brand-new ticket from first read to closure.
  answer: Triage and set priority, classify it (incident/request/etc.), verify identity if needed, gather
    information, apply the six-step method, communicate with the user and set expectations, resolve or
    escalate cleanly, then verify and document before closing.
  why: 'This sequence combines everything from the month: prioritisation, ITIL classification, methodical
    troubleshooting, communication, escalation, and documentation.'
- q: Why does a single shift draw on every topic from this month at once?
  answer: Because real tickets require you to prioritise (SLA), classify (ITIL), troubleshoot (the A+
    method), communicate well, escalate cleanly, and document, all together, not as separate exercises.
  why: The lab shows that helpdesk skill is the integration of all these practices applied fluidly under
    real conditions.
resources:
- label: Atlassian — IT service desk best practices
  url: https://www.atlassian.com/itsm/service-request-management/it-service-desk
- label: ServiceNow Docs — Incident Management workflow
  url: https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/incident-management/concept/c_IncidentManagement.html
- label: Zendesk — Agent workspace and working tickets
  url: https://support.zendesk.com/hc/en-us/articles/4408846407066-About-the-Zendesk-Agent-Workspace
- label: Microsoft Learn — Training catalog (IT support practice)
  url: https://learn.microsoft.com/en-us/training/
---

## The shift begins

This lab pulls the whole month together. You are starting an 09:00 shift on a busy service desk. Five tickets are already in your queue. Nothing here is new — but for the first time you must use *all* your skills at once: prioritise, classify, troubleshoot, communicate, escalate, and document. That integration *is* the job.

## Your 09:00 queue

```text
#1  INC: "Whole call centre lost their phones 2 minutes ago." (40 users)
#2  REQ: "Please install Adobe Acrobat on my laptop." (1 user)
#3  INC: "My monitor flickers occasionally." (1 user)
#4  INC: "I'm locked out and have a client call in 10 min." (1 user)
#5  INC: "Outlook won't send; error 0x800CCC0F." (1 user)
```

## Step 1: Triage the queue

Do not work in arrival order. Score each by **impact** and **urgency**:

| # | Type | Impact | Urgency | Priority |
|---|------|--------|---------|----------|
| 1 | Incident (likely **major**) | High (40) | High | **P1** |
| 4 | Incident | Low (1) | High (deadline) | **P2** |
| 5 | Incident | Low (1) | Medium | P3 |
| 2 | Service request | Low | Low | P4 |
| 3 | Incident | Low | Low | P4 |

Ticket #1 is a probable **major incident** — recognise it, raise the alarm, and get the right people on it *before* you touch anything else. You may own the comms, not the fix.

## Step 2: Work ticket #4 with method and care

The locked-out user is stressed and on a deadline — lead with empathy, then verify identity (it is an account change!), then act.

```text
You: "I can absolutely help with that, and I know the timing is
      tight. Quick security check first, per policy - can you
      confirm your employee ID and security answer? ... Thank you.
      You were locked out from failed sign-ins; I'm unlocking it
      now. Try signing in again for me. ... Working? Brilliant."
```

Notice the order: **empathy -> verify -> diagnose (lockout, not reset) -> act -> confirm with user**.

## Step 3: Escalate ticket #1 cleanly

The phone outage needs the telecoms/network team. Your handover:

```text
Ref: INC0050001 | Priority: P1 (suspected major incident)
Summary: Entire call centre (~40 users) lost desk phones at 09:02.
Impact: Customer calls failing; revenue + SLA impact now.
Tried: confirmed multiple users, network switch reachable by ping,
       no recent change noted in change calendar.
Contact: Floor lead Aisha Bello, ext. 2200.
Escalated to: Telecoms/Network on-call. Comms owner: me.
```

## Step 4: Document and close

When the Outlook ticket (#5) resolves, verify with the user, then write the record:

```text
Symptom: Outlook send failing, error 0x800CCC0F.
Cause:   Outgoing (SMTP) server setting was incorrect after profile reset.
Action:  Corrected SMTP server and port; sent test mail successfully.
Outcome: Verified with user - send/receive working. Resolved.
KB:      Linked to article "Fixing Outlook 0x800CCC0F send errors."
```

## Your task

Work the full queue above as if it were your shift. Produce: (1) your triage table with a priority for all five tickets and one line of justification each; (2) a short worked write-up of ticket #5 through the six-step method; (3) a clean escalation note for ticket #1; and (4) a closing message to the locked-out user in #4. Treat this as your portfolio piece for the month.
