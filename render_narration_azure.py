# -*- coding: utf-8 -*-
"""Render per-slide narration WAVs with Azure Neural TTS (replaces the SAPI step)."""
import os, sys
from azure_tts import synth, get_token

VOICE = os.environ.get('TTS_VOICE', 'en-US-JennyNeural')
RATE = os.environ.get('TTS_RATE', '-4%')

ROOT = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(ROOT, 'videos', 'M1_Functions')
count = int(open(os.path.join(VID, 'count.txt')).read().strip())

token = get_token()
print(f'Voice={VOICE} rate={RATE} — rendering {count} narration tracks...')
for i in range(1, count + 1):
    n = f'{i:02d}'
    text = open(os.path.join(VID, f'narr_{n}.txt'), encoding='utf-8').read()
    size = synth(text, VOICE, os.path.join(VID, f'audio_{n}.wav'), token=token, rate=RATE)
    print(f'  audio_{n}.wav  {size/1024:.0f} KB')
print('Done.')
