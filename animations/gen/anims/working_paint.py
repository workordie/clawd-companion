"""working-paint - Working variant: Clawd paints a little landscape at his easel.   Preview:  python3 gen/preview.py anim working-paint

Storyboard (one 16.6 s timeline drives every synced layer; _timeline() has the exact beats):
     0  frame 0: at HOME in a small red beret, palette (three paint dabs and a mixing spot) in his left
        claw, a long red-handled brush in his right, its green tip on the canvas's bottom-left corner: a
        tripod easel beside him holds a canvas with the sky and the sun already painted.  Eyes on it.
  0.52  HILL: the tip sweeps along the bottom row left to right and back along the next one, the green
        building up behind it, then dabs the hilltop; the brush lifts.  A blink, a look at you, his eyes
        go up to the sky first ("a tree, there") ...
  2.9   DAB (each new colour): the palette swings in front of him through a plain in-between, the brush
        dips into the mixing spot and takes the colour, the palette swings back out as the brush goes
        to the canvas.  TREE (dark green): the crown up high, then the trunk down onto the hill.
  4.4   STEP BACK to judge it: two steps back (legs swinging; palette and beret go with him), then the
        painter's measure, the brush held upright at arm's length, lids half down, eyes running over
        the picture (up, then level) ... one more thing: two steps back in.
  7.3   THE DOT: his eyes go to the sky, the brush comes in, touches a little bird far off, lifts.
  8.1   REWARD: sparkle eyes, a gold twinkle grows on the canvas corner and fades; a pleased look at
        you; a slow blink.
 10.3   FRESH CANVAS: his eyes go up first; a blank canvas comes down from above, his claw rises to meet
        its edge and guides it onto the ledge in front of the finished painting: it lands, bounces a
        row, settles; his claw lingers on the edge, then drops.
 11.8   SKY (cyan): two sweeps, along the top left to right, then back across the rows below.  A blink,
        eyes to the top corner first ... SUN (yellow): two dabs in the corner.  Green on the brush, the
        tip back on the bottom-left corner: frame 0.
Seamless: the timeline ends in frame 0's state (sky + sun painted, green on the brush).  The finished
painting disappears behind the fresh canvas, and in the instant it lands the paint layers clear (the
picture underneath is identical), so the swap never pops.  Blinks fall at uneven gaps (1.8, 9.7, 13.2 s).
Face: fine-line (STYLE 0b) eyes in their own fine layer over a solid face: open, half, line, look_*,
sparkle only.  Normal body size throughout.
Layers (back to front): easel (static: legs, ledge, mast, the blank canvas) | sky (+ sun) | land (hill,
tree, the dot) | fresh (the canvas coming down) | body (the cells every arm pose shares, legs, beret) |
larm (+ palette) | rarm (+ brush; its tip in the mixing spot while it dips) | face (fine) | fx.
The brush is drawn as a clean line from his claw to its tip; the arm pose for each tip position is
chosen so the brush stays a comfortable length and the arm holds still while the brush pivots.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'working-paint'
STATE = 'working (variant)'
DESC = ('In a little red beret, Clawd paints a landscape at his easel: dabs each colour from his palette, '
        'sweeps in the hill and a tree, steps back to measure it with his brush, adds a last little bird, '
        'sparkles, and guides a fresh canvas onto the easel for the next one.')


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


# ---------------------------------------------------------------------------------------------- props
# The canvas: a tan stretcher frame (lit top-left, shaded bottom-right: a mid-tone contour on both
# themes) round a paper-white surface; inner area x 23..28, y 6..11.
_CANVAS = [
    'tttttttT',
    'twwwwwwT',
    'twwwwwwT',
    'twwwwwwT',
    'twwwwwwT',
    'twwwwwwT',
    'twwwwwwT',
    'tTTTTTTT',
]
_CANVAS_AT = (22, 5)


def _easel():
    """A-frame tripod: two splayed front legs, a ledge the canvas stands on, the mast above it."""
    f = Frame()
    for x, y in ((23, 14), (23, 15), (22, 16), (22, 17), (22, 18), (22, 19)):
        f.put(x, y, 'T')
    for x, y in ((28, 14), (28, 15), (29, 16), (29, 17), (29, 18), (29, 19)):
        f.put(x, y, 'T')
    f.vline(25, 14, 18, 'd')                     # back leg (receding, darker)
    f.vline(26, 14, 18, 'T')
    f.hline(21, 30, 13, 'T')                     # the ledge, lit from the left
    f.hline(21, 23, 13, 't')
    f.vline(25, 3, 4, 't')                       # mast + clamp above the canvas
    f.vline(26, 3, 4, 'T')
    _paint(f, _CANVAS, *_CANVAS_AT)
    return f


# The picture, element by element.  Each element builds up in stages along its brush strokes (cells per
# stage, cumulative); _AIM is where the brush tip is when that stage appears.
def _cells(rows, x0, y0):
    return [(x0 + i, y0 + j, ch) for j, r in enumerate(rows) for i, ch in enumerate(r) if ch != '.']


def _rows(ch, ys, xs):
    return [(x, y, ch) for y in ys for x in xs]


_TOP, _LOW = (6, 7), (8, 9)
_PIC = {
    'sky': [_rows('c', _TOP, range(23, 26)), _rows('c', _TOP, range(23, 29)),
            _rows('c', _TOP + _LOW, range(23, 29))],
    'sun': [_cells(['y', 'y'], 27, 6), _cells(['yy', 'yj'], 27, 6)],
    'hill': [_rows('g', (11,), range(23, 26)), _rows('g', (11,), range(23, 29)),
             _rows('g', (10, 11), range(23, 29)),
             _rows('g', (10, 11), range(23, 29)) + _rows('g', (9,), range(26, 28))],
    'tree': [_cells(['G'], 24, 7), _cells(['.G.', 'GGG'], 23, 7), _cells(['.G.', 'GGG', '.T.', '.T.'], 23, 7)],
    'dot': [_cells(['G'], 26, 7)],                # the final touch: a little bird far off in the sky
}
_AIM = {
    'sky': [(25, 7), (28, 7), (23, 9)],
    'sun': [(27, 7), (28, 6)],
    'hill': [(25, 11), (28, 11), (23, 10), (27, 9)],
    'tree': [(24, 7), (24, 8), (24, 10)],
    'dot': [(26, 7)],
}
_ORDER = ('sky', 'sun', 'hill', 'tree', 'dot')
_PIC_LAYERS = {'sky': ('sky', 'sun'), 'land': ('hill', 'tree', 'dot')}   # drawn together: fewer frames

# Palette: kidney-shaped tan board with three dabs (sky, sun, hill; the dark green is mixed) and a mixing spot at the
# right end, where the brush dips.  It swings in front of him to dip (through a plain in-between).
_PALETTE = ['.tttttt.', 'tcygtttt', '.tttttt.']
_PAL_SWING = ['.tttttt.', 'ttttttTT', '..tttTT.']
_PAL_AT = {'side': (2, 14), 'mid': (6, 15), 'front': (11, 16)}
_MIX = (17, 17)                                  # the mixing spot when the palette is in front

# While it dips (right arm 'front'), the brush points down-left through his claw: the handle sticks up
# beside his shoulder, the tip goes into the mixing spot on the palette.
_DIP = [(21, 13, 'r'), (20, 14, 'r'), (18, 16, 'r')]       # + his claw at (19, 15) + the tip on _MIX

# His little red beret, worn slouched to the right (one row over his head-top).
_BERET = ['....R...', '.rrrrrr.', 'rrrrrrrR']
_BERET_AT = (12, 10)

# Right-arm poses the brush can work from, and where his claw grips it (at HOME).
_REACH = ('side', 'out', 'up', 'raise', 'wave', 'point')
_GRIP = {p: clawd(rarm=p).at('hand_r') for p in _REACH + ('front',)}


def _arm_for(tip, prefer):
    """The arm pose that holds the brush at a comfortable length (4-5 cells) for this tip; staying in
    the current pose when it can (the brush pivots in his claw instead of the arm jumping)."""
    best = None
    for p in _REACH:
        gx, gy = _GRIP[p]
        if tip[0] - gx < 1 or gy - tip[1] < 1:
            continue
        n = max(tip[0] - gx, gy - tip[1])
        score = abs(n - 4.5) + (0 if p == prefer else 0.75)
        if best is None or score < best[0]:
            best = (score, p)
    assert best, tip
    return best[1]


def _brush(f, grip, tip, colour):
    """Red handle from his claw to the paint-loaded tip (Bresenham, so the diagonals step cleanly)."""
    for (x, y) in _line_cells(grip, tip)[:-1]:
        f.put(x, y, 'r')
    f.put(tip[0], tip[1], colour)


def _line_cells(a, b):
    x0, y0 = a
    x1, y1 = b
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err, out = dx + dy, []
    while True:
        out.append((x0, y0))
        if (x0, y0) == (x1, y1):
            return out
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


# A fresh canvas lowered onto the easel: its top row per step (easing out as his claw takes it), a
# landing, a one-row bounce, settled.
_DROP = [-2, 3, 5, 4, 5]
_DROP_MS = [140, 150, 160, 100, 220]
_DROP_ARM = ['raise', 'wave', 'wave', 'wave', 'wave']
_FRESH = [r.replace('T', 't') for r in _CANVAS]  # (one wood tone: lighter in bytes, same read in motion)


# ---------------------------------------------------------------------------------------------- timeline
class _TL:
    """Beat list: (ms, state); every synced layer is cut from it, so nothing ever drifts."""

    def __init__(self):
        self.segs = []
        self.st = dict(expr='open', look='r', dx=0, legs='stand', larm='side', pal='side', rarm='side',
                       aim=(23, 11), tip='g', pic={'sky': 3, 'sun': 2, 'hill': 0, 'tree': 0, 'dot': 0},
                       drop=None, fx=None)

    def add(self, ms, pic=None, **kw):
        self.st.update(kw)
        if isinstance(kw.get('aim'), tuple) and 'rarm' not in kw:
            self.st['rarm'] = _arm_for(kw['aim'], self.st['rarm'])
        if pic:
            self.st['pic'] = dict(self.st['pic'], **pic)
        s = dict(self.st)
        s['pic'] = dict(self.st['pic'])
        self.segs.append((int(ms), s))

    def blink(self, slow=False):
        self.add(70 if slow else 60, expr='half')
        self.add(150 if slow else 90, expr='line')
        self.add(70 if slow else 60, expr='half')
        self.st['expr'] = 'open'

    def stroke(self, name, stages, ms):
        """The brush tip travels along the stroke and the paint appears behind it, stage by stage."""
        for k, d in zip(stages, ms):
            self.add(d, aim=_AIM[name][k - 1], pic={name: k})

    def dab(self, colour, then, look=True):
        """His eyes go to the palette (or stay on the canvas: he knows his palette), it swings in front
        of him through an in-between, the brush dips into the mixing spot and takes the colour; then the
        palette swings back out while the brush goes to `then` (a tip position, not painting yet)."""
        if look:
            self.add(160, look='d')
        self.add(100, larm='down', pal='mid')
        self.add(340 if look else 380, larm='front', pal='front', rarm='front', aim='dip', tip=colour)
        self.add(100, larm='down', pal='mid', aim=then, look='r')
        self.add(120, larm='side', pal='side')


def _timeline():
    t = _TL()
    # frame 0: the green tip on the canvas's bottom-left corner: about to sweep in the hill
    t.add(520)
    t.stroke('hill', [1, 2], [120, 150])                            # along the bottom, left to right
    t.stroke('hill', [3], [170])                                    # back along the next row
    t.stroke('hill', [4], [190])                                    # the hilltop
    t.add(260, aim=None, rarm='side')
    t.add(340)
    t.blink()
    t.add(260)
    t.add(500, look='c')
    t.add(220, look='ur')                                           # eyes on the sky: a tree, there
    # the tree: dark green, the crown up high, then the trunk down onto the hill
    t.dab('G', (25, 6), look=False)
    t.stroke('tree', [1, 2], [170, 160])
    t.stroke('tree', [3], [200])
    t.add(240, aim=None, rarm='side')
    # STEP BACK to judge it: two steps back (legs swing, the palette and beret go with him), then the
    # painter's measure: the brush held up at arm's length, lids half down, eyes running over the picture
    t.add(140, dx=-1, legs='walk_a')
    t.add(220, dx=-2, legs='stand')
    t.add(160, rarm='out', aim='vert')
    t.add(90, expr='half')
    t.add(560)
    t.add(320, look='ur')
    t.add(300, look='r')
    t.add(90, expr='open')
    t.add(260)                                                      # ... one more thing
    t.add(150, rarm='side', aim=None)
    t.add(140, dx=-1, legs='walk_b')
    t.add(220, dx=0, legs='stand')
    # the final dot, same dark green: a little bird far off in the sky (the brush comes in, touches, lifts)
    t.add(200, look='ur', aim=(25, 8))
    t.add(220, aim=(26, 7), pic={'dot': 1})
    t.add(160, aim=(25, 8))
    t.add(220, aim=None, rarm='side')
    # reward: sparkle eyes, a gold twinkle grows and fades on the canvas, a pleased look at you
    t.add(160, expr='sparkle', fx=0)
    t.add(110, fx=1)
    t.add(160, fx=2)
    t.add(130, fx=3)
    t.add(110, fx=0)
    t.add(300, fx=None)
    t.add(90, expr='half')
    t.add(520, expr='open', look='c')
    t.blink(slow=True)
    t.add(240)
    # a fresh canvas: his eyes go up first, it comes down from above, his claw rises to meet its edge and
    # guides it down onto the ledge in front of the finished painting; it lands, bounces a row, settles
    t.add(240, look='u')
    landed = False
    for i, (y, ms, arm) in enumerate(zip(_DROP, _DROP_MS, _DROP_ARM)):
        kw = dict(drop=y, rarm=arm, aim='vert' if arm != 'side' else None, look='ur' if i > 1 else 'u')
        if y == _CANVAS_AT[1] and not landed:                      # landed: the old painting is hidden
            kw['pic'] = {'sky': 0, 'sun': 0, 'hill': 0, 'tree': 0, 'dot': 0}
            landed = True
        t.add(ms, **kw)
    t.add(200, drop=None)
    t.add(160, rarm='side', aim=None, look='r')
    t.add(260)
    # sky: cyan, two sweeps high up (left to right, then back along the next rows)
    t.dab('c', (23, 7), look=True)
    t.stroke('sky', [1, 2], [130, 160])
    t.stroke('sky', [3], [190])
    t.add(240)
    t.blink()
    t.add(320)
    t.add(200, look='ur')                                           # eyes to the top corner first
    # sun: two dabs in the top corner
    t.dab('y', (26, 6), look=False)
    t.stroke('sun', [1, 2], [190, 200])
    t.add(140, aim=(26, 6))
    t.add(520, look='r')
    # green on the brush; it goes to the canvas's bottom-left corner .. frame 0
    t.dab('g', (23, 11), look=False)
    t.add(260)
    return t


# ---------------------------------------------------------------------------------------------- frames
_HX, _HY = HOME


def _pose(s):
    """His body with a solid face (the fine face layer draws his eyes)."""
    return clawd(eyes='blink', larm=s['larm'], rarm=s['rarm'], legs=s['legs'])


def _body_frame(s, beret=False):
    """The cells every arm pose shares (body + legs), wherever he stands, and his beret (nothing ever
    passes in front of his head)."""
    f = Frame()
    put_clawd(f, clawd(eyes='blink', larm='none', rarm='none', legs=s['legs']), _HX + s['dx'], _HY)
    if beret:
        _paint(f, _BERET, _BERET_AT[0] + s['dx'], _BERET_AT[1])
    return f


def _arm_cells(s, side):
    """One arm: the pose with only that arm, minus the body layer's cells."""
    p = clawd(eyes='blink', legs=s['legs'], larm=s['larm'] if side == 'l' else 'none',
              rarm=s['rarm'] if side == 'r' else 'none')
    f = Frame()
    put_clawd(f, p, _HX + s['dx'], _HY)
    still = _body_frame(s).px
    for c in [c for c, v in f.px.items() if still.get(c) == v]:
        del f.px[c]
    return f, p


