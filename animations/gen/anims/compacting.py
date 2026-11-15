"""compacting - Claude is compacting the conversation.  Preview:  python3 gen/preview.py anim compacting

Storyboard. One master loop (5520 ms) drives Clawd, the stack and every effect from the same beat list, so
nothing can drift. Busy and funny: three stomps that build in energy, a poof, a proud pat and a boop, then
a reset gag.
  A     0  READY (frame 0, the reduced-motion still): Clawd at HOME in a blue sweatband, arms tensed down,
           eyeing the top of a tall paper stack (paper_stack_tall: binder clip, pink tab) on his right.
  B   360  LEAP: a steep take-off, then he travels right (legs tucked, arms flung up, tails streaming);
           the apex is above the stack, so he drops onto it.
  C   630  STOMP 1: he lands and the pile gives under his weight (its top bundle dips a row, the binder clip
           with it, between his feet); he bounces up, fists raised; 880 SLAM: CRUNCH, the stack squashes
           into a splayed slab (impact blink), dust rolls off its base, a sheet squirts out low on the left
           and tumbles away over the empty side, the binder clip pings off over his head; 980 it springs back
           as the mid stack and he checks his work, fists still down (the next wind-up).
  D  1320  STOMP 2: a quick hop, a hang, a slam; 1550 CRUNCH to a flat slab (blink, dust, another
           sheet) -> the low stack. He watches the dust roll off.
  E  1850  STOMP 3, the big one: a look at YOU (here goes ...), a high hop easing into a long hang, an
           accelerating GROUND-POUND; 2420 POOF: a cloud swallows the pile; 2520 the blast flings him home on
           a parabola (looking back, a hair of hang at its apex); 2700 the cloud breaks into puffs (the ones he
           glides past are blown away) revealing a neat strapped PAPER CUBE; 2800 he lands at HOME (dust,
           blink).
  F  2920  PRIDE: he admires the cube while it twinkles; 3300 pats it twice; 3580 steps back a cell, arm
           cocked (the wind-up) ...
     3780  ... and BOOPS it: a fingertip contact, then it zooms off the right edge, speed lines trailing it
           (they never touch his arm); he holds the point.
  G  4060  RESET GAG: once the cube is gone a page flutters in on a falling-leaf zig-zag; 4210 he spots it
           and follows it down; 4510 it flattens out and hovers a row above the floor, 4630 settles as the
           first sheet of a new pile. A sweat bead forms; 4750 he gives YOU a long deadpan look while the
           sweat drop runs its course (rest, slide, slide, stretch, drip) ... 5400 and a whole ream drops out
           of the sky onto that sheet (he flinches), binder clip and all, landing exactly on the 5520 = 0 loop
           seam: frame 0's tall stack, which he turns to and tenses for again.
Layers (back to front): stack (piles with their resting clip, the cube and its zoom, the falling ream) |
fx (the flying clip, dust, poof, sheets, sparkle, speed lines, the page, the sweat drop: all beside or
behind him) | body (band tails behind Clawd, Clawd, band). Plain face only (open, blink, look_*), normal body size, no big arms-up stretch:
STYLE.md section 0.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'compacting'
STATE = 'Compacting the conversation'
DESC = ('Stomps a tall paper stack flat in three escalating hops until it poofs into a neat strapped cube, '
        'pats it and boops it away; then a page flutters back, he gives you a deadpan look, and a whole new '
        'ream drops in.')

_MID = get('paper_stack_mid')
_LOW = get('paper_stack_low')
_CUBE = get('paper_cube')
_SHEET = get('paper_sheet')
_DUST = get('dust_puff')
_POOF = get('poof')
_SPARK = get('sparkle')
_SWEAT = get('sweat_drop')
_LINES = get('motion_lines')

_SX = 25                        # stack centre column: its main body spans x 21..29, like Clawd's body on top


# =====================================================================================================
# Local sprites
# =====================================================================================================
def _bottom(rows, left):
    """Sprite whose leftmost column lands on x=`left` and bottom row on y when placed at (_SX, y)."""
    return Sprite(rows, anchor=(_SX - left, len(rows) - 1))


# The library tall stack (paper_stack_tall), cut into its clip, top, 2-row bundles and base so the pile can
# give a row, and so the new ream can land on the base. Sliced from the live library sprite so later polish
# shows up here; the local rows are only a fallback should its layout ever change.
_TALL_ROWS = get('paper_stack_tall').sprite(0).rows()
if len(_TALL_ROWS) != 14 or len(_TALL_ROWS[0]) != 10:
    _TALL_ROWS = ['..m.m.....', '..nnn.....', '.mmmmmmm..', 'mWWWWWWWm.', 'mwwwwwwwm.', 'mMMMMMMMm.',
                  '.mwwwwwwwm', '.mMMMMMMMm', '.mwwwwwwwm', '.mMMMMMMMp', 'mwwwwwwwm.', 'mMMMMMMMm.',
                  'mwwwwwwwm.', 'mmmmmmmmm.']
_TOP, _BASE = _TALL_ROWS[2:4], _TALL_ROWS[12:14]
_KEEP = [_TALL_ROWS[i:i + 2] for i in (4, 6, 8)]    # three bundles: 10 rows + the clip leave headroom on top
_CLIP_CELLS = [(x, y, ch) for y, r in enumerate(_TALL_ROWS[:2]) for x, ch in enumerate(r) if ch not in '. ']
_CX = (min(c[0] for c in _CLIP_CELLS) + max(c[0] for c in _CLIP_CELLS)) // 2
_CLIP = Sprite(cells=_CLIP_CELLS, anchor=(_CX, 1))                    # its binder clip (anchor: base centre)
_CLIP_FLY = _CLIP.recolor({'n': 's'})                                  # flying: steel survives the dark theme
_CLIP_TUMBLE = _CLIP_FLY.vflipped()                                    # ... upside down (anchor: its top row)

_STACKS = {
    'tall': _bottom(_TALL_ROWS[:10] + _BASE, 21),                         # clip, top, 3 bundles, base
    # his landing weight squeezes the top bundle to one row (its sheet edge vanishes under the top sheet);
    # the clip goes down with it, between his feet
    'tall_dip': _bottom(_TALL_ROWS[:4] + _KEEP[0][1:] + _KEEP[1] + _KEEP[2] + _BASE, 21),
    'mid': _bottom(_MID.sprite(0).rows(), 21),
    'low': _bottom(_LOW.sprite(0).rows(), 21),
    'cube': _bottom(_CUBE.sprite(0).rows(), 21),
    'base': _bottom(_TOP[:1] + _BASE, 21),   # the first page of the new pile, flat on the floor (outlined)
    'mid_sq': _bottom([             # squashed + splayed for one frame on impact
        '.mmmmmmmmm.',
        'mWWWWWWWWWm',
        'mwwwwwwwwwm',
        'mMMMMMMMMMm',
        'mwwwwwwwwwm',
        'mMMMMMMMMMm',
        'mmmmmmmmmmm',
    ], 20),
    'low_sq': _bottom([
        '.mmmmmmmmm.',
        'mWWWWWWWWWm',
        'mmmmmmmmmmm',
    ], 20),
}
# the new ream: clip, top and three bundles in one block; on the base it completes the tall stack exactly
_REAM = _bottom(_TALL_ROWS[:10], 21)


def _top_y(key):
    s = _STACKS[key]
    return GROUND - (s.y1 - s.y0) + (2 if key.startswith('tall') else 0)     # (the clip is not a step)


def _stand_y(key):
    """Box y of Clawd standing on that stack."""
    return _top_y(key) - 8


# Headband: a blue sweatband on the top row of his head (so every glance stays visible), its loose end on his
# left with two tails. Two sprites with the same anchor (slot head): the band, worn after Clawd, and the
# tails, worn BEFORE him so they stream behind him and never cover a raised arm.
def _blue(cells):
    return Sprite(cells=[(x, y, 'b') for x, y in cells], anchor=(5, 0))


_TAIL_KINDS = {                 # box coordinates; one colour: a navy accent would not survive 3 px cells
    'hang': [(-1, 0), (-2, 1), (-3, 2), (-3, 3), (-1, 1), (-1, 2), (-2, 3)],                 # at rest: droop
    'rise': [(-1, 0), (-2, 1), (-3, 2), (-4, 3), (-1, 1), (-1, 2), (-1, 3)],                 # going up / landing
    'fall': [(-1, -1), (-2, -2), (-3, -3), (-1, 0), (-2, 0), (-3, -1), (-4, -1)],            # coming down: flick up
    'flick': [(-1, -1), (-2, -2), (-3, -2), (-1, 0), (-2, 0), (-3, -1), (-4, -1)],           # ... near the top edge
    's1': [(-1, 0), (-2, 1), (-3, 1), (-4, 0), (-5, 0), (-1, 1), (-2, 2), (-3, 3), (-4, 3), (-5, 2)],  # streaming
    # with arms 'raise' his left hand fills box (-1, 0) and (-1, 1): these leave over it and trail from x <= -2
    'sr': [(-1, -1), (-2, -1), (-3, -1), (-4, 0), (-5, 0), (-2, 0), (-3, 1), (-4, 2), (-5, 2)],
    'sr2': [(-1, -1), (-2, -1), (-3, 0), (-4, 0), (-5, -1), (-2, 0), (-3, 1), (-4, 1), (-5, 2)],
}
_TAIL_NAMES = sorted(_TAIL_KINDS)
_TAILS = Item('compact_band_tails', 'head', 'sweatband tails (worn before Clawd)',
              [_blue(_TAIL_KINDS[k]) for k in _TAIL_NAMES])
_BAND = Item('compact_band', 'head', 'blue sweatband (worn after Clawd)', _blue([(x, 0) for x in range(10)]))


def _put_vis(f, spr, x, y):
    """Place a sprite, silently dropping the cells outside the canvas (things entering or leaving)."""
    for sx, sy, ch in spr.cells:
        X, Y = x + sx - spr.ax, y + sy - spr.ay
        if 0 <= X < W and 0 <= Y < H:
            f.put(X, Y, ch)


def _trim(spr, keep):
    """Copy of a sprite without the cells (in sprite space, relative to its anchor) that `keep` rejects."""
    return Sprite(cells=[c for c in spr.cells if keep(c[0] - spr.ax, c[1] - spr.ay)], anchor=(spr.ax, spr.ay))


# =====================================================================================================
# Master timeline: Clawd's beats, the stack's changes, tags for the effects
# =====================================================================================================
def _P(eyes='open', larm='side', rarm='side', legs='stand'):
    return clawd(eyes=eyes, larm=larm, rarm=rarm, legs=legs)


class _Timeline:
    def __init__(self):
        self.beats = []          # (t, ms, pose, x, y, tails)
        self.stack = []          # (t, key or None)
        self.tags = {}
        self.t = 0

    def add(self, ms, pose, x, y, tails='hang', stack=False, tag=None):
        if tag:
            self.tags[tag] = self.t
        if stack is not False:
            self.stack.append((self.t, stack))
        self.beats.append((self.t, ms, pose, x, y, tails))
        self.t += ms


def _timeline():
    T = _Timeline()
    yt, ym, yl = _stand_y('tall'), _stand_y('mid'), _stand_y('low')       # 2, 4, 7
    # A  ready at HOME, arms tensed, eyeing the top of the tall stack (the ream just landed on it)
    T.add(360, _P('look_ur', 'down', 'down'), 10, 12, 'hang', 'tall', 'start')
    # B  leap: steep take-off, then travel; the apex is above the stack top so he drops onto it
    T.add(60, _P('look_ur', 'up', 'up', 'short'), 10, 8, 'rise', tag='leap')
    T.add(60, _P('look_ur', 'raise', 'raise', 'short'), 11, 4, 'sr')
    T.add(70, _P('look_r', 'raise', 'raise', 'short'), 14, 2, 'sr2')
    T.add(80, _P('look_dr', 'up', 'up', 'short'), 17, 1, 's1')
    # C  stomp 1: lands, the pile gives a row under him (tails overshoot), he bounces up with his fists
    #    raised ... SLAM: the stack crunches down to mid; he checks his work, fists still down (the wind-up)
    T.add(100, _P('look_d', 'down', 'down'), 20, _stand_y('tall_dip'), 'rise', 'tall_dip', 'hit1')
    T.add(150, _P('look_d', 'up', 'up', 'short'), 20, yt - 1, 'hang')       # bounces off it, fists up
    T.add(100, _P('blink', 'down', 'down'), 20, _stand_y('mid_sq'), 'rise', 'mid_sq', 'crunch1')
    T.add(340, _P('look_d', 'down', 'down'), 20, ym, 'hang', 'mid')
    # D  stomp 2: hop, hang, slam: mid -> low; he watches the dust roll off
    T.add(170, _P('look_d', 'up', 'up', 'short'), 20, ym - 2, 'rise')
    T.add(60, _P('look_d', 'down', 'down'), 20, ym, 'fall', tag='hit2')
    T.add(100, _P('blink', 'down', 'down'), 20, _stand_y('low_sq'), 'rise', 'low_sq', 'crunch2')
    T.add(200, _P('look_dl'), 20, yl, 'hang', 'low')
    # E  stomp 3, the big one: a look at you (here goes ...), a high hop easing into a long hang, an
    #    accelerating ground-pound -> POOF; the blast throws him home on a parabola, looking back
    T.add(250, _P('open', 'down', 'down'), 20, yl, 'hang', tag='here')
    T.add(70, _P('look_d', 'up', 'up', 'short'), 20, yl - 4, 'rise')
    T.add(190, _P('look_d', 'up', 'up', 'short'), 20, yl - 6, 'hang')
    T.add(60, _P('look_d', 'up', 'up'), 20, yl - 4, 'flick')
    T.add(100, _P('blink', 'down', 'down'), 20, yl, 'fall', None, 'hit3')
    T.add(80, _P('look_dr', 'raise', 'raise', 'short'), 18, 4, 'sr', tag='poof')
    T.add(100, _P('look_dr', 'up', 'up', 'short'), 15, 3, 'rise')        # the apex: a hair of hang
    T.add(100, _P('look_r', 'up', 'up'), 12, 6, 'fall', tag='glide')
    T.add(120, _P('blink'), 10, 12, 'rise', tag='land')
    # F  proud of the cube: admires it while it twinkles, pats it twice, steps back a cell with his arm
    #    cocked (the wind-up) and boops it with a fingertip; he holds the point while it zooms away
    T.add(380, _P('look_r'), 10, 12, 'hang', tag='admire')
    T.add(100, _P('look_r', 'side', 'out'), 10, 12, 'hang', tag='pat')
    T.add(80, _P('look_r'), 10, 12, 'hang')
    T.add(100, _P('look_r', 'side', 'out'), 10, 12, 'hang')
    T.add(200, _P('look_r', 'side', 'down'), 9, 12, 'hang', tag='windup')
    T.add(430, _P('look_r', 'side', 'point'), 10, 12, 'hang', tag='poke')
    # G  the reset gag: a page flutters in, he follows it down; as it settles a sweat bead forms, he gives
    #    you a long deadpan look (the drop runs in the fx layer) ... and the ream lands on the seam
    T.add(300, _P('look_ur'), 10, 12, 'hang', tag='spot')
    T.add(240, _P('look_dr'), 10, 12, 'hang', tag='follow')
    T.add(650, _P('open'), 10, 12, 'hang', tag='deadpan')
    T.add(120, _P('blink'), 10, 12, 'rise', tag='flinch')              # the ream drops: he flinches
    return T


_T = _timeline()
_LOOP = _T.t
_TAG = _T.tags


# =====================================================================================================
# Effect events: (start ms, [(sprite or None, x, y, ms), ...]) per layer, each layer on its own clock
# =====================================================================================================
_EV = {'fx': [], 'stackfx': []}


def _ev(lay, t0, steps):
    _EV[lay].append((int(t0) % _LOOP, steps))


def _item(item, idx, ms, x, y):
    return [(item.sprite(i), x, y, m) for i, m in zip(idx, ms)]


_FLY = [_SHEET.sprite(i).recolor({'W': 'w'}) for i in range(3)]     # flying sheets: two tones are plenty


def _arc(pts, ms=100, phase=0):
    """A sheet flying along hand-keyed points, tumbling through its tilt frames 0,1,2,1."""
    return [(_FLY[[0, 1, 2, 1][(k + phase) % 4]], x, y, ms) for k, (x, y) in enumerate(pts)]


# crunches: dust rolls off the stack's base, a squeezed-out sheet squirts out low on the left and tumbles up
# and away over the empty side; on the first one the clip pings off, straight up from behind his head
_DUST_L = [_trim(_DUST.sprite(i), lambda x, y: x < 0).recolor({'w': 't'}) for i in range(3)]   # left half
for _tag, _path, _ph in (('crunch1', [(17, 15), (10, 10), (1, 7)], 0),
                         ('crunch2', [(15, 17), (8, 12), (0, 11)], 2)):
    _ev('fx', _TAG[_tag], [(_DUST_L[i], _SX, GROUND - 1, 100) for i in range(3)])
    _ev('fx', _TAG[_tag], _arc(_path, phase=_ph))
_ev('fx', _TAG['crunch1'], [(_CLIP_FLY, 25, 3, 100), (_CLIP_TUMBLE, 27, -1, 100)])   # ... out over the top

# the big one: a poof swallows the pile and breaks into a ring of puffs around the cube; its last specks
# skip his home box (no grit between his legs once he has landed)
_POOF_AT = (22, 15)
_PUFF = [_POOF.sprite(i).recolor({'W': 'w'}) for i in range(4)]       # one paper tone; the grey shade stays


def _clear_of(spr, x, y, tag):
    """`spr` placed at (x, y) minus every puff (connected part) touching Clawd in the beat at `tag`."""
    b = [b for b in _T.beats if b[0] == _TAG[tag]][0]
    f = Frame()
    wear(f, _TAILS, b[2], b[3], b[4], i=_TAIL_NAMES.index(b[5]))
    put_clawd(f, b[2], b[3], b[4])
    near = {(cx + dx, cy + dy) for cx, cy in f.px for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    cells = {(cx - spr.ax, cy - spr.ay): ch for cx, cy, ch in spr.cells}
    drop, todo = set(), [c for c in cells if (c[0] + x, c[1] + y) in near]
    while todo:                         # whole puffs go (8-connected), so no silhouette is left open
        c = todo.pop()
        if c in drop:
            continue
        drop.add(c)
        todo += [(c[0] + dx, c[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (c[0] + dx, c[1] + dy) in cells]
    return _trim(spr, lambda sx, sy: (sx, sy) not in drop)


# the ring breaks up as he glides past it: no puff touches him
_ev('fx', _TAG['hit3'], [(_PUFF[1], _POOF_AT[0], _POOF_AT[1], _TAG['glide'] - _TAG['hit3']),
                         (_clear_of(_PUFF[2], _POOF_AT[0], _POOF_AT[1], 'glide'), _POOF_AT[0], _POOF_AT[1],
                          _TAG['land'] - _TAG['glide']),
                         (_trim(_PUFF[3], lambda x, y: not (x + _POOF_AT[0] <= 20 and y + _POOF_AT[1] >= 12)),
                          _POOF_AT[0], _POOF_AT[1], _TAG['admire'] - _TAG['land'])])
# landing dust at home: only the left puff (the cube blocks the right one), then the cube twinkles while
# he admires it, on the same 120 ms beat: a full star that shrinks back to a thin cross and goes out
_ev('fx', _TAG['land'], [(_DUST_L[i], 15, GROUND - 1, 120) for i in range(2)])
_ev('fx', _TAG['admire'], _item(_SPARK, [2, 3], [120, 120], 27, 13))

# the boop: the fingertip touches the cube for 80 ms, then it zooms off the right edge (one blurred beat
# at +5, then gone); the speed lines trail it (row 14 from x 24, rows 16 and 18 from x 21: a clear cell between them and his
# pointing arm or body, and one between them and the cube), then fade further right
_ZOOM = _TAG['poke'] + 80
_CUBE_SMEAR = _STACKS['cube'].recolor({'W': 'w', 'M': 'w', 'B': 'b'})    # a 100 ms blur: flat tones
_ev('stackfx', _ZOOM, [(_CUBE_SMEAR, _SX + 5, GROUND, 100)])
_LINES_A = _trim(_LINES.sprite(0), lambda x, y: (x + 24 >= (24 if y == -2 else 21))
                 and x + 24 <= (25 if y == -2 else 24))
_LINES_B = _trim(_LINES.sprite(1), lambda x, y: x + 29 >= 28)
_ev('fx', _ZOOM, [(_LINES_A, 24, 16, 100), (_LINES_B, 29, 16, 100)])

# the page: a falling-leaf zig-zag on a 150 ms beat (face-on as it enters, tilted the way it glides), then it
# flattens out and hovers a row above the floor (the very sheet it becomes), and settles as the new pile's
# first sheet
_PAGE_T0 = _ZOOM + 200
_PAGE = [(27, 1, 1), (23, 6, 2), (26, 12, 0)]
_SETTLE = _PAGE_T0 + 150 * len(_PAGE) + 120
_ev('fx', _PAGE_T0, [(_FLY[fr], x, y, 150) for x, y, fr in _PAGE]
    + [(_STACKS['base'], _SX, GROUND - 1, 120)])

# the sweat drop, the library's own cycle: a bead forms as the page settles, then rest, slide, slide,
# stretch and the drip, which lands plip on the sheet's edge; it is gone as the ream lands on the seam
_DROP = [_SWEAT.sprite(i).recolor({'C': 'c'}) for i in range(7)]      # one white glint is plenty
_ev('fx', _SETTLE, [(_DROP[6], 15, 14, _TAG['deadpan'] - _SETTLE),
                    (_DROP[0], 15, 14, 300),
                    (_DROP[1], 15, 14, 120),
                    (_DROP[2], 15, 14, 120),
                    (_DROP[3], 15, 14, 110),
                    (_DROP[4], 15, 14, 120)])
_DRIP = _LOOP - 120

# the ream: out of the sky in two accelerating beats (its bottom at rows 1, 8), onto the sheet at the seam
_REAM_FALL = _REAM.recolor({'W': 'w'})       # falling fast: no top-face highlight until it lands
_ev('stackfx', _DRIP, [(_REAM_FALL, _SX, 1, 60), (_REAM_FALL, _SX, 8, 60)])

_STACK_KEYS = sorted([k for k in _T.stack if k[0] > 0]
                     + [(_TAG['glide'], 'cube'),            # revealed as the cloud breaks up
                        (_ZOOM, None),                      # booped away
                        (_SETTLE, 'base'),                  # the page settles
                        (0, 'tall')])


# =====================================================================================================
# Sampling helpers
# =====================================================================================================
def _draw_events(f, lay, t):
    for t0, steps in _EV[lay]:
        a = (t - t0) % _LOOP
        for spr, x, y, ms in steps:
            if a < ms:
                if spr is not None:
                    _put_vis(f, spr, x, y)
                break
            a -= ms
    return f


def _event_times(lay):
    ts = set()
    for t0, steps in _EV[lay]:
        t = t0
        for s in steps:
            ts.add(t % _LOOP)
            t += s[3]
        ts.add(t % _LOOP)
    return ts


def _sample(draw, times, name):
    """Frames at the given change times. A change closer than 40 ms to the previous one is folded
    into it, showing the newer state a hair early, so no layer ever has a sliver frame."""
    ts = sorted({t % _LOOP for t in times} | {0})
    keep = [[0, 0]]                      # [frame start, time sampled]
    for t in ts[1:]:
        if _LOOP - t < 40:
            continue
        if t - keep[-1][0] >= 40:
            keep.append([t, t])
        elif keep[-1][0] > 0:
            keep[-1][1] = t
    out = []
    for i, (t, ts_) in enumerate(keep):
        end = keep[i + 1][0] if i + 1 < len(keep) else _LOOP
        out.append((draw(ts_), end - t))
    return layer(name, out)


def _stack_key(t):
    cur = None
    for kt, k in _STACK_KEYS:
        if kt <= t:
            cur = k
    return cur


def _stack_frame(t):
    f = Frame()
    key = _stack_key(t)
    if key:
        f.place(_STACKS[key], _SX, GROUND)
    return _draw_events(f, 'stackfx', t)


def _body_frame(t):
    for b in _T.beats:
        if b[0] <= t < b[0] + b[1]:
            break
    _, _, pose, x, y, tails = b
    f = Frame()
    wear(f, _TAILS, pose, x, y, i=_TAIL_NAMES.index(tails))     # behind him
    put_clawd(f, pose, x, y)
    wear(f, _BAND, pose, x, y)
    return f


def build():
    beats = {b[0] for b in _T.beats}
    return anim(NAME, DESC, [
        _sample(_stack_frame, {kt for kt, _ in _STACK_KEYS} | _event_times('stackfx'), 'stack'),
        _sample(lambda t: _draw_events(Frame(), 'fx', t), _event_times('fx'), 'fx'),
        _sample(_body_frame, beats, 'body'),
    ], state=STATE)
