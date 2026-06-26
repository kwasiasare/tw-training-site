---
course: cloud-security-engineer
title: 'Capstone: Enterprise Cloud Threat-Hunting Dashboard'
month: 6
monthTitle: Capstone Projects & Career Launch
lesson: 3
summary: Leadership wants one place to see security across a multi-cloud estate. In this capstone you
  stand up a Microsoft Sentinel workspace, ingest signals from Entra ID, Microsoft 365, Azure Activity,
  and AWS, and write a custom KQL analytics rule that detects impossible travel, the same user signing
  in from two distant locations within minutes. You then connect that detection to a Logic App playbook
  that disables the account and routes it to PIM and analyst review, and you build a Workbook dashboard
  for leadership. You will write the KQL, build the SOAR automation, validate the end-to-end flow, and
  package it as a portfolio-grade SIEM/SOAR project. It draws directly on Modules 4 and 5.
objectives:
- Stand up a Microsoft Sentinel workspace and connect Entra, M365, Azure Activity, and AWS data connectors
- Write a custom KQL scheduled analytics rule that detects impossible-travel / concurrent anomalous logins
- Map alert entities (account, IP) so detections drive automated response
- Build a Logic App playbook that disables the account and routes the case to PIM and analyst review
- Validate the detection-to-response flow end to end with controlled test sign-ins
- Build a Workbook dashboard and assemble the KQL, playbook, and screenshots into a hireable portfolio
  artifact
video: cse-m6-l03-capstone-cloud-threat-hunting-dashboard.mp4
quiz:
- q: Why is Microsoft Sentinel a strong choice for centralized multi-cloud security reporting in this
    scenario?
  options:
  - It only works with Azure resources and nothing else
  - It is a cloud-native SIEM/SOAR that ingests signals from Microsoft and non-Microsoft sources (including
    AWS) and combines detection, hunting, and automated response in one workspace
  - It replaces the need for any data connectors
  - It stores data only on local analyst machines
  answer: 1
  why: Sentinel is a cloud-native SIEM and SOAR. With data connectors it ingests Entra, M365, Azure Activity,
    and AWS (CloudTrail/security data), then lets you run KQL analytics, hunting, workbooks, and playbooks
    over the unified data, which is exactly what 'one place to see security across multi-cloud' requires.
- q: In the impossible-travel KQL, why do you join the sign-in table to itself on the same UserPrincipalName?
  options:
  - To remove duplicate rows from the table
  - To compare two sign-in events for the same user and measure the time and distance between two different
    locations
  - Because KQL requires every query to use join
  - To convert the table into a workbook
  answer: 1
  why: A self-join pairs each sign-in with another sign-in by the same user, so you can compute the time
    gap and the geographic distance between the two events. That pairing is what lets you flag the same
    identity appearing in two far-apart places within an implausibly short window.
- q: What is the role of entity mapping in the analytics rule?
  options:
  - It makes the query run faster
  - It tags fields like the account and IP as recognized entities so the incident is investigable and
    so playbooks can act on those entities automatically
  - It encrypts the alert
  - It is only needed for workbooks, not rules
  answer: 1
  why: Entity mapping identifies the account, host, and IP within each alert. This enriches the incident
    graph for investigation and, critically, gives the playbook the structured entity (the account) it
    needs to disable the right user automatically rather than parsing free text.
- q: Why route the response through a Logic App playbook that disables the account AND sends it to PIM/analyst
    review, rather than only disabling the account silently?
  options:
  - Because Logic Apps cannot disable accounts
  - To combine fast automated containment with human oversight and a path to restore least-privilege access,
    reducing both risk and the chance of a disruptive false positive going unreviewed
  - Because PIM is required to run any Logic App
  - To make the playbook slower on purpose
  answer: 1
  why: Automated disablement contains the threat in seconds, but impossible travel can be a false positive
    (VPN, corporate proxy). Pairing automation with analyst review and a PIM-governed restore path gives
    speed without removing human judgment, and ensures access is brought back under least-privilege controls
    rather than ad hoc.
- q: When validating, how can you safely simulate impossible travel without traveling or using a real
    attacker?
  options:
  - Wait for a real attack to occur in production
  - Generate test sign-ins for a test account from two different network locations (e.g., a VPN exit in
    another country) within a short window, or inject crafted sample sign-in logs
  - Disable all logging during the test
  - Delete the analytics rule and recreate it
  answer: 1
  why: Using a dedicated test account, you can sign in from your normal location and then via a VPN exit
    node in a distant country within a few minutes, which produces two far-apart sign-ins. Alternatively
    you can inject crafted sample SigninLogs. Either approach drives the rule without any real compromise.
