"""Scenery: furniture, sets and small props for Clawd's scenes.

Slots: 'scene' = furniture / sets, 'ground' = props that rest on a surface (both anchored on their
bottom-center cell, so place them at (x, 19) to stand on the input box), 'fx' = floating things
(anchored on their visual center).

Every set below uses Clawd's NORMAL body at HOME (box (10, 12), eyes on row 14, arms x 10 / 20);
STYLE.md section 0: no crouch / squash / stretch.
  sleep     bed (15, 19) -> put_clawd (eyes 'closed') -> blanket / blanket_breathe (15, 19); moon fx (26, 5)
  working   chair (15, 19) -> put_clawd -> desk (18, 19) -> keyboard(_tap) (15, 16) + monitor (25, 15)
  typing    put_clawd -> laptop_back (15, 19)
  lounge    beanbag (15, 19) -> put_clawd -> beanbag_front (15, 19)
  vibe      speaker (26, 19) -> put_clawd -> dj_decks (15, 19); disco_ball fx (4, 6)
  hello     box (15, 19) -> put_clawd -> box_front (15, 19)
  ride      put_clawd(f, p, 10, 9) -> skateboard (15, 19);  put_clawd(f, p, 10, 10) -> cloud_platform (15, 19)
  compact   paper_stack_tall -> _mid -> _low -> paper_cube, all at (25, 19); paper_sheet fx; trash_bin (26, 19)
  plan      corkboard (7, 10) above-left + bookshelf (26, 19) (or the corkboard alone at (24, 9));
            lamp (5, 19) or on the desk top
Ground props that fit beside him at HOME with a 1-cell gap: x 1..8 on his left, x 22..30 on his right.
"""
from clawdlib import Item, Sprite


def _check(rows, name):
    w = len(rows[0])
    for r in rows:
        if len(r) != w:
            raise ValueError('%s: ragged row %r (%d vs %d)' % (name, r, len(r), w))
    return w


