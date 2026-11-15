"""manual-craft - Default (manual) permission mode, variant: handmade work.

Clawd in his cozy little workshop, brass goggles pushed up on his forehead and a small denim carpenter's
apron: he saws a plank at his workbench with slow, lazy strokes, waves hello, finishes the cut, sands the
piece in a cloud of wood dust that settles to reveal a little wooden heart, proudly shows it to you, tucks
it into his apron pocket and beckons the next board over.

STORYBOARD (ms; ONE master beat list drives every synced layer, so nothing can drift; loop 12 000 ms)
     0  A  SAW. Frame 0 at HOME: pull stroke, the red-handled saw in the cut, eyes on the cut (look_d), a
           crumb of sawdust falling out of the kerf through the air gap between bench and bin. Lazy strokes
           with long, uneven holds (pull 460 / push 430 / pull 400): each push pokes the blade tip out
           under the plank, each pull drops a crumb (110 + 110) onto the little heap.
  1730     a breather: he looks up at you (160) .. and waves, "hi" (raise 240 / wave 130 / raise 130 /
           wave 130 / raise 320) .. lowers the hand (300) .. blink (130), inside the still saw pose.
  3270     back to the cut: the last push goes THROUGH (440).
  3710  B  The cut is through, so the saw drops one cell through it while the off-cut tips into the bin
           (110); he lowers it behind the bench (130) and brings the green sanding block up (130).
           (Every saw move is <= 1 cell or slides along the blade, so no frame pops.)
  4080  C  SAND: four easy strokes (310 / 300 / 320 / 300); specks kick up, the wood dust builds into a cloud.
  5310  D  The dust settles: a little WOODEN HEART stands on the bench, a twinkle on its shoulder (sparkle
           frame 1, then 0) and the last dust in two small puffs at its feet (120 / 110) .. blink .. he looks
           at what he made (900).
  6560  E  SHOW: he takes it (130), lifts it (110 / 80), it overshoots a cell as the other hand flies up:
           ta-da (90). The wood glints (110 / 100) .. proud hold (1000) .. blink.
  8310  F  POCKET: the heart floats on an eased arc over his shoulder into the apron pocket, 1-2 cells per
           step, small steps at both ends (120 100 90 90 100 110 140) .. hand on the pocket, a content look
           at you (400) .. blink.
  9590  G  NEXT BOARD: he looks at the bin (300) and beckons once .. a board peeks out (180), stands up
           (300), leans .. and topples onto the bench, faster and faster (120/90/70): thunk, two little dust
           mounds (120), it slides into place (300).
 11370  H  He reaches behind the bench for the saw (130), brings it up (100) and sets it in: first push
           (400) .. = frame 0.
Holds of 300 ms or more fill about 60 % of the loop (the saw holds stay in 400-700 ms); no chain of quick
frames runs longer than ~0.9 s.
Ambient: steam curls from the mug on the lumber pile (6 frames, 1151 ms) and a moth naps on the lamp shade,
then flutters an uneven loop around the warm bulb once per 17 293 ms. Both lengths are prime, so the
ambient layers drift against the 12 s story and the scene never repeats exactly.

Layers (back to front): scene (lamp, standing boards, the bin's inner back wall, bench, sawdust heap, lumber
pile, mug) | work (plank, pieces, heart on the bench, the hopping board, the saw blade while it is in the
cut, thunk dust) | bin (front) | body (static: Clawd without arms, every eye hole the loop uses punched) |
goggles | pose (the eyelids that fill the unused eye holes + his left arm) | hand (right arm, saw, sanding
block, the heart he holds, sanding dust) | apron (in front: the heart sinks into its pocket) | fx (sawdust
crumbs, the reveal twinkle and puffs, glint) | steam | moth.
Composites are always exact kit poses: pose = (pose without right arm) - static body, hand = full pose -
(pose without right arm). In the cut the saw slides along its own 45 deg axis, so the pull pose's blade is
drawn once behind the plank (work layer) and a stroke only moves the red handle (+ the one blade cell and
the tip the push adds). Elsewhere the whole saw is drawn in the hand layer, hidden wherever plank, bench or
bin front are in front of it. No library item is edited (local recolors only).
Plain face only (open / blink / look_d / look_r; look_r only with a right arm that frames its eye),
normal body size (STYLE.md section 0). The apron's band stays between his eyes' columns (x 13-17), so the
look_d eye holes always sit in orange and never read as notches in a belt.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'manual-craft'
STATE = 'Default (manual) permission mode, variant: handmade work'
DESC = ('Handmade work: Clawd saws a plank at his little workbench, waves hello, sands the piece in a cloud of '
        'wood dust into a wooden heart, proudly shows it to you, tucks it into his apron pocket and beckons '
        'the next board over.')

# =====================================================================================================
# Library items (local recolors only)
# =====================================================================================================
_GOGGLES = get('goggles_up').sprite(0).recolor({'W': 'c'})   # solid lenses: no second pair of "eyes"
_SPARK = get('sparkle')
_GLINT = get('sparkle_small')
_STEAM = get('steam')
_MUG = get('mug').sprite(0).recolor({'b': 'B', 'c': 'b'})    # navy: echoes the apron, sits back


def _S(rows, anchor=(0, 0)):
    return Sprite(rows, anchor=anchor)


# =====================================================================================================
# Local sprites
# =====================================================================================================
# Hand saw, 45 deg: red pistol-grip handle (a hole in the middle), steel blade with a bright spine.
# Anchor = the grip (bottom-left of the handle).
_SAW = _S([
    '.rr......',
    'r.rm.....',
    'rrrsm....',
    '..sssm...',
    '....ssm..',
    '....sssm.',
    '......sm.',
    '......ss.',
], (0, 2))

# Sanding block: green block over rust sandpaper. Anchor = top-left (the grip side).
_BLOCK = _S(['ggg', 'OOO'])

# The wooden heart he makes: lit top-left, shadow bottom-right. Anchor = top-left.
_WHEART = _S([
    '.t.t.',
    'ttttT',
    'ttttT',
    '.tTT.',
    '..T..',
])

# Wood dust: a light core with a tan rim, so it never fuses with the (tan) wood and reads on both themes.
_DUST_S = _S(['.t.', 'twt'])
_CLOUD_M = _S(['.tt.', 'twwt', '.tt.'])
_CLOUD_L = _S(['.tt.t.', 'twwtwt', 'twwwwt', 'twwwwt', '.tttt.'])
# The last of the dust settles at the heart's feet (anchor = top-left; 'w' only inside, next to the wood).
_SETTLE_L = _S(['tw', 'tt'])
_SETTLE_R = _S(['.t', 'wt'])
# Thunk: little dust mounds kicked up along the board as it lands (anchor = top-left; the 'w' core rests
# on the board, so it never touches the background).
_THUNK = _S(['.t.', 'twt'])

# A little moth (ambient). Resting: wings folded into a tent on the lamp shade's shoulder.
# Flying: wings up / wings down, anchor = its body.
_MOTH_REST = _S(['m.', 'Nm'], (0, 1))
_MOTH_UP = _S(['m.m', '.N.'], (1, 1))
_MOTH_DN = _S(['.N.', 'm.m'], (1, 0))

# Scene: workbench (x 21-25), air gap (x 26), lumber bin (x 27-30) with boards leaning behind it, lumber pile
# + mug on the left, pendant lamp. The bench legs are wood (they read on dark), the rail between them shade.
_BENCH = [
    'TTTTT',
    'TdddT',
    'T...T',
]
_BENCH_X, _BENCH_Y = 21, 17
_BIN_X = 27
_BIN_BACK = 'GGGG'        # row 16: the bin's inner back wall (behind the plank); it hides the boards' feet
_BIN_FRONT = [            # rows 17-19: a painted bin, warm green, so the saw blade is the only gray here
    'gggg',
    'GGGG',
    'GGGG',
]
_LUMBER = [
    '.ttttttT',
    'TTTTTTT.',
    '.tttttT.',
]
_LUMBER_X, _LUMBER_Y = 1, 17
_MUG_AT = (1, 15)          # the mug on the lumber pile (its anchor row = its bottom row 16)
_STEAM_AT = (4, 10)        # 3 rows above the coffee
_LAMP = [
    '..n..',
    '..n..',
    '..n..',
    '.OOO.',
    'OoooO',
    '.jyj.',
]
_LAMP_X, _LAMP_Y = 22, 0
_MOTH_HOME = (26, 3)      # on the shade's right shoulder

_PY = 16                  # the plank lies on the bench top (row 17) ..
_PX0, _PX1 = 22, 28       # .. from x 22 across the air gap onto the bin's rim
_GAP = 26                 # the kerf is right over the gap, so sawdust and the blade tip fall through air
_HOP_X = 27               # the next board hops out of the bin here and topples onto the bench
_POCKET_Y = 16            # the apron's band: things that go into the pocket vanish below it
_HEART_BENCH = (22, 12)   # the finished heart stands on the bench (top-left cell)

# Eye holes the loop uses. The static body has all of them punched; the pose layer fills the unused ones.
# look_r is only used with a right arm that frames (20, 14); look_dr is never used (it would notch him).
_EYES = {
    'open': [(12, 14), (18, 14)],
    'look_d': [(12, 15), (18, 15)],
    'look_r': [(13, 14), (19, 14)],
    'blink': [],
}


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


def _grip(rarm):
    """Where a held item's grip lands for this right-arm shape (Clawd never leaves HOME)."""
    return clawd(rarm=rarm).at('hand_r')


