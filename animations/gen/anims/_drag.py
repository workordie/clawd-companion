"""Grab, throw, drop (DRAFTS; '_' files are skipped by make.py).

The patch lets you grab Clawd with the mouse, throw him or drop him. It moves the element; these
SVGs are what he does meanwhile. Everything is drawn around his home box so the patch only has to
position the element.

  grabbed     loop       held up by the top of his head (lifted a cell, legs dangling): bursts of
                         pedalling kicks with follow-through, a glance at the ground, uneven rhythm
  tumble      loop       thrown: two full turns in exact 90-degree steps about his body centre, with
                         motion arcs trailing his head and feet
  fall        loop       dropped from high up: arms flailing, legs fluttering, eyes wide, wind streaks
                         rushing up past him
  parachute   loop       hanging from a domed red/white canopy (panels, top-left light, scalloped
                         hem, lines to his hands): a slow pendulum sway, canopy leading, body lagging
  chute-pop   one-shot   (0.4 s) clicked under the chute: the lines snap, the canopy whips up and away
                         collapsing, he reaches after it; ends in the `fall` pose for the switch
  land        one-shot   a soft landing: contact with dust, a 1-cell rebound, arms follow through,
                         a look at the dust, a blink
  land-chute  one-shot   touchdown under the chute: he lets go, the canopy sinks behind him and drapes
                         on the ground at his side, sighs flat, and is packed away in a poof
  crash       one-shot   a hard landing after a throw: thud on his back with a burst, a bounce, legs
                         kicking, a flip back onto his feet, dizzy stars, he shakes them off
All one-shots end at HOME in the plain standing pose. He keeps his normal 9 x 6 body throughout (only
legs change; rotations are exact quarter turns).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402
from anims._click_kit import B, FX, compose, blink  # noqa: E402,F401

X0, Y0 = HOME
LEGX = (1, 3, 7, 9)                          # his leg columns in the box


# --------------------------------------------------------------------------------------------
# helpers
def safe(f, x, y, ch):
    """Put a pixel only if it is on the canvas (deliberately cropped things don't count as clipping)."""
    if 0 <= x < W * f.res and 0 <= y < H * f.res:
        f.put(x, y, ch)


def stamp(f, spr, x, y, flip=False, below=None):
    """Like Frame.place, cropped silently at the canvas edges (and at row `below` if given)."""
    if flip:
        spr = spr.flipped()
    for sx, sy, ch in spr.cells:
        yy = y + sy - spr.ay
        if below is not None and yy > below:
            continue
        safe(f, x + sx - spr.ax, yy, ch)


def rows_at(f, rows, x, y, skip='.'):
    """Draw a list of strings with its top-left at (x, y), cropped silently."""
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch not in skip and ch != ' ':
                safe(f, x + i, y + j, ch)


def item(name, i, x, y, flip=False, below=None):
    return lambda f: stamp(f, get(name).sprite(i), x, y, flip, below)


def him(f, x=X0, y=Y0, eyes='open', larm='side', rarm='side', legs='stand'):
    """Draw Clawd with his box's top-left at (x, y). legs: a kit leg style, or 4 (length, foot_dx) pairs
    for the columns 1, 3, 7, 9 (foot_dx bends the leg below its first cell sideways: a kick)."""
    custom = not isinstance(legs, str)
    p = clawd(eyes=eyes, larm=larm, rarm=rarm, legs='none' if custom else legs)
    put_clawd(f, p, x, y)
    if custom:
        for c, (n, fdx) in zip(LEGX, legs):
            for i in range(n):
                f.put(x + c + (fdx if i >= 1 else 0), y + 6 + i, '#')
    return p


def shot(behind=(), front=(), face=None, **kw):
    """One FINE frame: `behind` drawers, Clawd (kw -> him()), his fine face (a FINE_EYES name, or None
    for the kit eyes in kw), then `front` drawers. Drawers are callables f -> None on a normal frame."""
    f = Frame()
    for d in behind:
        d(f)
    x, y = kw.pop('x', X0), kw.pop('y', Y0)
    p = him(f, x, y, **kw)
    if not face:                             # plain kit eyes: stay at cell resolution
        for d in front:
            d(f)
        return f
    ff = fine(f)
    fine_face(ff, p, x, y, face)
    if front:
        g = Frame()
        for d in front:
            d(g)
        ff.px.update(fine(g).px)
    return ff


# --------------------------------------------------------------------------------------------
# quarter turns, done in fine pixels about his body centre so he spins in place without wobbling
SPIN_BOX = (X0, Y0 - 2)                      # box while spinning: lifted so the sideways poses fit
_BCX, _BCY = 2 * SPIN_BOX[0] + 11, 2 * SPIN_BOX[1] + 6     # body centre, a fine pixel corner


def spun(ff, rot):
    """Rotate a fine frame rot quarter turns clockwise about his body centre (exact, no rounding)."""
    out = Frame(res=2)
    out.meta = dict(ff.meta)
    for (i, j), c in ff.px.items():
        for _ in range(rot % 4):
            i, j = _BCX + _BCY - 1 - j, _BCY - _BCX + i
        safe(out, i, j, c)
    return out


def turned(rot, face=None, dy=0, **kw):
    """Clawd (kw -> him()) turned rot quarter turns clockwise, his box at SPIN_BOX (+dy rows)."""
    ff = fine(shot(face=face, x=SPIN_BOX[0], y=SPIN_BOX[1], **kw))
    ff = spun(ff, rot)
    if dy:
        ff = ff.shifted(0, 2 * dy)
    return ff


def arc(f, cx, cy, r, a0, a1, ch, dash=None):
    """Cells on a circle of radius r around (cx, cy) from angle a0 to a1 (degrees, screen: 0 = right,
    90 = down). dash: (on, off) cell counts to fade the tail."""
    pts = []
    steps = max(8, int(abs(a1 - a0) / 4))
    for s in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * s / steps)
        p = (int(round(cx + r * math.cos(a))), int(round(cy + r * math.sin(a))))
        if not pts or pts[-1] != p:
            pts.append(p)
    for n, (x, y) in enumerate(pts):
        if dash and n % sum(dash) >= dash[0]:
            continue
        if 1 <= x < W - 1 and 0 <= y < H:
            f.put(x, y, ch)


