# ======================================================================================
# USER FEEDBACK: the user reviewed this fine-face upgrade draft personally and approved it
# ("looks great go"). Keep the scene, beats and fine-line expressions; critics, fixers and judges
# should polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""typing - you are typing in the input box below him; Clawd, cub reporter, takes down your story.

Storyboard (one shared 9000 ms timeline drives every layer that follows him; times in ms). His face
acts in fine-line half-size pixels (STYLE.md 0b) in every beat; gaze = half-step offsets (below).
    0  HOME, head bowed over your text (his gray press fedora tipped forward), eyes down on your line
       (look d). A PRESS card (a white tab over a line of print) stands in the hat's navy band, a pencil
       is tucked in it at the left; his yellow legal pad (last note on it) stands at his left, a small
       to-go coffee at his right.
  590  reading along: his eyes follow your caret right (half-step, dr); 1150 a smooth fine blink
       (half > line > half, 220 ms) ..
 1560  .. return sweep to the start of the next line (dl), then on along it (d, 1980)
 2290  leans in: both arms drop, eyes on your words; 2480 they dart to a word (dr) and 2590 narrow at
       it for a beat (half lids, 80 ms: a quick focus, never held long enough to look drowsy): the
       anticipation for ..
 2670  .. "ooh!": his head comes up (hat level), WIDE eyes on you (a taller eye). The eyes lead: they
       hold 190 ms before the hat leaves; 2860 the hat hops a cell and the pencil's tip gleams (a gold
       glint dot, then a plus, one cell beyond the tip); wide 410 ms in all. 3080 the hat lands tipped
       forward (its brim presses his eyes back to round; the glint trails off as a dot, dropping with
       the tip) and settles level (3160): sparkle eyes, the idea has landed (330 ms) .. 3490 a glance up
       at the pencil in the band (ul) ..
 3580  .. reaches up: his hand goes behind the brim to the band and the pencil slides out one diagonal
       line at a time (3580 hand at the band, 3700 pulled out up-left; his eyes on it, ul), 3800 the arm
       lands and the pencil finishes turning a beat later, 3880 level on the way down to the pad (l)
 3990  flicks the page over the binding with the tip: catch + lift (eyes dl), 4090 back view (l),
       4190 upright (220 ms, ul), 4410 back view falling (l), 4520 a sliver, gone: his eyes ride the
       page up and back down in half-steps; the pencil is always the same 4 cells
 4620  poised over the fresh page, he checks your text once more (d, 200 ms) ..
 4820  .. and jots line 1, the arm travelling along it (point -> out -> side, uneven 170-190 ms
       strokes) while his eyes ride your line to the right (d, d, dr, dr), 5370 a lifted pause: a quick
       glance at his note (dl, 250 ms), 5620 line 2; the graphite appears under the tip, his eyes back
       on your text. The note he writes is exactly frame 0's page: seamless loop.
 5950  lifts the pencil off the page (level along the binding, eyes on it: l), 6020 raises it level,
       6100 the arm leads and the pencil turns up a beat later, 6180 raised, 6260 pushes it back into
       the band one line at a time (6260 / 6350), his hand stays a beat behind the brim; his eyes follow
       it up (l, ul, u). Every pencil step is 1-3 cells; only the deliberate catch-and-flick of the page
       (3990 / 4090) snaps 4.
 6470  "noted!": a pleased look at you, the lids ease down (half) into thin happy arcs (400 ms) and
       back up (half)
 6990  reads on (dl, 7240 d) .. 7450 the lids ease down into content cups, and the "mm-hm" double nod
       (7510 / 7780: the hat tips forward and the cups dip half a cell with it; his body never changes
       size), the cups held 540 ms .. 8050 eyes open (half), on along your line: d (8120), dr (8370),
       return sweep dl (8700), which flows straight into frame 0's d: dl > d > dr across the seam
