"""bypass - Bypass-permissions mode: living dangerously.

STORYBOARD (ms)  sign + body + fx loop 7680 ms; the sign's glint runs on its own co-prime period (7310 ms).
     0  "ting!" (frame 0 = the reduced-motion still): HOME column, riding the skateboard; devil horns, devil
        tail, sunglasses with the right-lens glint + a cyan twinkle off the right temple. On the right a
        street sign says NO (no skating, no entry, no permission ... not his problem). Twinkle fades (110),
        then one long calm hold (2600).
  2930  a little kick, and he cruises backwards (fakie) to the left, leading arm out, eased 10 -> 5
        (200 140 120 140 200 ms per cell). Every cell longer than 140 ms gets an fx-only in-between where the
        red mark on the gold wheels hops over, so the mark hops every 90-140 ms; speed streaks only on the two
        fastest cells. Arms drop as he slows (wind-up) and he stops at 5 (300).
  4030  RUN-UP to the right: a push-kick and he accelerates, 6 (200) 7 (140); the tail streams out behind.
  4370  OLLIE carried by that speed, one cell per frame: pop at 8 (90: the tail smacks the ground on row 19,
        dust bursts beside the tip) -> rise 9 (100: legs tucked, the front foot drags the nose up) -> peak 10
        (170: board level, hang time) -> drop 11 (100: feet down for the landing; rows 8 6 5 7 9, an even
        fall). A ground shadow tracks the height (7 5 7); streaks trail him.
  4830  touchdown at 12 (90): dust from both wheels, arms absorb, the shades slip a row ... rolls out 13 (140)
        14 (220) and comes to rest right under the NO sign, shades knocked crooked (360).
  5640  fingertip under the low lens (an orange notch biting the black lens; the tail flicks) 260 -> pushes:
        hand and lens rise together 170 -> leans on the NO sign's pole, nonchalant, while the light sweeps
        the lenses (60 160): cool again (560).
  6850  SHOVES OFF the pole into a manual (nose up, leaning back) and cruises home backwards: 13 (110) 12
        (130) 11 (140) 10 (240). The sign bends away (an even 6:1 kink), springs back past upright, settles:
        rules bent.
  7470  clack: the nose drops at HOME (puff), the tail swings on, the light sweeps his lenses (90 120) ->
        seam -> frame 0: the "ting" that punctuates his arrival.
  sign  its top-left corner winks every 7.3 s, co-prime with the main loop: a different beat each time.

LAYERS  scene (static pole foot) | sign (plate + upper pole: rests, wobbles after the shove) | body (tail,
Clawd, horns, shades, board) | fx (streaks, dust, shadow, glints, wheel-spin in-betweens) | sign_glint
(independent). sign, body and fx are built from ONE timeline, so they share every frame boundary; moments
where only an effect changes cost a small fx frame, not a body frame. The long HOME hold starts the loop, so
it is a single body frame.

Lint WARN "frame 0: Clawd is at (10, 9)" is deliberate: he rides the library skateboard at the HOME column
(feet on the deck, row 17; wheels on the ground, row 19), the skateboard's own ride convention.
"""
import sys, os
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'bypass'
STATE = 'Bypass-permissions mode (living dangerously)'
DESC = ('Rules? Shades on, devil horns and tail, Clawd skates under a NO sign: cruises, pops an ollie, lands '
        'with his shades knocked crooked, pushes them straight, shoves off the sign and manuals home.')

Y = 9                                        # box top while riding: feet on row 16, deck on 17, wheels on 19

# ---------------------------------------------------------------- library pieces
_LIB_SHADES = get('sunglasses_glint')        # 0 rest, 1-2 glint sweeps right, 3 twinkle, 4 fade
# horns and tail in flat red: at 3 px their pink tip and dark-red shading read the same as plain red, and
# dropping them saves two colors and ~5 runs in every body frame (~3 KB)
_FLAT_RED = {'p': 'r', 'R': 'r'}
_HORNS = Item('devil_horns', 'head', 'library devil_horns', [get('devil_horns').sprite(0).recolor(_FLAT_RED)])
_TAIL = Item('devil_tail', 'back', 'library devil_tail',     # 0 rest, 2 swung out (1, tucked, would touch
             [s.recolor(_FLAT_RED) for s in get('devil_tail').frames])   # the left horn at this dx: unused)
