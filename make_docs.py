# -*- coding: utf-8 -*-
"""Generate the AI career-transition plan (.docx) and month-to-month study guide (.pptx)."""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

from pptx import Presentation
from pptx.util import Inches as PInches, Pt as PPt
from pptx.dml.color import RGBColor as PRGB
from pptx.enum.text import PP_ALIGN

OUT = os.path.dirname(os.path.abspath(__file__))

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
ACCENT = RGBColor(0x2E, 0x86, 0xC1)
GREY = RGBColor(0x55, 0x55, 0x55)

# ---------------------------------------------------------------- WORD ----------
doc = Document()

# base style
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

def heading(text, level=1, color=NAVY):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = color
    return h

def para(text, bold=False, italic=False, size=11, color=None, space_after=6):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space_after)
    return p

def bullet(text, sub=False):
    p = doc.add_paragraph(style='List Bullet' if not sub else 'List Bullet 2')
    p.add_run(text)
    return p

# Title
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('From Maths Graduate to AI Job')
r.bold = True
r.font.size = Pt(26)
r.font.color.rgb = NAVY
sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('A 6-Month Aggressive Career-Transition Plan')
r.italic = True
r.font.size = Pt(14)
r.font.color.rgb = ACCENT

meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = meta.add_run('Starting point: Maths degree | L1 Support internship | Little/no coding | ~30+ hrs per week')
r.font.size = Pt(10)
r.font.color.rgb = GREY
doc.add_paragraph()

# Overview
heading('Overview', 1)
para('This plan moves a recent mathematics graduate with L1 support experience and little/no '
     'coding background into a first AI job, working at an aggressive pace of roughly 30+ hours '
     'per week. The strategy is to land an AI Application Developer role first (the only role '
     'realistically reachable in 3-6 months from zero code), then pivot toward ML Engineer or '
     'Data Scientist from inside a paid tech role - where the maths degree becomes a real '
     'differentiator.')

# Time to hire table
heading('Realistic Time-to-Hire by Role', 1)
para('Starting from near-zero coding is the binding constraint. These are time to first job, '
     'not time to mastery.', italic=True, color=GREY)

table = doc.add_table(rows=1, cols=4)
table.style = 'Light Grid Accent 1'
hdr = table.rows[0].cells
for i, t in enumerate(['Role', 'Time to junior job', 'Why', 'Maths leverage']):
    hdr[i].text = t
    for p in hdr[i].paragraphs:
        for run in p.runs:
            run.bold = True

rows = [
    ('AI Application Developer (LLM apps, RAG, agents, APIs)', '4-7 months',
     'Build on top of existing models; less heavy theory. Portfolio matters more than credentials.', 'Low-Medium'),
    ('Data Scientist / ML', '9-15 months',
     'Needs stats + ML + SQL + storytelling. Credential-heavy and crowded at junior level.', 'High'),
    ('ML / AI Engineer', '12-20 months',
     'Needs solid software engineering AND ML AND deployment. Hardest cold-start from no coding.', 'High'),
]
for role, time, why, lev in rows:
    cells = table.add_row().cells
    cells[0].text = role
    cells[1].text = time
    cells[2].text = why
    cells[3].text = lev

doc.add_paragraph()
para('Conclusion: Within a 3-6 month aggressive window, only AI Application Developer is '
     'realistically achievable as a first job. The other two are better treated as a year-1 '
     'destination you grow into from that first role.', bold=True)

# Recommendation
heading('Recommendation', 1)
para('Target AI Application Developer first, then pivot toward ML Engineer or Data Scientist '
     'from inside a paid tech role (much easier than from outside). Lead with the application '
     'skills now; lead with the maths degree in stage 2.')
para('Why this fits your background:', bold=True)
bullet('L1 support -> AI Application Dev is a natural adjacent move. Support means you understand '
       'users, ticketing, SLAs, debugging, and talking to non-technical people - exactly what AI '
       'app teams need. Frame yourself as "support engineer moving into building AI tools."')
bullet('Maths degree signals you can handle the theory later - recruiters trust it for the ML pivot.')
bullet('It is the only path with a credible 3-6 month timeline from zero code.')

# The plan
heading('The 6-Month Aggressive Plan (~30 hrs/week)', 1)

