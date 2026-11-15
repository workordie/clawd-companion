"""walk-right: the mirror image of walk-left (see walk_left.py), drawn at HOME."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims.walk_left import cycle, STATE     # noqa: E402

NAME = 'walk-right'
DESC = ('Walking right, traced from the reference walk: turned three-quarters, a five-pose stride that lifts him '
        'up to a cell, long jointed legs, arms swinging. Loops on the spot; the patch slides him 4 cells/s.')


def build():
    return anim(NAME, DESC, [layer('body', cycle('right'))], state=STATE)
