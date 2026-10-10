# Student-Facing Course Chatbot + Help Tool — Plan

Status: **APPROVED AND SHIPPED (Phases 1 & 2).** Kwasi approved the scope
boundary (§1, Tier A only) and engine choice (§2, Claude) on 2026-07-05 (see
the approval comment on Jira epic TW-116). Phase 1 (TW-117, cross-course
course Q&A) and Phase 2 (TW-118, site-help/FAQ) are both implemented,
reviewed (Sonnet → Opus → five-persona review → Fable test pass → live
production verification), merged to `master`, and live in production at
`www.salloma.com` with the `PUBLIC_CHATBOT_ENABLED` feature flag on. Phase 2
shipped 2026-07-06, riding the same flag as Phase 1 (no new flag was needed —
it extends the existing Stage-1 classifier with a `site_help` status, grounded
in a new curated `api/src/shared/faq.json`, still zero live-data reads).

**Update 2026-10-09 (TW-140): Claude is now served from Microsoft Foundry,
and the local LLM is discontinued.** Direct `ANTHROPIC_API_KEY` calls returned
401 in production, so all Claude calls (chat, tutor, advisor, grader) go through
`api/src/shared/claudeClient.js`: Foundry (`@anthropic-ai/foundry-sdk`, resource
`kasare-5989-resource`) when `ANTHROPIC_FOUNDRY_RESOURCE` (or `_BASE_URL`) and
`ANTHROPIC_FOUNDRY_API_KEY` are set, else the direct API. Models are env-driven
(`CLAUDE_MODEL_SELECT` / `_ANSWER` / `_TUTOR`, defaulting to haiku-4-5 /
sonnet-5 / opus-4-8; on Foundry these are deployment names). The local-LLM
gateway and AWS Bedrock engine chain (TW-137) were removed; the two-stage
design, grounding rules, site_help FAQ path and off-topic decline are unchanged.
References below to the internal local LLM are historical.

One revision made during implementation planning: the model tier originally
recommended in this document (`claude-opus-4-8` throughout) was revised to a
two-stage routing — `claude-haiku-4-5` for intent classification/lesson
selection, `claude-sonnet-5` for the actual grounded answer — after a
cost review concluded neither sub-task requires Opus-tier reasoning (see §2
and §7 for the updated detail). This was exactly the cost-optimization
comparison flagged as a to-do in the original §2 text below; references to
`claude-opus-4-8` further in this document reflect the pre-revision proposal
and are kept for historical context.

Phase 3 (account/progress-aware help) remains unstarted and still requires
its own separate approval gate per §1 — it has not been requested or
approved.

---

## 0. Why this is a new trust boundary, not an incremental feature

Training-website already has three Claude-powered, student-facing surfaces, all
sharing one design pattern established under TW-61 and carried through
`tutor.js` (TW-67), `grader.js` (TW-68), and `advisor.js` (TW-64):

- Model: `claude-opus-4-8`, `output_config: { effort: 'low' }`, bounded
  `max_tokens`, lazy singleton Anthropic client.
- Auth-gated: every AI endpoint sits behind SWA + Entra External ID (CIAM) auth;
  each handler re-checks `x-ms-client-principal` in code (`shared/principal.js`)
  and returns **403, not 401** (401 would trigger SWA's global redirect to
  `/signin/` and break the fetch call).
- Server-side grounding only: the client can never supply the material the
  model reasons over. `tutor.js` looks up the lesson server-side from
  `lessons.generated.json`; `grader.js` looks up the reference answer the same
  way. This is explicitly called out in the tutor's own comments as the reason
  the endpoint "can't be used as a free, ungrounded Claude proxy."
  `advisor.js` is the one exception — it takes user-supplied content (a résumé
  PDF) — but treats it strictly as **data, never instructions**, in the system
  prompt.
- Prompt-injection guarding: all three system prompts explicitly instruct the
  model to treat lesson text / learner answers / résumé content as data, never
  as instructions that override the system prompt.

