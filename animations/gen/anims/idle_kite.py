"""idle-kite - Idle variant: flying a kite.

STORYBOARD (s)    one loop = 18.00 s: long calm holds, one lull he pumps the kite out of, one gust with a leaf on it
   0.00  HOLD at HOME: left hand up on the line, eyes up on the kite (look_ul).  The yellow/blue harlequin kite
         rides high up-left (rows 1-8), its red/gold ribbon tail streaming downwind; the flower at the right leans
         in the same breeze (frame 0 = the reduced-motion still: it says 'breezy' twice)
   1.50  the tail ripples: an S-kink travels down it, one slow step every 1.25-1.35 s while the kite holds
   2.75  blink (with a ripple)
   4.10  (ripple) he glances at you (eyes open) .. and while he isn't looking the breeze drops:
   5.10  the flower stands up .. 5.45 he blinks at you, none the wiser ..
   5.85  .. the kite feels it: its tail drops limp and it wobbles (banks right, held 0.6 s) ..
   6.45  .. and sinks a cell, still banked; the line goes slack (a hook into his hand)
   7.25  he looks back up ..
   7.85  .. as the kite settles lower, upright, drifting downwind: the line droops in a U below his hand (1.0 s)
   8.85  double blink (8.85 / 9.10): oh!
   9.60  TUG: hand down a cell, eyes dip with it (look_l), the line snaps straight .. 9.74 the kite answers and
         climbs (its tail trailing straight below) as the hand comes back up .. 10.30 TUG .. 10.44 home again
  11.14  blink; the tail settles, hanging in the light air: a calm becalmed hold (1.3 s)
  12.56  the breeze comes back as a gust from the right: a leaf tumbles in at the edge (edge / face / back), one
         cell per step, riding high and fast (80-95 ms per step) with a lazy bob ..
  12.90  .. the gust bows the flower .. 13.23 he notices the leaf (look_r) .. 13.84 it passes over him (look_u) ..
  14.53  .. up to his left, slowing down (105-175 ms per step) as it nears the line (look_ul)
  14.83  it crosses the line by his hand and the gust reaches the kite: the line pulls taut, the tail streams out
         again and the kite banks left (held 0.55 s) .. 15.38 it lurches downwind, the lower tail lagging ..
  15.93  .. the tail catches up as the leaf, dropping clear of it, slides off the lower-left edge (gone 16.02)
  16.48  the gust passes: the kite rights itself and swings home, its tail stretching out behind .. 16.82 it
         catches up (blink)
  16.95  HOLD, identical to frame 0 -> loop: one calm 2.55 s hold across the seam
So the gust travels right to left as one wave of air: flower, leaf, line, kite.
Eye closures: 2.75, 5.45, 8.85 + 9.10, 11.14, 16.82 s; gaps 2.7 / 3.4 / 0.25 / 2.0 / 5.7 (the leaf holds his
eyes) / 3.9 s.
Energy (like idle: mostly holds): 46% of the loop in still moments of 1 s or more; 12 moments per loop change 10+
cells (the kite moving or banking, the flower, the tugs), at least 0.55 s apart except each tug and the climb
that answers it (0.14 s); nothing of that size for 6.6 s across the seam (16.48 -> 5.10) or 2.5 s after the tugs.

Kite: 7x8 harlequin diamond: yellow top-left panel with a gold rim on its outer edge (it holds the silhouette on
white), blue top-right and bottom-left, gold bottom-right (the shadow side: light from the top-left).
Moves one cell at a time, 0.55-1.9 s apart inside an episode (the tugs pump at 0.7 s), and holds still for 4.4 s
(10.44 -> 14.83) and 7.4 s (16.48 -> 5.85, across the seam) between episodes; a bank (roll) always leads the
move it belongs to by 0.55-0.6 s.  The banks are true ~18 degree rolls of the same diamond: top and bottom tips
shift a cell in opposite directions, the left and right spar tips a row in opposite directions, every edge an
even 1:2 / 2:1 / 1:1 run, the same four panels and the checker at the spar cross.  The ribbon hangs from cell
(3,7) of the sprite in every pose (part of the bottom tip in all three), so a bank alone never moves the tail.
Line: drawn from his hand to the bridle (hidden under the kite), under the kite.  Four tensions: taut (a straight
line: tug, gust), belly (a slight curve: normal), slack (a hook along his hand's row), limp (a U below his hand).
Tail: a traveling wave (each shape is the previous one moved one cell down the tail), so it ripples instead of
swinging like a stick; after a sideways move its lower half lags one beat and then catches up.
Leaf: one cell per step (its center), tumbling face -> edge -> back -> edge, entering and leaving at the edges.
Face: kit dots only (black ink, the user's look); look_ul only with the left arm 'up' (that arm cell frames the
corner eye, so it never touches the background), look_l with the arm down for a tug (the 'side' arm frames it),
look_r / look_u / open / blink anywhere.  Normal body throughout.
Layers (all one beat list, 18.00 s, so the line always meets his hand and his eyes always point at the action):
stem (static), flower head, kite + line (one layer: they change together), ribbon, body, leaf (in front of the
line it crosses).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'idle-kite'
STATE = 'Idle variant: flying a kite'
DESC = ('Flies a kite at home: it holds high in the breeze, its ribbon tail rippling; when the breeze drops he '
        'pumps it back up with two tugs, and a gust brings a leaf past him that makes the kite bank and swing.')

# ---------------------------------------------------------------- the kite (local sprites)
# 7x8 diamond, harlequin panels lit from the top-left: a = top-left (yellow) with e = its gold rim (the outer
# cells, so the yellow never touches the background), b = top-right (blue), B = bottom-left (blue),
# A = bottom-right (gold: the shadow side).  Anchor = the spar cross (3, 3) in every pose.
_K_UP = ['...e...',
         '..eab..',
         '.eaabb.',
         'eaaabbb',
         '.BBBAA.',
         '.BBBAA.',
         '..BBA..',
         '...B...']
# banked left (rolled ~18 degrees counter-clockwise): the top tip a cell left, the bottom tip a cell right, the
# left spar tip a row lower, the right one a row higher.  Edges: 1:2 (upper left), 2:1 (upper right), 1:2 (right),
# 1:1 (lower left).  The panel borders (the spars) roll with it: the cross-spar steps 2-3-2 cells across.
_K_L = ['..e....',
        '..ebb..',
        '.eaabbb',
        '.eaabAA',
        'eaBBAA.',
        '.BBBAA.',
        '..BBA..',
        '...BB..']
# banked right (rolled ~18 degrees clockwise): the mirror image of the outline; the panels follow the spars
_K_R = ['....e..',
        '..eee..',
        'eeaabb.',
        'BBaabb.',
        '.BBBAbb',
        '.BBBAA.',
        '..BAA..',
        '..BA...']
_KCOL = {'a': 'y', 'e': 'j', 'b': 'b', 'B': 'b', 'A': 'j'}


def _ksprite(rows):
    return Sprite([''.join(_KCOL.get(c, '.') for c in r) for r in rows], anchor=(3, 3), name='kite')


_KITE = {'up': _ksprite(_K_UP), 'l': _ksprite(_K_L), 'r': _ksprite(_K_R)}
_TIP = (0, 4)                   # where the ribbon hangs from, relative to the anchor: cell (3, 7), part of the
                                # bottom tip in every pose
_KHOME = (5, 4)                 # anchor at rest: kite x 2-8, rows 1-8
_BRIDLE = (2, 0)                # where the line ends: cell (5, 3), under the kite in every pose, so the line
                                # leaves the kite's lower right, clear of the tail

# ---------------------------------------------------------------- ribbon tail
# 5 cells hanging from the bottom tip; values = x offset of each cell from the tip.  The ripple is a traveling
# wave: _Q is the stream of steps fed in at the top (each frame the step pattern moves one cell down the tail),
# so an S-kink (+1 step) enters near the top and travels down to the end.  The first step never swings right
# (toward the line).
_Q = [-1, -1, 0, -1, -1, 0, 1, -1]
_WAVE0 = 3                     # phase shown in frame 0: a clean diagonal streaming downwind (the still)


def _wave(t):
    n = len(_Q)
    t += _WAVE0
    steps = [min(_Q[t % n], 0)] + [_Q[(t - k) % n] for k in (1, 2, 3)]
    offs = [0]
    for s in steps:
        offs.append(offs[-1] + s)
    return offs


_TAIL_SHAPE = {'hang': [0, 0, -1, -1, -1],      # becalmed: hangs nearly straight down
               'trail': [0, 0, 0, 0, 0]}        # climbing: trails straight below
_RIBCOL = ('r', 'j')                            # red / gold stripes (gold holds its edge on white)


# ---------------------------------------------------------------- the line
def _bezier(p0, c, p1):
    pts = []
    for i in range(129):
        t = i / 128.0
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]
        q = (int(math.floor(x + 0.5)), int(math.floor(y + 0.5)))
        if not pts or pts[-1] != q:
            pts.append(q)
    out = []
    for q in pts:                               # one pixel wide: drop L-corners and back-steps
        out.append(q)
        while len(out) >= 3 and abs(out[-3][0] - out[-1][0]) <= 1 and abs(out[-3][1] - out[-1][1]) <= 1:
            out.pop(-2)
    return out


# Slack lines hang from the kite and curl into his hand: the curl, as steps from the hand (then straight up to
# the bridle).  2 = slack: a hook along his hand's row; 3 = limp: a flat-bottomed U below his hand.
_DROOP = {2: [(0, 0), (-1, 0), (-2, -1)],
          3: [(0, 0), (-1, 1), (-2, 1), (-3, 0)]}


def _line(hand, end, sag):
    """sag 0 = taut (a straight line), 1 = belly (a slight curve), 2 = slack, 3 = limp (see _DROOP)."""
    (hx, hy), (ex, ey) = hand, end
    if sag == 1:
        return _bezier(hand, ((hx + ex) / 2.0 - 0.5, (hy + ey) / 2.0 + 1), end)
    pts = [hand] if sag == 0 else [(hx + a, hy + b) for a, b in _DROOP[sag]]
    f = Frame()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + [end]):
        f.line(x0, y0, x1, y1, 'm')
    return list(f.px)


# ---------------------------------------------------------------- Clawd
def _pose(eyes='look_ul', larm='up'):
    return clawd(eyes=eyes, larm=larm, rarm='side')


# ---------------------------------------------------------------- leaf (local)
# It tumbles face-on (a pointed blade, both diagonals) / edge-on (a sliver), so it reads as a leaf flipping
# over, not a green bit.  One green (g: 2.6:1 on white, 6.3:1 on dark).  face / edge / back are centered on
# their anchor; thin and tip only appear at the canvas edges (entering / leaving).
_LEAF = {
    'face': Sprite(['.gg', 'gg.'], anchor=(1, 0), name='leaf'),
    'edge': Sprite(['ggg'], anchor=(1, 0), name='leaf'),
    'back': Sprite(['gg.', '.gg'], anchor=(1, 0), name='leaf'),
    'thin': Sprite(['gg'], anchor=(0, 0), name='leaf'),
    'tip': Sprite(['g'], anchor=(0, 0), name='leaf'),
}

# ---------------------------------------------------------------- flower on the ground (library 'flower')
# It balances the kite across the scene and shows the wind: leaning downwind in the breeze (library frame 3),
# upright when the breeze drops (frame 0).  The stem is the same in both frames, so it is a static layer and
# only the head animates.
_FLOWER_AT = (26, GROUND)                     # stem base on the input box, right of Clawd
_FLOWER_FRAME = {'up': 0, 'lean': 3}
# local copy of those two library frames, used ONLY if the library is mid-save when this builds
_FLOWER_FALLBACK = {
    0: Sprite(['.p.p.', 'ppypp', '.rpr.', '..g..', '.Gg..', '..g..'], anchor=(2, 5), name='flower'),
    3: Sprite(['.p.p.', 'ppypp', '.rpr.', '...g.', '..Gg.', '...g.'], anchor=(3, 5), name='flower'),
}


def _flower_cells(i):
    """The library frame's cells, relative to its anchor (the stem base)."""
    try:
        spr = get('flower').sprite(i)
    except KeyError:
        spr = _FLOWER_FALLBACK[i]
    return {(x - spr.ax, y - spr.ay): ch for x, y, ch in spr.cells}