# --------------------------------------------------------------------------------------------
# grabbed
HANG, MID, TUCK = (3, 0), (2, 0), (1, 0)
KICK_A, KICK_B = (3, -1), (3, 1)             # pair A = legs 1+7 kicks swing left, B = legs 3+9 right


def legs_ab(a, b):
    return [a, b, a, b]


def grabbed():
    """Loop (~2.6 s). Held up by his head, lifted a cell: legs dangle 3 long. He hangs and looks down,
    realises, pedals in a burst (kicks swing out and come back), flails, gives up, glances at the
    ground either side, blinks, a shorter burst, and hangs looking down again."""
    y = Y0 - 1
    K = []
    def k(ms, a, b, la, ra, face=None, eyes='open', dx=0):
        K.append((shot(legs=legs_ab(a, b), larm=la, rarm=ra, face=face, eyes=eyes, x=X0 + dx, y=y), ms))
    k(480, HANG, HANG, 'out', 'out', face='look_d')         # the still: dangling, looking down
    k(150, HANG, HANG, 'up', 'up', face='wide')             # !
    k(90, TUCK, HANG, 'raise', 'out', face='wide')          # burst: pedal
    k(80, KICK_A, MID, 'out', 'raise', face='wide', dx=-1)
    k(90, HANG, TUCK, 'raise', 'down', face='wide')
    k(80, MID, KICK_B, 'down', 'raise', face='wide', dx=1)
    k(90, TUCK, HANG, 'raise', 'out', face='wide')
    k(100, KICK_A, MID, 'out', 'raise', face='wide', dx=-1)
    k(130, HANG, (3, 1), 'up', 'up', face='wide')           # follow-through: the B feet swing back
    k(160, HANG, HANG, 'side', 'side', face='open')         # gives up
    k(340, HANG, HANG, 'side', 'side', eyes='look_dl')      # how far down is it?
    k(280, HANG, HANG, 'side', 'side', eyes='look_dr')
    k(60, HANG, HANG, 'side', 'side', face='half')
    k(80, HANG, HANG, 'side', 'side', face='line')
    k(60, HANG, HANG, 'side', 'side', face='half')
    k(90, MID, KICK_B, 'up', 'raise', face='wide', dx=1)    # one more try
    k(80, KICK_A, TUCK, 'raise', 'up', face='wide')
    k(90, TUCK, KICK_B, 'up', 'raise', face='wide', dx=1)
    k(150, (3, -1), HANG, 'out', 'out', face='open')        # follow-through, arms drop to out
    k(220, HANG, HANG, 'out', 'out', face='look_d')
    return K


