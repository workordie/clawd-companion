"""plan - Plan mode (idle while in plan mode).   On screen for a long time: calm, studious.

Clawd the explorer-professor (library fedora + half-moon reading glasses) studies a treasure-map blueprint
on an easel: a dotted route winds from a yellow start dot to a red X.  A globe on a brass stand keeps him
company.  Plain face, normal body size throughout (STYLE.md section 0): the acting is in his eyes, claws,
glasses, pencil and props.

Clawd's cycle is 28 s: two different 14 s stories, each with calm holds between its beats.  The map on the
easel alternates between two routes, so the whole picture only repeats every 56 s.

STORY A "the thinker" (0 - 14 s)
   0.00  frame 0: studying the plan (eyes level on the easel, pencil upright in his claw).  Calm hold;
         2.60 blink
   3.82  "mm-hm" nod, nod: on the first dip the glasses slip down his nose and stay there (a gap opens
         between his eyes and the rims)
   4.77  he peers at you over the slipped glasses ("the plan, for your approval?") .. 5.67 blink .. holds
   6.43  his left claw comes up (in-between), catches the slipped lens (6.51) and pushes claw and glasses up
         together (6.65); eyes up, thinking; one unhurried chin tap (7.35)
   8.41  the claw goes back down through an in-between; still thinking (eyes up, 1.2 s) .. 9.69 glances at
         the globe
  10.21  the claw winds up, 10.32 brushes the globe's edge and follows through (out, then lifts off); the
         globe turns HALF a turn in 1-column steps that slow down smoothly (80, 70, 95, 135, 200 ms) and
         rests on its other continent (10.90) .. 11.30 blink, back to work: a long calm study
STORY B "the planner" (14 - 28 s)
  14.00  studying; 15.10 blink
  15.82  a fresh page: the claw raises the pencil (in-between), lays it half into the easel's tray (its tip
         touches first), lets go and is already on the page's bottom corner (16.02, a grip beat).  The claw
         LIFTS the page: its bottom edge follows the claw tip up the sheet's left edge, one row (16.18), two
         rows (16.33, the arm at full reach); the claw lets go there and the arm holds its reach in a
         follow-through while the page sails up (16.45, 16.52), rolls over the clip bar and hangs there a
         beat (16.59) as the arm relaxes down the same arc (raise, up), then drops behind; the fresh page's
         corner settles in two beats (16.89, 16.99)
  17.09  a blank page: he looks it over, then up ("where to?")
  18.79  the route draws itself in four strides while his eyes trace it (up along the top, then down the
         side): he is plotting it in his head; the pencil waits in the tray
  21.15  he regards the finished route .. 21.65 blink
  22.16  X marks the spot: his claw reaches for the tray (in-between), lifts the pencil by its end (tip still
         on the tray), sets it on the X's top-right, stroke '/' (the pencil slides down its own 45 deg axis,
         the ink appears behind the tip), lift, the crossing stroke, a 170 ms press; the pencil comes back up
         (in-between) to his side as the finished X glints: the whole X gold, then its centre, then red
  23.40  calm study (25.59 blink) across the seam into story A: about 8 s of stillness in all
Cross-loop variety: the route layer and the globe layer are 56 s long (two Clawd cycles): every other page
gets the other route (a clockwise curl from the top-left, or a switchback trail), and every other flick
turns the globe back to its first continent.  The brass meridian catches the light on its own co-prime loop
(7.31 s).
Layers (back to front): scene (static: easel, blank page, globe stand, globe) | globe (the spin, 56 s) |
route (56 s) | ink (the X, the turning page, the glint on the X) | pencil (under Clawd: his claw covers the
end he holds; it also carries the wet X strokes, since it has a frame per stroke anyway) | clawd-static (the
cells every pose shares, his usual study eyes included) | specs (the glasses alone: they only change when
they move) | clawd (only the cells that change; a claw at his face is drawn in front of the glasses) | hat
(static) | glint (ambient).  Every split is exact (asserted); build() also asserts that an eye in his edge
column always has that side's arm beside it (a black eye at his edge would melt into the dark theme), that
the claw is on the lifted edge while it lifts, and that the pencil tip is on every X cell it inks.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'plan'
STATE = 'Plan mode (idle in plan mode)'
DESC = ('Explorer Clawd in a fedora and reading glasses studies a treasure-map plan on an easel; he nods, peers at '
        'you over his glasses, spins the globe, turns to a fresh page, traces a new route and marks the X.')
LOOP = 28000                                 # Clawd's cycle: story A (thinker) + story B (planner)
STORY = 14000


def _item(name, fallback):
    try:
        return get(name)
    except KeyError:                         # library mid-save: a local copy of the same look
        return fallback


_GLASSES = _item('reading_glasses', Item('reading_glasses', 'face', 'local fallback',
                                         Sprite(['..TccdccT..', '...dd.dd...'], anchor=(5, -1))))
_HAT = _item('fedora', Item('fedora', 'head', 'local fallback', Sprite([
    '...TT.TT...', '..TtTTTTd..', '..tTTTTTd..', '..nKKKKKn..', 'TtTTTTTTTTd', '.dd.....dd.'], anchor=(5, 5))))
_TWINKLE = _item('sparkle_small', Item('sparkle_small', 'fx', 'local fallback', [
    Sprite(['j'], anchor=(0, 0)), Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1)),
    Sprite(['j.j', '.j.', 'j.j'], anchor=(1, 1))]))

# --------------------------------------------------------------------------------------------
# Easel + blueprint pad (right of Clawd)
# --------------------------------------------------------------------------------------------
SX0, SY0, SW, SH = 22, 3, 9, 10              # the sheet: x 22-30, rows 3-12 (bright frame line printed on it)
SX1, SY1 = SX0 + SW - 1, SY0 + SH - 1
TRAY_Y = 13


def _easel():
    f = Frame()
    for x, y in ((23, 14), (23, 15), (23, 16), (22, 17), (22, 18), (22, 19)):      # front legs, splayed
        f.put(x, y, 'T')
    for x, y in ((29, 14), (29, 15), (29, 16), (30, 17), (30, 18), (30, 19)):
        f.put(x, y, 'T')
    f.vline(26, 14, 18, 'd')                                                       # back leg (receding)
    f.put(26, 1, 'T')                                                              # mast top
    f.hline(23, 29, 2, 's')                                                        # clip bar
    f.put(23, 2, 'm')
    for y in range(SY0, SY1 + 1):                                                  # blank page: navy,
        for x in range(SX0, SX1 + 1):                                              # bright blue frame line
            f.put(x, y, 'b' if (x in (SX0, SX1) or y in (SY0, SY1)) else 'B')
    f.hline(23, 29, TRAY_Y, 'T')                                                   # tray on the front legs
    f.hline(23, 25, TRAY_Y, 't')                                                   # (lit from the left)
    return f


# The two routes, in drawing order: start dot, then dash / waypoint pairs into the X.  Both have ten cells and
# draw in the same four hops, and both run along the top first and then down the side, so his eyes can trace
# either one with the same glances (up, then right).
ROUTES = [
    # 1 (frame 0): a clockwise curl from the top-left corner, along the top, down the right side, into the X
    [((23, 4), 'y'), ((24, 4), 'b'), ((25, 4), 'W'), ((26, 4), 'b'), ((27, 5), 'W'), ((28, 6), 'b'),
     ((28, 7), 'W'), ((28, 8), 'b'), ((27, 9), 'W'), ((26, 10), 'b')],
    # 2: a switchback trail: east along row 5, round the bend, back west along row 7, down into the X
    [((24, 5), 'y'), ((25, 5), 'b'), ((26, 5), 'W'), ((27, 5), 'b'), ((28, 5), 'W'), ((28, 6), 'b'),
     ((27, 7), 'W'), ((26, 7), 'b'), ((25, 7), 'W'), ((24, 8), 'b')],
]
HOPS = [1, 4, 7, 10]                         # route cells shown after each hop: the start, then 3-cell strides
HOP_MS = [520, 560, 600, 680]                # the line travels, easing into the X
XC = (24, 10)                                # the X: centre + diagonal neighbours
TR, C_, BL, TL, BR = (25, 9), (24, 10), (23, 11), (23, 9), (25, 11)
INK = {'none': [], 'tr': [TR], 'tr_c': [TR, C_], 's1': [TR, C_, BL], 's1_tl': [TR, C_, BL, TL],
       'full': [TR, C_, BL, TL, BR]}
# while he inks the X, the wet strokes travel in the pencil layer (it has a frame per stroke anyway):
# the ink appears behind the tip.  The ink layer only knows 'full' and 'none'.
PEN_INK = {'s1b': 'tr', 's1c': 'tr_c', 's2a': 's1', 's2b': 's1_tl', 's2c': 's1_tl'}
_ROUTE_CELLS = sorted({c for r in ROUTES for c, _ in r})


def route(cells):
    f = Frame()
    for (x, y), ch in cells:
        f.put(x, y, ch)
    return f


# The turning page.  Stages 1-4: the lifted bottom edge has risen to row `edge` and the sheet folds at row
# `fold` (the paper's length is kept: fold ~ (bottom + edge) / 2).  Between them we see the paper's back, the
# fold is the rolling curl, and below it the fresh page shows (any route cell there gets the fresh page's
# navy).  Stages 1-2 follow the claw tip (the claw holds the edge); at 3 the page has left the claw.
# 'flap': thrown over the clip bar, where it hangs for a beat; 's1'/'s2': the fresh page's corner settles.
CURL = {1: (11, 12), 2: (10, 11), 3: (6, 9), 4: (3, 7)}
BACK, FOLD = 'c', 'C'                        # the back: plain cyan (no frame line on it); the curl catches the
                                             # light (its two end cells stay cyan so it never meets the background)


def ink(s):
    """The X ink, the turning page and the glint on the X (one layer: they never share a frame)."""
    f = Frame()
    st = s['curl']
    if st in CURL:
        edge, fold = CURL[st]
        for x, y in INK[s['ink']]:
            if y < edge:
                f.put(x, y, 'r')
        for x, y in _ROUTE_CELLS:                     # the fresh page under the fold: no route on it
            if fold < y < SY1:
                f.put(x, y, 'B')
        f.rect(SX0, edge, SW, fold - edge, BACK)
        f.hline(SX0, SX1, fold, BACK)
        f.hline(SX0 + 1, SX1 - 1, fold, FOLD)
    elif st == 'flap':                                # thrown over the clip bar: rolled over it, lit on top
        f.hline(SX0 + 1, SX1 - 1, 1, BACK)
        f.hline(SX0 + 2, SX1 - 2, 2, FOLD)
        f.put(SX0 + 1, 2, BACK)
        f.put(SX1 - 1, 2, BACK)
        f.hline(SX0, SX1, SY0, BACK)
    elif st == 's1':                                  # the fresh page's corner flutters down ...
        f.put(SX0, SY1 - 1, 'c')
        f.put(SX0, SY1, 'c')
        f.put(SX0 + 1, SY1, 'C')
    elif st == 's2':                                  # ... and settles
        f.put(SX0, SY1, 'c')
    else:
        for x, y in INK[s['ink']]:
            f.put(x, y, 'r')
        if s['fx'] is not None:                       # the X glints: the whole X (2), then its centre (0):
            f.place(_TWINKLE.sprite(s['fx']), *XC)    # never the plus, which would fill the X into a block
    return f


# --------------------------------------------------------------------------------------------
# Globe (left of Clawd): sphere x 2-8, rows 10-16, on a brass meridian and a wooden foot
# --------------------------------------------------------------------------------------------
GX, GY = 2, 10
_MASK = ['..XXX..',
         '.XXXXX.',
         'XXXXXXX',
         'XXXXXXX',
         'XXXXXXX',
         '.XXXXX.',
         '..XXX..']
_LAND = ['............',          # the whole way round (12 columns): two continents in columns 1-4 and 7-11,
         '..gg....ggg.',          # ocean in columns 0, 5 and 6, so each face shows one continent whole and
         '.gggg..ggggg',          # never a sliver of the other.  A flick turns it HALF way (6 columns): it
         '..ggg...gggg',          # rests on the other continent until the next flick
         '...gg....gg.',
         '...g.....g..',
         '............']
SPIN = len(_LAND[0])
HALF = SPIN // 2
GLINT = (1, 1)                    # a fixed highlight (light from the top-left): the surface turns under it
MERIDIAN = [(5, 9), (4, 9), (3, 9), (2, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 16), (3, 17),
            (4, 17), (5, 17)]


def globe(k):
    f = Frame()
    for y, row in enumerate(_MASK):
        for x, m in enumerate(row):
            if m != 'X':
                continue
            land = _LAND[y][(x + k) % SPIN] == 'g'
            shade = x >= 5 or (x == 4 and y >= 5)
            ch = ('G' if shade else 'g') if land else ('B' if shade else 'b')
            if (x, y) == GLINT:
                ch = 'c'
            f.put(GX + x, GY + y, ch)
    return f


def _globe_stand():
    f = Frame()
    for x, y in MERIDIAN:
        f.put(x, y, 'j')
    f.put(5, 8, 'J')
    f.hline(4, 6, 18, 'T')
    f.hline(3, 7, 19, 'T')
    return f


# --------------------------------------------------------------------------------------------
# Clawd, his glasses and his pencil
# --------------------------------------------------------------------------------------------
# Hand-made right arms for lifting the page (1-cell limbs like the kit's, relative to (arm column, ay) as in
# clawdlib.ARMS): the claw tip rises straight up the sheet's left edge, (22,12) 'wave' -> (22,11) -> (22,10).
_RARMS = {
    'lift1': [(0, 0), (1, -1), (1, -2), (2, -3)],             # tip (22,11): on the edge at curl 1
    'lift2': [(0, 0), (1, -1), (1, -2), (2, -3), (2, -4)],    # tip (22,10): full reach, on the edge at curl 2
}


def _pose(s):
    rarm = s['rarm']
    p = clawd(eyes=s['eyes'], larm=s['larm'], rarm='none' if rarm in _RARMS else rarm)
    cells = {(x, y): c for x, y, c in p.sprite.cells}
    if rarm in _RARMS:
        g = GEOM['normal']
        for dx, dy in _RARMS[rarm]:
            cells[(g['ax'][1] + dx, g['ay'] + dy)] = '#'
    if s['larm'] == 'chin' and s['tap']:
        # 'catch': the claw tip drops onto the slipped lens; 'drop': the whole claw dips a row (chin tap)
        moves = [(3, 3)] if s['tap'] == 'catch' else [(1, 4), (2, 4), (3, 3), (0, 3)]
        new = {}
        for (x, y) in moves:
            new[(x, y + 1)] = cells[(x, y)]
            cells[(x, y)] = '#'
        if (0, 3) in moves:
            del cells[(0, 3)]                # the arm stub outside his body dips with it
        cells.update(new)
    return Pose(Sprite(cells=[(x, y, c) for (x, y), c in cells.items()], anchor=(0, 0), name='clawd'),
                p.anchors, dict(p.spec, rarm=rarm, tap=s['tap']))


def _clawd_full(s):
    f = Frame()
    put_clawd(f, _pose(s))
    return f


def specs(s):
    """The reading glasses alone.  Slipped (spec=1) they sit a row lower, the half-moon rims lightened to
    the frame's wood so they don't read as the gap between his legs on the dark theme.  A claw at his face
    is drawn in front of them by the clawd layer above (it catches them, pushes them up, taps), so this
    layer only changes when the glasses themselves move."""
    f = Frame()
    spr = _GLASSES.sprite(0)
    if s['spec']:
        low = max(y for _, y, _ in spr.cells)
        spr = Sprite(cells=[(x, y, 'T' if (y == low and c == 'd') else c) for x, y, c in spr.cells],
                     anchor=(spr.ax, spr.ay))
    wear(f, Item('reading_glasses', 'face', '', spr), _pose(s), dy=s['spec'])
    return f


# The pencil: 4 cells (pink eraser, 2 yellow, graphite tip).  At rest it stands upright beside his claw (all
# 4 show); in a reaching claw the eraser end is hidden in the fist, so 3 cells show.  The tip is the last
# cell.  Poses are hand-placed so the tip lands exactly where the story needs it.
def _line(x0, y0, dx, dy):
    n = max(abs(dx), abs(dy))
    return [(x0 + int(round(dx * i / float(n))), y0 + int(round(dy * i / float(n)))) for i in range(1, n + 1)]


def _pen(cells):
    return [(x, y, 'N' if i == len(cells) - 1 else 'y') for i, (x, y) in enumerate(cells)]


PEN = {
    'rest':   [(21, 16, 'p'), (21, 15, 'y'), (21, 14, 'y'), (21, 13, 'N')],   # rarm side: upright
    'lift':   [(21, 15, 'p'), (21, 14, 'y'), (21, 13, 'y'), (21, 12, 'N')],   # rarm up: raised with the claw
    # the handoff in-between: the 'wave' claw (tip (22,12), at the tray's left end) holds the eraser end and
    # the tip already rests in the tray (an even 2:1 slope); a frame later it lies flat in the tray
    'half':   [(23, 12, 'p'), (24, 12, 'y'), (25, 13, 'y'), (26, 13, 'N')],
    'tray':   [(23, 13, 'p'), (24, 13, 'y'), (25, 13, 'y'), (26, 13, 'N')],   # laid in the easel's tray
    # X marks the spot: the tip on each X cell in drawing order.  Clean lines only (45 deg, or 1:2 / 2:1 with
    # even runs counting the cell hidden in his fist): during '/' the pencil keeps its 45 deg angle and slides
    # down its own axis as the arm draws back (wave -> raise -> up), the tip tracing the stroke
    's1a':    _pen(_line(22, 12, 3, -3)),         # wave:  tip on TR (25,9)
    's1b':    _pen(_line(21, 13, 3, -3)),         # raise: tip on C  (24,10)
    's1c':    _pen(_line(20, 14, 3, -3)),         # up:    tip on BL (23,11)
    's2a':    _pen(_line(22, 12, 1, -3)),         # wave:  tip on TL (23,9)
    's2b':    _pen(_line(21, 13, 3, -3)),         # raise: tip on C
    's2c':    _pen(_line(22, 12, 3, -1)),         # wave:  tip on BR (25,11), clear of the tray
}
PEN_TIP = {'s1a': TR, 's1b': C_, 's1c': BL, 's2a': TL, 's2b': C_, 's2c': BR}


def pencil(s):
    f = Frame()
    for x, y in INK[PEN_INK.get(s['pen'], 'none')]:   # the strokes so far, under the pencil
        f.put(x, y, 'r')
    for x, y, ch in PEN[s['pen']]:
        f.put(x, y, ch)
    return f


# --------------------------------------------------------------------------------------------
# the story
# --------------------------------------------------------------------------------------------
STUDY = 'look_r'            # level gaze at the easel: the side arm sits beside the edge-column eye
HOP_EYES = ['look_u', 'look_u', STUDY, STUDY]    # up along the top, then down the side


def story():
    S = []
    cur = dict(eyes=STUDY, larm='side', rarm='side', tap=None, spec=0, pen='rest', ink='full', curl=None,
               fx=None, globe=0, route='old')

    def add(ms, **kw):
        kw.setdefault('tap', None)
        cur.update(kw)
        S.append(dict(cur, ms=ms))

    def hold_until(t, **kw):                              # a calm hold that ends exactly at time t
        add(t - sum(b['ms'] for b in S), **kw)

    # ---------------- STORY A: the thinker ----------------
    add(2600)                                             # frame 0: studying the plan
    add(120, eyes='blink')
    add(1100, eyes=STUDY)
    # "mm-hm", "mm-hm": on the first dip the glasses slip
    add(150, eyes='look_dr', spec=1)                      # the glasses slip down his nose ...
    add(130, eyes=STUDY)                                  # ... and stay there
    add(150, eyes='look_dr')
    add(520, eyes=STUDY)
    # he peers at you over the slipped glasses
    add(900, eyes='open')
    add(110, eyes='blink')
    add(650, eyes='open')
    # catches the lens, pushes claw + glasses up together, thinks; a chin tap
    add(80, larm='front', eyes='look_u')
    add(140, larm='chin', tap='catch')
    add(700, spec=0)
    add(130, tap='drop')                                  # a chin tap
    add(930)
    add(80, larm='front')                                 # the claw comes down through an in-between
    add(1200, larm='side')                                # still thinking
    add(520, eyes='look_l')                               # ... the globe
    # flicks the globe half a turn: wind-up, contact, follow-through; 1-column steps that slow down
    add(110, larm='up')
    add(80, larm='point', globe=1)
    add(70, larm='out', globe=2)
    add(95, larm='up', globe=3)
    add(135, globe=4)
    add(200, globe=5)                                     # the slowest step: it eases to a stop ...
    add(400, globe=HALF)                                  # ... on its other side
    add(110, larm='side', eyes='blink')
    hold_until(STORY, eyes=STUDY)                         # back to work: a long calm study

    # ---------------- STORY B: the planner ----------------
    add(1100)
    add(120, eyes='blink')
    hold_until(STORY + 1820, eyes=STUDY)
    # a fresh page
    add(90, rarm='up', pen='lift')                        # raises the pencil
    add(110, rarm='wave', pen='half')                     # lays it half into the tray: the tip touches first
    add(160, pen='tray')                                  # lets go; the claw is on the page's bottom corner
    add(150, rarm='lift1', curl=1, eyes='look_u')         # lifts it: the edge follows the claw tip ...
    add(120, rarm='lift2', curl=2)                        # ... to full reach,
    add(70, curl=3)                                       # lets go: the page sails up while the arm holds its
    add(70, curl=4)                                       # full reach (the follow-through) ...
    add(100, rarm='raise', curl='flap', route='gone', ink='none')   # over the clip bar, where it hangs a beat;
    add(200, rarm='up')                                   # ... the arm relaxes down the same arc
    add(100, rarm='side', curl='s1', eyes=STUDY)          # ... and drops behind; the corner settles
    add(100, curl='s2')
    add(1000, curl=None)                                  # a blank page
    add(700, eyes='look_u')                               # where to?
    # the route draws itself, hop by hop, while his eyes trace it: he is plotting it in his head
    for k, (ms, eyes) in enumerate(zip(HOP_MS, HOP_EYES)):
        add(ms, route=k + 1, eyes=eyes)
    add(500)                                              # he regards it
    add(110, eyes='blink')
    add(400, eyes=STUDY)
    # X marks the spot
    add(80, rarm='out')                                   # reaches for the tray
    add(110, rarm='wave', pen='half')                     # lifts the pencil by its end, tip still on the tray
    add(130, pen='s1a')                                   # pencil down on the top-right
    add(110, rarm='raise', pen='s1b')                     # (the ink appears behind the tip)
    add(110, rarm='up', pen='s1c')
    add(140, rarm='wave', pen='s2a')                      # lift, down on the top-left
    add(110, rarm='raise', pen='s2b')
    add(170, rarm='wave', pen='s2c')                      # ... a press on the last cell
    add(80, rarm='up', pen='lift', ink='full', fx=2)      # the pencil comes back up (in-between): the X is
    add(90, rarm='side', pen='rest')                      # done and glints gold, then its centre, then red
    add(110, fx=0)
    hold_until(STORY + 11590, fx=None)                    # calm study
    add(110, eyes='blink')
    hold_until(LOOP, eyes=STUDY)                          # across the seam into story A
    return S


# --------------------------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------------------------
def _moving(px, cover, still):
    """The cells one animated Clawd frame must draw over the static layer and the glasses."""
    return {k: v for k, v in px.items()
            if (k in cover and v == '@') or (k not in cover and still.get(k) != v)}


def _bytes(cells):
    """Rough SVG cost of a frame's cells: a path per colour plus one rect per horizontal run."""
    runs = sum(1 for (x, y), v in cells.items() if cells.get((x - 1, y)) != v)
    return 60 * len(set(cells.values())) + 15 * runs


