# Download every course video from R2 into per-course folders for YouTube upload.
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