# --------------------------------------------------------------------------------------------
# tumble
def tumble():
    """Loop (2 turns, 640 ms). Exact quarter turns about his body centre with motion arcs trailing his
    head and his feet (clockwise spin). His arms and legs change every half turn (spread out, flung up,
    swapped) so the two turns differ; eyes wide, then open for a half turn."""
    seq = []
    cx, cy = SPIN_BOX[0] + 5.5, SPIN_BOX[1] + 3.0       # body centre in cells
    poses = [dict(larm='out', rarm='out', legs='stand', face='wide'),
             dict(larm='out', rarm='out', legs='stand', face='wide'),
             dict(larm='up', rarm='raise', legs=legs_ab(HANG, MID), face='wide'),
             dict(larm='up', rarm='raise', legs=legs_ab(HANG, MID), face='wide'),
             dict(larm='raise', rarm='up', legs=legs_ab(MID, HANG), face='open'),
             dict(larm='raise', rarm='up', legs=legs_ab(MID, HANG), face='open'),
             dict(larm='out', rarm='out', legs='stand', face='wide'),
             dict(larm='out', rarm='out', legs='stand', face='wide')]
    for n, kw in enumerate(poses):
        rot = n % 4
        ff = turned(rot, **kw)
        g = Frame()
        feet = 90 + 90 * rot                            # where his feet point (screen angle)
        for base in (feet, feet + 180):
            arc(g, cx, cy, 6.6, base - 22, base - 62, 'm')                 # solid right behind
            arc(g, cx, cy, 6.6, base - 67, base - 85, 'm', dash=(1, 1))    # fading tail
        trail = fine(g)
        for k_, v in trail.px.items():
            if k_ not in ff.px:
                ff.px[k_] = v
        seq.append((ff, 80))
    return seq


# --------------------------------------------------------------------------------------------
# fall
def streaks(f, k, lanes, speed=4, period=20):
    """Wind streaks rushing up past him. lanes: (x, length, phase) per streak; each moves `speed` cells up
    per frame and wraps every `period` rows (seamless when period / speed divides the loop)."""
    for x, length, phase in lanes:
        y0 = (phase - speed * k) % period - 2
        for j in range(length):
            y = y0 + j
            if 1 <= y <= H - 3:
                f.put(x, y, 'm')


FALL_BOX = (X0, Y0 - 1)
WIND = [(5, 5, 2), (6, 3, 12), (24, 4, 7), (26, 5, 17)]


def fall_pose(k):
    """Pose k (0-4) of the fall loop (frame 0 is also where chute-pop ends): arms flail overhead, legs
    flutter, a slight sideways wobble."""
    arms = [('wave', 'raise'), ('raise', 'wave'), ('wave', 'wave'), ('raise', 'up'), ('up', 'raise')][k]
    legs = [legs_ab(HANG, MID), legs_ab(MID, HANG), legs_ab(HANG, HANG), legs_ab(MID, HANG), legs_ab(HANG, MID)][k]
    dx = [0, 0, 0, 1, 0][k]
    return dict(larm=arms[0], rarm=arms[1], legs=legs, dx=dx)