def _split(frames, covers):
    """Clawd as two layers around his glasses: cells drawn in every frame go into a one-frame static layer,
    under the glasses; each animated frame, above the glasses, only carries the cells that differ from it,
    minus the cells the glasses cover in that frame (a claw '@' in front of the glasses stays).  Each static
    cell takes the colour that makes the animated frames cheapest (his usual study eyes are static ink, so a
    study frame doesn't redraw them).  The composite is exactly Clawd, then his glasses, then any claw in
    front of them (asserted); the SVG is much smaller and the glasses layer only changes when they move."""
    keys = None
    for f, _ in frames:
        keys = set(f.px) if keys is None else keys & set(f.px)
    distinct = []                            # what the SVG stores: runs of identical frames merge
    for (f, _), cover in zip(frames, covers):
        if not distinct or distinct[-1] != (f.px, cover.px):
            distinct.append((f.px, cover.px))
    still = {}
    for k in sorted(keys or ()):             # start from the most common colour ...
        count = {}
        for px, _ in distinct:
            count[px[k]] = count.get(px[k], 0) + 1
        still[k] = max(sorted(count), key=lambda c: count[c])

    def total():
        return sum(_bytes(_moving(px, cover, still)) for px, cover in distinct)
    best = total()
    colours = {k: sorted({px[k] for px, _ in distinct}) for k in sorted(keys or ())}
    mixed = [k for k, cs in colours.items() if len(cs) > 1]
    moves = [(k,) for k in mixed] + [(a, b) for i, a in enumerate(mixed) for b in mixed[i + 1:]]
    for ks in moves:                         # ... then let mixed cells (one, or a pair such as his two
        for c in colours[ks[0]]:             # eyes) take the colour that makes the frames cheapest
            if c in still[ks[0]] or any(c not in colours[k] or still[k] == c for k in ks):
                continue
            old = [still[k] for k in ks]
            for k in ks:
                still[k] = c
            t = total()
            if t < best:
                best = t
            else:
                for k, v in zip(ks, old):
                    still[k] = v
    still = Frame(still)
    moving = []
    for (f, ms), cover in zip(frames, covers):
        g = Frame(_moving(f.px, cover.px, still.px))
        g.meta = f.meta
        want = f.over(cover).over(Frame({k: '@' for k in cover.px if f.px.get(k) == '@'}))
        assert still.over(cover).over(g).px == want.px
        moving.append((g, ms))
    still.meta = frames[0][0].meta
    return still, moving