def _saw_cells(grip):
    gx, gy = grip
    return [(gx + sx - _SAW.ax, gy + sy - _SAW.ay, ch) for sx, sy, ch in _SAW.cells]


# While sawing, the saw slides along its own 45 deg axis between the pull ('up') and push ('out') grips.
# The pull blade lives in the work layer behind the plank; the push handle covers the cells it does not
# share, and the push only adds what the pull blade lacks (one blade cell + the tip in the air gap).
_PULL_ALL = _saw_cells(_grip('up'))
_PUSH_ALL = _saw_cells(_grip('out'))
_BLADE = [(x, y, ch) for x, y, ch in _PULL_ALL if ch != 'r']
_HANDLE = {
    'up': [(x, y, ch) for x, y, ch in _PULL_ALL if ch == 'r'],
    'out': [(x, y, ch) for x, y, ch in _PUSH_ALL if ch == 'r'],
}
_PUSH_EXTRA = [(x, y, ch) for x, y, ch in _PUSH_ALL
               if ch != 'r' and (x, y) not in {(bx, by) for bx, by, _ in _BLADE}]

# the hopping board: its top end at each step, pivoting on its foot (27, 16) inside the bin:
# peeking out, standing, leaning, then ~20 / 45 / 80 deg as it topples onto the bench
_HOP = {'peek': (27, 14), 'up': (27, 10), 'lean': (26, 10), 20: (25, 11), 45: (23, 12), 80: (21, 15)}

