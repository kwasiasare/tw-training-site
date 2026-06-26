---
course: cloud-security-engineer
title: Analytics Rules and MITRE ATT&CK Mapping
month: 4
monthTitle: Cloud SIEM & SOAR Operations with Microsoft Sentinel
lesson: 3
summary: 'A hunting query only finds threats when you run it; an analytics rule finds them automatically
  and turns matches into incidents your SOC can work. This lesson turns the KQL you wrote in Lesson 2
  into production detections: scheduled rules with frequency, lookback, and thresholds; entity mapping
  so incidents show real users, hosts, and IPs; and alert grouping that collapses related alerts into
  a single incident. You will also meet near-real-time (NRT) rules for low-latency detection, the built-in
  Fusion and machine-learning anomaly detections, and disciplined false-positive tuning. Every detection
  is mapped to MITRE ATT&CK tactics and techniques so you can read the coverage view and find gaps. The
  centerpiece is a runnable impossible-travel / concurrent-anomalous-login detection, the exact rule used
  in Capstone 3, plus how watchlists enrich and tune your rules.'
objectives:
- Create a scheduled analytics rule from a KQL query, setting frequency, lookback, and threshold
- Configure entity mapping so incidents surface accounts, hosts, and IP addresses
- Group related alerts into incidents and choose when to use near-real-time (NRT) rules
- Explain Fusion and machine-learning anomaly detections and when to rely on them
- Tune rules to cut false positives using thresholds, exclusions, and watchlists
- Map detections to MITRE ATT&CK tactics/techniques and read the coverage view
- Build and reason about an impossible-travel concurrent-login detection in KQL
video: cse-m4-l03-analytics-rules-and-mitre-attack-mapping.mp4
quiz:
- q: In a scheduled analytics rule, what is the relationship you must respect between query frequency
    and lookback period?
  options:
  - Frequency must always be longer than the lookback
  - Lookback should be at least as long as the frequency so no events fall between runs
  - They must be exactly equal at all times
  - Lookback has no relationship to frequency
  answer: 1
  why: If the lookback window is shorter than how often the rule runs, events occurring in the gap between
    runs are never evaluated. Setting lookback greater than or equal to frequency (often with a small
    overlap buffer) ensures continuous coverage; overlap can cause duplicate alerts, which alert grouping
    helps manage.
- q: What is the purpose of entity mapping in an analytics rule?
  options:
  - It speeds up the KQL query execution
  - It identifies columns as entities (account, host, IP) so incidents support investigation and correlation
  - It encrypts the alert payload
  - It schedules the rule to run more often
  answer: 1
  why: Entity mapping tells Sentinel which query columns represent real-world entities such as Account,
    Host, IP, or URL. Mapped entities appear on the incident, power the investigation graph, enable correlation
    across alerts, and let automation act on them. Without it, an alert is just a row of text with no
    pivot points.
- q: When is a near-real-time (NRT) rule the right choice over a standard scheduled rule?
  options:
  - When you need complex multi-table joins over weeks of data
  - When you need the lowest possible detection latency on a simple single-table condition
  - When you want to run machine-learning anomaly detection
  - When you need to query archived logs
  answer: 1
  why: NRT rules run approximately every minute to minimize the delay between an event and its alert,
    but they are limited (essentially a single source table and no unions/joins of multiple tables). They
    are ideal for high-priority, simple conditions where speed matters; complex correlation still belongs
    in scheduled rules.
- q: What does Sentinel's Fusion engine primarily do?
  options:
  - It merges duplicate workspaces into one
  - It correlates multiple lower-fidelity alerts and anomalies into high-confidence, multistage incidents
  - It compresses logs to reduce ingestion cost
  - It translates KQL into natural language
  answer: 1
  why: Fusion is a built-in, ML-based correlation engine that links seemingly unrelated lower-severity
    alerts and anomalies across the kill chain into a single high-confidence, multistage attack incident,
    surfacing attacks that no single rule would flag on its own.
- q: Which tuning technique best reduces false positives from a noisy detection without blinding you to
    real attacks?
  options:
  - Disable the rule entirely
  - Raise the threshold and exclude known-benign entities using a watchlist of approved sources
  - Shorten the lookback so fewer events are seen
  - Set the rule severity to Informational
  answer: 1
  why: Raising the threshold filters out low-volume noise, and excluding vetted benign sources (for example
    known admin jump hosts or sanctioned scanners) via a watchlist removes recurring false positives while
    keeping the detection live for everything else. Disabling the rule or hiding it as Informational simply
    loses the detection.
