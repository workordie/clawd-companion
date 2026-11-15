"""auto-robot - Auto mode, variant: a little robot does the work.   Preview: python3 gen/preview.py anim auto-robot

Storyboard (master loop T = 12.0 s; every synced layer is cut from the beat lists below)
  0.0 s  Clawd lounges at HOME in an open-sided striped deck chair (legs tucked: seated): shades on, a
         lemonade with a bendy straw in his left hand, a palm leaning over him. His little gold robot types
         at its tiny laptop with two little arms (the screen's glow lights its belly), eyes on the keys; a
         progress bar above it is 3/5 full.
  1.30   Clawd sips: the glass comes up in his hand, the bendy straw swings over to his face (the edge of
         his shades), the lemonade climbs the straw step by step (slurp) and the glass goes back down.
  2.50   the robot looks up at its screen, 2.58 stops typing and swings its left arm up, 2.66 cocks its
         fist high above its head (anticipation, held) ..
  2.95   SLAM on Enter: a smear, a flash at the contact, the bar fills up, the antenna wobbles (damped) and
         dings; 3.06 the bar becomes a green check (tiny, overshoot, settle); 3.17 its eyes go ^^.
  3.61   it turns to Clawd; 3.76 thumbs-up above its head (lift, overshoot with an antenna sway, settle,
         a ting).
         ... Clawd does not move at all: the stillness is the joke.
  4.86   the thumb comes down, it waits, blinks at 5.56 (its bulb goes dark with its eyes), gives up and
         looks back at its keys.
  5.84   ting! Clawd's shades glint .. 6.25 and, way too late, a lazy wave, each swing slower than the last
         (400 / 450 / 550 ms). The robot is typing again (a new, empty bar) and glances over at 6.5.
  9.40   Clawd slides his shades down to peek at the robot's progress (eyes look up-right over the lenses);
  9.65   the robot stops typing and looks up (hm?), 9.85 turns straight to him, antenna swaying: busted.
         They stare at each other .. 10.50 Clawd's eyes dart away, 10.75 he blinks and 10.86 slides the
         shades back up. The robot blinks (10.65) and beeps happily at 10.76 (^^, a cyan note floats up
         toward him). 11.25 it is back at work; typing runs through the loop seam.
Ambient: the typing hands run on their own 1.99 s loop (bursts with short rests), shown whenever the
master "pose" layer leaves the hands free (0-2.58, 6.0-9.65, 11.25-12.0 s: 58 % of the loop); each
keystroke swings a whole little arm (silver shoulder under the head's corner, forearm, gold hand). The palm
fronds lift in the breeze on a 5.06 s loop; the antenna bulb goes dark whenever the robot blinks (1.5,
5.56, 10.65 s) and once on its own mid-typing (7.3 s).
Frame 0 (reduced motion): Clawd lounging with shades + lemonade, the robot mid-keystroke, bar 3/5.
Plain face only (open / blink / look_*), see-through eye holes, normal body size: STYLE.md section 0.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401,F403
from acc import get                          # noqa: E402

NAME = 'auto-robot'
STATE = 'Auto mode (idle in that mode), variant: a robot does the work'
DESC = ('Autopilot: Clawd lounges in a deck chair with shades and a lemonade while his little robot types for him; '
        'it slams Enter, the progress bar turns into a check, it gives him a thumbs-up and he answers way too late '
        'with a lazy wave.')

T = 12000                # master loop


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


def _sum(keys):
    return sum(k[0] for k in keys)


def _segments(events, default):
    """Absolute (start, end, value) events over a default -> [(ms, value), ...] covering [0, T)."""
    out, t = [], 0
    for a, b, v in sorted(events, key=lambda e: e[0]):
        assert a >= t, ('events overlap', a, t)
        if a > t:
            out.append((a - t, default))
        out.append((b - a, v))
        t = b
    if t < T:
        out.append((T - t, default))
    return out


def _starts(keys):
    t, out = 0, []
    for k in keys:
        out.append(t)
        t += k[0]
    return out


# =====================================================================================================
# Scenery: open-sided deck chair (behind Clawd) and a palm leaning over him
# =====================================================================================================
CHAIR_TOP = 9
_STRIPES = 'bbwwbbbwwbb'                 # x 10..20: calm 2-cell stripes, symmetric around x 15


def _chair():
    """Backrest: wood top bar + striped canvas above his head and beside it (x 10 / x 20 down to row 13).
    The sides stay open below that, so his arm stubs and every gesture read against the page; armrests at
    row 16 under his arms, legs at x 9 / x 21, the navy seat sling behind his tucked legs. Canvas cells
    hidden behind his body are not drawn (his eye holes look through to the page)."""
    f = Frame()
    f.hline(10, 20, CHAIR_TOP, 'T')
    for y in range(CHAIR_TOP + 1, 14):
        for i, ch in enumerate(_STRIPES):
            x = 10 + i
            if y >= 12 and 11 <= x <= 19:
                continue
            f.put(x, y, ch)
    f.hline(9, 10, 16, 'T')
    f.hline(20, 21, 16, 'T')
    for y in range(17, 20):
        f.put(9, y, 'T')
        f.put(21, y, 'T')
    f.hline(10, 20, 18, 'B')
    return f


# palm: blue pot (x 1-5), a trunk leaning right, crown overhanging the chair's top-left corner
_CROWN = [                                       # x 1..12, rows 2..7 (row 2 = the tips the breeze lifts)
    '...gg..ggg..',
    '..gGGggGGGg.',
    '.gG..gGg..Gg',
    'gG..gGdGg..G',
    'g...g.d..g..',
    '.........g..',
]
CROWN_X = 1
_CROWN_BREEZE = '....gg..ggg.'                   # row 2 with the frond tips lifted to the right
_TRUNK = [(7, 7, 'T'), (6, 8, 't'), (6, 9, 't'), (5, 10, 'T'), (5, 11, 't'), (4, 12, 't'), (4, 13, 'T'), (3, 14, 't'),
          (3, 15, 't'), (2, 16, 'T')]            # leaning, even 2:1 steps, a wood ring every 3rd cell; it keeps two
                                                 # clear columns from the glass and its straw (the left third breathes)


def _palm():
    f = Frame()
    for x, y, ch in _TRUNK:
        f.put(x, y, ch)
    _paint(f, _CROWN[1:], CROWN_X, 3)
    _paint(f, ['bbbbB', '.bbbB', '..BB.'], 1, 17)
    return f


def _palm_tips():
    """Ambient loop (5.06 s, never in step with the master): the frond tips lift twice, unevenly."""
    rest, breeze = Frame(), Frame()
    _paint(rest, _CROWN[:1], CROWN_X, 2)
    _paint(breeze, [_CROWN_BREEZE], CROWN_X, 2)
    return [(rest, 2600), (breeze, 420), (rest, 1700), (breeze, 340)]


# =====================================================================================================
# Clawd: static torso + limbs, shades and juice layers, all cut from ONE beat list (never out of sync)
# =====================================================================================================
_SHADES = get('sunglasses_glint')       # 0 = plain shades, 1-2 glint sweeps, 3 twinkle, 4 fade

# lemonade for the RIGHT hand (grip = left wall); worn on his left hand it mirrors, the straw leans to him
_JUICE = Item('juice', 'hand', 'tall glass of lemonade with a red straw', Sprite([
    'r...',
    '.r..',
    'mrym',
    'myym',
    'myym',
    '.mm.',
], anchor=(0, 3)))
# sipping: the glass rides one row higher in the same hand (his arm stays in view, gripping it) and the
# bendy straw swings over to his face: up, over, and its tip (x 0, beyond the wall) against his shades' edge
_SIP = Item('juice_sip', 'hand', 'the lemonade lifted in his hand, the bendy straw bent to his face', Sprite([
    '.rr..',
    'rmrym',
    '.myym',
    '.myym',
    '..mm.',
], anchor=(1, 3)))
SIP_STRAW = [(8, 12), (9, 12), (10, 13)]  # the straw above the rim while he sips, glass to face (the slurp climbs it)

# cells of his face that change: the eye spots of open (row 14), look_ur and look_ul (row 13)
_EYE_SPOTS = {(12, 14), (18, 14), (13, 13), (19, 13), (11, 13), (17, 13)}


def _pose(larm='side', rarm='side', eyes='open'):
    return clawd(eyes=eyes, larm=larm, rarm=rarm, legs='short')     # see-through eye holes (official look)


def _drawn(pose):
    f = Frame()
    put_clawd(f, pose)
    return dict(f.px)


# his left arm never leaves 'side' (the glass rides up in his grip), so it lives in the static torso layer
_TORSO_CELLS = {k: v for k, v in _drawn(_pose('side', 'none', 'blink')).items() if k not in _EYE_SPOTS}


def _shade_cells(dy):
    f = Frame()
    wear(f, _SHADES, _pose(), i=0, dy=dy)
    return set(f.px)


def _part(cells, pose, name):
    """put_clawd() of just these cells (absolute), keeping the pose's anchors and spec for the tools."""
    spr = Sprite(cells=[(x - HOME[0], y - HOME[1], ch) for (x, y), ch in cells.items()], anchor=(0, 0), name=name)
    f = Frame()
    put_clawd(f, Pose(spr, pose.anchors, dict(pose.spec, part=name)))
    return f


