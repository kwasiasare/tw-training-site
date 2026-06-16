---
course: helpdesk-tier1-2
title: 'ITIL fundamentals: incident, problem and change'
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 3
summary: 'Get a clear, practical grounding in ITIL 4 and the three practices a helpdesk lives by every
  day: incident, problem, and change management.'
objectives:
- Explain what ITIL is and why organisations adopt it
- Define a service, value, and the four dimensions in plain terms
- Distinguish an incident from a problem with confidence
- Describe the goal of change management and why it protects users
- Recognise service requests as distinct from incidents
- Apply the correct ITIL practice to a real support scenario
video: hd4-l03-itil-fundamentals.mp4
quiz:
- q: What is the best plain-English definition of an incident in ITIL?
  options:
  - A planned upgrade to a system
  - An unplanned interruption or reduction in quality of a service
  - A request for new software
  - A monthly report
  answer: 1
  why: An incident is an unplanned event that breaks or degrades a service; the goal of incident management
    is to restore normal service as fast as possible.
- q: How does a problem differ from an incident?
  options:
  - A problem is the underlying cause of one or more incidents
  - They are the same thing
  - A problem is always less urgent than an incident
  - A problem only affects printers
  answer: 0
  why: Incidents are the visible symptoms; a problem is the root cause behind them. Problem management
    seeks to remove that cause so incidents stop recurring.
- q: What is the main goal of change management (change enablement)?
  options:
  - To stop all changes from happening
  - To speed up ticket closing
  - To make changes safely while minimising risk and disruption
  - To replace the helpdesk
  answer: 2
  why: Change enablement aims to maximise successful changes by assessing and controlling risk, so improvements
    happen without breaking services for users.
- q: A user asks to be given access to a shared mailbox. Which practice is this?
  options:
  - Incident management
  - Problem management
  - Major incident
  - Service request fulfilment
  answer: 3
  why: Nothing is broken — the user wants something provided as a standard offering, which is a service
    request, handled through request fulfilment, not incident management.
- q: In one sentence, explain the relationship between incidents and problems using an example.
  answer: If five users separately report the same email outage (five incidents), the single failed mail
    server behind them is the problem, and fixing the server resolves the root cause.
  why: Many incidents can share one underlying problem; problem management removes the cause so the incidents
    stop happening.
- q: Why does ITIL insist that most changes go through a controlled process?
  answer: Because uncontrolled changes are a leading cause of outages, a controlled process assesses risk
    and schedules changes so improvements don't break live services.
  why: Change enablement balances the need to improve with the need to protect stable, working services
    for users.
resources:
- label: Axelos — ITIL 4 Foundation certification
  url: https://www.axelos.com/certifications/itil-service-management/itil-4-foundation
- label: Atlassian — ITIL incident, problem and change management
  url: https://www.atlassian.com/itsm/itil
- label: ServiceNow Docs — Problem Management
  url: https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/problem-management/concept/c_ProblemManagement.html
- label: Microsoft Learn — Training catalog (ITIL & ITSM)
  url: https://learn.microsoft.com/en-us/training/
---

## What ITIL is and why it exists

**ITIL** (the IT Infrastructure Library) is the world's most widely adopted framework of **best practices** for IT service management. It is not a rulebook you must obey to the letter — it is a shared vocabulary and set of sensible practices so that IT teams everywhere work in a consistent, reliable way. The current version is **ITIL 4**.

The central idea is **value**: IT exists to help the business and its users achieve outcomes. A **service** is a way of delivering that value — email, the VPN, the finance system are all services. Your job on the desk is to keep those services flowing.

## The three practices you live by

ITIL 4 has many practices, but a helpdesk technician works with three constantly: **incident management**, **problem management**, and **change enablement**. Get these three clear and most of the framework falls into place.

## Incidents: restore service fast

An **incident** is an **unplanned interruption** to a service, or a reduction in its quality. The phone rings, email is down, a laptop won't boot — those are incidents. The single goal of **incident management** is to **restore normal service as quickly as possible**, even with a temporary fix or **workaround**. You are not required to find the deep cause; you are required to get the user working again.

```text
Incident: "Email is down for the whole Sales floor."
Goal: get Sales back on email ASAP, even via a workaround.
```

## Problems: remove the cause

A **problem** is the **underlying cause** of one or more incidents. If twelve people report the same outage, that is twelve incidents and likely one problem. **Problem management** investigates the root cause so the incidents stop coming back. It is slower, more analytical work — often done by Tier 2 and Tier 3.

```text
12 incidents: "Email down" reported by 12 users
 1 problem:   the failed mail server behind all of them
```

Incidents are the *symptoms*; the problem is the *disease*.

## Changes: improve without breaking things

A **change** is the addition, modification, or removal of anything that could affect services — a server patch, a firewall rule, a new application. **Change enablement** exists to make changes **safely**, because uncontrolled changes are one of the biggest causes of outages. Changes are usually assessed for risk and scheduled, sometimes through a **Change Advisory Board (CAB)**. Low-risk, routine changes may be pre-approved as **standard changes**.

## Service requests: nothing is broken

Not every contact is an incident. When a user wants something provided as a normal offering — software installed, access to a mailbox, a new monitor — that is a **service request**, handled through **request fulfilment**. The test is simple: *is something broken, or does the user want something provided?* Broken means incident; provide means request.

## Your task

For each of the following, label it Incident, Problem, Change, or Service Request, and write one sentence justifying your choice:

1. "My screen is frozen and I have a deadline."
2. "Please give me the Adobe Acrobat licence."
3. The network team plans to replace the core switch on Saturday night.
4. The desk has logged 30 tickets this week all about the VPN dropping; someone needs to find out why.
