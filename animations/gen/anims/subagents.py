"""subagents - Subagents are running.  Preview:  python3 gen/preview.py anim subagents

Storyboard (master loop 10.4 s). One carrier (the plain official mini Clawd) makes two trips per loop
and the stack visibly grows on its pallet: pallet -> crate 2 -> crate 3 -> the crane ships both. Its walks
live in a layer exactly half the master loop long (5.2 s), so every walk-in / walk-out plays twice per
loop at 1 cell per frame (library walk cycle empty-handed, the 2 library carry frames when loaded).
What happens at the stack differs per trip and lives in the synced 'carrier' layer.
  0.00  Frame 0: Captain Clawd at HOME (captain hat, clip-on ID badge, checklist held up by its corner
        in his raised left hand, 1 cell clear of the cap) points "right there!". The carrier has just set
        crate 3 on crate 2 (whose top shows between its raised hands); the crane hook waits; the typist
        mini works its heart-sticker laptop.
  0.09  wood dust squeezes out of the seam; his arm drops. 0.18 he nods (eyes a cell down). 0.30 the
        carrier lets go and looks to the boss; a check pops over the full stack (overshoot, settle).
        0.45 Clawd checks the list, 0.70 ticks item 2. 0.88 the carrier blinks ...
  1.00  ... and walks out, easing in (150, 130, 120, then 110 ms per cell); out of frame at 1.84.
        1.15 Clawd watches it go and cues the crane. The 3-crate stack stands alone with its check.
  1.90  the check clears, the hook lowers eased (1, 2, 2, 1 rows), 2.21 catches the stack (clink).
  2.90  lift: slow off the pallet, then faster (1, 2, 4, 5 rows), slewing 1 cell right, plain planks
        while it whizzes out. Clawd waves it goodbye (two strokes), still watching it.
  3.50  back to the list: 3.70 ticks item 3 (shipped), 3.90 the page curls up, 4.02 a fresh list.
        3.70 the empty hook drops back in (overshoot, settle).
  3.94  the carrier walks in with crate 2 (easing out, the last cells longest); 4.30 Clawd sees it,
        4.45 points "right here"; 4.84 it plants its feet at the pallet; 5.04 lowers the crate 1 row
        per frame and 5.26 sets it down (dust). Arm down, nod, 5.70 ticks item 1 on the fresh list.
  5.26  the carrier looks to the boss, 5.70 blinks, 5.82 glances at the hook side, 6.20 walks out.
  7.04  pallet + crate 2 stand alone; 7.10 Clawd checks on the typist (half-step glance down-left).
  8.90  he looks right: 9.14 the carrier walks in with crate 3 (it rides at slot height and glides
        onto crate 2); 9.25 Clawd waves it on, "come on!" (raise, then holds the wave).
 10.04  it plants its feet; 10.24 a little hop heaves the crate ... frame 0: it lands, Clawd points.
Independent co-prime layers: the typist's irregular key bursts (4.37 s); its "done!" beat (13.11 s =
3 x 4.37 s, so it always lands in a typing pause, hands down): it glances over at the boss, raises a
hand, and its lid's heart sticker turns into a green tick; Clawd's blinks with a double blink (9.37 s).
Plain face, black eyes, normal body size (STYLE.md section 0). His glances are fine-line half steps
(STYLE.md 0b) so a black eye never sits on his body's edge or at an arm's root (asserted in build()).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'subagents'
STATE = 'Subagents are running'
DESC = ('Captain Clawd (captain hat, badge, checklist) runs a crew of mini Clawds: a carrier stacks '
        'crates on a pallet, a typist works its laptop, he points, nods and ticks his list, and a crane '
        'hauls each finished stack away.')

LOOP = 10400
HALF = LOOP // 2                 # the carrier's walk layer: every walk plays twice per loop

# =====================================================================================================
# Sprites
# =====================================================================================================
_CARRY = get('mini_clawd_carry')
_WALK = get('mini_clawd_walk')
_PLAIN = get('mini_clawd')
_TYPE = get('mini_clawd_type')

# The crate the minis carry (top 3 rows of the library carry pose), anchored at its top-left cell.
_CRATE = Sprite(cells=[(x, y, ch) for x, y, ch in _CARRY.sprite(0).cells if y <= 2], anchor=(0, 0), name='crate')
# A low wooden pallet under the stack: lit deck, three blocks.
_PALLET = Sprite(['ttttttT',
                  'TT.T.Td'], anchor=(0, 0), name='pallet')

STACK_X = 24                     # stack columns 24..30 (Clawd's pointing hand ends at x 22)
SLOT_Y = {2: 15, 3: 12}          # top row of each crate on the pallet (rows 18-19)
HOOK_X = STACK_X + 3             # crane cable column
HOOK_REST = 5                    # hook bottom row while it waits: one cable cell shows above it
HOOK_CATCH = SLOT_Y[3] - 1       # hook bottom row when it holds the full stack


# The carrier's poses: the library carry / walk / plain minis (feet anchored on the ground row).
_POSES = {
    'carry': [Sprite(_CARRY.sprite(i).rows(), anchor=(3, 7)) for i in (0, 1)],
    'hop': [Sprite(_CARRY.sprite(0).rows(), anchor=(3, 8))],                 # the same, 1 row up
    'hands': [Sprite(_CARRY.sprite(0).rows()[3:], anchor=(3, 4))],          # both hands up, no crate
    'plain': [_PLAIN.sprite(0)],
    'walk': [_WALK.sprite(i) for i in range(4)],
}


def _mini_sprite(pose, i=0, look=0, blink=False):
    """The carrier: library pose, black eyes glancing sideways by `look` cells (never up or down: the
    rows above and below its eyes are its edges); blink = eyes shut for a frame."""
    frames = _POSES[pose]
    spr = frames[i % len(frames)]
    cells = {(x, y): ch for x, y, ch in spr.cells}
    eyes = [p for p, ch in cells.items() if ch == ERASE]
    for p in eyes:
        cells[p] = '#'
    if not blink:
        for x, y in eyes:
            cells[(x + look, y)] = EYE_INK
    return Sprite(cells=[(x, y, ch) for (x, y), ch in cells.items()], anchor=(spr.ax, spr.ay))


# Crane hook: pulley block lit from the top + gold hook. Rows relative to the hook's bottom row hy.
_HOOK = ['mmm', 'NNN', '.j.', 'j.j', '.jj']
# Check over a finished stack: a small v, the long stroke overshoots, then settles.
_CHECK_V = [(26, 8), (28, 8), (27, 9)]
_CHECK = [_CHECK_V + [(29, 7), (30, 6)], _CHECK_V + [(29, 7)]]
# Wood dust squeezed out of the left side of a seam (x, dy from the upper crate's bottom row).
_PUFF = [[(23, 0, 't'), (23, 1, 'T')],
         [(22, -1, 't'), (22, 0, 'T')]]
_CLINK_AT = (23, 9)              # open air left of the hook when it holds the stack


# =====================================================================================================
# Drawing helpers
# =====================================================================================================
def _put(f, x, y, ch, crop_ok=False):
    """Draw one cell. crop_ok marks the deliberate exits only (the carrier crossing the right edge, the
    stack leaving through the top); anything else off the canvas counts as clipping."""
    if crop_ok and not (0 <= x < W and 0 <= y < H):
        return
    f.put(x, y, ch)


def _stamp(f, spr, x, y, crop_ok=False):
    for sx, sy, ch in spr.cells:
        _put(f, x + sx - spr.ax, y + sy - spr.ay, ch, crop_ok)


def _crate(f, top, dx=0, crop_ok=False, plain=False):
    spr = _CRATE.recolor({'d': 'T'}) if plain else _CRATE
    _stamp(f, spr, STACK_X + dx, top, crop_ok=crop_ok)


def _paint_rows(f, rows, x0, y0, crop_ok=False):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                _put(f, x0 + i, y0 + j, ch, crop_ok)


def _segments(track, length):
    """(value, ms) list from an absolute-time track [(t, value)] covering [0, length)."""
    track = sorted(track, key=lambda kv: kv[0])
    out = []
    for k, (t, v) in enumerate(track):
        end = track[k + 1][0] if k + 1 < len(track) else length
        if end > t:
            out.append((v, end - t))
    return out


# =====================================================================================================
# Tracks: lists of (t_ms, value). Every synced layer reads only its own track.
# =====================================================================================================
_L, _C, _R = -1, 0, 1
LIFT = 2900                      # the crane lifts the stack off the pallet
OUT1 = 1000                      # the carrier starts walking out (and again at OUT1 + HALF)
_OUT_MS = (150, 130, 120, 110, 110, 110, 110)    # x 25..31: starts slow (turning), then a brisk walk
_IN_MS = (110, 110, 115, 120, 130, 145, 170, 200)    # x 31..24: eases out; at x 24 it plants its feet
HOP_MS = 160                     # crate 3: the heave before frame 0
ARRIVE = HALF - HOP_MS           # the carrier has planted its feet at x 24 (and again at ARRIVE + HALF)
IN1 = ARRIVE - sum(_IN_MS)       # the carrier starts walking in (and again at IN1 + HALF)
LAND2 = ARRIVE + 220             # crate 2 lands on the pallet


def _walk_track():
    """The carrier's walks (HALF-long layer): out empty-handed, in with a crate. None = not walking
    (it stands at the stack, drawn by the carrier layer)."""
    tr, t = [(0, None)], OUT1
    for k, (x, ms) in enumerate(zip(range(25, 32), _OUT_MS)):
        tr.append((t, ('walk', x, k % 4, _R)))
        t += ms
    tr.append((t, None))
    t = IN1
    for k, (x, ms) in enumerate(zip(range(31, 23, -1), _IN_MS)):
        tr.append((t, ('carry', x, (k + 1) % 2, _L)))     # ends on legs apart: planted
        t += ms
    tr.append((t, None))
    return tr


def _tracks():
    T = {k: [] for k in ('carrier', 'stack', 'crane', 'fx', 'eyes', 'arm', 'tick')}
    A2, A3 = ARRIVE, ARRIVE + HALF               # the two arrivals at the stack
    # ---- carrier at the stack: ('mini', pose, i, look[, blink]) plus a crate it is lowering -------
    c = T['carrier']
    c += [(0, (('mini', 'hands', 0, _C),)),                 # frame 0: crate 3 is down, hands still up
          (300, (('mini', 'plain', 0, _L),)),                # lets go, looks to the boss
          (OUT1 - 120, (('mini', 'plain', 0, _L, True),)),   # blink ... and off it goes
          (OUT1, ())]
    c += [(A2, (('mini', 'hands', 0, _C), ('crate', 13))),   # lowers crate 2, 1 row per frame
          (A2 + 110, (('mini', 'hands', 0, _C), ('crate', 14))),
          (LAND2, (('mini', 'plain', 0, _L),)),              # it is down: hands on its sides, looks up
          (5700, (('mini', 'plain', 0, _L, True),)),         # blink
          (5820, (('mini', 'plain', 0, _R),)),               # a glance at the empty hook: off it goes
          (OUT1 + HALF, ())]
    c += [(A3, (('mini', 'hop', 0, _C),))]                   # heave! (frame 0: the crate lands)
    # ---- stack: how many crates sit on the pallet -------------------------------------------------
    T['stack'] += [(0, 2), (LIFT, 0), (LAND2, 1)]
    # ---- fx: dust at each landing seam, check over the finished stack, clink on contact ----------
    T['fx'] += [(0, ()),
                (90, (('puff', SLOT_Y[3] + 2, 0),)), (170, (('puff', SLOT_Y[3] + 2, 1),)),
                (300, (('check', 0),)), (380, (('check', 1),)), (1900, ()),   # until the hook comes
                (2210, (('clink', 1),)), (2300, (('clink', 2),)), (2420, ()),
                (LAND2, (('puff', SLOT_Y[2] + 2, 0),)), (LAND2 + 80, (('puff', SLOT_Y[2] + 2, 1),)),
                (LAND2 + 190, ())]
    # ---- crane: (hook bottom row hy, crates hanging on it[, boom slew dx]); None = out of frame --
    T['crane'] += [(0, (HOOK_REST, 0)),
                   (1900, (6, 0)), (2010, (8, 0)), (2110, (10, 0)), (2210, (HOOK_CATCH, 0)),  # 1, 2, 2, 1
                   (LIFT, (HOOK_CATCH - 1, 2)), (LIFT + 220, (HOOK_CATCH - 3, 2)),          # up 1, 2,
                   (LIFT + 330, (HOOK_CATCH - 7, 2, 1)), (LIFT + 420, (HOOK_CATCH - 12, 2, 1)),  # 4, 5
                   (LIFT + 500, None),                                                       # gone
                   (3620, (2, 0)), (3710, (HOOK_REST + 1, 0)), (3820, (HOOK_REST, 0))]   # drops in, settles
    # ---- Clawd: eyes and right arm (separate layers: they rarely change together) ----------------
    T['eyes'] += [(0, 'open'),
                  (180, 'nod'),                # nod as the crate lands
                  (450, 'look_l'),             # the checklist (tick at 700)
                  (1150, 'look_r'),            # watches the carrier go, cues the crane, sees the stack off
                  (3500, 'look_l'),            # ticks "shipped", flips the page
                  (4300, 'look_r'),            # here comes crate 2
                  (LAND2 + 60, 'nod'),         # nod
                  (LAND2 + 260, 'look_l'),     # tick item 1, then watches the list a while
                  (7100, 'look_dl'),           # checks on the typist (all good)
                  (8900, 'look_r')]            # crate 3 is on its way: "come on!" ... frame 0: "right there!"
    T['arm'] += [(0, 'point'), (90, 'side'),
                 (LIFT, 'wave'), (LIFT + 180, 'raise'), (LIFT + 360, 'wave'), (LIFT + 560, 'side'),
                 (4450, 'point'), (LAND2, 'side'),
                 (9250, 'raise'), (9480, 'wave')]                  # "come on!" ... frame 0: points
    T['tick'] += [(0, 'one'), (700, 'two'), (3700, 'three'), (3900, 'lift'),
                  (4020, 'fresh'), (LAND2 + 440, 'one')]
    return T


# =====================================================================================================
# Clawd: a static body, black eyes and the right arm in their own small layers
# =====================================================================================================
_LARM = 'raise'                  # holds the checklist up by its corner, clear of the cap


def _pose(eyes='open', rarm='side'):
    return clawd(eyes=eyes, larm=_LARM, rarm=rarm)


_ARM_ROOT = (HOME[0] + 10, HOME[1] + 2)      # (20, 14): the right arm cell every arm shape shares


def _r_body():
    f = Frame()
    put_clawd(f, clawd(eyes='blink', larm=_LARM, rarm='none'))
    f.put(_ARM_ROOT[0], _ARM_ROOT[1], '#')
    for x in range(HOME[0] + 1, HOME[0] + 10):   # his top row is always under the cap's band
        f.px.pop((x, HOME[1]), None)
    return f


# His glances are the fine-line half steps (STYLE.md 0b): a full-cell look_l / look_r would put a black
# eye on his body's edge, right at an arm's root; on the dark theme it reads as a notch and the arm floats.
_FINE = dict(FINE_EYES)
_FINE['nod'] = [(0, 2, '_'), (1, 2, '_'), (0, 3, '_'), (1, 3, '_')]        # a full cell down (inside him)
_FINE['look_dl'] = [(-1, 1, '_'), (0, 1, '_'), (-1, 2, '_'), (0, 2, '_')]  # half a cell down and left
_SIDEWAYS = ('look_l', 'look_r', 'look_dl')      # not mirrored for the right eye


def _eye_px(eyes):
    """Fine (half-size) pixels of both black eyes."""
    p = _pose()
    out = []
    for side, key in ((0, 'eye_l'), (1, 'eye_r')):
        ex, ey = p.anchors[key]
        fx0, fy0 = 2 * (HOME[0] + ex), 2 * (HOME[1] + ey)
        mirror = side == 1 and eyes not in _SIDEWAYS
        for dx, dy, ch in _FINE[eyes]:
            out.append((fx0 + (1 - dx if mirror else dx), fy0 + dy))
    return out


def _r_eyes(eyes):
    f = Frame(res=2)
    for x, y in _eye_px(eyes):
        f.put(x, y, EYE_INK)
    return f


def _r_arm(rarm):
    f = Frame()
    for item in ARMS[rarm]:
        x, y = _ARM_ROOT[0] + item[0], _ARM_ROOT[1] + item[1]
        if (x, y) != _ARM_ROOT:
            f.put(x, y, item[2] if len(item) > 2 else '#')
    return f


def _check_eyes(T):
    """Every black eye pixel is surrounded by his orange body (never on an edge, never at an arm's
    root), at any moment of the loop."""
    body = {(x, y) for x, y, ch in clawd(eyes='blink', larm=_LARM, rarm='none').sprite.cells}
    body = {(2 * (HOME[0] + x) + i, 2 * (HOME[1] + y) + j) for x, y in body for i in (0, 1) for j in (0, 1)}
    for t, eyes in T['eyes']:
        px = set(_eye_px(eyes))
        for x, y in px:
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                assert q in body or q in px, 'eye %s at %s is too close to his edge (t=%d)' % (eyes, (x, y), t)


def _blink_layer():
    """Eyelids: covers every cell his eyes can occupy, so blinks work whatever he is looking at.
    Uneven gaps and one double blink (9370 ms, co-prime with the master loop)."""
    cover = Frame()
    for x0 in (HOME[0] + 1, HOME[0] + 7):
        cover.rect(x0, HOME[1] + 2, 3, 2, '#')
    empty = Frame()
    seq = [(empty, 3100), (cover, 130), (empty, 4300), (cover, 110), (empty, 90), (cover, 100),
           (empty, 1540)]
    return layer('blink', seq)


def _r_hat():
    f = Frame()
    wear(f, get('captain_hat'), _pose())
    return f


def _r_badge():
    """The library lanyard badge, card only: its straps would run up into his eye row and touch the
    eyes whenever he glances sideways, so he wears it as a clip-on card."""
    f = Frame()
    p = _pose()
    wear(f, get('lanyard_badge'), p)
    eye_row = p.at('face')[1]
    for q in [q for q in f.px if q[1] <= eye_row + 1]:
        del f.px[q]
    return f


# ---- the checklist ------------------------------------------------------------------------------------
_BOARD_FALLBACK = ['..mmm..', 'ttsSstT', 'tgwgmmT', 'twgwwwT', 'tgwgmmT', 'twgwwwT', 'twNwmmT', 'twwwwwT',
                   'TTTTTTT']


def _board_rows():
    """The library clipboard with its three items evenly spaced (2 rows each), so the third tick fits on
    the sheet: the blank row under the clip moves below the last item."""
    rows = get('clipboard').sprite(0).rows()
    if len(rows) == 9 and set(rows[2][1:-1]) == {'w'} and 'N' in rows[7]:
        return rows[:2] + rows[3:8] + [rows[2]] + rows[8:]
    return list(_BOARD_FALLBACK)


_BOARD_X, _BOARD_BOTTOM = HOME[0] - 8, HOME[1]   # x 2..8 (1 cell clear of the cap), rows 4..12
_ITEM_ROWS = (2, 4, 6)           # board rows of the three items (a tick takes its row and the next)


def _board_origin():
    rows = _board_rows()
    return _BOARD_X, _BOARD_BOTTOM - len(rows) + 1


def _r_clipboard():
    """Static board in the 'one' state (item 1 ticked, items 2-3 open); the tick layer changes it."""
    f = Frame()
    x0, y0 = _board_origin()
    _paint_rows(f, _board_rows(), x0, y0)
    _paint_item(f, _ITEM_ROWS[1], False)
    _paint_item(f, _ITEM_ROWS[2], False)
    return f


def _paint_item(f, r, ticked):
    x0, y0 = _board_origin()
    if ticked:
        cells = ((1, 0, 'g'), (2, 0, 'w'), (3, 0, 'g'), (1, 1, 'w'), (2, 1, 'g'), (3, 1, 'w'))
    else:
        cells = ((1, 0, 'w'), (2, 0, 'N'), (3, 0, 'w'), (1, 1, 'w'), (2, 1, 'w'), (3, 1, 'w'))
    for dx, dy, ch in cells:
        f.put(x0 + dx, y0 + r + dy, ch)


def _r_tick(state):
    f = Frame()
    if state == 'two':
        _paint_item(f, _ITEM_ROWS[1], True)
    elif state == 'three':
        _paint_item(f, _ITEM_ROWS[1], True)
        _paint_item(f, _ITEM_ROWS[2], True)
    elif state == 'fresh':
        _paint_item(f, _ITEM_ROWS[0], False)
    elif state == 'lift':                     # page turn: the old sheet curls up (then a fresh list)
        x0, y0 = _board_origin()
        rows = _board_rows()
        sheet = [(x0 + i, y0 + j) for j, r in enumerate(rows) for i, ch in enumerate(r)
                 if j >= 2 and ch in 'wgNmM']
        mid = (min(y for _, y in sheet) + max(y for _, y in sheet)) // 2
        for x, y in sheet:
            f.put(x, y, 'M' if y <= mid else 'w')
    return f


# =====================================================================================================
# Work lane: pallet, stack, crane, carrier, fx
# =====================================================================================================
def _r_pallet():
    f = Frame()
    f.place(_PALLET, STACK_X, GROUND - 1)
    return f


def _r_stack(n):
    f = Frame()
    for k in range(n):
        _crate(f, SLOT_Y[2 + k])
    return f


def _r_crane(v):
    f = Frame()
    if v is None:
        return f
    hy, load = v[0], v[1]
    dx = v[2] if len(v) > 2 else 0            # the boom slews a little as it hauls: an arc, not a lift
    top = hy - len(_HOOK) + 1
    if top > 0:                               # silver cable (the pulley block's own highlight tone)
        f.line(HOOK_X, 0, HOOK_X + dx, top - 1, 'm')
    _paint_rows(f, _HOOK, HOOK_X + dx - 1, top, crop_ok=True)
    fast = hy <= HOOK_CATCH - 6               # plain planks while it whizzes up (fewer colors)
    for k in range(load):
        _crate(f, hy + 1 + 3 * k, dx, crop_ok=True, plain=fast)
    return f


def _r_carrier(v):
    """The carrier at the stack (x 24). It is drawn the same way as in the shared walk frames (no
    stack-dependent contour), so nothing flickers when one layer hands it to the other."""
    f = Frame()
    for item in v:
        if item[0] == 'crate':                # a crate being set down: drawn behind the mini
            _crate(f, item[1])
    for item in v:
        if item[0] == 'mini':
            _, pose, i, look = item[:4]
            blink = len(item) > 4 and item[4]
            _stamp(f, _mini_sprite(pose, i, look, blink), STACK_X + 3, GROUND, crop_ok=True)
    return f


def _r_walk(v):
    f = Frame()
    if v is None:
        return f
    pose, x, i, look = v
    _stamp(f, _mini_sprite(pose, i, look), x + 3, GROUND, crop_ok=True)
    return f


def _r_fx(v):
    f = Frame()
    for item in v:
        if item[0] == 'puff':
            for x, dy, ch in _PUFF[item[2]]:
                f.put(x, item[1] + dy, ch)
        elif item[0] == 'check':
            for x, y in _CHECK[item[1]]:
                f.put(x, y, 'g')
        elif item[0] == 'clink':
            f.place(get('sparkle_small').sprite(item[1]), *_CLINK_AT)
    return f


# ---- independent ambient layers ---------------------------------------------------------------------
_TYPIST_AT = (4, GROUND)          # mini_clawd_type feet anchor: columns 1..7, rows 15..19
_KEYS_MS = 4370                   # co-prime with the 10400 ms master loop and the 9370 ms blinks


def _typist_layers():
    """Static typist + its keys (irregular bursts) + its eyes (every third pause it looks over at the
    boss, raises a hand and its lid shows a green tick: "done here!"). The raised hand also keeps the
    glancing eye inside its body."""
    a, b = Frame(), Frame()
    a.place(_TYPE.sprite(0), *_TYPIST_AT)
    b.place(_TYPE.sprite(1), *_TYPIST_AT)
    common = {p: ch for p, ch in a.px.items() if b.px.get(p) == ch}
    spr = _TYPE.sprite(0)
    holes = [(x - spr.ax + _TYPIST_AT[0], y - spr.ay + _TYPIST_AT[1]) for x, y, ch in spr.cells if ch == ERASE]
    ey = holes[0][1]
    hx0, hx1 = min(h[0] for h in holes), max(h[0] for h in holes)
    band = [(x, ey) for x in range(hx0 - 1, hx1 + 2)]
    eyes = Frame({p: common.pop(p) for p in band if p in common})
    for p in holes:
        eyes.put(p[0], p[1], EYE_INK)
    glance = Frame({p: '#' for p in band})
    for x, y in holes:
        glance.put(x + 1, y, EYE_INK)
    glance.put(hx1 + 2, ey, '#')              # the raised right hand, beside the glancing eye
    heart = [(x, y) for (x, y), ch in common.items() if ch == 'p']
    if heart:                                 # "done!": the lid's heart sticker becomes a green tick
        hx, hy = heart[0]
        for q in ((hx - 1, hy - 1), (hx + 1, hy - 1), (hx, hy)):
            glance.put(q[0], q[1], 'g')
    fa = {p: ch for p, ch in a.px.items() if p not in common and p not in eyes.px and p not in holes}
    fb = {p: ch for p, ch in b.px.items() if p not in common and p not in eyes.px and p not in holes}
    ka, kb = Frame(fa), Frame(fb)
    rest = Frame({p: ch for p, ch in list(fa.items()) + list(fb.items()) if p[1] > ey})   # hands down
    # a burst of 3 keys, a short think, one more key, a long think (4370 ms, irregular)
    keys = [(ka, 150), (kb, 140), (ka, 170), (rest, 1210), (kb, 160), (rest, 2540)]
    assert sum(ms for _, ms in keys) == _KEYS_MS
    look = [(eyes, 3 * _KEYS_MS - 900), (glance, 900)]
    return static('typist', Frame(common)), layer('typist_keys', keys), layer('typist_eyes', look)


# =====================================================================================================
def build():
    T = _tracks()
    _check_eyes(T)
    typist, typist_keys, typist_eyes = _typist_layers()
    return anim(NAME, DESC, [
        static('pallet', _r_pallet()),
        layer('stack', [(_r_stack(n), ms) for n, ms in _segments(T['stack'], LOOP)]),
        layer('crane', [(_r_crane(v), ms) for v, ms in _segments(T['crane'], LOOP)]),
        layer('walk', [(_r_walk(v), ms) for v, ms in _segments(_walk_track(), HALF)]),
        layer('carrier', [(_r_carrier(v), ms) for v, ms in _segments(T['carrier'], LOOP)]),
        layer('fx', [(_r_fx(v), ms) for v, ms in _segments(T['fx'], LOOP)]),
        typist,
        typist_keys,
        typist_eyes,
        static('body', _r_body()),
        layer('eyes', [(_r_eyes(v), ms) for v, ms in _segments(T['eyes'], LOOP)]),
        layer('arm', [(_r_arm(v), ms) for v, ms in _segments(T['arm'], LOOP)]),
        _blink_layer(),
        static('badge', _r_badge()),
        static('hat', _r_hat()),
        static('clipboard', _r_clipboard()),
        layer('tick', [(_r_tick(v), ms) for v, ms in _segments(T['tick'], LOOP)]),
    ], state=STATE)
