"""Example animation (files starting with '_' are not built). Preview:  python3 gen/preview.py anim _example

Shows the patterns every animation uses:
  * Clawd always drawn with put_clawd(), accessories with wear()
  * a body layer whose frames carry Clawd + everything attached to him (so they never desync)
  * an independent effect layer with its own loop length (steam)
  * frame 0 = a good still (reduced-motion users only ever see frame 0 of each layer)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import _example as ex               # real animations use: from acc import get

NAME = '_example'
STATE = 'example only'
DESC = 'Example: sips from a mug, blinks; steam loops on its own.'


def body(eyes='open', sip=False):
    f = Frame()
    p = clawd(eyes=eyes, rarm='up' if sip else 'side')
    put_clawd(f, p)
    wear(f, ex.BEANIE, p)
    wear(f, ex.MUG, p)
    return f


def build():
    b = [
        (body(), 1800),
        (body('blink'), 120),
        (body(), 900),
        (body(sip=True), 160),          # raise the mug
        (body('closed', sip=True), 700),  # sip with eyes closed
        (body(sip=True), 160),
        (body(), 1400),
    ]
    steam = []
    for i in range(3):
        f = Frame()
        f.place(ex.STEAM.sprite(i), HOME[0] + 13, HOME[1] + 1)
        steam.append((f, ex.STEAM.ms))
    return anim(NAME, DESC, [layer('body', b), layer('steam', steam)], state=STATE)