_TAIL_DX = 2                                 # worn 2 cells in: a compact curl (its root hides behind him)
_LINES = get('motion_lines')
_DUST = get('dust_puff')
_SPARK = get('sparkle_small')

# the shades: library frame 0 without the dim reflection pixel on the right lens (one color less per frame,
# and where an arm leaves the shades' side, _rim() gives that edge a clean gray rim like the top corners)
_BASE = _LIB_SHADES.sprite(0).recolor({'n': 'k'})
_SHADES = Item('sunglasses_glint', 'face', 'library sunglasses_glint, rest frame', [_BASE])
# knocked askew by the landing: the right lens hangs one row low, the bridge bends (both lenses keep shape)
_CROOKED = Item('sunglasses_glint', 'face', 'sunglasses knocked crooked', [
    Sprite(cells=[(x, y + (1 if x >= 6 else 0), ch) for x, y, ch in _BASE.cells],
           anchor=(_BASE.ax, _BASE.ay), name='sunglasses_crooked')])


def _diff(i):
    """Cells where sunglasses_glint frame i differs from the rest frame (derived from the data)."""
    base = {(x, y): ch for x, y, ch in _BASE.cells}
    return [(x, y, ch) for x, y, ch in _LIB_SHADES.sprite(i).cells if base.get((x, y)) != ch]


_LENS = {i: [c for c in _diff(i) if c[1] >= _BASE.y0] for i in (1, 2, 3, 4)}       # the light on the lenses
# the twinkle above the lenses, nudged one cell right and down: off the right horn, clear of the sign
_SKY = {i: [(x + 1, y + 1, ch) for x, y, ch in _diff(i) if y < _BASE.y0] for i in (3, 4)}
if not _SKY[3]:                              # (library changed again: keep a twinkle in the same spot)
    _SKY = {3: [(12, 1, 'c'), (11, 2, 'c'), (12, 2, 'W'), (13, 2, 'c'), (12, 3, 'c')], 4: [(12, 2, 'c')]}
_GLINT = {k: Sprite(cells=v, anchor=(_BASE.ax, _BASE.ay), name='glint_' + k) for k, v in (
    ('sweep1', _LENS[1]), ('sweep2', _LENS[2]), ('ting', _LENS[3] + _SKY[3]), ('fade', _LENS[4] + _SKY[4]))}

# ---------------------------------------------------------------- boards (library skateboard parts)
# trucks in gray (already in every body frame for the shades' rim: one color less), wheels in gold
# (readable on white); rolling wheels show a red mark (the deck's red: no extra color) hopping from cell to
# cell - it reads the spin better than a yellow highlight, which melts into the gold at 3 px
_FLAT = get('skateboard').sprite(0).recolor({'s': 'N', 'y': 'j'})     # 13x4, anchor = bottom-center
_POP = Sprite([                              # the pop: tail smacked onto the ground, nose up (moving right)
    '............r',
    '........rrrr.',
    '....rrrr.NN..',
    '..rr.....jj..',
    '.rNN.........',
    'r.jj.........',
], anchor=(6, 5), name='skate_pop')
_RISE = Sprite([                             # nose up, even 4:1 steps: rising, the front foot drags it up
    '............r',
    '........rrrr.',
    '....rrrr.NN..',
    'rrrr.....jj..',
    '..NN.........',
    '..jj.........',
], anchor=(6, 5), name='skate_rise')
_MANUAL = Sprite([                           # manual home (moving left): nose up, front wheels off the ground
    'r............',
    '.rrrrrr......',
    '..NN...rrrrrr',
    '..jj.....NN..',
    '.........jj..',
], anchor=(6, 4), name='skate_manual')
_WHEELS = {'flat': [(2, 3), (9, 3)], 'manual': [(9, 4)]}                # left cell of each grounded wheel pair