Hat: tipped forward = head bowed toward your text (frame 0, the close reading, the lean, the nods, the
landing); level = head up (eye contact, pencil work). Eye closures: the blink at 1.15 s, "noted!" at
6.47 s and the content nod at 7.45 s (uneven on purpose); the quick squint at 2.59 s sets up "ooh!".
Face (STYLE.md 0b): fine-line expressions only (the kit's fine_face: open, half, line, wide, sparkle,
happy, content), no mouth, no blush, never resized. Gaze = the kit's half-step look_* idea extended to
the diagonals: the expression's pixels shifted by half a cell (c at you, d your text, dl / dr the start
and end of your line, l / ul / u the pencil, the pad and the page). Guards: every eye pixel sits on his
face, never touches the background, and never hides under the hat (asserted per beat).
Ambient layers, independent of the story (co-prime lengths, so the mix keeps changing for minutes):
  steam    the to-go cup breathes: a thin wisp from the sip hole, a rest, a wisp leaning the other
           way, a longer rest (4840 ms; with the 9000 ms story it repeats only every ~18 min)
  twinkle  a tiny silver "listening" twinkle beside his head, then higher up on the next visit
           (uneven gaps of 10.9 / 11.8 s on a 22.7 s loop; the first at 5.28 s, as he checks his note).
           Silver with a white core, so the gold glint stays the "ooh!" moment's alone.
Layers that follow Clawd (notes, clawd-static + clawd, face, hat, band) are built from ONE beat list, so
their frame boundaries are identical and they can never drift apart; the split keeps the SVG small
(only the parts that change get new frames: his body has a solid face, the face layer holds only the
fine eye ink). The pad and the cup are one static layer.
SVG size: the built file is ~39 KB (svgwriter.mjs, under the 40 KB target); lint's estimate reads
~43 KB because it charges 60 bytes per color per frame, more than the real <path> costs. Most of the
bytes are the acting itself: 39 face frames (eye ink only) and 25 arm + pencil frames.
User taste (STYLE.md section 0): normal body size only, plain face + the 0b fine-line expressions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'typing'
STATE = 'You are typing in the input box below him'
DESC = ('Reporter Clawd in a press fedora reads along as you type (his eyes track your line in half-steps), '
        'goes wide-eyed "ooh!" at a good bit and jots it on his legal pad, smiles "noted!" and nods "mm-hm" '
        'with content eyes; his to-go coffee steams beside him.')

LOOP = 9000

# ------------------------------------------------------------------ local sprites
# Press fedora (gray-blue felt, navy band), anchored on his head-top pixel: the brim overlaps his top
# row, pinched crown lit from the top-left. A PRESS card stands in the band at the right and rises above
# the crown: a white tab with a graphite line of print under it, held by a gray contour (top and right)
# and the crown, so it reads as a card on the light theme and does not glare on the dark one (the eyes
# stay the brightest read on his face). Gray-blue + navy + white card: nothing like plan's brown fedora.
_FEDORA = Item('_press_fedora', 'head', 'Gray press fedora with a navy band and a PRESS card', Sprite([
    '.......NN..',
    '...ms.sWWN.',
    '..mssssnnN.',
    '..sBBBBBBs.',
    'mssssssssss',
], anchor=(5, 4)))
# The same hat tipped forward (head bowed: reading closely, the nods, the landing): the crown drops one
# row, the brim's ends stay on his top row and its front droops over his forehead (row 13). His top row
# stays covered from edge to edge (no orange nubs beside the crown); the face guard keeps every eye
# pixel below it (rows 14+), so it is never combined with an upward glance or wide eyes.
_FEDORA_TIP = Item('_press_fedora_tip', 'head', 'Press fedora tipped forward', Sprite([
    '.......NN..',
    '...ms.sWWN.',
    '..mssssnnN.',
    'mssBBBBBBss',
    '..sssssss..',
], anchor=(5, 3)))
_HAT = {'n': (_FEDORA, 0), 'up': (_FEDORA, -1), 'tip': (_FEDORA_TIP, 0)}

