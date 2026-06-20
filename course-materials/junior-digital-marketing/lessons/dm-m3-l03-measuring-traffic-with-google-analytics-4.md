---
course: junior-digital-marketing
title: Measuring Traffic with Google Analytics 4
month: 3
monthTitle: SEO, Analytics & Performance Measurement
lesson: 3
summary: Learn how to set up Google Analytics 4 (GA4) and navigate its core reports to measure website
  traffic, identify where visitors come from, track conversions, and understand user behavior so you can
  report on marketing performance.
objectives:
- Explain what GA4 is and how its event-based data model differs from older Universal Analytics
- Create a GA4 property and install the tracking tag on a website
- 'Navigate the main GA4 report areas: Reports, Acquisition, Engagement, and Real-time'
- Identify traffic sources and channels using the Acquisition reports
- Set up and read conversions (key events) to measure goal completions
- Read and interpret key metrics like users, sessions, engagement rate, and bounce
video: dm-m3-l03-measuring-traffic-with-google-analytics-4.mp4
quiz:
- q: What is the fundamental unit of data in GA4?
  options:
  - Sessions
  - Events
  - Pageviews
  - Goals
  answer: 1
  why: GA4 uses an event-based data model where every interaction — page views, scrolls, clicks, purchases
    — is recorded as an event.
- q: Which GA4 report would you use to confirm tracking is working right after installing the tag?
  options:
  - Acquisition
  - Real-time
  - Monetization
  - Engagement
  answer: 1
  why: The Real-time report shows activity on the site as it happens, so you can open the site in another
    tab and watch your own visit appear.
- q: A visitor arrives by clicking an unpaid post on Instagram. Which channel will GA4 assign?
  options:
  - Direct
  - Paid Social
  - Organic Social
  - Referral
  answer: 2
  why: Unpaid traffic from social media is categorized as Organic Social. Paid Social would only apply
    to ads.
- q: In GA4, what do you do to turn an important event into a conversion?
  options:
  - Create a Goal in Admin
  - Mark the event as a key event
  - Add a UTM parameter
  - Enable Enhanced Measurement
  answer: 1
  why: GA4 calls conversions 'key events.' You mark an event as a key event in the Events settings to
    start counting it as a conversion.
- q: What does the engagement rate metric measure, and what older metric does it effectively replace?
  answer: Engagement rate is the percentage of sessions that were engaged (lasted 10+ seconds, had a conversion,
    or had 2+ page views). It replaces the old bounce rate.
  why: GA4 favors engagement rate as a more positive, accurate measure; bounce rate in GA4 is simply its
    inverse.
- q: Name the three most common UTM parameters used to tag campaign links.
  answer: utm_source, utm_medium, and utm_campaign
  why: These three parameters tell GA4 where the traffic came from, the channel type, and the campaign
    name, feeding accurate data into the Acquisition reports.
resources:
- label: Google Analytics 4 Official Help Center
  url: https://support.google.com/analytics/answer/10089681
- label: GA4 Skillshop Course (Google's free certification)
  url: https://skillshop.exceedlms.com/student/catalog/list?category_ids=6431-google-analytics-4
- label: Google Analytics Demo Account (practice with real data)
  url: https://support.google.com/analytics/answer/6367342
- label: Campaign URL Builder (create UTM links)
  url: https://ga-dev-tools.google/campaign-url-builder/
---

## Why Google Analytics 4 Matters

As a junior digital marketing assistant, one of your core jobs is answering the question: *"Is our marketing actually working?"* Google Analytics 4 (GA4) is the free tool most businesses use to answer that question. It tells you how many people visit a website, where they came from, what they do once they arrive, and whether they complete the actions that matter (buying, signing up, contacting).

GA4 is the current version of Google Analytics, replacing the older Universal Analytics (UA), which stopped collecting data in July 2023. If you see tutorials mentioning "bounce rate" as the main metric or "Goals," they may be outdated — GA4 works differently.

## The Event-Based Data Model

The biggest change in GA4 is that **everything is an event**. In old Universal Analytics, data was organized around sessions and pageviews. In GA4, every interaction — a page view, a scroll, a click, a video play, a purchase — is recorded as an *event*.

- **Event**: something a user does (e.g. `page_view`, `scroll`, `click`, `session_start`).
- **Parameters**: extra detail attached to an event (e.g. which page, which link).
- **Key events (conversions)**: events you mark as especially important because they represent business goals.

This model lets GA4 track users across both websites and apps, and it is built with privacy and cookieless tracking in mind.

## Setting Up GA4

1. **Create a Google Analytics account** at analytics.google.com.
2. **Create a property** — a property holds the data for one website or app.
3. **Create a data stream** — for a website, choose "Web" and enter the site URL. GA4 generates a **Measurement ID** (looks like `G-XXXXXXXXXX`).
4. **Install the tag** on the website. Two common ways:
   - Paste the **Google tag (gtag.js)** snippet into the `<head>` of every page.
   - Use **Google Tag Manager (GTM)** to deploy the tag without editing code.
5. **Verify** data is flowing using the **Real-time** report — open the site in another tab and watch your visit appear.

GA4 automatically collects some events out of the box (called **Enhanced Measurement**): page views, scrolls, outbound clicks, site search, and file downloads.

## Key Reports You'll Use Daily

### Real-time
Shows who is on the site right now. Great for confirming a campaign launch or that tracking works.

### Acquisition
Answers *"Where did our traffic come from?"* It groups visitors into **channels**:
- **Organic Search** — from search engines like Google (unpaid).
- **Direct** — typed the URL or used a bookmark.
- **Organic Social** — from social media posts (unpaid).
- **Paid Search / Paid Social** — from ads.
- **Referral** — links from other websites.
- **Email** — from email campaigns (when tagged correctly).

### Engagement
Shows what people do: which pages they view, how long they stay, and which events fire.

### Monetization / Conversions
Shows revenue and key events (conversions) like form submissions or purchases.

## Key Metrics Explained

- **Users**: the number of distinct people who visited.
- **Sessions**: visits (one user can have several sessions).
- **Engaged sessions**: sessions lasting 10+ seconds, with a conversion, or 2+ page views.
- **Engagement rate**: % of sessions that were engaged. (GA4's healthier replacement for the old bounce rate.)
- **Bounce rate** (in GA4): the opposite of engagement rate — % of sessions that were *not* engaged.
- **Average engagement time**: how long users actively focused on the site.

## Setting Up Conversions (Key Events)

In GA4, you turn an important event into a conversion by marking it as a **key event**:
1. Go to **Admin → Events** (or **Data display → Events**).
2. Find the event (e.g. `generate_lead`, `purchase`, or a custom event).
3. Toggle **"Mark as key event."**

Now GA4 will count and report each time that action happens, so you can measure goal completions and conversion rates by channel.

## Using UTM Parameters

To make sure GA4 correctly attributes traffic from your campaigns, add **UTM parameters** to your links. Example:

`https://example.com/?utm_source=instagram&utm_medium=social&utm_campaign=spring_sale`

- `utm_source` — where it came from (instagram).
- `utm_medium` — the type of channel (social, email, cpc).
- `utm_campaign` — the campaign name.

These feed straight into the Acquisition reports so you can credit the right channel.

## Practical Tips

- Always check the **date range** in the top corner before reading any report.
- Compare periods (e.g. this month vs last month) to spot trends.
- Don't panic over single-day spikes — look at patterns over time.
- Use **Explore** for custom analysis once you're comfortable with standard reports.
