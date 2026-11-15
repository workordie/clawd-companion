"""wear: things Clawd wears on his BACK and around his NECK.

back items: anchor = his body center (box (5, 3)); wear() them BEFORE put_clawd() so he covers the middle.
            cape, wings_angel, wings_bat, wings_butterfly, jetpack, backpack, snail_shell, parachute,
            devil_tail, cat_tail
neck items: anchor = box (5, 4), two rows below his eyes; wear() them AFTER put_clawd().
            scarf, bow_tie, necktie, gold_chain, medal, lanyard_badge, tool_belt, apron
Sprites are drawn in Clawd-box coordinates (see _art) so every pixel's place on him is obvious.
Neck items keep his eyes and hands free in every allowed glance and arm pose (rules above the NECK section);
the one exception, bow_tie on look_dl/look_dr, says so in its desc. Animated items suggest a play order and ms.
"""
from clawdlib import HEX, Item, Sprite

BACK = (5, 3)
NECK = (5, 4)


def _art(rows, x0, y0, anchor, mirror=False):
    """rows in Clawd-box coordinates: rows[j][i] is box cell (x0 + i, y0 + j).
    mirror=True copies the drawing onto the other side around box column 5."""
    cells = {}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in '. ':
                continue
            if ch not in HEX:
                raise ValueError('wear: unknown color %r at box (%d,%d)' % (ch, x0 + i, y0 + j))
            cells[(x0 + i, y0 + j)] = ch
    if mirror:
        for (x, y), ch in list(cells.items()):
            cells.setdefault((10 - x, y), ch)
    return Sprite(cells=[(x, y, ch) for (x, y), ch in cells.items()], anchor=anchor)


def back(rows, x0, y0, mirror=False):
    return _art(rows, x0, y0, BACK, mirror)


def neck(rows, x0, y0, mirror=False):
    return _art(rows, x0, y0, NECK, mirror)


# ============================================================================================
# BACK
# ============================================================================================
def _cape(left, right):
    """Cape from per-row outer edges (rows 0-6; the inner part runs under his body). Lit red 'r' on every
    left-facing or top-facing edge (light from the top-left; it also keeps the dark cape visible on the dark
    theme), dark red 'R' elsewhere. His shoulder cells (0,0)/(10,0) stay dark so his top corners stay crisp."""
    cells = {(x, y) for y in range(7) for x in range(left[y], right[y] + 1)}
    c = {}
    for (x, y) in cells:
        c[(x, y)] = 'r' if (x - 1, y) not in cells or (x, y - 1) not in cells else 'R'
    c[(0, 0)] = c[(10, 0)] = 'R'
    return Sprite(cells=[(x, y, ch) for (x, y), ch in c.items()], anchor=BACK)


# Bell drape: hugs his shoulders, flares at the hem, hem visible between his legs. The swing frames are a
# pendulum: shoulders pinned, the hem moves one cell, volume stays within one pixel.
CAPE = Item('cape', 'back', "Red hero cape: bell drape from his shoulders, hem behind his legs. Sway as a pendulum: frames 0,1,0,2 at ~240 ms (0 is the still); with the crown it reads royal. wear before put_clawd", [
    _cape([0, -1, -1, -1, -2, -3, -4], [10, 11, 11, 11, 12, 13, 14]),
    _cape([0, -1, -1, -2, -3, -4, -5], [10, 11, 11, 11, 11, 12, 13]),
    _cape([0, -1, -1, -1, -1, -2, -3], [10, 11, 11, 12, 13, 14, 15]),
], ms=240)

def _wings(rows, x0, y0, shade_right=None):
    """Left wing drawn in box coords, mirrored onto the right side around box column 5. Light comes from the
    top-left, so on the right wing `shade_right` {highlight: base} demotes highlights that are not on its top edge."""
    spr = back(rows, x0, y0, mirror=True)
    if not shade_right:
        return spr
    cells = {(x, y): ch for x, y, ch in spr.cells}
    for (x, y), ch in list(cells.items()):
        if x > 5 and ch in shade_right and cells.get((x, y - 1)) not in (None, 'm', 'v'):
            cells[(x, y)] = shade_right[ch]
    return Sprite(cells=[(x, y, ch) for (x, y), ch in cells.items()], anchor=BACK)


