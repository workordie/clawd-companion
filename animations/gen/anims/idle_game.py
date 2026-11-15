"""idle-game - Idle variant: Clawd plays a little handheld game while he waits for you.

STORYBOARD (s)   one loop = 16.0 s; mostly calm holds, his thumbs play in small bursts
   0.00  HOLD at HOME, eyes down on his violet handheld; his hands wrap its sides.  The pea-green
         screen is lit: room 1, the red hero dot is lined up right next to a dark block.  His apple
         juice box stands on the left, a spare cartridge on the right.  (frame 0)
   2.20  burst 1: his left thumb holds the D-pad (that arm dips a cell), 2.34 his right thumb taps A
         (A goes dark red): the hero hops the block (the thumb lifts while he is still in the air),
         lands, walks out the right edge -> room 2 (3.12): two blocks, a gold star over the second
   3.36  thumbs rest, with a blink .. a long calm look at that star
   5.10  a lone little surprise: the gold star on the cartridge label twinkles (a hint of what's coming)
   6.52  a glance at you over the console ("watch this") .. blink, back to the game (7.52)
   8.04  burst 2: a little test hop in place (A) .. then D-pad (8.56), A a beat later (8.68): hop ..
         land between the blocks .. and hop again (9.16), grabbing the star in mid-air (the game
         freezes on the grab: the hero hangs in the air until 9.59)
   9.27  LEVEL UP: his thumbs lift off the keys as a gold spark zips out of the screen (80 ms steps,
         gold over his body, never white), arcing up past his head: dot (9.51), plus (9.59) ..
   9.67  .. the small star pops one row high (overshoot by position, not size) and settles (9.77)
   9.87  he looks up at it, a beat late .. 10.03 a little wind-up (the arm dips) .. 10.13 "yes!": a
         fist pump (right arm; the console stays in his left hand)
  10.43  he looks at you, proud, fist still up .. 10.73 the arm eases back down (side -> grip, 10.85)
  11.01  the star twinkles out, floating up (on screen 1.6 s in all)
  11.60  the hero's victory bounce on the screen, in time with his double toe tap (160 / 220 / 160 ms)
  12.40  blink, eyes back down; 12.80 the next level: room 1 again
  13.90  a lone thumb tap: the hero steps up to the block (lining up the jump = frame 0's screen)
  14.94  blink .. HOLD -> loop (0.94 s + the 2.2 s opening hold: one calm 3.1 s hold across the seam)
Blinks: 3.36, 7.52, 12.40, 14.94 s (gaps 4.2 / 4.9 / 2.5 / 4.4 s) - uneven on purpose.
Calm: ~56% of the loop is in stills of 0.9 s or more (idle: 53%); ~3.2 changes/s (idle 2.7).
Loudness: no moment changes more than 17 cells (the star's pop and settle); taps and the pump 2-5.

Grip: the kit 'front' arm silhouette (stubs on box row 3), but the dark hand cell sits one row lower
on the console's side, like the first two cells of the kit 'chin' arm; that keeps the eye row clean.
A thumb press dips the stub one cell (the kit 'front' arm, one row lower).  The pump uses the kit
'raise' and 'side' arms.
Layers (back to front): torso (Clawd's body, legs and eyes) | props (static: juice box, cartridge, the
console shell + lit screen) | limbs (his arms + the pressed A key, which always move together) | world
(blocks, the in-game star) | hero | fx (the level-up star, the cartridge twinkle).  ONE clock keys them all
(absolute key times; the level-up is offset from the grab), so taps, hops and the star never drift
apart; build() asserts no slot is under 60 ms.
User taste (STYLE.md section 0): normal body size, plain dot eyes only.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'idle-game'
STATE = 'Idle variant: playing a handheld game'
DESC = ('Plays a little violet handheld while he waits: his thumbs tap in small bursts, the screen dot '
        'hops over blocks and grabs a star that pops out above him, a fist pump, and a proud glance at you.')
LOOP = 16000

# ---------------------------------------------------------------- the console (local: none in the library)
# 7 x 3, held in front of his tummy between his hands (the hand cells land on x 11 and 19, row 16).
# Violet shell (shaded on the right), a 5 x 2 pea-green screen flush at the top, D-pad + B/A below.
# The top-left corner is plain violet: a lighter cell there merged with his left eye hole on the light theme.
CX, CY = 12, 16
_CONSOLE = Sprite([
    'vaaaaav',
    'vaaaaaV',
    'vKvvppV',
], anchor=(0, 0), name='_handheld')
BTN_A = (5, 2)                 # console-local cells
SCREEN = (1, 0)                # screen top-left, console-local (5 x 2: row 0 = air, row 1 = the lane)
A_DOWN = 'R'                   # A pressed: dark red, pushed in

HERO, BLOCK, STAR_IN = 'r', 'G', 'J'   # the in-game star is dark gold (3:1 on lime; blocks never sit in the air row)
ROOMS = {1: [(2, 1)], 2: [(1, 1), (3, 1)]}
STAR_CELL = (3, 0)             # room 2's star, right over the second block (screen-local)
HERO0 = (1, 1)                 # frame 0: lined up right next to room 1's block

# ---------------------------------------------------------------- props (local)
# Apple juice box with a pink bendy straw (anchor = bottom-center, it stands on the input box).
_JUICE = Sprite([
    '.pp',
    '.p.',
    'yyj',
    'ygj',
    'yrj',
    'yyj',
], anchor=(1, 5), name='_juice_box')
# A spare game cartridge standing on the input box (3 x 4, smaller than the handheld): gray shell with
# the cut top-right corner, a blue label with a gold star (the same star he earns), shaded on the right.
_CART = Sprite([
    'mm.',
    'bjN',
    'bbN',
    'mmN',
], anchor=(1, 3), name='_cartridge')
CART_X = 24
CART_STAR = (CART_X, GROUND - 2)            # the label's star cell on the canvas (inside the label)

# ---------------------------------------------------------------- level-up star (5 x 5) + library sparkles
_STAR5 = Sprite([
    '..j..',
    '.jyj.',
    'jWyyJ',
    '.jyJ.',
    '.J.J.',
], anchor=(2, 2), name='_star5')

# the in-game star leaving the screen: a gold spark with a short tail (head at the anchor, tail one
# cell back along the path).  Gold, never white: a white cell on his body reads as an extra eye hole.
_ZIP = {
    'zipA': Sprite(cells=[(0, 0, 'y'), (-1, 1, 'j')], anchor=(0, 0), name='_zip_rise'),   # rising up-right
    'zipB': Sprite(cells=[(0, 0, 'y'), (0, 1, 'j')], anchor=(0, 0), name='_zip_up'),      # rising straight up
}
# the cartridge label's gold star twinkling (1 cell, drawn over the label)
_DOT = {'Y': Sprite(['Y'], anchor=(0, 0), name='_dot_y'), 'W': Sprite(['W'], anchor=(0, 0), name='_dot_w')}


def _fx_sprite(kind):
    if kind in _ZIP:
        return _ZIP[kind]
    if kind.startswith('dot'):                 # dotY / dotW
        return _DOT[kind[3]]
    if kind == 'star5':
        return _STAR5
    if kind.startswith('sp'):                  # sp0..sp3 = library sparkle frames
        return get('sparkle').sprite(int(kind[2:]))
    raise KeyError(kind)


# ---------------------------------------------------------------- Clawd
_FOOT_R = (9, GEOM['normal']['ly'] + GEOM['normal']['ll'] - 1)   # his outer right foot (box cell)
_AY = GEOM['normal']['ay']                                        # the kit's arm row (box row 2)
_AX_L, _AX_R = GEOM['normal']['ax']                               # arm columns (0, 10)
# Right-arm shapes relative to (arm column, kit arm row); the left arm mirrors dx (as in the kit).
_ARM = {
    'grip':  [(0, 1), (-1, 2, '@')],   # holding: stub as kit 'front', hand on the console's side (kit 'chin' step)
    'press': [(0, 2), (-1, 2, '@')],   # a thumb presses: the stub dips a cell (kit 'front', one row lower)
    'side':  ARMS['side'],              # the pump eases back down through the kit 'side' arm
    'raise': ARMS['raise'],             # "yes!": a fist pump
}


def _torso_pose(eyes='look_d', tap=False, **_):
    """Body, legs and eyes (the arms live in the limbs layer).  tap: toe tap (outer right foot lifted)."""
    p = clawd(eyes=eyes, larm='none', rarm='none')
    cells = [c for c in p.sprite.cells if not (tap and (c[0], c[1]) == _FOOT_R)]
    return Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec, tap=tap))


def _limbs_pose(l='grip', r='grip', **_):
    """Only his arms (drawn over the torso; the dark hand cells sit on his body, in front of it)."""
    cells = {}
    for side, shape, base in (('l', l, _AX_L), ('r', r, _AX_R)):
        for item in _ARM[shape]:
            dx, dy = item[0], item[1]
            x = base + dx if side == 'r' else base - dx
            cells[(x, _AY + dy)] = item[2] if len(item) > 2 else '#'
    p = clawd(larm='none', rarm='none')
    return Pose(Sprite(cells=[(x, y, c) for (x, y), c in cells.items()], anchor=(0, 0), name='clawd_limbs'),
                p.anchors, dict(p.spec, larm=l, rarm=r, part='limbs'))


# ---------------------------------------------------------------- the clock: one list of keyframes
DEFAULT = dict(eyes='look_d', l='grip', r='grip', tap=False, room=1, hero=HERO0, star_in=False, btn=False,
               star=None, glint_c=None)


def _keys():
    """[(t, {changes})] on the loop clock, plus marks {name: t}."""
    keys, marks = [], {}

    def at(t, **kw):
        keys.append((t, kw))

    def seq(t, field, items):
        """items: (kind, ms, x, y) one after another; the field clears after the last."""
        for kind, ms, x, y in items:
            at(t, **{field: (kind, x, y)})
            t += ms
        at(t, **{field: None})
        return t

    def walk(t, cell, ms=260):
        at(t, hero=cell)
        return t + ms

    def hop(t, cell, ms=260):
        at(t, r='press', btn=True, hero=cell)        # A pressed: the hero jumps ..
        at(t + 110, r='grip', btn=False)              # .. the thumb lifts while he is in the air
        return t + ms

    # ---- 0.00 HOLD (frame 0: the reduced-motion still; the hero is lined up at the block)
    # ---- 2.20 burst 1: room 1 (block at 2)
    t = 2200
    at(t, l='press')                                  # D-pad first ..
    t = hop(t + 140, (2, 0))                          # .. A a beat later: over the block
    t = walk(t, (3, 1))                               # lands
    t = walk(t, (4, 1))
    at(t, room=2, hero=(0, 1), star_in=True)          # out the right edge: room 2, a star over block 2
    at(t + 240, l='grip', eyes='blink')               # 3.36 thumbs rest, with a blink ..
    at(t + 360, eyes='look_d')                        # .. eyes back on that star
    # ---- rest: he eyes the star on the screen; a lone little surprise: the cartridge's star twinkles
    seq(5100, 'glint_c', [('dotY', 100, CART_STAR[0], CART_STAR[1]),
                          ('dotW', 110, CART_STAR[0], CART_STAR[1]),
                          ('dotY', 90, CART_STAR[0], CART_STAR[1])])
    # ---- 6.52 a glance at you ("watch this") .. blink, back to the game
    at(6520, eyes='open')
    at(7520, eyes='blink')
    at(7640, eyes='look_d')                           # the eyes lead burst 2 by 0.4 s
    # ---- 8.04 burst 2: room 2 (blocks at 1 and 3): a test hop in place, then a quick double hop
    at(8040, r='press', btn=True, hero=(0, 0))        # A: the hero hops in place ..
    at(8300, r='grip', btn=False, hero=(0, 1))        # .. and lands where he stood
    t = 8560
    at(t, l='press')                                  # .. go: D-pad first ..
    t = hop(t + 120, (1, 0))                          # .. then A, a beat later: over block 1 ..
    t = walk(t, (2, 1), ms=220)                       # .. lands between the blocks ..
    g = marks['grab'] = t                             # .. and over block 2, grabbing the star in mid-air
    at(g, r='press', btn=True, hero=STAR_CELL, star_in=False)

    # ---- LEVEL UP (offsets from the grab).  The game freezes on the grab (the hero hangs in the air)
    at(g + 110, l='grip', r='grip', btn=False)        # thumbs lift off the keys ..
    at(g + 430, hero=(4, 1))                          # .. the game resumes: the hero lands
    out_t = g + 1850                                  # the star twinkles out (on screen 1.6 s in all)
    seq(g + 110, 'star', [
        ('zipA', 80, 17, 14), ('zipA', 80, 18, 12), ('zipB', 80, 18, 10),   # zips out, arcing up past him
        ('sp0', 80, 17, 9), ('sp1', 80, 16, 8),                             # .. slows: dot, plus ..
        ('star5', 100, 15, 6),                                              # .. pops one row high ..
        ('star5', out_t - (g + 610), 15, 7),                                # .. and settles over his head
        ('sp3', 100, 15, 7), ('sp1', 100, 15, 6), ('sp0', 90, 15, 5)])      # twinkles out, floating up
    at(g + 710, eyes='look_u')                        # he spots it, a beat late ..
    at(g + 870, r='press')                            # .. a little wind-up (the arm dips; A stays up) ..
    at(g + 970, r='raise')                            # .. "yes!": a fist pump (the console stays in his left hand)
    at(g + 1270, eyes='open')                         # .. looks at you, proud, the fist still up ..
    at(g + 1570, r='side')                            # .. and the arm eases back down onto the console
    at(g + 1690, r='grip')
    bounce = out_t + 290 + 300                        # after the star is gone: victory bounce + toe taps,
    for dt, up in [(0, True), (160, False), (380, True), (540, False)]:     # idle's unhurried 160/220/160
        at(bounce + dt, hero=(4, 0) if up else (4, 1), tap=up)
    at(12400, eyes='blink')
    at(12520, eyes='look_d')                          # back to the game ..
    at(12800, room=1, hero=(0, 1))                    # .. the next level: room 1
    # ---- a lone thumb tap breaks the long hold: the hero steps up to the block (= frame 0's screen)
    at(13900, l='press', hero=HERO0)
    at(14040, l='grip')
    # ---- the closing hold: a blink, then one long calm hold across the seam into frame 0
    at(14940, eyes='blink')
    at(15060, eyes='look_d')
    return keys, marks


def _intervals(keys):
    """(state, ms) for every slot between key times (stable: same-time keys apply in order)."""
    keys = sorted(keys, key=lambda k: k[0])
    snapped, last = [], None                          # keys under 40 ms after another snap onto it,
    for t, kw in keys:                                # so no layer ever gets a sliver of a frame
        if last is not None and 0 < t - last < 40:
            t = last
        snapped.append((t, kw))
        last = t
    keys = snapped
    times = sorted({0} | {t for t, _ in keys})
    assert times[-1] < LOOP, times[-1]
    st = dict(DEFAULT)
    out, i = [], 0
    for n, t in enumerate(times):
        while i < len(keys) and keys[i][0] == t:
            st.update(keys[i][1])
            i += 1
        end = times[n + 1] if n + 1 < len(times) else LOOP
        out.append((dict(st), end - t))
    assert min(ms for _, ms in out) >= 60, [ms for _, ms in out]
    assert out[-1][0] == dict(DEFAULT, eyes='look_d'), 'the loop must end in the frame-0 state'
    return out


def _layer(name, slots, draw):
    """One layer from the shared slots: frames merge where this layer's picture does not change."""
    frames = []
    for s, ms in slots:
        f = draw(s)
        if frames and frames[-1][0].rows() == f.rows():
            frames[-1] = (frames[-1][0], frames[-1][1] + ms)
        else:
            frames.append((f, ms))
    return layer(name, frames)


