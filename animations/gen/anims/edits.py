"""edits - Accept-edits mode (idle in that mode): Clawd the calm builder.

STORYBOARD (ms; loop 10000; one master beat list drives every synced layer, so nothing ever drifts)
     0  F0  AIM: Clawd at HOME in his yellow hard hat and tool belt (the belt's hammer loop is empty:
            the hammer is up in his right hand), eyes on a T-headed nail standing in the wooden top beam
            of the little brick wall he has stacked at his right. A striped traffic cone at his left.
            A long, still hold (1.2 s, plus the 0.2 s tail before the seam).
  1200  A   one tap: wrist flick through 45 deg, the hammer face lands on the nail head (it sinks a
            row), a little spark peeks out beside the face .. recoil through 45 deg .. aim, he checks it
  2100  B   wind-up, eased in: his arm straightens (hammer still upright, 80) .. the hammer leans back
            over his hat, left arm braces down: held 300 ms ..  2480 swing (upright 60, 45 deg 40,
            accelerating into the nail) ..
  2580      BANG: the nail goes flush, contact flash in front;  2640 the gold burst HELD 150 ms (core in
            front of the hammer, rays behind everything), reflex blink, the hard hat hops 2 rows (air
            under the brim) then 1;  2790 hat lands a beat later, burst flung out as spikes, sawdust
            puffs on the beam, brace relaxes;  2880 lone specks drift off
  3000  C   that took some effort: a bead of sweat pops out beside his hat while the hammer rests on
            the flush nail ..  3360 he lets the hammer settle against the beam, his arm hangs: a calm
            800 ms breather
  4250  D   phew: the bead swells into a drop and slides ..  4870 his left hand rises to the brim (the
            drop stretches) ..  4990 he tips the hat up off his head in two steps (brim resting on his
            hand, a wedge of air under it), the drop flicks off in two droplets, a relieved blink ..
  5460      he sets it back down, eased: the tilt comes out (80) .. level a row up (60) ..  5600 on;
            his hand lets go a beat behind the hat (raise -> up -> side)
  5710  E   admires the job: eyes down on the flush nail head (a silver dash in the beam) ..  6050 it
            twinkles (grow, star, thin plus) .. a 710 ms hold ..  7270 a long look out at you (1.3 s)
  8570  F   looks down at his belt pouch, takes a nail ..  8970 tosses it over his head: one full
            tumble on an eased arc, eyes follow it (up, then right); his right hand lifts the hammer
            off the beam in even steps (lean, settle, swing, aim) while the nail is in the air ..
  9720      it drops point-first into the beam and lands tipped: tink! and a puff of sawdust knocked
            out either side of the bite (the old flush head goes under the puff: the new nail takes
            its place) ..  9800 it stands upright, the puff thins to two specks, the tink fades to a
            dot .. the specks clear on the wrap = frame 0 (seamless)
Layers (back to front): site (static: wall, cone, his legs and tool belt; he never leaves HOME or lifts
a foot) | hat (merges while it rests) | body (Clawd; his frames leave out every cell the belt and the
hat cover, except his arms, so a raised arm passes in front of the brim) | blink (his own clock, below)
| tool (hammer + nail; the tap spark rides on its hit frame) | fx (the BANG's contact flash, the held
burst, spikes, sawdust, sweat, twinkle, the tossed nail, the landing puff) | glint, glint2 (ambient).
Riding effects overlap nothing they share a frame with, and every synced layer switches on the same
beat boundaries, so the picture is unchanged. hat, body, tool and fx share the one beat list.
VARIETY for a state that stays on for minutes: three layers run on their own clocks, co-prime with the
10 s story and with each other, so no two loops look alike (the full picture repeats only after days):
  blink   8900 ms   his ambient blink lands on a different beat every loop (during the hold, mid-toss,
                    next to a story blink = a double blink); the story keeps its acting blinks (the
                    BANG's reflex blink, the relieved one under the tipped hat)
  glint   7300 ms   a twinkle on the cone's upper reflective band (plus, turning x)
  glint2 11300 ms   a quick twinkle on its lower band
Plain face only (open / blink / look_*), normal body size (STYLE.md section 0). Eye glances are chosen
so both eye holes stay enclosed by his body or arms.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'edits'
STATE = 'Accept-edits mode (idle in that mode)'
DESC = ('Calm builder in a hard hat and tool belt: taps a nail into the beam of his little brick wall, '
        'BANG, rests the hammer, tips his hat off his sweaty brow, admires the work, then tosses the next '
        'nail into place.')

_HAT = get('hard_hat')
_BELT = get('tool_belt')
_HAMMER = get('hammer')
_HAM_UP = get('hammer_up')
_HAM_HIT = get('hammer_hit')
_IMPACT = get('impact_star')
_SWEAT = get('sweat_drop')
_SPARK = get('sparkle')
_GLINT = get('sparkle_small')

# The belt's own hammer (right hip: its head from box x 11, handle and grip at x 12) is in his hand, so
# the loop it hangs from, box (10, 5) and (11, 5), stays empty.
_bs = _BELT.sprite(0)
_BELT_SPR = Sprite(cells=[c for c in _bs.cells if not (c[0] >= 12 or (c[0] == 11 and c[1] < 5))],
                   anchor=(_bs.ax, _bs.ay), name='tool_belt_open_loop')

# The hard hat tipped up off his head, in two stages: his raised left hand holds the low left end of the
# brim (it lands at (9, 11), right on the 'raise' hand), the brim steps up to the right, so a wedge of
# air opens over his head. Gold contour lit from the top-left, the same ridge highlight, shaded right.
# Anchor (6, 6) = his head-top-center point.
_HAT_TIP = Item('hard_hat_tipped', 'head', 'local: the hard hat tipped up off his head (rising, tipped)', [
    Sprite([                       # rising: one step of tilt
        '....jjjjj..',
        '...jYyYyyj.',
        '..jYyyYyyjj',
        '..jyyyYyyjJ',
        '.jyyyyyJJJJ',
        'jjjjjj.....',
    ], anchor=(6, 6), name='hard_hat_tip_rising'),
    Sprite([                       # tipped: brim stepping up every 4 cells
        '...jjjjj...',
        '..jYyYyyj..',
        '.jYyyYyyyj.',
        '.jyyyYyyJJJ',
        '.jyyjjjJ...',
        'jjjj.......',
    ], anchor=(6, 6), name='hard_hat_tipped'),
])

# Wind-up: the library hammer leaning back over his head (head 2 cells back). Anchor = grip.
_HAM_BACK = Sprite([
    'mmssN',
    '.mssN',
    '..T..',
    '...T.',
    '...T.',
    '....T',
    '....T',
], anchor=(4, 6), name='hammer_back')

# Break: the hammer propped against the beam, held loosely in his hanging hand (rarm='down'): the
# library 45-degree hammer with one more handle cell, so its face rests on the beam top (row 13).
_HAM_LEAN = Sprite([
    '....m....',
    '....ms...',
    '.....ss..',
    '....T.sN.',
    '...T...NN',
    '..T......',
    '.T.......',
    'T........',
], anchor=(0, 7), name='hammer_lean')


# =====================================================================================================
# The impact (library impact_star, split so its core shows in front of the hammer)
# =====================================================================================================
def _split(spr, r):
    """(core, rays): cells within Chebyshev distance r of the anchor, and the rest."""
    near = lambda c: max(abs(c[0] - spr.ax), abs(c[1] - spr.ay)) <= r
    core = Sprite(cells=[c for c in spr.cells if near(c)], anchor=(spr.ax, spr.ay), name=spr.name)
    rays = Sprite(cells=[c for c in spr.cells if not near(c)], anchor=(spr.ax, spr.ay), name=spr.name)
    return core, rays


_FLASH = _IMPACT.sprite(0)
# warm gold instead of red: a satisfying clink, calmer than a red POW (and it can't merge into the bricks)
_CORE, _RAYS = _split(_IMPACT.sprite(1).recolor({'r': 'j'}), 2)
_HIT_AT = (26, 13)                         # where the hammer face meets the nail

# After the hold the burst is flung out: single ray tips one or two cells past its rim (all inside
# the 1-cell margin and clear of the hat, hammer and wall in that beat).
_SPIKES = [(20, 9, 'j'), (25, 6, 'j'), (30, 7, 'j'), (30, 11, 'j')]   # gold like the burst's tips

# Sawdust puffing out of the beam on the big hit (either side of the hammer face), then two lone
# specks drifting off. Tan with wood-brown undersides: no isolated paper-white specks.
_DUST = [
    [(24, 12, 't'), (23, 13, 't'), (24, 13, 'T'), (29, 12, 't'), (29, 13, 'T'), (30, 13, 't')],
    [(23, 12, 't'), (30, 12, 't')],
]

# The next nail landing: a smaller puff knocked out of the beam either side of the bite (clear of the
# tipped nail at (26-28, 12-14) and of the tink above it), then two specks drifting off as it rights.
_PUFF = [
    [(24, 13, 't'), (25, 13, 'T'), (29, 13, 'T'), (30, 13, 't')],
    [(23, 12, 't'), (30, 12, 't')],             # = the BANG's last specks: the same sawdust
]


# =====================================================================================================
# Scenery (static)
# =====================================================================================================
def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


# Little brick wall he has stacked, capped by a wooden top beam (the nail goes into the beam). The
# 'm' near its far end is the head of an earlier nail, already flush: evidence of the job.
_WALL = [
    'ttttttmT',
    'TTTTTTTT',
    'rrrRrrrR',
    'RRRRRRRR',
    'rRrrrRrr',
    'RRRRRRRR',
]
_WALL_X, _WALL_Y = 23, 14

# Traffic cone (lit from the top-left, two reflective bands; where a band touches the background its
# ends are light gray / gray, so the silhouette survives the light theme).
_CONE = [
    '..o..',
    '.ooO.',
    '.MWm.',
    '.ooO.',
    'oWWmO',
    'ooooO',
    'OOOOO',
]
_CONE_X, _CONE_Y = 1, 13

# =====================================================================================================
# The nail: a T head (silver 'mmm') on a steel shaft. Standing, it is 3 rows tall like the tossed one;
# its tip bites into the beam's top face (row 14). Flush, the head is a silver dash in the tan beam.
# =====================================================================================================
_NAIL_X = 26
_NAIL_HEAD_ROW = {'up': 12, 'tap': 13, 'flush': 14}


def _T(rows):
    return Sprite(rows, anchor=(1, 1), name='nail')


# One full clockwise tumble, 45 degrees a step; every orientation is 3 x 3, anchored on its center.
_FLY = {
    'v': _T(['mmm', '.s.', '.s.']),
    'd1': _T(['.mm', '.sm', 's..']),
    'h': _T(['..m', 'ssm', '..m']),
    'd2': _T(['s..', '.sm', '.mm']),
    'vi': _T(['.s.', '.s.', 'mmm']),
    'd3': _T(['..s', 'ms.', 'mm.']),
    'hi': _T(['m..', 'mss', 'm..']),
    'd4': _T(['mm.', 'ms.', '..s']),
}


def _nail(f, state):
    if state == 'land':                        # just landed, tipped right: tip in the beam at (26, 14)
        f.place(_FLY['d1'], _NAIL_X + 1, 13)
        return
    h = _NAIL_HEAD_ROW[state]
    for dx in (-1, 0, 1):
        f.put(_NAIL_X + dx, h, 'm')
    for y in range(h + 1, 15):
        f.put(_NAIL_X, y, 's')


# The library sweat drop, mirrored to his left (his right hand holds the hammer): anchored on his face
# point it hangs one cell clear of the hat dome. Anchor = his face point.
_SWEAT_AT = clawd().at('face')

# The drop flicked off as he tips the hat: two droplets on arcs out-left and down, starting where it
# hung (its stretched tail ends at x 6-7, rows 12-14). Two steps of each arc, one per beat.
_FLUNG = [[(x, y, 'c') for (x, y) in pair]
          for pair in zip(ballistic(6, 12, -1.4, -0.7, g=1.2, steps=3)[1:],
                          ballistic(7, 13, -1.1, -0.3, g=1.2, steps=3)[1:])]

# Ambient: the cone's two reflective bands catch the light now and then, each on its own loop
# (7300 ms upper band, 11300 ms lower band: co-prime with each other and with the 10 s story).
_BAND_HI = (3, 15)
_BAND_LO = (3, 17)


# =====================================================================================================
# Clawd, his tools, his hat
# =====================================================================================================
_RARM = {'aim': 'raise', 'swing': 'raise', 'hit': 'wave', 'back': 'high', 'cock': 'high',
         'settle': 'side', 'lean': 'down'}


def _pose(s):
    return clawd(eyes=s['eyes'], larm=s['larm'], rarm=_RARM[s['ham']])


def _arm_cells(p):
    """Canvas cells of his arms (box columns 0 / 10 and beyond)."""
    return {(HOME[0] + x, HOME[1] + y) for x, y, _ in p.sprite.cells if x <= 0 or x >= 10}


def _belt():
    f = Frame()
    f.place(_BELT_SPR, *clawd().at('neck'))
    return f


def _hat(s):
    """The hard hat: resting / hopping (dx, dy), or tipped up off his head. It is drawn BEFORE his
    body; the body leaves out every cell the hat covers except his arms, so an arm raised past the
    brim passes in front of it and the resting hat stays one frame all the way through the wind-up."""
    f = Frame()
    p = _pose(s)
    if s['hat'] in ('tip0', 'tip1'):
        wear(f, _HAT_TIP, p, i=int(s['hat'][-1]))
    else:
        wear(f, _HAT, p, dx=s['hat'][0], dy=s['hat'][1])
    return f


_LEG_ROWS = (18, 19)


def _legs():
    """His legs never change in this loop (he always stands at HOME), so they live in a static layer."""
    f = Frame()
    put_clawd(f, clawd())
    f.px = {c: ch for c, ch in f.px.items() if c[1] in _LEG_ROWS}
    return f


def _body(s, covered):
    """Clawd (kit pose via put_clawd) minus his legs (static layer) and minus the cells the belt and
    hat cover in this beat (the belt sits in front of him; the hat brim overlaps his top row), except
    his arms, which stay in front of the brim: same picture, smaller SVG."""
    f = Frame()
    p = _pose(s)
    put_clawd(f, p)
    arms = _arm_cells(p)
    for c in list(f.px):
        if (c in covered and c not in arms) or c[1] in _LEG_ROWS:
            del f.px[c]
    return f


def _tool(s):
    """The hammer in his right hand (aim: upright, raised | cock: upright, arm straight up, easing into
    the wind-up | back: wind-up, leaning back over his hat | swing: 45 deg | hit: level, face down on
    the nail | settle / lean: propped against the beam, held loosely) and the nail in the beam. On a light tap the nail head is drawn over the hammer
    face, so the face meets the head instead of swallowing it."""
    f = Frame()
    p = _pose(s)
    tap_hit = s['ham'] == 'hit' and s['nail'] == 'tap'
    if not tap_hit:
        _nail(f, s['nail'])
    kind = s['ham']
    if kind in ('aim', 'cock'):
        wear(f, _HAMMER, p)
    elif kind in ('swing', 'settle'):
        wear(f, _HAM_UP, p)
    elif kind == 'hit':
        wear(f, _HAM_HIT, p)
    elif kind == 'back':
        f.place(_HAM_BACK, *p.at('hand_r'))
    elif kind == 'lean':
        f.place(_HAM_LEAN, *p.at('hand_r'))
    if tap_hit:
        _nail(f, s['nail'])
    return f


# =====================================================================================================
# Master timeline
# =====================================================================================================
class _TL:
    def __init__(self):
        self.segs = []
        self.st = dict(eyes='look_r', larm='side', ham='aim', hat=(0, 0), nail='up')

    def add(self, ms, **kw):
        """kw changes the persistent state; fx / burst / flash / tik / held / fly last one beat only."""
        once = {k: kw.pop(k) for k in ('fx', 'burst', 'flash', 'tik', 'held', 'fly') if k in kw}
        self.st.update(kw)
        s = dict(self.st)
        s.update(once)
        self.segs.append((int(ms), s))


def _timeline():
    t = _TL()
    # A  F0: a long, still aim .. one light tap .. he checks it (his blinks live in their own layer)
    t.add(1200)
    t.add(80, ham='swing')
    t.add(110, ham='hit', nail='tap', tik=[(_FLASH,) + _HIT_AT])
    t.add(90, ham='swing')                                    # recoil through 45 deg
    t.add(620, ham='aim')
    # B  wind-up (eased in, held), the swing accelerates into the nail, BANG, the hold, spikes, sawdust
    t.add(80, ham='cock', larm='down')                        # arm straightens, hammer still upright
    t.add(300, ham='back')                                    # .. leans back over his hat: held
    t.add(60, ham='aim')
    t.add(40, ham='swing')
    t.add(60, ham='hit', nail='flush', flash=True)
    t.add(90, eyes='blink', hat=(0, -2), burst=True)         # the hold: air under the hopping brim
    t.add(60, hat=(0, -1), burst=True)
    t.add(90, eyes='look_r', larm='side', hat=(0, 0), fx=[('spikes',), ('dust', 0)])
    t.add(120, fx=[('dust', 1)])
    # C  that took some effort: a bead of sweat pops out beside his hat while the hammer rests on the
    #    flush nail .. he lets it settle against the beam, his arm hangs: a calm breather
    t.add(360, fx=[('sweat', 6)])
    t.add(90, ham='settle', fx=[('sweat', 6)])
    t.add(800, ham='lean', eyes='open', fx=[('sweat', 6)])
    # D  phew: the bead swells into a drop and slides, he tips the hat up off his brow, it flicks away
    t.add(280, fx=[('sweat', 0)])
    t.add(200, fx=[('sweat', 1)])
    t.add(140, fx=[('sweat', 2)])
    t.add(120, larm='up', eyes='look_l', fx=[('sweat', 3)])    # hand rises to the brim
    t.add(110, larm='raise', hat='tip0', fx=[('flung', 0)])   # tips the hat up: the drop flicks off
    t.add(160, eyes='blink', hat='tip1', fx=[('flung', 1)])   # wedge of air, a relieved blink
    t.add(200, eyes='open')                                   # a breath of air on his brow
    t.add(80, hat='tip0')                                     # sets it back: the tilt comes out ..
    t.add(60, hat=(0, -1))                                    # .. level, a row above his head ..
    t.add(110, hat=(0, 0), larm='up')                         # .. on; the hand lets go a beat behind
    # E  admire: eyes down on the flush nail, it twinkles, a content blink, a long look out at you
    t.add(340, larm='side', eyes='look_dr')
    for i, ms in ((1, 120), (2, 260), (3, 130)):             # plus, star, thin plus
        t.add(ms, fx=[(_SPARK.sprite(i), _NAIL_X, _NAIL_HEAD_ROW['flush'])])
    t.add(710)
    t.add(1300, eyes='open')                                  # (any blink here comes from the blink layer)
    # F  next nail: pouch, toss (the right hand lifts the hammer to AIM mid-flight), drop-in, tink
    t.add(240, eyes='look_dl', larm='down')
    t.add(160, eyes='look_l', larm='up', held=(9, 12))
    flight = [  # (center x, y, orientation, eyes, left arm, hammer: lifted off the beam in even steps)
        (10, 8, 'v', 'look_u', 'raise', 'lean'),
        (12, 5, 'd1', 'look_u', 'raise', 'settle'),
        (14, 3, 'h', 'look_u', 'up', 'swing'),
        (16, 2, 'd2', 'look_u', 'up', 'aim'),
        (18, 2, 'vi', 'look_u', 'side', 'aim'),
        (20, 2, 'd3', 'look_u', 'side', 'aim'),
        (22, 2, 'hi', 'look_u', 'side', 'aim'),
        (25, 3, 'd4', 'look_r', 'side', 'aim'),
        (26, 6, 'v', 'look_r', 'side', 'aim'),
        (26, 9, 'v', 'look_r', 'side', 'aim'),
    ]
    for x, y, spr, eyes, larm, ham in flight:                 # even frames: the spacing makes the arc
        t.add(75, eyes=eyes, larm=larm, ham=ham, fly=(spr, x, y))
    # tink! it lands tipped and knocks a puff of sawdust out of the beam (the puff also covers the old
    # head going: the new nail takes its place) .. it stands upright, the puff thins, the tink fades
    t.add(80, nail='land', fx=[(_GLINT.sprite(1), 29, 10), ('puff', 0)])
    t.add(10000 - sum(ms for ms, _ in t.segs), nail='up',     # = frame 0 (seamless); the last specks
          fx=[(_GLINT.sprite(0), 29, 10), ('puff', 1)])       # clear on the wrap
    return t


# =====================================================================================================
# Layer frames
# =====================================================================================================
def _scene():
    f = Frame()
    _paint(f, _WALL, _WALL_X, _WALL_Y)
    _paint(f, _CONE, _CONE_X, _CONE_Y)
    return f


def _behind(items, *front, keep=None):
    """Effects that happen BEHIND the beam, Clawd and the hammer: only the cells that show past the
    given frames are kept (and only those `keep` accepts). They overlap nothing, so they can ride on
    any layer at that beat."""
    f = Frame()
    for spr, x, y in items:
        f.place(spr, x, y)
    hidden = set()
    for fr in front:
        hidden |= set(fr.px)
    f.px = {c: ch for c, ch in f.px.items() if c not in hidden and (keep is None or keep(c))}
    return f


def _fx(s):
    f = Frame()
    for item in s.get('fx', ()):
        kind = item[0]
        if kind == 'spikes':
            for x, y, ch in _SPIKES:
                f.put(x, y, ch)
        elif kind == 'dust':
            for x, y, ch in _DUST[item[1]]:
                f.put(x, y, ch)
        elif kind == 'puff':
            for x, y, ch in _PUFF[item[1]]:
                f.put(x, y, ch)
        elif kind == 'sweat':
            f.place(_SWEAT.sprite(item[1]).flipped(), *_SWEAT_AT)
        elif kind == 'flung':
            for x, y, ch in _FLUNG[item[1]]:
                f.put(x, y, ch)
        else:
            spr, x, y = item
            f.place(spr, x, y)
    # The nail in his left hand, about to be tossed, and tumbling through the air: in flight (75 ms a
    # step) a 3-cell T can't show its two grays, so it is all silver, one color per frame; it shows
    # its steel shaft again once it bites into the beam (tool layer).
    if s.get('held'):
        f.place(_FLY['v'].recolor(_SILVER), *s['held'])
    if s.get('fly'):
        spr, x, y = s['fly']
        f.place(_FLY[spr].recolor(_SILVER), x, y)
    return f


_SILVER = {'s': 'm'}


def _glint_layer(name, at, period, steps):
    """Ambient, independent of the beat list: one twinkle on a reflective band per `period` ms. The
    periods are co-prime with the 10 s story, so each loop the glints land on different beats. The
    twinkle sits at the end of the layer's own loop: frame 0 (the reduced-motion still) is empty."""
    frames = [(Frame(), period - sum(ms for _, ms in steps))]
    for i, ms in steps:
        frames.append((Frame().place(_GLINT.sprite(i), *at), ms))
    assert total_ms(frames) == period
    return layer(name, frames)


