#!/usr/bin/env python3
"""Render a terminal-style screencast (animated GIF) for the skill's README."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 700
BG = (13, 17, 23)        # github dark
FG = (201, 209, 217)
MUT = (139, 148, 158)
GRN = (63, 185, 80)
CYN = (88, 166, 255)
YEL = (210, 153, 34)
RED = (248, 81, 73)
PUR = (188, 140, 255)
CHROME = (22, 27, 34)

MENLO = "/System/Library/Fonts/Menlo.ttc"
ARIALB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"

def f(path, size, idx=0):
    try: return ImageFont.truetype(path, size, index=idx)
    except Exception: return ImageFont.truetype(path, size)

mono   = f(MENLO, 22)
monob  = f(MENLO, 22, 1)
mono_s = f(MENLO, 17)
title  = f(ARIALB, 46)
subt   = f(ARIAL, 25)
small  = f(ARIAL, 18)

frames, durations = [], []

def base():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # window chrome
    d.rectangle([0, 0, W, 44], fill=CHROME)
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([22+i*26, 15, 36+i*26, 29], fill=c)
    return img, d

def win_title(d, t):
    w = d.textlength(t, font=mono_s)
    d.text(((W-w)/2, 14), t, font=mono_s, fill=MUT)

def add(img, dur):
    frames.append(img.convert("P", palette=Image.ADAPTIVE, colors=128))
    durations.append(dur)

def hold(img, ms): add(img, ms)

# ---------- Scene A: title card ----------
def card(lines, hold_ms=1400):
    img, d = base()
    win_title(d, "Claude")
    total = sum(h for _,_,_,h in lines)
    y = (H+44-total)/2
    for text, fnt, col, lh in lines:
        w = d.textlength(text, font=fnt)
        d.text(((W-w)/2, y), text, font=fnt, fill=col)
        y += lh
    hold(img, hold_ms)

card([
    ("Criminal Discovery Assistant", title, FG, 70),
    ("A Claude skill — how to use it", subt, CYN, 50),
    ("", subt, FG, 20),
    ("github.com/legalrealist/criminal-discovery-assistant", small, MUT, 30),
], 1600)

# ---------- terminal screen renderer ----------
def term(title_txt, lines, typing=None, cursor=True, prompt_y=70):
    """lines: list of (text, color). typing: (text,color) partially shown handled by caller."""
    img, d = base()
    win_title(d, title_txt)
    y = prompt_y
    for text, col in lines:
        d.text((40, y), text, font=mono, fill=col)
        y += 32
    if typing is not None:
        text, col = typing
        d.text((40, y), text, font=mono, fill=col)
        if cursor:
            cx = 40 + d.textlength(text, font=mono)
            d.rectangle([cx+2, y+3, cx+13, y+26], fill=FG)
    return img

def type_line(title_txt, prev, prefix, body, col, step=2, char_ms=45, prompt_y=70):
    """Animate typing `body` after `prefix` on a fresh line."""
    n = len(body)
    i = 0
    while i <= n:
        img = term(title_txt, prev, typing=(prefix+body[:i], col), prompt_y=prompt_y)
        add(img, char_ms)
        i += step
    # final settle
    img = term(title_txt, prev, typing=(prefix+body, col), cursor=False, prompt_y=prompt_y)
    add(img, 250)

# ---------- Scene B: install ----------
T1 = "zsh — install the skill"
lines = []
type_line(T1, lines, "$ ", "cd ~/.claude/skills", FG)
lines = [("$ cd ~/.claude/skills", FG)]
type_line(T1, lines, "$ ", "git clone https://github.com/legalrealist/criminal-discovery-assistant.git", FG, step=3, char_ms=28)
lines = [("$ cd ~/.claude/skills", FG),
         ("$ git clone https://github.com/legalrealist/criminal-discovery-assistant.git", FG)]
hold(term(T1, lines, typing=None, cursor=False), 400)
lines += [("Cloning into 'criminal-discovery-assistant'... done.", MUT)]
hold(term(T1, lines, cursor=False), 700)
lines += [("", FG), ("✓ Skill installed. Start a new Claude conversation.", GRN)]
hold(term(T1, lines, cursor=False), 1500)

# ---------- Scene C: use it in Claude ----------
T2 = "Claude — United States v. Doe"
intro = [("You", PUR)]
prompt = "Get me up to speed on this CJA case — the discovery is in ~/cases/US-v-Doe"
# type the user's message
i, n, base_lines = 0, len(prompt), intro
while i <= n:
    img = term(T2, base_lines, typing=("  "+prompt[:i], FG))
    add(img, 26); i += 3
hold(term(T2, base_lines+[("  "+prompt, FG)], cursor=False), 700)

conv = intro + [("  "+prompt, FG), ("", FG), ("Claude", CYN)]
hold(term(T2, conv + [("  Reading the case folder…", MUT)], cursor=False), 700)

steps = [
    "  ✓ Inventoried 6 items + production letter → discovery-tracker.xlsx",
    "  ✓ Drafted transcript of 1 recording (bodycam BWC-001)",
    "  ✓ Mapped indictment → Count 1 §841 distribution; Count 2 §922(g) felon-in-possession",
    "  ✓ First-pass review of evidence on each count",
    "  ✓ Wrote case-memory.md (updates in place as new discovery arrives)",
]
shown = []
for s in steps:
    # brief 'working' tick
    hold(term(T2, conv + shown + [("  ● working…", YEL)], cursor=False), 280)
    shown.append((s, GRN))
    hold(term(T2, conv + shown, cursor=False), 520)
hold(term(T2, conv + shown, cursor=False), 1100)

# ---------- Scene D: outputs tree ----------
T3 = "Finder — ~/cases/US-v-Doe/_case-assistant"
tree = [
    ("_case-assistant/", CYN),
    ("├── discovery-tracker.xlsx      sortable inventory: Bates, source, count, flags", FG),
    ("├── case-memory.md              living case summary + production log", FG),
    ("└── transcripts/", FG),
    ("    └── bodycam_BWC-001.md      DRAFT — verify against recording", MUT),
]
img, d = base(); win_title(d, T3)
y = 80
for t,c in tree:
    d.text((40,y), t, font=mono, fill=c); y += 38
hold(img, 2600)

# ---------- Scene E: case-memory peek ----------
T4 = "case-memory.md"
peek = [
    ("# Case Memory — United States v. Marcus Doe — 25-CR-00417", FG, monob),
    ("", FG, mono),
    ("## Flags to investigate", YEL, monob),
    ("  • Brady: Jane Roe — a different man placed the bag (exculpatory)", FG, mono),
    ("  • Suppression: 35-min stop awaiting K-9 (Rodriguez); air-freshener basis", FG, mono),
    ("  • Inconsistency: consent vs. search-incident-to-arrest", FG, mono),
    ("", FG, mono),
    ("## Missing / referenced-but-not-produced", RED, monob),
    ("  • 911 call recording      • Officer Reyes body-worn camera", FG, mono),
    ("", FG, mono),
    ("  cites every item to its source file — nothing fabricated", MUT, mono_s),
]
img, d = base(); win_title(d, T4)
y = 70
for t,c,fnt in peek:
    d.text((40,y), t, font=fnt, fill=c); y += 36 if fnt is not mono_s else 30
hold(img, 3400)

# ---------- Scene F: end card ----------
card([
    ("First pass for attorney review — not a substitute.", subt, FG, 46),
    ("Local-only  •  cites to source  •  flags, doesn’t conclude", small, GRN, 40),
    ("", subt, FG, 16),
    ("github.com/legalrealist/criminal-discovery-assistant", small, CYN, 30),
], 2600)

out = os.path.join(os.path.dirname(__file__), "demo.gif")
frames[0].save(out, save_all=True, append_images=frames[1:], duration=durations,
               loop=0, optimize=True, disposal=2)
print(f"wrote {out}  ({len(frames)} frames, {os.path.getsize(out)//1024} KB)")
