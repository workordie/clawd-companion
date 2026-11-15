"""working-mail - Working variant: Clawd sorts the mail.   Preview:  python3 gen/preview.py anim working-mail

Storyboard (one 17.4 s timeline drives every synced layer; _timeline() has the exact beats):
     0  frame 0: at HOME, a blue envelope held low in front of him in his left claw, a rubber stamp
        raised in his right, eyes down on the letter.  On the wall at his right hangs a wooden
        pigeonhole rack, 3 x 2 slots, each holding letters of one colour (red, blue, green / gold,
        violet, pink); a parcel crate stands under it.  At his left a steel mail chute comes down from
        the top, over a wire tray with a stack of envelopes (green, gold, violet).
        STAMP: wind-up (the stamp cocks a row higher), THUNK on the envelope's corner (the letter gives
        a row under the blow, two yellow sparks), a beat pressed down (one spark, fading), pulled back up:
        a red stamp is on the corner now.
  0.9   FLICK: eyes to the rack first, the letter dips in his claw (wind-up), an underhand flick: it
        sails up over his head on an arc, slowing at the top, into the blue slot; the slot's edge
        flashes blue, dims to navy, gone.  A look at you, a blink.
  3.3   NEXT: eyes to the tray first, his claw takes the top letter (violet), holds it up to read the
        address, brings it down in front of him (through an in-between); STAMP, FLICK: violet slot.
  6.4   PARCEL: his eyes go up, the parcel peeks out of the chute's mouth, drops onto the tray, bounces
        a row and settles (a tan dust puff fades).  He takes it, it lags behind his claw on the way in
        front of him and catches up; he tapes it shut in two pulls, glances at the crate, raises it
        beside his head and lobs it over into the crate (a puff that fades).  A slow blink.
 10.7   A red letter drops in (peek, fall, it flops flat and bounces a row): read, STAMP, FLICK: red slot.
 14.8   Two letters drop in one behind the other (violet, then blue on top), each flopping flat with a
        bounce; a blink; he takes the blue one, reads it, brings it down in front of him: frame 0.
Seamless: the tray holds green, gold, violet again and a blue letter is in his claw, as in frame 0.
Three letters filed and one parcel per loop; blinks at 2.9, 10.3 and 15.6 s.
Face: fine-line (STYLE 0b) eyes in their own fine layer over a solid face: open, half, line, look_*
only.  Normal body size throughout.
Layers (back to front): scene (static: rack with its letters, chute, tray) | stack | clawd (static: the
cells every pose shares) | larm (left arm + what it holds) | rarm (right arm + the stamp) | props (items
dropping from the chute, flicked letters, the lobbed parcel, sparks, flashes, puffs: one layer, since
they rarely overlap in time) | crate (static: a lobbed parcel drops in behind it) | face (fine).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'working-mail'
STATE = 'working (variant)'
DESC = ('Clawd sorts the mail: he takes colourful letters from the tray under a mail chute, reads each one, '
        'thunks a stamp on it and flicks it into the pigeonhole of its colour; now and then a parcel drops '
        'in, which he tapes shut and lobs into the crate.')


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


# ---------------------------------------------------------------------------------------------- props
# The pigeonhole rack, hung on the wall at his right: tan dividers lit from the left, shaded right and
# bottom; each slot shows the dark inside and, below it, the edges of the letters filed there.
_RACK = [
    'tttttttttT',
    'tddtddtddT',
    'trrtbbtggT',
    'tTTTTTTTTT',
    'tddtddtddT',
    'tjjtvvtppT',
    'TTTTTTTTTT',
]
_RACK_AT = (21, 3)
_SLOT = {'r': (22, 4), 'b': (25, 4), 'g': (28, 4), 'j': (22, 7), 'v': (25, 7), 'p': (28, 7)}   # opening

# The parcel crate on the floor under the rack (front face; a lobbed parcel drops in behind it).
_CRATE = [
    'tttttt',
    'TdTTdT',
    'TTTTTT',
    'dTTTTd',
]
_CRATE_AT = (24, 16)

# The mail chute from the top at his left (steel tube, dark inside, flared mouth), over a wire tray.
_CHUTE = [
    '.snnns.',
    '.snnns.',
    '.snnns.',
    '.snnns.',
    '.snnns.',
    'm.....m',
]
_CHUTE_AT = (2, 0)
_TRAY = ['s.....s', 'smmmmms']
_TRAY_AT = (2, 18)
_STACK_X, _STACK_Y = 3, 18            # envelopes lie in the tray edge-on: one 5-cell row each, upward
_PEEK_Y = 5                           # just under the chute's mouth

# Envelopes: 5 x 3 in their colour with a wide darker V flap; a red stamp on the corner once stamped.
_FLAP = {'r': 'R', 'b': 'B', 'g': 'G', 'j': 'J', 'v': 'V', 'p': 'r'}


def _envelope(c, stamped=False):
    d = _FLAP[c]
    rows = [d + c * 3 + d, c + d * 3 + c, c * 5]
    if stamped:
        rows[0] = rows[0][:4] + ('y' if c in 'rp' else 'r')
    return rows


_PARCEL = ['tttT', 'TTTd', 'TTTd']
_TAPE = [None, ['....', 'rr..'], ['....', 'rrrr']]   # red tape pulled round its middle, in two pulls
_FLY = {c: [_FLAP[c] + c + _FLAP[c], c * 3] for c in _FLAP}     # a letter in flight (3 x 2)

# Where his left claw holds a letter or the parcel (top-left), per arm pose.
_HELD_AT = {'out': (4, 13), 'up': (5, 10), 'front': (12, 16)}

# His rubber stamp (wood handle, red rubber), per right-arm pose; 'cock' = raised a row higher in
# his claw, the wind-up before the THUNK.
_STAMP = {
    'side': [(22, 14, 'T'), (22, 15, 'T'), (21, 16, 'R'), (22, 16, 'R'), (23, 16, 'R')],
    'up':   [(22, 12, 'T'), (22, 13, 'T'), (21, 14, 'R'), (22, 14, 'R'), (23, 14, 'R')],
    'cock': [(22, 11, 'T'), (22, 12, 'T'), (21, 13, 'R'), (22, 13, 'R'), (23, 13, 'R')],
    'chin': [(16, 15, 'T'), (16, 16, 'R')],     # THUNK on the corner of the letter in front of him
}


def _arc(x0, y0, x1, y1, n=5, g=1.0):
    """n+1 integer points from (x0, y0) to (x1, y1) on a thrown arc (y grows down)."""
    vx = (x1 - x0) / float(n)
    vy = (y1 - y0 - g * n * (n - 1) / 2.0) / n
    return [(int(round(x0 + vx * i)), int(round(y0 + vy * i + g * i * (i - 1) / 2.0))) for i in range(n + 1)]


# ---------------------------------------------------------------------------------------------- timeline
class _TL:
    """Beat list: (ms, state); every synced layer is cut from it, so nothing ever drifts."""

    def __init__(self):
        self.segs = []
        self.st = dict(expr='open', look='d', larm='front', rarm='up', stamp='up', held=('b', False),
                       hdy=0, hdx=0, tape=0, stack=['g', 'j', 'v'], fall=None, fly=None, fx=None, peek=None)

    def add(self, ms, **kw):
        self.st.update(kw)
        s = dict(self.st)
        s['stack'] = list(self.st['stack'])
        self.segs.append((int(ms), s))

    def blink(self, slow=False):
        self.add(70 if slow else 60, expr='half')
        self.add(150 if slow else 90, expr='line')
        self.add(70 if slow else 60, expr='half')
        self.st['expr'] = 'open'

    def stamp(self):
        """Wind-up (the stamp cocked a row higher), THUNK on the letter's corner (the letter gives a row
        under the blow, impact ticks), a beat pressed down (ticks fading), then pulled back up."""
        c, _ = self.st['held']
        self.add(150, rarm='up', stamp='cock')
        self.add(100, rarm='chin', stamp='chin', held=(c, True), hdy=1, fx=('thunk', 0))
        self.add(110, hdy=0, fx=('thunk', 1))
        self.add(150, rarm='up', stamp='up', fx=None)            # pulled back up off the letter
        self.add(200)

    def toss(self, c, pause=150):
        """Eyes to the slot first; the letter dips in his claw (wind-up), then an underhand flick: it
        sails up over his head on an arc (slowing at the top) into the slot of its colour; the slot's edge
        flashes in its colour, dims and is gone."""
        tx, ty = _SLOT[c]
        path = _arc(14, 16, tx + 1, ty, n=5, g=1.5)
        self.add(260, look='ur')
        self.add(140, hdy=1)
        self.add(90, larm='up', held=None, hdy=0, fly=(c, path[1]))
        for i, p in enumerate(path[2:-1]):
            self.add((110, 130, 120)[i], fly=(c, p))
        self.add(130, fly=None, larm='side', fx=('slot', c, 0))
        self.add(120, fx=('slot', c, 1))
        self.add(pause, fx=None)

    def pick(self, read=420):
        """Eyes to the tray first, then the claw goes to it, takes the top letter and lifts it up to read
        the address, and brings it down in front of him (through an in-between)."""
        c = self.st['stack'][-1]
        self.add(220, look='l')
        self.add(200, larm='out', held=(c, False), stack=self.st['stack'][:-1])
        self.add(read, larm='up', look='l')
        self.add(90, larm='out', look='d')
        self.add(190, larm='front')

    def drop(self, item, look=True):
        """The chute rattles: the item peeks out of its mouth (his eyes go up to it), drops onto the
        tray (a letter flops flat; the parcel lands on its base), bounces a row and settles."""
        if look:
            self.add(150, look='u')
        self.add(170, peek=item)
        top = _STACK_Y - sum(3 if c == 'P' else 1 for c in self.st['stack'])
        if item == 'P':
            self.add(110, peek=None, fall=(item, 'box', 7))
            self.add(100, fall=(item, 'box', top - 2), look='l')
            self.add(90, fall=(item, 'box', top - 3), fx=('dust', 0))
            self.add(120, fall=None, stack=self.st['stack'] + [item], fx=('dust', 1))
            self.add(130, fx=None)
        else:
            self.add(110, peek=None, fall=(item, 'face', 8), look='l')
            self.add(100, fall=(item, 'flat', top - 1))             # lands flat, bounces a row ...
            self.add(130, fall=None, stack=self.st['stack'] + [item])   # ... and settles


def _drop2(self, a, b):
    """Two letters at once: the first peeks out and falls, the second right behind it; each flops flat
    onto the tray with a little bounce."""
    top = _STACK_Y - sum(3 if c == 'P' else 1 for c in self.st['stack'])
    self.add(150, look='u')
    self.add(170, peek=a)
    self.add(110, peek=b, fall=(a, 'face', 8), look='l')
    self.add(100, peek=None, fall=[(a, 'flat', top - 1), (b, 'face', 8)])
    self.add(110, fall=(b, 'flat', top - 2), stack=self.st['stack'] + [a])
    self.add(130, fall=None, stack=self.st['stack'] + [b])


_TL.drop2 = _drop2


def _timeline():
    t = _TL()
    # frame 0: a blue letter in front of him, the stamp raised, eyes on the letter
    t.add(440)
    t.stamp()
    t.toss('b')
    t.add(380, look='c')
    t.blink()
    t.add(260)
    # the violet letter on top of the tray
    t.pick(read=460)
    t.stamp()
    t.toss('v', pause=200)
    # the chute drops a parcel: he takes it, tapes it shut in two pulls, raises it beside his head and
    # lobs it over into the crate (a tan puff that fades)
    t.drop('P')
    t.add(200, look='l')
    t.add(200, larm='out', held=('P', False), stack=t.st['stack'][:-1])
    t.add(100, larm='front', hdx=-3, look='d')              # the heavy parcel lags behind his claw ...
    t.add(200, hdx=0)                                        # ... and catches up
    t.add(150, rarm='chin', stamp='chin', tape=1)
    t.add(170, rarm='side', stamp='side', tape=2)
    t.add(260)
    t.add(240, look='r')
    t.add(200, larm='up', look='ur')                         # up beside his head, aiming ...
    path = _arc(7, 10, 26, 15, n=5, g=1.6)                   # ... and lobbed over it into the crate
    t.add(90, larm='side', held=None, tape=0, fly=('P', path[1]))
    for i, p in enumerate(path[2:]):
        t.add((110, 130, 100, 90)[i], fly=('P', p), look='ur')
    t.add(130, fly=None, fx=('puff', 0))
    t.add(130, fx=('puff', 1))
    t.add(140, fx=('puff', 2))
    t.add(200, fx=None, look='c')
    t.blink(slow=True)
    t.add(300)
    # a red letter drops in: read, stamp, toss
    t.drop('r')
    t.add(180)
    t.pick(read=500)
    t.stamp()
    t.toss('r', pause=260)
    # two more drop in (violet, then blue on top); he takes the blue one, reads it, brings it down in
    # front of him and raises the stamp: frame 0
    t.drop2('v', 'b')
    t.add(160)
    t.blink()
    t.add(120)
    t.pick(read=440)
    t.add(200)
    return t


# ---------------------------------------------------------------------------------------------- frames
def _pose(s):
    """His body with a solid face (the fine face layer draws his eyes)."""
    return clawd(eyes='blink', larm=s['larm'], rarm=s['rarm'])


_STILL = clawd(eyes='blink', larm='none', rarm='none')     # the cells every pose shares (static layer)


def _body_frame():
    f = Frame()
    put_clawd(f, _STILL)
    return f


def _arm_frame(s, side):
    """One arm (the pose minus the static body), plus what that hand holds."""
    p = clawd(eyes='blink', larm=s['larm'] if side == 'l' else 'none', rarm=s['rarm'] if side == 'r' else 'none')
    f = Frame()
    put_clawd(f, p)
    still = _body_frame().px
    for c in [c for c, v in f.px.items() if still.get(c) == v]:
        del f.px[c]
    if side == 'l' and s['held'] is not None:
        c, stamped = s['held']
        x, y = _HELD_AT[s['larm']]
        x += s['hdx']                             # the parcel lagging behind his claw
        y += s['hdy']                             # it gives a row under the stamp / dips for the flick
        if c == 'P':
            _paint(f, _PARCEL, x, y)
            if s['tape']:
                _paint(f, _TAPE[s['tape']], x, y)
        else:
            _paint(f, _envelope(c, stamped), x, y)
    if side == 'r':
        for x, y, ch in _STAMP[s['stamp']]:
            f.put(x, y, ch)
    return f


def _stack_frame(s):
    f = Frame()
    y = _STACK_Y
    for c in s['stack']:
        if c == 'P':
            _paint(f, _PARCEL, _STACK_X, y - 2)
            y -= 3
        else:
            f.hline(_STACK_X, _STACK_X + 4, y, c)
            y -= 1
    return f


def _fall_frame(s):
    """Items dropping out of the chute: a letter face-on, then flat on the tray a row high (the bounce);
    the parcel upright.  Before one drops, its bottom edge peeks out of the chute's mouth."""
    f = Frame()
    if s['peek'] is not None:
        c = s['peek']
        if c == 'P':
            f.hline(_STACK_X + 1, _STACK_X + 3, _PEEK_Y, 'T')
        else:
            f.hline(_STACK_X + 1, _STACK_X + 3, _PEEK_Y, c)
    falls = s['fall'] if isinstance(s['fall'], list) else ([s['fall']] if s['fall'] else [])
    for item, how, y in falls:
        if how == 'box':
            _paint(f, _PARCEL, _STACK_X + 1, y)
        elif how == 'face':
            _paint(f, _envelope(item), _STACK_X, y)
        else:
            f.hline(_STACK_X, _STACK_X + 4, y, item)
    return f


