"""rate-limit - Rate limited: waiting before Claude can continue.

STORYBOARD (s)   master loop 14.0 s; every synced layer is cut from ONE beat list (the grain layer from the
same sand schedule), so nothing drifts.
 A  0.00  HOLD (frame 0 = the reduced-motion still): Clawd at HOME, steaming blue mug in his left hand, a
          little sprout on his head (he has waited so long something grew), WATCHING the big hourglass
          beside him: half run, a funnel on top, a mound below, the stream. A pink snail (rate limit =
          slow) rests at his feet, spiral shell, eye stalks up.
    1.00  a breath of air sways the sprout .. 1.27 a dark grain slips through the neck and runs down the
          stream (110 ms a cell) .. 1.60 it lands: it becomes the mound's new top .. 2.00 blink
 B  2.53  tap .. tap with his right foot (impatient) .. 2.98 another grain .. 3.20 it lands as he stares
    3.35  he looks back at us: a sigh-length still hold (1.5 s) .. 4.98 a grain .. 5.20 it lands
 C  4.85  gaze drops .. 5.25 lids close: DOZING (both arms stay at his sides, behind the lid ends)
    5.45  the sprout wilts (a beat later) .. 5.75 a z drifts up-right one cell every 460 ms, growing
          small, medium, medium .. 7.13 big
 D  7.13  the LAST GRAIN slips through the neck .. 7.23 it lands: the top is empty and the glass goes
          "tink" (a glassy white/cyan twinkle beside the neck: dot, plus, dot)
    7.41  his eyes pop open (still slumped) and the big z bursts like a bubble (plus, then x)
    7.52  JOLT: a held hop, legs tucked, arms flung out; the sprout drags flat at take-off, catches up
          tall at the apex; a coffee drop jumps straight up out of the mug
    7.75  lands: the sprout squashes flat, the mug lags in the air .. 7.84 overshoot: arms down, the mug
          dips, the sprout rebounds tall .. 7.94 the falling drop lands IN the coffee (a ripple) while he
          glances left ("did anyone see that?") .. 8.24 eyes right: oh. It ran out.
 E  8.69  wind-up: arm down, he sizes up the glass (eyes down-right)
    8.82  the claw presses the top bulb's rim (contact), eyes up as it starts to rise
    8.91  the hourglass turns over clockwise on an eased arc (45 / 90 / 135 degrees at 8.91 / 9.00 / 9.13,
          lift 3 / 5 / 3, the 90-degree apex held longest); the arm follows through, his eyes follow the
          glass up, over and down, the sprout leans in its wind
    9.24  touchdown: a little dust; the first grain slips through the neck and the stream GROWS behind it,
          one cell per beat with the grain as its tip (9.24 / 9.33 / 9.43 / 9.53), his eyes follow it
          down; a gold twinkle on the cap (dot, plus, x)
 F 10.60  back to us .. 10.85 the mug comes up in two steps as he tips his head back (eyes up): a long
          sip .. 11.60 a sand stage drops .. 11.78 blink ("ahh") .. 11.91 back down in two steps
 G 12.01  calm, eyes on us .. 13.67 a grain runs down and lands on the seam .. 14.00 = 0.00 his eyes go
          back to the sand (frame 0)
Sand stages: full at the touchdown (9.24, its stream grown by 9.64), 11.60, 0.00 (on the seam), 1.60, 3.20,
5.20, the last grain 7.13, empty 7.23. The grains (their own synced layer, cut from the same schedule) land
on the stage changes while he watches (1.60 / 3.20 / 5.20) and on the seam, each becoming that stage's new
sand, so the glass visibly runs through the whole 5 s watch.
Independent ambient layers on co-prime loops, so consecutive 14 s loops never look the same:
  steam 1.31 s (an uneven 190-260 ms puff rhythm), and the SNAIL 29.3 s (its spiral shell is a static
  layer): after a long rest it stretches forward to inch along (rate limited: the shell stays put), gives
  up and pulls into its shell (half, gone), then peeks back out (an eye, half, out), each pass on a
  different beat of his story.
Plain face only (open / blink / look_* / closed while dozing), normal body size: STYLE.md section 0. His
eyes (black ink, drawn by the kit) never sit on his silhouette edge: look_r / look_dr / look_ur only while
that arm backs the edge cell, and the doze keeps both arms at his sides so the lid ends stay inside him.
Layout: the mug rides one row higher in his hand (MUG_LIFT) so a clear row separates it from the snail's
eye stalks; the snail's shell keeps the 1-cell canvas margin. A full-loop two-theme edge pass (every
moment of the 14 s loop and of the snail's 29.3 s loop) finds no vanishing edge pixel.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'rate-limit'
STATE = 'Rate limited: waiting before Claude can continue'
DESC = ('Waits beside a big hourglass with a steaming mug, a sprout on his head and a snail at his feet: '
        'watches the sand run, taps his foot, dozes off, jolts awake when the last grain drops, flips the '
        'hourglass over and settles back with a sip.')


def _item(name, fallback):
    try:
        return get(name)
    except KeyError:                          # library mid-save: same look, local copy
        return fallback


def _S(rows, anchor, name):
    return Sprite(rows, anchor=anchor, name=name)


# =====================================================================================================
# Local sprites
# =====================================================================================================
# The library mug, mirrored for his LEFT hand and re-lit from the top-left (same mug as 'working'). The
# grip is the handle's right end; MUG_LIFT raises it one row in his hand so a clear row stays between
# the mug and the snail below.
_MUG = _S([
    'cddB..',
    'cbbBbb',
    'cbbB.b',
    'cbbBbb',
], (5, 2), 'mug_l')
MUG_LIFT = -1

# Hourglass 7 x 11: wooden caps lit from the top-left, cyan glass rims around an ice interior.
_HG = [
    '.ttttt.',
    'tTTTTTT',
    'cCCCCCc',
    '.cCCCc.',
    '..cCc..',
    '...c...',
    '..cCc..',
    '.cCCCc.',
    'cCCCCCc',
    'tTTTTTT',
    '.TTTTT.',
]
HG_X0, HG_Y0 = 22, 9                 # top-left of the upright hourglass (it stands on row 19)
HG_CX, HG_CY = HG_X0 + 3, HG_Y0 + 5  # its centre: the neck
_NECK = (3, 5)

# Sand lives in the glass interior (the cyan rims always show). It moves in symmetric groups:
# the top drains from the middle of its surface (a funnel) while the bottom grows as a mound.
_DRAIN = [[(3, 2)], [(2, 2), (4, 2)], [(3, 3)], [(1, 2), (5, 2)], [(2, 3), (4, 3)], [(3, 4)]]
_FILL = [[(3, 8)], [(2, 8), (4, 8)], [(3, 7)], [(1, 8), (5, 8)], [(2, 7), (4, 7)], [(3, 6)]]
STAGES = len(_DRAIN)                 # stage 0 = top full ... stage STAGES = top empty
# When each middle stage begins (ms in the loop). Stage 0 (the touchdown after the flip, 'land' = its
# stream still hidden while the first grain grows it), the last grain and STAGES (empty) are taken from
# the timeline, so retiming can never desync them. Stage 2 begins on the loop seam (so the layer needs no
# extra frame for it) and frame 0 shows it.
_SAND_AT = {1: 11600, 2: 0, 3: 1600, 4: 3200, 5: 5200}
_GRAIN = 'J'                         # a dark grain running down the stream
_STEP = 110                          # ms per cell for a running grain

# Grain slides: (start ms, cells to run down the stream). Each one ends on a stage change, so the grain
# lands as that stage's new sand; the stage it runs in comes from the sand schedule (_grain_layer checks
# that the stream exists there and is long enough).
_SLIDES = [
    (1600 - 3 * _STEP, 3),           # -> stage 3 (the calm watch)
    (3200 - 2 * _STEP, 2),           # -> stage 4 (while he stares)
    (5200 - 2 * _STEP, 2),           # -> stage 5 (as his gaze drops)
    (14000 - 3 * _STEP, 3),          # -> stage 2, landing on the loop seam
]


def _sand_set(stage):
    return {c for g in _DRAIN[stage:] for c in g} | {c for g in _FILL[:stage] for c in g}


def _stream_cells(stage):
    """Local cells of the stream at a stage: the neck, then down to the mound top (none when empty)."""
    if stage >= STAGES:
        return []
    sand = _sand_set(stage)
    out, y = [_NECK], _NECK[1] + 1
    while y <= 8 and (3, y) not in sand:
        out.append((3, y))
        y += 1
    return out


def _bead(i, stage):
    return 'j' if (i + stage) % 2 == 0 else 'y'      # the stream's light/dark beads shift each stage


def _sand_cells(stage, stream=True, last=False):
    """{(x, y): ch} local sand cells. stream=False hides the stream (the first grain grows it).
    last = the last grain sits in the neck (the top bulb has just run empty)."""
    sand = _sand_set(STAGES - 1) - {(3, 4)} if last else _sand_set(stage)
    out = {}
    for (x, y) in sand:
        lit = (x, y - 1) not in sand and x <= 3          # light from the top-left
        out[(x, y)] = 'y' if lit else 'j'
    if last:
        out[_NECK] = 'j'
        return out
    if stream:
        for i, c in enumerate(_stream_cells(stage)):
            out[c] = _bead(i, stage)
    return out


# Spin frames, hand-drawn (the sand rides in the bulb that was at the bottom). At 45 degrees each bulb is
# a right triangle whose rims are the axis-aligned legs and whose cap is the diagonal. Centre cell = neck.
_SPIN = {
    45: [
        '.....Tt....',
        '.....cTt...',
        '.....cCTt..',
        '.....cCCTt.',
        '.....cCCCTt',
        'TcccccccccT',
        'tTyyjc.....',
        '.tTjjc.....',
        '..tTjc.....',
        '...tTc.....',
        '....tT.....',
    ],
    90: [
        '.tc.....ct.',
        'tTyc...cCTT',
        'tTjyc.cCCTT',
        'tTjjycCCCTT',
        'tTjjc.cCCTT',
        'tTjc...cCTT',
        '.Tc.....cT.',
    ],
    135: [
        '....tT.....',
        '...tTc.....',
        '..tTyc.....',
        '.tTyjc.....',
        'tTjjjc.....',
        'TcccccccccT',
        '.....cCCCTT',
        '.....cCCTT.',
        '.....cCTT..',
        '.....cTT...',
        '.....TT....',
    ],
}

# Landing dust for the hourglass: tiny puffs in the gaps beside its base (clear of his foot and the cap).
_HG_DUST = [
    {(21, 19): 't', (29, 19): 't'},
    {(21, 19): 'T', (30, 18): 't'},
]

# The coffee drop that jumps out of the mug when he jolts awake (absolute cells per beat). It leaves the
# coffee's left cell (x 4 while his arm is flung out, clear of the steam column), hangs at the top in the
# held beat, falls faster and faster (1, 2, 3 rows a beat) and drifts right with the mug coming back, so it
# lands IN the coffee: a one-beat ripple on the coffee's surface.
_SPLASH = [
    {(4, 8): 'T'},
    {(4, 6): 'T'},
    {(4, 7): 'T'},
    {(5, 9): 'T'},
]
_RIPPLE = {(5, 12): 'T'}

# The doze z: (item, x, y) per step, one cell up-right each step, growing as it rises, clear of the cap.
_Z = [('z_small', 19, 7), ('z_medium', 20, 6), ('z_medium', 21, 5), ('z_big', 22, 4)]
_ZZ = {
    'z_small': _item('z_small', Item('z_small', 'fx', 'local fallback', [
        _S(['lllv', '..lv', '.lv.', 'lllv'], (2, 2), 'z_small')])),
    'z_medium': _item('z_medium', Item('z_medium', 'fx', 'local fallback', [
        _S(['llllv', '...lv', '..lv.', '.lv..', 'llllv'], (2, 2), 'z_medium')])),
    'z_big': _item('z_big', Item('z_big', 'fx', 'local fallback', [
        _S(['lllllv', '....lv', '...lv.', '..lv..', '.lv...', 'lllllv'], (3, 3), 'z_big')])),
}
# When his eyes pop open the big z bursts like a bubble: a thin lavender plus, then a small x.
_ZPOP = [
    _S(['..l..', '.....', 'l.v.l', '.....', '..l..'], (2, 2), 'z_pop0'),
    _S(['l.l', '...', 'l.l'], (1, 1), 'z_pop1'),
]
_ZPOP_AT = (21, 3)

# Glints. The "tink" is glassy (white core, cyan arms) and sits just right of the neck, outside the
# glass, so it can never read as sand; the "ta-da" on the cap's corner after the flip is gold.
_SPARK = _item('sparkle_small', Item('sparkle_small', 'fx', 'local fallback', [
    _S(['j'], (0, 0), 'sparkle_small'),
    _S(['.j.', 'jyj', '.j.'], (1, 1), 'sparkle_small'),
    _S(['j.j', '.j.', 'j.j'], (1, 1), 'sparkle_small'),
]))
_TINK = (29, 13)
_TADA = (29, 9)

# The sprout on his head (the library 'sprout' plus local poses), anchored on his head-top pixel. It lives
# his moods: sways in a breath of air, wilts as he dozes, drags flat when he jolts up and springs tall at
# the apex, squashes on the landing and rebounds, and leans away from the wind of the turning hourglass.
_SPROUT = {
    'calm': _S(['ag.ga', '.gGg.', '..G..', '..G..'], (2, 3), 'sprout'),
    'sway': _S(['ag.ga', '.gGg.', '.G...', '.G...'], (1, 3), 'sprout_r'),
    'lean': _S(['ag.ga', '.gGg.', '...G.', '...G.'], (3, 3), 'sprout_l'),
    'wilt': _S(['.gGg.', 'a.G.a', '..G..'], (2, 2), 'sprout_wilt'),
    'flat': _S(['agGga', '..G..'], (2, 1), 'sprout_flat'),
    'tall': _S(['a...a', '.g.g.', '..G..', '..G..', '..G..'], (2, 4), 'sprout_tall'),
}
_SPROUT_LIB = _item('sprout', None)
if _SPROUT_LIB is not None and len(_SPROUT_LIB) >= 4:   # the library look wins for the poses it has
    _SPROUT['calm'] = _SPROUT_LIB.sprite(0)              # rest
    _SPROUT['sway'] = _SPROUT_LIB.sprite(1)              # leaning right
    _SPROUT['lean'] = _SPROUT_LIB.sprite(3)              # leaning left, away from the hourglass

# The snail (rate limit = slow) at his feet, left of and below the mug. Its round shell is lit from the
# top-left and carries a dark curl wrapped round a pale centre (the spiral, after the library
# snail_shell); it is a static layer, the snail never gets anywhere. The shell keeps the 1-cell canvas
# margin and touches the mug's corner only diagonally. The soft pink body runs out along the input box
# from under the shell's front, with two eye stalks (pink stalk, dark eye) that clear the mug by a row.
# Body poses act on their own 29.3 s loop: out (frame 0), reach (stretches one cell forward), half (half
# the foot, one stalk), hide, peek (one eye at the shell's mouth).
_SNAIL_SHELL = [            # x 1..4, rows 16..19
    '.tT.',
    'tddT',
    'TdYT',
    '.TT.',
]
_SNAIL_X0, _SNAIL_Y0 = 1, 16
_SNAIL_BODY = {             # x 4..10, rows 17..19: '+' body, '*' eye (stalks lean forward, toward him)
    'out':   ['..*.*..',
              '.+.+...',
              '++++...'],
    'reach': ['...*.*.',
              '..+.+..',
              '++++++.'],
    'half':  ['..*....',
              '.+.....',
              '+++....'],
    'peek':  ['.......',
              '.*.....',
              '++.....'],
    'hide':  ['.......',
              '.......',
              '.......'],
}
_SNAIL_INK = {'+': 'p', '*': 'n'}
SNAIL_LOOP = 29300
_SNAIL_SCRIPT = [(21400, 'out'),           # frame 0: resting, eye stalks up
                 (1900, 'reach'),          # it stretches to inch forward ... the shell stays put
                 (150, 'half'),            # ... gives up and pulls into its shell ...
                 (3900, 'hide'),
                 (1300, 'peek'),           # ... one eye peeks out ...
                 (650, 'half')]            # ... half out (then frame 0 again)


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


# =====================================================================================================
# Master timeline
# =====================================================================================================
class _TL:
    ONE_SHOT = ('splash', 'ripple', 'dust', 'tink', 'tada', 'sand', 'growth', 'zpop')

    def __init__(self):
        self.segs = []
        self.st = dict(eyes='look_r', larm='side', rarm='side', legs='stand', tap=False, dy=0, mug_dy=0,
                       sprout='calm', hg=('up', 0), z=None, zpop=None, splash=None, ripple=None, dust=None,
                       tink=None, tada=None, sand=None, growth=None)

    def add(self, ms, **kw):
        self.st.update(kw)
        self.segs.append((ms, dict(self.st)))
        for k in self.ONE_SHOT:               # one-shot effects only live for the beat they are given in
            self.st[k] = None


LOOP_MS = 14000


def _timeline():
    t = _TL()
    # A  frame 0: watching the sand
    t.add(1000)
    t.add(550, sprout='sway')                  # a breath of air
    t.add(450, sprout='calm')
    t.add(130, eyes='blink')
    t.add(400, eyes='look_r')
    # B  impatient: tap .. tap, then back to us with a sigh-length hold
    t.add(110, tap=True)
    t.add(150, tap=False)
    t.add(110, tap=True)
    t.add(450, tap=False)                      # 3.20: a stage drops while he stares
    t.add(1500, eyes='open')
    # C  dozing off: both arms stay at his sides (the kit's lid ends need an arm behind them)
    t.add(400, eyes='look_d')
    t.add(200, eyes='closed')
    t.add(300, sprout='wilt')                  # the sprout wilts a beat after the lids close
    t.add(460, z=0)
    t.add(460, z=1)
    t.add(460, z=2)
    # D  the last grain .. tink .. JOLT
    t.add(100, sand='last', z=3)               # the z has grown big
    t.add(60, sand='empty', tink=0)            # it lands: the glass goes "tink" ...
    t.add(120, tink=1)
    t.add(110, eyes='open', tink=0, z=None, zpop=0)   # ... his eyes pop open first; the z bursts
    t.add(90, dy=-1, legs='short', larm='out', rarm='out', sprout='flat', splash=0, zpop=1)   # take-off
    t.add(140, sprout='tall', splash=1)        # held in the air: the sprout catches up, overshoots tall
    t.add(90, dy=0, legs='stand', sprout='flat', mug_dy=-1, splash=2)   # lands: squash; the mug lags
    t.add(100, larm='down', rarm='down', mug_dy=0, sprout='tall', splash=3)   # overshoot: the mug dips
    t.add(120, larm='side', rarm='side', eyes='look_l', sprout='calm', ripple=1)   # the drop lands in it
    t.add(180)                                 # did anyone see that?
    t.add(450, eyes='look_r')                  # ... oh. It ran out.
    # E  flip the hourglass
    t.add(130, rarm='down', eyes='look_dr')    # wind-up: he sizes it up (the down arm backs the eye)
    t.add(90, rarm='wave', eyes='look_u')      # contact: the claw presses the top bulb's rim
    t.add(90, hg=('spin', 45, 3), rarm='raise')
    t.add(130, hg=('spin', 90, 5), rarm='up', eyes='look_ur', sprout='lean')
    t.add(110, hg=('spin', 135, 3), rarm='side', eyes='look_r')
    t.add(90, hg=('up', 0), sand='land', growth=0, dust=0, sprout='calm')    # touchdown
    t.add(100, dust=1, tada=0, growth=1, eyes='look_dr')   # the first grain runs down, the stream behind it
    t.add(100, tada=1, growth=2)               # ... his eyes follow it down
    t.add(110, tada=2, growth=3)
    t.add(100, sand='grown')                   # the stream is whole
    t.add(860)
    # F  coffee
    t.add(250, eyes='open')
    t.add(100, larm='up', mug_dy=1, eyes='look_u')   # the mug comes up as he tips his head back
    t.add(120, mug_dy=0)
    t.add(710)                                 # a long sip
    t.add(130, eyes='blink')                   # "ahh"
    t.add(100, eyes='open', larm='side', mug_dy=-1)
    # G  calm, eyes on us; frame 0 turns them back to the sand
    used = sum(ms for ms, _ in t.segs)
    t.add(LOOP_MS - used, mug_dy=0)
    return t


def _sand_schedule(segs):
    """[(t, stage)] sorted by time. 'land' = stage 0 with its stream still hidden, 0 = stage 0 with the
    stream grown, 'last' = the last grain in the neck, STAGES = empty."""
    sched, t = dict(_SAND_AT), 0
    for ms, s in segs:
        if s['sand'] == 'land':
            sched['land'] = t
        elif s['sand'] == 'grown':
            sched[0] = t
        elif s['sand'] == 'last':
            sched['last'] = t
        elif s['sand'] == 'empty':
            sched[STAGES] = t
        t += ms
    return sorted(((v, k) for k, v in sched.items()), key=lambda vk: vk[0])   # by time only


def _split(segs, cuts):
    """Cut the beat list at extra times (each piece keeps its beat's state)."""
    out, t = [], 0
    for ms, s in segs:
        inner = sorted(c for c in cuts if t < c < t + ms)
        edges = [t] + inner + [t + ms]
        for a, b in zip(edges, edges[1:]):
            out.append((b - a, s, a))
        t += ms
    return out


def _stage_at(sched, t):
    stage = sched[-1][1]                               # before the first change: the loop's last stage
    for tt, k in sched:
        if tt <= t:
            stage = k
    return stage


# =====================================================================================================
# Layer renderers
# =====================================================================================================
def _pose(s):
    p = clawd(eyes=s['eyes'], larm=s['larm'], rarm=s['rarm'], legs=s['legs'])
    if s['tap']:
        g = GEOM['normal']
        foot = (9, g['ly'] + g['ll'] - 1)            # lift his right foot one cell
        cells = [c for c in p.sprite.cells if (c[0], c[1]) != foot]
        p = Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec, tap=True))
    return p


