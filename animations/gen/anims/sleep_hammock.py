"""sleep-hammock - Sleep variant: an afternoon nap in a hammock.   Preview:  python3 gen/preview.py anim sleep-hammock

A striped green hammock hangs between two little wooden posts on the input box.  Clawd naps in it at HOME
in a straw sun hat, sunk in up to his chest, his arm stubs draped over the rim; thin fine-line lids
(STYLE.md 0b: fine() + fine_face(), no mouth, no blush, never resized).  His body never changes size: he
breathes with his arms (they hang over the rim, and rise a cell with each slow breath in), the sway moves
the whole hammock and him one cell, and the sling always stops a row below his eyes.

STORYBOARD (s)   one loop = 24.0 s; every layer runs on this clock
   0.00  frame 0 (the reduced-motion still): asleep in the hammock at rest, hat on, arms hanging over the
         rim, a little z half way up its float beside him.
   1.20  breath 1: his arms rise a cell (1.4 s) and sink back.  Breaths start 1.20 / 6.00 / 11.00 / 15.60 /
         20.90 s (gaps 4.8 / 5.0 / 4.6 / 5.3 / 4.3 s: uneven).  A z puffs out on the exhales at 2.60 and 17.00
         and floats up and to the right, over the right post; the 17.00 one is followed by a second (22.90),
         which is the z half way up in frame 0.
   8.90  a breeze: two wind streaks rush in from the left; the gust catches the hat's brim (9.06): it tips
         up, lifts off his head (9.14) and hangs in the air two rows up, drifting right with the gust ..
   9.30  .. the gust pushes the hammock: it sways right, back through the middle (fast), left, and settles
         in smaller swings (+1 0.90 / -1 0.80 / +1 0.55 s, the middle crossings 0.30 / 0.40 s), still at 12.25 ..
   9.66  .. the hat rocks and drops back onto his head (9.86, a beat after the hammock reaches the right; one
         cell of bounce, settled 10.10).  One eye cracks a sleepy 'half' and peeks up at the brim (10.30),
         stays a moment, closes (11.05).  Breath 3 rides through the sway.
  12.25  calm again until the seam: breaths 4 and 5, a z, the last exhale ends well before the loop seam.
Layers: posts (static) | hammock (ropes, Clawd's eyeless arm-less body, the sling in front of him; it only
changes when it sways) | arms (his two stubs: the breathing) | face (FINE: only his eye ink) | hat (on his
head, swaying with him, or in the air) | zzz | wind.  All on the one 24 s clock; no two keys closer than
50 ms (build() asserts >= 40 ms).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'sleep-hammock'
STATE = 'sleep (variant)'
DESC = ('Naps in a striped hammock strung between two little posts, a straw sun hat on his head: his arms rise '
        'and fall with slow breaths and a z floats up, then a breeze lifts his hat and rocks the hammock, the '
        'hat drops back on and he peeks up at it with one sleepy eye.')

LOOP = 24000
HX, HY = HOME

# ---------------------------------------------------------------- set: posts, ropes, sling
POSTS = (1, 28)                              # left column of each 2-wide post
POST_TOP = 8


def _posts():
    f = Frame()
    for x0 in POSTS:
        f.put(x0, POST_TOP - 1, 't')         # rounded cap, lit from the top-left
        f.put(x0 + 1, POST_TOP - 1, 'T')
        f.vline(x0, POST_TOP, GROUND, 'T')
        f.vline(x0 + 1, POST_TOP, GROUND, 'd')
    return f


# The sling, per column: rim (top row of the fabric in front of him) and bottom row.  Three lengthwise
# stripes: a lime rim catching the light, green, dark green underneath; it tapers into the gathered ends.
# The middle (x 11-19) hangs one row above the input box, deep enough to hide his lower body, and its rim
# (row 16) leaves a row of his face under his lids (row 14).
BOT = {4: 12, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 17}
RIM = {4: 12, 5: 12, 6: 12, 7: 13, 8: 14, 9: 15, 10: 15}
for _x in range(11, 20):
    BOT[_x], RIM[_x] = 18, 16
for _x in range(4, 11):
    BOT[30 - _x], RIM[30 - _x] = BOT[_x], RIM[_x]
RIM_C, MID_C, BOT_C = 'a', 'g', 'G'


def _fabric(x, y):
    r, b = RIM[x], BOT[x]
    if b == r:
        return MID_C
    if y == r:
        return RIM_C
    return BOT_C if y == b else MID_C


def _rope_ends(dx):
    return ((3, POST_TOP), (4 + dx, 11)), ((27, POST_TOP), (26 + dx, 11))


# ---------------------------------------------------------------- the straw hat (local: no sun hat in the library)
# Straw lit from the top-left (tan, gold, dark-gold shade), a blue ribbon band; the brim (11 wide) sits on
# his head (row 11).  Anchor = the brim's centre cell.  'tip' = the gust lifts its left side; 'tip_r' = it
# rocks back the other way as it falls.
HAT = {
    'on':    Sprite(['...tjjJ....',
                     '...bbbB....',
                     'tjjjjjjjjjJ'], anchor=(5, 2), name='straw_hat'),
    'tip':   Sprite(['..tjjJ.....',
                     '..bbbB.....',
                     'tjjjjj.....',
                     '.....jjjjjJ'], anchor=(5, 3), name='straw_hat'),
    'tip_r': Sprite(['....tjjJ...',
                     '....bbbB...',
                     '.....tjjjjJ',
                     'tjjjjJ.....'], anchor=(5, 3), name='straw_hat'),
}
HAT_ON = (15, 11)                            # brim centre on his head at HOME

# (t, (pose, x, y) or 'on').  The hat leaves his head on the first gust, hangs, drifts right with the
# gust (and the hammock), then falls back on.  'on' = on his head, swaying with him.
HAT_KEYS = [
    (0, 'on'),
    (9060, ('tip', 15, 11)),                 # the gust catches the brim ..
    (9140, ('tip', 15, 10)),                 # .. lifts it off ..
    (9220, ('on', 15, 9)),                   # .. it hangs two rows up ..
    (9460, ('on', 16, 9)),                   # .. drifting right with the gust ..
    (9660, ('tip_r', 16, 10)),               # .. rocks and falls ..
    (9780, ('on', 16, 10)),
    (9860, 'on'),                            # .. back on his head (the hammock is at +1 now)
    (9940, ('on', 16, 10)),                  # one cell of bounce
    (10100, 'on'),
]

# ---------------------------------------------------------------- Clawd
_BODY = clawd(eyes='blink', larm='none', rarm='none', legs='none')   # solid face: his eyes live on the fine layer
# His arm stubs (the kit's 1x2 arms, his arm columns 0 and 10): 'down' hangs them over the rim (rest /
# breathing out), 'side' is the kit's resting arm (breathing in: they ride up a cell).
_ARMS = {
    'down': Pose.from_rows(['.' * 11] * 3 + ['#.........#'] * 2, name='clawd_arms'),
    'side': Pose.from_rows(['.' * 11] * 2 + ['#.........#'] * 2, name='clawd_arms'),
}


def _hammock(dx):
    """Ropes, Clawd (eyeless, no arms) and the sling in front of him; dx = sway."""
    f = Frame()
    for a, b in _rope_ends(dx):
        f.line(a[0], a[1], b[0], b[1], 't')
    put_clawd(f, _BODY, HX + dx, HY)
    for x in RIM:
        for y in range(RIM[x], BOT[x] + 1):
            f.put(x + dx, y, _fabric(x, y))
    return f


def _arms(state, dx):
    f = Frame()
    put_clawd(f, _ARMS[state], HX + dx, HY)
    return f


# His face: the kit's fine-line eyes on his eyeless body; the layer keeps only the eye ink.  'peek' = one
# eye cracks to a sleepy half lid and glances up at the brim (moved one fine pixel up).
FACES = {'asleep': ('line', 'line', 0), 'half': ('line', 'half', 0), 'peek': ('line', 'half', -1)}


def _face(name, dx):
    left, right, gaze = FACES[name]
    f = Frame()
    put_clawd(f, _BODY, HX + dx, HY)
    base = fine(f)
    ff = fine_face(base.copy(), _BODY, HX + dx, HY, expr=left, right=right)
    split = 2 * (HX + dx + 5)                # his centre column: the screen-right eye is to the right of it
    out = Frame(res=2)
    for (x, y), ch in ff.px.items():
        if base.px.get((x, y)) != ch:
            out.px[(x, y + (gaze if x >= split else 0))] = ch
    assert set(out.px.values()) <= {EYE_INK}
    assert all(base.px.get(k) == '#' for k in out.px), 'his eye ink must sit on his face'
    out.meta = {'fine_face': [(left, right, gaze)]}
    return out


# ---------------------------------------------------------------- the master clock
SWAY = [                                     # (t, dx)
    (0, 0),
    (9300, 1), (10200, 0), (10500, -1), (11300, 0), (11700, 1), (12250, 0),
]
BREATH = [                                   # (t, arms): breathing in lifts them a cell
    (0, 'down'),
    (1200, 'side'), (2600, 'down'),
    (6000, 'side'), (7350, 'down'),
    (11000, 'side'), (12300, 'down'),
    (15600, 'side'), (17000, 'down'),
    (20900, 'side'), (22300, 'down'),
]
FACE = [(0, 'asleep'), (10300, 'half'), (10450, 'peek'), (10900, 'half'), (11050, 'asleep')]

# Zs: library z_small / z_medium on one hand-placed path up and to the right, above the right rope.
Z_PATH = [                                   # (item, centre x, centre y, ms): it puffs out a row clear of
    ('z_small', 22, 8, 380),                 # the hat brim and stays above the right rope and post
    ('z_small', 23, 7, 420),
    ('z_small', 24, 6, 470),
    ('z_medium', 25, 4, 560),
    ('z_medium', 26, 3, 520),
    ('z_small', 27, 3, 400),
]
Z_BIRTHS = (2600, 17000, 22900)

# Wind: two short streaks rush in from the left above his head as the breeze arrives.
WIND = [                                     # (t, [(x, y, length), ...])
    (8900, [(-1, 5, 3)]),
    (8980, [(3, 5, 3), (-1, 8, 2)]),
    (9060, [(8, 5, 3), (3, 8, 2)]),
    (9140, [(13, 4, 3), (8, 8, 3)]),
    (9220, [(19, 4, 3), (13, 7, 2)]),
    (9300, [(24, 4, 3), (21, 7, 3)]),
    (9380, [(29, 4, 2), (26, 6, 2)]),
    (9460, []),
]
WIND_C = 'm'


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


def _hat_frame(state, dx):
    """The hat on his head (it sways with him) or in the air."""
    f = Frame()
    if state == 'on':
        f.place(HAT['on'], HAT_ON[0] + dx, HAT_ON[1])
    else:
        pose, x, y = state
        f.place(HAT[pose], x, y)
    return f


def _wind(streaks):
    f = Frame()
    for x, y, n in streaks or ():
        for i in range(n):
            if 0 <= x + i < W:
                f.put(x + i, y, WIND_C)
    return f


def build():
    keys = {0}
    for track in (SWAY, BREATH, FACE, HAT_KEYS, WIND):
        keys |= {t for t, _ in track}
    keys |= _z_keys()
    keys = sorted(keys)
    segs = [(t, (keys[i + 1] if i + 1 < len(keys) else LOOP) - t) for i, t in enumerate(keys)]
    for t, ms in segs:
        assert ms >= 40, 'a %d ms sliver at %d ms' % (ms, t)

    ham, arms, fc, hat, zz, wd = [], [], [], [], [], []
    for t, ms in segs:
        dx = _at(SWAY, t, 0)
        h = _at(HAT_KEYS, t, 'on')
        ham.append((_hammock(dx), ms))
        arms.append((_arms(_at(BREATH, t, 'down'), dx), ms))
        fc.append((_face(_at(FACE, t, 'asleep'), dx), ms))
        hat.append((_hat_frame(h, dx), ms))
        zz.append((_z_frame(t), ms))
        wd.append((_wind(_at(WIND, t, [])), ms))
    for lst in (ham, arms, fc, hat, zz, wd):
        assert total_ms(lst) == LOOP
    return anim(NAME, DESC, [
        static('posts', _posts()),
        layer('hammock', ham),
        layer('arms', arms),
        layer('face', fc),
        layer('hat', hat),
        layer('zzz', zz),
        layer('wind', wd),
    ], state=STATE)
