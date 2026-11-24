#!/usr/bin/env python3
"""news-23 b49 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories. Output: entry.png 1024x1024.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"

def fb(sz):
    return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", sz)

def fr(sz):
    return ImageFont.truetype(FD + "DejaVuSans.ttf", sz)

def serifb(sz):
    return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", sz)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

BLACK = (10, 10, 10)
GOLD = (214, 164, 32)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
TEAL = (0, 128, 128)
NAVY = (10, 30, 66)
CREAM = (250, 244, 224)
GREY = (90, 90, 90)
LGREY = (230, 230, 230)
GREEN = (46, 139, 87)
BLUE = (30, 90, 168)
PURPLE = (110, 60, 160)
ORANGE = (200, 110, 20)

def tw(text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def th(text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[3] - b[1]

def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit(text, font, maxw, min_sz=9):
    """Shrink font until text fits maxw; returns (text, font)."""
    sz = font.size
    f = font
    while tw(text, f) > maxw and sz > min_sz:
        sz -= 1
        f = fb(sz) if "Bold" in f.getname()[0] or True else fr(sz)
    return text, f

def fitb(text, size, maxw, min_sz=8):
    sz = size
    while tw(text, fb(sz)) > maxw and sz > min_sz:
        sz -= 1
    return fb(sz)

def chip(x, y, label, color):
    f = fb(10)
    w = tw(label, f) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill="white")
    return w

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 58], fill=BLACK)
d.text((14, 6), "THE WORLD TODAY", font=serifb(40), fill="white")
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 14 - tw(dt, fb(20)), 18), dt, font=fb(20), fill=GOLD)

# ---------------------------------------------------------------- kicker
kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
d.text((14, 64), kick, font=fb(15), fill=RED)

# ---------------------------------------------------------------- number strip (5 cols x 2 rows), y 84..138
nums = [
    ("-3.3%", "KOSPI", RED),
    ("5.3", "US-CHINA POWER GAP", BLUE),
    ("11,762", "EBOLA CASES, DRC", GREEN),
    ("10T won", "SEOUL STABILISATION FUND", ORANGE),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", PURPLE),
    ("165", "RUSSIAN MISSILES IN A WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", BLUE),
    ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", ORANGE),
    ("$107.3B", "ANTHROPIC IPO \u2014 LARGEST", PURPLE),
]
colw = W // 5
for i, (num, lab, col) in enumerate(nums):
    cx = (i % 5) * colw + 12
    cy = 84 + (i // 5) * 27
    d.text((cx, cy), num, font=fb(19), fill=col)
    d.text((cx, cy + 20), lab, font=fb(8), fill=BLACK)

# ---------------------------------------------------------------- region bar y 140..158
regions = [("ASIA-PACIFIC 7", TEAL, 7), ("AMERICAS 8", NAVY, 8),
           ("MIDDLE EAST 6", ORANGE, 6), ("EUROPE 5", PURPLE, 5),
           ("AFRICA 3", RED, 3), ("WORLD 2", GREY, 2)]
tot = sum(r[2] for r in regions)
x = 0
for name, col, n in regions:
    wseg = int(W * n / tot)
    d.rectangle([x, 140, x + wseg - 1, 158], fill=col)
    f = fb(11)
    d.text((x + (wseg - tw(name, f)) // 2, 144), name, font=f, fill="white")
    x += wseg

# ---------------------------------------------------------------- UTC strip y 160..176
d.rectangle([0, 160, W, 176], fill=NAVY)
utc = "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles   ~18:00 IPO $97.17"
d.text((10, 163), utc, font=fr(11), fill="white")
d.text((W - 10 - tw("~ APPROX", fr(11)), 163), "~ APPROX", font=fr(11), fill=GOLD)

# ---------------------------------------------------------------- hero scenes y 178..330
sc_y, sc_h = 178, 152
cw = W // 3
# --- scene 1: Kospi chart
x0 = 0
d.rectangle([x0, sc_y, x0 + cw - 2, sc_y + sc_h], fill=NAVY)
d.text((x0 + 10, sc_y + 4), "-3.3%", font=fb(30), fill=(255, 90, 60))
pts = [(x0 + 12 + i * 26, sc_y + 78 - v) for i, v in enumerate([8, 22, 14, 30, 18, 34, 26, 40, 30, 44, 36, 48])]
d.line(pts, fill=(255, 120, 80), width=3)
for (px, py) in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD)
import random
random.seed(23)
for _ in range(26):
    bx = x0 + 8 + random.randint(0, cw - 30)
    bw = random.randint(8, 16)
    bh = random.randint(14, 52)
    by = sc_y + sc_h - 26 - bh
    d.rectangle([bx, by, bx + bw, sc_y + sc_h - 26], fill=(30, 60, 110))
    for wy in range(by + 4, sc_y + sc_h - 28, 9):
        d.rectangle([bx + 2, wy, bx + bw - 2, wy + 4], fill=(255, 220, 100))
d.rectangle([x0, sc_y + sc_h - 24, x0 + cw - 2, sc_y + sc_h], fill=BLACK)
d.text((x0 + 10, sc_y + sc_h - 20), "KOSPI 4,708.54  \u00b7  -161 PTS", font=fb(12), fill="white")
# --- scene 2: Guterres
x0 = cw
d.rectangle([x0, sc_y, x0 + cw - 2, sc_y + sc_h], fill=TEAL)
d.text((x0 + 12, sc_y + 8), "150 DELEGATES", font=fb(30), fill=GOLD)
d.text((x0 + 12, sc_y + 42), "BACK A RISK", font=fb(30), fill="white")
d.text((x0 + 12, sc_y + 76), "FRAMEWORK", font=fb(30), fill="white")
# globe bottom-right
gx, gy, gr = x0 + cw - 62, sc_y + sc_h - 58, 26
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(200, 240, 235), width=2)
d.ellipse([gx - gr // 2, gy - gr, gx + gr // 2, gy + gr], outline=(200, 240, 235), width=1)
d.line([gx - gr, gy, gx + gr, gy], fill=(200, 240, 235), width=1)
d.line([gx - gr + 8, gy - 14, gx + gr - 8, gy - 14], fill=(200, 240, 235), width=1)
d.line([gx - gr + 8, gy + 14, gx + gr - 8, gy + 14], fill=(200, 240, 235), width=1)
d.rectangle([x0, sc_y + sc_h - 24, x0 + cw - 2, sc_y + sc_h], fill=BLACK)
d.text((x0 + 10, sc_y + sc_h - 20), "UN  \u00b7  BRIDGETOWN", font=fb(12), fill="white")
# --- scene 3: Asia Power Index bars
x0 = 2 * cw
d.rectangle([x0, sc_y, x0 + cw - 2, sc_y + sc_h], fill=CREAM)
d.text((x0 + 10, sc_y + 6), "NARROWEST SINCE 2018", font=fb(13), fill=BLACK)
d.text((x0 + cw - 12 - tw("GAP 5.3", fb(13)), sc_y + 6), "GAP 5.3", font=fb(13), fill=(150, 110, 0))
bars = [("78.9", "US", NAVY, 96), ("73.6", "CHINA", RED, 88), ("40.5", "INDIA", GOLD, 52)]
bx = x0 + 16
for val, lab, col, bhgt in bars:
    by = sc_y + sc_h - 26 - bhgt
    d.rectangle([bx, by, bx + 82, sc_y + sc_h - 26], fill=col)
    d.text((bx + (82 - tw(val, fb(17))) // 2, by + 6), val, font=fb(17), fill="white")
    d.text((bx + (82 - tw(lab, fb(11))) // 2, by + bhgt - 20), lab, font=fb(11), fill="white")
    bx += 98
d.rectangle([x0, sc_y + sc_h - 24, x0 + cw - 2, sc_y + sc_h], fill=BLACK)
d.text((x0 + 10, sc_y + sc_h - 20), "ASIA POWER INDEX 2026", font=fb(12), fill="white")

# ---------------------------------------------------------------- hero text y 340..424
# generous white gap below the scene strips so headlines never touch them
heroes = [
    ("1", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED"),
    ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS", "REPORTED"),
    ("3", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED"),
]
hy = 342
for i, (num, head, body, src, ch) in enumerate(heroes):
    x0 = i * cw + 12
    maxw = cw - 24
    # number badge
    d.ellipse([x0, hy, x0 + 22, hy + 22], fill=RED)
    tw_n = tw(num, fb(13))
    d.text((x0 + (22 - tw_n) // 2, hy + 4), num, font=fb(13), fill="white")
    # headline (2 lines max, shrink to fit)
    hf = fitb(head, 15, maxw - 28)
    lines = wrap(head, hf, maxw - 28)
    ly = hy
    for ln in lines[:2]:
        d.text((x0 + 28, ly), ln, font=hf, fill=BLACK)
        ly += 17
    by = hy + 40
    blines = wrap(body, fr(11), maxw)
    for ln in blines[:2]:
        d.text((x0, by), ln, font=fr(11), fill=BLACK)
        by += 14
    # source + chip on their own row, well below body
    sy = hy + 40 + 28 + 4
    d.text((x0, sy), src, font=fr(9), fill=GREY)
    chip(x0 + maxw - 62, sy - 1, ch, NAVY)

# ---------------------------------------------------------------- MORE bar y 430..448
d.rectangle([0, 430, W, 448], fill=BLACK)
d.text((12, 433), "MORE OF THE DAY  \u2014  10 STORIES", font=fb(13), fill="white")

# ---------------------------------------------------------------- cards y 450..566 (5 cols x 2 rows)
cards = [
    ("AMERICAS", "1", "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED", NAVY),
    ("FBI", "2", "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED", DARKRED),
    ("WHITE HOUSE", "3", "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", "REPORTED", ORANGE),
    ("MARKETS", "4", "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", GREEN),
    ("SPORT", "5", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", RED),
    ("SPORT", "6", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", RED),
    ("LEGAL", "7", "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED", PURPLE),
    ("TECH", "8", "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", BLUE),
    ("EUROPE", "9", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", RED),
    ("SPACE", "10", "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite may carry a nuke.", "Reuters", "CLAIM", GREY),
]
cardw = W // 5
for i, (cat, num, head, body, src, ch, col) in enumerate(cards):
    cx = (i % 5) * cardw
    cy = 450 + (i // 5) * 58
    # category strip
    d.rectangle([cx, cy, cx + cardw - 2, cy + 14], fill=col)
    d.text((cx + 4, cy + 2), cat, font=fb(9), fill="white")
    d.text((cx + cardw - 14 - tw(num, fb(9)), cy + 2), num, font=fb(9), fill="white")
    # headline: shrink to one line, never touching chip (chip lives on bottom row)
    hf = fitb(head, 12, cardw - 12)
    d.text((cx + 4, cy + 17), head, font=hf, fill=BLACK)
    d.text((cx + 4, cy + 33), body, font=fr(9), fill=BLACK)
    # source + chip on their own bottom row
    d.text((cx + 4, cy + 45), src, font=fr(8), fill=GREY)
    chip(cx + cardw - 66, cy + 44, ch, NAVY if ch == "REPORTED" else RED)

# ---------------------------------------------------------------- map + ALSO y 570..876
d.rectangle([0, 570, W, 588], fill=BLACK)
d.text((12, 573), "WHERE IT HAPPENED", font=fb(13), fill="white")
d.text((342, 573), "ALSO ON MONDAY", font=fb(13), fill="white")
# map panel
d.rectangle([10, 592, 330, 872], outline=(150, 180, 200), width=1, fill=(235, 245, 250))
for gx in range(10, 331, 22):
    d.line([gx, 592, gx, 872], fill=(205, 225, 235), width=1)
for gy in range(592, 873, 22):
    d.line([10, gy, 330, gy], fill=(205, 225, 235), width=1)
# stylised land blobs
d.ellipse([18, 620, 150, 800], fill=(150, 210, 150))
d.ellipse([150, 600, 300, 760], fill=(150, 210, 150))
d.ellipse([210, 780, 300, 860], fill=(150, 210, 150))
d.ellipse([120, 760, 210, 850], fill=(150, 210, 150))
pins = [(60, 640), (80, 700), (110, 660), (95, 730), (140, 690),
        (190, 700), (230, 640), (260, 660), (170, 760), (120, 780),
        (210, 620), (240, 620), (280, 640)]
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline="white", width=1)
    d.text((px - 3, py - 6), str(i), font=fb(9), fill="white")
d.text((14, 830), "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", font=fr(9), fill=BLACK)
d.text((14, 842), "4 Washington \u00b7 5 New York \u00b7 6 Tehran \u00b7 7 Chicago", font=fr(9), fill=BLACK)
d.text((14, 854), "8 SF \u00b7 9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow", font=fr(9), fill=BLACK)
# ALSO list: two columns
also_l = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe",
    "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike",
    "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
]
also_r = [
    "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for j, t in enumerate(also_l):
    d.text((342, 594 + j * 30), t, font=fr(12), fill=BLACK)
for j, t in enumerate(also_r):
    d.text((690, 594 + j * 30), t, font=fr(12), fill=BLACK)

# ---------------------------------------------------------------- DATE CHECK y 880..950
d.rectangle([8, 880, W - 8, 950], outline=RED, width=2)
d.text((16, 886), "DATE CHECK", font=fb(14), fill=RED)
d.text((W - 16 - tw("READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", fb(9)), 888),
       "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=fb(9), fill=RED)
left = "LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro captured (22 Nov) \u00b7 EU\u2013Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)"
for j, ln in enumerate(wrap(left, fr(11), W - 32)):
    d.text((16, 906 + j * 14), ln, font=fr(11), fill=BLACK)
d.text((16, 934), "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
       font=fr(10), fill=BLACK)

# ---------------------------------------------------------------- footer y 954..986
d.text((10, 954), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", font=fr(9), fill=GREY)
d.text((10, 965), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing", font=fr(9), fill=GREY)
d.text((10, 976), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", font=fr(9), fill=GREY)

# ---------------------------------------------------------------- bottom bar y 988..1024
d.rectangle([0, 988, W, H], fill=BLACK)
foot = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - tw(foot, fb(15))) // 2, 1001), foot, font=fb(15), fill=GOLD)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG")
print("saved", out, os.path.getsize(out), "bytes")
