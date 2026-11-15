"""sit-edge-left - an idle he does now and then: sitting on the left end of the input box, legs dangling.
Preview:  python3 gen/preview.py anim sit-edge-left        (sit-edge-right is the mirror)

CONTRACT (the patch relies on it): the box's top-left corner is canvas point (13, 17): its top surface is the
line y = 17 and its side the line x = 13 (the box is x >= 13, y >= 17; the patch shows the real box, the SVG
never draws it). His body keeps its normal 9 x 6 size and sits on the surface (bottom of his body on row 16,
body cells 10-18), turned three-quarters toward the drop; his two front legs hang over the edge, left of
x = 13, in rows 17-18 (they never cross into the box; the back legs are folded under him, unseen).

STORYBOARD (ms)  one loop = 15 000 ms; calm, one small event per loop (a leaf)
     0  frame 0 = the still: seated on the edge, turned toward the drop, legs hanging; they swing lazily
        (both together, the far leg lagging and stopping at the box's side), eyes open, looking out
  1900  a blink
  2700  he looks down at the drop; his legs slow and hang still while he looks
  3900  looks out again, the legs pick the swing back up
  4450  a glance back, then he turns half-way round to you (legs still) .. 5100 a blink at you .. 5800 back
  6150  a little bout of alternating kicks, watching his feet (a blink at 6840)
  7350  lazy swinging again
  7610  a LEAF drifts in at the top right, rocking side to side as it falls (nose down the way it glides,
        flat where a swing turns): 7730 he notices it behind him, 8320 follows it up over his head (his
        legs go still), 9620 out in front; 10660 it swings down toward his hand, 10830 he reaches out just
        as it turns past his fingertips, and it falls away (11060); 11560 down into the drop (eyes wide), out of
        sight at the bottom (12080) while he watches it go
 12530  he looks out again, a blink (12760), the legs swing again .. 13700 a glance up at the sky
 14300  looks out; the legs hang .. frame 0 starts the swing again
Eye closures (smooth half/line/half blinks): 1.9, 5.1, 6.84, 12.76 s; gaps 3.2 / 1.7 / 5.9 / 4.1 s.

Clawd is FINE (half-size pixels): the walk's turned body (kit in hop_right.py), seated with his box at
canvas cell (9, 11). Layers (identical loop length, so they stay in step): legs (behind) | body (pose,
no eyes: it only changes for the half turn and the reach) | eyes | leaf (in front).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims._walk import mirrored            # noqa: E402
from anims.hop_right import draw_body, eye_cells   # noqa: E402

NAME = 'sit-edge-left'
STATE = 'idle (sitting on the edge)'
DESC = ('Sits on the left end of the input box with his legs dangling over the edge: lazy swings and kicks, '
        'glances around, watches a leaf drift past and fall into the drop. Loop.')

LOOP = 15000
BOX_X = 13                                   # the box's side (cells); the box is x >= 13, y >= 17
X0, Y0 = 18, 22                              # his box's top-left in fine pixels: cells (9, 11)
HIP_Y = Y0 + 12                              # fine row 34 = cell row 17, right under his body
EDGE_F = 2 * BOX_X                           # first fine column of the box (nothing may be drawn there below y 17)

# ---------------------------------------------------------------------------------------------
# legs: the two front legs dangling over the edge. Near leg (front, '#') and far leg ('@', behind it).
# Strokes are 2 half-pixels wide: x offsets per fine row from the hip (negative = out toward the drop).
# ---------------------------------------------------------------------------------------------
NEAR_HIP, FAR_HIP = X0 + 2, X0 + 6           # fine columns 20-21 and 24-25 (cells 10 and 12)
LEGS = {
    'h':  [0, 0, 0, 0],                      # hanging straight down
    'f1': [0, 0, -1, -1],                    # a little forward
    'f2': [0, -1, -1, -2],                   # forward (top of the swing)
    'b1': [0, 0, 1, 1],                      # a little back, under the edge (near leg only)
    'k':  [0, -1, -2],                       # a kick: forward and up
}


def legs_frame(near, far):
    ff = Frame(res=2)
    for hip, pose, ch in ((FAR_HIP, far, '@'), (NEAR_HIP, near, '#')):     # the far leg first (behind)
        for r, dx in enumerate(LEGS[pose]):
            for w in (0, 1):
                x = hip + dx + w
                if x >= EDGE_F:
                    raise ValueError('leg %r would cross into the box' % pose)
                ff.put(x, HIP_Y + r, ch)
    return ff


SWING = [('f1', 'h', 180), ('f2', 'f1', 430), ('f1', 'f1', 170), ('h', 'h', 170), ('b1', 'h', 430),
         ('h', 'h', 180)]                    # one lazy swing (1560 ms): both legs, the far one lagging
KICKS = [('k', 'h', 230), ('h', 'k', 230), ('k', 'h', 230), ('h', 'k', 230), ('h', 'h', 280)]   # 1200 ms


# ---------------------------------------------------------------------------------------------
# body and eyes
# ---------------------------------------------------------------------------------------------
def body_frame(kind='turned', near='rest'):
    ff = Frame(res=2)
    draw_body(ff, X0, Y0, kind, near, 'rest')
    ff.meta['clawd'] = [(X0 // 2, Y0 // 2, dict(body='sitting ' + kind))]
    return ff


def eyes_frame(kind, expr):
    ff = Frame(res=2)
    for x, y in eye_cells(kind, expr):
        ff.put(X0 + x, Y0 + y, EYE_INK)
    ff.meta['fine_face'] = [expr]
    return ff


# ---------------------------------------------------------------------------------------------
# the leaf: a green blade that rocks as it falls, nose down in the direction it glides ('/' gliding left,
# '\\' gliding right), flat for an instant where a swing turns. Cells of 2 x 2 half-pixels; anchor = top-left.
# ---------------------------------------------------------------------------------------------
LEAF = {
    '/':  ['.gg', 'gG.'],
    '\\': ['Gg.', '.gg'],
    '-':  ['gGg'],
    '.':  ['gG'],                            # leaving at the bottom edge
}
# (cell x, cell y, shape, ms): in at the top right, three swings down across his head and past his face,
# then into the drop and out at the bottom (the canvas ends 3 rows under the box's top: out of sight).
LEAF_PATH = [
    (25, -1, '/', 120), (23.5, 0, '/', 110), (22, 1, '/', 120), (21, 1.5, '/', 140),
    (20, 2, '-', 220),                                                    # turns ..
    (21, 2.5, '\\', 140), (22.5, 3.5, '\\', 120), (23.5, 4, '\\', 150),
    (24, 4.5, '-', 240),                                                  # .. turns again, behind his head
    (23, 5, '/', 140), (21.5, 5.5, '/', 110), (20, 6, '/', 100), (18, 6, '/', 100), (16, 6.5, '/', 100),
    (14, 6.5, '/', 100), (12, 7, '/', 100), (10, 7.5, '/', 110), (8, 8, '/', 120), (6.5, 8.5, '/', 140),
    (5, 9, '/', 160),                                                     # a long glide over his head
    (4.5, 9.5, '-', 260),                                                 # turns in front of his face ..
    (5, 10.5, '\\', 150), (5.5, 11.5, '\\', 170),                         # .. swings toward his hand ..
    (4.5, 12.5, '-', 230),                                                # .. turns just past his fingertips
    (3.5, 13.5, '/', 150), (2.5, 14.5, '/', 150),                         # .. and falls away
    (2, 15.5, '-', 200),
    (3, 16.5, '\\', 150), (4, 17.5, '\\', 130), (5, 18.5, '\\', 120),       # down into the drop ..
    (5.5, 19.5, '.', 120),                                                # .. and out of sight
]
LEAF_T0 = 7610                               # its 4th step lands on a legs beat (7960)


def leaf_frame(x, y, shape):
    ff = Frame(res=2)
    fx, fy = int(round(2 * x)), int(round(2 * y))
    for j, row in enumerate(LEAF[shape]):
        for i, ch in enumerate(row):
            if ch == '.':
                continue
            for dy in (0, 1):
                for dx in (0, 1):
                    px, py = fx + 2 * i + dx, fy + 2 * j + dy
                    if 0 <= px < 2 * W and 0 <= py < 2 * H:      # cropped silently at the canvas edge
                        ff.put(px, py, ch)
    return ff


def leaf_times():
    """Start time of every step of the leaf path."""
    out, t = [], LEAF_T0
    for step in LEAF_PATH:
        out.append(t)
        t += step[3]
    return out, t


# ---------------------------------------------------------------------------------------------
# the story: keyframes (t, value) per layer
# ---------------------------------------------------------------------------------------------
def blink(t, after='open'):
    """A smooth fine blink starting at t: half, line, half, then `after`."""
    return [(t, 'half'), (t + 70, 'line'), (t + 160, 'half'), (t + 230, after)]


def story():
    lt, t_gone = leaf_times()
    step = lambda i: lt[i]                   # noqa: E731
    t_back = t_gone + 450                    # he stops looking down after the leaf

    # body: the half turn to you, and the reach for the leaf
    body = [(0, ('turned', 'rest')), (4600, ('half', 'rest')), (5800, ('turned', 'rest')),
            (step(23), ('turned', 'fwd')), (step(25), ('turned', 'rest'))]   # reaches as it turns away
    # eyes (their kind follows the body)
    eyes = ([(0, 'open')] + blink(1900) +
            [(2700, 'open/d'), (3900, 'open'), (4450, 'open/r'), (4600, 'open')] + blink(5100) +
            [(5800, 'open'), (6150, 'open/d')] + blink(6840, after='open/d') + [(7350, 'open'),
             (step(1), 'open/r'),            # notices the leaf behind him ..
             (step(5), 'open/u'),            # .. follows it up over his head ..
             (step(15), 'open/l'),           # .. and out in front; reaches for it ..
             (step(24), 'open/d'),           # .. too late: it falls away ..
             (step(27), 'wide/d'),           # .. down into the drop!
             (step(29), 'open/d'),           # .. watching it go
             (t_back, 'open')] + blink(t_back + 240) + [(13700, 'open/u'), (14300, 'open')])
    # legs
    legs = []
    t = [0]

    def run(seq):
        for near, far, ms in seq:
            legs.append((t[0], (near, far)))
            t[0] += ms

    def hold(pose, until):
        legs.append((t[0], pose))
        t[0] = until
    run(SWING)
    run(SWING[:4])                           # .. 2510
    hold(('f1', 'h'), 2700)                  # slowing down: he looks at the drop ..
    hold(('h', 'h'), 3900)                   # .. legs still while he looks
    run(SWING[:3])                           # .. 4680
    hold(('h', 'h'), 5800)                   # still while he is turned to you
    hold(('f1', 'h'), 6150)
    run(KICKS)                               # .. 7350
    run(SWING[:2])                           # .. 7960
    hold(('f1', 'h'), 8250)                  # the leaf has his attention: legs slow ..
    hold(('h', 'h'), t_back)                 # .. and hang still while he watches it
    run(SWING)                               # swinging again ..
    hold(('h', 'h'), LOOP)                   # .. and hanging till frame 0 starts the swing again
    # leaf
    leaf = [(0, None)] + [(lt[i], (x, y, sh)) for i, (x, y, sh, ms) in enumerate(LEAF_PATH)] + [(t_gone, None)]
    return body, eyes, legs, leaf


def keyed(keys, make):
    """Keyframes (t, value) -> layer frames (Frame, ms) over the loop; the last key holds until LOOP."""
    keys = sorted(keys, key=lambda kv: kv[0])
    out = []
    for i, (t, v) in enumerate(keys):
        t2 = keys[i + 1][0] if i + 1 < len(keys) else LOOP
        if t2 > t:
            assert t2 - t >= 40, 'a %d ms sliver at %d ms: %r' % (t2 - t, t, v)
            out.append((make(v), t2 - t))
    assert total_ms(out) == LOOP, total_ms(out)
    return out


def sit_layers(facing='left'):
    body, eyes, legs, leaf = story()
    kind_at = lambda t: [v for tt, v in body if tt <= t][-1][0]     # noqa: E731
    eyes = [(t, (kind_at(t), e)) for t, e in eyes]
    layers = [
        ('legs', keyed(legs, lambda v: legs_frame(*v))),
        ('body', keyed(body, lambda v: body_frame(*v))),
        ('eyes', keyed(eyes, lambda v: eyes_frame(*v))),
        ('leaf', keyed(leaf, lambda v: leaf_frame(*v) if v else Frame(res=2))),
    ]
    if facing == 'right':
        layers = [(n, [(mirrored(f), ms) for f, ms in fr]) for n, fr in layers]
        for _, fr in layers:                 # report where his box really is (mirrored: cells 11-21)
            for f, _ in fr:
                if 'clawd' in f.meta:
                    f.meta['clawd'] = [(30 - (X0 // 2 + 10), y, spec) for _, y, spec in f.meta['clawd']]
    return [layer(n, fr) for n, fr in layers]


def build_sit(facing):
    name = 'sit-edge-' + facing
    desc = DESC.replace('left end', facing + ' end')
    return anim(name, desc, sit_layers(facing), state=STATE)


def build():
    return build_sit('left')