# angel wings: paper 'w' feathers, white 'W' highlight running along the leading edge, light-gray 'M' feather
# lines, silver 'm' contour (keeps the white readable on the light theme). All three frames are up-swept wing
# shapes rotating about the same shoulder root: rest (~30 deg up), raised, lowered (tip just below the root).
WINGS_ANGEL = Item('wings_angel', 'back', 'White feathered angel wings swept up from his shoulders. Frames 0-2 = rest/up/down: flap 0,1,0,2 at ~140 ms, or hold 0 (the still). wear before put_clawd', [
    _wings([
        'mm.......',
        'mWmm.....',
        'mwWWmm...',
        '.mwwWWmm.',
        '.mMwwwWWm',
        '..mMwMwww',
        '...mmMmww',
        '.....mmmw',
    ], -7, -4, {'W': 'w'}),
    _wings([
        'mm.....',
        'mWm....',
        'mwWm...',
        'mwwWm..',
        '.mMwWm.',
        '.mwMwWm',
        '..mwMwWm',
        '..mmwMww',
        '....mmww',
    ], -6, -7, {'W': 'w'}),
    _wings([
        '.....mmmm',
        '...mmWWWm',
        '.mmWWwwww',
        'mWwwMwMww',
        'mwMwwMwmw',
        '.mmMmmm..',
    ], -7, -1, {'W': 'w'}),
], ms=140)

# bat wings: deep violet 'V' membrane, violet 'v' finger bones / rim, lavender 'l' highlight on the arm bone that
# ends in a single claw tip. Frames: level, raised, down-stroke (bone angled down, tip below the root, same span).
WINGS_BAT = Item('wings_bat', 'back', 'Small bat wings; frames 0-2 = level/up/down: flap 0,1,0,2 at ~120 ms, or hold 0 (the still). wear before put_clawd', [
    _wings([
        'l.......',
        'vl......',
        'vVll....',
        'vVVVlll.',
        'vVVVVVVV',
        'v.VVv.VV',
        '..v.....',
    ], -6, -3),
    _wings([
        '..l.....',
        '.lvl....',
        'vVVvl...',
        'vVVVVl..',
        '.vVVVVl.',
        '..v.VVVl',
        '....v.VV',
    ], -6, -5),
    _wings([
        '....llll',
        '..llVVVV',
        'llVVVVVV',
        'vVVVvVVV',
        'v.Vv.VV.',
        '....v...',
    ], -6, 0),
], ms=120)

# jetpack: two silver tanks (silver edge 'm', chrome highlight 'S', steel shadow 's') with red nose cones that
# peek above his shoulders, nozzles that ramp lit-to-dark left to right like the tanks (m N n), red fins whose
# top cells catch the light, and flames: orange 'o' / red 'r' outline (readable on both themes) around a yellow
# 'y' body and a pale-yellow 'Y' core. (No backplate: his body always covers it.)
_TANKS = [
    '...r.........r...',
    '..rrR.......rrR..',
    '..mSs.......mSs..',
    '..mSs.......mSs..',
    '..mSs.......mSs..',
    '..mSs.......mSs..',
    '..mSs.......mSs..',
    '..mSs.......mSs..',
    '.rmNn.......mNnr.',
    'rrmNn.......mNnRR',
]
# one jet, 3 wide, starting right under the nozzle; yellow stays inside an orange/red outline
_FLAMES = [
    ['oYo', 'oyo', '.o.', '.r.', '...'],
    ['oYo', 'ror', '.r.', '...', '...'],
    ['oYo', 'oyo', '.or', '..r', '...'],
    ['oYo', 'oyo', 'oyo', '.o.', '.r.'],
]


def _jetpack(i=None):
    rows = list(_TANKS)
    if i is not None:                                     # i=None: engines off (safe at HOME, nothing below his feet)
        for a, b in zip(_FLAMES[i], _FLAMES[(i + 2) % 4]):   # the two jets flicker out of phase
            rows.append('..' + a + '.......' + b + '..')
    return back(rows, -3, -3)


