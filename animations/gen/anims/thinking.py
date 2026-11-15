# ======================================================================================
# USER FEEDBACK: the user reviewed this fine-face upgrade draft personally and approved it
# ("looks great go"). Keep the scene, beats and fine-line expressions; critics, fixers and judges
# should polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""thinking - Claude is thinking (extended thinking).   5-90 s on screen: calm, pondering, one little "eureka" per loop.

Expressive style (STYLE.md 0b): his FACE acts with the kit's fine-line eyes (fine() + fine_face(): half-step glances,
thin lids, ◡◡ / ◠◠ arcs, wide and sparkle eyes). No mouth, no blush, never resized: his normal body throughout.
Resting gaze: the half-step look_u, up at the thought cloud. Every glance is a half-step GAZE (one fine pixel: u, ur,
ul, r) and every lid is drawn at the current gaze ('half/u' = the bottom half of his raised eye), so a blink closes
over the pupil where he is looking instead of bobbing the eye down; gaze changes ride on blinks.

Storyboard (one loop = 11.94 s; every layer is cut from one beat table, story(), and the face track, face_track())
  A  RIGHT claw on chin, eyes up at the thought cloud
  0.00  frame 0 = the reduced-motion still: pondering under "..." (half-step look_u); the dots cycle . .. ...
        (0.65 / 1.07 / 1.49)
  1.55  his lids come down over his raised eyes (half/u) into a CONCENTRATED SQUINT (◡◡, 0.74 s): thinking hard ...
  2.28  ... the dots ignite (Claude orange); a beat later (2.36) his eyes snap open on them (look_u)
  2.44  they twinkle into sparks one by one, each drifting out of the "...": left 2.44, right 2.68 (2.76 his eyes
        follow it up-right), middle 2.94 (3.02 back up)
  3.18  the sparks converge, 3.34 merge in a little flash
  3.48  a dull bulb appears and sputters, pulses >= 340 ms apart (< 3 Hz): on 3.78 / dim 4.12; he watches, hoping ...
  4.23  ... it goes dark again: his lids droop (half/u), a moment of doubt ...
  4.47  ... then it comes ON and holds: 4.53 his eyes pop WIDE ("!": one fine row to three)
  4.77  realization: the whole cloud glows warm, SPARKLE eyes (the idea shines in them) and his chin claw falls away
  5.03  anticipation: both claws hang low (200 ms), the sparkle holds
  5.23  a tiny hop with his normal body, PLEASED ◠◠ arcs: 1 up (the claw leads, the free arm drags), 5.31 2 up (legs
        tucked, claw raised, the free arm still trailing), 5.48 1 up (the free arm catches up)
  5.57  lands, the claw dipping with the impact, in a puff of dust (the left puff rolls up against the books); the
        impact squeezes his eyes shut for a beat (line: the face takes the squash, his body never does)
  5.67  the claw pumps "got it!", beaming ◠◠ again; the whoosh flares the candle one beat late, 5.77 / 5.90 it settles
        back (tall and bright, then cooling)
  6.04  the bulb overloads, 6.16 the idea pops: four thought rings + a glint, 6.26 specks; his happy eyes close (line)
  6.38  the claw arcs down toward his chin (raise > up > chin), eyes opening (half) while a new thought-dot already
        rises beside his head
  B  LEFT claw on chin (the mirrored pondering pose)
  6.49  the new thought bubbles up, easing out (110 / 120 / 150 / 190 ms): dot, ring, puff, small cloud, cloud (7.06);
        his eyes rise with it: right at the dot (6.49), then up-right at the ring (6.60), staying on the cloud as it
        inflates there
  7.30  . .. ... and a long look aside at the candle (up-left, 0.85 s); then a quick double blink: the first carries
        his gaze back up to the cloud (8.15 half > line > half, 8.35 look_u), the second brings it down (8.45) ...
  8.64  ... to you: a short look ("one sec...", the official open eyes)
  9.12  back up; 9.50 a second idea: a gray bulb fades in, 9.61 he glances up at it (up-right); 9.93 it glows dimly
        once and never catches: a dud (an idea tested and dropped). 10.05 it dies, and a beat later his lids droop
        over the stare (half, still on the bulb): "hmm... no", deadpan, as he taps his chin twice, the claw coming off
        it (10.39 / 10.67)
 11.03  the lids close (line) as the claw leaves his chin; back to the RIGHT claw, eyes opening (half 11.16) up to the
        cloud (look_u 11.22) as the dud melts into dots (11.16 / 11.52) -> flows into frame 0
