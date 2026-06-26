# -*- coding: utf-8 -*-
"""Convert every videos/_decks/<slug>.json into a lesson Markdown page with valid
frontmatter (via PyYAML) for the Astro content collection."""
import os, sys, json, glob, yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
# Course-aware: pass a course slug, e.g. `python convert_decks_to_md.py kwasi-GenAI`.
COURSE_SLUG = sys.argv[1] if len(sys.argv) > 1 else 'dami-ai-career'
COURSE = os.path.join(ROOT, 'course-materials', COURSE_SLUG)
DECKS = os.path.join(COURSE, 'decks')
TOPICS = os.path.join(COURSE, 'lessons')
os.makedirs(TOPICS, exist_ok=True)

ok, bad = 0, []
for path in sorted(glob.glob(os.path.join(DECKS, '*.json'))):
    slug = os.path.splitext(os.path.basename(path))[0]
    try:
        deck = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        bad.append((slug, f'JSON parse: {e}')); continue
    try:
        # Short-answer quiz items have no options. The Astro content schema accepts
        # an array or an omitted field, but NOT options: null — so drop a null/empty
        # options key entirely (decks sometimes carry "options": null). See TW-81.
        quiz = []
        for q in deck.get('quiz', []):
            q = dict(q)
            if q.get('options') in (None, []):
                q.pop('options', None)
            quiz.append(q)
        fm = {
            'course': COURSE_SLUG,
            'title': deck['title'],
            'month': int(deck['month']),
            'monthTitle': deck['monthTitle'],
            'lesson': int(deck['lesson']),
            'summary': deck['summary'],
            'objectives': deck.get('objectives', []),
            'video': deck.get('video', f'{slug}.mp4'),
            'quiz': quiz,
            'resources': deck.get('resources', []),
        }
        body = deck.get('body_markdown', '').strip()
        front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=100).strip()
        md = f'---\n{front}\n---\n\n{body}\n'
        with open(os.path.join(TOPICS, f'{slug}.md'), 'w', encoding='utf-8') as f:
            f.write(md)
        ok += 1
    except Exception as e:
        bad.append((slug, f'build: {e}'))

print(f'Wrote {ok} lesson pages.')
if bad:
    print(f'{len(bad)} FAILED:')
    for s, e in bad:
        print(f'  {s}: {e}')
