# HOWTO — Spreadcom Learning YouTube Channel (host all courses)

A step-by-step guide to launch the **Spreadcom Learning** YouTube channel and upload all course
videos as one **public** playlist per course. Written so you can do it later, unattended.

- **Brand:** Spreadcom Learning · handle `@SpreadcomLearning`
- **Visibility:** Public (for reach + SEO), driving viewers to https://www.salloma.com
- **Upload method:** manual bulk upload in YouTube Studio, using the generated metadata sheet
  (the YouTube API caps uploads at ~6/day, so manual is far faster for this volume)

---

## 0. Where everything is

The ready-to-use **kit** is generated to a local (non-OneDrive) folder so it isn't deleted by sync:

```
C:\Temp\spreadcom-marketing\youtube\
├─ spreadcom-learning-banner.png / .jpg     2560×1440 channel banner
├─ spreadcom-learning-avatar.png / .jpg     800×800 channel avatar
├─ youtube_upload_metadata.csv              one row per video: title, description, tags, visibility, R2 url
├─ playlists.md                             12 playlist titles + descriptions
├─ channel_about.md                         channel name, handle, description, keywords, links
├─ upload_runbook.md                        the short version of this guide
└─ download_all_videos_from_r2.py           pulls every video to per-course folders
```

The **scripts that regenerate the kit** live in the repo at `youtube-kit/` (see §7).

> If `C:\Temp\spreadcom-marketing\youtube\` is missing (e.g. new machine), regenerate it — see **§7**.

**Inventory at last generation:** 12 courses · 388 lesson-videos in the sheet · **348 already on R2
(ready to upload)** · 256 also on local disk · 40 not yet rendered (in-progress Phase-2 lessons).

---

## 1. Create and brand the channel  (browser, ~15 min)

1. Sign in to YouTube with the **brand Google account** (not a personal one).
2. **Settings → Add or manage your channel(s) → Create a channel.** Use a **Brand Account** so the
   channel can be co-managed by more than one person later.
3. Name it **Spreadcom Learning**. Claim the handle **@SpreadcomLearning**
   (Settings → Channel → Advanced, or in Customize → Basic info).
4. **Customize channel → Branding:**
   - **Picture:** upload `spreadcom-learning-avatar.png`
   - **Banner image:** upload `spreadcom-learning-banner.png` (the text is inside YouTube's safe area,
     so it stays visible on TV, desktop and mobile)
   - **Video watermark:** reuse the avatar
5. **Customize channel → Basic info:** paste the **description**, **keywords**, and the **website link**
   (`https://www.salloma.com`, label "Start free →") from `channel_about.md`.
6. **Settings → Channel → Feature eligibility:** verify the account (phone) to unlock custom
   thumbnails and uploads longer than 15 min.

---

## 2. Get every video onto the computer

