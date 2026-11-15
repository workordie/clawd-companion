"""thinking-cube - Thinking variant: solving a colour-twist puzzle cube.   5-90 s on screen: calm, one payoff.

STORYBOARD   (one loop = 16.20 s; story() is the single beat list every layer is cut from)
  0.00  frame 0 (the reduced-motion still): Clawd at HOME holding a scrambled 3x3 colour cube in both claws in front
        of his belly, eyes down on it.  1.20 blink
  1.99  TWIST, bottom row to the right: his left claw drops to the bottom row (reach), pushes, and the row's colours
        ROLL round a sticker a frame (two in-betweens, then the quarter turn settles) and the claw lets go
  3.39  he studies it; TWIST, right column up: his right claw rolls it, the column's colours climb into the top edge
  4.45  blink; 5.00 he TURNS THE WHOLE CUBE round: both claws shift their grip, every row rolls a sticker, a
        corner-on view (half front, half side in shade), and the other side settles in his claws
  6.36  a long doubtful half-lid .. 7.46 a glance at you .. 8.06 back to it
  8.44  a quick FLURRY of four twists (middle row, column down, top row, column down; each still a full roll, just
        quicker) ... 9.89 SOLVED: green front, yellow top, blue side.  10.03 his eyes go wide and a glint sweeps
        across the solved face
 10.53  his eyes go up first, then PAYOFF: he lifts it onto his raised claw (eased: small, big, small moves), a
        twinkle grows and fades beside it, sparkle eyes (11.29); 12.07 a blink, and he looks at you
 12.97  his eyes drop, he lowers it back into both claws (eased); 13.70 blink
 14.35  the flick: the cube dips in his claws as his eyes go up (anticipation), he tosses it; it rises fast, slows
        to its apex, tumbling (corner, back, upside down ...) as its colours fly, falls faster, and he catches it
        (15.26) with a dip of his claws that settles (15.38): scrambled again -> frame 0
Eye closures: 1.20, 4.45, 12.07, 13.70 s and the doubtful half-lid at 6.36 s (irregular gaps).
The cube is a real 54-sticker model; the scramble is SOLVED with the story's seven moves undone (a search chose them
for a well-mixed start), so the flurry always ends solved.

Face: the kit's fine-line eyes (fine() + fine_face(): open / half / line / look_d / look_u / wide / sparkle).  No mouth,
no blush, never resized: his body never moves (the trunk is one static layer); only his arms, eyes and the cube do.
Holding pose: both arms come in front of his belly in body_shade ('@', the kit's convention for a limb crossing his
body), the claws on the cube's sides.
Layers (back to front): trunk (static: body, legs; solid face) | arms (both arms) | cube | face (FINE: only his eye
pixels) | fx (the twinkle, the glint on the solved face).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'thinking-cube'
STATE = 'thinking (variant)'
DESC = ('Puzzles over a colour-twist cube held in both claws: twists a row, studies it, turns it round, glances at '
        'you, then a quick flurry of twists solves it and he holds it up with a twinkle, before a little toss '
        'scrambles it again.')

HX, HY = HOME

# --------------------------------------------------------------------------------------------
# the cube: a real 3x3x3 sticker model (54 stickers: position and normal in {-1, 0, 1}^3, x right, y up, z toward
# you), turned a layer at a time.  A quarter turn is animated as a short marquee: the 12 stickers round the turning
# row (or column) roll by one per frame, so a twist reads as the colours rolling round.  Drawn as an oblique 4x4 view:
# the front 3x3, the top face's front edge above it (shifted right) and the right face's front column (top and middle)
# beside it, in shade.
# --------------------------------------------------------------------------------------------
SHADE = {'r': 'R', 'y': 'j', 'b': 'B', 'g': 'G'}
FACES = {(0, 0, 1): 'g', (1, 0, 0): 'b', (0, 1, 0): 'y', (0, 0, -1): 'r', (-1, 0, 0): 'y', (0, -1, 0): 'b'}


def _solved():
    st = []
    for n, c in FACES.items():
        ax = [i for i in range(3) if n[i]][0]
        others = [i for i in range(3) if i != ax]
        for u in (-1, 0, 1):
            for v in (-1, 0, 1):
                p = list(n)
                p[others[0]], p[others[1]] = u, v
                st.append((tuple(p), n, c))
    return tuple(sorted(st))


SOLVED = _solved()


def _rot(v, axis, q):
    """Rotate a vector q quarter turns about `axis`.  y, q=+1: the front row moves left (x, z) -> (-z, x).
    x, q=+1: the front column moves up (y, z) -> (z, -y)."""
    x, y, z = v
    for _ in range(q % 4):
        if axis == 1:
            x, z = -z, x
        else:
            y, z = z, -y
    return (x, y, z)


def move(st, axis, layer, q):
    """Quarter-turn (q = +-1, or more) every sticker whose position has pos[axis] == layer; layer None = the whole cube."""
    out = []
    for p, n, c in st:
        if layer is None or p[axis] == layer:
            p, n = _rot(p, axis, q), _rot(n, axis, q)
        out.append((p, n, c))
    return tuple(sorted(out))


def _get(st):
    return {(p, n): c for p, n, c in st}


def view(st):
    """The visible stickers: front rows (top to bottom, left to right), the top face's front edge, the side column."""
    g = _get(st)
    front = [''.join(g[((x, y, 1), (0, 0, 1))] for x in (-1, 0, 1)) for y in (1, 0, -1)]
    top = ''.join(g[((x, 1, 1), (0, 1, 0))] for x in (-1, 0, 1))
    side = ''.join(g[((1, y, 1), (1, 0, 0))] for y in (1, 0))
    return front, top, side