def _flower_parts():
    """(the part both poses share: a static sprite, {pose: sprite of the part that moves}); all anchored on the
    stem base, so frame.place(part, *_FLOWER_AT) puts each where the whole library flower would be."""
    cells = {k: _flower_cells(i) for k, i in _FLOWER_FRAME.items()}
    common = {p: ch for p, ch in cells['up'].items() if cells['lean'].get(p) == ch}

    def spr(d):
        return Sprite(cells=[(x, y, ch) for (x, y), ch in d.items()], anchor=(0, 0), name='flower')
    heads = {k: spr({p: ch for p, ch in c.items() if p not in common}) for k, c in cells.items()}
    return spr(common), heads


# ---------------------------------------------------------------- beats
# (ms, changes).  Keys: eyes, larm, kite=(dx, dy, tilt), sag, tail=wave index|'hang'|'trail', lag (x shift of the
# lower tail cells: follow-through; reset whenever 'tail' is set), flower='lean'|'up', leaf=(x, y, sprite)|None
_A = [  # riding high: calm holds, the tail rippling slowly
    (1500, dict(eyes='look_ul', larm='up', kite=(0, 0, 'up'), sag=1, tail=0, flower='lean', leaf=None)),  # frame 0
    (1250, dict(tail=1)),
    (120, dict(tail=2, eyes='blink')),               # a ripple and a blink
    (1230, dict(eyes='look_ul')),
]
_B = [  # a glance at you .. and the breeze drops: a lazy two-step settle
    (1000, dict(tail=3, eyes='open')),               # he glances at you ..
    (350, dict(flower='up')),                        # .. and the air goes still: the flower feels it first ..
    (110, dict(eyes='blink')),                       # (he blinks at you, none the wiser)
    (290, dict(eyes='open')),
    (600, dict(tail='hang', kite=(0, 0, 'r'))),      # .. the kite's tail drops and it wobbles (banks right) ..
    (800, dict(kite=(0, 1, 'r'), sag=2)),            # .. and sinks a cell: the line goes slack
    (600, dict(eyes='look_ul')),                     # he looks back up ..
    (1000, dict(kite=(-1, 2, 'up'), sag=3)),         # .. as it settles lower, drifting downwind: the line droops
    (110, dict(eyes='blink')),                       # oh!
    (140, dict(eyes='look_ul')),
    (100, dict(eyes='blink')),
    (400, dict(eyes='look_ul')),
]
_C = [  # tug .. tug: he pumps it back up in the light air
    (140, dict(eyes='look_l', larm='side', sag=0)),                                    # the line snaps straight
    (560, dict(eyes='look_ul', larm='up', kite=(0, 1, 'up'), tail='trail', sag=1)),    # .. it climbs
    (140, dict(eyes='look_l', larm='side', sag=0)),
    (700, dict(eyes='look_ul', larm='up', kite=(0, 0, 'up'), sag=1)),                  # .. home
    (120, dict(tail='hang', eyes='blink')),          # becalmed: the tail settles, hanging in the light air
    (1300, dict(eyes='look_ul')),
]


