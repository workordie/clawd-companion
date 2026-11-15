"""idle-pet - Idle variant: Clawd and his pet kitten.

STORYBOARD (s)   one loop = 20.00 s, ~40 % of it in still moments of 0.5 s or more.  Every layer is
                 built from ONE list of absolute-time events, so the kitten, its tail, Clawd and the effects
                 never drift apart, and independent actions are offset (nothing changes on the same frame by
                 accident).
   0.00  HOLD (frame 0 = the reduced-motion still): Clawd at HOME, eyes on you.  His little gray kitten
         sits beside him facing you (red collar, gold bell, white socks, tail curled in a hook); its ball
         of yarn (two wrap strands, lit from the top left) lies on the left, the loose end on the floor.
   1.60  it washes a paw, in a cat's rhythm: the white paw rises to its mouth .. Clawd blinks (1.78) ..
         lick (1.84: the paw stays put, the head dips onto it) .. up .. lick (2.10; the tail tip lifts as
         the overlap) .. the paw goes up over its ear (2.24) and strokes down over its eye (2.40); he
         glances down at it (2.62) .. paw down (2.70); the tail tip settles (2.88).
   2.88  HOLD 1.4 s: it sits, he watches it.
   4.26  it gets up: the tail rises first (anticipation) .. one stride toward him (4.41) .. it stands at
         his side (4.54) .. presses its head into his leg, ears back (4.71; he blinks at the bump, 4.90) ..
         its cheek slides up under his arm, which lifts out of the way (5.25); the bell jingles.
   5.85  it turns toward you as it sits back down (a 3/4 in-between, 5.85) .. sits (5.98), the tail a
         beat later (6.17) .. his raised arm reaches up and over (6.10) .. hovers (6.25; its eyes close) ..
         the PAT (6.35): his hand comes down on its head, which dips under it, one ear pressed flat ..
         a small heart pops from its head (6.49) .. the hand lifts and the head springs back up (6.77),
         the tail relaxes .. and the kitten pushes up into his hand for more (6.93) .. the hand goes back
         to his side (7.43 / 7.55) .. it keeps its eyes shut a beat, then gazes up at him (7.79); a lazy
         tail flick (7.90).  The heart floats up with a sway at slowing spacing, shrinks around its
         center (7.69) and fades (8.15-8.30).
   8.43  HOLD 0.9 s: they look at each other.
   9.30  the cat "I love you": its slow blink (560 ms) .. a pause .. and he slow-blinks back (10.16).
  10.66  a slow, contented tail swish (tip up, curl, down: 10.66-11.16); it settles as the kitten lies down.
  11.60  it lies down (front first) and curls up, head up (11.96); he blinks (12.10); its eyes droop
         (12.40) .. its head sinks onto its paws (12.90): asleep, its tail wrapped round, tip by its face.
  12.90  the nap (4.9 s), deep slow breaths eased by a half step (rest 1.5 s, in, full 1.5 s, out, rest):
         he watches it .. glances over at its ball of yarn (13.25-13.95) and back to it .. one small z
         drifts up from it (14.80) and his eyes follow it (15.06); its ear twitches in a dream (15.30);
         he blinks (15.72); the z fades (16.48-16.66) ..
  16.80  .. he glances at you: it's asleep.  HOLD 1.0 s.
  17.80  it wakes: head up, eyes still shut; he looks at it (17.95) .. eyes open (18.06) and it blinks
         itself awake (a double blink, 18.20 / 18.44) .. pushes up (18.70) .. sits, tail low (19.02) ..
         he blinks (19.14) and looks back at you (19.27) .. the tail curls into its hook (19.40).
  19.40  HOLD -> loop (0.6 s + the 1.6 s opening hold = a calm 2.2 s hold across the seam).
Clawd's eye closures: 1.78, 4.90, 10.16 (slow, 420 ms), 12.10, 15.72, 19.14 s
-> gaps 3.1 / 5.3 / 1.9 / 3.6 / 3.4 / 2.6 s.  Glance directions: you, down-right (the kitten), right
(the z / the kitten under his raised arm), down-left (the yarn).

Clawd: kit poses only (dot eyes, never resized, feet on row 19, always at HOME).  The pat adds two
hand-made right arms in the kit's style (1-cell stubs): the hand hovering over the kitten's head, and
the hand pressed down on it.  His black eyes never touch his silhouette edge (an ink cell there would
vanish on the dark theme): look_dr only with the right arm at its side; look_r while that arm is up /
out / reaching (its shoulder cell (20,14) closes the edge); look_dl with the left arm at its side.
Kitten (local sprites): gray 'm' with a gray 'N' contour on its right/bottom (mid-tones read on both
themes), pink ears + nose, ink eyes, white socks, red collar + gold bell.  Front view while it sits,
washes, gets patted and naps; side view while it walks to him and rubs his leg; a 3/4 view as it turns
back to you (the tail lags each turn).
Layers (back to front): scene (yarn, static) | tail | kitten | kitten_ov (1-3-cell overlays: blinks,
drowsy lids, breaths, an ear twitch, the washing paw's stroke) | body (Clawd) | eyes (Clawd's black
eyes, the kit's own eye cells for each pose) | fx (library heart_pop / heart / z_small).  All layers
come from the same beats (identical timing).  The tail, the kitten's small changes and Clawd's eyes
have their own layers, so a swish, a blink or a glance costs a few cells instead of a whole frame.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'idle-pet'
STATE = 'Idle variant: Clawd and his pet kitten'
DESC = ('Waits at home beside his gray kitten: it washes a paw, walks over to rub against his leg and gets '
        'a head pat (a heart floats up), trades a slow blink with him, then curls up for a nap while he '
        'keeps watch, and wakes again.')

# ============================================================================================
# The kitten (local sprites).  Gray fur 'm', gray contour/shade 'N' on its right and bottom,
# pink inner ears + nose, ink eyes 'k' (shut = 'N'), white socks 'w', red collar + gold bell.
# Each sprite is placed with its bottom-left cell on (x, GROUND).
# ============================================================================================
_KB = {
    # ---- front view
    'sit': [
        'm...m',
        'mp.pm',
        'mkmkm',
        'mmpmN',
        '.rjr.',             # red collar, gold bell
        'mwmwN',             # white socks
    ],
    'look': [            # sitting up tall, gazing up at him (the head one row higher, same columns)
        'm...m',
        'mp.pm',
        'mkmkm',
        'mmpmN',
        '.rjr.',
        'mmmmN',
        'mwmwN',
    ],
    # the paw wash: the white paw comes up to its mouth (light-gray forearm), the head dips onto the
    # paw while the paw stays put (that relative move is what reads as licking), then the paw goes up
    # over its ear and strokes down over its eye (those two are 2-3-cell overlays on 'wash_up', see
    # _EAR / _WIPE).  Eyes shut throughout.
    'wash_up': [
        'm...m',
        'mp.pm',
        'mNmNm',
        'mwpmN',             # the paw by its mouth
        'mMjr.',
        'mmmwN',             # (that sock is off the floor now)
    ],
    'wash_lick': [
        '.....',
        'm...m',
        'mp.pm',
        'mwmNm',             # same paw cell: the face comes down onto it
        'mMpmN',
        'mmmwN',
    ],
    'patted': [          # his hand on its head: the head dips a row, the ear under the hand presses flat,
        '....m',         # the other stays up; eyes squeezed shut; the collar is tucked under its chin
        'mm.pm',
        'mNmNm',
        'mmpmN',
        'mwmwN',
    ],
    'prop': [            # half lying: front up, hind end folded under (lying down / getting up)
        'm...m....',
        'mp.pm....',
        'mkmkm....',
        'mmpmNmmm.',
        '.rjrmmmmN',
        'mwmwNNNN.',
    ],
    'curl': [            # lying, head up; the tail wraps round its haunch, the tip curled up by its face
        'm...m....',
        'mp.pm.mm.',
        'mkmkmNmmm',
        'mmpmmmNNN',
        'mwmwmmmmN',
    ],
    'sleep': [           # asleep: the head sinks onto its paws, eyes shut, the tail tip by its face
        'm...m.mm.',
        'mp.pmNmmm',
        'mNmNmmNNN',
        'mmpmmmmmN',
    ],
    # ---- 3/4 view: turning back toward you as it sits down (front head, hindquarters still angled)
    'turn': [
        'm...m..',
        'mp.pm..',
        'mkmkm..',
        'mmpmNm.',
        '.rjrmmN',
        '.mwmNmN',
    ],
    # ---- side view, facing left (toward Clawd)
    'step': [            # mid-stride: front legs and hind legs spread
        '.m.N....',
        'mmmm....',
        'mkmmN...',
        'pmrmmmN.',
        '.mjmmmN.',
        'm..N.m.N',
    ],
    'stand': [
        '.m.N....',
        'mmmm....',
        'mkmmN...',
        'pmrmmmN.',
        '.mjmmmN.',
        '.m.N.mN.',
    ],
    'nuz_lo': [          # pressing its head into his leg: ears back, eyes shut
        '..mN....',
        'mmmm....',
        'mkmmN...',
        'pmrmmmN.',
        '.mjmmmN.',
        '.m.N.mN.',
    ],
    'nuz_hi': [          # .. then the cheek slides up along his side, under his arm (the bell jingles)
        '.m.N....',
        'mmmm....',
        'mkmmN...',
        'pmrmN...',
        '.mYmmmN.',
        '.mmmmmN.',
        '.m.N.mN.',
    ],
}
# Tails ('N'), as offsets from (x, GROUND), x = the kitten's left column.  Drawn in their own layer,
# behind the kitten.  (Lying down, the tail is part of the 'prop' / 'curl' / 'sleep' sprites.)
_KT = {
    'hook':  [(5, 0), (6, 0), (7, -1), (7, -2), (6, -3)],           # curled up beside it (rest)
    'hook2': [(5, 0), (6, 0), (7, -1), (7, -2), (7, -3), (6, -4)],  # .. the tip lifts (a slow swish)
    'low':   [(5, 0), (6, 0), (7, 0), (8, -1)],                     # lying along the floor, content
    'low2':  [(5, 0), (6, 0), (7, -1), (8, -2)],                    # .. a lazy flick of the tip
    'low3':  [(5, 0), (6, 0), (7, -1), (7, -2), (8, -3)],           # .. the tip swept up and curled
    'rise':  [(5, 0), (6, -1), (6, -2), (6, -3), (7, -4)],          # rising: it is about to get up
    'up':    [(7, -3), (7, -4), (7, -5), (6, -6)],                  # standing (side view): up, tip forward
    'up2':   [(7, -3), (7, -4), (7, -5), (8, -6)],                  # .. the tip quivers
}


def _kitten_sprite(body, eyes='open'):
    rows = _KB[body]
    if eyes != 'open':
        rows = [r.replace('k', 'N') for r in rows]
    return Sprite(rows, anchor=(0, len(rows) - 1), name='kitten_' + body)


# ============================================================================================
# Clawd: kit poses; the pat adds two hand-made right arms (1-cell stubs like the kit's arms)
# ============================================================================================
_ARMS = {   # right-arm cells relative to (arm column, resting-arm top row), like clawdlib.ARMS
    'pat_hover': [(0, 0), (1, 0), (2, -1)],     # the hand lifted just over the kitten's head
    'pat_press': [(0, 0), (1, 0), (2, 1)],      # .. and pressed down on it (the head dips under it)
}


# Black eyes (STYLE.md section 0) are plain ink cells, so they can live in their own layer: a glance or
# blink then costs two cells instead of a whole body frame.  (If the kit ever went back to see-through
# holes, which an upper layer cannot punch, the eyes simply stay in the body layer.)
_SPLIT_EYES = EYES_BLACK


def _pose(eyes='open', rarm='side'):
    if rarm in _ARMS:
        p = clawd(eyes=eyes, rarm='none')
        g = GEOM['normal']
        cells = list(p.sprite.cells) + [(g['ax'][1] + dx, g['ay'] + dy, '#') for dx, dy in _ARMS[rarm]]
        return Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec, rarm=rarm))
    return clawd(eyes=eyes, rarm=rarm)


# ============================================================================================
# Scenery: the kitten's ball of yarn: flat red, a pink highlight at the top left, two dark wrap strands
# curving round it and a dark rim at the bottom right; the loose end leaves the bottom right and lies
# on the floor with one soft hump (it stops just short of his foot).
# ============================================================================================
_YARN = Sprite([
    '.rrrr.....',
    'rprRrr....',
    'rrRrRr....',
    'rrRrRR.r..',
    '.rRRR.r.r.',
], anchor=(0, 4), name='yarn')
_YARN_AT = (1, GROUND)

# ============================================================================================
# Effects (library): heart_pop's tiny heart, then the small heart floats up and shrinks; one small
# sleep z drifts up from the napping kitten.  A one-cell dot is each one's last breath.
# ============================================================================================
_FX = {
    'heart_s': get('heart_pop').sprite(0),      # tiny pink heart (3x3, anchor = its center)
    'heart': get('heart').sprite(0),            # small red heart (5x5, anchor = its center)
    'z': get('z_small').sprite(0),
    'dot_p': Sprite(['p'], anchor=(0, 0), name='heart_dot'),
    'dot_l': Sprite(['l'], anchor=(0, 0), name='z_dot'),
}

# ============================================================================================
# Overlays (drawn over the kitten: far cheaper than whole kitten frames)
# ============================================================================================
S = 22                                                     # the kitten's spot (its left column)
_LIDS = ((S + 1, GROUND - 3, 'N'), (S + 3, GROUND - 3, 'N'))      # sitting: a blink
_LOOK_LIDS = ((S + 1, GROUND - 4, 'N'), (S + 3, GROUND - 4, 'N'))  # sitting up tall: the slow blink
_NAP = ((S + 1, GROUND - 2, 'N'), (S + 3, GROUND - 2, 'N'))       # lying, head up: drowsy lids
_IN = ((S + 6, GROUND - 4, 'm'),)                                   # asleep: the back half-risen ..
_FULL = ((S + 6, GROUND - 4, 'm'), (S + 7, GROUND - 4, 'm'))       # .. and at the top of a breath
_TWITCH = ((S + 4, GROUND - 4, 'N'),)                               # asleep: an ear flicks (dreaming)
_EAR = ((S + 1, GROUND - 4, 'w'), (S + 1, GROUND - 3, 'M'),
        (S + 1, GROUND - 2, 'M'))                                   # washing: the paw up over its ear ..
_WIPE = ((S + 1, GROUND - 3, 'w'), (S + 1, GROUND - 2, 'M'))       # .. stroking down over its eye

# ============================================================================================
# The timeline: absolute times (ms).  Each event sets some of: k (kitten body, x, eyes), tail
# (name, x), ov (overlay cells), eyes / arm (Clawd), fx (list of (fx, x, y)).
# ============================================================================================
TOTAL = 20000
_PAT_T = 6350                # his hand lands on its head (the heart pops 140 ms later)
_Z_T = 14800                 # the z leaves the sleeping kitten
_SIT = ('sit', S, 'open')


def _events():
    E = []

    def ev(t, **kw):
        E.append((t, kw))

    # A  frame 0: the still
    ev(0, k=_SIT, tail=('hook', S), ov=(), eyes='open', arm='side', fx=())
    # B  it washes a paw: up 240, lick 140, up 120, lick 140 (the tail tip lifts), over the ear 160,
    #    down over the eye 300, paw down.  He blinks, then glances down at it.
    ev(1600, k=('wash_up', S, 'shut'))
    ev(1780, eyes='blink')
    ev(1840, k=('wash_lick', S, 'shut'))
    ev(1900, eyes='open')
    ev(1980, k=('wash_up', S, 'shut'))
    ev(2100, k=('wash_lick', S, 'shut'), tail=('hook2', S))
    ev(2240, k=('wash_up', S, 'shut'), ov=_EAR)
    ev(2400, ov=_WIPE)
    ev(2620, eyes='look_dr')
    ev(2700, k=_SIT, ov=())
    ev(2880, tail=('hook', S))
    # C  HOLD: it sits, he watches it
    # D  it gets up (the tail leads), one stride to his side, presses its head into his leg ..
    ev(4260, tail=('rise', S))
    ev(4410, k=('step', S - 1, 'open'), tail=('up', S - 1))
    ev(4540, k=('stand', S - 2, 'open'), tail=('up', S - 2))
    ev(4710, k=('nuz_lo', S - 2, 'shut'), tail=('up2', S - 2))
    ev(4900, eyes='blink')                                  # he blinks at the bump
    ev(5030, eyes='look_dr')
    # .. and its cheek slides up under his arm, which lifts out of its way (the bell jingles)
    ev(5250, k=('nuz_hi', S - 2, 'shut'), tail=('up', S - 2), arm='up', eyes='look_r')
    # E  it turns back toward you as it sits down (3/4, then front; the tail a beat later); his raised
    #    arm reaches up and over and pats its head; it pushes up into his hand for more
    ev(5850, k=('turn', S - 1, 'open'), tail=('rise', S - 1))
    ev(5980, k=_SIT, tail=('rise', S))
    ev(6100, arm='wave')
    ev(6170, tail=('hook2', S))
    ev(6250, arm='pat_hover', ov=_LIDS)                     # (its eyes close as the hand comes)
    ev(_PAT_T, arm='pat_press', k=('patted', S, 'shut'), ov=())   # contact: the head dips under the hand
    ev(6770, arm='pat_hover', k=_SIT, ov=_LIDS)             # the hand lifts, the head springs back up ..
    ev(6860, tail=('low', S))                               # (the tail relaxes)
    ev(6930, k=('look', S, 'open'), ov=_LOOK_LIDS)          # .. and pushes up into the hand: more please
    ev(7430, arm='out')
    ev(7550, arm='side', eyes='look_dr')
    # F  it opens its eyes and gazes up at him; a lazy flick of the tail .. HOLD .. the slow-blink
    #    exchange (the cat "I love you") .. a slow, contented swish of the tail
    ev(7790, ov=())
    ev(7900, tail=('low2', S))
    ev(8430, tail=('low', S))
    ev(9300, ov=_LOOK_LIDS)                                 # its slow blink ..
    ev(9860, ov=())
    ev(10160, eyes='blink')                                 # .. a pause .. and he blinks back, slowly
    ev(10580, eyes='look_dr')
    ev(10660, tail=('low2', S))
    ev(10900, tail=('low3', S))
    ev(11160, tail=('low2', S))                             # (it settles as the kitten lies down)
    # G  it lies down (front first) and curls up; he blinks; drowsy; asleep
    ev(11600, k=('prop', S, 'open'), tail=None)
    ev(11960, k=('curl', S, 'open'))
    ev(12100, eyes='blink')
    ev(12230, eyes='look_dr')
    ev(12400, ov=_NAP)
    ev(12900, k=('sleep', S, 'shut'), ov=())
    # H  the nap (4.9 s): deep, slow, eased breaths (rest 1.5 s, in, full 1.5 s, out ..); he glances at
    #    its ball of yarn and back; one z drifts up and his eyes follow it; its ear twitches in a dream;
    #    he glances at you: it's asleep
    ev(13250, eyes='look_dl')                               # (its toy, left out on the floor)
    ev(13950, eyes='look_dr')
    for t0, ov in ((14400, _IN), (14600, _FULL), (16100, _IN), (16300, ())):
        ev(t0, ov=ov)
    ev(15060, eyes='look_r')                                # his eyes follow the z ..
    ev(15300, ov=_FULL + _TWITCH)                           # (its ear twitches in a dream)
    ev(15420, ov=_FULL)
    ev(15720, eyes='blink')
    ev(15850, eyes='look_r')
    ev(16800, eyes='open')                                  # .. then a glance at you: it's asleep
    # I  it wakes (head up, eyes still shut), opens its eyes and blinks itself awake (a double blink),
    #    pushes up and sits; he looks at it, blinks, looks back at you; its tail curls into the hook
    ev(17800, k=('curl', S, 'open'), ov=_NAP)               # head up, eyes still shut ..
    ev(17950, eyes='look_dr')
    ev(18060, ov=())                                        # .. open
    ev(18200, ov=_NAP)                                      # blink ..
    ev(18300, ov=())
    ev(18440, ov=_NAP)                                      # .. blink
    ev(18540, ov=())
    ev(18700, k=('prop', S, 'open'))
    ev(19020, k=_SIT, tail=('low', S))
    ev(19140, eyes='blink')
    ev(19270, eyes='open')                                  # he looks back at you
    ev(19400, tail=('hook', S))
    return E


def _heart_events(t):
    """The heart pops 140 ms after the pat lands: tiny, then the small heart (both centered on the same
    column, so it blooms up from the kitten's head), floats up with a sway at slowing spacing, shrinks
    around its own center and fades to a dot."""
    return [
        (t, [('heart_s', 25, 11)]),             # 100
        (t + 100, [('heart', 25, 10)]),         # 400
        (t + 500, [('heart', 25, 9)]),          # 340
        (t + 840, [('heart', 26, 8)]),          # 360 sway right
        (t + 1200, [('heart_s', 26, 8)]),       # 460 shrinks (same center)
        (t + 1660, [('dot_p', 25, 6)]),         # 150 a last pink dot, up and back left
        (t + 1810, []),
    ]


def _z_events(t):
    """One small z leaves the kitten's head and drifts up and right, slowing down; it fades to a dot."""
    return [
        (t, [('z', 26, 13)]),                   # 360
        (t + 360, [('z', 27, 12)]),             # 400
        (t + 760, [('z', 27, 11)]),             # 440
        (t + 1200, [('z', 28, 10)]),            # 480
        (t + 1680, [('dot_l', 29, 7)]),         # 180
        (t + 1860, []),
    ]


def _timeline():
    E = _events()
    E += [(t, {'fx': items}) for t, items in _heart_events(_PAT_T + 140)]
    E += [(t, {'fx': items}) for t, items in _z_events(_Z_T)]
    E.sort(key=lambda e: e[0])
    st = {}
    beats = []
    times = sorted({t for t, _ in E})
    for i, t in enumerate(times):
        for tt, kw in E:
            if tt == t:
                st.update(kw)
        end = times[i + 1] if i + 1 < len(times) else TOTAL
        assert end - t >= 60, 'beat at %d ms lasts only %d ms: offset the events' % (t, end - t)
        beats.append((end - t, dict(st)))
    assert sum(ms for ms, _ in beats) == TOTAL
    return beats


# ============================================================================================
# Frames
# ============================================================================================
def _tail_frame(s):
    f = Frame()
    if s['tail']:
        name, x = s['tail']
        for dx, dy in _KT[name]:
            f.put(x + dx, GROUND + dy, 'N')
    return f


def _kitten_frame(s):
    f = Frame()
    body, x, eyes = s['k']
    f.place(_kitten_sprite(body, eyes), x, GROUND)
    return f


def _overlay_frame(s):
    f = Frame()
    for x, y, ch in s['ov']:
        f.put(x, y, ch)
    return f


def _body_frame(s):
    f = Frame()
    put_clawd(f, _pose(s['eyes'] if not _SPLIT_EYES else 'blink', s['arm']))
    return f


def _eyes_frame(s):
    """Clawd's eyes alone: the kit's own eye cells for this pose (black ink), drawn over his eyeless
    body in the layer below.  Same beats as the body layer, so they can never drift apart."""
    f = Frame()
    if _SPLIT_EYES:
        p = _pose(s['eyes'], s['arm'])
        x0, y0 = HOME
        for x, y, ch in p.sprite.cells:
            if ch not in '#@%':
                f.put(x0 + x, y0 + y, ch)
    return f


def _fx_frame(s):
    f = Frame()
    for name, x, y in s['fx']:
        f.place(_FX[name], x, y)
    return f


def build():
    beats = _timeline()
    scene = Frame()
    scene.place(_YARN, *_YARN_AT)
    return anim(NAME, DESC, [
        layer('scene', [(scene, TOTAL)]),
        layer('tail', [(_tail_frame(s), ms) for ms, s in beats]),
        layer('kitten', [(_kitten_frame(s), ms) for ms, s in beats]),
        layer('kitten_ov', [(_overlay_frame(s), ms) for ms, s in beats]),
        layer('body', [(_body_frame(s), ms) for ms, s in beats]),
        layer('eyes', [(_eyes_frame(s), ms) for ms, s in beats]),
        layer('fx', [(_fx_frame(s), ms) for ms, s in beats]),
    ], state=STATE)
