# -*- coding: utf-8 -*-
"""Render ONE lesson video from a deck JSON file.
Voice alternates by lesson number: odd = female (Jenny), even = male (Guy).
Usage: python build_one_video.py <deck.json>
Outputs the mp4 into site/public/videos/<video filename from deck>."""
import os, re, sys, json, time, subprocess, urllib.error
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from azure_tts import synth, get_token, build_ssml
import azure_avatar

ROOT = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
SITE_VIDEOS = os.path.join(ROOT, 'course-materials', os.environ.get('COURSE_SLUG', 'dami-ai-career'), 'videos')

FEMALE = 'en-US-JennyNeural'
MALE = 'en-US-GuyNeural'
RATE = '-4%'

# Opt-in AI avatar presenter mode (TW-134). Default OFF; only the exact value
# 'corner' activates it - anything else is the existing (no-avatar) behavior.
AVATAR_MODE = os.environ.get('AVATAR_MODE', '').lower()
# Optional explicit overrides; when unset the avatar alternates with the voice
# (odd lesson = female Lisa, even = male Max) - see main().
AVATAR_CHARACTER = os.environ.get('AVATAR_CHARACTER')
AVATAR_STYLE = os.environ.get('AVATAR_STYLE')
# Each avatar needs its own corner crop of the 1920x1080 clip: Lisa is seated so
# her upper body fills the center half; Max is standing so we crop tight to his
# upper body to fill the corner at the same size. Tuned on the TW-134 prototype.
AVATAR_CROPS = {
    'lisa': 'crop=iw/2:ih:iw/4:0',
    'max': 'crop=680:760:620:30',
}
AVATAR_CROP_DEFAULT = 'crop=iw/2:ih:iw/4:0'

W, H = 1280, 720
NAVY = (0x1F, 0x3A, 0x5F); ACCENT = (0x2E, 0x86, 0xC1); WHITE = (0xFF, 0xFF, 0xFF)
DARK = (0x22, 0x2A, 0x33); GREY = (0x66, 0x66, 0x66); CODEBG = (0xF2, 0xF4, 0xF7)
GREEN = (0x1E, 0x8A, 0x4C)
# Resolve fonts cross-platform: Windows paths first (so local renders are unchanged),
# then Linux (Liberation/DejaVu) and macOS fallbacks, then PIL's default.
_FONT_DIRS = [
    'C:/Windows/Fonts/',
    '/usr/share/fonts/truetype/liberation/',
    '/usr/share/fonts/truetype/dejavu/',
    '/Library/Fonts/', '/System/Library/Fonts/Supplemental/',
]
_BOLD = ['arialbd.ttf', 'LiberationSans-Bold.ttf', 'DejaVuSans-Bold.ttf', 'Arial Bold.ttf']
_REG = ['arial.ttf', 'LiberationSans-Regular.ttf', 'DejaVuSans.ttf', 'Arial.ttf']
_MONO = ['consola.ttf', 'LiberationMono-Regular.ttf', 'DejaVuSansMono.ttf', 'Menlo.ttc']


def _font(size, names):
    for d in _FONT_DIRS:
        for n in names:
            p = d + n
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except OSError:
                    pass
    return ImageFont.load_default(size)


font_h = _font(40, _BOLD)
font_body = _font(32, _REG)
font_code = _font(23, _MONO)
font_small = _font(20, _REG)
font_big = _font(60, _BOLD)
font_sub = _font(30, _REG)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def footer(d, idx, total, label):
    d.line([(60, H - 60), (W - 60, H - 60)], fill=(0xDD, 0xDD, 0xDD), width=1)
    d.text((60, H - 48), label, font=font_small, fill=GREY)
    s = f'{idx}/{total}'
    d.text((W - 60 - d.textlength(s, font=font_small), H - 48), s, font=font_small, fill=GREY)


