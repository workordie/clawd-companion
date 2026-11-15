"""typing-juggle - Typing (variant): the letters you type pop out of the box and Clawd juggles them.
Preview:  python3 gen/preview.py anim typing-juggle

He stands at HOME on the input box juggling two fridge-magnet letters, a red A and a blue B, in arcs
over his head. Your keystrokes come up out of the box: a green C rises beside him like a bubble, he
catches it and juggles all three for a moment, then flicks the newcomer up and away off the top (sent!,
a twinkle where it left) and juggles on with A and B. Next loop a fresh C comes up.

TIMING: one juggling step = 140 ms (two rests are longer); loop = 42 steps = 6800 ms, all layers share
it. Letters are the kit's 3 x 5 font, one color each (mid-tones: they read on both themes).
STORYBOARD (steps; R / L = his right / left hand on screen)
     0  frame 0 (the reduced-motion still): HOME, the A at the top of its arc above his head, his left
        hand (raised) just tossing the B up, and a green C four rows out of the box beside his right
        foot, waiting its turn; his eyes up on the top of the pattern
   0-6  two-letter juggle: the A comes down into his left hand while the B sails over to the right;
        like a real juggler he keeps his eyes up on the top of the pattern (the kit's look_u)
     7  REST (500 ms): both letters caught; a blink-glance down at the C peeking out of the box
  8-14  the B goes up again from the right, the A from the left; the C rises into his right hand
        (12) and he glances at it
 15-23  THREE: he tosses the C in (sparkle eyes) and juggles A, B, C in a cascade (a throw every 3
        steps, alternating hands, the arcs crossing over his head)
 24-27  his left hand flicks the C up and away: it flies off the top-left (his eyes follow it) and a
        gold twinkle marks where it left
 27-36  A and B, two-letter juggle again
    37  REST (700 ms): both caught; a look at you and a blink
 38-41  on again; a new green C starts coming up out of the box -> frame 0 (seamless)
Paths (letter top-left cells): throw spot R (21, 9) with the arm up, catch spot R (21, 11) with the arm
at his side (the letter sits against his hand); the arc R -> L goes (20,5) (17,2) (14,1) (11,2) (8,5)
(7,8) and lands in the left catch spot (7, 11); L -> R mirrors it. No two letters ever overlap
(asserted every step); they swap sides above his head without touching.
Body: the normal body at HOME, never resized (STYLE.md 0); only the arms move (side / up). No mouth.
Face: fine-line eyes (STYLE.md 0b) in their own fine layer: open, half, line, sparkle, with gaze offsets
(the kit's look_u a full step up, and half steps left / right / down).
Layers (back to front): body (static, solid face, no arms) | face (fine) | juggle (his arms + the three
letters + the twinkle and the little pop when a C breaks the surface: one layer, because every step
changes them together).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'typing-juggle'
STATE = 'typing (variant)'
DESC = ('Juggles the letters you type: a red A and a blue B arc over his head, a green C pops up out of '
        'the input box, he works it into a three-letter cascade, then flicks it up and away with a '
        'twinkle and juggles on.')

STEP = 140
N = 42                                        # steps per loop
COLOR = {'A': 'r', 'B': 'b', 'C': 'g'}
SPS = get('sparkle_small')

# ------------------------------------------------------------------------------- paths
_THROW = {'r': (21, 9), 'l': (7, 9)}           # held up, about to be thrown (arm 'up')
_LOW = {'r': (21, 11), 'l': (7, 11)}           # caught, against his hand (arm 'side')
_ARC_R = [(21, 9), (20, 5), (17, 2), (14, 1), (11, 2), (8, 5), (7, 8)]   # release, then 6 steps in the air


def _mirror(p):
    return (28 - p[0], p[1])


_ARC = {'r': _ARC_R, 'l': [_mirror(p) for p in _ARC_R]}
_AWAY_L = [(7, 9), (6, 5), (5, 1), (4, -3)]    # the C flicked up and away off the top-left

# releases (step, hand) of the two house letters; they cycle with the loop
_RELEASES = {
    'A': [(12, 'l'), (21, 'r'), (30, 'l'), (39, 'r')],      # (39 wraps: frame 0's A is at its apex)
    'B': [(0, 'l'), (9, 'r'), (18, 'l'), (27, 'r')],
}
# the newcomer, step by step: out of the box (bobbing up), into his right hand, one arc over to the
# left hand, then flicked away
_C = {38: (21, 19), 39: (21, 18), 40: (21, 17), 41: (21, 16), 0: (21, 16), 1: (21, 16),
      2: (21, 16), 3: (21, 16), 4: (21, 16), 5: (21, 16), 6: (21, 16), 7: (21, 16),
      8: (21, 15), 9: (21, 14), 10: (21, 13), 11: (21, 12), 12: _LOW['r'], 13: _LOW['r'],
      14: _THROW['r']}
for _i, _p in enumerate(_ARC['r']):
    _C[15 + _i] = _p                          # released 15, in the air 16-21
_C[22] = _LOW['l']
_C[23] = _THROW['l']
for _i, _p in enumerate(_AWAY_L):
    _C[24 + _i] = _p                          # released 24, gone after 27
_C_STATE = {12: 'low', 13: 'low', 14: 'throw', 15: 'rel', 22: 'low', 23: 'throw', 24: 'rel'}
_TWINKLE = {28: 1, 29: 2, 30: 1, 31: 0}       # sparkle_small frame where the C left (twinkle)
_TWINKLE_AT = (6, 1)
_POP = {38: 1, 39: 0}                          # a tiny pop as the next C breaks the surface
_POP_AT = (24, 17)


def _house(letter, t):
    """(position, state) of the A or the B at step t: state 'rel' | 'air' | 'low' | 'throw'."""
    evs = sorted((s + k * N, h) for s, h in _RELEASES[letter] for k in (-1, 0, 1))
    last = max(e for e in evs if e[0] <= t)
    nxt = min(e for e in evs if e[0] > t)
    d = t - last[0]
    if d <= 6:
        return _ARC[last[1]][d], ('rel' if d == 0 else 'air')
    hand = 'l' if last[1] == 'r' else 'r'
    if t == nxt[0] - 1:
        return _THROW[hand], 'throw'
    return _LOW[hand], 'low'


def _pos(letter, t):
    if letter == 'C':
        return _C.get(t), _C_STATE.get(t, 'air')
    return _house(letter, t)


def _boxes_ok():
    for t in range(N):
        cells = {}
        for L in 'ABC':
            p, _ = _pos(L, t)
            if p is None:
                continue
            for i in range(3):
                for j in range(5):
                    if (p[0] + i, p[1] + j) in cells:
                        raise ValueError('step %d: %s overlaps %s' % (t, L, cells[(p[0] + i, p[1] + j)]))
                    cells[(p[0] + i, p[1] + j)] = L


_boxes_ok()


def _glyph(f, ch, p, col):
    """The kit's 3x5 font glyph with its top-left at p; only the cells inside the canvas are drawn
    (the C deliberately enters from below the canvas and leaves through the top)."""
    for gy, row in enumerate(FONT[ch]):
        for gx, bit in enumerate(row):
            x, y = p[0] + gx, p[1] + gy
            if bit == '1' and 0 <= x < W and 0 <= y < H:
                f.put(x, y, col)


def _letter_frame(letter, t):
    f = Frame()
    p, _ = _pos(letter, t)
    if p is not None:
        _glyph(f, letter, p, COLOR[letter])
    if letter == 'C':
        if t in _TWINKLE:
            f.place(SPS.sprite(_TWINKLE[t]), *_TWINKLE_AT)
        if t in _POP:
            f.place(SPS.sprite(_POP[t]), *_POP_AT)
    return f


# ------------------------------------------------------------------------------- Clawd
_TRUNK = Frame()
put_clawd(_TRUNK, clawd(eyes='blink', larm='none', rarm='none'))


def _arms_frame(t):
    """His arms at step t: up while a hand holds a letter at its throw spot (and releases it), else at
    his side (catching, holding low, or empty)."""
    arm = {'r': 'side', 'l': 'side'}
    for L in 'ABC':
        p, st = _pos(L, t)
        if st in ('throw', 'rel'):
            for h in 'rl':
                if p == _THROW[h]:
                    arm[h] = 'up'
    full = Frame()
    put_clawd(full, clawd(eyes='blink', larm=arm['l'], rarm=arm['r']))
    f = Frame({k: v for k, v in full.px.items() if k not in _TRUNK.px})
    f.meta = full.meta
    return f


# gaze offsets in fine (half-cell) pixels: 'U' is the kit's look_u (a full step up), with half steps
# sideways; 'dr' / 'r' half steps (down-right at the C in the box, right at the C in his hand)
_GAZE = {'c': (0, 0), 'U': (0, -2), 'Ul': (-1, -2), 'Ur': (1, -2), 'dr': (1, 1), 'r': (1, 0)}


def _face_frame(expr, look):
    """Only the fine eye ink: the kit's fine_face expression on his solid face, shifted by the gaze.
    Guard: every pixel stays well inside his face (so it never touches the background)."""
    p = clawd(eyes='blink')
    f = Frame()
    put_clawd(f, p)
    base = fine(f)
    ff = fine_face(base.copy(), p, expr=expr)
    dx, dy = _GAZE[look]
    ink = {(x + dx, y + dy): c for (x, y), c in ff.px.items() if base.px.get((x, y)) != c}
    x0, y0 = HOME
    for (x, y) in ink:
        if not (2 * (x0 + 1) < x < 2 * (x0 + 10) - 1 and 2 * y0 < y < 2 * (y0 + 6) - 1):
            raise ValueError('eye pixel (%d,%d) is off his face: %s %s' % (x, y, expr, look))
    g = Frame(ink, res=2)
    g.meta = {'fine_face': [(expr, expr)], 'gaze': look}
    return g


# ------------------------------------------------------------------------------- timeline
# beats: (step, ms, expr, gaze). A juggler keeps his eyes on the top of the pattern: 'U' (up), unless a
# step is scripted below. Every step gets at least one beat; the two rests are split for the face (the
# letters hold still).
_SPECIAL = {
    7: [(100, 'open', 'U'), (50, 'half', 'U'), (70, 'line', 'U'), (50, 'half', 'dr'),
        (230, 'open', 'dr')],                                  # rest 1: blink-glance at the C below
    12: [(STEP, 'open', 'r')], 13: [(STEP, 'open', 'r')],     # the C in his hand
    15: [(STEP, 'sparkle', 'U')], 16: [(STEP, 'sparkle', 'U')],     # three!
    25: [(STEP, 'open', 'Ul')], 26: [(STEP, 'open', 'Ul')], 27: [(STEP, 'open', 'Ul')],  # it flies off
    28: [(STEP, 'sparkle', 'Ul')],                            # ... sent! (the twinkle)
    37: [(260, 'open', 'c'), (50, 'half', 'c'), (90, 'line', 'c'), (50, 'half', 'c'),
         (250, 'open', 'c')],                                  # rest 2: a look at you and a blink
}


def _beats():
    out = []
    for t in range(N):
        for ms, expr, look in _SPECIAL.get(t, [(STEP, 'open', 'U')]):
            out.append((t, ms, expr, look))
    return out


def build():
    face, juggle = [], []
    for t, ms, expr, look in _beats():
        face.append((_face_frame(expr, look), ms))
        f = _arms_frame(t)
        for L in 'ABC':
            f = f.over(_letter_frame(L, t))
        juggle.append((f, ms))
    return anim(NAME, DESC, [
        static('body', _TRUNK),
        layer('face', face),
        layer('juggle', juggle),     # his arms + the letters: they change on the same steps
    ], state=STATE)
