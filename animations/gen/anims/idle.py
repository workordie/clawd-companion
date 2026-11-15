# ======================================================================================
# USER FEEDBACK: the user reviewed this fine-face upgrade draft personally and approved it
# ("looks great go"). Keep the scene, beats and fine-line expressions; critics, fixers and judges
# should polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""idle - Session idle: waiting for your prompt.   (expressive fine-line face, STYLE.md 0b)

STORYBOARD (s)    one loop = 21.44 s, mostly holds, punctuated by small life moments at uneven times.
                  His face acts with half-size (fine) pixels: smooth blinks, half-step glances, the
                  firefly's light sparkling in his eyes, one content (u u) and one happy (^ ^) moment.
   0.00  HOLD: neutral at HOME, the official open (black) eyes looking at you (frame 0 = the
         reduced-motion still; the face and firefly layers are empty)
   2.70  smooth blink: half > line > half > open (0.25 s)
   4.32  half-step glance up toward the chat .. hold 1.25 s .. back
   7.47  he settles in: a slow, contented blink; the lids lead and both arms relax a cell under the
         closed lids (7.57) .. eyes open (7.97) .. arms back (8.22)
  10.20  half-step glance down at the input box: an unhurried tap .. tap of one foot .. eyes back (11.38)
  12.44  FIREFLY drifts in at the left edge, bobbing.  He glances at it from the corner of his eye
         (12.59) .. double blink "huh?" (12.73 / 13.11: two distinct blinks); under the lids his eyes
         find it up-left (13.31) and he stares at it (it goes dark and hovers once, 13.54) .. it peaks
         above him (14.24) and a beat later his eyes catch up (14.31): left > up-left > up, on an arc
  14.53  it slows down as it comes in to land (ease-in) and its glow SPARKLES in his eyes ..
  15.34  .. it settles on his head; its glow lights the top of his head (body_light: 1 cell, 3 at the
         peak).  As the glow swells (15.62) he closes his eyes, CONTENT (u u), and basks in it for
         0.75 s .. it dims (16.25) .. a beat later he opens them and looks up: hm? (16.37) .. it glows
         again: sparkle (16.75)
  16.97  lift-off (ease-out), up and to the right; his sparkling eyes follow it up-right (17.21); the
         sparkle goes out when its light does (17.87); it hovers dark (18.01) and glows back (18.25)
         right where he is looking, up-right
  18.88  his hand comes up (an in-between, then the kit's raised arm at 18.95): bye!  It pulses back
         once (19.03); a beat later he smiles, HAPPY (^ ^) (19.12 / 19.20), as it drifts out at the
         top right
  19.60  the hand comes down the way it went up (down at 19.67), still smiling (the smile outlasts the
         wave) .. his eyes open as it vanishes (19.77 / 19.84): he watches the top corner where it
         went .. blink (20.54); under the closed lids his eyes come back to you
  20.79  HOLD -> loop: 0.65 s + the 2.7 s opening hold = one calm 3.35 s hold across the seam
Eye closures: 2.70, 7.47, 12.73 + 13.11, 15.55-16.44 (content), 19.12-19.84 (happy), 20.54 s.

Face: the kit's fine_face() expressions (open / half / line / sparkle / content / happy), each moved
by a half-step gaze (c l r u d ul ur: one fine pixel), so a blink or the sparkle keeps looking where
he looks; gaze 'c' is fine_face() itself, 'l' 'r' 'u' 'd' + open equal the kit's fine look_*.  The eye
colour is the kit's (black ink, STYLE.md 0).  No mouth, no blush, never resized; the arms are kit
shapes and the toe tap (outer right foot one cell up) is the one hand-made body variant.
Layers: trunk (STATIC: the kit body with the official eyes, minus the arms and the outer right foot)
| limbs (only those cells: they change with the arms and the tap) | face (FINE: only the half-size
eye pixels that differ from the trunk, so the official open eyes cost nothing) | firefly.  Trunk,
limbs and face are cut from ONE acting list, the firefly from its flight list; both lists are exactly
one loop long and every change lands on a shared time or >= 40 ms apart.  While it is near, his eyes
point at the firefly (his gaze is never more than ~26 deg off it), except for the first glimpse and
the double blink, which trail it on purpose.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'idle'
STATE = 'Session idle: waiting for your prompt'
DESC = ('Waits calmly at home with fine-line eyes: smooth blinks, half-step glances at the chat and the '
        'input box, a contented slow blink, a toe tap, and a firefly whose glow sparkles in his eyes; he '
        'closes them contentedly while it rests on his head, then smiles as he waves it goodbye.')

LOOP = 21440

# ---------------------------------------------------------------- Clawd: trunk (static) | limbs | face
HX, HY = HOME
_FOOT_R = (9, GEOM['normal']['ly'] + GEOM['normal']['ll'] - 1)   # his outer right foot (box cell)
_FOOT = (HX + _FOOT_R[0], HY + _FOOT_R[1])
_ARMS = {'side': ('side', 'side'), 'down': ('down', 'down'),     # down = relaxed
         'up': ('side', 'up'), 'raise': ('side', 'raise')}         # bye: up is the in-between


def _pose(arms='side', tap=False):
    la, ra = _ARMS[arms]
    p = clawd(larm=la, rarm=ra)
    if tap:
        # toe tap: the kit's outer right leg, one cell shorter (the foot lifts off the input box)
        cells = [c for c in p.sprite.cells if (c[0], c[1]) != _FOOT_R]
        p = Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec, tap=True))
    return p