def _clawd_torso():
    return _part(_TORSO_CELLS, _pose('side', 'none', 'blink'), 'clawd_torso')


def _clawd_limbs(larm='side', rarm='side', eyes='open', shades=0, **_):
    """Only what differs from the torso: arms, and the eye spots that are not under the shades."""
    p = _pose(larm, rarm, eyes)
    hidden = _shade_cells(shades)
    cells = {k: v for k, v in _drawn(p).items()
             if _TORSO_CELLS.get(k) != v and not (k in _EYE_SPOTS and k in hidden)}
    return _part(cells, p, 'clawd_limbs')


def _clawd_shades(shades=0, **_):
    f = Frame()
    wear(f, _SHADES, _pose(), i=0, dy=shades)
    return f


def _clawd_juice(glass='rest', **_):
    f = Frame()
    if glass == 'sip':
        wear(f, _SIP, _pose(), side='l')                 # same grip (his left hand), glass one row up
    else:
        wear(f, _JUICE, _pose(), side='l', dy=-1 if glass == 'mid' else 0)
    return f


CLAWD_KEYS = [
    (1300, {}),                                         # frame 0: the reduced-motion still
    (90, dict(glass='mid')),                            # sip: the glass comes up in his hand ..
    (800, dict(glass='sip')),                           # .. the straw swings to his face (the fx layer adds the slurp)
    (90, dict(glass='mid')),                            # .. and back down
    (3970, {}),                                         # still as a rock through the slam and the thumbs-up
    (140, dict(rarm='up')),                             # (the shades glint just before this, fx layer)
    (400, dict(rarm='wave')),                           # the lazy wave, way too late ..
    (450, dict(rarm='raise')),
    (550, dict(rarm='wave')),                           # .. each swing slower than the last
    (200, dict(rarm='up')),
    (1410, {}),
    (90, dict(shades=1)),                               # peeks over his shades ..
    (1010, dict(shades=2, eyes='look_ur')),             # .. at the robot's progress; 9.85 it looks back: busted
    (250, dict(shades=2, eyes='look_ul')),              # 10.5: his eyes dart away ..
    (110, dict(shades=2, eyes='blink')),
    (90, dict(shades=1)),                               # .. and the shades go back up
    (1050, {}),
]
_CS = _starts(CLAWD_KEYS)
T_SIP = _CS[2]                                          # 1390
T_WAVE = _CS[5]                                         # 6250
T_LOOK_AWAY = _CS[13]                                   # 10500


