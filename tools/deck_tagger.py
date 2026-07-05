#!/usr/bin/env python3
"""
deck_tagger.py - TW-115: batch-tag lesson decks and pre-filter currency drift
using ONLY the local LLM gateway's fast tier (/v1/classify, qwen2.5:3b).

Purpose
-------
Two things, in a single fast-tier call per lesson:

  Task A - skill/cert taxonomy tagging: extract short tags describing what a
           lesson teaches, aligned to a track's course.json "targetSkills"
           vocabulary when present (falls back to free-text tags otherwise).
           Feeds catalog metadata alongside build_catalog.py's course-level
           targetSkills (see build_catalog.py) - this is lesson-level detail.

  Task B - currency-drift pre-filter: flag mentions of pinned model names
           (gpt-4o, gpt-3.5, ...), retired cert exam codes, and "Chat
           Completions API" phrasing that may now be superseded by a
           "Responses API"-style approach. This is a pattern-detection
           pre-filter only - it narrows what the expensive professor /
           industry / certification review lenses need to look at first. It
           is NOT a replacement for those review passes.

Unit of work: course-materials/<slug>/lessons/*.md (NOT decks/*.json). This
matches TW-110's ingestion unit (391 files across 12 tracks = the ticket's
"~391 lesson decks") - see HOWTO_LLM_Ingestion.md's note on why lessons/*.md
is the clean per-lesson content unit (chunks cleanly, one file per lesson),
whereas decks/*.json is slide-deck presentation data, a different artifact.

Fast tier only: this script imports classify() from tools/local_llm_client.py
and calls nothing else from that module. classify() always hits
POST /v1/classify, which the gateway pins to the fast tier server-side
regardless of caller input - generate()/tier="standard" are never used here.

Usage
-----
    python tools/deck_tagger.py --track junior-digital-marketing
    python tools/deck_tagger.py --track ml-engineer --track data-scientist
    python tools/deck_tagger.py --all
    python tools/deck_tagger.py --track junior-digital-marketing --limit 3   # smoke test
    python tools/deck_tagger.py --all --key-file tools/training_website.key

Output: tools/reports/deck-tagging-report-<track-or-all>.md (checklist, for
humans / the next expert-review pass) and the same-named .json (full
structured data, for tooling). Progress is printed per lesson as it runs.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

# tools/local_llm_client.py lives alongside this script; add this script's own
# directory to sys.path so `import local_llm_client` works regardless of the
# caller's cwd (repo root, tools/, or elsewhere).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from local_llm_client import (  # noqa: E402
    classify,
    LocalLLMClientError,
    DEFAULT_BASE_URL,
)

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

DEFAULT_COURSE_MATERIALS_DIR = "course-materials"
DEFAULT_KEY_FILE = "tools/training_website.key"
DEFAULT_OUT_DIR = "tools/reports"

# Same cap build_lesson_index.py uses for lesson body text (see
# HOWTO_LLM_Ingestion.md) - keeps fast-tier calls quick and within the 3B
# model's comfortable context, while still covering frontmatter (title,
# summary, objectives) plus most of the lesson prose/code.
MAX_LESSON_CHARS = 8000

# The gateway box is shared with standard-tier/embedding workloads; a fast-tier
# classify() call can occasionally time out under contention even though it's
# cheap on its own. Matches ingest_docs.py's retry-once-after-a-pause pattern
# (see send_batch_with_retry) rather than failing a lesson on one transient
# timeout.
RETRY_PAUSE_SECS = 15

# How many independent classify() samples to take for the currency-flags task
# (fast tier only - still cheap). Real testing found the 3B fast-tier model
# has genuine run-to-run recall variance on this task: the identical
# instruction against the identical lesson text sometimes returned zero
# flags and sometimes correctly found real, grounded ones (verified against
# a lesson known via grep to contain a verbatim "gpt-4o-mini" mention).
# Sampling twice and taking the union (de-duplicated by pattern text)
# meaningfully improves recall for a pre-filter where missing a real flag is
# worse than one harmless duplicate - this does not change the tags task,
# which did not show the same instability in testing.
FLAGS_SAMPLES = 2

# --------------------------------------------------------------------------
# NOTE on two calls instead of one combined call
# --------------------------------------------------------------------------
# TW-115 explicitly allows either "call classify() twice ... or once with a
# combined instruction, your call - simplicity favors one call per lesson if
# you can express both tasks in one instruction+schema." A combined
# tags+currency-flags instruction was tried first and DID NOT hold up under
# real testing: against a lesson verified (via grep) to contain a verbatim
# "gpt-4o-mini" model string and repeated "Chat Completions API" phrasing,
# the fast-tier 3B model reliably returned correct tags but silently
# defaulted "currency_flags" to an empty list - i.e. it satisfied the first
# half of the schema and dropped the second under the combined instruction's
# complexity. Isolating the currency-flag task into its own single-purpose
# instruction (same lesson text, same model) correctly found both mentions
# with genuine grounded snippets. Since a checklist that silently misses real
# flags defeats the ticket's purpose, this script makes TWO classify() calls
# per lesson (fast tier only, same as one call) rather than one combined call.

TAGS_INSTRUCTION_TEMPLATE = """You are analyzing ONE lesson from a technical training course. \
Read the lesson text and respond with ONLY a single JSON object - no markdown \
code fences, no commentary before or after - matching exactly this schema:

{{"tags": [<2-6 short skill/certification taxonomy keywords for this lesson>]}}

Tag vocabulary guidance: {vocab_hint}

Only include tags that are actually grounded in the lesson text below - do not \
invent content."""

FLAGS_INSTRUCTION = """You are scanning ONE lesson from a technical training course for \
currency-drift patterns - this is a pre-filter to help human reviewers decide what \
to double check, not a judgment call on your part. Find every mention in the text \
below of:
- A pinned/legacy AI model name, e.g. "gpt-4o", "gpt-4o-mini", "gpt-3.5", \
"gpt-3.5-turbo", "claude-2", "claude-instant", or any other specific dated model \
version string
- A retired or old certification exam code
- The phrase "Chat Completions API" / "chat completions API" (a newer \
"Responses API"-style approach might now be more current)
- Any other explicit mention of a specific vendor API/product version that could \
have since changed

Respond with ONLY a single JSON object - no markdown code fences, no commentary \
before or after - matching exactly this schema:

{"currency_flags": [{"pattern": "<exact term/name found>", "snippet": "<verbatim excerpt containing it, under 160 chars>", "reason": "<why this may be worth an expert-review look>"}]}

List one entry per distinct mention found. If none of these patterns appear in the \
text, return an empty list for "currency_flags". Only report flags that are \
actually grounded in the lesson text below - do not invent content."""


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# --------------------------------------------------------------------------
# Course-materials discovery
# --------------------------------------------------------------------------

def discover_tracks(course_materials_dir):
    """Return sorted track slugs = subdirectories of course_materials_dir that
    contain a lessons/ subdirectory."""
    tracks = []
    try:
        entries = sorted(os.listdir(course_materials_dir))
    except OSError as e:
        raise SystemExit(f"Error: cannot list --course-materials-dir '{course_materials_dir}': {e}")
    for entry in entries:
        track_dir = os.path.join(course_materials_dir, entry)
        if os.path.isdir(os.path.join(track_dir, "lessons")):
            tracks.append(entry)
    return tracks


def load_target_skills(course_materials_dir, track):
    """Read course-materials/<track>/course.json and return its targetSkills
    list if present, else None. Missing/unreadable/malformed course.json is
    not fatal - just means no vocabulary hint for this track."""
    course_json_path = os.path.join(course_materials_dir, track, "course.json")
    try:
        with open(course_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    skills = data.get("targetSkills")
    if isinstance(skills, list) and skills:
        return [str(s) for s in skills]
    return None


def iter_lesson_files(course_materials_dir, track):
    """Yield sorted relative-to-track lesson .md filenames for one track."""
    lessons_dir = os.path.join(course_materials_dir, track, "lessons")
    try:
        names = sorted(f for f in os.listdir(lessons_dir) if f.lower().endswith(".md"))
    except OSError as e:
        eprint(f"Error: cannot list lessons/ for track '{track}': {e}")
        return []
    return names


# --------------------------------------------------------------------------
# JSON extraction from the fast-tier model's raw text output
# --------------------------------------------------------------------------

def extract_json_object(raw):
    """Best-effort extraction of a JSON object from a small 3B fast-tier
    model's text output, which may wrap the JSON in markdown code fences or
    add stray commentary. Returns the parsed dict, or raises ValueError with
    a short reason if nothing parseable is found.

    Tried in order: (1) the whole string as-is, (2) strip ```...``` fences,
    (3) the substring between the first '{' and the last '}'.
    """
    candidates = [raw.strip()]

    stripped = raw.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        candidates.append("\n".join(lines).strip())

    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(raw[start:end + 1])

    last_err = None
    for candidate in candidates:
        if not candidate:
            continue
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError as e:
            last_err = e
            continue
        if isinstance(parsed, dict):
            return parsed
        last_err = ValueError(f"parsed JSON was {type(parsed).__name__}, not an object")

    raise ValueError(f"no parseable JSON object found ({last_err})")


def normalize_result(parsed):
    """Coerce a parsed dict into {"tags": [str, ...], "currency_flags": [{...}, ...]},
    tolerating missing/wrong-typed fields from the small model rather than
    raising - only a totally unparseable response counts as a hard failure."""
    tags = parsed.get("tags")
    if not isinstance(tags, list):
        tags = []
    tags = [str(t).strip() for t in tags if str(t).strip()]

    raw_flags = parsed.get("currency_flags")
    if not isinstance(raw_flags, list):
        raw_flags = []
    flags = []
    for item in raw_flags:
        if not isinstance(item, dict):
            continue
        pattern = str(item.get("pattern", "")).strip()
        if not pattern:
            continue
        flags.append({
            "pattern": pattern,
            "snippet": str(item.get("snippet", "")).strip()[:300],
            "reason": str(item.get("reason", "")).strip(),
        })
    return tags, flags


# --------------------------------------------------------------------------
# Per-lesson processing
# --------------------------------------------------------------------------

def build_tags_instruction(target_skills):
    if target_skills:
        vocab_hint = (
            "Prefer these known skill tags where relevant to this lesson: "
            + ", ".join(target_skills)
            + ". You may add additional concise free-text tags if the lesson "
            "covers something not in this list."
        )
    else:
        vocab_hint = (
            "No fixed vocabulary is available for this course - use concise "
            "free-text skill/topic tags."
        )
    return TAGS_INSTRUCTION_TEMPLATE.format(vocab_hint=vocab_hint)


def call_classify_with_retry(text, instruction, key_file, base_url):
    """Call classify() once (fast tier only), retrying once after a pause on
    a transient LocalLLMClientError (see RETRY_PAUSE_SECS - the shared
    gateway box can have contention from concurrent standard-tier/embedding
    workloads even though this call itself is fast-tier only).

    Returns (raw_result_str, None) on success, or (None, error_message) if
    both attempts failed or the response shape was unexpected. Never raises.
    """
    try:
        data = classify(text, instruction, key_file=key_file, base_url=base_url)
    except LocalLLMClientError as e:
        time.sleep(RETRY_PAUSE_SECS)
        try:
            data = classify(text, instruction, key_file=key_file, base_url=base_url)
        except LocalLLMClientError as e2:
            return None, f"classify() call failed after 1 retry: {e2}"

    raw_result = data.get("result")
    if not isinstance(raw_result, str):
        return None, f"unexpected /v1/classify response shape: result was {type(raw_result).__name__}"
    return raw_result, None


def process_lesson(course_materials_dir, track, filename, tags_instruction, key_file, base_url):
    """Read one lesson file and make TWO focused classify() calls (fast tier
    only) - one for tags, one for currency-drift flags (see the module-level
    NOTE above explaining why this replaced a single combined call). Never
    raises - all failure modes are captured in the returned dict, either as
    a per-task "warnings" entry (lesson still reported with partial data) or,
    if BOTH tasks failed outright, as the dict's "error" field so the caller
    treats the whole lesson as a hard failure and continues the batch."""
    path = os.path.join(course_materials_dir, track, "lessons", filename)
    relpath = f"{track}/lessons/{filename}"

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        return {"lesson": relpath, "error": f"could not read file: {e}"}

    truncated = len(text) > MAX_LESSON_CHARS
    text_for_model = text[:MAX_LESSON_CHARS]

    tags = []
    flags = []
    warnings = []

    # Task A: tags
    raw, err = call_classify_with_retry(text_for_model, tags_instruction, key_file, base_url)
    if err:
        warnings.append(f"tags call failed: {err}")
    else:
        try:
            parsed = extract_json_object(raw)
            tags, _ = normalize_result(parsed)
        except ValueError as e:
            preview = raw.strip().replace("\n", " ")[:200]
            warnings.append(f"tags output did not parse as JSON: {e} (preview: {preview})")

    # Task B: currency-drift flags - sample FLAGS_SAMPLES times and merge the
    # union (de-duplicated by normalized pattern text) to compensate for the
    # small fast-tier model's real call-to-call recall variance on this task
    # (see FLAGS_SAMPLES comment above).
    flags_by_key = {}
    flags_calls_ok = 0
    flags_errors = []
    for sample_idx in range(FLAGS_SAMPLES):
        raw2, err2 = call_classify_with_retry(text_for_model, FLAGS_INSTRUCTION, key_file, base_url)
        if err2:
            flags_errors.append(err2)
            continue
        try:
            parsed2 = extract_json_object(raw2)
            _, sample_flags = normalize_result(parsed2)
        except ValueError as e:
            preview = raw2.strip().replace("\n", " ")[:200]
            flags_errors.append(f"output did not parse as JSON: {e} (preview: {preview})")
            continue
        flags_calls_ok += 1
        for flag in sample_flags:
            key = flag["pattern"].strip().lower()
            if key and key not in flags_by_key:
                flags_by_key[key] = flag
    flags = list(flags_by_key.values())
    if flags_calls_ok == 0:
        warnings.append(f"currency-flags calls all failed ({FLAGS_SAMPLES} attempt(s)): {'; '.join(flags_errors)}")
    elif flags_errors:
        warnings.append(f"currency-flags: {flags_calls_ok}/{FLAGS_SAMPLES} sample(s) succeeded; {len(flags_errors)} failed: {'; '.join(flags_errors)}")

    if err and flags_calls_ok == 0:
        # Both tasks failed outright - nothing usable for this lesson.
        return {"lesson": relpath, "error": "; ".join(warnings)}

    return {
        "lesson": relpath,
        "tags": tags,
        "currency_flags": flags,
        "truncated": truncated,
        "warnings": warnings,
    }


# --------------------------------------------------------------------------
# Report generation
# --------------------------------------------------------------------------

def write_reports(out_dir, label, generated_at, track_results, overall_stats):
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"deck-tagging-report-{label}.json")
    md_path = os.path.join(out_dir, f"deck-tagging-report-{label}.md")

    report_obj = {
        "generated_at": generated_at,
        "tier": "fast",
        "endpoint": "/v1/classify",
        "ticket": "TW-115",
        "stats": overall_stats,
        "tracks": track_results,
    }
    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report_obj, f, ensure_ascii=False, indent=2)
        f.write("\n")

    lines = []
    lines.append(f"# Deck Tagging & Currency-Drift Report — {label}")
    lines.append("")
    lines.append(f"Generated: {generated_at} via `/v1/classify` (fast tier, qwen2.5:3b) — TW-115")
    lines.append("")
    lines.append(
        "This is a pattern-detection pre-filter, not a substitute for the "
        "professor/industry/certification review lenses. Use it as an input "
        "checklist to narrow what those expensive passes look at first."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Tracks processed: {overall_stats['tracks_processed']}")
    lines.append(f"- Lessons attempted: {overall_stats['lessons_attempted']}")
    lines.append(f"- Lessons succeeded: {overall_stats['lessons_succeeded']}")
    lines.append(f"- Lessons failed: {overall_stats['lessons_failed']}")
    lines.append(f"- Lessons with currency flags: {overall_stats['lessons_with_flags']}")
    lines.append(f"- Total currency flags: {overall_stats['total_flags']}")
    lines.append("")

    lines.append("## Currency-Drift Checklist (review these first)")
    lines.append("")
    any_flags = False
    for track in track_results:
        for lesson in track["lessons"]:
            flags = lesson.get("currency_flags") or []
            if not flags:
                continue
            any_flags = True
            for flag in flags:
                lines.append(f"- [ ] `{lesson['lesson']}` — pattern: `{flag['pattern']}`")
                if flag.get("reason"):
                    lines.append(f"  - reason: {flag['reason']}")
                if flag.get("snippet"):
                    snippet = flag["snippet"].replace("\n", " ")
                    lines.append(f"  - snippet: \"{snippet}\"")
    if not any_flags:
        lines.append("_No currency-drift patterns flagged in this run._")
    lines.append("")

    lines.append("## Tags by Lesson")
    lines.append("")
    for track in track_results:
        lines.append(f"### {track['track']}")
        lines.append("")
        for lesson in track["lessons"]:
            tags = lesson.get("tags") or []
            tag_str = ", ".join(tags) if tags else "_(none extracted)_"
            lines.append(f"- `{lesson['lesson']}` — {tag_str}")
        lines.append("")

    lines.append("## Partial Warnings (lesson succeeded overall, one task had an issue)")
    lines.append("")
    any_warnings = False
    for track in track_results:
        for lesson in track["lessons"]:
            for w in lesson.get("warnings") or []:
                any_warnings = True
                lines.append(f"- `{lesson['lesson']}`: {w}")
    if not any_warnings:
        lines.append("_No partial warnings in this run._")
    lines.append("")

    failures = []
    for track in track_results:
        for f in track.get("failures", []):
            failures.append(f)
    lines.append("## Parse/Call Failures (lesson skipped entirely)")
    lines.append("")
    if failures:
        for f in failures:
            lines.append(f"- `{f['lesson']}`: {f['error']}")
            if f.get("raw_preview"):
                lines.append(f"  - raw output preview: `{f['raw_preview']}`")
    else:
        lines.append("_No failures in this run._")
    lines.append("")

    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
        f.write("\n")

    return json_path, md_path


# --------------------------------------------------------------------------
# Argument parsing
# --------------------------------------------------------------------------

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="deck_tagger.py",
        description=(
            "TW-115: batch-tag lesson decks (skill/cert taxonomy) and flag "
            "currency-drift patterns using ONLY the fast-tier /v1/classify "
            "endpoint. Never calls generate()/standard tier."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--track",
        action="append",
        metavar="SLUG",
        help="Track slug (course-materials/<slug>/) to process. Repeat for multiple tracks.",
    )
    group.add_argument("--all", action="store_true", help="Process every track under --course-materials-dir.")

    parser.add_argument(
        "--course-materials-dir",
        default=DEFAULT_COURSE_MATERIALS_DIR,
        help=f"Root containing per-track directories (default: {DEFAULT_COURSE_MATERIALS_DIR})",
    )
    parser.add_argument(
        "--key-file",
        default=DEFAULT_KEY_FILE,
        help=f"Path to a local file containing the raw API key (default: {DEFAULT_KEY_FILE}). Never pass the key itself on the command line.",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"Gateway base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument(
        "--out-dir",
        default=DEFAULT_OUT_DIR,
        help=f"Directory to write the report files into (default: {DEFAULT_OUT_DIR})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max lessons to process PER TRACK (for smoke-testing a subset instead of a full track).",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="Override the '<track-or-all>' slug used in output filenames.",
    )
    return parser.parse_args(argv)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def run(args):
    if args.all:
        tracks = discover_tracks(args.course_materials_dir)
        if not tracks:
            eprint(f"Error: no tracks found under --course-materials-dir '{args.course_materials_dir}'")
            return 1
        label = args.label or "all"
    else:
        tracks = args.track
        label = args.label or ("+".join(tracks) if len(tracks) > 1 else tracks[0])

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    track_results = []
    overall = {
        "tracks_processed": 0,
        "lessons_attempted": 0,
        "lessons_succeeded": 0,
        "lessons_failed": 0,
        "lessons_with_flags": 0,
        "total_flags": 0,
    }

    for track in tracks:
        track_dir = os.path.join(args.course_materials_dir, track)
        if not os.path.isdir(os.path.join(track_dir, "lessons")):
            eprint(f"Skipping unknown track '{track}' (no {track_dir}/lessons/ directory)")
            continue

        target_skills = load_target_skills(args.course_materials_dir, track)
        tags_instruction = build_tags_instruction(target_skills)
        filenames = iter_lesson_files(args.course_materials_dir, track)
        if args.limit is not None:
            filenames = filenames[:args.limit]

        total = len(filenames)
        print(f"=== track: {track} ({total} lesson(s){' [limited]' if args.limit else ''}) ===")
        if target_skills:
            print(f"    tag vocabulary hint from course.json targetSkills: {', '.join(target_skills)}")
        else:
            print("    no course.json targetSkills found - using free-text tags")

        lessons_out = []
        failures_out = []

        for idx, filename in enumerate(filenames, start=1):
            overall["lessons_attempted"] += 1
            result = process_lesson(args.course_materials_dir, track, filename, tags_instruction, args.key_file, args.base_url)

            if "error" in result:
                overall["lessons_failed"] += 1
                failures_out.append(result)
                print(f"[{track}][{idx}/{total}] {filename} -> FAILED: {result['error']}")
                continue

            overall["lessons_succeeded"] += 1
            n_flags = len(result["currency_flags"])
            if n_flags:
                overall["lessons_with_flags"] += 1
                overall["total_flags"] += n_flags
            print(
                f"[{track}][{idx}/{total}] {filename} -> "
                f"{len(result['tags'])} tag(s), {n_flags} currency flag(s)"
                + (" [partial - see warnings]" if result.get("warnings") else "")
            )
            for w in result.get("warnings") or []:
                print(f"    warning: {w}")
            lessons_out.append(result)

        overall["tracks_processed"] += 1
        track_results.append({
            "track": track,
            "target_skills": target_skills,
            "lessons": lessons_out,
            "failures": failures_out,
        })

    if overall["tracks_processed"] == 0:
        eprint("Error: no tracks were processed - nothing to report.")
        return 1

    json_path, md_path = write_reports(args.out_dir, label, generated_at, track_results, overall)

    print()
    print("=== SUMMARY ===")
    print(f"Tracks processed:         {overall['tracks_processed']}")
    print(f"Lessons attempted:        {overall['lessons_attempted']}")
    print(f"Lessons succeeded:        {overall['lessons_succeeded']}")
    print(f"Lessons failed:           {overall['lessons_failed']}")
    print(f"Lessons with flags:       {overall['lessons_with_flags']}")
    print(f"Total currency flags:     {overall['total_flags']}")
    print(f"JSON report:              {json_path}")
    print(f"Markdown checklist:       {md_path}")

    return 0 if overall["lessons_failed"] == 0 else 1


def main(argv=None):
    args = parse_args(argv)
    try:
        return run(args)
    except SystemExit:
        raise
    except Exception as e:
        eprint(f"Fatal error: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
