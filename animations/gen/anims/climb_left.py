"""climb-left: the mirror image of climb-right (see climb_right.py): he walks up a wall on his LEFT, its face at
x = 10 cells, his rear on the canvas's bottom edge. The patch slides him up 6 cells/s."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims.climb_right import frames, STATE  # noqa: E402
from anims.walk_left import mirrored         # noqa: E402

NAME = 'climb-left'
DESC = ('Walks straight up the wall on his left like a crab: the reference walk turned a quarter, feet on the '
        'wall, head up. Loops on the spot; the patch slides him up 6 cells/s.')


def build():
    return anim(NAME, DESC, [layer('body', [(mirrored(f), ms) for f, ms in frames()])], state=STATE)
