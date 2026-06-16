# -*- coding: utf-8 -*-
"""
Month 3 study pack generator: LLM Application Skills.
Builds a Word .docx using the shared doc_helpers module.

Run:  python make_month_3.py
Out:  Month_3_LLM_Applications_Study_Pack.docx
"""

from doc_helpers import (
    new_doc, title_block, h1, h2, h3, para, lead, bullet, numbered,
    code_block, callout, table_from_rows, quiz, page_break,
    NAVY, ACCENT, GREY, GREEN, AMBER, RED,
)

OUTPUT = "Month_3_LLM_Applications_Study_Pack.docx"


# --------------------------------------------------------------------------
# Small section helper to keep the topic structure uniform
# --------------------------------------------------------------------------
def topic_section(doc, number, title, intro_paras, code, code_caption,
                  mistakes, quiz_questions):
    """Render one topic: heading, notes, code, common-mistakes, quiz."""
    h1(doc, f"{number}. {title}")
    for p in intro_paras:
        para(doc, p)
    if code_caption:
        lead(doc, "Code example:", code_caption)
    if code:
        code_block(doc, code)
    callout(doc, "Common mistakes", mistakes, color=RED)
    quiz(doc, quiz_questions, title=f"{title} - Quiz")
    page_break(doc)


def build():
    doc = new_doc()

    # ----------------------------------------------------------------------
    # TITLE
    # ----------------------------------------------------------------------
    title_block(
        doc,
        "Month 3 - LLM Application Skills",
        "From maths graduate to AI engineer: a 6-month study pack",
        "Study pack 3 of 6  |  Approx. 30+ hrs/week  |  Prerequisites: Months 1-2 "
        "(Python, data handling, SQL, APIs)",
    )

    para(doc,
         "Welcome to Month 3. The first two months gave you Python, data handling, SQL "
         "and HTTP APIs. This month you turn those into the single most employable skill "
         "of the moment: building real applications on top of large language models (LLMs). "
         "By the end you will understand what an LLM actually is under the hood, how to call "
         "one well, how to give it tools, how to ground it in your own documents with "
         "retrieval-augmented generation (RAG), and how to measure whether your app is any good.",
         italic=True, color=GREY)
    para(doc,
         "We use the Anthropic Claude API as the primary example throughout, because it is "
         "what powers the coding assistant you are likely already using, and because its "
         "Messages API is clean and modern. Almost everything transfers directly to other "
         "providers such as OpenAI - only the SDK names and a few field shapes change. "
         "Wherever a concept is provider-agnostic (tokens, embeddings, cosine similarity, "
         "chunking, RAG, evaluation), it is true everywhere.")
    page_break(doc)

    # ----------------------------------------------------------------------
    # LEARNING OBJECTIVES
    # ----------------------------------------------------------------------
    h1(doc, "Learning objectives")
    para(doc, "By the end of Month 3 you will be able to:")
    objectives = [
        "Explain from first principles how an LLM turns text into tokens, predicts the next "
        "token, and how the context window and sampling temperature shape its behaviour.",
        "Write clear prompts and system prompts, and reason about why a given prompt succeeds "
        "or fails.",
        "Call the Anthropic Messages API from Python with the SDK, using message roles, system "
        "prompts and environment-variable API keys correctly.",
        "Define tools (function calling) and run an agentic loop where the model calls your "
        "code and you feed results back.",
        "Stream responses token-by-token and request guaranteed-valid structured (JSON) output.",
        "Estimate and control cost, latency and token usage, including prompt caching.",
        "Explain what an embedding is, compute cosine similarity by hand, and use embeddings "
        "for semantic search.",
        "Store and query embeddings in a Chroma vector database and choose a sensible chunking "
        "strategy for documents.",
        "Design a complete retrieval-augmented generation (RAG) pipeline end to end and explain "
        "every stage.",
        "Build an evaluation set, measure answer quality, and apply concrete techniques to "
        "reduce hallucination.",
        "Decide when to use a framework such as LangChain or LlamaIndex and when to hand-roll "
        "the code yourself.",
    ]
    for o in objectives:
        bullet(doc, o)
    page_break(doc)

    # ----------------------------------------------------------------------
    # TOPIC 1 - HOW LLMs WORK
    # ----------------------------------------------------------------------
    topic_section(
        doc, 1, "How LLMs work - tokens, context, sampling",
        [
            "A large language model is, at its core, a function that takes a sequence of text "
            "and predicts what comes next. It does not 'look things up' and it has no database "
            "of facts inside it. It was trained on a very large amount of text to minimise one "
            "objective: given everything so far, assign a probability to every possible next "
            "unit of text. Everything else - answering questions, writing code, reasoning - is "
            "an emergent consequence of doing that one task extremely well.",

            "The 'unit of text' is a TOKEN, not a word or a character. A tokenizer splits text "
            "into common sub-word pieces. Roughly, one English token is about 4 characters or "
            "0.75 words, so 1,000 tokens is about 750 words. The word 'tokenizer' might be one "
            "token; an unusual word, a code identifier, or non-English text may be several. This "
            "matters because you are billed per token, limited per token, and the model 'sees' "
            "the world in tokens. As a maths graduate, think of the model as a function over a "
            "discrete vocabulary V: at each step it outputs a probability distribution over all "
            "of V (often 100k+ symbols).",

            "The CONTEXT WINDOW is the maximum number of tokens the model can attend to at once "
            "- the input you send PLUS the output it generates must fit. Modern Claude models "
            "such as claude-opus-4-8 and claude-sonnet-4-6 have very large context windows (up "
            "to 1,000,000 tokens), but bigger is not free: more context means more cost and "
            "latency, and very long contexts can dilute the model's attention. The API is "
            "STATELESS - the model remembers nothing between calls. 'Memory' in a chat is an "
            "illusion you create by resending the whole conversation history each turn.",

            "SAMPLING and TEMPERATURE control how the next token is chosen from the predicted "
            "distribution. With low temperature the model almost always picks the most probable "
            "token (deterministic, focused, good for extraction and code). With high temperature "
            "the distribution is flattened and lower-probability tokens become more likely "
            "(varied, creative, good for brainstorming). Mathematically, temperature T rescales "
            "the logits z to z/T before the softmax: T -> 0 sharpens toward the argmax, T large "
            "flattens toward uniform. Note: the newest Claude models (Opus 4.7/4.8, Fable 5) "
            "remove the temperature knob and steer behaviour through prompting and an 'effort' "
            "setting instead; older models and most other providers still expose temperature.",

            "What LLMs CAN do: fluent language, summarising, translation, classification, "
            "drafting and transforming code, following instructions, and surprisingly good "
            "step-by-step reasoning. What they CANNOT reliably do: know facts after their "
            "training cut-off, do exact arithmetic on large numbers, guarantee truth (they will "
            "'hallucinate' confident but wrong answers), or recall anything you did not put in "
            "the context. The whole rest of this month is about engineering around those limits "
            "- giving the model tools, fresh data, and grounding.",
        ],
        '# Build intuition for tokens before you ever call a model.\n'
        '# The Anthropic API can count tokens exactly for a given model.\n'
        'from anthropic import Anthropic\n\n'
        'client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment\n\n'
        'text = "Tokenization splits text into sub-word pieces."\n'
        'resp = client.messages.count_tokens(\n'
        '    model="claude-sonnet-4-6",\n'
        '    messages=[{"role": "user", "content": text}],\n'
        ')\n'
        'print(resp.input_tokens)   # exact token count for THIS model\n\n'
        '# Rule of thumb when you cannot call the API:\n'
        'approx_tokens = len(text) / 4      # ~4 chars per token\n'
        'approx_tokens_alt = len(text.split()) / 0.75  # ~0.75 words per token',
        "Counting tokens exactly with the model's own tokenizer (never estimate with "
        "OpenAI's tiktoken for a Claude model - it is the wrong tokenizer and undercounts).",
        "Treating tokens as words (they are sub-word pieces); assuming the model 'remembers' "
        "previous calls (the API is stateless - you must resend history); thinking a huge "
        "context window is free (it costs tokens and latency); expecting exact maths or "
        "post-cutoff facts without giving the model a tool or fresh data; and confusing a "
        "low temperature with 'more correct' - it only means 'more deterministic'.",
        [
            {"q": "What is a token, most precisely?",
             "options": ["A single character", "A whole word",
                         "A common sub-word piece of text", "A sentence"],
             "answer": "C",
             "why": "Tokenizers split text into frequent sub-word units; ~4 chars / ~0.75 words each."},
            {"q": "The context window limits...",
             "options": ["Only the input you send", "Only the output generated",
                         "Input plus output combined", "The number of API calls per minute"],
             "answer": "C",
             "why": "Input + generated output together must fit inside the context window."},
            {"q": "Lowering the temperature makes the model's output...",
             "options": ["More random", "More deterministic / focused",
                         "Longer", "Cheaper"],
             "answer": "B",
             "why": "Low temperature sharpens the distribution toward the most probable token."},
            {"q": "True or false: the Messages API remembers your previous conversation automatically.",
             "answer": "False",
             "why": "The API is stateless; you resend the full history each call to create 'memory'."},
            {"q": "Short answer: roughly how many words is 1,000 tokens of English?",
             "answer": "About 750 words (~4 characters per token).",
             "why": "Useful for back-of-envelope cost and context-budget estimates."},
            {"q": "Which is an LLM genuinely UNRELIABLE at on its own?",
             "options": ["Summarising a paragraph", "Exact arithmetic on large numbers",
                         "Rewriting text in a friendlier tone", "Classifying sentiment"],
             "answer": "B",
             "why": "LLMs predict likely text; exact large-number arithmetic needs a tool/calculator."},
            {"q": "Short answer: in the softmax, what does dividing logits by temperature T do as T grows large?",
             "answer": "It flattens the distribution toward uniform, making varied tokens more likely.",
             "why": "z/T with large T reduces the gaps between logits; T->0 sharpens toward the argmax."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 2 - PROMPTING FUNDAMENTALS & SYSTEM PROMPTS
    # ----------------------------------------------------------------------
    topic_section(
        doc, 2, "Prompting fundamentals & system prompts",
        [
            "A prompt is the text you give the model to steer its next-token prediction. Because "
            "the model has no goals of its own, the quality of your prompt is the single biggest "
            "lever you control. Good prompting is mostly about being explicit: state the task, "
            "the audience, the format you want, and any constraints, and give an example if the "
            "format is non-obvious.",

            "There are two distinct channels. The SYSTEM PROMPT sets durable, high-level "
            "instructions and persona ('You are a precise SQL tutor. Answer in British English. "
            "If unsure, say so.'). The USER MESSAGE carries the specific request for this turn. "
            "Keep stable instructions in the system prompt and the variable request in the user "
            "message - this separation also helps caching and reuse later. In the Anthropic API "
            "the system prompt is a separate top-level 'system' parameter, not a message with a "
            "role.",

            "Useful, evidence-based techniques: (1) Be specific about output format - ask for "
            "'a JSON object with keys name and email' rather than 'the details'. (2) Give "
            "few-shot examples - show one or two input/output pairs and the model imitates them. "
            "(3) Ask for step-by-step reasoning on hard problems ('think through it before "
            "answering') - this 'chain of thought' measurably improves accuracy on multi-step "
            "tasks. (4) Tell the model what to do when it does not know ('If the answer is not in "
            "the provided text, reply: not found') to curb hallucination. (5) Put the long, "
            "reusable context first and the short, varying question last.",

            "A note on modern models: the newest Claude models follow instructions very "
            "literally, so aggressive shouting ('CRITICAL!! YOU MUST!!') tends to backfire and "
            "cause over-triggering. Prefer calm, precise instructions. Tune the prompt to the "
            "behaviour you actually want and test it, rather than piling on emphasis.",
        ],
        'from anthropic import Anthropic\n\n'
        'client = Anthropic()  # ANTHROPIC_API_KEY comes from the environment\n\n'
        'SYSTEM = (\n'
        '    "You are a precise data-extraction assistant. "\n'
        '    "Reply ONLY with the requested JSON and nothing else. "\n'
        '    "If a field is missing in the text, use null."\n'
        ')\n\n'
        'msg = client.messages.create(\n'
        '    model="claude-sonnet-4-6",\n'
        '    max_tokens=1024,\n'
        '    system=SYSTEM,                       # durable instructions / persona\n'
        '    messages=[\n'
        '        {"role": "user", "content": (\n'
        '            "Extract name and email as JSON keys name, email.\\n"\n'
        '            "Text: Contact Dr Amina Yusuf at amina@uni.ac.uk for details."\n'
        '        )},\n'
        '    ],\n'
        ')\n'
        'print(msg.content[0].text)',
        "A system prompt holding durable rules, with the variable request in the user message.",
        "Putting durable instructions in the user message instead of the system prompt; being "
        "vague about the output format and then complaining the output varies; over-emphasising "
        "with CAPS and exclamation marks (modern models over-trigger on this); forgetting to "
        "tell the model what to do when the answer is absent (so it invents one); and burying the "
        "actual question under a wall of context with no clear instruction.",
        [
            {"q": "What is the system prompt best used for?",
             "options": ["The single varying question for this turn",
                         "Durable instructions, persona and constraints",
                         "Storing the API key", "The model's reply"],
             "answer": "B",
             "why": "System = stable instructions/persona; user message = the specific request."},
            {"q": "Which technique most directly reduces hallucination?",
             "options": ["Raising temperature",
                         "Telling the model to say 'not found' when the answer is absent",
                         "Asking for a longer answer", "Using more emojis"],
             "answer": "B",
             "why": "Giving an explicit 'I don't know' escape hatch stops the model inventing answers."},
            {"q": "Few-shot prompting means...",
             "options": ["Calling the API a few times",
                         "Showing one or two example input/output pairs",
                         "Using a small model", "Limiting max_tokens"],
             "answer": "B",
             "why": "Examples in the prompt let the model imitate the desired pattern/format."},
            {"q": "True or false: in the Anthropic API the system prompt is a message with role 'system'.",
             "answer": "False",
             "why": "It is a separate top-level 'system' parameter, not a message role (except the "
                    "newer mid-conversation system-message beta)."},
            {"q": "Short answer: why ask a model to 'think step by step' on a hard problem?",
             "answer": "Chain-of-thought reasoning measurably improves accuracy on multi-step tasks.",
             "why": "Generating intermediate steps conditions the final answer on better reasoning."},
            {"q": "Where should the long, reusable context generally go relative to the short question?",
             "options": ["After the question", "Before the question",
                         "It does not matter", "In the system prompt only"],
             "answer": "B",
             "why": "Stable context first, varying question last - clearer for the model and better for caching."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 3 - CALLING THE LLM API
    # ----------------------------------------------------------------------
    topic_section(
        doc, 3, "Calling the LLM API (Anthropic Messages API)",
        [
            "Everything in the Anthropic API goes through a single endpoint: Messages "
            "(POST /v1/messages). You send a model id, a max_tokens limit, an optional system "
            "prompt, and a list of messages; you get back a structured response. The official "
            "Python SDK ('anthropic', installed with pip) wraps this so you write Python objects "
            "rather than raw HTTP.",

            "SETUP. Install with 'pip install anthropic'. Never hard-code your API key in source "
            "- set it as the environment variable ANTHROPIC_API_KEY and construct the client with "
            "a bare Anthropic(); the SDK reads the key for you. This keeps secrets out of your git "
            "history and lets you swap keys per environment. (OpenAI is the same idea: "
            "'pip install openai', set OPENAI_API_KEY, then OpenAI().)",

            "MESSAGE ROLES. The conversation is a list of dicts, each with a 'role' and "
            "'content'. The roles are 'user' (you / the human) and 'assistant' (the model). The "
            "first message must be 'user', and turns generally alternate user, assistant, user, "
            "and so on. To hold a multi-turn conversation you APPEND the model's previous reply "
            "to the list and send the whole list again - because the API is stateless, this "
            "resend is what creates continuity.",

            "THE RESPONSE. The reply's .content is a LIST of typed blocks, not a plain string. "
            "For a simple text answer the text lives in content[0].text, but get into the habit "
            "of checking each block's .type, because tool use and reasoning come back as other "
            "block types. The response also carries .usage (input/output token counts) and a "
            ".stop_reason telling you why generation ended (end_turn, max_tokens, tool_use, etc.). "
            "Wrap calls in try/except for the SDK's typed errors (RateLimitError, "
            "AuthenticationError, APIStatusError) rather than matching on error strings.",
        ],
        '# pip install anthropic\n'
        '# export ANTHROPIC_API_KEY=sk-ant-...   (never hard-code the key)\n'
        'import anthropic\n\n'
        'client = anthropic.Anthropic()   # key read from ANTHROPIC_API_KEY\n\n'
        'history = [{"role": "user", "content": "My name is Dami."}]\n'
        'r1 = client.messages.create(\n'
        '    model="claude-sonnet-4-6", max_tokens=512,\n'
        '    system="You are a friendly tutor.",\n'
        '    messages=history,\n'
        ')\n'
        'reply = next(b.text for b in r1.content if b.type == "text")\n'
        'history.append({"role": "assistant", "content": reply})\n\n'
        '# Second turn: resend the whole history so the model "remembers".\n'
        'history.append({"role": "user", "content": "What is my name?"})\n'
        'r2 = client.messages.create(\n'
        '    model="claude-sonnet-4-6", max_tokens=512, messages=history,\n'
        ')\n'
        'print(r2.content[0].text)          # -> mentions "Dami"\n'
        'print(r2.usage.input_tokens, r2.usage.output_tokens, r2.stop_reason)',
        "A two-turn conversation showing env-var keys, message roles and resent history.",
        "Hard-coding the API key in the source (leak it once, rotate forever) instead of using "
        "an environment variable; assuming response.content is a string (it is a list of blocks "
        "- use content[0].text or iterate by .type); starting the messages list with an "
        "'assistant' message or with non-alternating roles (returns a 400); and forgetting to "
        "append the assistant reply before the next turn, so the model 'forgets' everything.",
        [
            {"q": "How should you supply your API key to the SDK?",
             "options": ["Hard-code it in the script", "Pass it on the command line each run",
                         "Set the ANTHROPIC_API_KEY environment variable",
                         "Put it in a public README"],
             "answer": "C",
             "why": "Env vars keep secrets out of source/git and let you swap keys per environment."},
            {"q": "The two message roles in a basic Messages API call are:",
             "options": ["system and tool", "user and assistant",
                         "human and bot", "prompt and completion"],
             "answer": "B",
             "why": "Conversations alternate 'user' and 'assistant'; system is a separate parameter."},
            {"q": "response.content is...",
             "options": ["A plain string", "A list of typed content blocks",
                         "A pandas DataFrame", "A file handle"],
             "answer": "B",
             "why": "Iterate blocks and check .type; text is in a text block's .text."},
            {"q": "What creates 'memory' across turns with a stateless API?",
             "answer": "Resending the full conversation history (appending each prior reply) on every call.",
             "why": "The server stores nothing between calls; continuity is client-side."},
            {"q": "True or false: the first message in the list may have role 'assistant'.",
             "answer": "False",
             "why": "The first message must be 'user'; roles then alternate."},
            {"q": "Short answer: which response field tells you WHY generation stopped?",
             "answer": "stop_reason (e.g. end_turn, max_tokens, tool_use).",
             "why": "Branch on it - e.g. raise max_tokens if you hit the limit, or run a tool on tool_use."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 4 - TOOL / FUNCTION CALLING
    # ----------------------------------------------------------------------
    topic_section(
        doc, 4, "Tool / function calling",
        [
            "On its own a model can only produce text. TOOL USE (also called function calling) "
            "lets the model ask YOUR code to do something - look up the weather, query a "
            "database, do exact arithmetic, hit an API - and then continue using the result. "
            "This is how you give an LLM fresh data and real actions, and it is the foundation of "
            "'agents'.",

            "You define each tool with a name, a clear description (the model reads this to decide "
            "when to call it - be prescriptive about WHEN), and an input_schema written in JSON "
            "Schema describing the arguments. You pass the list of tools alongside your messages. "
            "The model does NOT run your code: when it wants a tool, it returns a content block of "
            "type 'tool_use' containing the tool name and the arguments it chose. Your program "
            "checks stop_reason == 'tool_use', executes the matching function, and sends the "
            "result back as a 'tool_result' block (carrying the same tool_use_id) in a new user "
            "message.",

            "This forms an AGENTIC LOOP: call the model; if it wants a tool, run it, append the "
            "result, call again; repeat until stop_reason is 'end_turn'. The model may request "
            "several tools at once, and may chain several rounds. The Anthropic SDK also offers a "
            "higher-level 'tool runner' that automates this loop, but you should understand the "
            "manual version first because it is where you put approval gates, logging and error "
            "handling.",

            "Design tips: keep the tool set small and focused; write descriptions that say when to "
            "use the tool, not just what it does; validate the arguments inside your function "
            "before acting (the model can pass bad input); and return errors as a tool_result "
            "with is_error set to true and a helpful message, so the model can recover rather "
            "than crash.",
        ],
        'import anthropic\nclient = anthropic.Anthropic()\n\n'
        'tools = [{\n'
        '    "name": "get_weather",\n'
        '    "description": "Get the current weather for a city. Call this whenever the user "\n'
        '                   "asks about current weather.",\n'
        '    "input_schema": {\n'
        '        "type": "object",\n'
        '        "properties": {"city": {"type": "string", "description": "City name"}},\n'
        '        "required": ["city"],\n'
        '    },\n'
        '}]\n\n'
        'def get_weather(city):\n'
        '    return f"18C and cloudy in {city}"   # your real implementation here\n\n'
        'messages = [{"role": "user", "content": "What is the weather in Accra?"}]\n'
        'resp = client.messages.create(model="claude-sonnet-4-6", max_tokens=1024,\n'
        '                              tools=tools, messages=messages)\n\n'
        'if resp.stop_reason == "tool_use":\n'
        '    messages.append({"role": "assistant", "content": resp.content})\n'
        '    results = []\n'
        '    for block in resp.content:\n'
        '        if block.type == "tool_use":\n'
        '            out = get_weather(**block.input)        # run YOUR code\n'
        '            results.append({"type": "tool_result",\n'
        '                            "tool_use_id": block.id, "content": out})\n'
        '    messages.append({"role": "user", "content": results})\n'
        '    final = client.messages.create(model="claude-sonnet-4-6", max_tokens=1024,\n'
        '                                   tools=tools, messages=messages)\n'
        '    print(final.content[0].text)',
        "Defining a tool, detecting tool_use, running your code, and returning a tool_result.",
        "Expecting the API to RUN your function (it never does - it only asks; you execute and "
        "return the result); forgetting to append the assistant's tool_use block before sending "
        "the tool_result; mismatching or omitting the tool_use_id linking request and result; "
        "writing vague tool descriptions so the model never calls the tool (or calls it for the "
        "wrong thing); and not validating the model-supplied arguments before acting on them.",
        [
            {"q": "When the model wants a tool, what does the API return?",
             "options": ["It runs your function and returns its value",
                         "A content block of type 'tool_use' with the name and arguments",
                         "An error", "A plain-text apology"],
             "answer": "B",
             "why": "The model only requests; your code executes and returns a tool_result."},
            {"q": "The agentic loop ends when stop_reason is...",
             "options": ["tool_use", "end_turn", "max_tokens", "refusal"],
             "answer": "B",
             "why": "end_turn means the model finished and wants no more tools."},
            {"q": "What links a tool_result back to its request?",
             "options": ["The tool name only", "The tool_use_id",
                         "The message index", "The timestamp"],
             "answer": "B",
             "why": "Each tool_result must carry the matching tool_use_id from the tool_use block."},
            {"q": "Where do you define a tool's arguments?",
             "options": ["In the system prompt", "In a JSON Schema input_schema",
                         "In a Python docstring only", "Nowhere - the model guesses"],
             "answer": "B",
             "why": "input_schema (JSON Schema) describes the expected arguments and which are required."},
            {"q": "True or false: a single model response can request several tools at once.",
             "answer": "True",
             "why": "The model can emit multiple tool_use blocks; execute all and return all results."},
            {"q": "Short answer: how should you return a failed tool execution to the model?",
             "answer": "As a tool_result with is_error=true and a helpful error message.",
             "why": "This lets the model adapt or try a different approach instead of producing garbage."},
            {"q": "Why be 'prescriptive about WHEN' in a tool description?",
             "options": ["It is required syntax", "It improves the model's decision to call the right tool",
                         "It reduces token cost", "It encrypts the tool"],
             "answer": "B",
             "why": "Modern models reach for tools more conservatively; trigger conditions raise should-call accuracy."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 5 - STREAMING & STRUCTURED OUTPUT
    # ----------------------------------------------------------------------
    topic_section(
        doc, 5, "Streaming responses & structured output (JSON)",
        [
            "STREAMING sends the response back token-by-token as it is generated, instead of "
            "waiting for the whole thing. Two reasons to use it. First, user experience: text "
            "appears immediately, the way a chat UI feels alive. Second, robustness: long "
            "generations can otherwise exceed an HTTP timeout - streaming keeps the connection "
            "busy. As a rule, stream whenever you ask for a large max_tokens or expect a long "
            "answer. The SDK's messages.stream() context manager exposes a simple text_stream "
            "iterator, and a get_final_message() call to retrieve the full assembled message and "
            "its usage afterwards.",

            "STRUCTURED OUTPUT solves a different problem: when your program needs to PARSE the "
            "model's answer, free-form prose is fragile. You want guaranteed-valid JSON matching "
            "a schema you defined. The naive approach - 'please reply in JSON' in the prompt - "
            "works most of the time but occasionally returns prose, a code fence, or a trailing "
            "comma that breaks json.loads. The robust approach is to constrain the output: with "
            "the Anthropic API you pass an output_config with a json_schema (or use the SDK's "
            "messages.parse() with a Pydantic model, which validates for you). Strict tool use "
            "(strict=true on a tool) similarly guarantees the tool arguments match the schema.",

            "Define your schema with additionalProperties set to false and list the required "
            "fields, so the model cannot wander off-format. The first request with a new schema "
            "incurs a small one-time compilation cost; afterwards it is cached. Structured output "
            "is the bridge between the fuzzy world of language and the strict world of your code, "
            "databases and downstream functions.",

            "A practical pattern: stream the visible answer to the user for responsiveness, but "
            "use a separate constrained call (or a tool) when you need machine-readable data. Do "
            "not try to parse a half-streamed buffer as JSON mid-flight - wait for the block to "
            "complete, or use the dedicated structured-output path.",
        ],
        '# --- Streaming text to the user ---------------------------------\n'
        'import anthropic\nclient = anthropic.Anthropic()\n\n'
        'with client.messages.stream(\n'
        '    model="claude-sonnet-4-6", max_tokens=1024,\n'
        '    messages=[{"role": "user", "content": "Write two sentences about Accra."}],\n'
        ') as stream:\n'
        '    for text in stream.text_stream:\n'
        '        print(text, end="", flush=True)     # appears token by token\n'
        '    final = stream.get_final_message()        # full message + usage\n\n'
        '# --- Guaranteed-valid JSON via a schema -------------------------\n'
        'resp = client.messages.create(\n'
        '    model="claude-sonnet-4-6", max_tokens=512,\n'
        '    messages=[{"role": "user",\n'
        '               "content": "Extract: Jane Doe, jane@co.com, Enterprise plan."}],\n'
        '    output_config={"format": {"type": "json_schema", "schema": {\n'
        '        "type": "object",\n'
        '        "properties": {"name": {"type": "string"},\n'
        '                       "email": {"type": "string"},\n'
        '                       "plan": {"type": "string"}},\n'
        '        "required": ["name", "email", "plan"],\n'
        '        "additionalProperties": False,\n'
        '    }}},\n'
        ')\n'
        'import json\n'
        'data = json.loads(next(b.text for b in resp.content if b.type == "text"))\n'
        'print(data["email"])',
        "Streaming text token-by-token, and a separate call constrained to a JSON schema.",
        "Relying on 'please answer in JSON' in the prompt and then crashing on the one reply that "
        "is wrapped in a code fence or has a stray comma - use a schema/structured output instead; "
        "trying to json.loads a partially streamed buffer; forgetting additionalProperties:false "
        "and required, so the shape drifts; and not streaming a large/long generation, then "
        "hitting an HTTP timeout.",
        [
            {"q": "A primary practical reason to stream a long response is...",
             "options": ["It is cheaper per token", "It avoids HTTP timeouts and feels responsive",
                         "It uses fewer tokens", "It improves factual accuracy"],
             "answer": "B",
             "why": "Streaming keeps the connection busy (no timeout) and shows text immediately."},
            {"q": "The most reliable way to get machine-parseable JSON is...",
             "options": ["Ask nicely in the prompt", "Raise the temperature",
                         "Constrain output with a JSON schema (structured output)",
                         "Lower max_tokens"],
             "answer": "C",
             "why": "A schema/structured-output guarantees valid, parseable JSON; prose requests can drift."},
            {"q": "Why set additionalProperties to false in your schema?",
             "answer": "So the model cannot add unexpected keys and the output stays in the exact shape.",
             "why": "It locks the object shape to your defined properties."},
            {"q": "After streaming, how do you get the full message and token usage?",
             "options": ["You cannot", "stream.get_final_message()",
                         "Re-call the API", "Read response.content"],
             "answer": "B",
             "why": "get_final_message() returns the assembled message with usage after the stream ends."},
            {"q": "True or false: you should json.loads the buffer while it is still streaming.",
             "answer": "False",
             "why": "Partial JSON is invalid; wait for completion or use the structured-output path."},
            {"q": "Short answer: name one thing structured output bridges.",
             "answer": "The fuzzy language world and the strict world of code/databases/functions.",
             "why": "It turns model text into reliably typed data your program can consume."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 6 - COST, LATENCY & TOKEN MANAGEMENT
    # ----------------------------------------------------------------------
    topic_section(
        doc, 6, "Cost, latency & token management",
        [
            "You are billed PER TOKEN, separately for input (the prompt you send) and output (what "
            "the model generates), and output is typically several times more expensive than "
            "input. So cost is roughly: input_tokens * input_price + output_tokens * output_price, "
            "priced per million tokens. For example, claude-sonnet-4-6 is around $3 per million "
            "input tokens and $15 per million output tokens; claude-opus-4-8 is around $5 and $25; "
            "the small, fast claude-haiku-4-5 is around $1 and $5. (Always confirm current prices "
            "- they change.) Every response's .usage object reports exactly how many tokens you "
            "used, which is your ground truth for billing.",

            "MODEL CHOICE is the biggest lever. Use a small fast model (Haiku) for simple, "
            "high-volume work like classification or routing; a balanced model (Sonnet) for most "
            "production tasks; and a top model (Opus) only when the task genuinely needs the extra "
            "capability. Do not reflexively reach for the most powerful model - it is the most "
            "expensive and the slowest.",

            "PROMPT CACHING dramatically cuts the cost of repeated context. If many requests share "
            "a large fixed prefix (a long system prompt, a big document, few-shot examples), you "
            "can cache that prefix so subsequent requests pay roughly one-tenth the input price "
            "for the cached part. The rule is a strict PREFIX MATCH: any byte change anywhere in "
            "the prefix invalidates the cache. So keep stable content first and frozen (never put "
            "a timestamp or a per-request id in your system prompt), and put the varying question "
            "after the cached section. Verify it works by checking usage.cache_read_input_tokens "
            "is non-zero on repeat calls.",

            "LATENCY is dominated by OUTPUT length - the model emits tokens roughly one at a time, "
            "so a 2,000-token answer takes far longer than a 200-token one. Reduce latency by "
            "asking for shorter answers, picking a faster model, streaming (so the user sees "
            "progress), and caching the input prefix. The Batches API offers ~50% cheaper "
            "processing for non-urgent bulk jobs. Always set a sensible max_tokens, count tokens "
            "before sending big inputs, and never silently truncate content to fit - chunk or "
            "summarise it instead.",
        ],
        'import anthropic\nclient = anthropic.Anthropic()\n\n'
        '# Estimate cost from exact usage after a call.\n'
        'resp = client.messages.create(\n'
        '    model="claude-sonnet-4-6", max_tokens=300,\n'
        '    messages=[{"role": "user", "content": "Summarise the water cycle in 3 lines."}],\n'
        ')\n'
        'IN_PRICE, OUT_PRICE = 3.0, 15.0          # $ per 1M tokens (confirm current)\n'
        'cost = (resp.usage.input_tokens  * IN_PRICE +\n'
        '        resp.usage.output_tokens * OUT_PRICE) / 1_000_000\n'
        'print(f"${cost:.6f}")\n\n'
        '# Prompt caching: cache a large, STABLE prefix; keep the question after it.\n'
        'big_doc = open("handbook.txt").read()      # reused across many questions\n'
        'resp2 = client.messages.create(\n'
        '    model="claude-sonnet-4-6", max_tokens=512,\n'
        '    system=[{"type": "text", "text": big_doc,\n'
        '             "cache_control": {"type": "ephemeral"}}],\n'
        '    messages=[{"role": "user", "content": "What is the refund policy?"}],\n'
        ')\n'
        'print(resp2.usage.cache_read_input_tokens)  # >0 on repeat => cache hit',
        "Computing exact cost from usage, and caching a large stable prefix to cut input cost.",
        "Defaulting to the most powerful (and most expensive) model for everything; putting a "
        "timestamp, UUID or other per-request value into a cached prefix and silently destroying "
        "every cache hit; guessing token counts with tiktoken on a Claude model; ignoring that "
        "OUTPUT tokens cost more and dominate latency; and truncating inputs to fit the window "
        "instead of chunking or summarising.",
        [
            {"q": "Which is usually more expensive per token?",
             "options": ["Input tokens", "Output tokens",
                         "They are always equal", "Cached tokens"],
             "answer": "B",
             "why": "Output is typically several times the input price and also drives latency."},
            {"q": "What instantly invalidates a cached prefix?",
             "options": ["A new question after it", "Any byte change inside the prefix",
                         "Using streaming", "A different max_tokens"],
             "answer": "B",
             "why": "Caching is a strict prefix match; any change in the prefix is a cache miss."},
            {"q": "For simple, high-volume classification you should prefer...",
             "options": ["The largest model", "A small fast model (e.g. Haiku)",
                         "Always Opus", "No model at all"],
             "answer": "B",
             "why": "Match model capability to task; small models are cheaper and faster for easy work."},
            {"q": "What field gives you the exact tokens used for billing?",
             "answer": "response.usage (input_tokens and output_tokens).",
             "why": "It is the ground-truth count for cost calculations."},
            {"q": "Latency is dominated by...",
             "options": ["Input length", "Output length",
                         "Number of tools", "The API key"],
             "answer": "B",
             "why": "Tokens are emitted roughly one at a time, so longer outputs take longer."},
            {"q": "True or false: a UUID in your system prompt is harmless for caching.",
             "answer": "False",
             "why": "It changes the prefix every request, so the cache never hits."},
            {"q": "Short answer: what does the Batches API trade for ~50% lower cost?",
             "answer": "Immediacy - results are asynchronous (up to ~24h) rather than real-time.",
             "why": "Good for bulk, non-latency-sensitive jobs."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 7 - EMBEDDINGS
    # ----------------------------------------------------------------------
    topic_section(
        doc, 7, "Embeddings - semantic similarity & the maths",
        [
            "An EMBEDDING is a vector of numbers (typically a few hundred to a couple of thousand "
            "dimensions) that represents the MEANING of a piece of text. An embedding model is "
            "trained so that texts with similar meaning map to vectors that point in similar "
            "directions, even if they share no words. 'How do I reset my password?' and 'I forgot "
            "my login credentials' end up close together; 'the cat sat on the mat' ends up far "
            "away. This is the engine behind semantic search and RAG.",

            "Because you have a maths degree, the geometry will feel natural. Each text becomes a "
            "point (equivalently, a direction) in a high-dimensional space R^n. Similarity is "
            "measured by COSINE SIMILARITY: the cosine of the angle between two vectors a and b, "
            "cos(theta) = (a . b) / (||a|| ||b||), where a . b is the dot product and ||a|| is the "
            "Euclidean norm. It ranges from -1 (opposite) through 0 (unrelated/orthogonal) to +1 "
            "(identical direction). We use the angle, not the raw distance, because embedding "
            "magnitude often encodes length or frequency rather than meaning; direction captures "
            "meaning. If you L2-normalise every vector to unit length, cosine similarity reduces "
            "to a plain dot product, which is why search libraries normalise first and then just "
            "take dot products.",

            "Workflow: pick an embedding model (Anthropic recommends a partner such as Voyage AI; "
            "OpenAI and open-source models like sentence-transformers also work), embed your "
            "documents once and store the vectors, then at query time embed the question and find "
            "the stored vectors with the highest cosine similarity - those are the most "
            "semantically relevant passages. Crucially, use the SAME embedding model for documents "
            "and queries; vectors from different models live in different, incompatible spaces.",

            "A subtlety: embeddings capture semantic similarity, not truth or recency. Two "
            "sentences can be close because they are about the same topic even if one is wrong. "
            "Embeddings find RELEVANT text; it is then the LLM's job (and your evaluation's job) "
            "to use that text faithfully. Keep that division of labour clear.",
        ],
        'import numpy as np\n\n'
        'def cosine_similarity(a, b):\n'
        '    a, b = np.asarray(a, float), np.asarray(b, float)\n'
        '    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))\n\n'
        '# Toy 3-D vectors standing in for real embeddings:\n'
        'password_reset = [0.90, 0.10, 0.05]\n'
        'forgot_login   = [0.88, 0.15, 0.02]   # similar meaning -> close direction\n'
        'cat_on_mat     = [0.02, 0.30, 0.95]   # unrelated -> different direction\n\n'
        'print(cosine_similarity(password_reset, forgot_login))  # ~0.99 (very similar)\n'
        'print(cosine_similarity(password_reset, cat_on_mat))    # ~0.13 (unrelated)\n\n'
        '# Real embeddings come from an embedding model, e.g. Voyage AI:\n'
        '#   import voyageai; vo = voyageai.Client()\n'
        '#   vecs = vo.embed(["...text..."], model="voyage-3").embeddings\n'
        '# Use the SAME model for documents and queries.',
        "Cosine similarity in NumPy, with toy vectors showing related vs unrelated meanings.",
        "Using a different embedding model for documents than for queries (their spaces do not "
        "match, so similarity is meaningless); comparing with Euclidean distance when the vectors "
        "are not normalised (cosine is the safe default); assuming 'similar' means 'true' or "
        "'up to date' (it only means semantically related); and forgetting to store the original "
        "text alongside the vector, so you retrieve a number with no passage to show.",
        [
            {"q": "An embedding represents...",
             "options": ["The exact words of a text", "The meaning of a text as a vector",
                         "The file size", "The token count"],
             "answer": "B",
             "why": "Similar meanings map to vectors pointing in similar directions."},
            {"q": "Cosine similarity of two unrelated (orthogonal) vectors is about...",
             "options": ["-1", "0", "+1", "Infinity"],
             "answer": "B",
             "why": "Orthogonal vectors have a 90-degree angle, cos(90) = 0."},
            {"q": "If vectors are L2-normalised to unit length, cosine similarity equals...",
             "options": ["Their Euclidean distance", "Their dot product",
                         "Their sum", "Their cross product"],
             "answer": "B",
             "why": "With ||a||=||b||=1 the denominator is 1, so cosine = a . b."},
            {"q": "Why must documents and the query use the same embedding model?",
             "answer": "Different models produce incompatible vector spaces, making similarity meaningless.",
             "why": "Only within one model's space are distances/angles comparable."},
            {"q": "True or false: a high cosine similarity guarantees the matched text is factually correct.",
             "answer": "False",
             "why": "Embeddings capture relevance/topic, not truth or recency."},
            {"q": "Short answer: write the cosine similarity formula for vectors a and b.",
             "answer": "cos(theta) = (a . b) / (||a|| * ||b||).",
             "why": "Dot product over the product of the Euclidean norms; ranges -1..+1."},
            {"q": "Cosine uses the ANGLE rather than raw distance mainly because...",
             "options": ["It is faster", "Magnitude often encodes length/frequency, not meaning",
                         "Distance is undefined in high dimensions", "It avoids negatives"],
             "answer": "B",
             "why": "Direction captures meaning; magnitude can reflect document length or word frequency."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 8 - VECTOR DATABASES WITH CHROMA
    # ----------------------------------------------------------------------
    topic_section(
        doc, 8, "Vector databases with Chroma",
        [
            "Once you have embeddings you need somewhere to store them and a fast way to find the "
            "nearest ones to a query. For a handful of vectors you could brute-force the cosine "
            "similarity against every stored vector in NumPy. But with thousands or millions of "
            "vectors that is slow, so we use a VECTOR DATABASE, which indexes vectors for "
            "approximate nearest-neighbour (ANN) search - returning the top matches in "
            "milliseconds. Chroma is a popular, beginner-friendly open-source choice that runs "
            "in-process (no server to set up) and can persist to disk.",

            "The core unit in Chroma is a COLLECTION: a named set of items, where each item has an "
            "id, a document (the original text), an embedding (the vector), and optional metadata "
            "(e.g. source filename, page number). You add items with collection.add(...) and "
            "search with collection.query(...). Chroma can even embed the text for you with a "
            "default model, but in a real RAG app you usually pass your own embeddings (from the "
            "same model you use for queries) for full control.",

            "Querying returns the top-k most similar documents, plus their ids, metadata and "
            "distances. The metadata is what lets you build CITATIONS later - you retrieve not "
            "just the text but where it came from. You can also filter by metadata (a 'where' "
            "clause) to, say, restrict the search to one document or one date range, combining "
            "semantic search with structured filtering.",

            "Persist the collection to disk (PersistentClient with a path) so you do not re-embed "
            "everything on every run - embedding is the slow, costly step, so do it once and "
            "reuse. Keep the original text stored alongside the vector; the vector alone is "
            "useless to a human or to the LLM, which needs the actual passage to answer from.",
        ],
        '# pip install chromadb\n'
        'import chromadb\n\n'
        'client = chromadb.PersistentClient(path="./chroma_store")  # persists to disk\n'
        'col = client.get_or_create_collection("handbook")\n\n'
        '# Add documents (here Chroma embeds with its default model; in RAG you can\n'
        '# instead pass embeddings=[...] computed with your own embedding model).\n'
        'col.add(\n'
        '    ids=["doc1", "doc2", "doc3"],\n'
        '    documents=[\n'
        '        "To reset your password, click Forgot password on the login page.",\n'
        '        "Refunds are issued within 14 days of purchase.",\n'
        '        "Our office hours are 9am to 5pm, Monday to Friday.",\n'
        '    ],\n'
        '    metadatas=[{"source": "auth.md"}, {"source": "billing.md"}, {"source": "info.md"}],\n'
        ')\n\n'
        'res = col.query(query_texts=["I forgot my login"], n_results=2)\n'
        'print(res["documents"][0])    # most similar passages, top-2\n'
        'print(res["metadatas"][0])    # their sources -> used for citations',
        "Adding documents with metadata to a persistent Chroma collection and querying top-k.",
        "Re-embedding and re-adding everything on every run instead of persisting the collection; "
        "embedding documents with one model and querying with another; storing only vectors and "
        "losing the original text (then having nothing to show the user or feed the LLM); "
        "forgetting metadata, so you cannot cite sources or filter; and asking for far too many "
        "results (huge n_results) and stuffing irrelevant noise into the prompt.",
        [
            {"q": "Why use a vector database instead of brute-force NumPy at scale?",
             "options": ["It is the only way to compute cosine",
                         "It indexes vectors for fast approximate nearest-neighbour search",
                         "It writes the prompt for you", "It stores API keys"],
             "answer": "B",
             "why": "ANN indexes return top matches in milliseconds across millions of vectors."},
            {"q": "In Chroma, a collection item typically holds...",
             "options": ["Only a vector", "id, document text, embedding and optional metadata",
                         "Only the source filename", "The API response"],
             "answer": "B",
             "why": "Storing the text + metadata is what enables answers and citations."},
            {"q": "What is the metadata mainly used for in a RAG app?",
             "answer": "Citations and filtering (e.g. which source/page a passage came from).",
             "why": "You retrieve where text came from, enabling cited answers and 'where' filters."},
            {"q": "Why persist the collection to disk?",
             "options": ["To avoid re-embedding everything each run",
                         "To make queries slower", "To hide the data",
                         "It is required by the API"],
             "answer": "A",
             "why": "Embedding is the slow/costly step; persist once and reuse."},
            {"q": "True or false: it is fine to embed documents and queries with different models.",
             "answer": "False",
             "why": "Their vector spaces differ, so similarity scores become meaningless."},
            {"q": "Short answer: what does collection.query return that you need for citations?",
             "answer": "The matched documents plus their ids/metadata (and distances).",
             "why": "Metadata carries the source so you can cite it."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 9 - CHUNKING STRATEGIES
    # ----------------------------------------------------------------------
    topic_section(
        doc, 9, "Chunking strategies for documents",
        [
            "You rarely embed a whole document as one vector. A long document covers many topics, "
            "so a single embedding becomes a blurry average that matches nothing well, and you "
            "could not fit a whole book into a prompt anyway. Instead you split documents into "
            "CHUNKS - smaller passages - embed each chunk, and retrieve the few chunks most "
            "relevant to the question. Chunking quality often makes or breaks a RAG system: "
            "retrieve the wrong chunks and even a perfect model cannot answer.",

            "The core trade-off is chunk SIZE. Chunks that are too large dilute meaning and waste "
            "tokens (you pay to stuff irrelevant text into the prompt). Chunks that are too small "
            "lose context - a sentence may be meaningless without its surrounding paragraph. A "
            "common starting point is a few hundred tokens per chunk (say 200-500), tuned to your "
            "content. Always think in TOKENS, not characters, because that is what both the "
            "embedding model and the LLM consume.",

            "OVERLAP helps. If you cut cleanly at boundaries, a fact that straddles a boundary gets "
            "split across two chunks and is retrievable from neither. Adding a small overlap (e.g. "
            "10-20% of the chunk size) so consecutive chunks share some text keeps such facts "
            "intact. Better still, chunk along NATURAL boundaries - paragraphs, headings, sections "
            "- so each chunk is a coherent unit. 'Recursive' splitters try to split on the "
            "largest natural separator first (sections, then paragraphs, then sentences) and only "
            "fall back to hard cuts when a piece is still too big.",

            "Always attach METADATA to each chunk: the source document, and ideally a section or "
            "page reference. This is what lets your final answer cite 'according to billing.md, "
            "section 3'. Match your strategy to the content: prose splits well by paragraph; code "
            "by function; tables and slides may need bespoke handling. Start simple "
            "(fixed-size-with-overlap), measure retrieval quality, then refine.",
        ],
        'def chunk_text(text, chunk_size=400, overlap=80):\n'
        '    """Split into ~chunk_size-word chunks with word overlap (words ~ tokens here).\n'
        '    In production, split on tokens and prefer natural boundaries."""\n'
        '    words = text.split()\n'
        '    chunks, start = [], 0\n'
        '    while start < len(words):\n'
        '        end = start + chunk_size\n'
        '        chunks.append(" ".join(words[start:end]))\n'
        '        start = end - overlap          # step back to create overlap\n'
        '    return chunks\n\n'
        'doc = open("handbook.txt").read()\n'
        'pieces = chunk_text(doc)\n'
        'records = [\n'
        '    {"id": f"handbook-{i}", "text": c,\n'
        '     "metadata": {"source": "handbook.txt", "chunk": i}}\n'
        '    for i, c in enumerate(pieces)\n'
        ']\n'
        '# Each record is embedded and stored; metadata enables later citations.',
        "Fixed-size chunking with overlap, attaching source metadata to each chunk record.",
        "Embedding entire documents as one vector (blurry, matches poorly); chunking with zero "
        "overlap so facts on a boundary become unretrievable; chunking by characters instead of "
        "tokens; making chunks so small they lose the surrounding context needed to make sense; "
        "and dropping metadata, leaving you unable to cite or trace where an answer came from.",
        [
            {"q": "Why not embed a whole long document as a single vector?",
             "options": ["It is illegal", "Its meaning becomes a blurry average that matches poorly",
                         "Vectors cannot be that long", "It is faster"],
             "answer": "B",
             "why": "One vector for many topics retrieves badly; chunking gives focused matches."},
            {"q": "Chunks that are too SMALL tend to...",
             "options": ["Cost more to store", "Lose surrounding context and become ambiguous",
                         "Always retrieve better", "Exceed the context window"],
             "answer": "B",
             "why": "A fragment may be meaningless without its paragraph; balance size carefully."},
            {"q": "What problem does chunk overlap solve?",
             "answer": "Facts that straddle a chunk boundary would otherwise be split and unretrievable.",
             "why": "Shared text between consecutive chunks keeps boundary-spanning facts intact."},
            {"q": "You should size chunks in...",
             "options": ["Characters", "Tokens", "Sentences only", "Megabytes"],
             "answer": "B",
             "why": "Tokens are what the embedding model and LLM actually consume and bill."},
            {"q": "A 'recursive' splitter prefers to split first on...",
             "options": ["Random positions", "The largest natural boundary (sections, then paragraphs)",
                         "Every character", "The middle of words"],
             "answer": "B",
             "why": "Splitting on natural separators keeps chunks coherent; hard cuts are a fallback."},
            {"q": "True or false: chunk metadata is optional and adds no value.",
             "answer": "False",
             "why": "Metadata (source, section/page) is what enables citations and filtering."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 10 - RAG END TO END
    # ----------------------------------------------------------------------
    topic_section(
        doc, 10, "Retrieval-Augmented Generation (RAG) end to end",
        [
            "RETRIEVAL-AUGMENTED GENERATION is the architecture that ties this whole month "
            "together. The idea: instead of hoping the model already knows the answer, you "
            "RETRIEVE relevant passages from your own data and put them in the prompt, then ask "
            "the model to answer USING ONLY those passages. This grounds the model in current, "
            "private, trustworthy text, dramatically reducing hallucination and letting it answer "
            "questions about data it was never trained on.",

            "There are two phases. INGESTION (offline, done once when documents change): load the "
            "documents, chunk them, embed each chunk, and store the vectors plus text and metadata "
            "in a vector database. QUERY (online, per question): embed the user's question, search "
            "the vector store for the top-k most similar chunks, assemble a prompt that includes "
            "those chunks as context, send it to the LLM with an instruction to answer only from "
            "the context (and to say 'I don't know' otherwise), and return the answer together "
            "with citations derived from the chunks' metadata.",

            "Put plainly, the query-time pipeline is: question -> embed -> retrieve top-k -> build "
            "context -> prompt the LLM -> grounded, cited answer. Each earlier topic this month is "
            "a piece of it: embeddings (topic 7), the vector store (topic 8), chunking (topic 9), "
            "the API call and prompting (topics 2-3), and structured/streamed output and cost "
            "control (topics 5-6). RAG is the assembly of those parts.",

            "Things that make RAG good in practice: a clear system instruction to use ONLY the "
            "provided context and to cite sources; including the source label with each retrieved "
            "chunk so the model can cite it; choosing a sensible k (too few misses the answer, too "
            "many adds noise and cost); and EVALUATING the whole pipeline (topic 11) because a "
            "failure could be in retrieval (wrong chunks) or generation (the model ignored good "
            "chunks) - you must measure to know which.",
        ],
        'import anthropic, chromadb\n\n'
        'client = anthropic.Anthropic()\n'
        'col = chromadb.PersistentClient("./chroma_store").get_collection("handbook")\n\n'
        'def answer(question, k=3):\n'
        '    # 1. RETRIEVE the top-k most relevant chunks (with their sources).\n'
        '    res = col.query(query_texts=[question], n_results=k)\n'
        '    chunks = res["documents"][0]\n'
        '    sources = [m["source"] for m in res["metadatas"][0]]\n\n'
        '    # 2. BUILD a context block labelled with sources for citation.\n'
        '    context = "\\n\\n".join(\n'
        '        f"[{s}] {c}" for s, c in zip(sources, chunks)\n'
        '    )\n\n'
        '    # 3. PROMPT the model to answer ONLY from the context, and cite.\n'
        '    system = ("Answer using ONLY the provided context. "\n'
        '              "Cite the [source] you used. "\n'
        '              "If the answer is not in the context, say you do not know.")\n'
        '    msg = client.messages.create(\n'
        '        model="claude-sonnet-4-6", max_tokens=512, system=system,\n'
        '        messages=[{"role": "user",\n'
        '                   "content": f"Context:\\n{context}\\n\\nQuestion: {question}"}],\n'
        '    )\n'
        '    return msg.content[0].text\n\n'
        'print(answer("How do I reset my password?"))',
        "A complete query-time RAG function: retrieve, build labelled context, prompt, cite.",
        "Retrieving good chunks but forgetting to instruct the model to use ONLY them (so it "
        "answers from training data and may hallucinate); not labelling chunks with sources, so "
        "the model cannot cite; choosing k poorly (too small misses the answer; too large floods "
        "the prompt with noise and cost); re-ingesting on every query instead of ingesting once; "
        "and treating RAG as one black box when debugging - you must separate retrieval failures "
        "from generation failures.",
        [
            {"q": "The core idea of RAG is to...",
             "options": ["Fine-tune the model on your data",
                         "Retrieve relevant passages and put them in the prompt to ground the answer",
                         "Increase the temperature", "Use a bigger context window only"],
             "answer": "B",
             "why": "RAG grounds the model in retrieved, trustworthy text instead of relying on memory."},
            {"q": "Which steps belong to the OFFLINE ingestion phase?",
             "options": ["Embed the question and search",
                         "Load, chunk, embed and store documents",
                         "Stream the answer", "Cite sources"],
             "answer": "B",
             "why": "Ingestion prepares the store; querying happens online per question."},
            {"q": "Put the query-time pipeline in order (short answer).",
             "answer": "Question -> embed -> retrieve top-k -> build context -> prompt LLM -> cited answer.",
             "why": "Each stage corresponds to a topic from this month."},
            {"q": "What single instruction most reduces hallucination in RAG?",
             "options": ["Use more tokens", "Answer using ONLY the provided context (else say 'I don't know')",
                         "Raise temperature", "Add more tools"],
             "answer": "B",
             "why": "Constraining the model to the retrieved context curbs invented answers."},
            {"q": "True or false: if a RAG answer is wrong, the fault is always in the LLM.",
             "answer": "False",
             "why": "It may be a retrieval failure (wrong chunks) or a generation failure - measure to tell."},
            {"q": "What enables citations in the final answer?",
             "answer": "Carrying each chunk's source metadata through retrieval into the prompt.",
             "why": "The model can only cite a source label that you include with the context."},
            {"q": "Choosing k too LARGE tends to...",
             "options": ["Improve accuracy for free", "Add irrelevant noise and cost",
                         "Break the embedding model", "Disable caching"],
             "answer": "B",
             "why": "Excess chunks dilute the signal and inflate token usage."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 11 - EVALUATING LLM APPS
    # ----------------------------------------------------------------------
    topic_section(
        doc, 11, "Evaluating LLM apps & reducing hallucination",
        [
            "An LLM app that you cannot measure is one you cannot trust or improve. Because the "
            "same prompt can give different answers, and because 'looks good' is not a metric, you "
            "need EVALUATION: a repeatable way to score quality. The cornerstone is an EVAL SET - "
            "a fixed collection of representative inputs, ideally with known good answers or clear "
            "acceptance criteria. You run your app over the eval set, score the outputs, and "
            "compare versions. Without this, every change is a guess.",

            "How to score depends on the task. For closed tasks (classification, extraction) you "
            "can compare to a gold answer with exact match, F1, or accuracy. For open tasks "
            "(summaries, RAG answers) there is no single right string, so common approaches are: "
            "human rating against a rubric; programmatic checks (does the answer contain the "
            "required fact? does it cite a real source? is it valid JSON?); and 'LLM-as-judge', "
            "where a separate model scores the answer against criteria you specify. LLM-as-judge "
            "scales well but must itself be validated against human judgement on a sample.",

            "For RAG specifically, evaluate the two stages separately. RETRIEVAL quality: did the "
            "top-k chunks actually contain the answer? (measure recall@k). GENERATION quality: "
            "given good chunks, did the model answer correctly and FAITHFULLY - i.e. is every "
            "claim supported by the retrieved context (groundedness), with no invented facts? "
            "Separating these tells you where to fix a problem: improve chunking/retrieval, or "
            "improve the prompt/model.",

            "Reducing HALLUCINATION is mostly engineering you have already met: ground the model in "
            "retrieved context and instruct it to use only that; give an explicit 'say I don't "
            "know' escape; ask for citations and then check they are real; request structured "
            "output where you can validate it; and keep a regression eval set so a prompt tweak "
            "that fixes one case does not silently break ten others. Treat evaluation as part of "
            "the build, not an afterthought.",
        ],
        '# A tiny eval harness: run the app over a fixed set and score it.\n'
        'eval_set = [\n'
        '    {"q": "How do I reset my password?", "must_contain": "Forgot password"},\n'
        '    {"q": "What is the refund window?",   "must_contain": "14 days"},\n'
        '    {"q": "When are office hours?",        "must_contain": "9am"},\n'
        ']\n\n'
        'def score(answer_fn):\n'
        '    passed = 0\n'
        '    for case in eval_set:\n'
        '        out = answer_fn(case["q"])\n'
        '        ok = case["must_contain"].lower() in out.lower()\n'
        '        passed += ok\n'
        '        print(f"{\'PASS\' if ok else \'FAIL\'}: {case[\'q\']}")\n'
        '    print(f"Score: {passed}/{len(eval_set)}")\n'
        '    return passed / len(eval_set)\n\n'
        '# score(answer)   # answer() is the RAG function from topic 10\n'
        '# For open-ended answers, replace the substring check with an LLM-as-judge\n'
        '# call that rates groundedness against the retrieved context.',
        "A tiny eval harness: run the app over a fixed set and score each case.",
        "Eyeballing a few outputs and declaring success (no fixed eval set, no repeatability); "
        "evaluating RAG as one black box so you cannot tell retrieval failures from generation "
        "failures; trusting an LLM judge without ever checking it against human ratings; scoring "
        "only accuracy and ignoring groundedness (an answer can be 'correct-sounding' yet "
        "unsupported); and tweaking prompts with no regression set, so fixes quietly cause new "
        "failures.",
        [
            {"q": "An eval set is...",
             "options": ["A set of API keys", "A fixed set of representative inputs (with criteria) to score on",
                         "The model's training data", "A list of prompts to never use"],
             "answer": "B",
             "why": "It gives a repeatable, comparable measure of quality across versions."},
            {"q": "'LLM-as-judge' means...",
             "options": ["The model picks its own training data",
                         "A separate model scores outputs against your criteria",
                         "A human rates every answer", "Using a courtroom dataset"],
             "answer": "B",
             "why": "It scales scoring but must be validated against human judgement on a sample."},
            {"q": "In RAG, recall@k measures...",
             "options": ["How fast retrieval is",
                         "Whether the top-k retrieved chunks actually contain the answer",
                         "The cost per query", "The model temperature"],
             "answer": "B",
             "why": "It isolates RETRIEVAL quality from generation quality."},
            {"q": "Short answer: what is 'groundedness' / faithfulness?",
             "answer": "Whether every claim in the answer is supported by the retrieved context.",
             "why": "A fluent answer can still hallucinate unsupported facts; faithfulness checks for that."},
            {"q": "Which does NOT directly reduce hallucination?",
             "options": ["Grounding in retrieved context", "An explicit 'say I don't know' escape",
                         "Asking for and verifying citations", "Raising the temperature"],
             "answer": "D",
             "why": "Higher temperature increases variability; the others constrain the model toward facts."},
            {"q": "True or false: you should validate an LLM judge against human ratings.",
             "answer": "True",
             "why": "Otherwise you trust a scorer whose accuracy you have never measured."},
            {"q": "Why evaluate retrieval and generation separately in RAG?",
             "answer": "To know whether to fix chunking/retrieval or the prompt/model when answers are wrong.",
             "why": "A single combined score hides where the failure actually is."},
        ],
    )

    # ----------------------------------------------------------------------
    # TOPIC 12 - FRAMEWORKS OVERVIEW
    # ----------------------------------------------------------------------
    topic_section(
        doc, 12, "Frameworks overview - LangChain vs LlamaIndex vs hand-rolling",
        [
            "Having built RAG from raw parts, you will meet frameworks that package those parts. "
            "The two best known are LangChain and LlamaIndex. They provide ready-made loaders, "
            "splitters, vector-store connectors, retrievers and chains, so you can wire a pipeline "
            "in a few lines rather than writing each stage yourself. The value is speed of "
            "assembly and a common vocabulary; the cost is an abstraction layer you must learn and "
            "occasionally fight.",

            "LANGCHAIN is broad and general: a large toolkit for composing LLM calls, tools, "
            "memory and multi-step 'chains' and agents across many providers. It shines when you "
            "are orchestrating complex, multi-step workflows and want lots of integrations off the "
            "shelf. LLAMAINDEX is more focused on the DATA side of RAG: ingesting, indexing and "
            "querying your documents. It tends to be the more ergonomic choice when your app is "
            "primarily 'chat with my documents' and you want strong indexing and retrieval "
            "abstractions. The two overlap and interoperate; the line is fuzzy and both evolve "
            "quickly.",

            "When should you HAND-ROLL instead? When the pipeline is simple (the topic-10 RAG "
            "function is about 20 lines and you fully understand every line); when you need tight "
            "control over prompts, cost and latency; when you want to minimise dependencies and "
            "the risk of breaking changes; and crucially while you are LEARNING - building it "
            "yourself first is the only way to understand what a framework is doing for you, and "
            "to debug it when the abstraction leaks.",

            "A pragmatic rule for this course: hand-roll your first RAG app (your Month-3 project) "
            "so you own the mechanics; reach for a framework later when you hit genuine complexity "
            "- many document loaders, many retrieval strategies, agent orchestration - that you do "
            "not want to reimplement. The official Anthropic SDK already gives you a clean Messages "
            "API and a tool runner, so you often need less framework than you think. Choose the "
            "lightest tool that does the job.",
        ],
        '# Hand-rolled RAG is short and fully transparent (see topic 10):\n'
        '#   question -> embed -> retrieve -> build context -> call API -> answer\n'
        '# About 20 lines, every line yours to read and debug.\n\n'
        '# A framework collapses the wiring, at the cost of an abstraction to learn.\n'
        '# Conceptual LlamaIndex-style sketch (API names change - check current docs):\n'
        '#   from llama_index.core import VectorStoreIndex, SimpleDirectoryReader\n'
        '#   docs  = SimpleDirectoryReader("./data").load_data()\n'
        '#   index = VectorStoreIndex.from_documents(docs)   # chunk+embed+store\n'
        '#   engine = index.as_query_engine()\n'
        '#   print(engine.query("How do I reset my password?"))\n\n'
        '# Decision rule:\n'
        '#   simple / learning / tight control  -> hand-roll\n'
        '#   many integrations / complex agents -> framework',
        "Hand-rolled vs framework RAG, with a decision rule for choosing between them.",
        "Reaching for a heavy framework on day one and never learning what it abstracts (so you "
        "cannot debug it when it leaks); assuming a framework removes the need to understand "
        "tokens, embeddings, chunking and evaluation (it does not); copying framework example "
        "code whose API has since changed; and adding large dependencies for a 20-line job, "
        "inheriting their breaking changes and bugs.",
        [
            {"q": "LlamaIndex is generally most focused on...",
             "options": ["Image generation", "The data/RAG side: ingesting, indexing and querying documents",
                         "Training models", "Billing"],
             "answer": "B",
             "why": "It specialises in document indexing and retrieval for RAG."},
            {"q": "LangChain is best described as...",
             "options": ["A vector database", "A broad toolkit for composing LLM calls, tools, memory and chains",
                         "An embedding model", "A tokenizer"],
             "answer": "B",
             "why": "It targets general multi-step orchestration across many integrations."},
            {"q": "A good reason to HAND-ROLL is...",
             "options": ["You want maximum dependencies",
                         "The pipeline is simple and you want control + understanding",
                         "You dislike Python", "Frameworks are illegal"],
             "answer": "B",
             "why": "Simple pipelines are short, and building them teaches you the mechanics."},
            {"q": "True or false: using a framework removes the need to understand embeddings and chunking.",
             "answer": "False",
             "why": "Frameworks wrap those concepts; you still need them to design and debug well."},
            {"q": "Short answer: what is the main cost of adopting a framework?",
             "answer": "An abstraction layer to learn, plus dependencies/breaking changes you must manage.",
             "why": "Speed of assembly is traded against control and added complexity."},
            {"q": "For your Month-3 project, the recommended approach is to...",
             "options": ["Use the biggest framework available", "Hand-roll it to own the mechanics",
                         "Avoid RAG entirely", "Skip evaluation"],
             "answer": "B",
             "why": "Building it yourself first makes later framework choices informed, not blind."},
        ],
    )

    # ----------------------------------------------------------------------
    # EXERCISES
    # ----------------------------------------------------------------------
    h1(doc, "Exercises")
    para(doc,
         "Work through these in order; each builds on the last and on the topics above. Commit "
         "your code as you go. Keep your API key in an environment variable throughout.")
    numbered(doc,
             "Token sense. Write a script that takes any text and prints (a) the exact token "
             "count from client.messages.count_tokens for claude-sonnet-4-6, and (b) your "
             "4-chars-per-token estimate. Compare them on English prose, on a Python file, and on "
             "a paragraph of a non-English language. Explain the differences in a comment.")
    numbered(doc,
             "First call. Using the Anthropic SDK and an env-var key, write a function ask(prompt, "
             "system=None) that calls the Messages API and returns the text. Print the usage "
             "tokens and stop_reason for each call.")
    numbered(doc,
             "Mini chatbot. Extend exercise 2 into a command-line chat loop that maintains history "
             "(append each user and assistant turn) so the model 'remembers' earlier turns. Prove "
             "it by telling it your name, then asking for it two turns later.")
    numbered(doc,
             "Structured extraction. Given a few messy free-text customer records, use structured "
             "output (a JSON schema with name, email, plan, all required, additionalProperties "
             "false) to return clean JSON. Validate each result with json.loads and assert the "
             "keys.")
    numbered(doc,
             "A real tool. Define and wire up a calculator tool (it takes a Python arithmetic "
             "expression and returns the exact result) so the model can do precise maths. Run the "
             "full manual agentic loop and confirm the model uses the tool for a hard sum it would "
             "otherwise get wrong.")
    numbered(doc,
             "Embeddings by hand. Implement cosine_similarity in NumPy. Take ten short sentences, "
             "embed them with an embedding model (Voyage AI, OpenAI, or sentence-transformers), "
             "and for a query sentence print the three most similar - by cosine similarity - with "
             "their scores. Sanity-check that semantically similar sentences rank highest.")
    numbered(doc,
             "Ingest into Chroma. Take a markdown or text document, chunk it (fixed size with "
             "overlap, sized in tokens), embed each chunk, and store ids, text and source metadata "
             "in a persistent Chroma collection. Query it with three questions and print the "
             "top-3 chunks and their sources for each.")
    numbered(doc,
             "End-to-end RAG with evaluation. Combine exercises 4-7 into a single answer(question) "
             "function that retrieves top-k chunks, prompts the model to answer ONLY from the "
             "context and cite sources, and returns the cited answer. Then build a small eval set "
             "(at least five Q&A pairs), score your app with a programmatic check, deliberately "
             "break retrieval (e.g. set k=0), and observe and explain the eval score dropping.")

    page_break(doc)

    # ----------------------------------------------------------------------
    # PROJECT BRIEF
    # ----------------------------------------------------------------------
    h1(doc, "Project brief: 'Chat with your documents' (a deployed RAG app)")

    h2(doc, "Goal")
    para(doc,
         "Build and DEPLOY a small web application that lets a user upload their own documents "
         "(PDF and/or markdown), ask questions in natural language, and receive answers grounded "
         "in those documents WITH CITATIONS back to the source. This is the capstone of Month 3: "
         "it exercises ingestion, chunking, embeddings, a Chroma vector store, retrieval, a "
         "grounded and cited LLM call, a Streamlit user interface, and a small evaluation. Hand-"
         "roll the RAG core (do not lean on a framework) so you own and understand every stage.")

    h2(doc, "Requirements")
    bullet(doc, "Ingestion: load PDF and markdown files; extract text; chunk into token-sized "
                "pieces with overlap; attach source metadata (filename and, ideally, page/section).")
    bullet(doc, "Embedding & storage: embed each chunk with a single embedding model and store "
                "ids, text and metadata in a PERSISTENT Chroma collection (so restarts do not "
                "re-embed). Use the same model for queries.")
    bullet(doc, "Retrieval: embed the question and retrieve the top-k most relevant chunks; make "
                "k configurable.")
    bullet(doc, "Generation: call the Anthropic Messages API (claude-sonnet-4-6 is a sensible "
                "default) with a system prompt that says answer ONLY from the provided context, "
                "cite the source of each fact, and say 'I don't know' when the context lacks the "
                "answer. Keep the API key in an environment variable.")
    bullet(doc, "Citations: every answer must show which source document/section each claim came "
                "from, derived from the retrieved chunks' metadata.")
    bullet(doc, "UI: a Streamlit app with a file uploader, a question box, the streamed answer, "
                "and the cited sources displayed beneath it.")
    bullet(doc, "Evaluation: a small eval set (>= 5 questions) with a script that scores answer "
                "quality (programmatic checks and/or LLM-as-judge for groundedness).")
    bullet(doc, "Cost awareness: display or log the token usage and an estimated cost per question.")
    bullet(doc, "Deployment: deploy the app so it is reachable by a URL (e.g. Streamlit Community "
                "Cloud), with the API key supplied as a secret, not committed to the repo.")

    h2(doc, "Milestones")
    numbered(doc, "Hard-coded context loop. A script that answers a question using ONE manually "
                  "pasted passage as context - proves the grounded, cited prompt works before any "
                  "retrieval exists.")
    numbered(doc, "Ingestion pipeline. Load and chunk real PDF/markdown files with overlap and "
                  "source metadata; print the chunks to verify them.")
    numbered(doc, "Vector store. Embed the chunks and store them in a persistent Chroma "
                  "collection; query it and confirm sensible top-k retrieval.")
    numbered(doc, "Retrieval-grounded answers. Replace the hard-coded passage with live top-k "
                  "retrieval; return answers grounded in retrieved chunks with citations.")
    numbered(doc, "Streamlit UI. Wrap the pipeline in a Streamlit app: upload, ask, stream the "
                  "answer, show cited sources.")
    numbered(doc, "Evaluation & tuning. Build the eval set, measure retrieval and generation "
                  "quality, and tune chunk size, k and the prompt to improve the score.")
    numbered(doc, "Deployed app with citations. Deploy publicly with the API key as a secret; "
                  "confirm end-to-end that a stranger can upload a document and get cited answers.")

    h2(doc, "Grading rubric")
    table_from_rows(
        doc,
        ["Criterion", "Weight", "What 'excellent' looks like"],
        [
            ["Ingestion & chunking", "15%",
             "PDF + markdown loaded; token-sized chunks with overlap; source metadata on every chunk."],
            ["Embeddings & vector store", "15%",
             "Single consistent embedding model; persistent Chroma; no re-embedding on restart."],
            ["Retrieval quality", "15%",
             "Top-k retrieval returns the right chunks; k configurable; measured recall@k."],
            ["Grounded, cited generation", "20%",
             "Answers use ONLY context, cite real sources, and say 'I don't know' when appropriate."],
            ["Streamlit UI & UX", "10%",
             "Clean upload/ask flow; streamed answer; sources shown clearly."],
            ["Evaluation", "10%",
             "Eval set of 5+; retrieval vs generation scored separately; groundedness checked."],
            ["Cost & token awareness", "5%",
             "Token usage and estimated cost surfaced; model choice justified."],
            ["Deployment", "10%",
             "Publicly reachable URL; API key kept as a secret, never committed."],
        ],
    )

    page_break(doc)

    # ----------------------------------------------------------------------
    # RESOURCES
    # ----------------------------------------------------------------------
    h1(doc, "Resources")
    para(doc, "All real, well-known sources. Search for the current page if a link has moved; "
              "do not trust any URL you cannot reach.")
    bullet(doc, "Anthropic documentation - the official Claude developer docs (Messages API, "
                "tool use, streaming, structured outputs, prompt caching): platform.claude.com/docs")
    bullet(doc, "Anthropic Python SDK - source, examples and README on GitHub: "
                "github.com/anthropics/anthropic-sdk-python")
    bullet(doc, "Anthropic 'Prompt engineering' guide and the interactive prompting tutorial in "
                "the Anthropic docs and cookbook (github.com/anthropics/anthropic-cookbook).")
    bullet(doc, "Chroma documentation - getting started, collections, persistence and querying: "
                "docs.trychroma.com")
    bullet(doc, "OpenAI API documentation - useful as the main alternative provider and for its "
                "clear embeddings guide: platform.openai.com/docs")
    bullet(doc, "LlamaIndex documentation - data-centric RAG framework, strong on ingestion and "
                "indexing: docs.llamaindex.ai")
    bullet(doc, "LangChain documentation - general LLM orchestration framework and concepts: "
                "python.langchain.com")
    bullet(doc, "Streamlit documentation - build and deploy the web UI, including Community Cloud "
                "deployment and secrets: docs.streamlit.io")
    bullet(doc, "sentence-transformers - free, local open-source embedding models and a clear "
                "explanation of semantic similarity: sbert.net")

    # ----------------------------------------------------------------------
    # SAVE
    # ----------------------------------------------------------------------
    doc.save(OUTPUT)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    build()
