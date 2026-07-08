# 🧑‍🏫 How to set up the Azure TTS Avatar presenter (TW-134)

This unlocks the opt-in **AI avatar presenter** mode for lesson videos: a small talking
presenter composited into the corner of the existing slides, instead of slides-with-narration
only. It is **off by default** (`AVATAR_MODE` unset) — the normal render path is unchanged.

**Time:** ~10 minutes. **Cost:** avatar synthesis is billed per minute of *output video*, not
per character — see the cost table below. Nothing is billed until `AVATAR_MODE=corner` is set
and a render is run.

---

## Why a separate resource

Azure's **batch avatar synthesis** API is only available in three regions:
**`westus2`**, **`westeurope`**, **`southeastasia`** (S0 tier). The existing `AZURE_SPEECH_KEY`
resource used for narration TTS lives in `eastus` and **cannot** do avatars — trying will fail
with a region/feature error. You need a **second, separate** Speech resource in one of the three
supported regions. The narration-only pipeline keeps using the `eastus` resource; nothing about
it changes.

## Step 1 — Create the Speech resource

**Portal:**
1. Go to <https://portal.azure.com> → **Create a resource** → search **Speech** → **Create**.
2. **Resource group:** same one as the rest of this project's Azure resources.
3. **Region:** `West US 2` (or West Europe / Southeast Asia).
4. **Name:** e.g. `tw-avatar-speech`.
5. **Pricing tier:** `S0` (avatar batch synthesis is not available on the free F0 tier).
6. **Create**. Once deployed, open the resource → **Keys and Endpoint** and copy **Key 1**.

**Or via CLI:**
```
az cognitiveservices account create --name tw-avatar-speech --resource-group <rg> \
  --kind SpeechServices --sku S0 --location westus2 --yes
```
Then fetch the key:
```
az cognitiveservices account keys list --name tw-avatar-speech --resource-group <rg>
```

## Step 2 — Fill in `.env`
Add (or update) these three lines in `.env` (already scaffolded in `.env.example`):
```
AZURE_AVATAR_SPEECH_KEY=<Key 1 from the resource>
AZURE_AVATAR_SPEECH_REGION=westus2
AZURE_AVATAR_ENDPOINT=
```
Leave `AZURE_AVATAR_ENDPOINT` blank unless you need to override it — it defaults to
`https://<region>.api.cognitive.microsoft.com`.

## Step 3 — Run the one-lesson prototype
The pipeline stays 100% opt-in via `AVATAR_MODE`. To render one lesson with the avatar
presenter (PowerShell):
```powershell
$env:COURSE_SLUG='cloud-security-engineer'
$env:AVATAR_MODE='corner'
python build_one_video.py "course-materials/cloud-security-engineer/decks/cse-m1-l01-zero-trust-foundations-and-the-security-stack.json"
```
This writes `<lesson-slug>.avatar.mp4` into the course's `videos/` folder — **not**
`<lesson-slug>.mp4` — so the currently-published video is never overwritten. Compare the two
side by side before deciding whether to promote avatar mode further.

To go back to normal (no-avatar) rendering, just unset `AVATAR_MODE` (or set it to anything
other than `corner`) and re-run — same command, same deck, no avatar billing.

## Characters and styles
`AVATAR_CHARACTER` (default `lisa`) and `AVATAR_STYLE` (default `graceful-sitting`) are
overridable via env vars. Useful options for `lisa`: `graceful-sitting`, `casual-sitting`. See
Microsoft's [standard avatar character/style gallery](https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/avatar-gallery)
for the full list and preview clips.

## Cost table
Avatar batch synthesis is billed **per minute of rendered output video**, at roughly **€1.74/min**
(check current pricing — this moves):

| Scope | Est. minutes | Est. cost |
|---|---|---|
| 1 prototype lesson (~5 min) | 5 | **~€8–9** |
| Full 388-lesson catalog (~5 min avg) | ~1,940 | **~€3,000+** |

**Always prototype one lesson first.** Do not point `AVATAR_MODE=corner` at a whole course or
the full catalog before the composited output (chromakey edges, avatar size/position, voice
sync) has been reviewed and tuned.

## Troubleshooting
- **Region / "feature not available" error on submit** — the key is in the wrong region. Avatar
  batch synthesis only works in `westus2` / `westeurope` / `southeastasia`. Double-check
  `AZURE_AVATAR_SPEECH_REGION` matches the resource you created.
- **Green halo / fringing around the avatar** — the chroma-key isn't tuned for this avatar's
  green-screen shade yet. In `build_one_video.py`'s avatar mux command, adjust the
  `chromakey=0x00B140:0.28:0.05` similarity (`0.28`) and blend (`0.05`) values — raise similarity
  a little to eat more of the fringe, raise blend for a softer edge.
- **Job stuck / takes a long time** — batch avatar synthesis has up to a **20-minute** processing
  cap per job; `azure_avatar.wait_for_job` polls every 10s up to a 30-minute timeout and raises if
  it's exceeded. A single lesson's per-slide jobs run as separate short clips, so this is rarely hit.
- **Interrupted run (Ctrl-C, crash, network drop)** — just re-run the exact same command. Avatar
  mode skips any slide whose `videos/_render/<slug>/avatar_NN.mp4` already exists, so you don't
  re-pay for clips already synthesized. The workdir is only cleaned up automatically for normal
  (non-avatar) renders — avatar-mode workdirs are left in place on purpose for this reason and for
  re-tuning the compositing without re-synthesizing.
