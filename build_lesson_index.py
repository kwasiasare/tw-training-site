#!/usr/bin/env python3
"""Build api/src/shared/lessons.generated.json — lesson text for the AI tutor (TW-67).

The managed Functions deployment only ships the `api/` folder, so the tutor backend
cannot read `course-materials/` at runtime. This script bundles each lesson's grounding
text (title, course, objectives, body) into a committed JSON the tutor Function requires,
keyed by lesson id (the markdown filename stem, which is also the topic id / video slug).

Mirrors build_catalog.py: regenerate + commit whenever lesson content changes.

Usage: python build_lesson_index.py
"""

import glob
import json
import os
import re

OUT = os.path.join("api", "src", "shared", "lessons.generated.json")
BODY_CHAR_CAP = 8000  # bound grounding tokens; lessons are well under this


def parse_lesson(path):
    """Return (lesson_id, {course, title, objectives, body}) or None if unparseable."""
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if not m:
        return None
    front, body = m.group(1), m.group(2).strip()

    def scalar(key):
        mm = re.search(rf"^{key}:\s*(.+)$", front, re.MULTILINE)
        return mm.group(1).strip().strip("'\"") if mm else ""

    # Objectives: a YAML list of "- ..." lines under `objectives:` up to the next key.
    objectives = []
    om = re.search(r"^objectives:\s*\n((?:\s*-\s.*\n?)+)", front, re.MULTILINE)
    if om:
        objectives = [re.sub(r"^\s*-\s+", "", ln).strip()
                      for ln in om.group(1).splitlines() if ln.strip().startswith("-")]

    lesson_id = os.path.splitext(os.path.basename(path))[0]
    return lesson_id, {
        "course": scalar("course"),
        "title": scalar("title"),
        "objectives": objectives,
        "body": body[:BODY_CHAR_CAP],
    }


def main():
    index = {}
    for md in sorted(glob.glob(os.path.join("course-materials", "*", "lessons", "*.md"))):
        parsed = parse_lesson(md)
        if not parsed:
            continue
        lesson_id, data = parsed
        if not data["title"]:
            continue
        index[lesson_id] = data

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"Wrote {len(index)} lesson(s) to {OUT}")


if __name__ == "__main__":
    main()
