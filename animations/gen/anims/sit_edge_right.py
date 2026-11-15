"""sit-edge-right - the mirror image of sit-edge-left: sitting on the RIGHT end of the input box, legs dangling
over its edge. Contract: the box's top-right corner is canvas point (18, 17) (the box is x <= 18, y >= 17);
his body sits on row 16 (cells 12-20), his legs hang right of x = 18 in rows 17-18.
See sit_edge_left.py for the storyboard. Preview:  python3 gen/preview.py anim sit-edge-right
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anims.sit_edge_left import build_sit, STATE  # noqa: E402,F401

NAME = 'sit-edge-right'
DESC = ('Sits on the right end of the input box with his legs dangling over the edge: lazy swings and kicks, '
        'glances around, watches a leaf drift past and fall into the drop. Loop.')


def build():
    return build_sit('right')
