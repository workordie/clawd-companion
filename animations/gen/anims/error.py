# ======================================================================================
# UPGRADE BRIEF: the approved 'error' animation, upgraded to the expressive fine-line face
# (STYLE.md 0b). Keep the concept, composition, props and beats; polish the face acting and the
# execution (timing, readability, craft, size) rather than redesigning it.
# ======================================================================================
"""error - Something failed.

STORYBOARD (ms)                                                  loop 5980 ms = 46 rain ticks of 130 ms
His FACE acts in the expressive fine-line style (STYLE.md 0b); [eyes] marks what it does. His eyes
REACT a beat (60-70 ms) after what happens to him and LEAD what he decides to do; his shoulders
flinch a beat after his eyes (overlap), so the face never just swaps like a sprite.
  ACT 1 - poor guy
     0  FRAME 0 (the reduced-motion still): at HOME, droopy (arms hang) under a little gray rain cloud
        that drizzles on his head (a drop emerging, one falling, one splashing), beside a red error sign
        (VS Code's own x glyph); [eyes] sad, cast down a half step. A drop drips off his arm into his
        puddle; in the next puddle his rubber duck (debugging buddy) floats and looks at him.
   390  SIGH: a quick inhale (shoulders rise: side; the arm drip lets go) [460 the lids drop to half]
        ... 520 held breath (up, 260) [eyes shut: thin lines] ... 780 then a slower exhale: a little
        breath puff huffs out right beside his face (side, 260) and drifts up and right, swelling, then
        peels into specks [850 heavy half lids lift ... 980 eyes open, cast down] while he sags (1040,
        arms hang). Up 2 rows in 130 ms, down in 520: a sigh, not a shrug (the shrug is palms out).
  1170  the PLIP drop is the only drop in the air (the cloud holds its next one) ...
  1300  PLIP: it lands right on his head with a wide V crown [1370 WINCE: eyes squeezed to thin lines,
        260] ... 1430 his shoulders flinch up (130) ...
  1560  ugh: the arms drop [1630 the wince lets go (half) ... 1690 a flat stare straight at you:
        deadpan 'really?', 260].
  ACT 2 - brave
  1950  he glares up at the cloud, arms still hanging [narrowed lids looking up, 190 ... 2140 the idea:
        his eyes open up, a beat before his hand moves] ...
  2210  reaches behind his back: a furled umbrella pokes up over his shoulder; 2340 WHIP: he brandishes it;
  2470  FWUMP: it half-opens against the cloud; 2600 POP: thrust open, bumping the cloud up (squash) + glint.
  2730  he settles under it, looking up while the drizzle drums on the canopy [2800 a smooth blink that
        closes looking up and reopens on the duck]; 2990 watches a run-off drop let go of the rib tip and
        plip onto his duck (it falls faster and faster) [eyes down-right];
        3250 looks at you and cocks his fist [3320 he BEAMS: happy thin arcs, 580 ms] ... 3380 a brave
        little fist (ting).
  ACT 3 - oops
  3770  (fist still up, still beaming) a gust streaks in over the sign; 3900 his eyes pop open to it
        (up-left) as it blows over the cloud (the streaks stop a clear cell short of it): its top lumps
        lean right; 4030 it reaches the drizzle (drops slant a column per tick) and hits the umbrella,
        which leans and tugs his arm up, so a drop sneaks past its edge [4090 a flinch: thin lines];
        4160 SNATCH: it flips inside out and slips off his fingertips [4220 WIDE 'oh no' eyes chase it
        up and right], then accelerates up and out of the top-right corner on a curve (4290, 4420), speed
        streaks climbing after it, while the cloud's lumps spring back a cell and it settles over him one
        row per tick (the sneaky drop splashes on his head).
  4290  he reaches after it and stares at the empty corner, arm still up (780 in all; 520 after it's gone)
        [still wide ... 4620 one slow, disbelieving blink: half > line (190) > half ... 4940 a blank stare]
  5070  OOPS: he looks at you, palms out [wide: '!'] as a sweat drop beads ... 5200 [a sheepish HAPPY:
        thin arcs, 460] while it just hangs there (the awkward pause)
  5590  his arms lower [5660 the smile melts: half lids ... 5720 eyes cast down]; the drop lets go fast:
        slides, stretches ... 5850 droop, it drips to the dry ground between the puddles -> frame 0
        (where it has soaked in).
  All along the cloud boils: its top lumps change shape at an irregular 1.2 / 1.6 / 1.2 / 0.8 / 0.9 s
  pace (plus the bump, the gust and the spring-back), its underside never moves.
Layers (back to front): scene (static: error sign + both puddles) | rain (one 130 ms tick per frame:
drops, splashes and drips simulated against whatever is under them, plus everything beat-synced that
lasts a single tick, riding on those frames instead of costing frames elsewhere: the breath puff, the
umbrella behind his back, the whip, fwump, pop, lean, snatch and flight poses, glint, wind, speed streaks,
fist ting, sweat drop; cells hidden behind the cloud, Clawd or umbrella at that tick are left out) | duck
(bobs on its own 19-tick 2470 ms beat, co-prime with the 46-tick loop; drawn over the rain so a drip can
never paint on it; afloat, its belly row is hidden and the puddle's water line shows) | cloud (boil +
bump + gust) | clawd (static: his trunk and legs, which never change here) | arms (only the kit's arm
cells) | face (FINE: only the half-size ink of his eyes) | umbrella (just the long open hold). Every
beat is a whole number of rain ticks, so the drizzle always knows what it lands on; the face runs on the
same clock with half-tick steps of its own (blinks, reactions), so it never drifts from the body.
Size: ~44.5 KB (lint estimate; under the 60 KB limit, over the 40 KB target). About half of it is the
rain layer: 46 one-tick frames of drizzle simulated against what is under it each tick, which is what
makes the plip, the drumming canopy, the run-off and the slanting gust work. Folding the arm cells into
those frames was measured to save only ~0.5 KB, and a thinner drizzle would lose the story, so the
size is accepted.
Face (STYLE.md 0b): the fine-line kit only (fine() + fine_face(); FINE_EYES open / half / line / happy /
wide), each moved by a half-step gaze (one fine pixel) so a lid closes where he is looking. Black ink
eyes, no mouth, no blush, normal body size throughout; he never leaves HOME, feet on row 19.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'error'
STATE = 'Something failed'
DESC = ('A little rain cloud drizzles on him beside a red error sign: he sighs and winces, pops open an '
        'umbrella and beams with a brave fist, until a gust flips it inside out and snatches it away: '
        'wide eyes, a blink, a sheepish smile. Oops.')

TICK = 130                       # rain step (ms); every beat lasts a whole number of ticks

_CLOUD_ITEM = get('rain_cloud')
_UMB = get('umbrella')
_SWEAT = get('sweat_drop')
_WIND = get('motion_lines')
_GLINT = get('sparkle_small')
_DUCK = get('rubber_duck_held')
_SMOKE = get('smoke_puff')


# ------------------------------------------------------------------ the cloud (boiling)
def _cloud_sprite():
    """The library rain cloud without its baked-in rain (my drops know where they land)."""
    s = _CLOUD_ITEM.sprite(0)
    return Sprite(cells=[c for c in s.cells if c[1] <= s.ay], anchor=(s.ax, s.ay), name='rain_cloud')


_CLOUD = _cloud_sprite()        # anchor = the underside's centre cell
# Boiling: the top lumps (cloud rows 0-1) change shape; the body rows and the underside never change,
# so the drizzle always leaves from the same cells. 'A' is the library cloud's own top.
_TOPS = {
    'B': ['...mm.mmm..',
          '.mmMMmMMmm.'],
    'C': ['.mmm...mm..',
          'mMMMmmmMmm.'],
}


def _cloud_variant(name, shift=0):
    """Cloud with top lumps `name`, shifted `shift` cells (the gust blows them right, they spring back)."""
    base = [c for c in _CLOUD.cells if c[1] >= _CLOUD.y0 + 2]
    if name == 'A':
        tops = [c for c in _CLOUD.cells if c[1] < _CLOUD.y0 + 2]
    else:
        tops = [(x, y + _CLOUD.y0, ch) for x, y, ch in Sprite(_TOPS[name]).cells]
    tops = [(x + shift, y, ch) for x, y, ch in tops]
    return Sprite(cells=base + tops, anchor=(_CLOUD.ax, _CLOUD.ay), name='rain_cloud_%s%+d' % (name, shift))


# bumped by the opening umbrella: flattened and wider for one beat (anchor = bottom-centre)
_CLOUD_SQUASH = Sprite([
    '..mmmmm.mmm..',
    '.mMMMMmmMmmm.',
    'mMMmmmmmmmmmN',
    '.NNNNNNNNNNN.',
], anchor=(6, 3), name='rain_cloud_squash')


# ------------------------------------------------------------------ local umbrella states
def _leaning(spr, k):
    """Shear: each row shifts right by k * (rows above the anchor). k = 0.5 is a clean 1:2 diagonal."""
    gy = spr.ay
    return Sprite(cells=[(x + int(math.floor(k * (gy - y) + 0.5)), y, ch) for x, y, ch in spr.cells],
                  anchor=(spr.ax, spr.ay), name=spr.name + '_lean')


_FURLED = Sprite([
    '.N.',
    '.l.',
    'lvV',
    'lvV',
    'lvV',
    '.v.',
    '.N.',
    '.N.',
    '.N.',
    '.N.',
    '.T.',
], anchor=(1, 10), name='umbrella_furled')
# behind his back, its top poking up over his right shoulder (grip hidden behind his body)
_BEHIND = _leaning(_FURLED, 0.5)
BEHIND_GRIP = (17, 17)
# brandished: the same 1:2 diagonal, out in his hand
_WHIP = Item('umbrella_whip', 'hand', 'local: furled umbrella brandished at a 1:2 diagonal', _leaning(_FURLED, 0.5))

_HALF = Item('umbrella_half', 'hand', 'local: umbrella half open (fwump), grip = anchor', Sprite([
    '.....N.....',
    '....lvV....',
    '...lvvvV...',
    '..llvvvVV..',
    '.llvvvvvVV.',
    'lv.v.N.V.VV',
    '.....N.....',
    '.....N.....',
    '.....N.....',
    '.....N.....',
    '.....T.....',
], anchor=(5, 10), name='umbrella_half'))

_LEAN = Item('umbrella_lean', 'hand', 'local: umbrella leaning in a gust', _leaning(_UMB.sprite(0), 0.3))


# The umbrella blown inside out: the ribs bend up, so the canopy becomes a narrower tulip on top of the
# shaft with its scalloped rib tips pointing up (same fabric colours, same shaft and grip as the library one).
_INSIDE_OUT = Sprite([
    'l...v.v...V',
    'll.vvvvv.VV',
    '.llvvvvvVV.',
    '..llvvvVV..',
    '...lvvvV...',
    '....lvV....',
    '.....N.....',
    '.....N.....',
    '.....N.....',
    '.....N.....',
    '.....T.....',
], anchor=(5, 10), name='umbrella_inside_out')
# speed streaks trailing something that flies up and to the right (two parallel 1:1 dashes)
_STREAKS = Sprite([
    '..s..s',
    '.s..s.',
    's..s..',
], anchor=(2, 1), name='streaks')


def _place_clip(f, spr, x, y):
    """frame.place that skips cells outside the canvas (things deliberately entering or leaving)."""
    for sx, sy, ch in spr.cells:
        px, py = x + sx - spr.ax, y + sy - spr.ay
        if 0 <= px < W and 0 <= py < H:
            f.put(px, py, ch)


# ------------------------------------------------------------------ the beats
LOW, MID, HIGH = (15, 7), (15, 6), (15, 5)      # cloud anchor (its bottom-centre cell)
SQUASH = 'squash'                               # HIGH, flattened by the bump

# (ticks, face, larm, rarm, umbrella, cloud, tag). face = his fine-line eyes from the beat's start (see
# _face_parts: an expression, optionally moved by a half-step gaze); _FACE_STEPS adds the in-between
# steps (smooth blinks, the melt of a smile).
_BEATS = [
    # ACT 1: poor guy
    (3, 'look_d', 'down', 'down', None, LOW, ''),             # FRAME 0: droopy in the drizzle, sad eyes down
    (1, 'look_d', 'side', 'side', None, LOW, 'sigh'),         # sigh: a quick inhale (the lids drop a beat later)
    (2, 'line_d', 'up', 'up', None, LOW, 'held'),             # ... held breath, eyes shut
    (2, 'line_d', 'side', 'side', None, LOW, 'exhale'),       # a long exhale: the breath puff; heavy lids lift
    (2, 'look_d', 'down', 'down', None, LOW, 'sag'),          # ... and he sags, eyes cast down
    (1, 'look_d', 'down', 'down', None, LOW, 'plip'),         # PLIP: a crown on his head (the WINCE follows) ...
    (1, 'line', 'side', 'side', None, LOW, 'hunch'),          # ... his shoulders flinch up a beat after the eyes
    (3, 'line', 'down', 'down', None, LOW, 'ugh'),            # ugh: the wince lets go into a deadpan stare at you
    # ACT 2: brave
    (2, 'half_u', 'down', 'down', None, LOW, 'glare'),        # glares up at the cloud (narrowed lids) .. an idea
    (1, 'look_u', 'down', 'none', 'behind', LOW, 'reach'),    # reaches behind his back
    (1, 'look_u', 'down', 'out', 'whip', LOW, ''),            # brandishes a furled umbrella
    (1, 'look_u', 'down', 'down', 'half', LOW, ''),           # fwump
    (1, 'look_u', 'down', 'side', 'open', SQUASH, 'pop'),     # POP: thrust open, bumps the cloud up
    (2, 'look_u', 'down', 'down', 'open', HIGH, 'settle'),    # settles; the drizzle drums on it
    (2, 'look_dr', 'down', 'down', 'open', HIGH, 'watch'),    # the run-off plips onto his duck
    (1, 'open', 'up', 'down', 'open', HIGH, 'brave'),         # looks at you, cocks his fist, beams ...
    (4, 'happy', 'raise', 'down', 'open', HIGH, 'fist'),      # ... brave little fist (ting), beaming
    # ACT 3: oops
    (1, 'look_ul', 'side', 'down', 'open', HIGH, 'gust'),     # the gust blows over the cloud: eyes pop open to it
    (1, 'look_ul', 'side', 'side', 'lean', HIGH, 'lean'),     # it hits the umbrella: leans, tugs his arm up; flinch
    (1, 'line', 'side', 'point', ('fly', 23, 14, 0.3), HIGH, 'snatch'),   # inside out, off his fingertips: OH NO
    (1, 'wide_ur', 'side', 'wave', ('fly', 26, 11, 0.6), MID, ''),        # he reaches after it
    (1, 'wide_ur', 'side', 'wave', ('fly', 28, 6, 0.75), LOW, ''),        # out the top-right corner
    (4, 'wide_ur', 'side', 'wave', None, LOW, 'gone'),        # still reaching, stares after it (+ a slow blink)
    (4, 'wide', 'out', 'out', None, LOW, 'oops'),             # oops: palms out at you, wide '!'; a sweat drop beads
    (2, 'happy', 'side', 'side', None, LOW, 'lower'),         # arms lower, the smile melts: it slides, stretches
    (1, 'look_d', 'down', 'down', None, LOW, ''),             # droop, it drips off -> frame 0
]
# In-between face steps: (beat tag, ms after its start, face). Smooth fine blinks go half > line > half
# (60-190 ms each); emotional holds stay about 400 ms or longer. A step sits on a rain tick or 60-70 ms
# into one, so the face never makes a composite moment shorter than MIN_GAP with the drizzle.
# Acting: his eyes REACT 60-70 ms after what happens to him (the sigh's shoulders, the plip, the gust,
# the snatch) and LEAD what he decides to do (the idea before the reach); the shoulders flinch a beat
# after the eyes (overlap).
_FACE_STEPS = [
    ('sigh', 70, 'half_d'),        # the lids drop a beat after the shoulders rise ...
    ('exhale', 70, 'half_d'),      # the exhale: heavy lids lift a beat after the shoulders drop ...
    ('exhale', 200, 'look_d'),     # ... open, sad, as the breath puff drifts away
    ('plip', 70, 'line'),          # WINCE: a beat after the drop hits
    ('ugh', 70, 'half'),           # the wince lets go ...
    ('ugh', 130, 'open'),          # ... into a flat stare straight at you (deadpan: 'really?')
    ('glare', 190, 'look_u'),      # the idea: his eyes open up a beat before his hand moves
    ('settle', 70, 'half_u'),      # safe under it: a smooth blink that closes looking up ...
    ('settle', 130, 'line_u'),
    ('settle', 200, 'half_dr'),    # ... and reopens on the duck (the blink carries the glance)
    ('brave', 70, 'happy'),        # a beat after he turns to you, he beams
    ('lean', 60, 'line'),          # FLINCH a beat after the gust yanks the umbrella ...
    ('snatch', 60, 'wide_ur'),     # ... and they pop WIDE as it flips and slips away: OH NO
    ('gone', 70, 'half_ur'),       # one slow, disbelieving blink ...
    ('gone', 130, 'line_ur'),
    ('gone', 320, 'half_ur'),
    ('gone', 390, 'look_ur'),      # ... then a blank stare at the empty corner
    ('oops', 130, 'happy'),        # '!' ... then a sheepish smile while the sweat drop hangs
    ('lower', 70, 'half'),         # the smile melts (half lids) as the drop lets go ...
    ('lower', 130, 'look_d'),      # ... into sad eyes cast down
]
MIN_GAP = 60                       # no face step (or face/rain composite moment) shorter than this
_START = []
_t = 0
for _b in _BEATS:
    _START.append(_t)
    _t += _b[0]
N_TICKS = _t
TOTAL = N_TICKS * TICK
assert TOTAL <= 6000, TOTAL


def _tick(tag):
    for i, b in enumerate(_BEATS):
        if b[6] == tag:
            return _START[i]
    raise KeyError(tag)


def _beat_at(k):
    """Beat index at rain tick k."""
    k %= N_TICKS
    for i in range(len(_BEATS) - 1, -1, -1):
        if _START[i] <= k:
            return i
    return 0


def _pose(i):
    # 'blink': no eye cells in his body; the fine face layer draws his eyes
    b = _BEATS[i]
    return clawd(eyes='blink', larm=b[2], rarm=b[3])


def _clawd_frame(i):
    f = Frame()
    put_clawd(f, _pose(i))
    return f


# Clawd is split by what changes, so each part only pays for its own changes (all are cut from the same
# clock, so they never drift): his trunk and legs never change here (he never leaves HOME), so they are
# one static layer; the arms layer holds only the kit's arm cells; the fine face layer only his eye ink.
# (Not in the scene layer: over the puddle, the gaps between his legs would be enclosed and the kit's
# black-eye safety net would ink them.)
_TRUNK = clawd(eyes='blink', larm='none', rarm='none')


def _trunk_frame():
    f = Frame()
    put_clawd(f, _TRUNK)
    return f


_TRUNK_CELLS = set(_trunk_frame().px)


def _arms_frame(i):
    """Only his arm cells: the kit pose drawn with put_clawd, minus the static trunk."""
    f = _clawd_frame(i)
    f.px = {c: ch for c, ch in f.px.items() if c not in _TRUNK_CELLS}
    return f


# ------------------------------------------------------------------ his face (fine-line, STYLE.md 0b)
_GAZE = {'c': (0, 0), 'u': (0, -1), 'd': (0, 1), 'ul': (-1, -1), 'ur': (1, -1), 'dr': (1, 1)}
_ARCS = ('happy', 'content')       # closed-eye arcs sit centred on the eye cell, whatever the gaze
_TRUNK_FINE = fine(_trunk_frame())
# his two 3x3-cell eye windows, in fine pixels: the face layer never draws outside them
_EYE_WIN = {(2 * (x + dx) + i, 2 * (y + dy) + j)
            for x, y in (_TRUNK.at('eye_l'), _TRUNK.at('eye_r'))
            for dx in (-1, 0, 1) for dy in (-1, 0, 1) for i in (0, 1) for j in (0, 1)}


def _face_parts(face):
    """'look_d' -> ('open', 'd'); 'half_d' -> ('half', 'd'); 'wide_ur' -> ('wide', 'ur'); 'line' -> ('line', 'c')."""
    expr, _, gaze = face.partition('_')
    return ('open' if expr == 'look' else expr), (gaze or 'c')


def _face_frame(face):
    """FINE layer frame: only the half-size ink pixels of the kit's fine_face() on top of his trunk,
    moved by the half-step gaze (so a half lid or a blink line closes where he is looking)."""
    expr, gaze = _face_parts(face)
    ff = fine_face(_TRUNK_FINE.copy(), _TRUNK, expr=expr)
    gx, gy = (0, 0) if expr in _ARCS else _GAZE[gaze]
    out = Frame(res=2)
    for (x, y), ch in ff.px.items():
        if _TRUNK_FINE.px.get((x, y)) != ch:
            out.put(x + gx, y + gy, ch)
    assert out.px and set(out.px) <= _EYE_WIN and set(out.px) <= set(_TRUNK_FINE.px), face
    out.meta = {'fine_face': [(expr, expr, gaze)]}
    return out


def _face_track():
    """[(face, ms)] on the body's clock: each beat's face from its start, plus the in-between steps."""
    ev = {}
    for i, b in enumerate(_BEATS):
        ev[_START[i] * TICK] = b[1]
    for tag, dt, face in _FACE_STEPS:
        assert dt % TICK == 0 or MIN_GAP <= dt % TICK <= TICK - MIN_GAP, ('face step between rain ticks', tag, dt)
        ev[_tick(tag) * TICK + dt] = face
    ts = sorted(ev)
    out = []
    for k, t in enumerate(ts):
        end = ts[k + 1] if k + 1 < len(ts) else TOTAL
        assert end - t >= MIN_GAP, ('face steps too close', t, end)
        out.append((ev[t], end - t))
    return out


def _umbrella_frame(i):
    f = Frame()
    umb = _BEATS[i][4]
    p = _pose(i)
    if umb == 'whip':
        wear(f, _WHIP, p)
    elif umb == 'half':
        wear(f, _HALF, p)
    elif umb == 'open':
        wear(f, _UMB, p)
    elif umb == 'lean':
        wear(f, _LEAN, p)
    elif isinstance(umb, tuple):
        _place_clip(f, _leaning(_INSIDE_OUT, umb[3]), umb[1], umb[2])
    return f


def _behind_cells(i):
    """The furled umbrella behind his back (drawn in the rain layer, under his body)."""
    if _BEATS[i][4] != 'behind':
        return {}
    f = Frame()
    f.place(_BEHIND, *BEHIND_GRIP)
    return f.px


def _rides_rain(i):
    """Umbrella poses that last exactly one rain tick (whip, fwump, pop, lean, snatch, flight) never
    overlap Clawd or the cloud, so they ride on the rain tick frames instead of costing umbrella-layer
    frames (pixel-identical); only the long open hold keeps its own layer."""
    if _BEATS[i][0] != 1 or _BEATS[i][4] in (None, 'behind'):
        return False
    me = _umbrella_frame(i).px
    return all(_umbrella_frame(j % len(_BEATS)).px != me for j in (i - 1, i + 1))


# the boil: (from tick, top lumps, shift). The gust blows the lumps a cell right, they spring back a
# cell left on the snatch, then settle; the seam (C -> A) is just one more boil step.
_BOIL = [(0, 'A', 0), (9, 'C', 0), (_tick('settle'), 'B', 0), (_tick('gust'), 'B', 1), (_tick('snatch'), 'B', -1),
         (_tick('snatch') + 1, 'A', 0), (_tick('oops'), 'C', 0)]


def _boil_at(k):
    cur = _BOIL[0]
    for b in _BOIL:
        if b[0] <= k:
            cur = b
    return cur[1], cur[2]


def _cloud_frame(k):
    f = Frame()
    c = _BEATS[_beat_at(k)][5]
    if c == SQUASH:
        f.place(_CLOUD_SQUASH, *HIGH)
    else:
        f.place(_cloud_variant(*_boil_at(k)), *c)
    return f


# ------------------------------------------------------------------ scenery: sign, puddles, duck
# VS Code's own error glyph as a little road sign planted beside him: red disc (pink glint top-left,
# dark-red shade bottom-right), white x, steel post.
_SIGN = Sprite([
    '..prr..',
    '.prrrr.',
    'rrWrWrR',
    'rrrWrrR',
    'rrWrWrR',
    '.rrrrR.',
    '..RRR..',
    '...s...',
    '...s...',
    '...s...',
    '...s...',
    '...N...',
], anchor=(3, 11), name='error_sign')
SIGN_AT = (4, GROUND)            # bottom of the post
# two puddles with a dry gap between them (one long line of water would read as a UI stroke): his, with
# cyan ripples where his arm drips land, and the duck's
_PUDDLE = Sprite(['BbbcbbbbbbbbbcB..BcbbbbB'], anchor=(0, 0), name='puddles')   # x 7-21 and 24-30
PUDDLE_AT = (7, GROUND)
# the duck faces him (flipped), top-left anchored. Afloat, its belly row is under water: the static
# puddle's water line shows in its place; when it bobs up, the belly clears the water.
_DUCK_SPR = _DUCK.sprite(0).flipped()
_DUCK_SPR = _DUCK_SPR.with_anchor(_DUCK_SPR.x0, _DUCK_SPR.y0)
_DUCK_AFLOAT = Sprite(cells=[c for c in _DUCK_SPR.cells if c[1] < _DUCK_SPR.y1], anchor=(0, 0), name='duck_afloat')
DUCK_AT = (24, 15)
_DUCK_CELLS = {(DUCK_AT[0] + x, DUCK_AT[1] + y) for x, y, ch in _DUCK_AFLOAT.cells}
DUCK_AFLOAT_MS, DUCK_UP_MS = 14 * TICK, 5 * TICK      # afloat 1.82 s, bobbed up 0.65 s


# ------------------------------------------------------------------ rain
# Hand-placed drizzle: tick -> column (absolute x, always under the cloud's underside at that tick).
# Irregular 1-5 tick gaps; a column is reused only after its drop has landed, so drops never stack.
# Frame 0 shows a drop emerging (tick 0), one falling (44) and a splash on his head (42). The PLIP drop
# (tick 6) lands on his head with a wide crown a beat before he squeezes his eyes shut, in a spotlight:
# for its last two ticks it is the only drop in the air (the cloud holds its next drop until tick 11),
# so its crown reads on its own; nothing falls at x >= 19 while the sweat drop is out. Under the open
# umbrella (HIGH) every column is over the canopy. The tick-3 drop lands after the sigh's breath puff
# has left his head. No two drops, drips or splashes ever touch (checked while placing them), so each
# reads as its own drop.
_SPAWN = {0: 16, 3: 19, 4: 12, 6: 16, 11: 15, 12: 18, 13: 12, 17: 14,
          21: 18, 23: 15, 24: 18, 27: 14, 28: 19, 31: 17,
          32: 11, 35: 15, 38: 17, 40: 12, 42: 17, 44: 13}
# drops, drips and splashes are all the puddle's blue (3.4:1 on white, 5:1 on dark): one colour per
# tick frame keeps the 46-frame rain layer lean.
RAIN = 'b'
_DRIP_ARM = {45: 'l', 2: 'r', 8: 'l', 12: 'r', 15: 'l'}   # tick -> arm that drips (only while it hangs down)
_HANG = {'l': 2, 'r': 2, 'tip': 0}       # ticks a drip clings before it falls (run-off accelerates: 1, then 2 rows)
# splash shapes, relative to the cell a drop lands on: a plain splash is a droplet each side; the
# run-off that plips onto the duck adds a crown tip; THE plip on his head throws a wide V crown (two
# droplets each side, the outer ones flung up a row: twice a plain splash's width)
_SPLASH = {'': ((-1, 0), (1, 0)), 'plip': ((-1, 0), (1, 0), (0, -1)),
           'head': ((-1, 0), (1, 0), (-2, -1), (2, -1))}
_RUNOFF = (_tick('settle'), _tick('brave'))                # ticks a drop leaves the canopy's right rib tip
_SLANT = {_tick('lean'), _tick('snatch')}                  # the gust reaches the drops: a column right per tick


def _solids(i):
    return set(_clawd_frame(i).px) | set(_umbrella_frame(i).px) | set(_behind_cells(i)) | _DUCK_CELLS


def _canopy_tip(i):
    """Below the open umbrella's right rib tip (where run-off drips form), or None."""
    if _BEATS[i][4] != 'open' or _BEATS[i][5] == SQUASH:
        return None
    px = _umbrella_frame(i).px
    x = max(xx for xx, yy in px)
    return (x, max(yy for xx, yy in px if xx == x) + 1)