# The heart's way into the pocket (top-left cells): an eased arc over his shoulder, small steps at both
# ends (slow out of the proud pose, slow in at the pocket), with the arm that carries it at each step.
_ARC = [
    ((20, 7), 'raise', 120),
    ((18, 7), 'high', 100),
    ((16, 8), 'high', 90),
    ((14, 10), 'chin', 90),
    ((13, 12), 'chin', 100),
    ((13, 13), 'chin', 110),
    ((13, 14), 'chin', 140),
]


# =====================================================================================================
# Master timeline
# =====================================================================================================
_ONCE = ('fx', 'hfx', 'wfx')


class _TL:
    def __init__(self, **st):
        self.segs = []
        self.st = dict(st)

    def add(self, ms, **kw):
        """kw changes the persistent state; fx / hfx / wfx (effects for the fx / hand / work layer) last
        one beat only."""
        once = {k: kw.pop(k) for k in _ONCE if k in kw}
        self.st.update(kw)
        s = dict(self.st)
        for k in _ONCE:
            s[k] = once.get(k, [])
        self.segs.append((int(ms), s))

    def pull(self, hold, **kw):
        """Pull stroke: the saw slides back up its axis and a crumb of sawdust falls out of the kerf through
        the air gap (110 ms per cell) onto the little heap; then the pose simply holds."""
        self.add(110, rarm='up', fx=[('crumb', _GAP, 17)], **kw)
        self.add(110, fx=[('crumb', _GAP, 18)])
        self.add(hold)

    def push(self, ms, **kw):
        """Push stroke: the saw slides one cell down its own axis, the blade tip shows under the plank."""
        self.add(ms, rarm='out', **kw)