# The pencil: ONE fixed design everywhere, a plain reporter's pencil (no eraser). Four cells from his
# grip to the tip: gold stick (its end in his fist), dark-gold sharpened wood, gray graphite tip (gold
# reads on both themes and against the gray hat; the dark cells give it contrast on the yellow page).
_PENCIL = ('j', 'j', 'J', 'N')
# Tucked in the hat band at the left: its end hides in the band, the rest sticks out up-left at 45
# degrees (canvas cells for the hat at rest). It hops with the hat; when the hat tips forward it stays
# put (it sits on the hat's left side, on the tilt axis), so it never overlaps the hat (asserted). In
# his hand it leaves the band one diagonal line at a time:
# y = x (band) -> y = x + 1 (hand at the band) -> y = x + 2 (pulled out).
_BAND = [(11, 11, 'j'), (10, 10, 'J'), (9, 9, 'N')]
_BAND_DY = {'n': 0, 'up': -1, 'tip': 0}


def _glint_at(hat):
    """The "ooh!" glint sits one cell beyond the band pencil's tip, so it rides the tip as the hat moves."""
    return (8, 8 + _BAND_DY[hat])


# Yellow legal pad standing at his left: red glued binding on top, cardboard back lit from the top-left
# (tan left edge, wood right edge and bottom right). Columns 3..8 (a 1-cell gap before his arm), rows
# 15..19. Anchor (0, 0) = its top-left cell, so pad-local cells place directly.
_PX, _PY = 3, 15
_PAD = Sprite([
    'rrrrrR',
    'tYYYYT',
    'tYYYYT',
    'tYYYYT',
    'tttTTT',
], anchor=(0, 0), name='_legal_pad')
# The note in writing order (pad-local): line 1 at (4..6, 16), line 2 at (6..7, 18). Every cell is
# exactly 3 cells (Chebyshev) from a kit hand, so the 4-cell pencil reaches it without stretching.
_NOTE = [(1, 1), (2, 1), (3, 1), (3, 3), (4, 3)]
_PAGE_UP = ['.tttt.', 'tYYYYt', 'tYYYYt', 'tYYYYt']        # the flipped page standing above the binding


def _notes(marks=5, page=None, **_):
    """Overlay on the pad (pad-local cells). marks = note cells written on the visible page.
    page = flip phase, the old page turning over the top binding toward you and behind the pad:
      'lift'   its bottom edge lifted to the middle of the pad (its first line still showing)
      'back'   above the binding, foreshortened (2 rows): we see its plain back
      'up'     standing straight up above the binding (4 rows)
      'sliver' edge-on, going down behind the pad (1 row)"""
    cells = {}
    if page == 'lift':
        marks = 3                                   # the old page's first line, still on the lifting page
        for x in range(6):
            cells[(x, 2)] = 't'                     # the lifted page's bottom edge, halfway up the pad
    elif page:
        marks = 0                                   # the fresh page below is blank
    for x, y in _NOTE[:marks]:
        cells[(x, y)] = 'N'                         # pencil graphite
    if page in ('up', 'back'):
        rows = _PAGE_UP if page == 'up' else _PAGE_UP[:2]
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch != '.':
                    cells[(x, y - len(rows))] = ch
    elif page == 'sliver':
        for x in range(1, 5):
            cells[(x, -1)] = 't'
    f = Frame()
    if cells:
        f.place(Sprite(cells=[(x, y, ch) for (x, y), ch in cells.items()], anchor=(0, 0), name='_notes'),
                _PX, _PY)
    return f


def _pencil_cells(grip, tip):
    """The 4-cell pencil from his grip (its end in his fist) to its tip, on the kit's Bresenham line.
    Every tip in the beat list sits exactly 3 cells (Chebyshev) from the grip, so the stick never
    changes length."""
    pts = list(Frame().line(grip[0], grip[1], tip[0], tip[1], 'j').px)    # drawn (and kept) in order
    if len(pts) != len(_PENCIL) or pts[0] != grip or pts[-1] != tip:
        raise ValueError('pencil %s -> %s is %d cells, not %d' % (grip, tip, len(pts), len(_PENCIL)))
    return [(px, py, ch) for (px, py), ch in zip(pts, _PENCIL)]


