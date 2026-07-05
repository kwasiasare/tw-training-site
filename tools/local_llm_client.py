#!/usr/bin/env python3
"""
local_llm_client.py - Thin wrappers over the local LLM gateway's REST API,
for use by the course-authoring pipeline (generate_course.py, build_catalog.py,
review scripts, etc.) that runs offline/locally.

The gateway (Tailscale-only, reachable at http://100.119.240.75:8000 from any
device on the tailnet) exposes:

    POST /v1/generate     {"prompt": str, "tier": "standard"|"fast"}
                          -> {"app": str, "response": str}

    POST /v1/recommend    {"query": str, "collection": str, "k": int}
                          -> {"app": str, "answer": str,
                              "sources": [{"text": str, "metadata": dict,
                                           "distance": float}, ...]}

    POST /v1/classify     {"text": str, "instruction": str}
                          -> {"app": str, "result": ...}
                          (server always uses the fast tier for this endpoint,
                          regardless of what the caller passes elsewhere)

    GET  /v1/collections  -> {"app": str, "collections": [str, ...]}

This module follows the same stdlib-only convention as tools/ingest_docs.py in
the sibling Building_LLM project (urllib.request / urllib.error / json - no
requests, no httpx, no third-party HTTP client) so it can be dropped into any
of the authoring scripts with zero new dependencies.

Auth: the Bearer key is read from a local file (never passed as a literal
string, never taken from an env var default) and stripped of whitespace. The
key is never printed or logged, and error messages are redacted so a leaked
request/response detail can't leak the Authorization header.

Usage example
-------------
    from tools.local_llm_client import generate, recommend, classify, list_collections

    KEY_FILE = "tools/training_website.key"  # git-ignored; not committed

    # Free-form generation (standard tier = full 14B model, can be slow).
    text = generate(
        "Write a one-sentence summary of Python decorators.",
        tier="standard",
        key_file=KEY_FILE,
    )
    print(text)

    # Fast-tier generation for latency-sensitive calls.
    quick = generate("Say hello in one word.", tier="fast", key_file=KEY_FILE)

    # RAG-style recommendation against a Chroma collection.
    result = recommend(
        "What are common mistakes with Python decorators?",
        collection="training-lesson-content",
        k=5,
        key_file=KEY_FILE,
    )
    print(result["answer"])
    for src in result["sources"]:
        print(src["metadata"], src["distance"])

    # Fast-tier structured extraction.
    parsed = classify(
        "Lesson 4: Intro to Decorators (45 min, beginner)",
        instruction="Extract {title, duration_minutes, level} as JSON.",
        key_file=KEY_FILE,
    )
    print(parsed["result"])

    # Discover what collections exist (not required by callers above, but
    # handy for one-off exploration / debugging).
    print(list_collections(key_file=KEY_FILE))
"""

import json
import re
import urllib.error
import urllib.request

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

DEFAULT_BASE_URL = "http://100.119.240.75:8000"

# Relative to the current working directory (typically the repo root when
# authoring scripts are run via `python generate_course.py ...` from the repo
# root). Git-ignored - see .gitignore. Never commit the real key.
DEFAULT_KEY_FILE = "tools/training_website.key"

# generate/recommend hit the standard-tier (CPU-bound 14B model) path on the
# gateway, which can be slow - match the gateway's own standard-tier timeout.
GENERATE_TIMEOUT_SECS = 300
RECOMMEND_TIMEOUT_SECS = 300

# classify always runs on the fast tier server-side, so a much shorter
# timeout is appropriate.
CLASSIFY_TIMEOUT_SECS = 60
LIST_COLLECTIONS_TIMEOUT_SECS = 60


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def redact(text):
    """Strip anything that looks like a bearer token out of a string before
    it is ever printed. Defense in depth - the key should never reach this
    path, but if request/error details get surfaced, scrub them anyway."""
    if text is None:
        return text
    return re.sub(r"Bearer\s+\S+", "Bearer <redacted>", text)


def _load_api_key(key_file):
    """Read and whitespace-strip the API key from a local file. Raises a
    clear, redaction-safe error if the file is missing/unreadable/empty.
    The key is returned but is never printed or logged by this module."""
    try:
        with open(key_file, "r", encoding="utf-8") as f:
            raw = f.read()
    except OSError as e:
        raise LocalLLMClientError(
            f"Could not read key file '{key_file}': {type(e).__name__}: {redact(str(e))}"
        )
    key = raw.strip()
    if not key:
        raise LocalLLMClientError(f"Key file '{key_file}' is empty after stripping whitespace.")
    return key


