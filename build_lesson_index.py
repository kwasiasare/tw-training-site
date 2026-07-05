#!/usr/bin/env python3
"""Build api/src/shared/lessons.generated.json — lesson text + quiz for the AI
tutor and AI answer-grading (TW-67, TW-68).

The managed Functions deployment only ships the `api/` folder, so the tutor and
grader backends cannot read `course-materials/` at runtime. This script bundles each
lesson's grounding text (title, course, objectives, body) and its quiz (so the grader
has the authoritative reference answers) into a committed JSON the Functions require,
keyed by lesson id (the markdown filename stem, which is also the topic id / video slug).

Mirrors build_catalog.py: regenerate + commit whenever lesson content changes.

Usage: python build_lesson_index.py
"""

import glob
import json
import os
import re

import yaml

OUT = os.path.join("api", "src", "shared", "lessons.generated.json")
BODY_CHAR_CAP = 8000  # bound grounding tokens; lessons are well under this

# dami-ai-career is unpublished (superseded by ai-app-developer-2026); its
# content stays in the repo but is excluded from the build. Must mirror the
# `!dami-ai-career/lessons/**` exclusion in site/src/content.config.ts — if the
# two drift, the tutor/chatbot's lesson index (this script's output) can cite
# lessons that don't correspond to any real page on the live site (TW-117).
UNPUBLISHED_COURSES = {"dami-ai-career"}


def parse_lesson(path):
    """Return (lesson_id, data) or None if unparseable."""
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if not m:
        return None
    try:
        front = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(front, dict) or not front.get("title"):
        return None

    # Keep only the quiz fields the grader/tutor need; normalise shape.
    quiz = []
    for item in front.get("quiz") or []:
        if not isinstance(item, dict):
            continue
        quiz.append({
            "q": item.get("q", ""),
            "options": item.get("options") or None,
            "answer": item.get("answer"),
            "why": item.get("why", ""),
        })

    lesson_id = os.path.splitext(os.path.basename(path))[0]
    return lesson_id, {
        "course": front.get("course", ""),
        "title": front.get("title", ""),
        "objectives": front.get("objectives") or [],
        "body": m.group(2).strip()[:BODY_CHAR_CAP],
        "quiz": quiz,
    }


def main():
    index = {}
    for md in sorted(glob.glob(os.path.join("course-materials", "*", "lessons", "*.md"))):
        course_slug = os.path.basename(os.path.dirname(os.path.dirname(md)))
        if course_slug in UNPUBLISHED_COURSES:
            continue
        parsed = parse_lesson(md)
        if not parsed:
            continue
        lesson_id, data = parsed
        index[lesson_id] = data

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"Wrote {len(index)} lesson(s) to {OUT}")


if __name__ == "__main__":
    main()
