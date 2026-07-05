# HOWTO — Ingesting Training-Website content into the local LLM platform (TW-110)

This wires the four Training-Website content collections into the local LLM gateway's
Chroma retrieval index using the existing `tools/ingest_docs.py` CLI (from the
`Building_LLM` repo). It is a repeatable step: re-run it whenever the underlying
content changes.

## Why four collections, not one

Mirrors the Guardian Baseline pattern: split by content-type / update cadence rather
than one giant collection, so each can be re-ingested independently at its own
natural cadence.

| Collection | Source | Update cadence |
|---|---|---|
| `training-lesson-content` | `course-materials/<slug>/lessons/*.md` (391 files across 12 tracks) | Whenever a course/lesson is published or edited |
| `training-curriculum-docs` | `course-materials/<slug>/course.json` (12 files) | On new course/module additions |
| `training-review-findings` | `review-summary.json`, `fix-targets.json` (repo root) | After each review pass |
| `training-internal-runbooks` | `HOWTO_*.md`, `SECURITY_REVIEW.md`, `MONITORING.md`, `LESSONS_LEARNED.md` (repo root) | Whenever these docs change |

### Note on `training-lesson-content` source choice

`build_lesson_index.py` bundles the same per-lesson text into a single combined
`api/src/shared/lessons.generated.json` (one JSON object keyed by lesson id, body
capped at 8000 chars) for the tutor/grader Functions at runtime. That combined file is
**not** used as the ingestion source here: `ingest_docs.py` chunks whole files at
heading boundaries and tags each chunk with its source *file path* for provenance —
chunking a single multi-lesson JSON blob would produce chunks with no clean per-lesson
boundary and every chunk's `source` metadata would just say `lessons.generated.json`
instead of identifying the actual lesson. The individual
`course-materials/<slug>/lessons/*.md` files are the primary source material
`build_lesson_index.py` itself reads from, and they chunk cleanly by heading — so they
are used directly instead.

### Note on "top-level curriculum docs"

Beyond the per-track `course.json` files, no additional top-level curriculum document
exists in the repo. `api/src/shared/catalog.generated.json` (built by
`build_catalog.py`) is a derived build artifact summarizing the same `course.json`
fields for the Custom Advisor's matcher — redundant with what's already being
ingested from `course.json`, so it is intentionally not ingested separately.

## Data sensitivity

`course-materials/` is generic instructional content. A scan of the lesson `.md`
files, `course.json` files, review findings, and runbook docs for email-address
patterns turned up only doc-placeholder addresses (`@contoso.com`, `@co.com`,
`@example.com`, `you@example.com`) used as examples inside lesson prose, plus one
internal operational contact address in `MONITORING.md` (the site owner's own alert
contact, not student data). Real student data (progress records, uploaded résumés)
lives only in Cosmos DB / Cloudflare R2 at runtime and is **not** read from this repo
and **not** in scope for this ingestion.

## Prerequisites

- `tools/ingest_docs.py` already deployed at `~/llm-platform/tools/ingest_docs.py` on
  the LLM server (kept in sync with `Building_LLM/tools/ingest_docs.py` — verify with
  `md5sum` on both sides before a real run if the tool has changed).
- An API key for this app already provisioned server-side at
  `~/llm-platform/keys/training-website-internal.key` (never copied off the server).
- SSH access: `ssh -i ~/.ssh/guardian_llm_server kasare@192.168.1.162`.

## Steps (repeat whenever content changes)

### 1. Stage only the in-scope files locally

Do **not** point `--source-dir` at whole track directories or `course-materials/`
directly — that would sweep in `decks/*.json` (slide decks), `videos/*.mp4`,
`study-packs/*.docx`, and stray per-track docs (e.g.
`course-materials/cloud-security-engineer/PLANNING.md`), none of which belong in these
four collections. Instead, stage a mirror containing only:

- `training-lesson-content/<slug>/lessons/*.md` (copy the `lessons/` subdir per track)
- `training-curriculum-docs/<slug>/course.json` (copy just `course.json` per track)
- `training-review-findings/{review-summary.json,fix-targets.json}` (repo root)
- `training-internal-runbooks/{HOWTO_*.md,SECURITY_REVIEW.md,MONITORING.md,LESSONS_LEARNED.md}` (repo root)

