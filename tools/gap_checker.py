#!/usr/bin/env python3
"""
gap_checker.py - TW-113: author-facing curriculum gap-checking CLI.

Answers free-text questions like "which courses still miss an MCP lesson?"
by retrieving grounded context from all three real, ingested LLM-gateway
collections and synthesizing a single cited answer.

FRAMING - READ THIS FIRST: this is a first-pass triage tool. It is a
complement to, NOT a replacement for, the five-persona peer review / the
professor / industry / certification review passes (see TW-69, TW-98,
TW-80). Those review lenses are the authoritative quality gates before
anything ships; this tool exists only to help an author quickly ask "does
anything already grounded in our own content/docs/findings suggest a gap
here?" before or between those passes. Nothing this tool prints should be
treated as a finding in itself - it is retrieval-grounded evidence for a
human to weigh, same spirit as quiz_assistant.py and deck_tagger.py.

The 3-retrieve + 1-synthesize pattern
--------------------------------------
For each question:

  1. Call recommend() ONCE per selected collection, SEQUENTIALLY (not in
     parallel - the gateway is a single shared CPU-bound box), against:
       - training-lesson-content   (what courses currently TEACH)
       - training-curriculum-docs  (what each track's course.json SAYS it
         should cover)
       - training-review-findings  (gaps ALREADY FLAGGED by prior review
         passes)
  2. Build a labeled context directly from the retrieved SOURCE CHUNKS
     (metadata + chunk text), not from the three per-collection "answer"
     strings. Chunks get deterministic citation IDs per collection - L1..Ln
     (lesson-content), C1..Cn (curriculum-docs), R1..Rn (review-findings) -
     assigned in the order the gateway returned them (nearest/most-relevant
     first, confirmed via real /v1/recommend calls - see below). Context is
     capped at ~12000 chars total; if over budget, the globally
     highest-distance (least relevant) chunks are dropped first, and the
     surviving chunks per collection are renumbered contiguously (no gaps).
  3. ONE generate() call (tier=args.tier) with a synthesis prompt asking the
     model to answer using ONLY the labeled excerpts, cite excerpt IDs
     inline (e.g. "[L2] [R1]"), say explicitly if the excerpts are
     insufficient rather than guess, and note whether a gap already appears
     flagged in review findings.
  4. Print the synthesized answer, then a deterministic "Sources" citation
     list built directly from sources[].metadata (independent of whether the
     model actually cited correctly).

Real metadata shape (verified via a live /v1/recommend call against all
three collections before writing this script - not guessed): each
sources[] entry is {"text": str, "metadata": dict, "distance": float}, and
metadata is always exactly {"source": <relpath str>, "chunk_index": int,
"total_chunks": int, "file_sha256": str, "file_mtime": ISO str}. There is
no separate "track"/"slug"/"title" field - "source" IS the identifying
path, e.g. "ai-app-developer-2026/lessons/aad-m3-l05-mcp-....md" for
lesson-content, "mlops-engineer/course.json" for curriculum-docs, or
"fix-targets.json" (a single shared file, distinguished by chunk_index) for
review-findings. Citation lines use metadata["source"] plus
chunk_index/total_chunks/distance directly - nothing here is invented.

Graceful degradation (no retries - this is interactive, not batch)
--------------------------------------------------------------------
- Each recommend() call is wrapped in try/except LocalLLMClientError. A
  failure marks that one collection FAILED in the status line (with the
  client's own already-redacted error message) and processing continues to
  the next collection.
- If ALL selected collections fail: print a clear error to stderr and
  sys.exit(1) - no synthesis is attempted.
- If retrieval succeeds for at least one collection but the single
  synthesis generate() call itself fails: degrade gracefully rather than
  hard-fail - print each successful collection's own "answer" field under
  "--- Per-collection answer (fallback: synthesis call failed) ---",
  followed by the normal Sources section.
- Exit code is 0 if any answer (synthesized or fallback) was printed, 1
  only if nothing could be produced at all.

Example commands
-----------------
    python tools/gap_checker.py "Which courses still miss a dedicated MCP (Model Context Protocol) lesson?"
    python tools/gap_checker.py "..." --k 8 --show-sources
    python tools/gap_checker.py "..." --collection training-review-findings --tier fast

Requires: nothing beyond the stdlib + tools/local_llm_client.py (itself
stdlib-only). A local key file (tools/training_website.key by default) must
exist to reach the gateway; see tools/local_llm_client.py for details. The
raw key is never printed or logged by this script.
"""

