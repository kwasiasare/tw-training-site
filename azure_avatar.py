# -*- coding: utf-8 -*-
"""Azure TTS Avatar (batch synthesis) via REST (stdlib only). Renders a
talking-avatar MP4 from SSML. Used by build_one_video.py's opt-in
AVATAR_MODE=corner to composite an AI presenter over the lesson slides.

Avatar batch synthesis needs a SEPARATE Speech resource in westus2 /
westeurope / southeastasia — see HOWTO_Azure_Avatar.md."""
import os, sys, time, urllib.request, urllib.error

from azure_tts import load_env, _read_with_retry

ROOT = os.path.dirname(os.path.abspath(__file__))

try:
    ENV = load_env()
except OSError:
    ENV = {}

KEY = ENV.get('AZURE_AVATAR_SPEECH_KEY', '') or os.environ.get('AZURE_AVATAR_SPEECH_KEY', '')
REGION = ENV.get('AZURE_AVATAR_SPEECH_REGION', '') or os.environ.get('AZURE_AVATAR_SPEECH_REGION', 'westus2')
ENDPOINT = ENV.get('AZURE_AVATAR_ENDPOINT', '') or f'https://{REGION}.api.cognitive.microsoft.com'
API_VERSION = '2024-08-01'


def require_config():
    if not KEY:
        raise SystemExit(
            "AVATAR_MODE=corner needs a SEPARATE Speech resource -\n"
            "avatar batch synthesis only works in westus2 / westeurope / southeastasia\n"
            "(the eastus resource used for narration TTS cannot do avatars).\n"
            "Set these in .env:\n"
            "  AZURE_AVATAR_SPEECH_KEY\n"
            "  AZURE_AVATAR_SPEECH_REGION\n"
            "  AZURE_AVATAR_ENDPOINT (optional)\n"
            "See HOWTO_Azure_Avatar.md for setup steps."
        )


def _sanitize_id(s):
    import re
    s = re.sub(r'[^A-Za-z0-9_-]', '-', s)
    s = s[:64]
    while s and not s[0].isalnum():
        s = s[1:]
    while s and not s[-1].isalnum():
        s = s[:-1]
    if len(s) < 3:
        s = (s + 'id0')[:3]
    return s[:64]


def submit_job(ssml, synthesis_id, character='lisa', style='graceful-sitting',
               bitrate_kbps=2000, background='#00B140FF'):
    synthesis_id = _sanitize_id(synthesis_id)
    url = f'{ENDPOINT}/avatar/batchsyntheses/{synthesis_id}?api-version={API_VERSION}'
    body = {
        'inputKind': 'SSML',
        'inputs': [{'content': ssml}],
        'avatarConfig': {
            'talkingAvatarCharacter': character,
            'talkingAvatarStyle': style,
            'videoFormat': 'Mp4',
            'videoCodec': 'h264',
            'bitrateKbps': bitrate_kbps,
            'backgroundColor': background,
        },
    }
    import json as _json
    req = urllib.request.Request(
        url, data=_json.dumps(body).encode('utf-8'), method='PUT',
        headers={
            'Ocp-Apim-Subscription-Key': KEY,
            'Content-Type': 'application/json',
        })
    try:
        _read_with_retry(req, 60)
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')
        raise urllib.error.HTTPError(e.url, e.code, f'{e.reason}: {detail}', e.headers, e.fp)
    return synthesis_id


def wait_for_job(synthesis_id, poll_interval=10, timeout_s=1800):
    import json as _json
    url = f'{ENDPOINT}/avatar/batchsyntheses/{synthesis_id}?api-version={API_VERSION}'
    start = time.time()
    while True:
        req = urllib.request.Request(url, method='GET',
                                      headers={'Ocp-Apim-Subscription-Key': KEY})
        try:
            data = _json.loads(_read_with_retry(req, 60))
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf-8', errors='replace')
            raise urllib.error.HTTPError(e.url, e.code, f'{e.reason}: {detail}', e.headers, e.fp)
        status = data.get('status')
        if status == 'Succeeded':
            return data['outputs']['result']
        if status == 'Failed':
            raise RuntimeError(f'Avatar job {synthesis_id} failed: {data.get("properties", {}).get("error", data)}')
        if time.time() - start > timeout_s:
            raise RuntimeError(f'Avatar job {synthesis_id} timed out after {timeout_s}s (status={status})')
        time.sleep(poll_interval)


def download_result(url, out_path):
    req = urllib.request.Request(url, method='GET',
                                  headers={'Ocp-Apim-Subscription-Key': KEY})
    data = _read_with_retry(req, 120)
    with open(out_path, 'wb') as f:
        f.write(data)
    return len(data)


def synth_avatar(ssml, out_mp4, character='lisa', style='graceful-sitting', synthesis_id=None):
    if synthesis_id is None:
        synthesis_id = _sanitize_id(f'avatar-{int(time.time())}-{os.getpid()}')
    synthesis_id = submit_job(ssml, synthesis_id, character=character, style=style)
    result_url = wait_for_job(synthesis_id)
    return download_result(result_url, out_mp4)


if __name__ == '__main__':
    # Smoke test: requires a real westus2/westeurope/southeastasia key. Not run
    # as part of this change (no key yet) - see HOWTO_Azure_Avatar.md.
    require_config()
    from azure_tts import build_ssml
    sample = "Hi, I'm your AI course presenter. This is a quick avatar smoke test."
    ssml = build_ssml(sample, 'en-US-JennyNeural')
    outdir = os.path.join(ROOT, 'videos', '_auditions')
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, 'avatar_smoke.mp4')
    n = synth_avatar(ssml, out)
    print(f'avatar_smoke.mp4: {n/1024:.0f} KB -> {out}')