def _rarm_frame(s):
    """His right arm and the brush in his claw (painting, resting, upright, or dipping into the
    palette's mixing spot)."""
    f, p = _arm_cells(s, 'r')
    gx, gy = p.at('hand_r', _HX + s['dx'], _HY)
    aim = s['aim']
    if aim == 'dip':
        for x, y, ch in _DIP:
            f.put(x + s['dx'], y, ch)
        f.put(_MIX[0] + s['dx'], _MIX[1], s['tip'])
    elif aim == 'vert':                           # held upright: measuring, or guiding the canvas edge
        for i, ch in enumerate(('r', 'r', 'r', s['tip'])):
            f.put(gx, gy - i, ch)
    else:
        if aim is None:                           # lifted off the canvas, resting
            aim = (gx + 3, gy - 3)
        _brush(f, (gx, gy), aim, s['tip'])
    return f


def _larm_frame(s):
    """His left arm and the palette: at his side, swinging past him (plain in-between), or in front of
    him for the brush to dip."""
    f, _ = _arm_cells(s, 'l')
    x, y = _PAL_AT[s['pal']]
    _paint(f, _PAL_SWING if s['pal'] == 'mid' else _PALETTE, x + s['dx'], y)
    return f


def _pic_frame(s, names):
    f = Frame()
    for name in names:
        k = s['pic'][name]
        if k:
            for x, y, ch in _PIC[name][k - 1]:
                f.put(x, y, ch)
    return f