# D: the gust.  The leaf path: (x, y, sprite, ms, extra changes on that step).  One cell per step (the leaf's
# center); fast while it rides the gust, slowing as it nears his hand and the line, then dropping away.
def _leaf_path():
    # (center x, top row) per step, one cell apart: in at the right edge with a lazy bob, over his head, up to his
    # left, across the line by his hand, then a steeper drop (clear of the tail) and out at the lower-left edge
    pts = [(30, 5), (29, 4), (28, 4), (27, 4), (26, 4), (25, 5), (24, 5), (23, 5), (22, 4), (21, 4), (20, 5),
           (19, 5), (18, 6), (17, 6), (16, 6), (15, 6), (14, 7), (13, 7), (12, 7), (11, 8), (10, 8), (9, 9),
           (8, 10), (7, 11), (7, 12), (6, 13), (5, 14), (4, 15), (3, 16), (2, 16), (1, 17)]
    ms = [90, 85, 80, 80, 85, 80, 80, 85, 80, 85, 85, 90, 90, 95, 100, 105, 105, 115, 125, 135, 145, 160,
          175, 140, 125, 110, 100, 95, 90, 85, 85]
    tumble = ['edge', 'face', 'face', 'edge', 'back', 'back']      # a lazy flip: face .. edge .. back .. edge
    extra = {
        (27, 4): dict(flower='lean'),                          # the gust bows the flower
        (23, 5): dict(eyes='look_r'),                          # he notices the leaf
        (16, 6): dict(eyes='look_u'),                          # it passes over him
        (10, 8): dict(eyes='look_ul'),                         # .. up to his left, near the line
        (8, 10): dict(kite=(0, 0, 'l'), sag=0, tail=6),        # it crosses the line: the gust reaches the kite
        (5, 14): dict(kite=(-1, 0, 'l'), lag=1),               # the kite lurches downwind, the lower tail lags
    }
    path = [(31, 5, 'tip', 90, {})]                            # enters at the right edge
    for i, ((x, y), t) in enumerate(zip(pts, ms)):
        path.append((x, y, tumble[i % len(tumble)], t, extra.get((x, y), {})))
    path += [(0, 18, 'thin', 90, {}),                          # slides off the lower-left edge ..
             (0, 18, 'tip', 100, dict(tail=7))]                # .. as the kite's tail catches up
    return path


