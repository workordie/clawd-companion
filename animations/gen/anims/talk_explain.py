"""talk-explain - The answer just arrived in his speech bubble: Clawd presents it (one-shot).
Preview:  python3 gen/preview.py anim talk-explain

Plays once when Claude's answer lands in the bubble (after talk-think), then the patch goes back to talk-listen.
The little Claude ✻ that pulsed over his head in talk-think shoots up into the bubble, he points after it, does a
small "ta-da", nods, and looks at you.  He sits at the right end of the input box, so the bubble most likely opens
above him and a bit to his LEFT: BUBBLE = -1 sets that side (+1 mirrors the point and the spark's flight).

STORYBOARD (ms)   one-shot = 3 030 ms; every layer is exactly that long
     0  frame 0 = the reduced-motion still: Clawd at HOME pointing up toward the bubble with his left claw, eyes
        on it (a half-step up and over), while the ✻ (full bloom) streaks up into it, a fading trail behind
   220  it is almost there (small, at the top edge) .. 310 gone into the bubble: a glint where it went in
   800  he lets the point go: both claws dip (anticipation) and his eyes come to you ..
   890  .. TA-DA: both claws out, his whole body pops up half a cell, sparkle eyes, a glint twinkles off each claw
  1050  lands back on the box and holds the ta-da
  1470  a nod: up half a cell, then down with the eyes dipping and the claws low ("there you go")
  1780  he looks at you, claws at his sides .. 2280 a smooth blink
  2530  the plain standing pose, official open eyes (the kit's default pose, exactly) .. 3030 end
Eye closures: 2.28 s (plus the nod's dip).

Face: fine-line eyes only (half-size black pixels, STYLE.md 0b): open / half / line / sparkle, moved by a half-step
gaze.  No mouth, no blush, never resized: the pops move his whole normal body half a cell (fine pixels).
Layers: body (normal pixels: Clawd drawn solid, no eye holes; the last beat is the kit's default pose with its own
eyes) | lift (FINE: the same body half a cell up) | face (FINE: only his black eye pixels) | fx (the spark, its
trail and the glints).  One beat list drives all four, so they never desync.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'talk-explain'
STATE = 'talk (answer arrived, one-shot)'
DESC = ('Presents the answer that just landed in his speech bubble: the little ✻ shoots up into it as he points '
        'after it, then a small ta-da with both claws out and sparkle eyes, a nod, and a look at you.')

BUBBLE = -1          # -1: the bubble opens above him and to his left (he sits at the right end of the box); +1 right

HX, HY = HOME
_G = GEOM['normal']
_EYES = ((HX + _G['ex'][0], HY + _G['ey']), (HX + _G['ex'][1], HY + _G['ey']))   # his eye cells at HOME

# half-step gaze (fine pixels).  's' = up toward the bubble's side.
_GAZE = {'c': (0, 0), 'u': (0, -1), 'd': (0, 1), 's': (BUBBLE, -1)}
_ALLOWED = ('open', 'half', 'line', 'wide', 'sparkle')      # the user's fine-line shapes (no arcs or cups)


def _side(arm):
    """(left, right) arms with `arm` on the bubble's side and the other at rest."""
    return (arm, 'side') if BUBBLE < 0 else ('side', arm)


_ARMS = {                                     # name: (left arm, right arm), kit shapes
    'side': ('side', 'side'),
    'point': _side('wave'),                   # pointing up after the spark, toward the bubble
    'down': ('down', 'down'),                 # anticipation / the nod's weight
    'out': ('out', 'out'),                    # ta-da
}


def _solid(arms):
    """Clawd at HOME with a solid face (eyes='blink': no eye cells; the face layer draws his eyes)."""
    la, ra = _ARMS[arms]
    p = clawd(eyes='blink', larm=la, rarm=ra)
    f = Frame()
    put_clawd(f, p)
    return f


def _eye_px(expr, lift):
    """Both eyes as fine pixels {(x, y): ch}: the kit's FINE_EYES shape moved by a half-step gaze, on a body
    lifted `lift` fine pixels.  The right eye mirrors the left (the sparkle's glint stays top-left)."""
    shape, _, gaze = expr.partition('/')
    if shape not in _ALLOWED:
        raise ValueError('eye shape %r is not one the user allows' % shape)
    gx, gy = _GAZE[gaze or 'c']
    out = {}
    for side, (ex, ey) in enumerate(_EYES):
        fx0, fy0 = 2 * ex, 2 * ey - lift
        mirror = side == 1 and shape != 'sparkle'
        for dx, dy, ch in FINE_EYES[shape]:
            x = fx0 + (1 - dx if mirror else dx) + gx
            out[(x, fy0 + dy + gy)] = EYE_INK if ch in '_e' else ch
    return out


