"""idle-bubbles - Idle variant: blowing soap bubbles.

STORYBOARD (s)    one loop = 18.00 s; holds = 50% (1.1 + 1.8 + 1.0 + 1.2 + 3.9 s), one long rest, one story at a time
   0.00  frame 0 (the reduced-motion still): at HOME, green bubble wand held up (leaning right), a tub of soap at
         his feet, and a bubble (blown by the small wave at the end of the loop) hanging over his head; eyes up on it.
         It has hung there since 17.80: HOLD 1.1 s across the seam
   0.90  .. pop: a sparkle with 4 specks, then the specks fly out (library soap_bubble pop frame)
   1.11  he keeps watching the spot .. blinks (1.37) .. HOLD 1.8 s, eyes on you
   3.30  a look down at the tub (0.6 s): the ring is empty, time for a dip
   3.90  DIP: the wand swings down, his arm reaches out (4.02), the ring goes half under (a ripple, 4.13), all the way
         in (the ripple spreads, 4.23) and soaks, comes half out (4.63) and out with a SOAP FILM (4.73: white glint
         core wrapped in cyan + pink sheen, lavender low right)
   4.86  he looks up at it as a drop falls from the ring, speeding up (rows 14 -> 15 -> 17); the ring swings up past
         rest (follow-through, 5.13) and settles (5.24) as the drop lands in the soap: plip (ripple + blink)
   5.38  BREATH 1.0 s: he admires the loaded ring
   6.38  THE WAVE: anticipation (tilts back, 300 ms), then the hand leads (6.84: the arm reaches out, the grip drops)
         while the ring drags behind and overshoots low (6.94); the film bulges out of its trailing side as a bud,
         grows, and is released as the ring settles low (7.08); what is left of the film sags in the ring
   7.08  the big one, the only thing moving: fast off the wand, his eyes up-right; over his head (7.44, eyes up), its
         crest (7.97); it drifts left, sinks, floats (8.94: up-left now, he raises his free hand via 'up'), sinks,
         sways back under itself, slows ..
  10.31  .. and settles on his fingertip: it rests there, HOLD 1.2 s
  11.51  pop: a droplet stays on his fingertip (11.72), rides his hand down via 'up' (11.97) .. he looks at it
         (12.07) .. blink: it is gone (12.37)
  12.50  HOLD 3.9 s, eyes on you: the one long rest
  16.43  THE SMALL WAVE (smaller and lazier than the first): he lifts the lowered wand back up (anticipation), sweeps
         it out (16.78: the hand leads again, a blink); the last of the film buds off behind as one more bubble and
         the ring is empty again (16.88); the bubble floats up, his eyes follow it (17.20: up), it rises a little past
         its spot (17.46) and settles into frame 0's hover (17.80)

Blinks: scripted after b0's pop, at the plip, when the droplet vanishes and on the small sweep.  The eyelid layer
runs 1.5 loops (27 s): one extra blink in the opening hold in one loop, one while the bubble rests on his fingertip
in the next, none in the third; always >= 0.6 s from a scripted closure, so never a flutter.

Timing model: every change is an event at an absolute time (_script); each layer gets a frame boundary only where its
own tracks change.  b0's flight is written in one piece across the seam (its sheen swirls every other step,
continuous through the seam).  Different layers' changes either coincide or are >= 80 ms apart (asserted).
Face: kit eyes only, and only where both holes stay enclosed (asserted): look_ur only with the wand arm 'up', look_r
while the arm is 'out', look_ul only with the left hand 'up' or 'high', look_l with the left arm at the side.
Normal body size throughout.
Layers (back to front): tub_back (static) | body (static: Clawd minus the cells that ever change) | face (eye rows,
both arms, the raised fingertip) | blink (1.5-loop eyelids) | wand (+ film) | tub_front (static: soap + front wall,
so the wand dips INTO the tub) | bubbles (b0 + the big one + their pops; never in the air together) | splash (the
drop and the ripples).  Every change time is checked: bubbles never overlap each other, the wand or him; particles
never cover him.
Library: soap_bubble (big bubble, its sheen and its pop), sparkle_small (the pop flash, recolored to soap).
Local: the bubble wand (the library 'wand' is a magic star wand), the tub, the bud stages, the drop and ripples.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'idle-bubbles'
STATE = 'Idle variant: blowing soap bubbles'
DESC = ('Blows soap bubbles: dips his wand in a tub of soap and waves it gently; his eyes follow the bubble on its '
        'lazy, wobbly flight until it settles on his raised fingertip and pops.')

LOOP = 18000


# =====================================================================================================
# Local sprites (the library 'wand' is a magic star wand, so the bubble wand and tub are drawn here)
# =====================================================================================================
def _ring(cx, cy):
    """5x5 wand ring around (cx, cy): base 'g' top/left, shade 'G' bottom/right, lime shine top-left."""
    cells = []
    for dx in (-1, 0, 1):
        cells.append((cx + dx, cy - 2, 'g'))
        cells.append((cx + dx, cy + 2, 'G'))
    for dy in (-1, 0, 1):
        cells.append((cx - 2, cy + dy, 'g'))
        cells.append((cx + 2, cy + dy, 'G'))
    cells += [(cx - 1, cy - 2, 'a'), (cx - 2, cy - 1, 'a')]
    return cells


# stick cells (grip first) and ring centre, relative to the grip
_ORIENT = {
    'r1':   ([(0, 0), (0, -1), (1, -2)], (2, -5)),
    'r2':   ([(0, 0), (1, -1), (2, -2)], (4, -4)),
    'r3':   ([(0, 0), (1, 0), (2, -1)], (5, -2)),
    'h':    ([(0, 0), (1, 0), (2, 0)], (5, 0)),
    'half': ([(0, 0), (1, 1)], (4, 3)),                         # ring half under the soap (tub_front hides the rest)
    'dip':  ([(0, 0), (1, 1), (2, 2), (3, 3)], None),           # ring all the way in
}
# soap film inside the ring (relative to its centre), coloured like the bubbles so it reads on both themes:
#   2 = loaded: a white glint core wrapped in cyan + pink sheen (top-left), a lavender sheen low right
#   1 = what is left after the big bubble took its share: the film sags into the bottom of the ring
_FILM = {0: [], 1: [(0, 1, 'l'), (1, 1, 'c')], 2: [(-1, -1, 'W'), (0, -1, 'c'), (-1, 0, 'p'), (1, 1, 'l')]}


def _wand_sprite(orient, film):
    stick, centre = _ORIENT[orient]
    d = {}
    for i, (x, y) in enumerate(stick):
        d[(x, y)] = 'G' if i == 0 else 'g'
    if centre is not None:
        for x, y, ch in _ring(*centre):
            d[(x, y)] = ch
        for dx, dy, ch in _FILM[film]:
            d[(centre[0] + dx, centre[1] + dy)] = ch
    return Sprite(cells=[(x, y, ch) for (x, y), ch in d.items()], anchor=(0, 0),
                  name='bubble_wand_%s_%d' % (orient, film))


_WAND_KEYS = [(o, f) for o in _ORIENT for f in sorted(_FILM)]
_WAND = Item('bubble_wand', 'hand', 'Green toy bubble wand: 5x5 ring on a stick (grip = anchor), optional soap film.',
             [_wand_sprite(o, f) for o, f in _WAND_KEYS])

# tub of soap, split so the wand dips INTO it: back rim (before the wand), soap + front wall (after it).
# The soap is tinted like a bubble film (lavender/cyan, one glint), enclosed by the blue rim on both themes.
_TUB_BACK = Sprite(['.bbbbb.'], anchor=(3, 0), name='tub_back')
_TUB_FRONT = Sprite(['bclWlcb',
                     '.BbbbB.'], anchor=(3, -1), name='tub_front')
TUB = (26, 17)                    # back rim centre; the soap is row 18
# rings spreading on the soap: the glint splits and runs outward
_RIPPLE = {1: Sprite(['WlW'], anchor=(1, 0), name='ripple_1'), 2: Sprite(['WlclW'], anchor=(2, 0), name='ripple_2')}

# bubbles (anchor = centre; for the 4x4 one the glint cell, upper-left of its middle)
_SOAP = get('soap_bubble')        # big 5x5 bubble: the sheen swirls through its frames; the last frame = pop
_SHEENS = max(1, len(_SOAP.frames) - 1)
_MID = Sprite(['.ll.',
               'lW.c',
               'p..c',
               '.cc.'], anchor=(1, 1), name='bubble_mid')
_TINY = Sprite(['.l.',
                'l.c',
                '.c.'], anchor=(1, 1), name='bubble_tiny')
_DROP = Sprite(['c'], anchor=(0, 0), name='drop')

# pop flash from the library's sparkle_small (its '+'), recolored to soap
_SPARK = get('sparkle_small').sprite(1).recolor({'j': 'l', 'y': 'W'})


def _pts(*cells):
    return Sprite(cells=list(cells), anchor=(0, 0))


def _specks(d):
    """4 droplets on the diagonals at distance d (lit colours top-left)."""
    return _pts((-d, -d, 'l'), (d, -d, 'c'), (-d, d, 'p'), (d, d, 'c'))


_FX = {    # particles, each a list of sprites placed at the popped bubble's centre
    # a big bubble pops in the open air: flash + specks, then the library's own pop frame (specks fly out)
    'pop_a':  [_specks(2), _SPARK],
    'pop_b':  [_SOAP.sprite(_SHEENS)],
    # the big one, on his fingertip (his head is down-right of it, so that speck becomes the droplet on his hand)
    'hand_a': [_specks(2), _SPARK],
    'hand_b': [_pts((-3, -3, 'l'), (3, -3, 'c'), (-3, 3, 'p'), (1, 2, 'c'))],
    'drip':   [_DROP],
}
_BUBBLE_KINDS = ('big', 'mid', 'tiny')


# =====================================================================================================
# The script: every change at an absolute time (ms).  Tracks:
#   rig  = (rarm, wand orientation)   film = 0 | 1 | 2   eyes = kit eyes   larm = his free arm
#   b0 / hero = (kind, x, y) | None; kind = big | mid | tiny | an _FX key (pop particles)
#   drop = (x, y) | None   ripple = 1 | 2 | None
# =====================================================================================================
R = ('up', 'r2')                 # rest: wand held up, leaning right (ring centre (25, 9))
LOW = ('up', 'r3')               # lowered rest after the first wave (ring centre (26, 11))

HOLD_A = 1800                    # the opening hold (after b0's pop)
GLANCE = 600                     # look at the tub before the dip
BREATH = 1000                    # admiring the loaded ring
REST = 1200                      # the bubble resting on his fingertip
# the big one's flight: (x, y, ms, extra events); his eyes and his free hand join in at the marked steps
HERO = [
    (21, 8, 160, {}),                                  # off the wand, fast ..
    (19, 7, 200, {}),
    (17, 6, 250, dict(eyes='look_u')),                 # .. over his head now
    (16, 5, 280, {}),
    (15, 4, 310, {}),                                  # crest
    (14, 4, 340, {}),                                  # drifts left ..
    (13, 5, 320, {}),                                  # .. sinks ..
    (12, 5, 320, dict(larm='up', eyes='look_ul')),     # .. floats (up-left now: he raises his hand) ..
    (11, 6, 290, {}),                                  # .. sinks ..
    (11, 7, 340, {}),                                  # .. sways back under itself ..
    (10, 8, 420, {}),                                  # .. slows ..
]
HERO_LAND = (9, 9)                                     # .. and settles on his fingertip
# b0 off the small wave: bud, grows, floats up a little past its spot and settles into frame 0's hover
B0 = [('tiny', 24, 9, 100, {}), ('mid', 22, 7, 140, {}), ('big', 20, 5, 180, {}),
      ('big', 18, 4, 260, dict(eyes='look_u')),       # over his head now (frame 0's gaze)
      ('big', 17, 3, 340, {})]                        # a little past its spot ..
B0_HOVER = (16, 4)
B0_SETTLED = 200                 # b0 reaches its hover this long before the seam ..
B0_POP = 900                     # .. and pops this long after it
TIMES = {}                       # the beat times, filled by _script() (for the storyboard / checks)


def _script():
    ev = {}

    def at(t, **kw):
        for k, v in kw.items():
            ev.setdefault(k, []).append((t, v))

    def seq(t, steps):
        for ms, kw in steps:
            at(t, **kw)
            t += ms
        return t

    # 0.00  frame 0: b0 hangs over his head (its whole flight is written at the small wave: it crosses the seam)
    at(0, rig=R, film=0, larm='side', eyes='look_u', hero=None, drop=None, ripple=None)
    TIMES['blink0'] = B0_POP + 90 + 120 + 260                  # b0's pop (0.90) is gone at 1.11: he watches the spot ..
    t = seq(TIMES['blink0'], [(130, dict(eyes='blink')),        # .. blink
                   (HOLD_A, dict(eyes='open'))])                # HOLD
    TIMES['glance'] = t
    t = seq(t, [(GLANCE, dict(eyes='look_d'))])                 # a look at the tub
    # dip
    TIMES['dip'] = t
    t = seq(t, [
        (120, dict(rig=('up', 'r3'))),
        (110, dict(rig=('out', 'h'))),
        (100, dict(rig=('out', 'half'), ripple=1)),             # half under: a ripple ..
        (400, dict(rig=('out', 'dip'), ripple=2)),              # .. all the way in: it spreads; soak
        (100, dict(rig=('out', 'half'))),
        (130, dict(rig=('out', 'h'), film=2)),                  # out, with a soap film
        (150, dict(rig=('up', 'r3'), eyes='look_ur', drop=(26, 14), ripple=None)),   # a drop falls from the ring ..
        (120, dict(rig=R, drop=(26, 15))),
        (110, dict(rig=('up', 'r1'), drop=(26, 17))),           # .. speeding up; the ring swings past rest ..
        (140, dict(rig=R, drop=None, ripple=1, eyes='blink')),  # .. and settles: plip
    ])
    TIMES['breath'] = t
    t = seq(t, [(BREATH, dict(ripple=None, eyes='look_ur'))])   # BREATH: he looks at the loaded ring
    # the wave: tilt back, the hand leads out and down while the ring drags, overshoots low, settles
    TIMES['wave'] = t
    t = seq(t, [
        (300, dict(rig=('up', 'r1'))),
        (160, dict(rig=R)),
        (100, dict(rig=('out', 'r3'), eyes='look_r', hero=('tiny', 24, 9))),     # the film bulges out behind ..
        (140, dict(rig=('out', 'h'), hero=('mid', 23, 10))),                      # .. grows at the overshoot ..
    ])
    at(t, rig=LOW, eyes='look_ur', film=1)                      # .. and is released as the ring settles low
    TIMES['release'] = t
    for x, y, ms, extra in HERO:
        at(t, hero=('big', x, y), **extra)
        if extra.get('larm') == 'up':
            at(t + 100, larm='high')                            # (the arm passes 'up' for 100 ms)
        t += ms
    at(t, hero=('big',) + HERO_LAND)
    TIMES['land'] = t
    t += REST
    hx, hy = HERO_LAND
    TIMES['pop'] = t
    t = seq(t, [
        (90, dict(hero=('hand_a', hx, hy))),                    # pop!
        (120, dict(hero=('hand_b', hx, hy))),
        (250, dict(hero=('drip', 10, 11))),                     # a droplet stays on his fingertip
        (100, dict(hero=('drip', 10, 12), larm='up')),          # hand down (via 'up'), the droplet rides it ..
        (300, dict(hero=('drip', 10, 13), larm='side', eyes='look_l')),   # .. he looks at it ..
        (130, dict(hero=None, eyes='blink')),                   # .. blink: gone
    ])
    at(t, eyes='open')                                          # the long HOLD
    TIMES['rest'] = t
    # the small wave: the last of the film becomes b0, which floats up over his head into frame 0
    t_sweep = LOOP - B0_SETTLED - sum(step[3] for step in B0)
    TIMES['small'] = t_sweep - 350
    seq(t_sweep - 350, [
        (350, dict(rig=R, eyes='look_ur')),                     # anticipation: he lifts the lowered wand
        (100, dict(rig=('out', 'r3'), eyes='blink')),           # sweep, the hand leads; a blink; b0 buds off behind ..
        (310, dict(rig=LOW, eyes='look_ur', film=0)),           # .. it has left: the ring is empty again
    ])
    at(t_sweep + sum(step[3] for step in B0[:3]), rig=R)       # the wand back at rest (frame 0), as b0 clears it
    t = t_sweep
    for kind, x, y, ms, extra in B0:
        at(t, b0=(kind, x, y), **extra)
        t += ms
    at(t, b0=('big',) + B0_HOVER)                               # it settles into the hover (frame 0) ..
    TIMES['hover'] = t
    seq(LOOP + B0_POP, [(90, dict(b0=('pop_a',) + B0_HOVER)), (120, dict(b0=('pop_b',) + B0_HOVER)),
                        (100, dict(b0=None))])                  # .. pop

    # the film swirls a quarter turn every other drift step (continuous along each flight, so also across the seam)
    for name in BUBBLES:
        k, out = 0, []
        for tt, v in sorted(ev.get(name, []), key=lambda e: e[0]):
            if v is not None and v[0] == 'big':
                v = v + (((k + 1) // 2) % _SHEENS,)
                k += 1
            out.append((tt, v))
        ev[name] = out
    return ev


BUBBLES = ('b0', 'hero')
# ambient eyelids on a 1.5-loop cycle (27 s): an extra blink in the opening hold in one loop, while the bubble rests
# on his fingertip in the next, none in the third; >= 0.6 s from every scripted closure (asserted)
BLINK_LOOP = LOOP * 3 // 2
BLINK_MS = 120


def _blink_at():
    """The eyelid layer's blink time (in its first loop): it falls in the opening hold, >= 0.6 s after the scripted
    blink, and its second showing (9 s later, in the next loop) in the bubble's rest on his fingertip, >= 0.3 s
    from either end; the middle of the window that satisfies both."""
    half = BLINK_LOOP - LOOP
    lo = max(TIMES['blink0'] + 600, TIMES['land'] + 300 - half)
    hi = min(TIMES['glance'] - 300 - BLINK_MS, TIMES['pop'] - 300 - BLINK_MS - half)
    assert lo <= hi, 'no room for the ambient blink: %d > %d' % (lo, hi)
    return (lo + hi) // 2


# =====================================================================================================
# Rendering
# =====================================================================================================
def _band(x, y):
    """Cells of Clawd that ever change: the eye rows, both arms, the tip of his raised left hand."""
    return (10 <= x <= 21 and 13 <= y <= 15) or (x, y) == (10, 12)


def _pose(eyes='open', rarm='up', larm='side'):
    """Kit pose; asserts both eye holes stay enclosed (a hole on his edge column needs the arm beside it)."""
    p = clawd(eyes=eyes, larm=larm, rarm=rarm)
    occ = {(x, y) for x, y, c in p.sprite.cells if c != ERASE}
    for x, y in [(x, y) for x in range(1, 10) for y in range(6) if (x, y) not in occ]:
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            assert q in occ, 'eye hole %s is open at %s (eyes=%s larm=%s rarm=%s)' % ((x, y), q, eyes, larm, rarm)
    return p


def _clawd(eyes, rarm, larm, keep):
    f = Frame()
    put_clawd(f, _pose(eyes, rarm, larm))
    for p in list(f.px):
        if _band(*p) != keep:
            del f.px[p]
    return f


def _wand(rig, film):
    rarm, orient = rig
    f = Frame()
    wear(f, _WAND, clawd(rarm=rarm), i=_WAND_KEYS.index((orient, film)))
    return f


def _draw(f, v):
    if v is None:
        return
    kind, x, y = v[0], v[1], v[2]
    if kind == 'big':
        f.place(_SOAP.sprite(v[3]), x, y)
    elif kind == 'mid':
        f.place(_MID, x, y)
    elif kind == 'tiny':
        f.place(_TINY, x, y)
    else:
        for spr in _FX[kind]:
            f.place(spr, x, y)


def _circular(ev):
    """Events -> sorted by time within the loop (later entries win ties)."""
    return {k: [(t % LOOP, v) for t, v in sorted(evs, key=lambda e: e[0] % LOOP)] for k, evs in ev.items()}


def _value(evs, t):
    cur = evs[-1][1] if evs else None          # nothing yet this loop: what the previous loop ended with
    for et, v in evs:
        if et > t:
            break
        cur = v
    return cur


def _times(ev, tracks):
    return sorted({0} | {t for k in tracks for t, _ in ev.get(k, [])})


def _layer(ev, name, tracks, render):
    times = _times(ev, tracks)
    frames = []
    for i, t0 in enumerate(times):
        t1 = times[i + 1] if i + 1 < len(times) else LOOP
        frames.append((render({k: _value(ev.get(k, []), t0) for k in tracks}), t1 - t0))
    return layer(name, frames)


def _bubbles_frame(st, names):
    f = Frame()
    for n in names:
        _draw(f, st.get(n))
    if st.get('drop'):
        f.place(_DROP, *st['drop'])
    if st.get('ripple'):
        f.place(_RIPPLE[st['ripple']], TUB[0], TUB[1] + 1)
    return f


STRICT = True           # every change time must be overlap-free (OVERLAPS lists any)
OVERLAPS = []
LAYER_TRACKS = {'face': ('eyes', 'rig', 'larm'), 'wand': ('rig', 'film'), 'bubbles': BUBBLES,
                'splash': ('drop', 'ripple')}


def _check(ev):
    """Bubbles never overlap each other, the wand or Clawd; particles never cover Clawd.  Layers change together
    or >= 80 ms apart; the eyelid layer's blink stays >= 600 ms from every scripted closure."""
    del OVERLAPS[:]
    for t in sorted({0} | {t for evs in ev.values() for t, _ in evs}):
        st = {k: _value(evs, t) for k, evs in ev.items()}
        wf = _wand(st['rig'], st['film'])
        body = Frame()
        put_clawd(body, _pose(st['eyes'], st['rig'][0], st['larm']))
        owners = {}
        for name in BUBBLES:
            v = st.get(name)
            one = Frame()
            _draw(one, v)
            solid = v is not None and v[0] in _BUBBLE_KINDS
            for p in one.px:
                if p in body.px or (solid and (p in wf.px or p in owners)):
                    OVERLAPS.append((t, name, p))
                owners[p] = name
        if st.get('drop') and (st['drop'] in wf.px or st['drop'] in body.px):
            OVERLAPS.append((t, 'drop', st['drop']))
    if STRICT and OVERLAPS:
        raise AssertionError('overlaps: %s' % OVERLAPS[:6])
    ambient = sorted({_blink_at(), (_blink_at() + BLINK_LOOP) % LOOP})     # its two blinks per 54 s, in loop time
    holds = [(TIMES['blink0'] + 130, TIMES['glance']), (TIMES['land'], TIMES['pop'])]
    for b in ambient:
        assert any(a + 300 <= b and b + BLINK_MS + 300 <= e for a, e in holds), 'ambient blink %d not in a hold' % b
    every = set(t for tr in LAYER_TRACKS.values() for t in _times(ev, tr))
    for extra in ([], ambient + [b + BLINK_MS for b in ambient]):
        ts = sorted(every | set(extra) | {LOOP})
        gaps = [(a, b) for a, b in zip(ts, ts[1:]) if b - a < 80]
        assert not gaps, 'layer changes closer than 80 ms: %s' % gaps[:6]
    closed = [t for t, v in ev['eyes'] if v == 'blink']
    for b in ambient:
        for c in closed:
            d = min(abs(b - c), LOOP - abs(b - c))
            assert d >= 600, 'ambient blink at %d is only %d ms from the scripted one at %d' % (b, d, c)


