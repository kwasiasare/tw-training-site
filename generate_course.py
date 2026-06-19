#!/usr/bin/env python3
"""AI course generator (TW-65) — author a bespoke course from a target profile.

Given a target role + skills (from the Custom Advisor's analysis), Claude authors:
  1. a curriculum outline (course.json + module/lesson titles), then
  2. one full DECK JSON per lesson (body_markdown + slides+narration + quiz).

Output lands in course-materials/<slug>/ in the EXACT format the existing pipeline
consumes, so the rest is unchanged:
    python convert_decks_to_md.py <slug>          # decks -> lesson markdown
    COURSE_SLUG=<slug> python batch_render.py      # decks -> narrated videos
    COURSE_SLUG=<slug> python upload_videos_r2.py  # videos -> R2
…then add a COURSES entry in site/src/consts.ts (the generation Action does this).

This script only AUTHORS content (Claude calls); it does not render or upload — that
keeps it fast + testable, and lets the Action orchestrate the heavy steps.

Usage:
  python generate_course.py --slug ai-app-dev-custom --prefix cx1 \
      --role "AI Application Developer" \
      --skills "python,rag,agents,apis,deployment" \
      --modules 4 --lessons-per-module 4

  # or drive it from a request JSON ({slug,prefix,role,skills,modules,lessonsPerModule}):
  python generate_course.py --request request.json

Requires: pip install anthropic ; ANTHROPIC_API_KEY in env or .env.
Model: claude-opus-4-8.
"""

import argparse
import json
import os
import re
import sys

MODEL = "claude-opus-4-8"


def load_env(path=".env"):
    env = dict(os.environ)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env.setdefault(k.strip(), v.strip())
    return env


def client():
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic is required: pip install anthropic")
    key = load_env().get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY is not set")
    return anthropic.Anthropic(api_key=key)


def _call(cli, system, user_text, schema, max_tokens=16000):
    """One structured-output Claude call. Streams to avoid the non-stream timeout
    guard on large max_tokens; returns the parsed JSON object."""
    with cli.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        system=system,
        output_config={"format": {"type": "json_schema", "schema": schema}},
        messages=[{"role": "user", "content": user_text}],
    ) as stream:
        msg = stream.get_final_message()
    if msg.stop_reason == "refusal":
        sys.exit("Claude declined to generate this course (refusal).")
    text = next((b.text for b in msg.content if b.type == "text"), None)
    if not text:
        sys.exit("No content returned from the model.")
    return json.loads(text)


# ── Schemas ────────────────────────────────────────────────────────────────
OUTLINE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "audience": {"type": "string"},
        "moduleTitles": {"type": "array", "items": {"type": "string"}},
        "lessons": {
            "type": "array",
            "items": {
                "type": "object", "additionalProperties": False,
                "properties": {
                    "module": {"type": "integer"},
                    "lessonInModule": {"type": "integer"},
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                },
                "required": ["module", "lessonInModule", "title", "summary"],
            },
        },
    },
    "required": ["title", "description", "audience", "moduleTitles", "lessons"],
}

_SLIDE = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "type": {"type": "string", "enum": ["title", "content"]},
        "title": {"type": "string"},
        "sub": {"type": "string"},
        "bullets": {"type": "array", "items": {"type": "string"}},
        "code": {"type": "string"},
        "narration": {"type": "string"},
    },
    "required": ["type", "title", "narration"],
}
_QUIZ = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "q": {"type": "string"},
        "options": {"type": "array", "items": {"type": "string"}},
        "answer": {"type": ["integer", "string"]},
        "why": {"type": "string"},
    },
    "required": ["q", "answer", "why"],
}
LESSON_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "summary": {"type": "string"},
        "objectives": {"type": "array", "items": {"type": "string"}},
        "body_markdown": {"type": "string"},
        "slides": {"type": "array", "items": _SLIDE},
        "quiz": {"type": "array", "items": _QUIZ},
        "resources": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"label": {"type": "string"}, "url": {"type": "string"}},
            "required": ["label"],
        }},
    },
    "required": ["summary", "objectives", "body_markdown", "slides", "quiz", "resources"],
}

OUTLINE_SYS = (
    "You are a senior curriculum designer for a project-based tech training platform. "
    "Design a focused, realistic, job-oriented course that takes a learner to a target role. "
    "Prefer practical, portfolio-building lessons over theory. Output ONLY the requested JSON."
)
LESSON_SYS = (
    "You are an expert instructor writing one self-contained video lesson. Produce clear lesson "
    "notes (body_markdown: GitHub-flavoured markdown, ## headings, no YAML), a slide deck with "
    "spoken narration for each slide (first slide type 'title'; the rest 'content' with 3-5 short "
    "bullets and optional code), and a short quiz (mix of multiple-choice with a 0-based integer "
    "answer into options, and one or two short-answer with a string answer). Output ONLY JSON."
)


