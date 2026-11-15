"""working-forge - Claude is running (working variant): Clawd the blacksmith.   Preview:  python3 gen/preview.py anim working-forge

STORYBOARD (one master beat list drives every synced layer, so nothing ever drifts; the master loop is
11.3 s, the pile cart runs over three of them)
     0  F0  Clawd at HOME, hammer raised high, eyes on a glowing yellow-orange curly brace '{' (a code
            bracket being forged) standing on the little anvil at his right. A water bucket stands under
            the anvil's horn at his right foot, a small brick furnace glows beyond the anvil, and at his
            left foot a little cart holds a finished steel bracket.
        A   SHAPE: a strike: a held aim, a wind-back over his head, a fast swing, the impact (a white-hot
            glint at the contact), sparks flying out on arcs and cooling, the hammer recoiling up; the
            glow cools from yellow toward orange. A blink.
        B   TURN IT OVER: a light tap and the piece hops, edge-on for a moment, and lands with a bounce.
        C   QUENCH: his eyes go to the bucket first; the hammer nudges the brace along the anvil and off the
            horn: it tips into the bucket, a splash grows and falls back, a puff of steam billows up and
            thins out while he lays the hammer on the anvil.
        D   ADMIRE: eyes down, his hand dips into the bucket, lifts out the cooled steel bracket (a drip
            falls back) and brings it up in front of his face; his left hand joins: he holds it with both
            hands, his eyes sparkle and a glint twinkles on the steel.
        E   ON THE PILE: he looks at the cart, his left hand carries the bracket over and drops it in at the
            near end; the brackets already there are nudged along: clink.
        F   NEXT PIECE: he looks back at the anvil, takes up the hammer; the furnace mouth flares and slides
            out the next white-hot bar onto the anvil (it settles with a bounce); two strikes (a blink
            between them) bend it into a brace ... hammer raised again = frame 0 (seamless).
PILE (its own layer, 3 master loops): the cart holds 1, then 2, then 3 brackets; when the third lands the full
cart rolls out to the left (wheels turning), and a moment later rolls back in empty, easing to a stop; the
next loop's bracket starts the new batch. Frame 0 shows the cart with one bracket.
Ambient: the furnace mouth flickers (2300 ms, its own loop).
Face: fine-line eyes only (open / half / line / look_l / look_r / look_d / sparkle), smooth irregular blinks;
his gaze always reaches a thing before his hand does. Normal body size throughout (STYLE.md section 0).
Unlike 'edits' (hammer and nail on a brick wall), the work here is hot metal: glow, sparks, the quench hiss,
the finished part admired and carted off.
Layers: scene (static: anvil, bucket + water, furnace, Clawd's torso: he never leaves HOME, only his arms
move) | glow | pile (cart, 3 loops) | face (fine eyes) | piece (the bracket wherever it is) |
work (right arm + hammer) | left (left arm) | fx (impact glint, sparks, splash, steam, drips, glints).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'working-forge'
STATE = 'working (variant)'
DESC = ('Blacksmith Clawd forges a glowing curly brace on his little anvil: steady strikes with sparks, turns it '
        'over, quenches it in the bucket with a puff of steam, holds up the cooled steel bracket with a '
        'sparkle and drops it in his cart, which rolls off full every third bracket while the furnace slides '
        'out the next glowing piece.')

_HAMMER = get('hammer')          # upright (raised high)
_HAMMER_UP = get('hammer_up')    # 45 degrees, mid-swing
_SPARK = get('sparkle_small')
_PUFF = get('smoke_puff')


def _paint(f, rows, x0, y0, clip=False):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                x, y = x0 + i, y0 + j
                if clip and not (0 <= x < W and 0 <= y < H):
                    continue
                f.put(x, y, ch)


# =====================================================================================================
# Scenery
# =====================================================================================================
# Anvil (x 23-28): a light face lit from the top-left, horn pointing at him over the bucket, dark body.
_ANVIL = [
    'mSmmmm',       # y 15 face (horn tip at x 23)
    '..NNNn',       # y 16
    '...Nn.',       # y 17 waist
    '..NNNn',       # y 18 foot
    '.NNNNn',       # y 19
]
_ANVIL_X, _ANVIL_Y = 23, 15

# Wooden bucket (x 20-22) under the horn, right at his foot: staves, a dark hoop, water on top.
_BUCKET = [
    'TcT',          # y 16 rim + water
    'tTd',          # y 17
    'ddd',          # y 18 hoop
    'tTd',          # y 19
]
_BUCKET_X, _BUCKET_Y = 20, 16

# Small brick furnace (x 28-30): a dark iron cap, bricks lit from the left, its mouth (x 28, rows 11-14)
# facing the anvil glows (glow layer).
_FURNACE = [
    'sms',          # y 9 cap
    'rrR',          # y 10
    '.rR',          # y 11 mouth ...
    '.RR',          # y 12
    '.rR',          # y 13
    '.RR',          # y 14 ... (x 28)
    'rrR',          # y 15
    'RrR',          # y 16
    'rrR',          # y 17
    'RrR',          # y 18
    'RRR',          # y 19
]
_FURNACE_X, _FURNACE_Y = 28, 9
_MOUTH = [(28, y) for y in range(11, 15)]

_TORSO = clawd(eyes='blink', larm='none', rarm='none')


def _scene():
    f = Frame()
    _paint(f, _FURNACE, _FURNACE_X, _FURNACE_Y)
    _paint(f, _ANVIL, _ANVIL_X, _ANVIL_Y)
    _paint(f, _BUCKET, _BUCKET_X, _BUCKET_Y)
    put_clawd(f, _TORSO)
    return f


# =====================================================================================================
# Braces: 3 x 5 shapes ('h' = the metal, 'e' = its cooler tips)
# =====================================================================================================
_SHAPES = {
    'bar':   ['.h.', '.h.', '.h.', '.h.', '.h.'],
    'bend':  ['.e.', 'h..', 'h..', 'h..', '.e.'],    # a '(' : half way
    'brace': ['.he', '.h.', 'h..', '.h.', '.he'],
    'edge':  ['.h.', '.h.', '.h.', '.h.', '.h.'],    # mid-flip, seen edge-on
}
_HEAT = {'flash': ('Y', 'y'), 'white': ('y', 'Y'), 'hot': ('y', 'o'), 'warm': ('o', 'O'),
         'steel': ('m', 's')}
_ON_ANVIL = (24, 10)             # top-left of a piece standing on the anvil face


def _brace(f, shape, x0, y0, col, tip=None, clip_below=None):
    for j, r in enumerate(_SHAPES[shape]):
        for i, ch in enumerate(r):
            if ch == '.' or (clip_below is not None and y0 + j > clip_below):
                continue
            x, y = x0 + i, y0 + j
            if 0 <= x < W and 0 <= y < H:
                f.put(x, y, tip if (ch == 'e' and tip) else col)


def _piece(s):
    """The bracket wherever it is: on the anvil (glowing; flaring white on impact; hopping when turned),
    sliding out of the furnace, tipping into the bucket, in his hands (cooled steel)."""
    f = Frame()
    pc = s['piece']
    if not pc:
        return f
    if pc[0] == 'anvil':
        _, shape, heat, dx, lift = pc
        col, tip = _HEAT[heat]
        x0 = _ON_ANVIL[0] + dx
        _brace(f, shape, x0, _ON_ANVIL[1] - lift, col, tip)
        if dx >= 3:                      # still half inside the furnace mouth
            for x, y in list(f.px):
                if x >= 28 and y >= 11:
                    del f.px[(x, y)]
    elif pc[0] == 'tip':                 # tipping off the horn: leaning, then into the bucket
        if pc[1] == 0:
            for x, y in ((23, 11), (22, 12), (22, 13), (21, 14)):
                f.put(x, y, 'o')
        else:
            f.vline(21, 13, 15, 'o')
    elif pc[0] == 'hand':                # cooled steel, top-left at (x, y)
        x0, y0 = pc[1], pc[2]
        _brace(f, 'brace', x0, y0, 'm', 's', clip_below=15 if (x0 >= 19 and y0 > 10) else None)
        if s.get('glint'):
            f.put(x0 + 1, y0, 'W')
    return f


# =====================================================================================================
# The cart of finished brackets (3 master loops)
# =====================================================================================================
_CART = [
    'ttttttttt',    # y 16 rim (lit)
    'TTTTTTTTT',    # y 17
    'TTTTTTTTT',    # y 18
]
_CART_X, _CART_Y = 1, 16
_WHEELS = (('d', 'N'), ('N', 'd'))      # two looks: the wheel turns
_SLOTS = (7, 4, 1)                       # x of the newest, then older brackets (tops on row 12)


def _cart(f, n, dx=0, wheel=0, drop=None):
    """The cart at offset dx with n brackets standing in it (the newest at the near end). drop: the new
    one is still falling (its top on row 11) while the others are only half nudged along."""
    _paint(f, _CART, _CART_X + dx, _CART_Y, clip=True)
    a, b = _WHEELS[wheel]
    for x in (2 + dx, 7 + dx):
        for xx, ch in ((x, a), (x + 1, b)):
            if 0 <= xx < W:
                f.put(xx, 19, ch)
    for k in range(n):
        x = _SLOTS[k] + dx
        y = 12
        if drop is not None:
            if k == 0:
                y = 11
            else:
                x = _SLOTS[k] + 1 + dx
        _brace(f, 'brace', x, y, 'm', clip_below=15)


# =====================================================================================================
# Clawd: arms + tools (normal pixels), face (fine pixels)
# =====================================================================================================
def _pose(s):
    return clawd(eyes='blink', larm=s['larm'], rarm=s['rarm'])


_TORSO_PX = None


def _arm(s, side):
    global _TORSO_PX
    if _TORSO_PX is None:
        t = Frame()
        put_clawd(t, _TORSO)
        _TORSO_PX = dict(t.px)
    f = Frame()
    put_clawd(f, _pose(s))
    mid = HOME[0] + 5
    return {c: ch for c, ch in f.px.items() if _TORSO_PX.get(c) != ch and ((c[0] < mid) == (side == 'l'))}


_HAMMER_ARM = {'high': 'high', 'back': 'high', 'swing': 'raise', 'strike': 'wave', 'tap': 'wave',
               'push': 'raise', 'take': 'up'}
_GRAY = {'N': 's', 'm': 's'}


def _hammer(f, s, p):
    """'high' = held straight up (library hammer); 'back' = wound back over his head; 'swing' = tipped
    forward 45 degrees (library); 'strike' = handle up-right from his hand, the 2 x 2 head on the top of
    the piece; 'tap' = the same a row higher (recoil, light taps); 'push' = level, nudging the piece; 'lay'
    = resting on the anvil; 'take' = his hand on it as he picks it up."""
    hm = s['hammer']
    gx, gy = p.at('hand_r')
    if hm == 'high':
        f.place(_HAMMER.sprite(0).recolor(_GRAY), gx, gy)
    elif hm == 'back':
        f.vline(gx, gy - 3, gy - 1, 'T')
        f.put(gx - 1, gy - 4, 'T')
        for x, y in ((gx - 3, gy - 6), (gx - 2, gy - 6), (gx - 3, gy - 5), (gx - 2, gy - 5)):
            f.put(x, y, 's')
    elif hm == 'swing':
        f.place(_HAMMER_UP.sprite(0).recolor(_GRAY), gx, gy)
    elif hm in ('strike', 'tap'):
        up = 1 if hm == 'tap' else 0
        f.put(gx + 1, gy - 1 - up, 'T')
        for x, y in ((gx + 2, gy - 3 - up), (gx + 3, gy - 3 - up), (gx + 2, gy - 2 - up), (gx + 3, gy - 2 - up)):
            f.put(x, y, 's')
    elif hm == 'push':                   # the claw hooked over the brace's top, pulling it toward him
        f.put(gx + 1, gy - 1, 'T')
        f.put(gx + 2, gy - 2, 'T')
        f.put(gx + 3, gy - 2, 's')
        f.put(gx + 3, gy - 3, 's')
    elif hm in ('lay', 'take'):
        f.hline(23, 25, 14, 'T')
        f.put(26, 14, 's')
        f.put(26, 13, 's')


def _work(s):
    f = Frame()
    f.px.update(_arm(s, 'r'))
    _hammer(f, s, _pose(s))
    return f


def _left(s):
    f = Frame()
    f.px.update(_arm(s, 'l'))
    return f


_FACE = {}


def _face(expr):
    if expr not in _FACE:
        p = clawd(eyes='blink')
        f = Frame()
        put_clawd(f, p)
        base = fine(f)
        ff = fine_face(base.copy(), p, expr=expr)
        g = Frame({c: v for c, v in ff.px.items() if base.px.get(c) != v}, res=2)
        g.meta = {'fine_face': [(expr, expr)]}
        _FACE[expr] = g
    return _FACE[expr].copy()


# =====================================================================================================
# Effects
# =====================================================================================================
# Sparks thrown out of the contact point on arcs: one ballistic path each, cooling as they fly.
_SPARK_PATHS = [ballistic(25, 9, vx, vy, g=0.7, steps=3)
                for vx, vy in ((-1.6, -1.3), (1.6, -1.1), (-0.5, -2.0), (1.1, -1.9))]
_SPARK_COL = ('y', 'y', 'o')


def _sparks(f, k, n):
    for path in _SPARK_PATHS[:n]:
        x, y = path[k]
        if 0 <= x < W and 0 <= y < H and not (x >= 28 and y >= 9):
            f.put(x, y, _SPARK_COL[k])


_SPLASH = [                      # out of the bucket (x 20-22), clear of his arm and body
    [(21, 15, 'c')],
    [(22, 14, 'c'), (21, 13, 'c')],
    [(23, 13, 'c'), (21, 12, 'c'), (22, 11, 'c')],
    [(23, 14, 'c'), (22, 13, 'c')],
]
# steam out of the bucket: (puff frame, x, y) per beat: it swells, rises and peels apart
_STEAM = [                       # one puff: it swells, rises and peels apart
    [(0, 22, 11)],
    [(1, 22, 10)],
    [(2, 22, 8)],
    [(2, 23, 6)],
    [(3, 23, 4)],
]


def _fx(s):
    f = Frame()
    sp = s.get('sparks')
    if sp is not None:
        _sparks(f, sp[0], sp[1])
    if s.get('impact'):                  # a white-hot glint where the hammer meets the brace
        f.put(23, 9, 'W')
        f.put(26, 10, 'Y')
    for x, y, ch in _SPLASH[s['splash']] if s.get('splash') is not None else ():
        f.put(x, y, ch)
    if s.get('steam') is not None:
        for k, x, y in _STEAM[s['steam']]:
            f.place(_PUFF.sprite(k), x, y)
    if s.get('ripple'):
        f.put(21, 16, 'C')
    if s.get('drip') is not None:
        x, y = s['drip']
        f.put(x, y, 'c')
    if s.get('twinkle') is not None:
        x, y, k = s['twinkle']
        f.place(_SPARK.sprite(k), x, y)
    if s.get('flare'):                   # the furnace mouth flares as it pushes out the next piece
        for x, y in _MOUTH:
            f.put(x, y, 'Y' if y in (12, 13) else 'y')
        f.put(27, 12, 'y')
    return f


# =====================================================================================================
# Master timeline
# =====================================================================================================
class _TL:
    ONCE = ('sparks', 'splash', 'steam', 'twinkle', 'glint', 'ripple', 'drip', 'impact', 'flare', 'drop')

    def __init__(self):
        self.segs = []
        self.st = dict(eyes='look_r', larm='side', rarm='high', hammer='high',
                       piece=('anvil', 'brace', 'hot', 0, 0))

    def add(self, ms, **kw):
        once = {k: kw.pop(k) for k in list(kw) if k in self.ONCE}
        if 'hammer' in kw and kw['hammer'] in _HAMMER_ARM and 'rarm' not in kw:
            kw['rarm'] = _HAMMER_ARM[kw['hammer']]
        self.st.update(kw)
        s = dict(self.st)
        s.update(once)
        self.segs.append((int(ms), s))

    def blink(self, **kw):
        back = self.st['eyes']
        self.add(60, eyes='half', **kw)
        self.add(90, eyes='line')
        self.add(60, eyes='half')
        self.st['eyes'] = back

    def strike(self, shape, heat, aim, hold, sparks=4):
        """aim (held high) -> wind back -> swing -> IMPACT (flash, the piece flares white and takes its new
        shape) -> sparks fly out on arcs while the hammer recoils -> back up high."""
        self.add(aim, hammer='high')
        self.add(130, hammer='back')
        self.add(60, hammer='swing')
        self.add(80, hammer='strike', piece=('anvil', shape, heat, 0, 0), impact=True, sparks=(0, sparks))
        self.add(100, hammer='tap', sparks=(1, sparks))
        self.add(110, hammer='high', sparks=(2, sparks))
        self.add(hold)


def _timeline():
    t = _TL()
    # A  shape: a strike (the glow cools a little), a blink
    t.strike('brace', 'warm', 620, 260)
    t.blink()
    t.add(220)
    # B  turn it over: a light tap, it hops, edge-on, lands with a bounce; one more strike
    t.add(80, hammer='swing')
    t.add(80, hammer='tap', piece=('anvil', 'brace', 'warm', 0, 1))
    t.add(120, piece=('anvil', 'edge', 'warm', 0, 3), eyes='open')
    t.add(90, piece=('anvil', 'brace', 'warm', 0, 1), eyes='look_r')
    t.add(320, piece=('anvil', 'brace', 'warm', 0, 0), hammer='high')
    # C  quench: eyes to the bucket, nudge it off the horn, splash, steam; the hammer is laid down
    t.add(240, eyes='look_d')
    t.add(110, hammer='swing')
    t.add(140, hammer='push', piece=('anvil', 'brace', 'warm', -1, 0))
    t.add(120, piece=('anvil', 'brace', 'warm', -2, 0))
    t.add(90, piece=('tip', 0))
    t.add(80, piece=('tip', 1), splash=0)
    t.add(90, piece=None, splash=1, steam=0)
    t.add(110, splash=2, steam=1)
    t.add(120, splash=3, steam=2, ripple=True, hammer='swing')
    t.add(150, steam=3, eyes='look_r', hammer='lay', rarm='up')
    t.add(180, steam=4, rarm='side')
    t.add(300)
    t.blink()
    t.add(120)
    # D  admire: eyes down, the hand dips in, lifts the cooled bracket (a drip), up to his face, both hands
    t.add(220, eyes='look_d')
    t.add(180, rarm='down', ripple=True)
    t.add(170, rarm='side', piece=('hand', 21, 11), drip=(22, 16))
    t.add(150, rarm='up', piece=('hand', 20, 9), eyes='look_r')
    t.add(170, rarm='chin', piece=('hand', 15, 10), eyes='open')
    t.add(200, larm='chin', eyes='half')
    t.add(120, eyes='sparkle', glint=True, twinkle=(16, 10, 1))
    t.add(200, glint=True, twinkle=(16, 10, 2))
    t.add(130, glint=True, twinkle=(16, 10, 0))
    t.add(480)
    # E  on the pile: eyes to the cart, the left hand carries it over and drops it in: clink
    t.add(200, eyes='look_l')
    t.add(180, rarm='side', larm='front', piece=('hand', 11, 9))
    t.add(170, larm='up', piece=('hand', 7, 8))
    t.add(160, larm='side', piece=('hand', 7, 10))
    t.add(130, larm='down', piece=None, drop=True)
    t.add(160, larm='side', twinkle=(8, 12, 1))
    t.add(400)
    # F  next piece: eyes back to the anvil, take up the hammer; the furnace flares and slides out a bar
    t.add(220, eyes='look_r')
    t.add(170, rarm='out')
    t.add(170, hammer='take')
    t.add(180, hammer='high')
    t.add(140, flare=True, piece=('anvil', 'bar', 'white', 3, 0))
    t.add(110, piece=('anvil', 'bar', 'white', 1, 0))
    t.add(80, piece=('anvil', 'bar', 'white', 0, 1))
    t.add(120, piece=('anvil', 'bar', 'white', 0, 0))
    t.strike('bend', 'white', 300, 220)
    t.blink()
    t.strike('brace', 'hot', 160, 280)
    return t


# =====================================================================================================
# Ambient: the furnace mouth flickers
# =====================================================================================================
def _glow():
    out = []
    for col, ms in (('oyyo', 1300), ('ojyo', 1000)):
        f = Frame()
        for (x, y), ch in zip(_MOUTH, col):
            f.put(x, y, ch)
        out.append((f, ms))
    return out


# =====================================================================================================
# The pile cart over 3 master loops: 1 -> 2 -> 3 (full: it rolls off, comes back empty) -> 0 -> 1
# =====================================================================================================
_ROLL_OUT = (-2, -6)            # it gathers speed ...
_ROLL_IN = (-4, -1)             # ... and comes back easing to a stop


def _pile(segs):
    loop = sum(ms for ms, _ in segs)
    drop_at, drop_ms = 0, 0
    clock = 0
    for ms, s in segs:
        if s.get('drop'):
            drop_at, drop_ms = clock, ms
        clock += ms
    frames = []

    def add(fr, ms):
        frames.append((fr, ms))

    def still(n):
        f = Frame()
        _cart(f, n)
        return f

    # loop 1: 1 -> 2, loop 2: 2 -> 3 then the full cart rolls off and back empty, loop 3: 0 -> 1
    for k, n in enumerate((1, 2, 0)):
        add(still(n), drop_at)
        f = Frame()
        _cart(f, n + 1, drop=True)
        add(f, drop_ms)
        rest = loop - drop_at - drop_ms
        if k != 1:
            add(still(n + 1), rest)
            continue
        add(still(3), 700)
        used = 700
        for i, dx in enumerate(_ROLL_OUT):
            f = Frame()
            _cart(f, 3, dx=dx, wheel=i % 2)
            add(f, 110)
            used += 110
        add(Frame(), 500)
        used += 500
        for i, dx in enumerate(_ROLL_IN):
            f = Frame()
            _cart(f, 0, dx=dx, wheel=i % 2)
            add(f, 140 + 80 * i)
            used += 140 + 80 * i
        assert used < rest, (used, rest)
        add(still(0), rest - used)
    return frames


def build():
    t = _timeline()
    face, piece, work, left, fx = [], [], [], [], []
    for ms, s in t.segs:
        face.append((_face(s['eyes']), ms))
        piece.append((_piece(s), ms))
        work.append((_work(s), ms))
        left.append((_left(s), ms))
        fx.append((_fx(s), ms))
    return anim(NAME, DESC, [
        static('scene', _scene()),
        layer('glow', _glow()),
        layer('pile', _pile(t.segs)),
        layer('face', face),
        layer('piece', piece),
        layer('work', work),
        layer('left', left),
        layer('fx', fx),
    ], state=STATE)