def bc(rows, name='', ax=None):
    """Sprite anchored on its bottom-center cell (ax overrides the column)."""
    w = _check(rows, name)
    return Sprite(rows, anchor=(w // 2 if ax is None else ax, len(rows) - 1), name=name)


def mid(rows, name=''):
    """Sprite anchored on its visual center (fx)."""
    w = _check(rows, name)
    return Sprite(rows, anchor=(w // 2, len(rows) // 2), name=name)


# ---------------------------------------------------------------- bedroom
# Patchwork quilt: 3-wide blue / violet patches; the front edge (row 3) is the next row of patches,
# offset and in shade, as the quilt curves down; a folded white cuff with silver ends on top.
BLANKET_ROWS = [
    'mWwwwwwwwwwwm',
    'bbvvvbbbvvvbB',
    'bbvvvbbbvvvbB',
    'VVBBBVVVBBBVV',
]
# breathing in: only the middle of the cuff (over his chest) lifts a row; the tucked corners stay
BLANKET_BREATHE_ROWS = [
    '..mWwwwwwwm..',
    'mWvvvbbbvvvwm',
] + BLANKET_ROWS[1:]

# pinched corner tips and a silver contour (light theme), lit from the top-left
PILLOW_ROWS = [
    'm.mmmmm.m',
    '.mWWwwwm.',
    '.mWwwwMm.',
    '.mwwwMMm.',
    'm.mmmmm.m',
]

BED_ROWS = [
    'tT.............tT',
    'tT....ttttt....tT',
    'tT..ttTTTTTtt..tT',
    'tTttTTTTTTTTTtttT',
    'tTTmmmmmmmmmmmTtT',
    'tTmWwwwwwwwwwwmtT',
    'tTmwwwwwwwwwwMmtT',
    'tTmMMMMMMMMMMMmtT',
    'tmWwwwwwwwwwwwwmT',
    'tmMMMMMMMMMMMMMmT',
    'ttttttttttttttttt',
    'TTTTTTTTTTTTTTTTT',
    'tT.............tT',
]

# ---------------------------------------------------------------- office
# tabletop over a dark lip shadow, three drawers with brass knobs, right side in shade
DESK_ROWS = [
    '.ttttttttttttttttt.',
    'ttttttttttttttttttT',
    'TdddddddddddddddddT',
    '.TTjTTdTTjTTdTTjTd.',
    '.TTTTTdTTTTTdTTTTd.',
]

LAPTOP_ROWS = [
    '.NNNNNNN.',
    'NmnPnpnnN',
    'NnnpppnnN',
    'NnnnpnnnN',
    'smmmmmmms',
]

# Six lines of syntax-colored code (12 rows: line, gap), indented like a function; the screen shows
# 5 rows and scrolls one line (2 rows) per frame, so the 6 frames loop seamlessly. Column 0 stays dark.
MON_PAGE = [
    '.vv.cc.',
    '.......',
    '..yy.g.',
    '.......',
    '..ppp..',
    '.......',
    '...cc..',
    '.......',
    '..g.ll.',
    '.......',
    '.vvv...',
    '.......',
]


# the same monitor showing a sad blue error screen, or a big green check
MON_ERROR = ['bbbbbbb', 'bbWbWbb', 'bbbbbbb', 'bbWWWbb', 'bWbbbWb']
MON_DONE = ['KKKKKKK', 'KKKKKgK', 'KKKKgKK', 'KgKgKKK', 'KKgKKKK']


def _monitor_with(screen, led='g', name='monitor'):
    """9x9 monitor: silver-glinted gray bezel around a 7x5 screen, power LED, neck and foot."""
    rows = ['mNNNNNNNN']
    rows += ['N' + s + 'N' for s in screen]
    rows += ['NNNNNNN' + led + 'N', '...NNn...', '..mNNNN..']
    return bc(rows, name)


def _monitor(k):
    return _monitor_with([MON_PAGE[(2 * k + r) % len(MON_PAGE)].replace('.', 'K') for r in range(5)])


# 2-cell keycaps over a row with the long spacebar in the middle
KEYBOARD_ROWS = [
    'mmNmmNmmNmm',
    'NNNmmmmmNNN',
]
_KEYCAPS = [(0, 1), (3, 4), (6, 7), (9, 10)]


def _keyboard(caps=(), space=False):
    rows = [list(r) for r in KEYBOARD_ROWS]
    for c in caps:
        for x in _KEYCAPS[c]:
            rows[0][x] = 'c'
    if space:
        for x in range(3, 8):
            rows[1][x] = 'c'
    return bc([''.join(r) for r in rows], 'keyboard_tap')


# armrests sit at seat level, so nothing sticks out beside his arms (or under a monitor on the desk)
CHAIR_ROWS = [
    '...bbbbbbbbb...',
    '.bbBBBBBBBBBBB.',
    '.bBBBBBBBBBBBB.',
    '.bBBBBBBBBBBBB.',
    '.bBBBBBBBBBBBB.',
    '..BBBBBBBBBBB..',
    'NNbbbbbbbbbbbNN',
    '.BBBBBBBBBBBBB.',
    '.......N.......',
    '..NnnnnnnnnnN..',
    '..N....N....N..',
]

# Slouchy beanbag in two parts so he sinks in: the back (drawn before him) is a U, high and lit on
# the left, slumped and shaded on the right, and never rises behind his face (eye holes stay clear,
# whatever he glances at); the front lip (drawn after him) hides his legs.
BEANBAG_ROWS = [
    '...lll...............',
    '.llvvvl..............',
    'llvvvvvl........vvV..',
    'lvvvvvvv......vvvvVV.',
    'lvvvvvvvvlllvvvvvvvVV',
    'lvvvvvvvvvvvvvvvvvvVV',
    'vvvvvvvvvvvvvvvvvvvVV',
    '.VVVVVVVVVVVVVVVVVVV.',
]
BEANBAG_FRONT_ROWS = [
    '.lvvvvlllllllllvvvvV.',
    'lvvvvvvvvvvvvvvvvvvVV',
    '.VVVVVVVVVVVVVVVVVVV.',
]

# ---------------------------------------------------------------- paper
# The stacks share one look (silver contour, lit top sheet, 2-row bundles: page edges over their
# shade) and one base: every bottom row spans dx -4..4 of the anchor, so swapping
# tall -> mid -> low -> paper_cube at one spot never moves the pile. compacting.py slices
# paper_stack_tall by rows: clip 0-1, top 2-3, four bundles 4-11, base 12-13 (keep that layout).
STACK_TALL = [
    '..m.m.....',
    '..nnn.....',
    '.mmmmmmm..',
    'mWWWWWWWm.',
    'mwwwwwwwm.',
    'mMMMMMMMm.',
    '.mwwwwwwwm',
    '.mMMMMMMMm',
    '.mwwwwwwwm',
    '.mMMMMMMMp',
    'mwwwwwwwm.',
    'mMMMMMMMm.',
    'mwwwwwwwm.',
    'mmmmmmmmm.',
]
STACK_MID = [
    '.mmmmmmm..',
    'mWWWWWWWm.',
    'mwwwwwwwm.',
    'mMMMMMMMm.',
    '.mwwwwwwwm',
    '.mMMMMMMMm',
    'mwwwwwwwm.',
    'mmmmmmmmm.',
]
STACK_LOW = [
    '.mmmmmmm..',
    'mWWWWWWWm.',
    '.mwwwwwwwm',
    '.mMMMMMMMm',
    'mmmmmmmmm.',
]
# 3/4 view: lit top face, layered front, shaded right face, one strap over the top and down the front
CUBE_ROWS = [
    '..mmmmmm.',
    '.mWWbWWmm',
    'mmmmBmmMm',
    'mwwwbwwMm',
    'mMMMbMMMm',
    'mwwwbwwMm',
    'mmmmbmmm.',
]
SHEET_FRAMES = [
    ['mmm...', 'mWwmm.', 'mwwwwm', '.mwwwm', '..mwwm', '...mmm'],
    ['mmmmm.', 'mWwwmm', 'mwwwwm', 'mwwwwm', 'mwwwwm', 'mmmmmm'],
    ['...mmm', '.mmwwm', 'mWwwwm', 'mwwwm.', 'mwwmm.', 'mmm...'],
]


# ---------------------------------------------------------------- props
def _hourglass(top, bot, stream):
    rows = [list('.ttttt.'), list('tTTTTTd')]
    shape = {0: (1, 5), 1: (2, 4), 2: (3, 3), 3: (2, 4), 4: (1, 5)}
    for y in range(5):
        r = ['.'] * 7
        a, b = shape[y]
        for x in range(a, b + 1):
            r[x] = 'C'
        r[a] = r[b] = 'c'
        rows.append(r)
    rows += [list('tTTTTTd'), list('.TTTTd.')]
    for (x, y) in top | bot:
        rows[2 + y][x] = 'j'
    for pile in (top, bot):
        for (x, y) in pile:
            wall = x in shape[y]
            if (x, y - 1) not in pile and not wall:
                rows[2 + y][x] = 'y'          # lit surface of the pile; sand on the glass wall stays gold
    if stream:
        rows[4][3] = 'y'
        if rows[5][3] in 'Cc':
            rows[5][3] = 'y'
    if rows[2][2] == 'C':
        rows[2][2] = 'W'
    return bc([''.join(r) for r in rows], 'hourglass')


# the flip: turned on its side (rotated a quarter), resting on the rims of its two caps; all the sand
# lies in the old bottom bulb, now on the left. Same bottom-center anchor, so it pivots on its spot.
HOURGLASS_FLIP = [
    '.t.....t.',
    'tTj...cTT',
    'tTyj.cWTT',
    'tTjjcCCTT',
    'tTjj.cCTT',
    'tTj...cTd',
    '.d.....d.',
]

_R0 = {(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)}
_R1 = {(2, 1), (3, 1), (4, 1)}
_R3 = {(2, 3), (3, 3), (4, 3)}
_R4 = {(1, 4), (2, 4), (3, 4), (4, 4), (5, 4)}
HOURGLASS_FRAMES = [
    _hourglass(_R0 | _R1, {(3, 4)}, True),
    _hourglass({(1, 0), (2, 0), (4, 0), (5, 0)} | _R1, {(2, 4), (3, 4), (4, 4)}, True),
    _hourglass({(1, 0), (5, 0)} | _R1, _R4, True),
    _hourglass(_R1, _R4 | {(3, 3)}, True),
    _hourglass({(3, 1)}, _R4 | _R3, True),
    _hourglass(set(), _R4 | _R3, False),
    bc(HOURGLASS_FLIP, 'hourglass'),
]

FLAMES = [
    ['...r...', '..rr...', '..ror..', '.royor.', '.rYyor.', 'rooYyor'],
    ['...r...', '...rr..', '..ror..', '.royyr.', '.royYr.', 'royYoor'],
    ['..r....', '..rr...', '.rorr..', '.ryoor.', '.rYyor.', 'roYyoor'],
    ['....r..', '...rr..', '..roor.', '.royor.', '.roYyr.', 'rooYyor'],
]
# two crossed logs glowing at the crossing, a ring of stones hugging them
LOGS = [
    'tTRoyoRTd',
    'dtTd.dTTd',
    'mNdtTTdmN',
]


def _campfire(k):
    rows = ['.' + r + '.' for r in FLAMES[k]] + LOGS
    return bc(rows, 'campfire')


# five spiky leaves fanning out of the pot: lime tips, green blades, dark green where they gather
PLANT_ROWS = [
    '....a....',
    '..a.a.a..',
    '..a.g.g..',
    'a..ggG..a',
    '.a.gGG.G.',
    '..ggGGG..',
    '..gGGGG..',
    '.OooooOO.',
    '..OooOR..',
    '..OOORR..',
    '...RRR...',
]

# Luxo-style desk lamp: green dome shade with a warm bulb, a '>' jointed arm, a weighted dome foot
LAMP_ROWS = [
    '..ggg...',
    '.ghggN..',
    'ghgggGN.',
    '.jYyj..N',
    '......N.',
    '.....N..',
    '...mNNn.',
    '..mNNNNn',
]

# side flaps in the darker inner-cardboard tone, so his raised / waving arms read in front of them
BOX_ROWS = [
    'TT...........TT',
    '.TT.ttttttt.TT.',
    '..tdddddddddt..',
    '..ttttttttttT..',
    '..tTTTTTTTTTd..',
    '..tTTTTTwwmTd..',
    '..tTTTTTmmmTd..',
    '..tTTTTTTTTTd..',
]
BOX_FRONT_ROWS = ['.' * 15] * 3 + BOX_ROWS[3:]


# ---------------------------------------------------------------- music
# Two turntables (silver plinths split by a steel seam) and a row of glowing pads. Each record has a
# colored label and a chrome tone arm: gray pivot on the back edge, headshell resting on the record.
# vibe.py splits this sprite at column 8 (keep 17x5: platters x 1-7 / 9-15, pads on row 4).
_ORBIT = [(2, 0), (4, 0), (4, 2), (2, 2)]          # spin mark, platter coords: a clockwise square


def _platter(k, label):
    p = [list('mKKKKKS'), list('KKK' + label + 'KSK'), list('mKKKKKm')]
    mx, my = _ORBIT[k % 4]
    p[my][mx] = 'N'
    return [''.join(r) for r in p]


def _decks(k):
    L, R = _platter(k, 'r'), _platter(k, 'y')
    rows = ['mmmmmmmNsmmmmmmNm']
    for i in range(3):
        rows.append('m' + L[i] + 's' + R[i] + 'm')
    rows.append('NccNccNNnNNppNppN')
    return bc(rows, 'dj_decks')


def _speaker(pump):
    cone = ['nnn', 'nmn', 'nnn'] if not pump else ['NNN', 'NSN', 'NNN']
    rows = ['mNNNNNN', 'NnnKnnN', 'NnKSKnN', 'NnnKnnN', 'NnKKKnN']
    rows += ['NK' + c + 'KN' for c in cone]
    rows += ['NnKKKnN', 'NNNNNNN']
    return bc(rows, 'speaker')


# ---------------------------------------------------------------- mini clawd
MINI = ['.#####.', '##_#_##', '.#####.', '.#...#.']
MINI_WALK = [
    ['.#####.', '##_#_##', '.######', '.#...#.'],
    ['.#####.', '##_#_##', '.#####.', '..#.#..'],
    ['.#####.', '##_#_##', '######.', '.#...#.'],
    ['.#####.', '##_#_##', '.#####.', '..#.#..'],
]
MINI_CARRY = [
    ['ttttttT', 'tdTTTdT', 'TTTTTTd', '#.....#', '#######', '##_#_##', '.#####.', '.#...#.'],
    ['ttttttT', 'tdTTTdT', 'TTTTTTd', '#.....#', '#######', '##_#_##', '.#####.', '..#.#..'],
]

MINI_TYPE = [
    ['.#####.', '.#_#_##', '#NNNNN.', '.NnpnN.', '.smmms.'],
    ['.#####.', '##_#_#.', '.NNNNN#', '.NnpnN.', '.smmms.'],
]

BLOCK_ROWS = [
    'ttttttT',
    'tdddddT',
    'tdTTtdT',
    'tdTtTdT',
    'tdtTTdT',
    'tdddddT',
    'TTTTTTd',
]

SKATE_ROWS = [
    'r...........r',
    '.rrrrrrrrrrr.',
    '..ss.....ss..',
    '..yy.....yy..',
]

CLOUD_ROWS = [
    '......lll......',
    '..ll.lWWLl.ll..',
    '.lWLlWWLLLlWLl.',
    'lLLLLLLLLLLLLLl',
    'llLLLLLLLLLLLll',
    '.lllllllllllll.',
]

MOON_FRAMES = [
    ['...jjj...', '..jyyy.j.', '.jyYy.jyj', '.jyy...j.', '.jyy.....', '.jyyy..j.', '..jyyy...', '...jjj...'],
    ['...jjj...', '..jyyy...', '.jyYy..j.', '.jyy.....', '.jyy...j.', '.jyyy.jyj', '..jyyy.j.', '...jjj...'],
]

TRASH_ROWS = [
    '..sNs..',
    '.mmmmm.',
    'msssssN',
    '.mSmSs.',
    '.mSmSs.',
    '.mSmSs.',
    '.mSmSs.',
    '.sssss.',
]


# ---------------------------------------------------------------- extras (plan / vibe sets)
BOOKSHELF_ROWS = [
    'ttttttttt',
    'TrbdgddpT',
    'TrbygdpdT',
    'TrbygpddT',
    'TTTTTTTTT',
    'TdcoddhdT',
    'TBcoRhGhT',
    'TBcoROOOT',
    'TTTTTTTTT',
    'TyddddvdT',
    'TybRRRvcT',
    'TybBBBvcT',
    'TTTTTTTTT',
    'TT.....TT',
]

CORKBOARD_ROWS = [
    'TTTTTTTTTTTTT',
    'TtttttprptttT',
    'TyryttppptttT',
    'TyyytttttcrcT',
    'TttttttttcccT',
    'TttarattttttT',
    'TttaaattlrltT',
    'TtttttttllltT',
    'TTTTTTTTTTTTT',
]

_DISCO = [
    '...N...',
    '...N...',
    '...N...',
    '..mSm..',
    '.mSmSs.',
    'mSmSmSs',
    'mmSmSsN',
    'mSmSsNs',
    '.sSsNs.',
    '..sNs..',
]
_DISCO_GLINTS = [[(2, 4), (1, 6)], [(3, 4), (2, 6)], [(4, 4), (3, 6)]]


def _disco(k):
    g = [list(r) for r in _DISCO]
    for (x, y) in _DISCO_GLINTS[k]:
        g[y][x] = 'W'
    rows = [''.join(r) for r in g]
    _check(rows, 'disco_ball')
    return Sprite(rows, anchor=(3, 6), name='disco_ball')


ITEMS = [
    Item('blanket', 'scene',
         'Patchwork quilt with a folded white cuff (13x4); place at (15, 19) after put_clawd: covers him from the waist down, his arms rest on the cuff',
         bc(BLANKET_ROWS, 'blanket'),
         preview={'at': (15, 19), 'z': 'front'}, tags=('sleep', 'bed')),
    Item('blanket_breathe', 'scene',
         'blanket breathing in: the middle of the cuff (over his chest) lifts 1 row, tucked corners stay; alternate with blanket (~1400/1100 ms), same anchor (15, 19), after put_clawd',
         bc(BLANKET_BREATHE_ROWS, 'blanket_breathe'),
         preview={'at': (15, 19), 'z': 'front'}, tags=('sleep', 'bed')),
    Item('pillow', 'ground',
         'Plump pillow with pinched corners (9x5) for the floor or a couch; ground (26, 19) right of Clawd (the bed has its own wide pillow)',
         bc(PILLOW_ROWS, 'pillow'),
         preview={'at': (26, 19), 'z': 'behind'}, tags=('sleep',)),
    Item('bed', 'scene',
         "Wooden bed seen from the foot, built-in pillow frames his head (17x13); place at (15, 19) BEFORE put_clawd, blanket after him; open eyes need clawd(holes=False) (pillow behind his face)",
         bc(BED_ROWS, 'bed'),
         preview={'at': (15, 19), 'z': 'behind'}, tags=('sleep', 'furniture')),
    Item('desk', 'scene',
         'Wooden desk with drawers (19x5); place at (18, 19) after put_clawd to hide his lower body; props stand on its top at y-4 (e.g. monitor at (25, 15))',
         bc(DESK_ROWS, 'desk'),
         preview={'at': (18, 19), 'z': 'front'}, tags=('working', 'plan', 'furniture')),
    Item('laptop_back', 'ground',
         'Laptop from behind, glowing heart sticker (9x5); place at (15, 19) after put_clawd: eyes peek over, arms free to type',
         bc(LAPTOP_ROWS, 'laptop_back'),
         preview={'at': (15, 19), 'z': 'front'}, tags=('working', 'typing')),
    Item('monitor', 'ground',
         'Monitor with code scrolling up a line per frame (9x9); frames 0-5 loop at ~220 ms; on the desk: desk (18, 19) + monitor (25, 15), 1 cell clear of his head',
         [_monitor(k) for k in range(6)], ms=220,
         preview={'at': (26, 19), 'z': 'behind'}, tags=('working',)),
    Item('monitor_error', 'ground',
         'Monitor with a sad blue error screen and a red power LED (9x9); swap in for monitor at the same spot (desk (18, 19) + (25, 15)) when something fails',
         _monitor_with(MON_ERROR, 'r', 'monitor_error'),
         preview={'at': (26, 19), 'z': 'behind'}, tags=('error', 'working')),
    Item('monitor_done', 'ground',
         'Monitor showing a big green check (9x9); swap in for monitor at the same spot (desk (18, 19) + (25, 15)) when the work is done',
         _monitor_with(MON_DONE, 'g', 'monitor_done'),
         preview={'at': (26, 19), 'z': 'behind'}, tags=('done', 'working')),
    Item('keyboard', 'ground',
         'Keyboard, front view: keycaps and spacebar (11x2); on the desk front at (15, 16), just under his eyes, after the desk',
         bc(KEYBOARD_ROWS, 'keyboard'),
         preview={'at': (15, 16), 'z': 'front'}, tags=('working', 'typing')),
    Item('keyboard_tap', 'ground',
         'keyboard with keys lighting cyan: frame 0 rest, 1-3 key hits (3 = double), 4 spacebar; play in an uneven order at 90-140 ms (e.g. 1,0,2,3,0,4); place like keyboard',
         [_keyboard(), _keyboard([1]), _keyboard([2]), _keyboard([0, 3]), _keyboard(space=True)], ms=120,
         preview={'at': (15, 16), 'z': 'front'}, tags=('working', 'typing')),
    Item('chair', 'scene',
         'Blue office chair with armrests (15x11); place at (15, 19) BEFORE put_clawd: backrest frames him, base peeks between his legs',
         bc(CHAIR_ROWS, 'chair'),
         preview={'at': (15, 19), 'z': 'behind'}, tags=('working', 'furniture')),
    Item('beanbag', 'scene',
         'Slouchy violet beanbag, back part (21x8); place at (15, 19) BEFORE put_clawd (normal body at HOME), then beanbag_front: he sinks in, eyes stay clear',
         bc(BEANBAG_ROWS, 'beanbag'),
         preview={'at': (15, 19), 'z': 'behind'}, tags=('vibe', 'idle', 'furniture')),
    Item('beanbag_front', 'scene',
         'Front lip of beanbag (21x3), same anchor; draw at (15, 19) AFTER put_clawd so his legs sink into the bag',
         bc(BEANBAG_FRONT_ROWS, 'beanbag_front'),
         preview={'at': (15, 19), 'z': 'front'}, tags=('vibe', 'idle', 'furniture')),
    Item('paper_stack_tall', 'ground',
         'Tall messy paper stack with a binder clip and a pink tab (10x14); ground (25, 19) right of Clawd; compacting = swap tall -> mid -> low -> paper_cube at the same anchor',
         bc(STACK_TALL, 'paper_stack_tall', ax=4),
         preview={'at': (25, 19), 'z': 'behind'}, tags=('compacting', 'plan')),
    Item('paper_stack_mid', 'ground',
         'Medium paper stack, one bundle slid aside (10x8); same base as the other stacks: swap in at the same anchor, e.g. (25, 19)',
         bc(STACK_MID, 'paper_stack_mid', ax=4),
         preview={'at': (25, 19), 'z': 'behind'}, tags=('compacting', 'plan')),
    Item('paper_stack_low', 'ground',
         'Low paper stack, two offset bundles (10x5); same base as the other stacks: swap in at the same anchor, e.g. (25, 19)',
         bc(STACK_LOW, 'paper_stack_low', ax=4),
         preview={'at': (25, 19), 'z': 'behind'}, tags=('compacting', 'plan')),
    Item('paper_cube', 'ground',
         'Compressed paper cube in 3/4 view with a blue strap (9x7): what compacting produces; swap in for paper_stack_low at the same anchor',
         bc(CUBE_ROWS, 'paper_cube'),
         preview={'at': (25, 19), 'z': 'behind'}, tags=('compacting',)),
    Item('paper_sheet', 'fx',
         'One flying sheet (6x6); frames tilt left/flat/right: ping-pong 0,1,2,1 at ~120 ms while drifting it along a path',
         [mid(f, 'paper_sheet') for f in SHEET_FRAMES], ms=120,
         preview={'at': (25, 6), 'z': 'front'}, tags=('compacting',)),
    Item('hourglass', 'ground',
         'Hourglass (7x9): frames 0-5 at ~600 ms as the sand runs down, frame 6 (on its side, 9x7) ~140 ms flips it, back to 0: seamless; ground (26, 19) or on the desk top',
         HOURGLASS_FRAMES, ms=[600, 600, 600, 600, 600, 600, 140],
         preview={'at': (26, 19), 'z': 'behind'}, tags=('rate-limit', 'waiting')),
    Item('campfire', 'ground',
         'Campfire: crossed logs, glowing embers, stones (9x9); frames 0-3 loop at ~130 ms, constant size; ground (26, 19) right of Clawd',
         [_campfire(k) for k in range(4)], ms=130,
         preview={'at': (26, 19), 'z': 'behind'}, tags=('idle', 'thinking', 'night')),
    Item('plant', 'ground',
         'Spiky houseplant in a terracotta pot (9x11), a bit taller than Clawd; ground (26, 19) right of him',
         bc(PLANT_ROWS, 'plant'),
         preview={'at': (26, 19), 'z': 'behind'}, tags=('decor',)),
    Item('lamp', 'ground',
         'Jointed desk lamp, green dome shade, warm bulb (8x8); ground (5, 19) left of Clawd, or on the desk top at (x, 15)',
         bc(LAMP_ROWS, 'lamp'),
         preview={'at': (5, 19), 'z': 'behind'}, tags=('plan', 'working', 'night')),
    Item('box', 'scene',
         'Open cardboard box with flaps and label (15x8); place at (15, 19) BEFORE put_clawd, box_front after him: he pops out',
         bc(BOX_ROWS, 'box'),
         preview={'at': (15, 19), 'z': 'behind'}, tags=('hello',)),
    Item('box_front', 'scene',
         'Front face of box, same anchor; draw at (15, 19) AFTER put_clawd so he is inside the box',
         bc(BOX_FRONT_ROWS, 'box_front'),
         preview={'at': (15, 19), 'z': 'front'}, tags=('hello',)),
    Item('dj_decks', 'scene',
         'DJ decks: two turntables with tone arms, spinning records, glowing pads (17x5); frames 0-3 loop at ~150 ms; place at (15, 19) after put_clawd (normal body: eyes peek over)',
         [_decks(k) for k in range(4)], ms=150,
         preview={'at': (15, 19), 'z': 'front'}, tags=('vibe', 'music')),
    Item('speaker', 'ground',
         'Floor speaker (7x10): frame 0 rest, frame 1 woofer pump; alternate on the beat (~300/150 ms); ground (26, 19) beside dj_decks',
         [_speaker(False), _speaker(True)], ms=[300, 150],
         preview={'at': (26, 19), 'z': 'behind'}, tags=('vibe', 'music')),
    Item('mini_clawd', 'ground',
         'Tiny Clawd for subagents (7x4), same 1-cell pixels, see-through eyes; ground: place at (x, 19), e.g. (25, 19)',
         bc(MINI, 'mini_clawd'),
         preview={'at': (25, 19), 'z': 'behind'}, tags=('subagents',)),
    Item('mini_clawd_walk', 'ground',
         'Tiny Clawd walking, legs step and arms swing (7x4); frames 0-3 loop ~130 ms, move him 1 cell per frame',
         [bc(f, 'mini_clawd_walk') for f in MINI_WALK], ms=130,
         preview={'at': (25, 19), 'z': 'behind'}, tags=('subagents',)),
    Item('mini_clawd_carry', 'ground',
         'Tiny Clawd carrying a crate overhead (7x8); frames 0-1 loop ~160 ms, move him 1 cell per frame',
         [bc(f, 'mini_clawd_carry') for f in MINI_CARRY], ms=160,
         preview={'at': (25, 19), 'z': 'behind'}, tags=('subagents', 'edits')),
    Item('mini_clawd_type', 'ground',
         'Tiny Clawd typing on a tiny heart-sticker laptop (7x5); frames 0-1 alternate his arms at ~150 ms; ground, e.g. (4, 19) left of Clawd',
         [bc(f, 'mini_clawd_type') for f in MINI_TYPE], ms=150,
         preview={'at': (25, 19), 'z': 'behind'}, tags=('subagents', 'working')),
    Item('block', 'ground',
         'Wooden crate / building block (7x7); ground (26, 19); stack the next one at y-7',
         bc(BLOCK_ROWS, 'block'),
         preview={'at': (26, 19), 'z': 'behind'}, tags=('subagents', 'edits')),
    Item('skateboard', 'scene',
         'Skateboard (13x4); to ride: put_clawd(f, p, x-5, y-10) (feet on the deck, 3 rows above HOME: hop on, or accept the off-HOME frame 0), then the board at (x, y) after him',
         bc(SKATE_ROWS, 'skateboard'),
         preview={'at': (15, 19), 'z': 'front'}, tags=('bypass',)),
    Item('cloud_platform', 'scene',
         'Fluffy cloud, lilac with white tops (15x6); to ride: put_clawd(f, p, x-5, y-9) (2 rows above HOME), cloud at (x, y) after him: his legs sink in',
         bc(CLOUD_ROWS, 'cloud_platform'),
         preview={'at': (15, 19), 'z': 'front'}, tags=('auto',)),
    Item('moon', 'fx',
         'Crescent moon with two twinkling stars (8x8); frames 0-1 alternate ~900 ms; anchor = moon center, e.g. (26, 5) or (5, 5)',
         [mid(f, 'moon') for f in MOON_FRAMES], ms=900,
         preview={'at': (26, 5), 'z': 'behind'}, tags=('sleep', 'night')),
    Item('trash_bin', 'ground',
         'Metal trash / compactor bin with lid and handle (7x8); ground (26, 19); arc paper_sheet into it',
         bc(TRASH_ROWS, 'trash_bin'),
         preview={'at': (26, 19), 'z': 'behind'}, tags=('compacting',)),
    Item('bookshelf', 'scene',
         'Wooden bookshelf: colorful books, a leaning book, a tiny plant (9x14); stand it at (26, 19) right of Clawd',
         bc(BOOKSHELF_ROWS, 'bookshelf'),
         preview={'at': (26, 19), 'z': 'behind'}, tags=('plan', 'decor')),
    Item('corkboard', 'scene',
         'Wall corkboard with pinned sticky notes (13x9); hang it high: bottom-center (24, 9) top right, or (7, 10) above-left of him',
         bc(CORKBOARD_ROWS, 'corkboard'),
         preview={'at': (24, 9), 'z': 'behind'}, tags=('plan', 'decor')),
    Item('disco_ball', 'fx',
         'Mirror disco ball on a string (7x10); frames 0-2 loop at ~220 ms as glints travel; anchor = ball center, (x, 6) hangs it from the top edge',
         [_disco(k) for k in range(3)], ms=220,
         preview={'at': (4, 6), 'z': 'behind'}, tags=('vibe', 'music')),
]