A course-wide chatbot inherits this same bar — it's still speaking with
authenticated students, on the public web, using the platform's name and
trust. It is **not** the same category as the internal tooling built this
session (`training-website-internal` on the Tailscale-only local LLM gateway,
TW-109 through TW-115): those tools are author-facing, never touch a student,
and run on a host that isn't reachable from the internet at all. Nothing
below reuses that internal box directly — see §2.

---

## 1. Scope boundary: course Q&A vs. general help vs. account/progress

This is the most consequential call in this document and needs Kwasi's
explicit sign-off before any code is written.

The corpus a chatbot could plausibly draw on splits into three tiers of very
different sensitivity:

| Tier | Example questions | Data touched | Sensitivity |
|---|---|---|---|
| **A. Course content** | "What's the difference between a token and an embedding?", "Which course covers Kubernetes?" | Public lesson content (`lessons.generated.json`), public catalog | Same as tutor.js today — public material, no student-specific data |
| **B. Site help / how-things-work** | "How do certificates work?", "How do I enroll?", "What does 'in progress' mean?" | Static FAQ-style knowledge, no live personal data | Low — same tier as A, just a different knowledge source |
| **C. Account/progress-aware help** | "What's my next lesson?", "Am I certified for the GenAI track?", "Why isn't my quiz score showing?" | Live Cosmos DB reads: `progress`, `enrollment`, `certificate`, `profile` docs, all keyed by `userId` | Materially higher — this is real per-student data flowing through a generative, conversational surface for the first time |

