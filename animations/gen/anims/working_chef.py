"""working-chef - Claude is running (working variant): Clawd the cook.   Preview:  python3 gen/preview.py anim working-chef

STORYBOARD (one master beat list drives every synced layer, so nothing ever drifts; loop 16.7 s)
     0  F0  Clawd at HOME in a small chef's toque, stirring a red soup pot on a little stove at his right
            with a wooden spoon, his eyes on the pot; soft steam curls up from it. At his left a carrot lies
            on a cutting board on a crate of carrots, his cleaver standing at the board's end.
        A   STIR: a slow circle (six phases: the handle draws an ellipse, the spoon dwells a moment at each
            side of the pot and a gold swirl follows it through the broth); a smooth blink.
        B   CHOP: his eyes go to the board first, then his hand takes the cleaver; three chops, each with a
            wind-up (wrist cocks, aims), a quick strike and a recoil; the cut coin hops onto the pile at the
            board's end. The rhythm is uneven, like real chopping.
        C   INTO THE POT: he glances at the pot (aiming), scoops the coins and the tip onto the blade in two
            slides, lifts them, dips (wind-up) and flicks: the pieces sail over his hat on an eased arc,
            slowing at the top, his eyes following them; plop, plop, plop: a splash grows out of the broth
            and falls back, ripples settle.
        D   NEXT CARROT: he looks down at the crate, his hand dips in, pulls a carrot up by its greens in two
            steps and lays it on the board, where it settles with a little bounce; the hand takes the
            cleaver again.
        E   TASTE: he looks at the spoon, lifts it out of the pot (a drip falls back in) and holds it up
            beside his face; his eyes close slowly to taste (a long fine 'line' hold) ... a beat ... then
            they light up: sparkle, and a twinkle grows and fades over the pot. Spoon back into the pot.
        F   SALT: he looks at the salt dish, his hand reaches over, pinches, rises over the pot and rubs
            twice: grains trickle down into the broth.
        G   STIR: one more slow circle, a calm look at the pot, a blink ... = frame 0 (seamless).
Ambient (own loops, co-prime with the story): soft steam wisps curl up from the pot, rise, sway and break off
(2280 ms); the oven window's glow breathes (3100 ms).
Face: fine-line eyes only (open / half / line / look_l / look_r / look_u / look_d / sparkle); every blink is
open-half-line-half-open, at irregular times. Normal body size throughout (STYLE.md section 0).
Layers: scene (static: crate, board, stove, pot + broth, salt dish, Clawd's torso + legs + toque: he never
leaves HOME, only his arms move) | glow | face (fine eyes) | board (left arm, cleaver, carrot, coins) | spoon
(right arm, spoon, the broth's swirl, the salt pinch) | fx (flying pieces, splash, drip, grains, twinkle) |
steam.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'working-chef'
STATE = 'working (variant)'
DESC = ('Chef Clawd cooks at a little stove: stirs his soup pot, chops a carrot and flips the pieces over his '
        'toque into the pot, pulls the next carrot from the crate, tastes the soup (eyes closed ... sparkle!), '
        'adds a pinch of salt and stirs on while the pot steams.')

_SPARK = get('sparkle')


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


# =====================================================================================================
# Scenery
# =====================================================================================================
# A small chef's toque (9 wide, 5 tall; the library hat reads big at real size): two puffed lobes lit from
# the top-left over a pleated band that sits on his head's top row (his top corners stay orange).
_TOQUE = Item('toque', 'head', 'small chef toque', [Sprite([
    '..mmm.mmm..',  # y 8 lobe tops
    '.mWwwmwwwm.',  # y 9
    '.mwwwwwwMm.',  # y 10
    '..mMwMwMm..',  # y 11 pleats
    '..mwMwMwm..',  # y 12 band, on his top row
], anchor=(5, 4), name='toque')])

# Crate of carrots (x 1-8, rows 16-19) with the cutting board on top (x 1-7, row 15). Carrot ends show
# between the slats; greens peek out of the crate's open corner at x 8.
_CRATE = [
    'jjjjjjJ.',     # y 15 cutting board (light wood, shaded end)
    'TTTTTTTT',     # y 16 crate rim
    'ToToToTd',     # y 17 carrots between the slats
    'TTTTTTTd',     # y 18
    'd.....dd',     # y 19 feet
]
_CRATE_X, _CRATE_Y = 1, 15
_GREENS = [(8, 15, 'g'), (8, 14, 'G')]

# Stove (x 21-30) and the soup pot standing on it (x 22-30, rows 12-16).
_STOVE = [
    'NmmmmmmmmN',   # y 17 top plate
    'NnnnnnnnnN',   # y 18 oven door (its window glows: glow layer)
    'NnnnnnnnyN',   # y 19 knob
]
_STOVE_X, _STOVE_Y = 21, 17
_POT = [
    '.mSmmmms.',    # y 12 back rim (a glint lit from the top-left)
    'Ns.....sN',    # y 13 handles, rim sides; the broth between them
    '.rWrrrrR.',    # y 14 front lip with a glint
    '.rrrrrrR.',    # y 15
    '..RRRRR..',    # y 16
]
_POT_X, _POT_Y = 22, 12
_BROTH_Y = 13
_BROTH = (24, 28)
_POT_FRONT = {(x, y) for y in range(14, 17) for x in range(23, 30)}   # held things hide behind it

# Salt dish on the stove's left corner: a light mound in a little gray bowl.
_SALT = [(21, 16, 'm'), (22, 16, 'N'), (21, 15, 'M'), (22, 15, 'm')]

_TORSO = clawd(eyes='blink', larm='none', rarm='none')


def _scene():
    f = Frame()
    _paint(f, _CRATE, _CRATE_X, _CRATE_Y)
    for x, y, ch in _GREENS:
        f.put(x, y, ch)
    _paint(f, _STOVE, _STOVE_X, _STOVE_Y)
    _paint(f, _POT, _POT_X, _POT_Y)
    f.hline(_BROTH[0], _BROTH[1], _BROTH_Y, 'j')
    for x, y, ch in _SALT:
        f.put(x, y, ch)
    put_clawd(f, _TORSO)
    wear(f, _TOQUE, _TORSO)
    return f


# =====================================================================================================
# Clawd: arms (normal pixels) and face (fine pixels)
# =====================================================================================================
def _pose(s):
    return clawd(eyes='blink', larm=s['larm'], rarm=s['rarm'])


_TORSO_PX = None


def _arm(s, side):
    """One arm's cells (side 'l' / 'r')."""
    global _TORSO_PX
    if _TORSO_PX is None:
        t = Frame()
        put_clawd(t, _TORSO)
        _TORSO_PX = dict(t.px)
    f = Frame()
    put_clawd(f, _pose(s))
    mid = HOME[0] + 5
    return {c: ch for c, ch in f.px.items() if _TORSO_PX.get(c) != ch and ((c[0] < mid) == (side == 'l'))}