def build():
    ev = _circular(_script())
    _check(ev)
    face = _layer(ev, 'face', LAYER_TRACKS['face'],
                  lambda s: _clawd(s['eyes'], s['rig'][0], s['larm'], True))
    wand = _layer(ev, 'wand', LAYER_TRACKS['wand'], lambda s: _wand(s['rig'], s['film']))
    bub = _layer(ev, 'bubbles', LAYER_TRACKS['bubbles'], lambda s: _bubbles_frame(s, BUBBLES))
    splash = _layer(ev, 'splash', LAYER_TRACKS['splash'], lambda s: _bubbles_frame(s, ()))

    lids = Frame()
    for x0 in (11, 17):
        lids.rect(x0, 13, 3, 3, '#')
    tb = _blink_at()
    blink = [(Frame(), tb), (lids, BLINK_MS), (Frame(), BLINK_LOOP - tb - BLINK_MS)]

    # holds: stretches >= 1 s where no layer but the ambient eyelids changes (wrapping across the seam)
    cuts = set()
    for lay in (face, wand, bub, splash):
        t, frs = 0, lay['frames']
        for i, fr in enumerate(frs):
            if i or frs[-1]['rows'] != fr['rows']:          # the seam is a cut only where the layer changes there
                cuts.add(t)
            t += fr['ms']
    cuts = sorted(cuts)
    gaps = [b - a for a, b in zip(cuts, cuts[1:] + [cuts[0] + LOOP])]
    holds = [g for g in gaps if g >= 1000]
    assert max(holds) >= 3500 and sum(holds) * 2 >= LOOP, 'holds %s = %d%%' % (holds, 100 * sum(holds) // LOOP)

    tub_back, tub_front = Frame(), Frame()
    tub_back.place(_TUB_BACK, *TUB)
    tub_front.place(_TUB_FRONT, *TUB)
    return anim(NAME, DESC, [
        static('tub_back', tub_back),
        static('body', _clawd('open', 'up', 'side', False)),
        face,
        layer('blink', blink),
        wand,
        static('tub_front', tub_front),
        bub,
        splash,
    ], state=STATE)
