#!/usr/bin/env python3
"""
quiz_assistant.py - TW-114: author-facing quiz drafting/review assistant.

Given a deck JSON file (course-materials/<slug>/decks/<lesson>.json), this CLI
calls the standard-tier local LLM gateway (via tools/local_llm_client.py) to
either:

  --mode draft    Draft candidate quiz items for a lesson whose quiz[] array
                   has too few items (or none), matching the deck's existing
                   quiz schema exactly so they can be hand-copied in.
  --mode review    Critique each EXISTING quiz item in the deck for ambiguity
                   / quality issues (unclear wording, distractor problems,
                   answer/why mismatches, etc).

THIS TOOL NEVER WRITES TO course-materials/*/decks/*.json. It only reads the
deck and writes a sibling `<deck-stem>.quiz-review.md` report next to it (or
wherever --output points). It is author-facing only: a human must review,
edit, and hand-copy any accepted suggestion into the real deck file, which
then still goes through the existing peer-review process before publish.
This tool has zero effect on anything student-facing (grader.js/tutor.js and
the published deck files are untouched).

Verified deck / quiz schema (read directly from real files - all 391 decks
under course-materials/*/decks/*.json, verified 2026-07-04, not just the one
example quoted in the ticket):

  deck (top level): slug, title, month, monthTitle, lesson, video, summary,
    objectives[], quiz[], resources[], body_markdown (str), slides[].

  quiz[] item (ONE quiz[] array per deck, i.e. per whole lesson; 4-6 items
    per deck observed across the corpus, no deck had zero):
    {
      "q": str,                       # question text
      "options": [str, ...] | null,   # MCQ: 2 or 4 choices (both lengths seen).
                                       # Short-answer items either OMIT this
                                       # key entirely (majority) or set it to
                                       # null (seen in a handful of decks) -
                                       # our validator accepts either form.
      "answer": int | str,            # MCQ: index into options (int).
                                       # Short-answer: the model answer (str).
      "why": str,                     # explanation. Present on effectively
                                       # all items (4 of 2340 items in the
                                       # corpus omit it); this tool always
                                       # emits it on drafted candidates.
    }

Design note on "lesson unit" granularity: the verified schema has exactly ONE
quiz[] array per deck (i.e. per whole lesson) - there is no per-slide quiz
structure. So this tool treats each deck as a single lesson unit and sources
context from body_markdown (falling back to concatenated slide narration if
body_markdown is missing/empty), rather than trying to generate a quiz per
slide.

Draft-mode coverage default (documented per TW-114 "use your judgment on a
sensible default, document it"): MIN_QUIZ_ITEMS = 4, matching the minimum
observed across the existing 391-deck corpus. If the deck's existing quiz[]
has fewer than 4 items (including zero), draft mode generates enough
candidates to reach 4. If it already has >= 4, draft mode reports "coverage
looks sufficient, skipping" unless --force is passed, in which case it
generates FORCE_EXTRA_ITEMS (2) extra candidates for the author to consider
as additional variety.

Usage:
  python tools/quiz_assistant.py --deck-path course-materials/<slug>/decks/<lesson>.json --mode review
  python tools/quiz_assistant.py --deck-path course-materials/<slug>/decks/<lesson>.json --mode draft
  python tools/quiz_assistant.py --deck-path ... --mode draft --force --tier fast --output out.md

Requires: nothing beyond the stdlib + tools/local_llm_client.py (itself
stdlib-only). A local key file (tools/training_website.key by default) must
exist to reach the gateway; see tools/local_llm_client.py for details. The
raw key is never printed or logged by this script.
"""

import argparse
import datetime
import json
import os
import re
import sys

try:
    from tools.local_llm_client import (
        DEFAULT_BASE_URL,
        DEFAULT_KEY_FILE,
        LocalLLMClientError,
        generate,
    )
except ImportError:
    # Fallback for running this script directly from within tools/, e.g.
    # `python tools/quiz_assistant.py ...` from the repo root - Python puts
    # this script's own directory (tools/) on sys.path, so a sibling import
    # works even though the `tools` package import above does not resolve.
    from local_llm_client import (
        DEFAULT_BASE_URL,
        DEFAULT_KEY_FILE,
        LocalLLMClientError,
        generate,
    )