def fall():
    """Loop (500 ms). Arms flail overhead, legs flutter, eyes wide, wind streaks rush up past him."""
    seq = []
    for k in range(5):
        pz = fall_pose(k)
        dx = pz.pop('dx')
        wind = lambda f, k=k: streaks(f, k, WIND)
        seq.append((shot(behind=[wind], face='wide', x=FALL_BOX[0] + dx, y=FALL_BOX[1], **pz), 100))
    return seq


# --------------------------------------------------------------------------------------------
# the parachute
# Canopy, 19 x 6: a dome of five panels (red / white / red / white / red) whose seams curve toward the
# apex, lit from the top-left (white highlights and a pink streak on the left, gray and dark red on the
# right), with a scalloped hem: each panel billows up between the cusps where the lines attach. White
# panels get a silver rim where they touch the sky, so the dome keeps its outline on the light theme.
CANOPY = [
    '.....rmmrrrmmR.....',
    '...rrWWWprrMMMRR...',
    '..rrwwwwrrrMMMMRR..',
    '.rrrwwwwrrrMMMMRRR.',
    'rrrwMMwrrrrrMMMMRRR',
    'R.Rm..mR...Rm..mR.R',
]
CUSPS = (0, 6, 12, 18)                       # sprite columns of the hem cusps the 4 lines hang from
HEM = len(CANOPY) - 1


def _shear(x, tilt):
    return 0 if 5 <= x <= 13 else (1 if x > 13 else -1) * tilt


def canopy_rows(tilt=0):
    """The canopy, tilted: tilt +1 lowers its right third a row and lifts its left third."""
    if not tilt:
        return CANOPY, 0
    w = len(CANOPY[0])
    grid = {}
    for y, row in enumerate(CANOPY):
        for x, ch in enumerate(row):
            if ch != '.':
                grid[(x, y + _shear(x, tilt) + 1)] = ch
    rows = [''.join(grid.get((x, y), '.') for x in range(w)) for y in range(len(CANOPY) + 2)]
    return rows, -1


def canopy(f, cx, top, tilt=0):
    """Draw the canopy centred on column cx with its dome top at row `top`. Returns the 4 line anchors."""
    rows, oy = canopy_rows(tilt)
    x0 = cx - len(CANOPY[0]) // 2
    rows_at(f, rows, x0, top + oy)
    out = []
    for c in CUSPS:
        out.append((x0 + c, top + HEM + _shear(c, tilt)))
    return out


CHUTE_BOX = (X0, Y0 - 1)                     # where he hangs under the chute


LINE = 's'                                   # the suspension lines


def rig(cx=0, tilt=0, bx=0, by=0, top=1, larm='raise', rarm='raise'):
    """A drawer for the open canopy plus its 4 lines to his hands (body box at CHUTE_BOX + (bx, by))."""
    def draw(f):
        anchors = canopy(Frame(), 15 + cx, top, tilt)
        p = clawd(larm=larm, rarm=rarm)
        lh = p.at('hand_l', CHUTE_BOX[0] + bx, CHUTE_BOX[1] + by)
        rh = p.at('hand_r', CHUTE_BOX[0] + bx, CHUTE_BOX[1] + by)
        for (ax, ay), hand in zip(anchors, (lh, lh, rh, rh)):
            f.line(ax, ay, hand[0], hand[1], LINE)
        canopy(f, 15 + cx, top, tilt)
    return draw


