# ======================================================================================
# USER FEEDBACK: the user reviewed this fine-face upgrade draft personally and approved it
# ("looks great go"). Keep the scene, beats and fine-line expressions; critics, fixers and judges
# should polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""question - Claude asked you a question and waits for your answer.   Preview:  python3 gen/preview.py anim question

Clawd as a curious little quiz host: a big blue "?" floats over his head, he holds two answer cards, a green
A and a violet B (Claude Code's questions come with options), and a brass desk bell waits on the input box for
your answer ("ring in when you're ready").  EXPRESSIVE style (STYLE.md 0b): his face acts with the fine-line
kit (half-size black eyes: wide, half-step glances, smooth blinks, content cups, a wink); no mouth, no blush,
never resized.

Storyboard: ONE 11900 ms story. Body, cards, face, "?" and glints are cut from the same clock, so every reaction
stays locked to his gestures. The big seesaw happens once per loop; in between he acts in small, patient beats,
and no hold of his arms lasts longer than ~3.5 s.  Face beats are marked  [face].
  t (ms)  beat
     0    HM? WHICH ONE? (frame 0): at HOME, both cards held out to you, the "?" at rest above his head, the
          bell on the input box at his right.  [face] WIDE eyes on you: an expectant, eyebrows-up "hm?".
   300    the "?" hops on his "hm?": anticipation squash held 120 ms (hook sinks onto the dot), launch stretch,
          apex hang, fall with the dot leading, landing squash (790) that shakes a gold glint loose: it drifts
          off up-right on a little arc as it fades (790-1100). Settled 880.
  1300    patient hold.  [face] the "hm?" melts into a smooth double blink (wide > half > line > half > open,
          then a quicker second one), a long half-step glance down-right, at the input box where your answer
          will appear and the bell beside it (1960); the bell's plunger catches the light under his gaze
          (2040): ring in when ready. Back to you (2520).
  3480    "A...?": [face] the eyes lead to A (half-step left), A lifts one cell (3560) and holds. "...or B?": the
          eyes swing through the middle to B (3900 / 3980) while A drops back with a one-cell overshoot; B lifts
          (4060). Eyes back to you (4400), then B settles with its own overshoot (4480).
  4980    the "?" tilts its head like a curious puppy: half-lean in (100 ms), full lean held 500 ms, swings back
          through upright (5580) into a small overshoot the other way, a half-lean (only the top row), so the
          swing decays 2 rows > 1 > 0 like a spring; upright at 5760.  [face] he looks up at it just as it
          reaches full lean (5080); 5880 a smooth blink that closes where he is looking (up at the "?") and
          opens on you (6090): the blink carries his gaze home.
  6810    [face] a thoughtful half-lid (hmm...): the thought leads the action.
  7140    relaxes: he lowers the cards softly to his sides (no bounce) and the "?" floats up as they go down,
          hook first; the dot follows (7240).  [face] the lids settle into CONTENT cups (u u, 7240): no rush,
          take your time. 8140 he peeks up at the floating "?" (half > open > look_u: the lids open first).
  8740    [face] the eyes lead to B; B rises through "held out", overshoots and settles high beside his head
          while the "?" sinks back hook first (soft squash): HOW ABOUT B? (9080, eyes on you)
          [face] 9250 he offers it with a tiny WINK (the eye beside B: half > ^ arc held 480 ms > half), and a
          gold glint twinkles off B's top corner inside the wink (9320): psst, B. The wink opens toward B
          (9800) and both eyes go up to it (9890: a diagonal half-step, up at the raised card).
 10370    B lifts one more cell (ease in) into the seesaw wind-up, held 180 ms (10450): B high while A dips;
          eases out (80 ms; [face] the eyes let go of B), the cards swing through "held out" ([face] the eyes
          lead up to where A is going) and trade places, each overshooting one cell (10800): ...OR A?
 11700    both cards come back out to you ([face] eyes back on you), overshoot (11790) as the eyes narrow (a
          half-lid squint: the anticipation of the take) and settle into frame 0, where the eyes pop wide: hm?
Eye closures: 1.30 + 1.64 (double blink), 5.88 (blink), 6.81-8.27 (half-lid, content), 9.25-9.89 (wink),
11.79 (squint): uneven on purpose.  Glances are fine half-steps: the kit's look_l / look_r / look_u plus
local diagonals (look_ur / look_ul / look_dr = the open eye moved one fine pixel each way, the way
idle_moods moves its gaze), and lids that close at the gaze (half_u / line_u / half_ur).  build() asserts
that the eyes never jump (each face frame shares ink with the next, or a lid morphs in place, e.g. the
wink's half > ^ arc) and never reach the edge of his body, whatever the arms do.
Layers: bell (static) | qmark (11900) | clawd (static: the cells of his body that are the same in every pose) |
body_b (normal res: the eye rows in plain orange + the arms, and card B in his right claw: his arms only
move on beats where B moves too, so the body rides in B's frames for free) | face (FINE: his eyes in
half-size pixels, one color, a handful of runs per expression; drawn after the body, the cards never touch
his face) | card_a (11900, same beat list: an A lift costs one small frame) | glints (11900: the hop glint,
the bell glint and the wink glint, always on cue) | twinkle (6810 ms, gcd 10 with 11900): one tiny gold glint
in the empty sky (plus -> cross -> dot; the loop ends on the dot, so it needs no trailing empty frame), so it
lands on a different story beat every pass and the combination only repeats every ~2.25 hours (lcm
8103900 ms).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'question'
STATE = 'Claude asked you a question and waits for your answer'
DESC = ('Quiz-host Clawd holds out two answer cards, A and B, under a big bobbing "?" with a brass desk bell '
        'beside him: a wide-eyed "hm?", half-step glances that weigh each card, a content wait, a wink for B, '
        'and smooth blinks while he waits for your answer.')

LOOP = 11900
_TW_LOOP = 6810            # the ambient sky twinkle's own loop (gcd 10 with LOOP); it fires at 6500 on the first pass

# ---------------------------------------------------------------------------------------------
# Local sprites
# ---------------------------------------------------------------------------------------------
# Hero question mark in two parts (hook + dot) so the dot can lag behind / lead the hook
# (squash and stretch without redrawing the glyph). Chunky 2-cell strokes, cyan highlight on the
# top-left, navy shade on the right / bottom; the dot is lit like the stem (glint top-left).
_HOOK_ROWS = [
    '.cbbb.',
    'cb..bB',
    '....bB',
    '...bB.',
    '..bB..',
]
_DOT = Sprite([
    '..cb..',
    '..bB..',
], anchor=(0, 0), name='qmark_dot')
_Q_X, _Q_Y = 13, 3          # top-left of the "?" at rest: hook rows 3-7, dot rows 9-10 (his head is row 12)


def _hook(lean=0, rows=2):
    """lean = -1 / 0 / +1: tilt the "?" by shifting its top `rows` rows (2 = full lean, 1 = half-lean on
    the way in), i.e. a small rotation around the middle of the glyph (qmark moves the dot the other way).
    A left lean also shifts the third row, so the back of the hook stays a straight column instead of
    bulging out to the right."""
    shifted = rows + (1 if lean < 0 and rows == 2 else 0)
    cells = []
    for y, row in enumerate(_HOOK_ROWS):
        for x, ch in enumerate(row):
            if ch != '.':
                cells.append((x + (lean if y < shifted else 0), y, ch))
    return Sprite(cells=cells, anchor=(0, 0), name='qmark_hook')


_GLYPH = {'A': ['.W.', 'W.W', 'WWW', 'W.W', 'W.W'],
          'B': ['WW.', 'W.W', 'WW.', 'W.W', 'WW.']}


def _card(letter, base, shade):
    rows = ['.' + base * 3 + '.']
    for r in _GLYPH[letter]:
        rows.append(base + r.replace('.', base) + shade)
    rows.append('.' + shade * 3 + '.')
    return rows


# Cards are held by their outer side edge, one row above the rounded bottom corner: B (right claw) by
# its left edge, A (left claw) by its right edge. The anchor lands on the kit's hand grip point, so the
# claw tip butts straight against the card's edge (never covering his arm), and an upward overshoot
# still touches the claw at the card's corner.
_CARD_A = Sprite(_card('A', 'g', 'G'), anchor=(4, 5), name='card_a')
_CARD_B = Sprite(_card('B', 'v', 'V'), anchor=(0, 5), name='card_b')

# Brass service bell for your answer (the library has no desk bell): plunger (silver knob on a steel rod,
# the detail that makes it read as a bell at real size), low dome lit from the top-left (yellow highlight,
# dark-gold shade on the right) on a wooden base. Compact (5 wide) and centered at x 28, so even B's
# overshoots keep a clear gap from it. Anchor = bottom-center, resting on the input box (x 26-30, rows 15-19).
_BELL = Sprite([
    '..m..',
    '..s..',
    '.yjJ.',
    'yjjjJ',
    'TTTTd',
], anchor=(2, 4), name='desk_bell')
_BELL_AT = (28, GROUND)
_BELL_GLINT = (29, 13)     # bursts just above-right of the plunger knob (28, 15): the cross's ray touches the
                           # knob from above and never paints over it; clear of card B (x <= 26)
_WINK_GLINT = (27, 6)      # "psst, B": off B's top-right corner while B is raised (x 21-25, rows 8-14), a cell
                           # clear of the card, the "?" and the bell
_HOP_GLINT = [(21, 4), (22, 3), (23, 3)]   # shaken loose by the landing: plus, cross, dot drifting up-right on a
                           # small decelerating arc, two cells clear of the landed hook (x <= 18)


def _lib(name, fallback):
    """Library item, or a local copy of it while another artist is mid-save (KeyError)."""
    try:
        return get(name)
    except KeyError:
        return fallback()


# Library glint (dot -> plus -> diagonal cross) for the hop, the bell and the ambient twinkles.
_SPARK = _lib('sparkle_small', lambda: Item('sparkle_small', 'fx', 'local fallback', [
    Sprite(['j'], anchor=(0, 0)),
    Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1)),
    Sprite(['j.j', '.y.', 'j.j'], anchor=(1, 1))]))