def _body(s):
    f = Frame()
    put_clawd(f, _pose(s), HOME[0], HOME[1] + s['dy'])
    return f


def _sprout(s):
    f = Frame()
    x, y = _pose(s).at('head', HOME[0], HOME[1] + s['dy'])
    f.place(_SPROUT[s['sprout']], x, y)
    return f


def _mug(s):
    f = Frame()
    x, y = _pose(s).at('hand_l', HOME[0], HOME[1] + s['dy'])
    f.place(_MUG, x, y + MUG_LIFT + s['mug_dy'])
    return f


def _glass(s):
    f = Frame()
    kind = s['hg'][0]
    if kind == 'up':
        _paint(f, _HG, HG_X0, HG_Y0)
    else:
        rows = _SPIN[s['hg'][1]]
        _paint(f, rows, HG_CX - len(rows[0]) // 2, HG_CY - s['hg'][2] - len(rows) // 2)
    return f


def _sand(s, stage):
    f = Frame()
    if s['hg'][0] != 'up':
        return f
    if stage == 'last':
        cells = _sand_cells(STAGES, last=True)
    elif stage == 'land':
        cells = _sand_cells(0, stream=False)
    else:
        cells = _sand_cells(stage)
    for (x, y), ch in cells.items():
        f.put(HG_X0 + x, HG_Y0 + y, ch)
    return f


def _fx(s):
    f = Frame()
    if s['z'] is not None:
        name, x, y = _Z[s['z']]
        f.place(_ZZ[name].sprite(), x, y)
    if s['zpop'] is not None:
        f.place(_ZPOP[s['zpop']], *_ZPOP_AT)
    if s['tink'] is not None:
        f.place(_SPARK.sprite(s['tink']).recolor({'y': 'W', 'j': 'c'}), *_TINK)
    if s['tada'] is not None:
        f.place(_SPARK.sprite(s['tada']), *_TADA)
    if s['growth'] is not None:                        # the first grain, the stream growing behind it
        path = _stream_cells(0)
        for i in range(s['growth']):
            x, y = path[i]
            f.put(HG_X0 + x, HG_Y0 + y, _bead(i, 0))
        x, y = path[s['growth']]
        f.put(HG_X0 + x, HG_Y0 + y, _GRAIN)
    if s['splash'] is not None:
        for (x, y), ch in _SPLASH[s['splash']].items():
            f.put(x, y, ch)
    if s['ripple'] is not None:
        for (x, y), ch in _RIPPLE.items():
            f.put(x, y, ch)
    if s['dust'] is not None:
        for (x, y), ch in _HG_DUST[s['dust']].items():
            f.put(x, y, ch)
    return f


def _grain_layer(sched):
    """The running grains: one dark cell stepping down the stream (synced: same 14 s loop as the sand)."""
    events = []
    for t0, n in _SLIDES:
        stage = _stage_at(sched, t0)
        assert isinstance(stage, int) and stage < STAGES, 'grain slide at %d: no stream (%r)' % (t0, stage)
        path = _stream_cells(stage)
        assert n <= len(path), 'grain slide at %d: stream has %d cells' % (t0, len(path))
        assert _stage_at(sched, t0 + n * _STEP - 1) == stage, 'grain slide at %d crosses a stage' % t0
        for i, c in enumerate(path[:n]):
            events.append((t0 + i * _STEP, c))
    events.sort()
    out, t = [], 0
    for i, (t0, c) in enumerate(events):
        if t0 > t:
            out.append((Frame(), t0 - t))
        end = min(t0 + _STEP, events[i + 1][0]) if i + 1 < len(events) else t0 + _STEP
        f = Frame()
        f.put(HG_X0 + c[0], HG_Y0 + c[1], _GRAIN)
        out.append((f, end - t0))
        t = end
    if t < LOOP_MS:
        out.append((Frame(), LOOP_MS - t))
    assert sum(ms for _, ms in out) == LOOP_MS
    return layer('grain', out)


def _snail_layers():
    shell = Frame()
    _paint(shell, _SNAIL_SHELL, _SNAIL_X0, _SNAIL_Y0)
    body = []
    for ms, pose in _SNAIL_SCRIPT:
        f = Frame()
        for j, r in enumerate(_SNAIL_BODY[pose]):
            for i, ch in enumerate(r):
                if ch in _SNAIL_INK:
                    f.put(4 + i, 17 + j, _SNAIL_INK[ch])
        body.append((f, ms))
    assert sum(ms for _, ms in body) == SNAIL_LOOP
    return [layer('snail', body), static('snail_shell', shell)]


_STEAM_MS = [190, 230, 190, 260, 210, 230]       # an uneven puff rhythm (1.31 s) that drifts against 14 s
_STEAM_FALLBACK = Item('steam', 'fx', 'local fallback', [
    _S(['.m', 'm.', 'm.', '.m', '.m'], (1, 2), 'steam'),
])


def _steam_layer():
    st = _item('steam', _STEAM_FALLBACK)
    out = []
    for i, ms in enumerate(_STEAM_MS):
        f = Frame()
        f.place(st.sprite(i), 6, 11 + MUG_LIFT)   # its bottom cell hides under the coffee: the wisp leaves the rim
        out.append((f, ms))
    return layer('steam', out)


def build():
    t = _timeline()
    assert sum(ms for ms, _ in t.segs) == LOOP_MS
    sched = _sand_schedule(t.segs)
    body, sprout, mug, glass, sand, fx = [], [], [], [], [], []
    for ms, s, t0 in _split(t.segs, [tt for tt, _ in sched]):
        stage = _stage_at(sched, t0)
        body.append((_body(s), ms))
        sprout.append((_sprout(s), ms))
        mug.append((_mug(s), ms))
        glass.append((_glass(s), ms))
        sand.append((_sand(s, stage), ms))
        fx.append((_fx(s), ms))
    return anim(NAME, DESC, _snail_layers() + [
        _steam_layer(),
        layer('glass', glass),
        layer('sand', sand),
        _grain_layer(sched),
        layer('body', body),
        layer('sprout', sprout),
        layer('mug', mug),
        layer('fx', fx),
    ], state=STATE)