def ring(st, axis, layer):
    """The 12 stickers round a turning row (axis y) or column (axis x), starting with the visible front ones."""
    g = _get(st)
    if axis == 1:                       # row y = layer: front L->R, right front->back, back R->L, left back->front
        y = layer
        return ([g[((x, y, 1), (0, 0, 1))] for x in (-1, 0, 1)] + [g[((1, y, z), (1, 0, 0))] for z in (1, 0, -1)] +
                [g[((x, y, -1), (0, 0, -1))] for x in (1, 0, -1)] + [g[((-1, y, z), (-1, 0, 0))] for z in (-1, 0, 1)])
    x = layer                           # column x = layer: front bottom->top, top front->back, back top->bottom, bottom
    return ([g[((x, y, 1), (0, 0, 1))] for y in (-1, 0, 1)] + [g[((x, 1, z), (0, 1, 0))] for z in (1, 0, -1)] +
            [g[((x, y, -1), (0, 0, -1))] for y in (1, 0, -1)] + [g[((x, -1, z), (0, -1, 0))] for z in (-1, 0, 1)])


def picture(front, top, side):
    return {'front': list(front), 'top': top, 'side': side}


def pic(st):
    return picture(*view(st))


def inbetween(st, axis, layer, q, k):
    """The picture k stickers (1 or 2) into a quarter turn: the turning row/column's colours rolled by k."""
    pc = pic(st)
    r = ring(st, axis, layer)
    s = k if q > 0 else -k
    rr = r[s:] + r[:s]
    if axis == 1:
        row = 1 - layer
        pc['front'][row] = ''.join(rr[0:3])
        if row < 2:
            pc['side'] = pc['side'][:row] + rr[3] + pc['side'][row + 1:]
    else:
        col = layer + 1
        for i, y in enumerate((2, 1, 0)):              # front rows bottom->top
            f = pc['front'][y]
            pc['front'][y] = f[:col] + rr[i] + f[col + 1:]
        pc['top'] = pc['top'][:col] + rr[3] + pc['top'][col + 1:]
    return pc


def corner_cells(st):
    """The cube two thirds into a quarter turn of the whole cube: every row's ring rolled by two, the right half in
    shade (it is turning away), the top face's right edge swinging round on top."""
    g = _get(st)
    d = {}
    for y, ly in enumerate((1, 0, -1)):
        r = ring(st, 1, ly)
        d[(0, y)], d[(1, y)], d[(2, y)], d[(3, y)] = r[2], r[3], SHADE[r[4]], SHADE[r[5]]
    for x, z in enumerate((1, 1, 0, -1)):
        d[(x, -1)] = g[((1 if x else 0, 1, z), (0, 1, 0))]
    return d