Eye closures: 1.55-2.36 (squint), 6.26-6.49, 8.15, 8.45, 11.03-11.22: uneven on purpose.
Ambient (own 4.4 s loop, gcd 20 ms with the story): the candle flame holds steady and only now and then flicks its
tip (lean left 1.50, stretch 2.94, lean right 4.18). Its unchanging root lives in the static study layer.
Face rig: the body layer draws him with a solid face (one frame per pose run, so body frames merge while only his
face acts); the face layer (FINE, half-size pixels) holds only the eye-area pixels that differ from that body: his
black eyes (the kit's EYE_INK), lids, arcs and glints. Together they composite to exactly fine(frame) +
fine_face(...), each eye moved by its half-step gaze (_target). Should the kit ever draw see-through eyes again, the
body run cuts the cells they need (_holes).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                           # noqa: E402

NAME = 'thinking'
STATE = 'Claude is thinking (extended thinking)'
DESC = ('Ponders by candlelight, claw on chin and eyes on his thought cloud: he squints in concentration until the dots '
        'spark into a bulb, goes wide-eyed then sparkly, hops "eureka!" beaming, the idea pops, a new thought bubbles '
        'up as he switches claws, and a second, dud bulb dies to a half-lidded "hmm... no".')

CX, CY = 24, 5            # thought-cloud anchor (its visual center): the cloud spans cols 18-30, rows 1-8


# --------------------------------------------------------------------------------------------
# reuse library sprites (with local copies, used only if the library is mid-save or changes shape)
# --------------------------------------------------------------------------------------------
def _lib(name, fallback):
    """Library item, or a local copy of it while another artist is mid-save (KeyError)."""
    try:
        return get(name)
    except KeyError:
        return fallback()


def _component(spr, seed):
    """Only the 4-connected blob of `spr` that contains `seed` (the cloud without its trailing circles)."""
    cells = {(x, y): c for x, y, c in spr.cells}
    todo, seen = [seed], set()
    while todo:
        p = todo.pop()
        if p in seen or p not in cells:
            continue
        seen.add(p)
        x, y = p
        todo += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return Sprite(cells=[(x, y, cells[(x, y)]) for (x, y) in seen], anchor=(spr.ax, spr.ay))


def _diff(a, b):
    """Cells of `a` that differ from `b` (what an item variant draws on top of the plain cloud)."""
    db = {(x, y): c for x, y, c in b.cells}
    return Sprite(cells=[(x, y, c) for x, y, c in a.cells if db.get((x, y)) != c], anchor=(a.ax, a.ay))


def _minus(a, b):
    """Cells of `a` that `b` does not cover."""
    cover = {(x, y) for x, y, _ in b.cells}
    return Sprite(cells=[c for c in a.cells if (c[0], c[1]) not in cover], anchor=(a.ax, a.ay))


def _rel(spr):
    return {(x - spr.ax, y - spr.ay): c for x, y, c in spr.cells}


def _rel_bounds(spr):
    return (spr.x0 - spr.ax, spr.x1 - spr.ax, spr.y0 - spr.ay, spr.y1 - spr.ay)


_LOCAL_CLOUD = ['...NNN.NNN...',
                '..NWwwNwwwN..',
                '.NwwwwwwwwwN.',
                'NwwwwwwwwwwwN',
                'NwwwwwwwwwwwN',
                'NwwwwwwwwwwMN',
                '.NwwNwwwNwMN.',
                '..NN.NNN.NN..']
_LOCAL_TRAIL = ['.............', '.....NN......', '....NwwN.....', '.....NN......', '...N.........']


def _local_thought(rows3=None, extra=None):
    rows = list(_LOCAL_CLOUD)
    if rows3:
        rows[3] = rows3
    if extra:
        for k, r in extra.items():
            rows[k] = r
    return Item('thought', 'fx', 'local fallback', Sprite(rows + _LOCAL_TRAIL, anchor=(6, 4)))


# Library thought cloud (+ its dots and bulb variants, extracted as the cells they add to the plain cloud).
_TB = _lib('thought_bubble', _local_thought).sprite(0)
_CLOUD = _component(_TB, (_TB.ax, _TB.ay))
_TRAIL = _rel(_minus(_TB, _CLOUD))                          # the trailing ring + the last dot, relative to CX, CY
_DOT_REL = (-3, 8)                                          # library convention: last dot = anchor + (-3, +8)
_RING_CELLS = {p: c for p, c in _TRAIL.items() if p != _DOT_REL}
_dots_item = _lib('thought_dots', lambda: Item('thought_dots', 'fx', 'local fallback', [
    _local_thought('NwwwnwwwwwwwN').sprite(0), _local_thought('NwwwnwnwwwwwN').sprite(0),
    _local_thought('NwwwnwnwnwwwN').sprite(0)]))
_DOTS = [_diff(_dots_item.sprite(i), _TB) for i in range(3)]
_BULB_ON = _diff(_lib('thought_bulb', lambda: _local_thought(extra={
    1: '..NWwjjjwwN..', 2: '.NwwjWyyjwwN.', 3: 'NwwwjyyyjwwwN', 4: 'NwwwwjyjwwwwN', 5: 'NwwwwsNswwwMN'})).sprite(0), _TB)
_ring_ok = _RING_CELLS and all(-2 <= x <= 1 and 5 <= y <= 7 for x, y in _RING_CELLS)
if _rel_bounds(_CLOUD) != (-6, 6, -4, 3) or _TRAIL.get(_DOT_REL) is None or not _ring_ok:
    # The layout (1-cell margins, the hop's arm clearance, the re-forming cloud) is tuned for the 13x8 library cloud
    # and its trail. If the library ever changes them, fall back to local copies so the composition never breaks.
    _CLOUD = Sprite(_LOCAL_CLOUD, anchor=(6, 4))
    _RING_CELLS = {(x - 2, y + 5): c for y, r in enumerate(['.NN.', 'NwwN', '.NN.']) for x, c in enumerate(r) if c != '.'}
    _DOTS = [Sprite(cells=[(dx, -1, 'n') for dx in (-2, 0, 2)[:i + 1]], anchor=(0, 0)) for i in range(3)]
    _BULB_ON = Sprite(['.jjj.', 'jWyyj', 'jyyyj', '.jyj.', '.sNs.'], anchor=(2, 3))
_RING = Sprite(cells=[(x, y, c) for (x, y), c in _RING_CELLS.items()], anchor=(0, 0))   # place at (CX, CY)
_DOT_AT = (CX + _DOT_REL[0], CY + _DOT_REL[1])              # (21, 13): just right of his head-top, touching nothing

_CLOUD_GLOW = _CLOUD.recolor({'w': 'Y', 'M': 'j'})          # the idea lights the whole thought warm
_DOTS_LIT = _DOTS[2].recolor({'n': 'o', 'N': 'o'})          # "..." ignites into the first sparks


def _only(spr, keep):
    """Drop cells that would just repaint the paper of the cloud (they cost bytes and show nothing)."""
    return Sprite(cells=[c for c in spr.cells if c[2] in keep], anchor=(spr.ax, spr.ay))


# Where the bulb's top meets the notch in the cloud's outline it touches the background: that cell keeps a mid-tone.
_NOTCH = (0, -3)                                    # (24, 2), relative to the cloud anchor (CX, CY)


def _notch(spr, ch):
    cells = [c for c in spr.cells if (c[0] - spr.ax, c[1] - spr.ay) != _NOTCH]
    if ch and len(cells) < len(spr.cells):
        cells.append((_NOTCH[0] + spr.ax, _NOTCH[1] + spr.ay, ch))
    return Sprite(cells=cells, anchor=(spr.ax, spr.ay))


_BULBS = {
    'on': _BULB_ON,
    'off': _BULB_ON.recolor({'j': 's', 'y': 'M', 'W': 'M'}),           # dull gray glass, no shine
    'dim': _BULB_ON.recolor({'j': 'J', 'y': 'j', 'W': 'j'}),           # a weak glow
    'hot': _notch(_BULB_ON.recolor({'y': 'Y', 'j': 'y'}), 'j'),        # overload, just before the idea pops
    'faint': _notch(_only(_BULB_ON.recolor({'j': 'M', 's': 'M', 'N': 'M'}), 'M'), None),   # a ghost fading in / out
}

_SPARK = _lib('sparkle_small', lambda: Item('sparkle_small', 'fx', 'local fallback', [
    Sprite(['j'], anchor=(0, 0)), Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1)),
    Sprite(['j.j', '.j.', 'j.j'], anchor=(1, 1))]))