def chute_shot(cx=0, tilt=0, bx=0, by=0, top=1, face=None, eyes='open', legs='stand', larm='raise', rarm='raise',
               extra=(), front=()):
    """Clawd hanging under the open chute. cx, bx: canopy / body offsets from centre."""
    return shot(behind=[rig(cx, tilt, bx, by, top, larm, rarm)] + list(extra), front=front, face=face, eyes=eyes,
                legs=legs, larm=larm, rarm=rarm, x=CHUTE_BOX[0] + bx, y=CHUTE_BOX[1] + by)


def sway(n=16, s0=1):
    """Pendulum phases: (canopy dx, tilt, body dx). The canopy leads, the body follows 0.7 rad later and
    swings further, so the lines slant toward him. Starts centred (s0). (A tilted canopy was tried: at 19
    cells a one-row shear kinks the dome, so tilt stays 0.)"""
    out = []
    for s in range(s0, s0 + n):
        th = 2 * math.pi * s / n
        c = int(round(1.0 * math.sin(th)))
        b = int(round(1.6 * math.sin(th - 0.7)))
        d = b - c
        out.append((c, 0, b))
    return out


def parachute():
    """Loop (3.2 s). A slow pendulum (see sway). He looks down at where he'll land as he swings right,
    blinks, glances down-left on the way back, and looks at you again."""
    eyes = ['open', 'open', 'open', 'look_d', 'look_d', 'look_dr', 'look_d', 'open',
            'open', 'blink', 'open', 'open', 'look_dl', 'look_dl', 'open', 'open']
    seq = []
    for (c, t, b), e in zip(sway(), eyes):
        if e == 'blink':
            seq.append((chute_shot(cx=c, tilt=t, bx=b, eyes='blink'), 120))
            seq.append((chute_shot(cx=c, tilt=t, bx=b), 80))
        else:
            seq.append((chute_shot(cx=c, tilt=t, bx=b, eyes=e), 200))
    return seq


# --------------------------------------------------------------------------------------------
# chute-pop
# The released canopy whipping away: it folds (narrower and taller, hem pulled in), then crumples into a
# tilted bundle as it flies, then a small twisted wad. Lines trail behind it (down-left).
WHIP1 = [
    '....rmmrrmR....',
    '..rrWWprrMMRR..',
    '.rrwwwrrrMMMRR.',
    '.rrwwwrrrMMMRR.',
    '..rrmwrrrMMRR..',
    '...R.m.R.m.R...',
]
WHIP2 = [
    '....rrmR..',
    '..rrWWrRR.',
    '.rrwwrrMRR',
    'rrwwrrMMR.',
    '.rRmrRMR..',
    '..m.R.m...',
]
WHIP3 = [
    '..rmR.',
    '.rWrRR',
    'rrwRM.',
    '.mRR..',
]


def trailing(f, rows, x, y, length):
    """Loose lines trailing down-left from every hem cusp (bottom-row pixel) of a whip sprite at (x, y)."""
    last = len(rows) - 1
    prev = -9
    for i, ch in enumerate(rows[last]):
        if ch != '.' and i - prev >= 4:          # spaced out, or the diagonals mesh into a checkerboard
            prev = i
            for j in range(1, length + 1):
                safe(f, x + i - j, y + last + j, LINE)


