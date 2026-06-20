---
course: junior-digital-marketing
title: Building Automated Campaigns in Mailchimp
month: 4
monthTitle: Email Marketing & Capstone Portfolio
lesson: 2
summary: Learn to design, segment, and automate an email sequence in Mailchimp, then measure performance
  using open and click-through rates to optimise your campaigns.
objectives:
- Set up a Mailchimp audience and import or collect subscriber contacts correctly
- Create audience segments and tags to target the right people with relevant messages
- Build a multi-email automated welcome sequence using Mailchimp's Customer Journey builder
- Write effective subject lines and email content that improve open and click rates
- Measure and interpret open rate, click-through rate (CTR), and other key metrics
- Apply A/B testing and list-hygiene best practices to improve campaign results
video: dm-m4-l02-building-automated-campaigns-in-mailchimp.mp4
quiz:
- q: What is the formula for click-through rate (CTR)?
  options:
  - Unique opens ÷ delivered × 100
  - Unique clicks ÷ delivered × 100
  - Total sends ÷ unsubscribes × 100
  - Bounces ÷ delivered × 100
  answer: 1
  why: 'CTR measures engagement: unique clicks divided by emails delivered, multiplied by 100.'
- q: In Mailchimp, which feature is the visual builder used to create automated email sequences?
  options:
  - Merge tags
  - Customer Journey
  - Audience dashboard
  - Content Studio
  answer: 1
  why: The Customer Journey builder lets you set a trigger and add steps like emails, delays, and branches.
- q: Why are clicks often considered more reliable than opens for measuring engagement?
  options:
  - Clicks are easier to fake
  - Apple Mail Privacy Protection inflates open rates
  - Opens are not tracked in Mailchimp
  - Clicks count every email sent
  answer: 1
  why: Apple Mail Privacy Protection auto-loads tracking pixels, inflating reported opens, so clicks better
    reflect real engagement.
- q: Which practice is both legally required and good for deliverability?
  options:
  - Buying targeted email lists
  - Including an unsubscribe link in every email
  - Sending to everyone with no segmentation
  - Hiding the sender name
  answer: 1
  why: An unsubscribe link is legally required under GDPR/CAN-SPAM and helps protect your sender reputation.
- q: What is a 'segment' in Mailchimp? Answer in one short sentence.
  answer: A saved filter that groups contacts based on conditions such as activity or location.
  why: Segments let you target relevant subsets of your audience, improving open and click rates.
- q: When running an A/B test, how many variables should you change at once?
  options:
  - As many as possible
  - One
  - Three
  - Zero
  answer: 1
  why: Testing one variable at a time ensures you know which change caused any difference in results.
resources:
- label: 'Mailchimp Help: Getting Started with Customer Journeys'
  url: https://mailchimp.com/help/about-customer-journeys/
- label: 'Mailchimp Help: About Email Marketing Reports'
  url: https://mailchimp.com/help/about-open-and-click-tracking/
- label: Mailchimp Email Marketing Benchmarks by Industry
  url: https://mailchimp.com/resources/email-marketing-benchmarks/
- label: ICO Guide to GDPR for Direct Marketing
  url: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/
---

## Why Email Automation Matters

Email remains one of the highest-ROI channels in digital marketing, often returning far more per pound spent than paid social. Automation lets you send the right message to the right person at the right time *without* manually pressing send. As a Junior Social Media Assistant, you'll often own the welcome series, newsletters, and promotional sends.

**Automation** = pre-built email sequences triggered by a subscriber action (e.g. signing up, clicking a link, abandoning a cart).

## Key Mailchimp Concepts

- **Audience (List):** Your central database of contacts. Most small brands use a single audience and organise people inside it.
- **Tags:** Manual or automated labels you attach to contacts (e.g. `webinar-signup`, `VIP`).
- **Segments:** Saved filters based on conditions (e.g. "opened last 3 emails" or "located in London").
- **Customer Journey:** Mailchimp's visual automation builder where you set a *starting point* (trigger) and add *steps* (emails, delays, conditions).
- **Merge tags:** Personalisation placeholders like `*|FNAME|*` that insert a subscriber's first name.

## Step 1 — Set Up Your Audience

1. Go to **Audience > All contacts**.
2. Add a signup form or import contacts (CSV). Only import people who **opted in** — this is a legal requirement under GDPR/CAN-SPAM.
3. Collect at minimum: email address, first name, and signup source.

## Step 2 — Segment Your Audience

Don't blast everyone the same message. Create segments such as:

- **New subscribers** (joined in last 7 days)
- **Engaged** (opened or clicked recently)
- **Inactive** (no opens in 90 days — candidates for a re-engagement email)

Segments make emails more relevant, which lifts open and click rates and reduces unsubscribes.

## Step 3 — Build an Automated Welcome Sequence

Use **Automations > Customer Journey > Build from scratch**.

A simple 3-email welcome journey:

1. **Trigger:** Contact joins audience / signup form submitted.
2. **Email 1 (immediately):** Warm welcome + what to expect.
3. **Delay:** Wait 2 days.
4. **Email 2:** Share your best content or a brand story.
5. **Delay:** Wait 3 days.
6. **Email 3:** Offer or call-to-action (discount code, free resource).

Add **if/else branches** to send different content based on whether someone opened Email 1.

## Step 4 — Write Emails That Convert

- **Subject line:** Short (under ~50 characters), curiosity or value-driven. This drives open rate.
- **Preview text:** The snippet after the subject — reinforce the subject.
- **Personalisation:** Use `*|FNAME|*` to greet by name.
- **One clear CTA:** A single, obvious button drives click-through rate.
- **Mobile-friendly:** Over half of emails are opened on phones — keep it scannable.

## Step 5 — Measure Performance

Key metrics in the campaign report:

- **Open Rate** = (unique opens ÷ emails delivered) × 100. Typical benchmark ~20–35%.
- **Click-Through Rate (CTR)** = (unique clicks ÷ emails delivered) × 100. Typical benchmark ~2–5%.
- **Bounce rate:** Undeliverable emails — high bounces hurt your sender reputation.
- **Unsubscribe rate:** If high, your content or frequency may be off.

> Note: Apple Mail Privacy Protection inflates open rates, so treat clicks as the more reliable engagement signal.

## Step 6 — Optimise with A/B Testing

Mailchimp lets you test variables like subject line, send time, or content. Send each version to a sample, and the winner (by opens or clicks) goes to the rest of the list. Test **one variable at a time**.

## List Hygiene Best Practices

- Remove or re-engage inactive contacts regularly.
- Always include an unsubscribe link (legally required).
- Never buy email lists — it damages deliverability and breaks the law.

## Capstone Tie-In

For your portfolio, document a complete automated welcome journey: include a screenshot of the Customer Journey map, your three email drafts, the segment you targeted, and a short report explaining the open/click results and what you'd improve.