heading('Months 1-2 - Python + Fundamentals (the make-or-break phase)', 2)
bullet('Python properly: syntax, data structures, functions, OOP basics (freeCodeCamp Python or '
       '"Python Crash Course" + daily practice).')
bullet('Git/GitHub, command line, reading docs. Push everything to GitHub from day one.')
bullet('Web basics: what an API is, JSON, HTTP requests (requests library).')
bullet('SQL basics (one week is enough to start).')
bullet('Milestone: 3-4 small scripts on GitHub (a CLI tool, an API-calling script).')

heading('Month 3 - LLM Application Skills (your specialty)', 2)
bullet('OpenAI / Anthropic APIs: prompting, system prompts, tool/function calling, streaming.')
bullet('Core patterns: RAG (embeddings, vector DBs like Chroma/Pinecone), agents, chunking, evaluation.')
bullet('A framework: LangChain or LlamaIndex - understand the underlying ideas, do not over-invest.')
bullet('Milestone: one working LLM app deployed (Streamlit/FastAPI) - a "chat with your documents" RAG app.')

heading('Month 4 - Build 2-3 Portfolio Projects That Look Like Real Products', 2)
para('Projects get you hired more than any certificate. Tie them to support - that is your edge:', italic=True)
bullet('AI support-ticket assistant - ingests a knowledge base, answers customer questions, suggests '
       'ticket responses. (Directly sells your L1 background.)')
bullet('RAG app over a real dataset with a clean UI.')
bullet('An agent that does a multi-step task (e.g. researches + summarizes).')
bullet('Each needs: clean GitHub README, a live demo link, a short write-up of decisions and trade-offs.')

heading('Month 5 - Polish, Deploy, Go Public', 2)
bullet('Deploy projects (Render, Railway, Hugging Face Spaces, or Azure).')
bullet('Write 2-3 short blog/LinkedIn posts explaining a project - this is interview gold.')
bullet('Rewrite CV around "Maths graduate + support engineer building AI applications." Lead with projects.')
bullet('Be ready to talk about prompt engineering, RAG, hallucination/eval, cost/latency trade-offs, testing.')

heading('Month 6 - Apply Hard + Interview Prep', 2)
bullet('Target titles: AI Engineer (junior), AI Application Developer, LLM Engineer, '
       'Forward-Deployed/Solutions Engineer, AI-focused Support Engineer, Associate ML/AI Engineer.')
bullet('Apply broadly (50-100+ roles); lean on the support -> AI angle for "AI support/automation" roles.')
bullet('Practice: explaining your projects, basic Python/SQL questions, system-design-lite for an LLM app.')

# Stage 2
heading('Stage 2 - The Pivot (Months 7-18, While Employed)', 1)
para('Once you are in a paid AI-adjacent role, that is when you invest the maths:')
bullet('Statistics & probability for ML, linear algebra refresh (fast for you - it is revision).')
bullet('Andrew Ng ML Specialization + Deep Learning Specialization.')
bullet('Move internal projects toward modelling/MLOps; your title drifts to ML Engineer or Data '
       'Scientist - now with production experience plus the maths degree.')

# Pitfalls
heading('Two Things to Watch', 1)
bullet('Do not skip Python fundamentals to rush to LLMs. The #1 failure mode is shallow framework '
       'knowledge with no real coding ability - interviewers catch it instantly.')
bullet('Projects beat certificates. Do courses to learn, but it is the deployed, documented, '
       'support-flavoured projects that land the interview.')

doc.save(os.path.join(OUT, 'AI_Career_Plan.docx'))
print('Saved AI_Career_Plan.docx')

# ---------------------------------------------------------------- PPTX ----------
prs = Presentation()
prs.slide_width = PInches(13.333)
prs.slide_height = PInches(7.5)
BLANK = prs.slide_layouts[6]

PNAVY = PRGB(0x1F, 0x3A, 0x5F)
PACCENT = PRGB(0x2E, 0x86, 0xC1)
PWHITE = PRGB(0xFF, 0xFF, 0xFF)
PGREY = PRGB(0x55, 0x55, 0x55)
PLIGHT = PRGB(0xEA, 0xF2, 0xF8)

