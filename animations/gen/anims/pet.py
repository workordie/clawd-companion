"""pet - you're petting him (moving the cursor back and forth over him).  Preview:  python3 gen/preview.py anim pet

One-shot (2.93 s), in place at HOME. He leans into it, sways in rhythm with your strokes, eyes closed
in contentment; little sparkles and notes float up beside him (never over him: that's where your
cursor is), a tiny shiver of joy, and back to the plain standing pose.

STORYBOARD (ms)
     0  plain at HOME, eyes on you (frame 0 = the reduced-motion still)
   140  the first stroke: his lids lower (half) ... and close (line, a thin content line, 210)
   330  he leans into your hand: his whole body sways a cell right and tilts (left shoulder up,
        right shoulder down); a gold glint pops up on that side and floats away, twinkling
   630  back through the middle ... 730 leans left: a violet note pops up on the left and floats up,
        swaying ... 1130 right again (a note) ... 1530 left again (a glint)
        (leans held 300 ms, the middle passed in 100 ms: the rhythm of a hand stroking him)
  1930  a tiny shiver of joy: his whole body quivers half a cell left and right, arms up a cell,
        while two little glints twinkle at his sides
  2170  settles, arms down ... 2250 eyes open slowly (half) ... 2330 a twinkle in his eyes
        (sparkle) ... 2710 plain open eyes, plain standing pose (ends at 2930)
Fine-line faces (half-size pixels): open, half, line, sparkle.  A fine body layer plus a normal-
resolution effects layer of the same length.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402
from anims._drag import him                  # noqa: E402

NAME = 'pet'
STATE = 'play (cursor petting him)'
DESC = 'Petted: eyes closed, he leans into your strokes side to side while glints and notes float up, a tiny happy shiver. One-shot.'

X0, Y0 = HOME
NOTE_SMALL = Sprite(['.vl', '.v.', 'vV.'], anchor=(1, 1))      # a 3x3 eighth note: pop-in / drift-off size
NOTE_DOT = Sprite(['v'], anchor=(0, 0))


def pose(face='open', dx=0, shift=0, tilt=0, **kw):
    """Clawd at HOME + dx cells (kw -> _drag.him: larm, rarm, legs). tilt +1 / -1: he leans right / left,
    one shoulder up and the other down (arms 'up' / 'down'), his normal body never changes shape.
    shift: fine pixels (half cells) sideways, for the shiver."""
    if tilt:
        kw['larm'], kw['rarm'] = ('up', 'down') if tilt > 0 else ('down', 'up')
    f = Frame()
    p = him(f, X0 + dx, Y0, **kw)
    ff = fine(f)
    fine_face(ff, p, X0 + dx, Y0, face)
    if shift:
        ff = ff.shifted(shift, 0)
    return ff


# ------------------------------------------------------------------ effects (normal resolution)
def spr(s, x, y):
    return lambda f: f.place(s, x, y)


def acc(name, i, x, y):
    return spr(get(name).sprite(i), x, y)


def glint(x, y, rise):
    """A small gold glint that pops in and floats up `rise`, twinkling (dot, plus, x, plus, dot)."""
    path = [(x, y), (x, y - 1), (x + rise[0], y - 2), (x + rise[0], y - 3), (x + rise[1], y - 4)]
    frames, ms = [0, 1, 2, 1, 0], [100, 100, 100, 100, 100]
    return [(m, acc('sparkle_small', i, px, py)) for i, m, (px, py) in zip(frames, ms, path)]


def note(x, y, sway):
    """A violet note that pops in small, floats up a cell per beat with a sway, shrinks and drifts off."""
    out = [(100, spr(NOTE_SMALL, x, y + 1))]
    for k, dx in enumerate(sway):
        out.append((150, acc('note', 0, x + dx, y - k)))
    n = len(sway)
    out += [(100, spr(NOTE_SMALL, x + sway[-1], y - n)), (100, spr(NOTE_DOT, x + sway[-1], y - n - 1))]
    return out


def twinkle(x, y, ms):
    return [(m, acc('sparkle_small', i, x, y)) for i, m in zip([0, 1, 2, 1, 0], ms)]


def fx_layer(name, total, runs, body_cuts=()):
    """runs: [(t0, [(ms, drawer or None), ...])] at absolute times; they may overlap. One normal frame
    per stretch of time in which nothing changes. A change within 40 ms of a body cut moves onto it, and
    changes of overlapping effects that fall within 40 ms of each other share one cut (no slivers)."""
    spans = []
    for t0, beats in runs:
        t = t0
        for ms, d in beats:
            if d is not None:
                spans.append((t, t + ms, d))
            t += ms
    near = lambda t: min(body_cuts, key=lambda c: abs(c - t)) if body_cuts else t
    spans = [(near(s0) if abs(near(s0) - s0) < 40 else s0, near(s1) if abs(near(s1) - s1) < 40 else s1, d)
             for s0, s1, d in spans]
    edges = sorted({c for s in spans for c in s[:2] if 0 < c < total})
    cuts = [0]
    for e in edges:
        if e - cuts[-1] >= 40 and total - e >= 40:
            cuts.append(e)
    cuts.append(total)
    snap = lambda t: min(cuts, key=lambda c: (abs(c - t), c))
    spans = [(snap(s0), snap(s1), d) for s0, s1, d in spans]
    frames = []
    for a, b in zip(cuts, cuts[1:]):
        f = Frame()
        for s0, s1, d in spans:
            if s0 <= a < s1:
                d(f)
        frames.append((f, b - a))
    return layer(name, frames)


# ------------------------------------------------------------------
def build():
    body, marks = [], {}

    def add(ms, *a, **kw):
        body.append((pose(*a, **kw), ms))

    def mark(name):
        marks[name] = total_ms(body)

    add(140)                                                  # plain (the still)
    add(70, 'half')                                           # the first stroke: lids lower...
    add(120, 'line')                                          # ...and close
    for k, side in enumerate([1, -1, 1, -1]):                 # leans into your hand, in rhythm
        mark('lean%d' % k)
        add(300, 'line', dx=side, tilt=side)
        add(100, 'line')
    mark('shiver')
    for s in (1, -1, 1, -1):                                  # a tiny shiver of joy (half a cell)
        add(60, 'line', shift=s, larm='up', rarm='up')
    add(80, 'line')
    add(80, 'half')
    mark('sparkle')
    add(380, 'sparkle')                                       # a twinkle in his eyes
    add(220, 'open')                                          # plain standing pose
    total = total_ms(body)

    m = marks
    runs = [
        (m['lean0'], glint(24, 10, (1, 2))),                  # right lean: a glint
        (m['lean1'], note(6, 9, [0, -1, 0, 1])),              # left lean: a note
        (m['lean2'], note(25, 9, [0, 1, 0, -1])),             # right: a note
        (m['lean3'], glint(7, 10, (-1, -2))),                 # left: a glint
        (m['shiver'], twinkle(7, 12, [60, 60, 60, 60, 80])),  # joy: glints at his sides, on his beat
        (m['shiver'] + 60, twinkle(23, 11, [60, 60, 60, 80, 80])),
    ]
    cuts, t = [], 0
    for _, ms in body:
        t += ms
        cuts.append(t)
    return anim(NAME, DESC, [layer('body', body), fx_layer('fx', total, runs, cuts)], state=STATE)
