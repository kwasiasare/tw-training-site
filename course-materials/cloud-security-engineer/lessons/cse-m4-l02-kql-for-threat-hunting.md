---
course: cloud-security-engineer
title: KQL for Threat Hunting
month: 4
monthTitle: Cloud SIEM & SOAR Operations with Microsoft Sentinel
lesson: 2
summary: 'KQL (Kusto Query Language) is the language every Sentinel detection, hunt, and workbook is built
  on, so fluency here pays off everywhere else in the module. This lesson builds your skills from a single
  filter up to a real multi-table hunting query, covering the operators that do ninety percent of the
  work: where, project, extend, summarize ... by, count, sort/top, join, union, and let. You will master
  datetime math with ago() and bin(), the difference between has and contains, parsing fields out of messy
  strings, and arg_max() for getting the latest record per entity. Throughout you work against the real
  tables a SOC hunts in every day: SigninLogs, AuditLogs, SecurityEvent, DeviceProcessEvents, and DeviceNetworkEvents.
  By the end you can write runnable hunting queries that find failed sign-in bursts, rare process executions,
  and suspicious account activity.'
objectives:
- Filter and shape data with where, project, and extend
- Aggregate with summarize, count(), dcount(), and the by clause, bucketing time with bin()
- Order and trim results using sort, top, and take
- Combine tables with join and stack sources with union
- Use let to parameterize hunts and arg_max() to get the latest record per entity
- Apply ago() and datetime math, parse, and the has vs contains distinction in real hunting queries
video: cse-m4-l02-kql-for-threat-hunting.mp4
quiz:
- q: Why is `has` usually preferred over `contains` when filtering a string column in KQL?
  options:
  - has is case-sensitive and contains is not
  - has matches whole indexed terms and is faster, while contains does a slower substring scan
  - contains cannot be used inside a where clause
  - has automatically deduplicates the result set
  answer: 1
  why: has matches on whole terms using the column's term index, so it is much faster on large tables.
    contains does an unindexed substring match anywhere in the value, which is slower and can produce
    noisy partial matches. Use contains only when you genuinely need a substring that is not a whole term.
- q: What does `summarize count() by bin(TimeGenerated, 1h), IPAddress` produce?
  options:
  - A single total count for the whole table
  - One row per IP with its most recent event time
  - A count of events grouped into one-hour time buckets per IP address
  - The raw events sorted by time and IP
  answer: 2
  why: bin() rounds TimeGenerated down to the start of each one-hour window, and summarize ... by groups
    on that bucket plus IPAddress, so you get a count of events per IP per hour. This time-bucketing is
    the standard way to build trends and spot bursts.
- q: You need the single most recent sign-in record for each user, keeping all that record's columns.
    Which is correct?
  options:
  - summarize max(TimeGenerated) by UserPrincipalName
  - summarize arg_max(TimeGenerated, *) by UserPrincipalName
  - top 1 by TimeGenerated
  - distinct UserPrincipalName, TimeGenerated
  answer: 1
  why: arg_max(TimeGenerated, *) returns the row with the maximum TimeGenerated for each group and the
    * keeps every column from that winning row. max() alone returns only the timestamp, losing the rest
    of the record; top 1 limits the whole result, not per user.
- q: What is the key difference between `union` and `join` in KQL?
  options:
  - union stacks rows from multiple tables together; join matches rows across tables on a shared key
  - union matches rows on a key; join stacks rows vertically
  - They are identical aliases for the same operation
  - union only works on numeric columns; join only on strings
  answer: 0
  why: union appends the rows of two or more tables into one result (vertical stacking), useful for combining
    similar event streams. join correlates rows from two tables horizontally where a key matches (for
    example linking a sign-in to a device event by account), letting you enrich or pivot across sources.
- q: Why use `let` at the top of a hunting query?
  options:
  - It is required before any summarize statement
  - It permanently stores results in a new Sentinel table
  - It defines reusable variables or sub-results, making the query readable and easy to tune
  - It converts the query into an analytics rule automatically
  answer: 2
  why: let binds a value, list, or even a tabular sub-query to a name. You can set a lookback window,
    a threshold, or a list of known-bad IPs once at the top and reuse it, which makes hunts self-documenting
    and lets you tune one number instead of editing the body in several places.
