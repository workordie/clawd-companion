"""Drag / throw: parachute (see _drag.py).  Preview:  python3 gen/preview.py anim parachute"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anims._drag import build_drag  # noqa: E402

NAME = 'parachute'


def build():
    return build_drag(NAME)
