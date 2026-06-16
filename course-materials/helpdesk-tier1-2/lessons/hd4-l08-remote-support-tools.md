---
course: helpdesk-tier1-2
title: Remote support tools and techniques
month: 4
monthTitle: 'The Helpdesk Professional: ITIL, Ticketing & Soft Skills'
lesson: 8
summary: Learn how to support users you cannot physically reach, using remote tools safely, securely,
  and with the consent and trust of the person on the other end.
objectives:
- Describe the common categories of remote support tools
- Always obtain user consent before connecting to their device
- Guide a user through actions using clear verbal screen-sharing
- Follow security best practices during a remote session
- Choose between remote control, screen-share, and remote command tools
- Run a safe, professional remote session from start to finish
video: hd4-l08-remote-support-tools.mp4
quiz:
- q: What must you do before taking remote control of a user's computer?
  options:
  - Nothing, just connect
  - Obtain the user's clear consent and explain what you'll do
  - Reboot it first
  - Disable their keyboard
  answer: 1
  why: Consent is both a courtesy and a security/privacy requirement; you explain what you are doing and
    the user agrees before you connect.
- q: Which is a key security practice during a remote session?
  options:
  - Confirm the user's identity, keep them watching, and end the session cleanly
  - Leave the session connected overnight
  - Ask for their password verbally
  - Turn off logging
  answer: 0
  why: Verify who you're helping, keep the user present and aware, never ask for passwords aloud, and
    disconnect cleanly so no access lingers.
- q: When would you guide a user verbally instead of taking remote control?
  options:
  - Never
  - Only on weekends
  - When you can't or shouldn't connect, or to help the user learn
  - When the ticket is closed
  answer: 2
  why: Verbal guidance suits situations where remote tools aren't available or appropriate, sensitive
    screens are involved, or when teaching the user helps them next time.
- q: Why should you avoid asking a user to read their password to you?
  options:
  - It is slow
  - Passwords are too long
  - It is fine to do so
  - It is a security risk and against good practice; you should never need their password
  answer: 3
  why: Technicians should never collect user passwords; doing so trains users to share credentials and
    creates a security and accountability risk.
- q: Name two categories of remote support tool and what each is best for.
  answer: Remote-control tools (e.g. for full hands-on troubleshooting), screen-sharing/co-browsing tools
    (to see what the user sees and guide them), and remote command/management tools (to run scripts or
    push fixes at scale). Each suits a different level of access and visibility.
  why: Matching the tool to the task keeps sessions efficient and minimises unnecessary access to the
    user's machine.
- q: Why is ending a remote session cleanly important?
  answer: A clean disconnect ensures no lingering access remains on the user's device, protects their
    privacy, and confirms to them that you are no longer connected.
  why: Leftover sessions are a security and trust risk; always disconnect and confirm with the user that
    the session has ended.
resources:
- label: Microsoft Learn — Quick Assist and Remote Help
  url: https://learn.microsoft.com/en-us/training/
- label: Microsoft Learn — Remote Desktop and remote support
  url: https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/welcome-to-rds
- label: Atlassian — Remote IT support best practices
  url: https://www.atlassian.com/itsm/service-request-management/it-service-desk
- label: CompTIA — A+ operational procedures and remote access
  url: https://www.comptia.org/certifications/a
---

## Supporting people you can't reach

Most support today is **remote**: the user is on another floor, in another city, or working from home. You will rarely walk to the desk. That makes **remote support tools** and the etiquette around them a daily skill. Used well, they let you fix things in minutes that would otherwise take a site visit. Used carelessly, they create security and trust problems.

## The categories of tool

Remote tools fall into a few broad groups:

- **Remote-control tools** let you see *and operate* the user's screen and mouse, as if you were sitting there. Best for hands-on troubleshooting.
- **Screen-sharing / co-browsing** lets you *see* what the user sees while *they* drive. Good for sensitive screens and for teaching.
- **Remote command / management tools** let you run commands or push fixes to many machines at once, often without interrupting the user. Best at scale.

Match the tool to the task: do not take full control when watching the user click would do.

## Consent comes first, always

Before you connect to anyone's machine, **get their consent** and explain what you are about to do. This is both basic courtesy and a privacy/security requirement.

```text
"To fix this fastest, I'd like to connect to your screen remotely.
You'll see a prompt asking you to allow it - I can't connect
unless you accept. You'll be able to see everything I do, and
you can take back control at any time. Is that okay?"
```

Notice it reassures the user they stay in control and can watch. That is how you build trust over a remote link.

## Guiding a user verbally

Sometimes you should *not* connect — the screen has sensitive data, the tool is unavailable, or teaching the user pays off. Then you **guide them verbally**. The skill is giving one clear instruction at a time and confirming each step.

```text
"Let's do this together. Bottom-left, click the Start button -
tell me when you see the menu. ... Great. Now type the word
'control' and press Enter. What do you see now?"
```

Slow, single steps with check-ins prevent the user racing ahead and getting lost.

## Security during the session

A remote session is privileged access, so treat it with care:

- **Verify identity** — confirm you are helping the right person.
- **Never ask for their password** out loud or in chat; you should not need it.
- **Keep the user present and aware** of what you are doing.
- **Avoid opening personal files** or anything unrelated to the issue.
- **End the session cleanly** and confirm the disconnect, so no access lingers.

These habits protect the user, protect you, and keep an auditable, professional standard.

## Your task

Write the spoken script you would use to start a remote-control session with a nervous, non-technical user who is reluctant to let you connect. Include: how you ask for consent, how you reassure them they stay in control, one security point you make, and how you tell them the session has ended at the close. Keep it warm and jargon-free.
