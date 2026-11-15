"""working-lab - Claude is running (working variant): Clawd the chemist.   Preview:  python3 gen/preview.py anim working-lab

STORYBOARD (one master beat list drives every synced layer, so nothing ever drifts; loop 12.25 s)
     0  F0  Clawd at HOME, brass goggles pushed up on his forehead, a clipboard in his left hand. In his
            right hand a blue test tube, held level just over the open rim of a pink flask that warms on a
            tripod over a small blue flame at his right; reagent bottles on a low shelf at the far left. His
            eyes are on the flask.
        A   POUR: he tips the tube: a thin blue stream runs down through the rim and the neck (it starts,
            runs, thins), the blue lands in the pink; he tips the tube back level and a last drop falls.
        B   REACTION: the colour changes gradually, from the top down: pink -> a lavender swirl -> mauve ->
            violet. Bubbles of different sizes rise out of the neck at their own pace and pop (a big one
            with a burst, small ones with a speck). Meanwhile he raises the tube and lowers it into its
            little stand at his foot.
        C   CHECK: his eyes on the flask, his hand takes it and lifts it off the tripod, swirls it (it rocks
            left and right, the liquid sloshes), raises it beside his face in two steps and looks through
            it ... the batch is right: his eyes sparkle and a twinkle grows and fades on the glass. Down in
            two steps, back onto the tripod, his hand lets go.
        D   NOTE: he looks at his clipboard first, lifts it in two steps, writes a line (it grows) and
            ticks it, blinks, then the used page curls over the clip and a fresh one shows; the clipboard
            goes down.
        E   NEXT RUN: on the flame the batch slowly turns back to pink (violet -> mauve -> pink) with a few
            lazy bubbles, while he looks down at the stand, takes the tube, raises it and holds it level
            over the rim again ... = frame 0 (seamless).
Ambient (own loops, co-prime with the story): the burner flame flickers (1900 ms); a glint runs over the
reagent bottles now and then (6100 ms).
Face: fine-line eyes only (open / half / line / look_l / look_r / look_d / sparkle; no look_u / wide: the
pushed-up goggles sit right above his eyes), smooth irregular blinks; his gaze always reaches a thing before
his hand does. Normal body size (STYLE.md section 0).
Layers: scene (static: tripod, lamp, tube stand, bottle shelf, Clawd's torso + goggles: he never leaves
HOME, only his arms move) | flame | glint | face (fine eyes) | flask (the flask, wherever it is) | right (right
arm + blue tube) | clip (left arm + clipboard) | fx (stream, drops, bubbles, twinkle).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'working-lab'
STATE = 'working (variant)'
DESC = ('Chemist Clawd in pushed-up goggles pours a thin stream from a blue test tube into a pink flask warming '
        'over a little flame: it bubbles and slowly turns violet, he swirls it and holds it up to the light '
        '(sparkle: the batch is right), ticks it off on his clipboard and lets it simmer back to pink for the '
        'next run.')

_GOGGLES = get('goggles_up')
_SPARK = get('sparkle_small')


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


# =====================================================================================================
# Scenery
# =====================================================================================================
# Tripod (x 22-26, gauze on row 17) over a little spirit lamp (x 23-25, row 19); the flame (row 18)
# flickers in its own layer.
_TRIPOD = [
    'NmmmN',        # y 17 gauze
    'N...N',        # y 18 legs
    'NmjmN',        # y 19 feet + the lamp (glass with its fuel)
]
_TRIPOD_X, _TRIPOD_Y = 22, 17

# One-slot test tube stand at his right foot (x 20-21): the blue tube rests in it between pours.
_STAND = [(20, 17, 'T'), (21, 17, 'T'), (20, 18, 'd'), (20, 19, 'd'), (21, 19, 'd')]

# A shelf of reagent bottles at the far left (x 1-4).
_SHELF = [
    '.g..',         # y 15
    'GgyJ',         # y 16
    'Ggyj',         # y 17
    'TTTT',         # y 18
    'd..d',         # y 19
]
_SHELF_X, _SHELF_Y = 1, 15

_TORSO = clawd(eyes='blink', larm='none', rarm='none')


def _scene():
    f = Frame()
    _paint(f, _SHELF, _SHELF_X, _SHELF_Y)
    _paint(f, _TRIPOD, _TRIPOD_X, _TRIPOD_Y)
    for x, y, ch in _STAND:
        f.put(x, y, ch)
    put_clawd(f, _TORSO)
    wear(f, _GOGGLES, _TORSO)
    return f


# =====================================================================================================
# The flask (Erlenmeyer, 5 x 5, open at the top)
# =====================================================================================================
_FLASK = [
    '.m.m.',        # rim (open: the stream and the bubbles pass through x 24)
    '.m.m.',        # neck
    'm123m',        # body, top row
    'm456m',        # body, bottom row
    'mmmmm',
]
_ON_TRIPOD = (22, 12)            # top-left when it stands on the gauze
# The liquid's six cells (top row left-right, bottom row left-right). The colour turns from the top down.
_LIQUID = {
    'p0': 'pppppp',
    'p1': 'pbpppp',              # the blue lands
    'p2': 'plpppp',              # it starts to mix
    'p3': 'lplplp',              # a lavender swirl ...
    'p4': 'lvlplp',              # ... mauve ...
    'p5': 'vlvlvl',
    'v': 'vlvvvv',               # ... violet (a lavender highlight on top)
    's1': 'lvvvvv',              # sloshing while he swirls it
    's2': 'vvlvvv',
    'c1': 'vlvlvl',              # cooling back to pink, from the top down
    'c2': 'lplvlv',
    'c3': 'plplpl',
    'c4': 'plpppp',
}


def _flask(f, x0, y0, liquid):
    cols = _LIQUID[liquid]
    for j, r in enumerate(_FLASK):
        for i, ch in enumerate(r):
            if ch == '.':
                continue
            f.put(x0 + i, y0 + j, cols[int(ch) - 1] if ch.isdigit() else ch)


def _flask_layer(s):
    f = Frame()
    fl = s['flask']
    if fl == 'tripod':
        _flask(f, _ON_TRIPOD[0], _ON_TRIPOD[1], s['liquid'])
    elif fl == 'held':                   # in his right hand, his grip at the flask's left side
        gx, gy = _pose(s).at('hand_r')
        _flask(f, gx + s.get('rock', 0), gy - 3, s['liquid'])
    return f


# =====================================================================================================
# Clawd: arms + what they hold (normal pixels), face (fine pixels)
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


# The blue test tube: glass ends 'm', blue liquid 'c' (light) / 'b'. Absolute cells per state.
_TUBE = {
    'ready': [(21, 10, 'm'), (22, 10, 'b'), (23, 10, 'c'), (24, 10, 'm')],    # level over the rim (F0)
    'pour':  [(21, 9, 'm'), (22, 10, 'c'), (23, 10, 'b'), (24, 11, 'b')],    # tipped: blue at the mouth
    'lift':  [(21, 11, 'm'), (22, 10, 'b'), (23, 9, 'c'), (24, 8, 'm')],     # rising, mouth up
    'hold':  [(21, 10, 'm'), (21, 11, 'c'), (21, 12, 'b'), (21, 13, 'm')],   # upright in his hand
    'low':   [(21, 12, 'm'), (21, 13, 'c'), (21, 14, 'b'), (21, 15, 'm')],   # going into the stand
    'stand': [(21, 14, 'm'), (21, 15, 'c'), (21, 16, 'b'), (21, 18, 'm')],   # resting in the stand
}


def _right(s):
    """His right arm and the blue test tube."""
    f = Frame()
    f.px.update(_arm(s, 'r'))
    for x, y, ch in _TUBE[s['tube']]:
        f.put(x, y, ch)
    return f


# Clipboard (5 x 5) in his left hand: wood board, paper, a written line, a tick slot, the steel clip.
_CLIP_ROWS = {
    'blank':  ['TsssT', 'TwwwT', 'TwwwT', 'TwwwT', 'TTTTT'],
    'write1': ['TsssT', 'TwwwT', 'TwNwT', 'TwwwT', 'TTTTT'],
    'write2': ['TsssT', 'TwwwT', 'TwNNT', 'TwwwT', 'TTTTT'],
    'tick':   ['TsssT', 'TwwwT', 'TgNNT', 'TwwwT', 'TTTTT'],
    'curl1':  ['TsssT', 'TwwMm', 'TwgNT', 'TwwwT', 'TTTTT'],     # the used page's corner lifts ...
    'curl2':  ['TsMmT', 'TwwmT', 'TwwwT', 'TwwwT', 'TTTTT'],     # ... and it folds over the clip
}
_CLIP_AT = {'side': (5, 14), 'out': (4, 12), 'up': (5, 10)}     # top-left per left-arm shape


def _clip(s):
    f = Frame()
    f.px.update(_arm(s, 'l'))
    x0, y0 = _CLIP_AT[s['larm']]
    _paint(f, _CLIP_ROWS[s['page']], x0, y0)
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
# Effects: the stream, drops, bubbles, the 'batch is right' twinkle
# =====================================================================================================
_STREAM = {                      # through the rim gap (x 24, row 12) and the neck (row 13)
    1: [(24, 12, 'b')],
    2: [(24, 12, 'b'), (24, 13, 'b')],
    3: [(24, 13, 'b')],          # thinning: the tail of it
}


def _bubble(f, x, y, kind):
    """'in' = a bright dot inside the liquid, 's' = a small bubble, 'b' = a big one (2 x 2, a glint),
    'pop' = a big one bursting (four specks), 'pip' = a small one popping (one speck)."""
    if kind == 'in':
        f.put(x, y, 'W')
    elif kind == 's':
        f.put(x, y, 'l')
    elif kind == 'b':
        f.put(x, y, 'l')
        f.put(x + 1, y, 'l')
        f.put(x, y + 1, 'l')
        f.put(x + 1, y + 1, 'v')
    elif kind == 'pop':
        for dx, dy in ((-1, -1), (2, -1), (-1, 2), (2, 2)):
            f.put(x + dx, y + dy, 'v')
    elif kind == 'pip':
        f.put(x, y, 'v')


# Each bubble: (first frame, [(x, y, kind), ...] one step per frame). They rise out of the neck at their
# own pace: a small one first, a big one that bursts, a quick small one, a late tiny one.
_BUBBLES = [
    (0, [(23, 15, 'in'), (24, 13, 's'), (24, 11, 's'), (24, 10, 's'), (25, 8, 'pip')]),
    (2, [(25, 14, 'in'), (24, 14, 'in'), (24, 13, 's'), (23, 10, 'b'), (23, 8, 'b'), (23, 7, 'pop')]),
    (5, [(23, 14, 'in'), (24, 13, 's'), (24, 11, 's'), (23, 9, 's'), (23, 8, 'pip')]),
    (8, [(25, 15, 'in'), (24, 13, 's'), (25, 11, 's'), (25, 10, 'pip')]),
]
_N_BUB = 12
# lazy bubbles while it simmers back (E): small and slow
_LAZY = [
    (0, [(24, 14, 'in'), (24, 13, 's'), (24, 11, 's'), (24, 10, 'pip')]),
    (3, [(23, 15, 'in'), (24, 13, 's'), (24, 11, 'pip')]),
]
_N_LAZY = 6


def _bubbles(f, table, k):
    for start, path in table:
        i = k - start
        if 0 <= i < len(path):
            _bubble(f, *path[i])


def _fx(s):
    f = Frame()
    for x, y, ch in _STREAM.get(s.get('stream'), ()):
        f.put(x, y, ch)
    if s.get('drop') is not None:        # a last drop from the tube's mouth
        f.put(24, 11 + s['drop'], 'b')
    if s.get('bub') is not None:
        _bubbles(f, _BUBBLES, s['bub'])
    if s.get('lazy') is not None:
        _bubbles(f, _LAZY, s['lazy'])
    if s.get('spark') is not None:
        f.place(_SPARK.sprite(s['spark']), 24, 8)
    return f


# =====================================================================================================
# Master timeline
# =====================================================================================================
class _TL:
    ONCE = ('stream', 'drop', 'bub', 'lazy', 'spark', 'rock')

    def __init__(self):
        self.segs = []
        self.st = dict(eyes='look_r', larm='side', rarm='wave', tube='ready', flask='tripod', liquid='p0',
                       page='blank')

    def add(self, ms, **kw):
        once = {k: kw.pop(k) for k in list(kw) if k in self.ONCE}
        self.st.update(kw)
        s = dict(self.st)
        s.update(once)
        self.segs.append((int(ms), s))

    def blink(self, slow=False):
        back = self.st['eyes']
        self.add(70 if slow else 60, eyes='half')
        self.add(110 if slow else 90, eyes='line')
        self.add(70 if slow else 60, eyes='half')
        self.st['eyes'] = back


def _timeline():
    t = _TL()
    # A  pour: tip the tube, a thin stream starts, runs, thins; tip it back, a last drop
    t.add(560)
    t.add(110, tube='pour', stream=1)
    t.add(130, stream=2, liquid='p1')
    t.add(150, stream=2, liquid='p1')
    t.add(120, stream=3, liquid='p2')
    t.add(110, tube='ready', drop=1)
    t.add(110, drop=2)
    t.add(200)
    # B  reaction: the colour turns from the top down while bubbles rise at their own pace; the tube
    #    goes up and into its stand
    colour = {0: 'p2', 2: 'p3', 4: 'p4', 6: 'p5', 9: 'v'}
    hand = {1: dict(rarm='raise', tube='lift'), 3: dict(rarm='up', tube='hold'),
            5: dict(rarm='side', tube='low'), 6: dict(tube='stand'), 8: dict(eyes='open'),
            10: dict(eyes='look_r')}
    for k in range(_N_BUB):
        kw = dict(bub=k)
        if k in colour:
            kw['liquid'] = colour[k]
        kw.update(hand.get(k, {}))
        t.add(120 if k < 6 else 130, **kw)
    t.add(320)
    t.blink()
    t.add(240)
    # C  check: eyes on it, take it, lift, swirl (rock and slosh), up beside his face, look ... sparkle
    t.add(160, rarm='out')
    t.add(150, flask='held')
    for rock, liq in ((-1, 's1'), (0, 's2'), (1, 's1'), (0, 's2'), (0, 'v')):
        t.add(120, rock=rock, liquid=liq)
    t.add(170, rarm='up')
    t.add(190, rarm='raise')
    t.add(300)
    t.add(130, eyes='half')
    t.add(100, eyes='sparkle', spark=0)
    t.add(110, spark=1)
    t.add(200, spark=2)
    t.add(110, spark=1)
    t.add(100, spark=0)
    t.add(420)
    t.add(130, eyes='look_r')
    t.add(170, rarm='up')
    t.add(170, rarm='out')
    t.add(130, flask='tripod')
    t.add(160, rarm='side')
    # D  note: eyes on the clipboard, lift it, write a line, tick it; the page curls over; down again
    t.add(240, eyes='look_l')
    t.add(130, larm='out')
    t.add(170, larm='up')
    t.add(240, page='write1')
    t.add(240, page='write2')
    t.add(320, page='tick')
    t.blink(slow=True)
    t.add(200)
    t.add(120, page='curl1')
    t.add(130, page='curl2')
    t.add(240, page='blank')
    t.add(130, larm='out')
    t.add(170, larm='side', eyes='look_r')
    # E  next run: it simmers back to pink with lazy bubbles; he takes the tube and holds it level again
    for k, liq in zip(range(_N_LAZY), ('c1', 'c1', 'c2', 'c3', 'c4', 'p0')):
        kw = dict(lazy=k, liquid=liq)
        if k == 2:
            kw['eyes'] = 'look_d'
        t.add(170, **kw)
    t.add(150, rarm='side')
    t.add(150, rarm='up', tube='hold', eyes='look_r')
    t.add(150, rarm='raise', tube='lift')
    t.add(170, rarm='wave', tube='ready')
    t.add(260)
    t.blink()
    t.add(300)
    return t


# =====================================================================================================
# Ambient
# =====================================================================================================
def _flame():
    out = []
    for cells, ms in (([(24, 18, 'c'), (23, 18, 'b'), (25, 18, 'b')], 600),
                      ([(24, 18, 'C'), (23, 18, 'b')], 500),
                      ([(24, 18, 'c'), (25, 18, 'b')], 400),
                      ([(24, 18, 'C'), (23, 18, 'b'), (25, 18, 'b')], 400)):
        f = Frame()
        for x, y, ch in cells:
            f.put(x, y, ch)
        out.append((f, ms))
    return out


def _glint():
    f = Frame()
    f.put(2, 15, 'h')               # a glint on the green bottle ...
    g = Frame()
    g.put(3, 16, 'Y')               # ... then on the yellow one
    return [(Frame(), 5500), (f, 140), (g, 140), (Frame(), 320)]


def build():
    t = _timeline()
    face, flask, right, clip, fx = [], [], [], [], []
    for ms, s in t.segs:
        face.append((_face(s['eyes']), ms))
        flask.append((_flask_layer(s), ms))
        right.append((_right(s), ms))
        clip.append((_clip(s), ms))
        fx.append((_fx(s), ms))
    return anim(NAME, DESC, [
        static('scene', _scene()),
        layer('flame', _flame()),
        layer('glint', _glint()),
        layer('face', face),
        layer('flask', flask),
        layer('right', right),
        layer('clip', clip),
        layer('fx', fx),
    ], state=STATE)
