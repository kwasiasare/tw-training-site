# Emit playlists.md, channel_about.md, upload_runbook.md, and download_all_videos_from_r2.py
import os, json, textwrap

OUT = r"C:\Temp\spreadcom-marketing\youtube"
cov = json.load(open(os.path.join(OUT, "_coverage.json"), encoding="utf-8"))
SITE = "https://www.salloma.com"
total = cov["total"]
local_total = sum(cov["local"].values())
r2_total = sum(cov["r2"].values())

def trim(s, n=300):
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"

# ---------- playlists.md ----------
lines = ["# Spreadcom Learning — YouTube Playlists (one per course)\n",
         f"_{len(cov['playlists'])} playlists · {total} videos total ({r2_total} ready on R2, {local_total} also on local disk)._\n",
         "Create each as a **Public** playlist. Add videos in module→lesson order (the CSV is already sorted that way).\n"]
for p in cov["playlists"]:
    slug = p["slug"]; vids = cov["by_course"].get(slug, 0); r2 = cov["r2"].get(slug, 0)
    lines.append(f"\n## {p['title']}")
    lines.append(f"*{vids} videos ({r2} ready on R2) · course slug `{slug}`*\n")
    lines.append("**Playlist description:**")
    lines.append("```")
    lines.append(trim(p["desc"], 500))
    lines.append("")
    lines.append(f"▶ Take the full course free (labs, quizzes, AI tutor, certificate): {SITE}")
    lines.append("✅ 100% free — just register after your first 2 lessons.")
    lines.append("```")
open(os.path.join(OUT, "playlists.md"), "w", encoding="utf-8").write("\n".join(lines))

# ---------- channel_about.md ----------
about = f"""# Spreadcom Learning — YouTube Channel Setup

**Channel name:** Spreadcom Learning
**Handle (suggested):** @SpreadcomLearning
**Tagline:** Free, job-ready tech courses — built around your career.

## Channel description (paste into Settings → Channel → About)
```
Spreadcom Learning offers FREE, job-ready courses for tech careers — IT helpdesk, AI engineering, data science, MLOps, cloud security, AI product management, digital marketing and more.

Every course is project-based and mapped to real 2026 job descriptions, with narrated video lessons, quizzes, an in-lesson AI tutor, and a completion certificate.

The best part: upload your résumé on our site and our AI builds (or matches) a course around YOUR target role.

▶ Start free: {SITE}
✅ 100% free — just register after your first 2 lessons.

New lessons added regularly. Subscribe and turn skills into offers.
```

## Links (Settings → Channel → Customization → Basic info → Links)
- Website: {SITE}  (label: "Start free →")

## Channel keywords (Settings → Channel → Basic info → Keywords)
```
free online courses, learn AI, data science course, machine learning, MLOps, cloud security, SC-500, IT helpdesk, AI engineer, career change tech, upskilling, Spreadcom Learning
```

## Art to upload
- **Profile picture (avatar):** `spreadcom-learning-avatar.png` (800×800)
- **Banner:** `spreadcom-learning-banner.png` (2560×1440; key text sits in the safe area)
- **Video watermark (optional):** reuse the avatar.

## Homepage layout (Customization → Layout)
- Add a **"Featured sections"** row per course playlist (so visitors see all 12 tracks).
- Pin a short channel-trailer or your most popular lesson for non-subscribers.
- Set end screens on each video linking to the next lesson + {SITE}.
"""
open(os.path.join(OUT, "channel_about.md"), "w", encoding="utf-8").write(about)