def _glint_overlay(i, shift=(-1, 1)):
    """sunglasses_glint frame i as a patch over the plain shades. The twinkle is moved next to the right
    lens's corner (clear of the chair) and drawn in gold around a white core, readable on both themes."""
    a, b = Frame(), Frame()
    wear(a, _SHADES, _pose(), i=0)
    wear(b, _SHADES, _pose(), i=i)
    f = Frame()
    for (x, y), ch in b.px.items():
        if a.px.get((x, y)) != ch:
            if (x, y) in a.px or ch not in 'cW':        # glint sweeping across the lenses
                f.put(x, y, ch)
            else:                                        # twinkle pixel outside the lenses
                f.put(x + shift[0], y + shift[1], 'j' if ch == 'c' else 'W')
    for (x, y), ch in a.px.items():                     # glint pixels of frame 0 that frame i hides
        if (x, y) not in b.px:
            f.put(x, y, 'k')
    return f


# =====================================================================================================
# Robot: shell (static), eyes, antenna, typing hands (own loop), arms (master), progress bar (master)
# =====================================================================================================
RX, RY = 24, 11                  # head x 24..30, rows 11..15; screen x 25..29 rows 12..14
BULB = (27, 9)                   # antenna bulb; stalk (27, 10)
_BOX = [                         # gold head lit from the top-left, night-blue screen. Below it only its belly
    '.jjjjj.',                   # shows, lit cyan by the laptop's screen, framed by its two forearms. The
    'jiiiiiJ',                   # laptop is wider than the robot, so its lid visibly cuts across it.
    'jiiiiiJ',
    'jiiiiiJ',
    '.JJJJJ.',
    '..ccc..',
]
_LAPTOP = [                      # its tiny laptop, from behind: gray lid with a glowing logo, steel base
    'NNNNNNN',
    'NnncnnN',
    'smmmmms',
]
LAP_Y = 17
_EYES = {                        # cells on the 5x3 screen
    'down':  [(1, 2), (3, 2)],
    'fwd':   [(1, 1), (3, 1)],
    'left':  [(0, 1), (2, 1)],
    'happy': [(1, 0), (3, 0), (0, 1), (2, 1), (4, 1), (0, 2, 'p'), (4, 2, 'p')],   # ^^ + pink cheeks
    'blink': [],
}
# Its little arms are silver tubes with gold hands: they come out from under the head's bottom corners and
# reach in front of the belly to the keys (shoulder, forearm, hand). Each keystroke swings a hand up over the
# glow and down onto the lid's top edge, so the whole arm changes shape (bent <-> straight diagonal).
METAL = 'm'                      # arm tubes: silver reads against the gold head, the cyan belly and the gray lid
ARM_L = [(24, 15), (25, 16)]     # left shoulder + forearm (master pose layer: hidden while that arm is raised)
ARM_R = [(30, 15), (29, 16)]     # right shoulder + forearm (never raised: part of the static shell)
HL, HR = (26, 16), (28, 16)      # hands lifted (over the glow); pressing = one row lower, on the lid's top edge