# Coffee to go, the library's 'coffee_togo' look (kraft cup, wood sleeve with an orange logo, silver
# sip lid overhanging evenly) one body row shorter, so it stays a cup next to him (6 rows; his body is
# 8) and stands on the input box. Top-left at (24, 14); the sip spout is (25..26, 14).
_CUP = Sprite([
    '.NN...',
    'mmmmmN',
    '.tttT.',
    '.ToTT.',
    '.TTTT.',
    '.tttT.',
], anchor=(0, 0), name='_coffee_togo_small')
_CUP_AT = (24, 14)


# Steam from the sip hole: a thin wisp that is born at the spout, curls up and thins out at the top,
# then a rest. Two wisps per cycle lean opposite ways; the rests differ (the cup "breathes").
def _wisp(path):
    n = len(path)
    steps = [path[:k + 1] for k in range(3)]                       # born: 1, 2, 3 cells
    steps += [path[k - 2:k + 1] for k in range(3, n)]               # rises (3 cells)
    steps += [path[n - 2:], path[n - 1:]]                           # thins out at the top
    return steps


_WISP_A = _wisp([(26, 13), (26, 12), (27, 11), (27, 10), (26, 9)])
_WISP_B = _wisp([(26, 13), (26, 12), (25, 11), (25, 10), (26, 9)])
_WISP_A_MS = (210, 220, 230, 240, 230, 220, 210)
_WISP_B_MS = (220, 230, 220, 250, 240, 230, 200)
_REST_A, _REST_B = 640, 1050                                        # cycle 4840 ms

# The listening twinkle: two spots to the right of his head (beside it, then higher up), one per visit;
# each visit is dot / plus / dot (310 ms). The gaps are uneven (10.9 s, 11.8 s); the loop is 22.7 s.
# Silver with a white core (the library glint recolored): calm, on-palette with the hat and the steam,
# and never mistaken for the gold "ooh!" glint at the pencil, which is the story's alone. The first
# visit lands as he checks his fresh note (5.28 s: a "nice note" twinkle), away from the "ooh!".
_TWINKLES = [((22, 9), 5280), ((24, 5), 10590)]                   # (spot, wait before it)
_TWINKLE_LOOP = 22700


def _silver(spr):
    """The library glint in silver: every pixel silver ('m', a mid-tone that reads on both themes), and
    a pixel enclosed by the glint on all four sides (the plus's core) white. Shape-based, so it stays a
    silver twinkle with a white core whatever colors the library glint is drawn in."""
    on = {(x, y) for x, y, _ in spr.cells}
    return Sprite(cells=[(x, y, 'W' if {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)} <= on else 'm')
                         for x, y, _ in spr.cells], anchor=(spr.ax, spr.ay), name=spr.name)


# ------------------------------------------------------------------ his face (fine-line, STYLE.md 0b)
# Gaze: half-step offsets in fine (half-cell) pixels, the kit's fine look_* (subtler than the kit's
# full-cell look_*) extended to the diagonals. The whole expression shifts, so a blink or the content
# cups close over the eyes exactly where they are looking.
_GAZE = {
    'c': (0, 0),        # at you: the official eye
    'd': (0, 1),        # your text in the input box below him (the kit's fine look_d)
    'dl': (-1, 1),      # the start of your line; the pad
    'dr': (1, 1),       # your caret, moving right
    'l': (-1, 0),       # the pencil held level beside him, the page over the binding
    'ul': (-1, -1),     # the pencil in the hat band (up-left), the page standing up
    'u': (0, -1),       # the hat band (the kit's fine look_u)
}
_BODY = set('#@%')


