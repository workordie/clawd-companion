"""hop-right - a small jump to the right, turned three-quarters toward where he hops (hop-left = mirror).
Preview:  python3 gen/preview.py anim hop-right

The patch carries the whole image along the jump arc on a FIXED 700 ms timeline (on the ground 0-150 ms, in
the air 150-550 ms, back on the ground 550-700 ms; arcs of about 2 to 12 cells). The SVG draws him in place
at HOME: his box never moves in the picture, only his pose changes.

STORYBOARD (ms)  one-shot, exactly 700 ms
    0  frame 0 = the still: standing turned toward the hop (the walk's standing pose), eyes down on the
       landing spot
   70  wind-up with the ARMS (never a crouch): both arms swing back, eyes narrow to half on the target
  150  takeoff (the patch starts lifting him): legs still stretched back, pushing off; arms swing up
  230  rising: the legs leave the ground and trail; arms forward and up
  330  top of the arc: legs tucked up to one cell, arms out front and back, eyes down on the landing spot
  450  coming down: legs reach down and forward for the ground, both arms raised for balance
  550  touchdown (the patch has set him down): feet planted a little ahead, arms out, eyes squeeze to half,
       a tiny dust puff at his feet
  620  the arms swing down, the puff rolls out
  660  the plain turned standing pose (the walk's standing(), eyes open), the last specks of dust

Clawd is FINE (half-size pixels): the walk's turned body (walk_left.py, traced from the user's reference: a
1.5-cell shaded flank, the near eye on the body's leading edge, legs where the official Clawd's stand) with
fine-pixel arms and legs. He keeps his full 9 x 6 body.
The drawing faces LEFT (like _walk.body_left); hop-right is its mirror image about his home box.

SHARED KIT: the turned-pose helpers below (turned(), front(), draw_body(), eye_cells() and the NEAR / FAR arm
tables) are also used by teeter_left.py and sit_edge_left.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402
from anims._walk import mirrored, FX0, FY0, GROUND_F, HIPS   # noqa: E402,F401

NAME = 'hop-right'
STATE = 'moving (hop)'
DESC = ('A small hop, turned three-quarters toward the right: the arms wind up, legs tuck in the air, arms out '
        'on the landing with a tiny dust puff. One-shot, 700 ms; the patch carries him along the arc.')

# --------------------------------------------------------------------------------------------
# SHARED KIT: Clawd turned three-quarters to the LEFT, in fine (half-size) pixels.
# Coordinates are fine pixels relative to his box's top-left (x0, y0); at HOME that is (FX0, FY0) = (20, 24).
# Body: columns 2-19, rows 0-11 (front face '#' 2-15, flank '@' 16-19; the half turn has a 1-cell flank).
# --------------------------------------------------------------------------------------------
# Arms are chains of 2 x 2 blocks (top-left corners). NEAR = the arm on his leading (screen-left) edge,
# FAR = the shaded arm at the back of his flank (drawn before the body, so whatever overlaps it is hidden).
NEAR = {
    'rest':  [(0, 4), (0, 6)],                 # hanging at his side (as in the walk)
    'up':    [(0, 2), (0, 4)],                 # raised a cell
    'down':  [(0, 6), (0, 8)],                 # dropped a cell
    'fwd':   [(-2, 4), (0, 4)],                # straight out in front
    'upfwd': [(0, 4), (-1, 3), (-2, 2)],       # up and forward (diagonal)
    'dnfwd': [(0, 4), (-1, 5), (-2, 6)],       # down and forward (diagonal)
    'back':  [(0, 4), (1, 6)],                 # swung back: the hand half behind his body
}
FAR = {                                        # level with the near arm at rest, as in the walk (walk_left.py)
    'rest':   [(20, 4), (20, 6)],
    'up':     [(20, 2), (20, 4)],
    'down':   [(20, 6), (20, 8)],
    'back':   [(20, 4), (22, 4)],              # straight out behind
    'upback': [(20, 4), (21, 3), (22, 2)],
    'dnback': [(20, 4), (21, 5), (22, 6)],
    'fwd':    [(20, 4), (19, 6)],              # swung forward: the hand behind his flank
}
FLANK = {'turned': 17, 'half': 18}             # first flank column: a 1.5-cell flank, as in the walk
EYE_X = {'turned': (2, 12), 'half': (3, 14)}   # left fine column of the near and the far eye
# The legs stand where the official Clawd's do (cells 11, 13, 17, 19), as in the walk; the rear one is shaded.
LEG_HIPS = {'turned': [(2, '#'), (6, '#'), (14, '#'), (18, '@')], 'half': [(2, '#'), (6, '#'), (14, '#'), (18, '@')]}
GAZE = {'': (0, 0), 'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0)}   # half-step glances


def _block(ff, x, y, ch):
    for dy in (0, 1):
        for dx in (0, 1):
            ff.put(x + dx, y + dy, ch)


def draw_body(ff, x0, y0, kind='turned', near='rest', far='rest'):
    """His body and arms (no eyes), in the walk's style (walk_left.py, traced from the user's reference):
    kind 'turned' (a 1.5-cell shaded flank) or 'half' (half-way round to you: a 1-cell flank, the far arm a row
    higher). Where the far arm joins, his side is lit full width; the near arm's joint next to his body is shaded."""
    flank = FLANK[kind]
    fdy = 0 if kind == 'turned' else -1
    band = set()
    for bx, by in FAR[far]:
        _block(ff, x0 + bx, y0 + by + fdy, '@')
        if bx == 20:
            band.update((by + fdy, by + fdy + 1))
    for y in range(12):
        for x in range(2, 20):
            ff.put(x0 + x, y0 + y, '#' if x < flank or y in band else '@')
    for bx, by in NEAR[near]:
        for dy in (0, 1):
            for dx in (0, 1):
                ff.put(x0 + bx + dx, y0 + by + dy, '@' if bx + dx == 1 else '#')