- q: Explain in 3-4 sentences how an impossible-travel detection works, why a naive distance check produces
    false positives, and one enrichment that reduces them.
  answer: An impossible-travel rule looks for the same account signing in from two different locations
    within a time window so short that physically traveling between them is impossible, implying at least
    one session is not the real user. It typically computes the geographic distance between consecutive
    sign-in locations and divides by the time between them to get an implied speed, alerting when that
    speed exceeds what air travel allows. A naive version produces false positives because VPNs, corporate
    proxies, mobile-carrier IP geolocation, and cloud egress can place the same legitimate user in far-apart
    locations within minutes. Enriching with a watchlist of known corporate VPN and proxy egress IP ranges
    (or trusted named locations) and excluding those sign-ins removes a large share of the noise while
    keeping genuine concurrent-location anomalies.
  why: Impossible travel infers an impossible implied travel speed between two sign-in locations for one
    account; the main false-positive source is VPN/proxy geolocation, which watchlists of trusted egress
    IPs and named locations help suppress.
resources:
- label: Create scheduled analytics rules in Microsoft Sentinel
  url: https://learn.microsoft.com/en-us/azure/sentinel/detect-threats-custom
- label: Map data fields to entities in analytics rules
  url: https://learn.microsoft.com/en-us/azure/sentinel/map-data-fields-to-entities
- label: Advanced multistage attack detection (Fusion)
  url: https://learn.microsoft.com/en-us/azure/sentinel/fusion
- label: Use watchlists in Microsoft Sentinel
  url: https://learn.microsoft.com/en-us/azure/sentinel/watchlists
---

## From Hunt to Detection

In Lesson 2 you wrote hunting queries. A hunt only finds threats **when a human runs it**. An **analytics rule** runs your KQL **on a schedule, automatically**, and converts matches into **alerts and incidents** your SOC works in a queue. This lesson turns your KQL into production detections and maps every one to **MITRE ATT&CK** so you can prove coverage and find gaps.

Sentinel offers several rule types: **scheduled** (custom KQL on a timer — your bread and butter), **near-real-time (NRT)** (low-latency, simple conditions), **Microsoft Security** (auto-create incidents from Defender alerts), **Fusion** (ML multistage correlation), and **anomaly** (built-in ML baselines). We focus on scheduled and NRT, then the ML rules.

## Anatomy of a Scheduled Rule: Frequency, Lookback, Threshold

When you create a scheduled rule you set:

- **Query frequency** — how often the rule runs (e.g., every 5 minutes, every hour).
- **Query lookback (period)** — how far back each run looks. **Lookback must be at least as long as frequency**, or events that occur between runs are never evaluated. A small overlap is common; alert grouping then handles any duplicates.
- **Alert threshold** — generate an alert only when the query returns more than N results (e.g., > 0, or > 5), filtering low-volume noise.
- **Event/alert grouping** — whether each row is its own alert or all results in a run form one alert, and how alerts roll into incidents.
- **Severity** and **MITRE technique** tags.

```kusto
// Detection logic for a scheduled rule: password-spray success
// Frequency: 1h, Lookback: 1h
let failThreshold = 50;
let sprayIPs =
    SigninLogs
    | where ResultType != 0
    | summarize Failures = count(), Accounts = dcount(UserPrincipalName) by IPAddress
    | where Failures > failThreshold and Accounts > 5;
SigninLogs
| where ResultType == 0
| join kind=inner (sprayIPs) on IPAddress
| project TimeGenerated, UserPrincipalName, IPAddress, Failures, Accounts
```

## Entity Mapping and Alert Grouping

An alert is useless if it is just text. **Entity mapping** tells Sentinel which columns are real-world **entities** — `Account`, `Host`, `IP`, `URL`, `FileHash`. Mapped entities appear on the incident, drive the **investigation graph**, allow correlation across alerts, and give automation something to act on (disable *this account*, block *this IP*).

For the rule above you'd map:

- **Account** identifier → `UserPrincipalName`
- **IP** address → `IPAddress`

**Alert grouping** then decides how alerts become incidents. Grouping alerts that share the same entities (e.g., the same account) within a time window collapses a storm of related alerts into **one incident**, so analysts see one story instead of fifty rows. This is also how you tame the duplicates that come from overlapping lookback windows.

## NRT, Fusion, and Anomaly Detections

**Near-real-time (NRT)** rules run about **once a minute** to minimize detection latency. The trade-off: they are deliberately simple — essentially a single source table, no multi-table `union`/`join`. Use NRT for high-priority, simple conditions (e.g., a specific high-risk sign-in or a known-bad process) where **speed** beats sophistication.

