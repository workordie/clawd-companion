"""question-scroll - Question variant: he holds up a scroll with a big "?".   Preview:  python3 gen/preview.py anim question-scroll

Clawd at HOME holds a paper scroll up beside him by its top rod (gold knobs, wooden rods), unrolled down to
the input box, a big blue "?" on it: Claude asked you something.  The inkwell and red quill he wrote it with
stand at his left.  He waits politely and inquisitively: glances at the "?", at you, down at the input box
where your answer goes, opens his free hand toward the quill ("well? your turn"), and once a loop rolls the
scroll up and flicks it open again with a little bounce to catch your eye.  His face acts with the fine-line
kit (STYLE.md 0b: open, half / line blinks, half-step glances, wide, sparkle); no mouth, no blush, never
resized: only his free arm stub and the props move.

STORYBOARD (ms)   one loop = 10 400 ms; body, scroll, face and glints share it
      0  frame 0 (the reduced-motion still): the scroll open beside him, "?" showing, the inkwell at his left,
         his eyes on you.
    900  a glint twinkles off the top of the "?" .. 1500 he glances at the scroll (look_r) .. 2150 back to you
   2700  blink (half > line > half > open)
   3250  "well?": his free (left) hand opens out toward the quill and his eyes go wide; 4300 the hand goes back
         down, the eyes soften (open)
   4750  a glance down at the input box, where your answer will go (look_d) .. 5450 back to you
   6000  he rolls the scroll up: it snaps up to the top rod like a blind (three quick steps, 110 ms); rolled,
         he looks at you (wide), squints a little (6500) .. 6560 flicks it open: the roll drops, faster and faster (60 / 60 / 50 ms),
         hits the bottom (6730), bounces up a cell and settles (6860): the "?" again, sparkly eyes (6730 - 7600)
         and a sparkle off the scroll's top corner
   7600  eyes open; 8050 a glance at the "?" .. 8550 back to you; 9050 a quick double blink; then a calm hold
         into the seam.
Eye closures: 2.77, 6.50 (a half-lid squint into the flick), 9.12 + 9.29 s (a double blink): uneven.  The
hand comes out once and the scroll rolls once, so no beat repeats within the loop.
Layers: inkwell (static) | body (Clawd with a solid face: his arms) | scroll | face (FINE: only his eye
ink) | glints.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'question-scroll'
STATE = 'question (variant)'
DESC = ('Holds up a paper scroll with a big blue "?" beside the inkwell he wrote it with: he glances at it, at '
        'you and at the input box where your answer goes, opens a polite "well?" hand toward the quill, then '
        'rolls the scroll up and flicks it open again with a bounce and a sparkle.')

LOOP = 10400
HX, HY = HOME

# ---------------------------------------------------------------- the scroll
# Held by its top rod: his right arm in the kit's 'wave' shape, the claw tip (22, 12) just under the rod's
# left knob.  Rods 9 wide (gold knobs 'j' at x 22 and 30, wood between), paper 7 wide (x 23-29): paper white
# with a white glint at the top-left, a silver edge on the left and a tan one on the right, so it keeps its
# shape on the light theme.  Open, the bottom rod hangs on row 19, on the input box.
SX0, SX1 = 22, 30                            # knob columns
TOP = 11                                     # top rod row
OPEN = GROUND                                # bottom rod row when it is open
ROLLED = TOP + 2                             # rolled up: top rod, the paper wound tight, bottom rod
# Bold "?" (cyan lit edge, blue, navy shade), 5 wide in the paper's 5 white columns, its dot two rows above
# the bottom rod.
GLYPH = [
    '.cbb.',
    'cb.bB',
    '...bB',
    '..bB.',
    '.....',
    '..bB.',
]
GX, GY = SX0 + 2, TOP + 1                    # glyph top-left: the first white column, the first paper row


def _scroll(bottom):
    """The scroll with its bottom rod on row `bottom` (ROLLED .. OPEN).  The paper hangs from the top rod,
    so a partly open scroll shows the top of the "?"; rolled up tight, the paper is one plain roll."""
    f = Frame()

    def rod(y):
        f.put(SX0, y, 'j')
        f.hline(SX0 + 1, SX1 - 1, y, 'T')
        f.put(SX1, y, 'j')

    rod(TOP)
    for y in range(TOP + 1, bottom):
        f.put(SX0 + 1, y, 'm')                           # left edge (silver)
        f.hline(SX0 + 2, SX1 - 2, y, 'w')
        f.put(SX1 - 1, y, 't')                           # right edge, in shade (tan)
        if y == TOP + 1:
            f.put(SX0 + 2, y, 'W')                       # a white glint at the top-left
        gy = y - GY
        if bottom > ROLLED and 0 <= gy < len(GLYPH):
            for gx, ch in enumerate(GLYPH[gy]):
                if ch != '.':
                    f.put(GX + gx, y, ch)
    rod(bottom)
    return f


# The inkwell he wrote it with, on the input box at his left: a navy glass bottle (lit blue edge) full of ink
# with a silver lip, a red quill standing in it.  Static; his "well?" hand opens toward it: your turn.
INKWELL = Sprite([
    '.....r',
    '....rR',
    '...rR.',
    '..rR..',
    '.mmsm.',
    'bBkkBB',
    'bkkkkB',
    '.BBBB.',
], anchor=(3, 7), name='inkwell')
INKWELL_AT = (5, GROUND)


# ---------------------------------------------------------------- Clawd: body (solid face) + fine face
def _pose(larm):
    return clawd(eyes='blink', larm=larm, rarm='wave')


def _body(larm):
    f = Frame()
    put_clawd(f, _pose(larm))
    return f


# Fine-line expressions: the kit's FINE_EYES (open, half / line blinks, the half-step look_r / look_d glances,
# wide, sparkle).  The (dx, dy) slot can move an expression's ink by whole fine pixels (none needed here).
FACES = {
    'open': ('open', (0, 0)), 'half': ('half', (0, 0)), 'line': ('line', (0, 0)),
    'look_r': ('look_r', (0, 0)), 'look_d': ('look_d', (0, 0)), 'wide': ('wide', (0, 0)),
    'sparkle': ('sparkle', (0, 0)),
}


def _face(name, larm):
    expr, (gx, gy) = FACES[name]
    p = _pose(larm)
    f = Frame()
    put_clawd(f, p)
    base = fine(f)
    ff = fine_face(base.copy(), p, expr=expr)
    out = Frame(res=2)
    for (x, y), ch in ff.px.items():
        if base.px.get((x, y)) != ch:
            out.px[(x + gx, y + gy)] = ch
    assert all(base.px.get(k) == '#' for k in out.px), 'his eye ink must sit on his face (%s)' % name
    out.meta = {'fine_face': [(expr, (gx, gy))]}
    return out


# ---------------------------------------------------------------- the clock
ROLL = 6000                                  # the scroll rolls up ..
FLICK = 6560                                 # .. and is flicked open
ARMS = [(0, 'side'), (3250, 'out'), (4300, 'side')]          # (t, left arm)
SCROLL = [                                   # (t, bottom rod row)
    (0, OPEN),
    (ROLL, 17), (ROLL + 50, 15), (ROLL + 110, ROLLED),                     # snaps up like a blind
    (FLICK, 14), (FLICK + 60, 15), (FLICK + 120, 17),                      # drops, faster and faster ..
    (FLICK + 170, OPEN), (FLICK + 230, OPEN - 1), (FLICK + 300, OPEN),     # .. bounces and settles
]
FACE = [
    (0, 'open'),
    (1500, 'look_r'), (2150, 'open'),                          # the "?" .. you
    (2700, 'half'), (2770, 'line'), (2890, 'half'), (2960, 'open'),   # blink
    (3250, 'wide'), (4300, 'open'),                            # "well?"
    (4750, 'look_d'), (5450, 'open'),                          # the input box, where your answer goes
    (ROLL + 110, 'wide'),                                      # rolled up: looks at you ..
    (FLICK - 60, 'half'),                                      # .. squints into the flick ..
    (FLICK + 170, 'sparkle'),                                  # .. ta-da
    (7600, 'open'),
    (8050, 'look_r'), (8550, 'open'),
    (9050, 'half'), (9120, 'line'), (9220, 'half'), (9290, 'line'), (9370, 'half'), (9440, 'open'),
]
# Glints (library sparkle_small: plus > cross > dot) above the scroll: one in the opening hold, one off its
# top-right corner as it lands open.
SPARK = get('sparkle_small')
GLINTS = [(900, (25, 9)), (FLICK + 300, (29, 9))]


def _glint_track():
    keys = [(0, None)]
    for t, at in GLINTS:
        keys += [(t, (1, at)), (t + 100, (2, at)), (t + 220, (0, at)), (t + 330, None)]
    return keys


def _glint(state):
    f = Frame()
    if state:
        i, (x, y) = state
        f.place(SPARK.sprite(i), x, y)
    return f


def _at(keys, t):
    v = None
    for k in keys:
        if k[0] <= t:
            v = k[1:] if len(k) > 2 else k[1]
    return v


def build():
    glints = _glint_track()
    keys = {0}
    for track in (ARMS, SCROLL, FACE, glints):
        keys |= {k[0] for k in track}
    keys = sorted(keys)
    segs = [(t, (keys[i + 1] if i + 1 < len(keys) else LOOP) - t) for i, t in enumerate(keys)]
    for t, ms in segs:
        assert ms >= 40, 'a %d ms sliver at %d ms' % (ms, t)
    body, scroll, face, gl = [], [], [], []
    for t, ms in segs:
        larm = _at(ARMS, t)
        body.append((_body(larm), ms))
        scroll.append((_scroll(_at(SCROLL, t)), ms))
        face.append((_face(_at(FACE, t), larm), ms))
        gl.append((_glint(_at(glints, t)), ms))
    for lst in (body, scroll, face, gl):
        assert total_ms(lst) == LOOP
    ink = Frame()
    ink.place(INKWELL, *INKWELL_AT)
    return anim(NAME, DESC, [
        static('inkwell', ink),
        layer('body', body),
        layer('scroll', scroll),
        layer('face', face),
        layer('glints', gl),
    ], state=STATE)