_E = [  # calm again
    (450, dict(leaf=None)),
    (350, dict(kite=(0, 0, 'up'), sag=1, lag=-1)),    # the gust passes: it rights itself and swings home ..
    (120, dict(tail=0, eyes='blink')),                # .. the tail catches up
    (1055, dict(eyes='look_ul')),                     # = frame 0: one calm hold across the seam
]


def _beats():
    leaf = [(ms, dict(ex, leaf=(x, y, spr))) for x, y, spr, ms, ex in _leaf_path()]
    return _A + _B + _C + leaf + _E


def _states():
    st, out = {}, []
    for ms, ch in _beats():
        if 'tail' in ch and 'lag' not in ch:
            ch = dict(ch, lag=0)
        st = dict(st, **ch)
        out.append((ms, dict(st)))
    return out


def _tail_cells(s):
    dx, dy, tilt = s['kite']
    tx, ty = _KHOME[0] + dx + _TIP[0], _KHOME[1] + dy + _TIP[1]
    r = s['tail']
    offs = list(_TAIL_SHAPE[r] if isinstance(r, str) else _wave(r))
    # the lower cells lag behind a sideways move.  Moving right (lag < 0) it starts a cell higher: a tail that
    # already streams at full slope would otherwise be clamped back to its own shape and hide the lag
    first = 2 if s['lag'] >= 0 else 1
    offs = [o + (s['lag'] if i >= first else 0) for i, o in enumerate(offs)]
    cells, prev = [], offs[0]
    for i, o in enumerate(offs):
        o = max(prev - 1, min(prev + 1, o))     # stay connected
        cells.append((tx + o, ty + 1 + i, _RIBCOL[i % 2]))
        prev = o
    return cells