def chute_pop():
    """One-shot (400 ms): snap! the lines part right above his hands (two sparks), the canopy jerks up a
    row; then it whips up and away to the right, folding, crumpling and trailing its loose lines, while
    he flings his arms up after it, eyes wide. The last frame is frame 0 of `fall`, which comes next."""
    seq = []
    box = dict(x=CHUTE_BOX[0], y=CHUTE_BOX[1])

    def snap(f):                                    # the upper halves of the lines stay on the canopy
        anchors = canopy(Frame(), 15, 0)
        for (ax, ay), d in zip(anchors, (1, -1, 1, -1)):
            f.line(ax, ay, ax + d, ay + 2, LINE)
        canopy(f, 15, 0)
    sparks = [item('sparkle_small', 1, 9, 8), item('sparkle_small', 1, 21, 8)]
    seq.append((shot(behind=[snap], front=sparks, face='wide', larm='raise', rarm='raise', **box), 70))

    def fly1(f):
        trailing(f, WHIP1, 12, -1, 3)
        rows_at(f, WHIP1, 12, -1)
    seq.append((shot(behind=[fly1], front=[item('sparkle_small', 2, 9, 8), item('sparkle_small', 2, 21, 8)],
                     face='wide', larm='wave', rarm='wave', **box), 70))

    def fly2(f):
        trailing(f, WHIP2, 19, -3, 4)
        rows_at(f, WHIP2, 19, -3)
    seq.append((shot(behind=[fly2], face='wide', larm='raise', rarm='wave', legs=legs_ab(MID, HANG), **box), 80))

    def fly3(f):
        trailing(f, WHIP3, 26, -2, 3)
        rows_at(f, WHIP3, 26, -2)
    seq.append((shot(behind=[fly3], face='wide', larm='wave', rarm='raise', legs=legs_ab(HANG, MID), **box), 80))
    # gone: the fall pose (= fall frame 0)
    pz = fall_pose(0)
    dx = pz.pop('dx')
    seq.append((shot(face='wide', x=FALL_BOX[0] + dx, y=FALL_BOX[1], **pz), 100))
    return seq


# --------------------------------------------------------------------------------------------
# land
def land():
    """One-shot (~1.4 s): contact with a dust burst (arms still up from the fall), arms swing down as
    he rebounds a cell, lands again with a smaller puff, arms follow through and settle, he looks at
    the dust, then back at you, and blinks."""
    D = 'dust_puff'
    seq = []
    def s(ms, *a, **kw):
        seq.append((shot(*a, **kw), ms))
    s(80, front=[item(D, 0, 15, 18)], larm='raise', rarm='raise', face='wide')
    s(90, front=[item(D, 1, 15, 18)], larm='up', rarm='up', face='wide')
    s(110, front=[item(D, 2, 15, 18)], larm='out', rarm='out', legs='short', y=Y0 - 1, face='open')  # rebound
    s(90, front=[item(D, 0, 15, 18)], larm='down', rarm='down', face='open')                        # down again
    s(120, front=[item(D, 2, 15, 18)], larm='side', rarm='side', face='open')                       # a smaller puff
    s(130, face='look_d')
    s(330, face='look_d')
    s(220, face='open')
    s(60, face='half')
    s(90, face='line')
    s(60, face='half')
    s(320, face='open')
    return seq


# --------------------------------------------------------------------------------------------
# land-chute
# The canopy losing its air: the same dome with rows taken out of its middle (flatter, same width)
SAG1 = [CANOPY[i] for i in (0, 1, 3, 4, 5)]
SAG2 = [CANOPY[1].replace('W', 'm')] + [CANOPY[i] for i in (3, 4, 5)]   # its new top gets the silver rim
# ...and lying in a heap on the ground at his left (partly behind him), sighing flatter
DRAPE = [
    '..pmr.....rR..',
    '.rrwwr..rrMMR.',
    'rrrwwwrrrrMMMR',
    'RRRmmmRRRRmmRR',
]
DRAPE_FLAT = [
    '...rmr...rR...',
    '.rrrwwrrrrMMR.',
    'RRRmmmRRRRmmRR',
]
DRAPE_FLATTER = [
    '..rrmmrrrrMR..',
    'RRRmmmRRRRmmRR',
]


