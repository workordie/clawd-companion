"""manual-drive - Default (manual) permission mode, variant: manual transmission.

Clawd drives a tiny mint bubble car (front view) by hand, a rubber duck riding on the roof.

STORYBOARD (body loop 12.0 s; times in ms). Physics rule: the road moves the car (a gentle bob, one bump);
the gearbox jolts the driver once (the upshift); whenever the car lifts, Clawd rises with it on the same tick, so
his hands never leave the wheel, and the lifted car leaves a real gap above the road. Calm stretches of 1-2 s sit
between the events.
     0  CRUISE: both hands on the wheel, eyes on the road (= on you), the gear stick standing in gate A beside
        him (red ball knob on a gray shaft, a strip of glass between it and the pillar), the duck on the roof
        facing left, antenna upright, an exhaust cloud behind the left fender (frame 0 = the reduced-motion still)
   700  a gentle suspension bob: car and Clawd rise 1 cell together, the duck rides up a beat later; the car
        settles first, its riders float a moment, then settle too
  2600  BUMP: the car pops up and squishes the duck into the roof (squeak!); the car drops, Clawd floats a
        beat with a startled blink, the duck is launched, turns around at the top of its hop and lands
        facing right with a little squash; the antenna whips and wobbles out
  3550  he glances up at the roof (what was that squeak?) .. back to the road, a calm second
  5250  SHIFT UP: a look at the stick and his right hand comes off the wheel (anticipation) .. he grips the
        stick under the knob
  5970  .. CLUNK: the knob drops into gate B (his hand goes down with it), a gold tick spark, the antenna
        flicks, he is jolted in his seat and the engine revs out a fat cloud .. eyes back on the road first,
        then the hand returns to the wheel
  6900  calm cruise (a blink)
  8000  HELLO: a little wave for you (raise, wiggle, raise), then back on the wheel
  8660  calm cruise (every third loop the car winks its right headlight at 9000: it closes a green lid, opens
        with a twinkle) .. a quick double blink
 10500  SHIFT DOWN, practiced: no look, no rev, no jolt: hand to the knob .. CLUNK back into gate A, the spark
        and the antenna carry it, he lets go at once; the clunk pops the duck up, it turns back to face left at
        the top of the hop and lands
 11220  calm cruise across the loop seam, into the gentle bob
Independent layers:
  exhaust (7.1 s): a medium puff (it wraps the loop seam: frame 0's cloud) and a small putt that leaves one
                   curl, at uneven gaps (3.5 s, 2.8 s); 7.1 s vs 12 s is nearly co-prime (LCM 14.2 min): the
                   first pass stays clear of the rev cloud, later passes line the puffs up differently every time
  lamp (36 s):     the headlight wink; 36 s = 3 body loops, so it always lands in the same calm stretch with the
                   car at rest (it is part of the car), as a rare surprise in the second loop of every three
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'manual-drive'
STATE = 'Default (manual) permission mode, variant: manual transmission'
DESC = ('Cruises a tiny mint bubble car with a rubber duck on the roof: hands on the wheel, he works the '
        'red-knobbed gear stick (clunk!), a bump squeaks the duck into a flip, and he waves hi.')


# ---------------------------------------------------------------- the car (local sprites)
# roles: 1 base, 2 highlight (light from the top-left), 3 shade, 5 glass; any other char = palette color
_BODY_COL = {'1': 'g', '2': 'h', '3': 'G', '5': 'C'}
_CAR = {
    9:  [(10, 20, '1')],
    10: [(8, 9, '1'), (10, 12, '2'), (13, 21, '1'), (22, 22, '3')],
    11: [(8, 8, '1'), (9, 21, '5'), (22, 22, '3')],
    12: [(7, 7, '1'), (8, 22, '5'), (23, 23, '3')],
    13: [(7, 7, '1'), (8, 22, '5'), (23, 23, '3')],
    14: [(4, 5, '1'), (7, 7, '1'), (8, 22, '5'), (23, 23, '3'), (25, 26, '1')],
    15: [(3, 3, '1'), (4, 4, 'W'), (5, 5, 'Y'), (6, 7, '1'), (8, 22, '5'), (23, 23, '3'), (24, 24, '1'),
         (25, 25, 'W'), (26, 26, 'Y'), (27, 27, '3')],
    16: [(2, 3, '1'), (4, 5, 'Y'), (6, 7, '1'), (8, 22, '5'), (23, 24, '1'), (25, 26, 'Y'), (27, 27, '1'),
         (28, 28, '3')],
    17: [(2, 6, '1'), (7, 23, '2'), (24, 27, '1'), (28, 28, '3')],
    18: [(2, 2, '3'), (7, 22, 'm'), (23, 23, 's'), (28, 28, '3')],      # bumper row (synced: it lifts away)
}
_BUMPER_ROW = 18
_TIRES = {18: [(3, 3, 'N'), (4, 5, 'K'), (6, 6, 'n'), (24, 24, 'N'), (25, 26, 'K'), (27, 27, 'n')],
          19: [(3, 4, 'n'), (5, 5, 'N'), (6, 6, 'n'), (24, 25, 'n'), (26, 26, 'N'), (27, 27, 'n')]}
_TIRE_TOPS = [(3, 6), (24, 27)]  # row 17 shows more tire while the body is lifted
_SEAT_HOLE = (11, 19, 12, 16)    # no glass where his body always is, so his eye holes show the real background
_GLINT = [(9, 12), (10, 11)]     # a little shine on the windshield (light from the top-left)


def _segments(table, dy, keep):
    f = Frame()
    for y, segs in table.items():
        for x0, x1, ch in segs:
            if keep(ch, y):
                for x in range(x0, x1 + 1):
                    f.put(x, y + dy, _BODY_COL.get(ch, ch))
    return f


def _car_body(dy, bumper=True):
    return _segments(_CAR, dy, lambda ch, y: ch != '5' and (bumper or y != _BUMPER_ROW))


def _glass(dy):
    f = _segments(_CAR, dy, lambda ch, y: ch == '5')
    for x, y in _GLINT:
        f.put(x, y + dy, 'W')
    x0, x1, y0, y1 = _SEAT_HOLE
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            f.px.pop((x, y), None)
    return f


def _wheel(dy):
    """Steering wheel seen edge-on just above the dash; his hands rest on it. It belongs to the car."""
    f = Frame()
    f.hline(10, 20, 16 + dy, 'n')
    f.put(15, 16 + dy, 'm')                   # horn button
    return f


def _bumper():
    """Resting bumper row: a synced layer, so a lifted car leaves a real gap (background) under it."""
    return Frame({k: v for k, v in _car_body(0).px.items() if k[1] == _BUMPER_ROW})


def _cabin():
    """Glass + the gear stick in gate A: drawn BEFORE Clawd, so the hand that grips the stick covers its shaft."""
    f = _glass(0)
    f.px.update(_lever_cells('A', 0))
    return f


def _lift_overlay():
    """Only the cells that differ while the car is lifted 1 cell: the raised body, glass, wheel and gear stick,
    plus taller tires. The resting car stays in static layers (the bumper row is synced), so every cell the
    lifted car vacates is either covered here or really empty."""
    rest, up = {}, {}
    for fr in (_glass(0), _wheel(0), _car_body(0, bumper=False), Frame(_lever_cells('A', 0))):
        rest.update(fr.px)
    for fr in (_glass(-1), _wheel(-1), _car_body(-1), Frame(_lever_cells('A', -1))):
        up.update(fr.px)
    f = Frame()
    for c in sorted(up):
        if rest.get(c) != up[c]:
            f.put(c[0], c[1], up[c])
    for x0, x1 in _TIRE_TOPS:
        for x in range(x0, x1 + 1):
            f.put(x, 17, 'n')
    vacated = [c for c in rest if c not in up and c not in f.px]
    assert not vacated, vacated
    return f


# ---------------------------------------------------------------- the gear stick (red ball knob on a gray shaft)
_STICK_X = 21                    # shaft column; the 2x2 knob covers x 21-22; x 22 below the knob stays glass,
_KNOB_TOP = {'A': 12, 'B': 13}   # so the stick never touches the dark-green pillar (x 23). B = one gate lower


def _lever_cells(gate, dy):
    """Round red knob (pink glint top-left, dark-red shade bottom-right) on a gray shaft that rises from
    behind the wheel. His grip cells sit right under the knob: 'out' (21, 14) in gate A, 'low' (21, 15) in B."""
    top = _KNOB_TOP[gate] + dy
    x = _STICK_X
    cells = {(x, top): 'p', (x + 1, top): 'r', (x, top + 1): 'r', (x + 1, top + 1): 'R'}
    for y in range(top + 2, 17 + dy):
        cells[(x, y)] = 'N'
    return cells


def _lever(s):
    """Gate A lives in the static cabin (and the lift overlay); this synced layer (also before Clawd) only
    draws gate B over it, with gate A's knob painted back to glass."""
    f = Frame()
    if s['knob'] != 'A':
        assert s['car'] == 0, s
        rest, knob = _lever_cells('A', 0), _lever_cells(s['knob'], 0)
        for c in rest:
            if c not in knob:
                f.put(c[0], c[1], 'C')
        for c, ch in knob.items():
            if rest.get(c) != ch:
                f.put(c[0], c[1], ch)
    return f


