---
course: helpdesk-tier1-2
title: Documentation and knowledge bases
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 6
summary: Learn to write ticket notes and knowledge-base articles that other technicians and users can
  actually follow, turning each solved problem into reusable knowledge.
objectives:
- Explain why documentation is a core helpdesk responsibility, not an afterthought
- Write clear, factual ticket notes that capture what was done and why
- Structure a knowledge-base (KB) article a user or technician can follow
- Distinguish internal documentation from user-facing articles
- Apply knowledge-centred service principles in everyday work
- Write a usable KB article from a solved ticket
video: hd4-l06-documentation-and-knowledge-bases.mp4
quiz:
- q: Why is documentation considered part of the actual job, not extra work?
  options:
  - It is required by law
  - It turns solved issues into reusable knowledge and lets others continue your work
  - It makes tickets look longer
  - It replaces troubleshooting
  answer: 1
  why: Good notes let any technician resume or repeat a fix without re-investigating, and KB articles
    deflect future tickets, so documentation directly multiplies the team's capacity.
- q: What makes a good knowledge-base article?
  options:
  - Lots of jargon to sound expert
  - A single long paragraph
  - A clear title, the problem, numbered steps, and the expected result
  - Only a screenshot
  answer: 2
  why: Useful KB articles have a searchable title, a description of the symptom, clear numbered steps,
    and confirmation of the expected outcome so the reader knows it worked.
- q: What is the difference between internal documentation and a user-facing article?
  options:
  - Internal docs can be technical; user-facing articles use plain language and avoid sensitive detail
  - There is no difference
  - Internal docs are always shorter
  - User-facing articles are for managers only
  answer: 0
  why: Internal notes can include technical detail and tools; user-facing self-help articles use plain
    language and never expose sensitive internal information.
- q: What does 'knowledge-centred service' (KCS) encourage technicians to do?
  options:
  - Avoid writing anything down
  - Only document at year end
  - Delete old articles immediately
  - Capture and reuse knowledge as part of solving each issue
  answer: 3
  why: KCS treats knowledge capture as a by-product of solving tickets, so the knowledge base grows and
    improves continuously through normal work.
- q: Write a good, searchable title for a KB article about resetting a forgotten domain password. Explain
    your choice.
  answer: Something like 'How to reset a forgotten Windows domain password (self-service)'. It names the
    system, the action, and the context, so users searching 'reset password' will find it.
  why: A searchable title contains the words users actually type and clearly states what the article covers.
- q: Why should ticket notes be factual and free of blame or opinion?
  answer: Tickets are official, shared records that others read and that may be audited, so notes must
    state facts and actions, not opinions or criticism of users or colleagues.
  why: Professional, factual notes protect everyone, stay useful over time, and avoid creating problems
    if the ticket is reviewed later.
resources:
- label: Atlassian — How to build a knowledge base
  url: https://www.atlassian.com/itsm/knowledge-management/what-is-a-knowledge-base
- label: Zendesk — Creating and managing knowledge base articles
  url: https://support.zendesk.com/hc/en-us/articles/4408839258522-Creating-or-editing-articles-in-the-knowledge-base
- label: ServiceNow Docs — Knowledge Management
  url: https://docs.servicenow.com/bundle/washingtondc-servicenow-platform/page/product/knowledge-management/concept/c_KnowledgeManagement.html
- label: Consortium for Service Innovation — KCS (Knowledge-Centered Service)
  url: https://www.serviceinnovation.org/kcs/
---

## Documentation is the work, not the paperwork

Many beginners treat writing things down as the annoying bit after the real work. Reframe it: on a service desk, **documentation is how your work scales**. A fix you record once can be repeated by anyone in minutes; a fix you keep in your head dies when you go to lunch. Two kinds of writing matter most: **ticket notes** and **knowledge-base articles**.

## Writing good ticket notes

Ticket notes are the running record of what happened. They should let a colleague pick up your ticket cold. Keep them **factual, chronological, and free of blame or opinion** — tickets are official records that can be audited.

```text
10:14 - User reports shared drive S: missing after reboot.
10:18 - Confirmed drive maps fine on a colleague's PC. Scope: 1 user.
10:25 - Found mapped-drive logon script not running; Group Policy
        not applied. Forced gpupdate /force - drive reappeared.
10:30 - Verified with user, S: now present and accessible. Resolved.
```

Notice it records *facts and actions with times*, not "user was clueless." Never write anything in a ticket you would not want the user, your boss, or an auditor to read.

## What a knowledge-base article is

A **knowledge base (KB)** is a searchable library of articles describing how to solve known issues. Some are **internal** (for technicians); some are **user-facing self-help** that deflect tickets entirely. A good article has a predictable structure:

```text
Title:    How to map the shared S: drive (Windows)
Applies to: Windows 11 domain PCs
Symptom:  The S: drive is missing from File Explorer
Steps:
  1. Open File Explorer and click "This PC".
  2. Click the three-dot menu, then "Map network drive".
  3. Choose drive letter S: and enter \\fileserver\shared.
  4. Tick "Reconnect at sign-in" and click Finish.
Expected result: The S: drive appears under "This PC".
```

A **searchable title** uses the words users actually type. Numbered **steps** are unambiguous. An **expected result** lets the reader confirm it worked.

## Internal vs user-facing

Internal docs can be technical and reference tools, scripts, or admin steps. **User-facing** articles use plain language, avoid jargon, and **never expose sensitive detail** such as server names or security settings the public should not see. Always ask: *who will read this?*

## Knowledge-centred service

**Knowledge-Centred Service (KCS)** is the principle that capturing knowledge should be a natural **by-product of solving tickets**, not a separate project. When you solve something new, you write or improve an article as you go. Over time the knowledge base becomes the team's collective memory, and First Contact Resolution climbs because answers are already written down.

## Your task

Take the solved ticket from earlier in the course where Sam's S: drive disappeared (or invent a similar fix you understand). Write a complete, user-facing KB article for it: a searchable title, an 'applies to' line, the symptom, numbered steps in plain language, and an expected result. Then write one sentence on what you would change if the article were internal-only instead.
