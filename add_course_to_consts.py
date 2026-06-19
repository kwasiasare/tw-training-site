#!/usr/bin/env python3
"""Insert a generated course into the site catalog (site/src/consts.ts COURSES).

Adding lessons under course-materials/<slug>/ is auto-discovered by Astro, but a
course only appears in the homepage/nav catalog when it has a COURSES entry. This
adds one from course.json (idempotent — skips if the slug is already present).

Usage: python add_course_to_consts.py <slug>
"""

import glob
import json
import os
import re
import sys

CONSTS = os.path.join("site", "src", "consts.ts")


def esc(s):
    return str(s).replace("\\", "\\\\").replace("'", "\\'")


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: add_course_to_consts.py <slug>")
    slug = sys.argv[1]
    course_dir = os.path.join("course-materials", slug)
    course = json.load(open(os.path.join(course_dir, "course.json"), encoding="utf-8"))

    decks = sorted(glob.glob(os.path.join(course_dir, "decks", "*.json")))
    sample = os.path.splitext(os.path.basename(decks[0]))[0] if decks else slug

    src = open(CONSTS, encoding="utf-8").read()
    if re.search(r"slug:\s*'" + re.escape(slug) + r"'", src):
        print(f"'{slug}' already in COURSES — nothing to do.")
        return

    tagline = course.get("audience") or course["description"][:120]
    entry = (
        "  {\n"
        f"    slug: '{esc(slug)}',\n"
        f"    title: '{esc(course['title'])}',\n"
        f"    tagline: '{esc(tagline)}',\n"
        f"    blurb: '{esc(course['description'])}',\n"
        f"    sample: '{esc(sample)}',\n"
        "    accent: '#7c3aed',\n"
        "  },"
    )

    m = re.search(r"export const COURSES: Course\[\] = \[(.*?)\n\];", src, re.S)
    if not m:
        sys.exit("Could not find the COURSES array in consts.ts")
    insert_at = m.start(0) + m.group(0).rindex("\n];")
    new = src[:insert_at] + "\n" + entry + src[insert_at:]
    with open(CONSTS, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(new)
    print(f"Added '{slug}' to COURSES (sample lesson: {sample}).")


if __name__ == "__main__":
    main()
