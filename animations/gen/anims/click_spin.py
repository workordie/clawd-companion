"""Click reaction: click-spin (see _clicks.py).  Preview:  python3 gen/preview.py anim click-spin"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anims._clicks import build_reaction, REACTIONS  # noqa: E402

NAME = 'click-spin'
STATE = 'clicked (one-shot)'
DESC = REACTIONS[NAME][1]


def build():
    return build_reaction(NAME)
