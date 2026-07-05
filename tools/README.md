# tools/

Internal authoring/ops scripts for the Training-website course pipeline. These
scripts assist course authors and are run manually/offline; none of them are
part of the deployed, student-facing site (the live `grader.js` / `tutor.js`
paths under `site/` are separate and untouched by anything here).

## local_llm_client.py

Thin stdlib-only (`urllib`/`json`, no third-party deps) wrapper over the
internal local LLM gateway (`/v1/generate`, `/v1/recommend`, `/v1/classify`,
`/v1/collections`). See the module docstring for usage. The Bearer key is read
from a local, git-ignored key file (`tools/training_website.key` by default)
and is never printed or logged.

## quiz_assistant.py (TW-114)

Author-facing CLI that helps draft or review quiz questions for a lesson
deck, using the standard tier of the local LLM gateway via
`local_llm_client.generate()`.

**This tool is draft-only and human-reviewed. It never writes to a deck JSON
file.** It reads `course-materials/<slug>/decks/<lesson>.json` and writes a
separate report file (`<lesson>.quiz-review.md` by default, or `--output`) —
it never edits, overwrites, or otherwise touches the deck file itself, and it
has no effect on anything student-facing. Every suggestion or critique in the
report is a draft for a human author to accept, edit, reject, or ignore. Any
quiz item that is ultimately hand-copied into a real deck JSON still goes
through the existing peer-review process before publish, exactly as if a
human had written it from scratch.

### Modes

- `--mode review`: for each existing item in the deck's `quiz[]` array, asks
  the model to critique it (clarity, distractor quality, answer correctness,
  `why` accuracy) using the lesson's own content as grounding. Output is
  prose critique per item — nothing is auto-applied.
- `--mode draft`: generates new candidate quiz items (matching the deck's
  exact schema) for lessons whose `quiz[]` array has fewer than 4 items
  (the minimum observed across the existing course corpus); if the deck
  already has 4+, draft mode reports "coverage looks sufficient" and skips
  generation unless `--force` is passed (which generates 2 extra candidates
  for variety). Model output is parsed and validated against the schema
  before being included in the report; anything that doesn't parse or
  doesn't match the schema is clearly labeled "needs manual cleanup" rather
  than silently included.

### Usage

```
python tools/quiz_assistant.py --deck-path course-materials/<slug>/decks/<lesson>.json --mode review
python tools/quiz_assistant.py --deck-path course-materials/<slug>/decks/<lesson>.json --mode draft
python tools/quiz_assistant.py --deck-path ... --mode draft --force --tier fast --output somewhere.md
```

Flags: `--deck-path` (required), `--mode draft|review` (required), `--output`
(optional report path override), `--tier standard|fast` (default `standard`;
`fast` is useful for quick/cheap smoke-testing), `--force` (draft mode only),
`--key-file` / `--base-url` (override the gateway key/location if needed).

### Workflow for authors

1. Run the tool against a deck in `review` and/or `draft` mode.
2. Open the generated `<lesson>.quiz-review.md` report.
3. For each suggestion/critique you agree with, hand-edit the real deck JSON
   yourself (copy in a drafted item, fix a flagged ambiguity, etc.).
4. Submit that change through the normal review process before publish.

The tool itself makes no commitment beyond producing that report.

## gap_checker.py (TW-113)

Author-facing CLI that answers a free-text gap-checking question (e.g. "which
courses still miss an MCP lesson?") by retrieving grounded context from all
three real, ingested LLM-gateway collections and synthesizing one cited
answer.

**This is a first-pass triage tool. It complements, and does NOT replace, the
five-persona peer review / professor / industry / certification review passes
(TW-69/TW-98/TW-80).** Nothing it prints is a finding in itself — it is
retrieval-grounded evidence for a human to weigh alongside those review
lenses, same spirit as `quiz_assistant.py` above.

### Pattern: retrieve-all-three, then synthesize once

For each question, it calls `recommend()` **sequentially** (never in
parallel — the gateway is a single shared CPU-bound box) once per selected
collection:

- `training-lesson-content` — what courses currently *teach*
- `training-curriculum-docs` — what each track's `course.json` *says* it
  should cover
- `training-review-findings` — gaps *already flagged* by prior review passes

The retrieved source chunks (not the per-collection `answer` strings) are
assigned deterministic citation IDs per collection — `L1..Ln`, `C1..Cn`,
`R1..Rn` — built from each chunk's real `metadata` (`source` relpath,
`chunk_index`/`total_chunks`, `distance`) and truncated to ~1000 chars each,
capped at ~12000 chars of total context (highest-distance/least-relevant
chunks dropped first if over budget). Then ONE `generate()` call (tier
`--tier`, default `standard`) synthesizes a single answer that must cite
excerpt IDs inline (e.g. `[L2] [R1]`) and explicitly note whether a gap is
already flagged in review findings.

### Graceful degradation (no retries — interactive tool)

- Each collection's `recommend()` call is independent: a failure marks that
  collection `FAILED` in the status line (with the client's own redacted
  error) and the others still run.
- If **all** selected collections fail, it prints an error and exits 1
  without attempting synthesis.
- If retrieval succeeds but the single synthesis `generate()` call fails, it
  falls back to printing each collection's own `answer` field under
  `--- Per-collection answer (fallback: synthesis call failed) ---`, plus the
  normal Sources section — it does not hard-fail.
- Exit code is 0 if any answer (synthesized or fallback) was printed, 1 only
  if nothing could be produced at all.

### Usage

```
python tools/gap_checker.py "Which courses still miss a dedicated MCP (Model Context Protocol) lesson?"
python tools/gap_checker.py "..." --k 8 --show-sources
python tools/gap_checker.py "..." --collection training-review-findings --tier fast
```

Flags: `question` (positional, required), `--k` (retrieval depth per
collection, default 5), `--collection` (repeatable, restricted to the 3 real
collection names above — default: all three), `--tier standard|fast`
(synthesis call only, default `standard`), `--show-sources` (also print
truncated chunk text under each citation line), `--key-file` / `--base-url`
(same convention as the other tools above).

Output is plain stdout (no report file): a status line per collection, the
synthesized (or fallback) answer with inline citations, then a deterministic
`=== Sources ===` list built directly from `sources[].metadata` — independent
of whether the model actually cited correctly.