def land_chute():
    """One-shot (~2.6 s). Touchdown under the chute (dust); he lets go and lowers his arms while the
    canopy, losing its air, sags and sinks, drifting left behind him, and settles in a heap at his side.
    He looks at it; it sighs flat; a poof packs it away; he looks back at you and blinks."""
    D = 'dust_puff'
    seq = []

    def c0(f):                                       # touchdown, still holding the lines
        a = canopy(Frame(), 15, 2)
        p = clawd(larm='raise', rarm='raise')
        lh, rh = p.at('hand_l'), p.at('hand_r')
        for (ax, ay), h in zip(a, (lh, lh, rh, rh)):
            f.line(ax, ay, h[0], h[1], LINE)
        canopy(f, 15, 2)
    seq.append((shot(behind=[c0], front=[item(D, 0, 15, 18)], larm='raise', rarm='raise'), 100))

    def sag(rows, x, y, droop):
        def d(f):                                    # loose lines hang straight down from the cusps
            for c in CUSPS:
                for j in range(1, droop + 1):
                    safe(f, x + c, y + len(rows) - 1 + j, LINE)
            rows_at(f, rows, x, y)
        return d
    seq.append((shot(behind=[sag(SAG1, 6, 4, 2)], front=[item(D, 1, 15, 18)], larm='up', rarm='up'), 120))
    seq.append((shot(behind=[sag(SAG2, 4, 8, 2)], front=[item(D, 2, 15, 18)], larm='out', rarm='out',
                     eyes='look_l'), 130))
    seq.append((shot(behind=[sag(SAG2, 2, 12, 1)], eyes='look_l'), 110))

    def heap(rows):
        return lambda f: rows_at(f, rows, 1, H - len(rows))
    seq.append((shot(behind=[heap(DRAPE)], eyes='look_l'), 640))                 # flump. he looks at it
    seq.append((shot(behind=[heap(DRAPE_FLAT)], eyes='look_l'), 150))            # it sighs flat
    seq.append((shot(behind=[heap(DRAPE_FLATTER)], eyes='look_l'), 380))
    # a poof packs it away (behind him; his left arm stays in front)
    for i, ms in enumerate([60, 110, 110, 140]):
        drawn = [heap(DRAPE_FLATTER)] if i == 0 else []
        seq.append((shot(behind=drawn + [item('poof', i, 8, 15, below=19)], eyes='look_l'), ms))
    seq.append((shot(face='open'), 300))
    seq.append((shot(face='half'), 60))
    seq.append((shot(face='line'), 90))
    seq.append((shot(face='half'), 60))
    seq.append((shot(face='open'), 360))
    return seq


# --------------------------------------------------------------------------------------------
# crash
def grounded(ff, lift=0):
    """Shift a turned fine frame so his lowest pixel rests on the ground row (minus `lift` cells), and
    tag him at HOME (he lies on the home spot)."""
    low = max(y for (x, y), c in ff.px.items() if c in '#@%k')
    out = ff.shifted(0, (2 * H - 1) - low - 2 * lift)
    out.meta['clawd'] = [(X0, Y0, dict(spec)) for _, _, spec in ff.meta.get('clawd', [])]
    return out


