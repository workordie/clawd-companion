"""Walk cycle (DRAFT; '_' files are skipped by make.py).  Preview:  python3 gen/preview.py anim _walk_left

Modeled on the user's reference recording (2026-11-13): while walking, Clawd turns three-quarters
toward where he is going. His face slides to that side (the near eye on the body's edge), the far
side of his body becomes a 2-cell flank in body_shade, the far arm is shaded, and his four legs
scuttle in two alternating pairs while his body bobs half a cell. His body keeps its full 9 x 6 size:
the flank is part of those 9 columns (front 7 + flank 2), so he never gets narrower.

The cycle has 8 steps. Each leg is planted for 5 of them (contact, load, passing, late, push-off: the
foot slides back one cell under him, so it stays put on the ground while the patch slides the
element) and swings for 3 (lift, tuck, reach). The two pairs are half a cycle apart, so a pair always
stands. The body is down on the contact and load steps and up half a cell on passing and reach; the
arms swing in opposition to the front legs.

The SVG walks on the spot; the patch slides the element along the input box at WALK_CELLS_PER_S
(4 cells/s = 12 CSS px/s at the default 3 px per cell): a planted foot moves back one cell over its
4 step intervals = 250 ms, which is exactly 4 cells/s, so the feet don't skate.
Frame 0 is the still (contact pose). walk-left faces left; walk-right is its mirror image.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

WALK_CELLS_PER_S = 4
STEP_MS = (62, 63)                           # alternating: 8 steps = 500 ms per cycle (2 cells of travel)

FX0, FY0 = 2 * HOME[0], 2 * HOME[1]          # his box's top-left in half-size pixels
GROUND_F = 2 * H - 1                          # bottom fine row (39)

# Leg strokes, one cell (2 half-pixels) wide: x offset per fine row from the hip, facing LEFT
# (negative = forward). Planted legs run down to the ground (the last offset repeats); lifted legs
# have exactly the listed length, so their foot hangs above the ground.
LEG = {
    'contact': [0, 0, -1, -1],               # planted, reaching forward
    'load':    [0, 0, 0, -1],                # weight on it, foot still forward
    'pass':    [0, 0, 0, 0],                 # straight under the hip
    'late':    [0, 0, 0, 1],                 # foot drifting behind
    'push':    [0, 0, 1, 1],                 # pushing off, leaning back
    'lift':    [0, 1, 1],                    # foot off the ground, trailing
    'tuck':    [0, 0, 0],                    # swinging through, straight under the hip
    'reach':   [0, -1, -1],                  # swinging forward, about to land
}
LIFTED = ('lift', 'tuck', 'reach')
CYCLE = ['contact', 'load', 'pass', 'late', 'push', 'lift', 'tuck', 'reach']
BOB = [0, 0, 1, 1, 0, 0, 1, 1]               # fine rows up: down on contact/load, up on passing/reach
# Near arm (front, screen-left) swing per step as (dx, dy) in half-pixels; the far arm mirrors it
# (opposition). The near arm swings back while the front leg reaches forward.
ARM = [(1, 0), (1, 0), (0, 0), (-1, 0), (-1, 0), (-1, 0), (0, 0), (1, 0)]

# Left half-pixel of each leg, in his box; the far-side leg is shaded. Legs 1+4 and 2+3 share a phase,
# so the two middle legs move together and no two neighbours ever touch (a closed gap between legs
# would be filled black like an eye): the outer gaps are 3 half-pixels and strides are +-1.
HIPS = [(2, '#'), (7, '#'), (11, '#'), (16, '@')]
PHASE = [0, 4, 4, 0]                         # step offset into CYCLE per leg


def body_left(ff, bob=0, eyes='open', arm=0):
    """His turned body, facing left, drawn into the fine frame `ff`. bob = fine rows up (0 or 1).
    arm = the near arm's swing: 0 (resting), 1 (one fine row down; the far arm one up), or a
    (dx, dy) pair: the near hand swings dx half-pixels (negative = forward, positive = back behind
    his body) pivoting at the shoulder, and the arm drops dy rows; the far arm does the opposite."""
    x0, y0 = FX0, FY0 - bob
    adx, ady = (0, arm) if isinstance(arm, int) else arm
    for y in range(4):                       # far arm (right), shaded, behind the flank
        for x in range(2):
            ff.put(x0 + 20 + x - (adx if y >= 2 else 0), y0 + 5 - ady + y, '@')
    for y in range(12):                      # body: front 7 cells '#', flank 2 cells '@'
        for x in range(2, 20):
            ff.put(x0 + x, y0 + y, '#' if x < 16 else '@')
    for y in range(4):                       # near arm (left), 1 cell wide, 2 tall: shoulder + hand
        for x in range(2):
            ff.put(x0 + x + (adx if y >= 2 else 0), y0 + 4 + ady + y, '#')
    if eyes == 'open':                       # near eye on the body's edge, far eye mid-face
        for ex in (2, 12):
            for dy in range(2):
                for dx in range(2):
                    ff.put(x0 + ex + dx, y0 + 4 + dy, 'k')
    elif eyes == 'half':
        for ex in (2, 12):
            for dx in range(2):
                ff.put(x0 + ex + dx, y0 + 5, 'k')
    elif eyes == 'line':
        for ex in (2, 12):
            for dx in range(-1, 3):
                if 2 <= ex + dx < 16:
                    ff.put(x0 + ex + dx, y0 + 5, 'k')


def legs_left(ff, k, bob=0):
    hip = FY0 + 12 - bob
    for (hx, ch), ph in zip(HIPS, PHASE):
        pose = CYCLE[(k + ph) % 8]
        dxs = LEG[pose]
        rows = len(dxs) if pose in LIFTED else GROUND_F - hip + 1
        for r in range(rows):
            dx = dxs[min(r, len(dxs) - 1)]
            for w in (0, 1):
                ff.put(FX0 + hx + dx + w, hip + r, ch)


def frame_left(k, eyes='open'):
    """Step k (0-7) of the cycle, facing left."""
    ff = Frame(res=2)
    k %= 8
    bob = BOB[k]
    body_left(ff, bob=bob, eyes=eyes, arm=ARM[k])
    legs_left(ff, k, bob=bob)
    ff.meta.setdefault('clawd', []).append((HOME[0], HOME[1], dict(eyes=eyes, body='walk')))
    return ff


def mirrored(ff):
    """The same fine frame flipped left-right about his home box (so walk-right stays at HOME)."""
    out = Frame(res=2)
    axis = 2 * FX0 + 21                      # box spans fine x FX0 .. FX0 + 21
    for (x, y), c in ff.px.items():
        out.px[(axis - x, y)] = c
    out.meta = dict(ff.meta)
    return out


# Four strides (2 s) with one smooth blink placed off the beat, so a long walk isn't mechanical.
BLINK = {(1, 5): 'half', (1, 6): 'line', (1, 7): 'line', (2, 0): 'half'}


def cycle(facing='left'):
    seq = []
    for s in range(4):
        for k in range(8):
            eyes = BLINK.get((s, k), 'open')
            seq.append((frame_left(k, eyes), STEP_MS[k % 2]))
    if facing == 'right':
        seq = [(mirrored(f), ms) for f, ms in seq]
    return seq


def build_walk(facing):
    name = 'walk-' + facing
    desc = ('Walking %s: turned three-quarters, scuttling legs, a half-cell bob, arms swinging. Loops on the '
            'spot; the patch slides him %d cells/s.' % (facing, WALK_CELLS_PER_S))
    return anim(name, desc, [layer('body', cycle(facing))], state='walking (moving along the input box)')


def standing(facing='left', eyes='open'):
    """Turned three-quarters but standing still (for a spin or a look over his shoulder): the walk body
    on his normal 1-cell legs, straight down. A fine frame at HOME."""
    ff = Frame(res=2)
    body_left(ff, bob=0, eyes=eyes, arm=0)
    hip = FY0 + 12
    for hx, ch in HIPS:
        for r in range(GROUND_F - hip + 1):
            for dx in (0, 1):
                ff.put(FX0 + hx + dx, hip + r, ch)
    ff.meta.setdefault('clawd', []).append((HOME[0], HOME[1], dict(eyes=eyes, body='turned')))
    return mirrored(ff) if facing == 'right' else ff