# ---------- upload_runbook.md ----------
rows_local = local_total
runbook = f"""# Spreadcom Learning — YouTube Upload Runbook

Goal: host all course videos on a **public** channel, one **playlist per course**, with SEO-ready
titles/descriptions. Total in sheet: **{total} videos** across **{len(cov['playlists'])} courses**
(**{r2_total} ready on R2**, **{rows_local} also on local disk**, {total - r2_total} not yet rendered).

> Why manual (not API): YouTube's API caps uploads at ~6/day (1,600 quota units each). For this volume,
> bulk-uploading in YouTube Studio is far faster and has no quota limit.

## 1. Create & brand the channel (browser, ~15 min)
1. Sign in to YouTube with the brand Google account → your avatar → **Create a channel** (or **Settings → Add/manage channels → Create a channel**). Use a **Brand Account** so others can co-manage.
2. Name it **Spreadcom Learning**; set the **@SpreadcomLearning** handle.
3. **Customize channel → Branding:** upload `spreadcom-learning-avatar.png` (picture) and `spreadcom-learning-banner.png` (banner).
4. **Basic info:** paste the description, keywords and website link from `channel_about.md`.

## 2. Get every video onto your computer (~ download)
- **{rows_local}** videos are already in `course-materials/<slug>/videos/`.
- Pull **all {r2_total}** from R2 into one organized folder (per course) by running:
  ```
  python download_all_videos_from_r2.py
  ```
  This writes to `C:\\Temp\\spreadcom-marketing\\youtube\\videos\\<course_slug>\\`.
- The {total - r2_total} not-yet-rendered lessons (Phase-2 in progress) can be rendered later with
  `COURSE_SLUG=<slug> python batch_render.py` and uploaded then.

## 3. Bulk-upload, one course at a time
1. **YouTube Studio → Create → Upload videos** → drag a course folder's MP4s (queue as many as you like; ~15 process at once).
2. Open `youtube_upload_metadata.csv` (UTF-8, opens in Excel/Google Sheets). It's sorted by **course → module → lesson**.
3. For each video, copy **youtube_title**, **description**, and **tags** from the matching row (match on `video_filename`).
4. Set **Visibility = Public** (or **Schedule** to drip 1–2/day for steady algorithm signals).
5. Audience: **"No, it's not made for kids."** Category: **Education**.

## 4. Build the playlists
1. Create one **Public** playlist per course — titles + descriptions in `playlists.md`.
2. Add each course's videos **in CSV row order** (module→lesson) so lessons play in sequence.
3. Tip: you can add a video to its playlist right from the upload dialog.

## 5. Polish & SEO
- Channel homepage: add a **Featured section per playlist** (all 12 tracks visible).
- Each description already leads with the lesson summary + `{SITE}` + the free CTA — keep the link in the **first 2 lines** (above the fold).
- Add **end screens** (last 20s) → "next lesson" + a link to {SITE}.
- Consider custom thumbnails later; the rendered title slide already reads well as a fallback.

## Files in this kit
- `youtube_upload_metadata.csv` — per-video title/description/tags/visibility (+ local path & R2 url)
- `playlists.md` — 12 playlist titles + descriptions
- `channel_about.md` — channel name, description, keywords, art
- `download_all_videos_from_r2.py` — pulls all videos to per-course folders
- `spreadcom-learning-banner.png` / `spreadcom-learning-avatar.png` — channel art
"""
open(os.path.join(OUT, "upload_runbook.md"), "w", encoding="utf-8").write(runbook)

# ---------- downloader ----------
dl = r'''# Download every course video from R2 into per-course folders for YouTube upload.
import os, csv, urllib.request
OUT = r"C:\Temp\spreadcom-marketing\youtube"
VID = os.path.join(OUT, "videos")
rows = list(csv.DictReader(open(os.path.join(OUT, "youtube_upload_metadata.csv"), encoding="utf-8-sig")))
todo = [r for r in rows if r["on_r2"] == "yes"]
print(f"{len(todo)} videos to fetch from R2")
ok = skip = fail = 0
for i, r in enumerate(todo, 1):
    d = os.path.join(VID, r["course_slug"]); os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, r["video_filename"])
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        skip += 1; continue
    try:
        urllib.request.urlretrieve(r["r2_url"], dst)
        ok += 1
        if ok % 25 == 0: print(f"  {i}/{len(todo)} ... {r['video_filename']}")
    except Exception as e:
        fail += 1; print("  FAIL", r["video_filename"], e)
print(f"done. downloaded={ok} skipped={skip} failed={fail} -> {VID}")
'''
open(os.path.join(OUT, "download_all_videos_from_r2.py"), "w", encoding="utf-8").write(dl)

print("Wrote: playlists.md, channel_about.md, upload_runbook.md, download_all_videos_from_r2.py")
print("Folder:", OUT)