class LocalLLMClientError(Exception):
    """Raised for any gateway/transport failure. Message is always
    redaction-safe (never contains the Authorization header or raw key)."""


# --------------------------------------------------------------------------
# Network core
# --------------------------------------------------------------------------

def _post_json(path, body, key_file, base_url, timeout):
    """POST a JSON body to base_url + path with Bearer auth, and return the
    parsed JSON response. Shared by generate()/recommend()/classify() to
    avoid duplicating urllib boilerplate.

    Raises LocalLLMClientError on any non-2xx response, connection failure,
    timeout, or malformed JSON response. Error messages are redacted so a
    leaked request/response detail can never include the Authorization header
    or raw key value.
    """
    api_key = _load_api_key(key_file)
    url = base_url.rstrip("/") + path
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        detail = _read_error_detail(e)
        raise LocalLLMClientError(f"{path} returned HTTP {e.code}: {detail}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise LocalLLMClientError(
            f"Request to {path} failed: {type(e).__name__}: {redact(str(e))}"
        )

    try:
        return json.loads(raw.decode("utf-8", errors="replace"))
    except json.JSONDecodeError as e:
        raise LocalLLMClientError(f"{path} returned invalid JSON: {e}")


def _get_json(path, key_file, base_url, timeout):
    """GET base_url + path with Bearer auth, and return the parsed JSON
    response. Same error-handling contract as _post_json()."""
    api_key = _load_api_key(key_file)
    url = base_url.rstrip("/") + path
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {api_key}")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        detail = _read_error_detail(e)
        raise LocalLLMClientError(f"{path} returned HTTP {e.code}: {detail}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise LocalLLMClientError(
            f"Request to {path} failed: {type(e).__name__}: {redact(str(e))}"
        )

    try:
        return json.loads(raw.decode("utf-8", errors="replace"))
    except json.JSONDecodeError as e:
        raise LocalLLMClientError(f"{path} returned invalid JSON: {e}")


def _read_error_detail(http_error):
    """Extract a redacted, length-capped body from an HTTPError for use in
    exception messages. Never includes request headers."""
    try:
        body = http_error.read()
        text = body.decode("utf-8", errors="replace")
    except Exception:
        text = str(http_error)
    text = redact(text)
    if len(text) > 500:
        text = text[:500] + "... (truncated)"
    return text


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def generate(prompt, tier="standard", key_file=DEFAULT_KEY_FILE, base_url=DEFAULT_BASE_URL):
    """Call POST /v1/generate and return just the response text (str).

    tier: "standard" (full model, slower - default) or "fast".
    key_file: path to a local file containing the raw Bearer key.
    Raises LocalLLMClientError on failure.
    """
    data = _post_json(
        "/v1/generate",
        {"prompt": prompt, "tier": tier},
        key_file,
        base_url,
        GENERATE_TIMEOUT_SECS,
    )
    return data["response"]


def recommend(query, collection, k=5, key_file=DEFAULT_KEY_FILE, base_url=DEFAULT_BASE_URL):
    """Call POST /v1/recommend and return the full parsed JSON dict, i.e.
    {"app": str, "answer": str, "sources": [{"text","metadata","distance"}, ...]}.

    Returning the full dict (rather than just "answer") because callers
    generally want the retrieved sources too, for citation/debugging.
    Raises LocalLLMClientError on failure.
    """
    return _post_json(
        "/v1/recommend",
        {"query": query, "collection": collection, "k": k},
        key_file,
        base_url,
        RECOMMEND_TIMEOUT_SECS,
    )


def classify(text, instruction, key_file=DEFAULT_KEY_FILE, base_url=DEFAULT_BASE_URL):
    """Call POST /v1/classify (server always uses the fast tier for this
    endpoint) and return the full parsed JSON dict, i.e.
    {"app": str, "result": ...}.

    Returning the full dict rather than just "result" so callers can inspect
    "app" if needed; "result" is typically what you want (data["result"]).
    Raises LocalLLMClientError on failure.
    """
    return _post_json(
        "/v1/classify",
        {"text": text, "instruction": instruction},
        key_file,
        base_url,
        CLASSIFY_TIMEOUT_SECS,
    )


def list_collections(key_file=DEFAULT_KEY_FILE, base_url=DEFAULT_BASE_URL):
    """Call GET /v1/collections and return the full parsed JSON dict, i.e.
    {"app": str, "collections": [str, ...]}. Not required by the ticket, but
    included for parity/debugging convenience.

    Raises LocalLLMClientError on failure.
    """
    return _get_json("/v1/collections", key_file, base_url, LIST_COLLECTIONS_TIMEOUT_SECS)