def eye_cells(kind='turned', expr='open'):
    """Fine eye pixels (relative to the box) for 'shape' or 'shape/gaze': shapes open, half, line, wide; gaze
    u, d, l, r (a half step). Pixels that would leave his front face are dropped (the near eye sits on the
    edge, so a forward glance narrows it instead of poking out)."""
    shape, _, gz = expr.partition('/')
    gx, gy = GAZE[gz]
    out = []
    for ex in EYE_X[kind]:
        if shape == 'open':
            cells = [(ex + dx, 4 + dy) for dy in (0, 1) for dx in (0, 1)]
        elif shape == 'half':
            cells = [(ex + dx, 5) for dx in (0, 1)]
        elif shape == 'line':
            cells = [(ex + dx, 5) for dx in range(-1, 3)]
        elif shape == 'wide':
            cells = [(ex + dx, 3 + dy) for dy in range(3) for dx in (0, 1)]
        else:
            raise ValueError('eye shape %r (the user allows open, half, line, wide + glances)' % shape)
        out += [(x + gx, y + gy) for x, y in cells if 2 <= x + gx < FLANK[kind]]
    return out


def draw_eyes(ff, x0, y0, kind='turned', expr='open'):
    for x, y in eye_cells(kind, expr):
        ff.put(x0 + x, y0 + y, EYE_INK)


def draw_legs(ff, x0, y0, legs, ground=GROUND_F, kind='turned'):
    """legs: one spec per hip of _walk.HIPS (front to back), each None (not drawn) or (offsets, planted):
    x offsets per fine row from the hip (negative = forward); a planted leg runs down to the ground row,
    repeating its last offset, a lifted one is exactly len(offsets) rows long."""
    hip = y0 + 12
    for (hx, ch), spec in zip(LEG_HIPS[kind], legs):
        if spec is None:
            continue
        offs, planted = spec
        rows = ground - hip + 1 if planted else len(offs)
        for r in range(rows):
            dx = offs[min(r, len(offs) - 1)]
            for w in (0, 1):
                ff.put(x0 + hx + dx + w, hip + r, ch)


