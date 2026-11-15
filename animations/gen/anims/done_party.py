# ======================================================================================
# USER FEEDBACK: the user reviewed this first draft personally and approved it ("i think its good").
# Keep the concept, the beats and the fine-line expressions. Critics, fixers and judges should
# polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""done-party - expressive 'done' variant: Clawd throws himself a little party.

Expressive style pilot (STYLE.md 0b): his face acts with the fine-line kit in every frame
(fine(frame) + fine_face(...)): sparkle eyes, thin lines, ◠◠ arcs, a wink, ◡◡ cups. No mouth, no
blush, normal body size throughout.

Storyboard (ms; one 7970 ms loop; everything runs on the same clock)
     0  "IT'S DONE!"  At HOME: party hat on, a loaded party popper held up in his right hand,
        his eyes TWINKLE (a second glint) with the big "ding!" star beside his head ... 140
        SPARKLE eyes hold while the star fades (gone by 590).
        (Frame 0 = the reduced-motion still: hat + popper + twinkling eyes + star + gift.)
   700  brace: eyes squeezed shut (thin lines), popper pulled down to his side, free arm out
   880  POP!  popper thrust up (library frame 1 + the confetti_burst flash): eyes go WIDE
   970  ◠◠ delighted squint while 8 library confetti pieces (all six kinds) fountain out of the
        popper (drag arcs: they shoot up, fan out, stall, then flutter down at their own speeds;
        heavy strips and curls fall fast, light flakes float). His free arm WAVES on the burst's
        own ticks: out (970), up (1150), out (1280). The cyan ribbon shoots up the popper's line
        and catches the air in the top-right corner.
  1610  his eyes open (half ... 1680 open): arm down, he looks right at you (330) ...
  2010  ... and WINKS (half ... 2070 ◠ + open), a tiny star twinkling by the closed eye ...
        2590 the wink opens (half) ...
  2650  wind-up: popper down to his side, eyes on it ... 2810 FLUNG: it leaves his hand on the
        tick his arms go up, spins up through the hanging ribbon and out of the top-right corner
        (2880) ... 2950 PROUD V pose, ◠◠ (540), and the ribbon, knocked loose, drops a cell and
        flutters down the right edge
  3490  anticipation: arms swing down, eyes shut (no crouch: normal body size)
  3650  JUMP: whole body up 2 cells, legs tucked ... 3720 apex (3 up, arms flung wide) ...
        3940 falling: the hat hangs in the air ... 4010 THUMP: home, eyes shut, dust_puff,
        the hat still a cell above his head ... 4100 the hat lands a beat late, its pom-pom
        flopping right; the thump makes the gift box hop. Nothing falls behind him, so the
        jump never uncovers confetti under his feet.
  4220  CONTENT ◡◡ glow, the long calm: two soft twinkles a tick apart (4340, 4460) while the
        last confetti drifts down on both sides (the slow violet flake between him and the
        gift, the ribbon down the right edge), gone past row 19 by 5190 ... a long quiet hold
  6920  eyes open (half ... 7000 open), he looks at you ... 7320 he hears something: looks up,
        hand ready, a glint up in the top-right corner (7460) ...
  7720  a fresh popper drops back in from the top, spinning, as the "ding!" twinkle starts to
        bloom ... 7790 he reaches up ... 7860 CATCH (eyes wide) ... 7970 = frame 0: popper
        lowered, twinkling eyes, big star - again!
Layers (back to front): confetti (behind Clawd, his hat, the popper and the gift; cells they hide
are left out) | body (normal res) | face (fine overlay: only his half-size eye pixels) | hat |
popper | fx (twinkles, dust) | gift (in front: the dust rolls behind it). Body, face, hat and popper
are built from the same beat list, so they never drift apart.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'done-party'
STATE = 'Done variant (expressive style): celebration'
DESC = ('Sparkle-eyed "it\'s done!", pops a party popper with a delighted squint, winks at you, '
        'tosses the popper, jumps for joy and glows contentedly while the confetti falls.')

