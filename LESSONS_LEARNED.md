# Lessons Learned — Training Website

Practical lessons captured while building the platform: a multi-course training site
(Astro + Azure Static Web Apps + Cloudflare R2) with two full courses, automated CI/CD,
and a course-production pipeline. Kept current as the project evolves.

---

## Architecture & platform

- **Static-first, offload heavy media.** Pre-render with Astro and serve the ~1 MB site from
  Azure SWA; stream the ~400 MB of videos from Cloudflare R2 (zero egress). Result: hosting is
  effectively free and every deploy is tiny. Bundling video into the site would blow past SWA
  limits and bloat CI.
- **One source of truth prevents drift.** Each lesson is a single JSON *deck*; the website page
  **and** the narrated video are both generated from it. Pages and videos can never disagree.
- **Self-contained course folders scale.** Putting each course's decks/lessons/videos/study-packs
  under `course-materials/<slug>/` made adding a second course a drop-in operation — and turned the
  multi-course platform into a small, data-driven change rather than a rewrite.
- **Derive structure from data, not hardcode.** The site builds its catalog and per-course modules
  from the lessons themselves (a `course` field + `course.json`), so adding content never means
  editing a hardcoded curriculum.
- **Astro's glob loader can read outside `src/`.** `base: '../course-materials'` with a
  `generateId` that returns the filename keeps slugs stable while lessons live with their course.

## Pipeline & content production

- **Parameterise tooling early.** A single `COURSE_SLUG` selector made every script
  (`convert_decks_to_md`, `batch_render`, `build_one_video`, `upload_videos_r2`, `make_study_packs`)
  course-aware. New courses reuse the whole pipeline unchanged.
- **Parallelise authoring with a shared spec.** Six subagents authored 35 lesson decks in parallel,
  each working from one authoring spec + a gold-standard example. Consistency came from the spec;
  **always validate** the output programmatically afterward (we checked JSON validity, required
  fields, slug/filename match, slide counts — 0 problems).
- **Idempotent sync.** The R2 uploader skips same-size objects, so re-runs only push new/changed
  videos — safe to run anytime.

## Git, CI/CD & deployment

- **dev → preview → master, always.** PRs to `master` get a throwaway SWA preview environment;
  merging deploys production. The preview build runs on a **fresh checkout**, which catches things
  local builds hide — e.g. `staticwebapp.config.json` must live in `site/public/` or it's missing
  from the deployed artifact.
- **Stay on `dev`.** After merging a PR and running `git checkout master && git pull`, it's easy to
  keep committing onto `master` by accident. Switch back to `dev` immediately; check
  `git rev-parse --abbrev-ref HEAD` before committing. Recovery: move commits with
  `git checkout dev && git merge master --ff-only`, then `git reset --hard origin/master` on master.
- **Watch every deploy to green.** A push that breaks CI is a failure, not a completion.
- **Deployment-token mismatches are common.** "deployment_token provided was invalid" means the
  GitHub secret doesn't match the SWA — re-set it from `az staticwebapp secrets list`.
- **robocopy `/MOVE` beats a rename when a folder is locked.** Moving the project directory failed
  because a shell held it as its CWD; a file-level `robocopy /MOVE` relocated the contents anyway.

## Azure SWA managed Functions + auth (hard-won)

- **SWA returns 404 — not 403 — when a route's `allowedRoles` check fails.** A protected `/api/*`
  route 404s for users lacking the role, which looks exactly like a missing endpoint. Gate API routes
  at `authenticated` and enforce specific roles **inside the function** (return a real 403) so failures
  are diagnosable.
- **An edited managed-function may not re-register.** Renaming a function's `route`/name across deploys
  had no effect (kept 404ing) while a brand-new function file deployed fine. When a function won't
  update, **create a fresh file with a new name** rather than editing the cursed one.
- **rolesSource roles attach at login.** Custom roles from the `rolesSource` function are stamped into
  the session at sign-in; setting `ADMIN_EMAILS` (or changing role logic) requires a **fresh logout/login**
  to take effect — `/.auth/me` after re-login is the source of truth for roles.
- **App settings are per-environment.** `az staticwebapp appsettings set` targets production; preview
  environments don't inherit them, so auth/DB-backed features can only be fully tested on prod.
- **Custom OIDC (Entra External ID) needs the SWA Standard plan;** the Free plan only does the
  preconfigured providers. The identity service itself is free under 50k MAU.
- **Debug with evidence, not edits.** Two wrong fixes came from guessing the layer. A 12-line anonymous
  `/api/ping` health-check (env presence + a Cosmos COUNT) proved functions deploy and Cosmos works,
  which isolated the real cause in one shot. Peer-review the diagnosis before shipping a fix.

## Verification & ways of working

- **Evidence over assertion.** Every change was proven: build page counts (66 → 103), `curl` status
  codes, R2 `HEAD` checks (`200 / video/mp4`), and grep on built HTML. Don't claim "done" without it.
- **Plan first for multi-step work, check in before heavy implementation.** A short plan with risks
  surfaced the real constraints early (e.g. self-contained courses means rewiring the build, not
  just moving files) and avoided wasted work.
- **Secrets discipline.** `.env` is git-ignored; `.env.example` documents required keys; R2 is
  public-read for now with a documented path to signed URLs when auth lands.

## Theming

- **Separate semantic colours from brand colours.** Headings reused the brand `--navy`, which is
  also a dark *background*; in dark mode that made headings invisible. Splitting out a `--heading`
  variable fixed it. Use translucent `rgba` tints for state colours (quiz correct/wrong) so they
  read on any background.
- **No flash of the wrong theme.** Default to dark on `<html>` and apply the saved preference in an
  inline `<head>` script that runs before paint; persist the toggle to `localStorage`.

## Tooling gotchas (Windows / PowerShell)

- `$HOME` is read-only — don't assign to it. Parentheses inside `$( ... -match '...' )` can break
  the parser; prefer `.Contains()` for simple checks.
- `grep` for a multibyte character (e.g. the `→` arrow) with `.` matches single bytes — verify with
  ASCII-only substrings instead.
- The harness resets the shell working directory each command; target absolute paths or `git -C`.