import argparse
import os
import sys

# tools/local_llm_client.py lives alongside this script; add this script's own
# directory to sys.path so `import local_llm_client` works regardless of the
# caller's cwd (repo root, tools/, or elsewhere). Same pattern as
# deck_tagger.py (NOT quiz_assistant.py's try/except tools.* package import).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from local_llm_client import (  # noqa: E402
    generate,
    recommend,
    LocalLLMClientError,
    DEFAULT_BASE_URL,
    DEFAULT_KEY_FILE,
)

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

# Canonical order - also the order collections are queried in and the order
# they appear in the status line / Sources section, regardless of the order
# --collection flags were passed in.
ALL_COLLECTIONS = (
    "training-lesson-content",
    "training-curriculum-docs",
    "training-review-findings",
)

CITATION_PREFIX = {
    "training-lesson-content": "L",
    "training-curriculum-docs": "C",
    "training-review-findings": "R",
}

SOURCE_DESCRIPTION = {
    "training-lesson-content": "lesson content (what courses currently teach)",
    "training-curriculum-docs": "curriculum docs (what each track's course.json says the course should cover)",
    "training-review-findings": "review findings (gaps already flagged by prior review passes)",
}

CHUNK_TEXT_TRUNCATE_CHARS = 1000
TOTAL_CONTEXT_BUDGET_CHARS = 12000