_FACE = {}


def _face(expr):
    """Only his eye pixels, in fine (half-size) pixels: the kit's fine_face expression on his solid face."""
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
# The spoon (right hand)
# =====================================================================================================
# Wooden spoon (light wood so it shows on both themes): from one cell past his grip down into the broth;
# below the front lip it is hidden by the pot. A circle seen from the side: (right arm, bowl x), the bowl
# dwelling a little longer at the sides (the timeline gives those phases more time).
_STIR = {                        # front of the pot left -> right with the hand forward ('wave'), back
    'a': ('raise', 25),          # right -> left with the hand back ('raise'): the handle draws an ellipse
    'b': ('wave', 26),
    'c': ('wave', 27),
    'd': ('wave', 28),
    'e': ('raise', 27),
    'f': ('raise', 26),
    'g': ('raise', 24),
}
_CIRCLE = 'bcdega'
_CIRCLE_MS = (150, 150, 230, 180, 230, 170)         # it dwells at the sides


def _spoon(s, p):
    """His right arm, the spoon in it (or resting in the pot), the gold swirl it stirs up, the pinch."""
    f = Frame()
    f.px.update(_arm(s, 'r'))
    sp = s['spoon']
    gx, gy = p.at('hand_r')
    if sp in _STIR:
        bx = _STIR[sp][1]
        f.line(gx - 1, gy - 1, bx, _BROTH_Y, 't')
    elif sp == 'lift':                   # up out of the broth, the bowl just over the rim
        f.line(gx - 1, gy - 2, gx + 2, gy, 't')
    elif sp == 'taste':                  # held up beside his face, the full bowl tipped toward him
        f.put(gx, gy, 't')
        f.put(gx, gy - 1, 't')
        f.put(gx - 1, gy - 2, 't')
        f.put(gx - 1, gy - 3, 'j')       # the soup in its bowl
    elif sp == 'rest':                   # leaning in the pot while his hand is at the salt dish
        f.line(22, 10, 25, _BROTH_Y, 't')
    for c in list(f.px):
        if c in _POT_FRONT:
            del f.px[c]
    if s.get('swirl') is not None:       # the gold swirl in the broth follows the spoon
        f.put(s['swirl'], _BROTH_Y, 'y')
    if s.get('pinch'):
        f.put(gx, gy, 'W' if s['pinch'] == 2 else 'M')
    return f


