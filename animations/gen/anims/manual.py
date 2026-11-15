"""manual - Default (manual) permission mode: Claude asks before every edit.

Pun: Clawd reads THE MANUAL.  A big, chunky violet instruction manual stands open at his left side (its
bottom board rests on the input box); his left claw holds the right page open at its outer edge.  The
manual's emblem, a gold cog, heads every page; Vol. 2 of the same manual stands at his right showing the
series cover (bold violet, big gold gear).  A little sprout grows on his head: the beginner's mark (he is new
here, so he asks about everything).  Plain face, normal body size throughout (STYLE.md section 0): the acting
is in his eyes and claws, the pages, the sprout and two tiny effects in the manual's own colours (a small
violet "?" when he asks, a green tick when you approve).

STORYBOARD (s)                 one story loop = 13.99 s; every synced layer is built from ONE beat list
  A  0.00  frame 0: reading the right page (eyes look_l), his claw holding the page open at its outer edge
     1.70  blink .. 2.32 a breath of air sways the sprout .. 3.02 eyes drift down the lines (3.26 the gear on
           Vol. 2 glints)
  B  3.82  his claw arcs up to step 1 (3.95), then runs down: step 2 (4.52), step 3 (4.99); eyes follow;
           quick 110-130 ms moves, uneven holds (460 / 360 / 700 ms: he lingers on step 3)
  C  5.69  looks up at you: "this one?" (650 ms) .. 6.34 blink .. 6.45 raises his free hand like a student
           (up > raise); 6.58 a small violet "?" rises out of his claw (2 frames) and hangs there, still
  D  7.30  nod, nod: eyes up and the claw lifts off step 3 (anticipation) .. 7.39 DOWN as one: eyes, sprout
           and claw (it taps step 3), held 200 ms .. 7.59 up: the claw lifts, the sprout lags, the hand
           starts down (at his side 7.68) .. 7.77 second nod: tap; the "?" loses its hook, its dot hops up,
           already green ..
     7.97  .. and blooms into a tick as he comes up: small > overshoot (8.06) > settle (8.19); the sprout
           swings right, left and rests (8.36): follow-through; his claw presses step 3 ..
     8.49  .. and it turns green in the book: a satisfied 0.96 s still, looking at you .. 9.45 eyes to the corner
  E  9.65  turns the page (eased): the claw lifts the corner (a grey curl), the page rises with its lit face
           (9.77, the cog and steps squeezed by perspective), stands up out of the gutter taller than the
           book (9.93: its corner arcs over), falls with its shaded back (9.99), lands with a bounce (10.14),
           settles (10.26); the tick shrinks away; the sticky tabs flip up in the draft; his eyes follow the
           page up and over; his claw goes back to holding the new page open (9.99)
  F 10.56  a calm read of the fresh page, hands still: from the top .. 11.16 down the lines .. 12.06 blink ..
    12.79  a glance at Vol. 2 waiting beside him .. blink-blink (13.31, 13.53: oh boy) .. 13.64 back to
           reading -> frame 0
Blinks / eye closures: 1.70, 6.34, 12.06, 13.31 + 13.53: uneven on purpose.
Long stills: 0-1.70 (2.05 s with the end of F), 8.49-9.45, 11.16-12.06.
Independent layers (co-prime with the story, so no two loops look alike):
  glint  7.68 s: now and then a pale glint twinkles on the gold gear of Vol. 2 (0-1-2-1-0; first at 3.26 s,
                 in the calm opening read)
  worm  29.30 s: a bookworm pokes out of Vol. 2's pages, inches along its top, rears up to watch him read,
                 turns and dives back in: its first visit rears up (12.73) just before Clawd glances over
                 (he seems to notice it).  Later in its loop it only peeks out and leans over to watch him;
                 the moment he glances over again (26.78 = 12.79 of the second story loop) it ducks back
                 in: whoops.  Its loop drifts 1.32 s against the story per pass, so later visits land on
                 different beats.
Static: Vol. 2 and the open book (one layer); the page turn and the tabs are thin additive overlays.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'manual'
STATE = 'Default (manual) permission mode: Claude asks before every edit'
DESC = ('Reads a chunky instruction manual: runs his claw down the steps, raises a hand to ask you "this one?", '
        'nods at your OK, ticks the step and turns the page; Vol. 2 (and its bookworm) waits beside him.')


def _item(name, fallback):
    try:
        return get(name)
    except KeyError:                         # library mid-save: a local copy of the same look
        return fallback


_SPROUT = _item('sprout', Item('sprout', 'head', 'local fallback', [
    Sprite(['ag.ga', '.gGg.', '..G..', '..G..'], anchor=(2, 3)),
    Sprite(['ag.ga', '.gGg.', '.G...', '.G...'], anchor=(1, 3)),
    Sprite(['ag.ga', '.gGg.', '..G..', '..G..'], anchor=(2, 3)),
    Sprite(['ag.ga', '.gGg.', '...G.', '...G.'], anchor=(3, 3)),
]))
_SPARKLE = _item('sparkle_small', Item('sparkle_small', 'fx', 'local fallback', [
    Sprite(['j'], anchor=(0, 0)), Sprite(['.j.', 'jyj', '.j.'], anchor=(1, 1)),
    Sprite(['j.j', '.j.', 'j.j'], anchor=(1, 1))]))
# the glint must be BRIGHTER than the gold gear it sits on: pale-yellow arms, white core
_GLINT = [s.recolor({'j': 'Y', 'y': 'W'}) for s in _SPARKLE.frames]

# the sprout with Clawd's head dipped in a nod (tipped toward us): derived from the live library sprite, so it
# always matches it: everything one row lower, the stem one cell shorter (nothing goes below his head-top)
_S0 = _SPROUT.sprite(0)
_SPROUT_DIP = Sprite(cells=[(x, y + 1, c) for x, y, c in _S0.cells if y + 1 <= _S0.ay], anchor=(_S0.ax, _S0.ay))

# small green tick (approved): pop tiny -> overshoot -> settle; anchored on its bottom point.  Deliberately
# smaller than the library's check_pop (8x5 settled), which is too loud for a long, calm mode state.
_TICK = [
    Sprite(['..g', 'g.g', '.g.'], anchor=(1, 2)),
    Sprite(['.....g', '....gG', '...gG.', 'g.gG..', '.gG...'], anchor=(1, 4)),
    Sprite(['....g', '...gG', 'g.gG.', '.gG..'], anchor=(1, 3)),
]

# the manual's emblem, a little gold cog (the same gold and violet hub as the big gear on Vol. 2's cover),
# lit from the top-left.  Anchor = its top-left cell.
_COG = Sprite(['yjj',
               'jVj',
               'jjJ'], anchor=(0, 0))
# the left page's figure: a blue part drawn as an IKEA-style diagram (cyan highlight top-left, navy shade
# bottom-right), with a paper margin so it reads as printed on the page.  Anchor = its top-left cell.
_FIG = Sprite(['cb',
               'bb',
               'bB'], anchor=(0, 0))

# --------------------------------------------------------------------------------------------
# The manual (standing open at his left).  Absolute canvas coordinates.
#   x 1 left board | x 2-4 left page | x 5 gutter | x 6-9 right page | x 10 right board (under his arm)
#   row 6 tabs | row 7 page tops | rows 8-16 pages | rows 17-18 page block | row 19 bottom board (on the
#   input box, like Clawd's feet and Vol. 2)
# --------------------------------------------------------------------------------------------
GUT = 5
LP = (2, 4)
RP = (6, 9)
TOP, PB = 7, 16
COG_AT = (7, 8)             # the emblem heads the right page (top-left cell)
FIG_AT = (3, 9)             # the figure on the left page (top-left cell); its caption 4 rows lower
STEPS = (12, 14, 16)        # step rows on the right page (all within his claw's reach)
STEP3_OK = ((6, 16), (7, 16))   # step 3's bullet + first word turn green when you approve it
V, VD, VL = 'v', 'V', 'l'   # cover: violet, deep violet shade, lavender highlight


def book_base():
    """The open manual at rest (static layer). The page turn and the tick are drawn over it."""
    f = Frame()
    for y in range(TOP + 1, PB + 3):                         # boards peeking out at the sides
        f.put(1, y, VL if y <= TOP + 2 else (V if y <= PB + 1 else VD))   # lit from the top-left
        f.put(10, y, V if y <= PB else VD)
    for y in range(TOP, PB + 1):                             # the two pages
        for x in range(LP[0], RP[1] + 1):
            f.put(x, y, 'w')
    f.vline(GUT, TOP + 1, PB, 'm')                           # gutter
    for x in (4, GUT, 6):                                    # page tops dip into the gutter
        f.put(x, TOP, '_')
    for x, y in ((2, TOP), (3, TOP), (4, TOP + 1), (6, TOP + 1), (7, TOP), (8, TOP), (9, TOP)):
        f.put(x, y, 'm')                                     # top edges of the page stacks
    for y in (PB + 1, PB + 2):                               # page block, two rows: the manual is THICK
        f.hline(2, 9, y, 'm')
        f.put(GUT, y, VD)
    f.hline(2, 9, PB + 3, VD)                                # bottom board, resting on the input box
    f.put(3, TOP - 1, 'j')                                   # sticky tabs poking out of the top
    f.put(8, TOP - 1, 'p')
    # left page: one bold figure (a blue part, lit top-left) and its caption: few, big marks read at 3 px
    f.place(_FIG, *FIG_AT)
    f.hline(LP[0], LP[1], FIG_AT[1] + 4, 'N')
    # right page: the cog emblem as its header, then the numbered steps (blue bullets)
    f.place(_COG, *COG_AT)
    for y in STEPS:
        f.put(6, y, 'b')
        f.hline(7, 8, y, 'N')
    return f


def _turning(f, outer, top, shade):
    """The page being turned, rotating about the gutter toward us.
    outer = column of its outer edge, top = row of its outer top corner (it is closer to us than the book,
    so it projects taller than the pages: the top corner traces an arc over the gutter).
    shade = colour of its face: lit 'w', or 'M' while its back is still tipped away from the top-left light."""
    side = 1 if outer > GUT else -1
    span = abs(outer - GUT)
    bottom = min(PB + (TOP - top + 1) // 2, PB + 1)        # the near edge stretches down, at most into the block
    for i in range(1, span + 1):
        x = GUT + side * i
        ty = TOP + 1 - int(round((TOP + 1 - top) * i / float(span)))
        by = PB + int(round((bottom - PB) * i / float(span)))
        for y in range(ty, by + 1):
            edge = (i == span) or y == ty or y == by or (i == 1 and y <= TOP)   # (inner edge above the gutter)
            f.put(x, y, 'm' if edge else shade)


# page-turn phases: (outer edge column, outer top row, face shade, printing on the face)
#   front of the old right page: its cog and steps squeezed by perspective; back = the new left page
_FRONT2 = [(6, 9, 'j'), (7, 8, 'y'), (7, 9, 'V'), (7, 10, 'J'), (6, 12, 'b'), (6, 14, 'b'), (6, 16, 'TICK'),
           (7, 12, 'N'), (7, 14, 'N'), (7, 16, 'TICK')]
_FRONT3 = [(6, 9, 'j'), (6, 12, 'b'), (6, 14, 'b'), (6, 16, 'TICK')]
_BACK6 = [(4, 9, 'b'), (4, 10, 'b'), (4, 11, 'B'), (4, 13, 'N')]
_BACK7 = [(3, 9, 'c'), (4, 9, 'b'), (3, 10, 'b'), (4, 10, 'b'), (3, 11, 'b'), (4, 11, 'B'), (3, 13, 'N'),
          (4, 13, 'N')]
TURN = {
    2: (8, 6, 'w', _FRONT2),
    3: (7, 5, 'w', _FRONT3),
    4: (6, 4, 'w', []),          # nearly edge-on, straight up out of the gutter
    5: (4, 5, 'M', []),
    6: (3, 6, 'M', _BACK6),
    7: (2, 7, 'w', _BACK7),      # lands, its outer corner still a row up
}


# the air pushed by the turning page lifts the sticky tabs for a moment (pink as the page rises past it,
# gold as it comes down on the left): one extra cell above the tab = the tab flipping up
_TAB_LIFT = {3: [(8, TOP - 2, 'p')], 4: [(8, TOP - 2, 'p')], 6: [(3, TOP - 2, 'j')]}


def pages(s):
    """Over the static book: the green step, the page-turn phases and the tabs lifting (additive only)."""
    f = Frame()
    k = s['turn']
    for x, y, ch in _TAB_LIFT.get(k, []):
        f.put(x, y, ch)
    if s['tick'] and k <= 1:
        for x, y in STEP3_OK:
            f.put(x, y, 'g')
    if k == 1:            # the corner lifts under his claw: the curl and its shadow (a little grey wedge)
        f.put(8, 16, 'm'); f.put(9, 16, 'N')
    elif k in TURN:
        outer, top, shade, printing = TURN[k]
        _turning(f, outer, top, shade)
        for x, y, ch in printing:
            f.put(x, y, ('g' if s['tick'] else ('b' if x == 6 else 'N')) if ch == 'TICK' else ch)
        if k == 7:
            f.put(2, TOP - 1, 'm')
    return f


# --------------------------------------------------------------------------------------------
# Vol. 2: standing closed, cover toward us (gold gear), its page block showing at the right
# --------------------------------------------------------------------------------------------
VOL_X, VOL_Y = 23, 10
_VOL = [
    'lvvvvvvm',
    'lvjvvjvM',
    'lvyjjjvm',
    'lyjVVjjM',
    'ljjVVjJm',
    'lvjjjJvM',
    'lvjvvJvm',
    'lvvvvvvM',
    'lvJjjJvm',
    'VVVVVVVm',
]
GEAR_TL = (VOL_X + 2, VOL_Y + 2)          # the lit top-left of the gear: where the light catches it


def scene():
    f = Frame()
    for yy, row in enumerate(_VOL):
        for xx, ch in enumerate(row):
            if ch != '.':
                f.put(VOL_X + xx, VOL_Y + yy, ch)
    return f.over(book_base())


GLINT_LOOP = 7680


def glint(first_ms):
    """The gear on Vol. 2 catches the light now and then: own loop (co-prime with the story).
    0-1-2-1-0: dot -> plus (white core) -> turned x -> plus -> dot; its first twinkle lands in a calm beat."""
    seq = [(0, 80), (1, 100), (2, 120), (1, 100), (0, 80)]
    out = [(Frame(), first_ms)]
    for i, ms in seq:
        f = Frame()
        f.place(_GLINT[i], *GEAR_TL)
        out.append((f, ms))
    out.append((Frame(), GLINT_LOOP - first_ms - sum(ms for _, ms in seq)))
    return out


# --------------------------------------------------------------------------------------------
# The bookworm: now and then an inchworm pokes out of Vol. 2's pages, inches along its top edge, rears up
# to watch Clawd read, turns and dives back in; later in its loop it only peeks out and ducks back.  Own
# loop (29.3 s), co-prime with the story, so it turns up during a different beat every time.
# Cells: (dx, dy, ch) from its head; it walks on row WY.
# --------------------------------------------------------------------------------------------
WY = VOL_Y - 1
WORM_LOOP = 29300
_W_FLAT = [(0, 0, 'G'), (1, 0, 'g'), (2, 0, 'g')]           # stretched out, head at the left
_W_ARCH = [(0, 0, 'G'), (1, -1, 'g'), (2, 0, 'g')]          # tail pulled up: the inchworm's hump
_W_REAR = [(0, -1, 'G'), (1, 0, 'g'), (2, 0, 'g')]          # head up, watching
_W_PEEK = [(0, -1, 'G'), (0, 0, 'g')]                       # just its head and neck, up out of the hole
_W_LOOK = [(-1, -1, 'G'), (0, 0, 'g')]                      # ... leaning over to look his way
_mirror = lambda cells: [(-dx, dy, ch) for dx, dy, ch in cells]


def _worm_frames(rear_at, spotted_at):
    """rear_at: loop time (ms) at which the worm should be rearing up on its first visit (he glances over
    and seems to notice it); spotted_at: loop time (ms) of his glance during its second, shorter visit: it
    has been leaning over to watch him read and ducks back in the moment he looks its way."""
    R = VOL_X + 7                                            # its hole: the top of Vol. 2's pages
    visit = [
        ([(0, 0, 'G')], R, 340),                             # pokes out of the pages
        (_W_FLAT, R - 2, 300),                               # slides out
        (_W_ARCH, R - 2, 240), (_W_FLAT, R - 3, 300),        # inches left
        (_W_REAR, R - 3, 1000),                              # rears up: what is he reading?
        (_mirror(_W_FLAT), R - 1, 300),                      # turns around
        (_mirror(_W_ARCH), R - 1, 240), (_mirror(_W_FLAT), R, 300),
        ([(0, 0, 'G')], R, 240),                             # dives back in (then hidden again)
    ]
    peek = [
        ([(0, 0, 'G')], R, 300),                             # pokes out ...
        (_W_PEEK, R, 460),                                   # ... head up: anyone there?
        (_W_LOOK, R, 1100),                                  # leans over to watch him read ...
        (_W_PEEK, R, 120),                                   # ... he looks this way: whoops,
        ([(0, 0, 'G')], R, 140),                             # ducks back in
    ]
    lead = rear_at - sum(ms for _, _, ms in visit[:4])       # hidden until then ...
    peek_at = spotted_at - sum(ms for _, _, ms in peek[:3]) + 60   # (60 ms: it reacts to his glance)
    gap = peek_at - lead - sum(ms for _, _, ms in visit)
    out = [(Frame(), lead)]
    for seq, hidden_after in ((visit, gap), (peek, None)):
        for cells, hx, ms in seq:
            f = Frame()
            for dx, dy, ch in cells:
                f.put(hx + dx, WY + dy, ch)
            out.append((f, ms))
        if hidden_after is not None:
            out.append((Frame(), hidden_after))
    out.append((Frame(), WORM_LOOP - sum(ms for _, ms in out)))   # ... and hidden again
    return out


# --------------------------------------------------------------------------------------------
# Clawd
# --------------------------------------------------------------------------------------------
# his left claw (screen-left arm), absolute cells.  'rim' = the kit's 'out' arm (mirrored): the claw tip
# lies on the right page's outer edge, holding the manual open
REACH = {
    'rim': [(10, 14), (9, 14)],
    12: [(10, 14), (9, 13), (8, 12)],      # kit 'wave': claw on step 1
    13: [(10, 14), (9, 13), (8, 13)],
    14: [(10, 14), (9, 14), (8, 14)],      # kit 'point': claw on step 2
    15: [(10, 14), (9, 15), (8, 15)],
    16: [(10, 15), (9, 16), (8, 16)],      # claw on step 3 (the page's bottom corner)
    'tap': [(10, 15), (9, 15), (8, 15)],   # lifted a cell off step 3 (each nod taps it)
    'lift': [(10, 15), (9, 15)],           # lifting the page corner
    'push': [(10, 14), (9, 14), (8, 14)],  # pushing the rising page over
}


def _pose(s):
    p = clawd(eyes=s['eyes'], larm='none', rarm=s['rarm'])
    cells = [(x, y, c) for x, y, c in p.sprite.cells]
    for ax, ay in REACH[s['reach']]:
        cells.append((ax - HOME[0], ay - HOME[1], '#'))
    return Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec, larm=s['reach']))


def body(s):
    f = Frame()
    put_clawd(f, _pose(s))
    return f


def sprout(s):
    f = Frame()
    p = _pose(s)
    if s['sprout'] == 'dip':
        f.place(_SPROUT_DIP, *p.at('head'))
    else:
        wear(f, _SPROUT, p, i=s['sprout'])
    return f


# the "?" is the 3x5 font glyph in the manual's violet (lit top-left cell): small and quiet, nothing like the
# question state's big blue "?".  Its top-left is (Q_X, q): q = 7 puts its dot right on his raised claw
# tip (21, 12); it rises to q = 5.  The tick's bottom point is TICK_AT: one clear row above Vol. 2.
Q_X = 20
TICK_AT = (21, 8)


def fx(s):
    f = Frame()
    q = s['q']
    if q == 'dot':                       # nod 2: the "?" loses its hook; its dot hops up, already green
        f.put(TICK_AT[0], TICK_AT[1], 'g')
    elif q is not None:
        f.text('?', Q_X, q, V)
        f.put(Q_X, q, VL)
    if s['tk'] is not None:
        f.place(_TICK[s['tk']], *TICK_AT)
    return f


# --------------------------------------------------------------------------------------------
# the story
# --------------------------------------------------------------------------------------------
READ = 'look_l'


def story():
    S = []
    cur = dict(eyes=READ, reach='rim', rarm='side', sprout=0, q=None, tk=None, tick=False, turn=0)

    def add(ms, mark=None, **kw):
        cur.update(kw)
        S.append(dict(cur, ms=ms, mark=mark))

    # A: reading, holding the page open (frame 0)
    add(1700)
    add(120, eyes='blink')
    add(500, eyes=READ)
    add(700, sprout=1)                    # a breath of air: the sprout sways
    add(800, eyes='look_dl', sprout=0, mark='calm')   # reads on down the page
    # B: the claw arcs up to step 1, then runs down the steps (slow in and out of each step)
    add(130, reach=13, eyes=READ)
    add(460, reach=12, eyes='look_ul')
    add(110, reach=13, eyes=READ)
    add(360, reach=14)
    add(110, reach=15, eyes='look_dl')
    add(700, reach=16)                    # he lingers on step 3 ...
    # C: "this one?" -- looks up at you, blinks, raises his free hand like a student
    add(650, eyes='open')
    add(110, eyes='blink')
    add(130, eyes='open', rarm='up')
    add(70, rarm='raise', q=7)            # the "?" rises out of his claw ...
    add(70, q=6)
    add(580, q=5)                         # ... and hangs there, small and quiet
    # D: nod, nod: each nod is one held DOWN key where eyes, sprout and claw (tapping step 3) move as one;
    #    the claw lifts on every up key, the sprout lags on the way up
    add(90, eyes='look_u', reach='tap')   # anticipation: head up, claw lifts
    add(200, eyes='look_d', sprout='dip', reach=16)                   # nod 1: tap
    add(90, eyes='open', reach='tap', rarm='up')                      # up (the sprout still down); hand starts down
    add(90, sprout=0, rarm='side')
    add(200, eyes='look_d', sprout='dip', reach=16, q='dot')          # nod 2: tap; the "?" collapses to a dot ...
    add(90, eyes='open', reach='tap', q=None, tk=0)                   # ... which blooms into a tick as he comes up
    add(130, sprout=1, tk=1)              # overshoot; the sprout swings right ...
    add(170, sprout=3, tk=2)              # ... settles; left ...
    add(130, sprout=0, reach=16)          # ... and rest; his claw presses step 3 ...
    add(960, tick=True)                   # ... and it turns green in the book: a satisfied still
    add(200, eyes='look_dl')
    # E: page turn (eased: slow lift, fast through the vertical, soft landing); the tick shrinks away
    add(120, reach='lift', turn=1, tk=0)
    add(90, reach='push', turn=2, tk=None, eyes=READ)
    add(70, reach=14, turn=3)
    add(60, turn=4, eyes='look_ul')
    add(70, reach='rim', turn=5)          # his claw goes back to holding the (new) right page
    add(80, turn=6, eyes=READ, tick=False)
    add(120, turn=7)
    add(300, turn=0)
    # F: a calm read of the fresh page (plain face, hands still: the long quiet middle of the read)
    add(600, eyes='look_ul')              # from the top ...
    add(900, eyes=READ)
    add(130, eyes='blink')
    add(600, eyes=READ)
    add(520, eyes='look_r', mark='glance')    # Vol. 2 is waiting ...
    add(110, eyes='blink')                # ... blink-blink (oh boy)
    add(110, eyes='look_r')
    add(110, eyes='blink')
    add(350, eyes=READ)                   # back to it (= frame 0)
    return S


def _t(S, mark):
    """Story time (ms) at which the beat with this mark starts."""
    t = 0
    for s in S:
        if s['mark'] == mark:
            return t
        t += s['ms']
    raise KeyError(mark)


def build():
    S = story()
    per = lambda fn: [(fn(s), s['ms']) for s in S]
    total = sum(s['ms'] for s in S)
    glance = _t(S, 'glance')
    return anim(NAME, DESC, [
        static('scene', scene()),
        layer('glint', glint(_t(S, 'calm') + 240)),   # inside the calm 800 ms hold
        # first visit: it rears up as he glances over; second (a peek): it ducks as he glances over again
        layer('worm', _worm_frames(glance - 60, total + glance)),
        layer('pages', per(pages)),
        layer('body', per(body)),
        layer('sprout', per(sprout)),
        layer('fx', per(fx)),
    ], state=STATE)
