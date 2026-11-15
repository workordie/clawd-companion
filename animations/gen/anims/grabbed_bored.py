"""grabbed-bored - you've been holding him up in the air for a long time.  Preview:  python3 gen/preview.py anim grabbed-bored

Loop (6.9 s). He is held EXACTLY the way `grabbed` holds him (anims/_drag.py): box lifted a cell to
(10, 11), so his head-top (the grip, under your cursor) is at (15, 11) and his legs dangle 3 cells
long down to the bottom row. His body never leaves that spot, so the patch can swap grabbed <->
grabbed-bored at any moment without a jump; only his limbs and face move (plus a sigh puff).

STORYBOARD (ms)
     0  HANG, limp and bored: arms hanging low, heavy half-lidded eyes, legs dangling (frame 0 =
        the reduced-motion still)
  1100  a slow, lazy sway under your grip: his feet drift right, the legs swing out (1220, held),
        back through the middle (1700), out to the left (1980, held) and back (2460)
  2620  a sigh: his shoulders rise as his eyes close (arms back up to his sides, eyes line) ...
  3010  ... and drop, with a gray puff beside his head that drifts off and breaks up
  3520  eyes half open again; he tucks his arms in (3620) and waits
  4160  a foot taps in the air: tap .. tap .. tap-tap (his right outer leg lifts a cell each time)
  5510  a glance up at you (look_u): "...well?", held
  6160  back to half-lidded, a slow blink (6270), arms drop back down to hang (6650), loop (6880)
Fine-line faces (half-size pixels): half, line, look_u.  A fine body layer plus a normal-resolution
layer for the puff with the same length.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402
from anims._drag import him                  # noqa: E402

NAME = 'grabbed-bored'
STATE = 'held up for a long time (drag)'
DESC = 'Held up too long: dangles limp with half-lidded eyes, sways, sighs, tucks his arms in, taps a foot, glances at you. Loop.'

X0, Y0 = HOME
BOX = (X0, Y0 - 1)                           # where `grabbed` holds him (head-top = the grip at (15, 11))
LEGX = (1, 3, 7, 9)                          # his leg columns in the box

# Legs: per leg (columns 1, 3, 7, 9), the x offset of each cell from the top down. They dangle 3 long
# like `grabbed`. A swing bends the leading leg of each pair from the knee and only the foot of the
# other, so no gap between two legs is ever closed off (the kit would fill it with eye ink).
HANG = [[0, 0, 0]] * 4
SWAY = {
    1: [[0, 0, 0], [0, 0, 1], [0, 0, 0], [0, 0, 1]],       # the feet start to drift right
    2: [[0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1]],       # swung out right
    -1: [[0, 0, -1], [0, 0, 0], [0, 0, -1], [0, 0, 0]],
    -2: [[0, -1, -1], [0, 0, -1], [0, -1, -1], [0, 0, -1]],
}
TAP = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0]]            # right outer foot lifted a cell: a tap


def pose(face='half', legs=HANG, **kw):
    """Clawd in the grabbed spot (kw -> _drag.him: larm, rarm), with a fine-line face."""
    f = Frame()
    x, y = BOX
    p = him(f, x, y, legs='none', **kw)
    for c, offs in zip(LEGX, legs):
        for i, d in enumerate(offs):
            f.put(x + c + d, y + 6 + i, '#')
    ff = fine(f)
    fine_face(ff, p, x, y, face)
    return ff


def puff(i, x, y):
    f = Frame()
    f.place(get('smoke_puff').sprite(i), x, y)
    return f


def build():
    limp = dict(larm='down', rarm='down')
    tuck = dict(larm='front', rarm='front')
    body = []

    def add(ms, *a, **kw):
        body.append((pose(*a, **kw), ms))
    add(1100, **limp)                                       # limp and bored (the still)
    for s, ms in [(1, 120), (2, 360), (1, 120), (0, 160), (-1, 120), (-2, 360), (-1, 120), (0, 160)]:
        add(ms, legs=SWAY[s] if s else HANG, **limp)        # a slow lazy sway (eased: holds at the ends)
    add(90, 'line')                                         # sigh: shoulders rise, eyes close
    add(300, 'line')
    t_puff = total_ms(body)
    add(110, 'line', **limp)                                # ...and drop: the puff
    add(400, 'line', **limp)
    add(100, **limp)                                        # eyes half open
    add(90, **tuck)                                         # tucks his arms in
    add(450, **tuck)
    for ms_up, ms_down in [(110, 200), (110, 200), (110, 110), (110, 400)]:
        add(ms_up, legs=TAP, **tuck)                        # tap ..
        add(ms_down, **tuck)
    add(100, 'look_u', **tuck)                              # glance at you: "...well?"
    add(550, 'look_u', **tuck)
    add(110, **tuck)
    add(260, 'line', **tuck)                                # a slow blink
    add(120, **tuck)
    add(230, **limp)                                        # arms drop: back to the still
    total = total_ms(body)

    fx = [(Frame(), t_puff)]
    for i, ms, x, y in [(0, 110, 23, 12), (1, 150, 24, 12), (3, 160, 25, 11)]:
        fx.append((puff(i, x, y), ms))                      # the sigh puff drifts off and breaks up
    fx.append((Frame(), total - total_ms(fx)))
    return anim(NAME, DESC, [layer('body', body), layer('puff', fx)], state=STATE)