def _underside(cloud):
    """Columns and row of the cloud's underside, or None while it is being bumped."""
    if cloud == SQUASH:
        return None
    cx, cy = cloud
    return {x - _CLOUD.ax + cx for x, y, ch in _CLOUD.cells if y == _CLOUD.ay}, cy


# ------------------------------------------------------------------ effects riding on the rain ticks
# The sigh's breath: a little puff huffs out right beside his face (one clear cell from his head),
# swells into the library smoke puff's first shape as it drifts up and right, peels into specks and
# fades (top-left anchored; silver with a gray underside so it reads on both themes, smaller and rounder
# than the rain cloud).
_BREATH = [
    (Sprite(['.mm',
             'mMm',
             '.N.'], name='breath_0'), 21, 11),
    (_SMOKE.sprite(0).with_anchor(_SMOKE.sprite(0).x0, _SMOKE.sprite(0).y0), 22, 9),
    (Sprite(['.m.m',
             'm.N.'], name='breath_2'), 24, 7),
    (Sprite(['m'], name='breath_3'), 26, 6),
]


def _clear_of(spr, x, y, cells):
    """`spr` placed at (x, y) minus every cell on or next to (8 ways) `cells`: wind passing behind the
    cloud keeps a clear ring of sky around its silhouette (the same grays: touching, even at a corner,
    it would look like a smeared cloud)."""
    keep = [(sx, sy, ch) for sx, sy, ch in spr.cells
            if not any((x + sx - spr.ax + gx, y + sy - spr.ay + gy) in cells
                       for gx in (-1, 0, 1) for gy in (-1, 0, 1))]
    return Sprite(cells=keep, anchor=(spr.ax, spr.ay), name=spr.name + '_clear')