# =====================================================================================================
# The board (left hand): cleaver, carrot, coins
# =====================================================================================================
# The board carrot: orange x 2..(5 - chops), pointed tip at x 2.
_CARROT_Y = 14
_PILE = [(7, 14, 'o'), (6, 14, 'O'), (7, 13, 'O')]            # where each new coin comes to rest


def _carrot(f, chops, lift=0):
    end = 5 - chops
    if end < 2:
        return
    for x in range(2, end + 1):
        f.put(x, _CARROT_Y - lift, 'o')
    f.put(2, _CARROT_Y - lift, 'O')


def _blade(f, x, y):
    f.put(x, y, 'm')
    f.put(x + 1, y, 'm')
    f.put(x, y + 1, 'm')
    f.put(x + 1, y + 1, 'm')


def _cleaver(f, s, p):
    """The cleaver: a 2x2 steel blade on the cut column, a dark handle back to his grip.
    rest  = standing on its edge at the board's end (handle at row 13, where an 'up' hand takes it)
    up    = raised over the cut (cx), at his grip row; 'cock' = the same one row lower (wrist bending)
    down  = edge on the board (strike)
    flat  = lying on the board, sliding under the coins (x = its left end)
    load  = held level with the pieces on it (row = blade row)
    flick = tipped up, empty."""
    kn = s['knife']
    gx, gy = p.at('hand_l')
    if kn == 'rest':
        _blade(f, 6, 13)
        f.put(8, 13, 'd')
    elif kn in ('up', 'cock', 'down'):
        cx = s['cut']
        top = 12 if kn == 'cock' else gy             # cock: half way between aim (11) and strike (13)
        _blade(f, cx, top)
        f.hline(cx + 2, 9, top, 'd')
    elif kn == 'flat':
        x0 = s['flat']
        f.hline(x0, x0 + 2, 14, 'm')
        f.hline(x0 + 3, 8, 14, 'd')
    elif kn == 'load':
        y = s['load']
        f.hline(4, 6, y, 'm')
        f.hline(7, 9, y, 'd')
        for x, ch in ((3, 'O'), (4, 'o'), (5, 'O'), (6, 'o')):
            f.put(x, y - 1, ch)
    elif kn == 'flick':
        f.put(gx, gy, 'd')
        f.put(gx - 1, gy - 1, 'm')
        f.put(gx - 1, gy - 2, 'm')
        f.put(gx - 2, gy - 2, 'm')


def _board(s):
    """The carrot on the board, the coins, the cleaver, a carrot in his hand, his left arm."""
    f = Frame()
    p = _pose(s)
    if s['carrot'] == 'board':
        _carrot(f, s['chops'], s.get('bounce', 0))
    for x, y, ch in _PILE[:s['coins']]:
        f.put(x, y, ch)
    hop = s.get('hop')                   # the coin just cut, on its way to the pile
    if hop is not None:
        x, y, ch = hop
        f.put(x, y, ch)
    if s['knife'] == 'flat' and s['flat'] <= 3:     # the coins and the tip ride onto the blade
        for x, ch in ((3, 'O'), (4, 'o'), (5, 'O'), (6, 'o')):
            f.put(x, 13, ch)
    if s['carrot'] in ('held', 'held2'):  # pulled out of the crate by its greens
        gx, gy = p.at('hand_l')
        n = 1 if s['carrot'] == 'held' else 3
        f.put(gx, gy, 'g')
        for k in range(1, n + 1):
            f.put(gx, gy + k, 'O' if k == n else 'o')
    _cleaver(f, s, p)
    f.px.update(_arm(s, 'l'))
    return f


# =====================================================================================================
# Effects: flying pieces, splash, drip, salt grains, the 'delicious' twinkle
# =====================================================================================================
def _flight(x0, y0, x1, y1, apex, ts):
    """Points on a parabola from (x0, y0) to (x1, y1) with its top at row `apex`, at parameters ts."""
    pts = []
    for t in ts:
        x = x0 + (x1 - x0) * t
        base = y0 + (y1 - y0) * t
        lift = 4 * t * (1 - t) * (min(y0, y1) - apex)
        pts.append((int(round(x)), int(round(base - lift))))
    return pts


# spacing: wide steps near the launch and the drop, short steps around the top (it hangs a moment)
_T = (0.0, 0.12, 0.24, 0.35, 0.45, 0.53, 0.61, 0.71, 0.83, 1.0)
_FLIGHT = _flight(6, 10, 26, 13, 4, _T)
_PIECES = ('o', 'O', 'o', 'O')                           # three coins and the tip, a step apart