# Clawd is split by what changes, so each part costs only its own changes: the trunk (the kit body with
# the official eyes, minus the arms and the tapping foot) never changes; the limbs layer holds only
# those cells; the fine face layer only the half-size eye pixels that differ from the trunk.  All
# three are cut from the same acting list, and they composite to exactly Clawd drawn whole.
_TRUNK = clawd(larm='none', rarm='none')
_TRUNK_CELLS = {(HX + x, HY + y) for x, y, ch in _TRUNK.sprite.cells} - {_FOOT}
_EYE_WIN = [(ex + dx, ey + dy) for ex, ey in (_TRUNK.at('eye_l'), _TRUNK.at('eye_r'))
            for dy in (-1, 0, 1) for dx in (-1, 0, 1)]                    # his 3x3-cell eye areas
_WIN_FINE = {(2 * x + i, 2 * y + j) for x, y in _EYE_WIN for i in (0, 1) for j in (0, 1)}
_HOLES = not EYES_BLACK     # should the kit ever draw see-through eyes again, the eye areas are cut
                            # out of the trunk and the face layer carries them whole


def _trunk():
    """STATIC: the kit body with the official eyes at HOME, minus the arms and the outer right foot."""
    f = Frame()
    put_clawd(f, _TRUNK)
    f.px.pop(_FOOT, None)
    if _HOLES:
        for x, y in _EYE_WIN:
            f.put(x, y, ERASE)
    return f


_TRUNK_FINE = fine(_trunk())


# ---------------------------------------------------------------- Clawd: fine-line eyes
_GAZE = {'c': (0, 0), 'l': (-1, 0), 'r': (1, 0), 'u': (0, -1), 'd': (0, 1), 'ul': (-1, -1), 'ur': (1, -1)}
_CLOSED = ('content', 'happy')          # closed-eye arcs sit centered on the eye cell, whatever the gaze


def _eyes(ff, pose, look, gaze):
    """Both eyes on a fine frame: the kit's fine_face(look), moved by a half-step gaze (one fine pixel),
    so a blink or the sparkle keeps looking where he looks.  Gaze 'c' is fine_face itself; 'l' 'r' 'u'
    'd' + 'open' equal the kit's fine look_l / look_r / look_u / look_d.  The pixels come from
    fine_face, so the kit's eye colour (black ink, STYLE.md 0) is used as is."""
    gx, gy = (0, 0) if look in _CLOSED else _GAZE[gaze]
    if (gx, gy) == (0, 0):
        return fine_face(ff, pose, expr=look)
    src = fine_face(ff.copy(), pose, expr=look)
    for key in ('eye_l', 'eye_r'):
        fx, fy = [2 * v for v in pose.at(key)]
        win = [(fx + dx, fy + dy) for dy in range(-2, 4) for dx in range(-2, 4)]   # his 3x3-cell eye area
        moved = {(x + gx, y + gy): src.px.get((x, y)) for x, y in win if src.px.get((x, y)) != '#'}
        for x, y in win:
            ff.put(x, y, '#')
        for (x, y), ch in moved.items():
            ff.put(x, y, ERASE if ch is None else ch)
    return ff


def _clawd(look, gaze, arms='side', tap=False):
    """(limbs, face) for one beat.  Clawd is drawn whole the normal way (put_clawd, the kit's official
    eyes), then fine() + the fine eyes; the limbs frame keeps only his cells that are not in the static
    trunk (the arms, the outer right foot), the FINE face frame only the half-size eye pixels that
    differ from the trunk, so the official open eyes cost nothing and the composite is exactly Clawd
    drawn whole."""
    p = _pose(arms, tap)
    f = Frame()
    put_clawd(f, p)
    ff = _eyes(fine(f), p, look, gaze)
    limbs = f.copy()
    limbs.px = {k: v for k, v in f.px.items() if k not in _TRUNK_CELLS}
    face = Frame(res=2)
    face.px = {k: v for k, v in ff.px.items() if k in _WIN_FINE and (_HOLES or _TRUNK_FINE.px.get(k) != v)}
    face.meta = {'fine_face': [(look, gaze)]}
    return limbs, face