def _fresh_frame(s):
    f = Frame()
    if s['drop'] is not None:
        y = s['drop']
        _paint(f, (_CANVAS if y == _CANVAS_AT[1] else _FRESH)[max(0, -y):], _CANVAS_AT[0], max(0, y))
    return f


_GAZE = {'c': (0, 0), 'r': (1, 0), 'l': (-1, 0), 'u': (0, -1), 'd': (0, 1), 'ur': (1, -1)}


def _face_frame(s):
    """His eyes as a fine (half-size pixel) overlay on his solid face: the kit's fine_face expression,
    shifted by the half-step gaze.  Guard: every eye pixel lies on his face."""
    p = _pose(s)
    x0 = _HX + s['dx']
    f = Frame()
    put_clawd(f, p, x0, _HY)
    base = fine(f)
    ff = fine_face(base.copy(), p, x0, _HY, expr=s['expr'])
    dx, dy = _GAZE[s['look']]
    ink = {(x + dx, y + dy): v for (x, y), v in ff.px.items() if base.px.get((x, y)) != v and v in 'kW'}
    for (x, y) in ink:
        if base.px.get((x, y)) != '#':
            raise ValueError('eye pixel (%d,%d) is off his face: %r' % (x, y, s))
    g = Frame(ink, res=2)
    g.meta = {'fine_face': [(s['expr'], s['expr'])]}
    return g


