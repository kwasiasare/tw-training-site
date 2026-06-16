# -*- coding: utf-8 -*-
"""Master 6-month curriculum backbone."""
import os
from doc_helpers import (new_doc, title_block, h1, h2, h3, para, lead, bullet,
                         numbered, callout, table_from_rows, page_break, GREEN, GREY)

OUT = os.path.dirname(os.path.abspath(__file__))
doc = new_doc()

title_block(doc,
    'Maths Graduate to AI Job - Master Curriculum',
    'A complete 6-month, project-based course (with study packs & quizzes)',
    'Start: Maths degree + L1 Support + little/no coding  |  ~30+ hrs/week  |  Target: AI Application Developer')

h1(doc, 'How this course works')
para(doc, 'This is a full self-study programme that takes you from near-zero coding to your first AI '
          'job in six months of focused effort (~30+ hours/week). It is project-based: every month '
          'ends in something you can show. Each month has its own in-depth Study Pack (a separate '
          'document) containing notes, worked examples, quizzes with answer keys, exercises, and a '
          'project brief with a grading rubric.')
lead(doc, 'The documents in this course:', '')
bullet(doc, 'Master Curriculum (this file) - the backbone and week-by-week map.')
bullet(doc, 'Month 1-6 Study Packs - deep material, quizzes, exercises and projects for each month.')
bullet(doc, 'Month 1 Daily Schedule - a day-by-day breakdown of the first (hardest) month.')
bullet(doc, 'AI Support-Ticket Project Spec - the flagship portfolio build.')

callout(doc, 'Principle', 'Projects beat certificates. Courses teach; deployed, documented, '
        'support-flavoured projects get you hired. Build something every single week.')

h1(doc, 'The six months at a glance')
table_from_rows(doc,
    ['Month', 'Theme', 'You will be able to...', 'Project / Output'],
    [
        ['1', 'Python Foundations + Git', 'Write real Python; use Git/GitHub daily', 'CLI "personal dashboard" capstone'],
        ['2', 'Data, SQL & Web APIs', 'Wrangle data with Pandas; query SQL; build a REST API', 'Data analysis + FastAPI service'],
        ['3', 'LLM Application Skills', 'Use LLM APIs, embeddings, RAG, evaluation', 'Deployed "chat with your docs" RAG app'],
        ['4', 'Portfolio Projects', 'Build agents, guardrails, production-shaped apps', 'AI support-ticket assistant + 2 more'],
        ['5', 'Polish, Deploy, Go Public', 'Deploy, monitor, optimise, write & brand', 'Live apps + blog posts + portfolio site'],
        ['6', 'Apply & Interview', 'Pass AI/LLM + coding interviews; tell your story', 'Applications + mock interviews + offers'],
    ])

h1(doc, 'Detailed week-by-week map')

months = [
    ('Month 1 - Python Foundations + Git', [
        'Week 1: setup, variables/types, operators, conditionals, lists, loops.',
        'Week 2: dictionaries/sets, functions, modules, errors, files.',
        'Week 3: Git & GitHub, OOP (classes/inheritance), JSON, virtual environments.',
        'Week 4: HTTP & APIs (requests), SQL taster (SQLite), capstone CLI project.',
    ]),
    ('Month 2 - Data, SQL & Web APIs', [
        'Week 1: advanced Python (comprehensions, generators, decorators), pytest testing.',
        'Week 2: NumPy + Pandas - loading, cleaning, transforming, aggregating data.',
        'Week 3: SQL in depth - joins, GROUP BY, subqueries; relational thinking.',
        'Week 4: REST APIs with FastAPI; consuming + building JSON services. Mini math-for-ML bridge.',
    ]),
    ('Month 3 - LLM Application Skills', [
        'Week 1: how LLMs work, tokens, prompting, system prompts; calling the Anthropic/OpenAI APIs.',
        'Week 2: tool/function calling, streaming, structured output, cost & latency.',
        'Week 3: embeddings, vector databases, semantic search; chunking strategies.',
        'Week 4: full RAG architecture + evaluation; build & deploy a "chat with your documents" app.',
    ]),
    ('Month 4 - Portfolio Projects', [
        'Week 1: prompt-engineering patterns, guardrails, hallucination control, evaluation harnesses.',
        'Week 2: agents & multi-step workflows; tools, planning, memory.',
        'Week 3: app architecture - FastAPI backend + Streamlit/React UI + storage.',
        'Week 4: build the AI support-ticket assistant end-to-end (flagship project).',
    ]),
    ('Month 5 - Polish, Deploy, Go Public', [
        'Week 1: deployment (Render/Railway/HF Spaces/Azure), environment & secrets, Docker basics.',
        'Week 2: observability, logging, evaluation in production, cost & latency optimisation.',
        'Week 3: portfolio site + clean READMEs + screenshots/demos for every project.',
        'Week 4: write 2-3 technical blog/LinkedIn posts; rebuild CV and LinkedIn profile.',
    ]),
    ('Month 6 - Apply & Interview', [
        'Week 1: job-search strategy, role targeting, application tracking, tailored CVs.',
        'Week 2: AI/LLM concept interviews + Python/SQL coding practice.',
        'Week 3: system-design-lite for LLM apps; behavioural (STAR) prep; the support->AI narrative.',
        'Week 4: mock interviews, apply at volume (50-100+), negotiation basics.',
    ]),
]
for mt, weeks in months:
    h2(doc, mt)
    for w in weeks:
        bullet(doc, w)

h1(doc, 'Weekly rhythm (every week, all 6 months)')
numbered(doc, 'Mon-Fri: ~6 hrs/day - learn a topic, then immediately practise it in code.')
numbered(doc, 'End of each day: commit to GitHub + write one sentence on what you learned.')
numbered(doc, 'End of each week: take that month-pack section quiz; fix anything you got wrong.')
numbered(doc, 'End of each week: ship something - a script, a feature, a deploy, or a post.')
numbered(doc, 'Weekends: rest or catch-up (do not burn out - this is a marathon at sprint pace).')

h1(doc, 'How each Study Pack is structured')
para(doc, 'Open the Month N Study Pack alongside this curriculum. Each one contains:')
bullet(doc, 'Learning objectives - what you can do by the end.')
bullet(doc, 'In-depth notes - each topic explained from first principles, with worked examples.')
bullet(doc, 'Quizzes - per-topic checks with full answer keys and explanations.')
bullet(doc, 'Exercises - hands-on coding tasks to cement the skill.')
bullet(doc, 'Project brief - the monthly build, milestones, and a grading rubric.')
bullet(doc, 'Resources - curated free/cheap materials to go deeper.')

callout(doc, 'Reminder', 'Do not skip Python fundamentals to rush to LLMs. Shallow framework '
        'knowledge with no real coding ability is the #1 reason career-changers fail interviews.', color=GREY)

doc.save(os.path.join(OUT, '00_Master_Curriculum.docx'))
print('Saved 00_Master_Curriculum.docx')