def add_box(slide, l, t, w, h):
    return slide.shapes.add_textbox(PInches(l), PInches(t), PInches(w), PInches(h))

def fill_rect(slide, l, t, w, h, color):
    from pptx.enum.shapes import MSO_SHAPE
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PInches(l), PInches(t), PInches(w), PInches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return shp

def set_text(tf, text, size, color, bold=False, align=PP_ALIGN.LEFT):
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = PPt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = 'Calibri'
    return p

def bullets(tf, items, size=16, color=PGREY):
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = '- ' + it
        r.font.size = PPt(size)
        r.font.color.rgb = color
        r.font.name = 'Calibri'
        p.space_after = PPt(8)

def content_slide(title, subtitle, items, footer):
    s = prs.slides.add_slide(BLANK)
    fill_rect(s, 0, 0, 13.333, 1.4, PNAVY)
    fill_rect(s, 0, 1.4, 13.333, 0.12, PACCENT)
    tb = add_box(s, 0.6, 0.25, 12, 0.8)
    set_text(tb.text_frame, title, 30, PWHITE, bold=True)
    if subtitle:
        sb = add_box(s, 0.6, 1.0, 12, 0.4)
        set_text(sb.text_frame, subtitle, 15, PRGB(0xCF, 0xE2, 0xF3), italic_ok=False) if False else \
            set_text(sb.text_frame, subtitle, 15, PRGB(0xCF, 0xE2, 0xF3))
    body = add_box(s, 0.7, 1.9, 12, 5.0)
    bullets(body.text_frame, items, size=17)
    ft = add_box(s, 0.6, 6.95, 12, 0.4)
    set_text(ft.text_frame, footer, 11, PGREY)
    return s

# Title slide
s = prs.slides.add_slide(BLANK)
fill_rect(s, 0, 0, 13.333, 7.5, PNAVY)
fill_rect(s, 0, 3.0, 13.333, 0.08, PACCENT)
tb = add_box(s, 1, 1.7, 11.3, 1.2)
set_text(tb.text_frame, 'Maths Graduate to AI Job', 44, PWHITE, bold=True, align=PP_ALIGN.CENTER)
sb = add_box(s, 1, 3.2, 11.3, 0.8)
set_text(sb.text_frame, 'Month-to-Month Study Guide  |  6-Month Aggressive Plan', 22, PRGB(0xCF, 0xE2, 0xF3), align=PP_ALIGN.CENTER)
mb = add_box(s, 1, 4.3, 11.3, 1.0)
set_text(mb.text_frame, 'Start: Maths degree + L1 Support + little/no coding  |  ~30+ hrs/week  |  Target: AI Application Developer',
         15, PRGB(0xAE, 0xD6, 0xF1), align=PP_ALIGN.CENTER)

# Roadmap overview slide
s = prs.slides.add_slide(BLANK)
fill_rect(s, 0, 0, 13.333, 1.4, PNAVY)
fill_rect(s, 0, 1.4, 13.333, 0.12, PACCENT)
tb = add_box(s, 0.6, 0.4, 12, 0.8)
set_text(tb.text_frame, 'The Roadmap at a Glance', 30, PWHITE, bold=True)
phases = [
    ('M1-2', 'Python + Fundamentals'),
    ('M3', 'LLM Application Skills'),
    ('M4', 'Build Portfolio Projects'),
    ('M5', 'Polish, Deploy, Go Public'),
    ('M6', 'Apply Hard + Interview'),
]
x = 0.5
boxw = 2.4
for label, txt in phases:
    fill_rect(s, x, 2.4, boxw, 2.2, PLIGHT)
    fill_rect(s, x, 2.4, boxw, 0.7, PACCENT)
    lb = add_box(s, x, 2.5, boxw, 0.5)
    set_text(lb.text_frame, label, 22, PWHITE, bold=True, align=PP_ALIGN.CENTER)
    cb = add_box(s, x+0.1, 3.3, boxw-0.2, 1.2)
    set_text(cb.text_frame, txt, 15, PNAVY, bold=True, align=PP_ALIGN.CENTER)
    x += boxw + 0.15
fb = add_box(s, 0.6, 5.2, 12, 1.5)
set_text(fb.text_frame, 'Then Stage 2 (Months 7-18, while employed): invest the maths -> pivot to ML Engineer / Data Scientist.',
         16, PGREY)

