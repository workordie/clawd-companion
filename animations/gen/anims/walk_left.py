"""Walk cycle, traced from the user's reference recording (Screen Recording 2026-11-13 at 3.14.04 am.mov).

The reference was traced frame by frame at half-cell precision (2026-11-15). Its stride is five poses, each held
about 100 ms, in which he steps two cells forward:
  CONTACT  body at standing height, legs short; the front foot just lifted, the others planted
  REACH    body up half a cell; the front leg reaches forward, a rear leg kicks back; near arm down, far arm up
  SPREAD   body up half a cell; the front foot planted ahead, legs splayed
  PUSH     body up a full cell; the front leg straight and planted, the second pushing back, the rear legs lifted
  PASS     body up half a cell; legs gathered under him, arms level again
He is turned three-quarters toward where he walks: both eyes slide to the leading side (the near eye on the body's
edge), the far 1.5 cells of his body are a shaded flank and the far arm is shaded; on the arm rows the body is lit
full width (the band the reference has). Legs are one cell wide and bend in half-cell steps (fine pixels), so the
diagonals stay smooth. His body keeps its full size; only the legs lengthen when he rises.
The reference Clawd is 8 cells wide with 2-cell arms; this is drawn on the official 9-wide Clawd (1-cell arms),
so the rear legs sit one cell further back than in the reference.

The SVG walks on the spot; the patch slides him at 4 cells/s (two cells per 500 ms stride). Planted feet drift
back in his frame by about the distance he moves, as in the reference, so they stay put on the ground.
Frame 0 is the contact pose. walk-right is the mirror image (walk_right.py).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'walk-left'
DESC = ('Walking left, traced from the reference walk: turned three-quarters, a five-pose stride that lifts him up '
        'to a cell, long jointed legs, arms swinging. Loops on the spot; the patch slides him 4 cells/s.')
STATE = 'walking (moving along the input box)'

FX0, FY0 = 2 * HOME[0], 2 * HOME[1]          # his box's top-left in half-size pixels (20, 24)
BX = FX0 + 2                                  # his body's left edge (fine x 22); body is 18 wide, 12 tall
POSE_MS = 100

# Legs: (rows, shaded). rows = the leg's left column (relative to his body's left edge) for each half-pixel row
# from his hip down; (x, w) marks a wider row (a knee). Planted legs reach the ground (4 + bob rows); lifted legs
# are shorter. A is the front leg, B the second, C the third, D the far rear leg (shaded, behind the flank).
POSES = {
    'contact': dict(bob=0, near=0, far=0, legs=[
        ([-1, -1, -1], False),
        ([3, 3, 2, 2], False),
        ([12, 12, 13, 13], False),
        ([16, 16, 16, 16], True)]),
    'reach': dict(bob=1, near=1, far=-1, legs=[
        ([0, (-1, 3), (-2, 3), -2], False),
        ([4, 4, 4, 4, 4], False),
        ([12, 12, (12, 3), 14], False),          # a 3-wide knee keeps the gap to the far leg open
        ([16, (16, 3), 17, 17, 17], True)]),
    'spread': dict(bob=1, near=1, far=-1, legs=[
        ([0, (-1, 3), -1, -2, -2], False),
        ([4, 4, (4, 3), 5, 5], False),
        ([11, 11, (11, 3), 12], False),
        ([16, (16, 3), 17, 18, 18], True)]),
    'push': dict(bob=2, near=1, far=-1, legs=[
        ([0, 0, 0, 0, 0, 0], False),
        ([3, 3, (3, 3), 4, 6, 6], False),
        ([(9, 3), (9, 3), 9, 9], False),
        ([(14, 3), (14, 3), 16, 16], True)]),
    'pass': dict(bob=1, near=0, far=0, legs=[
        ([(0, 5), (0, 5), (1, 3), (1, 3), 1], False),   # the two front legs gathered into one, as in the reference
        ([10, 10, 10, 10, 10], False),
        ([14, 14, 14, 13, 13], True)]),
}
CYCLE = ['contact', 'reach', 'spread', 'push', 'pass']
EYES = (0, 10)                                # left columns of his two eyes, relative to his body's left edge


def pose_frame(name, eyes='open'):
    """One pose of the stride, facing left, as a fine frame (64 x 40) with his box at HOME."""
    p = POSES[name]
    ff = Frame(res=2)
    top = FY0 - p['bob']
    band = set(range(top + 4 + p['far'], top + 8 + p['far']))      # lit full width where the far arm joins
    for y in range(top, top + 12):
        for x in range(18):
            ff.put(BX + x, y, '#' if x < 15 or y in band else '@')
    for y in range(top + 4 + p['far'], top + 8 + p['far']):          # far arm, shaded
        ff.put(BX + 18, y, '@')
        ff.put(BX + 19, y, '@')
    for y in range(top + 4 + p['near'], top + 8 + p['near']):        # near arm, its joint shaded
        ff.put(BX - 2, y, '#')
        ff.put(BX - 1, y, '@')
    for ex in (EYES if eyes else ()):
        if eyes == 'open':
            for dx in (0, 1):
                ff.put(BX + ex + dx, top + 4, 'k')
                ff.put(BX + ex + dx, top + 5, 'k')
        else:                                                         # 'line': a closed blink
            for dx in (0, 1):
                ff.put(BX + ex + dx, top + 5, 'k')
    leg_top = top + 12
    for rows, shaded in p['legs']:
        for r, spec in enumerate(rows):
            x, w = spec if isinstance(spec, tuple) else (spec, 2)
            for dx in range(w):
                ff.put(BX + x + dx, leg_top + r, '@' if shaded else '#')
    ff.meta.setdefault('clawd', []).append((HOME[0], HOME[1], dict(eyes=eyes, body='walk')))
    return ff


def mirrored(ff):
    """The same fine frame flipped left-right about his home box (so walk-right stays at HOME)."""
    out = Frame(res=2)
    axis = 2 * FX0 + 21                       # his box spans fine x FX0 .. FX0 + 21
    for (x, y), c in ff.px.items():
        out.px[(axis - x, y)] = c
    out.meta = dict(ff.meta)
    return out


# Four strides (2 s) with one blink off the beat, so a long walk isn't mechanical.
BLINK = {(1, 3), (1, 4)}


def cycle(facing='left', ms=POSE_MS, strides=4):
    seq = []
    for s in range(strides):
        for k, name in enumerate(CYCLE):
            f = pose_frame(name, 'line' if (s, k) in BLINK else 'open')
            seq.append((mirrored(f) if facing == 'right' else f, ms))
    return seq


def build():
    return anim(NAME, DESC, [layer('body', cycle('left'))], state=STATE)
