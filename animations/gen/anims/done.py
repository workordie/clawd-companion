# ======================================================================================
# USER FEEDBACK: the user reviewed this fine-face upgrade draft personally and approved it
# ("looks great go"). Keep the scene, beats and fine-line expressions; critics, fixers and judges
# should polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""done - Claude finished the task while you were not looking.

Expressive fine-line face (STYLE.md 0b): his eyes act with the half-size kit (fine() + fine_face())
on top of the approved animation, whose body, hat, props, confetti and timing are unchanged.
Black ink eyes (the kit's), no mouth, no blush, never a full-cell arch, normal body size in every
frame. Face arc of the loop: content glow > curious (the last flake) > proud (trophy) > a wink >
calm > anticipation > sparkle (the burst) > thump > delight > content glow.

Storyboard (ms). Clawd, his face, his hat, the confetti and the trophy glints all run on one 7800 ms
timeline (_TIMELINE + _FACE below); the balloon and the twinkles have their own loops for variety.
     0  PROUD at HOME, party hat on, eyes closed in a CONTENT glow (thin cups, like u u): the
        afterglow of the ta-da. His trophy stands on the input box at his right, a violet balloon is
        tied there at his left. Confetti from the last burst still drifts down, every piece in open
        air (frame 0 = a full party still for reduced motion); a twinkle glints by the hat tip.
        The pieces sink out of sight behind the balloon, Clawd and the trophy ...
  1190  ... until one blue flake is left, drifting down the gap by his left side: his eyes open
        (half) ... 1260 catch it (a half-step glance left) ... 1680 follow it down (a full kit step
        down-left: it falls away, so his eyes travel further) ... 2480 it falls past row 19 and is
        gone (no piles), and his eyes come back to you on that very frame
  3380  a smooth blink (half, line, half) while his hand moves to his trophy (3520) ... 3590 his
        eyes open on it (half-step glance right) ... 3770 it shines and twinkles, and its gleam
        catches in his eyes for as long as it does (a white glint, 320 ms): a quiet promise of the
        sparkle to come
  4370  he looks back at you, hand still on the trophy ... 4580 and WINKS (thin line), a little
        star shining by the closed eye: "look what we did" ... 5070 hand back down, a long calm
        hold (940 ms of open eyes: the wink stands on its own) ...
  6010  ONE slow smooth blink (half, line, half) that opens looking UP (a full kit step: "here I
        go...") ... 6450 his eyes lead: back to you, SPARKLING (the big moment; a still 300 ms
        "watch this!" before take-off) ... 6530 he swings his arms down (normal body size)
  6750  take-off: 2 cells up, legs tucked, arms up ... 6820 apex, 1 more cell, arms flung wide: POP
        at both hands and the sparkle TWINKLES with them all through the hang (a second glint in
        each eye), then the CONFETTI BURST
        (confetti_a..d snap ~4 cells out in the first frame, ease out on drag arcs, tumble, then
        flutter; heavy bits fall fast, light flakes float) + two big sparkles echo his eyes, in
        front of the paper (no piece touches one: each keeps its clean star shape); two pieces
        cross over his head
  7050  fall: legs reach down, the hat floats behind ... 7120 THUMP: eyes squeezed to thin lines,
        arms swung down, dust_puff (the right puff stops short of the trophy's foot), the hat
        dropping 1 cell and drifting right (its drops: 0, 1, 2)
  7210  ta-da: a DELIGHTED squint (thin arcs, like ^ ^), one arm up, the other hand on his trophy;
        the hat lands a frame late, off-centre ... 7310 hops back ... 7420 settles while the trophy
        shines and twinkles ... 7690 the raised arm comes halfway down and the hand leaves the cup
        (overlap: the arms settle first) ... 7730 the arcs soften (line) ...
  7800  = frame 0 (arms at his sides, the content glow)
Eye closures: 0-1190 (content), 3380 (blink), 4580 (wink), 6010 (slow blink), 7120-7800 (thump,
delight): uneven gaps of 2.2, 1.2, 1.4 and 1.1 s, never a flutter.
Layers (back to front): fx (confetti, then the sparkles, pops and dust on top of it: behind
everything, so the confetti falls behind Clawd and his props) | trophy (static) | balloon (4100 ms
sway) | body (normal res, no eye cells: it only changes when his arms, legs or height do) | face
(FINE: every eye pixel at half size, a handful per frame, plus the wink's star on the wink's own
frames) | hat (same timeline as the body, in its own layer only so its frames merge while it
rests) | glint (FINE: the trophy's shines and twinkles, and on those very frames the gleam in his
eyes) | twinkle (4700 ms). Body, face and hat are cut from the same beat list, so they never
drift; every layer on the main timeline is exactly 7800 ms.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *          # noqa: E402,F401,F403
from acc import get              # noqa: E402

NAME = 'done'
STATE = 'Claude finished the task (you have not looked yet)'
DESC = ('Sparkle-eyed, he jumps for joy in a confetti burst (his party hat lands a beat late), beams '
        'with a delighted squint and glows contentedly, follows the last flake down, then rests a '
        'proud hand on his trophy and winks at you.')

_HAT = get('party_hat')
_TROPHY = get('trophy')
_BALLOON = get('balloon')
_DUST = get('dust_puff')
_SPARK = get('sparkle')
_SPARK_S = get('sparkle_small')
# confetti tumble frames from the library, each piece in ONE colour (the tumble is in the shape):
# at 3 px a cell the two-tone flicker does not read, and every extra colour costs an SVG path in
# a dozen burst frames. Red strips, gold curls, green ribbons and blue flakes: blue, not cyan, so
# the last flake stays blue and reads on the light theme too (3.4:1 on white; cyan is 2.0:1).
_ONE = {'a': {'p': 'r', 'R': 'r'}, 'b': {'c': 'b'}, 'c': {'o': 'j'}, 'd': {'G': 'g'}}
_CONF = {k: [s.recolor(_ONE[k]) for s in get('confetti_' + k).frames] for k in 'abcd'}

TROPHY_AT = (24, GROUND)        # grip anchor = left end of its base: the cup spans x 22..30, rows 12..19
BALLOON_AT = (4, GROUND)        # string tied to the input box; the balloon floats at rows 9..13
_VIOLET = {'r': 'v', 'R': 'V'}  # cool violet balances the warm gold trophy, echoes the hat's pom-pom
                                # and is a color no confetti piece uses

# ------------------------------------------------------------------ Clawd + hat
# User preferences (STYLE.md sections 0 and 0b): normal body size in every frame (no crouch, squash
# or stretch); his face acts only with the fine-line kit (no mouth, no blush, no full-cell arches).
# These poses are the approved PLAIN-face body (kit eyes); the confetti uses them to know where it
# hides behind him. The drawn Clawd takes their arms and legs, and his eyes from _FACE below
# (the body layer is drawn with no eye cells; the fine face layer draws every eye pixel).
PROUD = clawd()                                                 # arms at his sides
BLINK = clawd(eyes='blink')
TRACK = clawd(eyes='look_l')                                    # catches the last flake at eye level
WATCH = clawd(eyes='look_dl')                                   # ... and follows it down
GLANCE = clawd(eyes='look_r', rarm='out')                       # admires his trophy, hand on it
SHOWOFF = clawd(rarm='out')                                     # ... and looks back at you
LOOKUP = clawd(eyes='look_u')                                   # "here I go..."
WINDUP = clawd(eyes='look_u', larm='down', rarm='down')         # arms swing back down
LAUNCH = clawd(eyes='look_u', larm='raise', rarm='raise', legs='short')
APEX = clawd(larm='wave', rarm='wave', legs='short')            # flings the confetti, faces you
FALL = clawd(larm='raise', rarm='raise')                        # legs reach for the ground
LAND = clawd(eyes='blink', larm='down', rarm='down')            # thump
TADA = clawd(larm='raise', rarm='out')                          # ta-da: hand on the trophy
SETTLE = clawd(larm='up')                                       # in-between into frame 0: the raised
                                                                # arm halfway down, hand off the cup

# (pose, box y, hat offset (dx, dy) from where it sits on his head, ms, tag)
# The party ends the loop, so frame 0 is the calm pose right after the ta-da, with the confetti
# still in the air. Rows of the calm part come after the confetti physics (they follow its flake).
_JUMP = [
    (LOOKUP, 12, (0, 0), 200, ''),      # anticipation: looks up ...
    (WINDUP, 12, (0, 0), 220, ''),      # ... winds up
    (LAUNCH, 10, (0, 0), 70, ''),       # take-off: 2 cells, legs tucked
    (APEX, 9, (0, 0), 230, 'burst'),    # 1 more cell, then hang time
    (FALL, 10, (0, -1), 70, ''),        # the hat floats behind ...
    (LAND, 12, (1, -2), 90, 'land'),    # thump; the hat drops 1, drifting right (spacing 0, 1, 2)
    (TADA, 12, (1, 0), 100, ''),        # it lands a frame late, off-centre ...
    (TADA, 12, (0, -1), 110, ''),       # ... hops back to the middle
    (TADA, 12, (0, 0), 270, ''),
    (SETTLE, 12, (0, 0), 110, ''),      # the arms settle (raise > up > side) a beat before the eyes
]
_SEAM = sum(row[3] for row in _JUMP[[row[4] for row in _JUMP].index('burst'):])  # confetti age at frame 0


def _plain_body_frames():
    """The approved plain-face Clawd on the timeline. Not drawn: the confetti uses it to know which
    cells hide it (his eyes are opaque ink either way, so he covers exactly the cells the drawn,
    eyeless body + fine face does)."""
    out = []
    for pose, y, _, ms, _ in _TIMELINE:
        f = Frame()
        put_clawd(f, pose, HOME[0], y)
        out.append((f, ms))
    return out


def hat_frames():
    """The party hat, worn on the very same pose every frame of the same timeline, drawn over Clawd.
    In its own layer only so that its frames merge while it rests: it hangs in the air at the top
    of the jump while he moves under it."""
    out = []
    for pose, y, (hdx, hdy), ms, _ in _TIMELINE:
        f = Frame()
        wear(f, _HAT, pose, HOME[0], y, dx=hdx, dy=hdy)
        out.append((f, ms))
    return out


# ------------------------------------------------------------------ confetti
# Physics: a piece leaves the hand at (dx * K, -lift * K) cells/s; air drag K eases it out to dx
# cells sideways while it rises, stalls and then falls at its terminal speed vt, with a sideways
# flutter. Heavy bits (strips, curls) fall fast; light flakes (vt < 8) float, sway and tumble at
# half rate. A piece that sinks out of sight behind the balloon, Clawd, his hat or the trophy is
# gone for good (it never peeks out between his feet or under the cup); the rest fall past row 19.
# Each piece is AIMED by where it is in frame 0 (the loop seam, 980 ms after the burst): the
# reduced-motion still shows every visible piece in open air, none touching the balloon, the hat,
# the trophy, the twinkle or another piece. _launch() solves dx and lift from that cell.
# (type, hand, frame-0 x, y, vt (cells/s), tumble offset, flutter amplitude (cells), Hz, phase)
_AIM = [
    ('a', 'l', 7, 15, 10.0, 0, 0.6, 1.1, 0.0),    # strip lobbed low: drops past his left side
    ('c', 'l', 3, 6, 8.6, 2, 0.3, 1.3, 2.1),      # curl high over the balloon, sinks behind it
    ('b', 'l', 7, 5, 6.0, 1, 0.8, 0.5, 2.2),      # THE LAST FLAKE: drifts down the gap between the
                                                  # balloon and his side while he watches it
    ('d', 'l', 15, 9, 7.2, 0, 0.5, 0.9, 0.7),     # ribbon over his head, sinks behind the hat
    ('b', 'l', 10, 7, 8.6, 2, 0.6, 0.8, 6.07),    # sways in behind his shoulder
    ('b', 'r', 16, 10, 9.4, 0, 0.4, 0.9, 0.4),    # crosses the ribbon over his head, behind the hat
    ('a', 'r', 27, 9, 9.8, 1, 0.6, 1.2, 1.9),     # over the trophy ...
    ('c', 'r', 24, 8, 9.2, 3, 0.6, 1.3, 3.6),
    ('b', 'r', 22, 5, 7.6, 3, 1.2, 0.4, 2.07),    # ... a flake that sways right, behind the cup
    ('d', 'r', 27, 5, 7.4, 0, 1.0, 1.0, 0.2),
]
_LAST_FLAKE = 2
_K = 8.0                         # air drag (1/s): a snappy pop that quickly turns into a flutter
_HANDS = {'l': APEX.at('hand_l', HOME[0], 9), 'r': APEX.at('hand_r', HOME[0], 9)}
# burst-relative frame grid while it pops; up to 600 ms it doubles as the grid of the sparkles and
# the dust, then even ~130 ms steps up to the loop seam
_POP = [0, 70, 150, 230, 300, 390, 490, 600]
_n = max(1, int(round((_SEAM - 600) / 130.0)))
_POP += [600 + int(round((_SEAM - 600) * k / float(_n))) for k in range(1, _n + 1)]


def _launch(aim):
    """(type, hand, x, y at the seam, ...) -> (type, hand, dx, lift, ...): the throw that puts the
    piece's anchor exactly on that cell in frame 0."""
    typ, hand, x, y, vt, tumble, amp, hz, ph = aim
    x0, y0 = _HANDS[hand]
    t = _SEAM / 1000.0
    e = math.exp(-_K * t)
    flutter = amp * (1 - e) * math.sin(2 * math.pi * hz * t + ph)
    dx = (x - x0 - flutter) / (1 - e)
    lift = (y0 + vt * t - y) / (1 - e) - vt / _K
    return (typ, hand, dx, lift, vt, tumble, amp, hz, ph)


_PIECES = [_launch(a) for a in _AIM]


def _piece_xy(p, age):
    """Drag physics: x eases out to dx (+ a flutter); y rises, stalls, then falls at vt."""
    _, hand, dx, lift, vt, _, amp, hz, ph = p
    x0, y0 = _HANDS[hand]
    t = age / 1000.0
    e = math.exp(-_K * t)
    x = x0 + dx * (1 - e) + amp * (1 - e) * math.sin(2 * math.pi * hz * t + ph)
    y = y0 + vt * t - (lift + vt / _K) * (1 - e)
    return int(round(x)), int(round(y))


def _visible(p, age):
    return _piece_xy(p, age)[1] <= GROUND


def _schedule():
    """Sample ages (ms after the burst): the pop grid, then one step per 140 ms while heavy bits
    fall, then one per 160 ms while only the light flakes float. Ends when everything is gone."""
    ages = list(_POP)
    a = ages[-1]
    while True:
        fast = any(_visible(p, a) and p[4] > 8 for p in _PIECES)
        a += 140 if fast else 160
        ages.append(a)
        if not any(_visible(p, a) for p in _PIECES):
            return ages


_AGES = _schedule()
_LIFE = _AGES[-1]


def _piece_cells(p, idx):
    """Canvas cells of piece p at sample idx (tumbling: heavy bits flip every sample, flakes every
    other sample, so the field never flips all at once)."""
    x, y = _piece_xy(p, _AGES[idx])
    step = idx if p[4] > 8 else idx // 2
    frames = _CONF[p[0]]
    spr = frames[(p[5] + step) % len(frames)]
    return [(x + sx - spr.ax, y + sy - spr.ay, ch) for sx, sy, ch in spr.cells]


# ------------------------------------------------------------------ the calm part of the timeline
# His eyes follow the last flake: they catch it at eye level (look left), follow it down (look
# down-left) and come back to you the very moment it falls past row 19, whatever the aim above.
_EYE_ROW = HOME[1] + PROUD.anchors['eye_l'][1]


def _flake_times():
    p = _PIECES[_LAST_FLAKE]
    marks = {}
    for a in _AGES:
        y = _piece_xy(p, a)[1]
        if a >= _SEAM:
            if y >= _EYE_ROW - 1:
                marks.setdefault('track', a - _SEAM)
            if y > _EYE_ROW:
                marks.setdefault('watch', a - _SEAM)
            if y > GROUND:
                marks['gone'] = a - _SEAM
                break
    return marks['track'], marks['watch'], marks['gone']


T_TRACK, T_WATCH, T_GONE = _flake_times()       # 1260, 1680, 2480 ms into the loop
_CALM = [
    (PROUD, 12, (0, 0), T_TRACK, ''),
    (TRACK, 12, (0, 0), T_WATCH - T_TRACK, ''),     # catches the last flake at eye level ...
    (WATCH, 12, (0, 0), T_GONE - T_WATCH, ''),      # ... follows it down until it is gone
    (PROUD, 12, (0, 0), 3400 - T_GONE, ''),
    (BLINK, 12, (0, 0), 120, ''),       # blinks as his gaze moves ...
    (GLANCE, 12, (0, 0), 850, 'glance'),  # ... to his trophy, and his hand rests on it
    (SHOWOFF, 12, (0, 0), 700, 'showoff'),  # "look what we did"
    (PROUD, 12, (0, 0), 1260, ''),      # a long calm hold; one slow blink carries his eyes up
]
_TIMELINE = _CALM + _JUMP
LOOP = sum(row[3] for row in _TIMELINE)


def _tag_time(tag):
    t = 0
    for row in _TIMELINE:
        if row[4] == tag:
            return t
        t += row[3]
    raise KeyError(tag)


T_GLANCE = _tag_time('glance')
T_SHOWOFF = _tag_time('showoff')
T_BURST = _tag_time('burst')
T_LAND = _tag_time('land')
T_LAUNCH = T_BURST - _JUMP[2][3]
T_TADA = T_LAND + _JUMP[5][3]
T_SHINE = T_GLANCE + 250                # the trophy shines while he admires it (3770)
T_WINK = T_SHOWOFF + 210                # ... he looks back at you and winks (4580)
T_SPARKLE = T_LAUNCH - 300              # sparkle eyes: a still 300 ms before take-off (6450)
T_UP = T_SPARKLE - 210                  # ... after a slow blink that opens looking up (6240)


# ------------------------------------------------------------------ his face (fine-line kit)
# (start ms, eyes): (left eye, right eye) are FINE_EYES names drawn with fine_face() (or a local
# variant from _GLINTS); a plain string is a kit glance (clawd(eyes=...)), kept where a full-cell
# eye move reads best at 3 px.
CONTENT, HAPPY, SPARKLE, LINE = ('content',) * 2, ('happy',) * 2, ('sparkle',) * 2, ('line',) * 2
OPEN, HALF, LOOK_R, TWINKLE = ('open',) * 2, ('half',) * 2, ('look_r',) * 2, ('twinkle',) * 2
# local variant: (FINE_EYES base, extra fine pixels from the top-left of each eye cell, the same
# for both eyes: light comes from one side)
_GLINTS = {
    'twinkle': ('sparkle', [(1, 1, 'W')]),  # the sparkle twinkles: a 2nd glint, bottom-right (as done-party)
}
# A third value in a face event is the wink's little star (a sparkle_small frame) by his closed eye:
# drawn in the face layer, so it rides the wink's own frames and costs none of its own.
WINK_AT = (9, 11)                 # by the outer corner of his winking (screen-left) eye, clear of the
                                  # hat (x >= 12) and the balloon; no confetti in the air then


def _blink(t, eyes=OPEN, half=60, line=80):
    """Smooth fine blink: half > line > half > back to `eyes`. Returns (events, end time)."""
    ev = [(t, HALF), (t + half, LINE), (t + half + line, HALF), (t + 2 * half + line, eyes)]
    return ev, t + 2 * half + line


def _face_track():
    ev = [(0, CONTENT)]                         # the afterglow: a content glow while confetti falls
    ev += [(T_TRACK - 70, HALF),                # his eyes open as the last flake drifts by ...
           (T_TRACK, ('look_l', 'look_l')),     # ... catch it at eye level (half a step) ...
           (T_WATCH, 'look_dl'),                # ... follow it down (a full kit step: it falls away) ...
           (T_GONE, OPEN)]                      # ... and come back to you when it is gone
    ev += [(T_GLANCE - 140, HALF), (T_GLANCE - 80, LINE),   # a smooth blink while his hand goes to
           (T_GLANCE, HALF), (T_GLANCE + 70, LOOK_R)]       # the trophy; eyes open on it (when it
                                                            # shines, the glint layer puts its gleam
                                                            # in his eyes)
    ev += [(T_SHOWOFF, OPEN)]                   # looks back at you ...
    w = T_WINK                                  # ... and winks: "look what we did"; a little star
    ev += [(w, ('half', 'open')),               # shines by the eye while it is closed
           (w + 60, ('line', 'open', 1)), (w + 430, ('half', 'open')), (w + 490, OPEN)]
    # a long calm hold, then ONE slow blink that opens looking up (a full kit step, so the eye
    # roll reads at 3 px): "here I go..." ...
    ev += _blink(T_UP - 230, eyes='look_u', half=70, line=90)[0]
    ev += [(T_SPARKLE, SPARKLE)]                # ... then at you, eyes sparkling, still, a beat before
                                                # his arms swing down ("watch this!")
    ev += [(T_BURST, TWINKLE)]                  # apex: the sparkle twinkles with the pops, all
                                                # through the hang (a 2nd glint) ...
    ev += [(T_BURST + _JUMP[3][3], SPARKLE)]    # ... and shines on as he falls
    ev += [(T_LAND, LINE)]                      # thump: eyes squeezed shut
    ev += [(T_TADA, HAPPY)]                     # ta-da: a delighted squint
    ev += [(LOOP - 70, LINE)]                   # it softens into the content glow of frame 0
    return sorted(ev, key=lambda e: e[0])


_FACE = _face_track()


def _beats():
    """Cut the body timeline and the face track into one beat list: [(ms, timeline row, eyes)].
    The body only changes where his arms, legs or height do (his eyes come from _FACE now)."""
    starts, t, cuts, prev = [], 0, set(), None
    for row in _TIMELINE:
        starts.append(t)
        body = (row[0].spec['larm'], row[0].spec['rarm'], row[0].spec['legs'], row[1])
        if body != prev:
            cuts.add(t)
        prev = body
        t += row[3]
    times = sorted(cuts | {t for t, _ in _FACE if t < LOOP})
    out = []
    for i, t in enumerate(times):
        end = times[i + 1] if i + 1 < len(times) else LOOP
        row = _TIMELINE[max(k for k, s in enumerate(starts) if s <= t)]
        eyes = [e for tt, e in _FACE if tt <= t][-1]
        out.append((end - t, row, eyes))
    return out


def _clawd_split(pose, x, y, eyes):
    """Clawd split into a normal-res body with NO eye cells (the kit's 'blink' eyes: it only
    changes when his arms, legs or height do, so its frames merge while his face acts) and a fine
    overlay holding every half-size eye pixel (the trick of done-party). A fine-line expression
    (eyes = (left, right) [, wink star frame]) is drawn with fine(frame) + fine_face() (+ a local
    glint); a kit glance (eyes = a kit eye name) is the kit's eye cells at half size. The two
    layers composite to exactly fine(frame) + fine_face(...), or exactly the kit's glance."""
    s = pose.spec
    limbs = dict(larm=s['larm'], rarm=s['rarm'], legs=s['legs'])
    p = clawd(eyes='blink', **limbs)
    f = Frame()
    put_clawd(f, p, x, y)
    star = None
    if isinstance(eyes, str):
        g = Frame()
        put_clawd(g, clawd(eyes=eyes, **limbs), x, y)
        ff = fine(g)
    else:
        eyes, star = tuple(eyes[:2]), (eyes[2] if len(eyes) > 2 else None)
        ff = fine(f)
        fine_face(ff, p, x, y, *[_GLINTS.get(e, (e,))[0] for e in eyes])
        for e, key in zip(eyes, ('eye_l', 'eye_r')):
            ex, ey = p.at(key, x, y)
            for dx, dy, ch in _GLINTS.get(e, (e, []))[1]:
                ff.put(2 * ex + dx, 2 * ey + dy, ch)
    face = Frame(res=2)
    face.meta = {'fine_face': [(eyes,) if isinstance(eyes, str) else eyes]}
    if star is not None:                            # the wink's star, in open air by his eye
        s_f = Frame()
        s_f.place(_SPARK_S.sprite(star), *WINK_AT)
        face.px.update(fine(s_f).px)
    for key in ('eye_l', 'eye_r'):
        ex, ey = p.at(key, x, y)
        for cy in range(ey - 1, ey + 2):            # fine_face and the kit glances stay within
            for cx in range(ex - 1, ex + 2):        # one cell of the eye
                quad = [(2 * cx + k % 2, 2 * cy + k // 2) for k in range(4)]
                b = f.px.get((cx, cy))
                if any(ff.px.get(q) is None for q in quad):    # see-through eye pixels (only if
                    f.px.pop((cx, cy), None)                   # the kit ever draws holes again):
                    b = None                                   # cut the body cell, redraw the rest
                for q in quad:
                    if ff.px.get(q) not in (None, b):
                        face.px[q] = ff.px[q]
    return f, face


def clawd_frames():
    body, face = [], []
    for ms, (pose, y, _, _, _), eyes in _beats():
        bf, fc = _clawd_split(pose, HOME[0], y, eyes)
        body.append((bf, ms))
        face.append((fc, ms))
    return body, face


# ------------------------------------------------------------------ drawing the confetti
_GONE_AT = {}


def _gone_age(i):
    """Age (ms) from which piece i is no longer drawn: it fell past row 19 or, on its way down, it
    sank completely out of sight behind the props or Clawd (whatever covers the fx layer then)."""
    if not _GONE_AT:
        spans = _occluders()
        for k, p in enumerate(_PIECES):
            vt, lift = p[4], p[3]
            peak = 1000.0 * math.log(max(1.0, (lift * _K + vt) / vt)) / _K
            gone = _LIFE
            for idx, a in enumerate(_AGES):
                if a < _POP[1]:
                    continue
                cells = _piece_cells(p, idx)
                if _piece_xy(p, a)[1] > GROUND:
                    gone = a
                    break
                t = (T_BURST + a) % LOOP
                hidden = next(c for s, e, c in spans if s <= t < e)
                if a > peak and all((x, y) in hidden for x, y, _ in cells):
                    gone = a
                    break
            _GONE_AT[k] = gone
    return _GONE_AT[i]


def _draw_confetti(f, age):
    if age < _POP[1] or age >= _LIFE:      # the first beat is the pop flash at his hands
        return
    idx = max(i for i, a in enumerate(_AGES) if a <= age)
    for k, p in enumerate(_PIECES):
        if _AGES[idx] < _gone_age(k):
            for x, y, ch in _piece_cells(p, idx):
                if 0 <= x < W and 0 <= y < H:
                    f.put(x, y, ch)


# ------------------------------------------------------------------ one-shot effects
def _seq(item, frames, ms):
    return [(item.sprite(i), m) for i, m in zip(frames, ms)]


def _trophy_shine():
    """The trophy's own glint (library frame 1) as an overlay: only the cells that differ from
    frame 0, placed with the trophy's anchor."""
    s0 = _TROPHY.sprite(0)
    s1 = _TROPHY.sprite(1) if len(_TROPHY) > 1 else s0
    base = {(x, y): ch for x, y, ch in s0.cells}
    diff = [(x, y, ch) for x, y, ch in s1.cells if base.get((x, y)) != ch]
    if not diff:                                  # no glint frame in the library: a small streak
        diff = [(3, 1, 'W'), (3, 2, 'W'), (4, 2, 'Y')]
    return Sprite(cells=diff, anchor=(s0.ax, s0.ay))


def _dust():
    """The library dust_puff, fitted into the gaps between the balloon string (x 4), his feet and
    the trophy (foot x 25-27, base x 24-28): frame 0 as is; frame 1 rolls 1 cell less far out (the
    library's frame 1 would touch the string), and the right puff, squeezed by the trophy, loses
    its outer column: 3 wide (x 21-23), a clear cell from his leg and from the trophy's foot, its
    outer bottom cell tan where it meets the dark-gold base (wood would smear into it); then the
    puffs thin out to the wisp on top of each (the library's wide frame 2 would leave specks stuck
    to the string and the trophy stem)."""
    s0, s1 = _DUST.sprite(0), _DUST.sprite(1)
    c1 = [(x + (1 if x < s1.ax else -1), y, 't' if ch == 'w' else ch) for x, y, ch in s1.cells]
    edge = max(x for x, _, _ in c1)                       # the right puff loses its outer column:
    c1 = [c for c in c1 if c[0] != edge]                  # 3 wide, a clear cell from his leg and
    edge, bottom = edge - 1, max(y for _, y, _ in c1)     # from the trophy's foot
    c1 = [(x, y, 't' if (x, y) == (edge, bottom) else ch) for x, y, ch in c1]
    top = min(y for _, y, _ in c1)
    c2 = [(x, y, 't') for x, y, _ in c1 if y == top]
    return [s0, Sprite(cells=c1, anchor=(s1.ax, s1.ay)), Sprite(cells=c2, anchor=(s1.ax, s1.ay))]


# white twinkles kept inside the cup (gold ones would vanish on gold, white ones on the light
# theme if they touched the background)
_G_SHINE = _trophy_shine()
_G_PLUS = Sprite(['.W.', 'WWW', '.W.'], anchor=(1, 1))
_G_DOT = Sprite(['W'], anchor=(0, 0))
_G_AT = (TROPHY_AT[0] + 2, TROPHY_AT[1] - 5)     # middle of the cup
_DUST_F = _dust()
_B = T_BURST
# pop flashes just past his flung hands (on the line of each arm), fully visible behind him
_POP_AT = {'l': (_HANDS['l'][0] - 1, _HANDS['l'][1]), 'r': (_HANDS['r'][0] + 1, _HANDS['r'][1])}
# (start ms, anchor position, [(sprite, ms), ...])
_FX_EVENTS = [                    # behind Clawd and his props, in front of the confetti
    (_B, _POP_AT['l'], _seq(_SPARK_S, [1], [_POP[1]])),        # pop! ...
    (_B, _POP_AT['r'], _seq(_SPARK_S, [1], [_POP[1]])),        # ... and the confetti flies out
    (_B, (7, 4), _seq(_SPARK, [0, 1, 2, 3], [70, 80, 80, 70])),
    (_B + 150, (27, 4), _seq(_SPARK, [0, 1, 2, 3], [80, 70, 90, 100])),
    (T_LAND, (15, GROUND - 1), list(zip(_DUST_F, [90, 100, 110]))),    # on the pop grid
]
_HALO = {id(s) for s in _SPARK.frames}      # the big stars outshine the paper right around them:
                                            # no confetti cell touches one (a gold curl would melt
                                            # into it), so each flash keeps its clean silhouette
_GLINT_EVENTS = [                 # in front of the trophy
    (T_SHINE, TROPHY_AT, [(_G_SHINE, 120)]),
    (T_SHINE + 120, _G_AT, [(_G_PLUS, 110), (_G_DOT, 90)]),
    # after the landing, on the confetti's own frame grid: shine, twinkle, fading dot at the seam
    (_B + _POP[-4], TROPHY_AT, [(_G_SHINE, _POP[-3] - _POP[-4])]),
    (_B + _POP[-3], _G_AT, [(_G_PLUS, _POP[-2] - _POP[-3]), (_G_DOT, _POP[-1] - _POP[-2])]),
]
# the trophy's gleam in his eyes while it shines and twinkles (he is looking right at it, half a
# step): a half-size white glint at the top-left of each eye, like the sparkle to come
_GLEAM = (T_SHINE, T_SHINE + 320)
_GLEAM_PX = [(2 * ex + 1, 2 * ey) for ex, ey in (GLANCE.at('eye_l'), GLANCE.at('eye_r'))]
assert ([e for t, e in _FACE if t <= _GLEAM[0]][-1] == LOOK_R and
        min(t for t, _ in _FACE if t > _GLEAM[0]) >= _GLEAM[1]), 'the gleam needs his eyes on the trophy'


def glint_frames():
    """The glint layer, FINE: the trophy's shines and twinkles (whole cells, doubled) and, on the
    very same frames, the gleam in his eyes (half-size pixels): in sync, at no extra frame."""
    out, t = [], 0
    for f, ms in _event_frames(_GLINT_EVENTS):
        ff = fine(f)
        if _GLEAM[0] <= t < _GLEAM[1]:
            for x, y in _GLEAM_PX:
                ff.put(x, y, 'W')
        out.append((ff, ms))
        t += ms
    return out


def _trophy_frame():
    f = Frame()
    f.place(_TROPHY.sprite(0), *TROPHY_AT)
    return f


def _occluders():
    """[(start, end, cells)] covered by the layers drawn over the fx layer: Clawd + hat on the
    timeline, plus the trophy and the cells the swaying balloon covers in every frame. Clawd is
    the approved plain-face body here: same arms, legs and height as the drawn one, and his eyes
    (black ink) are opaque either way, so he covers exactly the same cells."""
    always = set(_trophy_frame().px)
    sway = [set(f.px) for f, _ in balloon_frames()]
    always |= set.intersection(*sway)
    spans, t = [], 0
    for (bf, ms), (hf, _) in zip(_plain_body_frames(), hat_frames()):
        spans.append((t, t + ms, set(bf.px) | set(hf.px) | always))
        t += ms
    return spans


def _event_frames(events, confetti=False, behind=False):
    """Frames of a layer on the main timeline (LOOP ms): one-shot events (+ the confetti).
    behind=True: the layer sits under Clawd and his props, so cells they hide for the whole frame
    are left out (same picture, smaller SVG)."""
    times = {0}
    if confetti:
        times |= {(T_BURST + a) % LOOP for a in _AGES}
    for start, _, seq in events:
        t = start
        for _, ms in seq:
            times.add(t % LOOP)
            t += ms
        times.add(t % LOOP)
    ts = sorted(times)
    spans = _occluders() if behind else []
    out = []
    for i, t in enumerate(ts):
        end = ts[i + 1] if i + 1 < len(ts) else LOOP
        f = Frame()
        if confetti:                                 # the paper first: the flashes of light (stars,
            _draw_confetti(f, (t - T_BURST) % LOOP)  # pops) and the dust sit in front of it
        for start, (x, y), seq in events:
            tt = (t - start) % LOOP                  # events may wrap over the loop seam
            for spr, ms in seq:
                if 0 <= tt < ms:
                    if id(spr) in _HALO:
                        for sx, sy, _ in spr.cells:
                            cx, cy = x + sx - spr.ax, y + sy - spr.ay
                            for n in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                                f.px.pop(n, None)
                    f.place(spr, x, y)
                    break
                tt -= ms
        if behind:
            hidden = set.intersection(*[c for s, e, c in spans if s < end and e > t])
            for cell in hidden:
                f.px.pop(cell, None)
        out.append((f, end - t))
    return out


# ------------------------------------------------------------------ ambient twinkles (own loop)
TW_LOOP = 4700                  # 47 vs 78 (x100 ms): the twinkles land somewhere new each time
TW_MS = 110
_TW = [  # (start, position, frames of sparkle_small); the first one is already lit at t = 0
    (0, (13, 3), [1, 2, 1]),             # beside the hat tip, clear of the balloon and the burst stars
                                         # (dot > plus > x > plus > gone, like idle-moods' twinkle)
    (2900, (29, 9), [0, 1]),             # over the trophy's rim, out of the right burst star's reach
    (TW_LOOP - TW_MS, (13, 3), [0]),
]


def twinkle_frames():
    times = {0}
    for start, _, seq in _TW:
        times |= {start + k * TW_MS for k in range(len(seq) + 1)}
    ts = sorted(t for t in times if t < TW_LOOP)
    out = []
    for i, t in enumerate(ts):
        f = Frame()
        for start, pos, seq in _TW:
            k = (t - start) // TW_MS
            if t >= start and k < len(seq):
                f.place(_SPARK_S.sprite(seq[k]), *pos)
        out.append((f, (ts[i + 1] if i + 1 < len(ts) else TW_LOOP) - t))
    return out


# ------------------------------------------------------------------ balloon (own loop)
# long upright rests with an uneven nudge each way: a breeze, not a metronome (4100 ms)
_SWAY = [(0, 1700), (1, 500), (0, 1400), (2, 500)]


def balloon_frames():
    out = []
    for i, ms in _SWAY:
        f = Frame()
        f.place(_BALLOON.sprite(i).recolor(_VIOLET), *BALLOON_AT)
        out.append((f, ms))
    return out


def build():
    body, face = clawd_frames()
    return anim(NAME, DESC, [
        layer('fx', _event_frames(_FX_EVENTS, confetti=True, behind=True)),
        static('trophy', _trophy_frame()),
        layer('balloon', balloon_frames()),
        layer('body', body),
        layer('face', face),
        layer('hat', hat_frames()),
        layer('glint', glint_frames()),
        layer('twinkle', twinkle_frames()),
    ], state=STATE)