def render_title(s, idx, total, course_title):
    img = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(img)
    d.rectangle([0, 300, W, 308], fill=ACCENT)
    t = s.get('title', '')
    # wrap long titles
    lines = wrap(d, t, font_big, W - 160)
    ty = 230 - (len(lines) - 1) * 36
    for ln in lines:
        d.text(((W - d.textlength(ln, font=font_big)) / 2, ty), ln, font=font_big, fill=WHITE); ty += 72
    sub = s.get('sub', '')
    d.text(((W - d.textlength(sub, font=font_sub)) / 2, 330), sub, font=font_sub, fill=(0xCF, 0xE2, 0xF3))
    foot = f'An instructor lesson  -  {course_title}'
    d.text(((W - d.textlength(foot, font=font_small)) / 2, 640), foot, font=font_small, fill=(0xAE, 0xD6, 0xF1))
    return img


def render_content(s, idx, total, label):
    img = Image.new('RGB', (W, H), WHITE); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 110], fill=NAVY); d.rectangle([0, 110, W, 117], fill=ACCENT)
    for ln in wrap(d, s.get('title', ''), font_h, W - 120)[:1]:
        d.text((60, 32), ln, font=font_h, fill=WHITE)
    y = 158
    for b in s.get('bullets', []) or []:
        for i, ln in enumerate(wrap(d, b, font_body, W - 200)):
            if i == 0:
                d.ellipse([62, y + 12, 74, y + 24], fill=ACCENT)
            d.text((100, y), ln, font=font_body, fill=DARK); y += 42
        y += 8
    code = s.get('code')
    if code:
        cl = code.split('\n')
        ch = 32 * len(cl) + 28
        cy = max(y + 8, H - 80 - ch)
        d.rectangle([60, cy, W - 60, cy + ch], fill=CODEBG)
        d.rectangle([60, cy, 66, cy + ch], fill=ACCENT)
        ty = cy + 14
        for ln in cl:
            d.text((90, ty), ln, font=font_code, fill=GREEN if ln.strip().startswith('#') else NAVY); ty += 32
    footer(d, idx, total, label)
    return img