def _robot_shell():
    f = Frame()
    f.put(BULB[0], BULB[1] + 1, 's')                    # antenna stalk
    _paint(f, _BOX, RX, RY)
    _paint(f, _LAPTOP, RX, LAP_Y)
    for x, y in ARM_R:
        f.put(x, y, METAL)
    return f


def _hands(l='down', r='down'):
    """The two hands: 'up' = lifted over the glow, 'down' = on the lid's top edge, None = not drawn."""
    f = Frame()
    for (x, y), st in ((HL, l), (HR, r)):
        if st is not None:
            f.put(x, y + (0 if st == 'up' else 1), 'j')
    return f


# typing (own loop): which hand is lifted; '-' = both resting on the keys
_TYPE = [('L', 140), ('R', 120), ('L', 170), ('R', 130), ('L', 150), ('-', 330),     # a burst of five ..
         ('R', 140), ('L', 110), ('R', 160), ('-', 540)]                             # .. three, a longer rest
TYPE_LOOP = sum(ms for _, ms in _TYPE)                  # 1990 ms, co-prime-ish with the 12 s master


def _typing_layer():
    st = {'L': ('up', 'down'), 'R': ('down', 'up'), '-': ('down', 'down')}
    return [(_hands(*st[k]), ms) for k, ms in _TYPE]


# pose layer (master): the left arm, and it covers the typing hands whenever the robot does something else
_COVER = {HL: 'c', HR: 'c', (HL[0], HL[1] + 1): 'N'}
SLAM_AT = (HL[0], HL[1] + 1)     # the left hand slams down on the lid's top edge (26, 17)


