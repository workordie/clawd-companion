"""The style-options sheet: A | B | C side by side, each one frame in 16:9 and 9:16 (at half size).

  python3 -I sheet.py          reads out/style-options/{A,B,C}-{16x9,9x16}.png, writes out/style-options.png

The frames come from capture.mjs (same moment in all three looks). Halving is an exact 2x2 box filter, so the
pixel art stays even (every cell is a whole number of pixels in the sheet too).
"""
import os
import sys
sys.path.insert(0, __import__('site').getusersitepackages())
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'out', 'style-options')
OUT = os.path.join(HERE, 'out', 'style-options.png')

OPTIONS = [
    ('A', 'In VS Code',
     'A faithful dark VS Code window with the Claude Code chat panel and real context (the patch\'s own code, a turn '
     'in progress), drawn at 2x like a Retina screen recording: Clawd at his true size on the input box.',
     ['Clawd 2x (6 px a cell)', 'captions: lower-third pill (16:9),', 'a band above the window (9:16)',
      'shows it\'s real UI', 'Clawd is small, most on phones']),
    ('B', 'Stage',
     'The input box blown up 6x into a dark stage: Clawd big and crisp on its top edge, the captions typed into '
     'the box with a caret, the clip name in its footer pill; a flash and a pixel-snapped shake on the drops.',
     ['Clawd 6x (18 px a cell)', 'captions typed into the box', '(above it in 9:16)',
      'boldest, reads best on phones', 'least literal about VS Code']),
    ('C', 'Pixel Lab',
     'Light and technical, on Clawd\'s own cell grid: black ink, the input box as a white card, heavy black '
     'captions, and every clip labelled like a sprite sheet inside a dashed outline of his 32x20 canvas.',
     ['Clawd 6x (18 px a cell)', 'captions: top left, black', 'clip name + loop length on',
      'every shot: shows the craft', 'light: busier, less "phonk"']),
]

BG = (20, 20, 22)
FG = (240, 240, 242)
DIM = (150, 150, 158)
LINE = (52, 52, 58)


def font(size, weight='Bold', mono=False):
    f = ImageFont.truetype('/System/Library/Fonts/SFNSMono.ttf' if mono else '/System/Library/Fonts/SFNS.ttf', size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def wrap(draw, text, f, width):
    lines, line = [], ''
    for word in text.split():
        test = f'{line} {word}'.strip()
        if draw.textlength(test, font=f) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]


M, GAP, COL = 64, 56, 960
HEAD = 200
W = M * 2 + COL * 3 + GAP * 2
label_h = 250
H = HEAD + label_h + 540 + 36 + 960 + M

sheet = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(sheet)
d.text((M, 52), 'clawd-companion · showcase video · pick a look', font=font(64, 'Heavy'), fill=FG)
d.text((M, 136), 'One frame per look, the same moment in each (working-forge). 16:9 = 1920x1080 and 9:16 = 1080x1920, '
       'shown at exactly half size. Full-size frames: out/style-options/*.png', font=font(28, 'Regular'), fill=DIM)

for i, (letter, name, desc, notes) in enumerate(OPTIONS):
    x = M + i * (COL + GAP)
    y = HEAD
    d.line([(x, y), (x + COL, y)], fill=LINE, width=2)
    d.text((x, y + 24), letter, font=font(96, 'Black'), fill=FG)
    d.text((x + 84, y + 44), name, font=font(58, 'Heavy'), fill=FG)
    yy = y + 140
    for ln in wrap(d, desc, font(25, 'Regular'), COL):
        d.text((x, yy), ln, font=font(25, 'Regular'), fill=DIM)
        yy += 34
    y += label_h
    wide = Image.open(os.path.join(SRC, f'{letter}-16x9.png')).convert('RGB').reduce(2)
    sheet.paste(wide, (x, y))
    d.rectangle([x - 1, y - 1, x + wide.width, y + wide.height], outline=LINE)
    d.text((x + wide.width - 10, y + wide.height + 6), '16:9', font=font(22, 'Medium', mono=True), fill=DIM, anchor='ra')
    y += 540 + 36
    tall = Image.open(os.path.join(SRC, f'{letter}-9x16.png')).convert('RGB').reduce(2)
    sheet.paste(tall, (x, y))
    d.rectangle([x - 1, y - 1, x + tall.width, y + tall.height], outline=LINE)
    nx = x + tall.width + 36
    d.text((nx, y + 4), '9:16', font=font(22, 'Medium', mono=True), fill=DIM)
    ny = y + 60
    for k, note in enumerate(notes):
        if k == 3:
            ny += 26
        d.text((nx, ny), note, font=font(26, 'Medium' if k < 3 else 'Semibold'), fill=FG if k >= 3 else DIM)
        ny += 38

sheet.save(OUT, optimize=True)
print(OUT, sheet.size)