def _fx(k):
    """Effects for rain tick k: list of (sprite, x, y). All of them sit on the rain grid."""
    out = []
    t = _tick('exhale')            # the sigh's breath puff: huffs out beside his face, drifts up and away
    for n, (spr, x, y) in enumerate(_BREATH):
        if k == t + n:
            out.append((spr, x, y))
    t = _tick('pop')                                    # glint on the canopy's shoulder: plus, x, dot
    for n, fr in enumerate((1, 2, 0)):
        if k == t + n:
            out.append((_GLINT.sprite(fr), 26, 6))
    t = _tick('fist')                                   # ting: the fist's glint, plus, x, fading dot
    for n, fr in enumerate((1, 2, 0)):
        if k == t + n:
            out.append((_GLINT.sprite(fr), 10, 9))
    t = _tick('gust') - 1        # the gust streaks in over the sign, picking up speed (5, then 7 cells a
    for n, (fr, x, y) in enumerate(((0, 3, 4), (1, 8, 4), (0, 15, 5))):     # tick), passes behind the cloud,
        if k == t + n:                                                       # hits the canopy
            spr = _WIND.sprite(fr)
            if n == 1:           # reaching the cloud: the streaks stop a clear cell short of its edge
                spr = _clear_of(spr, x, y, set(_cloud_frame(k).px))
            out.append((spr, x, y))
    t = _tick('snatch') + 1      # streaks trailing the umbrella as it shoots up and out of the corner: they
    for n, (x, y) in enumerate(((23, 7), (24, 5), (29, 2))):   # climb with it (never sink), clear of its shaft
        if k == t + n:
            out.append((_STREAKS, x, y))
    return out