def cube_cells(pc, view_='front'):
    """{(x, y): colour} relative to the front face's top-left sticker (the top edge is row -1).
    view_: 'front' | 'corner' (turned 45 deg) | 'back' (mirrored) | 'flip' (upside down, while it tumbles)."""
    fr, top, side = pc['front'], pc['top'], pc['side']
    d = {}
    if view_ == 'corner':
        for x, c in enumerate(top[1:] + top[2] + top[2]):
            d[(x, -1)] = c
        for y in range(3):
            sc = side[min(y, 1)]
            d[(0, y)], d[(1, y)], d[(2, y)], d[(3, y)] = fr[y][1], fr[y][2], SHADE[sc], SHADE[sc]
        return d
    for y in range(3):
        for x in range(3):
            d[(x, y)] = fr[y][x]
    for y in range(2):
        d[(3, y)] = SHADE[side[y]]
    for x in range(3):
        d[(x + 1, -1)] = top[x]
    if view_ == 'back':
        d = {(3 - x, y): c for (x, y), c in d.items()}
    elif view_ == 'flip':
        d = {(x, 1 - y): c for (x, y), c in d.items()}
    return d


# the moves of the story, in order: (axis, layer, q); 'turn' = the whole cube.  The scramble is SOLVED with them
# undone, so the flurry always ends solved.
TWISTS = [(1, -1, -1),         # bottom row to the right (left claw)
          (0, 1, 1),            # right column up (right claw)
          ('turn',),            # the whole cube turned round
          (1, 0, -1),           # flurry: middle row to the right (left claw)
          (0, 1, -1),           #         right column down (right claw)
          (1, 1, 1),            #         top row to the left (right claw)
          (0, 1, -1)]           #         right column down: solved (a search picked these for a well-mixed scramble)


def _apply(st, m, sign=1):
    if m[0] == 'turn':
        return move(st, 1, None, sign)
    return move(st, m[0], m[1], sign * m[2])


SCRAMBLED = SOLVED
for _m in reversed(TWISTS):
    SCRAMBLED = _apply(SCRAMBLED, _m, -1)

CUBE_AT = (14, 16)                    # where the front face's top-left sticker sits while he holds it
TUMBLE = [picture(('ryb', 'gyr', 'byg'), 'bgr', 'yr'), picture(('gbr', 'ryg', 'ybr'), 'ryb', 'gb')]


# --------------------------------------------------------------------------------------------
# Clawd: static trunk + both arms.  Holding arms reach in front of his belly in body_shade ('@').
# --------------------------------------------------------------------------------------------
_SH = (10, 15, '#'), (20, 15, '#')    # the shoulders (arm stubs at his sides)
ARMS = {
    'L':     [_SH[0], (11, 16, '@'), (12, 17, '@'), (13, 17, '@')],           # left claw on the middle row
    'Lbot':  [_SH[0], (11, 16, '@'), (12, 17, '@'), (13, 18, '@')],           # ... on the bottom row
    'Lpush': [_SH[0], (11, 16, '@'), (12, 17, '@'), (13, 18, '@'), (14, 18, '@')],   # pushing the bottom row right
    'Lmidp': [_SH[0], (11, 16, '@'), (12, 17, '@'), (13, 17, '@'), (14, 17, '@')],   # pushing the middle row right
    'Lhi':   [_SH[0], (11, 16, '@'), (12, 16, '@'), (13, 16, '@')],           # holding it a row higher
    'R':     [_SH[1], (19, 16, '@'), (18, 17, '@')],                          # right claw on the side, middle row
    'Rtop':  [_SH[1], (19, 16, '@'), (18, 16, '@')],                          # ... on the top row
    'Rpush': [_SH[1], (19, 16, '@'), (18, 16, '@'), (17, 16, '@')],           # pushing the top row left
    'Rboth': [_SH[1], (19, 16, '@'), (18, 16, '@'), (17, 17, '@')],           # turning the whole cube (top + middle)
    'Rhi':   [_SH[1], (19, 15, '@'), (18, 15, '@')],                          # holding it a row higher
    'Rlift': [_SH[1], (19, 15, '@')],                                         # lifting it alone, up and right
}
for _side, _key in (('l', 'larm'), ('r', 'rarm')):
    _bare = {(x, y) for x, y, _ in clawd(eyes='blink', larm='none', rarm='none').sprite.cells}
    for _k in ('side', 'up', 'raise', 'down'):
        _p = clawd(eyes='blink', **{_key: _k, ('rarm' if _key == 'larm' else 'larm'): 'none'})
        ARMS[_side + ':' + _k] = [(HX + x, HY + y, c) for x, y, c in _p.sprite.cells if (x, y) not in _bare]


def trunk():
    f = Frame()
    put_clawd(f, clawd(eyes='blink', larm='none', rarm='none'))
    return f


