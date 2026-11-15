"""auto - Auto mode (idle in auto mode: Claude works autonomously).

Clawd is on autopilot: he hovers under a propeller beanie, flying a kite on a breezy day.
Frame 0 hovers EXACTLY above HOME (box (10, 10), 2 cells up, shadow on row 19): hovering is this
state's resting pose, like lying in bed is sleep's, so the swap from other states is a small lift
(2 rows, inside the brief's 1-3 cells; the shadow and the spinning propeller make the hover read).

STORYBOARD (8.91 s body loop; ms)
     0  HOVER above HOME: lazy propeller (280 ms ticks), kite up-right on a taut string, its tail streaming
        downwind, soft gray shadow on the ground (frame 0 = the reduced-motion still)
  1460  a breeze lifts him a cell (left arm lags down); 1580 blink .. 1710 he glances up at his kite: it
        twinkles in the sun
  2570  LULL: the propeller idles down (460 ms ticks) and the kite sags a row, its tail losing the wind ..
  2990  .. he sinks back too (left arm and propeller lag up) and his string hand follows the slack string
        down, a beat after the kite; the tail hangs limp; he idles in the lull
  4030  a gust blows in from the left, one streak whose head curls up .. 4130 he spots it (look left)
  4330  it reaches him: he spreads an arm, the wind spins the propeller up
  4480  it shoves him right (the propeller trails a column); the streak rushes on past him and up,
        lifting the kite back up a row: it tugs his hand up and stirs its tail ..
  4630  .. and hits the kite: it climbs, its tail streams out flat, the string snaps taut and yanks his
        hand up and him up-right; the propeller still trails ..
  4850  .. and catches up: he GLIDES under his kite, arm out, the kite doing the work (the propeller
        coasts); the tail whips back and settles in a damped sway; 5250 he lets the arm hang and dangles
  5830  glances back home ..
  6100  AUTOPILOT: he looks up as the propeller whirs (120 ms ticks, the loop's fastest) and hops up its
        stalk (it leads) ..
  6250  .. and it arcs him back over the top (arm lags down, he looks back toward home; the apex is a
        130 ms passing frame, the only moment 4 cells up) while the kite settles a column downwind;
  6380  down-left above home (arm and propeller lag up); the tail swings and streams again
  6640  he peeks down at his shadow while the propeller winds down (340 -> 460 ms ticks) ..
  7840  .. he sinks home (lags) as the breeze eases: the kite drifts back to its spot, tail swinging
  8800  blink, the loop's last beat: his eyes open on frame 0
Blinks at 1.58 s and 8.80 s (gaps 7.2 s and 1.7 s). Ambient, on its own 24.1 s loop: small clouds drift
downwind a column at a time (uneven 0.7-1 s holds) along rows 7-10, sliding BEHIND the beanie, the kite
string and the tail and out past the right edge while the next one drifts in from the left, so every 9 s
loop meets a different sky. The big cloud is static.
Layers: clawd, blade, hat (beanie dome + kite string + kite + its calm tail + shadow) and fx (gust,
glint, and the tail while it whips in the gust) are all cut from the same KEYS, so nothing on him or
his kite ever drifts. The blade sits UNDER the hat layer, whose hub caps it; its ticks carry across keys
(the propeller keeps its own rhythm against the body) and restart only when the blade moves, so it rides
along with his head. _seam_fit checks the blade ends on the phase that turns forward into frame 0's
wide blade.
Size (~49 KB lint estimate): the drifting sky is the big new cost (~10.7 KB), kept down three ways:
(1) two clouds share one 28-step conveyor instead of a 35-step trip plus a gap; (2) cloud cells that
his dome or body cover in EVERY body pose are never drawn (lossless: they can never be seen); (3) the
calm tail rides in the hat frames, whose palette already holds its colours, so only the gust whip,
which changes between hat cuts, costs frames of its own. The string hand's relax and tug fall on keys
that cut the hat anyway, and the loop ends on the blink so Clawd's last frame is not a copy of frame 0.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'auto'
STATE = 'Auto mode (idle in that mode: Claude works autonomously)'
DESC = ('Hovers on autopilot under a lazily spinning propeller beanie, flying a kite while clouds drift by: '
        'a gust lifts the kite and he glides under it, then the propeller arcs him back home.')


# ---------------------------------------------------------------- library pieces
# Local copies, used ONLY if the library is mid-save when this builds (get() raises KeyError).
_FALLBACK = {
    'propeller_beanie': ('head', (4, 5), [
        [b, '....s....', '..pygbv..', '.ryygbbv.', 'rryygbbvv', 'RRjjGBBVV']
        for b in ('.rrrmrrr.', '..rrmRR..', '...rmr...', '..RRmrr..')], (1, -5)),
    'sparkle_small': ('fx', (1, 1), [['...', '.j.', '...'], ['.j.', 'jyj', '.j.'], ['j.j', '.j.', 'j.j']], (0, 0)),
    'kite': ('hand', (0, 10), [
        ['......r..', '.....rry.', '....rrryy', '.....yyr.', '.....yyr.', '....m.y..'] + tail
        for tail in (['...m..N..', '...m...b.', '..m....N.', '.m......p', 'm........'],
                     ['...m..N..', '...m..b..', '..m....N.', '.m.....p.', 'm........'],
                     ['...m..N..', '...m.b...', '..m...N..', '.m....p..', 'm........'])], (0, 0)),
}


def _lib(name):
    try:
        return get(name)
    except KeyError:
        slot, anchor, frames, (ox, oy) = _FALLBACK[name]
        sprites = []
        for rows in frames:
            s = Sprite(rows, anchor=anchor, name=name)
            sprites.append(Sprite(cells=[(x + ox, y + oy, ch) for x, y, ch in s.cells],
                                  anchor=(anchor[0] + ox, anchor[1] + oy), name=name))
        return Item(name, slot, 'local fallback', sprites)


def _beanie_parts():
    """Split the library propeller beanie: the dome (+ stalk + hub) moves only with his head; the blade
    (its top row) spins. Blades come two ways: 'solid' (the hub cell takes the near half's colour, so a
    blade is one or two runs; drawn UNDER the dome layer, whose hub covers that cell) and 'lifted' (with
    its own hub, used when it rides a row up its stalk). Phases 1 and 3 keep the library's far-half shade."""
    it = _lib('propeller_beanie')
    s0 = it.sprite(0)
    top, hub_x = s0.y0, s0.ax
    # the 1-cell stalk and the hub take the shadow's gray: the axle reads as one piece and every hat
    # frame carries two colours less (the same look at one pixel)
    axle = {'s': 'N', 'm': 'N'}
    dome = Sprite(cells=[(x, y, axle.get(ch, ch)) for x, y, ch in s0.cells if y > top or x == hub_x],
                  anchor=(s0.ax, s0.ay), name='propeller_dome')
    solid, lifted = [], []
    for k in range(len(it.frames)):
        row = sorted(c for c in it.sprite(k).cells if c[1] == top)
        near = [c[2] for c in row if c[0] != hub_x][-1]          # the hub joins the right-hand run
        solid.append(Sprite(cells=[(x, y, near if x == hub_x else ch) for x, y, ch in row],
                            anchor=(s0.ax, s0.ay), name='propeller_blade'))
        lifted.append(Sprite(cells=[(x, y - 1, axle.get(ch, ch)) for x, y, ch in row], anchor=(s0.ax, s0.ay),
                             name='propeller_blade'))
    return Item('propeller_beanie', 'head', 'dome of the library propeller_beanie', dome), solid, lifted


