# Monitoring & Alerting Runbook (TW-42)

Operational visibility for the Training Website (Azure SWA `tw-training-site`, RG `training-site`).

## Resources

| Resource | Name | RG | Notes |
|----------|------|----|-------|
| Application Insights (workspace-based) | `tw-appinsights` | training-site | App/telemetry store |
| Log Analytics workspace | `tw-logs` | training-site | Backing workspace (PerGB2018) |
| Action group | `tw-alerts` | training-site | Emails **kasare@spreadcomgh.com** |

Cost: ingestion-based; first 5 GB/mo free. At current traffic this is effectively $0.

## What's instrumented

- **Functions (`api/`)** — auto-collected by the Azure Functions host via the SWA app setting
  `APPLICATIONINSIGHTS_CONNECTION_STRING`. Captures requests, dependencies, **failures**,
  **server exceptions**, and **server response time** with no code changes.
- **Frontend (Astro site)** — `@microsoft/applicationinsights-web` initialised in
  `site/src/components/Analytics.astro`, rendered from `BaseLayout` only when
  `PUBLIC_APPINSIGHTS_CONNECTION_STRING` is set at build time. Captures page views, route
  changes, AJAX (`/api/*`) timing, and unhandled JS exceptions.

### Connection-string wiring

| Where | Key | Purpose |
|-------|-----|---------|
| SWA app settings (prod) | `APPLICATIONINSIGHTS_CONNECTION_STRING` | Functions auto-collection |
| GitHub Actions **variable** | `PUBLIC_APPINSIGHTS_CONNECTION_STRING` | passed to the site build (`azure-swa-deploy.yml`) → exposed to the client SDK |

The instrumentation key in the connection string is a **write-only ingestion key**, intentionally
embeddable in client pages — it is not a secret. (Tracked for CSP allow-listing in TW-59.)

## Alerts (metric alerts → `tw-alerts`)

| Name | Condition | Window | Severity |
|------|-----------|--------|----------|
| `tw-failed-requests` | failed requests (count) > 5 | 5 min | 2 (Warning) |
| `tw-server-exceptions` | server exceptions (count) > 5 | 15 min | 2 (Warning) |
| `tw-server-latency` | avg server response time > 3000 ms | 5 min | 3 (Informational) |

Thresholds are launch defaults — tune in *App Insights → Alerts* once real traffic baselines exist.

### Availability (one-time portal step — not scripted)

Classic ping web tests are being retired, and the CLI path for **Standard** tests is unreliable, so
add it via the portal (~1 min):

1. `tw-appinsights` → **Availability** → **+ Add Standard test**.
2. URL `https://gray-river-01e111b0f.7.azurestaticapps.net/`, frequency 5 min, a few regions.
3. On the test, **enable the auto-created alert rule** and point its action group at `tw-alerts`.

(Once the custom domain from TW-36 is live, repoint the test URL to it.)

## Dashboards

App Insights ships the panes that satisfy the AC out of the box:

- **Failures** — failed request/exception rates and the top failing operations (errors).
- **Performance** — server + client response-time distributions (latency).
- **Usage** — users, sessions, page views, most-visited pages (usage).

Useful starter KQL (App Insights → Logs):

```kql
// Failure rate, last 24h, 1h bins
requests | where timestamp > ago(24h)
| summarize total=count(), failed=countif(success==false) by bin(timestamp,1h)
| extend failRate = round(100.0*failed/total,2)
```
```kql
// Slowest API operations
requests | where timestamp > ago(24h)
| summarize p95=percentile(duration,95), count() by name | order by p95 desc
```
```kql
// Top pages (client)
pageViews | where timestamp > ago(7d) | summarize views=count() by name | order by views desc
```

## Re-provisioning (reference)

```bash
# Workspace + App Insights
az monitor log-analytics workspace create -g training-site -n tw-logs -l eastus2
az monitor app-insights component create --app tw-appinsights -g training-site -l eastus2 \
  --kind web --application-type web --workspace <tw-logs resource id>
# Wire it
az staticwebapp appsettings set -n tw-training-site -g training-site \
  --setting-names "APPLICATIONINSIGHTS_CONNECTION_STRING=<connection string>"
gh variable set PUBLIC_APPINSIGHTS_CONNECTION_STRING --body "<connection string>"
# Alerts (action group + 3 metric alerts) — see commands in git history for TW-42.
```
