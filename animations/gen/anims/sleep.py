# ======================================================================================
# USER FEEDBACK: the user reviewed this fine-face upgrade draft personally and approved it
# ("looks great go"). Keep the scene, beats and fine-line expressions; critics, fixers and judges
# should polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""sleep - Idle for a long time: asleep.

Set (seen from the foot of the bed): a night sky with the crescent moon top-left and a few stars.
Clawd lies tucked in right on the input box: head on a plump pillow, the striped nightcap flopped
over it, a patchwork quilt pulled up to his chin, his two arm stubs lying over the cuff, holding
it.  Beside the bed his firefly friend from the idle animation glows in a jar: his night light.
His FACE acts in the expressive fine-line style (STYLE.md 0b: half-size pixels, fine() +
fine_face(), no mouth, no blush, never resized): thin 'line' lids while he sleeps, a sleepy
one-eyed 'half' peek when the bubble pops, and a dreamy 'content' smile in his eyes (u u) when he
drifts off again.

STORYBOARD (s)   master loop 13.2 s (Clawd, cap tail, quilt, bubble and Zs share it)
   0.00  REST, quilt low (frame 0 = the reduced-motion still): a small z just puffed out beside his
         cap, a big Z up in the top-right ("zZ"), moon, dim stars, the firefly glowing in its jar.
         Zs puff out at 0.00, 2.83 (on the first exhale) and 10.87.  Each floats up and to the
         right on the same hand-placed, gently swaying path: rise, drift, swell into z_medium,
         drift, swell into z_big (every swell keeps its bottom-left corner, so no edge ever moves
         down), then it recedes into the top-right corner (z_medium > z_small, its top-right corner
         still drifting 1 cell per step) and is gone.  The holds lengthen as it climbs (0.30 >
         0.56 s: it slows down as it rises, the big Z at the top is the slowest moment), then a
         slightly quicker fade (0.45, 0.39 s): 3.42 s in all.  Never more than 2, never touching.
   1.50  breath 1: the cuff swells up over his chest (middle 7 columns for 0.7 s, then all 11 with
         his hands riding up), holds 0.55 s, sinks back slowly (0.9 s).  0.33 s after the chest
         peaks the nightcap's tail swings like a damped pendulum, timed like one: it hangs out
         (0.44 s) .. whips back through rest (0.11 s, the bottom of the arc is the fastest
         moment) .. hangs at a smaller swing in (0.29 s) .. rest.  Every breath peak does this
         (breath 3's swing is a lazier 0.5 s late, and settles exactly on the loop seam).
   2.97  on that out-breath a snot bubble buds from his nose: dot > drip (3.30) > small (3.63) ...
         (every size grows on his centre column and hangs from the same 3-cell neck under his
         nose, clear of his lids)
   4.95  breath 2 in: it shrinks back (drip 5.28, dot 5.61) ... 6.20 out: it swells 3x3 (6.25) >
         5x4 > 5x5 (held 0.3 s) > 7x5 (6.90): big steps first, then a pause before the last one,
         which swells down and out from the neck.
   6.25  the last Z of the first half fades as the bubble starts to swell: the stage is clear.
   7.15  full-size wobble: it squashes shorter and wider (9x4, 7.15) > round (7.35): anticipation
   7.70  POP!  A small flash on his face; droplets arc up and out over the pillow and fall, two
         drop onto the quilt (7.70 - 8.07).
   7.80  startle, never quite awake: a gasp lifts the cuff and ONE eye flies open (the other
         stays shut); the pom flicks out (7.89) and back in (8.07), then settles (8.19); 7.98 he
         tugs the quilt up to his eyes (its ends ride up too: the cuff arcs between his hands)
         and that eye droops to a sleepy 'half', both lids a fine pixel higher so a strip of face
         shows above the cuff: a one-eyed peek over the quilt, held still for 0.5 s; 8.48 he
         lowers the quilt and the other eye cracks too: both heavy-lidded ('half' a fine pixel
         low), they look down his nose for the bubble (0.34 s); 8.82 the gaze drifts back and
         the lids get heavy ('half', 0.2 s) .. 9.02 shut .. 9.15 that first eye peeks once more
         ('half'), fighting it .. 9.35 asleep ('line'), and a long sigh lowers the quilt
         (9.35 - 10.25).  Awake 1.55 s in all, and the startled eye is the only full-height eye.
         No Zs from 6.25 to 10.87; 10.87 they come back.
   9.60  the bliss of dozing off again: a dreamy 'content' smile in his eyes (u u), held through
         the sigh and a beat past the Zs' return: it relaxes into thin 'line' lids on breath 3's
         inhale (11.05) and they stay into the seam.
   9.79  every other loop, while the top-right sky is empty: a shooting star falls down-left
         across it (during his dreamy smile) and burns out above the pillow as his sigh ends
         (10.25).
  11.05  breath 3; its slow exhale ends exactly on the loop seam, into frame 0.
Keys of the master-loop layers (and the synced shooting star) are either equal or >= 50 ms apart
(build() asserts it), so no two changes ever land a stray 10-40 ms apart.
Ambient layers on their own loops, so the night never repeats exactly: the library moon's two
stars swap (4.2 s), three tiny stars twinkle (4.7 / 6.1 / 8.3 s), the firefly glows, goes dark,
flits and lights up again in its jar (7.7 s).
Size: everything that never moves is ONE static layer (sky, jar glass, pillow, his head without
eye marks, the cap at rest, quilt, his resting hands); the animated layers carry only what
changes (the swung cap tail + the pillow it uncovers, the cuff + raised hands, bubble, Zs).  His
face is a FINE layer (res 2) that holds nothing but the half-size eye ink: the kit's fine_face()
on his lying head, minus the eyeless head itself, so it composites to exactly fine(head) +
fine_face() (each eye moved by its gaze) for a few runs of ink per frame.  A breath frame keeps
only what differs from the set: a raised hand repaints the two quilt cells it uncovers, while the
resting cuff stays on the 'breath' layer on purpose (in the static layer every lifted frame would
have to repaint the fabric under it).  Zs whose lives never overlap share a layer ('zzz' = the
0.00 Z, 'zzz2' = the other two), so no frame redraws a Z that did not move (merging them measured
bigger).  The estimate is ~42 KB, over the 40 KB ideal and well under 60 KB.  The rest is content:
a 13.2 s story on six synced layers (each nightcap swing repaints the library cap's six colours,
three Zs at 8 steps each, the bubble's 11 steps and its pop) plus the ambient sky.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'sleep'
STATE = 'Idle for a long time: asleep'
DESC = ('Tucked into bed on the input box in a striped nightcap, thin sleepy lids shut: the quilt rises and '
        'falls with slow breaths, Zs float up under a twinkling moon, his firefly glows in a jar, and a snot '
        'bubble swells until it pops and he peeks over the quilt with one heavy-lidded eye, then dozes off '
        'again with a dreamy smile in his eyes.')

T = 13200                                    # master loop (ms)


# ============================================================================================
# Library helpers
# ============================================================================================
def _split(sprites):
    """Cells shared by every frame (-> the static layer) and each frame's own extra cells."""
    sets = [{(x, y, c) for x, y, c in s.cells} for s in sprites]
    common = set.intersection(*sets)
    return common, [s - common for s in sets]


def _cells_sprite(cells, like, name):
    return Sprite(cells=sorted(cells), anchor=(like.ax, like.ay), name=name)


# ============================================================================================
# Local sprites (the library has no wide pillow or breathing quilt that frames a lying head, no
# snot bubble, and no night light)
# ============================================================================================
# Plump pillow behind his head (17x7), light from the top-left, silver contour for the light theme.
# Only its sides and its top-right tuft show around his head and cap (no top-left tuft: it peeked
# through the gap between the cap's tail and dome as a stray light pixel).  The right side pinches
# in; the left side runs straight down under the cap's pom, so wherever the pom swings it always
# hangs over pillow, never over the night sky (the swing frames can then repaint what it uncovers),
# and the lit column under the resting tail is one colour (one repaint colour per swing frame).
_PILLOW = Sprite([
    '.............mmm.',
    'mWWWmmmmmmmmmwMMm',
    'mWWwwwwwwwwwwwwMm',
    'mWWwwwwwwwwwwwMm.',
    'mWwwwwwwwwwwwwMm.',
    'mwwwwwwwwwwwwMMMm',
    '.mmm.........mmm.',
], anchor=(8, 6), name='pillow_wide')
PILLOW_AT = (15, 15)                         # bottom-center cell

# Quilt: the library 'blanket' patchwork (3-wide blue / violet patches, the front edge in shade, a
# folded white cuff) widened into a mound that covers the pillow width.  The static layer holds the
# fabric; the 'breath' layer draws the middle of the cuff: on row 16 when he has breathed out,
# lifted to row 15 over his chest when he breathes in (the fabric underneath then shows).
_QUILT_ROWS = {16: (8, 22), 17: (7, 23), 18: (6, 24), 19: (6, 24)}
_LIFT = {'low': None, 'mid': (12, 18), 'high': (10, 20), 'pull': (10, 20)}   # cuff columns lifted
_RISE = {'low': 0, 'mid': 1, 'high': 1, 'pull': 2}            # ... by this many rows
_CUFF_MOVES = (10, 20)                                       # cuff columns drawn by the breath layer
# A tug drags the cuff's ends up a row with it ({column: rows}; the pillow's bottom corners tuck
# under them), so the whole cuff rises in a mound instead of snapping in two at his hands.
_ENDS = {'pull': {8: 1, 9: 1, 21: 1, 22: 1}}


def _patch(x, y):
    blk = ((x - 14) // 3) % 2                # a violet patch centered on him, blue ones beside it
    x1 = _QUILT_ROWS[y][1]
    if y == 19:                              # front edge, in shade: the next row of patches
        return 'B' if blk == 0 else 'V'
    ch = 'v' if blk == 0 else 'b'
    if x == x1:                              # right edge in shade (light from the top-left)
        ch = 'V' if ch == 'v' else 'B'
    return ch


def _cuff(x):
    x0, x1 = _QUILT_ROWS[16]
    return 'm' if x in (x0, x1) else ('W' if x == x0 + 1 else 'w')


def _quilt(f):
    for y in (16, 17, 18, 19):
        x0, x1 = _QUILT_ROWS[y]
        for x in range(x0, x1 + 1):
            moving = y == 16 and _CUFF_MOVES[0] <= x <= _CUFF_MOVES[1]
            f.put(x, y, _patch(x, 17) if moving else (_cuff(x) if y == 16 else _patch(x, y)))


# Snot bubble: the library gum bubble's shape language (cyan rim, ice inside, white glint top-left),
# drawn locally at every size so library edits can never change the gag.  Anchor = the top-center
# cell, which touches his nose.  Every size grows on his centre column (x 15) and hangs from the
# same 3-cell neck under his nose, so it never touches his lids and always reads as hanging from
# his nose.  The full size stays inside rows 14-18: it hangs from his face instead of resting on the
# quilt's front edge, and the cuff's ends stay visible beside it.
NOSE = (15, 14)                              # just below and between his closed lids


def _b(rows, ax):
    return Sprite(rows, anchor=(ax, 0), name='snot_bubble')


def _bubbles():
    bub = {
        'dot':   _b(['c'], 0),
        'drop':  _b(['c', 'c'], 0),                                     # a drip, centred like the dot
        's3':    _b(['.c.', 'cCc', '.c.'], 1),
        's5x4':  _b(['.ccc.', 'cWCCc', 'cCCCc', '.ccc.'], 2),
        's5x5':  _b(['.ccc.', 'cWCCc', 'cWCCc', 'cCCCc', '.ccc.'], 2),
        'full':  _b(['..ccc..', '.cWWCc.', 'cWCCCCc', 'cCCCCCc', '.ccccc.'], 3),      # 7x5: swells down
                                                                                       # and out from the neck
        'squat': _b(['...ccc...', '.ccWCCcc.', 'cWCCCCCCc', '.ccccccc.'], 4),        # 9x4 wobble: shorter
    }                                                                                  # AND wider (a squash)
    sizes = {k: (s.w, s.h) for k, s in bub.items()}
    assert sizes == {'dot': (1, 1), 'drop': (1, 2), 's3': (3, 3), 's5x4': (5, 4), 's5x5': (5, 5),
                     'full': (7, 5), 'squat': (9, 4)}, sizes
    return bub


# POP: a small flash where the bubble was (white core on his face, ice arms; it never touches the
# background, so it reads on both themes and cannot strobe) and droplets thrown from its rim: two
# arc up and out over the pillow and fall, two drop onto the quilt.
_POP_FLASH = [(15, 15, 'W'), (14, 15, 'C'), (16, 15, 'C'), (15, 14, 'C'), (15, 16, 'C')]
_DROPLETS = [(12, 15, -2.0, -1.2), (18, 15, 2.0, -1.2),      # (x, y, vx, vy) at the bubble's rim
             (13, 18, -1.0, 0.9), (17, 18, 1.0, 0.9)]
POP_MS = (100, 90, 90, 90)                   # flash + droplets, then 3 frames of flight


def _pop_frames():
    paths = [ballistic(x, y, vx, vy, g=0.7, steps=len(POP_MS), drag=0.55) for x, y, vx, vy in _DROPLETS]
    out = []
    for i, ms in enumerate(POP_MS):
        f = Frame()
        if i == 0:
            for x, y, ch in _POP_FLASH:
                f.put(x, y, ch)
        for p in paths:
            x, y = p[i]
            if y <= GROUND:
                f.put(x, y, 'c')
        out.append((f, ms))
    return out


# Firefly night light: a glass jar (steel contour reads on both themes) with a cork, and the idle
# animation's firefly inside.  The glass is static; the firefly layer draws only the inside: one
# glowing cell with a softer halo on two sides, which goes dark, flits and lights up elsewhere.
JAR_AT = (26, 13)                            # top-left cell; the jar stands on row 19
_JAR = Sprite([
    '.ttT.',                                 # cork (tan, shaded right)
    '.sss.',                                 # rim
    's...s',
    's...s',
    's...s',
    's...s',
    '.sss.',
], anchor=(0, 0), name='jar')
_FF_A = (28, 17)                             # low in the jar, center
_FF_B = (27, 16)                             # up on the left


def _glow(glow, at):
    """The firefly (canvas cells): 'dim' = just the bug, 'lit' = core + a halo on two sides only
    (toward the middle of the jar, and below), 'bright' = a bigger, warmer glow."""
    x, y = at
    hx = 1 if x == 27 else -1                # halo toward the middle of the jar
    if glow == 'dim':
        return [(x, y, 'G')]
    if glow == 'lit':
        return [(x, y, 'a'), (x + hx, y, 'g'), (x, y + 1, 'g')]
    return [(x, y, 'y'), (x + hx, y, 'a'), (x, y + 1, 'a'), (x + hx, y + 1, 'g')]


# ============================================================================================
# Clawd lying down (same 1-cell scale and flat orange) + his fine-line face
# ============================================================================================
def _lying(eyes='blink'):
    """Clawd on his back, seen from the foot of the bed.  The pose box sits on HOME; the pillow props
    his head one row above his standing head.  His body continues under the quilt.  Drawn without
    eye marks ('blink'): his face is the fine 'face' layer.  Any eye ink is opaque ('holes=False'):
    the pillow is right behind his face."""
    p = clawd(eyes=eyes, holes=False, larm='none', rarm='none', legs='none')
    cells = {(x, y): ch for x, y, ch in p.sprite.cells}
    for y in range(6, 8):                    # lower body, hidden under the quilt
        for x in range(1, 10):
            cells[(x, y)] = '#'
    sprite = Sprite(cells=[(x, y - 1, ch) for (x, y), ch in cells.items()], anchor=(0, 0), name='clawd_lying')
    anchors = {k: (ax, ay - 1) for k, (ax, ay) in p.anchors.items()}
    return Pose(sprite, anchors, dict(p.spec, custom=True, lying=True))


def _face(name):
    """FINE frame (STYLE.md 0b) holding only his half-size eye ink, for a FACES entry (screen-left
    eye, screen-right eye, gaze).  The kit draws the expression on his lying head (fine() +
    fine_face()); everything that equals the eyeless head of the static set is dropped, so the layers
    composite to exactly fine(head) + fine_face(...).  The gaze then moves that ink by whole fine
    pixels (idle_moods' half-step gaze shift), e.g. up over the tugged-up quilt.  build() checks
    every key: the ink sits on his face with face (or ink) all around it, so a lid never touches the
    cuff, a hand or the bubble."""
    left, right, gaze = FACES[name]
    p = _lying()
    f = Frame()
    put_clawd(f, p)
    head = fine(f)
    ff = fine_face(head.copy(), p, expr=left, right=right)
    out = Frame(res=2)
    out.px = {(x, y + gaze): ch for (x, y), ch in ff.px.items() if head.px.get((x, y)) != ch}
    assert out.px and set(out.px.values()) == {EYE_INK}, 'his face should only add eye ink: %r' % (name,)
    assert all(head.px.get(k) == '#' for k in out.px), 'his eye ink should sit on his face: %r' % (name,)
    out.meta = {'fine_face': [(left, right, gaze)]}
    return out


def _hands(dy):
    """His two arm stubs (1x2, the kit's own arm shape, his arm columns 0 and 10) lying over the cuff,
    holding the quilt.  dy = -1 when the cuff under them is lifted, -2 when he tugs it up to his eyes."""
    rows = ['.' * 11] * (4 + dy) + ['#.........#'] * 2
    return Pose.from_rows(rows, name='clawd_hands')


# ============================================================================================
# Master timeline (ms).  Every list: [(t, state), ...], first key at 0, states hold until the next.
# ============================================================================================
def track(keys, total=T):
    out = []
    for i, (t, s) in enumerate(keys):
        end = keys[i + 1][0] if i + 1 < len(keys) else total
        if end > t:
            out.append((s, end - t))
    return out


POP = 7700
GASP = POP + 100                             # 7.80 s: he startles awake
PULL = GASP + 180                            # 7.98 s: tugs the quilt up to his eyes ..
PEEK = 500                                   # .. and peeks over it, holding still
LOWER = PULL + PEEK                          # 8.48 s: lowers it, looks down his nose
ASLEEP = 9350                                # lids closed for good

# Each breath: the middle of the cuff lifts (0.7 s) .. all of it, hands riding up (hold 0.55 s) ..
# a slow release (0.9 s) .. rest.  Inhales at 1.50 / 4.95 / (gasp 7.80) / 11.05 / 14.70 s: uneven.
BREATH = [
    (0, 'low'),
    (1500, 'mid'), (2200, 'high'), (2750, 'mid'), (3630, 'low'),       # breath 1 (bubble buds)
    (4950, 'mid'), (5610, 'high'), (6200, 'mid'), (7100, 'low'),       # breath 2 (bubble swells)
    (GASP, 'high'),                                                     # startled gasp ..
    (PULL, 'pull'),                                                     # .. quilt tugged up to his eyes
    (LOWER, 'high'),                                                    # lowers it, looks down
    (ASLEEP, 'mid'), (ASLEEP + 900, 'low'),                             # asleep: a long sigh out
    (11050, 'mid'), (11750, 'high'), (12300, 'mid'),                    # breath 3: its exhale ends
]                                                                       # on the seam, into frame 0

# His face, fine-line kit (FINE_EYES): (screen-left eye, screen-right eye, gaze).  The gaze moves the
# eye ink by whole fine pixels (-1 = up, +1 = down: a half-step glance).  He never quite wakes: one
# eye flies open for a beat and droops straight to 'half', the other only ever cracks to 'half', so
# that startled eye is the only full-height eye in the loop.  Then a 'content' smile in his eyes as
# sleep wins again.
FACES = {
    'asleep':  ('line', 'line', 0),          # thin, delicate lids (frame 0)
    'startle': ('line', 'open', 0),          # the pop: one eye flies open, the other stays shut
    'peek':    ('line', 'half', -1),         # it droops to a sleepy 'half', peeking over the quilt
                                             # tugged up under his eyes (one fine pixel up: a strip of
                                             # face shows between the lids and the cuff)
    'down':    ('half', 'half', 1),          # quilt lowered: both heavy-lidded, looking down his nose
    'heavy':   ('half', 'half', 0),          # .. the gaze drifts back and the lids get heavy
    'fight':   ('line', 'half', 0),          # that eye peeks once more, fighting it
    'content': ('content', 'content', 0),    # the bliss of dozing off: a dreamy smile in his eyes (u u)
}
# Keys equal or >= 50 ms from every other master-loop key (build() asserts it).
FACE = [
    (0, 'asleep'),
    (GASP, 'startle'),                       # 7.80 the pop: one eye flies open ..
    (PULL, 'peek'),                          # 7.98 .. and droops: a one-eyed peek over the quilt (0.5 s)
    (LOWER, 'down'),                         # 8.48 quilt down, the other eye cracks too: a heavy-lidded
                                             #      look down his nose, where did it go? (0.34 s)
    (8820, 'heavy'),                         # 8.82 the lids get heavy (0.2 s) ..
    (9020, 'asleep'),                        # 9.02 .. and shut ..
    (9150, 'fight'),                         # 9.15 .. that eye peeks once more, fighting it ..
    (ASLEEP, 'asleep'),                      # 9.35 .. asleep
    (9600, 'content'),                       # 9.60 the bliss of dozing off: a dreamy smile in his eyes
    (11050, 'asleep'),                       # 11.05 it relaxes into thin lids on breath 3's inhale, a
]                                            #       beat after the Zs come back (10.87)

# The nightcap's tail + pom: 'rest' / 'out' (swung away from his head) / 'in' (tucked toward it).
# After every breath peak a damped pendulum, timed like one: it hangs at the big 'out' extreme
# (~0.45 s), whips back through rest (0.11-0.12 s: the bottom of the arc is the fastest moment),
# hangs at the smaller 'in' extreme (~0.3 s) and settles at rest.  The startle flicks it out and
# straight back in, fast.
CAP = [
    (0, 'rest'),
    (2530, 'out'), (2970, 'rest'), (3080, 'in'), (3370, 'rest'),       # breath 1 (peak 2.20)
    (5950, 'out'), (6400, 'rest'), (6520, 'in'), (6820, 'rest'),       # breath 2 (peak 5.61)
    (GASP + 90, 'out'), (GASP + 270, 'in'), (GASP + 390, 'rest'),      # startle: flick out, in, settle
    (12250, 'out'), (12700, 'rest'), (12820, 'in'),                    # breath 3 (peak 11.75): a lazier
]                                                                       # swing; rest again on the seam

BUBBLE = [
    (0, None),
    (2970, 'dot'), (3300, 'drop'), (3630, 's3'),            # buds as he breathes out
    (5280, 'drop'), (5610, 'dot'),                          # shrinks back as he breathes in
    (6250, 's3'), (6400, 's5x4'), (6600, 's5x5'),           # swells as he breathes out: big steps
    (6900, 'full'),                                         # first, a pause before the last one
    (7150, 'squat'), (7350, 'full'),                        # wobbles at full size (anticipation)
    (POP, 'pop'),                                           # POP (flash, droplets arc out and fall)
]

# Zs: one hand-placed path, (library Z, top-left x, top-left y, hold ms).  It rises and drifts in
# turn (the gentle sway), swells with its bottom-left corner fixed (no edge ever moves down), then
# recedes into the top-right corner (its top-right corner keeps drifting 1 cell per step) and is
# gone.  The holds lengthen as it climbs (it slows down as it rises: ease out) up to the big Z at
# the top of its climb; the recede is a little quicker, a fade into the distance, not a glide.
# The spawn is as low as the set allows: its bottom-left cell (18, 7) keeps one free cell from the
# cap (16, 8) and one free row above the pillow's tuft (20-22, 9), which a z on row 8 would touch.
Z_PATH = [
    ('z_small', 18, 4, 300),                 # puffs out beside his cap
    ('z_small', 19, 3, 340),                 # rises
    ('z_small', 20, 3, 390),                 # drifts
    ('z_medium', 21, 2, 470),                # swells (bottom-left corner 1 cell right)
    ('z_medium', 22, 2, 520),                # drifts
    ('z_big', 23, 1, 560),                   # swells: the top of its climb, the slowest moment
    ('z_medium', 25, 1, 450),                # recedes into the corner ..
    ('z_small', 27, 1, 390),                 # .. and is gone (3.42 s in all)
]
Z_BIRTHS = [0, 2830, 10870]                  # frame 0: z_small just born + z_big (born 10.87)
# Zs whose lives never overlap share a layer, so no frame redraws a Z that did not change.
Z_LAYERS = (('zzz', (0,)), ('zzz2', (2830, 10870)))
MASTER_LAYERS = ('face', 'cap_tail', 'breath', 'bubble', 'zzz', 'zzz2')


# ============================================================================================
# Layers
# ============================================================================================
def _touch(a, b):
    """True when two cell sets overlap or touch (8-neighbourhood)."""
    return any((x + dx, y + dy) in b for x, y in a for dx in (-1, 0, 1) for dy in (-1, 0, 1))


def _z_sprite(name):
    s = get(name).sprite(0)
    return s.with_anchor(s.x0, s.y0)         # placed by its top-left corner


def _z_layers(scene):
    """One layer per group of Z_LAYERS.  A Z born late in the loop wraps to the start (seamless).
    Checked at every key time of every Z: 1-cell margins, never touching the set (cap, pillow,
    stars) and never touching another Z, on any layer."""
    starts = [sum(z[3] for z in Z_PATH[:k]) for k in range(len(Z_PATH))]
    life = sum(z[3] for z in Z_PATH)

    def keys_of(births):
        return sorted({0} | {(b + s) % T for b in births for s in starts + [life]})

    def cells(b, t):
        age = (t - b) % T
        if age >= life:
            return None
        name, x, y, _ = Z_PATH[max(k for k, s in enumerate(starts) if s <= age)]
        return set(Frame().place(_z_sprite(name), x, y).px.items())

    assert sorted(b for _, bs in Z_LAYERS for b in bs) == sorted(Z_BIRTHS)
    solid = set(scene.px)                    # the set: no Z may touch the cap, pillow or a star
    for t in keys_of(Z_BIRTHS):
        placed = [{p for p, _ in c} for c in (cells(b, t) for b in Z_BIRTHS) if c]
        for i, g in enumerate(placed):
            assert all(1 <= yy and 1 <= xx <= W - 2 for xx, yy in g), t   # 1-cell margins
            assert not _touch(g, solid), 'a Z touches the set at %d ms' % t
            for h in placed[i + 1:]:
                assert not _touch(g, h), 'Zs touch at %d ms' % t
    out = []
    for name, births in Z_LAYERS:
        frames = []
        keys = keys_of(births)
        for i, t in enumerate(keys):
            alive = [c for c in (cells(b, t) for b in births) if c]
            assert len(alive) <= 1, 'Zs sharing layer %r overlap in time' % name
            f = Frame()
            for (x, y), ch in (alive[0] if alive else ()):
                f.put(x, y, ch)
            frames.append((f, (keys[i + 1] if i + 1 < len(keys) else T) - t))
        out.append(layer(name, frames))
    return out


def _breath_frame(state, scene):
    """The moving middle of the cuff, and his hands holding it ('pull' = tugged up to his eyes).
    His resting hands are part of the static set, so the frame keeps only what differs from it:
    the cuff, hands that ride up with it, and the quilt a raised hand uncovers."""
    f = Frame()
    rest, quilt = Frame(), Frame()
    put_clawd(rest, _hands(0))
    _quilt(quilt)
    for x, y in rest.px:                     # the quilt under his resting hands (the static set
        f.put(x, y, quilt.get(x, y))         # draws them over it), shown when they ride up
    up, rise = _LIFT[state], _RISE[state]
    for x in range(_CUFF_MOVES[0], _CUFF_MOVES[1] + 1):
        lifted = up is not None and up[0] <= x <= up[1]
        y = 16 - (rise if lifted else 0)
        f.put(x, y, _cuff(x))
        for yy in range(y + 1, 16):          # fabric uncovered under a cuff lifted 2 rows
            f.put(x, yy, _patch(x, 17))
    for x, r in _ENDS.get(state, {}).items():
        f.put(x, 16 - r, _cuff(x))           # the cuff's ends, dragged up by the tug ..
        for yy in range(17 - r, 17):         # .. uncover the fabric under them
            f.put(x, yy, _patch(x, 17))
    under = -rise if up and up[0] <= HOME[0] else 0   # do his hands (x 10 / 20) ride up with it?
    put_clawd(f, _hands(under))
    f.px = {k: ch for k, ch in f.px.items() if scene.px.get(k) != ch}
    return f


def _bubble_frames():
    bub = _bubbles()
    out = []
    for size, ms in track(BUBBLE):
        if size == 'pop':
            pops = _pop_frames()
            out += pops
            out.append((Frame(), ms - sum(m for _, m in pops)))
            continue
        f = Frame()
        if size:
            f.place(bub[size], *NOSE)
        out.append((f, ms))
    return out


# ---------------------------------------------------------------- the night sky
MOON_AT = (5, 5)
STARS = [(13, 3), (3, 12), (28, 10)]


def _moon_twinkle():
    """The two stars beside the library moon swap places (its frames 0 / 1), unevenly."""
    moon = get('moon')
    _, extra = _split(moon.frames)
    out = []
    for i, ms in ((0, 2900), (1, 1300)):
        f = Frame()
        f.place(_cells_sprite(extra[i], moon.sprite(i), 'moon_stars'), *MOON_AT)
        out.append((f, ms))
    return out


def _star(idx, period, big=True):
    """One tiny star: a dim dot (in the static sky), then a twinkle at the end of its loop:
    plus .. turning to a cross (library sparkle_small frames 1, 2), or just a plus."""
    sp = get('sparkle_small')
    x, y = STARS[idx]
    tw = [(1, 140), (2, 160)] if big else [(1, 280)]
    seq = [(None, period - sum(ms for _, ms in tw))] + tw
    out = []
    for fr, ms in seq:
        f = Frame()
        if fr is not None:
            f.place(sp.sprite(fr), x, y)
        out.append((f, ms))
    return out


METEOR_T = 2 * T                             # once every other loop ..
METEOR_AT = T + 9790                         # .. just after he has dozed off again (ends 10.25 s,
                                             # as his sigh ends): the Zs are not back up there yet


def _meteor():
    """A shooting star falls down-left across the top-right sky on the library shooting_star's
    2:1 slope and in its colours (yellow head, gold trail, rust tail end: the trail reads on the
    light theme too), and burns out above the pillow.  It is synced to the master loop on purpose:
    it falls in the window when no Z is up there, and every other loop is a little different."""
    steps = [
        ([(29, 1, 'j')], 90),                                                  # a spark
        ([(27, 2, 'y'), (28, 2, 'j'), (29, 1, 'j'), (30, 1, 'O')], 90),
        ([(25, 3, 'y'), (26, 3, 'j'), (27, 2, 'j'), (28, 2, 'O'), (29, 1, 'O')], 90),
        ([(23, 4, 'y'), (24, 4, 'j'), (25, 3, 'j'), (26, 3, 'O'), (27, 2, 'O')], 90),
        ([(21, 5, 'j'), (22, 5, 'O'), (23, 4, 'O')], 100),                     # burns out
    ]
    out = [(Frame(), METEOR_AT)]
    for px, ms in steps:
        f = Frame()
        for x, y, ch in px:
            f.put(x, y, ch)
        out.append((f, ms))
    out.append((Frame(), METEOR_T - METEOR_AT - sum(ms for _, ms in steps)))
    return out


def _firefly():
    """Glows, brightens, goes dark and flits up-left, lights up there, goes dark again and comes
    back to light up where it started (7.7 s, uneven)."""
    seq = [('lit', _FF_A, 2300), ('bright', _FF_A, 900), ('dim', _FF_B, 1100),
           ('lit', _FF_B, 1700), ('dim', _FF_A, 1700)]
    out = []
    for glow, at, ms in seq:
        f = Frame()
        for x, y, ch in _glow(glow, at):
            f.put(x, y, ch)
        out.append((f, ms))
    return out


# ---------------------------------------------------------------- the static set + the cap
def _set_and_cap():
    """Everything that never moves, in ONE static layer, back to front: moon crescent (the cells
    both library frames share), three dim stars, the jar glass, pillow, his head (no eye marks:
    they live on the fine 'face' layer), the library nightcap's dome and brim, the quilt, and his
    hands resting on its cuff.
    His head lies still on the pillow, so only the cap's drooping tail + pom swing.  The 'cap_tail'
    layer is empty while it rests; its 'out' and 'in' frames draw the swung tail and repaint the
    pillow cells the resting tail leaves uncovered (taken from the set itself, so they always
    match).  The swing frames are picked by shape, not index: the one reaching furthest left is
    'out', the one tucked furthest right is 'in'."""
    f = Frame()
    moon = get('moon')
    common, _ = _split(moon.frames)
    f.place(_cells_sprite(common, moon.sprite(0), 'moon_body'), *MOON_AT)
    for x, y in STARS:
        f.place(get('sparkle_small').sprite(0), x, y)
    f.place(_JAR, *JAR_AT)
    f.place(_PILLOW, *PILLOW_AT)
    put_clawd(f, _lying('blink'))
    behind = f.copy()                        # what the cap's tail hangs over
    cap = get('nightcap')
    rest = cap.sprite(0)
    swings = list(cap.frames[1:])
    assert len(swings) >= 2, 'nightcap: needs a tail-out and a tail-in frame'
    swing = {'out': min(swings, key=lambda s: s.x0), 'in': max(swings, key=lambda s: s.x0)}
    assert swing['out'].x0 < rest.x0 < swing['in'].x0, 'nightcap: the tail no longer swings out / in'
    hx, hy = _lying().at('head')
    f.place(rest, hx, hy)
    _quilt(f)
    put_clawd(f, _hands(0))                  # his hands resting on the cuff
    r = Frame().place(rest, hx, hy).px
    tails = {'rest': Frame()}
    for k, spr in swing.items():
        o = Frame().place(spr, hx, hy).px
        d = Frame()
        for (x, y), ch in o.items():
            if r.get((x, y)) != ch:
                d.put(x, y, ch)
        for (x, y) in set(r) - set(o):       # tail cells the swing uncovers: what is behind them
            assert behind.get(x, y) != '.', 'the resting tail hangs over the night sky at (%d, %d)' % (x, y)
            d.put(x, y, behind.get(x, y))
        tails[k] = d
    return f, tails


def _at(l, t):
    """The rows a built layer shows at time t."""
    t %= sum(fr['ms'] for fr in l['frames'])
    for fr in l['frames']:
        if t < fr['ms']:
            return fr['rows']
        t -= fr['ms']


def _check_face(layers, keys):
    """At every master key: no later layer draws over his eye ink, and each fine ink pixel has ink
    or his orange face on all four sides, so his lids never touch the cuff, a hand or the bubble."""
    fi = [l['name'] for l in layers].index('face')
    for t in keys:
        ink = {(x, y) for y, row in enumerate(_at(layers[fi], t)) for x, ch in enumerate(row) if ch != '.'}
        under, over = {}, set()
        for i, l in enumerate(layers):
            if i != fi:
                for y, row in enumerate(_at(l, t)):
                    for x, ch in enumerate(row):
                        if ch != '.':
                            under[(x, y)] = ch
                            if i > fi:
                                over.add((x, y))
        for x, y in ink:
            assert (x // 2, y // 2) not in over, 'something covers his eye at %d ms' % t
            for nx, ny in ((x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                assert (nx, ny) in ink or under.get((nx // 2, ny // 2)) == '#', \
                    'his lid touches %r at %d ms' % (under.get((nx // 2, ny // 2)), t)


def build():
    scene, cap_tails = _set_and_cap()

    layers = [
        static('set', scene),
        layer('moon', _moon_twinkle()),
        layer('star_a', _star(0, 4700)),
        layer('star_b', _star(1, 6100)),
        layer('star_c', _star(2, 8300, big=False)),
        layer('meteor', _meteor()),
        layer('firefly', _firefly()),
        layer('face', [(_face(name), ms) for name, ms in track(FACE)]),
        layer('cap_tail', [(cap_tails[k], ms) for k, ms in track(CAP)]),
        layer('breath', [(_breath_frame(s, scene), ms) for s, ms in track(BREATH)]),
        layer('bubble', _bubble_frames()),
    ] + _z_layers(scene)
    keys = set()
    for l in layers:                         # every master-loop layer must stay in sync with Clawd
        total = sum(fr['ms'] for fr in l['frames'])
        if l['name'] in MASTER_LAYERS:
            assert total == T, l['name']
        if total % T == 0:                   # master-loop layers + the meteor (synced on purpose)
            t = 0
            for fr in l['frames']:
                keys.add(t % T)
                t += fr['ms']
    keys = sorted(keys)
    for a, b in zip(keys, keys[1:] + [keys[0] + T]):   # changes coincide or are >= 50 ms apart
        assert b - a >= 50, 'master-loop keys %d and %d are only %d ms apart' % (a, b % T, b - a)
    _check_face(layers, keys)
    life = sum(z[3] for z in Z_PATH)
    fall = (METEOR_AT % T, METEOR_AT % T + 460)
    for b in Z_BIRTHS:                       # no Z is up in the sky while the shooting star falls
        assert all((t - b) % T >= life for t in range(fall[0], fall[1], 10)), 'a Z meets the meteor'
    return anim(NAME, DESC, layers, state=STATE)