def _frames(expr, arms, lift):
    """(body, lifted, face) frames for one beat.  lift: 0 on the box, 1 = half a cell up (fine).
    expr 'plain' = the kit's default standing pose, exactly (put_clawd(f, clawd())), with its own eyes."""
    if expr == 'plain':
        f = Frame()
        put_clawd(f, clawd())
        return f, Frame(res=2), Frame(res=2)
    solid = _solid(arms)
    fine_body = fine(solid)
    body, lifted = solid, Frame(res=2)
    if lift:
        body, lifted = Frame(), fine_body.shifted(0, -lift)
    under = lifted if lift else fine_body
    face = Frame(res=2)
    for (x, y), ch in _eye_px(expr, lift).items():
        if under.px.get((x, y)) != '#':
            raise ValueError('%s: eye pixel %r is off his face' % (expr, (x, y)))
        face.px[(x, y)] = ch
    face.meta = {'fine_face': [expr]}
    return body, lifted, face


# ---------------------------------------------------------------- effects
# The spark is talk-think's ✻ (same sprites): it leaves from just above his head toward the bubble.
_SPARK = {
    'star':  Sprite(['#.#.#',
                     '.#o#.',
                     '#oyo#',
                     '.#o#.',
                     '#.#.#'], anchor=(2, 2), name='spark_star'),
    'plus':  Sprite(['..#..',
                     '..o..',
                     '#oyo#',
                     '..o..',
                     '..#..'], anchor=(2, 2), name='spark_plus'),
}
_GLINT = [Sprite(['j'], anchor=(0, 0), name='glint_dot'),                      # the library's sparkle_small,
          Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1), name='glint_plus'),     # drawn locally: dot > plus > x
          Sprite(['j.j', '.j.', 'j.j'], anchor=(1, 1), name='glint_x')]
_S = BUBBLE                                   # x direction of the flight


def _fx(state):
    f = Frame()
    if state == 'fly0':          # the ✻ streaks up toward the bubble, its trail fading behind it
        f.place(_SPARK['star'], HX + 5 + 3 * _S, 4)
        f.put(HX + 5 + 1 * _S, 7, 'o')
        f.put(HX + 5, 8, 'O')
    elif state == 'fly1':        # almost in: the thinner ✢ at the top edge
        f.place(_SPARK['plus'], HX + 5 + 5 * _S, 2)
        f.put(HX + 5 + 3 * _S, 4, 'o')
        f.put(HX + 5 + 2 * _S, 5, 'O')
    elif state and state.startswith('in'):       # gone into the bubble: a glint where it went in
        k = int(state[2:])
        f.place(_GLINT[k], HX + 5 + 6 * _S, 1)
    elif state and state.startswith('tada'):     # a glint up and out from each claw (the 'out' tips: 9 and 21, row 14)
        k = int(state[4:])
        for x in (HX - 4, HX + 14):
            f.place(_GLINT[k], x, HY - 1)
    return f


# ---------------------------------------------------------------- the beats: (ms, eyes, arms, lift, fx)
_BEATS = [
    (220, 'open/s', 'point', 0, 'fly0'),     # frame 0: pointing up after the ✻ as it streaks into the bubble
    (90, 'open/s', 'point', 0, 'fly1'),
    (100, 'open/s', 'point', 0, 'in1'),      # it went in: a glint
    (110, 'open/s', 'point', 0, 'in2'),
    (90, 'open/s', 'point', 0, 'in0'),
    (190, 'open/s', 'point', 0, None),       # "there!"
    (90, 'open', 'down', 0, None),           # anticipation: the claws dip, the eyes come to you ..
    (160, 'sparkle', 'out', 1, 'tada1'),     # .. TA-DA: claws out, a half-cell pop, a glint off each claw
    (140, 'sparkle', 'out', 0, 'tada2'),
    (120, 'sparkle', 'out', 0, 'tada1'),
    (160, 'sparkle', 'out', 0, 'tada0'),
    (110, 'open', 'side', 1, None),          # a nod: up ..
    (200, 'open/d', 'down', 0, None),        # .. and down, claws low ("there you go")
    (500, 'open', 'side', 0, None),          # he looks at you
    (70, 'half', 'side', 0, None),           # a smooth blink
    (110, 'line', 'side', 0, None),
    (70, 'half', 'side', 0, None),
    (500, 'plain', 'side', 0, None),         # the plain standing pose (the kit default, eyes open) -> talk-listen
]
LENGTH = sum(b[0] for b in _BEATS)


def build():
    body, lifted, face, fx = [], [], [], []
    for ms, eyes, arms, lift, ef in _BEATS:
        b, l, f = _frames(eyes, arms, lift)
        body.append((b, ms))
        lifted.append((l, ms))
        face.append((f, ms))
        fx.append((_fx(ef), ms))
    return anim(NAME, DESC, [layer('body', body), layer('lift', lifted), layer('face', face), layer('fx', fx)],
                state=STATE)