# His blinks run on their own loop too (8900 ms, co-prime with everything else), so from one 10 s
# story to the next they fall on different beats: during the hold, mid-toss, right after a story
# blink (a double blink) .. The story keeps its acting blinks (the BANG's reflex blink, the relieved
# one under the tipped hat, the content one before he looks out at you).
_BLINK_PERIOD, _BLINK_MS = 8900, 120


def _blink_layer(poses):
    """Paints his body orange over every cell that is an eye hole in any pose of the loop, so it reads
    as a plain kit blink whatever he is looking at. Safe on its own clock: he never leaves HOME, and
    the eye cells lie inside his body block (rows 13-15), clear of every hat, tool and effect.
    Built from a kit 'blink' pose drawn with put_clawd; frame 0 is empty (eyes open)."""
    holes = set()
    x0, y0 = HOME
    for p in poses:
        drawn = {(x0 + x, y0 + y) for x, y, ch in p.sprite.cells if ch not in (ERASE, EYE_INK)}   # eyes are black ink now (user)
        holes |= {(x0 + x, y0 + y) for x in range(1, 10) for y in range(0, 6)} - drawn
    shut = Frame()
    put_clawd(shut, clawd(eyes='blink'))
    shut.px = {c: ch for c, ch in shut.px.items() if c in holes}
    assert holes and all(ch == '#' for ch in shut.px.values()) and len(shut.px) == len(holes)
    return layer('blink', [(Frame(), _BLINK_PERIOD - _BLINK_MS), (shut, _BLINK_MS)])


