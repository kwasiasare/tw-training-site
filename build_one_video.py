# -*- coding: utf-8 -*-
"""Render ONE lesson video from a deck JSON file.
Voice alternates by lesson number: odd = female (Jenny), even = male (Guy).
Usage: python build_one_video.py <deck.json>
Outputs the mp4 into site/public/videos/<video filename from deck>."""
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from azure_tts import synth, get_token

ROOT = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
SITE_VIDEOS = os.path.join(ROOT, 'course-materials', 'dami-ai-career', 'videos')

FEMALE = 'en-US-JennyNeural'
MALE = 'en-US-GuyNeural'
RATE = '-4%'

W, H = 1280, 720
NAVY = (0x1F, 0x3A, 0x5F); ACCENT = (0x2E, 0x86, 0xC1); WHITE = (0xFF, 0xFF, 0xFF)
DARK = (0x22, 0x2A, 0x33); GREY = (0x66, 0x66, 0x66); CODEBG = (0xF2, 0xF4, 0xF7)
GREEN = (0x1E, 0x8A, 0x4C)
F = 'C:/Windows/Fonts/'
font_h = ImageFont.truetype(F + 'arialbd.ttf', 40)
font_body = ImageFont.truetype(F + 'arial.ttf', 32)
font_code = ImageFont.truetype(F + 'consola.ttf', 23)
font_small = ImageFont.truetype(F + 'arial.ttf', 20)
font_big = ImageFont.truetype(F + 'arialbd.ttf', 60)
font_sub = ImageFont.truetype(F + 'arial.ttf', 30)


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


def render_title(s, idx, total):
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
    foot = 'An instructor lesson  -  Maths to AI Course'
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
    label = f"Maths -> AI   |   Month {deck.get('month')}: {deck.get('monthTitle','')}   |   {deck.get('title','')}"
    slug = deck.get('slug') or os.path.splitext(os.path.basename(deck_path))[0].replace('.slides', '')
    video_name = deck.get('video') or f'{slug}.mp4'

    work = os.path.join(ROOT, 'videos', '_render', slug)
    os.makedirs(work, exist_ok=True)
    total = len(slides)
    token = get_token()
    segs = []
    for i, s in enumerate(slides, 1):
        n = f'{i:02d}'
        img = render_title(s, i, total) if s.get('type') == 'title' else render_content(s, i, total, label)
        png = os.path.join(work, f'slide_{n}.png'); img.save(png)
        wav = os.path.join(work, f'audio_{n}.wav')
        synth(s.get('narration', ' '), voice, wav, token=token, rate=RATE)
        seg = os.path.join(work, f'seg_{n}.mp4')
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
    # cleanup work dir
    for fn in os.listdir(work):
        os.remove(os.path.join(work, fn))
    os.rmdir(work)
    print(f'{slug}: {video_name}  ({os.path.getsize(out)/1024/1024:.1f} MB, {voice}, {total} slides)')
    return out


if __name__ == '__main__':
    main(sys.argv[1])