_HAT = get('party_hat')
_POPPER = get('party_popper')
_GIFT = get('gift_box')
_DUST = get('dust_puff')
_SPARK = get('sparkle')
_SPARK_S = get('sparkle_small')
_BURST = get('confetti_burst')
# Library confetti, each piece in ONE color (the tumble is in the shape): at 3 px a cell the
# two-tone flicker does not read, and every extra color costs bytes in every confetti frame.
_ONE = {'a': {'p': 'r', 'R': 'r'}, 'b': {'b': 'c'}, 'c': {'o': 'j'}, 'd': {'g': 'c', 'G': 'c'},
        'e': {'p': 'r'}, 'f': {'l': 'v'}}
_CONF = {k: [s.recolor(_ONE[k]) for s in get('confetti_' + k).frames] for k in 'abcdef'}


def _hat_flop():
    """The library party hat with its pom-pom (top three rows) flopped one cell right: worn on
    the frame the hat lands, a beat after Clawd (follow-through)."""
    s = _HAT.sprite(0)
    top = s.y0 + 2
    cells = [(x + 1 if y <= top else x, y, ch) for x, y, ch in s.cells]
    return Item('party_hat_flop', 'head', 'party hat, pom-pom flopped right', Sprite(cells=cells, anchor=(s.ax, s.ay)))


_HAT_FLOP = _hat_flop()


# ------------------------------------------------------------------ helpers
def _rot(spr, q):
    """Sprite turned q quarter turns clockwise (screen coords), anchor included (lossless)."""
    cells, ax, ay = list(spr.cells), spr.ax, spr.ay
    for _ in range(q % 4):
        cells = [(-y, x, ch) for x, y, ch in cells]
        ax, ay = -ay, ax
    return Sprite(cells=cells, anchor=(ax, ay), name=spr.name)


def _put_in(f, spr, x, y):
    """Place spr (anchor on (x, y)) keeping only the cells inside the canvas: for things that
    deliberately fly in or out across an edge."""
    for sx, sy, ch in spr.cells:
        px, py = x + sx - spr.ax, y + sy - spr.ay
        if 0 <= px < W and 0 <= py < H:
            f.put(px, py, ch)