def _timeline():
    t = _TL(eyes='look_d', larm='side', rarm='up', saw='cut', held=None, work='kerf')
    # ---- A  SAW (frame 0 = pull stroke, a crumb falling out of the cut). Lazy strokes, uneven holds.
    t.pull(460)
    t.push(430)
    t.pull(400)
    t.add(160, eyes='open')                        # a breather: he looks up at you ..
    t.add(240, larm='raise')                       # .. and waves, "hi"
    t.add(130, larm='wave')
    t.add(130, larm='raise')
    t.add(130, larm='wave')
    t.add(320, larm='raise')
    t.add(300, larm='side')
    t.add(130, eyes='blink')
    t.push(440, eyes='look_d', work='through')    # back to it: the last push goes through
    # ---- B  the saw drops through the cut, the off-cut tips into the bin; saw down, sanding block up
    t.add(110, saw=('at', 22, 15), work='tilt')
    t.add(130, rarm='down', saw=('at', 21, 16), work='blank')
    t.add(130, rarm='side', saw=None, held='block')
    # ---- C  SAND: four easy strokes, the dust builds into a cloud that swallows the piece
    t.add(310, rarm='out', hfx=[('speck', 25, 13)])
    t.add(300, rarm='point', hfx=[('speck', 21, 13), ('sprite', _DUST_S, 23, 12)])
    t.add(320, rarm='out', hfx=[('speck', 26, 13), ('sprite', _CLOUD_M, 22, 12)])
    t.add(300, rarm='side', held=None, hfx=[('sprite', _CLOUD_L, 21, 12)])
    # ---- D  the dust settles: a wooden heart
    t.add(120, work='heart', fx=[('spark', 1, 26, 11), ('sprite', _SETTLE_L, 21, 15),
                                 ('sprite', _SETTLE_R, 25, 15)])
    t.add(110, fx=[('spark', 0, 26, 11), ('speck', 21, 16), ('speck', _GAP, 17)])
    t.add(120, eyes='blink')
    t.add(900, eyes='look_r')                      # he looks at what he made
    # ---- E  SHOW
    t.add(130, rarm='out')                                         # takes it ..
    t.add(110, rarm='up', held=('heart', 21, 10, False), work='empty', eyes='open')   # .. lifts ..
    t.add(80, rarm='raise', held=('heart', 21, 8, False))
    t.add(90, held=('heart', 21, 7, False), larm='wave')                             # .. ta-da!
    t.add(110, held=('heart', 21, 8, False), fx=[('glint', 1, 26, 8)])
    t.add(100, fx=[('glint', 2, 26, 8)])
    t.add(1000)                                                    # proud hold
    t.add(130, eyes='blink')
    # ---- F  POCKET: an eased arc over his shoulder into the apron pocket
    for k, ((x, y), arm, ms) in enumerate(_ARC):
        kw = dict(rarm=arm, held=('heart', x, y, y >= 12))
        if k == 0:
            kw.update(eyes='look_d', larm='side')
        t.add(ms, **kw)
    t.add(400, held=None, eyes='open')             # in: hand on the pocket, a content look at you
    t.add(130, eyes='blink')
    # ---- G  NEXT BOARD: "come here" .. a board hops out of the bin and topples onto the bench
    t.add(300, rarm='side', eyes='look_r')
    t.add(180, rarm='point')
    t.add(180, rarm='up', work=('hop', 'peek'))
    t.add(300, rarm='side', work=('hop', 'up'))
    t.add(120, work=('hop', 'lean'))
    t.add(120, work=('hop', 20))                               # .. falls, faster and faster ..
    t.add(90, work=('hop', 45), eyes='look_d')
    t.add(70, work=('hop', 80))
    t.add(120, work=('slid', 21), wfx=[('sprite', _THUNK, 22, 14), ('sprite', _THUNK, 25, 14)])
    t.add(300, work='plank')                                   # thunk, it slides into place
    # ---- H  the saw comes back from behind the bench
    t.add(130, rarm='down', saw=('at', 21, 16))
    t.add(100, rarm='out', saw=('at', 22, 15))
    t.push(400, saw='cut', work='kerf')                        # first bite: frame 0 is the next pull
    return t


# =====================================================================================================
# Layer frames
# =====================================================================================================
def _plank(f, x0, x1, kerf=False):
    f.hline(x0, x1, _PY, 't')
    f.put(x1, _PY, 'T')
    if kerf:
        f.put(_GAP, _PY, 'd')


