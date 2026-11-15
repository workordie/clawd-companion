"""talk-listen - You clicked Clawd to talk to him: his speech bubble is open and he listens while you type.
Preview:  python3 gen/preview.py anim talk-listen

The bubble is a real HTML box above him (the /btw side question, restyled), so nothing here draws a bubble:
he just listens, looking up at it. He sits at the right end of the input box, so the bubble most likely opens
above him and a bit to his LEFT: BUBBLE = -1 sets that side (+1 mirrors every side-dependent glance).

STORYBOARD (ms)   one loop = 11 770 ms; calm and attentive, long holds between small beats
     0  frame 0 = the reduced-motion still: Clawd at HOME, eyes a half-step up at the bubble (fine look_u),
        arms at his sides: attentive.  HOLD 1.9 s
  1900  smooth blink at his raised gaze (half > line > half: the lids close over the raised pupils)
  3050  READING ALONG as you type: his eyes go to the start of your line (up and toward the bubble's side),
        3610 slide along it to the end above him, 4110 a return sweep to the next line, 4490 and along again
  5090  "mm-hm" double nod: his whole body lifts half a cell, 5200 drops back with the eyes dipping and the
        claws swinging low (the weight of the nod); again 5400 / 5500, the second one held longer
  6420  "go on...": a blink carries his eyes down to you; 6860 the right claw rolls twice (out, up, in, down:
        the "keep going" roll) and 7600 stays held out, palm up .. 7900 rests;  8100 back up at the bubble
  9000  "oh?": something in your question catches his interest: eyes wide, he perks up half a cell, shoulders
        up .. 9240 settles;  9350 "ooh": sparkle eyes, a little glint twinkles up toward the bubble
 10100  a quicker blink .. HOLD 1.46 s -> frame 0 (3.36 s of calm across the seam)
Eye closures: 1.90, 6.42 (carries the glance to you), 10.10 s: gaps 4.5 / 3.7 / 3.6 s.

Face: fine-line eyes only (half-size black pixels, STYLE.md 0b): open / half / line / wide / sparkle, moved by a
half-step gaze (c u d, and s = up toward the bubble's side: one fine pixel; 'open/u' == the kit's fine look_u).
No mouth, no blush, never resized: his normal body throughout; the nods and the perk lift the whole body half a
cell (fine pixels), the feet leave the box.
Layers: body (normal pixels: Clawd drawn solid, no eye holes; empty while he is lifted) | lift (FINE: the same
solid body half a cell up) | face (FINE: only his black eye pixels) | fx (the glint).  All four are cut from one
beat list, so they never desync; body + lift + face composite to Clawd drawn whole with fine_face().
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'talk-listen'
STATE = 'talk (listening)'
DESC = ('Listens while you type your question in his speech bubble: eyes up on it, he reads along as the words '
        'appear, nods "mm-hm", rolls a claw "go on", and perks up sparkle-eyed at a good bit, with slow uneven blinks.')

BUBBLE = -1          # -1: the bubble opens above him and to his left (he sits at the right end of the box); +1 right

HX, HY = HOME
_G = GEOM['normal']
_EYES = ((HX + _G['ex'][0], HY + _G['ey']), (HX + _G['ex'][1], HY + _G['ey']))   # his eye cells at HOME
_FOOT = (HX + _G['legs'][3], HY + _G['ly'] + _G['ll'] - 1)                       # outer right foot (unused here)

# half-step gaze (fine pixels).  's' = up toward the bubble's side, 'o' = up toward the other side.
_GAZE = {'c': (0, 0), 'u': (0, -1), 'd': (0, 1), 's': (BUBBLE, -1), 'o': (-BUBBLE, -1)}
_ALLOWED = ('open', 'half', 'line', 'wide', 'sparkle')      # the user's fine-line shapes (no arcs or cups)

_ARMS = {                                     # name: (left arm, right arm), kit shapes
    'side': ('side', 'side'),
    'down': ('down', 'down'),                 # the nod's weight: both arms swing low
    'r_out': ('side', 'out'),                 # the "go on" roll: out ..
    'r_raise': ('side', 'raise'),             # .. up ..
    'r_up': ('side', 'up'),                   # .. in ..
    'up': ('up', 'up'),                       # "oh?": the shoulders come up as he perks up
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
    """(body, lifted, face) frames for one beat.  lift: 0 on the box, 1 = half a cell up (fine)."""
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


# ---------------------------------------------------------------- the glint ("ooh, good question")
# The library's sparkle_small (dot > plus > x), drawn locally so this file never depends on the library's state.
_GLINT = [Sprite(['j'], anchor=(0, 0), name='glint_dot'),
          Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1), name='glint_plus'),
          Sprite(['j.j', '.j.', 'j.j'], anchor=(1, 1), name='glint_x')]
_GLINT_AT = (HX + 5 + BUBBLE * 7, HY - 2)        # (8, 10): up and out from his head, toward the bubble


def _glint(k):
    f = Frame()
    if k is not None:
        f.place(_GLINT[k], *_GLINT_AT)
    return f


# ---------------------------------------------------------------- the beats: (ms, eyes, arms, lift, glint)
U = 'open/u'
_BEATS = [
    (1900, U, 'side', 0, None),           # frame 0: attentive, eyes up at the bubble
    (70, 'half/u', 'side', 0, None),      # smooth blink at the raised gaze
    (110, 'line/u', 'side', 0, None),
    (70, 'half/u', 'side', 0, None),
    (900, U, 'side', 0, None),
    # reading along as you type: start of the line (toward the bubble's side), along it, return sweep, along
    (560, 'open/s', 'side', 0, None),
    (500, U, 'side', 0, None),
    (380, 'open/s', 'side', 0, None),
    (600, U, 'side', 0, None),
    # "mm-hm" double nod: up half a cell, then down with the eyes dipping and the arms low
    (110, U, 'side', 1, None),
    (200, 'open', 'down', 0, None),
    (100, U, 'side', 1, None),
    (280, 'open', 'down', 0, None),
    (640, U, 'side', 0, None),
    # "go on...": a blink carries his eyes down to you, then the right claw rolls twice and ends held out
    (70, 'half/u', 'side', 0, None),
    (100, 'line', 'side', 0, None),
    (70, 'half', 'side', 0, None),
    (200, 'open', 'side', 0, None),
    (100, 'open', 'r_out', 0, None),
    (90, 'open', 'r_raise', 0, None),
    (90, 'open', 'r_up', 0, None),
    (90, 'open', 'side', 0, None),
    (100, 'open', 'r_out', 0, None),
    (90, 'open', 'r_raise', 0, None),
    (90, 'open', 'r_up', 0, None),
    (90, 'open', 'side', 0, None),
    (300, 'open', 'r_out', 0, None),      # "... go on"
    (200, 'open', 'side', 0, None),
    (900, U, 'side', 0, None),            # back up at the bubble
    # "oh?": something in your question catches his interest: eyes wide, he perks up half a cell, shoulders up
    (240, 'wide/u', 'up', 1, None),
    (110, 'wide/u', 'side', 0, None),
    (120, 'sparkle/u', 'side', 0, 0),     # "ooh": it shines in his eyes; a glint twinkles toward the bubble
    (110, 'sparkle/u', 'side', 0, 1),
    (110, 'sparkle/u', 'side', 0, 2),
    (110, 'sparkle/u', 'side', 0, 1),
    (100, 'sparkle/u', 'side', 0, 0),
    (200, 'sparkle/u', 'side', 0, None),
    (60, 'half/u', 'side', 0, None),      # a quicker blink
    (90, 'line/u', 'side', 0, None),
    (60, 'half/u', 'side', 0, None),
    (1460, U, 'side', 0, None),           # HOLD -> frame 0
]
LOOP = sum(b[0] for b in _BEATS)


def build():
    body, lifted, face, fx = [], [], [], []
    for ms, eyes, arms, lift, glint in _BEATS:
        b, l, f = _frames(eyes, arms, lift)
        body.append((b, ms))
        lifted.append((l, ms))
        face.append((f, ms))
        fx.append((_glint(glint), ms))
    return anim(NAME, DESC, [layer('body', body), layer('lift', lifted), layer('face', face), layer('fx', fx)],
                state=STATE)