def _clunk(s):
    """The clunk: a little gold tick spark (library sparkle_small) popping off the knob's top-right corner,
    drawn over the pillar (after the car)."""
    f = Frame()
    if s['clunk'] is not None:
        top = _KNOB_TOP[s['knob']] + s['car']
        knob = _lever_cells(s['knob'], s['car'])
        spark = get('sparkle_small').sprite(1 + s['clunk'])
        for sx, sy, ch in spark.cells:
            c = (_STICK_X + 2 + sx - spark.ax, top - 1 + sy - spark.ay)
            if c not in knob:
                f.put(c[0], c[1], ch)
    return f


# ---------------------------------------------------------------- riders: rubber duck + antenna
def _duck_sprite(face):
    s = get('rubber_duck_held').sprite(0)       # small upright duck, beak to the right
    if face == 'l':
        s = s.flipped()
    bottom = [x for x, y, c in s.cells if y == s.y1]
    cx = (min(bottom) + max(bottom)) // 2        # keep its seat centered on the roof when it turns
    return s.with_anchor(cx, s.y1 + 1)


def _duck(s):
    f = Frame()
    f.place(_duck_sprite(s['face']), 15, 9 + s['duck'])      # absolute: it lags the car's moves
    return f


def _squeak(s):
    """squeak! a gold zigzag just in front of the squished duck's beak (found from the library sprite, so it
    stays aligned if the duck is polished: today the beak tip is at (12, 6) and the zigzag at x 9-10, rows 3-7)."""
    f = Frame()
    if s['squeak']:
        d = Frame()
        d.place(_duck_sprite(s['face']), 15, 9)
        beak = [k for k, ch in d.px.items() if ch == 'o'] or list(d.px)
        if s['face'] == 'l':
            x0, step = min(x for x, _ in beak) - 2, -1
        else:
            x0, step = max(x for x, _ in beak) + 2, 1
        y0 = min(y for _, y in beak) - 2
        for i in range(5):
            f.put(x0 + step * (i % 2), y0 + i, 'j')
    return f