# ---------------------------------------------------------------- the acting: (ms, look, gaze, arms)
# tap=True rows are written with arms 'tap' (arms at the side, outer right foot lifted).
_ACT = [
    (2700, 'open', 'c', 'side'),          # frame 0: the reduced-motion still (official open eyes)
    (70, 'half', 'c', 'side'),            # smooth blink
    (110, 'line', 'c', 'side'),
    (70, 'half', 'c', 'side'),
    (1370, 'open', 'c', 'side'),
    (1250, 'open', 'u', 'side'),          # half-step glance up toward the chat
    (1900, 'open', 'c', 'side'),
    (100, 'half', 'c', 'side'),           # settles in: a slow, contented blink, the lids lead ..
    (300, 'line', 'c', 'down'),           # .. the arms relax under the closed lids ..
    (100, 'half', 'c', 'down'),
    (250, 'open', 'c', 'down'),           # .. eyes open ..
    (1980, 'open', 'c', 'side'),          # .. arms back
    (300, 'open', 'd', 'side'),           # half-step glance down at the input box (the eyes lead) ..
    (160, 'open', 'd', 'tap'),            # .. tap,
    (220, 'open', 'd', 'side'),
    (160, 'open', 'd', 'tap'),            # .. tap (unhurried)
    (340, 'open', 'd', 'side'),
    (1210, 'open', 'c', 'side'),          # 11.38: eyes back to you (the firefly is coming in at 12.44)
    (140, 'open', 'l', 'side'),           # 12.59  a flicker at the edge of his eye: a glance ..
    (70, 'half', 'l', 'side'),            # 12.73  .. double blink "huh?" (two distinct blinks) ..
    (140, 'line', 'l', 'side'),
    (60, 'half', 'l', 'side'),
    (110, 'open', 'l', 'side'),           # 13.00  (open as it peaks)
    (60, 'half', 'l', 'side'),
    (140, 'line', 'l', 'side'),
    (80, 'half', 'ul', 'side'),           # 13.31  .. under the lids his eyes find it, up-left ..
    (920, 'open', 'ul', 'side'),          # 13.39  .. and he stares (it goes dark and hovers at 13.54)
    (220, 'open', 'u', 'side'),           # 14.31  it peaked above him (14.24): a beat later his eyes catch up
    (1020, 'sparkle', 'u', 'side'),       # 14.53  it comes in to land: its glow sparkles in his eyes
    (70, 'half', 'u', 'side'),            # 15.55  the glow swells on his head ..
    (750, 'content', 'u', 'side'),        # 15.62  .. content (u u), basking in it
    (70, 'half', 'u', 'side'),            # 16.37  it dimmed (16.25): a beat later he opens his eyes ..
    (310, 'open', 'u', 'side'),           # 16.44  .. hm?
    (460, 'sparkle', 'u', 'side'),        # 16.75  it glows again .. and lifts off (16.97)
    (660, 'sparkle', 'ur', 'side'),       # 17.21  his sparkling eyes follow it up and to the right
    (1010, 'open', 'ur', 'side'),         # 17.87  its light goes down, so does the sparkle; it hovers
                                          #        dark (18.01) and glows back where he is looking
    (70, 'open', 'ur', 'up'),             # 18.88  his hand comes up (in-between) ..
    (170, 'open', 'ur', 'raise'),         # 18.95  .. raised: bye! ..
    (80, 'half', 'ur', 'raise'),          # 19.12  .. it pulsed back once (19.03); a beat later ..
    (400, 'happy', 'ur', 'raise'),        # 19.20  .. he smiles (^ ^) as it drifts away
    (70, 'happy', 'ur', 'up'),            # 19.60  the hand comes down the way it went up ..
    (100, 'happy', 'ur', 'side'),         # 19.67  .. down, still smiling ..
    (70, 'half', 'ur', 'side'),           # 19.77  .. eyes open as it vanishes ..
    (700, 'open', 'ur', 'side'),          # 19.84  .. he watches the top corner where it went ..
    (70, 'half', 'ur', 'side'),           # 20.54  .. blinks ..
    (110, 'line', 'ur', 'side'),
    (70, 'half', 'c', 'side'),            #        .. (the eyes come back under the lids) ..
    (650, 'open', 'c', 'side'),           # 20.79  .. and waits for you again (flows into frame 0's hold)
]