def _string_cells(spr):
    """The kite string = the same-coloured cells 8-connected to the grip (the sprite's anchor)."""
    colour = {(x, y): ch for x, y, ch in spr.cells}
    start = (spr.ax, spr.ay)
    if start not in colour:
        return set()
    ch0, seen, todo = colour[start], {start}, [start]
    while todo:
        x, y = todo.pop()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = (x + dx, y + dy)
                if q not in seen and colour.get(q) == ch0:
                    seen.add(q)
                    todo.append(q)
    return seen


def _kite_parts():
    """Library kite split into the diamond (+ its knot), the tail's bow shapes (relative to the knot) and
    the string's top cell, the tie (the string itself is drawn live from his hand)."""
    it = _lib('kite')
    s0 = it.sprite(0)
    frames = []
    for k in range(len(it.frames)):
        s = it.sprite(k)
        string = _string_cells(s)
        frames.append(set(c for c in s.cells if (c[0], c[1]) not in string))
        if k == 0:
            tie = min(string, key=lambda c: (c[1], -c[0]))   # the string's top cell, next to the diamond
    shared = set.intersection(*frames)
    diamond = Sprite(cells=sorted(shared), anchor=(s0.ax, s0.ay), name='kite')
    knot = max(shared, key=lambda c: c[1])                   # lowest diamond cell: where the tail hangs
    tails = {k: [(x - knot[0], y - knot[1], ch) for x, y, ch in sorted(f - shared)] for k, f in enumerate(frames)}
    return diamond, tails, (tie[0] - s0.ax, tie[1] - s0.ay), (knot[0] - s0.ax, knot[1] - s0.ay)


