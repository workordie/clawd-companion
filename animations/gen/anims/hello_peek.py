"""hello-peek - Session start (variant): Clawd climbs up from behind the input box.
Preview:  python3 gen/preview.py anim hello-peek

A ONE-SHOT greeting (the patch plays it once when the chat panel opens; idle follows), so the story
reads left to right and ends in the plain standing pose at HOME, held.
The canvas's bottom edge is the input box's top border: below it, he is hidden behind the box.

STORYBOARD (ms; one shared timeline drives every layer; 3960 ms in all)
     0  frame 0 (the reduced-motion still: the peeking start): only the top two rows of his head show
        above the box edge, and his two fingertips hook over the edge beside it (Kilroy style)
   380  he rises a row: his eyes come up over the edge, looking up a little (peek!)
   510  up one more: chin on the sill, both arms resting on the edge; eyes on the room
   690  looks LEFT (slides there in a half step, then the full step; held 290 ms), back through the
        middle, then RIGHT (held), back to the middle ...
  1650  ... spots YOU: a gold "!" pops above his head and his eyes go WIDE (220 ms), then a quick
        blink (half, line, half) and they SPARKLE: it's you!
  2190  climbs out: both hands push down on the edge (the arms stay planted, he rises a row), his body
        clears the edge (legs still behind it, arms out), a hop to one row above HOME with his legs
        tucked, and at 2470 he lands at HOME on the box (dust puffs roll out from his feet).
        The "!" is gone once he leaves the sill.
  2770  waves hello with his right arm (wave, raise, wave, raise, wave), sparkle eyes
  3480  arm down, the sparkle fades to his plain open eyes: the plain standing pose at HOME, held to
        the end (480 ms), so wherever the patch cuts to idle he is standing ready
Body: always the normal 9 x 6 body at normal size (STYLE.md 0): behind the box he is simply clipped by
the edge (his pose is trimmed to the canvas, nothing is drawn outside it), and the hop moves his whole
body. Hand-made cells: only the two fingertips on the edge in the first two keys.
Face: fine-line eyes (STYLE.md 0b) in their own fine layer over a solid face: open, wide, half, line,
sparkle, with half- and full-step gaze offsets for the look-around (look_l / look_r / look_u family).
Layers: clawd (body + dust + "!") | face (fine eye ink). Both are cut from the same KEYS.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'hello-peek'
STATE = 'hello (variant)'
DESC = ('Peeks up from behind the input box (just the top of his head and two fingertips on the edge), '
        'looks left and right, spots you with a little "!", climbs up onto the box with a hop and waves '
        'hello, then stands ready.')

DUST = get('dust_puff')

# Gaze offsets in fine (half-cell) pixels: the kit's fine look_* steps, plus the full-cell versions
# (the kit's own look_l / look_r) for the clear left / right scan.
_GAZE = {
    'c': (0, 0),
    'u': (0, -1),       # fine look_u
    'l1': (-1, 0),      # fine look_l (half step)
    'l2': (-2, 0),      # kit look_l (full cell)
    'r1': (1, 0),
    'r2': (2, 0),
}

# a small gold "!" (2 wide: a 3-cell bar over a dot), lit from the top-left: a yellow tip, gold body and
# a dark-gold shadow side, so it reads on both themes; anchor = the dot's left cell
_BANG = Sprite(['yj',
                'jJ',
                'jJ',
                '..',
                'jJ'], anchor=(0, 4), name='peek_bang')
_BANG_AT = (15, 14)          # above his head while he is on the sill (head top = row 16)

# ------------------------------------------------------------------------------------ keys
# y = his box's top row (HOME 12); nubs = the two fingertips on the edge; eyes = FINE_EYES name or None;
# look = _GAZE key; bang = the "!"; dust = dust_puff frame.
KEYS = [
    # behind the box: the top of his head and his fingertips over the edge
    ('peek0',  dict(y=18, nubs=1, larm='none', rarm='none', eyes=None), 380),
    ('peek1',  dict(y=17, nubs=1, larm='none', rarm='none', look='u'), 130),
    # chin on the sill, arms on the edge
    ('sill',   dict(y=16), 180),
    # looks left ... and right
    ('l_a',    dict(y=16, look='l1'), 60),
    ('l_b',    dict(y=16, look='l2'), 290),
    ('l_c',    dict(y=16, look='l1'), 60),
    ('mid',    dict(y=16), 60),
    ('r_a',    dict(y=16, look='r1'), 60),
    ('r_b',    dict(y=16, look='r2'), 290),
    ('r_c',    dict(y=16, look='r1'), 60),
    ('mid2',   dict(y=16), 80),
    # ... spots you!
    ('spot',   dict(y=16, eyes='wide', bang=1), 220),
    ('bl1',    dict(y=16, eyes='half', bang=1), 50),
    ('bl2',    dict(y=16, eyes='line', bang=1), 80),
    ('bl3',    dict(y=16, eyes='half', bang=1), 50),
    ('glee',   dict(y=16, eyes='sparkle', bang=1), 140),
    # climbs out: both hands push down on the edge (the arms stay put, he rises), hop, land at HOME
    ('push',   dict(y=15, larm='down', rarm='down', eyes='sparkle'), 100),
    ('rise',   dict(y=14, larm='out', rarm='out', eyes='sparkle'), 70),    # legs still behind the edge
    ('apex',   dict(y=11, larm='out', rarm='out', legs='short', eyes='sparkle'), 110),
    ('land',   dict(larm='out', rarm='out', eyes='sparkle', dust=0), 80),
    ('settle', dict(eyes='sparkle', dust=1), 100),
    ('dust',   dict(eyes='sparkle', dust=2), 120),
    # waves hello (right arm)
    ('w1',     dict(rarm='wave', eyes='sparkle'), 180),
    ('w2',     dict(rarm='raise', eyes='sparkle'), 100),
    ('w3',     dict(rarm='wave', eyes='sparkle'), 160),
    ('w4',     dict(rarm='raise', eyes='sparkle'), 100),
    ('w5',     dict(rarm='wave', eyes='sparkle'), 170),
    # the plain standing pose, held until idle takes over
    ('ready',  dict(), 480),
]


def _kit(k):
    return clawd(eyes='blink', larm=k.get('larm', 'side'), rarm=k.get('rarm', 'side'),
                 legs=k.get('legs', 'stand'))


def _pose(k):
    """His pose for key k with a solid face (the face layer draws his eyes), trimmed to the canvas
    when he is still behind the box, plus the two fingertips on the edge in the first keys."""
    y = k.get('y', HOME[1])
    p = _kit(k)
    cells = [c for c in p.sprite.cells if y + c[1] <= GROUND]
    if k.get('nubs'):
        r = GROUND - y
        cells += [(-1, r, '#'), (11, r, '#')]
    return Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec))


def _body(k):
    f = Frame()
    put_clawd(f, _pose(k), HOME[0], k.get('y', HOME[1]))
    if k.get('dust') is not None:
        f.place(DUST.sprite(k['dust']), 15, GROUND - 1)
    if k.get('bang'):
        f.place(_BANG, *_BANG_AT)
    return f


def _face(k):
    """Only the fine eye pixels (ink and glint) for key k: the kit's fine_face expression shifted by
    the gaze. Guard: every pixel lies on his visible face and never touches the background."""
    g = Frame(res=2)
    expr = k.get('eyes', 'open')
    if expr is None:
        return g
    y = k.get('y', HOME[1])
    p = _pose(k)                                 # trimmed to the canvas: nothing drawn outside it
    f = Frame()
    put_clawd(f, p, HOME[0], y)
    body = fine(_body(k))
    base = fine(f)
    ff = fine_face(base.copy(), p, HOME[0], y, expr=expr)
    dx, dy = _GAZE[k.get('look', 'c')]
    ink = {(x + dx, yy + dy): c for (x, yy), c in ff.px.items() if base.px.get((x, yy)) != c}
    for (x, yy) in ink:
        if body.px.get((x, yy)) != '#':
            raise ValueError('eye pixel (%d,%d) is off his face: %r' % (x, yy, k))
        for n in ((x + 1, yy), (x - 1, yy), (x, yy + 1), (x, yy - 1)):
            if n not in ink and body.px.get(n) not in ('#', '@', '%'):
                raise ValueError('eye pixel (%d,%d) touches the background: %r' % (x, yy, k))
    g.px = ink
    g.meta = {'fine_face': [(expr, expr)], 'gaze': k.get('look', 'c')}
    return g


def build():
    body = [(_body(k), ms) for _, k, ms in KEYS]
    face = [(_face(k), ms) for _, k, ms in KEYS]
    # the last key is exactly the plain standing pose at HOME (kit default, eyes open)
    end = fine(body[-1][0]).over(face[-1][0])
    plain = Frame()
    put_clawd(plain, clawd())
    assert end.px == fine(plain).px, 'hello-peek must end in the plain standing pose'
    return anim(NAME, DESC, [layer('clawd', body), layer('face', face)], state=STATE)