_SPARK = get('sparkle')


def _fx_frame(s):
    f = Frame()
    if s['fx'] is not None:
        f.place(_SPARK.sprite(s['fx']), 28, 6)
    return f


def build():
    t = _timeline()
    total = sum(ms for ms, _ in t.segs)
    names = list(_PIC_LAYERS) + ['fresh', 'body', 'larm', 'rarm', 'face', 'fx']
    tracks = {k: [] for k in names}
    for ms, s in t.segs:
        for k, parts in _PIC_LAYERS.items():
            tracks[k].append((_pic_frame(s, parts), ms))
        tracks['fresh'].append((_fresh_frame(s), ms))
        tracks['body'].append((_body_frame(s, beret=True), ms))
        tracks['larm'].append((_larm_frame(s), ms))
        tracks['rarm'].append((_rarm_frame(s), ms))
        tracks['face'].append((_face_frame(s), ms))
        tracks['fx'].append((_fx_frame(s), ms))
    for k, v in tracks.items():
        assert total_ms(v) == total, k
    first, last = t.segs[0][1], t.segs[-1][1]
    for key in ('pic', 'tip', 'larm', 'rarm', 'pal', 'aim', 'drop', 'dx', 'legs', 'look', 'expr'):
        assert first[key] == last[key], 'not seamless: %s %r %r' % (key, first[key], last[key])
    layers = [static('easel', _easel())]
    layers += [layer(k, tracks[k]) for k in names]
    return anim(NAME, DESC, layers, state=STATE)