JETPACK = Item('jetpack', 'back', "Twin rocket jetpack: frames 0-3 = flames at ~80 ms (they hang 4 rows below his feet: hover him 4+ rows up, legs='short' so the jets show whole); frame 4 = engines off, safe at home. wear before put_clawd",
               [_jetpack(i) for i in range(4)] + [_jetpack()], ms=80)

# backpack: worn a little off-center so it peeks out past his LEFT shoulder (a centered bag peeking over his
# head reads as a hat). Green 'g', dark-green 'G' shadow/seams, mint 'h' flap highlight kept off the
# silhouette (mint fades on the light theme), gold 'j' buckle, carry loop on top, front pocket.
BACKPACK = Item('backpack', 'back', 'Small green backpack peeking out past his left shoulder (loop, flap, buckle, pocket). wear before put_clawd', [
    back([
        '..ggg..',
        '..G.G..',
        '.ggggg.',
        'ghhhhgG',
        'gggjggG',
        'gGGGGgG',
        'gGgggGG',
        'gGGGGGG',
        '.GGGGG.',
    ], -4, -4),
])

# ---- extras (back) -------------------------------------------------------------------------
# butterfly wings: violet rim, cyan forewing with ice highlight and a yellow eyespot, violet near the body,
# pink hindwing. Frames: open, up, down (same 23-cell span, pixel counts within a few cells).
WINGS_BUTTERFLY = Item('wings_butterfly', 'back', 'Colorful butterfly wings (breezy auto mode); frames 0-2 = open/up/down: flap 0,1,0,2 at ~150 ms, or hold 0 (the still). wear before put_clawd', [
    _wings([
        '.VV.....',
        'VCcVV...',
        'VcyccVV.',
        'VccccvvV',
        '.VVcvvVV',
        '..VppVV.',
        '..VPpV..',
        '...VV...',
    ], -6, -4),
    _wings([
        '.VV.....',
        'VCcV....',
        'VcycV...',
        'VcccvV..',
        '.VccvvV.',
        '..VVvvVV',
        '..VppVVV',
        '..VPpV..',
        '...VV...',
    ], -5, -5),
    _wings([
        '.VVV....',
        'VCccVVV.',
        'VcyccvvV',
        '.VVccvvV',
        '..VVppVV',
        '..VPppV.',
        '...VVV..',
    ], -6, -2),
], ms=150)

# snail shell: tan shell with one continuous dark-wood spiral (outer rim -> closed center, 1:1 corners), a
# pale-yellow glint top-left, wood outline on a symmetric disc; peeks out past his left shoulder like the backpack.
# A slow-snail pun for rate-limit.
SNAIL_SHELL = Item('snail_shell', 'back', 'Spiral snail shell peeking out past his left shoulder (rate-limit: slow-snail pun). wear before put_clawd', [
    back([
        '..TTTT...',
        '.TtYttT..',
        'TtdddttT.',
        'TdtttdtT.',
        'TdtdtdtT.',
        'TdtddtTT.',
        '.TdtttT..',
        '..TTTT...',
    ], -5, -4),
])