# ---------------------------------------------------------------- firefly (local sprites; none in the library)
_FF = {
    'off':  Sprite(['G'], anchor=(0, 0), name='firefly_off'),      # light off: just the little bug
    'low':  Sprite(['g'], anchor=(0, 0), name='firefly_low'),
    'lit':  Sprite(['.g.', 'gag', '.g.'], anchor=(1, 1), name='firefly_lit'),
    'peak': Sprite(['.g.', 'gYg', '.g.'], anchor=(1, 1), name='firefly_peak'),
    # hovering right above his head: its light already catches the top of his head
    'near': Sprite(['.g.', 'gag', '.g.', '.%.'], anchor=(1, 1), name='firefly_near'),
    # resting on his head, glow spread flat; it lights the top of his head (body_light '%' = STYLE's
    # "deliberate lighting effect").  At the peak the halo rises and the light spreads to 3 cells.
    'sit':      Sprite(['gag', '.%.'], anchor=(1, 0), name='firefly_sit'),
    'sit_peak': Sprite(['.g.', 'gYg', '%%%'], anchor=(1, 1), name='firefly_sit_peak'),
}

# The flight: (x, y, glow, ms).  Before 12.44 s and after 19.84 s the firefly layer is one empty frame.
_DARK_BEFORE, _DARK_AFTER = 12440, 1600
_FLIGHT = [
    # drifts in from the left edge with a lazy bob
    (0, 8, 'off', 150), (1, 8, 'low', 140), (2, 7, 'lit', 140), (3, 7, 'lit', 130), (4, 7, 'peak', 110),
    (5, 8, 'lit', 140), (6, 8, 'lit', 140), (7, 8, 'low', 150),
    (8, 7, 'off', 260),                   # goes dark and hovers
    (8, 7, 'low', 160), (9, 7, 'lit', 140), (10, 6, 'lit', 140), (11, 6, 'peak', 140), (12, 6, 'lit', 150),
    # comes in to land, slowing down (ease-in)
    (13, 7, 'lit', 160), (14, 8, 'lit', 180), (15, 9, 'lit', 210), (15, 10, 'near', 260),
    # rests on his head and glows .. dims .. glows again
    (15, 11, 'sit', 280), (15, 11, 'sit_peak', 380), (15, 11, 'sit', 250), (15, 11, 'low', 500),
    (15, 11, 'sit', 220),
    # lifts off (ease-out), up and to the right
    (16, 10, 'near', 240), (17, 9, 'lit', 200), (18, 8, 'peak', 170), (19, 8, 'lit', 150), (20, 7, 'lit', 140),
    (21, 7, 'low', 140),
    (22, 7, 'off', 240),                  # dark again, hovering ..
    (22, 8, 'low', 180), (23, 8, 'lit', 160), (24, 8, 'lit', 150), (25, 7, 'lit', 140),   # .. glows back
    (26, 7, 'lit', 150),                  # bye! ..
    (27, 6, 'peak', 170),                 # .. it pulses back once
    (28, 6, 'lit', 160), (29, 5, 'lit', 150), (30, 5, 'low', 160),   # fading as it leaves at the top right
    (31, 4, 'off', 170),
]


def _ff_frame(x, y, glow):
    f = Frame()
    f.place(_FF[glow], x, y)
    return f


def _starts(durations):
    out, t = [], 0
    for ms in durations:
        out.append(t)
        t += ms
    return out, t


def build():
    limbs, face = [], []
    for ms, look, gaze, arms in _ACT:
        lb, fc = _clawd(look, gaze, 'side' if arms == 'tap' else arms, tap=arms == 'tap')
        limbs.append((lb, ms))
        face.append((fc, ms))
    ff = ([(Frame(), _DARK_BEFORE)] + [(_ff_frame(x, y, g), ms) for x, y, g, ms in _FLIGHT]
          + [(Frame(), _DARK_AFTER)])
    # one clock: both tracks are one loop long, and no two changes land 1-39 ms apart (no slivers)
    t_act, n_act = _starts([ms for ms, _, _, _ in _ACT])
    t_ff, n_ff = _starts([ms for _, ms in ff])
    assert n_act == n_ff == LOOP, (n_act, n_ff)
    ts = sorted(set(t_act) | set(t_ff))
    assert all(b - a >= 40 for a, b in zip(ts, ts[1:])), 'sliver between body/face and firefly changes'
    return anim(NAME, DESC, [layer('trunk', [(_trunk(), LOOP)]), layer('limbs', limbs), layer('face', face),
                             layer('firefly', ff)], state=STATE)
