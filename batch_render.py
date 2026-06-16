# -*- coding: utf-8 -*-
"""Render videos for every deck JSON in videos/_decks (or a passed subset).
Serial to respect Azure free-tier rate limits. Skips ones already rendered unless --force."""
import os, sys, glob, traceback
import build_one_video

ROOT = os.path.dirname(os.path.abspath(__file__))
# Course-aware: set COURSE_SLUG=<slug> in the environment (default dami-ai-career).
COURSE = os.path.join(ROOT, 'course-materials', os.environ.get('COURSE_SLUG', 'dami-ai-career'))
DECKS = os.path.join(COURSE, 'decks')
SITE_VIDEOS = os.path.join(COURSE, 'videos')

force = '--force' in sys.argv
only = [a for a in sys.argv[1:] if not a.startswith('--')]

paths = [os.path.join(DECKS, f'{s}.json') for s in only] if only else sorted(glob.glob(os.path.join(DECKS, '*.json')))
print(f'{len(paths)} deck(s) to consider. force={force}')
done, skipped, failed = 0, 0, []
for p in paths:
    import json
    try:
        deck = json.load(open(p, encoding='utf-8'))
    except Exception as e:
        failed.append((os.path.basename(p), f'json: {e}')); continue
    slug = deck.get('slug') or os.path.splitext(os.path.basename(p))[0]
    video = deck.get('video', f'{slug}.mp4')
    out = os.path.join(SITE_VIDEOS, video)
    if os.path.exists(out) and not force:
        print(f'skip {slug} (exists)'); skipped += 1; continue
    try:
        build_one_video.main(p)
        done += 1
    except Exception as e:
        failed.append((slug, str(e)))
        print(f'FAILED {slug}: {e}')
        traceback.print_exc()

print(f'\nRendered {done}, skipped {skipped}, failed {len(failed)}')
for s, e in failed:
    print(f'  FAIL {s}: {e}')
