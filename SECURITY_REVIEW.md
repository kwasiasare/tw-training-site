# Security Review — Training Website (TW-19)

**Date:** 2026-06-19 · **Scope:** SWA managed Functions (`api/`), Astro site (`site/`),
auth config, signed-URL video delivery, secrets & repo hygiene. **Method:** manual review +
two automated sweeps (secret scan over working tree + full git history; frontend XSS/data-flow).

## Summary

Overall posture is **good**. Authn/authz is correctly delegated to SWA with sound route gating,
all Cosmos queries are parameterized and user-scoped (no injection / IDOR), and **no secrets are
committed** (tree or history). One real DOM-XSS bug and several hardening gaps were found; the
code-fixable ones are fixed in this change. Two items need a product/ops decision (below).

Severity: **BLOCKER** must fix before launch · **MAJOR** fix before launch w/ sign-off ·
**MINOR** fix when convenient · **INFO** note.

---

## AC1 — Auth & token validation: **PASS** (1 minor)

- Microsoft Entra External ID via SWA custom OIDC. Functions run `authLevel: 'anonymous'` and
  trust (a) SWA route-level role gating and (b) the SWA-injected `x-ms-client-principal` header,
  decoded in `api/src/shared/principal.js` (returns `null` on missing/malformed/no-userId — safe).
- Route rules (`site/public/staticwebapp.config.json`) are correctly ordered: specific anonymous
  exceptions (`/api/GetRoles` for the rolesSource callback, `/api/video` for free previews) precede
  the `/api/*` → `authenticated` catch-all; `/api/stats` & `/api/profile` are `authenticated`;
  `/admin*` is `administrator`. `stats` **also** re-checks the admin role in-function (defense in depth).
- **Trust boundary (by design):** SWA *managed* Functions have no independent public hostname, so the
  `x-ms-client-principal` header cannot be forged from outside the SWA front door. This assumption is
  the basis of the auth model — if the API is ever migrated to bring-your-own Functions, the header
  must be re-validated server-side.
- **[MINOR] (CWE-200) `/api/GetRoles` is anonymously callable and reveals admin emails.** Anyone can
  POST an email and learn whether it is an administrator. No privilege is granted (SWA only applies
  these roles during a genuine server-side login), so impact is limited to admin-email enumeration.
  *Recommend:* accept (low risk) or have GetRoles return roles only for a verified pipeline call.

## AC2 — Signed-URL & data-access: **PASS w/ 1 product decision**

- `api/src/functions/video.js`: lesson slug is regex+length validated, the R2 object key is derived
  **server-side** (`<slug>.mp4`) so the client cannot request arbitrary paths (no traversal), URLs
  are short-lived (1h) presigned **GET**s, and denials return **403** (not 401) to avoid the
  signin-redirect turning the player fetch into HTML. `r2.js` presigns locally; creds from env. ✔
- Cosmos access (`enroll`, `progress`, `profile`, `stats`): **all queries parameterized** (no NoSQL
  injection), scoped by the **validated** `userId` from the principal; document ids and partition
  keys derive from `userId`, not from input → **no IDOR**. `stats` does a full scan but is admin-gated. ✔
- **[MAJOR] (CWE-285) Video access is authenticated but NOT enrollment-gated.** `video.js` grants a
  signed URL to *any* logged-in user for *any* lesson; enrollment records exist but are never checked.
  This contradicts TW-32's acceptance criteria ("verifies auth + enrollment", "denies non-enrolled
  users"). **Decision needed:** if all content is meant to be available to any signed-in user (the
  current de-facto model — first 2 lessons free, the rest login-gated), update TW-32's AC to
  "auth-gated"; if courses are meant to be segmented, add an enrollment check in `video.js`.
- **[FIXED] DOM-XSS in `site/public/progress.js`.** The `course` value from `/api/progress` was
  concatenated into `innerHTML` unescaped (the only page lacking the `esc()` discipline used by
  `/account` and `/admin`). A signed-in user can POST an arbitrary `course` string and have it execute
  on their own `/account` (stored self-XSS). **Fix:** added an `esc()` helper and escaped the value.
- **[FIXED] (CWE-20) Missing input validation on `course`/`lesson`.** `enroll`/`progress` accepted
  arbitrary free-text → data pollution (e.g. fake lesson names surfacing in admin stats) and the
  untrusted-render root cause above. **Fix:** both now require a slug (`^[a-z0-9-]+$/i`, ≤80 chars;
  matches real ids incl. `kwasi-GenAI`), with tests.

## AC3 — Secrets & least privilege: **PASS**

- **Secret scan CLEAN.** No secrets in the working tree or anywhere in git history (`git log -S`
  pickaxe over `--all`). `.gitignore` ignores `.env`/`*.env` and allows `.env.example` (verified
  placeholder-only across its history). The on-disk `.env` holds real keys but is correctly gitignored
  and untracked. The three `cloudflarestorage` hits are interpolated/placeholder URLs, not literals.
- **[FIXED]** Added `local.settings.json` / `api/local.settings.json` to `.gitignore` (defense in
  depth — the repo has an Azure Functions `api/` dir; that file would hold real connection strings).
- **[INFO] Least-privilege (ops verification, not code):**
  - R2 API token used by `r2.js` should be scoped **read-only** on the single `tw-course-videos`
    bucket (presigning only needs Object Read). Verify in the Cloudflare dashboard.
  - Cosmos uses a full `COSMOS_CONNECTION_STRING` (primary key = full access). Consider a scoped/RBAC
    credential for the Functions if Cosmos RBAC is adopted.
  - `ADMIN_EMAILS` lives in SWA app settings (not in repo) — good.

## Additional hardening

- **[FIXED]** Added `globalHeaders` to the SWA config: `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`,
  `Strict-Transport-Security: max-age=31536000; includeSubDomains`.
- **[MINOR, follow-up] Content-Security-Policy not set.** A strict CSP is the strongest XSS
  defense-in-depth but the site uses inline `<script>` blocks (e.g. `VideoEmbed.astro`, `set:html`
  JSON islands), so it needs per-build nonces/hashes. Tracked as a follow-up, not done here to avoid
  breaking the player.
- **[INFO] `stats` 500 returns `detail: err.message`** (`stats.js`) — internal error text, admin-only
  surface. Low risk; can be dropped.

---

## Fixes applied in this change

1. `site/public/progress.js` — escape API `course` value before `innerHTML` (DOM-XSS fix).
2. `api/src/functions/enroll.js`, `progress.js` — slug-validate `course`/`lesson` (+ tests).
3. `site/public/staticwebapp.config.json` — security `globalHeaders`.
4. `.gitignore` — ignore `local.settings.json`.

## Open items (no code change here)

| # | Item | Severity | Owner |
|---|------|----------|-------|
| 1 | Enrollment gating for video vs. update TW-32 AC | MAJOR | Product |
| 2 | Verify R2 token is read-only; consider scoped Cosmos cred | INFO | Ops |
| 3 | Add a CSP (needs inline-script nonces) | MINOR | Eng (follow-up) |
| 4 | `/api/GetRoles` admin-email enumeration | MINOR | accept / Eng |
