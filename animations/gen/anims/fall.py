"""Drag / throw: fall (see _drag.py).  Preview:  python3 gen/preview.py anim fall"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anims._drag import build_drag  # noqa: E402

NAME = 'fall'


def build():
    return build_drag(NAME)