def _in_bounds(c):
    return 1 <= c[0] <= 30 and 1 <= c[1] <= 14


def _in_front(spr):
    """An impact sprite at the contact point, drawn in front, but never below the beam's top face."""
    f = Frame().place(spr, *_HIT_AT)
    f.px = {c: ch for c, ch in f.px.items() if c[1] <= 14}
    return f


def build():
    t = _timeline()
    belt = _belt()
    site = _scene().over(_legs()).over(belt)     # everything that never changes, in one static layer
    body, tool, hat, fx = [], [], [], []
    for ms, s in t.segs:
        h, tl = _hat(s), _tool(s)
        b = _body(s, set(belt.px) | set(h.px))  # the belt and hat show where the body leaves a gap
        # a light tap's spark peeks out beside the hammer face (rides on the tool layer's hit frame)
        tl = tl.over(_behind(s.get('tik', ()), site, b, tl, h))
        e = _fx(s)
        if s.get('flash'):
            # BANG contact: the flash in front of the hammer face, down to the beam's top face (fx is
            # the top synced layer, and the tool layer's hit frame then runs on unbroken)
            e = e.over(_in_front(_FLASH))
        if s.get('burst'):
            # the held BANG (fx is the top synced layer): rays behind the beam, Clawd, the hammer and
            # his hopping hat (nothing on the bricks or past the margin), the bright core in front of
            # the hammer face, down to the beam's top face
            rays = _behind([(_RAYS,) + _HIT_AT], site, b, tl, h, keep=_in_bounds)
            e = e.over(rays).over(_in_front(_CORE))
        body.append((b, ms))
        tool.append((tl, ms))
        hat.append((h, ms))
        fx.append((e, ms))
    assert total_ms(body) == 10000, total_ms(body)
    return anim(NAME, DESC, [
        static('site', site),
        layer('hat', hat),
        layer('body', body),
        _blink_layer([_pose(s) for _, s in t.segs]),
        layer('tool', tool),
        layer('fx', fx),
        _glint_layer('glint', _BAND_HI, 7300, ((1, 120), (2, 140))),      # plus, turning x
        _glint_layer('glint2', _BAND_LO, 11300, ((1, 140),)),             # a quick plus
    ], state=STATE)