_SPARKS_O = [_SPARK.sprite(k).recolor({'j': 'o'}) for k in range(3)]   # Claude-orange twinkles: dot, plus, x
_GLINT = _lib('sparkle', lambda: Item('sparkle', 'fx', 'local fallback', [
    Sprite(['j'], anchor=(0, 0)), Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1)),
    Sprite(['...j...', '...j...', '..jyj..', 'jjyWyjj', '..jyj..', '...j...', '...j...'], anchor=(3, 3)),
    Sprite(['..j..', '..j..', 'jjyjj', '..j..', '..j..'], anchor=(2, 2))]))

# The sparks of an idea, absolute cells: each one twinkles once as it drifts out of the "...", then all converge.
_SPARKS = {
    'L':     [((21, 3), 1), ((24, 4), 0), ((26, 4), 0)],    # the left spark pops up-left (plus)
    'R':     [((21, 3), 0), ((24, 4), 0), ((27, 3), 1)],    # the right one pops up-right
    'M':     [((21, 3), 0), ((24, 4), 2), ((27, 3), 0)],    # the middle one twinkles in place (x)
    'close': [((22, 3), 0), ((24, 5), 0), ((26, 3), 0)],    # converging on the bulb's spot
    'merge': [((24, 4), 1)],                                # merged: a little flash
}

