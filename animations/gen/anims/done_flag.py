"""done-flag - done variant: Clawd plants a pennant on top of the blocks he built.

A little staircase of finished toy blocks stands on the input box at his left (green, gold, then a
tall blue one right beside him) with a red pennant planted on top. Once per loop he can't resist: he
pulls the flag out, waves it overhead (it swings from shoulder to shoulder, the pennant snapping),
and plants it back on the summit with a THUNK: specks fly, a twinkle blooms, his eyes sparkle. The
rest of the loop is a calm, proud wait while the pennant flutters in an uneven breeze.
Plain black eyes with the fine-line kit (STYLE.md 0b: open, half, line, sparkle) and one kit
glance (look_l, his eyes on the flag); no mouth, no blush, normal body size in every frame.

STORYBOARD (ms; one 7600 ms loop; every layer runs on the same clock)
     0  PLANTED! (frame 0 = the reduced-motion still): his left hand still on the pole, the flag
        standing on the blue block, two specks kicked up at its foot, a big twinkle beside the flag
        top, SPARKLE eyes, the pennant snapping up
   130  the specks fly out and settle, the twinkle thins (long plus, plus, dot) ... 520 gone
   520  his eyes open: he looks at you ... 760 he lets go of the pole: the long calm, the pennant
        fluttering on uneven holds (0.3-1.2 s)
  2300  blink (half, line, half)
  3300  a glance at his flag (kit look_l) ... 4000 back to you
  4900  blink ... a long hold
  6020  he looks at the flag again ... 6120 grabs the pole (out) ... 6280 its foot leaves the block
        (up) ... 6370 PULLS IT OUT (raise), eyes SPARKLE ... and waves it: high (6500), raise,
        wave (6720), raise, high (6950): the pole swings x 8-10 while the pennant snaps up and down
  7100  aims (raise, eyes back on the block top) ... 7480 THUNK: planted, eyes squeezed shut
  7600  = frame 0: specks, twinkle, sparkle eyes
Eye closures: 2.30, 4.90 and 7.48 s (the thunk's squeeze); gaps 2.6, 2.6, 2.4 s.
Layers (back to front): blocks (static) | flag (pole + pennant; behind Clawd, so his hand covers
the pole's foot when he holds it) | body (normal res, no eye cells) | face (FINE overlay: only his
half-size eye pixels) | fx (specks, twinkle). All on one clock, so the flag never leaves his hand.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'done-flag'
STATE = 'done (variant)'
DESC = ('Plants a red pennant on top of a little staircase of finished blocks: pulls it out, waves it '
        'overhead and plants it back with a thunk and a twinkle, then waits proudly while it '
        'flutters, blinking and glancing at it.')

LOOP = 7600
_SPK = get('sparkle')

# ------------------------------------------------------------------ the blocks (local props)
# Toy blocks, flat mid-tones (they read on both themes), a lighter top-left corner and a shaded
# right column. Bottom-left anchors: green 2x2 at x 1-2, gold 3x3 at x 3-5, blue 4x4 at x 6-9 (a
# clear column, x 10, between it and Clawd's body).


def _block(w, h, base, light, shade, name):
    rows = []
    for r in range(h):
        rows.append(''.join(light if (r == 0 and c == 0) else shade if c == w - 1 else base
                            for c in range(w)))
    return Sprite(rows, anchor=(0, h - 1), name=name)


_BLOCKS = [(_block(2, 2, 'g', 'g', 'G', 'block_green'), (1, GROUND)),
           (_block(3, 3, 'j', 'y', 'J', 'block_gold'), (3, GROUND)),
           (_block(4, 4, 'b', 'c', 'B', 'block_blue'), (6, GROUND))]

# ------------------------------------------------------------------ the flag (local prop)
# Red pennant (5x5 isosceles, lit top half red, lower half dark red) on a silver pole with a gold
# knob. Sprite space: pole at x 5 (rows 1-9), knob (5, 0), pennant x 0-4 rows 1-5 (tip at x 0).
# Anchor = the grip: the pole cell one above its foot. Planted, the grip is (8, 14) (his left hand
# 'out' holds it there) and the foot rests on the blue block's top; held up, the grip is his hand.
_PENNANT = ['...rr',
            '.rrrr',
            'rrrrr',
            '.RRRR',
            '...RR']
# flutter: row offset of the tip column (the rest of the cloth stays put)
_FLUTTER = {'A': 0, 'U': -1, 'D': 1}


def _flag(shape):
    cells = [(5, y, 'm') for y in range(1, 10)] + [(5, 0, 'j')]
    for y, row in enumerate(_PENNANT):
        for x, ch in enumerate(row):
            if ch != '.':
                cells.append((x, 1 + y + (_FLUTTER[shape] if x == 0 else 0), ch))
    return Sprite(cells=cells, anchor=(5, 8), name='pennant_' + shape)


_FLAGS = {k: _flag(k) for k in _FLUTTER}
PLANTED = (8, 14)              # grip when planted: the foot (8, 15) stands on the blue block (row 16)
STAR_AT = (13, 6)              # the twinkle blooms right of the flag top, clear of pole and head


def _segments(track):
    """[(t, value), ...] (t ascending, first t = 0) -> [(value, ms), ...] ending at LOOP."""
    out = []
    for i, (t, v) in enumerate(track):
        t2 = track[i + 1][0] if i + 1 < len(track) else LOOP
        assert t2 > t, (t, t2)
        out.append((v, t2 - t))
    return out


# ------------------------------------------------------------------ the timeline
# Clawd + flag: (t, left arm, flag held (True) or planted, pennant shape)
_MAIN = [
    (0, 'out', False, 'U'),       # PLANTED: hand still on the pole; the pennant snaps up ...
    (130, 'out', False, 'D'),     # ... and down ...
    (260, 'out', False, 'A'),     # ... and settles
    (760, 'side', False, 'A'),    # he lets go: the long calm, the pennant fluttering
    (1500, 'side', False, 'U'),
    (1800, 'side', False, 'A'),
    (2900, 'side', False, 'D'),
    (3150, 'side', False, 'A'),
    (4300, 'side', False, 'U'),
    (4550, 'side', False, 'A'),
    (5400, 'side', False, 'D'),
    (5700, 'side', False, 'A'),
    (6120, 'out', False, 'A'),    # grabs the pole ...
    (6280, 'up', True, 'A'),      # ... the foot leaves the block ...
    (6370, 'raise', True, 'D'),   # ... PULLS IT OUT
    (6500, 'high', True, 'U'),    # waves it: swing right ...
    (6610, 'raise', True, 'D'),
    (6720, 'wave', True, 'U'),    # ... swing left ...
    (6840, 'raise', True, 'D'),
    (6950, 'high', True, 'U'),    # ... swing right
    (7100, 'raise', True, 'A'),   # aims at the summit
    (7480, 'out', False, 'A'),    # THUNK
]
# (t, expression): a FINE_EYES name (fine-line kit) or a kit glance name
_FACE = [
    (0, 'sparkle'),               # planted!
    (520, 'open'),
    (2300, 'half'), (2360, 'line'), (2450, 'half'), (2510, 'open'),
    (3300, 'look_l'),             # a glance at his flag
    (4000, 'open'),
    (4900, 'half'), (4960, 'line'), (5050, 'half'), (5110, 'open'),
    (6020, 'look_l'),             # eyes on the flag, then the hand follows
    (6370, 'sparkle'),            # pulled out: celebrate
    (7100, 'look_l'),             # aims at the block top
    (7480, 'line'),               # THUNK: eyes squeezed shut
]
# (t, [(kind, arg), ...]): 'specks' (1-2), 'star' (sparkle frame)
_FX = [
    (0, [('specks', 1), ('star', 2)]),
    (130, [('specks', 2), ('star', 3)]),
    (260, [('star', 1)]),
    (390, [('star', 0)]),
    (520, []),
]
# specks kicked up at the pole's foot (tan, like dust; the right one stays clear of his hand at
# (9, 14) in 'out')
_SPECKS = {1: [(7, 15), (9, 15)], 2: [(6, 14), (5, 15)]}


def _body(larm):
    """Clawd with NO eye cells (kit 'blink'): the face layer draws every eye pixel."""
    f = Frame()
    put_clawd(f, clawd(eyes='blink', larm=larm))
    return f


_FACES = {}


def _face(expr):
    """FINE overlay holding only his half-size eye pixels: a FINE_EYES name drawn with fine_face(),
    or a kit glance (its eye cells at half size). Body + overlay composite exactly to
    fine(frame) + fine_face(...)."""
    if expr not in _FACES:
        p = clawd(eyes='blink')
        f = Frame()
        put_clawd(f, p)
        base = fine(f)
        if expr in FINE_EYES:
            ff = fine_face(base.copy(), p, HOME[0], HOME[1], expr)
        else:
            g = Frame()
            put_clawd(g, clawd(eyes=expr))
            ff = fine(g)
        out = Frame(res=2)
        out.px = {q: c for q, c in ff.px.items() if base.px.get(q) != c}
        out.meta = {'fine_face': [(expr, expr)]}
        _FACES[expr] = out
    return _FACES[expr].copy()


def _flag_frame(larm, held, shape):
    f = Frame()
    at = clawd(larm=larm).at('hand_l') if held else PLANTED
    f.place(_FLAGS[shape], *at)
    return f


def _blocks():
    f = Frame()
    for spr, at in _BLOCKS:
        f.place(spr, *at)
    return f


def _fx(items):
    f = Frame()
    for kind, arg in items:
        if kind == 'specks':
            for x, y in _SPECKS[arg]:
                f.put(x, y, 't')
        elif kind == 'star':
            f.place(_SPK.sprite(arg), *STAR_AT)
    return f


def build():
    main = _segments([(t, (a, h, s)) for t, a, h, s in _MAIN])
    body = [(_body(a), ms) for (a, h, s), ms in main]
    flag = [(_flag_frame(a, h, s), ms) for (a, h, s), ms in main]
    face = [(_face(v), ms) for v, ms in _segments(_FACE)]
    fx = [(_fx(v), ms) for v, ms in _segments(_FX)]
    for lst in (body, flag, face, fx):
        assert total_ms(lst) == LOOP
    return anim(NAME, DESC, [
        static('blocks', _blocks()),
        layer('flag', flag),
        layer('body', body),
        layer('face', face),
        layer('fx', fx),
    ], state=STATE)