- q: Write, in plain English plus a short KQL sketch, how you would hunt for accounts experiencing a brute-force
    pattern of failed sign-ins from a single IP in the last 24 hours, and name two fields you would group
    or threshold on.
  answer: Start from SigninLogs over the last 24 hours and keep only failures, where ResultType != 0 (or
    the non-zero error codes). Then summarize a count and a distinct count of targeted accounts per source
    IP and per hour, for example summarize Failures = count(), Accounts = dcount(UserPrincipalName) by
    IPAddress, bin(TimeGenerated, 1h). Finally filter for IPs that exceed a threshold, such as where Failures
    > 50 and Accounts > 5, which indicates one IP spraying many accounts rather than a single user mistyping
    a password. The fields I group and threshold on are IPAddress (the source) and the count of failures
    plus the distinct count of UserPrincipalName (the spread across accounts).
  why: A real brute-force or password-spray hunt filters SigninLogs to failures, aggregates by source
    IP and time, and thresholds on both volume and the number of distinct accounts targeted, distinguishing
    an attack from ordinary user error.
resources:
- label: KQL quick reference
  url: https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/kql-quick-reference
- label: Hunt for threats with Microsoft Sentinel
  url: https://learn.microsoft.com/en-us/azure/sentinel/hunting
- label: summarize operator reference
  url: https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/summarize-operator
- label: Microsoft Sentinel SigninLogs table reference
  url: https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/signinlogs
---

## Why KQL Is the Core Skill

Every analytics rule, every hunt, every workbook tile, and most automation triggers in Microsoft Sentinel are **KQL queries** underneath. If you can write KQL, you can detect, investigate, and report; if you can't, you are stuck clicking other people's content. KQL is a **read-only pipeline language**: you start with a table and pipe (`|`) it through operators that filter, reshape, aggregate, and join. Data flows left to right, top to bottom, and each operator transforms the rows coming into it.

The good news: about eight operators do ninety percent of real hunting. We'll build them up from a single filter to a full multi-table hunt.

## Filter and Shape: where, project, extend

Start by **filtering early** with `where` — it cuts the data the rest of the pipeline must process. `project` selects (and renames) only the columns you want; `extend` adds a new calculated column.

```kusto
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != 0          // 0 means success; non-zero is a failure
| project TimeGenerated, UserPrincipalName, IPAddress, ResultType, AppDisplayName
| extend FailureHour = bin(TimeGenerated, 1h)
```

Note `ago(24h)` — KQL has first-class **datetime math**. `ago(7d)`, `now()`, and arithmetic like `TimeGenerated > ago(1h)` are everywhere. Always put a time filter first; it is the cheapest, highest-impact filter you can apply.

## Aggregate: summarize, count, by, bin

`summarize` is the workhorse. It collapses many rows into grouped aggregates using functions like `count()`, `dcount()` (distinct count), `sum()`, `min()`, and `max()`, grouped by the columns after `by`. Bucketing time with `bin()` turns raw events into trends.

```kusto
// Failed sign-ins per source IP per hour over the last day
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != 0
| summarize Failures = count(), Accounts = dcount(UserPrincipalName)
    by IPAddress, bin(TimeGenerated, 1h)
| sort by Failures desc
```

This already looks like a detection: failures grouped by source IP and hour, plus how many distinct accounts each IP hit. An IP with high `Failures` **and** high `Accounts` is password-spraying.

## Order and Trim: sort, top, take

`sort by ... desc` orders results; `top N by Col` returns the N highest rows (a sort plus a limit); `take N` grabs an arbitrary N rows for a quick peek (not ordered, useful only for sampling).

```kusto
// The 10 noisiest source IPs by failed sign-ins
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != 0
| summarize Failures = count() by IPAddress
| top 10 by Failures desc
```

## Find the Rare: summarize + thresholds

Threat hunting is often about **finding the rare**, not the common. On endpoints, a process that has only ever run a handful of times can be far more interesting than the busiest one. Group, count, then filter on the count.

