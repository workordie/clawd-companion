"""thinking-stars - Thinking variant: stargazing; the stars join up into ideas.   5-90 s on screen: calm, one payoff.

Storyboard (one loop = 16.83 s; every layer but the far stars is cut from one beat list, story())
  0.00  frame 0 (the reduced-motion still): Clawd at HOME gazing up at a "?" drawn in the stars above him (gold
        stars, thin lavender lines), three loose stars around it.  1.20 blink
  2.13  the question lets go: its lines break up (dashed, then sparse) and are gone (2.51)
  2.67  the ten stars drift to new places (eased, five steps); his eyes stay with them
  3.68  one by one, a line GROWS from star to star (three beats a line), the star it reaches twinkling softly:
        top (3.68), right side (4.28; blink 4.77), bottom (5.17), left side (5.73) ... a box?  (6.28, a doubtful
        half-lid) ... then four short legs grow, two at a time (6.88, 7.13), and at 7.68 the two stars inside light
        up as EYES: it's a tiny Clawd in the sky.  7.91 his eyes go wide
  8.07  PAYOFF: the glow flows along every line from its start star and the constellation shines Clawd orange
        (8.20), its corner stars twinkle, the shine is in his eyes (sparkle); 9.20 a blink, and he glances at you
 10.26  a meteor streaks right to left across the whole top of the sky; a beat later his eyes catch it (look_r),
        follow it overhead and off to the left (look_l); its tail lingers, shortening and cooling (11.25 - 11.51)
 11.77  the glow ebbs back along the lines, 12.30 they break up and fade; 12.84 blink; 13.21 the stars drift back;
        14.22 - 15.26 the "?" grows back stroke by stroke, 15.54 its dot twinkles; 16.08 blink -> frame 0
Eye closures: 1.20, 4.77, 9.20, 12.84, 16.08 s, and the half-lid at 6.28 s.  The far stars twinkle on their own
co-prime 4.8 s loop.

Face: the kit's fine-line eyes (fine() + fine_face(): open / half / line / look_u / look_r / look_l / wide /
sparkle).  No mouth, no blush, never resized: his body never moves (one static layer); only his eyes act.
Two-theme rule: stars are gold ('j', with yellow/white cores only inside a twinkle), lines lavender ('l'), the glow
Clawd orange: all mid-tones that read on #1E1E1E and on #FFFFFF.
Layers (back to front): far (a few faint far stars twinkling on their own loop) | lines | stars | body (static
Clawd, solid face) | face (FINE: only his eye pixels) | shoot (the shooting star).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'thinking-stars'
STATE = 'thinking (variant)'
DESC = ('Stargazes under a "?" drawn in the stars: it fades, the stars drift and he joins them up line by line into '
        'a tiny Clawd constellation that glows orange, a shooting star streaks past, and the stars drift back into '
        'the question.')

HX, HY = HOME

# --------------------------------------------------------------------------------------------
# the two constellations.  Ten stars each; star i of the "?" drifts to star i of the Clawd and back (each paired with
# a near one, so the drift paths are short).
# --------------------------------------------------------------------------------------------
Q = [(13, 3), (15, 1), (18, 1), (19, 3), (16, 6), (16, 8), (16, 10),        # the "?": hook, stem, dot
     (5, 4), (24, 7), (8, 9)]                                              # three loose stars
C = [(11, 3), (13, 5), (17, 5), (19, 3), (19, 8), (17, 10), (13, 10),      # Clawd: TL, eyes, TR, BR, feet ...
     (11, 8), (19, 10), (11, 10)]                                          # ... BL, feet
C_EYES = (1, 2)

Q_LINES = [(Q[0], Q[1]), (Q[1], Q[2]), (Q[2], Q[3]), (Q[3], Q[4]), (Q[4], Q[5])]     # the "?" (Q[6] is its dot)
BOX = [((11, 3), (19, 3)), ((19, 3), (19, 8)), ((19, 8), (11, 8)), ((11, 8), (11, 3))]
LEGS = [((11, 8), (11, 10)), ((19, 8), (19, 10)), ((13, 8), (13, 10)), ((17, 8), (17, 10))]


def seg(a, b):
    """The cells of a line from a to b, in drawing order (Bresenham, clean diagonals)."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err, out = dx + dy, []
    while True:
        out.append((x0, y0))
        if (x0, y0) == (x1, y1):
            return tuple(out)
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


# --------------------------------------------------------------------------------------------
# layers
# --------------------------------------------------------------------------------------------
PLUS = Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1))                  # a soft twinkle (the brightest a star gets)


