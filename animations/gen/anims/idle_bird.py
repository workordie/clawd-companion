"""idle-bird - Idle variant: a little bird friend.   Preview:  python3 gen/preview.py anim idle-bird

STORYBOARD (ms)   one loop = 20 000 ms; the bird visits once; long calm holds around its visit
     0  HOLD 3.3 s (frame 0 = the reduced-motion still): Clawd at HOME gazing up at a little bluebird perched
        on the left half of his head, facing right (looking room ahead of it)
  3300  blink-glance: his eyes come back to you .. HOLD 1.1 s
  4520  HOP-HOP: it crouches, and its first hop catches his eye (look_u, 4640): two low sparrow hops to the
        right half of his head, wing folded (eye rows 10, 8, 10, 8, 10); its tail lands a beat late (5060) .. 0.65 s
  5830  SONG: neck stretched, beak to the sky, eyes shut (320 ms); a tiny note pops out a clear cell away and
        drifts up-right, slowing, then shrinks and is gone (6850)
  6650  he looks at you: "did you hear that?" (750 ms) .. blink-glance back up at it (7400)
  7520  HOLD 1.1 s, both still
  8620  PREEN: head turned back over its shoulder, buried in its feathers at the base of the tail (8920), then
        at the shoulder (9170), head pops back up (9420) .. HOLD 1.2 s
 10620  he blinks and OFFERS HIS ARM (side -> up -> raise) and holds it out (400 ms) .. it takes the offer: it
        crouches (11120) and hops over on an arc with its apex above the gap (eye rows 10, 7, 6, 7, 10); contact
        (11470); a beat later his hand gives and the bird sinks with it, its wing over the dipped tip (11560);
        both spring back, its tail flicking up (11670), and settle (11780) .. HOLD 1.1 s on his hand
 12880  it turns to face him, head first then body .. a SLOW SHARED BLINK (13360, 300 ms): a tiny heart grows
        from a dot between them, rises easing out, shrinks back to a dot and is gone (13360-14460) .. 0.3 s
 14760  it turns back to the sky (head first, then body), looks, decides .. crouch (15170)
 15290  TAKE-OFF: its push dips his hand; it accelerates (steps of 1, 1, 2, 2, 3 cells) out through the top
        right while his eyes follow it (look_r); then his hand lowers and his eyes rise after it (look_ur, 15720)
 16180  HOLD 2.2 s alone, back to you .. blink (18380) and a glance up at his empty head (18500)
 19000  it flutters back in from the left on an arc (90 ms flaps); he spots it (look_l, 19090); wings up, it
        glides (19270) into a flare (19380) as he follows it overhead (look_u), brakes with one more wingbeat
        (19490), flares, feet reaching (19610), touches down and absorbs it (19740) as he blinks: he feels its
        little feet; its tail follows (19870)
 20000  = frame 0
Eye closures: 3.30, 7.40, 10.62, 13.36 (slow, shared), 18.38, 19.74 s; gaps 4.1 / 3.2 / 2.7 / 5.0 / 1.4 / 3.6 s.
Full holds (nothing moves): 3.3, 1.1, 1.1, 1.2, 1.1, 2.2 s = half the loop (idle: 53 %); no busy stretch longer
than 3.3 s; 61 moments (3.05 changes/s); never more than 12 changes in any 2 s (idle's firefly: 14).
Layers change on shared beats wherever they can (no composite moment shorter than 70 ms).

Face: kit eyes only, and only where both holes stay enclosed: open / blink / look_u / look_l with the arm at the
side, look_u / look_r / blink with the arm raised or giving (the arm's elbow cell closes look_r's hole), look_ur only
with the 'up' arm (its cell closes the head-corner hole).  The one hand-made variant is 'give': the kit 'raise'
arm minus its tip cell, so his hand dips one cell under the bird's weight on landing and when it pushes off (the
same technique as idle's toe tap).
Layers: body (Clawd) | bird | fx (note, heart).  All three share LOOP, so his eyes always point at the bird.  The
bird is drawn locally (no bird in the library): blue 'b' body, navy 'B' wing (its outermost tips are mid-tone 'b'
so a flapping wing stays visible on the dark theme), gold 'j' beak and leg, and a see-through eye hole like
Clawd's own.  Anchor = the perch cell under its foot: (x, 12) stands it on his head, (21, 12) on the tip of his
raised hand, (21, 13) on his hand while it gives.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'idle-bird'
STATE = 'Idle variant: a little bird friend'
DESC = ('Waits calmly with a little bluebird on his head: he watches it hop, sing and preen, offers it his hand '
        'as a perch, shares a slow blink and a tiny heart with it, then follows it with his eyes as it flies '
        'off and later flutters back.')

LOOP = 20000

# ---------------------------------------------------------------- the bird (local sprites, facing right)
# '.' inside the bird = its see-through eye.  anchor = the perch cell under its foot.
_ROWS = {
    'perch':  (['...bb.',
                '.bbb.j',
                'bBBbb.',
                '..j...'], (2, 4)),
    'blink':  (['...bb.',          # its eye closes for a moment
                '.bbbbj',
                'bBBbb.',
                '..j...'], (2, 4)),
    'tail':   (['...bb.',          # tail flicked up (follow-through after a landing)
                'bbbb.j',
                '.BBbb.',
                '..j...'], (2, 4)),
    'lookb':  (['..bb..',          # head turned back over its shoulder (turns, preening)
                '.j.bb.',
                'bBBbb.',
                '..j...'], (2, 4)),
    'crouch': (['...bb.',          # legs bent, body down on the perch (anticipation / landing)
                'bbbb.j',
                '.BBbb.'], (2, 3)),
    'hop':    (['...bb.',          # small hop: the perch pose lifted, wing folded, leg tucked
                '.bbb.j',
                'bBBbb.'], (2, 4)),
    'air':    (['.b....',          # big hop: wing up, leg dangling
                '.BBbb.',
                'bbbb.j',
                '.bbbb.',
                '..j...'], (2, 5)),
    'chirp':  (['.....j',          # singing: neck stretched, eyes shut, beak tilted up to the sky
                '...bb.',
                '.bbbb.',
                'bBBb..',
                '..j...'], (2, 5)),
    'dip':    (['......',          # preen: head buried in its feathers, beak at the base of the tail ..
                '.jbbb.',
                'bBBbb.',
                '..j...'], (2, 4)),
    'dip2':   (['......',          # .. then at the shoulder (the wing keeps beak and leg apart)
                '.bjbb.',
                'bBBbb.',
                '..j...'], (2, 4)),
    'fly_up': (['.b....',          # wing up
                '.BBbb.',
                'bbbb.j',
                '.bbbb.'], (2, 5)),
    'fly_dn': (['...bb.',          # wing down
                '.bbb.j',
                'bBBbb.',
                '.b....'], (2, 4)),
    'land':   (['b.....',          # flare: wings up and back, leg reaching down
                'bB.bb.',
                '.bbb.j',
                '..bbb.',
                '..j...'], (2, 5)),
}
_BIRD = {}
for _k, (_r, _a) in _ROWS.items():
    _BIRD[(_k, 'r')] = Sprite(_r, anchor=_a, name='bird_' + _k)
    _BIRD[(_k, 'l')] = _BIRD[(_k, 'r')].flipped()

# fx sprites.  The library note is 5x6 (bigger than the bird): this one is bird-sized (anchor = top-left).
_FXS = {
    'note':    Sprite(['.vv',
                       '.v.',
                       'vv.'], anchor=(0, 0), name='chirp_note'),
    'note_s':  Sprite(['.v',
                       'vv'], anchor=(0, 0), name='chirp_note_small'),
    'heart':   get('heart_pop').sprite(0),      # the library's tiny 3x3 heart (pop-in frame); anchor = center
    'dot':     Sprite(['p'], anchor=(0, 0), name='heart_dot'),   # the heart as it grows in / shrinks away
}


def _place(f, spr, x, y):
    """frame.place with the sprite trimmed to the canvas first. Only the bird's deliberate entry (left edge)
    and exit (right edge) ever lose pixels, so nothing is reported as accidentally clipped."""
    keep = [(sx, sy, ch) for sx, sy, ch in spr.cells
            if 0 <= x + sx - spr.ax < W and 0 <= y + sy - spr.ay < H]
    f.place(Sprite(cells=keep, anchor=(spr.ax, spr.ay), name=spr.name), x, y)


# ---------------------------------------------------------------- Clawd: (t ms, eyes, right arm)
# right arm: a kit arm, or 'give' = the raised hand dipping one cell under the bird's weight
_CLAWD = [
    (0,     'look_u', 'side'),    # frame 0: gazing up at his friend
    (3300,  'blink',  'side'),    # blink-glance ..
    (3420,  'open',   'side'),    # .. back to you
    (4640,  'look_u', 'side'),    # its first hop catches his eye
    (6650,  'open',   'side'),    # "did you hear that?"
    (7400,  'blink',  'side'),    # blink-glance ..
    (7520,  'look_u', 'side'),    # .. back up at it; it preens
    (10620, 'blink',  'up'),      # he blinks and offers his arm ..
    (10720, 'look_u', 'raise'),   # .. and holds it there
    (11560, 'look_u', 'give'),    # it lands: a beat later the hand gives under its weight ..
    (11670, 'look_u', 'raise'),   # .. and springs back
    (13360, 'blink',  'raise'),   # slow, contented blink (the bird blinks with him)
    (13660, 'look_u', 'raise'),
    (15290, 'look_r', 'give'),    # push-off: the hand dips; his eyes follow it to the right ..
    (15720, 'look_ur', 'up'),     # .. it is gone: the hand lowers as his eyes rise after it
    (16180, 'open',   'side'),    # back to you
    (18380, 'blink',  'side'),
    (18500, 'look_u', 'side'),    # a glance up at his empty head
    (19090, 'look_l', 'side'),    # spots it coming in from the left
    (19380, 'look_u', 'side'),    # follows it overhead
    (19740, 'blink',  'side'),    # touch-down: he feels its little feet
    (19870, 'look_u', 'side'),
]

# ---------------------------------------------------------------- bird: (t ms, pose, x, y, facing)
_BIRDS = [
    (0,     'perch',  13, 12, 'r'),
    # hop-hop: low hops, wing folded (eye rows 10, 8, 10, 8, 10)
    (4520,  'crouch', 13, 12, 'r'),    # anticipation
    (4640,  'hop',    14, 11, 'r'),
    (4740,  'crouch', 15, 12, 'r'),
    (4840,  'hop',    16, 11, 'r'),
    (4940,  'crouch', 17, 12, 'r'),    # lands
    (5060,  'tail',   17, 12, 'r'),    # the tail lands a beat late
    (5180,  'perch',  17, 12, 'r'),
    # song: one chirp, beak to the sky
    (5830,  'chirp',  17, 12, 'r'),
    (6150,  'perch',  17, 12, 'r'),
    # preen
    (8620,  'lookb',  17, 12, 'r'),    # head turned back over its shoulder ..
    (8920,  'dip',    17, 12, 'r'),    # .. buried in its feathers at the base of the tail ..
    (9170,  'dip2',   17, 12, 'r'),    # .. then at the shoulder
    (9420,  'perch',  17, 12, 'r'),    # head pops back up
    # onto his hand: an arc with its apex above the gap (eye rows 10, 7, 6, 7, 10, then 11 as the hand gives)
    (11120, 'crouch', 17, 12, 'r'),    # it takes the offer: anticipation
    (11240, 'air',    18, 10, 'r'),
    (11320, 'air',    19, 9, 'r'),
    (11400, 'air',    20, 10, 'r'),
    (11470, 'crouch', 21, 12, 'r'),    # contact (squash) ..
    (11560, 'crouch', 21, 13, 'r'),    # .. a beat later his hand gives and it sinks with it ..
    (11670, 'tail',   21, 12, 'r'),    # .. both spring back, its tail flicking up ..
    (11780, 'perch',  21, 12, 'r'),    # .. and settle
    (12880, 'lookb',  21, 12, 'r'),    # its head turns to him first ..
    (13010, 'perch',  21, 12, 'l'),    # .. then its body: face to face
    (13360, 'blink',  21, 12, 'l'),    # a slow blink, together
    (13660, 'perch',  21, 12, 'l'),
    (14760, 'lookb',  21, 12, 'l'),    # head back toward the sky first ..
    (14890, 'perch',  21, 12, 'r'),    # .. then its body: it looks, decides
    (15170, 'crouch', 21, 12, 'r'),    # anticipation
    # take-off: the push dips his hand; it accelerates (steps 1, 1, 2, 2, 3) out through the right edge
    (15290, 'fly_dn', 22, 10, 'r'),
    (15380, 'fly_up', 23, 8, 'r'),
    (15470, 'fly_dn', 25, 7, 'r'),
    (15555, 'fly_up', 27, 6, 'r'),
    (15640, 'fly_dn', 30, 5, 'r'),     # last glimpse: its back half at the edge
    (15720, None,     0, 0, 'r'),
    # arrival from the left: up on an arc to its apex (x 5-8), a glide, then braking down onto his head
    (19000, 'fly_dn', -1, 8, 'r'),     # its head peeks in at the left edge
    (19090, 'fly_up', 2, 7, 'r'),
    (19180, 'fly_dn', 5, 6, 'r'),
    (19270, 'fly_up', 8, 6, 'r'),      # wings stay up: it glides ..
    (19380, 'land',   10, 8, 'r'),     # .. into a flare: braking (ease in)
    (19490, 'fly_dn', 12, 10, 'r'),    # one more braking wingbeat
    (19610, 'land',   13, 11, 'r'),    # flare, feet reaching
    (19740, 'crouch', 13, 12, 'r'),    # touch-down: it absorbs the landing
    (19870, 'tail',   13, 12, 'r'),    # the tail follows .. frame 0
]

# ---------------------------------------------------------------- fx: (t ms, [(kind, x, y), ...])
_FX = [
    (0,     []),
    # one note pops out with the chirp, a clear cell above the beak (20, 7), and drifts up-right, slowing
    # (200, 370, 250 ms), then shrinks away
    (5830,  [('note_s', 21, 4)]),
    (6030,  [('note', 22, 2)]),
    (6400,  [('note', 23, 1)]),
    (6650,  [('note_s', 24, 1)]),
    (6850,  []),
    # a tiny heart grows from a dot between the two friends as they blink, rises easing out (200, 300, 350 ms)
    # and shrinks back to a dot, still rising, before it is gone
    (13360, [('dot', 17, 7)]),
    (13460, [('heart', 17, 6)]),
    (13660, [('heart', 17, 5)]),
    (13960, [('heart', 17, 4)]),
    (14310, [('dot', 17, 3)]),
    (14460, []),
]


def _segments(keys):
    """[(t, value), ...] (t ascending, first t = 0) -> [(value, ms), ...] ending at LOOP."""
    out = []
    for i, (t, v) in enumerate(keys):
        t2 = keys[i + 1][0] if i + 1 < len(keys) else LOOP
        assert t2 > t, (t, t2)
        out.append((v, t2 - t))
    return out


_TIP = (GEOM['normal']['ax'][1] + 1, GEOM['normal']['ay'] - 2)   # box cell of the raised hand's tip (11, 0)


def _pose(eyes, arm):
    if arm == 'give':
        # the kit's raised arm with its tip cell removed: the hand dips one cell under the bird
        p = clawd(eyes=eyes, rarm='raise')
        cells = [c for c in p.sprite.cells if (c[0], c[1]) != _TIP]
        return Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec, give=True))
    return clawd(eyes=eyes, rarm=arm)


def _clawd_frame(eyes, arm):
    f = Frame()
    put_clawd(f, _pose(eyes, arm))
    return f


def _bird_frame(pose, x, y, face):
    f = Frame()
    if pose:
        _place(f, _BIRD[(pose, face)], x, y)
    return f


def _fx_frame(items):
    f = Frame()
    for kind, x, y in items:
        f.place(_FXS[kind], x, y)
    return f


def build():
    body = [(_clawd_frame(*v), ms) for v, ms in _segments([(t, (e, a)) for t, e, a in _CLAWD])]
    bird = [(_bird_frame(*v), ms) for v, ms in _segments([(t, (p, x, y, fc)) for t, p, x, y, fc in _BIRDS])]
    fx = [(_fx_frame(v), ms) for v, ms in _segments(_FX)]
    for lst in (body, bird, fx):
        assert total_ms(lst) == LOOP
    return anim(NAME, DESC, [layer('body', body), layer('bird', bird), layer('fx', fx)], state=STATE)
