# -*- coding: utf-8 -*-
"""Azure Neural TTS via REST (stdlib only). Used to audition voices and to
render narration WAVs for the instructor videos."""
import os, sys, time, urllib.request, urllib.error, html

ROOT = os.path.dirname(os.path.abspath(__file__))


def _read_with_retry(req, timeout, attempts=6):
    """POST and read the full response, retrying transient network failures."""
    last = None
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except (urllib.error.URLError, ConnectionResetError, TimeoutError, OSError) as e:
            last = e
            if i < attempts - 1:
                time.sleep(2 * (i + 1))
    raise last


def load_env():
    env = {}
    p = os.path.join(ROOT, '.env')
    with open(p, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"')
    return env


ENV = load_env()
KEY = ENV.get('AZURE_SPEECH_KEY', '')
REGION = ENV.get('AZURE_SPEECH_REGION', 'eastus')


def get_token():
    url = f'https://{REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    req = urllib.request.Request(url, data=b'', method='POST',
                                 headers={'Ocp-Apim-Subscription-Key': KEY})
    return _read_with_retry(req, 30).decode('utf-8')


def build_ssml(text, voice, lang=None, rate='-4%'):
    if lang is None:
        lang = 'en-GB' if voice.startswith('en-GB') else 'en-US'
    return (
        f"<speak version='1.0' xml:lang='{lang}'>"
        f"<voice xml:lang='{lang}' name='{voice}'>"
        f"<prosody rate='{rate}'>{html.escape(text)}</prosody>"
        f"</voice></speak>"
    )


def synth(text, voice, out_path, token=None, lang=None, rate='-4%'):
    if token is None:
        token = get_token()
    ssml = build_ssml(text, voice, lang=lang, rate=rate)
    url = f'https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1'
    req = urllib.request.Request(
        url, data=ssml.encode('utf-8'), method='POST',
        headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'dami-course-tts',
        })
    audio = _read_with_retry(req, 60)
    with open(out_path, 'wb') as f:
        f.write(audio)
    return len(audio)


if __name__ == '__main__':
    # Audition mode: render a sample sentence in several voices.
    sample = ("Welcome to Month One of your journey from maths graduate to A I engineer. "
              "In this lesson we'll cover one of the most important ideas in all of programming: "
              "functions. By the end you'll know how to write your own functions and reuse them.")
    voices = [
        'en-GB-SoniaNeural',   # GB female
        'en-GB-RyanNeural',    # GB male
        'en-US-JennyNeural',   # US female
        'en-US-GuyNeural',     # US male
        'en-US-AriaNeural',    # US female (alt)
    ]
    outdir = os.path.join(ROOT, 'videos', '_auditions')
    os.makedirs(outdir, exist_ok=True)
    try:
        token = get_token()
    except urllib.error.HTTPError as e:
        print('TOKEN ERROR', e.code, e.reason)
        sys.exit(1)
    print('Token OK. Rendering auditions...')
    for v in voices:
        try:
            n = synth(sample, v, os.path.join(outdir, f'{v}.wav'), token=token)
            print(f'  {v}: {n/1024:.0f} KB')
        except urllib.error.HTTPError as e:
            print(f'  {v}: HTTP {e.code} {e.reason} -> {e.read()[:200]}')
    print('Auditions saved to', outdir)