- **256** videos are already in `course-materials\<slug>\videos\`.
- To stage **all 348** (organized per course) in one place, run from the repo root:
  ```powershell
  python youtube-kit\download_all_videos_from_r2.py
  ```
  Files land in `C:\Temp\spreadcom-marketing\youtube\videos\<course_slug>\`. It is **idempotent**
  (skips files already downloaded), so it's safe to re-run.
- The **40 not-yet-rendered** lessons can be produced later with the video pipeline, then uploaded:
  ```powershell
  $env:COURSE_SLUG="<slug>"; python batch_render.py        # renders missing decks → MP4
  $env:COURSE_SLUG="<slug>"; python upload_videos_r2.py     # (optional) push them to R2 too
  ```

---

## 3. Bulk-upload, one course at a time

1. **YouTube Studio → Create → Upload videos.** Drag a course folder's `.mp4` files
   (`…\youtube\videos\<course_slug>\`). You can queue many; ~15 process at once.
2. Open **`youtube_upload_metadata.csv`** (UTF-8 — opens cleanly in Excel or Google Sheets).
   It is sorted **course → module → lesson**. Match each upload by the **`video_filename`** column.
3. For each video, copy in:
   - **Title** ← `youtube_title`
   - **Description** ← `description` (already leads with the lesson summary + salloma.com link +
     the free CTA, so the link sits above the fold)
   - **Tags** ← `tags`
4. **Visibility = Public.** (Or use **Schedule** to drip 1–2 per day for steadier algorithm signals.)
5. **Audience:** "No, it's not made for kids." **Category:** Education.

> Tip: do one full course end-to-end first (e.g. `cloud-security-engineer`, 28–29 videos) to settle
> your rhythm before doing the big ones (`dami-ai-career` 65, `helpdesk-tier1-2` 61).

---

## 4. Build the playlists (one per course)

1. **Studio → Content → Playlists → New playlist.** Create one **Public** playlist per course —
   titles + descriptions are in **`playlists.md`**.
2. Add each course's videos **in CSV row order** (module → lesson) so lessons play in sequence.
   You can also add a video to its playlist directly from the upload dialog.

The 12 playlists: AI Application Developer · Applied GenAI Engineer · Cloud Security Engineer ·
Data Scientist · Machine Learning Engineer · MLOps Engineer · AI App Developer · Agentic AI Engineer ·
AI Product Manager · IT Helpdesk Tier 1-2 · IT Helpdesk Tier 3 (Advanced) · Junior Digital Marketing.

---

## 5. Polish & SEO

- **Homepage layout (Customize → Layout):** add a **Featured section per playlist** so visitors see
  all 12 tracks; pin a short channel trailer for non-subscribers.
- **End screens** (last ~20 s of each video): "next lesson" + a link to https://www.salloma.com.
- Keep the **salloma.com link in the first 2 lines** of every description (the CSV already does this).
- Custom thumbnails are optional — the rendered title slide already reads well as a fallback.
- Add the channel/playlist links back on the site for cross-promotion (see §6).

---

## 6. (Optional) Wire the channel into the site

- Put `custom-training-og-1200x630.png` in `site/public/` and add Open Graph tags so shared links
  show a rich preview:
  ```html
  <meta property="og:image" content="https://www.salloma.com/custom-training-og-1200x630.png" />
  <meta name="twitter:card" content="summary_large_image" />
  ```
- Add a "Watch on YouTube" link in the site footer once the channel URL is live.

---

## 7. Regenerate / refresh the kit later (when courses change)

The kit is data-driven from the lesson files, so after adding lessons/courses just re-run the
generators from the repo root (needs `pip install pyyaml boto3 pillow`; R2 creds are read from `.env`):

```powershell
python youtube-kit\generate_youtube_kit.py     # rebuilds youtube_upload_metadata.csv (+ checks R2)
python youtube-kit\generate_youtube_docs.py    # rebuilds playlists.md, channel_about.md, runbook
python youtube-kit\make_youtube_art.py         # rebuilds banner + avatar
```

All outputs go to `C:\Temp\spreadcom-marketing\youtube\`. The CSV's `local_exists` / `on_r2` columns
tell you exactly what's ready to upload and what still needs rendering.

---

## 8. Notes & troubleshooting

- **Why not auto-upload via API?** `videos.insert` costs 1,600 of the default 10,000 daily quota units
  (~6 uploads/day). For 348 videos that's ~2 months unless you request a quota increase. Manual bulk
  upload has no such limit. If you still want automation, request a quota bump in Google Cloud and ask
  for the API uploader script.
- **Copyright/Content ID:** all narration is your Azure-TTS audio and all slides are your own assets, so
  there's nothing third-party to trip Content ID. Music, if you add any later, must be licensed.
- **Files vanished from a repo folder?** This repo lives under OneDrive, which deletes untracked files
  from synced folders. That's why the kit is written to `C:\Temp\…`; keep durable docs/scripts
  **committed** (tracked files are safe).
- **Video source of truth:** every published lesson video is in the R2 bucket `tw-course-videos`
  (public base `https://pub-178640b0d3e549d097dc751f9d1b9867.r2.dev`), named `<lesson-slug>.mp4`.