def _parachute(inflated):
    """Red/white canopy high above him and gray suspension lines meeting at his shoulders in two clean V's.
    inflated=True lifts the dome one row (the canopy 'breathes'); the hem and the lines never move."""
    c = {}
    if inflated:
        rows = {-11: (3, 7), -10: (1, 9), -9: (0, 10), -8: (-1, 11), -7: (-2, 12), -6: (-2, 12)}
    else:
        rows = {-10: (2, 8), -9: (0, 10), -8: (-1, 11), -7: (-2, 12), -6: (-2, 12)}
    first = min(rows)
    for y, (a, b) in rows.items():
        for x in range(a, b + 1):
            g = (x + 2) // 3                         # gores 0..4: red, white, red, white, red
            top = y == first or x < rows[y - 1][0] or x > rows[y - 1][1]
            if g % 2 == 0:                           # red gores: lit on the left, shaded on the right
                ch = 'r' if g == 0 or (g == 2 and x < 6) else 'R'
            else:                                    # white gores: silver rim on top and hem (light theme), gray shade right
                ch = 'm' if top or y == -6 else ('w' if g == 1 else 'M')
            c[(x, y)] = ch
    c[(-1, -7)] = 'p'                                # satin glint on the lit side of the canopy
    for (x0, y0), (x1, y1) in (((-2, -5), (2, -1)), ((2, -5), (2, -1)), ((12, -5), (8, -1)), ((8, -5), (8, -1))):
        n = max(abs(x1 - x0), abs(y1 - y0))          # 1:1 diagonals and verticals only: perfectly clean steps
        for k in range(n + 1):
            c.setdefault((x0 + (x1 - x0) * k // n, y0 + (y1 - y0) * k // n), 'N')
    return Sprite(cells=[(x, y, ch) for (x, y), ch in c.items()], anchor=BACK)


PARACHUTE = Item('parachute', 'back', 'Red/white parachute above him, lines to his shoulders (hello: float him down). Frames 0-1 breathe: ~700 ms settled, ~450 ms puffed. wear before put_clawd',
                 [_parachute(False), _parachute(True)], ms=[700, 450])

# devil tail: thin red shaft in an S-curve with a spade tip (pink glint top, lit left, shaded right/bottom); the root
# tucks behind his lower-left side. Pairs with headwear's devil_horns (+ wings_bat) for a full little devil.
DEVIL_TAIL = Item('devil_tail', 'back', "Red devil tail with a spade tip curling out from behind his left side (bypass/mischief; pair with devil_horns). Swish 0,1,0,2 at ~250 ms, or hold 0. wear before put_clawd (after wings_bat so the spade shows over the wing)", [
    back(['.p.....',
           'rrR....',
           'rRR....',
           '..r....',
           '...r...',
           '...r...',
           '....r..',
           '.....rR'], -6, -2),
    back(['..p....',
           '.rrR...',
           '.rRR...',
           '...r...',
           '...r...',
           '....r..',
           '....r..',
           '.....rR'], -6, -2),
    back(['p......',
           'rrR....',
           'rRR....',
           '..r....',
           '..r....',
           '...r...',
           '....r..',
           '.....rR'], -7, -2),
], ms=250)

# cat tail: 2-wide gray tail (silver lit left edge, gray right edge) rising from behind his lower-left side and
# curling over at the tip like a question mark. Pairs with headwear's cat_ears.
CAT_TAIL = Item('cat_tail', 'back', "Gray cat tail rising from behind his left side, tip curled like a question mark (pair with cat_ears). Frames 0-2 = rest/tip up/curl low: swish 0,1,0,2 at ~300 ms with long holds on 0. wear before put_clawd", [
    back(['.mN...',
           'mN.m..',
           'N..mN.',
           '...mN.',
           '...mN.',
           '....mN',
           '....NN'], -5, -1),
    back(['...m..',
           '..mN..',
           '.mN...',
           '.mN...',
           '..mN..',
           '...mN.',
           '....mN',
           '....NN'], -5, -2),
    back(['......',
           'mNmN..',
           'N..mN.',
           '...mN.',
           '...mN.',
           '....mN',
           '....NN'], -5, -1),
], ms=300)

# ============================================================================================
# NECK  (drawn on his body, after him). Where a neck item may put pixels, in box coordinates:
#   row 3      only columns 4-6. His eye holes move down onto row 3 (columns 1-3 and 7-9) for look_d /
#              look_dl / look_dr, and his hands sit at (1,3)/(9,3) with arms='front'.
#   rows 4-5   his chest, columns 1-9. (0,4)/(10,4) are his hands with arms='down', so stay inside.
#   rows 6-7   between his legs only (columns 2, 4-6, 8): pendants and tie tips hang there. Row 7 is the
#              ground row, fine because the user never wants body='crouch'/'squash' (they would push it off).
# ============================================================================================
def _cells(d, anchor=NECK):
    return Sprite(cells=[(x, y, ch) for (x, y), ch in d.items()], anchor=anchor)


# scarf: red knit band low on his chest (eye-safe), dark-red lower row puffing past his sides, a knot on his left
# hip and a tan-striped tail that rises out to his LEFT in the breeze (his right side is where held items go).
# The tail is built from per-column top/bottom edges; where the top edge steps, the bottom edge steps one column
# later, so the strip bends instead of shearing. Frames: rest, tip up, tip down (one row per step).
def _scarf(top, bot, tip):
    c = {}
    for x in range(1, 10):
        c[(x, 4)] = 'r'
    for x in range(0, 11):
        c[(x, 5)] = 'R'
    c[(-1, 4)] = 'r'
    c[(-1, 5)] = 'r'
    c[(-1, 6)] = 'R'
    c[(0, 6)] = 'R'                                   # knot under the band's left end
    for k, x in enumerate(range(-2, -2 - len(top), -1)):
        for y in range(top[k], bot[k] + 1):
            if x in (-4, -6):
                c[(x, y)] = 't'                       # knit stripes (tan stays visible on white)
            else:
                c[(x, y)] = 'r' if y == top[k] else 'R'
    c[tip] = 'R'                                      # frayed tip
    return _cells(c)


SCARF = Item('scarf', 'neck', "Cozy red knit scarf, knot on his left hip, striped tail rising out to his left in the breeze. Play frames 0,1,0,2 at ~200 ms (0 is the still). Low band keeps every glance and arms='down' free. wear after put_clawd", [
    _scarf([4, 3, 3, 2, 2], [5, 5, 4, 4, 3], (-7, 3)),
    _scarf([4, 3, 3, 2, 1], [5, 5, 4, 3, 3], (-7, 2)),
    _scarf([4, 3, 3, 3, 3], [5, 5, 4, 4, 4], (-7, 4)),
], ms=200)

# bow tie: dark-red wings with a lit top-left cell each and a pink pinched knot (bright red would melt into his
# orange). Its top corners (3,3)/(7,3) are the only neck pixels outside the eye-safe columns: the bow shape needs them.
BOW_TIE = Item('bow_tie', 'neck', "Classy dark-red bow tie with a pink knot (dressed up, hello). Static. Its top corners hide one eye on look_dl/look_dr: use level, up or look_d glances. wear after put_clawd", [
    neck([
        'rR.rR',
        'RRpRR',
        'RR.RR',
    ], 3, 3),
])

# necktie: navy knot, narrow blue neck, blade lit on the left (blue) and shaded on the right (navy), point between
# his legs. No collar: white collar points read as holes or teeth on his face.
NECKTIE = Item('necktie', 'neck', 'Blue office necktie: navy knot under his eyes, blade hanging between his legs. Static (working, plan). wear after put_clawd', [
    neck([
        '.B.',
        '.b.',
        'bbB',
        'bbB',
        '.b.',
    ], 4, 3),
])

# gold chain: chunky two-tone strands (yellow lit edge, dark-gold underside) in a narrow V that stays inside his eyes,
# and a cut diamond (cyan crown, ice table facet, blue shade + point) hanging between his legs. A full-width V reads
# as a grin; this narrow one reads as a pendant. Frames: plain, glint (a diagonal shine from the lit facet up
# onto his chest), afterglow. Every glint cell sits on the gem or on him, never on the background.
def _chain(glint=()):
    c = {(3, 4): 'y', (7, 4): 'y',
         (3, 5): 'J', (4, 5): 'y', (6, 5): 'y', (7, 5): 'J',
         (4, 6): 'c', (5, 6): 'C', (6, 6): 'b',
         (5, 7): 'b'}
    for p in glint:
        c[p] = 'W'
    return _cells(c)


GOLD_CHAIN = Item('gold_chain', 'neck', 'Gold chain with an iced-out diamond between his legs (vibe). Hold 0 for ~3 s, then glint 1-2 at 90/120 ms; vary the hold each loop (e.g. 2.8 s, 4.1 s). wear after put_clawd', [
    _chain(),
    _chain([(4, 5), (5, 6)]),
    _chain([(5, 6)]),
], ms=[3000, 90, 120])

# medal: two-tone ribbon V (lit blue left strap, navy right strap) starting below his eye row, its tips rounding off
# the top corners of a gold coin that hangs between his legs (lit top-left, dark-gold bottom-right).
# Frames: plain, glint (a diagonal shine across the coin's lit top-left), afterglow; the coin keeps its outline.
def _medal(glint=()):
    c = {(2, 4): 'b', (3, 4): 'b', (7, 4): 'B', (8, 4): 'B',
         (3, 5): 'b', (4, 5): 'b', (5, 5): 'y', (6, 5): 'B', (7, 5): 'B',
         (4, 6): 'Y', (5, 6): 'y', (6, 6): 'j',
         (4, 7): 'j', (5, 7): 'J', (6, 7): 'J'}
    for p in glint:
        c[p] = 'W'
    return _cells(c)


MEDAL = Item('medal', 'neck', 'Gold winner medal on a blue ribbon, coin between his legs (done). Hold 0 for ~3 s, then glint 1-2 at 90/120 ms; vary the hold each loop (e.g. 2.6 s, 3.9 s). wear after put_clawd', [
    _medal(),
    _medal([(4, 6), (5, 5)]),
    _medal([(4, 6)]),
], ms=[3000, 90, 120])

# lanyard badge: navy cords that run down between his eyes (columns 4 and 6 never hold an eye in any glance) to a
# portrait ID card: blue header with a steel clip, a little photo of him (rust), light-gray card with a silver
# shade edge, steel bottom corner. No white on the card: on the light theme white reads as a hole in him.
LANYARD_BADGE = Item('lanyard_badge', 'neck', 'ID badge on a navy lanyard: blue header, steel clip, his photo (working). Static. wear after put_clawd', [
    neck([
        'B.B',
        'B.B',
        'bsb',
        'OMm',
        'mms',
    ], 4, 2),
])


# tool belt: leather belt (lit wood row, dark-wood row, gold buckle). Left hip: a leather pouch with a red
# screwdriver handle and a steel wrench sticking out. Right hip: a claw hammer hanging head-up in a belt loop.
# Everything outside him starts at row 5 or at x <= -1 / x >= 11, so his hands stay free in every arm pose.
def _tool_belt():
    c = {}
    for x in range(1, 10):
        c[(x, 4)] = 'T'
        c[(x, 5)] = 'd'
    c[(5, 4)] = 'j'
    c[(5, 5)] = 'J'
    # pouch on his left hip (tan flap lit from the top-left, wood body)
    c.update({(-2, 5): 't', (-1, 5): 't', (0, 5): 'T',
              (-2, 6): 'T', (-1, 6): 'T', (0, 6): 'T'})
    c.update({(-2, 3): 'r', (-2, 4): 'r',            # screwdriver handle
              (-1, 3): 'm', (-1, 4): 's'})           # wrench
    # hammer in a loop on his right hip
    c.update({(10, 5): 'T', (11, 5): 'T',            # loop
              (11, 4): 'm', (12, 4): 'm', (13, 4): 's',
              (12, 5): 'T', (12, 6): 'T', (12, 7): 'r'})
    return _cells(c)


TOOL_BELT = Item('tool_belt', 'neck', 'Leather tool belt with a gold buckle: pouch with screwdriver + wrench on his left hip, hammer in a loop on his right (edits mode). Static. wear after put_clawd', [_tool_belt()])

# apron: chef apron in light gray (white would read as a hole on the light theme) with a paper highlight on its
# lit left edge and silver shade on the right: bib, navy waist ties whose ends hang at his sides, and a skirt that
# flares wider than the bib with a silver hem. The hem covers the tops of his inner legs: the apron hangs in front.
APRON = Item('apron', 'neck', 'Little chef apron: gray-white bib, navy waist ties, flared skirt with a silver hem over his inner legs. Static. wear after put_clawd', [
    neck([
        '...wMm...',
        'BBBwMmBBB',
        'B.wMMMm.B',
        '.mmmmmms.',
    ], 1, 3),
])

ITEMS = [CAPE, WINGS_ANGEL, WINGS_BAT, JETPACK, BACKPACK, SCARF, BOW_TIE, NECKTIE, GOLD_CHAIN, MEDAL,
         LANYARD_BADGE, TOOL_BELT, APRON,
         WINGS_BUTTERFLY, SNAIL_SHELL, PARACHUTE, DEVIL_TAIL, CAT_TAIL]