def main(deck_path):
    deck = json.load(open(deck_path, encoding='utf-8'))
    slides = deck['slides']
    lesson = int(deck.get('lesson', 1))
    voice = FEMALE if lesson % 2 == 1 else MALE
    # Presenter pairs with the voice: odd lesson = female Lisa (seated), even =
    # male Max (business). Explicit env overrides win; the crop follows the
    # chosen character so an override keeps the right framing.
    if lesson % 2 == 1:
        avatar_char, avatar_style = 'lisa', 'graceful-sitting'
    else:
        avatar_char, avatar_style = 'max', 'business'
    avatar_char = AVATAR_CHARACTER or avatar_char
    avatar_style = AVATAR_STYLE or avatar_style
    avatar_crop = AVATAR_CROPS.get(avatar_char, AVATAR_CROP_DEFAULT)
    course_title = (deck.get('courseTitle') or os.environ.get('COURSE_TITLE')
                     or os.environ.get('COURSE_SLUG', 'dami-ai-career').replace('-', ' ').title())
    label = f"{course_title}   |   Month {deck.get('month')}: {deck.get('monthTitle','')}   |   {deck.get('title','')}"
    slug = deck.get('slug') or os.path.splitext(os.path.basename(deck_path))[0].replace('.slides', '')
    video_name = deck.get('video') or f'{slug}.mp4'
    if AVATAR_MODE == 'corner':
        # Never clobber the published (non-avatar) video.
        video_name = os.path.splitext(video_name)[0] + '.avatar.mp4'

    work = os.path.join(ROOT, 'videos', '_render', slug)
    os.makedirs(work, exist_ok=True)
    total = len(slides)

    token = None
    if AVATAR_MODE == 'corner':
        azure_avatar.require_config()
    else:
        token = get_token()

    if AVATAR_MODE == 'corner':
        # Phase A: submit all avatar jobs up front (skip any slide whose avatar
        # clip already exists on disk, so an interrupted run can resume without
        # re-paying for synthesis).
        jobs = {}
        for i, s in enumerate(slides, 1):
            n = f'{i:02d}'
            if os.path.exists(os.path.join(work, f'avatar_{n}.mp4')):
                continue
            ssml = build_ssml(s.get('narration', ' '), voice, rate=RATE)
            synthesis_id = azure_avatar._sanitize_id(f'{slug}-s{n}-{int(time.time())}')
            # The S0 tier rate-limits the create-synthesis call (429 seen at
            # ~2 back-to-back submits on the TW-134 prototype), so pace the
            # submits and back off + retry on 429 instead of crashing (a crash
            # here abandons already-submitted, already-billed jobs).
            for attempt in range(6):
                try:
                    jobs[n] = azure_avatar.submit_job(ssml, synthesis_id,
                                                       character=avatar_char, style=avatar_style)
                    break
                except urllib.error.HTTPError as e:
                    if e.code != 429 or attempt == 5:
                        raise
                    m = re.search(r'retry after (\d+)', str(e.reason), re.IGNORECASE)
                    wait = int(m.group(1)) + 2 if m else 32
                    print(f'  slide {n}: submit rate-limited (429), retrying in {wait}s...')
                    time.sleep(wait)
            time.sleep(3)  # pace successive submits below the S0 call-rate cap
        # Phase B: wait for and download each submitted job.
        for n, synthesis_id in jobs.items():
            result_url = azure_avatar.wait_for_job(synthesis_id)
            azure_avatar.download_result(result_url, os.path.join(work, f'avatar_{n}.mp4'))

    segs = []
    for i, s in enumerate(slides, 1):
        n = f'{i:02d}'
        img = render_title(s, i, total, course_title) if s.get('type') == 'title' else render_content(s, i, total, label)
        png = os.path.join(work, f'slide_{n}.png'); img.save(png)
        seg = os.path.join(work, f'seg_{n}.mp4')
        if AVATAR_MODE == 'corner':
            avatar_mp4 = os.path.join(work, f'avatar_{n}.mp4')
            # NOTE: the avatar mp4 already carries the narration audio (from
            # batch synthesis), so we do NOT call synth() here - this both
            # guarantees lip-sync and avoids double-billing Azure TTS.
            # chromakey/crop/overlay values tuned against the cse-m1-l01
            # prototype: the Azure avatar's green matte is ~0x00B040, and
            # similarity 0.15 keys the background cleanly while keeping the
            # presenter solid (0.20+ starts ghosting her body; the original
            # 0.28 keyed her out almost entirely). 360px bottom-right reads
            # well and clears the footer on both navy-title and white slides.
            # avatar_crop is per-character (Lisa seated vs Max standing).
            subprocess.run([FF, '-y', '-loop', '1', '-i', png, '-i', avatar_mp4,
                            '-filter_complex',
                            f"[1:v]chromakey=0x00B040:0.15:0.05,despill=type=green,"
                            f"{avatar_crop},scale=-2:360[av];"
                            "[0:v][av]overlay=x=W-w-24:y=H-h-80:shortest=1,format=yuv420p[v]",
                            '-map', '[v]', '-map', '1:a', '-af', 'apad=pad_dur=0.6',
                            '-c:v', 'libx264', '-r', '25', '-c:a', 'aac', '-b:a', '192k',
                            '-shortest', seg], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            wav = os.path.join(work, f'audio_{n}.wav')
            synth(s.get('narration', ' '), voice, wav, token=token, rate=RATE)
            subprocess.run([FF, '-y', '-loop', '1', '-i', png, '-i', wav,
                            '-af', 'apad=pad_dur=0.6', '-c:v', 'libx264', '-tune', 'stillimage',
                            '-pix_fmt', 'yuv420p', '-r', '25', '-c:a', 'aac', '-b:a', '192k',
                            '-shortest', seg], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segs.append(seg)
    listf = os.path.join(work, 'concat.txt')
    with open(listf, 'w') as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    os.makedirs(SITE_VIDEOS, exist_ok=True)
    out = os.path.join(SITE_VIDEOS, video_name)
    subprocess.run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', listf, '-c', 'copy', out],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if AVATAR_MODE != 'corner':
        # cleanup work dir (avatar mode keeps its workdir around - both so a
        # failed/interrupted run can resume via skip-if-exists, and so the
        # paid avatar clips survive while the ffmpeg overlay/chromakey
        # settings above get tuned against the prototype output)
        for fn in os.listdir(work):
            os.remove(os.path.join(work, fn))
        os.rmdir(work)
    print(f'{slug}: {video_name}  ({os.path.getsize(out)/1024/1024:.1f} MB, {voice}, {total} slides)')
    return out


if __name__ == '__main__':
    main(sys.argv[1])