def _kite_frame(s):
    """The line (from his hand to the bridle) with the kite on top of its end."""
    f = Frame()
    dx, dy, tilt = s['kite']
    ax, ay = _KHOME[0] + dx, _KHOME[1] + dy
    hand = _pose(s['eyes'], s['larm']).at('hand_l')
    for x, y in _line(hand, (ax + _BRIDLE[0], ay + _BRIDLE[1]), s['sag']):
        f.put(x, y, 'm')
    f.place(_KITE[tilt], ax, ay)
    return f


def _ribbon_frame(s):
    f = Frame()
    for x, y, ch in _tail_cells(s):
        f.put(x, y, ch)
    return f


def _body_frame(s):
    f = Frame()
    put_clawd(f, _pose(s['eyes'], s['larm']))
    return f


def _leaf_frame(s):
    f = Frame()
    if s['leaf']:
        x, y, k = s['leaf']
        f.place(_LEAF[k], x, y)
    return f


def _head_frame(heads, s):
    f = Frame()
    f.place(heads[s['flower']], *_FLOWER_AT)
    return f


def build():
    sts = _states()
    common, heads = _flower_parts()
    stem = Frame()
    stem.place(common, *_FLOWER_AT)
    # one still frame (no keyframes in the SVG), given the loop's length so all layers share one cycle
    layers = [layer('stem', [(stem, sum(ms for ms, _ in sts))]),
              layer('flower', [(_head_frame(heads, s), ms) for ms, s in sts]),
              layer('kite', [(_kite_frame(s), ms) for ms, s in sts]),
              layer('ribbon', [(_ribbon_frame(s), ms) for ms, s in sts]),
              layer('body', [(_body_frame(s), ms) for ms, s in sts]),
              layer('leaf', [(_leaf_frame(s), ms) for ms, s in sts])]
    return anim(NAME, DESC, layers, state=STATE)