# ------------------------------------------------------------------ per-beat frames
def _pose(larm='side', rarm='side', **_):
    """His body with a solid face: the fine face layer draws his eyes in every beat."""
    return clawd(eyes='blink', larm=larm, rarm=rarm)


def _face_frame(expr='open', look='d', **kw):
    """His eyes as a fine (half-size pixel) overlay on his solid face: the kit's fine_face expression,
    shifted by the half-step gaze. Only the ink (and the sparkle's glint) pixels: one color, a few runs.
    Guards: every pixel lies on his face (not on an arm or the pencil), never touches the background
    (no notch at his edge), and is never covered by the hat in this beat."""
    p = _pose(**kw)
    f = Frame()
    put_clawd(f, p)
    base = fine(f)
    ff = fine_face(base.copy(), p, expr=expr)
    dx, dy = _GAZE[look]
    ink = {(x + dx, y + dy): v for (x, y), v in ff.px.items() if base.px.get((x, y)) != v}
    body = fine(_clawd_frame(**kw)).px
    hat = fine(_hat_frame(**kw)).px
    x0, y0 = HOME
    for (x, y) in ink:
        if body.get((x, y)) != '#' or not (2 * (x0 + 1) <= x < 2 * (x0 + 10) and 2 * y0 <= y < 2 * (y0 + 6)):
            raise ValueError('eye pixel (%d,%d) is off his face: %s %s %r' % (x, y, expr, look, kw))
        if (x, y) in hat:
            raise ValueError('eye pixel (%d,%d) hides under the hat: %s %s %r' % (x, y, expr, look, kw))
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n not in ink and body.get(n) not in _BODY:
                raise ValueError('eye pixel (%d,%d) touches the background: %s %s %r' % (x, y, expr, look, kw))
    g = Frame(ink, res=2)
    g.meta = {'fine_face': [(expr, expr)], 'gaze': look}
    return g


def _clawd_frame(**kw):
    """Clawd plus the pencil when it is in his hand: one frame per beat, drawn under the hat."""
    f = Frame()
    put_clawd(f, _pose(**kw))
    pen = kw.get('pen', 'band')
    if pen != 'band':
        for x, y, ch in _pencil_cells(_pose(**kw).at('hand_l'), pen):
            f.put(x, y, ch)
    return f


def _hat_frame(hat='n', **kw):
    f = Frame()
    item, dy = _HAT[hat]
    wear(f, item, _pose(**kw), dy=dy)
    return f


def _band_frame(pen='band', hat='n', spark=None, **kw):
    """The pencil while it is tucked in the band (it hops with the hat) plus the "ooh!" glint one cell
    beyond its tip. Its own small layer: it only changes at the hop, the grab and the tuck. Neither it
    nor the hand pencil ever overlaps the hat (asserted), so their layers can sit anywhere."""
    f = Frame()
    if pen == 'band':
        for x, y, ch in _BAND:
            f.put(x, y + _BAND_DY[hat], ch)
    if spark is not None:
        if pen != 'band':
            raise ValueError('the glint belongs to the band pencil')
        f.place(get('sparkle_small').sprite(spark), *_glint_at(hat))
    hat_px = _hat_frame(hat=hat, **kw).px
    hand = _clawd_frame(hat=hat, pen=pen, **kw).px if pen != 'band' else {}
    clash = (set(f.px) | {k for k, c in hand.items() if c in _PENCIL}) & set(hat_px)
    if clash:
        raise ValueError('pencil/glint under the hat at %s' % sorted(clash))
    return f


def _split(frames):
    """Clawd as two layers: the cells every beat shares (his body with its solid face, legs, the arm
    cell that never moves) go into a one-frame static layer; each beat's frame only carries what differs
    (the arms, the pencil). The composite is exactly the full frame (asserted); the SVG is much smaller."""
    keys = None
    for f, _ in frames:
        keys = set(f.px) if keys is None else keys & set(f.px)
    still = Frame()
    for k in sorted(keys):
        colors = sorted({f.px[k] for f, _ in frames})
        if len(colors) == 1:
            still.px[k] = colors[0]
    moving = []
    for f, ms in frames:
        g = Frame({k: v for k, v in f.px.items() if still.px.get(k) != v})
        g.meta = f.meta
        assert still.over(g).px == f.px
        moving.append((g, ms))
    still.meta = frames[0][0].meta
    return still, moving


