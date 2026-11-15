"""working-knit - Working variant: Clawd knits little striped scarves.   Preview:  python3 gen/preview.py anim working-knit

Storyboard (one 17.2 s timeline drives every synced layer; _timeline() has the exact beats):
     0  frame 0: at HOME, his right claw holds the knitting up beside him: needle A level with the newest
        row of stitches (yarn loops) along it and a red knob at its end, the working needle B crossing it
        up to the right (red knob high), a little striped scarf hanging from it (blue, blue, orange,
        orange from the fringed bottom up).  A strand rises from a ball of two-tone yarn on the ground at
        his right into the work; his knitting basket (handle, a finished scarf folded inside) stands at
        his left.  Eyes on the work.
        ROW: two or three stitches, each B's tip dipping into the loops (click) and coming back out, at
        an uneven pace; then the row is done: the scarf grows one row (stripes and fringe step down) and
        the strand pulls taut, then slackens.
        STRIPE: his eyes go to the ball first, then it turns over in four eased steps (the new colour
        comes up on top) and the strand changes colour; eyes back on the work.
  0.5   STRIPE (blue), ROW: the scarf is finished, five rows, fringe just above the ground; a double blink.
  3.5   CHECK, the reward: eyes up first, then he lifts it beside his head (an in-between on the way up
        and down), sparkle eyes, a gold twinkle grows, turns and fades as it runs down the stripes.
  5.6   CAST OFF + HAND-OFF: B slips the last loops off, the scarf folds up from the bottom in two steps
        into a bundle; he looks at the basket first, dips his claw (wind-up), swings it up and lets go:
        the bundle floats over his head on a slow arc (it hangs at the top) and sinks into the basket
        behind its rim; a soft tan puff fades out.  A slow blink.
  9.3   CAST ON: B winds new loops onto the bare needle (two, then four), the first blue row drops with
        its fringe; ROW (blue); STRIPE (orange, the ball turns back); ROW; a glance at you and a blink;
        ROW ... frame 0.
Seamless: every loop knits one whole scarf (blue, blue, orange, orange, blue), hands it off and comes
back to frame 0's four rows with orange running; the ball turns over and back once per loop.  Blinks are
uneven (a double at 2.6 s, a slow one at 8.4 s, a single at 14.6 s).
Face: fine-line (STYLE 0b) eyes in their own fine layer over a solid face: open, half, line, look_*,
sparkle only.  Normal body size throughout; his arms, eyes and the props do the acting.
Layers (back to front): basket (static back: handle, folded scarf) | ball | strand | scarf (stitches on
needle A, the hanging work, the folded scarf in his claw / in flight) | rim (static basket front, so the
scarf sinks in) | clawd (+ the needles in his claw) | click (B's tip) | face (fine) | fx.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'working-knit'
STATE = 'working (variant)'
DESC = ('Cozy Clawd knits little blue-and-orange striped scarves: the needles click, the yarn ball tugs and '
        'rolls, the scarf grows row by row, he holds it up to admire it, then folds it into his basket and '
        'casts on the next one.')


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


# ---------------------------------------------------------------------------------------------- props
# His knitting basket on the left: the back (wood handle, the finished scarf folded on top, the rim
# posts) and the front (tan rim, woven wood) in separate static layers, so a tossed scarf can sink in.
_BASKET_BACK = [
    '..TTTT..',
    '.T....T.',
    'tbboobbt',
]
_BASKET_FRONT = [
    'tttttttt',
    'TdTTdTTd',
    '.TdTTdT.',
]
_BASKET_AT = (1, 14)

# The yarn: one ball of two-tone (self-striping) yarn on the ground at his right.  The colour on top is
# the colour running off it; it turns over in four eased steps when the stripe changes and rocks a
# little when a row pulls on it.  Angle 0 = orange on top ... 4 = blue on top (lit top-left).
_BALL = [
    ['.oo.', 'oyoO', 'bbbB', '.BB.'],
    ['.oo.', 'oybB', 'obbB', '.BB.'],
    ['.ob.', 'oybB', 'oObB', '.OB.'],
    ['.bb.', 'oCbB', 'oobB', '.OO.'],
    ['.bb.', 'bCbB', 'oooO', '.OO.'],
]
_BALL_AT = (27, 16)
_STRAND = {False: [(28, 15), (27, 15), (26, 14)],      # slack: it sags along the ball's top first
           True: [(28, 15), (27, 14), (26, 14)]}       # taut: straight up into the work

# The work, relative to the grip (his hand_r point; 'lift' moves it one row lower for in-betweens).
# Needle A lies level along the scarf's top edge: in his claw at the left end, the newest row of stitches
# (yarn loops) along it, a red knob at the right end.  The working needle B crosses it up and to the
# right (red knob high); its tip clicks in and out of the stitches (its own tiny layer).
_A_ENDS = [(0, 0, 'm'), (5, 0, 'm'), (6, 0, 'r')]
_LOOPS = [(i, 0) for i in range(1, 5)]
_B = [(2, 1, 'm'), (3, 0, 'm'), (4, -1, 'm'), (5, -2, 'm'), (6, -3, 'r')]
_B_TIP = {'rest': (1, 2), 'in': (2, 2)}
_SCARF_DX, _SCARF_W = 1, 4                     # the scarf hangs from x grip+1 .. grip+4
_DARK = {'o': 'O', 'b': 'B'}
_ROWS = 'bboob'                                # one finished scarf, cast-on row first
_FRINGE = 'b.b.'                               # the cast-on edge's fringe (every scarf starts blue)
_BUNDLE = ['oooo', 'bBbB', 'b.b.']             # the finished scarf folded up, for the hand-off

# The hand-off: the folded scarf's top-left per step, from his raised claw up over his head and down
# into the basket (spacing tightens near the top of the arc: it floats, then drops in).
_TOSS = [(20, 8), (17, 5), (14, 3), (11, 3), (8, 5), (6, 8), (4, 12), (4, 14)]
_TOSS_MS = [90, 100, 130, 140, 110, 90, 100, 150]
_TOSS_LOOK = ['ur', 'u', 'u', 'ul', 'ul', 'l', 'dl', 'dl']
_PUFF = [[(1, 13), (8, 13), (2, 12), (7, 12)], [(1, 12), (8, 12)], [(0, 11), (9, 11)]]


# ---------------------------------------------------------------------------------------------- timeline
class _TL:
    """Beat list: (ms, state); every synced layer is cut from it, so nothing ever drifts."""

    def __init__(self):
        self.segs = []
        self.st = dict(expr='open', look='r', rarm='up', lift=0, b='rest', rows=4, fold=0, cast=4,
                       bundle=None, yarn='o', ball=0, taut=False, fx=None, puff=None)

    def add(self, ms, **kw):
        self.st.update(kw)
        self.segs.append((int(ms), dict(self.st)))

    def blink(self, slow=False):
        self.add(70 if slow else 60, expr='half')
        self.add(150 if slow else 90, expr='line')
        self.add(70 if slow else 60, expr='half')
        self.st['expr'] = 'open'

    def stitch(self, dip, out):
        self.add(dip, b='in')
        self.add(out, b='rest')

    def row(self, beats, pause=260):
        """A few stitches (B's tip dips in, clicks, comes back out), then the row is done: the scarf
        grows one row and the strand pulls taut, then slackens."""
        for dip, out in beats:
            self.stitch(dip, out)
        self.add(150, rows=self.st['rows'] + 1, taut=True)
        self.add(pause, taut=False)

    def stripe(self, new):
        """The yarn changes colour: his eyes go to the ball first, then it turns over in eased steps
        (new colour on top) and his eyes come back to the work."""
        self.add(260, look='dr')
        steps = [1, 2, 3, 4] if new == 'b' else [3, 2, 1, 0]
        for i, (a, ms) in enumerate(zip(steps, (90, 110, 130, 170))):
            self.add(ms, ball=a, taut=i < 2, yarn=new if i >= 2 else self.st['yarn'])
        self.add(160, taut=False)
        self.add(180, look='r')


def _timeline():
    t = _TL()
    # frame 0: the scarf four rows long (blue, blue, orange, orange), eyes on the work
    t.add(480)
    t.stripe('b')
    t.row([(170, 230), (160, 250)], pause=260)                      # row 5 (blue): finished
    t.blink()
    t.add(120)
    t.blink()
    t.add(200)
    # CHECK (the reward beat): eyes up first, then he lifts the finished scarf beside his head (an
    # in-between on the way up and down), sparkle eyes, a gold twinkle runs down the stripes
    t.add(150, look='ur')
    t.add(90, rarm='raise', lift=1)
    t.add(130, lift=0)
    t.add(160, expr='sparkle', fx=(0, 0))
    t.add(110, fx=(0, 1))
    t.add(130, fx=(1, 2))
    t.add(130, fx=(1, 1))
    t.add(120, fx=(2, 2))
    t.add(110, fx=(2, 1))
    t.add(100, fx=(2, 0))
    t.add(300, fx=None)
    t.add(90, expr='half')
    t.add(120, expr='open', look='r', lift=1)
    t.add(140, rarm='up', lift=0)
    t.add(260)
    # CAST OFF + HAND-OFF: B slips the last loops off, the scarf folds up from the bottom (two steps)
    # into a bundle; he looks at the basket first, dips his claw (wind-up), swings it up and lets go:
    # the bundle floats over his head on an arc and drops into the basket, a soft puff fades out
    t.add(150, b='in')
    t.add(120, fold=1, b='rest')
    t.add(120, fold=2)
    t.add(150, rows=0, fold=0, cast=0, bundle='held')
    t.add(300, look='l')
    t.add(150, rarm='side', look='dl')
    t.add(110, rarm='up', look='l')
    t.add(90, rarm='raise', look='ur')
    for i, (ms, look) in enumerate(zip(_TOSS_MS, _TOSS_LOOK)):
        t.add(ms, bundle=i, look=look, rarm='raise' if i < 2 else ('up' if i < 4 else t.st['rarm']))
    t.add(130, bundle=None, puff=0)
    t.add(130, puff=1)
    t.add(150, puff=2)
    t.add(200, puff=None)
    t.blink(slow=True)
    t.add(260, look='r')
    # CAST ON: B winds new loops onto the bare needle (two, then four), the first blue row drops with
    # its fringe; then one more row (blue)
    t.stitch(170, 190)
    t.add(130, cast=2)
    t.stitch(160, 200)
    t.add(130, cast=4)
    t.add(220, rows=1)
    t.add(200)
    t.row([(160, 230), (150, 220), (160, 240)], pause=300)          # row 2 (blue)
    # the yarn turns orange: rows 3 and 4, with a glance at you and a blink between them .. frame 0
    t.stripe('o')
    t.row([(170, 240), (160, 250)], pause=320)                      # row 3 (orange)
    t.add(480, look='c')
    t.blink()
    t.add(380)
    t.add(200, look='r')
    t.row([(150, 230), (160, 220), (150, 250)], pause=320)          # row 4 (orange)
    return t


# ---------------------------------------------------------------------------------------------- frames
def _pose(s):
    """His body with a solid face (the fine face layer draws his eyes)."""
    return clawd(eyes='blink', rarm=s['rarm'])


def _grip(s):
    gx, gy = _pose(s).at('hand_r')
    return gx, gy + s['lift']


def _clawd_frame(s):
    """Clawd and the needles in his claw (A's ends and B: they only move when his arm moves); the
    stitches on A belong to the work (scarf layer), B's clicking tip has its own layer."""
    f = Frame()
    put_clawd(f, _pose(s))
    gx, gy = _grip(s)
    for dx, dy, ch in _A_ENDS + _B:
        f.put(gx + dx, gy + dy, ch)
    return f


def _click_frame(s):
    f = Frame()
    gx, gy = _grip(s)
    dx, dy = _B_TIP[s['b']]
    f.put(gx + dx, gy + dy, 'm')
    return f


def _scarf_frame(s):
    """The work: the stitches on needle A (yarn loops in the newest row's colour, or bare needle), the
    rows hanging from it (newest on top, the cast-on row and its fringe at the bottom); while it folds
    up, its bottom edge rises; the folded bundle in his claw or in flight."""
    f = Frame()
    gx, gy = _grip(s)
    x0 = gx + _SCARF_DX
    n = s['rows']
    top = _ROWS[n - 1] if n else 'b'
    for i, (dx, dy) in enumerate(_LOOPS):
        if n or i < s['cast']:
            f.put(gx + dx, gy + dy, top if i % 2 == 0 else _DARK[top])
        else:
            f.put(gx + dx, gy + dy, 'm')
    if s['fold']:                                 # folding up: the underside shows along the bottom
        keep = n - 1 - s['fold']
        for j in range(keep):
            f.hline(x0, x0 + _SCARF_W - 1, gy + 1 + j, _ROWS[n - 1 - j])
        f.hline(x0, x0 + _SCARF_W - 1, gy + 1 + keep, 'B')
    else:
        for j in range(n):
            f.hline(x0, x0 + _SCARF_W - 1, gy + 1 + j, _ROWS[n - 1 - j])
        if n:
            _paint(f, [_FRINGE], x0, gy + 1 + n)
    b = s['bundle']
    if b == 'held':
        _paint(f, _BUNDLE, x0, gy + 1)
    elif b is not None:
        _paint(f, _BUNDLE, *_TOSS[b])
    return f


def _ball_frame(s):
    """The ball, current colour on top (it turns over in eased steps when the stripe changes)."""
    f = Frame()
    _paint(f, _BALL[s['ball']], *_BALL_AT)
    return f


def _strand_frame(s):
    """The strand from the ball up into the side of the work, beside needle A's end: slack it sags
    a cell, taut (a row pulling on it) it runs straight."""
    f = Frame()
    for x, y in _STRAND[s['taut']]:
        f.put(x, y, s['yarn'])
    return f


def _back_frame():
    f = Frame()
    _paint(f, _BASKET_BACK, *_BASKET_AT)
    return f


def _front_frame():
    f = Frame()
    _paint(f, _BASKET_FRONT, _BASKET_AT[0], _BASKET_AT[1] + len(_BASKET_BACK))
    return f


_GAZE = {'c': (0, 0), 'r': (1, 0), 'l': (-1, 0), 'u': (0, -1), 'd': (0, 1), 'ur': (1, -1),
         'ul': (-1, -1), 'dl': (-1, 1), 'dr': (1, 1)}


def _face_frame(s):
    """His eyes as a fine (half-size pixel) overlay on his solid face: the kit's fine_face expression,
    shifted by the half-step gaze.  Guard: every eye pixel lies on his face."""
    p = _pose(s)
    f = Frame()
    put_clawd(f, p)
    base = fine(f)
    ff = fine_face(base.copy(), p, expr=s['expr'])
    dx, dy = _GAZE[s['look']]
    ink = {(x + dx, y + dy): v for (x, y), v in ff.px.items() if base.px.get((x, y)) != v and v in 'kW'}
    for (x, y) in ink:
        if base.px.get((x, y)) != '#':
            raise ValueError('eye pixel (%d,%d) is off his face: %r' % (x, y, s))
    g = Frame(ink, res=2)
    g.meta = {'fine_face': [(s['expr'], s['expr'])]}
    return g


_SPARK = get('sparkle_small')


def _fx_frame(s):
    """The twinkle running down the finished scarf while he admires it (it grows, turns and fades as it
    goes), and the soft puff where the scarf drops into the basket (fading out)."""
    f = Frame()
    if s['fx'] is not None:
        step, i = s['fx']
        gx, gy = _grip(s)
        f.place(_SPARK.sprite(i), gx + 3 - step, gy + 2 + step)
    if s['puff'] is not None:
        for x, y in _PUFF[s['puff']]:
            f.put(x, y, 't')
    return f


def build():
    t = _timeline()
    total = sum(ms for ms, _ in t.segs)
    tracks = {k: [] for k in ('ball', 'strand', 'scarf', 'clawd', 'click', 'face', 'fx')}
    for ms, s in t.segs:
        tracks['ball'].append((_ball_frame(s), ms))
        tracks['strand'].append((_strand_frame(s), ms))
        tracks['scarf'].append((_scarf_frame(s), ms))
        tracks['clawd'].append((_clawd_frame(s), ms))
        tracks['click'].append((_click_frame(s), ms))
        tracks['face'].append((_face_frame(s), ms))
        tracks['fx'].append((_fx_frame(s), ms))
    for k, v in tracks.items():
        assert total_ms(v) == total, k
    first, last = t.segs[0][1], t.segs[-1][1]
    for key in ('rows', 'yarn', 'ball', 'rarm', 'lift', 'b', 'cast', 'look', 'expr'):
        assert first[key] == last[key], 'not seamless: %s' % key
    layers = [static('basket', _back_frame())]
    layers += [layer(k, tracks[k]) for k in ('ball', 'strand', 'scarf')]
    layers += [static('rim', _front_frame())]
    layers += [layer(k, tracks[k]) for k in ('clawd', 'click', 'face', 'fx')]
    return anim(NAME, DESC, layers, state=STATE)
