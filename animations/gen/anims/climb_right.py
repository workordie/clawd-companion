"""climb-right: he walks straight up a wall on his right, the way a crab or a beetle does.

It is the walk cycle (walk_left.py, traced from the user's reference walk) turned a quarter: walk-right rotated
90 degrees counter-clockwise, so his feet are on the wall, his head points up and his back faces away from the wall.
The stride's bob becomes a small push away from the wall, and his planted feet drift down in his frame by the
distance he climbs, so they stay put on the wall. (The first draft, a standing Clawd reaching up hand over hand,
read as a stiff figure floating up with an antenna; 2026-11-15.)

Contract (custom.js places it):
- The wall's face is the line x = 21 cells (fine x 42); his feet are against it and nothing crosses it.
- His rear (the bottom of the turned body) is on the canvas's bottom edge (y = 20 cells), so a climb starts with
  him standing on the bottom of the panel, and his front reaches up to row 9.
- The SVG climbs on the spot; the patch slides the whole image up at 6 cells/s (the stride's 2 cells per 335 ms).
- At the top the patch flips him upright onto the box (a quarter turn over the corner) and he walks on.
climb-left is the mirror image (wall on his left, at x = 10 cells).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims.walk_left import cycle            # noqa: E402

NAME = 'climb-right'
DESC = ('Walks straight up the wall on his right like a crab: the reference walk turned a quarter, feet on the '
        'wall, head up. Loops on the spot; the patch slides him up 6 cells/s.')
STATE = 'climbing (walking up the side of the input box)'
POSE_MS = 67                                 # 5 poses = 335 ms per 2-cell stride = 6 cells/s


def turned(ff):
    """A walk-right frame turned 90 degrees counter-clockwise: feet on the wall at fine x 42, rear on the bottom edge."""
    out = Frame(res=2)
    for (x, y), c in ff.px.items():
        out.px[(y + 2, 59 - x)] = c          # ground y 40 -> wall x 42; his back (x 20) -> bottom row 39
    out.meta = dict(ff.meta)
    return out


def frames():
    return [(turned(f), ms) for f, ms in cycle('right', POSE_MS)]


def build():
    return anim(NAME, DESC, [layer('body', frames())], state=STATE)