### 2. Copy the staged content to the server

```bash
scp -i ~/.ssh/guardian_llm_server -r <staged-dir>/training-lesson-content \
  <staged-dir>/training-curriculum-docs \
  <staged-dir>/training-review-findings \
  <staged-dir>/training-internal-runbooks \
  kasare@192.168.1.162:~/llm-platform/training-ingest-src/
```

This overwrites the previous copy in place — `ingest_docs.py` re-ingesting an edited
file safely upserts the same chunk IDs. See the **known limitation** below for
deleted/shrunk files.

### 3. Dry-run each collection first — always

```bash
ssh -i ~/.ssh/guardian_llm_server kasare@192.168.1.162 '
cd ~/llm-platform &&
python3 tools/ingest_docs.py --source-dir training-ingest-src/training-lesson-content   --collection training-lesson-content   --extensions .md   --dry-run --verbose --base-url http://100.119.240.75:8000 &&
python3 tools/ingest_docs.py --source-dir training-ingest-src/training-curriculum-docs  --collection training-curriculum-docs  --extensions .json --dry-run --verbose --base-url http://100.119.240.75:8000 &&
python3 tools/ingest_docs.py --source-dir training-ingest-src/training-review-findings   --collection training-review-findings   --extensions .json --dry-run --verbose --base-url http://100.119.240.75:8000 &&
python3 tools/ingest_docs.py --source-dir training-ingest-src/training-internal-runbooks --collection training-internal-runbooks --extensions .md   --dry-run --verbose --base-url http://100.119.240.75:8000
'
```

Review file/chunk counts against the expected scale (see TW-110 dry-run report for the
July 2026 baseline: 412 files / 4,675 chunks / ~3.9 MB total across the four
collections) before proceeding.

### 4. Real run (only after reviewing the dry-run output)

Same commands as step 3 but drop `--dry-run` and add
`--key-file ~/llm-platform/keys/training-website-internal.key`:

```bash
ssh -i ~/.ssh/guardian_llm_server kasare@192.168.1.162 '
cd ~/llm-platform &&
python3 tools/ingest_docs.py --source-dir training-ingest-src/training-lesson-content   --collection training-lesson-content   --extensions .md   --key-file keys/training-website-internal.key --base-url http://100.119.240.75:8000 &&
python3 tools/ingest_docs.py --source-dir training-ingest-src/training-curriculum-docs  --collection training-curriculum-docs  --extensions .json --key-file keys/training-website-internal.key --base-url http://100.119.240.75:8000 &&
python3 tools/ingest_docs.py --source-dir training-ingest-src/training-review-findings   --collection training-review-findings   --extensions .json --key-file keys/training-website-internal.key --base-url http://100.119.240.75:8000 &&
python3 tools/ingest_docs.py --source-dir training-ingest-src/training-internal-runbooks --collection training-internal-runbooks --extensions .md   --key-file keys/training-website-internal.key --base-url http://100.119.240.75:8000
'
```

The API key never leaves the server — it is read from a local file on the box that
also runs the gateway, and the SSH session only ever sends the `--key-file` *path*,
never the key itself.

## Known limitation: orphaned chunks

`ingest_docs.py` upserts by a stable `<relpath>::<chunk_index>` ID, so re-ingesting an
edited file safely overwrites its old chunks. But there is no delete endpoint on the
gateway: if a lesson file shrinks, is renamed, or is deleted (e.g. a track is retired
or a lesson is merged into another), its old chunk IDs are **not** removed from
Chroma and become stale orphans. If that happens, a gateway-side delete/reset endpoint
would be needed — this ingestion step alone cannot clean that up.

## Re-running after content changes

- New/edited lessons → re-stage + re-copy + re-ingest `training-lesson-content` only.
- New course or module → re-stage + re-copy + re-ingest `training-curriculum-docs` only.
- New review pass → re-stage + re-copy + re-ingest `training-review-findings` only.
- Runbook doc edits → re-stage + re-copy + re-ingest `training-internal-runbooks` only.

Each collection can be re-ingested independently; there's no need to redo all four
just because one changed.