def _put_center(f, spr, cx, cy):
    """Place spr with the middle of its drawn pixels on (cx, cy), clipped to the canvas."""
    _put_in(f, spr.with_anchor((spr.x0 + spr.x1) // 2, (spr.y0 + spr.y1) // 2), cx, cy)


# ------------------------------------------------------------------ Clawd: body (normal) + face (fine)
def _clawd_split(pose, x, y, left, right):
    """Clawd drawn the normal way, his face drawn with the fine-line kit (fine + fine_face), then
    split into a normal-res body and a fine overlay that only holds the half-size face pixels.
    The pose is built with blink eyes, so the body has no eye cells and the overlay only holds
    the ink and glints. The two layers composite to exactly fine(frame) + fine_face(...), at a
    fraction of the size, and the body frames merge while only his face acts.
    'glint' = sparkle eyes with a second glint at the bottom-right (the sparkle twinkles)."""
    f = Frame()
    put_clawd(f, pose, x, y)
    ff = fine(f)
    fine_face(ff, pose, x, y, *['sparkle' if e == 'glint' else e for e in (left, right)])
    for e, key in zip((left, right), ('eye_l', 'eye_r')):
        if e == 'glint':
            ex, ey = pose.at(key, x, y)
            ff.put(2 * ex + 1, 2 * ey + 1, 'W')
    face = Frame(res=2)
    face.meta = {'fine_face': [(left, right)]}
    for key in ('eye_l', 'eye_r'):
        ex, ey = pose.at(key, x, y)
        for cy in range(ey - 1, ey + 2):
            for cx in range(ex - 1, ex + 2):
                quad = [(2 * cx + k % 2, 2 * cy + k // 2) for k in range(4)]
                b = f.px.get((cx, cy))
                if any(ff.px.get(q) is None for q in quad):      # see-through eye pixels (if the
                    f.px.pop((cx, cy), None)                     # kit ever goes back to holes)
                    b = None
                for q in quad:
                    if ff.px.get(q) not in (None, b):
                        face.px[q] = ff.px[q]
    return f, face


# ------------------------------------------------------------------ the main timeline
# (ms, larm, rarm, legs, body dy, (left eye, right eye), hat dy (or 'flop'), popper, tag)
#   popper: ('hand', item frame) | ('fly', item frame, center x, center y, quarter turns) | None
_TOSS = [('fly', 2, 24, 5, 1), ('fly', 2, 27, 0, 2)]      # the spent popper spins up and away
_BACK = [('fly', 0, 25, 0, 2), ('fly', 0, 25, 2, 3)]      # ... and a loaded one drops back in
_BEATS = [
    (140, 'side', 'up', 'stand', 0, ('glint', 'glint'), 0, ('hand', 0), 'start'),   # his eyes twinkle with the "ding!"
    (560, 'side', 'up', 'stand', 0, ('sparkle', 'sparkle'), 0, ('hand', 0), ''),
    (180, 'out', 'side', 'stand', 0, ('line', 'line'), 0, ('hand', 0), 'brace'),
    (90, 'out', 'raise', 'stand', 0, ('wide', 'wide'), 0, ('hand', 1), 'pop'),
    (180, 'wave', 'raise', 'stand', 0, ('happy', 'happy'), 0, ('hand', 2), 'yay'),   # the free arm waves
    (130, 'raise', 'raise', 'stand', 0, ('happy', 'happy'), 0, ('hand', 2), ''),     # (out, up, out) on the
    (330, 'wave', 'raise', 'stand', 0, ('happy', 'happy'), 0, ('hand', 2), ''),      # burst's own ticks
    (70, 'wave', 'raise', 'stand', 0, ('half', 'half'), 0, ('hand', 2), ''),
    (330, 'side', 'raise', 'stand', 0, ('open', 'open'), 0, ('hand', 2), 'look'),
    (60, 'side', 'raise', 'stand', 0, ('half', 'open'), 0, ('hand', 2), 'wink'),
    (520, 'side', 'raise', 'stand', 0, ('happy', 'open'), 0, ('hand', 2), ''),
    (60, 'side', 'raise', 'stand', 0, ('half', 'open'), 0, ('hand', 2), ''),       # the wink opens
    (160, 'side', 'side', 'stand', 0, ('look_r', 'look_r'), 0, ('hand', 2), 'windup'),
    (70, 'raise', 'raise', 'stand', 0, ('happy', 'happy'), 0, _TOSS[0], 'throw'),   # it leaves his hand
    (70, 'raise', 'raise', 'stand', 0, ('happy', 'happy'), 0, _TOSS[1], ''),        # as his arms go up
    (540, 'raise', 'raise', 'stand', 0, ('happy', 'happy'), 0, None, 'proud'),
    (160, 'down', 'down', 'stand', 0, ('line', 'line'), 0, None, 'antic'),
    (70, 'raise', 'raise', 'short', -2, ('happy', 'happy'), 0, None, 'launch'),
    (220, 'wave', 'wave', 'short', -3, ('happy', 'happy'), 0, None, 'apex'),
    (70, 'raise', 'raise', 'stand', -2, ('happy', 'happy'), -1, None, 'fall'),
    (90, 'down', 'down', 'stand', 0, ('line', 'line'), -1, None, 'land'),
    (120, 'side', 'side', 'stand', 0, ('happy', 'happy'), 'flop', None, 'settle'),
    (2700, 'side', 'side', 'stand', 0, ('content', 'content'), 0, None, 'content'),
    (80, 'side', 'side', 'stand', 0, ('half', 'half'), 0, None, ''),
    (320, 'side', 'side', 'stand', 0, ('open', 'open'), 0, None, 'awake'),
    (400, 'side', 'up', 'stand', 0, ('look_u', 'look_u'), 0, None, 'lookup'),
    (70, 'side', 'up', 'stand', 0, ('look_u', 'look_u'), 0, _BACK[0], 'drop'),
    (70, 'side', 'raise', 'stand', 0, ('look_u', 'look_u'), 0, _BACK[1], ''),
    (110, 'side', 'raise', 'stand', 0, ('wide', 'wide'), 0, ('hand', 0), 'catch'),
]
LOOP = sum(b[0] for b in _BEATS)


def _starts():
    out, t = [], 0
    for b in _BEATS:
        out.append(t)
        t += b[0]
    return out


_T = _starts()
_TAG = {b[8]: t for b, t in zip(_BEATS, _T) if b[8]}


def _pose(b):
    # blink: no eye cells in the body; the fine face overlay draws his eyes
    return clawd(eyes='blink', larm=b[1], rarm=b[2], legs=b[3])


_CF = {}


def clawd_frames():
    """(body, face, hat, popper) frame lists, one entry per beat (cached: the confetti culling
    reads them too)."""
    if not _CF:
        body, face, hat, pop = [], [], [], []
        for b in _BEATS:
            ms, dy = b[0], b[4]
            p = _pose(b)
            x, y = HOME[0], HOME[1] + dy
            bf, fc = _clawd_split(p, x, y, b[5][0], b[5][1])
            body.append((bf, ms))
            face.append((fc, ms))
            hf = Frame()
            if b[6] == 'flop':
                wear(hf, _HAT_FLOP, p, x, y)
            else:
                wear(hf, _HAT, p, x, y, dy=b[6])
            hat.append((hf, ms))
            pf = Frame()
            if b[7] is not None:
                if b[7][0] == 'hand':
                    wear(pf, _POPPER, p, x, y, i=b[7][1])
                    if b[7][1] == 1:                        # POP: the library burst's flash
                        pf.place(_BURST.sprite(0), *_MOUTH)
                else:
                    _, i, cx, cy, q = b[7]
                    _put_center(pf, _rot(_POPPER.sprite(i), q), cx, cy)
            pop.append((pf, ms))
        _CF['frames'] = (body, face, hat, pop)
    return tuple([(f.copy(), ms) for f, ms in lst] for lst in _CF['frames'])


# ------------------------------------------------------------------ confetti (behind everything)
_MOUTH = (26, 6)       # the popper's mouth while he holds it up ('raise'): grip (21, 11) + (5, -5)
# Drag physics: a piece leaves the mouth, rises h cells while it eases out to dx cells sideways
# (the sideways drag is slower than the rise, _KX, so pieces leave the cone going UP and then fan
# out: a fountain, not a flat streak), stalls, then falls at its terminal speed vt with a sideways
# flutter. Heavy bits (strips, curls) fall fast, light flakes float.
# (type, launch delay ms, dx, h, vt cells/s, k drag 1/s, flutter amp, Hz, phase, tumble offset, color)
_KX = 0.45
# Nothing falls behind Clawd: a piece sinking behind him would peek out between his legs and be
# uncovered by the jump. Every piece rains down left of him, right of him, or behind the gift.
_PIECES = [
    # over his head (clear of the hat tip, rows 1-3), raining down to the left of him
    # the LAST FLAKE: floats down between him and the gift; its path is tuned so that after the
    # burst it never touches him (raised hands, the jump's flung arms), the gift or a twinkle
    ('f', 40, -19.2, 5.0, 4.98, 7.5, 0.5, 0.34, 1.22, 0, None),
    # a heavy strip: slips behind the hat's left slope and drops out behind his left leg
    ('e', 30, -15.0, 4.0, 13.0, 6.0, 0.3, 1.1, 2.0, 1, None),
    ('c', 10, -23.0, 3.5, 7.5, 6.0, 0.5, 1.3, 4.0, 2, 'v'),    # violet: a gold curl would melt into the gift's bow
    # the RIBBON shoots up the popper's line and catches the air in the top-right corner (barely
    # sinking), until the flung popper sails through it and knocks it loose (_KNOCK): then it
    # flutters down the right edge, the counterweight to the last flake on the left
    ('d', 20, 1.4, 5.0, 0.6, 6.5, 0.9, 1.1, 0.5, 0, None),
    # up and down the right side, peaking at different heights
    ('a', 0, -5.0, 2.5, 9.0, 6.0, 0.4, 1.2, 0.0, 2, None),
    ('b', 40, -2.5, 2.5, 7.6, 6.5, 0.7, 0.8, 5.0, 1, None),
    ('f', 20, -0.5, 3.5, 6.8, 7.5, 1.0, 0.6, 2.5, 3, None),
    ('c', 0, 1.5, 3.5, 8.0, 6.0, 0.4, 1.3, 1.0, 0, 'r'),      # red: 3 confetti colors, not 4 (bytes)
]
# piece -> (age when it is knocked loose, fall speed after that, the knock's jolt in cells): the
# ribbon drops the moment the tossed popper has sailed through it (out of the top-right corner)
_KNOCK = {[p[0] for p in _PIECES].index('d'): (_TAG['proud'] - _TAG['pop'], 8.0, 1.0)}


def _lift_for(h, vt, k):
    """C such that the drag arc peaks h cells above the start (bisection)."""
    lo, hi = vt / k * 1.0001, 400.0
    for _ in range(60):
        c = (lo + hi) / 2
        if c - vt / k - (vt / k) * math.log(c * k / vt) < h:
            lo = c
        else:
            hi = c
    return (lo + hi) / 2


_C = [_lift_for(p[3], p[4], p[5]) for p in _PIECES]


def _piece_xy(i, age_ms):
    """Cell of piece i at age_ms after the pop (None before its launch)."""
    typ, delay, dx, h, vt, k, amp, hz, ph = _PIECES[i][:9]
    t = (age_ms - delay) / 1000.0
    if t < 0:
        return None
    e = 1 - math.exp(-k * t)
    x = _MOUTH[0] + dx * (1 - math.exp(-_KX * k * t)) + amp * e * math.sin(2 * math.pi * hz * t + ph)
    y = _MOUTH[1] + vt * t - _C[i] * e
    if i in _KNOCK:                 # caught in the air until the flung popper knocks it loose
        age_k, vt_k, kick = _KNOCK[i]
        tk = (age_k - delay) / 1000.0
        if t >= tk:
            y += kick + (vt_k - vt) * (t - tk)
    return int(round(x)), int(round(y))


def _piece_sprite(i, n):
    p = _PIECES[i]
    frames = _CONF[p[0]]
    spr = frames[(p[9] + n) % len(frames)]
    if p[10]:
        spr = spr.recolor({ch: p[10] for _, _, ch in spr.cells})
    return spr


def _alive(i, a):
    xy = _piece_xy(i, a)
    return xy is None or xy[1] <= GROUND


_STEP = 320             # the flutter-down after the burst: one step per ~1.5-3 cells of fall


def _event_times():
    """Every beat start and fx change (absolute ms)."""
    ts = set(_T)
    for start, _, seq in _fx_events():
        for _, ms in seq:
            ts.add(start)
            start += ms
        ts.add(start)
    return sorted(ts)


def _ages():
    """Frame ages after the pop: quick steps through the burst (the first lands on the yay beat),
    then ~_STEP ms steps spaced so that one lands exactly on the knock (the ribbon drops the moment
    the popper clears it). A step within 45 ms of a beat or fx change is moved onto it, so the
    layers change together (no sliver moments of a few ms)."""
    t_pop = _TAG['pop']
    ages = [_TAG['yay'] - t_pop, 170, 270, 400, 560]
    knock = min(v[0] for v in _KNOCK.values())
    n = max(1, int(round((knock - ages[-1]) / float(_STEP))))
    a0 = ages[-1]
    steps = [a0 + (knock - a0) * j / float(n) for j in range(1, n)]
    a, tail = knock, []
    while True:
        a += _STEP
        tail.append(a)
        if not any(_alive(i, a) for i in range(len(_PIECES))):
            break
    snaps = [s - t_pop for s in _event_times()]

    def snap(v):
        best = min(snaps, key=lambda s: abs(s - v))
        return best if abs(best - v) <= 45 else v
    for v in [snap(v) for v in steps] + [knock] + [snap(v) for v in tail[:-1]] + [tail[-1]]:
        v = int(round(v))
        if v - ages[-1] >= 100:
            ages.append(v)
    return ages


_AGES = []


def _ages_list():
    if not _AGES:
        _AGES.extend(_ages())
    return _AGES


_COVER = {}


def _covered(t, until):
    """Cells hidden for the whole span [t, until) by the layers drawn over the confetti (Clawd's
    body, his hat, the popper, the gift): confetti there is left out (same picture, smaller SVG)."""
    if not _COVER:
        body, _, hat, pop = clawd_frames()
        _COVER['clawd'] = [(t0, t0 + _BEATS[k][0], set(body[k][0].px) | set(hat[k][0].px) | set(pop[k][0].px))
                           for k, t0 in enumerate(_T)]
        spans, g0 = [], 0
        for f, ms in gift_frames():
            spans.append((g0, g0 + ms, set(f.px)))
            g0 += ms
        _COVER['gift'] = spans
    sets = []
    for s0, e0, c0 in _COVER['clawd']:
        for s1, e1, c1 in _COVER['gift']:
            if max(s0, s1, t) < min(e0, e1, until):
                sets.append(c0 | c1)
    return set.intersection(*sets) if sets else set()


def confetti_frames():
    t_pop = _TAG['pop']
    ages = _ages_list()
    out = [(Frame(), t_pop + ages[0])]
    for n, a in enumerate(ages):
        t = t_pop + a
        end = min(t_pop + ages[n + 1] if n + 1 < len(ages) else LOOP, LOOP)
        f = Frame()
        hidden = _covered(t, end)
        for i in range(len(_PIECES)):
            xy = _piece_xy(i, a)
            if xy is None or xy[1] > GROUND:
                continue
            spr = _piece_sprite(i, n)
            for sx, sy, ch in spr.cells:
                px, py = xy[0] + sx - spr.ax, xy[1] + sy - spr.ay
                if (px, py) not in hidden and 0 <= px < W and 0 <= py <= GROUND:
                    f.put(px, py, ch)
        out.append((f, end - t))
    return out


# ------------------------------------------------------------------ one-shot effects (in front)
def _seq(item, idx, ms):
    return [(item.sprite(i), m) for i, m in zip(idx, ms)]


def _fx_events():
    c = _TAG['content']
    return [
        (0, (7, 9), _seq(_SPARK, [2, 1], [460, 130])),                                # "ding!"
        (_TAG['wink'], (8, 11), _seq(_SPARK_S, [1, 2, 1], [110, 120, 90])),           # the wink's star (a cell clear of him)
        (_TAG['land'], (15, GROUND - 1), _seq(_DUST, [0, 1, 2], [90, 120, 120])),
        (c + 120, (7, 11), _seq(_SPARK_S, [1, 2, 1], [120] * 3)),                     # the glow: two soft
        (c + 240, (23, 9), _seq(_SPARK_S, [2, 1], [120] * 2)),                        # twinkles: the 2nd pops in a tick later
        (_TAG['lookup'] + 140, (25, 2), _seq(_SPARK_S, [1], [260])),                  # something up there
        (_TAG['drop'], (7, 9), _seq(_SPARK, [1], [250])),                             # "ding!" blooms into frame 0
    ]


def fx_frames():
    events = _fx_events()
    times = {0}
    for start, _, seq in events:
        t = start
        for _, ms in seq:
            times.add(t)
            t += ms
        times.add(t)
    ts = sorted(x for x in times if x < LOOP)
    out = []
    for i, t in enumerate(ts):
        end = ts[i + 1] if i + 1 < len(ts) else LOOP
        f = Frame()
        for start, (x, y), seq in events:
            tt = t - start
            for spr, ms in seq:
                if 0 <= tt < ms:
                    f.place(spr, x, y)
                    break
                tt -= ms
        out.append((f, end - t))
    return out


# ------------------------------------------------------------------ scenery
GIFT_AT = (3, GROUND)          # bottom-center of the gift box (it spans x 1-5)


def gift_frames():
    """The gift on the input box; the landing thump makes it hop one cell."""
    g = _GIFT.sprite(0).with_anchor(2, 5)
    rest, hop = Frame(), Frame()
    rest.place(g, *GIFT_AT)
    hop.place(g, GIFT_AT[0], GIFT_AT[1] - 1)
    t = _TAG['settle']
    return [(rest, t), (hop, 120), (rest.copy(), LOOP - t - 120)]


def build():
    body, face, hat, pop = clawd_frames()
    layers = [
        layer('confetti', confetti_frames()),
        layer('body', body),
        layer('face', face),
        layer('hat', hat),
        layer('popper', pop),
        layer('fx', fx_frames()),
        layer('gift', gift_frames()),
    ]
    return anim(NAME, DESC, layers, state=STATE)