def _beats():
    """One shared timeline: (body kwargs, notes kwargs, ms). Face: expr = a FINE_EYES expression
    (default 'open'), look = a _GAZE key (default 'd', on your text)."""
    B = []

    def add(ms, pd=None, **kw):
        B.append((kw, pd or {}, ms))

    # reading closely, head bowed: eyes follow your caret right, a smooth blink, return sweep, on along it
    add(590, look='d', hat='tip')
    add(560, look='dr', hat='tip')
    add(60, expr='half', look='dr', hat='tip')
    add(100, expr='line', look='dr', hat='tip')
    add(60, expr='half', look='dr', hat='tip')
    add(190, look='dr', hat='tip')
    add(420, look='dl', hat='tip')               # return sweep: new line
    add(310, look='d', hat='tip')
    # leans in: both arms drop, eyes on your words .. they dart to a word and narrow, a quick focus
    # (the anticipation; never held long enough to read as sleepy)
    add(190, look='d', hat='tip', larm='down', rarm='down')
    add(110, look='dr', hat='tip', larm='down', rarm='down')
    add(80, expr='half', look='dr', hat='tip', larm='down', rarm='down')
    # "ooh!": head up, wide eyes on you (they lead: held before the hat leaves), then the hat hops a
    # cell (glint), lands tipped (the glint trails off with the tip) and settles level
    add(190, expr='wide', look='c', larm='down', rarm='down')
    add(100, expr='wide', look='c', hat='up', spark=0)
    add(120, expr='wide', look='c', hat='up', spark=1)
    add(80, look='c', hat='tip', spark=0)        # lands tipped forward: the brim presses the eyes round
    add(330, expr='sparkle', look='c')           # settles level: the idea has landed
    add(90, look='ul')                           # a glance up at the pencil in the band before the reach
    # pulls the pencil from the band: hand at the band (behind the brim), out up-left, the arm lands and
    # the pencil finishes turning a beat later, level on the way down
    add(120, look='ul', larm='high', pen=(7, 8))
    add(100, look='ul', larm='raise', pen=(6, 8))
    add(80, look='ul', larm='up', pen=(6, 11))
    add(110, look='l', larm='up', pen=(6, 13))
    # flicks the page over the binding with the tip; his eyes ride the page up and down
    add(100, pd={'page': 'lift'}, look='dl', larm='side', pen=(6, 17))
    add(100, pd={'page': 'back'}, look='l', larm='up', pen=(6, 13))
    add(220, pd={'page': 'up'}, look='ul', larm='up', pen=(6, 11))
    add(110, pd={'page': 'back'}, look='l', larm='up', pen=(6, 13))
    add(100, pd={'page': 'sliver'}, look='l', larm='up', pen=(6, 14))
    # poised over the fresh page, he checks your text once more ...
    add(200, pd={'marks': 0}, larm='up', pen=(6, 14))
    # ... and jots line 1 (the arm travels along it while his eyes ride your line to the right), a lifted
    # pause with a glance at his note, line 2
    add(190, pd={'marks': 1}, larm='point', pen=(4, 16))
    add(170, pd={'marks': 2}, look='dr', larm='out', pen=(5, 16))
    add(190, pd={'marks': 3}, look='dr', larm='side', pen=(6, 16))
    add(250, pd={'marks': 3}, look='dl', larm='side', pen=(6, 17))
    add(180, pd={'marks': 4}, larm='side', pen=(6, 18))
    add(150, pd={'marks': 5}, larm='side', pen=(7, 18))
    add(70, look='l', larm='side', pen=(6, 15))  # lifts it off the page: level along the binding
    # tucks it back: level, raised (the pencil turns a beat after the arm), pushed into the band one line
    # at a time, his hand stays a beat
    add(80, look='l', larm='up', pen=(6, 13))
    add(80, look='ul', larm='up', pen=(6, 11))
    add(80, look='ul', larm='raise', pen=(6, 8))
    add(90, look='ul', larm='high', pen=(7, 8))
    add(120, look='u', larm='high')
    # "noted!": a pleased look at you, the lids ease into thin happy arcs and back
    add(60, expr='half', look='u')
    add(400, expr='happy', look='c')
    add(60, expr='half', look='c')
    # reads on; "mm-hm" double nod with content cups that dip with the hat; eyes open, on along the line
    add(250, look='dl')
    add(210, look='d')
    add(60, expr='half', look='d')
    add(140, expr='content', look='d', hat='tip')
    add(130, expr='content', look='c')
    add(140, expr='content', look='d', hat='tip')
    add(130, expr='content', look='d', hat='tip')
    add(70, expr='half', look='d', hat='tip')
    add(250, look='d', hat='tip')
    add(330, look='dr', hat='tip')
    add(0, look='dl', hat='tip')                 # return sweep (new line) -> frame 0; fills to LOOP ms
    total = sum(ms for _, _, ms in B)
    kw, pd, _ = B[-1]
    B[-1] = (kw, pd, LOOP - total)
    if B[-1][2] < 250:
        raise ValueError('story too long: the last beat only gets %d ms' % B[-1][2])
    return B