def _check(S):
    """Guard rails: (1) an eye in his edge column always has that side's arm beside it (his eyes are black
    ink: at his edge one would melt into the dark theme and read as a notch bitten out of his head); (2)
    while the page lifts, the claw tip is on its lifted edge; (3) the pencil tip lands on each X cell as it
    is drawn; (4) the routes stay clear of the X and the sheet's frame line; (5) the loop is exactly LOOP ms
    and story B starts at STORY."""
    hx, hy = HOME
    for s in S:
        px = _clawd_full(s).px
        for y in range(hy, hy + 6):
            for x in (hx + 1, hx + 9):
                if px.get((x, y)) not in ('#', '@'):
                    out = x - 1 if x == hx + 1 else x + 1
                    assert (out, y) in px, 'eye at (%d,%d) touches the background: %s' % (
                        x, y, (s['eyes'], s['larm'], s['rarm']))
        if s['curl'] in (1, 2):
            g = GEOM['normal']
            dx, dy = _RARMS[s['rarm']][-1]
            tip = (hx + g['ax'][1] + dx, hy + g['ay'] + dy)
            assert tip[1] == CURL[s['curl']][0] and SX0 <= tip[0] <= SX1, ('claw off the edge', s['curl'], tip)
    for k, tip in PEN_TIP.items():
        assert PEN[k][-1][:2] == tip, k
    xs = set(INK['full'])
    for r in ROUTES:
        assert len(r) == HOPS[-1]
        for (x, y), _ in r:
            assert SX0 < x < SX1 and SY0 < y < SY1 and (x, y) not in xs, (x, y)
    assert sum(s['ms'] for s in S) == LOOP
    t = 0
    for s in S:
        if t == STORY:
            break
        t += s['ms']
    assert t == STORY