def _heart_at(f, x, y, ymax=GROUND + 1):
    """Wooden heart with its top-left cell at (x, y); rows >= ymax are hidden (it sinks into the pocket)."""
    for sx, sy, ch in _WHEART.cells:
        if y + sy < ymax:
            f.put(x + sx, y + sy, ch)


def _pieces(s):
    """The work layer without the saw blade: plank / pieces / heart / hopping board (= the saw's occluders)."""
    f = Frame()
    w = s['work']
    if w == 'kerf':
        _plank(f, _PX0, _PX1, kerf=True)
    elif w == 'plank':
        _plank(f, _PX0, _PX1)
    elif w == 'through':                  # cut through: the off-cut still lies on the bin's rim
        _plank(f, _PX0, _GAP - 1)
        _plank(f, _GAP + 1, _PX1)
    elif w == 'tilt':                     # .. it tips into the bin, its end the last to go
        _plank(f, _PX0, _GAP - 1)
        f.put(_PX1, _PY, 'T')
    elif w == 'blank':
        _plank(f, _PX0, _GAP - 1)
    elif w == 'heart':
        _heart_at(f, *_HEART_BENCH)
    elif isinstance(w, tuple) and w[0] == 'hop':
        tx, ty = _HOP[w[1]]
        f.line(_HOP_X, _PY, tx, ty, 't')
    elif isinstance(w, tuple) and w[0] == 'slid':
        _plank(f, w[1], w[1] + (_PX1 - _PX0))
    return f


def _work(s):
    f = Frame()
    if s['saw'] == 'cut':
        for x, y, ch in _BLADE:
            if not (_BIN_X <= x < _BIN_X + 4 and y >= _BENCH_Y):   # (behind the bin's front: never seen)
                f.put(x, y, ch)
    f = f.over(_pieces(s))
    return _fx(s, 'wfx', f)


def _occluders(s):
    """Cells in front of the saw: the plank / pieces, the bench and the bin's front (never the blade)."""
    occ = set(_pieces(s).px)
    for x in range(_BENCH_X, _BENCH_X + 5):
        for y in range(_BENCH_Y, GROUND + 1):
            occ.add((x, y))
    for x in range(_BIN_X, _BIN_X + 4):
        for y in range(_BENCH_Y, GROUND + 1):
            occ.add((x, y))
    return occ


def _static_body():
    f = Frame()
    put_clawd(f, clawd(eyes='blink', larm='none', rarm='none'))
    for cells in _EYES.values():
        for x, y in cells:
            f.put(x, y, '_')
    return f


_BODY = _static_body()


def _pose_frame(s, rarm):
    f = Frame()
    put_clawd(f, clawd(eyes=s['eyes'], larm=s['larm'], rarm=rarm))
    return f


def _diff(full, base):
    """Cells of `full` that `base` lacks or colors differently (a later layer cannot erase, so check)."""
    missing = [p for p in base.px if p not in full.px]
    if missing:
        raise ValueError('pose needs holes the layer below lacks: %s' % missing)
    f = Frame()
    for (x, y), ch in full.px.items():
        if base.px.get((x, y)) != ch:
            f.put(x, y, ch)
    f.meta = dict(full.meta)
    return f


def _pose(s):
    """Eyelids (filling the eye holes not in use) + left arm: the pose without its right arm, minus the
    static body."""
    return _diff(_pose_frame(s, 'none'), _BODY)


def _rarm(s):
    """His right arm: the full kit pose minus the same pose without it (composite = exactly the pose)."""
    if s['eyes'] == 'look_r' and (20, 14) not in {(10 + x, 12 + y) for x, y, _ in
                                                  clawd(rarm=s['rarm']).sprite.cells}:
        raise ValueError('look_r with rarm=%r would notch his right eye' % s['rarm'])
    return _diff(_pose_frame(s, s['rarm']), _pose_frame(s, 'none'))


