"""thinking-pace - Thinking variant: pacing up and down.   Preview:  python3 gen/preview.py anim thinking-pace

STORYBOARD (ms)   one loop = 12 160 ms; calm, one small payoff (the thought arriving) per loop
  He paces to and fro around HOME, turned three-quarters toward where he walks (the traced walk in walk_left.py, its
  5-pose stride), eyes down on the floor, at a slow pondering pace (115 ms a step, easing in and out of every
  stop: 2.2 cells/s; the normal walk is 4).  The planted feet never skate: his body moves exactly as far as the
  planted foot slides back in the kit (one fine pixel on steps 2, 3, 6 and 7 of the cycle).
  Route: HOME -> 1.5 cells right -> back past HOME to 1.5 cells left -> HOME (each walk frame costs ~1 KB, so
  this keeps the SVG near 53 KB).  Every turn goes through in-betweens: turned, half-turned, facing you,
  half-turned the other way; his eyes glance where he is going first.
     0  frame 0 = the reduced-motion still: Clawd at HOME facing you, eyes up (half-step look_u) under a small
        gray "..." that ripples once: pondering.
  1600  a blink; his eyes drop to the floor and the "..." fades; he glances right, turns, and paces off.
        At the right end he stops, looks up: a faint gray glint flickers above his head and fizzles (almost!);
        a blink, a glance back over his shoulder, he turns (through facing you) and paces back past HOME.
        At the left end he stops and looks up again: nothing comes, his lids droop; he glances back, turns
        and paces home.
        At HOME he turns to face you, eyes up ... the thought arrives: a gold sparkle twinkles above his head,
        his eyes go wide, then sparkle; a little nod (eyes and claws dip); the "..." fades back in -> frame 0.
Eye closures: three smooth blinks (half, line, half) at uneven spacing (1.6, 5.1, 6.7 s) and a lid droop at the left
end (8.6 s).

Clawd is FINE (half-size pixels): the walk kit's turned body, the half-turn in-betweens drawn here in the kit's
style (a 1-cell flank, the face half-way round), and his front pose (fine() of the kit pose).  While he walks his
eyes ride in the body frame; while he stands the body frame has no eyes (so it merges across blinks and glances)
and the small 'face' layer draws them.  Eyes: open, half, line, wide, sparkle, each moved by a half-step gaze
(u / d / l / r), i.e. only the user's fine-line set.  He never changes size; frame 0 is at HOME facing front
(the home-spot check differs only on walking frames).
Layers: clawd (fine) | face (fine) | thought ("...", the faint glint, the gold sparkle).  All share LOOP.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402
from anims.walk_left import POSES, CYCLE, pose_frame, mirrored, FX0, FY0   # noqa: E402   the traced walk
from anims.hop_right import turned, LEG     # noqa: E402   its turned body, standing
GROUND_F = 2 * H - 1

NAME = 'thinking-pace'
STATE = 'thinking (variant)'
DESC = ('Paces slowly to and fro around his spot, turned toward where he walks and eyes on the floor; at each end '
        'he stops and looks up as an idea almost comes, and back home he turns to you as the thought sparkles.')

STEP = 184                                    # ms per pose of the walk's 5-pose stride (2 cells): 2.2 cells/s
EASE_IN = (264, 224, 200)                     # the first poses of a walk are slower ...
EASE_OUT = (208, 248)                         # ... and so are the last ones
D = [0, 1, 2, 3, 3]                           # fine pixels the body has moved by pose k of a stride (4 per stride)
REACH = 3                                     # how far each side of HOME he paces: 3 fine pixels = 1.5 cells


# --------------------------------------------------------------------------------------------
# eyes (fine pixels).  pose eye spots (box-relative fine x of the near and far eye, facing left), rows 4-5.
# --------------------------------------------------------------------------------------------
EYE_X = {'turned': (2, 12), 'half': (3, 14), 'front': (4, 16)}
_GZ = {'': (0, 0), 'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0)}


def _eye_cells(shape, ex):
    if shape == 'open':
        return [(ex + dx, 4 + dy, EYE_INK) for dy in (0, 1) for dx in (0, 1)]
    if shape == 'half':
        return [(ex + dx, 5, EYE_INK) for dx in (0, 1)]
    if shape == 'line':
        return [(ex + dx, 5, EYE_INK) for dx in range(-1, 3)]
    if shape == 'wide':
        return [(ex + dx, 3 + dy, EYE_INK) for dy in (0, 1, 2) for dx in (0, 1)]
    if shape == 'sparkle':
        return [(ex + dx, 4 + dy, 'W' if (dx, dy) == (0, 0) else EYE_INK) for dy in (0, 1) for dx in (0, 1)]
    raise ValueError('eye shape %r (the user allows open, half, line, wide, sparkle + glances)' % shape)


def _draw_eyes(ff, kind, expr, bob=0, mirror=False):
    """Eyes on a facing-left body (mirror=True for a front pose, whose glint and glances must not flip later)."""
    shape, _, gz = expr.partition('/')
    gx, gy = _GZ[gz]
    for ex in EYE_X[kind]:
        for x, y, c in _eye_cells(shape, ex):
            ff.put(FX0 + x + gx, FY0 - bob + y + gy, c)


# --------------------------------------------------------------------------------------------
# bodies (FINE, facing left at HOME; _place() mirrors / moves them)
# --------------------------------------------------------------------------------------------
def _legs_straight(ff, hips):
    hip = FY0 + 12
    for hx, ch in hips:
        for r in range(GROUND_F - hip + 1):
            for d in (0, 1):
                ff.put(FX0 + hx + d, hip + r, ch)


def _turned():
    ff = Frame(res=2)
    return turned(kind='turned', expr=None, legs=[LEG['stand']] * 4)


def _half():
    """Half-way round: a 1-cell flank, the face half-way to his side (the shared kit's half turn, walk style)."""
    return turned(kind='half', expr=None, legs=[LEG['stand']] * 4)


def _front(larm='side', rarm='side'):
    f = Frame()
    put_clawd(f, clawd(eyes='blink', larm=larm, rarm=rarm))
    return fine(f)


def _place(ff, facing, dxf, kind='turned'):
    """facing 'left' / 'right' / 'front'; moved dxf fine pixels from HOME."""
    out = mirrored(ff) if facing == 'right' else ff
    out = out.shifted(dxf, 0)
    out.meta = {'clawd': [(HOME[0] + dxf // 2, HOME[1], dict(body=kind))]}
    return out


def walk(facing, k, dxf, expr='open/d'):
    """Pose k (0-4) of the traced walk turned toward `facing`, dxf fine pixels from HOME; his eyes ride along."""
    bob = POSES[CYCLE[k]]['bob']
    ff = pose_frame(CYCLE[k], eyes=None)
    _draw_eyes(ff, 'turned', expr, bob)
    return _place(ff, facing, dxf, 'walk')


def eyes(kind, facing, dxf, expr):
    """The face layer: only his eyes for a standing pose (kind turned / half / front)."""
    ff = Frame(res=2)
    if facing == 'front':
        _draw_eyes(ff, 'front', expr)
        out = ff.shifted(dxf, 0)
    else:
        shape, _, gz = expr.partition('/')
        if facing == 'right':                       # glances are screen directions: flip them before mirroring
            gz = {'l': 'r', 'r': 'l'}.get(gz, gz)
        _draw_eyes(ff, kind, shape + ('/' + gz if gz else ''))
        out = _place(ff, facing, dxf)
    if facing == 'right' and expr.startswith('sparkle'):
        raise ValueError('the sparkle glint would flip')
    out.meta = {'fine_face': [expr]}
    return out


_BODIES = {}


def body(kind, facing, dxf, larm='side', rarm='side'):
    key = (kind, facing, dxf, larm, rarm)
    if key not in _BODIES:
        if kind == 'front':
            _BODIES[key] = _place(_front(larm, rarm), 'front', dxf, 'front')
        elif kind == 'half':
            _BODIES[key] = _place(_half(), facing, dxf, 'half')
        else:
            _BODIES[key] = _place(_turned(), facing, dxf)
    return _BODIES[key].copy()


# --------------------------------------------------------------------------------------------
# the story: (body frame, face frame or None, ms) + named times for the thought layer
# --------------------------------------------------------------------------------------------
def _story():
    s, T = [], {}

    def stand(kind, facing, dxf, expr, ms, **arms):
        s.append((body(kind, facing, dxf, **arms), eyes(kind, facing, dxf, expr), ms))

    def turn(kind, facing, dxf, expr, ms):
        """A passing in-between of a turn: shown once, so his eyes ride in the body frame (smaller SVG)."""
        b = body(kind, facing, dxf)
        b.px.update(eyes(kind, facing, dxf, expr).px)
        s.append((b, None, ms))

    def mark(name):
        T[name] = sum(ms for _, _, ms in s)

    def walk_run(facing, dxf0, dist, blink=None):
        """Walk `dist` fine pixels (2 per cell) from dxf0: kit steps until the body has moved that far."""
        steps = []
        i = 0
        while not steps or steps[-1] < dist:
            steps.append(4 * (i // 5) + D[i % 5])
            i += 1
        n = len(steps)
        sign = 1 if facing == 'right' else -1
        for i, moved in enumerate(steps):
            ms = EASE_IN[i] if i < len(EASE_IN) else EASE_OUT[i - (n - len(EASE_OUT))] if i >= n - len(EASE_OUT) else STEP
            s.append((walk(facing, i % 5, dxf0 + sign * moved, (blink or {}).get(i, 'open/d')), None, ms))
        return dxf0 + sign * dist

    F, Hf, Tn = 'front', 'half', 'turned'
    # HOME, facing you: pondering under the "..." (frame 0)
    stand(F, F, 0, 'open/u', 1600)
    stand(F, F, 0, 'half/u', 70)
    stand(F, F, 0, 'line', 80)
    stand(F, F, 0, 'half/d', 70)
    mark('floor')
    stand(F, F, 0, 'open/d', 420)                     # eyes to the floor ...
    stand(F, F, 0, 'open/r', 260)                     # ... a glance right (the gaze leads) ...
    turn(Hf, 'right', 0, 'open/d', 110)               # ... and he turns
    x = walk_run('right', 0, REACH)
    # right end
    stand(Tn, 'right', x, 'open/d', 380)              # stops
    mark('right_up')
    stand(Tn, 'right', x, 'open/u', 1150)             # looks up: an idea almost comes ...
    stand(Tn, 'right', x, 'half/u', 70)               # ... and fizzles: a blink
    stand(Tn, 'right', x, 'line', 80)
    stand(Tn, 'right', x, 'half/d', 70)
    stand(Tn, 'right', x, 'open/l', 320)              # a glance back over his shoulder ...
    turn(Hf, 'right', x, 'open/l', 100)               # ... and he turns, through facing you
    turn(F, F, x, 'open/l', 110)
    turn(Hf, 'left', x, 'open/d', 100)
    x = walk_run('left', x, 2 * REACH, {6: 'half/d', 7: 'line/d', 8: 'half/d'})   # a blink on the way past HOME
    # left end
    stand(Tn, 'left', x, 'open/d', 380)
    mark('left_up')
    stand(Tn, 'left', x, 'open/u', 760)               # looks up again: nothing comes ...
    stand(Tn, 'left', x, 'half/u', 420)               # ... his lids droop: not yet
    stand(Tn, 'left', x, 'open/r', 320)               # a glance back toward HOME ...
    turn(Hf, 'left', x, 'open/r', 100)                # ... and he turns
    turn(F, F, x, 'open/r', 110)
    turn(Hf, 'right', x, 'open/d', 100)
    x = walk_run('right', x, REACH)
    assert x == 0
    # HOME
    turn(Hf, 'right', 0, 'open/d', 120)               # stops, half-turned ...
    mark('home')
    stand(F, F, 0, 'open/u', 220)                     # ... turns to you, eyes up ...
    stand(F, F, 0, 'wide', 160)                       # ... the thought arrives: wide ...
    stand(F, F, 0, 'sparkle', 560)                    # ... sparkle
    stand(F, F, 0, 'open/d', 180, larm='down', rarm='down')   # a little nod: eyes and claws dip
    stand(F, F, 0, 'open', 130)
    mark('dots_in')
    stand(F, F, 0, 'open/u', 200)                     # eyes back up as the "..." fades in -> frame 0
    return s, T


# --------------------------------------------------------------------------------------------
# thought layer (normal pixels): "...", the faint glint, the gold sparkle; each grows in and fades out
# --------------------------------------------------------------------------------------------
_DOTS = get('dots_wave')                     # gray "..." with a wave hopping through it (frame 3 = resting)
_DOTS_FAINT = _DOTS.sprite(3).recolor({'N': 'm'})
_SPARK = get('sparkle')                      # gold twinkle: dot, plus, star, long plus
_FAINT = [s.recolor({'j': 'm', 'y': 'm'}) for s in get('sparkle_small').frames]   # a gray glint that almost came


def _thought(items):
    f = Frame()
    for kind, i, x, y in items:
        spr = {'dots': lambda: _DOTS.sprite(i), 'dots_faint': lambda: _DOTS_FAINT, 'spark': lambda: _SPARK.sprite(i),
               'faint': lambda: _FAINT[i]}[kind]()
        f.place(spr, x, y)
    return f


def _thought_track(T):
    hx, hy = HOME[0] + 5, HOME[1] - 2            # above his head at HOME (15, 10)
    rx = hx + 2                                  # ... at the right end (1.5 cells over)
    up, home = T['right_up'], T['home']
    return [
        (0, [('dots', 3, hx, hy)]),              # frame 0: resting "..."
        (600, [('dots', 0, hx, hy)]),            # one slow ripple through it
        (780, [('dots', 1, hx, hy)]),
        (960, [('dots', 2, hx, hy)]),
        (1140, [('dots', 3, hx, hy)]),
        (T['floor'], [('dots_faint', 0, hx, hy)]),   # eyes to the floor: the dots fade
        (T['floor'] + 150, []),
        (up + 250, [('faint', 0, rx, hy - 2)]),      # the faint glint: dot, plus, dot, gone
        (up + 380, [('faint', 1, rx, hy - 2)]),
        (up + 560, [('faint', 0, rx, hy - 2)]),
        (up + 680, []),
        (home + 120, [('spark', 0, hx, hy - 2)]),    # the gold sparkle grows (his eyes go wide a beat later) ...
        (home + 220, [('spark', 1, hx, hy - 2)]),
        (home + 330, [('spark', 2, hx, hy - 2)]),
        (home + 520, [('spark', 3, hx, hy - 2)]),
        (home + 660, [('spark', 1, hx, hy - 2)]),
        (home + 780, [('spark', 0, hx, hy - 2)]),    # ... and fades
        (home + 880, []),
        (T['dots_in'], [('dots_faint', 0, hx, hy)]),  # the "..." fades back in -> frame 0
    ]


def _segments(keys, loop):
    out = []
    for i, (t, v) in enumerate(keys):
        t2 = keys[i + 1][0] if i + 1 < len(keys) else loop
        assert t2 > t, (t, t2, v)
        out.append((v, t2 - t))
    return out


def build():
    story, T = _story()
    loop = sum(ms for _, _, ms in story)
    empty = Frame(res=2)
    clawd_l = [(b, ms) for b, _, ms in story]
    face_l = [(e if e is not None else empty, ms) for _, e, ms in story]
    thought = [(_thought(v), ms) for v, ms in _segments(_thought_track(T), loop)]
    for lst in (clawd_l, face_l, thought):
        assert total_ms(lst) == loop
    return anim(NAME, DESC, [
        layer('clawd', clawd_l),                 # fine (half-size pixels): walk kit, half-turns, front pose
        layer('face', face_l),                   # fine: his eyes while he stands
        layer('thought', thought),
    ], state=STATE)
