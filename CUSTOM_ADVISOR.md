# Custom Training Advisor (TW-61)

A signed-in user uploads a résumé (PDF) + a short questionnaire. Claude analyses it and
either **matches** them to an existing course (enrolls them) or **queues a bespoke course**
that an offline pipeline generates, reviews, and publishes — the library then **reuses** it
for future matching résumés.

## Flow

```
/custom (sign-in) ──POST /api/custom-advisor──▶ store résumé (private R2)
   │                                            └▶ Claude analysis (Opus 4.8, structured JSON)
   │                                               └▶ match library? ─ yes ▶ enroll
   │                                                                 ─ no  ▶ queue generationRequest
   ▼
generate-course Action (manual dispatch)  →  author (Claude) → decks→md → render videos
   →  upload to R2  →  register in catalog (+ catalog.generated.json) →  DRAFT PR (human review)
   →  merge = publish + reusable
```

## Components

| Piece | Where |
|---|---|
| Intake page | `site/src/pages/custom.astro` (flag `PUBLIC_CUSTOM_ADVISOR_ENABLED`) |
| API | `api/src/functions/custom-advisor.js` — `GET` (status) / `POST` (analyse+match) / `DELETE` (forget) |
| Claude analysis | `api/src/shared/advisor.js` (`claude-opus-4-8`, `output_config.format` + `effort:'low'`) |
| Matcher | `api/src/shared/matcher.js` + `catalog.js` (+ `catalog.generated.json`) |
| Résumé storage | `api/src/shared/resumes.js` → private R2 bucket `tw-resumes` |
| Generator | `generate_course.py`, `add_course_to_consts.py`, `build_catalog.py`, `.github/workflows/generate-course.yml` |

## Privacy & data handling

- **Collected:** the résumé PDF, the questionnaire answers, and the derived analysis/plan.
- **Stored:** the résumé in the **private** R2 bucket `tw-resumes` (never public, never the videos
  bucket), keyed `‹userId›/‹ts›.pdf`; the analysis + outcome + consent flag in Cosmos (`‹userId›:advisor`).
- **Consent:** required (checkbox) before upload; the consent flag is persisted with the advisor doc.
- **Deletion (right to be forgotten):** `DELETE /api/custom-advisor` removes the résumé object **and**
  the advisor + generationRequest docs. Surfaced as a **"Forget my résumé & training data"** button on `/account`.
- **Retention:** set an R2 lifecycle rule on `tw-resumes` to auto-expire objects after **180 days**
  (Cloudflare dashboard → R2 → `tw-resumes` → Settings → Object lifecycle rules; the app's scoped token
  can't set this via API).
- **Least privilege:** the app writes résumés with a token scoped to `tw-resumes` only
  (`RESUME_R2_*`), separate from the videos token.
- **No PII in logs:** the function logs only `Error` objects (`context.error`), never résumé content
  or the API key.

## Security

- **Upload validation (server-side):** PDF magic-byte check (`%PDF-`) + 5 MB cap; slug-style ids.
- **Auth:** `/api/*` is auth-gated by SWA + an in-function principal check.
- **Prompt injection:** the résumé/questionnaire are **untrusted input to the model** — `advisor.js`'s
  system prompt instructs Claude to treat them strictly as data, never instructions, and the
  structured-output schema constrains the response.
- **Output escaping:** all API data is HTML-escaped before `innerHTML` on `/custom` and `/account`.

## Content safety (generated courses)

AI-authored course content is **never auto-published** — the generator opens a **draft PR**; a human
reviews the lessons and merges to publish (TW-66). Reviewer checklist: factual accuracy, no unsafe or
off-topic content, quiz answers correct, lessons map to the intended role.

## Generation pipeline ops

- Manual: **Actions → Generate course → Run workflow** (slug, role, skills, modules, lessons/module).
- Repo **secrets** required: `ANTHROPIC_API_KEY`, `AZURE_SPEECH_KEY/REGION`, `R2_*`.
- One-time GitHub setting: **Allow GitHub Actions to create and approve pull requests** (else the Action
  pushes the branch but can't open the PR).
- **Cost/time:** rendering is slow + costs Azure TTS per lesson; keep courses modest (default 4×4 = 16).

## Cost

- Analysis: `claude-opus-4-8` at `effort:'low'`, ~a few **cents** per submission (~15 s).
- Generation: Claude authoring per lesson + Azure Neural TTS per lesson + R2 storage.

## Config (prod SWA app settings)

`ANTHROPIC_API_KEY`, `R2_ACCOUNT_ID`, `RESUME_R2_ACCESS_KEY_ID`, `RESUME_R2_SECRET_ACCESS_KEY`,
`RESUME_R2_BUCKET` (+ the shared `R2_*` for video signing). Feature flag: GitHub variable
`PUBLIC_CUSTOM_ADVISOR_ENABLED=true`. See `HOWTO_Resume_Storage.md`.