def _antenna(s):
    """Whip antenna on the right fender: steel stalk, 2-cell blue bead (the red ball belongs to the gear knob).
    ant = (stalk lean, bead lean): the stalk's top bends, or only the bead wobbles (half amplitude)."""
    f = Frame()
    bx, by = 26, 13 + s['car']
    lean, bead = s['ant']
    for k in range(5):
        f.put(bx + (lean if k >= 3 else 0), by - k, 's')
    f.put(bx + bead, by - 5, 'b')
    f.put(bx + bead, by - 6, 'b')
    return f


# ---------------------------------------------------------------- Clawd
def _pose(s):
    if s['r'] == 'low':
        # 'out' with the hand one row lower: he holds the stick down in gate B (hand right under the knob)
        assert s['l'] == 'front', s
        base = clawd(eyes=s['eyes'], larm=s['l'], rarm='out', legs='none')
        d = {(x, y): ch for x, y, ch in base.sprite.cells}
        d[(11, 3)] = d.pop((11, 2))
        w, h = max(x for x, _ in d) + 1, max(y for _, y in d) + 1
        return Pose.from_rows([''.join(d.get((x, y), '.') for x in range(w)) for y in range(h)], name='clawd')
    return clawd(eyes=s['eyes'], larm=s['l'], rarm=s['r'], legs='none')


def _clawd(s):
    f = Frame()
    put_clawd(f, _pose(s), HOME[0], HOME[1] + s['cl'])
    for k in [k for k in f.px if k[1] >= 16]:
        del f.px[k]                               # always behind the wheel or the dash: keep the SVG small
    return f


# ---------------------------------------------------------------- the shared timeline
_START = dict(car=0, cl=0, duck=0, face='l', ant=(0, 0), eyes='open', l='front', r='front', knob='A',
              clunk=None, rev=None, squeak=0)

