# HOWTO — Résumé storage + enabling the Custom Advisor (TW-61)

The Custom Training Advisor stores uploaded résumés (PII) in a **private** Cloudflare
R2 bucket and analyses them with Claude. This guide wires the backend so the feature
can be turned on. The Phase 1 code is already deployed but **flagged off**.

## 0. Prerequisites (already done)
- Claude is configured in the prod SWA app settings: `ANTHROPIC_FOUNDRY_RESOURCE` + `ANTHROPIC_FOUNDRY_API_KEY` (Microsoft Foundry, TW-140), or `ANTHROPIC_API_KEY` as the direct-API fallback.
- `R2_ACCOUNT_ID` is set (shared with the videos bucket).

## 1. Create the private bucket `tw-resumes`

Your normal R2 token is scoped to the videos bucket and **cannot create buckets**, so
pick one:

**Option A — Cloudflare dashboard (simplest):**
1. Cloudflare → **R2** → **Create bucket**.
2. Name: `tw-resumes`. Location: default. **Do NOT enable public access / r2.dev** —
   résumés must stay private.

**Option B — script:** create an **Account-level "Admin Read & Write"** R2 API token,
put it in `.env` as `R2_ADMIN_ACCESS_KEY_ID` / `R2_ADMIN_SECRET_ACCESS_KEY`, then:
```bash
python setup_r2_resumes.py
```
(The script is idempotent and never enables public access.)

## 2. Create a scoped write token for the app
1. Cloudflare → **R2** → **Manage R2 API Tokens** → **Create API token**.
2. Permissions: **Object Read & Write**, scoped to **`tw-resumes` only** (least privilege).
3. Copy the Access Key ID + Secret.

## 3. Wire the app (prod SWA app settings)
Add these to the Static Web App (Configuration → Application settings):
| Setting | Value |
|---|---|
| `RESUME_R2_ACCESS_KEY_ID` | the scoped token's access key id |
| `RESUME_R2_SECRET_ACCESS_KEY` | the scoped token's secret |
| `RESUME_R2_BUCKET` | `tw-resumes` (only if you changed the name) |

(The app falls back to the shared `R2_*` creds if these are unset, but that token can't
write to `tw-resumes`, so set the dedicated ones.)

## 4. Turn the feature on
Set the GitHub Actions **variable** `PUBLIC_CUSTOM_ADVISOR_ENABLED=true`, then re-run
the deploy (push to master or re-run the workflow). The "Custom training" nav link and
`/custom` page become active.

```bash
gh variable set PUBLIC_CUSTOM_ADVISOR_ENABLED --body true
```

## 5. Verify
Sign in on the prod site → **Custom training** → upload a PDF résumé + consent → you
should get the Time-to-Hire table and either a matched course (enrolled) or a
"building your custom course" message. This exercises the live Claude
structured-output call (the one piece mocked in CI).

## Data handling notes
- Résumés are stored only in the private `tw-resumes` bucket, keyed by user id.
- Consent is required before upload; the consent flag is recorded with the advisor doc.
- **Deletion:** `DELETE /api/custom-advisor` removes a user's résumé object + advisor/plan
  docs; users can trigger it from the **"Forget my résumé & training data"** button on `/account`.
- **Retention (action required):** set a **180-day** object lifecycle rule on `tw-resumes` in the
  Cloudflare dashboard (R2 → `tw-resumes` → Settings → Object lifecycle rules). The app's scoped
  token cannot set this via API (`AccessDenied`), so it must be done in the dashboard.
- See `CUSTOM_ADVISOR.md` for the full privacy / security / content-safety review.