# ---------------------------------------------------------------------------------------------
# Clawd: static rows | body (normal res) | face (fine overlay)
# ---------------------------------------------------------------------------------------------
# Clawd never leaves HOME and never changes body shape here, so the cells that are the same in every
# pose (his top row, the lower body and the legs) go in a static layer; the body layer only carries what
# changes: the eye rows and the arms. His face is drawn with the fine-line kit (fine + fine_face) and
# split off: the body layer keeps plain orange where his eyes are (each eye row is one run, and the body
# only changes when the arms move) and the fine face layer holds only the half-size pixels that are not
# body orange, i.e. the eye ink itself: one color, a handful of runs per expression. (Should the kit ever
# draw see-through eyes again, clawd_split cuts the cells a see-through half needs out of the body, so the
# split stays correct.) The composite is exactly fine(put_clawd(pose)) + fine_face(...) (checked in build()).
_BX0, _BX1 = HOME[0] + 1, HOME[0] + 9                    # body columns 11-19
_BY0, _BY1 = HOME[1], HOME[1] + 5                        # body rows 12-17
_FIXED_ROWS = (HOME[1], HOME[1] + 4, HOME[1] + 5, HOME[1] + 6, HOME[1] + 7)   # rows 12, 16, 17, 18, 19
_BLACKEN = globals().get('blacken_eye_holes')            # what layer() does to every frame (kit, black eyes)


