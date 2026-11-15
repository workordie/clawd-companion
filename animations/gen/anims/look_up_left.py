"""look-up-left: at the bottom of the panel, Clawd sizes up the input box high above him to his LEFT.
Preview:  python3 gen/preview.py anim look-up-left

The mirror image of look-up-right (see look_up_right.py for the storyboard): he glances left (fine
look_l), turns three-quarters toward the box and looks up at it, blinks, hand to chin, a look at you,
then a determined 1-cell hop. A one-shot (1950 ms) in place at HOME, starting and ending in
put_clawd's default standing pose with eyes open; the patch then starts walk-left.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anims.look_up_right import build_look_up, STATE   # noqa: E402,F401

NAME = 'look-up-left'
DESC = ('At the bottom of the panel: turns and looks up at the input box high on his left, hand to chin, '
        'then a determined hop. One-shot, ends standing.')


def build():
    return build_look_up('left')