def _fist(x0, y0):
    """3x3 fist lit from the top-left: gold top-left 2x2, dark gold along the right and the bottom."""
    return [(x0 + i, y0 + j, 'J' if 2 in (i, j) else 'j') for j in range(3) for i in range(3)]


# Raised, the left arm comes out from behind the head's left edge: shoulder (23, 12), right beside the head
# (24, 12), in every raised pose. Fists are 3x3, the forearm enters at the bottom centre; the thumb (1x2)
# rises from the fist's top-left corner, toward Clawd. Everything stays a cell clear of the chair's top bar.
_M = METAL
ARM = {
    'lift':  [(23, 12, _M), (23, 11, _M), (22, 9, 'j'), (23, 9, 'j'), (22, 10, 'j'), (23, 10, 'j')],   # half way
    'wind':  [(23, 12, _M), (22, 11, _M), (22, 10, _M), (22, 9, _M)] + _fist(21, 6),           # cocked back, high
    'smear': [(22, 8, 's'), (22, 9, 's'), (22, 10, 's'), (22, 11, 's'), (23, 12, 's'), (23, 13, 's'),
              (23, 14, 's'), (24, 15, 's'), (25, 16, 's'), (26, 16, 'j')],               # whoosh, down the side
    'thumb': [(23, 12, _M), (23, 11, _M), (23, 10, _M)] + _fist(22, 7) + [(22, 6, 'j'), (22, 5, 'j')],
}
ARM['thumb_o'] = [(23, 12, _M)] + [(x, y - 1, ch) for x, y, ch in ARM['thumb']]   # overshoot: one row higher
THUMB_TIP = (22, 5)
_IMPACT = get('impact_star')


def _pose_frame(st):
    f = Frame()
    raised = st in ARM
    if not raised:
        for x, y in ARM_L:                               # left shoulder + forearm, down at the keys
            f.put(x, y, METAL)
    if st is None:
        return f                                         # hands free: the typing layer shows
    for (x, y), ch in _COVER.items():
        f.put(x, y, ch)
    f.put(HR[0], HR[1] + 1, 'j')                         # right hand rests on the keys
    if not raised:
        f.put(SLAM_AT[0], SLAM_AT[1], 'j')               # .. and so does the left one
    for x, y, ch in ARM.get(st, []):
        f.put(x, y, ch)
    if st == 'impact':                                   # contact flash (library impact_star, the small one)
        f.place(_IMPACT.sprite(0), SLAM_AT[0], SLAM_AT[1])
    return f


T_STOP = 2500                    # typing stops for the slam
T_SLAM = 2950
T_UP = 3760                      # thumbs-up starts
T_PEEKED = 9650                  # caught peeking: the robot stops typing ..
T_BACK = 11250                   # .. and goes back to work
POSE_KEYS = _segments([
    (T_STOP + 80, T_STOP + 160, 'lift'),                 # its eyes went to the screen; it swings its arm up ..
    (T_STOP + 160, T_SLAM - 60, 'wind'),                 # .. and cocks its fist high: anticipation, held
    (T_SLAM - 60, T_SLAM, 'smear'),
    (T_SLAM, T_SLAM + 80, 'impact'),                     # SLAM
    (T_SLAM + 80, T_UP, 'rest'),
    (T_UP, T_UP + 90, 'lift'),
    (T_UP + 90, T_UP + 180, 'thumb_o'),                  # overshoot ..
    (T_UP + 180, 4860, 'thumb'),                         # .. settle
    (4860, 4970, 'lift'),
    (4970, 6000, 'rest'),                                # waits for an answer, gives up
    (T_PEEKED, T_BACK, 'rest'),                          # caught by Clawd's peek: stops typing
], None)
T_THUMB = T_UP + 180

