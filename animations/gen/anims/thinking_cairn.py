"""thinking-cairn - Thinking variant: zen stone stacking.   Preview:  python3 gen/preview.py anim thinking-cairn

STORYBOARD (ms)   one loop = 14 650 ms; calm, one small payoff (a sparkle on the finished cairn) per loop
  Scene: right of Clawd a gray boulder; on it he stacks three rounded pebbles (a broad tan one, a silver one, a small
  brown one), each two cells tall, into a straight little cairn whose top rises above his head.  The loose pebbles lie
  in a heap in front of the boulder's foot.  He pinches each pebble by its left end with his right claw; his eyes
  always get there first (the heap, then the stone, then the spot on the cairn).
     0  frame 0 = the reduced-motion still: Clawd at HOME holding the tan pebble over the boulder, eyes on it
        (look_r), the silver and brown pebbles waiting on the ground.  He considers it; a glance at the spot.
  1300  wind-up: the stone lifts a row, then he sets it down (two steps) and lets go (the claw drops away).
  1900  it WOBBLES (tips right, tips left): his eyes go wide, 2180 his claw shoots out and steadies it; it holds:
        2600 a calm closed-eye moment (half, line 0.5 s, half), and the claw lets go.
  3900  eyes to the heap; he reaches down for the silver pebble (reach, grip), lifts it beside his head (4530),
        eyes on the cairn, brings it over (hover, then one row above its spot) and considers it; 5300 a glance at
        you ("hm?"); 5900 wind-up, down, placed: it settles with a little tip and holds.  6600 a blink.
  7100  the small brown pebble: eyes to the heap, reach, grip, lift high, over the cairn (7870); a long consideration
        with his eyes on it; 9070 a small pull back (anticipation), forward, placed on top.
  9640  the top two WOBBLE: wide eyes, 9920 the claw steadies them, 10300 the calm closed-eye moment.
 11100  he lets go: it holds.  A sparkle grows on top of the finished cairn and fades, sparkle in his eyes.
 12100  ... then the top two tip and slide off, falling onto the heap one after the other (the brown one bounces),
        and the tan one slumps after them: soft clacks and little puffs of dust.  His eyes go wide, follow them
        down, droop and close for a calm moment: no matter.
 13930  eyes on the tan pebble on top of the heap; he picks it up and lifts it over the boulder -> frame 0.
Eye closures: 2.60 (calm), 6.60, 10.30 (calm), 13.40 (calm) s.

Face rig (as in thinking.py): the body layer draws him with a solid face; the face layer (FINE, half-size pixels)
holds only his black eye pixels.  Fine-line faces used: open, half, line, look_r (+ a half-step up or down for the
heap or a raised stone), wide, sparkle.  He never changes size: every reach is his arm alone (arm shapes drawn here
at normal cell size, 2-3 cells long like the kit's).
Layers: boulder (static) | stones (the three pebbles: heap, cairn, wobbles, topple) | body (Clawd + the pebble in
his claw, in front of the cairn) | face | fx (sparkle, clacks, dust).  All share LOOP.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'thinking-cairn'
STATE = 'thinking (variant)'
DESC = ('Zen focus: stacks rounded pebbles into a little cairn on a boulder beside him, considering each one; he '
        'steadies the wobbles with a claw and a calm blink, a sparkle crowns it, then the top stones topple back '
        'onto the heap and he starts again.')

# --------------------------------------------------------------------------------------------
# Stones (top-left anchored).  Mid-tone stone colours (N m s t T): they read on both themes; light from the top-left.
# --------------------------------------------------------------------------------------------
_BOULDER = Sprite(['.sssssss.',
                   'sNNNNNNNN',
                   'NNNNNNNNN'], anchor=(0, 0))          # cols 21-29, rows 17-19
BOULDER_AT = (21, 17)
STONES = {
    'tan':    Sprite(['.tttt.',
                      'ttTTTT'], anchor=(0, 0)),         # 6 x 2: the broad bottom pebble
    'silver': Sprite(['.mm.',
                      'sssN'], anchor=(0, 0)),           # 4 x 2
    'brown':  Sprite(['.t.',
                      'TTT'], anchor=(0, 0)),            # 3 x 2: the little top one
}
# The cairn: centred on col 24-25 above the boulder, every pebble's left end within reach of his claw (col 22-23).
STACK = {'tan': (22, 15), 'silver': (23, 13), 'brown': (23, 11)}
# The heap in front of the boulder's foot: brown and silver on the ground, tan lying across them.
HEAP = {'brown': (20, 18), 'silver': (23, 18), 'tan': (21, 16)}


def _stone(name, tilt=0):
    """A pebble, optionally tipped: tilt +1 lifts its right half a row (it slopes down to the left), -1 its left."""
    s = STONES[name]
    if not tilt:
        return s
    half = s.w / 2.0
    return Sprite(cells=[(x, y - (1 if ((x >= half) if tilt > 0 else (x < half)) else 0), c) for x, y, c in s.cells],
                  anchor=(0, 0))


# --------------------------------------------------------------------------------------------
# Clawd's right arm: canvas cells (he is always at HOME); None = the kit's resting arm.
# --------------------------------------------------------------------------------------------
_ARMS = {
    'side':  None,
    'down':  [(20, 15), (20, 16)],                 # kit 'down': also the grip on the tan pebble in the heap
    'out':   [(20, 14), (21, 14)],                 # tip (21, 14)
    'up':    [(20, 13), (20, 14)],                 # kit 'up': tip (20, 13)
    'high':  [(20, 12), (20, 13), (20, 14)],       # kit 'high': tip (20, 12)
    'h15':   [(20, 14), (21, 15)],                 # tip (21, 15)
    'h16':   [(20, 15), (21, 16)],                 # tip (21, 16)
    'r11':   [(20, 13), (21, 12), (22, 11)],       # tip (22, 11)
    'b11':   [(20, 13), (21, 12), (21, 11)],       # tip (21, 11): pulled back
    'r12':   [(20, 14), (21, 13), (22, 12)],       # kit 'wave': tip (22, 12)
    'r13':   [(20, 14), (21, 13), (22, 13)],       # tip (22, 13)
    'r14':   [(20, 14), (21, 14), (22, 14)],       # kit 'point': tip (22, 14)
    'rel':   [(20, 14), (21, 13)],                 # letting go upward
    'pick2': [(20, 16), (21, 17), (22, 18)],       # down to the silver pebble's left end
    'pick3': [(20, 15), (20, 16), (21, 17)],       # down onto the brown pebble
}


def _pose(arm):
    if _ARMS[arm] is None:
        return clawd(eyes='blink')
    p = clawd(eyes='blink', rarm='none')
    hx, hy = HOME
    spr = p.sprite.over(Sprite(cells=[(x - hx, y - hy, '#') for x, y in _ARMS[arm]], anchor=(0, 0)))
    return Pose(spr, p.anchors, dict(p.spec, rarm=arm))


def _body(state):
    arm, held = state
    f = Frame()
    put_clawd(f, _pose(arm))
    if held:
        name, x, y = held
        f.place(STONES[name], x, y)
    return f


# --------------------------------------------------------------------------------------------
# Face (fine eye ink only), with a half-step gaze: 'shape' or 'shape/gaze'
# --------------------------------------------------------------------------------------------
_GAZE = {'': (0, 0), 'u': (0, -1), 'd': (0, 1)}
_FACE_BASE = fine(_body(('side', None)))


def _eyes(expr):
    shape, _, gz = expr.partition('/')
    if shape in ('happy', 'content', 'squint'):
        raise ValueError('the user dislikes %r eyes' % shape)
    ff = fine_face(_FACE_BASE.copy(), _pose('side'), expr=shape)
    gx, gy = _GAZE[gz]
    out = Frame(res=2)
    for (x, y), c in ff.px.items():
        if _FACE_BASE.px.get((x, y)) != c:
            out.px[(x + gx, y + gy)] = c
    out.meta = {'fine_face': [expr]}
    return out


# --------------------------------------------------------------------------------------------
# fx: every effect grows in and fades out
# --------------------------------------------------------------------------------------------
_SPARK = get('sparkle')                                  # gold: dot, plus, star, long plus
SPARK_AT = (24, 7)                                       # above the top pebble (its top is row 11)
_CLACK = [{(-1, -1): 'm', (1, -1): 'm'},                 # soft clack: two ticks over the impact ...
          {(-2, -1): 'N', (2, -1): 'N'}]                 # ... spreading and dimming
_DUST = [{(-1, 0): 't', (1, 0): 't'},                    # a little puff at both ends of the landing pebble ...
         {(-2, 0): 't', (2, 0): 't', (-1, -1): 't', (1, -1): 't'},
         {(-3, -1): 't', (3, -1): 't'}]                  # ... thinning out


def _fx(items):
    f = Frame()
    for kind, i, x, y, w in items:
        if kind == 'spark':
            f.place(_SPARK.sprite(i), *SPARK_AT)
        elif kind == 'clack':
            for (dx, dy), c in _CLACK[i].items():
                f.put(x + (dx if dx < 0 else w - 1 + dx), y + dy, c)
        elif kind == 'dust':
            for (dx, dy), c in _DUST[i].items():
                f.put(x + (dx if dx < 0 else w - 1 + dx), y + 1 + dy, c)
    return f


# --------------------------------------------------------------------------------------------
# The story: beats (t, arm, held stone or None, stone moves); stones = {name: (x, y, tilt)} lying in the world.
# --------------------------------------------------------------------------------------------
LOOP = 14650


def _story():
    rows = []
    st = {'silver': HEAP['silver'] + (0,), 'brown': HEAP['brown'] + (0,)}

    def beat(t, arm, held=None, moves=None):
        for k, v in (moves or {}).items():
            if v is None:
                st.pop(k, None)
            else:
                st[k] = v if len(v) == 3 else tuple(v) + (0,)
        rows.append((t, (arm, held), dict(st)))

    def at(name, tilt=0, dx=0, dy=0):
        x, y = STACK[name]
        return (x + dx, y + dy, tilt)

    A, B, C = 'tan', 'silver', 'brown'
    # ---- the tan pebble (frame 0: holding it one row over its spot) ----
    beat(0, 'h15', (A, 22, 14))
    beat(1300, 'out', (A, 22, 13))                     # wind-up: it lifts a row ...
    beat(1420, 'h15', (A, 22, 14))                     # ... and comes down ...
    beat(1510, 'h16', None, {A: at(A)})                # ... onto the boulder
    beat(1730, 'down')                                 # the claw drops away ...
    beat(1830, 'side')
    beat(1900, 'side', None, {A: at(A, 1)})            # WOBBLE: tips right ...
    beat(2040, 'side', None, {A: at(A, -1)})           # ... and left ...
    beat(2180, 'h16', None, {A: at(A, 1)})             # ... his claw shoots out ...
    beat(2290, 'h16', None, {A: at(A)})                # ... and steadies it: it holds
    beat(3500, 'down')
    beat(3600, 'side')
    # ---- the silver pebble ----
    beat(4150, 'h16')                                  # reaching down ...
    beat(4250, 'pick2')                                # ... grip
    beat(4430, 'h15', (B, 22, 14), {B: None})          # lifted (in front of the cairn) ...
    beat(4530, 'up', (B, 21, 12))                      # ... up beside his head
    beat(4680, 'r12', (B, 23, 11))                     # over the cairn (hover) ...
    beat(4810, 'r13', (B, 23, 12))                     # ... one row above its spot: considering
    beat(5900, 'r12', (B, 23, 11))                     # wind-up
    beat(6010, 'r13', (B, 23, 12))
    beat(6100, 'r14', None, {B: at(B, 1)})             # placed: it settles with a little tip ...
    beat(6200, 'r14', None, {B: at(B)})                # ... and sits
    beat(6300, 'out')                                  # letting go
    beat(6400, 'side')
    # ---- the brown pebble ----
    beat(7350, 'down')                                 # reaching down ...
    beat(7450, 'pick3')                                # ... grip
    beat(7620, 'h15', (C, 22, 14), {C: None})          # lifted ...
    beat(7720, 'high', (C, 21, 11))                    # ... high beside his head ...
    beat(7870, 'r11', (C, 23, 10))                     # ... over the cairn: a long consideration
    beat(9070, 'b11', (C, 22, 10))                     # a small pull back ...
    beat(9180, 'r11', (C, 23, 10))                     # ... forward ...
    beat(9270, 'r12', None, {C: at(C)})                # ... placed on top
    beat(9470, 'rel')
    beat(9560, 'side')
    beat(9640, 'side', None, {B: at(B, 1), C: at(C, 1)})       # WOBBLE 2: the top two
    beat(9780, 'side', None, {B: at(B, -1), C: at(C, -1)})
    beat(9920, 'r14', None, {B: at(B, 1), C: at(C, 1)})        # the claw steadies them
    beat(10030, 'r14', None, {B: at(B), C: at(C)})
    beat(11100, 'out')                                 # he lets go: it holds
    beat(11200, 'side')
    # ---- the topple: the top two tip and slide off onto the heap, the tan one slumps after them ----
    beat(12100, 'side', None, {B: at(B, 1), C: at(C, 1)})
    beat(12260, 'side', None, {C: (22, 12, 1)})
    beat(12350, 'side', None, {C: (21, 14, 1), B: (22, 14, 1)})
    beat(12430, 'side', None, {C: (20, 16, 1), B: (22, 16, 1)})
    beat(12500, 'side', None, {C: HEAP[C], B: (23, 17, 1)})            # brown lands ...
    beat(12570, 'side', None, {C: (20, 17, 0), B: HEAP[B]})            # ... bounces; silver lands
    beat(12640, 'side', None, {C: HEAP[C], A: at(A, 1)})               # brown settles; tan tips ...
    beat(12730, 'side', None, {A: HEAP[A]})                            # ... and slumps onto the heap
    # ---- back to the tan pebble ----
    beat(14150, 'down')                                # grip (on the heap) ...
    beat(14350, 'side', (A, 21, 14), {A: None})        # ... lifts it (-> frame 0)
    return rows


def _face_track():
    R, Rd, Ru = 'look_r', 'look_r/d', 'look_r/u'
    return [
        (0, R),
        (700, Rd), (1100, R),                                            # a glance at the spot
        (1300, Rd),                                                      # eyes on the spot first, then it goes down
        (1980, 'wide'),                                                  # the wobble
        (2600, 'half'), (2680, 'line'), (3230, 'half'), (3310, R),       # it holds: a calm closed-eye moment
        (3900, Rd),                                                      # to the heap ...
        (4430, R), (4530, Ru),                                           # ... up with the stone ...
        (4680, R),                                                       # ... the spot on the cairn
        (5300, 'open'), (5800, R),                                       # "hm?": a glance at you
        (5900, Rd),                                                      # placing it
        (6600, 'half'), (6670, 'line'), (6750, 'half'), (6820, R),       # blink
        (7100, Rd),                                                      # to the heap
        (7620, R), (7720, Ru),                                           # up with the little one
        (9070, R),                                                       # anticipation: the spot
        (9720, 'wide'),                                                  # wobble 2
        (10300, 'half'), (10380, 'line'), (10930, 'half'), (11010, R),   # the calm moment
        (11300, Ru), (11400, 'sparkle'), (12000, Ru),                    # it stands: the sparkle on top
        (12180, 'wide'),                                                 # ... it tips
        (12350, Rd),                                                     # following them down
        (13000, 'half/d'), (13400, 'line'), (13850, 'half/d'), (13930, Rd),   # no matter: a calm blink
        (14350, R),
    ]


def _fx_track():
    def landing(t, name, x, y):
        w = STONES[name].w
        return [(t, [('clack', 0, x, y, w), ('dust', 0, x, y + 1, w)]),
                (t + 70, [('clack', 1, x, y, w), ('dust', 1, x, y + 1, w)])]

    tr = [(0, [])]
    # sparkle on the finished cairn: dot, plus, star, plus, dot
    for t, i in ((11300, 0), (11400, 1), (11520, 2), (11720, 1), (11840, 0)):
        tr.append((t, [('spark', i, 0, 0, 0)]))
    tr.append((11940, []))
    # landings: each one a clack + dust (dust thins out, clacks spread)
    tr += [(12500, [('clack', 0, 20, 18, 3), ('dust', 0, 20, 18, 3)]),
           (12570, [('clack', 1, 20, 18, 3), ('dust', 1, 20, 18, 3), ('clack', 0, 23, 18, 4), ('dust', 0, 23, 18, 4)]),
           (12640, [('dust', 2, 20, 18, 3), ('clack', 1, 23, 18, 4), ('dust', 1, 23, 18, 4)]),
           (12730, [('dust', 2, 23, 18, 4), ('clack', 0, 21, 16, 6)]),
           (12800, [('clack', 1, 21, 16, 6)]),
           (12900, [])]
    return tr


def _segments(keys):
    out = []
    for i, (t, v) in enumerate(keys):
        t2 = keys[i + 1][0] if i + 1 < len(keys) else LOOP
        assert t2 > t, (t, t2, v)
        out.append((v, t2 - t))
    return out


def _boulder():
    f = Frame()
    f.place(_BOULDER, *BOULDER_AT)
    return f


def _stones(st):
    f = Frame()
    for name in ('brown', 'silver', 'tan'):             # tan lies on top in the heap
        if name in st:
            x, y, tilt = st[name]
            f.place(_stone(name, tilt), x, y)
    return f


def build():
    story = _story()
    body = [(_body(v), ms) for v, ms in _segments([(t, b) for t, b, _ in story])]
    stones = [(_stones(v), ms) for v, ms in _segments([(t, s) for t, _, s in story])]
    face = [(_eyes(v), ms) for v, ms in _segments(_face_track())]
    fx = [(_fx(v), ms) for v, ms in _segments(_fx_track())]
    for lst in (body, stones, face, fx):
        assert total_ms(lst) == LOOP
    return anim(NAME, DESC, [
        layer('boulder', [(_boulder(), LOOP)]),
        layer('stones', stones),
        layer('body', body),                # Clawd + the pebble in his claw (in front of the cairn)
        layer('face', face),                # fine-line eyes (half-size pixels)
        layer('fx', fx),
    ], state=STATE)