# a new cloud inflating: puff -> small cloud -> (library cloud)
_PUFF = Sprite(['.NN.', 'NwwN', '.NN.'], anchor=(1, 1))
_CLOUD_S = Sprite(['..NN.NN..',
                   '.NwwNwwN.',
                   'NwwwwwwwN',
                   '.NwwwwwN.',
                   '..NNNNN..'], anchor=(4, 2))

# the cloud bursting: four little thought rings (clear of the glint's long arms), then specks drifting outward
_POP_RING = Sprite(['.N.', 'NwN', '.N.'], anchor=(1, 1))
_POP_RINGS = [(-5, -2), (-4, 2), (4, -2), (5, 2)]
_POP_SPECKS = [(-6, -3, 'N'), (-7, 1, 'M'), (-5, 4, 'N'), (5, -4, 'N'), (6, 0, 'M'), (5, 4, 'M')]


# the study corner: two books (green cloth, leather tome with a gold band and a ribbon), a lavender candle
# on a gold dish (static), its flame flickering on its own loop, flaring up when he lands from the hop
_BOOKS = Sprite(['.gggggG',
                 '.GhhGGG',
                 'TTTTrTO',
                 'TddjrdO'], anchor=(3, 3))          # mid-tone wood / rust contour: reads on the dark theme too
_CANDLE = Sprite(['.lLv.',
                  '.llv.',
                  '.llv.',
                  'jjjjJ'], anchor=(2, 3))
_CANDLE_AT = (4, 15)                        # dish on the books (row 15), wax rows 12-14, flame above
_FLAMES = [Sprite(['.o.', 'oyo', 'oYo', '.o.'], anchor=(1, 3)),           # 0 steady teardrop  (the yellow core is
           Sprite(['oo.', 'oyo', 'oYo', '.o.'], anchor=(1, 3)),           # 1 tip leans left    always capped in
           Sprite(['.oo', 'oyo', 'oYo', '.o.'], anchor=(1, 3)),           # 2 tip leans right   orange, so it reads
           Sprite(['.o.', '.o.', 'oyo', 'oYo', '.o.'], anchor=(1, 4))]    # 3 stretches tall    on white too)
_FLAME_LOOP = [(0, 1500), (1, 200), (0, 1240), (3, 160), (0, 1080), (2, 220)]   # 4.4 s: long steady holds, rare flicks
_FLARE = Sprite(['..o..',
                 '.oyo.',
                 '.oYo.',
                 'oyYyo',
                 '.oYo.',
                 '..o..'], anchor=(2, 5))       # the air of his landing makes the flame flare ...
_SETTLE = [Sprite(['.o.', 'oyo', 'oyo', 'oYo', '.o.'], anchor=(1, 4)),    # ... and settle back, tall and bright,
           Sprite(['.o.', 'ooo', 'oyo', 'oYo', '.o.'], anchor=(1, 4))]    # then cooling (both cover every flame frame)
_FLAME_AT = (4, 11)                         # flame base sits right on the wax


def _placed(spr, x, y):
    return {(x + sx - spr.ax, y + sy - spr.ay): ch for sx, sy, ch in spr.cells}


# The steady teardrop is common to every flame frame: it lives in the static study layer, and the flame layer only
# adds the one tip cell that flicks (lean left / lean right / stretch); its frame 0 is empty.
_FLAME_PX = [_placed(s, *_FLAME_AT) for s in _FLAMES]
_FLAME_ROOT = {p: c for p, c in _FLAME_PX[0].items() if all(fp.get(p) == c for fp in _FLAME_PX)}


# --------------------------------------------------------------------------------------------
# Clawd
# --------------------------------------------------------------------------------------------
_POSES = {
    'R':       dict(rarm='chin'),                             # right claw on chin
    'L':       dict(larm='chin'),                             # left claw on chin (mirrored pondering pose)
    'Ltap':    dict(larm='down'),                             # chin tap: the claw comes off his chin for a beat
    'stand':   dict(),
    'lower':   dict(larm='up'),                               # the eureka claw arcs down toward his chin (raise > up > chin)
    'drop':    dict(rarm='down'),                             # realization: the chin claw falls away
    'gather':  dict(rarm='down', larm='down'),                # anticipation: both claws low, a beat of stillness
    'takeoff': dict(larm='up', rarm='down'),                  # the eureka claw leads, the free arm drags
    'apex':    dict(larm='raise', rarm='down', legs='short'),
    'descent': dict(larm='raise'),                            # the free arm catches up
    'land':    dict(larm='up'),                               # the claw dips with the impact ...
    'cheer':   dict(larm='raise'),                            # ... and pumps back up: "got it!"
}