# ---------------------------------------------------------------- local sprites
def _cloud(mask, glint=()):
    """Puffy cloud from an interior mask: pale-lilac fill (optional white glint), lavender rim all round
    (the light colours never touch the background, so it reads on both themes)."""
    inside = {(x, y) for y, r in enumerate(mask) for x, ch in enumerate(r) if ch == 'X'}
    cells = {}
    for x, y in inside:
        cells[(x, y)] = 'W' if (x, y) in glint else 'L'
    for x, y in inside:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in inside:
                cells[(x + dx, y + dy)] = 'l'
    # anchor = top-left of the drawn cloud (rim included)
    return Sprite(cells=[(x + 1, y + 1, c) for (x, y), c in cells.items()], anchor=(0, 0), name='cloud')


_CLOUD_A = _cloud(['.XX....', 'XXXX.X.', 'XXXXXXX'], {(1, 0)})
_CLOUD_B = _cloud(['.XX.', 'XXXX'])      # the drifting ones: no glint (every position is its own frame)
CLOUD_A_AT = (1, 1)      # the big cloud stays put (static layer)
CLOUD_B_Y = 7            # the small ones drift along rows 7-10 (a clear row under the big cloud): behind
                         # the dome, the kite string and the tail
CLOUD_B_X0 = 3           # frame 0 (the still): one small cloud just under the big one, clear of his hat
CLOUD_B_IN = -4          # a cloud drifts in with its two right columns showing ..
CLOUD_B_OUT = 30         # .. and out with its two left columns showing
# A conveyor of two identical clouds half a closed track apart: as one drifts out on the right the next
# drifts in on the left, so the 35-column trip costs CLOUD_B_STEPS frames, not 35 + a gap. (The fewest
# steps that keep the second cloud off-canvas in frame 0.)
CLOUD_B_STEPS = CLOUD_B_OUT - CLOUD_B_X0 + 1
# uneven holds per column (ms), a fixed table so the drift breathes instead of ticking: ~0.86 s per column,
# a 24 s loop against the ~9 s body loop, so every pass meets him in a different pose
CLOUD_B_HOLDS = (860, 720, 980, 800, 900, 1040, 760, 880, 820, 960, 700, 900, 1000, 780,
                 840, 940, 760, 880, 820, 1000, 740, 860, 920, 780, 960, 820, 880, 800)