def arms(s):
    f = Frame()
    for k in (s['larm'], s['rarm']):
        for x, y, c in ARMS[k]:
            f.put(x, y, c)
    return f


def cube(s):
    f = Frame()
    ax, ay = s['at']
    if isinstance(s['cube'], dict) and 'cells' in s['cube']:
        cells = s['cube']['cells']
    else:
        pc = s['cube'] if isinstance(s['cube'], dict) else pic(s['cube'])
        cells = cube_cells(pc, s['view'])
    for (x, y), c in cells.items():
        f.put(ax + x, ay + y, c)
    return f


_EYE_POSE = clawd(eyes='blink')


def face(s):
    """FINE layer: only the half-size eye pixels that differ from his solid face."""
    f = Frame()
    put_clawd(f, _EYE_POSE)
    base = fine(f)
    ff = fine_face(base.copy(), _EYE_POSE, HX, HY, s['face'])
    out = Frame(res=2)
    for q, v in ff.px.items():
        if base.px.get(q) != v:
            out.px[q] = v
    out.meta = {'fine_face': [s['face']]}
    return out


# --------------------------------------------------------------------------------------------
# effects: the twinkle (grows in, fades out) and a glint sweeping across the solved face (mint on green)
# --------------------------------------------------------------------------------------------
TWINKLE = [
    Sprite(['j'], anchor=(0, 0)),
    Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1)),
    Sprite(['...j...', '...j...', '..jyj..', 'jjyWyjj', '..jyj..', '...j...', '...j...'], anchor=(3, 3)),
    Sprite(['..j..', '..j..', 'jjyjj', '..j..', '..j..'], anchor=(2, 2)),
]
TW_AT = (26, 6)
GLINT = [[(0, 0)], [(1, 0), (0, 1)], [(2, 0), (1, 1), (0, 2)], [(2, 1), (1, 2)], [(2, 2)]]   # a diagonal sweep


def fx(s):
    f = Frame()
    for item in s['fx']:
        if item[0] == 'tw':
            f.place(TWINKLE[item[1]], *TW_AT)
        else:                                          # ('glint', k): over the front face at CUBE_AT
            for x, y in GLINT[item[1]]:
                f.put(CUBE_AT[0] + x, CUBE_AT[1] + y, 'h')
    return f


# --------------------------------------------------------------------------------------------
# the story
# --------------------------------------------------------------------------------------------
DOWN = 'look_d'
# which claw turns what: (reach, push, back) arm poses
CLAWS = {
    (1, 1):  (dict(rarm='Rtop'), dict(rarm='Rpush'), dict(rarm='R')),               # top row, right claw pushing left
    (1, 0):  (dict(rarm='Rtop'), dict(larm='Lmidp'), dict(larm='L', rarm='R')),     # middle row, left claw pushing right
    (1, -1): (dict(larm='Lbot'), dict(larm='Lpush'), dict(larm='L')),               # bottom row, left claw pushing right
    (0, 1):  (dict(rarm='R'), dict(rarm='Rtop'), dict(rarm='R')),                   # right column: the claw rolls it up
}