# ---------------------------------------------------------------- drawing
def _props():
    """Everything that never moves, drawn over his torso: the juice box and the cartridge beside him
    (they never touch him) and the console in front of his tummy (his hands hold it steady)."""
    f = Frame()
    f.place(_JUICE, 6, GROUND)
    f.place(_CART, CART_X, GROUND)
    f.place(_CONSOLE, CX, CY)
    return f


def _torso(s):
    f = Frame()
    put_clawd(f, _torso_pose(**s))
    return f


def _limbs(s):
    f = Frame()
    put_clawd(f, _limbs_pose(**s))
    if s['btn']:
        f.put(CX + BTN_A[0], CY + BTN_A[1], A_DOWN)   # A goes down while pressed
    return f


def _world(s):
    f = Frame()
    ox, oy = CX + SCREEN[0], CY + SCREEN[1]
    for bx, by in ROOMS[s['room']]:
        f.put(ox + bx, oy + by, BLOCK)
    if s['star_in']:
        f.put(ox + STAR_CELL[0], oy + STAR_CELL[1], STAR_IN)
    return f


def _hero(s):
    f = Frame()
    hx, hy = s['hero']
    f.put(CX + SCREEN[0] + hx, CY + SCREEN[1] + hy, HERO)
    return f


def _fx(*fields):
    def draw(s):
        f = Frame()
        for fld in fields:
            if s[fld]:
                kind, x, y = s[fld]
                f.place(_fx_sprite(kind), x, y)
        return f
    return draw


def build():
    keys, _ = _keys()
    slots = _intervals(keys)
    return anim(NAME, DESC, [
        _layer('torso', slots, _torso),
        static('props', _props()),
        _layer('limbs', slots, _limbs),
        _layer('world', slots, _world),
        _layer('hero', slots, _hero),
        _layer('fx', slots, _fx('star', 'glint_c')),   # never at the same time: one layer
    ], state=STATE)