_SPLASH = [                                              # grows out of the broth and falls back
    [(26, 12, 'y')],
    [(25, 12, 'y'), (27, 11, 'y'), (26, 11, 'j')],
    [(24, 11, 'j'), (28, 10, 'j'), (26, 10, 'y'), (27, 12, 'y')],
    [(24, 12, 'j'), (28, 11, 'j'), (26, 11, 'y')],
    [(28, 12, 'j'), (25, 12, 'j')],
]
_RIPPLE = [(25, 'y'), (27, 'y')]


def _fx(s):
    f = Frame()
    k = s.get('fly')
    if k is not None:
        for j, ch in enumerate(_PIECES):
            i = k - j
            if 0 <= i < len(_FLIGHT) - 1:            # the last point is in the broth: gone
                x, y = _FLIGHT[i]
                f.put(x, y, ch if i % 2 == 0 else ('O' if ch == 'o' else 'o'))   # tumbling
    sp = s.get('splash')
    if sp is not None:
        for x, y, ch in _SPLASH[sp]:
            f.put(x, y, ch)
    if s.get('ripple'):
        for x, ch in _RIPPLE:
            f.put(x, _BROTH_Y, ch)
    d = s.get('drip')
    if d is not None:                    # a drip falls from the lifted spoon back into the pot
        f.put(24, (12, 13)[d], ('j', 'y')[d])
    g = s.get('grains')
    if g is not None:
        pts = [((23, 11),), ((24, 12), (23, 11)), ((24, 13), (23, 12), (24, 11)), ((24, 13),)][g]
        for x, y in pts:
            f.put(x, y, 'm')
    if s.get('spark') is not None:
        f.place(_SPARK.sprite(s['spark']), 25, 7)
    return f


# =====================================================================================================
# Master timeline
# =====================================================================================================
class _TL:
    ONCE = ('fly', 'grains', 'spark', 'splash', 'ripple', 'pinch', 'swirl', 'hop', 'drip', 'bounce')

    def __init__(self):
        self.segs = []
        self.st = dict(eyes='look_r', larm='side', rarm='raise', spoon='a', knife='rest', cut=5,
                       chops=0, coins=0, carrot='board', flat=8, load=12)

    def add(self, ms, **kw):
        once = {k: kw.pop(k) for k in list(kw) if k in self.ONCE}
        self.st.update(kw)
        s = dict(self.st)
        s.update(once)
        if s['spoon'] in _STIR and 'swirl' not in once:
            s['swirl'] = _STIR[s['spoon']][1]
        self.segs.append((int(ms), s))

    def blink(self, slow=False, **kw):
        back = self.st['eyes']
        self.add(70 if slow else 60, eyes='half', **kw)
        self.add(120 if slow else 90, eyes='line')
        self.add(70 if slow else 60, eyes='half')
        self.st['eyes'] = back

    def stir(self, scale=1.0, phases=_CIRCLE, ms=_CIRCLE_MS):
        for ph, m in zip(phases, ms):
            self.add(m * scale, spoon=ph, rarm=_STIR[ph][0])