_BEATS = [
    (700, {}),                                                        # 0 cruise (frame 0)
    # a gentle suspension bob: car + Clawd up together, the duck rides up a beat later, the riders float
    (120, dict(car=-1, cl=-1)),                                       # 700
    (260, dict(duck=-1)),                                             # 820
    (140, dict(car=0)),                                               # 1080
    (1380, dict(cl=0, duck=0)),                                       # 1220
    # BUMP: the car pops up and squishes the duck (squeak!) .. Clawd floats, the duck is launched
    (100, dict(car=-1, cl=-1, ant=(1, 1), squeak=1)),                 # 2600
    (100, dict(car=0, duck=-1, ant=(-1, -1), eyes='blink')),          # 2700 whoa
    (110, dict(cl=0, duck=-2, ant=(0, 1), squeak=0, eyes='open')),    # 2800
    (130, dict(face='r', ant=(0, 0))),                                # 2910 the duck turns at the top
    (100, dict(duck=-1)),                                             # 3040
    (70, dict(duck=1)),                                               # 3140 .. lands with a little squash
    (340, dict(duck=0)),                                              # 3210
    # glance at the roof: what was that?
    (700, dict(eyes='look_u')),                                       # 3550
    (1000, dict(eyes='open')),                                        # 4250 calm
    # SHIFT UP: a look at the stick as the hand leaves the wheel (it frames his glancing eye), grip, CLUNK,
    # seat jolt, rev cloud
    (300, dict(eyes='look_r', r='side')),                             # 5250
    (420, dict(r='out')),                                             # 5550 hand on the stick, under the knob
    (80, dict(knob='B', r='low', clunk=0, ant=(1, 1))),               # 5970 CLUNK
    (90, dict(cl=-1, clunk=1, rev=('u', 0), ant=(0, -1))),            # 6050 jolted
    (110, dict(cl=0, clunk=None, rev=('u', 1), ant=(0, 0))),          # 6140
    (140, dict(rev=('u', 2))),                                        # 6250
    (170, dict(rev=('u', 3))),                                        # 6390
    (140, dict(rev=None)),                                            # 6560
    (120, dict(eyes='open')),                                         # 6700 eyes back on the road first
    (80, dict(r='side')),                                             # 6820
    # calm cruise
    (550, dict(r='front')),                                           # 6900
    (120, dict(eyes='blink')),                                        # 7450
    (430, dict(eyes='open')),                                         # 7570
    # HELLO: a little wave for you: raise, wiggle out, back, down
    (80, dict(l='side')),                                             # 8000
    (170, dict(l='raise')),                                           # 8080
    (150, dict(l='wave')),                                            # 8250
    (170, dict(l='raise')),                                           # 8400
    (90, dict(l='side')),                                             # 8570
    # calm cruise (the lamp layer's wink lands at 9000-9510 every third loop), a quick double blink
    (940, dict(l='front')),                                           # 8660
    (110, dict(eyes='blink')),                                        # 9600
    (120, dict(eyes='open')),                                         # 9710
    (100, dict(eyes='blink')),                                        # 9830
    (570, dict(eyes='open')),                                         # 9930
    # SHIFT DOWN, practiced: no look, no rev, no jolt; CLUNK back into gate A, he lets go at once; the clunk
    # pops the duck up, it turns back to face left at the top of the hop and lands
    (80, dict(r='side')),                                             # 10500
    (280, dict(r='low')),                                             # 10580 hand on the stick (gate B)
    (80, dict(knob='A', r='out', clunk=0)),                           # 10860 CLUNK
    (90, dict(clunk=1, duck=-1, ant=(0, 1))),                         # 10940 the duck hops
    (120, dict(r='side', clunk=None, face='l', ant=(0, 0))),          # 11030 lets go; the duck turns at the top
    (70, dict(duck=1)),                                               # 11150 .. lands
    (680, dict(duck=0, r='front')),                                   # 11220
]
LOOP = 12000


def _ticks():
    st, out = dict(_START), []
    for ms, ch in _BEATS:
        st = dict(st, **ch)
        assert st['car'] == 0 or st['cl'] == st['car'], st    # a lifted car always carries Clawd up with it
        assert st['car'] == 0 or st['r'] == 'front', st       # .. with his hands on the wheel (stick at rest)
        out.append((dict(st), ms))
    rest = LOOP - sum(ms for _, ms in out)
    assert rest >= 100, rest
    out.append((dict(_START), rest))            # cruise into the loop
    return out


# ---------------------------------------------------------------- per-layer renderers
_REV_PATH = {'u': {0: (2, 13), 1: (3, 12), 2: (4, 11), 3: (4, 10)}}   # up-shift: a fat cloud, frames 0-3


def _rev(s):
    f = Frame()
    if s['rev'] is not None:
        kind, k = s['rev']
        f.place(get('smoke_puff').sprite(k), *_REV_PATH[kind][k])
    return f


