---
title: Negotiation, offers & evaluating roles
month: 6
monthTitle: Apply & Interview
lesson: 9
summary: Read an offer letter properly, evaluate the whole role, and negotiate calmly so you accept a
  job you actually want.
objectives:
- Read a written offer and identify every component of total compensation
- Separate base salary from bonus, equity, pension and benefits
- Research a fair market range using public salary data
- Negotiate respectfully with a clear, evidence-based counter
- 'Evaluate a role beyond money: growth, manager, learning and risk'
- Avoid common first-job mistakes like verbal-only acceptance
- Compare two offers with a simple weighted scorecard
video: m6-l09-negotiation.mp4
quiz:
- q: Which of these is part of TOTAL compensation but is NOT base salary?
  options:
  - The number printed as annual gross pay
  - An annual performance bonus
  - Your hourly overtime for one shift
  - The tax deducted at source
  answer: 1
  why: Base salary is your fixed annual gross pay. A performance bonus, equity, pension and benefits are
    extra components that together form total compensation.
- q: What is the single most important rule before you celebrate or resign?
  answer: Get the offer in writing and read every line before accepting.
  why: A verbal 'yes' is not a contract. Always wait for a written offer, read base, bonus, start date
    and conditions, then respond.
- q: You are offered 38000 but research shows the role typically pays 40000 to 46000. What is the most
    professional response?
  options:
  - Accept immediately so you don't seem greedy
  - Reject the offer in anger
  - Thank them, then counter near 44000 citing your research
  - Demand 60000 to leave room
  answer: 2
  why: A polite, specific, evidence-based counter inside the real market range is professional and usually
    expected. Extreme anchors damage trust.
- q: True or false — once you sign, salary is the only thing that matters about a job.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Manager quality, learning, the team, growth path and stability often matter more for your
    career than a few thousand pounds in year one.
- q: Name two non-salary factors worth weighing when comparing two job offers.
  answer: 'Any two of: quality of the manager, learning opportunities, growth path, team, tech stack,
    remote flexibility, job security, commute.'
  why: Especially in your first AI role, learning and a good manager compound over your whole career far
    more than a small pay difference.
- q: Why should you ask for a little time to consider an offer rather than accepting on the call?
  answer: It lets you read the written terms, research the range, and decide calmly instead of emotionally.
  why: Asking for 24 to 48 hours is normal and reasonable. It protects you from rushed decisions and gives
    space to prepare a counter.
resources:
- label: Levels.fyi — salary data for tech and AI roles
  url: https://www.levels.fyi/
- label: Glassdoor — company reviews and salary ranges
  url: https://www.glassdoor.com/
- label: Harvard Business Review — 15 Rules for Negotiating a Job Offer
  url: https://hbr.org/2014/04/15-rules-for-negotiating-a-job-offer
- label: UK Gov — Check your employment contract and rights
  url: https://www.gov.uk/employment-contracts-and-conditions
---

## Get it in writing first

An offer is exciting, but the golden rule is simple: **do not accept, celebrate, or resign from anything until you have the offer in writing**. A verbal 'we'd love to have you' is not a contract. Wait for the written offer, then read every single line.

It is completely normal to say: *'Thank you so much, I'm really excited — could you send the details in writing? I'd like a day or two to review.'* Good employers expect this.

## Read the whole package

Salary is only one part. **Total compensation** is base plus everything else.

- **Base salary** — your fixed annual gross pay
- **Bonus** — often a percentage of base, sometimes guaranteed in year one
- **Equity / share options** — common at startups, worth understanding
- **Pension** — employer contribution, real money
- **Benefits** — holiday days, private healthcare, learning budget, remote flexibility

Write them all into one place so you compare like for like.

## Research a fair range

Never negotiate on a feeling. Find the real market range using public data, then anchor your number with evidence.

```python
# Quick total-comp comparison
def total_comp(base, bonus_pct, pension_pct, learning_budget=0):
    bonus = base * bonus_pct
    pension = base * pension_pct
    return base + bonus + pension + learning_budget

offer_a = total_comp(40000, 0.10, 0.05, 1000)
offer_b = total_comp(44000, 0.00, 0.03, 0)
print(round(offer_a), round(offer_b))   # 47000 45320
```

## Make a calm, specific counter

Negotiation is not a fight. State a clear number inside the real range, give a one-line reason, and stay warm. Keep it short.

```bash
# A counter is just a calm, written reply. Sketch it first:
# 1. Thank them genuinely
# 2. Restate your excitement for the role
# 3. Ask: "Is there flexibility on base toward 44000?"
# 4. Give one reason (market data, your skills)
# 5. Stop talking and let them respond
```

## Evaluate the role, not just the money

In your first **A I** job, what you *learn* and *who you learn from* often matter more than a few thousand pounds. Score the whole role.

| Factor | Weight |
|---|---|
| Manager quality | High |
| Learning & growth | High |
| Compensation | Medium |
| Stability | Medium |
| Commute / remote | Low |

## Your task

Take a real or sample job advert. Write out its **total compensation**, research the market range on two sites, and draft a three-sentence counter email you would actually feel comfortable sending.