def _timeline():
    t = _TL()
    # A  stir: two slow circles, a blink between them
    t.add(420)
    t.stir()
    t.add(180)
    t.blink()
    t.add(260)
    # B  chop: eyes first, then the hand takes the cleaver; three chops (cock, aim, strike, recoil)
    t.add(320, eyes='look_l')
    t.add(180, larm='up')                                      # takes the cleaver where it stands
    holds = (170, 230, 150)
    for k in range(3):
        cx = 5 - k
        t.add(120 if k == 0 else 140, knife='cock', cut=cx, larm='up', coins=k)  # wrist cocks (the last
        t.add(holds[k], knife='up', larm='raise')              # aim                 coin lands on the pile)
        t.add(80, knife='down', larm='up')                     # tok
        t.add(110, knife='cock', chops=k + 1, hop=(cx + 1, 13, 'o'))     # recoil, the coin hops
    t.add(200, coins=3)
    # C  aim at the pot, scoop, lift, dip, flick: over his hat into the pot
    t.add(230, eyes='look_r')                                  # where to?
    t.add(200, eyes='look_l')
    t.add(150, knife='flat', flat=5, larm='side', coins=3)     # the blade slides under the coins ...
    t.add(150, flat=3, coins=0, chops=4)                       # ... and the tip
    t.add(160, knife='load', load=13, larm='up')               # lifts them
    t.add(140, load=14, larm='side')                           # dip: wind-up
    t.add(80, knife='flick', larm='raise', fly=0)              # flick!
    t.add(90, larm='wave', fly=1)                              # follow-through
    n = len(_FLIGHT) + len(_PIECES) - 1
    for i in range(2, n):
        kw = dict(fly=i)
        if i == 3:
            kw.update(larm='raise')
        if i == 4:
            kw.update(larm='up', knife='rest', eyes='look_u')
        if i == 5:
            kw.update(larm='side')
        if i == 8:
            kw.update(eyes='look_r')
        ms = 105 if 4 <= i <= 6 else 85
        if i >= len(_FLIGHT) - 1:                              # the first piece has landed: splash
            kw['splash'] = min(i - (len(_FLIGHT) - 1), 2)
        t.add(ms, **kw)
    t.add(120, splash=3, ripple=True)
    t.add(180, splash=4, ripple=True)
    t.add(260)
    t.blink()
    t.add(120)
    # D  next carrot: eyes down at the crate, the hand dips in, pulls it up, lays it on the board
    t.add(260, eyes='look_d')
    t.add(150, larm='side')
    t.add(190, larm='down')
    t.add(140, larm='side', carrot='held')
    t.add(170, larm='up', carrot='held2', eyes='look_l')
    t.add(150, larm='out', carrot='board', chops=0, bounce=1)
    t.add(130, carrot='board')
    t.add(330, larm='side')
    # E  taste: eyes on the spoon, lift it out (a drip), beside his face, slow close ... sparkle
    t.add(260, eyes='look_r')
    t.add(160, spoon='g', rarm='raise')
    t.add(170, spoon='lift', rarm='raise', drip=0)
    t.add(120, drip=1)
    t.add(170, rarm='up', spoon='taste')
    t.add(120, eyes='half')
    t.add(680, eyes='line')
    t.add(120, eyes='half')
    t.add(150, eyes='open')
    t.add(110, eyes='sparkle', spark=0)
    t.add(110, spark=1)
    t.add(230, spark=2)
    t.add(140, spark=3)
    t.add(110, spark=0)
    t.add(320)
    t.add(160, eyes='look_r', rarm='raise', spoon='lift')
    t.add(160, spoon='g')
    t.add(170, spoon='a')
    # F  salt: eyes on the dish, reach, pinch, over the pot, two rubs: grains trickle in
    t.add(240, eyes='look_d')
    t.add(150, rarm='out', spoon='rest')
    t.add(260, rarm='side', pinch=2)
    t.add(140, rarm='up', pinch=2, eyes='look_r')
    t.add(170, rarm='wave', pinch=2)
    t.add(120, rarm='raise', grains=0)
    t.add(120, rarm='wave', grains=1)
    t.add(110, grains=2)
    t.add(120, rarm='raise', grains=3)
    t.add(260)
    t.add(160, rarm='raise', spoon='a')
    # G  one more slow circle, a calm look, a blink, home
    t.add(160)
    t.stir(1.15)
    t.add(320)
    t.blink(slow=True)
    t.add(380)
    return t


# =====================================================================================================
# Ambient layers
# =====================================================================================================
_STEAM = get('steam')


def _steam():
    """Two soft wisps (the library's S-curve wisp: it leaves the broth, sways up and breaks off), the
    second three frames behind the first, slow."""
    n = len(_STEAM)
    frames = []
    for i in range(n):
        f = Frame()
        f.place(_STEAM.sprite(i), 25, 9)
        f.place(_STEAM.sprite((i + 3) % n), 28, 8)
        frames.append((f, 380))
    return frames


def _glow():
    """The oven window's glow breathes: dim, warming, bright, cooling."""
    out = []
    for cols, ms in (('OOOOO', 1300), ('oOoOo', 700), ('ooooy', 1100)):
        f = Frame()
        for i, ch in enumerate(cols):
            f.put(27 - i, 18, ch)
        out.append((f, ms))
    return out


def build():
    t = _timeline()
    face, spoon, board, fx = [], [], [], []
    for ms, s in t.segs:
        p = _pose(s)
        face.append((_face(s['eyes']), ms))
        spoon.append((_spoon(s, p), ms))
        board.append((_board(s), ms))
        fx.append((_fx(s), ms))
    return anim(NAME, DESC, [
        static('scene', _scene()),
        layer('glow', _glow()),
        layer('face', face),
        layer('board', board),
        layer('spoon', spoon),
        layer('fx', fx),
        layer('steam', _steam()),
    ], state=STATE)
