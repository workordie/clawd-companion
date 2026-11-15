"""hop-left - the mirror image of hop-right (see hop_right.py for the storyboard and the 700 ms timeline).
Preview:  python3 gen/preview.py anim hop-left
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anims.hop_right import build_hop, STATE  # noqa: E402,F401

NAME = 'hop-left'
DESC = ('A small hop, turned three-quarters toward the left: the arms wind up, legs tuck in the air, arms out '
        'on the landing with a tiny dust puff. One-shot, 700 ms; the patch carries him along the arc.')


def build():
    return build_hop('left')