def _rolling(spr, pairs, phase):
    hi = {(x + phase, y) for x, y in pairs}
    return Sprite(cells=[(x, y, 'r' if (x, y) in hi else ch) for x, y, ch in spr.cells],
                  anchor=(spr.ax, spr.ay), name=spr.name)


# the tail's smack / the nose's clack: left half of the library landing dust (bottom row on the ground)
_PUFF = Sprite(cells=[c for c in _DUST.sprite(0).cells if c[0] < _DUST.sprite(0).ax], anchor=(7, 3), name='pop_puff')

# ground shadow under the airborne board (graphite: a crisp shadow on white, subtle on dark)
_SHADOW = {w: Sprite(['n' * w], anchor=(w // 2, 0), name='shadow_%d' % w) for w in (5, 7, 9)}

# ---------------------------------------------------------------- the NO sign
# A street sign that just says NO, red letters on a white plate between gray rails (the letters' outer strokes
# are its side edges: mid-tone red on both themes). A rectangle on a pole: nothing like error's round sign.
SIGN_X = 26                                  # the pole's column; the plate spans 22..29 on rows 1..6
_PLATE = Sprite([r.replace('.', 'w') for r in (
    'NNNNNNNN',
    'r..r.rrr',
    'rr.r.r.r',
    'r.rr.r.r',
    'r..r.rrr',
    'NNNNNNNN',
)], anchor=(4, 5), name='no_sign_plate')     # anchor: the pole column, bottom rail
SIGN_GLINT = (22, 2)                         # the plate's top-left corner, where the light comes from
_BEND = 13                                   # the pole bends above this row when the sign leans


def _sign(lean=0):
    """The plate and the upper pole; lean = -1 / 0 / +1: the top sways a cell (an even 6:1 kink)."""
    f = Frame()
    f.vline(SIGN_X + lean, 7, _BEND - 1, 'N')                  # gray like the rails: 3 colors per frame
    f.place(_PLATE, SIGN_X + lean, 6)
    return f


def _sign_foot():
    f = Frame()
    f.vline(SIGN_X, _BEND, GROUND - 1, 'N')
    f.hline(SIGN_X - 1, SIGN_X + 1, GROUND, 'N')
    return f


# ---------------------------------------------------------------- Clawd poses
def _pose(arms, legs='stand'):
    """A kit pose; for leg lengths the kit has no name for (a tuple: outer-left, inner-left, inner-right,
    outer-right) the same kit pose is rebuilt with Pose.from_rows: same cells, same orange, a cell or two
    changed. (The fingertip on the shades is drawn after the accessories, in _moment.)"""
    if not isinstance(legs, tuple):
        return clawd(larm=arms[0], rarm=arms[1], legs=legs)
    kit = clawd(larm=arms[0], rarm=arms[1], legs='none')
    cells = {(x, y): ch for x, y, ch in kit.sprite.cells}
    g = GEOM['normal']
    for col, n in zip(g['legs'], legs):
        for i in range(n):
            cells[(col, g['ly'] + i)] = '#'
    pad = -min(0, min(x for x, _ in cells))                  # arms 'out' reach box column -1
    grid = [['.'] * (max(x for x, _ in cells) + pad + 1) for _ in range(max(y for _, y in cells) + 1)]
    for (x, y), ch in cells.items():
        grid[y][x + pad] = ch
    p = Pose.from_rows([''.join(r) for r in grid], anchors=clawd(larm=arms[0], rarm=arms[1]).anchors,
                       name='clawd_custom')
    p.sprite = p.sprite.moved(-pad, 0)
    return p


def _rim(frame):
    """Shade cells in ink that touch the background (an arm moved away) get the rim's gray, so his head
    outline never vanishes on the dark theme."""
    for (x, y), ch in list(frame.px.items()):
        if ch == 'k' and any((x + dx, y + dy) not in frame.px for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            frame.px[(x, y)] = 'N'


def _clip_place(f, spr, x, y, x_min=1, x_max=W - 2, min_run=3, flip=False, rows=None):
    """place, but drop cells outside [x_min, x_max] (streaks that would run off the canvas or into the sign);
    a row clipped shorter than min_run cells is dropped entirely (no stray dots). rows: keep only these."""
    if flip:
        spr = spr.flipped()
    out = {}
    for sx, sy, ch in spr.cells:
        cx, cy = x + sx - spr.ax, y + sy - spr.ay
        if x_min <= cx <= x_max and 0 <= cy < H and (rows is None or cy in rows):
            out.setdefault(cy, []).append((cx, ch))
    for cy, cells in out.items():
        if len(cells) >= min_run:
            for cx, ch in cells:
                f.put(cx, cy, ch)


# ---------------------------------------------------------------- one moment
def _moment(x, y=Y, arms=('side', 'side'), legs='stand', hand=None, board='flat', phase=None, shades='on',
            tail=0, glint=None, lines=None, dust=None, puff=None, shadow=None, spin=False):
    """Returns (body, fx) frames. x, y = Clawd's box.
    board : 'flat' under his feet | 'pop' (tail on the ground) | 'rise' (in the air, nose up, under his front
            feet) | 'manual' (nose up on the left, riding the back wheels)
    phase : None = wheels still; 0 / 1 = rolling, which cell of each grounded wheel carries the red mark
    spin  : (fx) the in-between: the mark hops to the wheels' other cell
    shades: 'on' | 'slip' (slid down a row by the impact) | 'crooked' (right lens hangs low)
    hand  : 'low' fingertip under the low lens | 'push' lens pushed back up, fingertip on its corner
    tail  : devil_tail frame (0 rest, 2 swung out)
    fx    : glint = key of _GLINT; lines = (frame, 'L' trailing left | 'R' trailing right, n): speed streaks
            kept to the n cells nearest to him; dust = (frame, world x of the landing); puff = (x, y) of the
            bottom-right cell of a small puff; shadow = its width."""
    body, fx = Frame(), Frame()
    p = _pose(arms, legs)
    wear(body, _TAIL, p, x, y, i=tail, dx=_TAIL_DX)
    put_clawd(body, p, x, y)
    wear(body, _HORNS, p, x, y)
    if shades == 'crooked':
        wear(body, _CROOKED, p, x, y)
    else:
        wear(body, _SHADES, p, x, y, dy=1 if shades == 'slip' else 0)
    if hand == 'low':                                          # under the low right lens
        body.put(x + 9, y + 4, '@')
        body.put(x + 8, y + 4, '#')
    elif hand == 'push':                                       # lens back up, the fingertip still on it
        body.put(x + 9, y + 3, '@')
        body.put(x + 8, y + 3, '#')
    deck = y + (7 if legs == 'short' else 8)                    # the row right under his feet
    wheels = []
    if board == 'flat':
        spr = _rolling(_FLAT, _WHEELS['flat'], phase) if phase is not None else _FLAT
        body.place(spr, x + 5, deck + 2)
        wheels = [(x - 1 + wx, deck - 1 + wy) for wx, wy in _WHEELS['flat']]
    elif board == 'rise':
        body.place(_RISE, x + 5, deck + 4)
    elif board == 'pop':
        body.place(_POP, x + 5, GROUND)
    elif board == 'manual':
        spr = _rolling(_MANUAL, _WHEELS['manual'], phase) if phase is not None else _MANUAL
        body.place(spr, x + 5, GROUND)
        wheels = [(x - 1 + wx, GROUND - 4 + wy) for wx, wy in _WHEELS['manual']]
    _rim(body)
    # ---- effects (same timing, separate layer)
    if spin and phase is not None:                            # in-between: the red mark hops over
        for wx, wy in wheels:
            fx.put(wx + phase, wy, 'j')
            fx.put(wx + 1 - phase, wy, 'r')
    if shadow:
        fx.place(_SHADOW[shadow], x + 5, GROUND)
    if lines is not None:
        i, side, n = lines
        if side == 'R':                                       # moving left: streaks trail on his right,
            near = x + 12 if arms[1] != 'out' else x + 13     # never reaching the pole
            _clip_place(fx, _LINES.sprite(i), near + 3, y + 3, x_min=near, x_max=min(near + n - 1, SIGN_X - 3),
                        flip=True, min_run=2)
        else:                                                 # moving right: streaks trail on his left, low
            near = x - 3 if arms[0] != 'out' else x - 4       # (under the tail's curl)
            _clip_place(fx, _LINES.sprite(i), near - 1, y + 6, x_min=max(1, near - n + 1), x_max=near, min_run=2,
                        rows=range(y + 4, GROUND))
    if puff is not None:
        fx.place(_PUFF, *puff)
    if dust is not None:                                      # anchored where he landed; stops at the post
        _clip_place(fx, _DUST.sprite(dust[0]), dust[1], GROUND - 1, x_max=SIGN_X - 2, min_run=1)
    if glint:
        fx.place(_GLINT[glint], *p.at('face', x, y))
    return body, fx


def _sign_glint(loop):
    """The sign's corner winks now and then, on a period co-prime with the main loop (a different beat every
    time; the combination only repeats after hours). Frame 0 is empty: the still stays calm."""
    seq = [(1, 120), (2, 130)]
    period = next(p for d in range(0, 3000, 10) for p in (7300 + d, 7300 - d) if gcd(p, loop) == 10)
    frames = [(Frame(), period - sum(ms for _, ms in seq))]
    for i, ms in seq:
        f = Frame()
        f.place(_SPARK.sprite(i), *SIGN_GLINT)
        frames.append((f, ms))
    return layer('sign_glint', frames)


def build():
    T = []                                   # (body, fx, sign lean, ms)
    k = [0]                                  # wheel-spin counter: the mark hops every (half) cell
    last = [0]                               # where the mark sat in the last rolling body frame

    def add(ms, lean=0, half=None, roll=False, keep=False, **kw):
        """One moment. roll: the wheels turn (their red mark hops a cell every frame). A rolling cell held
        longer than the 140 ms motion range gets an fx-only in-between halfway through (the mark hops to the
        wheels' other cell; the body frame is shared, so it costs a small fx frame); half = fx overrides for
        that second half. keep: the wheels have stopped, the mark stays where the last rolling body frame had
        it (so that body frame simply continues)."""
        if roll:
            kw['phase'] = last[0] = k[0] % 2
        elif keep:
            kw['phase'] = last[0]
        if roll and ms > 140:
            a = ms // 2
            T.append(_moment(**kw) + (lean, a))
            kw2 = dict(kw, spin=True)
            kw2.update(half or {})
            T.append(_moment(**kw2) + (lean, ms - a))
            k[0] += 2
        else:
            T.append(_moment(**kw) + (lean, ms))
            k[0] += 1 if roll else 0

    # HOME. Frame 0 (the reduced-motion still) is the "ting" that punctuates his arrival home (the loop ends
    # with the nose dropping at HOME and the light sweeping his lenses), then one long calm hold.
    add(220, x=10, glint='ting')
    add(110, x=10, glint='fade')
    add(2600, x=10)
    # a little kick, then cruise backwards (fakie) to the left, leading arm out; eased, streaks only on the
    # fast cells
    add(200, x=9, arms=('out', 'side'), legs='walk_a', roll=True, tail=0)
    add(140, x=8, arms=('out', 'side'), roll=True, tail=0, lines=(1, 'R', 5))
    add(120, x=7, arms=('out', 'side'), roll=True, tail=0, lines=(0, 'R', 6))
    add(140, x=6, arms=('out', 'out'), roll=True, tail=0)       # slowing: arms out for balance ...
    add(200, x=5, arms=('down', 'down'), roll=True, tail=0)     # ... arms drop: wind-up ...
    add(300, x=5, arms=('down', 'down'), keep=True, tail=0)    # ... and stops
    # RUN-UP to the right, accelerating; the tail streams out behind him
    add(200, x=6, arms=('down', 'down'), legs='walk_a', roll=True, tail=0)   # a push-kick
    add(140, x=7, arms=('down', 'down'), roll=True, tail=2, lines=(1, 'L', 3))
    # OLLIE at that speed: pop -> rise -> peak (hang) -> drop -> land, one cell per frame
    add(90, x=8, y=Y - 1, arms=('raise', 'out'), legs=(3, 2, 1, 1), board='pop', tail=2, puff=(6, GROUND),
        lines=(0, 'L', 5))
    add(100, x=9, y=Y - 3, arms=('raise', 'out'), legs='short', board='rise', tail=2, shadow=7, lines=(1, 'L', 5))
    add(170, x=10, y=Y - 4, arms=('raise', 'out'), legs='short', tail=2, shadow=5, lines=(0, 'L', 3))
    add(100, x=11, y=Y - 2, arms=('out', 'out'), tail=0, shadow=7, lines=(1, 'L', 5))   # feet down to land
    # touchdown: dust where he lands, arms absorb, the shades slip ... rolls out and stops under the sign
    add(90, x=12, arms=('down', 'down'), roll=True, shades='slip', tail=0, dust=(0, 17))
    add(140, x=13, roll=True, shades='crooked', tail=0, dust=(1, 17))
    add(220, x=14, roll=True, shades='crooked', tail=0, dust=(2, 17), half={'dust': None})
    add(360, x=14, keep=True, shades='crooked', tail=0)        # right under the NO sign. A beat.
    # fix the shades: fingertip under the low lens, push it back up ...
    add(260, x=14, arms=('side', 'down'), hand='low', shades='crooked', tail=2)   # tail flicks
    add(170, x=14, hand='push', tail=0)
    # ... and lean on the NO sign's pole, nonchalant, while the light sweeps the lenses: cool again
    add(60, x=14, arms=('side', 'out'), tail=0, glint='sweep1')
    add(160, x=14, arms=('side', 'out'), tail=0, glint='sweep2')
    add(560, x=14, arms=('side', 'out'), tail=0)
    # shove off the pole (it bends away, springs back: rules bent) into a manual home, leaning back
    add(110, x=13, arms=('side', 'point'), legs=(1, 1, 2, 2), board='manual', tail=0, lean=1)
    add(130, x=12, arms=('out', 'down'), legs=(1, 1, 2, 2), board='manual', roll=True, tail=0, lean=-1)
    add(140, x=11, arms=('out', 'down'), legs=(1, 1, 2, 2), board='manual', roll=True, tail=0)
    add(240, x=10, arms=('out', 'down'), legs=(1, 1, 2, 2), board='manual', roll=True, tail=0)
    # clack: the nose drops at HOME, the tail swings on; the light sweeps his lenses -> seam -> frame 0: ting
    add(90, x=10, puff=(10, GROUND), tail=2, glint='sweep1')
    add(120, x=10, tail=2, glint='sweep2')

    loop = sum(ms for _, _, _, ms in T)
    body = layer('body', [(b, ms) for b, _, _, ms in T])
    fx = layer('fx', [(f, ms) for _, f, _, ms in T])
    sign = layer('sign', [(_sign(lean), ms) for _, _, lean, ms in T])
    # the pole's foot never moves: a static layer, given the main loop's length so it adds nothing to the loop
    return anim(NAME, DESC, [layer('scene', [(_sign_foot(), loop)]), sign, body, fx, _sign_glint(loop)],
                state=STATE)