def gen_outline(cli, role, skills, modules, per_module):
    user = (
        f"Design a course that gets a learner job-ready as: {role}.\n"
        f"Skills to cover (from a résumé gap analysis): {', '.join(skills)}.\n"
        f"Structure: exactly {modules} modules, {per_module} lessons each "
        f"({modules * per_module} lessons total). moduleTitles must have {modules} entries. "
        f"Each lesson: module (1..{modules}), lessonInModule (1..{per_module}), a concrete title, "
        f"and a one-sentence summary. Order from fundamentals to capstone."
    )
    return _call(cli, OUTLINE_SYS, user, OUTLINE_SCHEMA, max_tokens=8000)


def gen_lesson(cli, role, course_title, module_title, lesson):
    user = (
        f"Course: {course_title} (target role: {role}).\n"
        f"Module: {module_title}.\n"
        f"Lesson title: {lesson['title']}\n"
        f"Lesson summary: {lesson['summary']}\n\n"
        "Write the full lesson: objectives (4-6), body_markdown (the teaching notes), a slide deck "
        "with narration (6-10 slides), a quiz (4-6 questions), and 2-4 resources. Keep it practical."
    )
    return _call(cli, LESSON_SYS, user, LESSON_SCHEMA, max_tokens=16000)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48] or "lesson"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", help="path to a request JSON")
    ap.add_argument("--slug")
    ap.add_argument("--prefix", default="cx")
    ap.add_argument("--role")
    ap.add_argument("--skills", default="")
    ap.add_argument("--modules", type=int, default=4)
    ap.add_argument("--lessons-per-module", type=int, default=4)
    args = ap.parse_args()

    req = {}
    if args.request:
        with open(args.request, encoding="utf-8") as fh:
            req = json.load(fh)
    slug = args.slug or req.get("slug")
    prefix = args.prefix or req.get("prefix", "cx")
    role = args.role or req.get("role")
    skills = (args.skills and args.skills.split(",")) or req.get("skills", [])
    modules = args.modules if args.request is None else req.get("modules", args.modules)
    per_module = req.get("lessonsPerModule", args.lessons_per_module) if req else args.lessons_per_module
    skills = [s.strip() for s in skills if s and s.strip()]
    if not slug or not role:
        sys.exit("Need --slug and --role (or a --request JSON with them).")

    course_dir = os.path.join("course-materials", slug)
    decks_dir = os.path.join(course_dir, "decks")
    for sub in ("decks", "lessons", "videos", "study-packs"):
        os.makedirs(os.path.join(course_dir, sub), exist_ok=True)

    cli = client()

    print(f"Authoring outline for '{role}' → {slug} ({modules}×{per_module})…")
    outline = gen_outline(cli, role, skills, modules, per_module)
    module_titles = outline["moduleTitles"]

    decks = []
    for i, lesson in enumerate(outline["lessons"], start=1):
        m = lesson["module"]
        lim = lesson["lessonInModule"]
        lesson_slug = f"{prefix}-m{m}-l{lim:02d}-{slugify(lesson['title'])}"
        mtitle = module_titles[m - 1] if 1 <= m <= len(module_titles) else f"Module {m}"
        print(f"  [{i}/{len(outline['lessons'])}] {lesson_slug}")
        content = gen_lesson(cli, role, outline["title"], mtitle, lesson)
        deck = {
            "slug": lesson_slug,
            "title": lesson["title"],
            "month": m,
            "monthTitle": mtitle,
            "lesson": lim,
            "video": f"{lesson_slug}.mp4",
            "summary": content["summary"],
            "objectives": content["objectives"],
            "quiz": content["quiz"],
            "resources": content["resources"],
            "body_markdown": content["body_markdown"],
            "slides": content["slides"],
        }
        with open(os.path.join(decks_dir, f"{lesson_slug}.json"), "w", encoding="utf-8") as fh:
            json.dump(deck, fh, ensure_ascii=False, indent=2)
        decks.append(deck)

    course_json = {
        "slug": slug,
        "title": outline["title"],
        "description": outline["description"],
        "audience": outline["audience"],
        "modules": modules,
        "lessons": len(decks),
        "layout": {"decks": "decks", "lessons": "lessons", "videos": "videos", "studyPacks": "study-packs"},
        "moduleTitles": {str(i + 1): t for i, t in enumerate(module_titles)},
        "generated": True,
        "targetRole": role,
        "targetSkills": skills,
    }
    with open(os.path.join(course_dir, "course.json"), "w", encoding="utf-8") as fh:
        json.dump(course_json, fh, ensure_ascii=False, indent=2)

    print(
        f"\nWrote {len(decks)} decks + course.json to {course_dir}.\nNext:\n"
        f"  python convert_decks_to_md.py {slug}\n"
        f"  COURSE_SLUG={slug} python batch_render.py\n"
        f"  COURSE_SLUG={slug} python upload_videos_r2.py\n"
        f"  (then add a COURSES entry for '{slug}' in site/src/consts.ts)"
    )


if __name__ == "__main__":
    main()