STRING = 'N'             # kite string: gray reads on both themes (4.6:1 on white, 3.6:1 on dark) and shares
                         # the shadow's and stalk's colour, so the hat layer carries no extra colour for it
SHADOW = 'N'             # soft ground shadow, never black
_SHADOW_W = {11: 9, 10: 7, 9: 5, 8: 3}     # shadow width per box-top row: higher = smaller

# kite grip anchor per state: 'low' = sagging in the lull, 'gust' = climbed, 'settle' = blown a column
# downwind after the gust, before it drifts back to 'rest'
KITE_AT = {'rest': (21, 12), 'low': (21, 13), 'gust': (21, 11), 'settle': (22, 12)}

# tail shapes, relative to the knot: the library's three sway frames (0 = streaming downwind at rest,
# 1 = between, 2 = hanging back / limp) plus our own gust streamer, blown out flat downwind
_TAIL_GUST = {'s1': [(1, 1, 'b'), (2, 1, 'N'), (3, 1, 'p')]}


# ---------------------------------------------------------------- master timeline
def K(ms, x, y, larm, rarm, eyes, legs, spin, lift=0, drag=0, kite='rest', sync=False, tail=0):
    """One key: duration, box top-left, arms, eyes, legs, ms per propeller tick, lift = 1 when the blade
    rides a row up its stalk (it leads a climb / lags a sink), drag = blade x offset (it trails a shove),
    kite = where the kite flies, sync = the propeller starts a fresh tick here (a deliberate change of
    pace), tail = the kite tail's calm shape, drawn in the hat frame (None while WHIP animates it in the fx
    layer). Change `tail` only on keys that change the hat anyway. His right hand always holds the string."""
    return dict(ms=ms, x=x, y=y, larm=larm, rarm=rarm, eyes=eyes, legs=legs, spin=spin, lift=lift,
                drag=drag, kite=kite, sync=sync, tail=tail)


