# ======================================================================================
# USER FEEDBACK: the user reviewed this first draft personally and approved it ("i think its good").
# Keep the concept, the beats and the fine-line expressions. Critics, fixers and judges should
# polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""idle-moods - Idle variant (expressive style pilot): little moods and micro-expressions.

STORYBOARD (s)   one loop = 19.9 s; his FACE tells the story with fine-line eyes (STYLE.md 0b); a blue
                 butterfly, the pink flower on his head and a lavender flower in the grass give him things
                 to react to.  Calm holds between the moments (2.2, 1.0, 1.15, 1.4, 1.0 s + 2.8 s across
                 the seam), so the loop breathes like the approved idle.
   0.00  HOLD at HOME, official open eyes.  A blue butterfly basks, wings open, on the pink flower tucked
         at the corner of his head; the stem bends out under its weight.  A lavender flower grows in a
         grass tuft at his left (frame 0 = the reduced-motion still)
   2.20  smooth blink (open > half > line > half > open)
   3.35  the butterfly folds its wings up .. 3.50 he rolls his eyes up to it (look_u)
   4.50  TAKE-OFF: it lets go; a beat later his flower springs up past rest and wobbles out (follow-
         through).  It arcs over his head (spacing eases in and out); his eyes trail it on an arc, up-left
         (4.87) then left (5.16), and it glides down to hover over the lavender ..
   5.66  .. touches down; the lavender gives under it a beat later (5.77).  He blinks, quickly (5.96);
         it fans its wings open as his eyes reopen (6.18)
   6.60  lift-off: the lavender recoils, then springs past rest; the butterfly climbs out at the top
         left, speeding up (gone 7.25).  His eyes follow it up-left (6.98) and stay on the empty spot
   8.40  eyes back to you .. 8.90 WINK (his screen-left eye: half > line > half) with a glint at the
         corner of that eye; his flower cocks out like a hat a beat after the eye closes and comes back a
         beat after it opens (overlap)
  10.50  he settles: eyes go half > content cups (u u), the arms relax a beat later (10.80) .. a long
         cozy hold ..
  12.20  .. the butterfly slides back in at the top right edge, slows, hovers ..
  13.15  .. and touches down on his flower (it eases in: left, then down), which gives straight down
         under it (13.26): 13.37 SURPRISE (wide eyes), both hands flinch up a beat later (13.44, held
         0.17 s)
  14.01  double take: a glance to the right, where the flutter came from (look_r) .. 14.45 then up
         (look_u): there it is ..
  15.12  DELIGHT: happy arcs (^ ^); a beat later the hands go up and the butterfly opens its wings hello
         (15.21); the flower bobs up and out with his joy (15.32) and settles bent out under the weight
         (15.54), the butterfly riding it with one fan of its wings (open > up > open); a glint twinkles
         left of his head, then one right of the flower (15.45 - 15.89)
  16.24  eyes open (half > open), hands down a beat after (16.31) .. 17.30 a glance down at the input
         box (waiting for your prompt) ..
  18.25  the butterfly takes one slow basking wing-breath .. 19.00 a slow blink .. HOLD -> loop
         (0.57 s + the 2.2 s opening hold across the seam)
Eye closures: 2.20, 5.96 (quick), 8.90 (wink), 10.50-13.37 (content), 15.05-16.24 (happy), 19.00 (slow).