def _sweat_frame(k):
    """Library sweat-drop frame for rain tick k: it beads on the shrug, hangs through the awkward pause,
    then lets go fast: slide, stretch, drip."""
    t = _tick('oops')
    seq = [6, 0, 0, 0, 1, 3, 4]
    return seq[k - t] if 0 <= k - t < len(seq) else None


_SWEAT_NUDGE = {4: (-1, 2)}      # library frame -> (dx, dy): the falling drip


def _simulate():
    """The drizzle, one entry per rain tick of the loop: (beat index, pieces). Each piece is the list of
    cells of one drop streak, hanging/falling drip or splash (kept apart so tools can check spacing)."""
    n = N_TICKS
    plip = _tick('plip') - 4                 # the PLIP drop leaves the low cloud 4 ticks before the squeeze
    assert _SPAWN.get(plip) is not None
    sweat = [k for k in range(n) if _sweat_frame(k) is not None]
    assert all(x < 19 for k, x in _SPAWN.items() if sweat[0] - 4 <= k <= sweat[-1]), 'rain on the sweat drop'
    cache = {}
    drops, drips, out = [], [], []
    for k in range(-n, n):                   # one warm-up loop, then the recorded loop
        kk = k % n
        i = _beat_at(kk)
        if i not in cache:
            cache[i] = (_solids(i), _canopy_tip(i), _pose(i), _underside(_BEATS[i][5]))
        solid, tip, pose, under = cache[i]
        dx = 1 if kk in _SLANT else 0
        splash, nxt = [], []
        for x, y, tag, _s in drops:
            if (x, y) in solid:              # swallowed by something that just appeared
                continue
            if (x + dx, y + 1) in solid or y + 1 > GROUND or x + dx > W - 2:
                splash.append((x, y, tag))
            else:
                nxt.append((x + dx, y + 1, tag, dx))
        drops = nxt
        if kk in _SPAWN and under:
            cols, cy = under
            x = _SPAWN[kk]
            assert x in cols, ('drop not under the cloud', kk, x)
            if _BEATS[i][5] == HIGH and _BEATS[i][4] == 'open':
                assert 14 <= x, ('drop misses the canopy', kk, x)
            if (x, cy + 1) not in solid:
                drops.append((x, cy + 1, 'head' if kk == plip else '', 0))
        nd = []                              # drips (x, y, age, src): cling _HANG ticks, then fall
        for x, y, age, src in drips:
            if age < _HANG[src] and src in ('l', 'r') and pose.spec['larm' if src == 'l' else 'rarm'] != 'down':
                age = _HANG[src]             # his arm moved: the hanging drip lets go now
            if age < _HANG[src]:
                nd.append((x, y, age + 1, src))
                continue
            ny = y
            for _ in range(2 if src == 'tip' and age > _HANG[src] else 1):
                if (x, ny + 1) in solid or ny + 1 > GROUND:
                    break
                ny += 1
            if (x, ny + 1) in solid or ny + 1 > GROUND:
                splash.append((x, ny, 'plip' if src == 'tip' else ''))   # run-off plips on the duck: a crown
            else:
                nd.append((x, ny, age + 1, src))
        drips = nd
        if _BEATS[i][4] is None and kk in _DRIP_ARM:
            src = _DRIP_ARM[kk]
            if pose.spec['larm' if src == 'l' else 'rarm'] == 'down':
                drips.append((HOME[0] + (0 if src == 'l' else 10), HOME[1] + 5, 0, src))
        if tip and kk in _RUNOFF:
            drips.append((tip[0], tip[1], 0, 'tip'))
        if k < 0:
            continue
        pieces = [[(x - s, y - 1), (x, y)] for x, y, tag, s in drops]      # a 2-cell streak; slanted in the gust
        pieces += [[(x, y)] for x, y, age, src in drips]
        for x, y, tag in splash:
            cells = [(x + sx, y + sy) for sx, sy in _SPLASH[tag]]
            cells = [c for c in cells if c not in solid and 0 <= c[0] < W]
            if cells:
                pieces.append(cells)
        out.append((i, pieces))
    return out