def _hand(s):
    """Right arm + the saw, the sanding block, the heart he holds, and the sanding dust."""
    f = _rarm(s)
    occ = _occluders(s)

    def put(x, y, ch):
        if (x, y) not in occ and 0 <= x < W and 0 <= y <= GROUND:
            f.put(x, y, ch)

    saw, rarm = s['saw'], s['rarm']
    if saw == 'cut':                               # in the cut: only the handle (+ push extras) move
        for x, y, ch in _HANDLE['out' if rarm == 'out' else 'up']:
            put(x, y, ch)
        if rarm == 'out':
            for x, y, ch in _PUSH_EXTRA:
                put(x, y, ch)
    elif isinstance(saw, tuple):                   # out of the cut: the whole saw, behind bench / bin
        for x, y, ch in _saw_cells(saw[1:]):
            put(x, y, ch)
    held = s['held']
    if held == 'block':
        gx, gy = _grip(rarm)
        for sx, sy, ch in _BLOCK.cells:
            put(gx + sx, gy + sy, ch)
    elif isinstance(held, tuple) and held[0] == 'heart':
        _heart_at(f, held[1], held[2], _POCKET_Y if held[3] else GROUND + 1)
    return _fx(s, 'hfx', f)


def _fx(s, key='fx', f=None):
    f = Frame() if f is None else f
    for item in s[key]:
        kind = item[0]
        if kind == 'crumb' or kind == 'speck':
            f.put(item[1], item[2], 't')
        elif kind == 'sprite':
            f.place(item[1], item[2], item[3])
        elif kind == 'spark':
            f.place(_SPARK.sprite(item[1]), item[2], item[3])
        elif kind == 'glint':
            f.place(_GLINT.sprite(item[1]), item[2], item[3])
    return f


def _scene():
    f = Frame()
    _paint(f, _LAMP, _LAMP_X, _LAMP_Y)
    f.vline(30, 8, _PY - 1, 'T')                            # boards leaning behind the bin ..
    f.vline(29, 10, _PY - 1, 't')                           # .. their feet hidden by its back wall
    _paint(f, [_BIN_BACK], _BIN_X, _PY)
    _paint(f, _BENCH, _BENCH_X, _BENCH_Y)
    f.put(_GAP - 1, GROUND, 't')                            # the little sawdust heap under the cut
    f.put(_GAP, GROUND, 't')
    _paint(f, _LUMBER, _LUMBER_X, _LUMBER_Y)
    f.place(_MUG, *_MUG_AT)
    return f


def _bin():
    f = Frame()
    _paint(f, _BIN_FRONT, _BIN_X, _BENCH_Y)
    return f


def _goggles():
    f = Frame()
    f.place(_GOGGLES, *clawd().at('face'))
    return f


def _apron():
    """A small denim carpenter's apron: navy band and pocket panel between his eye columns (x 13-17), so
    row 16 under his eyes stays orange."""
    f = Frame()
    f.hline(13, 17, 16, 'B')          # band (= the pocket's mouth)
    f.hline(13, 17, 17, 'b')          # denim panel ..
    f.put(15, 17, 'B')                # .. with a pocket seam
    return f


def _moth():
    """A moth naps on the lamp shade (frame 0) and, once per 17 293 ms (prime, so it drifts against the
    12 s story and the steam), flutters a quick, uneven loop around the warm bulb and lands again."""
    rest = Frame()
    rest.place(_MOTH_REST, *_MOTH_HOME)
    path = [(27, 2), (28, 4), (28, 6), (26, 8), (23, 8), (21, 6), (21, 3), (23, 2), (25, 2)]
    beats = [100, 110, 90, 120, 100, 110, 90, 130, 140]       # uneven wingbeats
    frames = [(rest, 17293 - sum(beats))]
    for k, ((x, y), ms) in enumerate(zip(path, beats)):
        f = Frame()
        f.place(_MOTH_UP if k % 2 == 0 else _MOTH_DN, x, y)
        frames.append((f, ms))
    return frames


def build():
    segs = _timeline().segs
    work, pose, hand, fx = [], [], [], []
    for ms, s in segs:
        work.append((_work(s), ms))
        pose.append((_pose(s), ms))
        hand.append((_hand(s), ms))
        fx.append((_fx(s), ms))
    steam = []
    for i, ms in enumerate((190, 180, 200, 190, 210, 181)):      # 1151 ms: prime
        f = Frame()
        f.place(_STEAM.sprite(i), *_STEAM_AT)
        steam.append((f, ms))
    return anim(NAME, DESC, [
        static('scene', _scene()),
        layer('work', work),
        static('bin', _bin()),
        static('body', _BODY),
        static('goggles', _goggles()),
        layer('pose', pose),
        layer('hand', hand),
        static('apron', _apron()),
        layer('fx', fx),
        layer('steam', steam),
        layer('moth', _moth()),
    ], state=STATE)