KEYS = [
    K(1460, 10, 10, 'side', 'up', 'open', 'stand', 280),               # 0 frame 0: the reduced-motion still
    K(120, 10, 9, 'down', 'up', 'open', 'stand', 280),                 # 1 a breeze lifts him (left arm lags down)
    K(130, 10, 9, 'side', 'up', 'blink', 'stand', 280),                # 2 the arm settles; blink ..
    K(860, 10, 9, 'side', 'up', 'look_ur', 'stand', 280),              # 3 .. glance up at the kite (it glints)
    K(420, 10, 9, 'side', 'up', 'look_ur', 'stand', 460, sync=True, kite='low', tail=1),  # 4 LULL: the propeller
                                                                       #   idles down, the kite sags, its tail
                                                                       #   loses the wind ..
    K(140, 10, 10, 'up', 'side', 'open', 'stand', 460, lift=1, kite='low', tail=2),  # 5 .. he sinks too (left
                                                                       #   arm + blade lag up); his string hand
                                                                       #   follows the slack string down a beat
                                                                       #   after the kite; the tail hangs limp
    K(1000, 10, 10, 'side', 'side', 'open', 'stand', 460, kite='low', tail=2),   # 6 idling in the lull; a gust
    K(200, 10, 10, 'side', 'side', 'look_l', 'stand', 460, kite='low', tail=2),  # 7 .. he spots it coming
    K(150, 10, 10, 'out', 'side', 'look_l', 'stand', 180, kite='low', tail=2),   # 8 GUST_HIT: arm out, the wind
                                                                       #   spins the propeller up
    K(150, 11, 10, 'out', 'up', 'look_l', 'stand', 160, drag=-1, tail=1),  # 9 shoved right (blade trails); the
                                                                       #   kite lifts and tugs his hand up; tail stirs
    K(220, 12, 9, 'out', 'raise', 'open', 'stand', 170, drag=-1, kite='gust', tail=None),  # 10 the kite climbs:
                                                                       #   yank up-right, blade still trails ..
    K(400, 12, 9, 'out', 'raise', 'open', 'stand', 200, kite='gust', tail=None),  # 11 .. catches up: he glides,
                                                                       #   the kite doing the work (prop coasts)
    K(580, 12, 9, 'side', 'raise', 'open', 'stand', 320, kite='gust', tail=None),  # 12 dangles under his kite
    K(270, 12, 9, 'side', 'raise', 'look_l', 'stand', 320, kite='gust', tail=None),  # 13 glances back home
    K(150, 12, 9, 'side', 'raise', 'look_u', 'stand', 120, lift=1, kite='gust', tail=None),  # 14 AUTOPILOT whirs,
                                                                       #   the blade leads up its stalk
    K(130, 11, 8, 'down', 'up', 'look_dl', 'stand', 120, kite='settle', tail=1),  # 15 over the top (apex: a
                                                                       #   passing frame); kite settles, tail swings
    K(140, 10, 9, 'up', 'up', 'look_d', 'stand', 120, lift=1, kite='settle'),  # 16 down-left (arm + blade lag)
    K(120, 10, 9, 'side', 'up', 'look_d', 'stand', 120, kite='settle'),
    K(740, 10, 9, 'side', 'up', 'look_d', 'stand', 340, kite='settle'),  # 18 peeks down at his shadow ..
    K(460, 10, 9, 'side', 'up', 'look_d', 'stand', 460, sync=True, kite='settle'),  # 19 .. the propeller idles
    K(140, 10, 10, 'up', 'up', 'open', 'stand', 460, lift=1, tail=1),  # 20 he sinks home (lags) as the breeze
                                                                       #   eases: the kite drifts back, tail swings
    K(820, 10, 10, 'side', 'up', 'open', 'stand', 280, tail=1),        # 21 settled (the seam fit may tune it)
    K(110, 10, 10, 'side', 'up', 'blink', 'stand', 280, tail=1),       # 22 blink: the loop's last beat, it opens
                                                                       #    straight into frame 0
]
LOOP_MAX = 9000          # the brief: a 5-9 s loop
FLOAT = 6                # index of the float in the lull (the seam fit may tune it)
PEEK = 18                # index of the peek at his shadow (the seam fit may tune it)
SETTLE = 21              # index of the hold after he sinks home (the seam fit may tune it)
GUST_HIT = 8             # index of the key where the gust reaches him
GLANCE = 3               # index of the key where he looks up at his kite

# the tail while the gust whips it (keys with tail=None), drawn in the fx layer: (key index, ms into that
# key, shape). It streams out flat as the kite climbs, whips back, overshoots and settles: a damped sway.
WHIP = [
    (10, 0, 's1'),
    (11, 0, 0),
    (11, 220, 2),
    (12, 0, 1),
    (12, 230, 0),
]


def _starts(keys):
    t, out = 0, []
    for k in keys:
        out.append(t)
        t += k['ms']
    return out, t


# ---------------------------------------------------------------- body-clock layers
def _pose(k):
    return clawd(eyes=k['eyes'], larm=k['larm'], rarm=k['rarm'], legs=k['legs'])


def _clawd_frame(k):
    f = Frame()
    put_clawd(f, _pose(k), k['x'], k['y'])
    return f


def _route(hx, hy, tx, ty):
    """Kite string from the hand (hx, hy) up-right to the tie (tx, ty) with even steps only: a 45-degree
    run, plus any extra flat steps at the hand end (the string sags there) or extra steep steps at the
    kite end (where a string hangs steepest)."""
    dx, dy = tx - hx, hy - ty
    assert dx >= 0 and dy >= 0, (hx, hy, tx, ty)
    cells, x, y = [(hx, hy)], hx, hy
    for _ in range(max(0, dx - dy)):
        x += 1
        cells.append((x, y))
    for _ in range(min(dx, dy)):
        x, y = x + 1, y - 1
        cells.append((x, y))
    for _ in range(max(0, dy - dx)):
        y -= 1
        cells.append((x, y))
    return cells