def _solid(kind, y):
    """Clawd in a kit pose with a solid face (no eye holes yet), his normal body size (STYLE.md section 0)."""
    p = clawd(eyes='blink', **_POSES[kind])
    f = Frame()
    put_clawd(f, p, HOME[0], y)
    return p, f


def _eye_area(p, y, key):
    """The 3x3 cells around one eye ('eye_l' / 'eye_r'), as fine pixels: everything a fine-line expression can touch."""
    ex, ey = p.at(key, HOME[0], y)
    return [(2 * ex + dx, 2 * ey + dy) for dy in range(-2, 4) for dx in range(-2, 4)]


# Half-step gaze (one fine pixel, like the kit's fine look_*): 'shape/gaze' is the kit's fine_face(shape) with each eye
# moved by the gaze, so a lid or a blink line closes over the pupil where he is looking ('open/u' == the kit's look_u,
# 'half/u' == the bottom half of his raised eye). No suffix = centered on the eye cell (the kit's own drawing).
_GAZE = {'': (0, 0), 'u': (0, -1), 'ur': (1, -1), 'ul': (-1, -1), 'r': (1, 0), 'l': (-1, 0)}


def _parse(expr):
    shape, _, gaze = expr.partition('/')
    if shape not in FINE_EYES or gaze not in _GAZE:
        raise ValueError('unknown expression %r (FINE_EYES name, optionally /%s)' % (expr, '|/'.join(sorted(_GAZE)[1:])))
    return shape, _GAZE[gaze]


def _target(kind, y, expr):
    """Clawd's eye area drawn the expressive way, fine(frame) + fine_face(...) with each eye moved by its gaze:
    {fine pixel: color, None = see-through}. expr: 'shape' or 'shape/gaze', or a (left, right) pair of those."""
    p, f = _solid(kind, y)
    base = fine(f)
    left, right = expr if isinstance(expr, tuple) else (expr, expr)
    (ls, lg), (rs, rg) = _parse(left), _parse(right)
    ff = fine_face(base.copy(), p, HOME[0], y, ls, rs)
    out = {}
    for key, (gx, gy) in (('eye_l', lg), ('eye_r', rg)):
        win = _eye_area(p, y, key)
        # What fine_face drew on his face (eye, lid, arc, glint; None = see-through). Everything else stays as the solid
        # body drew it: fine_face repaints its whole eye box orange, which would wipe the claw on his chin.
        ink = {q: ff.px.get(q) for q in win if ff.px.get(q) not in (base.px.get(q), '#')}
        for q in win:
            out[q] = base.px.get(q)
        for (qx, qy), v in ink.items():
            q = (qx + gx, qy + gy)
            if q not in win or base.px.get(q) != '#':       # stays in its own eye area, on bare face (not the claw)
                raise ValueError('%r: the %s would leave his face at fine %r' % (expr, key, q))
            out[q] = v
    return out