def turned(kind='turned', near='rest', far='rest', expr='open', legs=None, x0=FX0, y0=FY0):
    """One fine frame of Clawd turned three-quarters LEFT with his box at fine (x0, y0)."""
    ff = Frame(res=2)
    draw_body(ff, x0, y0, kind, near, far)
    if expr:
        draw_eyes(ff, x0, y0, kind, expr)
    if legs:
        draw_legs(ff, x0, y0, legs, kind=kind)
    ff.meta['clawd'] = [(x0 // 2, y0 // 2, dict(body=kind, eyes=expr))]
    return ff


def front(expr='open', larm='side', rarm='side'):
    """The plain front pose at HOME (put_clawd), as a fine frame; expr is a fine_face name."""
    f = Frame()
    p = clawd(larm=larm, rarm=rarm)
    put_clawd(f, p)
    ff = fine(f)
    if expr != 'open':
        fine_face(ff, p, expr=expr)
    return ff


def fx(name, i, x, y):
    """A library effect as a fine frame (to lay over a fine Clawd frame)."""
    f = Frame()
    f.place(get(name).sprite(i), x, y)
    return fine(f)


# --------------------------------------------------------------------------------------------
# the hop
# --------------------------------------------------------------------------------------------
LEG = {
    'stand':   ([0], True),                    # straight down to the ground
    'push':    ([0, 0, 1, 1], True),           # stretched back, pushing off
    'contact': ([0, 0, -1, -1], True),         # planted a little ahead
    'trail':   ([0, 1, 1], False),             # just left the ground, trailing
    'tuck':    ([0, 0], False),                # tucked up to one cell
    'reach':   ([0, 0, -1, -1], False),        # reaching down and forward for the ground
}


def hop_frames():
    """The hop facing LEFT (hop-left as drawn); 700 ms."""
    seq = []

    def k(ms, near, far, expr, legs, puff=None):
        if not isinstance(legs, (list, tuple)):
            legs = [legs] * 4
        ff = turned(near=near, far=far, expr=expr, legs=[LEG[l] for l in legs])
        if puff is not None:
            ff.px.update(fx('dust_puff', puff, 15, GROUND - 1).px)
        seq.append((ff, ms))
    # on the ground: anticipation with the arms and eyes
    k(70, 'rest', 'rest', 'open/d', 'stand')                         # frame 0: eyes on the landing spot
    k(80, 'back', 'dnback', 'half/d', 'stand')                       # wind-up: arms swing back
    # in the air (the patch carries him)
    k(80, 'upfwd', 'up', 'open', ['push', 'push', 'push', 'push'])   # takeoff: legs push, arms swing up
    k(100, 'upfwd', 'upback', 'open', ['trail', 'trail', 'trail', 'trail'])   # rising
    k(120, 'fwd', 'back', 'open/d', 'tuck')                          # top: tucked, arms out
    k(100, 'upfwd', 'upback', 'open/d', 'reach')                     # coming down: legs reach
    # back on the ground
    k(70, 'fwd', 'back', 'half', 'contact', puff=0)                  # touchdown
    k(40, 'dnfwd', 'dnback', 'open', 'stand', puff=1)                # arms swing down
    k(40, 'rest', 'rest', 'open', 'stand', puff=2)                   # the plain turned standing pose
    assert total_ms(seq) == 700
    return seq


def build_hop(facing):
    seq = hop_frames()
    if facing == 'right':
        seq = [(mirrored(f), ms) for f, ms in seq]
    name = 'hop-' + facing
    desc = DESC.replace('toward the right', 'toward the ' + facing)
    return anim(name, desc, [layer('body', seq)], state=STATE)


def build():
    return build_hop('right')
