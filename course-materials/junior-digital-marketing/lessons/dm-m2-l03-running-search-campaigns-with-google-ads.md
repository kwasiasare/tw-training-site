---
course: junior-digital-marketing
title: Running Search Campaigns with Google Ads
month: 2
monthTitle: Paid Advertising with Meta & Google Ads
lesson: 3
summary: 'Learn to build a Google Ads search campaign from the ground up: setting goals, structuring ad
  groups around tight keyword themes, choosing keyword match types, writing high-performing responsive
  search ads, and adding extensions and negatives to keep spend efficient.'
objectives:
- Explain how Google Search ads work and the role of the ad auction and Quality Score
- Structure a campaign into themed ad groups with relevant keywords
- Select appropriate keyword match types and add negative keywords
- Write compelling responsive search ads with strong headlines, descriptions, and assets
- Set budgets, bidding strategies, and conversion tracking to measure results
video: dm-m2-l03-running-search-campaigns-with-google-ads.mp4
quiz:
- q: What three components mainly determine your Ad Rank in the Google Search auction?
  options:
  - Bid, Quality Score, and ad asset impact
  - Budget, brand name, and website age
  - Number of keywords, account age, and bid
  - Click-through rate only
  answer: 0
  why: Ad Rank combines your maximum bid, your Quality Score (expected CTR, ad relevance, landing page
    experience), and the expected impact of assets and formats.
- q: Which match type gives you the tightest control over which searches trigger your ad?
  options:
  - Broad match
  - Phrase match
  - Exact match
  - Negative match
  answer: 2
  why: Exact match [keyword] only shows your ad for searches with the same meaning as the keyword, giving
    the most control over targeting.
- q: What is the main purpose of negative keywords?
  options:
  - To increase your maximum bid automatically
  - To stop ads showing for irrelevant searches and save budget
  - To improve landing page speed
  - To create new ad groups
  answer: 1
  why: Negative keywords prevent your ads from appearing on searches you don't want, reducing wasted spend
    and improving relevance.
- q: Why should you avoid pinning every headline in a responsive search ad?
  options:
  - Pinning is not allowed by Google
  - Pinning increases cost per click directly
  - Pinning limits Google's ability to test combinations and can lower Ad Strength
  - Pinning deletes other headlines
  answer: 2
  why: Pinning locks headlines to fixed positions, reducing the combinations Google can test, which often
    lowers Ad Strength and performance. Pin only when necessary.
- q: In one sentence, why must conversion tracking be set up before using smart bidding like Target CPA?
  answer: Because smart bidding relies on conversion data to optimise; without tracking it has no signal
    to bid toward and you can't measure results.
  why: Smart bidding strategies use conversion data to make decisions, so tracking must be in place first
    to provide the signal and to prove ROI.
- q: What is the recommended rule of thumb when organising keywords into ad groups?
  answer: Keep one tight theme per ad group so keywords and ads match closely, improving relevance and
    Quality Score.
  why: Tightly themed ad groups ensure ads are highly relevant to the keywords, which raises Quality Score
    and lowers costs.
resources:
- label: 'Google Ads Help: About responsive search ads'
  url: https://support.google.com/google-ads/answer/7684791
- label: 'Google Ads Help: About keyword matching options'
  url: https://support.google.com/google-ads/answer/7478529
- label: 'Google Skillshop: Google Ads Search Certification'
  url: https://skillshop.exceedlms.com/student/path/18103-google-ads-search-certification
- label: 'Google Ads Help: About Quality Score'
  url: https://support.google.com/google-ads/answer/6167118
---

## Why Search Campaigns Matter

Google Search campaigns show text ads to people who are *actively searching* for what you offer. Because the user has high intent (they typed the query), search ads often deliver strong return on ad spend. Your job as a junior assistant is to make sure the right ad shows for the right query at the right cost.

## How the Search Auction Works

Every time someone searches, Google runs an instant auction. Your ad position and cost depend on **Ad Rank**, which combines:

- **Your bid** – the maximum you'll pay for a click
- **Quality Score** – Google's 1-10 rating based on expected click-through rate, ad relevance, and landing page experience
- **Ad assets and formats** – extensions and other enhancements

A higher Quality Score means you can rank higher while paying *less* per click. So relevance is not just good practice — it saves money.

## Account Structure

Good structure keeps ads relevant and easy to manage:

```
Account
 └── Campaign (budget, location, bidding)
      └── Ad Group (one theme / keyword set)
           ├── Keywords
           └── Responsive Search Ads
```

**Rule of thumb:** one tight theme per ad group. For a shoe shop, don't mix "running shoes" and "hiking boots" in one ad group. Split them so each ad group's ads and keywords match.

## Keywords and Match Types

Match types control how closely a search must match your keyword:

- **Broad match** `running shoes` – widest reach, can trigger loosely related searches. Use with smart bidding and watch closely.
- **Phrase match** `"running shoes"` – searches that include the meaning of the phrase.
- **Exact match** `[running shoes]` – searches with the same meaning as the keyword. Tightest control.

**Negative keywords** stop your ads showing for irrelevant terms (e.g. add `free`, `jobs`, `repair` if you don't want those). Review the **Search Terms report** regularly to find new negatives and new keyword ideas.

## Writing Responsive Search Ads (RSAs)

RSAs let you supply up to **15 headlines** and **4 descriptions**; Google mixes them to find top combinations.

Best practices:

- Include your main keyword in at least 2-3 headlines for relevance
- Add benefits, offers, and a clear **call to action** ("Shop Now", "Get a Free Quote")
- Make headlines distinct so combinations don't repeat
- Pin sparingly — pinning a headline to position 1 limits Google's testing
- Aim for an **Ad Strength** of "Good" or "Excellent"

## Ad Assets (Extensions)

Add assets to take up more space and give users more reasons to click:

- **Sitelinks** – links to specific pages
- **Callouts** – short phrases like "Free Delivery"
- **Structured snippets** – lists (e.g. Brands, Services)
- **Call asset** – phone number

## Budgets, Bidding & Conversions

- Set a realistic **daily budget**; Google may spend up to 2x on a given day but balances over the month.
- Start with **Maximise Clicks** to gather data, then move to **Maximise Conversions** or **Target CPA/ROAS** once conversion tracking has data.
- **Conversion tracking is essential** — without it, smart bidding is blind and you can't prove results.

## A Simple Build Checklist

1. Define the goal (sales, leads, calls).
2. Set campaign settings: networks (Search only to start), locations, languages, budget, bidding.
3. Create ad groups by theme.
4. Add 5-15 keywords per ad group with chosen match types.
5. Write 2-3 RSAs per ad group; aim for good Ad Strength.
6. Add assets/extensions.
7. Add negative keywords.
8. Confirm conversion tracking is live, then launch and monitor.
