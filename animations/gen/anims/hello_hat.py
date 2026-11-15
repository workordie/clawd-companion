"""hello-hat - hello variant: a gentleman's greeting with a bowler hat (one-shot, 3.7 s).

The panel opens and Clawd is wearing a little brown bowler that has just twinkled into place. He
lifts it to you by the brim with sparkling eyes, holds it there a beat, looks at you warmly, sets
it back on, blinks, then flicks it off his head: it pops up and vanishes in a twinkle. He ends in
the plain standing pose at HOME, eyes open, exactly idle's frame 0, and holds it.
Plain black eyes with the fine-line kit (STYLE.md 0b: open, half, line, sparkle, look_u); no
mouth, no blush, normal body size in every frame (he never dips or crouches).

STORYBOARD (ms; one 3740 ms timeline, played once)
     0  HELLO (frame 0 = the reduced-motion still): at HOME in the bowler, right hand on the brim,
        eyes open, a big twinkle beside the hat (it has just appeared) ... 300 the twinkle thins
   400  he LIFTS it: the hat rises a row and leans a cell toward his hand (brim on his hand), eyes
        SPARKLE ("hello!"), the twinkle fades (plus, dot) ... he holds the hat up, sparkling at you
        (670 ms in all)
  1170  the sparkle softens (half) into open eyes on you, hat still raised ... 1460 he sets it back
        on his head
  1580  hand off the brim (up, side) ... 2020 a blink (half, line, half) ... 2340 he glances up at
        his hat (fine look_u)
  2590  he reaches up (up) ... 2680 FLICK: the brim is pushed up and the hat pops off (2 rows,
        then 4) ... 2860 it vanishes in a twinkle (big star > long plus > plus > dot) while his eyes
        follow it, and his hand comes down
  3060  eyes back on you ... 3240 the plain standing pose (= idle's frame 0), held 500 ms to the end
Layers (back to front): body (normal res, no eye cells) | face (FINE overlay: only his half-size
eye pixels) | hat | fx (twinkles). All share one timeline, so the hat never leaves his hand.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'hello-hat'
STATE = 'hello (variant)'
DESC = ('Greets you in a little bowler hat: lifts it by the brim with sparkling eyes, sets it back '
        'on, then flicks it off into a twinkle and stands ready.')

_SPK = get('sparkle')

# ------------------------------------------------------------------ the bowler (local prop)
# Brown bowler (derby): a round 3-5-7 dome lit from the top-left (tan highlight, wood base, dark-wood
# shade on the right), a graphite band (charcoal would vanish on the dark theme once the hat is in
# the air, splitting it in two), an 11-wide brim whose bottom row sits on his top row (box x
# 0-10, like the library top hat, so his raised 'raise' hand at (21, 12) touches its right end).
# Anchor = his head-top-center (box (5, 0)).
_BOWLER = Sprite([
    '....tTT....',
    '...tTTTd...',
    '..tTTTTTd..',
    '..nnnnnnn..',
    'TTTTTTTTTTd',
], anchor=(5, 4), name='bowler')
# hat offsets (dx, dy) from its seat on his head
SEAT, LIFT = (0, 0), (1, -1)        # lifted: up a row and a cell toward his hand (brim end on it)
FLICK1, FLICK2 = (1, -2), (1, -4)   # flicked off: it pops up, then twinkles away
TWINKLE_IN = (7, 8)                 # the twinkle it appeared in (left of the hat, clear of it)
TWINKLE_OUT = (16, 5)               # where it vanishes (the middle of the hat at FLICK2)

# ------------------------------------------------------------------ the timeline
# (name, ms, right arm, left arm, hat offset or None, face, fx (sparkle frame, at) or None)
KEYS = [
    ('hi',     300, 'raise', 'side', SEAT, 'open', (2, TWINKLE_IN)),
    ('hi2',    100, 'raise', 'side', SEAT, 'open', (3, TWINKLE_IN)),
    ('lift',   100, 'raise', 'side', LIFT, 'sparkle', (1, TWINKLE_IN)),
    ('tip',    250, 'raise', 'side', LIFT, 'sparkle', (0, TWINKLE_IN)),
    ('tip2',   420, 'raise', 'side', LIFT, 'sparkle', None),     # a held beat: "hello!"
    ('soft',    90, 'raise', 'side', LIFT, 'half', None),        # the sparkle softens ...
    ('gaze',   200, 'raise', 'side', LIFT, 'open', None),        # ... into open eyes on you
    ('on',     120, 'raise', 'side', SEAT, 'open', None),
    ('let',     90, 'up', 'side', SEAT, 'open', None),
    ('rest',   350, 'side', 'side', SEAT, 'open', None),
    ('bl1',     60, 'side', 'side', SEAT, 'half', None),
    ('bl2',     90, 'side', 'side', SEAT, 'line', None),
    ('bl3',     60, 'side', 'side', SEAT, 'half', None),
    ('rest2',  110, 'side', 'side', SEAT, 'open', None),
    ('look',   250, 'side', 'side', SEAT, 'look_u', None),
    ('reach',   90, 'up', 'side', SEAT, 'look_u', None),
    ('flick',   90, 'raise', 'side', FLICK1, 'look_u', None),
    ('fly',     90, 'raise', 'side', FLICK2, 'look_u', None),
    ('pop',    100, 'raise', 'side', None, 'look_u', (2, TWINKLE_OUT)),
    ('pop2',   100, 'up', 'side', None, 'look_u', (3, TWINKLE_OUT)),
    ('pop3',    90, 'side', 'side', None, 'open', (1, TWINKLE_OUT)),
    ('pop4',    90, 'side', 'side', None, 'open', (0, TWINKLE_OUT)),
    ('end',    500, 'side', 'side', None, 'open', None),    # = idle's frame 0
]
LOOP = sum(k[1] for k in KEYS)


def _pose(rarm, larm):
    return clawd(eyes='blink', rarm=rarm, larm=larm)


def _body(rarm, larm):
    """Clawd with NO eye cells (kit 'blink'): the face layer draws every eye pixel."""
    f = Frame()
    put_clawd(f, _pose(rarm, larm))
    return f


def _face(expr):
    """FINE overlay holding only his half-size eye pixels (fine_face on a fine copy of the body,
    minus the body itself): body + overlay composite exactly to fine(frame) + fine_face(...)."""
    p = _pose('side', 'side')
    f = Frame()
    put_clawd(f, p)
    base = fine(f)
    ff = fine_face(base.copy(), p, HOME[0], HOME[1], expr)
    out = Frame(res=2)
    out.px = {q: c for q, c in ff.px.items() if base.px.get(q) != c}
    out.meta = {'fine_face': [(expr, expr)]}
    return out


def _hat(rarm, larm, off):
    f = Frame()
    if off is not None:
        hx, hy = _pose(rarm, larm).at('head')
        f.place(_BOWLER, hx + off[0], hy + off[1])
        f.meta['items'] = ['bowler']
    return f


def _fx(spk):
    f = Frame()
    if spk is not None:
        f.place(_SPK.sprite(spk[0]), *spk[1])
    return f


def build():
    body, face, hat, fx = [], [], [], []
    for _, ms, rarm, larm, off, expr, spk in KEYS:
        body.append((_body(rarm, larm), ms))
        face.append((_face(expr), ms))
        hat.append((_hat(rarm, larm, off), ms))
        fx.append((_fx(spk), ms))
    return anim(NAME, DESC, [
        layer('body', body),
        layer('face', face),
        layer('hat', hat),
        layer('fx', fx),
    ], state=STATE)
