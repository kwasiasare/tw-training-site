# -*- coding: utf-8 -*-
"""Generate the Month 6 study pack: Apply Hard + Interview Prep.
Final month of the 6-month "Maths graduate to AI job" course.
Imports shared styling from doc_helpers (do NOT modify that module).
"""
from doc_helpers import (
    new_doc, title_block, h1, h2, h3, para, lead, bullet, numbered,
    code_block, callout, table_from_rows, quiz, page_break,
    NAVY, ACCENT, GREY, GREEN, AMBER, RED,
)

OUT = "Month_6_Apply_and_Interview_Study_Pack.docx"


def build():
    doc = new_doc()

    # ---------------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------------
    title_block(
        doc,
        "Month 6 - Apply Hard + Interview Prep",
        "From Maths Graduate to AI Job: The Landing Month",
        "6-Month AI Career Transition | Month 6 of 6 | ~30+ hrs/week | Study Pack",
    )

    lead(doc, "Where you are:",
         "You have finished Months 1-5: Python fundamentals, working with data, "
         "building LLM applications, two-to-three portfolio projects, and deployment "
         "plus personal branding. You can write Python, query a database, build a RAG "
         "pipeline, and ship something to a URL. You also bring a maths degree and an "
         "L1 support internship - both are genuine assets, not gaps to apologise for.")
    lead(doc, "What this month is:",
         "Not more building. This month is a focused, high-volume campaign to convert "
         "your skills and portfolio into interviews, and interviews into an offer. You "
         "apply in volume, prepare deliberately for each interview stage, and rehearse "
         "until your story and your answers are smooth.")
    callout(doc, "Mindset",
            "Job-hunting is a numbers game layered on a craft. Volume gets you "
            "interviews; preparation converts them. Track everything, treat every "
            "rejection as data, and keep your pipeline full so no single 'no' can sink "
            "your week.", color=ACCENT)

    # ---------------------------------------------------------------
    # LEARNING OBJECTIVES
    # ---------------------------------------------------------------
    h1(doc, "Learning objectives")
    para(doc, "By the end of Month 6 you will be able to:", color=GREY)
    objectives = [
        "Identify and target the 4-6 junior AI/LLM job titles that realistically match a "
        "maths-plus-support-plus-portfolio profile, and articulate the support->AI angle.",
        "Tailor a CV and application to a specific job description, pass basic ATS keyword "
        "screening, and write quantified, AI-flavoured CV bullets.",
        "Answer common AI/LLM concept questions (RAG vs fine-tuning, embeddings, hallucination "
        "control, evaluation, context windows, agents) with correct, concise model answers.",
        "Solve typical entry-level Python and SQL interview problems and explain your approach "
        "and complexity out loud.",
        "Sketch a system-design-lite answer for a RAG or support-assistant application, covering "
        "ingestion, retrieval, generation, evaluation and guardrails.",
        "Deliver structured behavioural answers using the STAR method and tell a coherent "
        "maths-to-support-to-AI narrative.",
        "Approach a take-home assignment strategically: scope it, ship a clean README, and avoid "
        "over-engineering.",
        "Evaluate an offer, negotiate professionally, and plan a credible first 30/60/90 days.",
        "Run a disciplined application campaign with a tracker, weekly targets, and follow-ups.",
        "Assemble a complete interview-readiness package as the capstone of the whole programme.",
    ]
    for o in objectives:
        bullet(doc, o)

    page_break(doc)

    # ===============================================================
    # TOPIC 1 - JOB-SEARCH STRATEGY & ROLE TARGETING
    # ===============================================================
    h1(doc, "1. Job-search strategy & role targeting")
    para(doc,
         "Most early-career job searches fail not because the candidate is unqualified, "
         "but because they aim at the wrong titles, apply too thinly, and give up after a "
         "small number of rejections. Before you send a single application, decide which "
         "roles you are actually a fit for and build a system to apply consistently.")

    h2(doc, "Which titles to target")
    para(doc,
         "The AI job market uses inconsistent titles. The same actual job may be advertised "
         "under several names. Your job is to recognise the roles where 'can build and ship a "
         "small LLM app' plus 'maths' plus 'customer-facing support' is genuinely competitive. "
         "Treat these as your primary targets:")
    targets = [
        ["Title", "What it really is", "Why you fit"],
        ["AI Engineer (Junior / Associate)",
         "Builds features on top of LLM APIs: prompts, RAG, evaluation, glue code.",
         "Your portfolio projects map almost directly onto this work."],
        ["AI Application Developer",
         "Software developer who specialises in LLM-powered product features.",
         "Python + deployment + an app you can demo."],
        ["LLM Engineer",
         "Focus on retrieval, prompting, eval, sometimes light fine-tuning/ops.",
         "RAG and evaluation experience from Months 3-4."],
        ["Forward-Deployed / Solutions Engineer",
         "Sits between product and customer; builds and configures for clients.",
         "Support background = customer empathy + technical build skills."],
        ["AI-focused Support / Support Engineer (AI products)",
         "L2/technical support for an AI product company; debugging, light scripting.",
         "Direct upgrade from your L1 internship - lowest-friction entry point."],
        ["Data / Analytics Engineer (AI-adjacent)",
         "SQL + Python pipelines feeding AI features.",
         "Maths + SQL + Python; a strong fallback lane."],
    ]
    table_from_rows(doc, targets[0], targets[1:])
    para(doc,
         "Secondary / stretch targets to apply to selectively but not depend on: ML Engineer, "
         "Machine Learning Engineer, Research Engineer, Data Scientist. These often demand more "
         "classical ML, deep-learning, or production-ops experience than a six-month transition "
         "provides. Apply if the JD reads 'applied' and product-focused; skip if it is heavy on "
         "training models from scratch, distributed training, or a PhD preference.", color=GREY)

    h2(doc, "Leaning on the support -> AI angle")
    para(doc,
         "Do not hide the support internship - lead with it as a differentiator. Companies "
         "building AI products are drowning in candidates who can write a prompt but have never "
         "spoken to a frustrated user, written a clear ticket, or escalated cleanly. You have. "
         "The forward-deployed, solutions-engineer, and AI-support lanes specifically reward this "
         "combination of customer skill and build ability.")
    para(doc, "Reframe each part of your background as an asset:")
    bullet(doc, "Maths degree -> comfort with probability, linear algebra and rigour; you "
                "understand embeddings, similarity, and why an LLM is a probabilistic system.")
    bullet(doc, "Support internship -> user empathy, written communication, debugging under "
                "pressure, calm with ambiguity, and real exposure to how software fails for users.")
    bullet(doc, "Self-taught coding + portfolio -> evidence of drive and the ability to learn "
                "fast, which is exactly what a junior hire is bought on.")

    h2(doc, "Building the application system")
    para(doc, "Treat applications as a weekly pipeline with explicit targets:")
    numbered(doc, "Set a weekly volume target (e.g. 15-25 tailored applications) and protect the time.")
    numbered(doc, "Split effort: ~70% well-matched roles, ~20% stretch roles, ~10% reach companies you love.")
    numbered(doc, "For every role, spend 15-25 minutes tailoring - not hours. Volume beats perfection early.")
    numbered(doc, "Warm applications (referral, recruiter, founder DM) convert far better than cold portals; "
                  "spend a fixed slice of time each week on outreach and your network.")
    numbered(doc, "Log every application in the tracker (see Project brief) and follow up after 7-10 days.")

    code_block(doc,
        "WEEKLY JOB-SEARCH CADENCE (example, ~12 focused hrs)\n"
        "------------------------------------------------------\n"
        "Mon  2h  Source + tailor 6 applications (well-matched lane)\n"
        "Tue  2h  Concept + Python interview practice\n"
        "Wed  2h  Source + tailor 6 applications + 3 networking touches\n"
        "Thu  2h  SQL + system-design-lite practice; 1 mock interview\n"
        "Fri  2h  Source + tailor 6 applications; send follow-ups due this week\n"
        "Sat  2h  Review tracker metrics; refine CV; rehearse STAR stories\n"
        "Target: ~18 applications/week, 1 mock/week, follow-ups every 7-10 days")

    callout(doc, "Common mistakes",
            "(1) Targeting only 'ML Engineer' or 'Data Scientist' and ignoring the AI-application "
            "and support-engineer lanes where you are most competitive. (2) Applying to 3 'dream' "
            "jobs a week and calling it a search - volume is the engine. (3) Hiding the support "
            "internship instead of selling it. (4) Relying only on cold portal applications and "
            "skipping referrals/outreach. (5) Quitting after 20-30 rejections; entry-level searches "
            "routinely need 100+ applications. (6) Not tracking anything, so you can't see what's "
            "working.", color=RED)

    quiz(doc, [
        {"q": "Which title is usually the LOWEST-friction entry point for someone with an L1 "
              "support internship moving into AI?",
         "options": ["ML Research Engineer", "AI-focused Support / Support Engineer at an AI "
                     "product company", "Senior Data Scientist", "Distributed Systems Engineer"],
         "answer": "B",
         "why": "It is a direct upgrade from L1 support and reuses your strongest existing experience."},
        {"q": "Roughly what split of effort across lanes is recommended?",
         "options": ["100% dream companies", "70% well-matched / 20% stretch / 10% reach",
                     "50% well-matched / 50% reach", "All stretch roles to aim high"],
         "answer": "B",
         "why": "Most volume should go where you convert; a small slice on stretch/reach keeps upside open."},
        {"q": "True/False: You should hide your support internship because it isn't an AI role.",
         "answer": "False",
         "why": "Customer empathy + written communication + debugging are exactly what forward-deployed, "
                "solutions, and AI-support roles reward; lead with it."},
        {"q": "Short answer: Name two AI-adjacent fallback lanes that suit a maths-plus-SQL profile.",
         "answer": "Data Engineer and Analytics Engineer (also Data Analyst in AI-product teams).",
         "why": "They lean on SQL + Python + maths and still sit close to AI features."},
        {"q": "Why is a 'warm' application generally better than a cold portal application?",
         "answer": "Referrals/recruiter/founder intros bypass the resume black hole and convert to "
                   "interviews at a much higher rate.",
         "why": "Cold portal apply rates are low; a human referral dramatically raises callback odds."},
        {"q": "True/False: Quitting after ~25 rejections is reasonable for an entry-level AI search.",
         "answer": "False",
         "why": "Entry-level searches often need 100+ applications; keep the pipeline full and treat "
                "rejections as data."},
    ], title="Topic 1 Quiz")

    page_break(doc)

    # ===============================================================
    # TOPIC 2 - TAILORING CVs, ATS, AI-FLAVOURED BULLETS
    # ===============================================================
    h1(doc, "2. Tailoring CVs & applications (ATS basics)")
    para(doc,
         "A CV has one job: get you to a human conversation. For junior roles it is usually "
         "first scanned by an Applicant Tracking System (ATS) and then skimmed by a recruiter for "
         "6-10 seconds. Optimise for both: machine-readable structure plus quantified, relevant bullets.")

    h2(doc, "ATS basics")
    para(doc, "ATS software parses your CV into fields and ranks it against the job description. "
              "To survive parsing and keyword matching:")
    bullet(doc, "Use a single-column, standard layout. Avoid tables, text boxes, columns, images, "
                "and headers/footers for key content - many parsers drop them.")
    bullet(doc, "Use standard section headings: Experience, Education, Skills, Projects.")
    bullet(doc, "Mirror the language of the job description. If it says 'RAG', 'vector database', "
                "'LLM evaluation', use those exact terms where they are true.")
    bullet(doc, "Submit as .docx or a text-based PDF (not a scanned/image PDF). Save with a clear "
                "filename like 'Firstname_Lastname_CV.pdf'.")
    bullet(doc, "Spell out an acronym once with the term, e.g. 'retrieval-augmented generation (RAG)', "
                "so both forms match.")
    callout(doc, "ATS reality check",
            "ATS keyword matching is real but blunt. Do not keyword-stuff or paste hidden white text - "
            "modern systems and recruiters catch it and it reads as dishonest. Match terms only where "
            "the claim is genuinely true.", color=AMBER)

    h2(doc, "Tailoring workflow (15-25 minutes per role)")
    numbered(doc, "Read the JD and highlight the 6-10 'must-have' keywords and responsibilities.")
    numbered(doc, "Reorder your Skills line so the matched tools appear first.")
    numbered(doc, "Pick the 2-3 most relevant projects/experiences and rewrite their top bullets to "
                  "mirror the JD's priorities.")
    numbered(doc, "Adjust the one-line professional summary to name the target role and 2-3 keywords.")
    numbered(doc, "Run a final pass: every bullet should be quantified or specific, no typos, one page.")

    h2(doc, "Writing AI-flavoured CV bullets")
    para(doc, "The strongest bullets follow Action verb + what you did + tools + quantified result. "
              "Weak bullets describe duties; strong bullets describe impact. Compare:")
    code_block(doc,
        "WEAK (duty, vague):\n"
        "  - Worked on a chatbot project using AI.\n"
        "  - Responsible for answering customer support tickets.\n\n"
        "STRONG (action + tools + quantified result):\n"
        "  - Built a retrieval-augmented (RAG) support assistant in Python using\n"
        "    OpenAI embeddings + a FAISS vector store, cutting answer-lookup time\n"
        "    in a 200-document test set from minutes to <2 seconds.\n"
        "  - Designed an LLM evaluation harness scoring 50 Q&A pairs on faithfulness\n"
        "    and relevance, raising answer accuracy from 71% to 89% after prompt\n"
        "    and retrieval tuning.\n"
        "  - Deployed a Streamlit LLM app to a public URL with API-key handling and\n"
        "    request logging; documented setup in a README used by 3 peer reviewers.\n"
        "  - Resolved ~30 L1 support tickets/week with a 95%+ CSAT, writing clear\n"
        "    reproduction steps that reduced back-and-forth escalations.")
    para(doc, "Notice the support bullet is quantified too - it is part of your story, not a footnote.")

    h2(doc, "A clean one-page structure")
    code_block(doc,
        "FIRSTNAME LASTNAME            City | email | github.com/you | linkedin.com/in/you\n"
        "------------------------------------------------------------------------------\n"
        "SUMMARY  (2 lines: target role + maths + support + 'builds & ships LLM apps')\n"
        "SKILLS   Python, SQL, RAG, LLM APIs, embeddings, vector DBs, Git, Streamlit/FastAPI\n"
        "PROJECTS (2-3, each with 2-3 quantified bullets + a live link / repo)\n"
        "EXPERIENCE (support internship, quantified bullets)\n"
        "EDUCATION (BSc Mathematics, classification, relevant modules)")

    callout(doc, "Common mistakes",
            "(1) One generic CV for every role. (2) Multi-column / table-heavy layouts that ATS "
            "mangle. (3) Duty bullets ('responsible for...') instead of quantified impact. (4) "
            "Keyword-stuffing or hidden white text. (5) Burying projects below a long skills dump. "
            "(6) Going over one page as a junior. (7) Claiming tools you can't discuss in an "
            "interview.", color=RED)

    quiz(doc, [
        {"q": "Why avoid multi-column, table-based CV layouts when an ATS is in play?",
         "answer": "Many ATS parsers read content in the wrong order or drop text in tables/columns, "
                   "so key information can be lost or garbled.",
         "why": "Single-column, standard-heading layouts parse most reliably."},
        {"q": "Which bullet is strongest?",
         "options": ["Worked on AI chatbots.",
                     "Responsible for the RAG system.",
                     "Built a RAG support assistant (Python, embeddings, FAISS) cutting lookup time "
                     "to <2s on a 200-doc set.",
                     "Familiar with several AI tools."],
         "answer": "C",
         "why": "It combines an action verb, the tools, and a quantified result."},
        {"q": "True/False: Pasting hidden white-text keywords is a smart way to beat the ATS.",
         "answer": "False",
         "why": "Modern ATS and recruiters detect it; it reads as dishonest and gets you rejected."},
        {"q": "Short answer: How should you handle the acronym RAG on a CV for ATS matching?",
         "answer": "Write it out once with the acronym, e.g. 'retrieval-augmented generation (RAG)', "
                   "so both the full term and the acronym match.",
         "why": "Different JDs use different forms; spelling it once covers both."},
        {"q": "Roughly how long should tailoring a CV to one role take in a high-volume campaign?",
         "options": ["A few hours", "15-25 minutes", "30 seconds", "A full day"],
         "answer": "B",
         "why": "Enough to mirror the JD's keywords and reorder projects, without killing your volume."},
        {"q": "Short answer: What is the recommended CV length for a junior candidate?",
         "answer": "One page.",
         "why": "Recruiters skim juniors quickly; one focused page outperforms two padded ones."},
    ], title="Topic 2 Quiz")

    page_break(doc)

    # ===============================================================
    # TOPIC 3 - AI/LLM CONCEPT INTERVIEW QUESTIONS
    # ===============================================================
    h1(doc, "3. AI/LLM concept interview questions (with model answers)")
    para(doc,
         "Concept rounds test whether you understand the systems you build, not just whether you "
         "can wire libraries together. Aim for answers that are correct, concise (45-90 seconds "
         "spoken), and show you know the trade-offs. Below are the highest-frequency topics with "
         "model answers.")

    h3(doc, "RAG vs fine-tuning")
    para(doc,
         "RAG (retrieval-augmented generation) injects relevant external text into the prompt at "
         "query time, so the model answers from retrieved context. Fine-tuning updates the model's "
         "weights on example data to change its behaviour or style. Use RAG when the knowledge is "
         "large, changes often, or must be cited/traceable - it is cheaper to update (re-index, no "
         "retraining) and reduces hallucination by grounding answers. Use fine-tuning to teach a "
         "consistent format, tone, or task behaviour the base model is weak at, or to bake in stable "
         "domain skills. They are complementary: you can fine-tune for format and use RAG for facts.")

    h3(doc, "Embeddings")
    para(doc,
         "An embedding is a fixed-length vector that represents the meaning of a piece of text, so "
         "that semantically similar texts sit close together in vector space. We measure closeness "
         "with cosine similarity. In RAG we embed each document chunk, store the vectors in a vector "
         "database, embed the user's query, and retrieve the nearest chunks. Embeddings power "
         "semantic search (matching meaning, not just keywords), clustering, and deduplication.")

    h3(doc, "Hallucination and how to control it")
    para(doc,
         "A hallucination is fluent, confident output that is factually wrong or unsupported - it "
         "happens because an LLM predicts likely tokens, not verified truth. Controls: (1) ground "
         "with RAG and instruct the model to answer only from provided context; (2) tell it to say "
         "'I don't know' when context is insufficient; (3) lower temperature for factual tasks; (4) "
         "ask for citations/quotes and verify them; (5) constrain with structured output / schemas; "
         "(6) add an evaluation or self-check step. You reduce hallucination; you cannot fully eliminate it.")

    h3(doc, "Evaluation")
    para(doc,
         "Because outputs are open-ended, you need an eval harness, not just eyeballing. Build a "
         "fixed test set of inputs with expected behaviour, then score with a mix of: exact/structured "
         "checks where possible; reference-based metrics; and 'LLM-as-judge' for qualities like "
         "faithfulness (is the answer supported by the retrieved context?), relevance, and "
         "correctness. For RAG specifically, evaluate retrieval (did we fetch the right chunks?) "
         "separately from generation. Track metrics over time so prompt or model changes are measured, not guessed.")

    h3(doc, "Context windows")
    para(doc,
         "The context window is the maximum number of tokens (prompt + output) a model can handle at "
         "once. A token is roughly 3-4 characters / about 0.75 words in English. Implications: long "
         "documents must be chunked and retrieved rather than pasted wholesale; cost and latency grow "
         "with tokens used; and very long contexts suffer 'lost in the middle' - models attend best to "
         "the start and end. RAG exists partly to put only the most relevant tokens into a finite window.")

    h3(doc, "Agents")
    para(doc,
         "An LLM agent uses the model to decide and act in a loop: it can call tools (search, a "
         "calculator, an API, code execution), observe the results, and iterate toward a goal, rather "
         "than producing a single response. Useful for multi-step tasks needing live data or actions. "
         "Trade-offs: more capable but slower, costlier, harder to make reliable, and they can loop or "
         "go off-track - so add step limits, guardrails, and observability. For many problems a single "
         "well-grounded RAG call is simpler and more reliable than an agent.")

    code_block(doc,
        "ONE-LINE SOUNDBITES (memorise these openers, then expand)\n"
        "---------------------------------------------------------\n"
        "RAG vs fine-tune : 'RAG changes what the model KNOWS; fine-tuning changes\n"
        "                    how it BEHAVES.'\n"
        "Embedding        : 'A vector capturing meaning; similar text -> nearby vectors.'\n"
        "Hallucination    : 'Confident output not grounded in fact; ground with RAG +\n"
        "                    let it say I-dont-know + cite sources.'\n"
        "Evaluation       : 'Fixed test set + faithfulness/relevance scoring; measure,\n"
        "                    dont eyeball.'\n"
        "Context window   : 'Token budget for prompt+output; chunk & retrieve, mind\n"
        "                    cost and lost-in-the-middle.'\n"
        "Agent            : 'LLM in a loop calling tools toward a goal; powerful but add\n"
        "                    limits and guardrails.'")

    callout(doc, "Common mistakes",
            "(1) Saying fine-tuning 'adds knowledge' as the default fix - for changing facts, RAG is "
            "usually the right tool. (2) Confusing embeddings (meaning vectors) with tokens (text "
            "units). (3) Claiming you can 'eliminate' hallucination. (4) Saying you evaluate 'by "
            "reading the outputs' with no harness. (5) Treating a bigger context window as a free "
            "substitute for retrieval. (6) Reaching for an agent when a single RAG call would be more "
            "reliable.", color=RED)

    quiz(doc, [
        {"q": "Your support docs change weekly and answers must be traceable to a source. RAG or "
              "fine-tuning, and why?",
         "answer": "RAG - it grounds answers in retrievable, citable context and updates by re-indexing "
                   "with no retraining; fine-tuning bakes facts into weights and is costly to refresh.",
         "why": "RAG fits frequently-changing, source-attributable knowledge."},
        {"q": "What does cosine similarity between two embeddings measure?",
         "options": ["The token count difference", "How semantically similar the two texts are",
                     "The model's temperature", "The size of the context window"],
         "answer": "B",
         "why": "Embeddings place similar meanings close together; cosine similarity quantifies that closeness."},
        {"q": "Name three concrete techniques to reduce hallucination in a RAG app.",
         "answer": "Any three of: ground in retrieved context and answer only from it; allow 'I don't know'; "
                   "lower temperature; require citations and verify them; constrain to structured output; "
                   "add an eval/self-check step.",
         "why": "These ground or constrain the model rather than relying on its priors."},
        {"q": "True/False: A token is exactly one word.",
         "answer": "False",
         "why": "A token is a sub-word unit, roughly 3-4 characters / ~0.75 words in English."},
        {"q": "In RAG evaluation, why separate retrieval metrics from generation metrics?",
         "answer": "So you know whether a bad answer came from fetching the wrong chunks (retrieval) or "
                   "from poor use of correct chunks (generation), which need different fixes.",
         "why": "Separating them localises the failure and tells you what to improve."},
        {"q": "When is an agent the WRONG choice?",
         "options": ["When the task is a single grounded lookup answerable by one RAG call",
                     "When the task needs many tool calls and live data",
                     "When you need iterative reasoning with actions",
                     "When you need to call external APIs in a loop"],
         "answer": "A",
         "why": "Agents add latency, cost and reliability risk; a single RAG call is simpler when it suffices."},
        {"q": "Short answer: What is 'lost in the middle'?",
         "answer": "The tendency of LLMs to attend less well to information placed in the middle of a very "
                   "long context than to the start or end.",
         "why": "It is a reason to retrieve and place only the most relevant chunks, not dump everything."},
    ], title="Topic 3 Quiz")

    page_break(doc)

    # ===============================================================
    # TOPIC 4 - PYTHON CODING INTERVIEW PRACTICE
    # ===============================================================
    h1(doc, "4. Python coding interview practice")
    para(doc,
         "Entry-level AI/application roles rarely ask hard competitive-programming puzzles. They ask "
         "clean, correct solutions to practical problems, and they listen to how you think: clarify "
         "the question, state your approach, code it, test on an example, and mention time/space "
         "complexity. Practise talking while you code. Below are worked problems; the answer key holds "
         "full solutions.")

    para(doc, "Work each problem yourself first, then check the answer key for a worked solution and "
              "complexity analysis.", italic=True, color=GREY)

    code_block(doc,
        "P1. Count word frequencies\n"
        "    Given a string of text, return a dict of word -> count, case-insensitive,\n"
        "    ignoring surrounding punctuation. Then return the top-k most common words.\n\n"
        "P2. Two-sum\n"
        "    Given a list of integers and a target, return the indices of the two numbers\n"
        "    that add up to target. Assume exactly one solution. Aim for O(n).\n\n"
        "P3. Chunk a list\n"
        "    Write chunk(lst, n) that splits a list into consecutive sub-lists of size n\n"
        "    (last chunk may be shorter). Relevant: chunking documents for RAG.\n\n"
        "P4. Group anagrams\n"
        "    Given a list of strings, group the anagrams together.\n\n"
        "P5. Cosine similarity (no numpy)\n"
        "    Given two equal-length lists of floats, compute their cosine similarity.\n"
        "    Relevant: comparing embeddings.\n\n"
        "P6. Flatten nested JSON-ish dict\n"
        "    Flatten a nested dict into dot-keyed pairs, e.g. {'a':{'b':1}} -> {'a.b':1}.")

    callout(doc, "Common mistakes",
            "(1) Coding in silence - interviewers score your communication. (2) Jumping to code before "
            "clarifying inputs, edge cases and expected output. (3) Ignoring empty/None/duplicate inputs. "
            "(4) Not stating time/space complexity. (5) Reinventing what the standard library already does "
            "(collections.Counter, defaultdict, sorted with key). (6) Never testing on a concrete example "
            "before declaring done.", color=RED)

    quiz(doc, [
        {"q": "P1 - Word frequencies + top-k. Provide a working solution and its complexity.",
         "answer":
            "from collections import Counter\n"
            "import re\n"
            "def word_freq(text):\n"
            "    words = re.findall(r\"[a-z0-9']+\", text.lower())\n"
            "    return Counter(words)\n"
            "def top_k(text, k):\n"
            "    return word_freq(text).most_common(k)\n"
            "# re.findall extracts word tokens and drops surrounding punctuation.\n"
            "# Counter.most_common(k) returns the k highest counts.\n"
            "# Time O(n) to build counts; most_common(k) is O(n log k). Space O(u) for u unique words.",
         "why": "Use the standard library (Counter); normalise case and strip punctuation with a regex."},
        {"q": "P2 - Two-sum in O(n). Provide a solution.",
         "answer":
            "def two_sum(nums, target):\n"
            "    seen = {}                       # value -> index\n"
            "    for i, x in enumerate(nums):\n"
            "        need = target - x\n"
            "        if need in seen:\n"
            "            return [seen[need], i]\n"
            "        seen[x] = i\n"
            "    return None\n"
            "# Single pass with a hash map. Time O(n), space O(n).\n"
            "# The naive double loop is O(n^2) - mention you rejected it for the hash-map approach.",
         "why": "A hash map of value->index lets you check the complement in O(1) per element."},
        {"q": "P3 - chunk(lst, n). Provide a solution and a RAG-relevant note.",
         "answer":
            "def chunk(lst, n):\n"
            "    if n <= 0:\n"
            "        raise ValueError('n must be positive')\n"
            "    return [lst[i:i+n] for i in range(0, len(lst), n)]\n"
            "# chunk([1,2,3,4,5], 2) -> [[1,2],[3,4],[5]]\n"
            "# Time O(len(lst)), space O(len(lst)). Same idea splits document tokens into\n"
            "# overlapping windows for RAG (add a stride < n for overlap).",
         "why": "Slicing with a step over range(0, len, n) is the idiomatic chunker; guard n<=0."},
        {"q": "P4 - Group anagrams. Provide a solution.",
         "answer":
            "from collections import defaultdict\n"
            "def group_anagrams(words):\n"
            "    groups = defaultdict(list)\n"
            "    for w in words:\n"
            "        key = ''.join(sorted(w))   # anagrams share a sorted-letter key\n"
            "        groups[key].append(w)\n"
            "    return list(groups.values())\n"
            "# group_anagrams(['eat','tea','tan','ate','nat']) ->\n"
            "#   [['eat','tea','ate'], ['tan','nat']]\n"
            "# Time O(m * k log k) for m words of length up to k. Space O(m*k).",
         "why": "Sorted letters form a canonical key so anagrams collide in the same bucket."},
        {"q": "P5 - Cosine similarity without numpy. Provide a solution.",
         "answer":
            "import math\n"
            "def cosine(a, b):\n"
            "    if len(a) != len(b):\n"
            "        raise ValueError('vectors must be equal length')\n"
            "    dot = sum(x*y for x, y in zip(a, b))\n"
            "    na = math.sqrt(sum(x*x for x in a))\n"
            "    nb = math.sqrt(sum(y*y for y in b))\n"
            "    if na == 0 or nb == 0:\n"
            "        return 0.0                 # undefined for a zero vector; return 0 by convention\n"
            "    return dot / (na * nb)\n"
            "# cosine([1,0,1],[1,0,1]) == 1.0. Time O(n), space O(1).",
         "why": "Cosine = dot product / (||a|| * ||b||); guard length mismatch and zero vectors."},
        {"q": "P6 - Flatten a nested dict to dot keys. Provide a solution.",
         "answer":
            "def flatten(d, parent='', sep='.'):\n"
            "    out = {}\n"
            "    for k, v in d.items():\n"
            "        key = f'{parent}{sep}{k}' if parent else k\n"
            "        if isinstance(v, dict):\n"
            "            out.update(flatten(v, key, sep))\n"
            "        else:\n"
            "            out[key] = v\n"
            "    return out\n"
            "# flatten({'a': {'b': 1, 'c': {'d': 2}}}) -> {'a.b': 1, 'a.c.d': 2}\n"
            "# Recursion over nested dicts. Time O(total keys), space O(depth) on the call stack.",
         "why": "Recurse into dict values, accumulating a dotted prefix; base case writes the leaf."},
    ], title="Topic 4 - Python Practice Problems (worked solutions in key)")

    page_break(doc)

    # ===============================================================
    # TOPIC 5 - SQL INTERVIEW PRACTICE
    # ===============================================================
    h1(doc, "5. SQL interview practice")
    para(doc,
         "SQL is one of the most common screening filters for data-adjacent and AI-application roles, "
         "and it plays to your maths strengths. Interviewers look for correct joins, aggregation with "
         "GROUP BY / HAVING, and (for mid questions) window functions. Practise reading a schema and "
         "writing a query out loud. Assume this schema for the problems below:")
    code_block(doc,
        "SCHEMA\n"
        "------\n"
        "customers(id, name, country, signup_date)\n"
        "orders(id, customer_id, order_date, amount)\n"
        "tickets(id, customer_id, created_at, status, priority)   -- support tickets")
    para(doc, "Work each query yourself, then check the answer key for a worked solution and notes.",
         italic=True, color=GREY)
    code_block(doc,
        "S1. Total revenue per country, highest first.\n"
        "S2. Customers who have NEVER placed an order.\n"
        "S3. Top 3 customers by total spend.\n"
        "S4. Monthly order count and revenue for 2025.\n"
        "S5. Each customer's most recent order (one row per customer).\n"
        "S6. Customers with an open support ticket AND at least one order over 100.")

    callout(doc, "Common mistakes",
            "(1) Using WHERE to filter an aggregate instead of HAVING. (2) Forgetting that COUNT(col) "
            "skips NULLs while COUNT(*) doesn't. (3) Using INNER JOIN when you need a LEFT JOIN to keep "
            "non-matching rows (e.g. customers with no orders). (4) Putting non-aggregated columns in "
            "SELECT that aren't in GROUP BY. (5) Reaching for a subquery when a window function (e.g. "
            "ROW_NUMBER) is cleaner. (6) Forgetting to handle ties in 'top N'.", color=RED)

    quiz(doc, [
        {"q": "S1 - Total revenue per country, highest first. Write the query.",
         "answer":
            "SELECT c.country, SUM(o.amount) AS revenue\n"
            "FROM customers c\n"
            "JOIN orders o ON o.customer_id = c.id\n"
            "GROUP BY c.country\n"
            "ORDER BY revenue DESC;\n"
            "-- Join orders to their customer, aggregate by country, sort descending.",
         "why": "Aggregate SUM grouped by country; ORDER BY the alias descending."},
        {"q": "S2 - Customers who have NEVER placed an order. Write the query.",
         "answer":
            "SELECT c.id, c.name\n"
            "FROM customers c\n"
            "LEFT JOIN orders o ON o.customer_id = c.id\n"
            "WHERE o.id IS NULL;\n"
            "-- LEFT JOIN keeps all customers; rows with no matching order have NULL order columns.\n"
            "-- Equivalent: WHERE c.id NOT IN (SELECT customer_id FROM orders) -- beware NULLs in NOT IN.",
         "why": "LEFT JOIN + 'IS NULL on the right table' is the canonical anti-join."},
        {"q": "S3 - Top 3 customers by total spend. Write the query.",
         "answer":
            "SELECT c.id, c.name, SUM(o.amount) AS total_spend\n"
            "FROM customers c\n"
            "JOIN orders o ON o.customer_id = c.id\n"
            "GROUP BY c.id, c.name\n"
            "ORDER BY total_spend DESC\n"
            "LIMIT 3;\n"
            "-- For tie-safe results use RANK() OVER (ORDER BY SUM(...) DESC) and keep rank <= 3.",
         "why": "Group + sum + order desc + LIMIT; mention RANK() if ties must be kept."},
        {"q": "S4 - Monthly order count and revenue for 2025. Write the query (standard SQL).",
         "answer":
            "SELECT DATE_TRUNC('month', order_date) AS month,\n"
            "       COUNT(*) AS order_count,\n"
            "       SUM(amount) AS revenue\n"
            "FROM orders\n"
            "WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'\n"
            "GROUP BY DATE_TRUNC('month', order_date)\n"
            "ORDER BY month;\n"
            "-- Filter the year with a half-open range (sargable, index-friendly).\n"
            "-- MySQL alternative: GROUP BY DATE_FORMAT(order_date,'%Y-%m').",
         "why": "Truncate to month, count and sum, and use a half-open date range for the year."},
        {"q": "S5 - Each customer's most recent order, one row per customer. Write the query.",
         "answer":
            "SELECT id, customer_id, order_date, amount\n"
            "FROM (\n"
            "  SELECT o.*,\n"
            "         ROW_NUMBER() OVER (PARTITION BY customer_id\n"
            "                            ORDER BY order_date DESC, id DESC) AS rn\n"
            "  FROM orders o\n"
            ") t\n"
            "WHERE rn = 1;\n"
            "-- ROW_NUMBER partitions by customer and ranks orders newest-first; rn=1 is the latest.\n"
            "-- The id DESC tiebreaker makes the result deterministic when dates tie.",
         "why": "ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) then filter rn = 1 is the standard 'latest per group'."},
        {"q": "S6 - Customers with an OPEN ticket AND at least one order over 100. Write the query.",
         "answer":
            "SELECT DISTINCT c.id, c.name\n"
            "FROM customers c\n"
            "JOIN tickets t ON t.customer_id = c.id AND t.status = 'open'\n"
            "JOIN orders  o ON o.customer_id = c.id AND o.amount > 100;\n"
            "-- Two joins enforce both conditions; DISTINCT collapses duplicate rows from the fan-out.\n"
            "-- Or use EXISTS subqueries to avoid the join fan-out entirely.",
         "why": "Join both conditions and DISTINCT, or two EXISTS subqueries; both express the AND."},
    ], title="Topic 5 - SQL Practice Problems (worked solutions in key)")

    page_break(doc)

    # ===============================================================
    # TOPIC 6 - SYSTEM-DESIGN-LITE FOR LLM APPS
    # ===============================================================
    h1(doc, "6. System-design-lite for LLM apps")
    para(doc,
         "For junior AI roles you won't be asked to design a planet-scale system, but you may be asked "
         "'How would you build a support assistant over our docs?' They are checking whether you can "
         "reason about an end-to-end LLM system and name the trade-offs. Use a repeatable structure: "
         "clarify -> sketch the pipeline -> name the components -> discuss evaluation & guardrails -> "
         "mention scaling and cost.")

    h2(doc, "A reusable answer structure")
    numbered(doc, "Clarify requirements: who are the users, what corpus, what latency/accuracy bar, "
                  "any privacy or compliance constraints, expected volume?")
    numbered(doc, "Draw the RAG pipeline at a high level (ingestion path + query path).")
    numbered(doc, "Name each component and the key decision in it.")
    numbered(doc, "Explain evaluation: how you'd measure retrieval and answer quality.")
    numbered(doc, "Cover guardrails, failure modes, monitoring, cost and scaling.")

    h2(doc, "Worked example: design a support assistant over company docs")
    code_block(doc,
        "RAG SUPPORT-ASSISTANT ARCHITECTURE\n"
        "==================================\n\n"
        "INGESTION (offline, batch / on doc update)\n"
        "  docs/tickets/FAQ\n"
        "     -> clean & parse (strip HTML, dedupe)\n"
        "     -> chunk (e.g. ~500 tokens, ~10-15% overlap, keep section metadata)\n"
        "     -> embed each chunk (embedding model)\n"
        "     -> upsert into VECTOR DB (id, vector, text, source, url, updated_at)\n\n"
        "QUERY (online, per user question)\n"
        "  user question\n"
        "     -> embed query\n"
        "     -> vector search: top-k similar chunks (optionally + keyword/BM25 = hybrid)\n"
        "     -> (optional) re-rank top-k for precision\n"
        "     -> build prompt: system rules + retrieved context + question\n"
        "     -> LLM generates grounded answer WITH source citations\n"
        "     -> post-process: guardrail checks, format, attach source links\n"
        "     -> return answer; log query, chunks, answer, latency, feedback\n\n"
        "CROSS-CUTTING\n"
        "  Eval harness   : retrieval hit-rate + faithfulness/relevance (LLM-as-judge)\n"
        "  Guardrails     : answer only from context; 'I don't know' fallback; PII/abuse filter\n"
        "  Caching        : cache embeddings and frequent Q&A to cut cost/latency\n"
        "  Monitoring     : log everything; track cost, latency, thumbs-up rate, refusals\n"
        "  Human handoff  : low-confidence or no-context -> escalate to a human agent")

    para(doc, "Key decisions you should be ready to justify: chunk size and overlap (too small loses "
              "context, too large dilutes relevance and costs more tokens); top-k (more recall vs more "
              "noise/cost); hybrid search vs pure vector (keyword helps exact IDs/error codes); whether "
              "a re-ranker is worth the latency; and where the human-in-the-loop handoff lives - a point "
              "your support background lets you speak to credibly.")

    callout(doc, "Common mistakes",
            "(1) Jumping into components without clarifying requirements. (2) Forgetting the offline "
            "ingestion/indexing path and only describing query time. (3) No evaluation story. (4) No "
            "guardrails or 'I don't know' fallback. (5) Ignoring cost, latency and monitoring. (6) "
            "Over-engineering with agents/fine-tuning when plain RAG meets the bar. (7) No human-handoff "
            "path for a support product.", color=RED)

    quiz(doc, [
        {"q": "What should be the FIRST thing you do in a system-design-lite answer?",
         "options": ["Pick a vector database", "Clarify requirements (users, corpus, latency, "
                     "accuracy, privacy, volume)", "Start writing the prompt", "Choose the LLM"],
         "answer": "B",
         "why": "Clarifying requirements scopes the design and shows senior-style thinking."},
        {"q": "Name the two main paths of a RAG system and what each does.",
         "answer": "Ingestion (offline): clean, chunk, embed and index documents into the vector store. "
                   "Query (online): embed the question, retrieve top-k chunks, build the prompt, generate "
                   "a grounded answer.",
         "why": "Forgetting the offline indexing path is a classic gap."},
        {"q": "Why might you add keyword/BM25 search alongside vector search (hybrid)?",
         "answer": "Pure semantic search can miss exact tokens like error codes, product IDs or SKUs; "
                   "keyword search catches exact matches, so hybrid improves recall on those.",
         "why": "Vectors capture meaning but can miss precise literal strings."},
        {"q": "True/False: Bigger chunks are always better because they keep more context.",
         "answer": "False",
         "why": "Large chunks dilute relevance, add noise and cost more tokens; size is a trade-off "
                "tuned against retrieval quality."},
        {"q": "Short answer: For a support assistant, what failure-handling path should you include?",
         "answer": "A low-confidence / no-relevant-context fallback that says 'I don't know' and escalates "
                   "to a human agent, plus logging for review.",
         "why": "Graceful degradation and human handoff are essential for a support product."},
        {"q": "What two things should you log per query to support evaluation and monitoring?",
         "answer": "Any two of: the query, the retrieved chunks/sources, the final answer, latency, cost/"
                   "tokens, and user feedback (thumbs up/down).",
         "why": "Logging the query+retrieval+answer lets you debug failures and measure quality over time."},
    ], title="Topic 6 Quiz")

    page_break(doc)

    # ===============================================================
    # TOPIC 7 - BEHAVIOURAL INTERVIEWS (STAR) + NARRATIVE
    # ===============================================================
    h1(doc, "7. Behavioural interviews (STAR) & your narrative")
    para(doc,
         "Behavioural rounds predict how you'll actually work: how you handle conflict, failure, "
         "ambiguity, and learning. The reliable framework is STAR - Situation, Task, Action, Result. "
         "Prepare 6-8 stories from your support internship, projects, and degree that you can flex to "
         "answer most behavioural questions.")

    h2(doc, "The STAR method")
    bullet(doc, "Situation - briefly set the context (1-2 sentences). Where, when, what was happening.")
    bullet(doc, "Task - what was your specific responsibility or the problem you owned.")
    bullet(doc, "Action - what YOU did, step by step (use 'I', not 'we'); this is the bulk of the answer.")
    bullet(doc, "Result - the outcome, quantified if possible, plus what you learned.")

    h2(doc, "STAR answer template + worked example")
    code_block(doc,
        "STAR TEMPLATE\n"
        "-------------\n"
        "S: \"In my support internship, ...\"            (1-2 sentences of context)\n"
        "T: \"I was responsible for ...\"                (your specific task)\n"
        "A: \"So I first ... then ... and I also ...\"   (YOUR concrete actions)\n"
        "R: \"As a result ... and I learned ...\"        (quantified outcome + lesson)\n\n"
        "WORKED EXAMPLE - 'Tell me about a difficult customer/problem.'\n"
        "S: During my L1 support internship, a customer escalated angrily because a\n"
        "   billing error had locked them out of the product for two days.\n"
        "T: I owned the ticket and needed to resolve it and rebuild trust, without the\n"
        "   authority to issue refunds myself.\n"
        "A: I acknowledged the impact and apologised, reproduced the issue to confirm the\n"
        "   root cause, wrote clear reproduction steps, and escalated to billing with a\n"
        "   concise summary so they could act fast. I kept the customer updated every few\n"
        "   hours rather than going silent.\n"
        "R: The lockout was fixed within the day, the customer stayed on, and my\n"
        "   reproduction template was reused by the team. I learned that calm, frequent\n"
        "   communication often matters as much as the fix itself.")

    h2(doc, "Crafting your maths -> support -> AI narrative")
    para(doc,
         "You will be asked 'Tell me about yourself' or 'Why this role?' Have a tight 60-90 second "
         "story that connects your three chapters into one arc, ending on the role you're interviewing "
         "for. Structure: where you started (maths), what you learned about yourself (support), what "
         "you built (the transition + portfolio), and why this role is the natural next step.")
    code_block(doc,
        "NARRATIVE TEMPLATE (60-90 seconds)\n"
        "----------------------------------\n"
        "\"I started in mathematics, where I got comfortable with probability and the\n"
        " kind of rigorous thinking behind how models like LLMs actually work. In my\n"
        " support internship I discovered I love being close to users and solving their\n"
        " problems - and I kept hitting moments where a smarter, AI-driven tool could\n"
        " have helped. So over the last six months I taught myself Python, SQL and how\n"
        " to build LLM applications, and I shipped [project]: a RAG support assistant\n"
        " that [quantified result]. This role sits exactly at the intersection of what\n"
        " I'm good at and what I want to do - building useful AI features close to real\n"
        " users - which is why I'm excited to be here.\"")

    callout(doc, "Common mistakes",
            "(1) Saying 'we' so much the interviewer can't tell what YOU did. (2) All Situation, almost "
            "no Action or Result. (3) No quantified outcome. (4) Rambling life story for 'tell me about "
            "yourself' instead of a 60-90s arc ending on this role. (5) Trash-talking a previous "
            "employer/customer. (6) Apologising for the career change instead of framing it as deliberate "
            "and evidenced.", color=RED)

    quiz(doc, [
        {"q": "What do the letters in STAR stand for?",
         "answer": "Situation, Task, Action, Result.",
         "why": "It structures behavioural answers so the interviewer can follow context, your role, "
                "your actions, and the outcome."},
        {"q": "Which part of a STAR answer should be the LONGEST?",
         "options": ["Situation", "Task", "Action", "Result"],
         "answer": "C",
         "why": "Action is where you show what YOU specifically did - the part interviewers score most."},
        {"q": "True/False: Using 'we' throughout your STAR answer is fine.",
         "answer": "False",
         "why": "Interviewers need to know what YOU did; over-using 'we' hides your individual contribution."},
        {"q": "Roughly how long should your 'tell me about yourself' narrative be?",
         "options": ["10-15 seconds", "60-90 seconds", "5 minutes", "As long as it takes"],
         "answer": "B",
         "why": "A tight 60-90s arc ending on the target role keeps the interviewer engaged."},
        {"q": "Short answer: How should you frame your career change from maths/support to AI?",
         "answer": "As a deliberate, evidence-backed transition (degree + support strengths + self-taught "
                   "build skills + shipped portfolio), not as a gap to apologise for.",
         "why": "Confident framing turns the change into a differentiator."},
        {"q": "Short answer: Give one strong source domain for STAR stories given this background.",
         "answer": "The L1 support internship (difficult customers, escalations, debugging), portfolio "
                   "projects (overcoming a technical blocker), or the maths degree (a hard project/deadline).",
         "why": "These give concrete, ownable Situations with measurable Results."},
    ], title="Topic 7 Quiz")

    page_break(doc)

    # ===============================================================
    # TOPIC 8 - TAKE-HOME ASSIGNMENTS
    # ===============================================================
    h1(doc, "8. Take-home assignments strategy")
    para(doc,
         "Many AI-application and startup roles use a take-home: build a small app or solve a data/LLM "
         "problem in a fixed time. They are an opportunity - they reward exactly the build-and-ship "
         "skills you spent five months on. The trap is over-engineering. Reviewers value clarity, "
         "correctness, and judgement about scope far more than features.")

    h2(doc, "How to approach a take-home")
    numbered(doc, "Clarify the brief and the time box. If it says '~4 hours', respect it; don't spend 20.")
    numbered(doc, "Restate the requirements in your README so the reviewer sees you understood the ask.")
    numbered(doc, "Build the smallest correct end-to-end solution first (make it work), then improve.")
    numbered(doc, "Write a clear README: what it does, how to run it, decisions, trade-offs, what you'd "
                  "do with more time.")
    numbered(doc, "Add a few tests for the core logic - it signals professionalism more than extra features.")
    numbered(doc, "Keep the code clean and readable; commit in sensible steps if a repo is requested.")

    h2(doc, "What reviewers actually score")
    table_from_rows(doc,
        ["They reward", "They penalise"],
        [["Correct, working end-to-end solution", "Impressive-looking but broken / won't run"],
         ["Clear README with run steps + decisions", "No instructions; reviewer can't run it"],
         ["Sensible scope for the time box", "Over-engineering, gold-plating, scope creep"],
         ["Readable, well-named code + a few tests", "Clever but unreadable; zero tests"],
         ["Honest 'what I'd do with more time'", "Pretending the solution is production-perfect"],
         ["Handling obvious edge cases", "Ignoring empty input / errors entirely"]])

    code_block(doc,
        "README SKELETON FOR A TAKE-HOME\n"
        "-------------------------------\n"
        "# Project name\n"
        "What it does (2-3 lines) and how it maps to the brief.\n\n"
        "## How to run\n"
        "  python -m venv .venv && source .venv/bin/activate\n"
        "  pip install -r requirements.txt\n"
        "  cp .env.example .env   # add your API key\n"
        "  python app.py\n\n"
        "## Design decisions\n"
        "  - Why I chose X over Y (e.g. FAISS vs hosted DB for a small local task)\n"
        "  - Key trade-offs and assumptions\n\n"
        "## Testing\n"
        "  pytest    # covers <core module>\n\n"
        "## With more time I would\n"
        "  - Add evaluation harness / auth / better error handling / CI")

    callout(doc, "Common mistakes",
            "(1) Over-engineering and blowing past the time box. (2) No README, or one the reviewer can't "
            "follow to run the project. (3) Hard-coding secrets / committing API keys. (4) Zero tests. "
            "(5) Ignoring the brief's actual question to show off something flashier. (6) Submitting "
            "something that doesn't run on a clean machine. (7) Not stating assumptions and trade-offs.",
            color=RED)

    quiz(doc, [
        {"q": "A take-home says '~4 hours'. What's the right response to scope?",
         "options": ["Spend 20 hours to dazzle them", "Respect the time box; ship the smallest correct "
                     "end-to-end solution and note what you'd add with more time", "Skip it",
                     "Do only the easy 20%"],
         "answer": "B",
         "why": "Reviewers test judgement about scope; respecting the box and being explicit about "
                "trade-offs scores well."},
        {"q": "True/False: Adding lots of extra features always improves a take-home score.",
         "answer": "False",
         "why": "Over-engineering and scope creep are penalised; clarity, correctness and scope judgement win."},
        {"q": "Name two things a strong take-home README must contain.",
         "answer": "Any two of: what it does, how to run it (exact commands), design decisions/trade-offs, "
                   "how to test it, and what you'd do with more time.",
         "why": "If the reviewer can't run it or understand your choices, even good code loses points."},
        {"q": "Why add a few tests even if the brief doesn't require them?",
         "answer": "They signal professionalism and that you verify your own work; they often impress more "
                   "than extra features.",
         "why": "Tests demonstrate engineering maturity and correctness."},
        {"q": "Short answer: Why is committing an API key into the repo a serious mistake?",
         "answer": "It leaks a secret/credential (a security risk and unprofessional); use a .env file and "
                   "a .env.example instead, and add .env to .gitignore.",
         "why": "Secret hygiene is a basic, watched-for engineering signal."},
        {"q": "What is the FIRST thing to build in a take-home?",
         "options": ["A polished UI", "The smallest correct end-to-end solution that runs",
                     "A full test suite", "A deployment pipeline"],
         "answer": "B",
         "why": "Make it work end-to-end first; then improve within the remaining time."},
    ], title="Topic 8 Quiz")

    page_break(doc)

    # ===============================================================
    # TOPIC 9 - NEGOTIATION, OFFERS & EVALUATING ROLES
    # ===============================================================
    h1(doc, "9. Negotiation, offers & evaluating roles")
    para(doc,
         "Getting the offer is not the finish line - evaluating and negotiating it is the last skill of "
         "the month. Even as a junior you can usually negotiate respectfully, and you should evaluate the "
         "whole role, not just the salary. Done politely and with data, negotiation rarely costs you an "
         "offer and often gains meaningful value.")

    h2(doc, "Evaluating an offer (beyond salary)")
    bullet(doc, "Learning & mentorship - will you have senior engineers to learn from? For a first AI "
                "job this often outweighs a few thousand in salary.")
    bullet(doc, "The actual work - how much is real AI/LLM building vs glue/ops/support? Read between "
                "the lines of the JD and ask in interviews.")
    bullet(doc, "Total compensation - base, bonus, equity, pension, benefits, holiday - not just base.")
    bullet(doc, "Growth & stability - team size, funding/runway (startup), promotion path, attrition.")
    bullet(doc, "Working conditions - remote/hybrid/on-site, hours culture, location, manager quality.")

    h2(doc, "How to negotiate (junior-friendly)")
    numbered(doc, "Do your research: know the market range for the role, level and location before you talk numbers.")
    numbered(doc, "Let them name a number first where you can ('What's the budgeted range for this role?').")
    numbered(doc, "Always express enthusiasm first, then ask - never an ultimatum.")
    numbered(doc, "Anchor on a researched range, not a single figure, and justify with your value.")
    numbered(doc, "Negotiate the whole package: if base is fixed, ask about signing bonus, start date, "
                  "learning budget, review timeline, or extra holiday.")
    numbered(doc, "Get the final offer in writing before resigning anywhere or declining other processes.")

    code_block(doc,
        "POLITE NEGOTIATION SCRIPT\n"
        "-------------------------\n"
        "\"Thank you so much - I'm genuinely excited about this role and the team.\n"
        " I've researched comparable junior AI roles in this market, and based on that\n"
        " and the skills I'd bring - building and shipping RAG applications, plus my\n"
        " support background - I was hoping we could look at a base of [X to Y].\n"
        " Is there flexibility there?\"\n\n"
        "IF BASE IS FIXED:\n"
        "\"I understand the base is set. Would you be open to a signing bonus, an earlier\n"
        " salary review at six months, or a learning/conference budget?\"\n\n"
        "ALWAYS: stay warm, never ultimatum, get the final number in writing.")

    callout(doc, "Common mistakes",
            "(1) Accepting on the spot out of relief without evaluating or asking. (2) Naming a number "
            "first when you could let them anchor. (3) Negotiating with no market research. (4) Treating "
            "it as a fight / issuing ultimatums. (5) Optimising only salary and ignoring mentorship, "
            "learning and the actual work - which matter most for a first AI role. (6) Resigning or "
            "declining other offers before the new one is in writing.", color=RED)

    quiz(doc, [
        {"q": "For a FIRST AI job, which factor often matters as much as or more than salary?",
         "options": ["The office snacks", "Mentorship/learning and how much real AI building you'll do",
                     "The job title's prestige", "The company logo"],
         "answer": "B",
         "why": "Early career, growth and relevant hands-on work compound more than a small salary delta."},
        {"q": "True/False: As a junior you should never attempt to negotiate.",
         "answer": "False",
         "why": "Polite, researched negotiation rarely costs the offer and often adds real value."},
        {"q": "Before negotiating, what must you do first?",
         "answer": "Research the market range for that role, level and location so your ask is grounded in data.",
         "why": "An anchored, justified range is credible; a random number is not."},
        {"q": "If the base salary is fixed, name two other things you can negotiate.",
         "answer": "Any two of: signing bonus, earlier salary review, learning/conference budget, extra "
                   "holiday, start date, equity, remote flexibility.",
         "why": "Compensation is a package; value can come from many levers."},
        {"q": "Short answer: What must you have before resigning or declining other processes?",
         "answer": "The final offer in writing.",
         "why": "Verbal offers can change; never give up leverage or another job before it's documented."},
        {"q": "What tone should a negotiation take?",
         "options": ["An ultimatum", "Warm and enthusiastic, then a researched ask",
                     "Cold and demanding", "Apologetic and self-deprecating"],
         "answer": "B",
         "why": "Enthusiasm-first framing keeps the relationship positive while you ask."},
    ], title="Topic 9 Quiz")

    page_break(doc)

    # ===============================================================
    # TOPIC 10 - FIRST 30/60/90 DAYS
    # ===============================================================
    h1(doc, "10. Your first 30/60/90 days in the new AI job")
    para(doc,
         "How you start sets your reputation. A 30/60/90-day plan shows interviewers you think ahead, "
         "and it genuinely helps you ramp once hired. The arc is: learn first, contribute small, then "
         "own something. Resist the urge to ship big changes in week one before you understand the system.")

    h2(doc, "The plan")
    table_from_rows(doc,
        ["Phase", "Theme", "What you do"],
        [["Days 1-30", "Learn & absorb",
          "Set up your environment; read the codebase, docs and runbooks; map the system and who owns "
          "what; ask lots of questions; ship a tiny first PR (a bug fix or doc update) to learn the "
          "pipeline; meet your team and stakeholders."],
         ["Days 31-60", "Contribute",
          "Take ownership of small, well-defined tasks end to end; improve prompts/retrieval/evals on an "
          "existing feature; write tests and docs; start reviewing others' PRs; build trust by delivering "
          "reliably and communicating clearly."],
         ["Days 61-90", "Own & propose",
          "Own a small feature or improvement end to end; propose a measured improvement (e.g. an eval "
          "metric, a retrieval tweak) backed by data; deepen domain knowledge; set development goals with "
          "your manager."]])

    code_block(doc,
        "30/60/90 ONE-LINERS (say these in an interview)\n"
        "-----------------------------------------------\n"
        "30:  \"Listen and learn - understand the codebase, the users, and how the\n"
        "      LLM system is built and evaluated; ship one tiny PR to learn the flow.\"\n"
        "60:  \"Start contributing - own small tasks end to end, add tests and evals,\n"
        "      and build trust by delivering reliably.\"\n"
        "90:  \"Own a feature and propose a data-backed improvement; set goals with\n"
        "      my manager for the next quarter.\"")

    para(doc, "Tie it to this role specifically: as a support-background hire, an easy early win is "
              "bringing the user's voice into the AI team - flagging real failure modes, improving the "
              "'I don't know' / escalation behaviour, or strengthening the eval set with real questions "
              "users actually ask.")

    callout(doc, "Common mistakes",
            "(1) Trying to rewrite the system in week one before understanding it. (2) Staying silent and "
            "not asking questions for fear of looking junior - asking is expected and valued early. (3) No "
            "measurable early win. (4) Not building relationships across the team. (5) A vague plan with no "
            "phases. (6) Forgetting to align goals with your manager by day 90.", color=RED)

    quiz(doc, [
        {"q": "What is the correct THEME ordering across the three phases?",
         "options": ["Own -> Contribute -> Learn", "Learn -> Contribute -> Own & propose",
                     "Propose -> Learn -> Contribute", "Contribute -> Own -> Learn"],
         "answer": "B",
         "why": "You earn the right to own and propose by learning and contributing first."},
        {"q": "True/False: A great way to impress in week one is to push a large refactor of the codebase.",
         "answer": "False",
         "why": "Big changes before you understand the system are risky and erode trust; learn first, ship "
                "small first."},
        {"q": "What is a good Day 1-30 deliverable to learn the pipeline?",
         "answer": "A tiny first PR such as a small bug fix or documentation update.",
         "why": "It teaches you the build/review/deploy flow with low risk."},
        {"q": "Short answer: What's an easy early win specific to a support-background AI hire?",
         "answer": "Bringing the user's voice in: flagging real failure modes, improving 'I don't know'/"
                   "escalation behaviour, or enriching the eval set with real user questions.",
         "why": "It uses your differentiator and delivers visible value fast."},
        {"q": "By Day 90, what should you do with your manager?",
         "answer": "Align on development goals / objectives for the next quarter (and propose a data-backed "
                   "improvement).",
         "why": "It shows ownership and sets you up for the next phase."},
        {"q": "Why is asking lots of questions in the first 30 days a good thing?",
         "options": ["It isn't - it looks junior", "It is expected and valued; it accelerates ramp and "
                     "prevents costly wrong assumptions", "It annoys the team", "It wastes time"],
         "answer": "B",
         "why": "New hires are expected to ask; questions are how you ramp and avoid mistakes."},
    ], title="Topic 10 Quiz")

    page_break(doc)

    # ===============================================================
    # EXERCISES
    # ===============================================================
    h1(doc, "Exercises")
    para(doc, "Do these throughout the month. They are deliberately practical - each produces an asset "
              "or a reusable skill for your campaign.")
    numbered(doc, "Application-tracker setup: build the tracker from the Project brief (spreadsheet or "
                  "Notion) with all columns, statuses and a follow-up reminder rule. Log your first 10 "
                  "real applications into it this week.")
    numbered(doc, "Role-targeting list: find and save 25 live job postings across your primary lanes "
                  "(AI Engineer junior, AI Application Developer, LLM Engineer, Forward-Deployed/Solutions, "
                  "AI-support). For each, note the top 5 keywords from the JD.")
    numbered(doc, "CV bullet rewrite: take 6 weak/duty-style bullets from your current CV and rewrite each "
                  "as an action + tools + quantified-result bullet. Have a peer or AI critique them.")
    numbered(doc, "Tailoring drill: pick 3 real postings and produce 3 tailored one-page CVs and 3 short, "
                  "specific cover notes - timed at 20 minutes each to build speed.")
    numbered(doc, "Concept-answer bank: write and rehearse out-loud 45-90 second answers to the 8 concept "
                  "questions in Topic 3 until they're smooth without notes.")
    numbered(doc, "Coding + SQL drills: solve all Topic 4 and Topic 5 problems from scratch without looking "
                  "at the key, talking through your approach aloud (record yourself once).")
    numbered(doc, "Mock interviews: run at least 3 mock interviews - one technical (Python/SQL live), one "
                  "concept/system-design-lite, one behavioural - with a peer, a mentor, or an AI interviewer. "
                  "Get feedback and iterate.")
    numbered(doc, "Portfolio pitch: prepare and rehearse a 5-minute spoken walkthrough of your best project "
                  "(problem -> what you built -> a result -> what you learned), timed and recorded.")

    page_break(doc)

    # ===============================================================
    # PROJECT BRIEF (CAPSTONE)
    # ===============================================================
    h1(doc, "Project brief - Capstone: Interview-Readiness Package")
    para(doc,
         "Your capstone for Month 6 - and for the whole programme - is a complete interview-readiness "
         "package: the toolkit you will actually use to run your campaign and walk into interviews "
         "prepared. Treat it as a real deliverable you keep using until you're hired.")

    h2(doc, "Deliverables")
    bullet(doc, "Application tracker (spreadsheet or Notion) with a clean schema and a follow-up system.")
    bullet(doc, "A polished one-page narrative document + a tailored, ATS-friendly master CV.")
    bullet(doc, "A bank of 6-8 STAR stories covering the common behavioural themes.")
    bullet(doc, "Written model answers to the top 20 AI interview questions (concept + behavioural).")
    bullet(doc, "A rehearsed 5-minute presentation of your best portfolio project (slides or live demo).")

    h2(doc, "Suggested application-tracker schema")
    table_from_rows(doc,
        ["Column", "Purpose / example"],
        [["Company", "Employer name"],
         ["Role / lane", "Title + which target lane (e.g. AI App Dev)"],
         ["Link", "URL of the posting"],
         ["Date applied", "When you submitted"],
         ["Source", "Portal / referral / recruiter / outreach"],
         ["Status", "Applied / Screen / Interview / Take-home / Offer / Rejected"],
         ["Contact", "Recruiter or referrer name"],
         ["Next action + date", "e.g. 'Follow up 2026-06-22'"],
         ["Notes", "JD keywords, prep notes, interviewer names"]])

    h2(doc, "Milestones")
    table_from_rows(doc,
        ["Week", "Milestone"],
        [["Week 1", "Tracker built and live; master CV + one-page narrative drafted; 15+ applications logged."],
         ["Week 2", "STAR bank (6-8 stories) written; CV tailored to 3 real roles; concept-answer bank started; "
                    "applications continuing at target volume."],
         ["Week 3", "Top-20 AI interview answers written; 5-minute portfolio presentation built and rehearsed "
                    "once; 2+ mock interviews done."],
         ["Week 4", "Full package polished; all answers rehearsed out loud; 3+ mocks completed; campaign "
                    "running steadily with follow-ups; ready for live interview loops."]])

    h2(doc, "Rubric")
    table_from_rows(doc,
        ["Criterion", "Excellent", "Adequate", "Needs work"],
        [["Application tracker",
          "Complete schema, live, used daily, with follow-up rule and metrics.",
          "Tracker exists with core columns and most apps logged.",
          "Ad-hoc list or nothing tracked."],
         ["CV & narrative",
          "One page, ATS-friendly, quantified AI bullets; tight 60-90s narrative.",
          "Mostly tailored, some quantified bullets, narrative drafted.",
          "Generic, duty bullets, no clear narrative."],
         ["STAR bank",
          "6-8 stories, strong Action+Result, quantified, rehearsed.",
          "4-5 usable stories with outcomes.",
          "Few/weak stories, mostly Situation."],
         ["Top-20 answers",
          "All 20 correct, concise, in your own voice, rehearsed aloud.",
          "Most answered correctly, some rough.",
          "Sparse or incorrect answers."],
         ["Portfolio pitch",
          "Clear 5-min story (problem->build->result->learning), timed, confident.",
          "Covers the project but over/under time or unfocused.",
          "Rambling, no result, not rehearsed."],
         ["Campaign discipline",
          "Hit weekly volume, warm outreach, follow-ups on time.",
          "Applied regularly, some follow-ups.",
          "Sporadic applications, no follow-up."]])

    callout(doc, "Done means",
            "By the end of Month 6 you can open your tracker, see a healthy pipeline, pull up a tailored "
            "CV in minutes, answer the top concept and behavioural questions smoothly, and confidently "
            "present your best project in five minutes. That is interview-ready.", color=GREEN)

    page_break(doc)

    # ===============================================================
    # RESOURCES
    # ===============================================================
    h1(doc, "Resources")
    para(doc, "Real, well-known resources. Search by name; avoid relying on any single one.", color=GREY)
    bullet(doc, "LeetCode (leetcode.com) - Python coding interview practice; focus on Easy/Medium "
                "arrays, hash maps, strings.")
    bullet(doc, "StrataScratch and DataLemur - SQL and data-interview practice with real-style questions.")
    bullet(doc, "'Cracking the Coding Interview' by Gayle Laakmann McDowell - the classic technical-"
                "interview prep book (concepts and behavioural guidance).")
    bullet(doc, "Pramp / interviewing.io - free or freemium peer and professional mock interviews.")
    bullet(doc, "Tech Interview Handbook (techinterviewhandbook.org) - free, high-quality guide to CVs, "
                "behavioural and coding interviews.")
    bullet(doc, "'Never Split the Difference' by Chris Voss and the Harvard PON (Program on Negotiation) "
                "blog - negotiation principles.")
    bullet(doc, "DeepLearning.AI short courses (deeplearning.ai) and the OpenAI / Anthropic documentation "
                "- to firm up RAG, embeddings, evaluation and agent concepts for the concept round.")
    bullet(doc, "LinkedIn Jobs, Otta/Welcome to the Jungle, and Wellfound (AngelList Talent) - sourcing "
                "AI and startup roles across your target lanes.")

    para(doc, "")
    callout(doc, "Final word",
            "You've built the skills over five months. This month is about belief plus volume plus "
            "preparation. Keep the pipeline full, treat every interview as practice for the next, and "
            "remember your maths-plus-support-plus-builder profile is genuinely rare. Go and land it.",
            color=NAVY)

    doc.save(OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