def _holes(kind, y, exprs):
    """Body cells that must be see-through so that every expression in `exprs` can show its eye holes."""
    _, f = _solid(kind, y)
    return frozenset((qx // 2, qy // 2) for e in exprs for (qx, qy), v in _target(kind, y, e).items()
                     if v is None and (qx // 2, qy // 2) in f.px)


def body(kind, y, holes):
    """Body layer: the solid pose with the eye cells of this pose run cut out (the face layer fills the rest)."""
    _, f = _solid(kind, y)
    for c in holes:
        f.px.pop(c, None)
    return f


def face(kind, y, holes, expr):
    """Face layer (FINE): only the half-size eye-area pixels that differ from body(kind, y, holes)."""
    under = fine(body(kind, y, holes))
    out = Frame(res=2)
    for q, v in _target(kind, y, expr).items():
        b = under.px.get(q)
        if v is None:
            if b is not None:
                raise ValueError('%s needs a see-through cell at %r (pose %s)' % (expr, (q[0] // 2, q[1] // 2), kind))
        elif v != b:
            out.px[q] = v
    out.meta = {'fine_face': [expr]}
    return out


# --------------------------------------------------------------------------------------------
# cloud layer (shape + trail)
# --------------------------------------------------------------------------------------------
def cloud(state):
    f = Frame()
    st = state
    if st in ('full', 'glow'):
        f.place(_CLOUD_GLOW if st == 'glow' else _CLOUD, CX, CY)
        f.place(_RING, CX, CY)
        if st == 'full':                       # the last dot lets go while the idea glows (his arm passes there in the hop)
            f.put(_DOT_AT[0], _DOT_AT[1], 'N')
    elif st == 'pop1':
        for dx, dy in _POP_RINGS:
            f.place(_POP_RING, CX + dx, CY + dy)
    elif st == 'pop2':
        for dx, dy, ch in _POP_SPECKS:
            f.put(CX + dx, CY + dy, ch)
    elif st.startswith('form'):                # a new thought bubbles up from his head
        n = int(st[4:])
        f.put(_DOT_AT[0], _DOT_AT[1], 'N')
        if n >= 2:
            f.place(_RING, CX, CY)
        if n == 3:
            f.place(_PUFF, CX - 3, CY + 2)
        if n == 4:
            f.place(_CLOUD_S, CX - 1, CY + 1)
    elif st != 'none':
        raise ValueError(state)
    return f


# --------------------------------------------------------------------------------------------
# thought layer (what is inside / around the cloud)
# --------------------------------------------------------------------------------------------
def thought(state):
    f = Frame()
    if state is None:
        return f
    kind, _, arg = state.partition(':')
    if kind == 'dots':
        f.place(_DOTS[int(arg)], CX, CY)
    elif kind == 'ignite':
        f.place(_DOTS_LIT, CX, CY)
    elif kind == 'spark':
        for (x, y), k in _SPARKS[arg]:
            f.place(_SPARKS_O[k], x, y)
    elif kind == 'bulb':
        f.place(_BULBS[arg], CX, CY)
    elif kind == 'glint':          # a glint where the bulb was (thin cross -> plus)
        f.place(_GLINT.sprite(int(arg)), CX, CY - 1)
    else:
        raise ValueError(state)
    return f


# --------------------------------------------------------------------------------------------
# the story: (ms, pose or (pose, y), cloud, thought, fx, tag)
# --------------------------------------------------------------------------------------------
def story():
    s = []

    def add(ms, b, c, t, m=None, tag=None):
        s.append((ms, b, c, t, m, tag))

    R, L = 'R', 'L'
    # ---- A: right claw on chin -------------------------------------------------------------
    add(650, R, 'full', 'dots:2')                           # frame 0
    add(420, R, 'full', 'dots:0')
    add(420, R, 'full', 'dots:1')
    add(360, R, 'full', 'dots:2')
    add(130, R, 'full', 'dots:2')
    add(300, R, 'full', 'dots:2')
    # the dots ignite and twinkle into sparks one by one, then converge where the bulb will be
    add(160, R, 'full', 'ignite', tag='ignite')             # a beat later his eyes snap open on them
    add(240, R, 'full', 'spark:L')
    add(260, R, 'full', 'spark:R', tag='spark_r')           # his eyes follow the right spark ...
    add(240, R, 'full', 'spark:M', tag='spark_m')           # ... and come back up for the middle one
    add(160, R, 'full', 'spark:close')
    add(140, R, 'full', 'spark:merge')
    # a dull bulb sputters on (each pulse >= 340 ms after the last: under 3 Hz)
    add(300, R, 'full', 'bulb:off')
    add(120, R, 'full', 'bulb:on')
    add(220, R, 'full', 'bulb:off')
    add(110, R, 'full', 'bulb:dim')
    add(240, R, 'full', 'bulb:off', tag='doubt')            # dark again: his lids droop ...
    add(300, R, 'full', 'bulb:on', tag='bulb')               # ... it holds: wide eyes
    # realization: the idea lights the whole cloud, it sparkles in his eyes, and his chin claw falls away
    add(260, 'drop', 'glow', 'bulb:on', tag='idea')
    # eureka hop: anticipation with both claws low, then his whole (normal) body goes up 1, 2 (legs tucked), 1
    add(200, 'gather', 'glow', 'bulb:on')
    add(80, ('takeoff', 11), 'glow', 'bulb:on', tag='hop')
    add(170, ('apex', 10), 'glow', 'bulb:on')
    add(90, ('descent', 11), 'glow', 'bulb:on')
    add(100, 'land', 'glow', 'bulb:on', 'dust0', tag='land')           # lands: a puff of dust, the claw dips
    add(100, 'cheer', 'glow', 'bulb:on', 'dust1,flare', tag='cheer')  # "got it!": the whoosh flares the candle,
    add(130, 'cheer', 'glow', 'bulb:on', 'dust2,settle0')             # one beat late, and it settles back
    add(140, 'cheer', 'glow', 'bulb:on', 'settle1')
    add(120, 'cheer', 'glow', 'bulb:hot')                              # the idea overloads ...
    add(100, 'cheer', 'pop1', 'glint:3')                               # ... and pops
    add(120, 'cheer', 'pop2', 'glint:1', tag='pop2')
    add(110, 'lower', 'form1', None, tag='stand1')                     # a new thought-dot is already rising
    # ---- B: left claw on chin; the new thought bubbles up (easing out into the full cloud) -----
    add(110, L, 'form1', None, tag='B')                    # his eyes rise with it: the dot ...
    add(120, L, 'form2', None, tag='ring')                 # ... the ring ...
    add(150, L, 'form3', None)                             # ... and the cloud inflating up-right
    add(190, L, 'form4', None)
    add(240, L, 'full', None)
    add(450, L, 'full', 'dots:0', tag='candle')            # a long look aside at the candle
    add(400, L, 'full', 'dots:1')
    add(140, L, 'full', 'dots:2', tag='blinks')            # quick double blink (each one carries a gaze change)
    add(110, L, 'full', 'dots:2')
    add(130, L, 'full', 'dots:2')
    add(110, L, 'full', 'dots:2')
    add(480, L, 'full', 'dots:2', tag='you')               # a short look at you: "one sec..."
    add(380, L, 'full', 'dots:0', tag='back2')
    # a second idea: a gray bulb that glows dimly once and never catches (a dud). "hmm... no."
    add(110, L, 'full', 'bulb:faint')
    add(320, L, 'full', 'bulb:off', tag='dud')
    add(120, L, 'full', 'bulb:dim')
    add(340, L, 'full', 'bulb:off', tag='dud_off')
    add(130, 'Ltap', 'full', 'bulb:off')                    # "hmm... no": two chin taps
    add(150, L, 'full', 'bulb:off')
    add(130, 'Ltap', 'full', 'bulb:off')
    add(230, L, 'full', 'bulb:off')
    # back to the right claw; the dud melts into dots
    add(130, 'stand', 'full', 'bulb:faint', tag='stand2')
    add(360, R, 'full', 'dots:0', tag='A2')
    add(420, R, 'full', 'dots:1')
    return s


def _tags(rows):
    t, out = 0, {}
    for row in rows:
        if row[5]:
            out[row[5]] = t
        t += row[0]
    return out


REACT = 80          # ms: his eyes answer a stimulus a beat after it (cause, then effect), never on the same frame


def face_track(T):
    """Fine-line acting on the story clock: (start ms, expression); each holds until the next one.
    Expressions are FINE_EYES names with an optional half-step gaze ('half/u', 'open/ur': see _GAZE). Lids are drawn at
    the current gaze, so they close over the pupil instead of bobbing the eye; gaze changes ride on blinks. Smooth
    blinks go half > line > half (60 / 70-80 / 60 ms); emotional beats hold 400-1200 ms (STYLE.md 0b)."""
    U = 'look_u'                                            # resting gaze (== 'open/u'): a half-step up, at the cloud
    b = T['blinks']
    return [
        (0, U),                                             # frame 0: pondering, eyes up at the thought cloud
        (1550, 'half/u'), (1620, 'squint/u'),               # the lids come down over his raised eyes: concentrating ...
        (T['ignite'] + REACT, U),                           # ... the dots ignite: a beat later his eyes snap open on them
        (T['spark_r'] + REACT, 'open/ur'),                  # following the right spark up-right ...
        (T['spark_m'] + REACT, U),                          # ... and back up for the middle one
        (T['doubt'], 'half/u'),                             # the bulb sputters out again: a droop of doubt ...
        (T['bulb'] + 60, 'wide'),                           # ... it catches and holds: "!" (one fine row to three)
        (T['idea'], 'sparkle'),                             # the idea shines in his eyes
        (T['hop'], 'happy'),                                # eureka hop: pleased arcs
        (T['land'], 'line'), (T['cheer'], 'happy'),         # the landing squeezes his eyes (no body squash), "got it!"
        (T['pop2'], 'line'), (T['stand1'], 'half'),         # the idea pops; eyes close, then open ...
        (T['B'], 'look_r'), (T['ring'], 'open/ur'),         # ... and rise with the new thought: the dot, then up-right
                                                            # on the ring and the cloud inflating there (it sits up-right)
        (T['candle'], 'open/ul'),                           # a long look aside at the candle (0.85 s, a clear saccade) ...
        (b, 'half/ul'), (b + 60, 'line/u'), (b + 140, 'half/u'), (b + 200, U),   # ... a blink carries his gaze back up,
        (b + 300, 'half/u'), (b + 360, 'line'), (b + 430, 'half'),            # a second one brings it down ...
        (T['you'], 'open'),                                 # ... to you: "one sec..." (the official open eyes)
        (T['back2'], U),
        (T['dud'], 'open/ur'),                              # a glance up at the gray bulb ...
        (T['dud_off'] + REACT, 'half/ur'),                  # ... it dies: his lids droop over the stare, "hmm... no"
        (T['stand2'], 'line/u'), (T['A2'], 'half/u'), (T['A2'] + 60, U),   # lids close, claws switch, back up
    ]


# --------------------------------------------------------------------------------------------
# fx (story-synced): landing dust and the candle flare
# --------------------------------------------------------------------------------------------
_DUST = _lib('dust_puff', lambda: Item('dust_puff', 'fx', 'local fallback', [
    Sprite(['.t...........t.', 'tTT.........tTT'], anchor=(7, 0)),
    Sprite(['.tt...............tt.', 'twtt.............twtt', 'tTTT.............tTTT'], anchor=(10, 1)),
    Sprite(['tt.....................tt', 'tT.....................tT', '...t.................t...'], anchor=(12, 2))]))
_DUST_AT = (15, GROUND - 1)                  # feet center, one row above the ground (library convention)
# On the left the dust has only the 3 columns between the books and his leg: it rolls up against the books there.
_DUST_LEFT = {1: (Sprite(['.t.', 'twt', 'tTT'], anchor=(0, 0)), (8, 17)),
              2: (Sprite(['t'], anchor=(0, 0)), (9, 16))}      # the last speck rises in the gap


def fx(state, study):
    f = Frame()
    for tok in (state or '').split(','):
        if tok.startswith('dust'):
            k = int(tok[4:])
            d = Frame()
            d.place(_DUST.sprite(k), *_DUST_AT)
            for (x, y), ch in d.px.items():
                left = x < _DUST_AT[0]
                if (x, y) not in study.px and not (left and k in _DUST_LEFT):
                    f.put(x, y, ch)
            if k in _DUST_LEFT:
                spr, at = _DUST_LEFT[k]
                f.place(spr, *at)
        elif tok == 'flare':
            f.place(_FLARE, *_FLAME_AT)
        elif tok.startswith('settle'):
            f.place(_SETTLE[int(tok[6:])], *_FLAME_AT)
    return f


def _study():
    f = Frame()
    f.place(_BOOKS, 4, GROUND)
    f.place(_CANDLE, *_CANDLE_AT)
    for (x, y), ch in _FLAME_ROOT.items():
        f.put(x, y, ch)
    return f


def _clawd_layers(rows):
    """Body (normal pixels) and face (fine pixels) layers from the story rows and the face track.
    A pose run (consecutive rows in the same pose and height) gets ONE body frame whose see-through eye cells are
    the union that its expressions need, so body frames still merge while only his face acts."""
    loop = sum(r[0] for r in rows)
    track = face_track(_tags(rows))
    times = [t for t, _ in track]
    if times != sorted(times) or times[0] != 0 or len(set(times)) != len(times) or times[-1] >= loop:
        raise ValueError('face track out of order: %r' % times)

    def expr_at(t):
        cur = None
        for tt, e in track:
            if tt <= t:
                cur = e
        return cur

    runs, t = [], 0                                         # [t0, t1, pose, y]
    for ms, bd, _, _, _, _ in rows:
        kind, y = (bd, HOME[1]) if isinstance(bd, str) else bd
        if runs and runs[-1][2:] == [kind, y]:
            runs[-1][1] = t + ms
        else:
            runs.append([t, t + ms, kind, y])
        t += ms
    b, fc = [], []
    for t0, t1, kind, y in runs:
        cuts = sorted({t0} | {tt for tt in times if t0 < tt < t1})
        segs = [(c0, c1, expr_at(c0)) for c0, c1 in zip(cuts, cuts[1:] + [t1])]
        holes = _holes(kind, y, {e for _, _, e in segs})
        b.append((body(kind, y, holes), t1 - t0))
        for c0, c1, e in segs:
            if c1 - c0 < 40:
                raise ValueError('face sliver %d-%d (%s): line the track up with the pose runs' % (c0, c1, e))
            fc.append((face(kind, y, holes, e), c1 - c0))
    return b, fc


def build():
    study = _study()
    rows = story()
    b, fc = _clawd_layers(rows)
    c, t, e = [], [], []
    for ms, _, cl, th, ef, _ in rows:
        c.append((cloud(cl), ms))
        t.append((thought(th), ms))
        e.append((fx(ef, study), ms))
    flame = []
    for k, ms in _FLAME_LOOP:
        f = Frame()
        for (x, y), ch in _FLAME_PX[k].items():
            if (x, y) not in _FLAME_ROOT:
                f.put(x, y, ch)
        flame.append((f, ms))
    return anim(NAME, DESC, [
        static('study', study),
        layer('flame', flame),
        layer('fx', e),
        layer('body', b),
        layer('face', fc),                  # fine-line expressions (half-size pixels), synced to the body
        layer('cloud', c),
        layer('thought', t),
    ], state=STATE)