# robot eyes (absolute ms; 'down' = on the keys in between)
T_CONTACT = 9850                 # it looks straight back at the peeking Clawd (he looks away at T_LOOK_AWAY)
FACE_KEYS = _segments([
    (1500, 1610, 'blink'),
    (T_STOP, 3170, 'fwd'),                               # eyes on the screen for the big Enter
    (3170, 3610, 'happy'),                               # after the slam
    (3610, 5560, 'left'),                                # turns to Clawd, thumbs-up, waits ..
    (5560, 5670, 'blink'),                               # .. gives up
    (6500, 6990, 'left'),                                # glances at the late wave while typing
    (T_PEEKED, T_CONTACT, 'fwd'),                        # stops: hm?
    (T_CONTACT, 10650, 'left'),                          # eye contact with the peeking Clawd (0.65 s mutual)
    (10650, 10760, 'blink'),
    (10760, T_BACK, 'happy'),                            # beep!
], 'down')
T_BEEP = 10760


def _face(face):
    f = Frame()
    for cell in _EYES[face]:
        f.put(RX + 1 + cell[0], RY + 1 + cell[1], cell[2] if len(cell) > 2 else 'c')
    if face == 'blink':                                  # its bulb goes dark when it blinks (drawn over the
        f.put(BULB[0], BULB[1], 'R')                     # antenna layer; never during a sway, see build())
    return f


def _bulb(state='on', sway=0):
    f = Frame()
    bx, by = BULB[0] + sway, BULB[1]
    if state == 'flash':
        for gx, gy in ((-1, 0), (1, 0), (0, -1)):
            f.put(bx + gx, by + gy, 'y')
        f.put(bx, by, 'Y')
    else:
        f.put(bx, by, {'on': 'r', 'off': 'R'}[state])
    return f


ANTENNA_KEYS = _segments([                              # (the bulb also blinks with its eyes: face layer)
    (T_SLAM, T_SLAM + 90, ('on', -1)),                   # damped wobble after the slam ..
    (T_SLAM + 150, T_SLAM + 230, ('on', 1)),
    (T_SLAM + 230, T_SLAM + 410, ('flash', 0)),          # .. ding
    (T_UP + 90, T_UP + 190, ('on', 1)),                  # follow-through of the thumb's overshoot
    (7300, 7430, ('off', 0)),                            # on its own, in the long stretch of typing
    (T_CONTACT, T_CONTACT + 120, ('on', -1)),            # it turns to Clawd: the antenna sways toward him
], ('on', 0))

# progress bar above the robot (master): fills while it types, full on the slam, then the check pops
BAR_X, BAR_Y, BAR_N = 25, 6, 5
_CHECK = get('check_pop')
CHECK_AT = (25, 4)               # settles on x 22-29, rows 2-6 (clear of the antenna flash)


def _bar(n):
    f = Frame()
    if n is None:
        return f
    for i in range(BAR_N):
        f.put(BAR_X + i, BAR_Y, 'g' if i < n else 'N')
    return f


def _check(i):
    f = Frame()
    f.place(_CHECK.sprite(i), CHECK_AT[0], CHECK_AT[1])
    return f


BAR_KEYS = [                     # (ms, ('bar', fill) or ('check', frame) or None)
    (1300, ('bar', 3)),
    (T_SLAM - 1300, ('bar', 4)),
    (110, ('bar', 5)),                                   # the slam completes it
    (60, ('check', 0)), (80, ('check', 1)), (300, ('check', 2)),
    (6000 - T_SLAM - 550, None),                         # no task while it celebrates and waits
    (900, ('bar', 0)),                                   # back to work: a new task
    (1400, ('bar', 1)),
    (3100, ('bar', 2)),                                  # (paused while Clawd peeks)
    (T - 11400, ('bar', 3)),
]


# =====================================================================================================
# FX (master loop): slurp, ting at the thumb, shades glint, the robot's beep note
# =====================================================================================================
def _fx_layer(events):
    """events: list of (start_ms, [(Frame, ms), ...]); overlapping events are composited."""
    cuts = {0, T}
    spans = []
    for start, frames in events:
        t = start
        for fr, ms in frames:
            spans.append((t, t + ms, fr))
            cuts.update((t, t + ms))
            t += ms
        assert t <= T, ('fx overrun', t)
    cuts = sorted(cuts)
    out = []
    for a, b in zip(cuts, cuts[1:]):
        f = Frame()
        for s0, s1, fr in spans:
            if s0 <= a < s1:
                f = f.over(fr)
        out.append((f, b - a))
    return out


