"""talk-think - Your question is sent and Claude is answering in his bubble (it shows a pulsing orange ✻ and
"Answering..."). Clawd works it out with a little ✻ of his own.   Preview:  python3 gen/preview.py anim talk-think

The spark is Claude's asterisk, the glyph in the bubble, drawn small (5x5) in Claude orange with a hot core. It
breathes like the CLI spinner: the full ✳, a +, a small ✢, then its diagonal tips shoot out again (a twinkle), and
it floats just above his head.  No chalkboard, cube, gears, cloud, bulb, stars or pacing, no claw on his chin:
just Clawd, the spark, a tapping foot and his claws.  Two little cause-and-effect beats per loop: his flick spins
it up, his pumping claw lifts it back up.

STORYBOARD (ms)   one loop = 6 080 ms; busy-calm.  The spark breathes every 710 ms (✳ 260, + 130, ✢ 190, twinkle 130)
     0  frame 0 = the reduced-motion still: Clawd at HOME, eyes a half-step up (fine look_u) on the full ✳
        floating two rows above his head, arms at his sides
   260  he taps his right foot on the "+" of each breath while he watches it (260, 970, 1680); 710 it drifts
        down a cell
  1880  smooth blink at his raised gaze
  2130  he reaches up under it, elbow first (2220 claw raised beneath it), and it rises to meet his claw ..
  2480  .. he FLICKS it (the claw whips out and back): it spins up, a step every 70 ms, rising another cell;
        2620 the light is in his eyes (sparkle) .. 2970 it blooms white-hot and throws off four specks that
        drift out, cooling to rust (3100)
  3240  it settles back into its breath as his claw comes down (3240 up, 3330 side)
  3950  a glance at you, tapping his foot (4210): "almost there..." .. 4530 back up at it
  4660  it drifts down again .. 4820 "come on, up!": his left claw pumps it up twice (raised 4920, 5140) ..
  5240  .. and it floats back up
  5630  tap .. 5800 a quick blink -> frame 0
Eye closures: 1.88, 5.80 s (gaps 3.9 / 2.2 s).

Face: fine-line eyes only (half-size black pixels, STYLE.md 0b): open / half / line / sparkle, moved by a half-step
gaze ('open/u' == the kit's fine look_u).  No mouth, no blush, never resized; the toe tap is the kit body with
its outer right foot one cell shorter (the foot lifts off the box, as in idle).
Layers: body (normal pixels: Clawd drawn solid, no eye holes) | face (FINE: only his black eye pixels) | spark.
All cut from one clock: every body beat lands on a spark step or >= 40 ms from one (build() asserts it).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'talk-think'
STATE = 'talk (answering)'
DESC = ('Works out the answer under a little orange Claude ✻ that breathes above his head: he taps his foot as he '
        'watches it, flicks it into a bright spin, sparkle-eyed, glances at you ("almost there"), and pumps it back up '
        'with his other claw when it drifts down.')

HX, HY = HOME
_G = GEOM['normal']
_EYES = ((HX + _G['ex'][0], HY + _G['ey']), (HX + _G['ex'][1], HY + _G['ey']))   # his eye cells at HOME
_FOOT_R = (_G['legs'][3], _G['ly'] + _G['ll'] - 1)                               # outer right foot (box cell)

_GAZE = {'c': (0, 0), 'u': (0, -1), 'd': (0, 1), 'ul': (-1, -1), 'ur': (1, -1)}
_ALLOWED = ('open', 'half', 'line', 'wide', 'sparkle')      # the user's fine-line shapes (no arcs or cups)

_ARMS = {                                     # name: (left arm, right arm), kit shapes
    'side': ('side', 'side'),
    'r_up': ('side', 'up'),                   # the reach: elbow up ..
    'r_raise': ('side', 'raise'),             # .. claw raised under the spark
    'r_wave': ('side', 'wave'),               # the flick
    'l_up': ('up', 'side'),                   # "come on, up!": the left claw pumps ..
    'l_raise': ('raise', 'side'),
}


def _solid(arms, tap=False):
    """Clawd at HOME with a solid face (eyes='blink': no eye cells; the face layer draws his eyes)."""
    la, ra = _ARMS[arms]
    p = clawd(eyes='blink', larm=la, rarm=ra)
    if tap:          # toe tap: the outer right leg one cell shorter, the foot lifts off the input box
        cells = [c for c in p.sprite.cells if (c[0], c[1]) != _FOOT_R]
        p = Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec, tap=True))
    f = Frame()
    put_clawd(f, p)
    return f


def _eye_px(expr):
    """Both eyes as fine pixels {(x, y): ch}: the kit's FINE_EYES shape moved by a half-step gaze.
    The right eye mirrors the left (the sparkle's glint stays top-left)."""
    shape, _, gaze = expr.partition('/')
    if shape not in _ALLOWED:
        raise ValueError('eye shape %r is not one the user allows' % shape)
    gx, gy = _GAZE[gaze or 'c']
    out = {}
    for side, (ex, ey) in enumerate(_EYES):
        fx0, fy0 = 2 * ex, 2 * ey
        mirror = side == 1 and shape != 'sparkle'
        for dx, dy, ch in FINE_EYES[shape]:
            x = fx0 + (1 - dx if mirror else dx) + gx
            out[(x, fy0 + dy + gy)] = EYE_INK if ch in '_e' else ch
    return out


def _clawd(expr, arms, tap):
    """(body, face) frames for one beat."""
    body = _solid(arms, tap)
    under = fine(body)
    face = Frame(res=2)
    for (x, y), ch in _eye_px(expr).items():
        if under.px.get((x, y)) != '#':
            raise ValueError('%s: eye pixel %r is off his face' % (expr, (x, y)))
        face.px[(x, y)] = ch
    face.meta = {'fine_face': [expr]}
    return body, face


# ---------------------------------------------------------------- the spark: Claude's ✻, 5x5, anchor = center
# '#' Claude orange rays, 'o' orange, 'y' hot core, 'Y' white-hot (the bloom).  Every edge pixel is a mid-tone,
# so it reads on both themes; the pale core is always enclosed.
_SPARK = {
    'small': Sprite(['.o.',
                     'oyo',
                     '.o.'], anchor=(1, 1), name='spark_small'),       # ✢ small, between pulses
    'x':     Sprite(['#...#',
                     '..o..',
                     '.oyo.',
                     '..o..',
                     '#...#'], anchor=(2, 2), name='spark_x'),         # blooming: the diagonal tips shoot out
    'star':  Sprite(['#.#.#',
                     '.#o#.',
                     '#oyo#',
                     '.#o#.',
                     '#.#.#'], anchor=(2, 2), name='spark_star'),      # ✳ full bloom (the still)
    'plus':  Sprite(['..#..',
                     '..o..',
                     '#oyo#',
                     '..o..',
                     '..#..'], anchor=(2, 2), name='spark_plus'),      # shrinking back
    'bloom': Sprite(['#.....#',
                     '.o.o.o.',
                     '..oyo..',
                     '.oyYyo.',
                     '..oyo..',
                     '.o.o.o.',
                     '#.....#'], anchor=(3, 3), name='spark_bloom'),   # spun up: white-hot, specks fly off ..
    'bloom2': Sprite(['O.......O',
                      '.........',
                      '..#.#.#..',
                      '...#o#...',
                      '..#oyo#..',
                      '...#o#...',
                      '..#.#.#..',
                      '.........',
                      'O.......O'], anchor=(4, 4), name='spark_bloom2'),   # .. drift out, cooling to rust
}
SX = HX + 5                                   # above the middle of his head (col 15)
_BREATH = [('star', 260), ('plus', 130), ('small', 190), ('x', 130)]   # one breath = 710 ms, from full bloom
_SPIN = ['x', 'star', 'plus', 'star', 'x', 'star', 'plus']             # the flick: 70 ms a step


def _spark_steps():
    """[(frame name, ms)] for one loop, and the step index of each named beat."""
    steps, tags = [], {}

    def breath(n=1):
        for _ in range(n):
            steps.extend(_BREATH)

    breath(3)                                   # watching, tapping along
    tags['reach'] = len(steps)
    steps += [('star', 260), ('plus', 90)]      # he reaches up under it ..
    tags['flick'] = len(steps)
    steps += [(k, 70) for k in _SPIN]           # .. flicks it: it spins up ..
    tags['bloom'] = len(steps)
    steps += [('bloom', 130), ('bloom2', 140)]  # .. and blooms bright, throwing off specks
    tags['settle'] = len(steps)
    breath(1)                                   # back to its breath
    tags['glance'] = len(steps)
    breath(3)
    return steps, tags


_STEPS, _TAG = _spark_steps()
_START = [sum(ms for _, ms in _STEPS[:i]) for i in range(len(_STEPS) + 1)]
LOOP = _START[-1]


def T(step, dt=0):
    """Start time (ms) of spark step `step` (negative counts from the end), plus dt."""
    return _START[step % len(_STEPS)] + dt


# the float: centre row 7 (a 2-row gap over his head); it drifts down a cell, comes back up to meet his claw,
# rises one more on the flick and settles, then drifts down and back again before the loop
_FLOAT = [(0, 7), (T(4), 8), (T(_TAG['reach']), 7), (T(_TAG['flick']), 6), (T(_TAG['settle']), 7),
          (T(_TAG['glance'] + 4), 8), (T(_TAG['glance'] + 7), 7)]


def _spark_track():
    out = []
    for i, (name, ms) in enumerate(_STEPS):
        y = [yy for t0, yy in _FLOAT if t0 <= _START[i]][-1]
        out.append((name, y, ms))
    return out


_TRACK = _spark_track()


def _spark_frame(name, y):
    f = Frame()
    f.place(_SPARK[name], SX, y)
    return f


# ---------------------------------------------------------------- Clawd: (t ms, eyes, arms, tap)
# Every key lands on a spark step or >= 40 ms away from one (build() checks it): the beats share one clock.
U = 'open/u'
R, F, G = _TAG['reach'], _TAG['flick'], _TAG['glance']
_KEYS = [
    (0,          U, 'side', False),         # frame 0: watching the spark
    (T(1),       U, 'side', True),          # tap on the "+" of each breath ..
    (T(2),       U, 'side', False),
    (T(5),       U, 'side', True),          # .. tap ..
    (T(6),       U, 'side', False),
    (T(9),       U, 'side', True),          # .. tap
    (T(10),      U, 'side', False),
    (T(11, -120), 'half/u', 'side', False),  # smooth blink, the lids close over his raised eyes
    (T(11, -60), 'line/u', 'side', False),
    (T(11, 60),  'half/u', 'side', False),
    (T(R),       U, 'r_up', False),         # he reaches up under it, the elbow first ..
    (T(R, 90),   U, 'r_raise', False),      # .. claw raised beneath it
    (T(F),       U, 'r_wave', False),       # the flick ..
    (T(F + 1),   U, 'r_raise', False),
    (T(F + 2),   'sparkle/u', 'r_raise', False),   # .. it spins up: the light is in his eyes
    (T(_TAG['settle']), 'sparkle/u', 'r_up', False),   # it settles; the claw comes down
    (T(_TAG['settle'], 90), U, 'side', False),
    (T(G),       'open', 'side', False),    # a glance at you: "almost there..."
    (T(G + 1),   'open', 'side', True),     # .. tapping his foot
    (T(G + 2),   'open', 'side', False),
    (T(G + 3),   U, 'side', False),         # back up at it: it is drifting down (G + 4) ..
    (T(G + 4, 160), U, 'l_up', False),      # .. "come on, up!": his other claw pumps it up ..
    (T(G + 5),   U, 'l_raise', False),
    (T(G + 6),   U, 'l_up', False),
    (T(G + 6, 90), U, 'l_raise', False),    # .. twice ..
    (T(G + 7),   U, 'side', False),         # .. and it floats back up
    (T(G + 9),   U, 'side', True),          # tap
    (T(G + 10),  U, 'side', False),
    (T(-2, 40),  'half/u', 'side', False),  # a quick blink
    (T(-2, 100), 'line/u', 'side', False),
    (T(-1),      'half/u', 'side', False),
    (T(-1, 60),  U, 'side', False),
]


def _segments(keys):
    out = []
    for i, k in enumerate(keys):
        t2 = keys[i + 1][0] if i + 1 < len(keys) else LOOP
        assert t2 > k[0], (k, t2)
        out.append((k[1:], t2 - k[0]))
    return out


def build():
    body, face = [], []
    for (eyes, arms, tap), ms in _segments(_KEYS):
        b, f = _clawd(eyes, arms, tap)
        body.append((b, ms))
        face.append((f, ms))
    spark = [(_spark_frame(n, y), ms) for n, y, ms in _TRACK]
    assert total_ms(body) == total_ms(spark) == LOOP
    cuts = sorted(set(_START[:-1]) | {k[0] for k in _KEYS})
    slivers = [(a, b) for a, b in zip(cuts, cuts[1:] + [LOOP]) if b - a < 40]
    assert not slivers, 'beats closer than 40 ms: %r' % slivers
    return anim(NAME, DESC, [layer('body', body), layer('face', face), layer('spark', spark)], state=STATE)