def _fixed(x, y):
    return _BX0 <= x <= _BX1 and y in _FIXED_ROWS


def clawd_static():
    f = Frame()
    put_clawd(f, clawd())
    for x, y in list(f.px):
        if not _fixed(x, y):
            f.put(x, y, ERASE)
    return f


# Local fine expressions: a kit FINE_EYES shape moved by a half-step gaze (dx, dy) in fine pixels, the way
# idle_moods moves its gaze. The kit's fine glances are only l / r / u / d; these add the diagonals (up at a
# raised card, down at the input box by the bell) and lids that close where he is looking, so a blink or the
# end of the wink never makes the eye jump.
_LOCAL = {
    'look_ur': ('open', (1, -1)),        # up at the raised B card
    'look_ul': ('open', (-1, -1)),       # up at the raised A card
    'look_dr': ('open', (1, 1)),         # down at the input box, toward the bell
    'half_u': ('half', (0, -1)),         # a blink that closes while he looks up at the "?"
    'line_u': ('line', (0, -1)),
    'half_ur': ('half', (1, -1)),        # the wink opens toward B
}


def _gazed(ff, pose, left, right):
    """fine_face() with the local expressions: draw the kit shape, then move each eye's ink by its gaze."""
    fine_face(ff, pose, expr=_LOCAL.get(left, (left,))[0], right=_LOCAL.get(right, (right,))[0])
    for key, e in (('eye_l', left), ('eye_r', right)):
        gx, gy = _LOCAL[e][1] if e in _LOCAL else (0, 0)
        if not (gx or gy):
            continue
        ex, ey = pose.at(key)
        win = [(2 * ex + dx, 2 * ey + dy) for dy in range(-2, 4) for dx in range(-2, 4)]   # his 3x3-cell eye area
        ink = {(x + gx, y + gy): ff.px.get((x, y)) for x, y in win if ff.px.get((x, y)) != '#'}
        assert all(q in win for q in ink), 'a %s glance leaves the eye area' % e
        for x, y in win:
            ff.put(x, y, '#')
        for (x, y), ch in ink.items():
            ff.put(x, y, ERASE if ch is None else ch)      # None = a see-through half (if the kit ever goes back)
    return ff