def _rain_layer():
    frames = []
    for kk, (i, pieces) in enumerate(_simulate()):
        pose = _pose(i)
        f = Frame()
        for (x, y), ch in _behind_cells(i).items():
            f.put(x, y, ch)
        for cells in pieces:
            for x, y in cells:
                f.put(x, y, RAIN)
        for spr, x, y in _fx(kk):
            _place_clip(f, spr, x, y)
        if _rides_rain(i):                   # over the wind, as if in front (it never overlaps Clawd)
            f.px.update(_umbrella_frame(i).px)
        sw = _sweat_frame(kk)
        if sw is not None:   # the drip falls fast, a cell left (clear of the duck's beak), its tip down on
            # the dry ground between the puddles (row 19), where it soaks in on the next tick (frame 0)
            dx, dy = _SWEAT_NUDGE.get(sw, (0, 0))
            wear(f, _SWEAT, pose, i=sw, dx=dx, dy=dy)
        # cells the cloud, Clawd or the open umbrella cover at this tick never show: leave them out
        # (pixel-identical, fewer bytes: drop tails tucked under the cloud, the wind behind it, the grip
        # of the umbrella behind his back)
        hidden = set(_cloud_frame(kk).px) | set(_clawd_frame(i).px)
        if not _rides_rain(i):
            hidden |= set(_umbrella_frame(i).px)
        for c in hidden:
            f.px.pop(c, None)
        frames.append((f, TICK))
    return frames