def _route_frame(c, r):
    """Clawd cycle c (0 or 1) starts with ROUTES[c] on the easel; its fresh page gets the other route."""
    old, new = ROUTES[c], ROUTES[1 - c]
    if r == 'old':
        return route(old)
    if r == 'gone':
        return Frame()
    return route(new[:HOPS[r - 1]])


def build():
    S = story()
    _check(S)
    per = lambda fn: [(fn(s), s['ms']) for s in S]
    scene = _easel().over(_globe_stand()).over(globe(0))
    base = globe(0).px

    def spin(k):                             # only the cells that differ from the scene's globe
        g = globe(k % SPIN)
        return Frame({c: v for c, v in g.px.items() if base.get(c) != v})

    # two Clawd cycles: the first flick turns the globe to its far side, the second brings it home; the
    # first fresh page gets route 2, the second route 1 again
    rounds = [(spin(c * HALF + s['globe']), s['ms']) for c in (0, 1) for s in S]
    routes = [(_route_frame(c, s['route']), s['ms']) for c in (0, 1) for s in S]
    still, moving = _split(per(_clawd_full), [specs(s) for s in S])
    hat = Frame()
    wear(hat, _HAT, clawd())
    # ambient: a glint runs down the brass meridian now and then, on its own co-prime loop
    glint = [(Frame().put(x, y, 'y'), 90) for x, y in MERIDIAN[1:5]]
    glint.append((Frame(), 7310 - 90 * len(glint)))
    return anim(NAME, DESC, [
        static('scene', scene),
        layer('globe', rounds),
        layer('route', routes),
        layer('ink', per(ink)),
        layer('pencil', per(pencil)),                     # under Clawd: his claw covers the end he holds
        static('clawd-static', still),
        layer('specs', per(specs)),                       # between: claws at his face are drawn in front
        layer('clawd', moving),
        static('hat', hat),
        layer('glint', glint),
    ], state=STATE)