def _fine_ref(larm, rarm, left, right):
    """The reference picture: Clawd drawn the normal way, his face drawn with the fine-line kit."""
    p = clawd(larm=larm, rarm=rarm)
    f = Frame()
    put_clawd(f, p)
    ff = fine(f)
    _gazed(ff, p, left, right)
    return p, f, ff


def clawd_split(larm, rarm, left, right):
    """-> (body, face): the normal-res body frame (eye rows painted plain orange + arms; the fixed rows are
    left to the static layer) and the fine face overlay (only the half-size pixels that differ from it)."""
    p, f, ff = _fine_ref(larm, rarm, left, right)
    face = Frame(res=2)
    face.meta = {'fine_face': [(left, right)]}
    for key in ('eye_l', 'eye_r'):
        f.put(*p.at(key), ch='#')                       # the eyes live in the face layer
    for key in ('eye_l', 'eye_r'):
        ex, ey = p.at(key)
        for cy in (ey - 1, ey, ey + 1):
            for cx in (ex - 1, ex, ex + 1):
                quad = [ff.px.get((2 * cx + k % 2, 2 * cy + k // 2)) for k in range(4)]
                b = f.px.get((cx, cy))
                if all(q == b for q in quad):
                    continue
                cut = None in quad
                if cut:
                    f.px.pop((cx, cy), None)        # a see-through half: the whole cell leaves the body
                for k, q in enumerate(quad):
                    if q is not None and (cut or q != b):
                        face.px[(2 * cx + k % 2, 2 * cy + k // 2)] = q
    for x, y in list(f.px):
        if _fixed(x, y):
            f.put(x, y, ERASE)
    return f, face


def _check_pose(larm, rarm, left, right, static, body, face):
    """Guard rails: (1) static + body + face rebuild exactly the kit picture (fine(pose) + fine_face), and
    layer()'s eye pass leaves every one of these frames as it is (what is checked is what ships); (2) no
    half-pixel of his eyes sits on the edge of his body (a glance must never notch his outline)."""
    pose = (larm, rarm, left, right)
    _, _, ref = _fine_ref(larm, rarm, left, right)
    if _BLACKEN is not None:
        for fr in (static, body, face):
            assert _BLACKEN(fr.copy()).px == fr.px, 'layer() would repaint part of the frame: %s' % (pose,)
    comp = fine(static.over(body)).over(face)
    assert comp.px == ref.px, 'static/body/face split broke the pose %s' % (pose,)
    for y in range(2 * _BY0, 2 * _BY1 + 2):
        for x in range(2 * _BX0, 2 * _BX1 + 2):
            if ref.px.get((x, y)) != '#':
                assert 2 * _BX0 < x < 2 * _BX1 + 1 and 2 * _BY0 < y < 2 * _BY1 + 1, \
                    'eye pixel at fine (%d,%d) on the edge of his body: %s' % (x, y, pose)


def _check_smooth(faces):
    """Guard rail for the brief's smooth fine eyes: from one face frame to the next (and across the loop seam)
    each eye's ink shares a half-pixel with the next frame's, or, when a lid changes shape in place (half >
    ^ arc), every ink half-pixel of each touches the other's. A pupil never jumps."""
    def eyes(fr):
        left, right = set(), set()
        for x, y in fr.px:
            (left if x < W else right).add((x, y))
        return left, right

    def near(a, b):
        return all(any(abs(x - u) + abs(y - v) <= 1 for u, v in b) for x, y in a)
    seq = [eyes(f) for f in faces]
    for i, cur in enumerate(seq):
        for a, b in zip(cur, seq[(i + 1) % len(seq)]):
            assert a & b or (near(a, b) and near(b, a)), 'an eye jumps after face frame %d' % i


def card(which, larm='out', rarm='out', a=0, b=0):
    """One card in its claw; a / b = the A / B card's vertical offset from its grip (a lift, or the
    follow-through overshoot in the direction the claw was moving). Card A has its own layer and card B
    rides in the body's frames (body_b), both on the same beat list as the face: a blink or a glance costs
    nothing in either, and an A lift costs nothing in body_b."""
    f = Frame()
    p = clawd(larm=larm, rarm=rarm)
    if which == 'a':
        x, y = p.at('hand_l')
        f.place(_CARD_A, x, y + a)
    else:
        x, y = p.at('hand_r')
        f.place(_CARD_B, x, y + b)
    return f


def qmark(hook=0, dot=None, dx=0, lean=0, rows=2):
    """hook / dot = vertical offsets from rest (the dot follows the hook unless given: a lagging or
    leading dot is the squash / stretch), dx = sideways drift, lean = tilt (-1 left, +1 right; rows=1 is
    the half-lean in-between, which leaves the dot in place)."""
    f = Frame()
    f.place(_hook(lean, rows), _Q_X + dx, _Q_Y + hook)
    shift = -lean if rows == 2 else 0
    f.place(_DOT, _Q_X + dx + shift, _Q_Y + 6 + (hook if dot is None else dot))
    return f


def glint(i, x, y):
    f = Frame()
    f.place(_SPARK.sprite(i), x, y)
    return f


def twinkles(events, at):
    """events: [(start_ms, (x, y) or [(x, y) per step]), ...] -> timed frames: pops in as a plus, turns
    45 deg (cross), shrinks to a dot, gone. A list of three positions makes the glint drift as it fades."""
    for start, pos in events:
        path = pos if isinstance(pos, list) else [pos] * 3
        for (dt, i), (x, y) in zip(((0, 1), (90, 2), (210, 0)), path):
            at.append((start + dt, glint(i, x, y)))
        at.append((start + 310, Frame()))
    return at


def at_times(events, total):
    """[(start_ms, Frame), ...] (sorted, first at 0) -> [(Frame, ms), ...] filling `total`."""
    events = sorted(events, key=lambda e: e[0])
    assert events[0][0] == 0
    out = []
    for i, (t, f) in enumerate(events):
        end = events[i + 1][0] if i + 1 < len(events) else total
        assert end > t, 'two events at %d ms' % t
        out.append((f, end - t))
    return out


# ---------------------------------------------------------------------------------------------
# The story
# ---------------------------------------------------------------------------------------------
OUT = dict(larm='out', rarm='out')           # both cards held out to you
B_UP = dict(larm='side', rarm='up')          # B raised beside his head, A low
A_UP = dict(larm='up', rarm='side')
SIDE = dict(larm='side', rarm='side')
WIND = dict(larm='down', rarm='raise')
RISE = dict(larm='side', rarm='out')
# Body + cards: (key, ms, arms, card offsets).  The keys are the approved beat clock (the "?", the glints
# and the face are cued from it); the face has its own track on the same clock (face_track() below), so
# keys like blink1 / blink3 / blink4 now only mark time: the face track decides what the eyes do there.
BEATS = [
    ('which', 1300, OUT, {}),                          # frame 0: hm? which one? (the "?" hops)
    ('blink1', 110, OUT, {}),                          # patient hold (face: double blink)
    ('gap', 140, OUT, {}),
    ('blink2', 110, OUT, {}),
    ('look', 300, OUT, {}),
    ('down', 560, OUT, {}),                            # your answer goes down there (bell glints)
    ('wait', 960, OUT, {}),
    ('eyeA', 80, OUT, {}),                             # the eyes lead...
    ('liftA', 340, OUT, dict(a=-1)),                   # ...A?
    ('mid', 80, OUT, dict(a=-1)),                      # eyes swing through the middle
    ('eyeB', 80, OUT, dict(a=1)),                      # A drops back (overshoot)
    ('liftB', 340, OUT, dict(b=-1)),                   # ...or B?
    ('back1', 80, OUT, dict(b=-1)),                    # eyes back to you first...
    ('settle', 80, OUT, dict(b=1)),                    # ...then B settles (overshoot)
    ('well', 520, OUT, {}),
    ('upq', 800, OUT, {}),                             # watches the "?" tilt
    ('blink3', 110, OUT, {}),
    ('wait2', 1150, OUT, {}),
    ('relax', 100, SIDE, {}),                          # lowers the cards softly (no bounce)
    ('rest', 1500, SIDE, {}),                          # content; the "?" floats up
    ('leadB', 160, SIDE, {}),                          # anticipation for B: the eyes lead
    ('rise', 90, RISE, {}),
    ('arrive', 90, B_UP, dict(b=-1)),                  # overshoot
    ('howB', 700, B_UP, {}),                           # how about B? (face: a wink)
    ('blink4', 110, B_UP, {}),                         # (the wink covers it)
    ('eyeB2', 480, B_UP, {}),                          # ...B?
    ('lift', 80, B_UP, dict(b=-1)),                    # B lifts a cell: eases into the wind-up
    ('windup', 180, WIND, {}),                         # seesaw anticipation (held)
    ('ease', 80, B_UP, dict(b=-1)),                    # eases out of the extreme
    ('swing', 90, OUT, {}),
    ('Aup', 100, A_UP, dict(a=-1, b=1)),               # overshoot
    ('eyeA2', 800, A_UP, {}),                          # ...or A?
    ('back', 90, OUT, {}),
    ('present', 110, OUT, dict(a=1, b=-1)),            # cards overshoot -> frame 0
]


def _clock():
    T, t = {}, 0
    for key, ms, _, _ in BEATS:
        T[key] = t
        t += ms
    assert t == LOOP, 'beats add up to %d ms, not %d' % (t, LOOP)
    return T


T = _clock()
WINK = T['howB'] + 170                       # the wink: half-lid here, the ^ arc 70 ms later (+ B's glint)


def _seq(track, t, steps):
    """Append sequential (ms, value) steps starting at time t; returns the end time."""
    for ms, v in steps:
        track.append((t, v))
        t += ms
    return t


def _eyes(e, r=None):
    return (e, e if r is None else r)


def face_track():
    """[(t, (left eye, right eye))]: fine-line expressions on the story clock."""
    f = [(0, _eyes('wide'))]                                   # frame 0: hm? which one?
    # the "hm?" melts into a smooth double blink (the second one quicker: the lids snap shut, open softly)
    _seq(f, T['blink1'], [(60, _eyes('half')), (90, _eyes('line')), (60, _eyes('half')), (130, _eyes('open')),
                          (80, _eyes('line')), (60, _eyes('half')), (0, _eyes('open'))])
    _seq(f, T['down'], [(560, _eyes('look_dr')), (0, _eyes('open'))])      # the input box, by the bell .. you
    f.append((T['eyeA'], _eyes('look_l')))                                 # A...?
    f.append((T['mid'], _eyes('open')))                                    # (through the middle)
    f.append((T['eyeB'], _eyes('look_r')))                                 # ...or B?
    f.append((T['back1'], _eyes('open')))
    f.append((T['upq'], _eyes('look_u')))                                  # the "?" tilts
    # a smooth blink that closes where he is looking (up at the "?") and opens on you
    _seq(f, T['blink3'], [(60, _eyes('half_u')), (90, _eyes('line_u')), (60, _eyes('half_u')), (0, _eyes('open'))])
    f.append((T['relax'] - 330, _eyes('half')))                # a thoughtful half-lid leads the relax ..
    _seq(f, T['rest'], [(900, _eyes('content')), (70, _eyes('half')), (60, _eyes('open')),
                        (0, _eyes('look_u'))])                 # .. u u .. the lids open, then a peek at the "?"
    f.append((T['leadB'], _eyes('look_r')))                                # the eyes lead to B
    t = _seq(f, T['howB'], [(170, _eyes('open'))])                         # HOW ABOUT B?
    assert t == WINK
    _seq(f, t, [(70, _eyes('open', 'half')), (480, _eyes('open', 'happy')),      # a tiny wink (the eye beside B)
                (90, _eyes('look_ur', 'half_ur'))])                        # .. that opens toward B ..
    f.append((T['eyeB2'], _eyes('look_ur')))                               # .. eyes up on the raised B
    f.append((T['ease'], _eyes('open')))                                   # lets go of B ..
    f.append((T['swing'], _eyes('look_ul')))                               # .. the eyes lead up to where A goes
    f.append((T['back'], _eyes('open')))                                   # back to you ..
    f.append((T['present'], _eyes('half')))                    # .. a squint as the cards overshoot: frame 0
    return sorted(f, key=lambda e: e[0])                       # pops wide from it (hm?)


def _segments():
    """Cut body beats and face events into one list: [(ms, arms, card offsets, (left, right))]."""
    face = face_track()
    cuts = sorted(set(T.values()) | {t for t, _ in face})
    out = []
    for i, t in enumerate(cuts):
        end = cuts[i + 1] if i + 1 < len(cuts) else LOOP
        beat = [b for b in BEATS if T[b[0]] <= t][-1]
        expr = [e for tt, e in face if tt <= t][-1]
        if out and out[-1][1:] == (beat[2], beat[3], expr):
            out[-1] = (out[-1][0] + end - t,) + out[-1][1:]       # nothing changes on this cut
        else:
            out.append((end - t, beat[2], beat[3], expr))
    for ms, arms, kw, expr in out:
        assert ms >= 40, 'a %d ms sliver: %s %s %s' % (ms, arms, kw, expr)
    return out


def build():
    st = clawd_static()
    bb, fc, ca = [], [], []
    for ms, arms, kw, (left, right) in _segments():
        body, face = clawd_split(arms['larm'], arms['rarm'], left, right)
        _check_pose(arms['larm'], arms['rarm'], left, right, st, body, face)
        # His arms only ever move on a beat where card B moves too, so the body rides in card B's frames
        # (B drawn over the body, as before): the same pixels without a body layer's own 9 frames.
        b_frame = body.over(card('b', **dict(arms, **kw)))
        if _BLACKEN is not None:
            assert _BLACKEN(b_frame.copy()).px == b_frame.px, 'layer() would repaint body + B: %s' % (arms,)
        bb.append((b_frame, ms))
        fc.append((face, ms))
        ca.append((card('a', **dict(arms, **kw)), ms))
    _check_smooth([f for f, _ in fc])

    # The "?": hops when he asks "hm? which one?", tilts while he waits, floats while he relaxes.
    p = 300                                       # a held beat after the cards settle into frame 0
    tl = T['upq'] - 100                           # the "?" tilts first, he looks up as it reaches full lean
    q = at_times([
        (0, qmark()),
        (p, qmark(1, 0)),                                          # hop: anticipation (squash, held)
        (p + 120, qmark(-1, 0)),                                   # launch (stretch)
        (p + 190, qmark(-2, -1)),
        (p + 280, qmark(-2)),                                      # apex hang
        (p + 410, qmark(-1, 0)),                                   # fall, dot leading (stretch)
        (p + 490, qmark(1, 0)),                                    # land (squash)
        (p + 580, qmark()),
        (tl, qmark(lean=1, rows=1)),                               # curious tilt: half-lean...
        (tl + 100, qmark(lean=1)),                                 # ...full lean, hold
        (tl + 600, qmark()),                                       # swings back through upright...
        (tl + 680, qmark(lean=-1, rows=1)),                        # ...a half-lean overshoot (2 > 1 > 0 rows)
        (tl + 780, qmark()),
        (T['relax'], qmark(-1, 0)),                                # as the cards go down it floats up, hook
        (T['rest'], qmark(-1)),                                    # first (stretch); the dot follows
        (T['arrive'], qmark(0, -1)),                               # sinks, hook first (soft squash)
        (T['howB'], qmark()),
    ], LOOP)

    # Glints on the story clock, so they always land on cue: one shaken loose by the hop's landing impact
    # (it drifts away as it fades), one on the bell 80 ms after he looks down at it, one off B's corner
    # inside the wink (all three phases fit in the 480 ms ^ hold).
    gl = twinkles([(p + 490, _HOP_GLINT), (T['down'] + 80, _BELL_GLINT), (WINK + 70, _WINK_GLINT)],
                  [(0, Frame())])
    # One ambient sky twinkle on its own co-prime loop (first pass: in the quiet hold after the tilt). The
    # loop ends on its dot, so the layer needs no trailing empty frame.
    tw = [e for e in twinkles([(_TW_LOOP - 310, (4, 3))], [(0, Frame())]) if e[0] < _TW_LOOP]

    scene = Frame()
    scene.place(_BELL, *_BELL_AT)
    return anim(NAME, DESC, [
        static('bell', scene),
        layer('qmark', q),
        static('clawd', st),
        layer('body_b', bb),                      # his eye rows + arms, and card B in his right claw
        layer('face', fc),                        # after the body (the cards never touch his face)
        layer('card_a', ca),
        layer('glints', at_times(gl, LOOP)),
        layer('twinkle', at_times(tw, _TW_LOOP)),
    ], state=STATE)
