"""typing-drums - Typing (variant): Clawd drums along on the input box while you type.
Preview:  python3 gen/preview.py anim typing-drums

He stands at HOME on the input box with a drumstick in each hand and plays the box top beside his feet,
the way you play the keys: little bursts, pauses, a quick roll. Every hit throws gold sound ticks off
the box. He drums "see-saw" style, like real alternating strokes: one stick strikes while the other
lifts, so there is always one stick down on the box and one raised and ready (two raised sticks would
read as antlers).

TIMING: one 16th = 110 ms; changes sit on the 55 ms half-16th grid (no moment is shorter than 55 ms).
Loop = 72 16ths = 7920 ms; all layers share it.
STORYBOARD (16ths; R = right stick, L = left stick)
     0  frame 0 (the reduced-motion still): HOME, the right stick down on the box with its gold ticks,
        the left stick raised and ready, his eyes down on the box (on your text)
   0-18 a light groove in typing bursts: R L R . . . L R L R . . R . L   (a blink at 8.5)
  19-29 a pause: the left stick rests on the box, the right one ready; he looks up at you for a beat
        and blinks (23)
  30-35 the roll: R L R L, both sticks lift (34, the wind-up) and the ACCENT: both down at once,
        bigger ticks on both sides, sparkle eyes (35)
  37-42 the flourish: he lifts the right stick and twirls it once round his fist (8 directions,
        55 ms each), his eyes on it; the left stick rests on the box; caught, ready (sparkle: got it)
  48-71 back to the groove, relaxed: R L R . L R L . . R L, his eyes closed (thin lines) from 48 to
        62 to feel the beat, then open on the box again; the next R is frame 0 (seamless)
Stick poses (right hand; the left mirrors around x = 15): 'up' = ready (arm at his side, the stick
pointing up and out, its tip beside his shoulder, below his head-top), 'hit' (arm down, the bead tip on
the box top at row 19). Every stick is 4 cells (wood, tan bead tip) in every pose and twirl direction.
Body: the normal body at HOME, never resized (STYLE.md 0); only the arms move. No mouth, no blush.
Face: fine-line eyes (STYLE.md 0b) in their own fine layer: open, half, line, sparkle, and half-step
gaze offsets (look_d / look_r / look_u family). Blinks at 8.5 and 23, closed eyes 48-62.
Layers (back to front): body (static: his body with a solid face, no arms) | face (fine eye ink) |
drums (arms + sticks + ticks; one layer because they change on the same beats; drawn over the face, so
the twirling stick passes in front of him).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'typing-drums'
STATE = 'typing (variant)'
DESC = ('Drums along on the input box while you type: a stick in each hand, see-saw strokes in little '
        'bursts and pauses like typing, a roll and a two-stick accent, a stick twirl, and gold sound '
        'ticks on every hit.')

U = 110                      # one 16th (ms)
H = U // 2                   # the half-16th grid every change sits on
LOOP_U = 72
LOOP = LOOP_U * U

# ------------------------------------------------------------------------------- the score
# (16th, hand): 'r' / 'l' strike (the other stick lifts), 'b' both strike (the accent)
HITS = [
    (0, 'r'), (2, 'l'), (4, 'r'), (8, 'l'), (10, 'r'), (12, 'l'), (13, 'r'),     # typing bursts
    (16, 'r'), (18, 'l'),                                                       # ... and a pause
    (30, 'r'), (31, 'l'), (32, 'r'), (33, 'l'), (35, 'b'),                      # roll + accent
    (48, 'r'), (50, 'l'), (52, 'r'), (56, 'l'), (58, 'r'), (60, 'l'),           # eyes-closed groove
    (66, 'r'), (68, 'l'),
]
LIFTS = [(15, 'r'), (34, 'b'), (37, 'r')]   # extra lifts: before a repeated stroke, the accent's wind-up,
                                             # before the twirl
TWIRL = (38, 42)             # the right stick's twirl (16ths): one full turn, 8 directions x 55 ms

# eyes: (16th, expr, gaze); expr = FINE_EYES name, gaze = _GAZE key. Each holds until the next.
EYES = [
    (0, 'open', 'd'),
    (8.5, 'half', 'd'), (9, 'line', 'd'), (10, 'half', 'd'), (10.5, 'open', 'd'),
    (19, 'open', 'c'),                                           # the pause: a look at you
    (23, 'half', 'c'), (23.5, 'line', 'c'), (24.5, 'half', 'c'), (25, 'open', 'c'),
    (28, 'open', 'd'),
    (35, 'sparkle', 'c'),                                        # the accent
    (37, 'open', 'r'), (39, 'open', 'ur'), (41, 'open', 'r'),    # on the twirl
    (42, 'sparkle', 'c'),                                        # caught it
    (45, 'open', 'd'),
    (47.5, 'half', 'd'), (48, 'line', 'd'),                      # eyes closed, feeling the groove
    (61.5, 'half', 'd'), (62, 'open', 'd'),
]
_GAZE = {'c': (0, 0), 'd': (0, 1), 'r': (1, 0), 'ur': (1, -1)}   # fine (half-cell) offsets

# ------------------------------------------------------------------------------- sticks
WOOD, BEAD = 'T', 't'
# right hand: (arm, grip, tip) per pose; the left mirrors (x -> 30 - x)
_POSE_R = {
    'up':  ('side', (21, 15), (24, 13)),
    'hit': ('down', (21, 16), (24, 19)),
}
# the twirl round the 'out' grip (22, 14), clockwise from pointing right (the ready pose's side)
_TWIRL_GRIP = (22, 14)
_TWIRL_TIPS = [(25, 14), (25, 17), (22, 17), (19, 17), (19, 14), (19, 11), (22, 11), (25, 11)]


def _mx(x):
    return 30 - x


def _stick(f, grip, tip):
    pts = list(Frame().line(grip[0], grip[1], tip[0], tip[1], WOOD).px)    # drawn in order, grip first
    if len(pts) != 4 or pts[0] != grip or pts[-1] != tip:
        raise ValueError('stick %s -> %s is %d cells' % (grip, tip, len(pts)))
    for i, (x, y) in enumerate(pts):
        f.put(x, y, BEAD if i == 3 else WOOD)


def _events():
    """Per hand, the sorted (time ms, state) changes: 'hit' (down on the box) or 'up' (ready)."""
    ev = {'r': [], 'l': []}
    for u, h in HITS:
        t = int(u * U)
        if h == 'b':
            ev['r'].append((t, 'hit'))
            ev['l'].append((t, 'hit'))
        else:
            other = 'l' if h == 'r' else 'r'
            ev[h].append((t, 'hit'))
            ev[other].append((t, 'up'))
    for u, h in LIFTS:
        for hand in (('r', 'l') if h == 'b' else (h,)):
            ev[hand].append((int(u * U), 'up'))
    return {k: sorted(v) for k, v in ev.items()}


_EV = _events()


def _hand_state(hand, t):
    """'hit' / 'up' or ('twirl', i) for hand 'r' / 'l' at time t (ms, inside the loop)."""
    if hand == 'r' and TWIRL[0] * U <= t < TWIRL[1] * U:
        return ('twirl', (t - TWIRL[0] * U) // H)
    state = _EV[hand][-1][1]                     # wraps: the state left at the end of the loop
    for te, s in _EV[hand]:
        if te <= t:
            state = s
    return state


def _drums_frame(t):
    """Arms + sticks + ticks at time t (the arms are the kit pose minus his armless body)."""
    sr, sl = _hand_state('r', t), _hand_state('l', t)
    arm_r = 'out' if isinstance(sr, tuple) else _POSE_R[sr][0]
    full = Frame()
    put_clawd(full, clawd(eyes='blink', larm=_POSE_R[sl][0], rarm=arm_r))
    f = Frame({k: v for k, v in full.px.items() if k not in _TRUNK.px})
    f.meta = full.meta
    if isinstance(sr, tuple):
        _stick(f, _TWIRL_GRIP, _TWIRL_TIPS[sr[1] % 8])
    else:
        _stick(f, _POSE_R[sr][1], _POSE_R[sr][2])
    _, g, tp = _POSE_R[sl]
    _stick(f, (_mx(g[0]), g[1]), (_mx(tp[0]), tp[1]))
    _ticks(f, t)
    return f


# ------------------------------------------------------------------------------- ticks
# gold sound ticks thrown off the box where a bead hits (right tip (24, 19); the left mirrors), clear
# of the stick: contact = two short strokes (up-and-out, and along the box), then the same strokes
# one cell further out, shrunk to their outer cells, fading.
_TICKS = {
    0: [(26, 17), (27, 16), (26, 19), (27, 19)],
    1: [(28, 15), (28, 19)],
}
# the accent: a third stroke straight up, and every stroke a cell longer on the way out
_TICKS_BIG = {
    0: [(24, 16), (24, 15), (26, 17), (27, 16), (26, 19), (27, 19)],
    1: [(24, 14), (24, 13), (28, 15), (29, 14), (28, 19), (29, 19)],
}


def _ticks(f, t):
    for u, h in HITS:
        th = int(u * U)
        for k in (-LOOP, 0, LOOP):
            d = t - (th + k)
            if 0 <= d < 2 * U:
                cells = (_TICKS_BIG if h == 'b' else _TICKS)[0 if d < U else 1]
                for s in (('r', 'l') if h == 'b' else (h,)):
                    for x, y in cells:
                        f.put(x if s == 'r' else _mx(x), y, 'j')


# ------------------------------------------------------------------------------- face
def _eyes_at(t):
    cur = EYES[0]
    for e in EYES:
        if e[0] * U <= t:
            cur = e
    return cur[1], cur[2]


def _face_frame(t):
    """Only the fine eye ink: the kit's fine_face expression on his solid face, shifted by the gaze.
    Guard: every pixel stays well inside his face (never on its edge, so never touching the background)."""
    expr, look = _eyes_at(t)
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


# ------------------------------------------------------------------------------- build
_TRUNK = Frame()
put_clawd(_TRUNK, clawd(eyes='blink', larm='none', rarm='none'))


def _cuts():
    """Every time a layer changes, all on the 55 ms grid."""
    cuts = {0, LOOP}
    for u, _ in HITS:
        for d in (0, U, 2 * U):
            cuts.add(int(u * U + d) % LOOP)
    for u, _ in LIFTS:
        cuts.add(int(u * U))
    for i in range(TWIRL[0] * 2, TWIRL[1] * 2 + 1):
        cuts.add(i * H)
    for e in EYES:
        cuts.add(int(e[0] * U))
    cuts = sorted(cuts)
    assert all(c % H == 0 for c in cuts)
    return cuts


def build():
    cuts = _cuts()
    drums, face = [], []
    for a, b in zip(cuts, cuts[1:]):
        drums.append((_drums_frame(a), b - a))
        face.append((_face_frame(a), b - a))
    for lst in (drums, face):
        assert total_ms(lst) == LOOP
    return anim(NAME, DESC, [
        static('body', _TRUNK),
        layer('face', face),
        layer('drums', drums),
    ], state=STATE)