# --------------------------------------------------------------------------
# Defaults / thresholds (see module docstring for rationale)
# --------------------------------------------------------------------------

MIN_QUIZ_ITEMS = 4
FORCE_EXTRA_ITEMS = 2
MAX_CONTEXT_CHARS = 6000
VALID_OPTION_LENGTHS = (2, 4)


# --------------------------------------------------------------------------
# Deck loading / lesson text extraction
# --------------------------------------------------------------------------

def load_deck(deck_path):
    """Read and parse the deck JSON. Raises SystemExit with a clear message
    on any I/O or parse failure. Never mutates or writes back the file."""
    try:
        with open(deck_path, "r", encoding="utf-8") as f:
            raw = f.read()
    except OSError as e:
        sys.exit(f"Could not read deck file '{deck_path}': {type(e).__name__}: {e}")
    try:
        deck = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"Deck file '{deck_path}' is not valid JSON: {e}")
    if not isinstance(deck, dict):
        sys.exit(f"Deck file '{deck_path}' does not contain a JSON object at the top level.")
    return deck


def get_lesson_text(deck):
    """Return the best available lesson narrative text: body_markdown if
    present/non-empty, else concatenated slide narration. Truncated to
    MAX_CONTEXT_CHARS to keep prompts a reasonable size for the standard-tier
    model; truncation is noted in the returned text so it's visible in
    reports if it happens."""
    body = deck.get("body_markdown")
    if isinstance(body, str) and body.strip():
        text = body.strip()
        source = "body_markdown"
    else:
        slides = deck.get("slides") or []
        narrations = [
            s.get("narration", "")
            for s in slides
            if isinstance(s, dict) and s.get("narration")
        ]
        text = "\n\n".join(narrations).strip()
        source = "slide narration (body_markdown was missing/empty)"

    if len(text) > MAX_CONTEXT_CHARS:
        text = text[:MAX_CONTEXT_CHARS] + "\n\n...[truncated for prompt length]..."
    return text, source


# --------------------------------------------------------------------------
# Quiz item validation (against the verified schema)
# --------------------------------------------------------------------------

def validate_quiz_item(item):
    """Return a list of problem strings (empty list = valid). Mirrors the
    schema verified from real deck files (see module docstring)."""
    problems = []
    if not isinstance(item, dict):
        return ["item is not a JSON object"]

    q = item.get("q")
    if not isinstance(q, str) or not q.strip():
        problems.append("missing/empty 'q' (question text) string")

    why = item.get("why")
    if why is not None and (not isinstance(why, str) or not why.strip()):
        problems.append("'why' is present but is not a non-empty string")

    options = item.get("options")
    answer = item.get("answer")

    if options is not None:
        if not isinstance(options, list) or not all(isinstance(o, str) and o.strip() for o in options):
            problems.append("'options' must be a list of non-empty strings (or null/omitted for short-answer)")
        elif len(options) not in VALID_OPTION_LENGTHS:
            problems.append(
                f"'options' has {len(options)} entries; the verified corpus convention is 2 or 4"
            )
        if not isinstance(answer, int) or isinstance(answer, bool):
            problems.append("MCQ item (has 'options') must have an integer 'answer' index")
        elif isinstance(options, list) and not (0 <= answer < len(options)):
            problems.append(f"'answer' index {answer} is out of range for {len(options)} options")
    else:
        if not isinstance(answer, str) or not answer.strip():
            problems.append("short-answer item (no 'options') must have a non-empty string 'answer'")

    return problems


# --------------------------------------------------------------------------
# Model output parsing (draft mode)
# --------------------------------------------------------------------------