def crash():
    """One-shot (~3.5 s). Thud: upside down on his back, a burst behind him and dust; a small bounce;
    lies still (ow); legs kick; flips over in a quarter turn and lands on his feet; dizzy stars circle
    while he sways and follows them with his eyes; he shakes them off (they fly away) and blinks."""
    D, IMP, ST = 'dust_puff', 'impact_star', 'dizzy_stars'
    seq = []

    def down(ms, rot, lift=0, behind=(), front=(), **kw):
        ff = grounded(turned(rot, **kw), lift)
        if behind:
            g = Frame()
            for d in behind:
                d(g)
            for k_, v in fine(g).px.items():
                ff.px.setdefault(k_, v)
        if front:
            h = Frame()
            for d in front:
                d(h)
            ff.px.update(fine(h).px)
        seq.append((ff, ms))
    # thud (upside down, his head on the ground)
    flash = [item(IMP, 0, 10, 18, below=19), item(IMP, 0, 20, 18, below=19)]           # where his head hits
    down(60, 2, behind=flash, front=[item(D, 0, 15, 18)], larm='out', rarm='out', face='wide')
    down(90, 2, behind=[item(IMP, 2, 15, 15, below=19)], front=[item(D, 1, 15, 18)], larm='out', rarm='out',
         face='wide')                                                                      # spikes fly out
    down(90, 2, lift=1, front=[item(D, 2, 15, 18)], larm='up', rarm='up', legs=legs_ab(HANG, MID),
         face='wide')                                                                      # small bounce
    down(100, 2, front=[item(D, 0, 15, 18)])                                              # down again, softer
    down(110, 2, front=[item(D, 2, 15, 18)], face='half')
    down(320, 2, face='line')                                                              # ...ow
    down(80, 2, face='half')
    down(220, 2, face='open')
    down(90, 2, legs='walk_a')                                                             # legs kick
    down(90, 2, legs='walk_b')
    down(110, 2, legs='walk_a')
    seq.append((turned(3, larm='up', rarm='up', face='wide'), 80))                         # flip!
    seq.append((shot(larm='up', rarm='up', legs='short', y=Y0 - 1, face='wide'), 80))
    seq.append((shot(front=[item(D, 0, 15, 18)], larm='out', rarm='out', face='open'), 90))   # lands on his feet
    # dazed: stars circle, he sways with them and follows them with his eyes
    sway_ = [0, 0, 1, 1, 0, 0, -1, -1]
    looks = ['look_l', 'look_l', 'look_r', 'look_r'] * 2
    for k in range(8):
        dx = sway_[k]
        fr = [item(ST, k % 4, 15 + dx, 10)]
        if k < 2:
            fr.append(item(D, k + 1, 15, 18))
        seq.append((shot(front=fr, eyes=looks[k], x=X0 + dx), 120))
    # shake it off: the stars fly apart and fade
    flung = [[(12, 8), (18, 8), (15, 7)], [(9, 6), (21, 6), (15, 4)], [(6, 4), (24, 3), (16, 1)]]
    for k, (dx, eyes) in enumerate([(1, 'look_r'), (-1, 'look_l'), (1, 'look_r'), (0, 'open')]):
        fr = []
        if k < 3:
            fr = [item('sparkle_small', 1 if k < 2 else 0, x, y_) for x, y_ in flung[k]]
        seq.append((shot(front=fr, larm='out', rarm='out', eyes=eyes, x=X0 + dx), 70))
    seq.append((shot(face='open'), 300))
    seq.append((shot(face='half'), 60))
    seq.append((shot(face='line'), 90))
    seq.append((shot(face='half'), 60))
    seq.append((shot(face='open'), 360))
    return seq


DRAG = {
    'grabbed': (grabbed, 'Held up by his head: dangles, pedals in bursts, glances at the ground. Loop.', 'dragging'),
    'tumble': (tumble, 'Thrown: spins through the air in quarter turns with motion arcs. Loop.', 'thrown (flying)'),
    'fall': (fall, 'Dropped from high up: arms flailing, legs fluttering, eyes wide, wind rushing past. Loop.', 'falling'),
    'parachute': (parachute, 'Chute open: a slow pendulum sway, canopy leading, glancing at the ground. Loop.', 'parachuting'),
    'land': (land, 'Soft landing: dust, a little rebound, arms follow through, settle. One-shot.', 'landed'),
    'land-chute': (land_chute, 'Touchdown under the chute: it sinks behind him, drapes, sighs flat, packed away in a poof. One-shot.', 'landed'),
    'chute-pop': (chute_pop, 'Clicked under the chute: the lines snap, the canopy whips away, he reaches after it. One-shot, then fall.', 'falling'),
    'crash': (crash, 'Hard landing after a throw: thud on his back, bounce, flips upright, dizzy, shakes it off. One-shot.', 'landed hard'),
}


def build_drag(name):
    fn, desc, state = DRAG[name]
    frames = fn()
    res = frames[0][0].res
    if any(f.res != res for f, _ in frames):           # a mixed sequence: make it all fine
        frames = [(fine(f), ms) for f, ms in frames]
    return anim(name, desc, [layer('body', frames)], state=state)