def _fly_frame(s):
    f = Frame()
    if s['fly'] is not None:
        item, (x, y) = s['fly']
        _paint(f, _PARCEL if item == 'P' else _FLY[item], x - 1, y - 1)
    return f


def _scene():
    f = Frame()
    _paint(f, _RACK, *_RACK_AT)
    _paint(f, _CHUTE, *_CHUTE_AT)
    _paint(f, _TRAY, *_TRAY_AT)
    return f


def _crate():
    f = Frame()
    _paint(f, _CRATE, *_CRATE_AT)
    return f


_GAZE = {'c': (0, 0), 'r': (1, 0), 'l': (-1, 0), 'u': (0, -1), 'd': (0, 1), 'ur': (1, -1), 'ul': (-1, -1)}


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


_THUNK = [[(17, 16), (17, 18)], [(18, 17)]]   # little yellow impact sparks beside the letter's corner, fading
_PUFF = [[(23, 15), (30, 15), (24, 14), (29, 14)], [(23, 14), (30, 14)], [(22, 13), (31, 13)]]
_DUST = [[(2, 16), (8, 16), (2, 15), (8, 15)], [(1, 15), (9, 15)]]


def _fx_frame(s):
    f = Frame()
    fx = s['fx']
    if fx is None:
        return f
    kind = fx[0]
    if kind == 'thunk':
        for x, y in _THUNK[fx[1]]:
            f.put(x, y, 'y')
    elif kind == 'slot':                         # the letter pops into its slot: its edge flashes in
        c, k = fx[1], fx[2]                       # its colour, then dims to the flap colour, then gone
        x, y = _SLOT[c]
        f.hline(x, x + 1, y, c if k == 0 else _FLAP[c])
    elif kind == 'puff':                         # the parcel lands in the crate
        for x, y in _PUFF[fx[1]]:
            f.put(x, y, 't')
    elif kind == 'dust':                         # the parcel lands on the tray
        for x, y in _DUST[fx[1]]:
            f.put(x, y, 't')
    return f


