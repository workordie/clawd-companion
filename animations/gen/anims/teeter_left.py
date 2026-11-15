"""teeter-left - at the very end of the input box with the drop on his LEFT: he wobbles and catches his balance.
Preview:  python3 gen/preview.py anim teeter-left        (teeter-right is the mirror)

CONTRACT (the patch relies on it): drawn in place at HOME. The box's left edge is the vertical line x = 13, so
columns 10-12 of his home box hang over empty space (nothing below them; the patch shows the real box, the
SVG never draws it). Turned toward the drop, only his front leg (half-cells 22-23) is over the edge. He ends
in the plain front standing pose (put_clawd default, eyes open) so the patch can walk him back or hop him off.

STORYBOARD (ms)  one-shot, 1600 ms
     0  frame 0 = the still: he has walked up to the edge, turned toward the drop; his front foot found
        nothing and hangs a little raised over the edge; he peers down at the drop
   160  whoa: eyes wide on the drop, both arms jerk up
   240  he tips toward the drop (1, then 2 half-cells; his planted feet stay, the legs slant): the arms windmill
        in forward circles, the front foot pedals the air, eyes wide on the drop
   580  back over the middle and too far the other way: leaning away, the front foot tucks up and the next
        foot lifts its heel, arms still windmilling
   920  back to the middle, arms out wide; one smaller tip toward the drop (1000) and back: he holds still,
        balanced, arms out (1090)
  1230  phew: the arms come down, a relieved blink (1300), he turns to you (1390, half turn) and stands in the
        plain front pose (1460-1600)

Clawd is FINE (half-size pixels): the turned body of the walk (kit in hop_right.py). He never changes size:
leaning is his whole body sliding half a cell over his planted feet.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims._walk import mirrored, FX0       # noqa: E402
from anims.hop_right import turned, front   # noqa: E402

NAME = 'teeter-left'
STATE = 'moving (teetering at the edge)'
DESC = ('At the very end of the input box with the drop on his left: he wobbles, arms windmilling and his front '
        'foot pedalling over nothing, catches his balance, sighs and turns to you. One-shot.')

# Planted legs when his body has slid dx half-cells: x offsets per row from the (moved) hip, so the foot stays.
LEAN = {0: [0], -1: [0, 0, 1, 1], -2: [0, 1, 1, 2], 1: [0, 0, -1, -1], 2: [0, -1, -1, -2]}
# The front foot over the drop (lifted strokes from its hip, negative = toward the drop).
FOOT = {
    'dangle': [0, 0, -1],                    # hanging a little raised, toe toward the drop
    'fwd':    [0, -1, -1],                   # pedalling: out over the drop
    'back':   [0, 1],                        # pedalling: pulled back and up
    'mid':    [0, 0, 1],
    'tuck':   [0, 0],                        # tucked up (leaning away)
}
# Windmill: both arms turn forward circles, half a turn apart (the near arm shows the front of its circle,
# the far arm the back of its own).
MILL = [('up', 'dnback'), ('upfwd', 'back'), ('fwd', 'upback'), ('dnfwd', 'up')]
OUT = ('fwd', 'back')                        # arms out wide for balance
LENGTH = 1600


def pose(ms, dx, arms, expr, foot, heel=False, kind='turned'):
    planted = (LEAN[dx], True)
    second = (LEAN[dx][:3] if dx else [0, 0, 0], False) if heel else planted   # leg 2 lifts its heel
    legs = [(FOOT[foot], False), second, planted, planted]
    return (turned(kind=kind, near=arms[0], far=arms[1], expr=expr, legs=legs, x0=FX0 + dx), ms)


def teeter_frames():
    """Facing LEFT (teeter-left as drawn)."""
    seq = [
        pose(160, 0, ('rest', 'rest'), 'open/d', 'dangle'),   # frame 0: at the edge, peering down
        pose(80, 0, ('up', 'up'), 'wide/d', 'fwd'),           # whoa!
        pose(80, -1, MILL[0], 'wide/d', 'back'),              # tipping toward the drop, windmilling
        pose(90, -2, MILL[1], 'wide/d', 'fwd'),
        pose(90, -2, MILL[2], 'wide/d', 'mid'),
        pose(80, -1, MILL[3], 'wide/d', 'fwd'),
        pose(70, 0, MILL[0], 'wide', 'back'),                 # back over the middle ..
        pose(80, 1, MILL[1], 'wide', 'tuck', heel=True),      # .. and too far the other way
        pose(110, 2, MILL[2], 'wide', 'tuck', heel=True),
        pose(80, 1, MILL[3], 'wide', 'tuck'),
        pose(80, 0, OUT, 'open/d', 'dangle'),                 # arms out wide
        pose(90, -1, OUT, 'open/d', 'fwd'),                   # one smaller tip toward the drop ..
        pose(140, 0, OUT, 'open', 'dangle'),                  # .. and back: balanced. hold
        pose(70, 0, ('dnfwd', 'dnback'), 'half', 'dangle'),   # phew: arms come down
        pose(90, 0, ('rest', 'rest'), 'line', 'dangle'),      # a relieved blink
        pose(70, 0, ('rest', 'rest'), 'half', 'dangle', kind='half'),   # turning to you
    ]
    seq.append((front(), LENGTH - total_ms(seq)))              # the plain standing pose
    return seq


def build_teeter(facing):
    seq = teeter_frames()
    if facing == 'right':
        seq = [(mirrored(f), ms) for f, ms in seq]
    name = 'teeter-' + facing
    desc = DESC.replace('on his left', 'on his ' + facing)
    return anim(name, desc, [layer('body', seq)], state=STATE)


def build():
    return build_teeter('left')