def _placed(spr, x, y):
    f = Frame()
    f.place(spr, x, y)
    return f


def _beep_note():
    return get('note').sprite(0).recolor({'v': 'c', 'l': 'c', 'V': 'b'})


def _slurp(n):
    """The lemonade has climbed the first n straw cells (glass -> his face)."""
    f = Frame()
    for x, y in SIP_STRAW[:n]:
        f.put(x, y, 'j')
    return f


def build():
    for nm, keys in (('clawd', CLAWD_KEYS), ('pose', POSE_KEYS), ('face', FACE_KEYS), ('antenna', ANTENNA_KEYS),
                     ('bar', BAR_KEYS)):
        assert _sum(keys) == T, (nm, _sum(keys), T)
        assert all(k[0] >= 40 for k in keys), (nm, [k for k in keys if k[0] < 40])
    assert T_LOOK_AWAY - T_CONTACT >= 500, 'the busted stare needs time to land'
    ant_starts, face_starts = _starts(ANTENNA_KEYS), _starts(FACE_KEYS)
    for (fms, fst), f0 in zip(FACE_KEYS, face_starts):
        if fst == 'blink':
            for (ams, ast), a0 in zip(ANTENNA_KEYS, ant_starts):
                assert ast == ('on', 0) or a0 + ams <= f0 or a0 >= f0 + fms, ('bulb blink during a sway', f0, ast)

    limbs_l = [(_clawd_limbs(**kw), ms) for ms, kw in CLAWD_KEYS]
    shades_l = [(_clawd_shades(**kw), ms) for ms, kw in CLAWD_KEYS]
    juice_l = [(_clawd_juice(**kw), ms) for ms, kw in CLAWD_KEYS]
    pose_l = [(_pose_frame(st), ms) for ms, st in POSE_KEYS]
    face_l = [(_face(st), ms) for ms, st in FACE_KEYS]
    ant_l = [(_bulb(*st), ms) for ms, st in ANTENNA_KEYS]
    bar_l = [((_bar(v[1]) if v[0] == 'bar' else _check(v[1])) if v else Frame(), ms) for ms, v in BAR_KEYS]

    spk, note = get('sparkle_small'), _beep_note()
    glint_ms = list(_SHADES.ms[1:5]) if isinstance(_SHADES.ms, (list, tuple)) else [60, 60, 180, 110]
    sx, sy = THUMB_TIP[0] - 2, THUMB_TIP[1] - 2
    events = [
        # slurp: the lemonade climbs the straw cell by cell and holds at his face
        (T_SIP + 120, [(_slurp(1), 110), (_slurp(2), 110), (_slurp(3), 300)]),
        (T_THUMB + 20, [(_placed(spk.sprite(k), sx, sy), ms) for k, ms in ((0, 70), (1, 100), (2, 130), (1, 110))]),
        # the library's ting (sweep, sweep, twinkle, fade) ends as his arm comes up to wave
        (T_WAVE - sum(glint_ms), [(_glint_overlay(k), ms) for k, ms in zip((1, 2, 3, 4), glint_ms)]),
        # the beep floats up, then drifts toward Clawd, clear of the chair and the bar; it fades to a dot
        (T_BEEP + 40, [(_placed(note, 23, 5), 280), (_placed(note, 22, 4), 320),
                       (_placed(spk.sprite(0).recolor({'j': 'c'}), 21, 3), 140)]),
    ]

    full = lambda nm, fr: layer(nm, [(fr, T)])
    return anim(NAME, DESC, [
        full('chair', _chair()),
        full('palm', _palm()),
        layer('palm_tips', _palm_tips()),
        full('clawd', _clawd_torso()),
        layer('limbs', limbs_l),
        layer('shades', shades_l),
        layer('juice', juice_l),
        full('robot', _robot_shell()),
        layer('antenna', ant_l),
        layer('face', face_l),
        layer('typing', _typing_layer()),
        layer('pose', pose_l),
        layer('bar', bar_l),
        layer('fx', _fx_layer(events)),
    ], state=STATE)
