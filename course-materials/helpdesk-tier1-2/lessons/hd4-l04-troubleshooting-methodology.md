---
course: helpdesk-tier1-2
title: The troubleshooting methodology (the A+ 6-step model)
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 4
summary: Learn the CompTIA A+ six-step troubleshooting model so you fix problems methodically instead
  of guessing, and document them as you go.
objectives:
- Recite the six steps of the CompTIA A+ troubleshooting methodology in order
- Gather information and identify symptoms before changing anything
- Form and test one theory of probable cause at a time
- Verify full system functionality and apply preventive measures
- Document findings, actions, and outcomes in the ticket
- Apply the full method to a realistic support scenario
video: hd4-l04-troubleshooting-methodology.mp4
quiz:
- q: What is the correct first step of the A+ troubleshooting methodology?
  options:
  - Implement the solution
  - Identify the problem
  - Document findings
  - Reboot everything
  answer: 1
  why: Step one is always to identify the problem by gathering information, asking the user, and noting
    symptoms before touching anything.
- q: After you establish a theory of probable cause, what comes next?
  options:
  - Close the ticket
  - Order new hardware
  - Test the theory to determine the cause
  - Escalate immediately
  answer: 2
  why: 'Step three is to test the theory: confirm whether your suspected cause is correct before you commit
    to a fix. If not confirmed, form a new theory.'
- q: Why should you change only one thing at a time when testing?
  options:
  - It is faster
  - Because tickets require it
  - To use less electricity
  - So you know which change actually fixed or affected the issue
  answer: 3
  why: Changing one variable at a time means you can attribute the result to that change; changing several
    at once hides what actually worked.
- q: What does 'verify full system functionality' mean?
  options:
  - Confirm the original issue is fixed and nothing else broke
  - Restart the computer
  - Close the ticket without checking
  - Ask another technician to look
  answer: 0
  why: After applying a fix you confirm the original symptom is gone and the rest of the system still
    works, ideally with the user, before closing.
- q: List the six steps of the A+ troubleshooting methodology in order.
  answer: 1) Identify the problem; 2) Establish a theory of probable cause; 3) Test the theory; 4) Establish
    a plan of action and implement the solution; 5) Verify full system functionality and apply preventive
    measures; 6) Document findings, actions, and outcomes.
  why: Following the steps in order keeps troubleshooting systematic and repeatable rather than a guessing
    game.
- q: Why is the final documentation step important even after the fix works?
  answer: Documentation records what was wrong and how it was fixed so the same issue can be solved faster
    next time and feeds the knowledge base.
  why: Good documentation turns one solved ticket into reusable knowledge for the whole team and prevents
    repeated investigation.
resources:
- label: CompTIA — A+ Certification (Core 2 objectives include troubleshooting)
  url: https://www.comptia.org/certifications/a
- label: Microsoft Learn — Troubleshoot client connectivity and devices
  url: https://learn.microsoft.com/en-us/training/
- label: Atlassian — IT troubleshooting best practices
  url: https://www.atlassian.com/itsm/incident-management
- label: ServiceNow Docs — Working with incidents
  url: https://docs.servicenow.com/bundle/washingtondc-it-service-management/page/product/incident-management/concept/c_IncidentManagement.html
---

## Why method beats guessing

Beginners often troubleshoot by trying random fixes until something works. It feels productive but it is slow, it breaks things, and you can never explain what fixed the issue. The **CompTIA A+ troubleshooting methodology** is a six-step model that turns troubleshooting into a repeatable, professional process. Learn it once and use it on everything from a frozen laptop to a network outage.

```text
1. Identify the problem
2. Establish a theory of probable cause
3. Test the theory
4. Establish a plan of action and implement the solution
5. Verify full functionality and apply preventive measures
6. Document findings, actions, and outcomes
```

## Step 1: Identify the problem

Before you touch anything, **gather information**. Ask the user what happened, what changed, and when it started. Note exact error messages. A useful question script:

```text
"When did this start?"
"What were you doing right before it happened?"
"Has anything changed recently - updates, new software, a move?"
"Does it happen every time, or sometimes?"
```

Also check the obvious: is it plugged in, is anyone else affected? Identifying scope early tells you whether this is one machine or an outage.

## Step 2: Establish a theory of probable cause

Form a **single, testable theory**. Start with the **most likely and simplest** cause — the famous principle is to question the obvious. "The password is wrong" or "the cable is loose" before "the motherboard has failed." Use your knowledge and the symptoms to make an educated guess, not a wild one.

## Step 3: Test the theory

Now **test it**. If your theory is right, you have found the cause. If it is wrong, form a *new* theory — do not start guessing randomly. Change **one thing at a time** so you always know what affected the result. If you cannot confirm a cause, this is often where you **escalate**.

## Step 4: Plan and implement the solution

With the cause confirmed, decide *how* to fix it, considering impact. Will the fix require a reboot, downtime, or a heads-up to others? Then implement it cleanly. For risky fixes, note a way back.

## Step 5: Verify functionality and prevent recurrence

Confirm the **original symptom is gone** and that **nothing else broke**. Do this *with the user* where possible — they decide whether it is truly fixed. Then think about **prevention**: should a setting change, or a knowledge article be written, so this does not happen again?

## Step 6: Document everything

Finally, **document** the symptoms, the cause, the actions you took, and the outcome in the ticket. This is not paperwork for its own sake — it is what lets the next technician (often future-you) solve the same issue in minutes, and it feeds the **knowledge base**.

## Your task

A user reports: "My laptop won't connect to Wi-Fi since this morning, but my phone connects to the same network fine." Write out how you would work this ticket through all six steps. For each step, write one or two lines: the questions you would ask, your first theory, how you would test it, a plausible fix, how you would verify, and a one-line documentation summary.