**Recommendation:** draw the line between B and C, not between A and B. Ship A
and B together as the initial chatbot (a single "ask about any course, or how
the site works" surface). Treat C as an explicitly separate, later-gated
phase (§7, Phase 3) — not because the individual Cosmos reads are risky (
`progress.js`/`profile.js` already expose this to the signed-in owner via
normal REST endpoints), but because once a generative model is the thing
composing the answer, you introduce new failure modes that don't exist in a
deterministic REST response: the model could misstate a student's own
progress, could be prompt-injected into requesting or fabricating data about
*other* students, or could blend account context into a course-content answer
in a way that's hard to test exhaustively. That's a genuinely different
review than "does this Claude call answer questions about lesson text
correctly."

**Do not blur this line at build time.** Phase 1/2 should be implementable
with zero new Cosmos read paths from the chatbot's code path — if an
implementer finds themselves reaching for `cosmos.js` from the chatbot
handler, that's a signal scope has crept into tier C without the separate
approval this doc calls for.

---

## 2. Engine choice: Claude vs. the internal local LLM

**Recommendation: Claude, not the internal local LLM (Ollama/Chroma on the
Tailscale-only box).** This is a clear recommendation, not a coin-flip —
three independent reasons all point the same way. (Which Claude model
tier to use is a separate, since-revised question — see the shipped-status
note at the top of this document and the update at the end of this section.)

1. **Reachability is a hard blocker, not a preference.** The local LLM
   gateway (`100.119.240.75:8000`) is Tailscale-only by design (that was the
   whole point of keeping the internal tooling internal). The public
   `salloma.com` site cannot call it directly. Making it reachable would mean
   standing up a new internet-facing proxy — its own auth, its own rate
   limiting, its own hardening, its own attack surface — *before* you've
   written a single line of chatbot logic. That's strictly more new
   infrastructure and more new risk than calling an API (Anthropic's) the
   codebase already calls successfully three times over, with an
   `ANTHROPIC_API_KEY` already provisioned in Functions app settings.
2. **Quality and latency don't clear the bar for an unsupervised
   student-facing surface.** The internal tools (`quiz_assistant.py`,
   `gap_checker.py`, `deck_tagger.py`) run against `qwen2.5:14b`/`qwen2.5:3b`
   on Ollama, and every one of them has a human course author reviewing the
   output before it reaches a student. A course-wide chatbot answers students
   directly, in real time, with no human in the loop. That's a higher bar,
   not a lower one, than the internal tools — the opposite of where a
   cheaper/slower/lower-quality model is an acceptable trade.
3. **One vendor, one trust story.** Tutor/grader/advisor already share one
   incident-response path, one abuse-monitoring surface, one ToS/vendor
   relationship. Splitting the platform's public AI surfaces across two
   different backends (Anthropic-hosted here, self-hosted there) doubles the
   operational and safety review surface for no real benefit — the local LLM
   isn't free in any way that matters once you count the proxy build-out in
   reason 1.

Cost is the one real argument for the local LLM, but cost is already managed
on the existing surfaces via `effort: 'low'` + bounded `max_tokens` + history
truncation, and §6 recommends the same pattern here plus rate limiting
(currently absent platform-wide). If usage volume ever makes Claude costs a
real problem, the right lever is tightening those bounds or evaluating a
cheaper Claude model tier for the high-volume/low-complexity "site help"
tier — not routing student-facing answers through a slower, lower-quality,
unreachable-without-new-infra backend.

**Update (2026-07-05, during implementation planning):** this exact
comparison was done for Phase 1 before Sonnet implemented it. Verdict: the
two sub-tasks in the two-stage pipeline (§5) have very different shapes —
classifying intent and picking 1-3 lesson IDs from a title list is a narrow
routing task, and answering from already-retrieved lesson text is
"synthesize from provided context," not open-ended reasoning. Neither is
Opus-shaped work. Shipped routing: `claude-haiku-4-5` (no `effort` param —
unsupported on Haiku) for Stage 1, `claude-sonnet-5` with `effort: 'low'`
for Stage 2. This roughly halves per-query cost versus all-Opus with no
observed quality loss, and off-topic/no-match questions never reach Stage 2
at all, keeping that traffic nearly free. Live-verified in production
(Jira TW-117).

---

## 3. Relationship to the existing tutor (`tutor.js`)

**Recommendation: run alongside tutor.js as a distinct, complementary
feature — do not replace it, and do not widen tutor.js's own scope.**

`tutor.js`'s single-lesson grounding is a deliberate, valuable design choice
(the code comments say so explicitly: stay within the scope of *this lesson*
and *this course*). That constraint is what makes the tutor's answers
reliably on-topic and cheap to ground (one lesson's ~8000 chars, not the
whole catalog). Diluting it to answer catalog-wide questions would make it
worse at the one job it does well.

The new chatbot fills a gap tutor.js structurally cannot: cross-course
questions ("which course teaches Kubernetes?", "what's the difference
between the ML Engineer and MLOps Engineer tracks?") and general site-help
questions that aren't about a specific lesson's material at all. Concretely:

- **Tutor.js stays**: per-lesson, inline, deep-dive on the current lesson's
  material. No change to its code, scope, or system prompt.
- **New chatbot**: catalog-wide, site-wide, reachable from any page via a
  floating widget (§4). Answers "which course / which lesson" questions and
  general how-the-site-works questions.
- **Overlap handling**: when a student asks the global chatbot a question
  that's actually about the lesson they're currently on, that's fine — the
  chatbot's retrieval step (§5) will surface that lesson's content same as
  any other. No special-casing needed at launch. A future enhancement (not
  in scope here) could have the widget pass the current lesson id as a hint
  so the chatbot can bias retrieval toward it, but that's an optimization,
  not a requirement.

---

## 4. UI/UX placement

**Recommendation: a global floating widget, added once to
`site/src/layouts/BaseLayout.astro`, present on every page.**

Grounding in the actual site structure: `BaseLayout.astro` is the single
layout every page (`index`, `courses/[course]`, `topics/[...id]`, `custom`,
`account`, `certificate`, `signin`, `admin`) already renders through, and it
already carries global `is:inline` scripts (the `progress.js` include, the
`/.auth/me` auth-state hydration script) — this is an established pattern for
"appears everywhere" functionality in this MPA (no client-side router, so
there's no other single insertion point that reaches every page). The natural
spot is right before `</body>`, after the existing `progress.js` include.

Why not the alternatives:
- **A dedicated help page** — adds a navigation click of friction for what's
  meant to be an ambient, always-available help feature; contradicts "help
  tool for the site" framing in the ask.
- **Per-lesson embedding only** (i.e., folding it into `Tutor.astro`) — fails
  the "any course" requirement outright, and re-blurs the tutor/chatbot
  separation from §3.

There is currently **no shared chat component** — `Tutor.astro` is the only
chat UI in the codebase, and it's a `<details>`-based inline panel scoped to
one lesson. Recommend factoring the reusable bits (message-bubble log,
textarea+send, Enter-to-send, 403→sign-in-link handling, `textContent`-only
rendering to avoid XSS) into a small shared script/component so both
`Tutor.astro` and the new global widget use the same tested interaction
pattern, rather than forking a second copy of that logic.

---

## 5. Grounding / data architecture

**Recommendation: no new vector database. Reuse the existing
`lessons.generated.json` bundle with a lightweight two-stage lookup —
metadata-only catalog first, full body text only for the lessons that
matter.**

Justification against the actual corpus size: `lessons.generated.json` is
**3.35 MB, 391 lessons across 12 course tracks**, already committed to the
repo and already bundled with every API deployment (the SWA managed-Functions
runtime can't see `course-materials/` at deploy time, which is exactly why
`build_lesson_index.py` exists to flatten it into this one JSON file that
ships with the API). That is a small corpus by any standard — small enough
that a new RAG/vector layer would be solving a problem this platform doesn't
have yet:

- **Stage 1 — catalog-level context.** Build (at the same `build_lesson_index.py`
  step, or a small sibling script) a compact index of just `{course, lessonId,
  title, objectives, summary}` for all 391 lessons — this is on the order of a
  few hundred bytes each, well under 200 KB total, cheap enough to include
  directly as system-prompt context (or to search over with plain
  string/keyword scoring server-side) so the model can identify which 1-3
  lessons are actually relevant to the student's question, or ask a
  clarifying question if the query is ambiguous across courses.
- **Stage 2 — targeted grounding.** Once 1-3 relevant lesson ids are
  identified, fetch those specific lessons' full `body` text server-side via
  the *exact same* `shared/lessons.js` → `getLesson(lessonId)` lookup
  `tutor.js` already uses, and answer grounded in that text. The client never
  supplies lesson content, preserving the same "can't be used as a free
  ungrounded proxy" property tutor.js already has.

This deliberately avoids standing up a new vector store reachable from the
public internet. It also deliberately does **not** reuse the internal
Tailscale-only Chroma collection `training-lesson-content` (4,349 chunks over
the same 391 lessons) — that collection lives on a box the public site
cannot reach, and bridging it would require the same new proxy-infra problem
called out in §2. The source corpus is identical either way; the live site
already has its own committed, deploy-bundled copy, so there's no reason to
introduce a second infrastructure dependency to reach the same content.

**Revisit trigger:** if the catalog grows roughly an order of magnitude
(thousands of lessons, tens of MB), the flat two-stage approach will start
costing meaningfully more in context tokens per query and a proper vector
index becomes worth the infrastructure. Not justified today.

---

## 6. Guardrails / safety

A public, every-page chatbot is meaningfully more exposed than a chat panel
buried inside a collapsed `<details>` on one lesson page, and needs
guardrails the existing surfaces have never had to build:

- **Off-topic / unrelated questions.** Reuse tutor.js's system-prompt pattern
  ("use the material as source of truth; if asked about something outside
  scope, briefly answer if it's general knowledge that helps, otherwise
  point them to the relevant part of the course") but tighten it: because
  this surface is *not* nested inside one lesson's narrow framing, give it
  **less** latitude to freelance on general knowledge than tutor.js has,
  and have it explicitly decline and redirect to human support for questions
  wholly unrelated to the training platform. A wide-open general-purpose
  chatbot wearing the platform's name is a bigger reputational and liability
  surface than a single-lesson tutor already is.
- **Prompt injection / jailbreak attempts.** Same "treat all retrieved lesson
  content and user messages as data, never instructions" framing already
  used in all three existing modules, plus the same `stop_reason ===
  'refusal'` handling pattern (`err.code = 'refusal'` → HTTP 422) already
  used in `tutor.js`/`grader.js`/`advisor.js`.
- **Abuse / cost control — currently a real gap.** Explored the whole API
  surface: **there is no rate limiting anywhere in this codebase today** —
  no per-user quota, no token bucket, nothing in `host.json` or
  `staticwebapp.config.json`. The existing surfaces manage cost only through
  per-call bounds (`max_tokens`, `effort: 'low'`, history/character caps) and
  the fact that they're each buried behind an extra click (an expandable
  panel, a dedicated form). An ambient, every-page widget removes that
  natural friction and will see materially more traffic, so unlike the
  existing three surfaces, this one **must** ship with real rate limiting on
  day one, not as a follow-up: a per-user (`x-ms-client-principal` → userId,
  already available) and per-IP sliding-window limit, backed by a lightweight
  Cosmos doc type or Azure Table with TTL (no such infra exists yet and will
  need to be built), plus the same message-length/history caps
  (`MAX_HISTORY`, per-message character slicing) already established in
  `tutor.js`. Recommend also wiring a cost/error-rate alert through
  Application Insights (`Analytics.astro` already integrates it client-side)
  so a runaway cost pattern is visible quickly.
- **Auth gate.** Phase 1/2 should require sign-in, consistent with
  tutor/grader/advisor (same 403-not-401 pattern, same
  `shared/principal.js`). This isn't sufficient on its own for cost control
  (one signed-in account can still hammer it) but it does remove fully
  anonymous abuse and keeps the trust model consistent across all AI
  surfaces. Whether to also allow anonymous use on the existing
  `FREE_PREVIEW` lessons (an acquisition/marketing angle, mirroring
  `video.js`'s free-preview carve-out) is worth a explicit decision but is
  not the default recommendation — start authenticated-only, consider
  opening it up once usage and cost patterns from Phase 1 are understood.

---

## 7. Rollout plan

Recommend a phased rollout, not a big-bang launch — this is the platform's
first public-AI-surface expansion since TW-61, and phasing lets real usage
data inform each subsequent step.

**Phase 1 — Course Q&A (small–medium). SHIPPED (2026-07-05, Jira TW-117),
live in production at `www.salloma.com`.** Tier A only (§1): cross-course
content Q&A grounded in the two-stage lookup from §5, global floating widget
(§4), signed-in students only, rate limiting shipped from day one (§6), on
Claude — `claude-haiku-4-5` for classification/lesson-selection,
`claude-sonnet-5` for the grounded answer (see the cost-revision note in §2;
the `claude-opus-4-8` reference here reflects the original pre-revision
proposal). Application Insights logging of query volume, refusal rate, and
rough topic distribution is live; use it to inform Phase 2 scope in detail.

**Phase 2 — Site help / FAQ (small–medium). SHIPPED (2026-07-06, Jira TW-118),
live in production at `www.salloma.com`.** Extended tier B (§1): non-personal
"how the site works" questions (enrollment, certificates, custom training,
support), grounded in a new curated FAQ knowledge source
(`api/src/shared/faq.json`, 18 entries) via a 5th Stage-1 classification
status (`site_help`) and a new whole-FAQ-grounded Stage 2
(`answerSiteHelpQuestion`) — still zero new Cosmos read paths. Personal-account
questions route here too and get a generic explanation + Account/support
redirect, never fabricated data. Rides the same `PUBLIC_CHATBOT_ENABLED` flag
as Phase 1.

**Phase 3 — Account/progress-aware help (medium–large, requires a fresh,
separate approval gate).** Tier C (§1): read-only access to the signed-in
student's *own* progress/enrollment/certificate data ("what's my next
lesson," "am I certified for X"), reusing the existing principal-scoped
Cosmos read patterns from `progress.js`/`profile.js`/`certificate.js`, never
cross-user. Do not begin this phase under the same approval as Phase 1/2 —
it's a materially different risk profile (§1) and deserves its own explicit
go-ahead and its own review, the same way the internal LLM platform's
app-registration step was held for separate approval this session.

---

## Recommended enrichment features (beyond the chatbot)

Six concrete additions, grounded in what actually exists in this codebase
today, prioritized over a longer undifferentiated list:

1. **Cross-course search/discovery** (small–medium). A catalog-wide search
   surfaced in the UI (the homepage already has a client-side lesson search
   per `index.astro`, but nothing catalog-wide with course context). Natural
   sequencing win: this can reuse the exact tier-A catalog-metadata index
   built for the chatbot's Stage 1 retrieval (§5), so it's cheapest to build
   right after Phase 1 ships. Small if client-side fuzzy search over the
   small metadata JSON; medium if it grows a server-side endpoint.

2. **Personalized "what's next" course recommendation** (medium). Extend
   `matcher.js`'s existing `targetProfile`-based matching (already built for
   the Custom Training Advisor, TW-64/66) to also run for a student who has
   completed a track: recommend the next logical course from their
   `progress`/`enrollment` Cosmos docs against the same `catalog.js`
   `targetProfile` data. No chatbot dependency — this can ship independently
   of everything above, and is a natural fit for `account.astro`'s existing
   dashboard.

3. **Progress dashboard enrichment** (small–medium). `account.astro` already
   shows enrolled courses and custom-training status; extend it with
   per-course completion percentage, quiz-score history, and
   certificates-in-progress, all from data `progress.js`/`certificate.js`
   already write to Cosmos. Pure read-side feature, no AI involved, low risk,
   no dependency on the chatbot work.

4. **Spaced-repetition quiz review** (medium). The quiz schema already
   carries reference answers per lesson (`{q, options, answer, why}`,
   consumed today by `grader.js`) — a periodic "review these 5 questions you
   missed or haven't seen in a while" feature could reuse this data directly.
   Needs one new Cosmos doc type to track per-question review intervals
   (a simple fixed-interval or SM-2-style schedule) and could be surfaced on
   `account.astro` or via the existing email pipeline (`shared/notify.js`
   already sends transactional email for the advisor flow).

5. **Certificate/badge expansion** (small). Certificates already exist
   per-course (TW-69, durable/permanent per the TW-98 decision) but there are
   no smaller-milestone badges ("first quiz passed," "5-lesson streak") to
   drive engagement between course completions. Mostly a UI + one new Cosmos
   doc-type feature; no AI dependency, no dependency on the chatbot work.

6. **Gap-checker-informed "recently updated" banner** (medium). This session
   already built `gap_checker.py` (TW-113, Done) as an internal, author-facing
   tool on the Tailscale-only LLM gateway that flags curriculum drift. Rather
   than making the public site call that internal box directly (the same
   proxy-infra problem as §2), the recommended integration is a periodic
   *export*: an internal script run manually or via CI writes a small
   committed JSON (same pattern as `catalog.generated.json`) listing lessons
   flagged as recently reviewed/updated, which the site consumes the same
   inert way it consumes `lessons.generated.json` today — no live proxy, no
   new security surface, and it reuses already-completed internal tooling
   work rather than leaving it siloed.

---

## Explicit approval gate

This document, and the accompanying Jira epic, propose the first expansion
of Training-website's public student-facing AI surface since TW-61. Per
Kwasi's standing workflow (mirroring how the internal LLM platform's
app-registration step, TW-111, was held for explicit approval before any
server-side registration happened), **no implementation work against this
plan should begin until Kwasi has explicitly signed off on**:

- §1 — the tier A/B/C scope boundary (specifically: agreeing Phase 1/2 stay
  out of live Cosmos/account data, and Phase 3 gets its own separate gate).
- §2 — the engine choice (Claude, not the internal local LLM).

Everything else in this document (UI placement, grounding architecture,
guardrails, phasing, enrichment features) is this session's recommendation
and open to adjustment, but those two decisions are the ones worth pausing
on before writing code.
