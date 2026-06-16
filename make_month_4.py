# -*- coding: utf-8 -*-
"""
Month 4 study pack generator: Portfolio Projects.
Run from the working directory:  python make_month_4.py
Produces: Month_4_Portfolio_Projects_Study_Pack.docx
"""
from doc_helpers import (
    new_doc, title_block, h1, h2, h3, para, lead, bullet, numbered,
    code_block, callout, table_from_rows, quiz, page_break,
    NAVY, ACCENT, GREY, GREEN, AMBER, RED,
)

OUTFILE = "Month_4_Portfolio_Projects_Study_Pack.docx"


def build():
    doc = new_doc()

    # ------------------------------------------------------------------ #
    # 1. TITLE BLOCK
    # ------------------------------------------------------------------ #
    title_block(
        doc,
        "Month 4 - Portfolio Projects",
        "Turning skills into real, product-shaped AI apps",
        "Maths Graduate to AI Job - 6-Month Track  |  ~30 hrs/week  |  Months 1-3 complete",
    )

    para(
        doc,
        "You have spent three months building the raw materials: Python, data wrangling, "
        "SQL, APIs, and the core LLM-application skills including retrieval-augmented "
        "generation (RAG). Month 4 is where those materials become a product. The goal is "
        "not more tutorials - it is to ship two or three apps that a hiring manager can open, "
        "run, and immediately understand. Your L1 support internship is a genuine asset here: "
        "the flagship project is an AI support-ticket assistant, and you already know what a "
        "real support workflow feels like. Lean on that.",
        size=11,
    )
    para(
        doc,
        "Everything in this pack uses the Anthropic Claude Messages API as the reference "
        "implementation. Keep your API key in an environment variable, never in code, and "
        "never commit it. We will repeat that until it is muscle memory.",
        italic=True, color=GREY, size=10,
    )

    # ------------------------------------------------------------------ #
    # 2. LEARNING OBJECTIVES
    # ------------------------------------------------------------------ #
    h1(doc, "Learning objectives")
    para(doc, "By the end of Month 4 you should be able to:")
    objectives = [
        "Apply prompt-engineering patterns (few-shot, chain-of-thought, role prompting, "
        "output formatting, reusable templates) deliberately rather than by trial and error.",
        "Design guardrails that keep an LLM grounded in supplied context, refuse or escalate "
        "when unsure, and validate both inputs and outputs.",
        "Build an evaluation harness: a test set, a scoring function, and a regression check "
        "you can run every time you change a prompt.",
        "Decide when a single API call is enough and when a multi-step agent with tools is "
        "justified - and implement a tool-using agent with the Claude API.",
        "Separate an AI application into backend, frontend, and storage layers with clear "
        "responsibilities and clean boundaries.",
        "Expose an AI workflow over a FastAPI backend, including a streaming endpoint and a "
        "background task.",
        "Build an interactive UI with Streamlit and wire it to your backend.",
        "Ingest files and PDFs: parse them, chunk them sensibly for retrieval, and reason "
        "about chunk size and overlap.",
        "Manage secrets and configuration with environment variables and a typed settings "
        "object - and explain why keys never enter version control.",
        "Structure a project so the code is readable, testable, and reviewable - the quality "
        "bar that separates a portfolio piece from a homework submission.",
    ]
    for o in objectives:
        bullet(doc, o)

    page_break(doc)

    # ================================================================== #
    # TOPIC 1 - PROMPT ENGINEERING PATTERNS
    # ================================================================== #
    h1(doc, "1. Prompt-engineering patterns")

    para(
        doc,
        "A prompt is a program written in natural language. Like any program it has inputs, "
        "structure, and a contract for its output. The model is a probabilistic interpreter: "
        "the same prompt can give slightly different answers, so your job is to constrain the "
        "space of plausible outputs until almost all of them are correct. The patterns below "
        "are the levers you pull to do that.",
    )
    para(
        doc,
        "Start from first principles. The model predicts the next token given everything "
        "before it. So every word you place earlier in the prompt conditions everything that "
        "comes after. That single fact explains why role prompting works (it sets the "
        "distribution of 'who is speaking'), why few-shot works (it shows the pattern to "
        "continue), and why output-format instructions work best when placed last and stated "
        "concretely (they are the most recent, most salient instruction before generation).",
    )

    h2(doc, "The five core patterns")

    lead(doc, "Few-shot prompting.",
         "Show the model two to five worked examples of the input/output mapping you want, "
         "then give it a fresh input. The examples teach format, tone, and edge-case handling "
         "far more reliably than a paragraph of description. Use it for classification, "
         "extraction, and consistent formatting. Keep examples diverse and representative of "
         "the real distribution - three carefully chosen examples beat ten near-duplicates.")

    lead(doc, "Chain-of-thought (CoT).",
         "Ask the model to reason step by step before committing to an answer. For arithmetic, "
         "multi-hop logic, and policy decisions this materially improves accuracy because the "
         "intermediate tokens give the model 'room to compute'. With modern Claude models you "
         "can also let the model think adaptively (the API decides how much reasoning to do) "
         "instead of forcing 'think step by step' into every prompt - but understanding the "
         "underlying pattern is essential.")

    lead(doc, "Role prompting.",
         "Open with a role: 'You are a senior support engineer who writes calm, precise "
         "replies.' This conditions vocabulary, tone, and the kind of mistakes the model "
         "avoids. Roles belong in the system prompt, which is the stable, cacheable prefix of "
         "the conversation.")

    lead(doc, "Output formatting.",
         "State the exact output shape and put that instruction near the end. 'Return only a "
         "JSON object with keys category, confidence, and reason. No prose.' For "
         "machine-readable output, prefer the API's structured-output feature over hoping the "
         "model obeys - but a clear instruction is still your first line of defence.")

    lead(doc, "Prompt templates.",
         "A template is a reusable prompt with named slots you fill at runtime. Treating "
         "prompts as templates (not f-strings scattered through your code) is what lets you "
         "version them, test them, and reuse them. This is the bridge from 'prompting' to "
         "'prompt engineering'.")

    h2(doc, "Worked example: a reusable, role + few-shot + format prompt")

    code_block(doc, r'''import os
from anthropic import Anthropic

# The key is read from the ANTHROPIC_API_KEY environment variable.
# Never hardcode it. Anthropic() picks it up automatically.
client = Anthropic()

# --- Role prompt lives in the system prompt (stable, cacheable prefix) ---
SYSTEM_PROMPT = (
    "You are a senior customer-support engineer. "
    "You categorise support tickets accurately and never invent product features."
)

# --- A reusable template with a named slot ---
CATEGORISE_TEMPLATE = """\
Categorise the support ticket into exactly one of:
billing, bug, how-to, account, other.

Here are examples:
Ticket: "I was charged twice this month."        -> billing
Ticket: "The export button does nothing."         -> bug
Ticket: "How do I reset my password?"             -> how-to

Now categorise this ticket. Return ONLY the category word, nothing else.
Ticket: "{ticket}"
"""

def categorise(ticket: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",        # cheap + fast is fine for classification
        max_tokens=16,                    # one word out, so keep it tiny
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user",
             "content": CATEGORISE_TEMPLATE.format(ticket=ticket)}
        ],
    )
    # response.content is a list of blocks; take the first text block.
    text = next(b.text for b in message.content if b.type == "text")
    return text.strip().lower()

if __name__ == "__main__":
    print(categorise("My invoice shows the wrong VAT amount."))  # -> billing''')

    para(
        doc,
        "Notice the structure: role in the system prompt, examples in the body, and the "
        "format instruction ('Return ONLY the category word') placed last. The template has a "
        "single named slot, so the same prompt is reused for every ticket and could be unit "
        "tested in isolation.",
        size=10, color=GREY, italic=True,
    )

    callout(
        doc, "Common mistakes",
        "Burying the output-format instruction in the middle of a long prompt (put it last). "
        "Using too many near-identical few-shot examples, which teaches the model nothing new "
        "and wastes tokens. Writing 'think step by step' but then giving max_tokens=20, so the "
        "model has no room to reason. Putting the role in the user message instead of the "
        "system prompt, which weakens it and breaks prompt caching. Pasting prompts as raw "
        "f-strings throughout the codebase so they can never be versioned or tested.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "Where should an output-format instruction usually go, and why?",
            "answer": "At or near the END of the prompt.",
            "why": "It is the most recent instruction before generation, so it is the most "
                   "salient; the model conditions its next tokens most strongly on what came "
                   "just before.",
        },
        {
            "q": "Which pattern is most appropriate for teaching a consistent output FORMAT "
                 "with minimal description?",
            "options": ["Chain-of-thought", "Few-shot prompting",
                        "Increasing max_tokens", "Lowering the temperature"],
            "answer": "B - Few-shot prompting.",
            "why": "A few worked input/output examples demonstrate format directly, which is "
                   "more reliable than describing it in prose.",
        },
        {
            "q": "True or false: role prompting belongs in the system prompt rather than the "
                 "user message.",
            "options": ["True", "False"],
            "answer": "A - True.",
            "why": "The system prompt is the stable, high-authority prefix; placing the role "
                   "there strengthens it and keeps it cacheable.",
        },
        {
            "q": "Why does chain-of-thought often improve accuracy on multi-step problems?",
            "answer": "The intermediate reasoning tokens give the model 'room to compute' a "
                      "multi-step result instead of guessing an answer in one jump.",
            "why": "Each generated reasoning token conditions the next, so the model can build "
                   "the answer incrementally rather than predicting it all at once.",
        },
        {
            "q": "What is the practical advantage of treating a prompt as a TEMPLATE with "
                 "named slots rather than inline f-strings?",
            "answer": "It can be versioned, reused, and unit tested independently of the call "
                      "site.",
            "why": "Centralising the prompt makes it a first-class artefact you can change and "
                   "evaluate, rather than scattered strings.",
        },
        {
            "q": "You give three few-shot examples that are all almost identical billing "
                 "tickets. What is the likely problem?",
            "options": [
                "The model will refuse to answer",
                "The examples fail to teach edge cases or other categories",
                "The prompt will exceed the context window",
                "Few-shot prompting cannot be used for classification",
            ],
            "answer": "B - The examples fail to teach edge cases or other categories.",
            "why": "Diverse, representative examples are what carry information; near-duplicates "
                   "waste tokens and leave other categories undemonstrated.",
        },
    ], title="Quiz - Prompt-engineering patterns")

    page_break(doc)

    # ================================================================== #
    # TOPIC 2 - GUARDRAILS & HALLUCINATION CONTROL
    # ================================================================== #
    h1(doc, "2. Guardrails & hallucination control")

    para(
        doc,
        "A language model is a fluent guesser. Left to itself it will answer confidently even "
        "when it does not know, because producing plausible text is exactly what it was "
        "trained to do. A guardrail is any mechanism that constrains that behaviour so the "
        "system is safe to put in front of a user. For a support assistant this is the single "
        "most important engineering concern: a wrong-but-confident answer to a billing "
        "question is worse than no answer at all.",
    )
    para(
        doc,
        "Think in terms of four layers. (1) Grounding: give the model the source material and "
        "tell it to answer only from that material. (2) Refusal and escalation: when the "
        "context does not contain the answer, the model should say so and hand off to a human "
        "rather than improvise. (3) Input validation: check what comes in before it ever "
        "reaches the model. (4) Output validation: check what comes out before it reaches the "
        "user. No single layer is sufficient; together they make hallucinations rare and "
        "recoverable.",
    )

    h2(doc, "Grounding and 'answer only from context'")
    para(
        doc,
        "The core grounding instruction is blunt and effective: supply the retrieved context, "
        "then instruct the model to answer using only that context and to say 'I don't know' "
        "if the answer is not present. Pair this with citations so a reviewer can trace every "
        "claim back to a source chunk. Grounding does not make hallucination impossible, but "
        "it changes the default from 'invent something' to 'admit the gap'.",
    )

    h2(doc, "Worked example: grounded answer with refusal/escalation")

    code_block(doc, r'''import os
from anthropic import Anthropic

client = Anthropic()

GROUNDED_SYSTEM = """\
You are a support assistant. Answer ONLY using the information in <context>.
Rules:
- If the answer is not contained in <context>, reply exactly: ESCALATE
- Never use outside knowledge or guess.
- When you do answer, cite the source id in square brackets, e.g. [doc-3].
"""

def answer_from_context(question: str, context_chunks: list[dict]) -> dict:
    # Build a context block the model can cite from.
    context = "\n\n".join(
        f"<source id=\"{c['id']}\">{c['text']}</source>" for c in context_chunks
    )
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=GROUNDED_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"<context>\n{context}\n</context>\n\nQuestion: {question}",
        }],
    )
    text = next(b.text for b in message.content if b.type == "text").strip()

    # Output guardrail: turn the sentinel into a real control-flow signal.
    if text == "ESCALATE":
        return {"status": "escalate",
                "answer": None,
                "reason": "Answer not found in retrieved context."}
    return {"status": "answered", "answer": text, "reason": None}

if __name__ == "__main__":
    chunks = [{"id": "doc-1",
               "text": "Refunds are issued within 5 business days to the original card."}]
    print(answer_from_context("How long do refunds take?", chunks))
    print(answer_from_context("Do you support Apple Pay?", chunks))  # -> escalate''')

    para(
        doc,
        "The pattern is: a strict system prompt that defines a refusal sentinel (ESCALATE), a "
        "context block the model is told to confine itself to, and an output check that "
        "converts the sentinel into a branch in your code. The model's text is never trusted "
        "blindly - your code decides what 'escalate' means.",
        size=10, color=GREY, italic=True,
    )

    h2(doc, "Input and output validation")
    bullet(doc, "Input validation: reject empty or absurdly long inputs, strip or neutralise "
                "attempts at prompt injection (e.g. 'ignore your instructions'), and enforce a "
                "maximum length before you spend tokens.")
    bullet(doc, "Output validation: confirm the output matches the expected shape (valid JSON, "
                "an allowed category, a citation present), and fall back to escalation if it "
                "does not. Treat the model as an untrusted upstream service.")

    callout(
        doc, "Common mistakes",
        "Trusting the model's confidence as if it were a probability of correctness - fluency "
        "is not accuracy. Grounding the model but then letting it answer when retrieval "
        "returned nothing relevant (always check that you actually retrieved something). "
        "Forgetting an output check, so a malformed or off-policy answer reaches the user. "
        "Building only a happy path with no escalation route, which is the one path support "
        "users hit most. Writing 'answer only from context' but not giving the model any way "
        "to signal 'I can't' - it will then answer anyway.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "What does it mean to 'ground' an LLM answer?",
            "answer": "To supply source material as context and instruct the model to answer "
                      "only from it.",
            "why": "Grounding shifts the default behaviour from inventing an answer to using "
                   "(and ideally citing) supplied evidence.",
        },
        {
            "q": "Your retrieval step returns zero relevant chunks but you still call the "
                 "model with an empty context. What is the safest behaviour?",
            "options": [
                "Let the model answer from general knowledge",
                "Escalate or return 'I don't know' without calling the model, or have the "
                "model refuse",
                "Increase max_tokens and retry",
                "Lower the temperature to 0",
            ],
            "answer": "B - Escalate / refuse rather than answer ungrounded.",
            "why": "With no relevant context, any answer is ungrounded and likely to "
                   "hallucinate; refusal/escalation is correct.",
        },
        {
            "q": "True or false: a confident-sounding answer from an LLM is good evidence that "
                 "the answer is correct.",
            "options": ["True", "False"],
            "answer": "B - False.",
            "why": "Fluency and confidence are properties of the text, not measures of factual "
                   "accuracy.",
        },
        {
            "q": "Name one INPUT-side guardrail and one OUTPUT-side guardrail.",
            "answer": "Input: reject over-length input or neutralise injection attempts. "
                      "Output: validate that the response is well-formed JSON / an allowed "
                      "category / contains a citation.",
            "why": "Input guards protect the model; output guards protect the user. You need "
                   "both.",
        },
        {
            "q": "Why is a refusal sentinel (e.g. the literal word ESCALATE) useful?",
            "answer": "It gives your code a reliable, machine-checkable signal to branch on "
                      "for handing off to a human.",
            "why": "A fixed token is easy to detect exactly, turning a fuzzy 'I'm not sure' "
                   "into deterministic control flow.",
        },
        {
            "q": "What is prompt injection, in one sentence?",
            "answer": "Untrusted input that tries to override or subvert the system's "
                      "instructions (e.g. 'ignore previous instructions and ...').",
            "why": "Treating user/document text as data, not as instructions, plus input "
                   "validation, is the defence.",
        },
    ], title="Quiz - Guardrails & hallucination control")

    page_break(doc)

    # ================================================================== #
    # TOPIC 3 - EVALUATION HARNESSES
    # ================================================================== #
    h1(doc, "3. Evaluation harnesses")

    para(
        doc,
        "You cannot improve what you cannot measure. An evaluation harness is the part of an "
        "LLM project that turns 'it seems better now' into a number you can defend. It has "
        "three pieces: a test set of inputs with known-good expectations, a scoring function "
        "that compares an output to the expectation, and a runner that executes the whole set "
        "and reports a result. Once you have it, every prompt change becomes a measurable "
        "experiment instead of a guess.",
    )
    para(
        doc,
        "The hardest part is the test set. Build it from real or realistic inputs - for the "
        "support assistant, use anonymised tickets. Cover the easy cases, the edge cases, and "
        "the cases that SHOULD escalate (these are as important as the answerable ones). "
        "Twenty good cases beat two hundred sloppy ones. Treat the test set as code: it lives "
        "in the repository and grows whenever you find a new failure.",
    )

    h2(doc, "Scoring: exact, structural, and model-graded")
    bullet(doc, "Exact / keyword match: cheap and deterministic. Good for categories, yes/no, "
                "and 'did it escalate?' checks.")
    bullet(doc, "Structural checks: is the JSON valid, is the category in the allowed set, is "
                "a citation present? These catch format regressions.")
    bullet(doc, "Model-graded (LLM-as-judge): use a second model call to score open-ended "
                "answers against a rubric when there is no single correct string. Powerful but "
                "more expensive and itself needs sanity-checking.")

    h2(doc, "Worked example: a minimal regression harness")

    code_block(doc, r'''import json
from anthropic import Anthropic

client = Anthropic()

# 1) The test set lives in the repo and grows over time.
TEST_SET = [
    {"q": "How long do refunds take?",  "expect_status": "answered",
     "must_include": ["5 business days"]},
    {"q": "Do you support Apple Pay?",  "expect_status": "escalate",
     "must_include": []},
]

CONTEXT = [{"id": "doc-1",
            "text": "Refunds are issued within 5 business days to the original card."}]

def run_case(case: dict) -> dict:
    # answer_from_context() is the grounded function from Topic 2.
    result = answer_from_context(case["q"], CONTEXT)

    # 2) Scoring function: structural + keyword checks.
    passed = result["status"] == case["expect_status"]
    if passed and result["status"] == "answered":
        passed = all(kw in result["answer"] for kw in case["must_include"])
    return {"q": case["q"], "passed": passed, "got": result}

def run_suite() -> float:
    results = [run_case(c) for c in TEST_SET]
    n_pass = sum(r["passed"] for r in results)
    for r in results:
        flag = "PASS" if r["passed"] else "FAIL"
        print(f"[{flag}] {r['q']}")
    score = n_pass / len(results)
    print(f"\nScore: {n_pass}/{len(results)} = {score:.0%}")
    return score

if __name__ == "__main__":
    # 3) Regression gate: fail the build if the score drops below a threshold.
    assert run_suite() >= 1.0, "Regression: prompt change lowered the eval score."''')

    para(
        doc,
        "This is deliberately small, but it has the three essential parts and a regression "
        "gate (the assert). Run it before and after every prompt change. When you find a new "
        "failure in production, add it to TEST_SET so it can never silently regress again.",
        size=10, color=GREY, italic=True,
    )

    callout(
        doc, "Common mistakes",
        "Evaluating only the cases your prompt already handles, so the harness always passes "
        "and proves nothing. Omitting escalation/refusal cases - then shipping a model that "
        "answers things it should decline. Using LLM-as-judge for everything when an exact "
        "match would be cheaper and more reliable. Not gating on a threshold, so a regression "
        "slips through unnoticed. Letting the test set live outside version control so it "
        "drifts and rots. Scoring on the same inputs you used to tune the prompt, which "
        "over-fits and inflates the number.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "What are the three essential components of an evaluation harness?",
            "answer": "A test set (inputs + expected outcomes), a scoring function, and a "
                      "runner that reports a result.",
            "why": "Together they convert subjective 'it feels better' into a repeatable, "
                   "comparable number.",
        },
        {
            "q": "Why must a support-assistant test set include cases that SHOULD escalate?",
            "answer": "Because correctly refusing/escalating is a core requirement; a harness "
                      "that only tests answerable cases hides the most dangerous failures.",
            "why": "Over-answering is exactly the behaviour guardrails exist to prevent, so it "
                   "must be measured.",
        },
        {
            "q": "Which scoring method is best for checking 'did the model output one of the "
                 "allowed category words?'",
            "options": ["LLM-as-judge", "Exact / structural match",
                        "Human review only", "Embedding similarity"],
            "answer": "B - Exact / structural match.",
            "why": "A fixed allowed set is checked deterministically and cheaply with an exact "
                   "or membership match.",
        },
        {
            "q": "True or false: you should tune your prompt on the same examples you use to "
                 "report your final eval score.",
            "options": ["True", "False"],
            "answer": "B - False.",
            "why": "Tuning and reporting on the same data over-fits and inflates the score; "
                   "keep a held-out set.",
        },
        {
            "q": "What is 'LLM-as-judge' and when is it appropriate?",
            "answer": "Using a second model call to grade an open-ended answer against a "
                      "rubric, appropriate when there is no single correct string.",
            "why": "It handles subjective/open answers but costs more and must itself be "
                   "sanity-checked.",
        },
        {
            "q": "You find a new failure in production. What is the disciplined next step for "
                 "your harness?",
            "answer": "Add that case to the test set so the harness will catch any future "
                      "regression of it.",
            "why": "Growing the suite from real failures is how it stays honest and "
                   "protective over time.",
        },
    ], title="Quiz - Evaluation harnesses")

    page_break(doc)

    # ================================================================== #
    # TOPIC 4 - AGENTS & MULTI-STEP WORKFLOWS
    # ================================================================== #
    h1(doc, "4. Agents & multi-step workflows")

    para(
        doc,
        "A single API call maps one input to one output. An agent is a loop: the model is "
        "given tools, it decides which tool to call, your code runs the tool and feeds the "
        "result back, and the loop repeats until the model produces a final answer. The model "
        "supplies the planning; your code supplies the execution and the guardrails. That loop "
        "is the whole idea - everything else is detail.",
    )
    para(
        doc,
        "The most important agent skill is knowing when NOT to build one. Agents are slower, "
        "costlier, and harder to debug than a single call. Reach for an agent only when the "
        "task is genuinely multi-step and hard to specify in advance, the value justifies the "
        "extra cost and latency, and errors can be caught and recovered from. If you can solve "
        "the task with one well-crafted call or a fixed code-orchestrated pipeline, do that "
        "instead.",
    )

    h2(doc, "Tools, planning loops, and memory")
    bullet(doc, "Tools: functions you expose to the model with a name, a description, and a "
                "JSON input schema. The description is how the model decides when to call the "
                "tool - be prescriptive about WHEN, not just what it does.")
    bullet(doc, "Planning loop: keep calling the model, executing requested tools, and "
                "appending results until stop_reason is 'end_turn'. Cap the number of "
                "iterations so a confused agent cannot loop forever.")
    bullet(doc, "Memory: within a run, the growing message list IS the memory. Across runs, "
                "you persist state yourself (a file, a database). Start with in-conversation "
                "memory; add cross-session memory only when the product needs it.")

    h2(doc, "Worked example: a tool-using agent (manual loop)")

    code_block(doc, r'''import json
from anthropic import Anthropic

client = Anthropic()

# 1) Define a tool: name, description (say WHEN to use it), and input schema.
TOOLS = [{
    "name": "lookup_order",
    "description": "Look up an order's status by its id. "
                   "Call this whenever the user asks about a specific order.",
    "input_schema": {
        "type": "object",
        "properties": {"order_id": {"type": "string"}},
        "required": ["order_id"],
    },
}]

# 2) Your code actually executes the tool.
def lookup_order(order_id: str) -> str:
    fake_db = {"A100": "shipped", "A200": "processing"}
    return fake_db.get(order_id, "not found")

def run_agent(user_input: str, max_steps: int = 5) -> str:
    messages = [{"role": "user", "content": user_input}]
    for _ in range(max_steps):                      # cap the loop
        resp = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        if resp.stop_reason == "end_turn":
            return next(b.text for b in resp.content if b.type == "text")

        # Append the assistant turn (it contains the tool_use blocks).
        messages.append({"role": "assistant", "content": resp.content})

        # Execute each requested tool and feed results back.
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                if block.name == "lookup_order":
                    out = lookup_order(block.input["order_id"])
                else:
                    out = "Unknown tool"
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,    # must match the tool_use id
                    "content": out,
                })
        messages.append({"role": "user", "content": tool_results})
    return "Stopped: reached the step limit."

if __name__ == "__main__":
    print(run_agent("What's the status of order A100?"))''')

    para(
        doc,
        "Trace the loop: the model asks to call lookup_order, your code runs it, the result "
        "goes back as a tool_result block with the matching tool_use_id, and the model uses it "
        "to write the final answer. The max_steps cap is your safety valve. The Anthropic SDK "
        "also offers a tool runner that automates this loop, but writing it by hand once is the "
        "best way to understand what an agent actually is.",
        size=10, color=GREY, italic=True,
    )

    callout(
        doc, "Common mistakes",
        "Building an agent when a single call would do - the most common over-engineering "
        "trap. Forgetting to append the assistant's tool_use turn before sending tool results, "
        "which breaks the conversation. Mismatching tool_use_id between the request and the "
        "result. Omitting the iteration cap, so a confused agent loops indefinitely and burns "
        "tokens. Writing vague tool descriptions, so the model never calls the tool (or calls "
        "it at the wrong time). Trusting tool inputs from the model without validating them "
        "before execution.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "In one sentence, what distinguishes an agent from a single LLM call?",
            "answer": "An agent runs a loop where the model calls tools and your code feeds "
                      "results back until a final answer is produced.",
            "why": "The defining feature is the model-drives, code-executes loop, not a single "
                   "input-to-output mapping.",
        },
        {
            "q": "Which of these is the WEAKEST reason to build an agent?",
            "options": [
                "The task is multi-step and hard to specify in advance",
                "A single well-crafted call already solves the task",
                "Errors can be caught and recovered from",
                "The outcome justifies higher cost and latency",
            ],
            "answer": "B - A single well-crafted call already solves the task.",
            "why": "If one call suffices, an agent only adds cost, latency, and debugging "
                   "difficulty.",
        },
        {
            "q": "Why must each tool_result carry the tool_use_id from the request?",
            "answer": "So the model can match the result to the specific tool call it made.",
            "why": "The id links request and response; a mismatch breaks the loop or confuses "
                   "the model.",
        },
        {
            "q": "True or false: you should cap the number of agent loop iterations.",
            "options": ["True", "False"],
            "answer": "A - True.",
            "why": "A cap prevents a confused agent from looping forever and burning tokens.",
        },
        {
            "q": "Within a single agent run, what serves as the agent's working memory?",
            "answer": "The growing list of messages (the conversation history) passed on each "
                      "call.",
            "why": "Each call sends the full history, so prior tool results and turns are the "
                   "in-run memory; cross-run memory must be persisted separately.",
        },
        {
            "q": "What makes a good tool DESCRIPTION for the model?",
            "answer": "It states clearly WHEN to call the tool, not just what it does.",
            "why": "The model uses the description to decide whether and when to invoke the "
                   "tool, so trigger conditions matter.",
        },
    ], title="Quiz - Agents & multi-step workflows")

    page_break(doc)

    # ================================================================== #
    # TOPIC 5 - APPLICATION ARCHITECTURE
    # ================================================================== #
    h1(doc, "5. Application architecture")

    para(
        doc,
        "A demo is one script. A product is layers with clear boundaries. The standard shape "
        "of an AI app is three layers: a frontend the user interacts with, a backend that "
        "holds the logic and talks to the model, and storage that persists data and "
        "embeddings. Separating them is not bureaucracy - it is what lets you test the backend "
        "without a browser, swap the UI without touching the logic, and keep your API key on "
        "the server where the user can never see it.",
    )

    h2(doc, "The three layers and their responsibilities")
    table_from_rows(
        doc,
        ["Layer", "Responsibility", "Typical tech", "Never does"],
        [
            ["Frontend", "Collect input, display output, basic UX",
             "Streamlit, React", "Hold the API key; contain business logic"],
            ["Backend", "Prompts, model calls, guardrails, orchestration",
             "FastAPI, Python", "Render UI; assume a single user"],
            ["Storage", "Persist documents, embeddings, chat history",
             "SQLite/Postgres, a vector store", "Contain prompt logic"],
        ],
    )

    para(
        doc,
        "The cardinal rule for AI apps specifically: the model is called from the backend, "
        "never the frontend. If the browser calls Anthropic directly, your key is exposed to "
        "every user. The frontend talks to YOUR backend; your backend talks to the model. This "
        "single boundary protects your key, lets you add guardrails in one place, and means "
        "you can change models without redeploying the UI.",
    )

    h2(doc, "A clean request flow")
    numbered(doc, "User types a question in the frontend (Streamlit).")
    numbered(doc, "Frontend sends an HTTP request to your backend (FastAPI).")
    numbered(doc, "Backend retrieves relevant chunks from storage (the vector store).")
    numbered(doc, "Backend builds the grounded prompt and calls the Claude API.")
    numbered(doc, "Backend validates the output, then returns it to the frontend.")
    numbered(doc, "Frontend displays the answer (and any citations).")

    callout(
        doc, "Common mistakes",
        "Calling the model directly from the frontend, exposing your API key to every user. "
        "Putting business logic and prompts in the UI layer, so the logic cannot be tested or "
        "reused. Mixing storage queries into prompt-building code, creating a tangle that is "
        "impossible to change safely. Designing for exactly one user and one session, then "
        "discovering you cannot add login or history later. Skipping the backend entirely "
        "'just for the demo' and then never being able to harden it.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "What are the three standard layers of an AI application?",
            "answer": "Frontend, backend, and storage.",
            "why": "Each owns a distinct responsibility - UI, logic/model calls, and "
                   "persistence respectively.",
        },
        {
            "q": "Why must the model be called from the backend rather than the frontend?",
            "options": [
                "Backends are faster than browsers",
                "To keep the API key off the client and centralise guardrails",
                "The frontend cannot make HTTP requests",
                "Models only accept requests from servers",
            ],
            "answer": "B - To keep the API key off the client and centralise guardrails.",
            "why": "A frontend call would expose the key to every user; the backend is the "
                   "single trusted place for keys and policy.",
        },
        {
            "q": "True or false: prompt-building logic belongs in the storage layer.",
            "options": ["True", "False"],
            "answer": "B - False.",
            "why": "Prompts and orchestration belong in the backend; storage only persists "
                   "data and embeddings.",
        },
        {
            "q": "Name one concrete benefit of separating the backend from the frontend.",
            "answer": "You can test the backend without a UI, swap the UI without touching "
                      "logic, or change models without redeploying the frontend (any one).",
            "why": "Clear boundaries let each layer change independently.",
        },
        {
            "q": "In the standard request flow, which layer retrieves relevant chunks before "
                 "the model is called?",
            "answer": "The backend (querying the storage / vector store).",
            "why": "Retrieval is orchestration logic, so the backend performs it against "
                   "storage before building the grounded prompt.",
        },
    ], title="Quiz - Application architecture")

    page_break(doc)

    # ================================================================== #
    # TOPIC 6 - FASTAPI FOR AI APPS
    # ================================================================== #
    h1(doc, "6. FastAPI for AI apps")

    para(
        doc,
        "FastAPI is a Python web framework that turns functions into HTTP endpoints, with "
        "automatic request validation (via Pydantic) and automatic interactive docs. For AI "
        "apps it is an excellent fit: it is async-friendly (so you can stream model output "
        "without blocking), it validates incoming JSON for you, and it gives you a clean place "
        "to put your backend logic. Three capabilities matter most for this month: ordinary "
        "endpoints, streaming responses, and background tasks.",
    )

    h2(doc, "Endpoints, streaming, and background tasks")
    bullet(doc, "Endpoint: a function decorated with @app.post(...) that takes a validated "
                "request model and returns a response. This is the backbone of your backend.")
    bullet(doc, "Streaming: return a StreamingResponse that yields tokens as the model "
                "produces them, so the user sees output appear immediately instead of waiting "
                "for the whole answer. Essential for good chat UX.")
    bullet(doc, "Background task: schedule work to run AFTER the response is returned - logging "
                "the interaction, updating analytics, or kicking off a slow re-index - without "
                "making the user wait for it.")

    h2(doc, "Worked example: a chat endpoint with streaming and a background task")

    code_block(doc, r'''from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from anthropic import Anthropic

app = FastAPI()
client = Anthropic()   # reads ANTHROPIC_API_KEY from the environment

class ChatRequest(BaseModel):       # FastAPI validates the body against this
    question: str

def log_interaction(question: str) -> None:
    # Runs after the response is sent; the user never waits for it.
    with open("interactions.log", "a", encoding="utf-8") as f:
        f.write(question + "\n")

@app.post("/chat")
def chat(req: ChatRequest, background: BackgroundTasks):
    # Schedule post-response work.
    background.add_task(log_interaction, req.question)

    def token_stream():
        # Streaming avoids HTTP timeouts on long answers and improves UX.
        with client.messages.stream(
            model="claude-opus-4-8",
            max_tokens=1024,
            messages=[{"role": "user", "content": req.question}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(token_stream(), media_type="text/plain")

# Run with:  uvicorn main:app --reload
# Interactive docs are auto-generated at  http://127.0.0.1:8000/docs''')

    para(
        doc,
        "The request body is validated by ChatRequest, the answer streams back token by token "
        "via StreamingResponse, and the logging runs as a background task so it never delays "
        "the user. Visit /docs and FastAPI gives you a live test page for free.",
        size=10, color=GREY, italic=True,
    )

    callout(
        doc, "Common mistakes",
        "Blocking on a long non-streaming call and hitting an HTTP timeout - stream for long "
        "or large outputs. Doing slow work (logging, re-indexing) inline so the user waits for "
        "it instead of using a background task. Skipping the Pydantic request model and "
        "parsing raw JSON by hand, losing automatic validation. Returning the whole model "
        "object instead of a clean JSON response. Putting the API key in the code or in the "
        "request instead of reading it from the environment on the server.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "What does FastAPI give you automatically when you declare a Pydantic request "
                 "model?",
            "answer": "Automatic validation of the incoming request body (and auto-generated "
                      "interactive docs).",
            "why": "Pydantic models define and enforce the expected shape, so malformed "
                   "requests are rejected before your code runs.",
        },
        {
            "q": "Why use a StreamingResponse for long model answers?",
            "options": [
                "It is the only way to call the model",
                "It shows output as it is generated and avoids HTTP timeouts",
                "It encrypts the response",
                "It reduces the number of tokens used",
            ],
            "answer": "B - It shows output as generated and avoids HTTP timeouts.",
            "why": "Streaming improves perceived latency and keeps the connection alive for "
                   "long generations.",
        },
        {
            "q": "What is a background task used for in a FastAPI endpoint?",
            "answer": "Running work after the response is returned (e.g. logging, analytics, "
                      "re-indexing) so the user does not wait for it.",
            "why": "It decouples non-urgent work from the response path, keeping the request "
                   "fast.",
        },
        {
            "q": "True or false: the API key should be sent in the request body to the chat "
                 "endpoint.",
            "options": ["True", "False"],
            "answer": "B - False.",
            "why": "The key stays on the server, read from the environment; clients never "
                   "send or see it.",
        },
        {
            "q": "Where does FastAPI expose its auto-generated interactive documentation by "
                 "default?",
            "answer": "At the /docs path.",
            "why": "FastAPI serves a Swagger UI at /docs so you can try endpoints without "
                   "writing a client.",
        },
    ], title="Quiz - FastAPI for AI apps")

    page_break(doc)

    # ================================================================== #
    # TOPIC 7 - STREAMLIT UIs
    # ================================================================== #
    h1(doc, "7. Building UIs with Streamlit")

    para(
        doc,
        "Streamlit lets you build a usable web UI in pure Python, with no HTML, CSS, or "
        "JavaScript. You write a normal top-to-bottom script; Streamlit turns calls like "
        "st.text_input and st.button into widgets and re-runs the whole script on every "
        "interaction. For a portfolio it is ideal: a reviewer can run one command and click "
        "around your app in seconds. Understanding its execution model - the script re-runs "
        "top to bottom each time, and session_state is how you remember things between runs - "
        "is the key to using it well.",
    )

    h2(doc, "The execution model and session state")
    bullet(doc, "Re-run on interaction: every widget interaction re-executes the script from "
                "the top. Your code must be written to survive being run repeatedly.")
    bullet(doc, "session_state: a dict-like store that persists across re-runs within a "
                "session. Use it for chat history and anything else you must remember.")
    bullet(doc, "Caching: decorate expensive setup (loading an index, building a client) so it "
                "is not redone on every re-run.")

    h2(doc, "Worked example: a chat UI that calls your backend")

    code_block(doc, r'''import requests
import streamlit as st

st.title("Support Assistant")

# session_state persists across the top-to-bottom re-runs.
if "history" not in st.session_state:
    st.session_state.history = []        # list of (role, text)

# Render the existing conversation.
for role, text in st.session_state.history:
    with st.chat_message(role):
        st.write(text)

# chat_input returns the new message (or None) on each re-run.
question = st.chat_input("Ask about your account or orders...")
if question:
    st.session_state.history.append(("user", question))
    with st.chat_message("user"):
        st.write(question)

    # The UI calls YOUR backend, never the model directly.
    resp = requests.post("http://127.0.0.1:8000/chat",
                         json={"question": question}, timeout=60)
    answer = resp.text

    st.session_state.history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.write(answer)

# Run with:  streamlit run app.py''')

    para(
        doc,
        "The UI keeps the conversation in session_state, renders it on every re-run, and sends "
        "each new question to your FastAPI backend - which is where the model, the key, and the "
        "guardrails live. The frontend never touches the Claude API directly.",
        size=10, color=GREY, italic=True,
    )

    callout(
        doc, "Common mistakes",
        "Forgetting that the script re-runs top to bottom, so variables defined inline reset "
        "every interaction - use session_state for anything that must persist. Calling the "
        "Claude API directly from the Streamlit app, putting your key in the browser process "
        "and bypassing your backend. Reloading a heavy index or rebuilding a client on every "
        "re-run instead of caching it. Storing the API key in the Streamlit script. Blocking "
        "the UI on a long request with no spinner or feedback, so it looks frozen.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "What happens to a Streamlit script each time the user interacts with a "
                 "widget?",
            "answer": "The entire script re-runs from top to bottom.",
            "why": "Streamlit's model is to re-execute the script on every interaction, which "
                   "is why persistent state needs session_state.",
        },
        {
            "q": "How do you persist chat history across re-runs in Streamlit?",
            "options": ["A global variable", "st.session_state",
                        "A local file written each run", "It persists automatically"],
            "answer": "B - st.session_state.",
            "why": "session_state is the dict-like store that survives re-runs within a "
                   "session; plain variables reset.",
        },
        {
            "q": "True or false: a Streamlit frontend should call the Claude API directly for "
                 "simplicity.",
            "options": ["True", "False"],
            "answer": "B - False.",
            "why": "That would put the API key in the client and bypass the backend's "
                   "guardrails; the UI should call your backend.",
        },
        {
            "q": "Why should you cache expensive setup (like loading an index) in Streamlit?",
            "answer": "Because the script re-runs on every interaction; without caching the "
                      "expensive work repeats each time.",
            "why": "Caching avoids redoing slow setup on every re-run, keeping the app "
                   "responsive.",
        },
        {
            "q": "Name one thing you should NOT store in a Streamlit script.",
            "answer": "The API key (or any secret).",
            "why": "Secrets belong in server-side environment variables / config, never in the "
                   "frontend code.",
        },
    ], title="Quiz - Building UIs with Streamlit")

    page_break(doc)

    # ================================================================== #
    # TOPIC 8 - FILES & PDFs
    # ================================================================== #
    h1(doc, "8. Working with files & PDFs")

    para(
        doc,
        "Most knowledge bases arrive as files - PDFs, Word documents, web exports. To use them "
        "in a RAG system you must turn them into clean text, split that text into chunks, and "
        "store each chunk with its embedding so it can be retrieved later. The two design "
        "decisions that matter most are how you chunk (size and overlap) and what metadata you "
        "attach (source, page, section), because retrieval quality and citation quality both "
        "depend on them.",
    )

    h2(doc, "Parsing and chunking from first principles")
    bullet(doc, "Parse: extract text from the file. PDFs are the awkward case - layout, "
                "columns, headers, and footers can scramble the text, so inspect the output of "
                "your parser before trusting it.")
    bullet(doc, "Chunk size: large chunks carry more context but dilute relevance and cost more "
                "tokens; small chunks are precise but can lose the surrounding meaning. A few "
                "hundred to ~1000 tokens is a common starting range - then tune with your eval "
                "harness.")
    bullet(doc, "Overlap: let consecutive chunks share a little text (e.g. 10-15%) so a "
                "sentence split across a boundary still appears whole in at least one chunk.")
    bullet(doc, "Metadata: store source filename, page, and any section heading with each "
                "chunk. This is what makes citations like [refund-policy.pdf p.2] possible.")

    h2(doc, "Worked example: parse a PDF and chunk it with overlap")

    code_block(doc, r'''from pypdf import PdfReader

def pdf_to_text(path: str) -> list[dict]:
    """Extract text per page, keeping the page number as metadata."""
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": i, "text": text})
    return pages

def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    """Split into overlapping word-windows. size/overlap are in words here."""
    words = text.split()
    chunks, start = [], 0
    step = size - overlap                      # advance less than the window
    while start < len(words):
        window = words[start:start + size]
        chunks.append(" ".join(window))
        start += step
    return chunks

def ingest(path: str) -> list[dict]:
    """Produce retrieval-ready records with source metadata for citations."""
    records = []
    for page in pdf_to_text(path):
        for j, chunk in enumerate(chunk_text(page["text"])):
            records.append({
                "id": f"{path}-p{page['page']}-c{j}",
                "source": path,
                "page": page["page"],
                "text": chunk,
                # In a real app you'd compute and store an embedding here.
            })
    return records

if __name__ == "__main__":
    recs = ingest("refund-policy.pdf")
    print(f"{len(recs)} chunks; first id = {recs[0]['id']}")''')

    para(
        doc,
        "Each record carries an id, the source file, the page, and the text - everything a "
        "citation needs. The overlap (step = size - overlap) ensures a sentence straddling a "
        "boundary still lands intact in at least one chunk. Tune size and overlap with your "
        "eval harness rather than guessing once and forgetting.",
        size=10, color=GREY, italic=True,
    )

    callout(
        doc, "Common mistakes",
        "Trusting PDF text extraction without inspecting it - garbled columns and headers "
        "silently poison retrieval. Chunking with zero overlap, so answers split across a "
        "boundary are never retrieved whole. Making chunks so large that retrieval returns "
        "mostly irrelevant text and burns tokens. Dropping page/source metadata, which makes "
        "citations impossible. Picking a chunk size once and never re-tuning it against your "
        "evals. Ingesting binary or scanned PDFs (image-only) and wondering why no text comes "
        "out - those need OCR.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "Why do you add OVERLAP between consecutive chunks?",
            "answer": "So a sentence or idea split across a chunk boundary still appears whole "
                      "in at least one chunk.",
            "why": "Without overlap, content straddling a boundary may never be retrieved "
                   "intact.",
        },
        {
            "q": "What is the trade-off between large and small chunks?",
            "answer": "Large chunks carry more context but dilute relevance and cost more "
                      "tokens; small chunks are precise but can lose surrounding meaning.",
            "why": "Chunk size balances retrieval precision against preserved context; tune it "
                   "with evals.",
        },
        {
            "q": "Which metadata is essential to attach to a chunk to enable citations?",
            "options": ["The embedding model name", "Source filename and page/section",
                        "The chunk's token count", "The time of ingestion"],
            "answer": "B - Source filename and page/section.",
            "why": "Citations like [refund-policy.pdf p.2] require the source and location to "
                   "be stored with the chunk.",
        },
        {
            "q": "True or false: PDF text extraction can always be trusted without inspection.",
            "options": ["True", "False"],
            "answer": "B - False.",
            "why": "Layout, columns, headers, and footers often scramble extracted text; "
                   "always inspect the parser output.",
        },
        {
            "q": "You ingest a scanned PDF and get no text out. What is the likely cause and "
                 "fix?",
            "answer": "It is an image-only PDF; you need OCR to extract text.",
            "why": "Scanned pages contain images of text, not selectable text, so a text "
                   "parser returns nothing without OCR.",
        },
        {
            "q": "Why should chunk size and overlap be tuned with your evaluation harness?",
            "answer": "Because the best values depend on your documents and questions; the "
                      "harness lets you measure retrieval quality objectively instead of "
                      "guessing.",
            "why": "Chunking parameters trade off precision and context; only measurement "
                   "tells you what works for your data.",
        },
    ], title="Quiz - Working with files & PDFs")

    page_break(doc)

    # ================================================================== #
    # TOPIC 9 - SECRETS & CONFIGURATION
    # ================================================================== #
    h1(doc, "9. Secrets & configuration management")

    para(
        doc,
        "An API key is a credential: anyone who has it can spend your money and act as you. "
        "The entire discipline of secrets management follows from that. The rule is simple and "
        "absolute: secrets live in the environment, never in code, and never in version "
        "control. Configuration - the non-secret knobs like model name or chunk size - should "
        "also be centralised rather than scattered as magic values, so you can change "
        "behaviour without hunting through the codebase.",
    )

    h2(doc, "The .env pattern and a typed settings object")
    bullet(doc, "A .env file holds key=value pairs locally and is loaded into the environment "
                "at startup. It is for your machine and must be git-ignored.")
    bullet(doc, "A .env.example file (committed) lists the NAMES of required variables with no "
                "real values, so a new developer knows what to set.")
    bullet(doc, "Add .env to .gitignore on day one. A leaked key in git history is hard to "
                "fully remove and should be rotated immediately.")
    bullet(doc, "Centralise non-secret config (model id, chunk size, thresholds) in one "
                "settings object so values are not duplicated across files.")

    h2(doc, "Worked example: a typed settings object and a git-ignored .env")

    code_block(doc, r'''# ---------- .env  (LOCAL ONLY - listed in .gitignore, never committed) ----------
# ANTHROPIC_API_KEY=sk-ant-...your-real-key...
# MODEL=claude-opus-4-8
# CHUNK_SIZE=800

# ---------- .env.example  (committed - names only, no real values) ----------
# ANTHROPIC_API_KEY=
# MODEL=claude-opus-4-8
# CHUNK_SIZE=800

# ---------- config.py ----------
import os
from dataclasses import dataclass
from dotenv import load_dotenv      # pip install python-dotenv

load_dotenv()                        # reads .env into the process environment

@dataclass(frozen=True)
class Settings:
    # Secret: read from env, never written down in code.
    anthropic_api_key: str = os.environ["ANTHROPIC_API_KEY"]
    # Non-secret config with sensible defaults.
    model: str = os.environ.get("MODEL", "claude-opus-4-8")
    chunk_size: int = int(os.environ.get("CHUNK_SIZE", "800"))

settings = Settings()

# Elsewhere in the app, just import `settings`:
#   from config import settings
#   client = Anthropic(api_key=settings.anthropic_api_key)
#   ... or simply Anthropic(), which reads ANTHROPIC_API_KEY itself.

if __name__ == "__main__":
    # Print config WITHOUT leaking the secret.
    print("model:", settings.model, "| chunk_size:", settings.chunk_size)
    print("key loaded:", bool(settings.anthropic_api_key))   # True, not the value''')

    para(
        doc,
        "The secret enters only through the environment; config has typed defaults; and the "
        "diagnostic print confirms the key is loaded without ever displaying it. The .env file "
        "is git-ignored, and .env.example documents what to set. This is the exact pattern a "
        "reviewer expects to see.",
        size=10, color=GREY, italic=True,
    )

    callout(
        doc, "Common mistakes",
        "Hardcoding the key in source and pushing it - the single most common and most "
        "damaging mistake. Committing .env because it was not added to .gitignore. Printing or "
        "logging the key while debugging. Putting the key in a Streamlit script or sending it "
        "from the frontend. Scattering magic values (model names, chunk sizes) across many "
        "files instead of one settings object. Assuming a leaked key is harmless if the repo "
        "is private - rotate it anyway.",
        color=RED,
    )

    quiz(doc, [
        {
            "q": "State the core rule of secrets management in one sentence.",
            "answer": "Secrets live in the environment, never in code, and never in version "
                      "control.",
            "why": "A credential in code or git history can be read and abused by anyone with "
                   "access to the repo.",
        },
        {
            "q": "What is the purpose of a committed .env.example file?",
            "options": [
                "To store the real keys safely",
                "To document the NAMES of required variables without real values",
                "To back up the .env file",
                "To configure the production server automatically",
            ],
            "answer": "B - To document required variable names without real values.",
            "why": "It tells a new developer what to set while keeping actual secrets out of "
                   "the repo.",
        },
        {
            "q": "True or false: if you accidentally commit your API key but the repo is "
                 "private, you do not need to rotate it.",
            "options": ["True", "False"],
            "answer": "B - False.",
            "why": "Private repos can be cloned, shared, or made public later; a committed key "
                   "should always be rotated.",
        },
        {
            "q": "What single file entry prevents your local secrets file from being "
                 "committed?",
            "answer": "Adding .env to .gitignore.",
            "why": "Git then ignores the file, so it is never staged or pushed.",
        },
        {
            "q": "Why centralise non-secret config (model id, chunk size) in one settings "
                 "object?",
            "answer": "So values are not duplicated across files and behaviour can be changed "
                      "in one place.",
            "why": "Centralised config avoids magic values and makes changes safe and "
                   "consistent.",
        },
        {
            "q": "You want to confirm the key loaded correctly. What should you print?",
            "answer": "A boolean such as bool(api_key) - never the key value itself.",
            "why": "Printing the actual key risks leaking it into logs or screenshots.",
        },
    ], title="Quiz - Secrets & configuration management")

    page_break(doc)

    # ================================================================== #
    # TOPIC 10 - PUTTING IT TOGETHER
    # ================================================================== #
    h1(doc, "10. Putting it together - project structure & code quality")

    para(
        doc,
        "The final skill of the month is the one hiring managers actually judge: can you "
        "structure a project so that someone else can read it, run it, and trust it? A "
        "portfolio piece is not measured only by whether it works - it is measured by how "
        "quickly a reviewer understands it. That comes from a predictable layout, a clear "
        "README, small focused functions, tests, and the discipline you have practised all "
        "month around secrets and guardrails.",
    )

    h2(doc, "A predictable project layout")
    code_block(doc, r'''support-assistant/
|-- README.md            # what it is, how to run it, a screenshot/gif
|-- requirements.txt     # pinned dependencies
|-- .env.example         # required variable names (no secrets)
|-- .gitignore           # includes .env
|-- config.py            # typed settings, reads the environment
|-- app/
|   |-- backend.py       # FastAPI app: endpoints, guardrails
|   |-- agent.py         # model calls, prompts, tools
|   |-- ingest.py        # parse + chunk + embed documents
|   |-- retrieve.py      # vector search over the knowledge base
|-- ui/
|   |-- streamlit_app.py # the frontend
|-- evals/
|   |-- test_set.json    # evaluation cases (incl. escalation cases)
|   |-- run_evals.py     # the regression harness
|-- tests/
    |-- test_agent.py    # unit tests for pure logic''')

    h2(doc, "Code-quality habits that signal seniority")
    bullet(doc, "A README a stranger can follow: one paragraph on what it does, exact run "
                "commands, and a screenshot or short GIF.")
    bullet(doc, "Small functions with single responsibilities and clear names; type hints on "
                "public functions.")
    bullet(doc, "Prompts as named templates in one place, not scattered f-strings.")
    bullet(doc, "An eval harness committed alongside the code, with escalation cases included.")
    bullet(doc, "Secrets in the environment; .env git-ignored; .env.example committed.")
    bullet(doc, "Pinned dependencies in requirements.txt so the project runs the same on a "
                "reviewer's machine.")
    bullet(doc, "A few unit tests for the pure logic (parsing, chunking, scoring), even if you "
                "cannot test the live model call.")

    callout(
        doc, "Common mistakes",
        "A README that says only 'AI app' with no run instructions - the reviewer closes the "
        "tab. One enormous file with everything in it, so nothing can be found or tested. No "
        "pinned dependencies, so it breaks on someone else's machine. Committed secrets or a "
        "missing .gitignore. No evals, so you cannot demonstrate the app actually works. Dead "
        "code, commented-out experiments, and a 'final_v2_real' file left in the repo. Skipping "
        "tests entirely when the pure logic (chunking, scoring) is trivially testable.",
        color=AMBER,
    )

    quiz(doc, [
        {
            "q": "What is the single most important file for a reviewer's first impression, "
                 "and what must it contain?",
            "answer": "The README - it must say what the app does and give exact commands to "
                      "run it (ideally with a screenshot/GIF).",
            "why": "Reviewers triage on the README; if they cannot run it quickly, they move "
                   "on.",
        },
        {
            "q": "Why pin dependencies in requirements.txt?",
            "options": [
                "To make the repo smaller",
                "So the project runs the same on a reviewer's machine",
                "To hide which libraries you used",
                "It is required by FastAPI",
            ],
            "answer": "B - So the project runs the same on a reviewer's machine.",
            "why": "Pinned versions make the environment reproducible and avoid 'works on my "
                   "machine' failures.",
        },
        {
            "q": "True or false: it is fine to ship a portfolio project with no evaluation "
                 "harness as long as it runs.",
            "options": ["True", "False"],
            "answer": "B - False.",
            "why": "Evals are how you demonstrate (and defend) that the app works; their "
                   "absence is a red flag.",
        },
        {
            "q": "Give one code-quality habit that signals seniority in an AI project.",
            "answer": "Any of: small single-responsibility functions, prompts as named "
                      "templates, committed evals with escalation cases, secrets in the "
                      "environment, pinned dependencies, unit tests for pure logic.",
            "why": "These show you can build something maintainable and trustworthy, not just "
                   "a working demo.",
        },
        {
            "q": "Which pure-logic components of a RAG app are easy to unit test even without "
                 "calling the model?",
            "answer": "Parsing, chunking, retrieval scoring, and output validation logic.",
            "why": "These are deterministic functions with no model dependency, so they are "
                   "straightforward to test.",
        },
    ], title="Quiz - Project structure & code quality")

    page_break(doc)

    # ================================================================== #
    # EXERCISES
    # ================================================================== #
    h1(doc, "Exercises")
    para(
        doc,
        "Work through these in order; each builds a piece you will reuse in the projects. "
        "Commit your work to git as you go.",
    )
    numbered(doc, "Prompt template + classifier: build a reusable categorise() function for "
                  "support tickets using role + few-shot + format. Write five tickets by hand "
                  "and confirm the output is always one allowed category word.")
    numbered(doc, "Grounded answerer with escalation: implement answer_from_context() with an "
                  "ESCALATE sentinel. Feed it a question whose answer IS in the context and one "
                  "whose answer is NOT, and verify it escalates on the second.")
    numbered(doc, "Evaluation harness: assemble a test set of at least 12 cases (include at "
                  "least 4 that should escalate), write a scoring function, and add a "
                  "regression gate. Record your starting score.")
    numbered(doc, "Tool-using agent: build the lookup_order agent with a manual loop and a "
                  "max_steps cap. Add a second tool (e.g. lookup_invoice) and confirm the model "
                  "chooses the right one.")
    numbered(doc, "FastAPI backend: expose your grounded answerer as a /chat endpoint with a "
                  "Pydantic request model, streaming response, and a background logging task. "
                  "Test it from /docs.")
    numbered(doc, "Streamlit frontend: build a chat UI that calls your FastAPI backend (not the "
                  "model directly), persists history in session_state, and shows a spinner "
                  "while waiting.")
    numbered(doc, "PDF ingestion: write ingest() to parse a real PDF, chunk it with overlap, "
                  "and attach source + page metadata. Inspect the extracted text and report any "
                  "parsing problems you find.")
    numbered(doc, "Secrets hygiene audit: add config.py with a typed Settings object, create "
                  ".env and .env.example, add .env to .gitignore, and grep your whole repo to "
                  "prove no key string is committed anywhere.")

    # ================================================================== #
    # PROJECT BRIEFS
    # ================================================================== #
    h1(doc, "Project briefs")
    para(
        doc,
        "Build the flagship in full; the two shorter briefs round out your portfolio and let "
        "you show range. Each has milestones and a grading rubric. Put each in its own "
        "repository with a README a stranger can follow.",
    )

    # ----- FLAGSHIP ----- #
    h2(doc, "FLAGSHIP - AI Support-Ticket Assistant")
    para(
        doc,
        "This is the centrepiece of your portfolio and it is chosen deliberately to sell your "
        "L1 support background. You already understand support workflows, escalation, and what "
        "a good reply looks like - this project turns that domain knowledge into engineering "
        "evidence. Build it well and it becomes the project you talk about in every interview.",
        bold=False,
    )
    lead(doc, "What it does.",
         "Given a customer support ticket, the assistant: (1) retrieves relevant knowledge-base "
         "articles via RAG, (2) categorises the ticket, (3) drafts a cited reply grounded only "
         "in the retrieved articles, and (4) escalates to a human when it is not confident the "
         "answer is supported. It runs behind a Streamlit UI a support agent could actually "
         "use.")
    lead(doc, "Why it sells you.",
         "It pairs a real, relatable business problem with every skill from this month - RAG, "
         "guardrails, evaluation, architecture, FastAPI, Streamlit, ingestion, and secrets - "
         "and it is rooted in work you have genuinely done.")

    h3(doc, "Architecture")
    bullet(doc, "Frontend: Streamlit - paste a ticket, see the draft reply, the category, the "
                "citations, and an 'escalate' indicator.")
    bullet(doc, "Backend: FastAPI - retrieval, categorisation, grounded drafting, guardrails, "
                "and the escalate-if-unsure decision.")
    bullet(doc, "Storage: a vector store of knowledge-base chunks with source/page metadata, "
                "plus a log of drafted replies.")

    h3(doc, "Milestones")
    numbered(doc, "M1 - Ingest a knowledge base: parse the KB articles (incl. at least one "
                  "PDF), chunk with overlap, attach source metadata, and store embeddings.")
    numbered(doc, "M2 - Retrieval + categorisation: given a ticket, retrieve the top relevant "
                  "chunks and categorise the ticket into a fixed set.")
    numbered(doc, "M3 - Grounded cited drafting: draft a reply that uses ONLY retrieved chunks "
                  "and cites them; include the escalate-if-unsure guardrail.")
    numbered(doc, "M4 - Evaluation harness: build a labelled ticket test set (include "
                  "must-escalate tickets), score answer correctness, citation presence, and "
                  "escalation accuracy; add a regression gate.")
    numbered(doc, "M5 - FastAPI backend: expose draft-reply as a streaming endpoint with a "
                  "background task that logs each interaction.")
    numbered(doc, "M6 - Streamlit UI + polish: build the agent-facing UI, write the README "
                  "with a GIF, ensure secrets are git-ignored, and pin dependencies.")

    h3(doc, "Rubric")
    table_from_rows(
        doc,
        ["Criterion", "Weight", "Excellent", "Needs work"],
        [
            ["RAG grounding & citations", "20%",
             "Replies use only retrieved context and cite sources accurately",
             "Answers drift beyond context or omit citations"],
            ["Escalate-if-unsure guardrail", "20%",
             "Reliably escalates when the answer is unsupported",
             "Answers confidently when it should escalate"],
            ["Evaluation harness", "20%",
             "Test set incl. escalation cases; scores correctness, citation, escalation; "
             "regression gate",
             "No evals or only happy-path cases"],
            ["Architecture & separation", "15%",
             "Clean frontend/backend/storage split; key only on backend",
             "Logic in the UI or key exposed to the client"],
            ["FastAPI + Streamlit", "15%",
             "Streaming endpoint, background task, usable UI calling the backend",
             "UI calls model directly or backend missing"],
            ["Code quality & docs", "10%",
             "Clear README+GIF, pinned deps, secrets git-ignored, some tests",
             "Sparse README, committed secrets, no tests"],
        ],
    )

    # ----- SHORTER BRIEF 1 ----- #
    h2(doc, "SHORTER BRIEF 1 - Research-and-Summarise Agent")
    para(
        doc,
        "A multi-step agent that, given a question, plans and uses tools (e.g. web search and a "
        "fetch tool, or a local document search) to gather information, then writes a concise, "
        "cited summary. The point is to demonstrate genuine agentic behaviour - a planning loop "
        "with tools - and the judgement to know when an agent is warranted.",
    )
    h3(doc, "Milestones")
    numbered(doc, "M1 - Define tools (search and fetch/read) with clear, when-to-use "
                  "descriptions and input schemas.")
    numbered(doc, "M2 - Implement the agent loop with a max-steps cap and tool-input "
                  "validation.")
    numbered(doc, "M3 - Produce a cited summary; ensure every claim traces to a fetched "
                  "source.")
    numbered(doc, "M4 - Add a small eval set (does it cite? does it stay on topic? does it stop "
                  "cleanly?) and a simple UI or CLI.")
    h3(doc, "Rubric")
    table_from_rows(
        doc,
        ["Criterion", "Weight", "Excellent", "Needs work"],
        [
            ["Tool design", "25%",
             "Clear schemas and when-to-use descriptions; model calls the right tool",
             "Vague tools the model misuses or ignores"],
            ["Agent loop & safety", "25%",
             "Correct loop, max-steps cap, validated tool inputs",
             "No cap, broken loop, or unvalidated inputs"],
            ["Citations & grounding", "25%",
             "Every claim traces to a fetched source",
             "Unsourced or fabricated claims"],
            ["Evaluation & polish", "25%",
             "Eval set + clean README and runnable UI/CLI",
             "No evals; hard to run"],
        ],
    )

    # ----- SHORTER BRIEF 2 ----- #
    h2(doc, "SHORTER BRIEF 2 - Polished RAG App over a Chosen Domain")
    para(
        doc,
        "Pick a domain you find interesting - a set of recipes, a board-game rulebook, a course "
        "syllabus, a company's public docs - and build a clean, grounded question-answering app "
        "over it. The emphasis is on polish: good ingestion, accurate citations, a tidy UI, and "
        "an eval harness. This shows you can take RAG from notebook to product.",
    )
    h3(doc, "Milestones")
    numbered(doc, "M1 - Choose a domain and ingest its documents (parse, chunk with overlap, "
                  "metadata, embeddings).")
    numbered(doc, "M2 - Build grounded, cited Q&A with an 'I don't know' fallback when "
                  "retrieval is weak.")
    numbered(doc, "M3 - Build a Streamlit UI showing answers with citations; back it with a "
                  "small FastAPI (or callable backend module).")
    numbered(doc, "M4 - Add an eval set for the domain and tune chunk size/overlap against it; "
                  "write the README.")
    h3(doc, "Rubric")
    table_from_rows(
        doc,
        ["Criterion", "Weight", "Excellent", "Needs work"],
        [
            ["Ingestion quality", "25%",
             "Clean parsing, sensible chunking + overlap, metadata for citations",
             "Garbled text, no overlap, no metadata"],
            ["Grounded Q&A + fallback", "30%",
             "Cited answers; honest 'I don't know' on weak retrieval",
             "Ungrounded answers; never admits gaps"],
            ["UI & architecture", "20%",
             "Tidy UI calling a backend; key kept server-side",
             "Logic in UI or key exposed"],
            ["Evaluation & tuning", "25%",
             "Eval set; chunk size/overlap tuned with measurements; clear README",
             "No evals; parameters guessed and never checked"],
        ],
    )

    page_break(doc)

    # ================================================================== #
    # RESOURCES
    # ================================================================== #
    h1(doc, "Resources")
    para(
        doc,
        "All real, primary sources. Read the official docs first - they are the most accurate "
        "and stay current.",
    )
    bullet(doc, "Anthropic Claude developer documentation (Messages API, tool use, streaming, "
                "structured outputs): platform.claude.com/docs")
    bullet(doc, "Anthropic prompt-engineering guide (patterns, examples, the prompt library): "
                "in the Anthropic documentation under 'prompt engineering'.")
    bullet(doc, "Anthropic Python SDK (source, examples, and README): "
                "github.com/anthropics/anthropic-sdk-python")
    bullet(doc, "FastAPI official documentation (endpoints, streaming responses, background "
                "tasks, Pydantic models): fastapi.tiangolo.com")
    bullet(doc, "Streamlit official documentation (widgets, session_state, caching, chat "
                "elements): docs.streamlit.io")
    bullet(doc, "pypdf documentation (PDF text extraction): pypdf.readthedocs.io")
    bullet(doc, "python-dotenv documentation (loading .env files): "
                "github.com/theskumar/python-dotenv")
    bullet(doc, "Pydantic documentation (data validation and typed settings): "
                "docs.pydantic.dev")

    para(
        doc,
        "Build in the open: push each project to GitHub with a strong README, and write a short "
        "post explaining one decision you made (your chunking strategy, your escalation rule). "
        "Shipped, explained work is what turns a maths degree and a support internship into an "
        "AI-engineering offer.",
        italic=True, color=GREY, size=10,
    )

    doc.save(OUTFILE)
    print(f"Saved {OUTFILE}")


if __name__ == "__main__":
    build()
