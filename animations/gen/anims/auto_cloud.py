"""auto-cloud - Auto mode (idle in that mode), variant: cloud surfing.

Storyboard (body loop 11.98 s; ms)
     0  CRUISE (frame 0): Clawd surfs a fluffy cloud 3 cells above the input box, arms out for balance,
        red scarf rising in the breeze, soft shadow on the input box; a gust drifts past on both sides
  2400  a breeze flicks the scarf tip up and he blinks
  3480  LIFT: the cloud swells up under him (he sinks into the fluff a beat, the scarf tip sags) ..
  3740  .. he rides high, eyeing the swoop ahead
  4690  SWOOP RIGHT, one gentle eased carve: he banks (outside arm up), the cloud tips down-right and
        slides out from under him, so he hangs in the air (lavender wisps trail off its flank) ..
  5190  .. still hanging as it levels out: he spots the gap below him ..
  5390  .. and drifts down onto it .. 5590 touches down, arms level .. 5770 sinks softly into the fluff
        (blink; two tiny specks puff out) .. 5960 rides the bottom of the swoop
  6360  glances back home .. 6620 the cloud carries him back up-left (pressed in) .. home
  7140  peeks down at his shadow
  9340  the breeze lulls (the scarf tip sags), he blinks .. and glances left
 10220  LEAN LEFT: he banks the other way, the cloud dips down-left (he floats a beat) and he settles
        into the dip, enjoying the view .. 11720 it swings back up (pressed in) -> home = frame 0
Calm by design: every motion step is 180-300 ms, eased by long holds on both sides; his arms only move
on the two banks; blinks fall 3.4 / 3.6 / 5.0 s apart.
Ambient, on loops co-prime with the body: the breeze (4.34 s: thin steel streaks drift in on the right
and out on the left at one cell per 140 ms, about three quarters of the time, then a one-second lull)
and a pair of distant birds gliding through the open sky up top (15.3 s). Static sky: two tiny far
clouds and a little sun peeking out from behind one.

Rider physics: he follows the cloud one key late (column `rel`), so he floats a beat when it drops
away and is pressed into the fluff when it rises; on the swoop he hangs for two keys (rel -2, 440 ms)
so the gap under his feet reads. The scarf follows his own motion (tip up while he falls, tip down when he is
pressed or rising, always via rest). _check_keys enforces the motion rules; _check_clear proves the
breeze and the birds never touch Clawd, his scarf, the cloud or the sky sprites, whatever key the body
is on.

HOME: x is HOME's (10); y is 7 rows up (box (10, 5)) because he rides a cloud floating 3 cells above
the input box ("on the cloud above HOME", per the brief), so lint's frame-0 HOME warning is expected.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'auto-cloud'
STATE = 'Auto mode (idle in that mode), variant: cloud surfing'
DESC = ('Surfs a fluffy cloud on autopilot, arms out and scarf in the breeze: rides a gentle swoop to the '
        'right (hanging in the air a beat), dips to the left, while a soft breeze and distant birds drift past.')

CLOUD_DY = 11           # cloud anchor (bottom-center) = box + (5, 11): his feet tuck into the top puffs


# ---------------------------------------------------------------- local sprites
def _far_cloud(mask):
    """Tiny distant cloud: pale-lilac body, lavender rim (only mid-tones touch the background)."""
    inside = {(x, y) for y, r in enumerate(mask) for x, ch in enumerate(r) if ch == 'X'}
    cells = {}
    for x, y in inside:
        cells[(x, y)] = 'L'
    for x, y in inside:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in inside:
                cells[(x + dx, y + dy)] = 'l'
    return Sprite(cells=[(x + 1, y + 1, c) for (x, y), c in cells.items()], anchor=(0, 0), name='far_cloud')


_FAR_A = _far_cloud(['.XX..', 'XXXXX'])
_FAR_B = _far_cloud(['XXX'])
# a little sun peeking out from behind the small far cloud: gold rim (reads on white), pale core glint
_SUN = Sprite(['.jjj.', 'jyyyj', 'jyYyj', 'jyyyj', '.jjj.'], anchor=(0, 0), name='sun')

# distant bird: wings up (v, also the glide) / wings down (^); gray reads on both themes
_BIRD = [
    Sprite(['N.N', '.N.'], anchor=(1, 1), name='bird'),
    Sprite(['.N.', 'N.N'], anchor=(1, 1), name='bird'),
]

# soft ground shadow by the cloud's bottom row (higher = smaller); one mid-tone reads on both themes
_SHADOW = {15: 'NNNNNNN', 16: 'NNNNNNNNN', 17: 'NNNNNNNNNNN'}


def _clip_place(f, spr, x, y):
    """Place a sprite that deliberately enters / leaves the canvas (cells outside are skipped)."""
    for sx, sy, ch in spr.cells:
        px, py = x + sx - spr.ax, y + sy - spr.ay
        if 0 <= px < W and 0 <= py < H:
            f.put(px, py, ch)


# ---------------------------------------------------------------- master timeline
# (ms, x, y, rel, larm, rarm, eyes, scarf, fx)
#   x, y  : the cloud's resting box for Clawd (cloud anchor = (x + 5, y + CLOUD_DY))
#   rel   : Clawd's vertical lag behind the cloud; he is drawn at (x, y + rel)
#           (-1 = floats a beat above the fluff, +1 = pressed into it)
#   scarf : library scarf frame (0 rest, 1 tip up, 2 tip down), driven by his own motion: tip up while
#           he falls, tip down when he is pressed or rises; always via rest (one row per step). While
#           he hangs at box y 4 it rests (he is not moving), which also keeps it clear of the far cloud
#           above (_check_clear)
#   fx    : 'w1' / 'w2' / 'w3' lavender wisps trailing the swooping cloud's flank, 'p' two tiny
#           landing specks
O, S, R = 'out', 'side', 'raise'          # R: arm lifted out-and-up (the outside arm of a bank)
KEYS = [
    # CRUISE
    (2400, 10, 5, 0, O, O, 'open', 0, None),        # frame 0: the reduced-motion still
    (130, 10, 5, 0, O, O, 'blink', 1, None),        # a breeze flicks the scarf, he blinks
    (950, 10, 5, 0, O, O, 'open', 0, None),
    # LIFT: the cloud swells up under him (he sinks into the fluff a beat, scarf tip droops)
    (260, 10, 4, 1, O, O, 'open', 2, None),
    (950, 10, 4, 0, O, O, 'look_r', 0, None),       # rides high, eyeing the swoop ahead
    # SWOOP RIGHT: one gentle eased carve down-right and back
    (260, 11, 5, -1, R, S, 'look_r', 0, 'w1'),      # banks; the cloud tips down-right, he floats a beat
    (240, 12, 6, -2, R, S, 'look_r', 0, 'w2'),      # .. it slides out from under him: he hangs in the air
    (200, 13, 6, -2, R, S, 'look_d', 0, 'w3'),      # .. still hanging as it levels out: he spots the gap
    (200, 13, 6, -1, R, S, 'look_d', 1, None),      # .. and drifts down onto it (scarf tip lifts)
    (180, 13, 6, 0, O, O, 'open', 0, None),         # touches down, arms level
    (190, 13, 6, 1, O, O, 'blink', 2, 'p'),         # sinks softly into the fluff: two specks puff out
    (400, 13, 6, 0, O, O, 'open', 0, None),         # the far point: rides the bottom of the swoop ..
    (260, 13, 6, 0, O, O, 'look_l', 0, None),       # .. glances back home
    (240, 12, 5, 1, O, O, 'look_l', 2, None),       # the cloud carries him back up-left (pressed in)
    (280, 11, 5, 0, O, O, 'open', 0, None),
    # CRUISE
    (900, 10, 5, 0, O, O, 'look_d', 0, None),       # home; peeks down at his shadow
    (1300, 10, 5, 0, O, O, 'open', 0, None),
    (130, 10, 5, 0, O, O, 'blink', 2, None),        # the breeze lulls (scarf tip sags), he blinks ..
    (750, 10, 5, 0, O, O, 'look_l', 0, None),       # .. and glances left (anticipation)
    # LEAN LEFT: a gentle dip out to the left; the swing back home is the loop seam
    (300, 9, 6, -1, S, R, 'look_l', 1, None),       # banks; the cloud dips down-left, he floats a beat
    (1200, 8, 6, 0, S, R, 'look_l', 0, None),       # .. settles into the dip, enjoying the view
    (260, 9, 5, 1, O, O, 'open', 2, None),          # it swings back up (pressed in) -> home = frame 0
]


def _check_keys():
    """No jitter: Clawd and the cloud never step in opposite vertical directions, nobody moves more than
    one cell per key, the scarf tip changes one row at a time (via rest), and the loop flows into
    frame 0."""
    for a, b in zip(KEYS, KEYS[1:] + KEYS[:1]):
        dc = b[2] - a[2]
        dp = (b[2] + b[3]) - (a[2] + a[3])
        if dc * dp < 0 or max(abs(dc), abs(dp), abs(b[1] - a[1])) > 1:
            raise ValueError('auto-cloud: jerky motion between %r and %r' % (a, b))
        if {a[7], b[7]} == {1, 2}:
            raise ValueError('auto-cloud: scarf skips its rest frame between %r and %r' % (a, b))
    k0 = KEYS[0]
    if (k0[1], k0[2], k0[3], k0[4], k0[5], k0[6], k0[7], k0[8]) != (10, 5, 0, O, O, 'open', 0, None):
        raise ValueError('auto-cloud: frame 0 must be the plain cruise pose')


def _cloud_cells(x, y):
    spr = get('cloud_platform').sprite(0)
    ax, ay = x + 5, y + CLOUD_DY
    return {(ax + sx - spr.ax, ay + sy - spr.ay) for sx, sy, ch in spr.cells}


def _clawd_frame(k):
    ms, x, y, rel, la, ra, eyes, sc, fx = k
    f = Frame()
    p = clawd(eyes=eyes, larm=la, rarm=ra)
    put_clawd(f, p, x, y + rel)
    wear(f, get('scarf'), p, x, y + rel, i=sc)
    # pixels the cloud (drawn on top with the same timing) always hides are left out: same picture,
    # smaller SVG
    for cell in _cloud_cells(x, y):
        f.px.pop(cell, None)
    if fx == 'p':
        # as he sinks into the fluff, two tiny specks puff out of the cloud's flanks for one beat (one
        # cell clear of the cloud, his scarf and his arms). They ride in this layer because it changes
        # on this key anyway: no extra frames
        f.put(x - 3, y + 7, 'l')
        f.put(x + 13, y + 7, 'l')
    return f


# swoop wisps: (row offset from the cloud's bottom row, length) trailing off its left flank with a
# one-cell gap; they grow in as it tips into the swoop and thin out as it levels off
WISPS = {'w1': ((-3, 2),), 'w2': ((-3, 3), (-1, 2)), 'w3': ((-1, 2),)}


def _cloud_frame(k):
    """The cloud, its ground shadow and (while it swoops) the lavender wisps trailing it: all of them
    move only with the cloud, so one layer carries them (they never overlap Clawd)."""
    ms, x, y, rel, la, ra, eyes, sc, fx = k
    f = Frame()
    cb = y + CLOUD_DY
    sh = _SHADOW[cb]
    f.place(Sprite([sh], anchor=(len(sh) // 2, 0)), x + 5, GROUND)
    for dy, ln in WISPS.get(fx, ()):
        f.hline(x - 3 - ln, x - 4, cb + dy, 'l')
    f.place(get('cloud_platform').sprite(0), x + 5, cb)
    return f


# ---------------------------------------------------------------- ambient: the breeze
# Thin steel streaks drift right to left (the way his scarf blows) at one cell per tick. Each one grows
# in, drifts and thins out inside a pocket of open sky that never touches anything the body layers
# ever draw (checked in _check_clear): right of his arm and the cloud's flank, where the breeze blows
# in from the edge, and under his scarf, past the cloud's trailing side, where it blows out of the
# picture. Staggered so one is usually drifting somewhere; the loop (4.34 s) is co-prime with the body
# (11.98 s) and the birds (15.3 s), so the sky never lines up the same way twice for minutes.
WIND_TICK = 140
WIND_TICKS = 31
# (start tick, row, head column at the start, streak length per tick)
STREAKS = [
    # a gust (frame 0 catches both mid-drift): one blows in right of his arm, one blows out past the
    # cloud's trailing flank
    (-3, 9, 31, (1, 2, 3, 3, 2, 1)),
    (-2, 15, 4, (1, 2, 3, 3, 3, 2)),
    # then single streaks, one after another: at the cloud's level, under the scarf tip, by his shoulder
    (4, 16, 31, (1, 2, 3, 3, 2)),
    (9, 13, 4, (1, 2, 2, 3, 3, 2)),
    (15, 11, 31, (1, 2, 3, 3, 2, 1)),
    # .. and a one-second lull before the next gust
]


def _wind_frames():
    frames = []
    for t in range(WIND_TICKS):
        f = Frame()
        for t0, row, hx, lens in STREAKS:
            a = (t - t0) % WIND_TICKS
            if a >= len(lens):
                continue
            head = hx - a
            for xx in range(head, head + lens[a]):
                if 0 <= xx < W:
                    f.put(xx, row, 's')
        frames.append((f, WIND_TICK))
    return frames


# ---------------------------------------------------------------- ambient: distant birds
BIRD_LOOP = 15300
BIRD_MS = 200                 # one cell per 200 ms: far away, unhurried
BIRD_LAG = 5                  # the second bird flies the same arc 5 steps behind: always two cells clear
                              # of the first, so their wings never merge into one dotted line
# wing rhythm: flap, then glide (wings held up) for a few steps; the pair flaps out of phase
BIRD_WINGS = (1, 0, 0, 0, 1, 0, 0)
# the arc (anchor = the bird's body cell): dips in from the top edge, glides left along rows 1-2
# through the open band between the far cloud and the sun, and rises out over the top. The band stays a
# cell clear of everything Clawd, his scarf and the cloud ever cover (checked in _check_clear)
BIRD_PATH = [(21, 0), (20, 1), (19, 1), (18, 2), (17, 2), (16, 2), (15, 2), (14, 2), (13, 1),
             (12, 1), (11, 0)]


def _bird_frames():
    """Frame 0 is empty sky: the pair is a passing event, not part of the reduced-motion still."""
    n = len(BIRD_PATH) + BIRD_LAG
    frames = [(Frame(), BIRD_LOOP - BIRD_MS * n)]
    nw = len(BIRD_WINGS)
    for k in range(n):
        f = Frame()
        for b, phase in ((k, 0), (k - BIRD_LAG, 3)):
            if 0 <= b < len(BIRD_PATH):
                _clip_place(f, _BIRD[BIRD_WINGS[(b + phase) % nw]], *BIRD_PATH[b])
        frames.append((f, BIRD_MS))
    return frames


def _touches(f, cover):
    return next(((x, y) for (x, y) in f.px for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                 if (x + dx, y + dy) in cover), None)


def _check_clear(sky, body, moving):
    """Nothing collides, not even diagonally: Clawd, his scarf, the cloud, its shadow and the wisps stay
    clear of the sky sprites at every key; the breeze and the birds stay clear of all of it at every
    moment of their own loops (whatever key the body is on)."""
    for name, frames in body:
        for i, (f, ms) in enumerate(frames):
            hit = _touches(f, sky.px)
            if hit:
                raise ValueError('auto-cloud: %s key %d touches the sky at %r' % (name, i, hit))
    cover = set(sky.px)
    for name, frames in body:
        for f, ms in frames:
            cover.update(f.px)
    for name, frames in moving:
        for i, (f, ms) in enumerate(frames):
            hit = _touches(f, cover)
            if hit:
                raise ValueError('auto-cloud: %s frame %d touches the scene at %r' % (name, i, hit))


def build():
    _check_keys()
    sky = Frame()
    sky.place(_FAR_A, 1, 1)
    sky.place(_SUN, 26, 1)
    sky.place(_FAR_B, 24, 3)

    clawd_l = [(_clawd_frame(k), k[0]) for k in KEYS]
    cloud_l = [(_cloud_frame(k), k[0]) for k in KEYS]
    birds, wind = _bird_frames(), _wind_frames()
    _check_clear(sky, [('clawd', clawd_l), ('cloud', cloud_l)], [('birds', birds), ('wind', wind)])

    return anim(NAME, DESC, [
        static('sky', sky),
        layer('birds', birds),
        layer('wind', wind),
        layer('clawd', clawd_l),
        layer('cloud', cloud_l),
    ], state=STATE)
