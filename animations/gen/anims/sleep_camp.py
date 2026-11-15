"""sleep-camp - Sleep variant: dozing off by a campfire.   Preview:  python3 gen/preview.py anim sleep-camp

A night out camping, all set up on the input box: a little canvas tent on the left, a crackling campfire on
the right, and Clawd at HOME zipped into a violet mummy sleeping bag, the hood framing his face, one arm out
of the bag holding a marshmallow on a stick over the fire.  Thin fine-line lids (STYLE.md 0b: fine() +
fine_face(), no mouth, no blush); his body never changes size: he breathes with his arm (it rises a cell on
each slow breath in, lifting the stick), and only the stick tips as he nods off.

STORYBOARD (s)   one loop = 22.0 s (Clawd, stick, face, pop and Zs); the flames and embers loop on their own
   0.00  frame 0 (the reduced-motion still): asleep in the bag, the marshmallow held over the flames, a z
         half way up its float over the tent.
   1.10  breath 1: his arm and the stick rise a cell (1.4 s) and sink back.  Breaths start 1.10 / 5.80 /
         10.40 / 16.60 / 20.30 s (gaps 4.7 / 4.6 / 6.2 / 3.7 / 2.8: uneven, slower as he sinks deeper).
   7.60  nodding off: on the out-breath his grip slackens and the stick tips down a cell; 12.30 a second
         cell: the marshmallow hangs just over the flame tips.
  14.20  POP: a log pops, two sparks jump out of the fire.  14.30 one eye flies open (the one nearest the
         fire), 14.40 he jerks the stick up (a cell above where it started), 14.55 the eye droops to a sleepy
         'half' and glances at the fire, 15.25 he lets the stick settle back to where it started, 15.45 the
         lid drops ('half' > 'line', 15.70).  Asleep again.
         Zs puff out at 3.00 and 20.80 and float up and to the left over the tent; the 20.80 one is half way
         up in frame 0.
Ambient, on their own loops so the fire never repeats exactly: the flames flicker through four shapes on a
slow, uneven 2.97 s cycle (no strobing: each shape holds 0.33-0.9 s), and an ember rises from the fire,
drifts right and fades (4.31 s).
Layers: set (static: tent, logs and stones, the bag with Clawd's eyeless face in its hood) | flames | embers |
arm (his arm stub, the stick and the marshmallow) | face (FINE: only his eye ink) | pop | zzz.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'sleep-camp'
STATE = 'sleep (variant)'
DESC = ('Camps out on the input box: zipped into a violet sleeping bag beside his little tent, he dozes off '
        'holding a marshmallow over a crackling campfire; the stick droops toward the flames until a log pops, '
        'he jerks it up with one sleepy eye and drifts off again while Zs float up.')

LOOP = 22000
FLAME_LOOP = 2970
EMBER_LOOP = 4310
HX, HY = HOME

# ---------------------------------------------------------------- the set
# A little A-frame canvas tent (lit left face tan, shaded right face wood), its door open on a dark inside
# (graphite, so the doorway still reads on the dark theme), the flaps tied back in paper white.  Anchor =
# bottom-centre; it stands on the input box at x 5.
TENT = Sprite([
    '....d....',
    '...tTT...',
    '..ttTTT..',
    '.ttwnTTT.',
    '.twnnnwT.',
    'ttnnnnnwT',
    'tnnnnnnnT',
], anchor=(4, 6), name='tent')
TENT_AT = (5, GROUND)

# Campfire: crossed logs glowing where they cross, a ring of stones (static); the flames are their own layer.
FIRE_X = 26                                  # centre column of the fire
LOGS = Sprite([
    'mTdOoRTs',
    'sNdTTdNs',
], anchor=(4, 1), name='campfire_logs')
# Four flame shapes (red rim, orange, yellow, a pale-yellow heart), 8 wide like the logs, standing on them.
FLAMES = [
    ['...r....',
     '...rr...',
     '..rorr..',
     '..oyyo..',
     '.royYor.'],
    ['....r...',
     '...rr...',
     '..rror..',
     '..oyyo..',
     '.roYyor.'],
    ['........',
     '...r.r..',
     '..rorr..',
     '.royyor.',
     '.royYor.'],
    ['..r.....',
     '..rr....',
     '..rorr..',
     '..oyyor.',
     '.royYor.'],
]
FLAME_SEQ = [(0, 900), (1, 330), (3, 520), (2, 400), (1, 470), (3, 350)]     # sums to FLAME_LOOP

# The violet mummy bag: a hood framing his face (lavender lit edge, deep-violet shade on the right) and the
# quilted body (deep-violet baffle lines).  His right arm comes out through the side.
HOOD = Sprite([                              # x 9-21 at HOME: a soft frame around his whole face (rounded
    '..lvvvvvvvV..',                         # corners, never over it)
    '.l.........V.',
    '.v.........V.',
    '.v.........V.',
    '.v.........V.',
], anchor=(0, 0), name='bag_hood')
BAG_BODY = Sprite([
    '.lvvvvvvvvvV.',
    'lvVVVVVVVVVvV',
    'vvvvvvvvvvvvV',
    'VVVVVVVVVVVVV',
], anchor=(0, 0), name='bag_body')
_FACE_POSE = clawd(eyes='blink', larm='none', rarm='none', legs='none')   # his face in the hood (eyes on the fine layer)


def _set():
    f = Frame()
    f.place(TENT, *TENT_AT)
    f.place(LOGS, FIRE_X, GROUND)
    put_clawd(f, _FACE_POSE)
    f.place(HOOD, HX - 1, HY - 1)
    f.place(BAG_BODY, HX - 1, HY + 4)
    return f


# ---------------------------------------------------------------- his arm, the stick, the marshmallow
# The arm stub pokes out of the bag at x 21; the stick (wood) runs up and right from his claw to a
# marshmallow (white top, toasted golden-brown underside) over the flames.  lift = -1 while breathing in (the arm and
# stick ride up a cell), droop = how far the tip has sunk as he nods off (-1 = jerked up after the pop).
_ARM = Pose.from_rows(['.' * 12] * 2 + ['...........#'] * 2, name='clawd_arm_out')


def _arm(lift, droop):
    f = Frame()
    put_clawd(f, _ARM, HX, HY + lift)
    hx, hy = HX + 12, HY + 2 + lift          # first stick cell, just right of his claw
    tx, ty = FIRE_X, 10 + lift + droop       # marshmallow's lower-left cell
    f.line(hx, hy, tx - 1, ty + 1, 'T')
    f.put(tx, ty - 1, 'W')                   # white top, lit from the top-left; silver shade on the right
    f.put(tx + 1, ty - 1, 'm')               # (so it keeps its shape on the light theme too); its
    f.put(tx, ty, 't')                       # underside toasted golden-brown by the fire
    f.put(tx + 1, ty, 'T')
    return f


# ---------------------------------------------------------------- face (fine layer: eye ink only)
# (screen-left eye, screen-right eye, gaze of the screen-right eye in fine pixels (dx, dy)).
FACES = {
    'asleep': ('line', 'line', (0, 0)),
    'startle': ('line', 'open', (0, 0)),     # the eye nearest the fire flies open
    'peek': ('line', 'half', (1, 0)),        # .. droops to a sleepy half lid, glancing at the fire
    'half': ('line', 'half', (0, 0)),
}


def _face(name):
    left, right, (gx, gy) = FACES[name]
    f = Frame()
    put_clawd(f, _FACE_POSE)
    base = fine(f)
    ff = fine_face(base.copy(), _FACE_POSE, expr=left, right=right)
    split = 2 * (HX + 5)
    out = Frame(res=2)
    for (x, y), ch in ff.px.items():
        if base.px.get((x, y)) != ch:
            if x >= split:
                x, y = x + gx, y + gy
            out.px[(x, y)] = ch
    assert set(out.px.values()) <= {EYE_INK}
    assert all(base.px.get(k) == '#' for k in out.px), 'his eye ink must sit on his face'
    out.meta = {'fine_face': [(left, right, (gx, gy))]}
    return out


# ---------------------------------------------------------------- master clock
POP = 14200
LIFT = [                                     # (t, lift): -1 = breathing in
    (0, 0),
    (1100, -1), (2500, 0),
    (5800, -1), (7200, 0),
    (10400, -1), (11900, 0),
    (16600, -1), (17900, 0),
    (20300, -1), (21500, 0),
]
DROOP = [                                    # (t, droop)
    (0, 0),
    (7600, 1),                               # nodding off: the tip sinks a cell ..
    (12300, 2),                              # .. and another: right over the flame tips
    (POP + 200, -1),                         # jerked up (a cell above where it started) ..
    (POP + 1050, 0),                         # .. and let settle
]
FACE = [
    (0, 'asleep'),
    (POP + 100, 'startle'),
    (POP + 350, 'peek'),
    (POP + 1250, 'half'),
    (POP + 1500, 'asleep'),
]
# The pop: two sparks jump out of the logs and arc away (one up-left toward him but well short, one up-right).
POP_STEPS = [                                # (dt, [(x, y, ch)])
    (0, [(25, 16, 'y'), (27, 16, 'y'), (26, 15, 'W')]),
    (100, [(24, 14, 'y'), (28, 14, 'y')]),
    (200, [(23, 13, 'o'), (29, 13, 'o')]),
    (300, [(23, 14, 'O'), (30, 13, 'O')]),
    (400, []),
]

# Zs: library z_small / z_medium floating up and to the left over the tent.
Z_PATH = [                                   # (item, centre x, centre y, ms)
    ('z_small', 9, 8, 380),
    ('z_small', 8, 7, 420),
    ('z_small', 7, 6, 470),
    ('z_medium', 6, 4, 560),
    ('z_medium', 5, 3, 520),
    ('z_small', 4, 2, 400),
]
Z_BIRTHS = (3000, 20800)


def _at(keys, t, default=None):
    v = default
    for k, s in keys:
        if k <= t:
            v = s
    return v


def _z_frame(t):
    life = sum(z[3] for z in Z_PATH)
    f = Frame()
    for b in Z_BIRTHS:
        age = (t - b) % LOOP
        if age >= life:
            continue
        acc = 0
        for item, cx, cy, ms in Z_PATH:
            if age < acc + ms:
                f.place(get(item).sprite(0), cx, cy)
                break
            acc += ms
    return f


def _z_keys():
    starts, acc = [], 0
    for z in Z_PATH:
        starts.append(acc)
        acc += z[3]
    return {(b + s) % LOOP for b in Z_BIRTHS for s in starts + [acc]}


def _pop_frame(t):
    f = Frame()
    dt = t - POP
    cur = None
    for d, px in POP_STEPS:
        if 0 <= d <= dt:
            cur = px
    for x, y, ch in cur or ():
        f.put(x, y, ch)
    return f


# ---------------------------------------------------------------- ambient loops
def _flames():
    out = []
    for k, ms in FLAME_SEQ:
        f = Frame()
        f.place(Sprite(FLAMES[k], anchor=(4, 4), name='flames'), FIRE_X, GROUND - 2)
        out.append((f, ms))
    assert total_ms(out) == FLAME_LOOP
    return out


def _embers():
    """One ember rises out of the flames, drifts right of the marshmallow and fades (gold > orange > rust)."""
    steps = [((27, 12), 'y', 200), ((28, 10), 'o', 260), ((28, 8), 'o', 300), ((29, 6), 'O', 340)]
    out = [(Frame(), EMBER_LOOP - sum(s[2] for s in steps))]
    for (x, y), ch, ms in steps:
        f = Frame()
        f.put(x, y, ch)
        out.append((f, ms))
    return out


def build():
    keys = {0}
    for track in (LIFT, DROOP, FACE):
        keys |= {t for t, _ in track}
    keys |= {POP + d for d, _ in POP_STEPS}
    keys |= _z_keys()
    keys = sorted(keys)
    segs = [(t, (keys[i + 1] if i + 1 < len(keys) else LOOP) - t) for i, t in enumerate(keys)]
    for t, ms in segs:
        assert ms >= 40, 'a %d ms sliver at %d ms' % (ms, t)

    arm, fc, pop, zz = [], [], [], []
    for t, ms in segs:
        arm.append((_arm(_at(LIFT, t, 0), _at(DROOP, t, 0)), ms))
        fc.append((_face(_at(FACE, t, 'asleep')), ms))
        pop.append((_pop_frame(t), ms))
        zz.append((_z_frame(t), ms))
    for lst in (arm, fc, pop, zz):
        assert total_ms(lst) == LOOP
    return anim(NAME, DESC, [
        static('set', _set()),
        layer('flames', _flames()),
        layer('embers', _embers()),
        layer('arm', arm),
        layer('face', fc),
        layer('pop', pop),
        layer('zzz', zz),
    ], state=STATE)
