# Build a YouTube upload kit for all courses: metadata CSV + playlists + channel About + runbook.
import os, re, csv, glob, json
import yaml

ROOT = r"C:\Users\KwasiAsare\OneDrive - Spreadcom Ltd\Desktop\claude-01\Training-website"
OUT = r"C:\Temp\spreadcom-marketing\youtube"
os.makedirs(OUT, exist_ok=True)
SITE = "https://www.salloma.com"

# R2 source base + bucket listing (so we know what's actually uploaded)
def load_env():
    env = {}
    p = os.path.join(ROOT, ".env")
    with open(p, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"')
    return env
ENV = load_env()
R2_BASE = ENV.get("R2_PUBLIC_BASE", "https://pub-178640b0d3e549d097dc751f9d1b9867.r2.dev").rstrip("/")
r2_keys = set()
try:
    import boto3
    s3 = boto3.client("s3", endpoint_url=f"https://{ENV['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
                      aws_access_key_id=ENV["R2_ACCESS_KEY_ID"], aws_secret_access_key=ENV["R2_SECRET_ACCESS_KEY"])
    tok = None
    while True:
        kw = {"Bucket": ENV["R2_BUCKET"], "MaxKeys": 1000}
        if tok: kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []): r2_keys.add(o["Key"])
        if r.get("IsTruncated"): tok = r["NextContinuationToken"]
        else: break
    print(f"R2 bucket '{ENV['R2_BUCKET']}': {len(r2_keys)} objects")
except Exception as e:
    print("R2 listing skipped:", e)

SHORT = {
    "cloud-security-engineer": "Cloud Security Engineer",
    "dami-ai-career": "AI Application Developer",
    "kwasi-GenAI": "Applied GenAI Engineer",
    "helpdesk-tier1-2": "IT Helpdesk Tier 1-2",
    "helpdesk-tier3-advanced": "IT Helpdesk Tier 3 (Advanced)",
    "data-scientist": "Data Scientist",
    "ml-engineer": "Machine Learning Engineer",
    "mlops-engineer": "MLOps Engineer",
    "ai-app-developer-2026": "AI App Developer",
    "agentic-ai-engineer": "Agentic AI Engineer",
    "ai-product-manager": "AI Product Manager",
    "junior-digital-marketing": "Junior Digital Marketing",
}

def frontmatter(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    if not m: return None, ""
    try: fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError: return None, ""
    return fm, m.group(2)

def trim_lead(text, n=380):
    text = " ".join(text.split())
    if len(text) <= n: return text
    cut = text[:n]
    dot = cut.rfind(". ")
    return (cut[:dot+1] if dot > 120 else cut.rstrip() + "…")

rows = []
playlists = []
courses = sorted(c for c in glob.glob(os.path.join(ROOT, "course-materials", "*", "course.json")))
for cj_path in courses:
    cdir = os.path.dirname(cj_path)
    slug = os.path.basename(cdir)
    cj = json.load(open(cj_path, encoding="utf-8"))
    short = SHORT.get(slug, slug.replace("-", " ").title())
    ctitle = cj.get("title", short)
    cdesc = cj.get("description", "")
    skills = cj.get("targetSkills", []) or []
    playlist_title = f"{short} — Full Course (Free)"
    playlists.append((slug, playlist_title, ctitle, cdesc))

    lessons = []
    for md in glob.glob(os.path.join(cdir, "lessons", "*.md")):
        fm, body = frontmatter(md)
        if not fm or not fm.get("video"): continue
        lessons.append((fm.get("month", 0), fm.get("lesson", 0), fm, body))
    lessons.sort(key=lambda x: (x[0], x[1]))

    for month, lnum, fm, body in lessons:
        vfile = fm["video"]
        title = fm.get("title", "")
        yt_title = f"{title} | {short} (M{month}·L{lnum})"
        if len(yt_title) > 100:
            yt_title = f"{title[:100-len(short)-14]}… | {short}"
        # objectives bullets
        objs = fm.get("objectives") or []
        obj_block = "\n".join("• " + o for o in objs[:4])
        lead = trim_lead(fm.get("summary", "") or title)
        desc = (
            f"{lead}\n\n"
            f"🎓 Part of the FREE \"{short}\" course on Spreadcom Learning.\n"
            f"▶ Full course, hands-on labs, quizzes & an AI tutor: {SITE}\n"
            f"✅ 100% free — just register after your first 2 lessons.\n\n"
            f"In this lesson you'll learn to:\n{obj_block}\n\n"
            f"📚 Playlist: {playlist_title}\n"
            f"🌐 {SITE}\n\n"
            f"#SpreadcomLearning #{slug.replace('-', '').replace('_','')} #FreeCourse #OnlineLearning"
        )
        tags = skills[:14] + [short, "Spreadcom Learning", "free course", "online course", "tutorial", "2026"]
        # keep tags under ~480 chars total
        out_tags, total = [], 0
        for t in tags:
            if total + len(t) + 1 > 480: break
            out_tags.append(t); total += len(t) + 1
        local = os.path.join(cdir, "videos", vfile)
        rows.append({
            "course": short, "course_slug": slug, "module": month, "lesson": lnum,
            "playlist": playlist_title, "video_filename": vfile,
            "local_path": local if os.path.exists(local) else "",
            "local_exists": "yes" if os.path.exists(local) else "no",
            "on_r2": "yes" if vfile in r2_keys else "no",
            "r2_url": f"{R2_BASE}/{vfile}",
            "youtube_title": yt_title, "visibility": "Public", "tags": ", ".join(out_tags),
            "description": desc,
        })

# ---- write CSV ----
csv_path = os.path.join(OUT, "youtube_upload_metadata.csv")
cols = ["course","course_slug","module","lesson","playlist","video_filename","local_path",
        "local_exists","on_r2","r2_url","youtube_title","visibility","tags","description"]
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)

# ---- coverage summary ----
from collections import Counter
by_course = Counter(r["course_slug"] for r in rows)
local_cnt = Counter(r["course_slug"] for r in rows if r["local_exists"] == "yes")
r2_cnt = Counter(r["course_slug"] for r in rows if r["on_r2"] == "yes")
print(f"\nTotal videos in sheet: {len(rows)}")
print(f"  with local file: {sum(local_cnt.values())}   on R2: {sum(r2_cnt.values())}")
print(f"Playlists (courses): {len(playlists)}")
print("CSV:", csv_path)

# expose for the next cells
import json as _j
open(os.path.join(OUT, "_coverage.json"), "w").write(_j.dumps({
    "total": len(rows), "by_course": dict(by_course), "local": dict(local_cnt), "r2": dict(r2_cnt),
    "playlists": [{"slug": s, "title": t, "course_title": ct, "desc": d} for s,t,ct,d in playlists]
}))