**Fusion** is a built-in **ML correlation engine**. It links lower-fidelity alerts and anomalies across the kill chain — say an anomalous sign-in followed by mailbox-rule creation followed by mass download — into a **single high-confidence, multistage incident** that no individual rule would raise. You don't write Fusion logic; you enable it and triage what it surfaces.

**Anomaly** rules ship ML baselines (e.g., unusual volume of sign-in failures for an account vs. its own history). You can tune their thresholds and run them in *flighting* mode before enabling.

## Tuning to Reduce False Positives

The fastest way to lose a SOC's trust is a noisy rule. Tune deliberately:

1. **Raise the threshold** so genuinely low-volume noise drops out.
2. **Exclude known-benign entities** — sanctioned scanners, admin jump hosts, corporate VPN egress IPs.
3. **Use a watchlist** to hold those exclusions as data you can update without editing the rule (more below).
4. **Group alerts** so repeats collapse into one incident.
5. **Measure** — review the rule's alert volume and true/false-positive ratio, then iterate. Never disable a valuable detection just because it is noisy; tune it.

## Watchlists

A **watchlist** is a small reference table you upload (CSV) and join against in KQL — lists of VIP accounts, terminated employees, trusted VPN/proxy egress IP ranges, or asset inventories. They keep tuning data **out of the query body** so non-developers can maintain it.

```kusto
// Suppress sign-ins coming from approved corporate VPN egress IPs
let TrustedEgress = _GetWatchlist('TrustedVPNIPs') | project IPAddress;
SigninLogs
| where TimeGenerated > ago(1h)
| where IPAddress !in (TrustedEgress)
```

## The Impossible-Travel Detection (Capstone 3)

Now the centerpiece. **Impossible travel** flags one account signing in from two locations so far apart, so close in time, that the implied travel speed is physically impossible — meaning at least one session is not the real user. The technique: for each account, line up consecutive sign-ins, compute the **geo distance** between their locations and the **time delta**, derive an implied **km/h**, and alert when it exceeds what air travel allows.

```kusto
// Impossible-travel / concurrent anomalous login
// Frequency: 1h, Lookback: 1h. MITRE: Initial Access (T1078 Valid Accounts)
let lookback = 1h;
let maxSpeedKmH = 900.0;          // faster than a commercial jet => impossible
let TrustedEgress = _GetWatchlist('TrustedVPNIPs') | project IPAddress;
SigninLogs
| where TimeGenerated > ago(lookback)
| where ResultType == 0                                  // successful sign-ins only
| where IPAddress !in (TrustedEgress)                    // drop corporate VPN/proxy noise
| where isnotempty(LocationDetails.geoCoordinates.latitude)
| extend lat = toreal(LocationDetails.geoCoordinates.latitude),
         lon = toreal(LocationDetails.geoCoordinates.longitude),
         City = tostring(LocationDetails.city),
         Country = tostring(LocationDetails.countryOrRegion)
| sort by UserPrincipalName asc, TimeGenerated asc
| serialize
| extend prevLat = prev(lat), prevLon = prev(lon),
         prevTime = prev(TimeGenerated), prevCity = prev(City),
         prevUser = prev(UserPrincipalName), prevIP = prev(IPAddress)
| where UserPrincipalName == prevUser                    // compare within the same user
| extend DistanceKm = geo_distance_2points(lon, lat, prevLon, prevLat) / 1000.0
| extend HoursApart = datetime_diff('second', TimeGenerated, prevTime) / 3600.0
| where HoursApart > 0
| extend ImpliedSpeedKmH = DistanceKm / HoursApart
| where DistanceKm > 500 and ImpliedSpeedKmH > maxSpeedKmH
| project TimeGenerated, UserPrincipalName,
          FromCity = prevCity, FromIP = prevIP,
          ToCity = City, ToIP = IPAddress,
          DistanceKm = round(DistanceKm, 0),
          HoursApart = round(HoursApart, 2),
          ImpliedSpeedKmH = round(ImpliedSpeedKmH, 0)
```

Map **Account** → `UserPrincipalName` and **IP** → `ToIP` (and optionally `FromIP`). The watchlist of trusted VPN/proxy egress IPs is what keeps this rule from drowning in false positives — the single most important tuning step. Tag it to MITRE **Initial Access / T1078 Valid Accounts**.

## MITRE ATT&CK Mapping and the Coverage View

Every rule should declare the **tactics** (the attacker's goal — Initial Access, Persistence, Exfiltration) and **techniques** (the how — T1078, T1110) it detects. Sentinel's **MITRE ATT&CK coverage view** then renders the matrix colored by how many active rules cover each technique, so you can **see your blind spots** at a glance: a column with no detections is a tactic an attacker could move through unseen. Use it to prioritize which detections to build next — coverage, not raw rule count, is what protects you.