SYNTHESIS_PROMPT_TEMPLATE = """Answer the author's question using ONLY the excerpts below. Cite excerpt IDs inline like [L2] [R1]. Excerpts come from {n_sources} source{plural}: {source_descriptions}. If the excerpts don't contain enough to answer, say what's missing rather than guessing. Note explicitly whether a gap appears already-flagged in review findings or not.

Question: {question}

Excerpts:
{context}

Answer:"""


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# --------------------------------------------------------------------------
# Argument parsing
# --------------------------------------------------------------------------

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="gap_checker.py",
        description=(
            "TW-113: first-pass triage tool - retrieves grounded context from "
            "all three real LLM-gateway collections (lesson content, curriculum "
            "docs, review findings) and synthesizes one cited answer to a "
            "free-text gap-checking question. Complements, does not replace, "
            "the five-persona / professor / industry / certification review passes."
        ),
    )
    parser.add_argument("question", help="Free-text question, e.g. \"which courses still miss an MCP lesson?\"")
    parser.add_argument("--k", type=int, default=5, help="Retrieval depth per collection (default: 5)")
    parser.add_argument(
        "--collection",
        action="append",
        choices=ALL_COLLECTIONS,
        dest="collections",
        metavar="{" + ",".join(ALL_COLLECTIONS) + "}",
        help="Restrict to specific collection(s). Repeat for multiple. Default: all three.",
    )
    parser.add_argument(
        "--tier",
        choices=["standard", "fast"],
        default="standard",
        help="Tier for the FINAL synthesis generate() call only (default: standard). Retrieval always uses recommend()'s own tier.",
    )
    parser.add_argument(
        "--show-sources",
        action="store_true",
        help="Also print truncated chunk text under each citation line.",
    )
    parser.add_argument("--key-file", default=DEFAULT_KEY_FILE, help=f"Path to a local file containing the raw API key (default: {DEFAULT_KEY_FILE}). Never pass the key itself on the command line.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"Gateway base URL (default: {DEFAULT_BASE_URL})")
    return parser.parse_args(argv)


# --------------------------------------------------------------------------
# Retrieval
# --------------------------------------------------------------------------

def retrieve_all(question, collections, k, key_file, base_url):
    """Sequentially call recommend() once per collection (never in parallel -
    single shared CPU-bound gateway box). Returns (results, status_parts):

      results: {collection: {"ok": True, "data": <full recommend() dict>}
                             | {"ok": False, "error": <redacted str>}}
      status_parts: list of human-readable "<collection> (ok, N chunks)" /
                    "<collection> (FAILED: <reason>)" strings, in
                    `collections` order, for the status line.

    Never raises - each collection's failure is captured independently so
    one bad collection doesn't stop the others (no retries; interactive tool).
    """
    results = {}
    status_parts = []
    for collection in collections:
        try:
            data = recommend(question, collection=collection, k=k, key_file=key_file, base_url=base_url)
        except LocalLLMClientError as e:
            err = str(e)
            results[collection] = {"ok": False, "error": err}
            status_parts.append(f"{collection} (FAILED: {err})")
            continue
        sources = data.get("sources") or []
        results[collection] = {"ok": True, "data": data}
        status_parts.append(f"{collection} (ok, {len(sources)} chunk{'s' if len(sources) != 1 else ''})")
    return results, status_parts


# --------------------------------------------------------------------------
# Context building / citation assignment
# --------------------------------------------------------------------------

def build_citation_entries(ok_collections, results):
    """Flatten every retrieved source across the successful collections into
    one list of candidate entries, apply the ~12000-char total budget
    (dropping globally-highest-distance chunks first when over budget), then
    assign deterministic per-collection citation IDs (L1..Ln / C1..Cn /
    R1..Rn) to the survivors in their original per-collection retrieval
    order (renumbered contiguously - no gaps from dropped chunks).

    Returns a dict: {collection: [ {"id": "L1", "metadata": dict,
    "distance": float, "text": str (full, untruncated)} , ... ]} in
    ALL_COLLECTIONS order, survivors only.
    """
    candidates = []
    for collection in ok_collections:
        sources = results[collection]["data"].get("sources") or []
        for order_idx, src in enumerate(sources):
            candidates.append({
                "collection": collection,
                "order_idx": order_idx,
                "metadata": src.get("metadata") or {},
                "distance": src.get("distance"),
                "text": src.get("text") or "",
            })

    # Decide inclusion by walking candidates in ascending-distance order
    # (None distances sort last, treated as least relevant) and accumulating
    # the formatted-block size; once the budget would be exceeded, that
    # candidate and all remaining (higher-distance) ones are dropped.
    def sort_key(c):
        d = c["distance"]
        return (d is None, d if d is not None else 0.0)

    running_total = 0
    included_keys = set()
    for cand in sorted(candidates, key=sort_key):
        block_len = _estimate_block_len(cand)
        if running_total + block_len > TOTAL_CONTEXT_BUDGET_CHARS and included_keys:
            # Always keep at least one entry even if a single chunk alone
            # would blow the budget - a synthesis call with zero context
            # is worse than one oversized excerpt.
            continue
        included_keys.add((cand["collection"], cand["order_idx"]))
        running_total += block_len

    by_collection = {c: [] for c in ALL_COLLECTIONS}
    for collection in ok_collections:
        sources = results[collection]["data"].get("sources") or []
        survivors = [
            cand for cand in candidates
            if cand["collection"] == collection and (collection, cand["order_idx"]) in included_keys
        ]
        survivors.sort(key=lambda c: c["order_idx"])  # original retrieval order
        prefix = CITATION_PREFIX[collection]
        for i, cand in enumerate(survivors, start=1):
            by_collection[collection].append({
                "id": f"{prefix}{i}",
                "metadata": cand["metadata"],
                "distance": cand["distance"],
                "text": cand["text"],
            })
    return by_collection


def _estimate_block_len(cand):
    truncated = cand["text"][:CHUNK_TEXT_TRUNCATE_CHARS]
    meta = cand["metadata"]
    header = f"[??] ({cand['collection']}) source: {meta.get('source')} (chunk {meta.get('chunk_index')}/{meta.get('total_chunks')}, distance {_fmt_distance(cand['distance'])})"
    return len(header) + len(truncated) + 2


def _fmt_distance(distance):
    if isinstance(distance, (int, float)):
        return f"{distance:.2f}"
    return "unknown"


def format_context_block(entry, collection):
    meta = entry["metadata"]
    truncated = entry["text"][:CHUNK_TEXT_TRUNCATE_CHARS]
    header = (
        f"[{entry['id']}] ({collection}) source: {meta.get('source')} "
        f"(chunk {meta.get('chunk_index')}/{meta.get('total_chunks')}, distance {_fmt_distance(entry['distance'])})"
    )
    return f"{header}\n{truncated}"


def build_context_text(citation_entries):
    """citation_entries: {collection: [entry, ...]} in ALL_COLLECTIONS order.
    Returns the full labeled context string for the synthesis prompt."""
    blocks = []
    for collection in ALL_COLLECTIONS:
        for entry in citation_entries.get(collection, []):
            blocks.append(format_context_block(entry, collection))
    return "\n\n".join(blocks)


def build_synthesis_prompt(question, ok_collections, context_text):
    descriptions = [SOURCE_DESCRIPTION[c] for c in ALL_COLLECTIONS if c in ok_collections]
    n = len(descriptions)
    return SYNTHESIS_PROMPT_TEMPLATE.format(
        n_sources=n,
        plural="" if n == 1 else "s",
        source_descriptions="; ".join(descriptions),
        question=question,
        context=context_text,
    )


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def print_sources_section(citation_entries, show_sources):
    print("=== Sources ===")
    any_entries = False
    for collection in ALL_COLLECTIONS:
        entries = citation_entries.get(collection, [])
        if not entries:
            continue
        any_entries = True
        print(f"[{collection}]")
        for entry in entries:
            meta = entry["metadata"]
            print(f"  {entry['id']:<4}{meta.get('source', '?')}   (distance {_fmt_distance(entry['distance'])})")
            if show_sources:
                truncated = entry["text"][:CHUNK_TEXT_TRUNCATE_CHARS]
                indented = "\n".join(f"      {line}" for line in truncated.splitlines())
                print(indented)
        print()
    if not any_entries:
        print("(no sources - all selected collections failed)")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def run(args):
    collections = [c for c in ALL_COLLECTIONS if c in (args.collections or ALL_COLLECTIONS)]

    print(f"Question: {args.question}")
    results, status_parts = retrieve_all(args.question, collections, args.k, args.key_file, args.base_url)
    print("Collections queried: " + ", ".join(status_parts))
    print()

    ok_collections = [c for c in collections if results[c]["ok"]]
    if not ok_collections:
        eprint("Error: all selected collections failed to retrieve - nothing to synthesize.")
        return 1

    citation_entries = build_citation_entries(ok_collections, results)
    context_text = build_context_text(citation_entries)
    synthesis_prompt = build_synthesis_prompt(args.question, ok_collections, context_text)

    answer_text = None
    synth_error = None
    try:
        answer_text = generate(synthesis_prompt, tier=args.tier, key_file=args.key_file, base_url=args.base_url)
    except LocalLLMClientError as e:
        synth_error = str(e)

    if answer_text is not None:
        print("=== Answer ===")
        print(answer_text.strip())
    else:
        print(f"--- Per-collection answer (fallback: synthesis call failed: {synth_error}) ---")
        for collection in ok_collections:
            print(f"[{collection}]")
            print((results[collection]["data"].get("answer") or "(no answer field returned)").strip())
            print()
    print()

    print_sources_section(citation_entries, args.show_sources)

    return 0


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