# Month slides
content_slide('Months 1-2: Python + Fundamentals', 'The make-or-break phase',
    ['Python properly: syntax, data structures, functions, OOP basics',
     'Tools: freeCodeCamp Python OR "Python Crash Course" + daily practice',
     'Git/GitHub, command line, reading docs - push everything from day one',
     'Web basics: APIs, JSON, HTTP requests (requests library)',
     'SQL basics (one week to get started)',
     'MILESTONE: 3-4 small scripts on GitHub (CLI tool, API-calling script)'],
    'Goal: become genuinely comfortable writing code. Do not rush this.')

content_slide('Month 3: LLM Application Skills', 'Your specialty starts here',
    ['OpenAI / Anthropic APIs: prompting, system prompts, tool calling, streaming',
     'RAG: embeddings, vector DBs (Chroma / Pinecone), chunking, evaluation',
     'Agents and multi-step task patterns',
     'A framework: LangChain or LlamaIndex - learn the ideas, do not over-invest',
     'MILESTONE: one deployed LLM app - a "chat with your documents" RAG app'],
    'Goal: build and ship your first real AI application.')

content_slide('Month 4: Build Portfolio Projects', '2-3 products that look real',
    ['AI support-ticket assistant - knowledge base + answers + suggested replies (sells L1 background)',
     'RAG app over a real dataset with a clean UI',
     'An agent that does a multi-step task (research + summarize)',
     'Each: clean GitHub README, live demo link, write-up of decisions & trade-offs'],
    'Goal: projects > certificates. Tie them to support - that is your edge.')

content_slide('Month 5: Polish, Deploy, Go Public', 'Make it visible',
    ['Deploy projects: Render, Railway, Hugging Face Spaces, or Azure',
     'Write 2-3 short blog / LinkedIn posts explaining a project - interview gold',
     'Rewrite CV: "Maths graduate + support engineer building AI applications"',
     'Lead with projects, not coursework',
     'Be ready to discuss: prompt engineering, RAG, hallucination/eval, cost/latency, testing'],
    'Goal: a public, credible portfolio and a sharpened CV.')

content_slide('Month 6: Apply Hard + Interview Prep', 'Convert effort into offers',
    ['Target titles: AI Engineer (junior), AI Application Developer, LLM Engineer,',
     '   Forward-Deployed / Solutions Engineer, AI-focused Support Engineer',
     'Apply broadly: 50-100+ roles',
     'Lean on support -> AI angle for "AI support/automation" roles',
     'Practice: explain your projects, basic Python/SQL, system-design-lite for an LLM app'],
    'Goal: land the first AI job.')

content_slide('Stage 2: The Pivot (Months 7-18)', 'While employed - now use the maths',
    ['Statistics & probability for ML; linear algebra refresh (revision for you)',
     'Andrew Ng ML Specialization + Deep Learning Specialization',
     'Move internal projects toward modelling / MLOps',
     'Title drifts to ML Engineer or Data Scientist - now with production experience'],
    'Goal: grow from AI app developer into a deeper ML/DS role.')

# Closing tips slide
s = prs.slides.add_slide(BLANK)
fill_rect(s, 0, 0, 13.333, 7.5, PNAVY)
tb = add_box(s, 1, 0.8, 11.3, 1.0)
set_text(tb.text_frame, 'Two Things to Watch', 34, PWHITE, bold=True, align=PP_ALIGN.CENTER)
b1 = add_box(s, 1.5, 2.4, 10.3, 1.6)
set_text(b1.text_frame, '1. Do not skip Python fundamentals to rush to LLMs. Shallow framework knowledge with no '
         'real coding ability is the #1 failure mode - interviewers catch it instantly.', 20, PWHITE)
b2 = add_box(s, 1.5, 4.4, 10.3, 1.6)
set_text(b2.text_frame, '2. Projects beat certificates. Do courses to learn, but it is the deployed, documented, '
         'support-flavoured projects that land the interview.', 20, PWHITE)

prs.save(os.path.join(OUT, 'AI_Study_Guide.pptx'))
print('Saved AI_Study_Guide.pptx')