def _split(name, frames):
    """Cells drawn in every frame of a synced layer go into a one-frame static layer (in their most-shown
    color); each animated frame then only carries the cells that differ from it. Same picture, much
    smaller SVG (the animated layer draws over the static one)."""
    keys = None
    for f, _ in frames:
        keys = set(f.px) if keys is None else keys & set(f.px)
    if not keys:
        return [layer(name, frames)]
    still = Frame()
    for k in sorted(keys):
        shown = {}
        for f, ms in frames:
            shown[f.px[k]] = shown.get(f.px[k], 0) + ms
        still.px[k] = max(sorted(shown), key=lambda c: shown[c])
    moving = []
    for f, ms in frames:
        g = Frame({k: v for k, v in f.px.items() if still.px.get(k) != v})
        g.meta = f.meta
        moving.append((g, ms))
    return [static(name + '-still', still), layer(name, moving)]


# ---------------------------------------------------------------- exhaust (independent loop)
_EXHAUST_LOOP = 7100
_WISP = Sprite(['m.', '.N'], anchor=(0, 1), name='exhaust_wisp')   # what is left of a small puff
_PUFFS = [   # (sprite: smoke_puff frame or 'w' = wisp or None, anchor x, anchor y, ms)
    (1, 3, 11, 160), (3, 4, 10, 200),                   # MEDIUM puff (swells, peels into curls), wraps the seam
    (None, 0, 0, 3500),
    (0, 3, 12, 130), ('w', 3, 12, 160),                 # a SMALL putt: a little puff, then one curl drifts off
    (None, 0, 0, 2780),
    (0, 3, 12, 170),                                    # the medium puff starts
]


def _exhaust():
    out = []
    for k, x, y, ms in _PUFFS:
        f = Frame()
        if k == 'w':
            f.place(_WISP, x, y)
        elif k is not None:
            f.place(get('smoke_puff').sprite(k), x, y)
        out.append((f, ms))
    assert sum(ms for _, ms in out) == _EXHAUST_LOOP
    return out


# ---------------------------------------------------------------- headlight wink (independent loop)
_LAMP_LOOP = 3 * LOOP                  # always the same calm stretch of the body loop (car at rest) ..
_WINK_AT = LOOP + 9000                 # .. in the second loop of every three
_LAMP = [(25, 15), (26, 15), (25, 16), (26, 16)]   # the right headlight (clear of the exhaust)
_TWINKLE_AT = (28, 14)                 # off the lamp's top-right corner, clear of the antenna


def _lamp(ticks):
    """The car winks at you: a green lid (body green, dark-green lash line) shuts its right headlight for
    one of Clawd's blink lengths, then the lamp opens with a twinkle (0-1-2-1)."""
    car = _car_body(0)
    shut = Frame()
    for x, y in _LAMP:
        shut.put(x, y, 'g' if y == 15 else 'G')
    seq = [(Frame(), _WINK_AT), (shut, 150)]
    for k in (0, 1, 2, 1):
        f, spr = Frame(), get('sparkle_small').sprite(k)
        for sx, sy, ch in spr.cells:
            c = (_TWINKLE_AT[0] + sx - spr.ax, _TWINKLE_AT[1] + sy - spr.ay)
            if c not in car.px:
                f.put(c[0], c[1], ch)
        seq.append((f, 90))
    w0 = _WINK_AT % LOOP
    w1, t = w0 + sum(ms for _, ms in seq[1:]), 0
    for s, ms in ticks:                       # drawn on the resting car: the car must be at rest the whole wink
        assert not (t < w1 and t + ms > w0) or s['car'] == 0, (t, s)
        t += ms
    seq.append((Frame(), _LAMP_LOOP - sum(ms for _, ms in seq)))
    return layer('lamp', seq)


def build():
    ticks = _ticks()
    synced = lambda fn: [(fn(s), ms) for s, ms in ticks]
    lift, bumper = _lift_overlay(), _bumper()
    layers = [layer('exhaust', _exhaust()), layer('rev', synced(_rev)),
              static('tires', _segments(_TIRES, 0, lambda ch, y: True)), static('cabin', _cabin()),
              layer('lever', synced(_lever))]
    layers += _split('clawd', synced(_clawd))
    layers += [static('wheel', _wheel(0)), static('car', _car_body(0, bumper=False)),
               layer('car-bob', synced(lambda s: lift if s['car'] else bumper))]
    layers += [_lamp(ticks)]
    layers += _split('duck', synced(_duck))
    # antenna + clunk spark + squeak share one synced layer: they change on the same ticks (fewer SVG frames)
    layers += _split('fx', synced(lambda s: _antenna(s).over(_clunk(s)).over(_squeak(s))))
    return anim(NAME, DESC, layers, state=STATE)