def build():
    t = _timeline()
    total = sum(ms for ms, _ in t.segs)
    names = ('stack', 'larm', 'rarm', 'props', 'face')
    tracks = {k: [] for k in names}
    for ms, s in t.segs:
        tracks['stack'].append((_stack_frame(s), ms))
        tracks['larm'].append((_arm_frame(s, 'l'), ms))
        tracks['rarm'].append((_arm_frame(s, 'r'), ms))
        props = _fall_frame(s).over(_fly_frame(s)).over(_fx_frame(s))
        tracks['props'].append((props, ms))
        tracks['face'].append((_face_frame(s), ms))
    for k, v in tracks.items():
        assert total_ms(v) == total, k
    first, last = t.segs[0][1], t.segs[-1][1]
    for key in ('stack', 'held', 'larm', 'rarm', 'stamp', 'look', 'tape', 'hdy', 'expr'):
        assert first[key] == last[key], 'not seamless: %s %r %r' % (key, first[key], last[key])
    layers = [static('scene', _scene()), layer('stack', tracks['stack']), static('clawd', _body_frame())]
    layers += [layer(k, tracks[k]) for k in ('larm', 'rarm', 'props')]
    layers += [static('crate', _crate()), layer('face', tracks['face'])]
    return anim(NAME, DESC, layers, state=STATE)