def _steam_layer():
    seq = [(c, ms) for c, ms in zip(_WISP_A, _WISP_A_MS)] + [(None, _REST_A)]
    seq += [(c, ms) for c, ms in zip(_WISP_B, _WISP_B_MS)] + [(None, _REST_B)]
    seq = seq[2:] + seq[:2]                      # frame 0: a full 3-cell wisp rising from the spout
    out = []
    for cells, ms in seq:
        f = Frame()
        for x, y in cells or ():
            f.put(x, y, 'm')
        out.append((f, ms))
    return layer('steam', out)


def _twinkle_layer():
    """Dot / plus / dot (310 ms) at each spot in turn, in silver. The first lands on his note check at
    5.28 s; later ones drift over the whole story (co-prime with it), so the mix keeps changing."""
    tw = get('sparkle_small')
    out = []
    for spot, wait in _TWINKLES:
        out.append((Frame(), wait))
        for i, ms in ((0, 90), (1, 130), (0, 90)):
            f = Frame()
            f.place(_silver(tw.sprite(i)), *spot)
            out.append((f, ms))
    out.append((Frame(), _TWINKLE_LOOP - total_ms(out)))
    return layer('twinkle', out)


def build():
    tracks = {'notes': [], 'clawd': [], 'face': [], 'hat': [], 'band': []}
    for kw, pd, ms in _beats():
        tracks['notes'].append((_notes(**pd), ms))
        tracks['clawd'].append((_clawd_frame(**kw), ms))
        tracks['face'].append((_face_frame(**kw), ms))
        tracks['hat'].append((_hat_frame(**kw), ms))
        tracks['band'].append((_band_frame(**kw), ms))
    still, moving = _split(tracks['clawd'])
    # static props: the legal pad at his left, the to-go coffee at his right
    scene = Frame()
    scene.place(_PAD, _PX, _PY)
    scene.place(_CUP, *_CUP_AT)
    return anim(NAME, DESC, [
        static('scene', scene),
        _steam_layer(),
        layer('notes', tracks['notes']),
        static('clawd-static', still),           # his body with a solid face, legs, the still arm cells
        layer('clawd', moving),                  # the arms, the pencil in his hand
        layer('face', tracks['face']),           # his eyes: fine-line expressions + half-step gaze
        layer('hat', tracks['hat']),
        layer('band', tracks['band']),           # the pencil tucked in the band + the "ooh!" glint
        _twinkle_layer(),
    ], state=STATE)
