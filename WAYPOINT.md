# 🚩 WAYPOINT — resume point (safe to restart the PC)

_Last updated before a planned PC restart. Everything below is on disk and survives a reboot.
The only thing that stops on restart is the local dev server (just re-run it — see below)._

## ▶️ RIGHT NOW — what we were about to do
**Deploy the current site to Azure Static Web Apps, with videos served from Cloudflare R2.**

**Blocked on you:** set up Cloudflare R2 and add credentials to `.env` (project root). Steps are
in the chat ("Set up Cloudflare R2"). Add these keys to `.env`, then tell Claude "done":
```
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET=tw-course-videos
R2_PUBLIC_BASE=https://pub-xxxxx.r2.dev
```

**Then Claude will (automatically):**
1. Upload all 65 videos in `site/public/videos/` to the R2 bucket (boto3, S3 API).
2. Rebuild the site with `PUBLIC_VIDEO_CDN_BASE=<R2_PUBLIC_BASE>` so videos load from R2.
3. Strip `dist/videos` so nothing heavy is bundled.
4. `az staticwebapp create` (Free tier) + deploy `dist` via the SWA CLI → live URL.
   (Azure CLI is already logged in as kasare@spreadcomgh.com, "Azure subscription 1".)

## ✅ DONE so far
- **Course content:** 65 lessons authored. Word study packs (`Month_*_Study_Pack.docx`),
  `00_Master_Curriculum.docx`, `AI_Career_Plan.docx`, `AI_Study_Guide.pptx`, project spec.
- **Website:** Astro site in `site/` — builds clean, 66 pages (home + 65 lessons),
  interactive quizzes, video embeds. Data-driven from `videos/_decks/*.json`.
- **Videos:** all **65 rendered** in `site/public/videos/` (273 MB), alternating
  Azure neural voices (odd lesson = Jenny female, even = Guy male).
- **Jira:** project **TW "Training-Website"** (spreadcomgh.atlassian.net) — 8 epics
  (TW-1..TW-8) + 46 stories, the full platform backlog.
- **Decisions:** platform = Azure SWA + Entra External ID + Cosmos DB + Functions;
  video = Cloudflare R2 (zero egress). `.env` holds Azure Speech key (region eastus).

## 🔧 How to restart the dev server (to test locally again)
```
cd "C:\Users\KwasiAsare\OneDrive - Spreadcom Ltd\Desktop\claude-01\Dami\site"
npm run dev          # then open http://localhost:4321/
```

## 🗂️ Key files / scripts (all in project root unless noted)
- `doc_helpers.py` + `make_*.py` — generate the Word/PPTX study materials.
- `make_slides.py`, `azure_tts.py`, `build_one_video.py`, `batch_render.py`,
  `render_narration_azure.py` — the deck→slides→narration→MP4 video pipeline
  (azure_tts now has retry/backoff; voice alternates by lesson parity).
- `convert_decks_to_md.py` — `videos/_decks/<slug>.json` → `site/src/content/topics/<slug>.md`.
- `videos/_decks/*.json` — the 65 lesson decks (source of truth for pages + videos).
- `site/src/consts.ts` — curriculum outline + `videoCdnBase` (reads PUBLIC_VIDEO_CDN_BASE).
- `site/src/components/{Quiz,VideoEmbed}.astro`, `site/src/pages/topics/[...id].astro`.
- `.env` — secrets (git-ignored): Azure Speech, soon Cloudflare R2.

## 🧭 After deploy — suggested next work (the TW backlog)
MVP slice: **TW-1** (repo + SWA + CI/CD) → **TW-3** (auth) → **TW-4** (progress tracking)
→ **TW-5** (R2 signed URLs / proper video delivery). Admin dashboard = TW-6.

## ⚠️ Notes
- Not a git repo yet (TW-1 covers this). Consider `git init` before deploying.
- The 273 MB of videos are intentionally NOT meant for the SWA bundle — they go to R2.
- Background dev server (id may differ after restart) — just re-run `npm run dev`.
