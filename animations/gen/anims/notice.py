"""notice - your mouse cursor has just moved onto him.  Preview:  python3 gen/preview.py anim notice

One-shot (1.34 s), in place at HOME. It plays often, so it is short and light: a small startle, a
look up at you, a little "oh, hi" hand, and back to the plain standing pose.

STORYBOARD (ms)
     0  plain at HOME, eyes on you (frame 0 = the reduced-motion still)
    80  startle: his eyes go wide, both arms jump up a cell; three short steel surprise ticks pop
        out over his head
   140  hup!: a 1-cell hop with his whole normal body (push-off on long legs, then airborne with
        his legs tucked); the ticks fly a cell further out
   300  lands: arms follow through out, then back to his sides; the ticks fade to specks and go
   430  he looks up, at the cursor (look_u) ...
   550  "oh, hi": his right hand comes up (up > raise) and stays up a moment while he looks at you
   870  hand down, eyes back on you (930), a smooth blink (1020), plain standing pose (ends at 1340)
Fine-line faces (half-size pixels): open, wide, look_u, half, line.  One fine body layer, plus a
normal-resolution layer for the ticks with the same length.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims._drag import him, safe            # noqa: E402

NAME = 'notice'
STATE = 'play (cursor moved onto him)'
DESC = 'Cursor moves onto him: a little startled hop, then he looks up at you and lifts a hand, "oh, hi". One-shot.'

X0, Y0 = HOME
TICK = 's'                                   # steel: a neutral mid-tone that reads on both themes


def pose(face='open', dy=0, right=None, **kw):
    """Clawd (kw -> _drag.him: larm, rarm, legs) at HOME + dy rows, with a fine-line face."""
    f = Frame()
    p = him(f, X0, Y0 + dy, **kw)
    ff = fine(f)
    fine_face(ff, p, X0, Y0 + dy, face, right=right)
    return ff


# surprise ticks over his head: (dx, dy) cells relative to his head-top-center pixel
TICKS = [
    [(-3, -3), (-2, -2), (0, -4), (0, -3), (3, -3), (2, -2)],          # pop: short strokes near his head
    [(-4, -4), (-3, -3), (0, -5), (0, -4), (4, -4), (3, -3)],          # fly out a cell
    [(-5, -5), (0, -6), (5, -5)],                                      # specks
]


def ticks(k, head_y):
    f = Frame()
    hx = X0 + 5
    for dx, dy in TICKS[k]:
        safe(f, hx + dx, head_y + dy, TICK)
    return f


def build():
    up, out = dict(larm='up', rarm='up'), dict(larm='out', rarm='out')
    body = [
        (pose(), 80),                                         # plain (the still)
        (pose('wide', **up), 60),                             # startle
        (pose('wide', dy=-1, legs='long', **up), 60),         # push-off: feet still down
        (pose('wide', dy=-1, legs='short', **up), 100),       # airborne, legs tucked
        (pose('open', **out), 60),                            # lands: arms follow through
        (pose('open'), 70),
        (pose('look_u'), 120),                                # ...what was that? (looks up at you)
        (pose('look_u', rarm='up'), 60),
        (pose('look_u', rarm='raise'), 260),                  # "oh, hi"
        (pose('look_u', rarm='up'), 60),
        (pose('open'), 90),
        (pose('half'), 60),                                   # blink
        (pose('line'), 80),
        (pose('half'), 60),
        (pose('open'), 120),                                  # plain standing pose
    ]
    total = total_ms(body)
    fx = [(Frame(), 80),                                      # nothing yet
          (ticks(0, Y0), 60),                                 # pop (with the startle)
          (ticks(1, Y0 - 1), 160),                            # fly out (during the hop)
          (ticks(2, Y0), 60),                                 # specks (landing)
          (Frame(), total - 360)]
    return anim(NAME, DESC, [layer('body', body), layer('ticks', fx)], state=STATE)