Face: fine-line kit only (fine() + fine_face(); FINE_EYES open/half/line/content/happy/wide), each eye
moved by a half-step gaze (c l r u d ul: one fine pixel; 'open' + l/r/u/d equals the kit's fine look_*), so
a blink closes where he is looking.  The eye colour is the kit's (black ink, STYLE.md 0).  No mouth, no
blush, never resized; Clawd never leaves HOME, feet on row 19.
Layers (back to front): scene (STATIC: everything that never moves: the grass, the lavender's stem base,
Clawd's trunk = the kit body with no arms and no eye pixels, his flower's stem base) | lavender (its
bloom: rest / dip / spring) | arms (only the kit's arm cells) | face (FINE: his eyes, the half-size ink
pixels; at 'open' exactly the official eyes) | flower (his bloom: bend / spring / sway) | butterfly | fx
(both glint tracks).  The story is written as tracks of timed events on ONE clock; every layer is cut
from the same beat list (identical lengths), so his arms, eyes, the flowers and the butterfly never drift
apart, and _beats() refuses any two event times closer than MIN_GAP (no slivers).  The split costs no
pixels: the composite equals Clawd drawn whole with put_clawd + fine_face, every beat.
Library: flower (his pink flower: rest + sway frames; bent and stretched stems are derived from them;
the lavender one is the same sprite recolored), sparkle_small (glints).  Local: the butterfly, grass.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'idle-moods'
STATE = 'Idle variant (expressive style): little moods and micro-expressions'
DESC = ('Waits at home while a butterfly basks on the flower on his head: fine-line blinks, glances that '
        'follow it to a flower in the grass, a wink at you, a cozy content settle, wide-eyed surprise and a '
        'double take when it lands back, then delighted happy eyes.')

HX, HY = HOME
LOOP = 19900
MIN_GAP = 60       # two different event times are at least this far apart (no sub-60 ms slivers)

# ---------------------------------------------------------------- Clawd: body | fine face overlay
_EYE_CELLS = [(HX + 2, HY + 2), (HX + 8, HY + 2)]
_WIN = [(ex + dx, ey + dy) for ex, ey in _EYE_CELLS for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
_WIN_FINE = {(2 * x + i, 2 * y + j) for x, y in _WIN for i in (0, 1) for j in (0, 1)}

_ARMS = {
    'side': ('side', 'side'),
    'down': ('down', 'down'),      # relaxed
    'up': ('up', 'up'),            # a little flinch / delight
}


def _pose(arms='side'):
    la, ra = _ARMS[arms]
    return clawd(larm=la, rarm=ra)


# Clawd is split by what changes, so each part costs only its own changes (every part is cut from the
# same beat list, so they never drift): his trunk (the kit's body with no arms and no eye pixels) is
# static; the arms layer holds only the kit's arm cells; the fine face layer draws his eyes.
_TRUNK = clawd(eyes='blink', larm='none', rarm='none')
_TRUNK_CELLS = {(HX + x, HY + y) for x, y, ch in _TRUNK.sprite.cells}
_HOLES = not EYES_BLACK        # if the kit ever goes back to see-through eyes: cut the eye windows out
                               # of the trunk and let the face layer draw the whole windows


def _trunk(cut=_HOLES):
    f = Frame()
    put_clawd(f, _TRUNK)
    if cut:
        for x, y in _WIN:
            f.put(x, y, ERASE)
    return f


def _arms(arms):
    """Only his arm cells: the kit pose drawn with put_clawd, minus the static trunk."""
    f = Frame()
    put_clawd(f, _pose(arms))
    f.px = {k: v for k, v in f.px.items() if k not in _TRUNK_CELLS}
    return f


# Face track values: an expression + a half-step gaze (one fine pixel).
_GAZE = {'c': (0, 0), 'l': (-1, 0), 'r': (1, 0), 'u': (0, -1), 'd': (0, 1), 'ul': (-1, -1)}
_LOOK = {
    'open': ('open', 'c'), 'look_l': ('open', 'l'), 'look_r': ('open', 'r'), 'look_u': ('open', 'u'),
    'look_d': ('open', 'd'), 'look_ul': ('open', 'ul'),
    'wide': ('wide', 'c'), 'half': ('half', 'c'), 'content': ('content', 'c'), 'happy': ('happy', 'c'),
}
_CLOSED = ('content', 'happy')     # closed-eye arcs sit centered on the eye cell, whatever the gaze


def _eyes(ff, pose, left, right, gaze):
    """Both eyes on a fine frame: the kit's fine_face(left, right), each eye moved by the gaze, so a
    half lid or a blink line closes over the pupil where he is looking."""
    src = fine_face(ff.copy(), pose, expr=left, right=right)
    for key, expr in (('eye_l', left), ('eye_r', right)):
        gx, gy = (0, 0) if expr in _CLOSED else _GAZE[gaze]
        fx, fy = [2 * v for v in pose.at(key)]
        win = [(fx + dx, fy + dy) for dy in range(-2, 4) for dx in range(-2, 4)]   # his 3x3-cell eye area
        moved = {(x + gx, y + gy): src.px.get((x, y)) for x, y in win if src.px.get((x, y)) != '#'}
        for x, y in win:
            ff.put(x, y, '#')
        for (x, y), ch in moved.items():
            ff.put(x, y, ERASE if ch is None else ch)
    return ff


_TRUNK_FINE = fine(_trunk(cut=False))


def _face(look, lid):
    """FINE layer: his eyes, the half-size ink pixels of the kit's fine_face() on top of the trunk
    (at 'open' they are exactly the official eyes).  lid = None, or a blink/wink lid (shape, which):
    ('half' | 'line', 'both' | 'left'), drawn at the current gaze."""
    expr, gaze = _LOOK[look]
    left = right = expr
    if lid is not None:
        shape, which = lid
        left = shape
        right = shape if which == 'both' else expr
    ff = _eyes(_TRUNK_FINE.copy(), _TRUNK, left, right, gaze)
    out = Frame(res=2)
    out.px = {k: v for k, v in ff.px.items() if k in _WIN_FINE and (_HOLES or _TRUNK_FINE.px.get(k) != v)}
    out.meta = {'fine_face': [(left, right, gaze)]}
    return out


# ---------------------------------------------------------------- flowers (library 'flower')
_FL = get('flower')
FL_DX = 3                      # his flower is tucked at the top-right corner of his head
DAISY = (5, GROUND)            # the lavender flower stands in the grass at his left (stem bottom)


def _stem_row(spr):
    """Highest row that is a single stem cell (just under the bloom), or None."""
    rows = {}
    for x, y, ch in spr.cells:
        rows.setdefault(y, []).append((x, ch))
    for y in sorted(rows):
        if y < spr.ay and len(rows[y]) == 1 and rows[y][0][1] in 'gG':
            return y
    return None


def _dipped(spr):
    """The bloom one row lower: the top stem cell folds away (it bends under a weight)."""
    sy = _stem_row(spr)
    if sy is None:
        return spr
    cells = [(x, y + 1 if y < sy else y, ch) for x, y, ch in spr.cells if y != sy]
    return Sprite(cells=cells, anchor=(spr.ax, spr.ay), name=spr.name + '_dip')


def _stretched(spr):
    """The bloom one row higher: the stem springs up a cell (overshoot)."""
    sy = _stem_row(spr)
    if sy is None:
        return spr
    sx, sch = [(x, ch) for x, y, ch in spr.cells if y == sy][0]
    cells = [(x, y - 1 if y <= sy else y, ch) for x, y, ch in spr.cells] + [(sx, sy, sch)]
    return Sprite(cells=cells, anchor=(spr.ax, spr.ay), name=spr.name + '_up')


def _states(f0, f1, f3):
    return {'rest': f0, 'sway_r': f1, 'sway_l': f3, 'up': _stretched(f0), 'dip': _dipped(f0),
            'dip_r': _dipped(f1)}


def _split(states):
    """The cells every state shares (the stem base: the bend happens above it) can live in a static
    layer: returns ({state: the rest of it}, the shared base).  Computed, so it adapts if the library
    flower is redrawn (worst case the base is empty and the states carry everything)."""
    common = None
    for s in states.values():
        common = set(s.cells) if common is None else common & set(s.cells)
    tops = {k: Sprite(cells=[c for c in s.cells if c not in common], anchor=(s.ax, s.ay), name=s.name)
            for k, s in states.items()}
    s = states['rest']
    return tops, Sprite(cells=sorted(common), anchor=(s.ax, s.ay), name=s.name + '_stem')


_FLOWER = _states(_FL.sprite(0), _FL.sprite(1), _FL.sprite(3))
_FL_TOP, _FL_STEM = _split(_FLOWER)
_FL_ITEMS = {k: Item('flower', 'head', 'flower state ' + k, [s]) for k, s in _FL_TOP.items()}
_FL_STEM_ITEM = Item('flower', 'head', 'flower stem base', [_FL_STEM])
_LAV = {'p': 'l', 'r': 'v'}    # the same flower in lavender / violet
_DAISY = _states(*[_FL.sprite(i).recolor(_LAV) for i in (0, 1, 3)])
_DS_TOP, _DS_STEM = _split(_DAISY)


def _bloom_top(spr, x, y):
    """Absolute (center x, top row) of a flower sprite's bloom when its anchor is at (x, y)."""
    top = min(sy for sx, sy, ch in spr.cells)
    xs = [sx for sx, sy, ch in spr.cells if sy in (top, top + 1)]
    return x + (min(xs) + max(xs)) // 2 - spr.ax, y + top - spr.ay


def _head_anchor():
    hx, hy = _pose().at('head')
    return hx + FL_DX, hy


def _flower(state):
    f = Frame()
    wear(f, _FL_ITEMS[state], _pose(), dx=FL_DX)
    return f


def _flower_stem():
    f = Frame()
    wear(f, _FL_STEM_ITEM, _pose(), dx=FL_DX)
    return f


def _daisy(state):
    f = Frame()
    f.place(_DS_TOP[state], *DAISY)
    return f


# ---------------------------------------------------------------- static scene: grass tufts
# Every tip that touches the background is green (lime vanishes on the light theme); the lavender's
# stem stands in the gap of the left tuft.
_GRASS_L = Sprite(['g...g..', '.g...g.', '.Gg.gG.'], anchor=(3, 2), name='grass_l')   # around the lavender
_GRASS_R = Sprite(['..g.', 'g.g.', 'gGgG'], anchor=(1, 2), name='grass_r')


def _scene():
    """Everything that never moves, in one static layer: the grass, the lavender's stem base, Clawd's
    trunk and his flower's stem base.  (Nothing animated ever overlaps these parts except his flower's
    stem over his head's top row, drawn after the trunk here, and the dipped lavender over a grass
    tip, drawn by the lavender layer above.)"""
    f = Frame()
    f.place(_GRASS_L, DAISY[0], GROUND)
    f.place(_GRASS_R, 26, GROUND)
    f.place(_DS_STEM, *DAISY)              # the lavender's stem base (its bloom and bend animate)
    f = f.over(_trunk())
    f.meta = {'clawd': [(HX, HY, _TRUNK.spec)]}
    return f.over(_flower_stem())


# ---------------------------------------------------------------- the butterfly (local; anchor = body center)
_BF = {
    'open': Sprite(['cb.bc', 'bbBbb', '.b.b.'], anchor=(2, 1), name='bfly_open'),   # wings spread
    'up': Sprite(['c.c', 'bBb', '.B.'], anchor=(1, 1), name='bfly_up'),             # wings raised (V)
}
PO, PU = ('perch', 'open'), ('perch', 'up')        # on his flower
DO, DU = ('daisy', 'open'), ('daisy', 'up')        # on the lavender flower


def _place(f, spr, x, y):
    """Place without counting cells outside the canvas as clipping (it flies in and out at the edges)."""
    for sx, sy, ch in spr.cells:
        px, py = x + sx - spr.ax, y + sy - spr.ay
        if 0 <= px < W and 0 <= py < H:
            f.put(px, py, ch)


def _bfly(state, flower_state, daisy_state):
    f = Frame()
    if state is None:
        return f
    if state[0] == 'perch':
        cx, top = _bloom_top(_FLOWER[flower_state], *_head_anchor())
        x, y, wing = cx, top - 2, state[1]
    elif state[0] == 'daisy':
        cx, top = _bloom_top(_DAISY[daisy_state], *DAISY)
        x, y, wing = cx, top - 2, state[1]
    else:
        x, y, wing = state
    _place(f, _BF[wing], x, y)
    return f


# ---------------------------------------------------------------- fx (glints)
_GLINT = get('sparkle_small')
WINK_AT = (9, 11)                      # glint at the outer corner of his winking (screen-left) eye
JOY_L, JOY_R = (8, 10), (24, 9)        # delight glints: left of his head, right of his flower


def _fx(items):
    f = Frame()
    for i, x, y in items:
        f.place(_GLINT.sprite(i), x, y)
    return f


# ---------------------------------------------------------------- the story: tracks of timed events
def _seq(track, t, steps):
    """Append sequential (ms, value) steps starting at time t; returns the end time."""
    for ms, v in steps:
        track.append((t, v))
        t += ms
    return t


def _blink(lids, t, which='both', half=70, line=110):
    """Smooth fine blink as a lid: half > line > half > open (it closes where he is looking)."""
    return _seq(lids, t, [(half, ('half', which)), (line, ('line', which)), (half, ('half', which)), (0, None)])


def _twinkle(fx, t, at, last=110):
    """One glint (library sparkle_small): dot > plus > x > plus, then gone."""
    g = lambda i: ((i,) + at,)
    return _seq(fx, t, [(90, g(0)), (110, g(1)), (130, g(2)), (last, g(1)), (0, ())])


def _story():
    tr = {k: [] for k in ('face', 'lids', 'arms', 'flower', 'daisy', 'bf', 'fx', 'fx2')}
    face, lids, arms, flower, daisy, bf, fx, fx2 = (tr[k] for k in ('face', 'lids', 'arms', 'flower', 'daisy',
                                                                    'bf', 'fx', 'fx2'))
    face.append((0, 'open'))
    lids.append((0, None))
    arms.append((0, 'side'))
    flower.append((0, 'dip_r'))
    daisy.append((0, 'rest'))
    bf.append((0, PO))
    fx.append((0, ()))
    fx2.append((0, ()))

    # -- A: resting together; frame 0 is the still
    _blink(lids, 2200)
    bf.append((3350, PU))                                      # it folds its wings up ..
    face.append((3500, 'look_u'))                              # .. he rolls his eyes up to it

    # -- B: take-off; up and over his head (spacing eases in and out), a glide and a hover over the
    #    lavender, then it touches down
    t = _seq(bf, 4500, [
        (120, (20, 4, 'open')), (120, (18, 3, 'up')), (130, (15, 2, 'open')), (140, (12, 3, 'up')),
        (150, (9, 5, 'open')), (160, (7, 8, 'up')), (170, (6, 10, 'open')), (170, (5, 11, 'open'))])
    # his flower lets go: the stem recoils a frame after the release, overshoots, wobbles out
    _seq(flower, 4500, [(120, 'rest'), (120, 'up'), (130, 'rest'), (140, 'sway_l'), (0, 'rest')])
    face.append((4870, 'look_ul'))                             # his eyes trail it on an arc ..
    face.append((5160, 'look_l'))                              # .. and catch up to the left
    bf.append((t, DU))                                         # 5660 touches the lavender ..
    daisy.append((t + 110, 'dip'))                             # .. which gives under it a beat later
    _blink(lids, t + 300, half=60, line=100)                   # a quick blink while it sips ..
    bf.append((t + 520, DO))                                   # .. it fans its wings as his eyes reopen
    # lift-off: the lavender recoils, then springs past rest; out at the top left, speeding up
    _seq(bf, 6600, [(140, (5, 11, 'open')), (130, (5, 9, 'up')), (110, (6, 7, 'open')),
                    (100, (5, 4, 'up')), (90, (3, 2, 'open')), (80, (1, 0, 'up')), (0, None)])
    _seq(daisy, 6600, [(140, 'rest'), (130, 'up'), (0, 'rest')])
    face.append((6980, 'look_ul'))                             # his eyes follow it up and out ..

    # -- C: .. he watches the empty spot .. eyes back to you .. a wink
    face.append((8400, 'open'))
    _blink(lids, 8900, which='left', line=520)                 # 8900 half, 8970 line, 9490 half, 9560
    _twinkle(fx, 8970, WINK_AT)
    _seq(flower, 9060, [(740, 'sway_r'), (0, 'rest')])         # cocks like a hat a beat after the eye ..

    # -- D: the cozy settle; the butterfly comes back while his eyes are closed
    _seq(face, 10500, [(90, 'half'), (0, 'content')])
    arms.append((10800, 'down'))                               # the arms relax a beat after the eyes
    land = _seq(bf, 12200, [(100, (32, 2, 'open')), (120, (29, 2, 'up')), (140, (26, 3, 'open')),
                            (160, (23, 3, 'up')), (190, (21, 4, 'open')), (240, (19, 4, 'up'))])

    # -- E: it lands: surprise .. a double take .. delight
    bf.append((land, PU))                                      # 13150 touches down on his flower ..
    flower.append((land + 110, 'dip'))                         # .. which gives straight down under it
    face.append((land + 220, 'wide'))                          # he feels it: SURPRISE
    _seq(arms, land + 290, [(170, 'up'), (0, 'side')])        # the hands flinch a beat after the eyes
    face.append((land + 860, 'look_r'))                        # where did that come from? ..
    face.append((land + 1300, 'look_u'))                       # .. oh, up there!
    joy = land + 1970                                          # 15120
    _seq(face, joy - 70, [(70, 'half'), (1050, 'happy'), (70, 'half'), (0, 'open')])
    _seq(arms, joy + 90, [(1100, 'up'), (0, 'side')])         # hands up after the eyes, down after they open
    # the flower bobs with his joy (up and out, then it settles, bent out under the weight as at frame
    # 0) and the butterfly rides it fanning its wings hello: open > up > open
    _seq(flower, joy + 200, [(220, 'sway_r'), (0, 'dip_r')])
    _seq(bf, joy + 90, [(110, PO), (220, PU), (0, PO)])
    _twinkle(fx, joy, JOY_L, last=90)
    _twinkle(fx2, joy + 330, JOY_R)                            # its own track: both glints play in full

    # -- F: wind-down: a glance at the input box, a basking wing-breath, a slow blink, HOLD into the loop
    _seq(face, 17300, [(700, 'look_d'), (0, 'open')])
    _seq(bf, 18250, [(320, PU), (0, PO)])
    _blink(lids, 19000, half=90, line=150)
    return tr


def _beats():
    """Cut the tracks into one beat list: [(ms, state)] with every track's current value."""
    tracks = _story()
    times = sorted({t for ev in tracks.values() for t, _ in ev if t < LOOP} | {0})
    for a, b in zip(times, times[1:] + [LOOP]):
        if b - a < MIN_GAP:
            raise ValueError('idle-moods: events at %d and %d ms are only %d ms apart' % (a, b, b - a))
    beats = []
    for i, t in enumerate(times):
        end = times[i + 1] if i + 1 < len(times) else LOOP
        st = {}
        for k, ev in tracks.items():
            cur = None
            for tt, v in sorted(ev, key=lambda e: e[0]):
                if tt <= t:
                    cur = v
            st[k] = cur
        beats.append((end - t, st))
    return beats


def build():
    beats = _beats()
    lay = {k: [] for k in ('lavender', 'arms', 'face', 'flower', 'bfly', 'fx')}
    for ms, s in beats:
        lay['lavender'].append((_daisy(s['daisy']), ms))
        lay['arms'].append((_arms(s['arms']), ms))
        lay['face'].append((_face(s['face'], s['lids']), ms))
        lay['flower'].append((_flower(s['flower']), ms))
        lay['bfly'].append((_bfly(s['bf'], s['flower'], s['daisy']), ms))
        lay['fx'].append((_fx(s['fx'] + s['fx2']), ms))
    layers = [layer('scene', [(_scene(), LOOP)])] + [layer(k, v) for k, v in lay.items()]
    return anim(NAME, DESC, layers, state=STATE)