def build():
    arms = [(_arms_frame(i), b[0] * TICK) for i, b in enumerate(_BEATS)]
    face = [(_face_frame(fc), ms) for fc, ms in _face_track()]
    umb = [(Frame() if _rides_rain(i) else _umbrella_frame(i), b[0] * TICK) for i, b in enumerate(_BEATS)]
    cloud = [(_cloud_frame(k), TICK) for k in range(N_TICKS)]
    rain = _rain_layer()
    duck, duck_up = Frame(), Frame()
    duck.place(_DUCK_AFLOAT, *DUCK_AT)
    duck_up.place(_DUCK_SPR, DUCK_AT[0], DUCK_AT[1] - 1)
    scene = Frame()
    scene.place(_SIGN, *SIGN_AT)
    scene.place(_PUDDLE, *PUDDLE_AT)
    trunk = _trunk_frame()
    for i in range(len(_BEATS)):         # the trunk really is static, and no arm ever covers an eye window
        f = _clawd_frame(i).px
        assert all(f.get(c) == ch for c, ch in trunk.px.items()), 'his trunk changed: it cannot be static'
        assert not {(2 * x + a, 2 * y + b) for x, y in _arms_frame(i).px for a in (0, 1) for b in (0, 1)} & _EYE_WIN
    assert total_ms(arms) == total_ms(face) == total_ms(rain) == total_ms(cloud) == TOTAL, (
        total_ms(arms), total_ms(face), total_ms(rain), TOTAL)
    return anim(NAME, DESC, [
        static('scene', scene),
        layer('rain', rain),
        # the duck bobs on its own 19-tick beat (2.47 s, co-prime with the 46-tick loop): its hops land on
        # rain ticks (no sliver moments) and the combination repeats only every ~114 s
        layer('duck', [(duck, DUCK_AFLOAT_MS), (duck_up, DUCK_UP_MS)]),
        layer('cloud', cloud),
        static('clawd', trunk),
        layer('arms', arms),
        layer('face', face),                                # FINE: his eyes act
        layer('umbrella', umb),
    ], state=STATE)
