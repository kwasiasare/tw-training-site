# YouTube channel art: banner (2560x1440, text in safe area) + avatar (800x800).
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Temp\spreadcom-marketing\youtube"
os.makedirs(OUT, exist_ok=True)
NAVY = (0x1F, 0x3A, 0x5F); NAVY_BOT = (0x0D, 0x11, 0x17)
ACCENT = (0x2E, 0x86, 0xC1); WHITE = (0xFF, 0xFF, 0xFF)
LIGHT = (0xEA, 0xF2, 0xFB); MUTED = (0xB4, 0xC4, 0xD6); CARD = (0x1A, 0x2E, 0x49)

_DIRS = ['C:/Windows/Fonts/', '/usr/share/fonts/truetype/liberation/', '/usr/share/fonts/truetype/dejavu/']
_BOLD = ['arialbd.ttf', 'LiberationSans-Bold.ttf', 'DejaVuSans-Bold.ttf']
_REG  = ['arial.ttf', 'LiberationSans-Regular.ttf', 'DejaVuSans.ttf']
def font(size, names):
    for d in _DIRS:
        for n in names:
            if os.path.exists(d + n):
                try: return ImageFont.truetype(d + n, size)
                except OSError: pass
    return ImageFont.load_default(size)

def monogram(d, x, y, s, badge=NAVY):
    sc = s / 64.0; X = lambda v: x + v*sc; Y = lambda v: y + v*sc
    d.rounded_rectangle([x, y, x+s, y+s], radius=int(12*sc), fill=badge)
    w = max(3, int(5*sc))
    d.line([(X(14),Y(44)),(X(26),Y(20)),(X(38),Y(44))], fill=ACCENT, width=w, joint='curve')
    d.line([(X(18),Y(36)),(X(34),Y(36))], fill=ACCENT, width=w)
    wm = max(3, int(4*sc))
    d.line([(X(44),Y(24)),(X(52),Y(24)),(X(52),Y(40)),(X(44),Y(40))], fill=WHITE, width=wm, joint='curve')
    d.line([(X(44),Y(32)),(X(50),Y(32))], fill=WHITE, width=wm)

def grad(d, W, H, top=NAVY, bot=NAVY_BOT):
    for y in range(H):
        t = y/(H-1)
        d.line([(0,y),(W,y)], fill=tuple(int(a+(b-a)*t) for a,b in zip(top,bot)))

# ---------------- BANNER 2560x1440 ----------------
W, H = 2560, 1440
img = Image.new('RGB', (W, H), NAVY_BOT); d = ImageDraw.Draw(img); grad(d, W, H)
cx, cy = W//2, H//2  # safe area ~ center 1546x423

f_word = font(150, _BOLD); f_tag = font(58, _REG); f_url = font(54, _BOLD)
logo_s = 168
word = "Spreadcom Learning"
ww = d.textlength(word, font=f_word)
group_w = logo_s + 40 + ww
gx = cx - group_w/2
row1_y = cy - 150
monogram(d, int(gx), int(row1_y), logo_s, badge=CARD)
d.text((gx + logo_s + 40, row1_y + (logo_s - f_word.size)/2 - 8), word, font=f_word, fill=WHITE)
tag = "Free, job-ready tech courses — built around your career"
tw = d.textlength(tag, font=f_tag)
d.text((cx - tw/2, cy + 60), tag, font=f_tag, fill=MUTED)
url = "www.salloma.com      ·      100% FREE      ·      12 career tracks"
uw = d.textlength(url, font=f_url)
d.text((cx - uw/2, cy + 150), url, font=f_url, fill=ACCENT)
img.save(os.path.join(OUT, "spreadcom-learning-banner.png"), "PNG")
img.convert('RGB').save(os.path.join(OUT, "spreadcom-learning-banner.jpg"), "JPEG", quality=92)
print("banner", img.size)

# ---------------- AVATAR 800x800 ----------------
S = 800
av = Image.new('RGB', (S, S), NAVY); da = ImageDraw.Draw(av)
grad(da, S, S, top=(0x24,0x44,0x6E), bot=(0x12,0x22,0x38))
# big monogram marks centered (no inner badge — bg is the badge)
m = 470; mx = (S-m)//2; my = (S-m)//2 - 30
monogram(da, mx, my, m, badge=(0x1A,0x2E,0x49))
# wordmark under it
fa = font(58, _BOLD)
w1 = "SPREADCOM"; w2 = "LEARNING"
da.text(((S-da.textlength(w1, font=fa))/2, my+m+18), w1, font=fa, fill=WHITE)
fa2 = font(50, _BOLD)
da.text(((S-da.textlength(w2, font=fa2))/2, my+m+78), w2, font=fa2, fill=ACCENT)
av.save(os.path.join(OUT, "spreadcom-learning-avatar.png"), "PNG")
av.convert('RGB').save(os.path.join(OUT, "spreadcom-learning-avatar.jpg"), "JPEG", quality=92)
print("avatar", av.size)