def extract_json_array(text):
    """Best-effort extraction of a JSON array from a raw model response that
    may include code fences or stray prose around the JSON. Returns the
    array substring, or None if no balanced '[...]' block is found."""
    stripped = text.strip()
    stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
    stripped = re.sub(r"\s*```\s*$", "", stripped)

    start = stripped.find("[")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(stripped)):
        ch = stripped[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return stripped[start : i + 1]
    return None


def parse_draft_response(raw_text):
    """Try to parse the model's draft response into a list of quiz-item
    dicts. Returns (items_or_None, error_message_or_None). Never raises -
    callers use a None items list as the "needs manual cleanup" signal."""
    blob = extract_json_array(raw_text)
    if blob is None:
        return None, "No JSON array ('[...]') found in the model response."
    try:
        parsed = json.loads(blob)
    except json.JSONDecodeError as e:
        return None, f"Extracted JSON array did not parse: {e}"
    if not isinstance(parsed, list):
        return None, "Parsed JSON was not a list."
    return parsed, None


# --------------------------------------------------------------------------
# Prompt construction
# --------------------------------------------------------------------------

SCHEMA_EXAMPLE = """[
  {"q": "<MCQ question text>", "options": ["<choice A>", "<choice B>", "<choice C>", "<choice D>"], "answer": 2, "why": "<why this answer is correct, in one or two sentences>"},
  {"q": "<short-answer question text>", "answer": "<model answer, a sentence or two>", "why": "<why this is the expected answer>"}
]"""


def build_draft_prompt(deck, lesson_text, source_note, existing_qs, n_needed):
    title = deck.get("title", deck.get("slug", "this lesson"))
    objectives = deck.get("objectives") or []
    objectives_block = "\n".join(f"- {o}" for o in objectives) or "(none listed)"
    existing_block = "\n".join(f"- {q}" for q in existing_qs) or "(none yet)"

    return f"""You are drafting candidate quiz questions for an internal training course lesson.
This is DRAFT content only - a human author will review, edit, and approve it before it
is ever added to the real course. Do not include any commentary outside the JSON.

Lesson title: {title}

Lesson objectives:
{objectives_block}

Lesson content (source: {source_note}):
---
{lesson_text}
---

Existing quiz questions already in this lesson (do NOT repeat these or ask near-duplicates):
{existing_block}

Task: write exactly {n_needed} NEW candidate quiz item(s) that test understanding of the
lesson content above. Mix multiple-choice and short-answer if you write more than one.
Each item MUST match this exact JSON schema (this is the schema this course's real decks
use - match it exactly, field names included):

{SCHEMA_EXAMPLE}

Rules:
- Multiple-choice items: "options" is a list of 4 plausible, unambiguous choices (2 is
  also acceptable for true/false-style questions); "answer" is the integer index (0-based)
  of the correct option.
- Short-answer items: omit "options" entirely; "answer" is a string with the expected answer.
- "why" is always a short, accurate explanation of the correct answer.
- Respond with ONLY the JSON array, no markdown code fences, no extra prose before or after.
"""


def build_review_prompt(deck, lesson_text, source_note, item, idx, total):
    title = deck.get("title", deck.get("slug", "this lesson"))
    item_json = json.dumps(item, indent=2, ensure_ascii=False)

    return f"""You are reviewing an existing quiz question from an internal training course
lesson for ambiguity and quality issues, to help a human author decide whether to keep,
fix, or replace it. This is a review only - you are not editing anything directly.

Lesson title: {title}

Lesson content (source: {source_note}, for context):
---
{lesson_text}
---

Quiz item {idx} of {total} to review (verbatim JSON from the deck):
{item_json}

Critique this quiz item. Specifically address:
1. Is the question wording clear and unambiguous?
2. If it has multiple-choice options: are the distractors plausible but clearly wrong, and
   is exactly one option defensibly correct (no overlap/tie with another option)?
3. Is the "answer" actually correct given the lesson content above?
4. Is the "why" explanation accurate, clear, and does it match the marked answer?
5. Any suggested rewrite, if you see a problem (optional, keep it brief).

Respond in plain prose (not JSON), a short paragraph or bullet list. If you find no
issues, say so explicitly rather than inventing a problem.
"""


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------

def run_draft_mode(deck, lesson_text, source_note, tier, key_file, base_url, force):
    existing = deck.get("quiz") or []
    existing = [it for it in existing if isinstance(it, dict)]
    existing_qs = [it.get("q", "") for it in existing]
    n_existing = len(existing)

    if n_existing >= MIN_QUIZ_ITEMS and not force:
        decision = (
            f"Existing quiz has {n_existing} item(s) (>= threshold {MIN_QUIZ_ITEMS}); "
            f"coverage looks sufficient. Skipping generation. Pass --force to generate "
            f"{FORCE_EXTRA_ITEMS} extra candidate(s) anyway."
        )
        return {"decision": decision, "n_requested": 0, "candidates": [], "raw_response": None}

    if n_existing >= MIN_QUIZ_ITEMS and force:
        n_needed = FORCE_EXTRA_ITEMS
        decision = (
            f"Existing quiz has {n_existing} item(s) (>= threshold {MIN_QUIZ_ITEMS}); "
            f"--force set, generating {n_needed} extra candidate(s) for variety."
        )
    else:
        n_needed = MIN_QUIZ_ITEMS - n_existing
        decision = (
            f"Existing quiz has {n_existing} item(s) (< threshold {MIN_QUIZ_ITEMS}); "
            f"generating {n_needed} candidate item(s) to reach the threshold."
        )

    prompt = build_draft_prompt(deck, lesson_text, source_note, existing_qs, n_needed)
    try:
        raw = generate(prompt, tier=tier, key_file=key_file, base_url=base_url)
    except LocalLLMClientError as e:
        return {
            "decision": decision,
            "n_requested": n_needed,
            "candidates": [{"status": "error", "problems": [f"gateway call failed: {e}"], "item": None, "raw": None}],
            "raw_response": None,
        }

    parsed, parse_error = parse_draft_response(raw)
    candidates = []
    if parsed is None:
        candidates.append({"status": "needs manual cleanup", "problems": [parse_error], "item": None, "raw": raw})
    else:
        for item in parsed:
            problems = validate_quiz_item(item)
            candidates.append({
                "status": "ok" if not problems else "needs manual cleanup",
                "problems": problems,
                "item": item,
                "raw": None,
            })
    return {"decision": decision, "n_requested": n_needed, "candidates": candidates, "raw_response": raw}


def run_review_mode(deck, lesson_text, source_note, tier, key_file, base_url):
    existing = deck.get("quiz") or []
    existing = [it for it in existing if isinstance(it, dict)]
    results = []
    total = len(existing)
    for idx, item in enumerate(existing, start=1):
        prompt = build_review_prompt(deck, lesson_text, source_note, item, idx, total)
        try:
            critique = generate(prompt, tier=tier, key_file=key_file, base_url=base_url)
        except LocalLLMClientError as e:
            critique = f"[ERROR calling gateway for this item: {e}]"
        results.append({"idx": idx, "item": item, "critique": critique})
    return results


# --------------------------------------------------------------------------
# Report rendering
# --------------------------------------------------------------------------

def _quiz_item_markdown(item):
    lines = [f"- **q:** {item.get('q', '(missing)')}"]
    options = item.get("options")
    if options:
        for i, opt in enumerate(options):
            marker = " <- answer" if item.get("answer") == i else ""
            lines.append(f"  - [{i}] {opt}{marker}")
    else:
        lines.append(f"  - **answer (short-answer):** {item.get('answer', '(missing)')}")
    if item.get("why"):
        lines.append(f"  - **why:** {item['why']}")
    return "\n".join(lines)


def render_draft_report(deck, deck_path, args, lesson_text, source_note, result):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append(f"# Quiz Assistant Report - draft mode")
    lines.append("")
    lines.append("**DRAFT ONLY - this is a suggestion, not applied to any file.** A human author")
    lines.append("must review, edit, and hand-copy any accepted item into the real deck JSON;")
    lines.append("it then still goes through the existing peer-review process before publish.")
    lines.append("See tools/README.md.")
    lines.append("")
    lines.append(f"- Deck: `{deck_path}`")
    lines.append(f"- Lesson: {deck.get('title', deck.get('slug', '(untitled)'))}")
    lines.append(f"- Generated: {now}")
    lines.append(f"- Tier: {args.tier}")
    lines.append(f"- Lesson text source: {source_note}")
    lines.append("")
    lines.append("## Coverage decision")
    lines.append("")
    lines.append(result["decision"])
    lines.append("")
    if not result["candidates"]:
        lines.append("(No candidates generated.)")
    else:
        lines.append("## Candidate quiz items")
        lines.append("")
        for n, cand in enumerate(result["candidates"], start=1):
            status = cand["status"].upper()
            lines.append(f"### Candidate {n} - {status}")
            lines.append("")
            if cand["item"] is not None:
                lines.append("```json")
                lines.append(json.dumps(cand["item"], indent=2, ensure_ascii=False))
                lines.append("```")
            if cand.get("raw"):
                lines.append("Raw (unparsed) model output:")
                lines.append("")
                lines.append("```")
                lines.append(cand["raw"])
                lines.append("```")
            if cand["problems"]:
                lines.append("")
                lines.append("Issues found (needs manual cleanup before use):")
                for p in cand["problems"]:
                    lines.append(f"- {p}")
            lines.append("")
    return "\n".join(lines)


def render_review_report(deck, deck_path, args, lesson_text, source_note, results):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append(f"# Quiz Assistant Report - review mode")
    lines.append("")
    lines.append("**DRAFT/ADVISORY ONLY - this is a critique, not applied to any file.** A human")
    lines.append("author must decide whether to keep, fix, or replace any flagged item in the")
    lines.append("real deck JSON; any change still goes through the existing peer-review process")
    lines.append("before publish. See tools/README.md.")
    lines.append("")
    lines.append(f"- Deck: `{deck_path}`")
    lines.append(f"- Lesson: {deck.get('title', deck.get('slug', '(untitled)'))}")
    lines.append(f"- Generated: {now}")
    lines.append(f"- Tier: {args.tier}")
    lines.append(f"- Lesson text source: {source_note}")
    lines.append(f"- Existing quiz items reviewed: {len(results)}")
    lines.append("")
    if not results:
        lines.append("(No existing quiz items to review.)")
    for r in results:
        lines.append(f"## Item {r['idx']} of {len(results)}")
        lines.append("")
        lines.append(_quiz_item_markdown(r["item"]))
        lines.append("")
        lines.append("**Model critique:**")
        lines.append("")
        lines.append(r["critique"])
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def default_output_path(deck_path):
    stem, _ext = os.path.splitext(deck_path)
    return f"{stem}.quiz-review.md"


def main():
    parser = argparse.ArgumentParser(
        description=(
            "TW-114 author-facing quiz drafting/review assistant. Draft-only output; "
            "never writes to the deck JSON. See tools/README.md."
        )
    )
    parser.add_argument("--deck-path", required=True, help="Path to a deck JSON file (course-materials/<slug>/decks/<lesson>.json)")
    parser.add_argument("--mode", required=True, choices=["draft", "review"], help="draft: generate candidate quiz items; review: critique existing quiz items")
    parser.add_argument("--output", default=None, help="Report output path (default: <deck-stem>.quiz-review.md alongside the deck)")
    parser.add_argument("--tier", default="standard", choices=["standard", "fast"], help="Model tier to call (default: standard)")
    parser.add_argument("--force", action="store_true", help="Draft mode only: generate extra candidates even if the deck already meets the coverage threshold")
    parser.add_argument("--key-file", default=DEFAULT_KEY_FILE, help="Path to the local gateway API key file")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Gateway base URL")
    args = parser.parse_args()

    deck = load_deck(args.deck_path)
    lesson_text, source_note = get_lesson_text(deck)

    if args.mode == "draft":
        result = run_draft_mode(deck, lesson_text, source_note, args.tier, args.key_file, args.base_url, args.force)
        report = render_draft_report(deck, args.deck_path, args, lesson_text, source_note, result)
        n_ok = sum(1 for c in result["candidates"] if c["status"] == "ok")
        n_bad = sum(1 for c in result["candidates"] if c["status"] != "ok")
        summary = (
            f"[draft] {args.deck_path}: {result['decision']}\n"
            f"[draft] Candidates generated: {len(result['candidates'])} "
            f"(valid: {n_ok}, needs manual cleanup: {n_bad})"
        )
    else:
        results = run_review_mode(deck, lesson_text, source_note, args.tier, args.key_file, args.base_url)
        report = render_review_report(deck, args.deck_path, args, lesson_text, source_note, results)
        summary = f"[review] {args.deck_path}: critiqued {len(results)} existing quiz item(s)"

    output_path = args.output or default_output_path(args.deck_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(summary)
    print(f"Report written to: {output_path}")
    print("Reminder: draft/critique only - nothing was written to the deck JSON. Human review required before use.")


if __name__ == "__main__":
    main()
