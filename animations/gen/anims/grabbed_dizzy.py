"""grabbed-dizzy - you're shaking him while you hold him up.  Preview:  python3 gen/preview.py anim grabbed-dizzy

Loop (1.76 s). Held EXACTLY the way `grabbed` holds him (anims/_drag.py): box lifted a cell to (10, 11),
head-top (the grip, under your cursor) at (15, 11), legs dangling 3 cells long. Frame 0 has him right
there, so the patch can swap grabbed <-> grabbed-dizzy without a jump. While shaken, his floppy body
wobbles a cell either side of the grip and back; everything loose on him lags behind.

STORYBOARD (ms; 16 steps of 90-140 ms, the stars step once per frame: 4 full orbits per loop)
     0  frame 0 (the reduced-motion still): under the grip, three little stars circling over his head,
        legs trailing, arms flopped out, eyes rolled off to one side
        Each swing: his body slides a cell (the stars follow his head a step late); while he moves,
        his legs trail behind (the leading leg of each pair further than the other: they scissor) and
        the arm on the trailing side is flung out while the other hangs; when he stops at the end of
        the swing, legs and arms swing through past him the other way.
        Eyes: they lag the motion (look_l / look_r), squeeze shut for a beat now and then (line), and
        twice they go their own ways: one up, one down (dazed)
   330  ... swings left ... 770 right again ... 1010 a quick small one left ... 1300 right, left (1540)
Fine-line faces (half-size pixels): look_l, look_r, look_u, look_d, line, half.  One fine layer (the
stars stay locked to his head).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402
from anims._drag import him                  # noqa: E402

NAME = 'grabbed-dizzy'
STATE = 'shaken while held (drag)'
DESC = 'Shaken while held up: his floppy body wobbles under your grip, legs and arms flop behind, eyes roll, stars circle his head. Loop.'

X0, Y0 = HOME
BOX = (X0, Y0 - 1)                           # where `grabbed` holds him (head-top = the grip at (15, 11))
LEGX = (1, 3, 7, 9)
# a leg swung s cells' worth: x offset of each of its 3 cells from the top down (0 = dangling straight).
# The leg on the leading side of each pair always swings further than the other, or the gap between
# them closes up (pose() checks: the kit would fill a closed gap with eye ink).
SWING = {0: [0, 0, 0], 1: [0, 0, 1], 2: [0, 1, 1], 3: [0, 1, 2],
         -1: [0, 0, -1], -2: [0, -1, -1], -3: [0, -1, -2]}


def gaps(f):
    """Transparent cells enclosed by his body (between the legs): the kit would ink them like eyes."""
    out, stack = set(), [(x, y) for x in range(W) for y in (0, H - 1)] + [(x, y) for y in range(H) for x in (0, W - 1)]
    while stack:
        x, y = stack.pop()
        if (x, y) in out or (x, y) in f.px or not (0 <= x < W and 0 <= y < H):
            continue
        out.add((x, y))
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(x, y) for x in range(W) for y in range(H) if (x, y) not in f.px and (x, y) not in out]


def pose(dx, swing_a, swing_b, larm, rarm, face, right=None, stars=None):
    """Clawd in the grabbed spot shifted dx cells; legs 1+7 (pair A) and 3+9 (pair B) swung; stars =
    (frame, x offset) of the dizzy stars circling his head, or None."""
    f = Frame()
    x, y = BOX[0] + dx, BOX[1]
    p = him(f, x, y, legs='none', larm=larm, rarm=rarm)
    for c, s in zip(LEGX, (swing_a, swing_b, swing_a, swing_b)):
        for i, d in enumerate(SWING[s]):
            f.put(x + c + d, y + 6 + i, '#')
    holes = gaps(f)
    if holes:
        raise ValueError('closed gap between his legs at %s (dx %d, swings %d/%d)' % (holes, dx, swing_a, swing_b))
    ff = fine(f)
    fine_face(ff, p, x, y, face, right=right)
    if stars is not None:
        g = Frame()
        i, sx = stars
        g.place(get('dizzy_stars').sprite(i), BOX[0] + 5 + sx, BOX[1] - 2)   # orbit centre: 2 rows over his head
        ff.px.update(fine(g).px)
    return ff


# (ms, body dx, leg swing pair A, pair B, left arm, right arm, face, right eye if different)
STEPS = [
    (120, 0, -2, -1, 'out', 'down', 'look_l', None),        # still: sliding back to centre, legs trailing
    (100, 1, -3, -1, 'out', 'down', 'look_l', None),        # pulled right: legs + left arm trail
    (110, 1, 1, 2, 'down', 'out', 'look_r', None),          # stops: everything swings through
    (110, 0, 0, 2, 'down', 'out', 'line', None),            # back: squeeze
    (90, -1, 1, 3, 'down', 'out', 'look_r', None),          # pulled left
    (140, -1, -2, -1, 'out', 'up', 'look_u', 'look_d'),     # stops: eyes go their own ways
    (100, 0, -2, 0, 'out', 'down', 'look_l', None),
    (110, 1, -3, -1, 'out', 'down', 'look_l', None),        # right again
    (130, 1, 1, 3, 'up', 'out', 'look_r', None),
    (100, 0, 0, 2, 'down', 'out', 'half', None),
    (90, -1, 1, 3, 'down', 'out', 'look_r', None),          # a quick small one left
    (100, 0, -2, -1, 'out', 'down', 'look_l', None),
    (110, 1, -3, -1, 'out', 'down', 'look_d', 'look_u'),    # right (dazed the other way round)
    (130, 1, 1, 2, 'down', 'out', 'look_r', None),
    (110, 0, 0, 2, 'down', 'out', 'line', None),
    (110, -1, 1, 3, 'down', 'out', 'look_r', None),         # left; then frame 0 slides back to centre
]


def build():
    frames = []
    n = len(STEPS)
    for k, (ms, dx, sa, sb, la, ra, face, right) in enumerate(STEPS):
        lag = STEPS[k - 1][1]                               # the stars follow his head a step late
        frames.append((pose(dx, sa, sb, la, ra, face, right, stars=(k % 4, lag)), ms))
    assert n % 4 == 0                                       # whole star orbits: a seamless loop
    return anim(NAME, DESC, [layer('body', frames)], state=STATE)