def lines(s):
    """s['lines']: tuple of (cells in drawing order, colour, how many are drawn, pattern).  pattern: 'all', 'dash'
    (every other cell), 'sparse' (every third), 'glow' (the first half of the line lit orange, the rest lavender: the
    glow flowing along it from its start star)."""
    f = Frame()
    for cells, ch, n, pat in s['lines']:
        for i, (x, y) in enumerate(cells[:n]):
            if (pat == 'dash' and i % 2) or (pat == 'sparse' and i % 3):
                continue
            f.put(x, y, ('#' if i < (len(cells) + 1) // 2 else 'l') if pat == 'glow' else ch)
    return f


def stars(s):
    f = Frame()
    for i, (x, y) in enumerate(s['stars']):
        if i in s['flash']:
            f.place(PLUS, x, y)
        else:
            f.put(x, y, 'j')
    return f


def body():
    f = Frame()
    put_clawd(f, clawd(eyes='blink'))
    return f


_P = clawd(eyes='blink')


def face(s):
    """FINE layer: only the half-size eye pixels that differ from his solid face."""
    f = Frame()
    put_clawd(f, _P)
    base = fine(f)
    ff = fine_face(base.copy(), _P, HX, HY, s['face'])
    out = Frame(res=2)
    for q, v in ff.px.items():
        if base.px.get(q) != v:
            out.px[q] = v
    out.meta = {'fine_face': [s['face']]}
    return out


# the meteor: a white-hot head (a little gold plus) and a gold-to-rust tail streaking right to left across the top
# of the sky; the tail grows as it comes in and lingers, shortening and cooling, after the head has gone
TAIL = 'yjjooOO'


def meteor_path():
    return [(x, 1 if x >= 9 else 2) for x in range(33, -9, -3)]     # drops a row only once it is past the box


def shoot(s):
    f = Frame()
    if not s['shoot']:
        return f
    k, cut = s['shoot']                          # k: step along the path; cut: tail cells already burnt out
    path = meteor_path()
    hx, hy = path[min(k, len(path) - 1)]
    cells = {}
    if k < len(path):                            # the head
        cells[(hx, hy)] = 'W'
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            cells[(hx + dx, hy + dy)] = 'j'
    trail = []                                   # the tail: the cells it has just crossed, nearest first
    for (px, py), (qx, qy) in zip(path[max(0, k - 3):k + 1][::-1], path[max(0, k - 3):k + 1][::-1][1:]):
        trail += [c for c in seg((px, py), (qx, qy))[1:]]
    if k >= len(path):
        trail = [(x + 3 * (k - len(path) + 1), y) for x, y in trail]
    for i, c in enumerate(trail[:len(TAIL)]):
        if i >= len(TAIL) - cut:
            break
        cells.setdefault(c, TAIL[i + max(0, cut - 2)] if i + max(0, cut - 2) < len(TAIL) else 'O')
    for (x, y), ch in cells.items():
        if 0 <= x < W and 0 <= y < H:
            f.put(x, y, ch)
    return f


# far stars: faint gray dots that twinkle now and then (own loop, co-prime with the story)
FAR = [(2, 1), (28, 2), (30, 8), (3, 11), (23, 0)]
FAR_LOOP = [(None, 1300), (1, 110), (None, 1250), (3, 120), (None, 900), (0, 110), (None, 1010)]


def far(tw):
    f = Frame()
    for i, (x, y) in enumerate(FAR):
        if i == tw:
            f.place(Sprite(['.N.', 'NjN', '.N.'], anchor=(1, 1)), x, y)
        else:
            f.put(x, y, 'N')
    return f


# --------------------------------------------------------------------------------------------
# the story
# --------------------------------------------------------------------------------------------
UP = 'look_u'


def _lerp_pts(a, b, t):
    return [(int(round(lerp(p[0], q[0], t))), int(round(lerp(p[1], q[1], t)))) for p, q in zip(a, b)]


def story():
    S = []
    q_full = tuple((seg(a, b), 'l', 99, 'all') for a, b in Q_LINES)
    st = dict(stars=list(Q), lines=q_full, flash=(), face=UP, shoot=None)

    def b(ms, **kw):
        kw.setdefault('flash', ())
        kw.setdefault('shoot', None)
        st.update(kw)
        S.append((ms, dict(st)))

    def blink(after, eyes=None):
        eyes = eyes or st['face']
        b(70, face='half')
        b(90, face='line')
        b(70, face='half')
        b(after, face=eyes)

    def drift(a, bpos, ms=(170, 140, 120, 140, 180)):
        ts = ease(len(ms) + 1, 'inout')[1:]
        for t, m in zip(ts, ms):
            b(m, stars=_lerp_pts(a, bpos, t))

    def grow(new, steps, ms, done=(), flash_end=True):
        """Lines growing in from their start stars: `new` lines drawn over `steps` frames (all together)."""
        for k in range(1, steps + 1):
            cur = tuple(done) + tuple((c, 'l', -(-len(c) * k // steps), 'all') for c in new)
            ends = tuple(st['stars'].index(c[-1]) for c in new if c[-1] in st['stars']) if (k == steps and flash_end) else ()
            b(ms[k - 1], lines=cur, flash=ends)
        return tuple(done) + tuple((c, 'l', 99, 'all') for c in new)

    def restyle(pattern, colour='l'):
        return tuple((c, colour, n, pattern) for c, _, n, _ in st['lines'])

    # ---- frame 0: gazing up at the "?" ----------------------------------------------------------------
    b(1200)
    blink(700)
    # ---- the question lets go: its lines break up and fade ------------------------------------------------
    b(200, lines=restyle('dash'))
    b(180, lines=restyle('sparse'))
    b(160, lines=())
    drift(Q, C)
    b(260)
    # ---- one by one, lines grow between the stars: a box ... ------------------------------------------------
    box = [seg(a, b_) for a, b_ in BOX]
    done = grow([box[0]], 3, (110, 110, 140))
    b(240)
    done = grow([box[1]], 3, (100, 100, 130), done)
    b(160)
    blink(170)
    done = grow([box[2]], 3, (110, 110, 140), done)
    b(200)
    done = grow([box[3]], 3, (100, 100, 130), done)
    b(220)
    b(380, face='half')                                    # ... a box?
    b(220, face=UP)
    # ---- ... four short legs, and the two stars inside light up as eyes: it's Clawd -----------------------
    legs = [seg(a, b_) for a, b_ in LEGS]
    done = grow(legs[:2], 2, (110, 140), done)
    done = grow(legs[2:], 2, (110, 140), done)
    b(300)
    b(140, flash=C_EYES)                                   # the eyes light up ...
    b(90)
    b(160, face='wide')                                    # ... and a beat later his eyes go wide
    # ---- payoff: it glows Clawd orange --------------------------------------------------------------------
    b(130, lines=restyle('glow'))                          # the glow flows along every line from its start ...
    b(150, lines=restyle('all', '#'), face='sparkle', flash=(0, 4))
    b(150, flash=(3, 7))
    b(140)
    b(560)
    b(70, face='half')
    b(80, face='line')
    b(70, face='half')
    b(620, face='open')                                    # a glance at you: that's me
    b(220, face=UP)
    # ---- a meteor streaks across the top of the sky, right to left; his eyes chase it ------------------------
    n = len(meteor_path())
    eyes = {1: 'look_r', 4: UP, 9: 'look_l'}               # he notices it a beat after it appears
    for k in range(n):
        b(70, shoot=(k, 0), **({'face': eyes[k]} if k in eyes else {}))
    for cut in (2, 4, 6):                                  # the tail lingers, shortening and cooling
        b(90, shoot=(n - 1 + cut // 2, cut))
    b(260, face=UP)
    # ---- the glow cools, the lines fade, the stars drift back -------------------------------------------------
    b(150, lines=restyle('glow'))                          # ... and ebbs back the same way
    b(380, lines=restyle('all', 'l'))
    b(200, lines=restyle('dash'))
    b(180, lines=restyle('sparse'))
    b(160, lines=())
    blink(140)
    drift(C, Q)
    b(260)
    # ---- the question grows back, stroke by stroke --------------------------------------------------------------
    q = [seg(a, b_) for a, b_ in Q_LINES]
    done = ()
    for i, c in enumerate(q):
        done = grow([c], 2, (110, 150 if i < 4 else 170), done, flash_end=False)
    b(160, flash=(6,))                                     # ... and its dot
    b(380)
    blink(520, UP)
    return S


def build():
    S = story()
    farl = [(far(tw), ms) for tw, ms in FAR_LOOP]
    return anim(NAME, DESC, [
        layer('far', farl),
        layer('lines', [(lines(s), ms) for ms, s in S]),
        layer('stars', [(stars(s), ms) for ms, s in S]),
        static('body', body()),
        layer('face', [(face(s), ms) for ms, s in S]),
        layer('shoot', [(shoot(s), ms) for ms, s in S]),
    ], state=STATE)