- q: 'In two to four sentences, explain the design trade-offs of the impossible-travel rule: what makes
    it valuable, what causes false positives, and one tuning step you would apply before enabling auto-disable
    in production.'
  answer: Impossible travel is valuable because it catches credential theft and session hijacking that
    single-event rules miss, the same identity cannot physically be in Massachusetts and abroad ten minutes
    apart. Its main false-positive sources are corporate VPNs, cloud proxies, mobile carrier NAT, and
    roaming, which make legitimate users appear to jump locations. Before enabling auto-disable I would
    tune the rule by excluding known corporate egress IP ranges and trusted named locations, requiring
    the second sign-in to be from an untrusted or risky IP, and possibly correlating with an Entra ID
    Protection risk signal, and I might start the playbook in 'require analyst approval' mode rather than
    fully automatic. This keeps detection sensitive while preventing disruptive mass lockouts.
  why: A strong answer names the detection value (catches what single-event rules miss), concrete false-positive
    drivers (VPN/proxy/roaming), and at least one real tuning lever (trusted-location/IP exclusion, risk
    correlation, or analyst-approval gating) before full automation.
resources:
- label: Microsoft Sentinel documentation
  url: https://learn.microsoft.com/en-us/azure/sentinel/overview
- label: Create custom analytics rules to detect threats (Sentinel)
  url: https://learn.microsoft.com/en-us/azure/sentinel/detect-threats-custom
- label: Automate threat response with playbooks in Microsoft Sentinel
  url: https://learn.microsoft.com/en-us/azure/sentinel/automate-responses-with-playbooks
- label: Connect Sentinel to Amazon Web Services to ingest AWS service log data
  url: https://learn.microsoft.com/en-us/azure/sentinel/connect-aws
---

## Scenario

The CISO is tired of swivel-chairing between the Entra portal, the Microsoft 365 admin center, the Azure portal, and the AWS console to answer one question: 'Are we under attack right now?' Leadership wants **one centralized security dashboard across the multi-cloud estate**, with automated response for the obvious wins. Your capstone delivers exactly that with **Microsoft Sentinel**: a single SIEM/SOAR workspace that ingests identity and cloud signals, detects **impossible travel** (the same user appearing in two distant locations within minutes, classic credential theft), automatically contains the account, and visualizes it all for leadership.

This is the headline project for Modules 4 (Cloud SIEM & SOAR with Sentinel) and 5 (Security Automation with PowerShell, Graph, and Logic Apps). It proves you can run a cloud SOC, write detections in KQL, and automate response, the core of a modern security engineering role.

## Architecture

Five components, left to right:

1. **Ingestion - Data connectors.** A Sentinel workspace on a Log Analytics workspace, with connectors for **Microsoft Entra ID** (SigninLogs, AuditLogs), **Microsoft 365** (Defender/Office activity), **Azure Activity**, and **AWS** (CloudTrail / AWS security data via the S3 connector). Now Entra sign-ins and AWS API activity live in one query surface.
2. **Detection - Custom KQL analytics rule.** A scheduled rule runs the impossible-travel query on **SigninLogs** every few minutes, emitting an alert/incident when the same user signs in from two far-apart locations inside a short window.
3. **Enrichment - Entity mapping.** The rule maps **Account** (UserPrincipalName) and **IP** as entities so the incident is investigable and the playbook can act on the account.
4. **Response - Logic App playbook.** An automation rule triggers a **Sentinel playbook** (Logic App) that **disables the user in Entra ID via Microsoft Graph**, posts the case to the SOC channel/ticket, and routes it to **PIM**/analyst review for a governed restore.
5. **Reporting - Workbook dashboard.** A Sentinel **Workbook** visualizes sign-ins by country, top risky IPs, impossible-travel incidents over time, and AWS activity, the leadership view.

## The impossible-travel KQL

The heart of the project. This scheduled rule self-joins `SigninLogs` to pair two successful sign-ins by the same user, then flags pairs that are geographically far apart but close in time, for example one from Massachusetts and one from a foreign IP within 10 minutes:

```kusto
let timeWindow = 10m;
let lookback = 1h;
let successful =
    SigninLogs
    | where TimeGenerated > ago(lookback)
    | where ResultType == 0                 // successful sign-ins only
    | extend City = tostring(LocationDetails.city),
             Country = tostring(LocationDetails.countryOrRegion),
             Lat = todouble(LocationDetails.geoCoordinates.latitude),
             Lon = todouble(LocationDetails.geoCoordinates.longitude)
    | project TimeGenerated, UserPrincipalName, IPAddress, City, Country, Lat, Lon;
successful
| join kind=inner (
    successful
    | project-rename TimeGenerated2 = TimeGenerated, IPAddress2 = IPAddress,
                     City2 = City, Country2 = Country, Lat2 = Lat, Lon2 = Lon
  ) on UserPrincipalName
| where TimeGenerated < TimeGenerated2                     // ordered pair, no self-match
| where TimeGenerated2 - TimeGenerated <= timeWindow        // within the short window
| where Country != Country2 or IPAddress != IPAddress2      // genuinely different origin
| extend DistanceKm = geo_distance_2points(Lon, Lat, Lon2, Lat2) / 1000.0
| where DistanceKm > 500                                    // implausibly far apart
| extend MinutesApart = datetime_diff('minute', TimeGenerated2, TimeGenerated)
| project UserPrincipalName, TimeGenerated, City, Country, IPAddress,
          TimeGenerated2, City2, Country2, IPAddress2, DistanceKm, MinutesApart
```

Key ideas: filter to **successful** sign-ins (`ResultType == 0`), **self-join on UserPrincipalName** to compare two events for one identity, use `geo_distance_2points` for great-circle distance, and require both a large distance and a short time gap. In the rule wizard, set the schedule (run every 5-10 min, lookback 1h), map **Account = UserPrincipalName** and **IP = IPAddress**, and set incident creation on.

## Step-by-step build

**Step 0 - Prerequisites.** An Azure subscription with a Log Analytics workspace, an Entra tenant generating sign-ins, and (optionally) an AWS account for the AWS connector. Use evaluation/free tiers.

**Step 1 - Onboard Sentinel.** Create/choose a Log Analytics workspace and enable Microsoft Sentinel on it.

**Step 2 - Connect data.** Install the **Microsoft Entra ID** connector and enable SigninLogs + AuditLogs (via Diagnostic settings). Add **Microsoft 365** and **Azure Activity** connectors. Add the **Amazon Web Services** connector (S3-based) to pull CloudTrail. Confirm tables populate (`SigninLogs`, `AWSCloudTrail`).

**Step 3 - Create the analytics rule.** New > **Scheduled query rule**; paste the KQL; set frequency/lookback; map entities; enable **Create incidents**; set severity Medium/High.

**Step 4 - Build the playbook.** Create a **Logic App** playbook triggered by *Microsoft Sentinel incident*. Steps: parse the **Account** entity; call **Microsoft Graph** (or the Entra connector) to **disable the user** (`accountEnabled = false`) and/or revoke sessions; post an adaptive card to Teams/create a ticket; add a task to **review in PIM**. Attach it via an **automation rule** so qualifying incidents run it automatically (or with analyst approval).

**Step 5 - Build the workbook.** Create a **Workbook** with tiles: sign-ins by country (map), impossible-travel incidents over time, top source IPs, and AWS CloudTrail activity. This is the leadership dashboard.

## Validation / Testing

Drive the whole chain safely:

- **Simulate impossible travel:** with a dedicated **test account**, sign in from your normal location, then within a few minutes sign in again through a **VPN exit node in another country**. Two far-apart successful sign-ins now exist in `SigninLogs`. (Alternatively, inject crafted sample `SigninLogs` rows.)
- **Confirm detection:** run the KQL manually in Logs to see the pair returned; then wait for the scheduled rule to fire and create an **incident** with the account and IP entities mapped.
- **Confirm response:** verify the playbook ran, the **test account is disabled** in Entra (and sessions revoked), the **Teams card/ticket** posted, and a **PIM/analyst review** task exists.
- **Confirm false-positive handling:** repeat using a *trusted* corporate VPN IP that you have added to **trusted named locations**, and show the rule does NOT fire, demonstrating your tuning.
- **Confirm dashboard:** the Workbook shows the incident on the map and timeline.

Keep a *Stage | Test | Expected | Observed | Pass/Fail* table and capture screenshots at each stage.

## What to put in your portfolio

- **Architecture diagram**: connectors -> Sentinel -> analytics rule -> playbook -> workbook.
- **The KQL detection** as a clean, commented `.kql` file in your repo (this is the single most impressive artifact, interviewers will ask you to read it line by line).
- **The playbook**: exported Logic App JSON / ARM template, with the account-disable and PIM-routing steps.
- **Workbook export** (JSON) and screenshots of the leadership dashboard.
- **A short demo video** of the impossible-travel simulation triggering the incident, the auto-disable, and the dashboard updating.
- **A design doc** covering the detection logic, the false-positive tuning, and why you gated full automation behind analyst review.

Resume bullet, impact-first: 'Built a Microsoft Sentinel SIEM/SOAR with multi-cloud connectors (Entra, M365, Azure, AWS); authored a KQL impossible-travel detection wired to a Logic App playbook that auto-disables compromised accounts and routes them to PIM review, containing credential-theft incidents in under a minute.'
