"""done-bell - done variant: "order up!" Clawd rings a little service bell.

A chrome desk bell stands on the input box at his right. Once per loop he gives it a light tap and
then a proper DING: gold ring-waves roll out of the bell, a sparkle blooms, his eyes sparkle. The
rest of the loop is a calm, satisfied wait (he may be on screen for a long time): uneven blinks, a
glance at his bell when it gleams, his hand never far from it.
Plain black eyes with the fine-line kit (STYLE.md 0b: open, half, line, sparkle) and one full kit
glance (look_dr) at the bell; no mouth, no blush, normal body size in every frame.

STORYBOARD (ms; one 7330 ms loop; every layer runs on the same clock)
     0  DING! (frame 0 = the reduced-motion still): his right hand on the bell's plunger (pressed),
        the free arm up a cell ("ding!"), SPARKLE eyes; the first ring hugs the bell top, a big
        sparkle above-right of it
   130  the ring rolls out (2nd ring), the plunger springs back up, the star thins to a long plus
   260  the 3rd ring breaks up at the edge of the scene, the star shrinks (plus, dot at 390) ... 520
        gone; the free arm comes down
   520  his eyes open: he looks at you, hand still resting on the bell (it is done)
   860  he lifts his hand off the bell (out, side) ... a long calm hold
  2280  blink (half, line, half)
  3420  a glance down at his bell (kit look_dr): its chrome gleams (a glint on the dome, 3480-3880)
  4120  back to you ... 4760 blink ... a long hold
  6130  anticipation: his eyes go to the bell and his hand rises (up 6230, wave 6330: raised over
        the plunger; his eyes follow it, look_r) ... 6430 his eyes come back to you: "ready?"
  6800  a light tap: the plunger dips, a small ring, a half-lid flinch ... 6900 the hand goes back up
  7230  the real one: the hand comes down on the plunger, eyes squeezed shut (line) ...
  7330  = frame 0: DING!
Eye closures: 2.28, 4.76, 6.80 (half), 7.23 s; gaps 2.5, 2.0, 0.4, 2.4 s.
Layers (back to front): bell (2 frames: plunger up / pressed) | body (normal res, no eye cells: it
only changes when his arms do) | face (FINE overlay: only his half-size eye pixels) | fx (rings,
sparkle, the dome's gleam). All four share LOOP, so the hand, the plunger and the ring never drift.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'done-bell'
STATE = 'done (variant)'
DESC = ('Rings a little service bell beside him, a light tap and then a proper "ding!" with rolling '
        'ring-waves and a sparkle, then waits contentedly with a hand near his bell, blinking and '
        'glancing at it when it gleams.')

LOOP = 7330
_SPK = get('sparkle')
_SPS = get('sparkle_small')

# ------------------------------------------------------------------ the bell (local prop)
# Chrome desk bell: graphite plunger knob on a gray stem, a rounded steel dome lit from the top-left
# (a chrome highlight inside a silver top-left contour, so the dome holds its shape on the light
# theme too; gray shade on the right), a graphite base plate. Anchor = bottom-center. At (23, 19)
# it spans x 20-26, rows 14-19: the plunger knob (23, 14) is level with his 'point' hand (22, 14),
# so the hand comes down right onto it (pressed, the knob sinks to (23, 15)).
BELL_AT = (23, GROUND)
_BELL = Sprite([
    '...n...',
    '...N...',
    '.mmmss.',
    'mSSsssN',
    'mssssNN',
    'nnnnnnn',
], anchor=(3, 5), name='service_bell')
_BELL_DOWN = Sprite([          # plunger pressed: the knob sinks onto the dome, the stem hides
    '...n...',
    '.mmmss.',
    'mSSsssN',
    'mssssNN',
    'nnnnnnn',
], anchor=(3, 4), name='service_bell_pressed')

# ------------------------------------------------------------------ ring-waves (local fx)
# Pixel quarter-circles around the bell (center (23, 16)), from above the plunger round to its right
# side: radius 4, 6, then a broken radius-8 ring that fades out (dark gold) at the edge of the
# scene. Clawd's arm is on the left of the bell, so the rings only roll up and to the right.
_RINGS = {
    1: [(23, 12), (24, 12), (25, 13), (26, 14), (27, 15), (27, 16)],
    2: [(23, 10), (24, 10), (25, 10), (26, 11), (27, 12), (28, 13), (29, 14), (29, 15), (29, 16)],
    3: [(24, 8), (25, 8), (28, 10), (29, 11), (30, 13), (30, 14)],
}
_RING_CH = {1: 'j', 2: 'j', 3: 'J'}
STAR_AT = (28, 5)              # the sparkle blooms above-right of the bell, clear of every ring
GLEAM_AT = (25, 16)            # a glint on the dome's lit shoulder while he admires it


def _segments(track):
    """[(t, value), ...] (t ascending, first t = 0) -> [(value, ms), ...] ending at LOOP."""
    out = []
    for i, (t, v) in enumerate(track):
        t2 = track[i + 1][0] if i + 1 < len(track) else LOOP
        assert t2 > t, (t, t2)
        out.append((v, t2 - t))
    return out


# ------------------------------------------------------------------ Clawd: arms (body) and face
# (t, right arm, left arm)
_ARMS = [
    (0, 'point', 'up'),         # DING: hand on the plunger, the free arm up a cell
    (520, 'point', 'side'),
    (860, 'out', 'side'),       # the hand lifts off the bell ...
    (960, 'side', 'side'),      # ... and rests: the long calm
    (6230, 'up', 'side'),       # anticipation: the hand rises ...
    (6330, 'wave', 'side'),     # ... and hovers over the plunger
    (6800, 'point', 'side'),    # a light tap
    (6900, 'wave', 'side'),
    (7230, 'point', 'side'),    # the real one -> DING (frame 0)
]
# (t, expression): a FINE_EYES name (fine-line kit) or a kit glance name
_FACE = [
    (0, 'sparkle'),             # DING!
    (520, 'open'),              # (with the free arm coming down)
    (2280, 'half'), (2340, 'line'), (2430, 'half'), (2490, 'open'),
    (3420, 'look_dr'),          # a glance down at his bell as it gleams
    (4120, 'open'),
    (4760, 'half'), (4820, 'line'), (4910, 'half'), (4970, 'open'),
    (6130, 'look_dr'),          # eyes to the bell ...
    (6230, 'look_r'),           # ... following the hand as it rises (kit look_dr would put his right
                                # eye on the body's edge once the arm leaves his side)
    (6430, 'open'),             # ... and back to you: "ready?"
    (6800, 'half'),             # the light tap: a little flinch
    (6900, 'open'),
    (7230, 'line'),             # the real one: eyes squeezed shut
]
_PRESS = [(0, True), (130, False), (6800, True), (6900, False), (7230, True)]
# (t, [(kind, arg), ...]): kind 'ring' (1-3), 'star' (sparkle frame), 'gleam' (sparkle_small frame)
_FX = [
    (0, [('ring', 1), ('star', 2)]),
    (130, [('ring', 2), ('star', 3)]),
    (260, [('ring', 3), ('star', 1)]),
    (390, [('star', 0)]),
    (520, []),
    (3480, [('gleam', 0)]),
    (3570, [('gleam', 1)]),
    (3690, [('gleam', 2)]),
    (3790, [('gleam', 0)]),
    (3880, []),
    (6800, [('ring', 1)]),      # the light tap: one small ring
    (6900, []),
]


def _body(rarm, larm):
    """Clawd with NO eye cells (kit 'blink'): the face layer draws every eye pixel, so the body
    frames merge while only his face acts."""
    f = Frame()
    put_clawd(f, clawd(eyes='blink', rarm=rarm, larm=larm))
    return f


_FACES = {}


def _face(expr):
    """FINE overlay holding only his half-size eye pixels for `expr`: a FINE_EYES name drawn with
    fine_face(), or a kit glance (its eye cells at half size). Body + overlay composite exactly to
    fine(frame) + fine_face(...)."""
    if expr not in _FACES:
        p = clawd(eyes='blink')
        f = Frame()
        put_clawd(f, p)
        base = fine(f)
        if expr in FINE_EYES:
            ff = fine_face(base.copy(), p, HOME[0], HOME[1], expr)
        else:
            g = Frame()
            put_clawd(g, clawd(eyes=expr))
            ff = fine(g)
        out = Frame(res=2)
        out.px = {q: c for q, c in ff.px.items() if base.px.get(q) != c}
        out.meta = {'fine_face': [(expr, expr)]}
        _FACES[expr] = out
    return _FACES[expr].copy()


def _bell(pressed):
    f = Frame()
    f.place(_BELL_DOWN if pressed else _BELL, *BELL_AT)
    return f


def _fx(items):
    f = Frame()
    for kind, arg in items:
        if kind == 'ring':
            for x, y in _RINGS[arg]:
                f.put(x, y, _RING_CH[arg])
        elif kind == 'star':
            f.place(_SPK.sprite(arg), *STAR_AT)
        elif kind == 'gleam':
            f.place(_SPS.sprite(arg), *GLEAM_AT)
    return f


def build():
    body = [(_body(*v), ms) for v, ms in _segments([(t, (r, l)) for t, r, l in _ARMS])]
    face = [(_face(v), ms) for v, ms in _segments(_FACE)]
    bell = [(_bell(v), ms) for v, ms in _segments(_PRESS)]
    fx = [(_fx(v), ms) for v, ms in _segments(_FX)]
    for lst in (body, face, bell, fx):
        assert total_ms(lst) == LOOP
    return anim(NAME, DESC, [
        layer('bell', bell),
        layer('body', body),
        layer('face', face),
        layer('fx', fx),
    ], state=STATE)