```kusto
// Rarely-seen process executions in the last 7 days
DeviceProcessEvents
| where TimeGenerated > ago(7d)
| summarize Executions = count(),
            Devices = dcount(DeviceName),
            FirstSeen = min(TimeGenerated),
            LastSeen = max(TimeGenerated)
    by FileName, FolderPath
| where Executions <= 3 and Devices <= 2
| sort by Executions asc
```

Processes that ran only a couple of times on only a couple of devices are exactly where novel attacker tooling hides.

## Combine Sources: union and join

`union` **stacks** rows from similar tables; `join` **correlates** rows across tables on a shared key.

```kusto
// union: combine interactive and non-interactive sign-in failures
union SigninLogs, AADNonInteractiveUserSignInLogs
| where TimeGenerated > ago(24h)
| where ResultType != 0
| summarize Failures = count() by UserPrincipalName
| sort by Failures desc
```

```kusto
// join: which accounts that failed sign-in also spawned suspicious processes?
let failedAuth =
    SigninLogs
    | where TimeGenerated > ago(24h)
    | where ResultType != 0
    | distinct UserPrincipalName;
DeviceProcessEvents
| where TimeGenerated > ago(24h)
| where FileName in~ ("powershell.exe", "cmd.exe", "wscript.exe")
| join kind=inner (failedAuth) on $left.AccountUpn == $right.UserPrincipalName
| project TimeGenerated, AccountUpn, DeviceName, FileName, ProcessCommandLine
```

The `kind=inner` keeps only rows that match on both sides. Other kinds (`leftouter`, `leftanti`) let you find rows that are present in one table but missing in another — `leftanti` is great for "first time we've ever seen this."

## let, parse, has vs contains, and arg_max

Four finishing skills tie real hunts together.

**`let`** binds reusable values or sub-queries at the top, so you tune one number instead of many:

```kusto
let lookback = 24h;
let failThreshold = 50;
SigninLogs
| where TimeGenerated > ago(lookback)
| where ResultType != 0
| summarize Failures = count(), Accounts = dcount(UserPrincipalName) by IPAddress
| where Failures > failThreshold and Accounts > 5
```

**`has` vs `contains`:** `has` matches whole indexed **terms** and is fast; `contains` does a slow substring scan. Prefer `has`.

```kusto
SecurityEvent
| where TimeGenerated > ago(24h)
| where EventID == 4688                    // a new process was created
| where CommandLine has "Invoke-WebRequest" // term match, fast
| project TimeGenerated, Computer, Account, NewProcessName, CommandLine
```

**`parse`** pulls structured fields out of messy strings:

```kusto
DeviceNetworkEvents
| where TimeGenerated > ago(24h)
| where RemoteUrl has "login"
| parse RemoteUrl with "https://" Host "/" *
| summarize Connections = count() by Host, DeviceName
| sort by Connections desc
```

**`arg_max`** returns the full record with the maximum value per group — the standard way to get the **latest** state per entity:

```kusto
// Latest sign-in per user, keeping all columns of that record
SigninLogs
| where TimeGenerated > ago(7d)
| summarize arg_max(TimeGenerated, *) by UserPrincipalName
| project UserPrincipalName, TimeGenerated, IPAddress, Location, ResultType
```

## Putting It Together: a Real Hunt

Here is a complete, runnable hunt that finds source IPs spraying many accounts and enriches each with the account it most recently succeeded against — the kind of query you'd save as a Sentinel hunting query and later promote to an analytics rule.

```kusto
let lookback = 24h;
let sprayIPs =
    SigninLogs
    | where TimeGenerated > ago(lookback)
    | where ResultType != 0
    | summarize Failures = count(), Accounts = dcount(UserPrincipalName) by IPAddress
    | where Failures > 50 and Accounts > 5;
SigninLogs
| where TimeGenerated > ago(lookback)
| where ResultType == 0                       // successful sign-ins
| join kind=inner (sprayIPs) on IPAddress
| summarize arg_max(TimeGenerated, UserPrincipalName, Location) by IPAddress, Failures, Accounts
| project IPAddress, Failures, Accounts, CompromisedHint = UserPrincipalName, Location, TimeGenerated
| sort by Failures desc
```

That single query filters, aggregates, thresholds, joins, and takes the latest record per group — every core operator working together. You are now ready to turn hunts like this into scheduled analytics rules.
