"""thinking-chalk - Thinking variant: working a sum out on a little chalkboard.   5-90 s on screen: calm, one payoff.

STORYBOARD   (one loop = 17.85 s; every layer but the board is cut from one beat list, story())
  0.00  frame 0 (the reduced-motion still): Clawd at HOME beside a green chalkboard (wooden frame lit from the
        top-left, tray ledge, little feet), a stick of chalk raised against its edge, eyes on the clean board.
        0.95 blink
  1.60  A  "1+1": his eyes go up first, then the claw: from where he stands he chalks the first "1" (1.95 - 2.11);
        he shuffles along the board a cell a beat (2.51 / 2.71 / 2.87, the claw rising as he lands) and chalks the
        "+" (stem down, then the bar, 3.24 - 3.75); one more step (4.11) and the second "1" (4.55 / 4.71).  The line
        is above his head, so nothing hides it; in every writing frame the chalk tip is on the newest chalk cell
        (build() asserts it).
  5.10  B  a blink carries his eyes down to the space below; he chalks the answer in tallies RIGHT TO LEFT while
        stepping back along the board (5.57, 6.44, 7.42), so his arm never crosses a stroke he has already written.
  7.88  C  III?  a slow, doubtful half-lid (8.20), a look at you (9.14), back; the claw draws back and down
        (wind-up) and taps the chalk twice on the nearest stroke (10.02)
 10.57  D  he rubs that stroke out with his claw (up, down, up), a puff of chalk dust swelling then thinning away
        as it rises; a pale-green ghost is left.  II.  11.71 blink
 12.16  E  one step on, the claw dips (wind-up) and underlines the II in three beats; a gold twinkle grows in above
        the board (13.02), wide eyes, then the shine is in his eyes (sparkle) as he looks at you; blink, back to it
 15.29  F  he wipes the board in eased sweeps, stepping back along it (answer, top line, first "1"), each sweep
        leaving a pale smear for a beat and a puff of dust that rises and thins; home, the last dust settles, a
        glance at you, back to the clean board -> frame 0
Eye closures: 0.95, 5.10, 11.71, 14.72 s, and the doubtful half-lid at 8.20 s.

Face: the kit's fine-line eyes (fine() + fine_face(): open / half / line / look_r / look_u / wide / sparkle); his gaze
always moves a beat before his claw.  No mouth, no blush, normal body size (he steps with the kit's walk legs).
His right arm uses the kit shapes plus three hand-drawn 3-cell ones at the same scale: 'low' (reaching down-right to
the tray line) and 'pt_u' / 'pt_d' (the pointing arm with its claw tilted up / down, for rubbing).
Layers (back to front): board (static) | sum, answer (the chalk on the slate, two bands of rows) | trunk (Clawd minus his right arm; changes only
when he steps) | arm (right arm + chalk stick) | face (FINE: only his eye pixels) | fx (dust, twinkle).  All but the
board are cut from one beat list, so they always agree.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'thinking-chalk'
STATE = 'thinking (variant)'
DESC = ('Works a sum out on a little chalkboard: chalks "1+1" and tallies III, doubts it, taps the board, rubs one '
        'stroke out in a puff of chalk dust, underlines the II with a twinkle, then wipes the board clean for the next one.')

HX, HY = HOME

# --------------------------------------------------------------------------------------------
# the chalkboard (right of Clawd): wooden frame, green slate, a tray ledge and two little feet
# --------------------------------------------------------------------------------------------
BX0, BY0, BX1, BY1 = 21, 7, 30, 18            # outer frame; the slate is x 22-29, rows 8-17; row 18 = tray


def _board():
    f = Frame()
    f.rect(BX0 + 1, BY0 + 1, BX1 - BX0 - 1, BY1 - BY0 - 1, 'G')     # slate
    f.hline(BX0, BX1 - 1, BY0, 't')                                 # top rail, lit
    f.vline(BX0, BY0 + 1, BY1 - 1, 't')                             # left rail, lit
    f.vline(BX1, BY0, BY1 - 1, 'T')                                 # right rail, in shade
    f.hline(BX0, BX1, BY1, 'T')                                     # the tray ledge
    f.put(BX0, BY1, 't')
    for x in (22, 23, 28, 29):                                       # two little feet
        f.put(x, GROUND, 'd' if x in (23, 29) else 'T')
    return f


# chalk on the slate (absolute cells)
ONE_A = [(22, 9), (22, 10), (22, 11)]
STEM = [(25, 9), (25, 10), (25, 11)]
BAR = [(24, 10), (25, 10), (26, 10)]
ONE_B = [(28, 9), (28, 10), (28, 11)]
T3 = [(27, 13), (27, 14), (27, 15)]           # the tallies, written right to left
T2 = [(25, 13), (25, 14), (25, 15)]
T1 = [(23, 13), (23, 14), (23, 15)]           # ... one too many: rubbed out
UNDER = [(24, 17), (25, 17), (26, 17), (27, 17)]
GHOST = [(23, 13), (23, 15)]                  # what the rub leaves of T1 (pale green)


# --------------------------------------------------------------------------------------------
# Clawd's right arm: cells relative to his shoulder (arm column, arm row) and the grip point of the chalk
# --------------------------------------------------------------------------------------------
_G = GEOM['normal']
ARMS = {
    'side':  ([(0, 0), (0, 1)], (1, 1)),
    'up':    ([(0, -1), (0, 0)], (1, -1)),
    'down':  ([(0, 1), (0, 2)], (1, 2)),
    'high':  ([(0, 0), (0, -1), (0, -2)], (0, -3)),
    'raise': ([(0, 0), (1, -1), (1, -2)], (1, -3)),
    'wave':  ([(0, 0), (1, -1), (2, -2)], (2, -3)),
    'out':   ([(0, 0), (1, 0)], (2, 0)),
    'point': ([(0, 0), (1, 0), (2, 0)], (3, 0)),
    'low':   ([(0, 0), (1, 1), (2, 2)], (3, 3)),          # hand-drawn: reaching down-right to the tray line
    'pt_u':  ([(0, 0), (1, 0), (2, -1)], None),           # hand-drawn: pointing, claw tilted up (rubbing)
    'pt_d':  ([(0, 0), (1, 0), (2, 1)], None),            # hand-drawn: pointing, claw tilted down (rubbing)
}
DIRS = {'u': (0, -1), 'ur': (1, -1), 'r': (1, 0), 'dr': (1, 1), 'd': (0, 1)}


def _shoulder(dx):
    return HX + _G['ax'][1] + dx, HY + _G['ay']


def arm_cells(s):
    sx, sy = _shoulder(s['dx'])
    return [(sx + x, sy + y) for x, y in ARMS[s['arm']][0]]


def chalk_cells(s):
    """The chalk stick: from the grip point just outside his claw, n cells in direction d (the tip is last)."""
    if not s['chalk']:
        return []
    d, n = s['chalk']
    sx, sy = _shoulder(s['dx'])
    gx, gy = ARMS[s['arm']][1]
    ddx, ddy = DIRS[d]
    return [(sx + gx + ddx * i, sy + gy + ddy * i) for i in range(n)]


def _pose(s):
    """The kit pose (for put_clawd and the eyes): the right arm is drawn by the arm layer."""
    return clawd(eyes='blink', larm='side', rarm='none', legs=s['legs'])


def _at(s):
    return HX + s['dx'], HY


def trunk(s):
    f = Frame()
    put_clawd(f, _pose(s), *_at(s))
    return f


def arm(s):
    f = Frame()
    for x, y in arm_cells(s):
        f.put(x, y, '#')
    for x, y in chalk_cells(s):
        f.put(x, y, 'w')
    return f


def face(s):
    """FINE layer: only the half-size eye pixels that differ from his solid-faced body."""
    p = _pose(s)
    x, y = _at(s)
    f = Frame()
    put_clawd(f, p, x, y)
    base = fine(f)
    ff = fine_face(base.copy(), p, x, y, s['face'])
    out = Frame(res=2)
    for q, v in ff.px.items():
        if base.px.get(q) != v:
            out.px[q] = v
    out.meta = {'fine_face': [s['face']]}
    return out


def marks(s, rows):
    """The chalk on the slate, one band of rows (the "1+1" line and the answer area are separate layers, so each
    frame only carries the band that changed)."""
    f = Frame()
    for x, y in s['ghost']:
        if y in rows:
            f.put(x, y, 'g')
    for x, y in s['marks']:
        if y in rows:
            f.put(x, y, 'w')
    return f


# --------------------------------------------------------------------------------------------
# effects: chalk dust (grows in, swells, thins away) and the twinkle (grows in, fades out)
# --------------------------------------------------------------------------------------------
DUST = [
    Sprite(['M', 'm'], anchor=(0, 1)),                                   # 0 a first wisp
    Sprite(['.M.', 'MMm', '.m.'], anchor=(1, 1)),                        # 1 a puff
    Sprite(['.MM.', 'MMMm', '.mm.'], anchor=(1, 1)),                     # 2 swelling
    Sprite(['.m.m', 'm.m.', '..m.'], anchor=(1, 1)),                     # 3 thinning
    Sprite(['m..m', '.m..'], anchor=(1, 1)),                             # 4 specks
    Sprite(['..m'], anchor=(1, 0)),                                      # 5 the last speck
]
TWINKLE = [
    Sprite(['j'], anchor=(0, 0)),
    Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1)),
    Sprite(['...j...', '...j...', '..jyj..', 'jjyWyjj', '..jyj..', '...j...', '...j...'], anchor=(3, 3)),
    Sprite(['..j..', '..j..', 'jjyjj', '..j..', '..j..'], anchor=(2, 2)),
]
TW_AT = (27, 4)


def fx(s):
    f = Frame()
    for kind, k, x, y in s['fx']:
        f.place(DUST[k] if kind == 'dust' else TWINKLE[k], x, y)
    return f


def tw(k):
    return ('tw', k) + TW_AT


def dust(k, x, y):
    return ('dust', k, x, y)


# --------------------------------------------------------------------------------------------
# the story: beats carry their state forward (fx resets every beat).  write=cell asserts the chalk tip is on it.
# --------------------------------------------------------------------------------------------
LOOK, UP = 'look_r', 'look_u'
REST = dict(arm='up', chalk=('ur', 2))        # the chalk raised against the board's edge (at HOME)
REST_IN = dict(arm='up', chalk=('u', 2))      # in front of the board: held upright, clear of the chalk marks


def story():
    S = []
    st = dict(dx=0, legs='stand', face=LOOK, marks=(), ghost=(), fx=(), tag=None, **REST)

    def b(ms, write=None, tag=None, **kw):
        kw.setdefault('fx', ())
        st.update(kw)
        if write is not None:
            tip = chalk_cells(st)[-1]
            if tip != write:
                raise ValueError('chalk tip %r is not on the chalk cell %r (%s)' % (tip, write, st['arm']))
            if write not in st['marks']:
                st['marks'] = st['marks'] + (write,)
        S.append((ms, dict(st, tag=tag)))

    def blink(after, eyes=None, tag=None):
        eyes = eyes or st['face']
        b(70, face='half', tag=tag)
        b(90, face='line')
        b(70, face='half')
        b(after, face=eyes)

    # ---- frame 0: beside a clean board, chalk raised: where to start? -------------------------------
    b(950, tag='f0')
    blink(420)
    # ---- A: "1+1" (his eyes go up first) -------------------------------------------------------------------
    b(240, face=UP, tag='A')
    b(110, arm='raise')                                  # the claw comes up (the chalk touches the slate)
    b(160, arm='high', chalk=('ur', 3), write=(22, 9))   # the first "1", top to bottom
    b(200, arm='raise', chalk=('r', 2), write=(22, 11), marks=st['marks'] + ((22, 10),))
    b(200, **REST)
    b(200, dx=1, legs='walk_a')                          # shuffle along, a cell a beat (slow, quick, settle)
    b(160, dx=2, legs='walk_b')
    b(370, dx=3, legs='stand', arm='raise')              # lands, the claw rising to the board
    b(160, arm='high', chalk=('ur', 3), write=(25, 9))   # the "+": stem down ...
    b(190, arm='raise', chalk=('r', 2), write=(25, 11), marks=st['marks'] + ((25, 10),))
    b(160, arm='high', chalk=('ur', 2), write=(24, 10))   # ... then the bar, left to right
    b(170, arm='wave', write=(26, 10))
    b(190, **REST_IN)
    b(440, dx=4, legs='stand', arm='raise')              # one step on, the claw already rising
    b(160, arm='wave', chalk=('ur', 3), write=(28, 9))   # the second "1" (a long reach: the chalk at full length)
    b(170, chalk=('r', 3), write=(28, 11), marks=st['marks'] + ((28, 10),))
    b(220, **REST_IN)
    # ---- B: the answer, in tallies, right to left as he steps back ------------------------------------
    blink(240, LOOK, tag='B')                            # a blink carries his eyes down to the space below
    b(130, arm='out', chalk=('ur', 2), write=(27, 13))   # the far one: the chalk tilts down the stroke
    b(180, chalk=('dr', 2), write=(27, 15), marks=st['marks'] + ((27, 14),))
    b(210, **REST_IN)
    b(220, dx=3, legs='walk_a')
    b(130, legs='stand')
    for x, dx in ((25, 3), (23, 1)):
        if dx == 1:
            b(210, dx=2, legs='walk_b')
            b(250, dx=1, legs='stand')
        b(130, arm='up', chalk=('r', 2), write=(x, 13))  # nearer ones: the claw itself travels down the stroke
        b(180, arm='side', chalk=('r', 2), write=(x, 15), marks=st['marks'] + ((x, 14),))
        b(180, **REST_IN)
    # ---- C: hmm.  III? ---------------------------------------------------------------------------------
    b(320, tag='C')
    b(90, face='half')
    b(600)                                               # a slow, doubtful half-lid
    b(90, face=LOOK)
    b(160)
    b(480, face='open')                                  # ... at you
    b(240, face=LOOK)
    b(160, arm='side', chalk=('u', 2))                  # wind-up: the claw draws back and down ...
    b(110, arm='up', chalk=('r', 2), tag='tap')          # ... tap (the tip on the top of the stroke)
    b(130, arm='side', chalk=('u', 2))
    b(110, arm='up', chalk=('r', 2))                     # tap
    b(200, **REST_IN)
    # ---- D: rub it out --------------------------------------------------------------------------------
    gone = tuple(c for c in st['marks'] if c not in T1)
    b(120, arm='point', chalk=None, fx=(dust(0, 24, 14),), tag='D')
    b(110, arm='pt_u', fx=(dust(1, 24, 13),))
    b(110, arm='pt_d', marks=gone + ((23, 13),), fx=(dust(2, 24, 13),))
    b(120, arm='pt_u', marks=gone, ghost=tuple(GHOST), fx=(dust(2, 24, 12),))
    b(130, arm='point', fx=(dust(3, 24, 11),))
    b(170, fx=(dust(4, 24, 10),), **REST_IN)
    b(180, fx=(dust(5, 24, 9),))
    b(200)
    blink(220, LOOK)                                     # II.  better.
    # ---- E: underline it; payoff ------------------------------------------------------------------------
    b(200, dx=2, legs='walk_b', tag='E')
    b(130, legs='stand')
    b(120, arm='side')
    b(140, arm='down', chalk=('dr', 2), write=(24, 17))
    b(120, arm='low', chalk=('r', 2), write=(26, 17), marks=st['marks'] + ((25, 17),))
    b(150, chalk=('r', 3), write=(27, 17))
    b(160, fx=(tw(0),), **REST_IN)
    b(110, face='wide', fx=(tw(1),), tag='pay')
    b(300, fx=(tw(2),))
    b(130, face='sparkle', fx=(tw(3),))
    b(150, fx=(tw(1),))
    b(560)
    b(90, face='open')
    b(200)
    blink(340, LOOK)
    # ---- F: wipe the board, stepping back along it -------------------------------------------------------
    def smear(cells):
        return tuple(c for i, c in enumerate(sorted(cells)) if i % 2 == 0)

    def without(cells):
        return tuple(c for c in st['marks'] if c not in set(cells))

    l2 = T2 + T3 + UNDER
    b(140, arm='point', chalk=None, tag='F')             # sweep 1: the answer
    b(130, arm='pt_d', marks=without(l2), ghost=smear(l2), fx=(dust(1, 26, 15),))
    b(130, arm='pt_u', ghost=(), fx=(dust(2, 26, 14),))
    b(140, arm='wave', fx=(dust(3, 26, 12),))            # sweep 2: the top line (the claw rises along it)
    b(140, arm='raise', marks=without(ONE_B + STEM + BAR), ghost=smear(ONE_B + STEM + BAR), fx=(dust(1, 26, 10),))
    b(190, dx=1, legs='walk_a', ghost=(), fx=(dust(2, 26, 9),))
    b(140, legs='stand', fx=(dust(4, 26, 8),))
    b(140, arm='raise', marks=(), ghost=smear(ONE_A), fx=(dust(1, 23, 10),))
    b(200, dx=0, legs='walk_b', ghost=(), fx=(dust(2, 23, 9),))
    b(170, legs='stand', fx=(dust(3, 23, 8),), **REST)
    b(240, fx=(dust(4, 23, 7),))
    b(260)
    b(540, face='open', tag='end')                       # a glance at you: next one!
    return S


def tags(S):
    t, out = 0, {}
    for ms, s in S:
        if s['tag']:
            out[s['tag']] = t
        t += ms
    return out


def build():
    S = story()
    return anim(NAME, DESC, [
        static('board', _board()),
        layer('sum', [(marks(s, range(8, 12)), ms) for ms, s in S]),
        layer('answer', [(marks(s, range(12, 18)), ms) for ms, s in S]),
        layer('trunk', [(trunk(s), ms) for ms, s in S]),
        layer('arm', [(arm(s), ms) for ms, s in S]),
        layer('face', [(face(s), ms) for ms, s in S]),
        layer('fx', [(fx(s), ms) for ms, s in S]),
    ], state=STATE)
