"""teeter-right - the mirror image of teeter-left: the drop is on his RIGHT, the box's edge is the vertical
line x = 18 (columns 18-20 of his home box hang over empty space). See teeter_left.py for the storyboard.
Preview:  python3 gen/preview.py anim teeter-right
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anims.teeter_left import build_teeter, STATE  # noqa: E402,F401

NAME = 'teeter-right'
DESC = ('At the very end of the input box with the drop on his right: he wobbles, arms windmilling and his front '
        'foot pedalling over nothing, catches his balance, sighs and turns to you. One-shot.')


def build():
    return build_teeter('right')