def _tail_cells(kite, shape, tails, knot_rel):
    shapes = dict(tails)
    shapes.update(_TAIL_GUST)
    kx, ky = KITE_AT[kite]
    nx, ny = kx + knot_rel[0], ky + knot_rel[1]
    return [(nx + dx, ny + dy, ch) for dx, dy, ch in shapes[shape]]


def _hat_frame(k, dome, tie_rel, diamond, tails, knot_rel):
    """Everything that moves only when his whole body, his kite hand or the kite moves: beanie dome,
    kite string, kite and its calm tail, ground shadow. The kite's and tail's colours are all in the
    beanie already, so they cost the hat no extra colour."""
    f = Frame()
    kx, ky = KITE_AT[k['kite']]
    f.place(diamond, kx, ky)
    if k['tail'] is not None:
        for x, y, ch in _tail_cells(k['kite'], k['tail'], tails, knot_rel):
            f.put(x, y, ch)
    p = _pose(k)
    wear(f, dome, p, k['x'], k['y'])
    hx, hy = p.at('hand_r', k['x'], k['y'])
    for x, y in _route(hx, hy, kx + tie_rel[0], ky + tie_rel[1]):
        f.put(x, y, STRING)
    w = _SHADOW_W[k['y']]
    f.hline(k['x'] + 5 - w // 2, k['x'] + 5 + w // 2, GROUND, SHADOW)
    return f


def _blade_pose(k):
    return (k['x'] + k['drag'], k['y'], k['lift'])


def _blade_pieces(keys):
    """Blade timeline: [phase, x, y, lift, ms] pieces. The propeller turns at each key's `spin` (ms per
    tick) and its progress through a tick carries across key boundaries, so it keeps its own rhythm
    against the body and eases through changes of pace (half a fast tick + half a slow tick). Only a key
    that moves the blade (body, lift or drag) or asks for `sync` starts a new tick, so blade and head move
    together. A tick never leaves a sliver before such a break or the loop seam: it holds on instead."""
    out = []
    phase, done = 0, 0.0                       # done = fraction of the current tick already shown
    n = len(keys)
    for i, k in enumerate(keys):
        pose = _blade_pose(k)
        if done >= 0.999 or (i and (pose != _blade_pose(keys[i - 1]) or k['sync']) and done > 0):
            phase, done = (phase + 1) % 4, 0.0
        breaks = i == n - 1 or _blade_pose(keys[i + 1]) != pose or keys[i + 1]['sync']
        left = k['ms']
        while left > 0:
            piece = min(max(1, int(round((1.0 - done) * k['spin']))), left)
            if breaks and left - piece < max(60, k['spin'] // 2):
                piece = left                   # no sliver before a break: this tick holds on
            if out and out[-1][:4] == [phase] + list(pose):
                out[-1][4] += piece
            else:
                out.append([phase] + list(pose) + [piece])
            left -= piece
            done += piece / float(k['spin'])
            if done >= 0.999 and left > 0:
                phase, done = (phase + 1) % 4, 0.0
    return out


def _seam_fit(keys):
    """The blade's 4 frames are widths 7-5-3-5: a seamless loop must END on phase 3 to turn forward into
    frame 0's wide blade, with a calm last tick (0.8-1.4 ticks) and no frame under 60 ms. KEYS are tuned
    to close the seam as they stand; if an edit breaks it, nudge calm holds (only ever longer) and the
    settle hold, smallest change first, within the 9 s loop. Deterministic."""
    pieces = _blade_pieces(keys)
    if _seam_ok(keys, pieces) and _starts(keys)[1] <= LOOP_MAX:
        return list(keys), pieces
    total = _starts(keys)[1]
    knobs = [(0, range(0, 281, 40)),              # calm holds only ever get longer: the frame-0 hover,
             (FLOAT, range(0, 281, 40)),          # the float in the lull,
             (PEEK, range(0, 281, 40)),           # the peek at his shadow;
             (SETTLE, range(-300, 301, 10))]      # the hold after he sinks home may give a little
    combos = [()]
    for _, r in knobs:
        combos = [c + (d,) for c in combos for d in r]
    combos.sort(key=lambda c: (sum(abs(d) for d in c), c))
    for c in combos:
        if total + sum(c) > LOOP_MAX:
            continue
        trial = list(keys)
        for (i, _), d in zip(knobs, c):
            trial[i] = dict(trial[i], ms=trial[i]['ms'] + d)
        pieces = _blade_pieces(trial)
        if _seam_ok(trial, pieces):
            return trial, pieces
    raise ValueError('auto: no seamless blade phase found')


def _seam_ok(keys, pieces):
    last = pieces[-1]
    return last[0] == 3 and 0.8 * keys[-1]['spin'] <= last[4] <= 1.4 * keys[-1]['spin'] \
        and min(p[4] for p in pieces) >= 60


def _blade_frames(pieces, solid, lifted):
    frames = []
    for ph, x, y, lift, ms in pieces:
        f = Frame()
        f.place((lifted if lift else solid)[ph], x + 5, y)
        frames.append((f, ms))
    return frames


# ---------------------------------------------------------------- fx: gust, glint, the whipping tail
# One gust streak (row 14, clear of the clouds' rows), timed from the hit: it blows in from the left edge
# and its head curls up into a swirl .. it reaches him; as he is shoved it rushes on past his right side
# and up (the kite lifts a row), then on up the right side into the kite's tail as the kite climbs.
# (key index, ms into the key, ms, cells)
_GUST = [
    (GUST_HIT, -300, 100, [(0, 14), (1, 14), (2, 14)]),
    (GUST_HIT, -200, 100, [(x, 14) for x in range(1, 5)]),
    (GUST_HIT, -100, 100, [(x, 14) for x in range(3, 6)] + [(6, 13), (6, 12), (5, 12)]),
    (GUST_HIT, 0, 150, [(x, 14) for x in range(6, 10)]),
    (GUST_HIT + 1, 0, 150, [(23, 16), (24, 16), (25, 15), (26, 14)]),
    (GUST_HIT + 2, 0, 220, [(27, 13), (28, 12), (29, 11), (30, 10)]),   # as long as the tail streams
]
_GLINT = [(200, 0, 100), (300, 1, 120), (420, 2, 100)]   # (ms after the glance starts, sparkle_small frame, ms):
                                                          # dot, plus, x: a twinkle that turns as it fades


def _fx_layer(keys, glint_at, tails, knot_rel):
    """Composite of timed events [(start, ms, cells)], cut wherever any of them starts or ends."""
    starts, total = _starts(keys)
    events = []
    for ki, rel, ms, cells in _GUST:
        events.append((starts[ki] + rel, ms, [(x, y, 'c') for x, y in cells]))
    spark = _lib('sparkle_small')
    for rel, i, ms in _GLINT:
        s = spark.sprite(i)
        events.append((starts[GLANCE] + rel, ms,
                       [(glint_at[0] + x - s.ax, glint_at[1] + y - s.ay, ch) for x, y, ch in s.cells]))
    whip = sorted((starts[i] + dt, shape, i) for i, dt, shape in WHIP)
    for n, (t, shape, i) in enumerate(whip):
        end = whip[n + 1][0] if n + 1 < len(whip) else \
            starts[next(j for j in range(i, len(keys)) if keys[j]['tail'] is not None)]
        events.append((t, end - t, _tail_cells(keys[i]['kite'], shape, tails, knot_rel)))
    cuts = sorted({0, total} | {s for s, _, _ in events} | {s + ms for s, ms, _ in events})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        f = Frame()
        for s, ms, cells in events:
            if s <= a < s + ms:
                for x, y, ch in cells:
                    f.put(x, y, ch)
        out.append((f, b - a))
    return out


# ---------------------------------------------------------------- the drifting clouds
def _always_covered(timelines):
    """Cells that the layers above the clouds draw in EVERY moment of the body loop (his dome and body in
    all his poses). A cloud cell there can never be seen, whatever the cloud loop's phase, so the clouds
    skip it: the same picture, a smaller SVG."""
    cuts = set()
    for tl in timelines:
        t = 0
        for _, ms in tl:
            cuts.add(t)
            t += ms
    covered = None
    for c in sorted(cuts):
        occ = set()
        for tl in timelines:
            t = 0
            for f, ms in tl:
                if t <= c < t + ms:
                    occ |= set(f.px)
                    break
                t += ms
        covered = occ if covered is None else covered & occ
    return covered or set()


def _cloud_layer(hidden):
    """Small clouds drift downwind one column at a time with uneven holds along rows 7-10, behind his dome,
    the kite string and the tail, out past the right edge. Two identical clouds ride a closed track half a
    track apart, so as one drifts out on the right the next one drifts in on the left; frame 0 shows one."""
    span = CLOUD_B_OUT - CLOUD_B_IN + 1               # visible positions (x0 = IN .. OUT)
    track = 2 * CLOUD_B_STEPS
    assert span <= track, 'cloud conveyor: track too short'
    first = CLOUD_B_X0 - CLOUD_B_IN                   # cloud A's track index in frame 0
    assert first + CLOUD_B_STEPS >= span, 'cloud conveyor: frame 0 would show the second cloud'
    out = []
    for k in range(CLOUD_B_STEPS):
        f = Frame()
        for idx in (first + k, first + k + CLOUD_B_STEPS):
            idx %= track
            if idx >= span:
                continue                              # off-canvas stretch of the track
            x0 = CLOUD_B_IN + idx
            for sx, sy, ch in _CLOUD_B.cells:
                x, y = x0 + sx, CLOUD_B_Y + sy
                if 0 <= x < W and (x, y) not in hidden:
                    f.put(x, y, ch)
        out.append((f, CLOUD_B_HOLDS[k % len(CLOUD_B_HOLDS)]))
    return out


def build():
    dome, solid, lifted = _beanie_parts()
    diamond, tails, tie_rel, knot_rel = _kite_parts()
    keys, pieces = _seam_fit(KEYS)

    clawd_l, hat_l = [], []
    for k in keys:
        clawd_l.append((_clawd_frame(k), k['ms']))
        hat_l.append((_hat_frame(k, dome, tie_rel, diamond, tails, knot_rel), k['ms']))
    blade_l = _blade_frames(pieces, solid, lifted)

    # the glint nestles into the kite's sunny top-left edge: 2 cells left of its top tip
    top = min(diamond.cells, key=lambda c: (c[1], c[0]))
    kx, ky = KITE_AT[keys[GLANCE]['kite']]
    glint_at = (kx + top[0] - 2 - diamond.ax, ky + top[1] - diamond.ay)
    fx_l = _fx_layer(keys, glint_at, tails, knot_rel)

    sky = Frame()
    sky.place(_CLOUD_A, *CLOUD_A_AT)
    clouds = _cloud_layer(_always_covered([clawd_l, blade_l, hat_l, fx_l]))

    return anim(NAME, DESC, [
        static('sky', sky),
        layer('cloud', clouds),            # drifts behind everything but the big cloud
        layer('clawd', clawd_l),
        layer('blade', blade_l),           # under the hat layer: the dome's hub caps the solid blade
        layer('hat', hat_l),               # beanie dome, kite string, kite + calm tail, shadow
        layer('fx', fx_l),                 # gust streak, the kite's glint, the tail whipping in the gust
    ], state=STATE)
