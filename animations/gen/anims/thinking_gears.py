"""thinking-gears - Thinking variant: the gears in his head.   Preview:  python3 gen/preview.py anim thinking-gears

STORYBOARD (ms)   one loop = 12 350 ms; calm, one small payoff (the restart) per loop
     0  frame 0 = the reduced-motion still: Clawd at HOME, eyes up (half-step look_u) at two interlocking gears
        floating above his head (a big gold one, a small steel one).  They turn clockwise / counter-clockwise, one
        third of a tooth every 340 ms (three rotation positions, so the direction reads), always meshing.
  1360  a smooth blink at his raised gaze.  2720-3400 a short glance at you, then back up.
  4080  the gears slow down, each step longer than the last (380 ... 1000 ms); 5300 his lids droop (half): "hm?"
  7260  ... they stall.  7710 CREAK: they strain one step forward and slip back, strain ticks pulsing out on both
        sides (grow, spread, fade); a beat later his eyes go wide.
  8270  he blinks, eyes back up on the gears; 8570 his claw comes up (up, raise) and winds up out to the side (8750),
        then KNOCKS down on top of his head (8930), rebounds, KNOCKS again (9180): his eyes squeeze shut on each
        impact and knock marks spread from the spot.
  9360  JOLT: the gears hop a cell and kick back into motion; a spark grows and fades at the top of the mesh and a
        puff of steam swells out of the steel gear and drifts off.  They spin up fast (80 ms per step) and ease back
        to the steady pace by 10.3 s.  His eyes go wide, the claw comes down, then sparkle (it works!), and he gives
        a little nod (10650: eyes and claws dip).
 10990  back to watching (look_u); a blink at 12010; the steady turning flows into frame 0.
Eye closures: 1.36, 8.27, 8.93 + 9.18 (knocks), 10.65 (nod, eyes down), 12.01 s: uneven on purpose.

Face rig (as in thinking.py): the body layer draws him with a solid face; the face layer (FINE, half-size pixels)
holds only his black eye pixels, moved by a half-step gaze ('half/u' = the lower half of a raised eye), so a blink
closes over the pupil where he is looking.  Fine-line faces used: open, half, line, look_u, look_d, wide, sparkle.
Gears: the gold gear has 8 teeth, the steel one 6; both step a third of a tooth per frame (15 and 20 degrees), so
their rims move at the same speed and the teeth stay interlocked at the mesh (cols 15-16).  What every rotation
position shares (body, hub) lives in the 'core' layer, which only changes for the jolt; the 'teeth' layer holds
only what moves.  Light from the top-left on every tooth.
Layers: core | teeth | fx (creak, knock marks, spark, steam) | body | face.  All share LOOP.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'thinking-gears'
STATE = 'thinking (variant)'
DESC = ('Watches two interlocking gears turn above his head; they slow, stall and creak, so he knocks on his head '
        'twice and they jolt back to life with a spark and a puff of steam while he nods.')

# --------------------------------------------------------------------------------------------
# Gears.  Each gear = a round body + 2x2 teeth on a ring; three rotation positions a third of a tooth apart.
# --------------------------------------------------------------------------------------------
BX, BY = 7, 1                 # big gold gear: 10 x 10, cols 7-16, rows 1-10
SX, SY = BX + 8, BY + 1       # small steel gear: 8 x 8, cols 15-22, rows 2-9
_GOLD = ('j', 'y', 'J', 'J')  # base, light (top-left edges), shadow (bottom-right edges), hub
_STEEL = ('s', 'm', 'N', 'n')
# Gold teeth (top-left cell of each 2x2 tooth) per rotation position, clockwise: 0, 15 and 30 degrees.
_BIG_TEETH = [[(4, 0), (7, 1), (8, 4), (7, 7), (4, 8), (1, 7), (0, 4), (1, 1)],
              [(5, 0), (7, 2), (8, 5), (6, 7), (3, 8), (1, 6), (0, 3), (2, 1)],
              [(6, 1), (8, 3), (7, 6), (5, 8), (2, 7), (0, 5), (1, 2), (3, 0)]]
_MESH_OFFSET = 1              # which steel position meets gold position 0 (teeth in each other's gaps)


def _disc(size, r):
    c = (size - 1) / 2.0
    return {(x, y) for y in range(size) for x in range(size) if math.hypot(x - c, y - c) <= r}


def _hub(size):
    c = size // 2 - 1
    return {(c, c), (c + 1, c), (c, c + 1), (c + 1, c + 1)}


def _big(k):
    cells = _disc(10, 3.2)
    for x, y in _BIG_TEETH[k]:
        cells |= {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
    return cells


def _small(k):
    """6 teeth turning counter-clockwise, 20 degrees per position."""
    cells = _disc(8, 2.4)
    c = 3.5
    for i in range(6):
        th = math.radians(-20 * k + 60 * i)
        x0 = int(round(c + 3.2 * math.cos(th) - 0.5))
        y0 = int(round(c + 3.2 * math.sin(th) - 0.5))
        cells |= {(x, y) for x in (x0, x0 + 1) for y in (y0, y0 + 1) if 0 <= x < 8 and 0 <= y < 8}
    return cells


def _shade(cells, body, hub, mat, ox, oy):
    """{canvas cell: color}.  The round body is flat (it never changes as the gear turns, so it lives in the static
    core); each tooth takes the light: its outer edges facing down/right in shadow, up/left lit (top-left light)."""
    base, hi, lo, hc = mat
    out = {}
    for (x, y) in cells:
        if (x, y) in hub:
            c = hc
        elif (x, y) in body:
            c = base
        elif (x, y + 1) not in cells or (x + 1, y) not in cells:
            c = lo
        elif (x, y - 1) not in cells or (x - 1, y) not in cells:
            c = hi
        else:
            c = base
        out[(ox + x, oy + y)] = c
    return out


def _gears_px(k, dy):
    """Both gears at rotation position k (0-2), lifted dy rows: {cell: color} (gold in front at the mesh)."""
    px = _shade(_small((k + _MESH_OFFSET) % 3), _disc(8, 2.4), _hub(8), _STEEL, SX, SY + dy)
    px.update(_shade(_big(k), _disc(10, 3.2), _hub(10), _GOLD, BX, BY + dy))
    return px


def _split(dy):
    """-> (core: what all three positions share, [teeth per position])."""
    full = [_gears_px(k, dy) for k in range(3)]
    core = {p: c for p, c in full[0].items() if all(f.get(p) == c for f in full[1:])}
    return core, [{p: c for p, c in f.items() if core.get(p) != c} for f in full]


_GEARS = {dy: _split(dy) for dy in (0, -1)}


def _frame(px):
    f = Frame()
    for (x, y), c in px.items():
        f.put(x, y, c)
    return f


# --------------------------------------------------------------------------------------------
# Clawd: body poses (solid face; box coords for hand-drawn arms) + fine eye ink
# --------------------------------------------------------------------------------------------
def _with_arm(cells, **kw):
    """The kit pose with a hand-drawn right arm (box coords, normal 1-cell pixels, body color)."""
    p = clawd(eyes='blink', rarm='none', **kw)
    spr = p.sprite.over(Sprite(cells=[(x, y, '#') for x, y in cells], anchor=(0, 0)))
    return Pose(spr, p.anchors, dict(p.spec, rarm='custom'))


_POSES = {
    'stand': lambda: clawd(eyes='blink'),
    'down':  lambda: clawd(eyes='blink', larm='down', rarm='down'),       # the nod: both claws dip
    'up':    lambda: clawd(eyes='blink', rarm='up'),                      # the claw comes up ...
    'raise': lambda: clawd(eyes='blink', rarm='raise'),                   # ... beside his head ...
    'wind':  lambda: clawd(eyes='blink', rarm='wave'),                    # ... winds up out to the side ...
    'knock': lambda: _with_arm([(10, 2), (10, 1), (10, 0), (9, -1)]),      # ... and comes down on his head: knock!
}


def _body(name):
    f = Frame()
    put_clawd(f, _POSES[name]())
    return f


_GAZE = {'': (0, 0), 'u': (0, -1), 'd': (0, 1)}
_BASE = fine(_body('stand'))


def _eyes(expr):
    """FINE frame with only his eye ink for expr 'shape' or 'shape/gaze' (the gaze moves the ink one fine pixel)."""
    shape, _, gz = expr.partition('/')
    if shape in ('happy', 'content', 'squint'):
        raise ValueError('the user dislikes %r eyes' % shape)
    ff = fine_face(_BASE.copy(), _POSES['stand'](), expr=shape)
    gx, gy = _GAZE[gz]
    out = Frame(res=2)
    for (x, y), c in ff.px.items():
        if _BASE.px.get((x, y)) != c:
            out.px[(x + gx, y + gy)] = c
    out.meta = {'fine_face': [expr]}
    return out


# --------------------------------------------------------------------------------------------
# fx: each effect grows in and fades out over a few frames
# --------------------------------------------------------------------------------------------
_PUFF = get('smoke_puff')
_SPARK = [s.recolor({'j': 'o', 'y': 'W'}) for s in get('sparkle_small').frames]   # orange glint, white core
_WISP = Sprite(['m'], anchor=(0, 0))
# Strain ticks pulsing out on both sides of the pair (left of the gold gear, right of the steel one), rows 5-6.
_CREAK = [
    {(5, 5): 'N', (24, 6): 'N'},                                                   # a twitch ...
    {(5, 5): 'N', (5, 6): 'N', (3, 5): 'N', (24, 5): 'N', (24, 6): 'N', (26, 6): 'N'},   # ... a shudder ...
    {(3, 6): 'm', (26, 5): 'm'},                                                   # ... dying away
]
# Knock marks spreading from where the claw lands on his head (19, 11).
_KNOCKS = [
    {(18, 10): 'm', (20, 10): 'm'},
    {(17, 10): 'm', (21, 10): 'm', (19, 9): 'm'},
    {(16, 10): 'N', (22, 10): 'N'},
]
MESH_TOP = (16, 1)


def _fx(items):
    f = Frame()
    for kind, i in items:
        if kind == 'spark':
            f.place(_SPARK[i], *MESH_TOP)
        elif kind == 'wisp':
            f.place(_WISP, SX + 8, SY + 3)
        elif kind == 'puff':
            f.place(_PUFF.sprite(i), *[(SX + 9, SY + 3), (SX + 10, SY + 2), (SX + 11, SY + 1), (SX + 11, SY + 1)][i])
        else:
            for (x, y), c in {'creak': _CREAK, 'knock': _KNOCKS}[kind][i].items():
                f.put(x, y, c)
    return f


# --------------------------------------------------------------------------------------------
# tracks: (start ms, value); each value holds until the next start
# --------------------------------------------------------------------------------------------
STEADY = 340                                  # ms per rotation step (a third of a tooth)
STEADY_BEFORE = 12                            # 4080 ms of steady turning, then ...
SLOW_DOWN = (380, 460, 580, 760, 1000)        # ... each step longer than the last ...
STALL = STEADY_BEFORE * STEADY + sum(SLOW_DOWN)   # 7260: ... until they stop
CREAK = STALL + 450                           # 7710
BLINK2 = CREAK + 560                          # 8270
ARM_UP = CREAK + 860                          # 8570: up, raise, wind-up ...
KNOCK1 = ARM_UP + 360                         # 8930
KNOCK2 = KNOCK1 + 250                         # 9180
JOLT = KNOCK2 + 180                           # 9360
SPIN_UP = (90, 80, 90, 110, 140, 190, 250)    # the jolt step, then easing back to STEADY
SPIN = [JOLT + sum(SPIN_UP[:i]) for i in range(len(SPIN_UP) + 1)]   # step start times (SPIN[-1] = steady again)
STEADY_AFTER = 6
LOOP = SPIN[-1] + STEADY_AFTER * STEADY       # 12 350
AFTER = [SPIN[-1] + i * STEADY for i in range(STEADY_AFTER)]       # steady step start times after the spin-up


def _gear_track():
    """(t, (position, dy)).  Steady -> slow down -> stall + creak -> jolt -> spin up -> steady."""
    out, t, k = [], 0, 0

    def step(ms, dy=0):
        nonlocal t, k
        out.append((t, (k, dy)))
        t += ms
        k = (k + 1) % 3

    for _ in range(STEADY_BEFORE):
        step(STEADY)
    for ms in SLOW_DOWN:
        step(ms)
    assert t == STALL, t
    stall = (k - 1) % 3                          # the position it stopped on
    out.append((CREAK, (k, 0)))                  # CREAK: it strains one step forward ...
    out.append((CREAK + 110, (stall, 0)))        # ... and slips back
    t = JOLT
    for i, ms in enumerate(SPIN_UP):
        step(ms, dy=-1 if i == 0 else 0)         # the jolt: one step forward, hopping a cell; then spinning up
    for _ in range(STEADY_AFTER):
        step(STEADY)
    assert t == LOOP and k == 0, (t, k)          # the last step flows into frame 0's position
    return out


def _pose_track():
    return [
        (0, 'stand'),
        (ARM_UP, 'up'),           # his claw comes up ...
        (ARM_UP + 90, 'raise'),
        (ARM_UP + 180, 'wind'),   # ... winds up out to the side (anticipation) ...
        (KNOCK1, 'knock'),        # ... knock!
        (KNOCK1 + 120, 'raise'),  # rebound
        (KNOCK2, 'knock'),        # knock!
        (KNOCK2 + 120, 'raise'),
        (SPIN[2], 'up'),          # the claw comes down as they spin up
        (SPIN[3], 'stand'),
        (AFTER[1], 'down'),       # the nod: arms dip with his eyes
        (AFTER[1] + 180, 'stand'),
    ]


def _face_track():
    U = 'look_u'
    return [
        (0, U),
        (1360, 'half/u'), (1430, 'line/u'), (1510, 'half/u'), (1580, U),        # blink at his raised gaze
        (2720, 'open'),                                                        # a glance at you ...
        (3400, U),                                                             # ... back up
        (5300, 'half/u'),                                                      # they slow: lids droop, "hm?"
        (CREAK + 110, 'wide'),                                                 # the creak: wide eyes
        (BLINK2, 'half'), (BLINK2 + 70, 'line'), (BLINK2 + 150, 'half/u'), (BLINK2 + 220, U),   # blink, back up
        (ARM_UP + 180, 'half/u'),                                              # winding up: determined
        (KNOCK1, 'line/u'), (KNOCK1 + 120, 'half/u'),                          # knock: eyes squeeze shut
        (KNOCK2, 'line/u'), (KNOCK2 + 120, 'half/u'),                          # knock
        (SPIN[1], 'wide'),                                                     # the jolt: wide (a beat late)
        (SPIN[4], 'sparkle'),                                                  # it works!
        (AFTER[1], 'look_d'), (AFTER[1] + 180, 'open'), (AFTER[2], U),         # a little nod, back to watching
        (AFTER[5], 'half/u'), (AFTER[5] + 70, 'line/u'), (AFTER[5] + 150, 'half/u'), (AFTER[5] + 220, U),   # blink
    ]


def _fx_track():
    return [
        (0, []),
        (CREAK, [('creak', 0)]),
        (CREAK + 110, [('creak', 1)]),
        (CREAK + 240, [('creak', 2)]),
        (CREAK + 380, []),
        (KNOCK1, [('knock', 0)]),
        (KNOCK1 + 120, [('knock', 1)]),
        (KNOCK1 + 190, [('knock', 2)]),
        (KNOCK2, [('knock', 0)]),
        (KNOCK2 + 120, [('knock', 1)]),               # (the jolt follows on its heels)
        (SPIN[0], [('spark', 0)]),
        (SPIN[1], [('spark', 1), ('wisp', 0)]),
        (SPIN[2], [('spark', 2), ('puff', 0)]),
        (SPIN[3], [('spark', 1), ('puff', 1)]),
        (SPIN[4], [('spark', 0), ('puff', 2)]),
        (SPIN[5], [('puff', 2)]),
        (SPIN[6], [('puff', 3)]),
        (SPIN[7], []),
    ]


def _segments(keys):
    out = []
    for i, (t, v) in enumerate(keys):
        t2 = keys[i + 1][0] if i + 1 < len(keys) else LOOP
        assert t2 > t, (t, t2, v)
        out.append((v, t2 - t))
    return out


def build():
    gears = _segments(_gear_track())
    core = [(_frame(_GEARS[dy][0]), ms) for (k, dy), ms in gears]
    teeth = [(_frame(_GEARS[dy][1][k]), ms) for (k, dy), ms in gears]
    fx = [(_fx(v), ms) for v, ms in _segments(_fx_track())]
    body = [(_body(v), ms) for v, ms in _segments(_pose_track())]
    face = [(_eyes(v), ms) for v, ms in _segments(_face_track())]
    for lst in (core, teeth, fx, body, face):
        assert total_ms(lst) == LOOP
    return anim(NAME, DESC, [
        layer('core', core),
        layer('teeth', teeth),
        layer('fx', fx),
        layer('body', body),
        layer('face', face),                # fine-line eyes (half-size pixels)
    ], state=STATE)
