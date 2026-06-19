#!/usr/bin/env python3
"""Build api/src/shared/catalog.generated.json from published generated courses (TW-66).

Scans course-materials/*/course.json for AI-generated courses (generated: true) and
writes their target-profiles so the Custom Advisor's matcher can REUSE them for future
résumés — the library compounds. Run by the generate-course Action after authoring;
the resulting file is committed in the draft PR, so on merge the API can reuse it.

Usage: python build_catalog.py
"""

import glob
import json
import os

OUT = os.path.join("api", "src", "shared", "catalog.generated.json")


def main():
    items = []
    for course_json in sorted(glob.glob(os.path.join("course-materials", "*", "course.json"))):
        try:
            c = json.load(open(course_json, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not c.get("generated"):
            continue
        role = c.get("targetRole")
        if not role:
            continue
        items.append({
            "slug": c["slug"],
            "title": c.get("title", c["slug"]),
            "summary": (c.get("description") or "")[:300],
            "targetProfile": {
                "role": role,
                "level": c.get("level", "mid"),
                "skills": c.get("targetSkills") or [],
            },
        })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(items, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"Wrote {len(items)} generated course profile(s) to {OUT}")


if __name__ == "__main__":
    main()