def story():
    S = []
    st = dict(cube=SCRAMBLED, view='front', at=CUBE_AT, larm='L', rarm='R', face=DOWN, fx=())
    moves = list(TWISTS)

    def b(ms, **kw):
        kw.setdefault('fx', ())
        st.update(kw)
        S.append((ms, dict(st)))

    def blink(after, eyes=None):
        eyes = eyes or st['face']
        b(70, face='half')
        b(90, face='line')
        b(70, face='half')
        b(after, face=eyes)

    def twist(ms=(150, 90, 90, 110, 200)):
        """A quarter turn: the claw reaches, pushes, the row's (column's) colours roll round one sticker per frame,
        it settles, the claw lets go."""
        axis, layer, q = moves.pop(0)
        reach, push, back = CLAWS[(axis, layer)]
        if axis == 0 and q < 0:                                        # ... or down
            reach, push = dict(rarm='Rtop'), dict(rarm='R')
        start = st['cube']
        if ms[0]:
            b(ms[0], **reach)
        b(ms[1], cube=inbetween(start, axis, layer, q, 1), **push)
        b(ms[2], cube=inbetween(start, axis, layer, q, 2))
        b(ms[3], cube=move(start, axis, layer, q), **reach)
        if ms[4]:
            b(ms[4], **back)

    # ---- frame 0: studying the scrambled cube ------------------------------------------------
    b(1200)
    blink(560)
    # ---- a twist of the bottom row; study; a twist of the right column --------------------------
    twist()
    b(760)
    twist()
    b(420)
    blink(320)
    # ---- turn the whole cube round: the side face swings to the front -------------------------
    moves.pop(0)
    start = st['cube']
    b(150, rarm='Rtop', larm='Lhi')                                    # both claws shift their grip
    roll1 = pic(start)
    for y in (1, 0, -1):
        roll1['front'][1 - y] = inbetween(start, 1, y, 1, 1)['front'][1 - y]
    roll1['side'] = ''.join(inbetween(start, 1, y, 1, 1)['side'][1 - y] for y in (1, 0))
    b(110, rarm='Rboth', cube=roll1)
    b(150, cube=dict(cells=corner_cells(start)))
    b(170, view='front', cube=move(start, 1, None, 1), rarm='Rtop')
    b(220, rarm='R', larm='L')
    b(560)
    # ---- doubt; a glance at you -----------------------------------------------------------------
    b(90, face='half')
    b(700)
    b(90, face=DOWN)
    b(220)
    b(600, face='open')
    b(380, face=DOWN)
    # ---- the flurry: quicker twists, every one still a full roll ---------------------------------
    twist((110, 70, 70, 90, 0))
    twist((90, 70, 70, 90, 0))
    twist((90, 70, 70, 90, 0))
    twist((90, 70, 70, 100, 140))
    if st['cube'] != SOLVED:
        raise ValueError('the flurry should end solved')
    b(140)
    b(130, face='wide', fx=(('glint', 0),))
    b(90, fx=(('glint', 1),))
    b(90, fx=(('glint', 2),))
    b(90, fx=(('glint', 3),))
    b(100, fx=(('glint', 4),))
    b(160, face='look_u')                                              # his eyes go up first ...
    # ---- payoff: lift it onto his raised claw (eased), twinkle, sparkle eyes, at you --------------
    b(130, larm='l:side', rarm='Rlift', at=(15, 14), face='look_u')
    b(100, rarm='r:up', at=(18, 10))
    b(140, rarm='r:raise', at=(20, 9))
    b(120, fx=(('tw', 0),))
    b(110, fx=(('tw', 1),))
    b(110, face='sparkle', fx=(('tw', 2),))
    b(260, fx=(('tw', 3),))
    b(130, fx=(('tw', 1),))
    b(120, fx=(('tw', 0),))
    b(160)
    blink(670, 'open')                                                 # a blink, and at you: got it
    # ---- lower it (eased), blink, then the flick: a little toss scrambles it -----------------------------
    b(110, face=DOWN)
    b(140, rarm='r:up', at=(18, 10))
    b(110, rarm='Rlift', at=(15, 14))
    b(150, larm='Lhi', rarm='Rhi', at=(14, 15))
    b(220, larm='L', rarm='R', at=CUBE_AT)
    blink(420, DOWN)
    b(160, larm='Lbot', at=(14, 17), face='look_u')                    # anticipation: the cube dips, his eyes go up
    b(80, larm='l:up', rarm='r:up', at=(14, 13), view='corner', face='look_u', cube=TUMBLE[0])   # flick: fast ...
    b(90, at=(14, 10), view='back', cube=TUMBLE[1])
    b(120, at=(14, 8), view='flip', cube=TUMBLE[0])
    b(170, at=(14, 7), view='corner', cube=TUMBLE[1])                  # ... slowing to the apex
    b(120, at=(14, 8), view='back', cube=TUMBLE[0])
    b(90, at=(14, 10), view='flip', cube=TUMBLE[1], face=DOWN)
    b(80, at=(14, 13), view='corner', cube=SCRAMBLED)                  # ... falling faster
    b(120, larm='Lbot', rarm='R', at=(14, 17), view='front')           # caught: the claws give a little
    b(180, larm='L', at=CUBE_AT)                                       # and settle
    b(640)
    return S


def build():
    S = story()
    return anim(NAME, DESC, [
        static('trunk', trunk()),
        layer('arms', [(arms(s), ms) for ms, s in S]),
        layer('cube', [(cube(s), ms) for ms, s in S]),
        layer('face', [(face(s), ms) for ms, s in S]),
        layer('fx', [(fx(s), ms) for ms, s in S]),
    ], state=STATE)
