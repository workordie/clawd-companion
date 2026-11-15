"""Hand props for Clawd: things he holds (mug, phone, tools, signs, snacks, party stuff ...).

Anchor convention for the 'hand' slot: each sprite's anchor is its GRIP cell, the cell just outside his
right hand. Where that lands in his 11x8 box depends on the arm:
    rarm='side' -> (11, 3)   'up' -> (11, 1)   'raise' -> (11, -1)   'out' -> (12, 2)   'high' -> (10, -1)
    'down' -> (11, 4)   'wave' -> (12, -1)   'front' -> (8, 3)
Props extend right/up from the grip and stay clear of his body. The one deliberate exception is the
two-handed controller, which he holds in front of his tummy. wear(f, item, pose, side='l') mirrors a
prop into his left hand automatically. Each desc names the arm pose the prop was designed for. The
stock contact sheet previews every hand prop with rarm='side' only, so props designed for other poses
look offset there.

Left-hand caveat: mirroring also flips text and asymmetric glyphs. The placards (sign_*) are symmetric
around their stick, so for the left hand place them unmirrored to keep '?', 'HI' and the check readable:
    f.place(get('sign_question').sprite(), *pose.at('hand_l'))
Animated: frame order and ms are in each desc; ms may be a list (one value per frame).
"""
from clawdlib import Item, Sprite


def _sp(rows, anchor):
    return Sprite(rows, anchor=anchor)


def _grid(w, h):
    return [['.'] * w for _ in range(h)]


def _rows(g):
    return [''.join(r) for r in g]


def _line(x0, y0, x1, y1):
    """Bresenham cells from (x0, y0) to (x1, y1), both ends included."""
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def _over(base, rows, ox=0, oy=0):
    """`base` with `rows` drawn on top, the rows' top-left at (ox, oy) in base's space ('.' keeps,
    '_' erases). The anchor stays the base's."""
    cells = {(x, y): ch for x, y, ch in base.cells}
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch == '_':
                cells.pop((ox + i, oy + j), None)
            elif ch != '.':
                cells[(ox + i, oy + j)] = ch
    return Sprite(cells=[(x, y, ch) for (x, y), ch in cells.items()], anchor=(base.ax, base.ay))


# =====================================================================================================
# Drinks, devices, paper
# =====================================================================================================
# The mug keeps its handle toward his hand, so it also stands on a surface with the handle facing
# Clawd and its coffee centred (typing.py re-anchors it on the input box under a steam wisp). In his
# hand that handle merges into his arm, so mug_held turns the same mug round: handle out.
MUG = Item('mug', 'hand', "Blue coffee mug held by its handle (handle toward his hand); also stands on a surface "
           "(re-anchor to its bottom row). rarm='side' to hold, 'up' to sip with eyes='look_u' or a short "
           "eyes='blink' (~140 ms). For a mug in his hand that must read at 3 px, prefer mug_held.", _sp([
               '..cTTB',
               'bbcbbB',
               'b.cbbB',
               'bbcbbB',
           ], (0, 2)), tags=('idle', 'coffee', 'working'))

MUG_HELD = Item('mug_held', 'hand', "The blue coffee mug held by the cup with its handle out, so the D-shaped handle "
                "stays free and reads at real size. rarm='side' to hold, 'up' to sip (eyes='look_u' or a short "
                "blink). Steam: the fx 'steam' with its anchor at grip + (1, -5).", _sp([
                    'cTTB..',
                    'cbbBbb',
                    'cbbB.b',
                    'cbbBbb',
                ], (0, 2)), tags=('idle', 'coffee', 'working'))

# A social feed, 3 cells wide and 6 rows long: blue post, caption, pink post, caption. Each frame shows
# 4 rows of it, 2 rows further down, so the loop always scrolls up.
_FEED = ['bbC', 'bbC', 'ccC', 'ppC', 'ppC', 'ccC']


def _phone(k):
    screen = [_FEED[(2 * k + i) % len(_FEED)] for i in range(4)]
    return _sp(['.mkm.'] + ['m' + row + 'N' for row in screen] + ['.NNN.'], (0, 4))


PHONE = Item('phone', 'hand', "Silver smartphone with a lit feed that scrolls up: frames 0-2 loop at ~650 ms (each "
             "frame scrolls the feed 2 rows; vary the holds for a natural thumb-scroll). Hold with rarm='up' (beside "
             "his face, pair with eyes='look_r') or 'side'.", [_phone(0), _phone(1), _phone(2)], ms=650,
             tags=('idle', 'rate-limit', 'waiting'))

BOOK = Item('book', 'hand', "Open red hardcover held up to read or show: lit left page, shaded right page. "
            "Hold with rarm='up' (eyes='look_r' to read).", _sp([
                '.mmm.mmm.',
                'rwwwNMMMR',
                'rwmmNMmmR',
                'rwwwNMMMR',
                'rwmmNMmmR',
                '.rrrRRRR.',
            ], (0, 4)), tags=('plan', 'thinking', 'read'))

CLIPBOARD = Item('clipboard', 'hand', "Clipboard: steel clip, paper with two ticked checklist items and one still "
                 "open. Hold with rarm='side' or 'up'.", _sp([
                     '..mmm..',
                     'ttsSstT',
                     'twwwwwT',
                     'tgwgmmT',
                     'twgwwwT',
                     'tgwgmmT',
                     'twgwwwT',
                     'twNwmmT',
                     'TTTTTTT',
                 ], (0, 7)), tags=('plan', 'working', 'edits'))

MAGNIFIER = Item('magnifier', 'hand', "Magnifying glass: gold rim, glass with a glint, wood handle = grip. "
                 "rarm='side' or 'up' (searching, inspecting).", _sp([
                     '...yjj.',
                     '..yWCCJ',
                     '..jCCcJ',
                     '..jCccJ',
                     '...JJJ.',
                     '..J....',
                     '.T.....',
                     'T......',
                 ], (0, 7)), tags=('thinking', 'question', 'search'))


# =====================================================================================================
# Tools
# =====================================================================================================
WRENCH = Item('wrench', 'hand', "Chunky steel open-end wrench, jaw up, handle = grip. rarm='side' to hold, 'up' or "
              "'raise' to brandish (working, fixing).", _sp([
                  '...m.s.',
                  '..ms.ss',
                  '..ms.sN',
                  '..sssN.',
                  '.msN...',
                  'msN....',
                  'sN.....',
              ], (0, 6)), tags=('working', 'error', 'tool'))

# Hammer swing set: hammer (upright) -> hammer_up (45 deg) -> hammer_hit (level, face down). The same
# head in all three: claw end tapered, striking face blunt. The face is on the right of the upright
# head, so it leads the swing and lands facing down. Light stays top-left in every frame.
HAMMER = Item('hammer', 'hand', "Claw hammer held upright (wood handle, steel head, face on the right). rarm='side' "
              "at rest, rarm='raise' as the wind-up of a swing.", _sp([
                  'mmssN',
                  '.mssN',
                  '..T..',
                  '..T..',
                  '..T..',
                  '..T..',
                  '..T..',
              ], (2, 6)), tags=('working', 'edits', 'tool'))

HAMMER_UP = Item('hammer_up', 'hand', "Hammer swung to 45 deg mid-swing: claw up-left, blunt face down-right, the same "
                 "head as 'hammer'. Use rarm='raise' or 'up' between 'hammer' (rarm='raise') and 'hammer_hit' "
                 "(rarm='out' or 'wave') for a ~60-90 ms swing frame.", _sp([
                     '...m....',
                     '...ms...',
                     '....ss..',
                     '...T.sN.',
                     '..T...NN',
                     '.T......',
                     'T.......',
                 ], (0, 6)), tags=('working', 'tool'))

HAMMER_HIT = Item('hammer_hit', 'hand', "Hammer at the end of a swing: level handle, head striking downward. Use with "
                  "rarm='out' (or 'wave'); the striking face's bottom cells are 2 rows below the grip, 4-5 cells "
                  "right.", _sp([
                      '....m.',
                      '....ms',
                      'TTTTss',
                      '....sN',
                      '....sN',
                  ], (0, 2)), tags=('working', 'tool'))

FISHING_ROD = Item('fishing_rod', 'hand', "Fishing rod held up and out: cork handle + reel at the grip, rod rising "
                   "to its tip 8 right/6 up of the grip; the line hangs from (8,-5) to a red-pink bobber at "
                   "(8,-2)..(8,-1) (offsets from the grip). Frame 1 = a bite: the rod bows, its tip dips 4 rows "
                   "and the bobber is yanked 4 rows down to (8,2)..(8,3); flick 0/1 at ~120 ms. Longer line: extra "
                   "'m' cells at x+8, bobber below them. rarm='out' or 'up'.", [
                       _sp(['.......TT',
                            '.....TT.m',
                            '....T...m',
                            '...T....m',
                            '..T.....r',
                            '.ts.....p',
                            't........'], (0, 6)),
                       _sp(['....TTT..',
                            '...T...T.',
                            '..T.....T',
                            '.ts.....m',
                            't.......m',
                            '........m',
                            '........r',
                            '........p'], (0, 4)),
                   ], ms=[900, 120], tags=('hooks', 'idle', 'fishing'))

FISH = Item('fish', 'fx', "Blue fish (8x4, about his body width) flopping: frames 0-1 alternate the tail flick at "
            "~150 ms. Anchor = body center. To hang a catch, put its mouth (0,2) under the line's end: anchor = "
            "(line_x + 3, line_end_y + 1), and drop the bobber.", [
                _sp(['...BB...',
                     '.bbbbb.B',
                     'bkbbbbB.',
                     '.ccccb.B'], (3, 2)),
                _sp(['...BB.BB',
                     '.bbbbbB.',
                     'bkbbbb..',
                     '.ccccb..'], (3, 2)),
            ], ms=150, tags=('hooks', 'fishing'))

CONTROLLER = Item('controller', 'hand', "Game controller held at tummy height with BOTH hands: use larm='front', "
                  "rarm='front' and wear it once on the right hand (d-pad left, 4 buttons right; it covers the tops "
                  "of his inner legs). Pair with eyes='look_d' (eyes on the game), 'open' or 'look_u'; avoid "
                  "look_l, look_r, look_dl and look_dr (with both arms in front they put an eye on his body edge "
                  "or on a forearm).", _sp([
                      'mKmmmrm',
                      'KKKmgmb',
                      'NKN.NyN',
                  ], (6, -1)), tags=('idle', 'vibe', 'game'))

PENCIL = Item('pencil', 'hand', "Big yellow pencil held by the eraser end, tip up-right (pink eraser, steel "
              "ferrule, sharpened graphite tip). rarm='side' or 'up'; wiggle between them to 'write' in the air.", _sp([
                  '........N',
                  '.......tt',
                  '......yj.',
                  '.....yj..',
                  '....yj...',
                  '...yj....',
                  '..yj.....',
                  '.ms......',
                  'pr.......',
              ], (0, 8)), tags=('edits', 'plan', 'typing'))

PAINTBRUSH = Item('paintbrush', 'hand', "Paintbrush: red handle, steel ferrule, tan bristles dipped in blue paint, "
                  "tip up-right. rarm='side' or 'up'.", _sp([
                      '.......b',
                      '......cb',
                      '.....cbB',
                      '....ttT.',
                      '...msN..',
                      '..msN...',
                      '..r.....',
                      '.r......',
                      'r.......',
                  ], (0, 8)), tags=('edits', 'creative'))

# =====================================================================================================
# Fun & party
# =====================================================================================================
_BALLOON = ['.rrr.',
            'rWrrr',
            'rrrrR',
            'rrrrR',
            '.rRR.',
            '..R..']


def _balloon(dx):
    g = _grid(7, 11)
    for y, row in enumerate(_BALLOON):
        for x, ch in enumerate(row):
            if ch != '.':
                g[y][x + 1 + dx] = ch
    for x, y in _line(3 + dx, 6, 3, 10):
        g[y][x] = 'N'
    return _sp(_rows(g), (3, 10))


BALLOON = Item('balloon', 'hand', "Red balloon on a string, string end = grip, floats 5 rows above the hand. "
               "Gentle sway: play frames 0,1,0,2 at ~450 ms (0 = upright still). rarm='side' or 'up'.",
               [_balloon(0), _balloon(-1), _balloon(1)], ms=450, tags=('done', 'hello', 'party'))


def _flag(offs):
    """Racing flag: a 6x6 cloth (5x4 black/white checks inside a silver hem on the top, bottom and free
    edge, so it holds on both themes) on a steel pole. offs[c] lifts cloth column c by one row."""
    g = _grid(7, 11)
    g[0][0] = 'j'
    for y in range(1, 11):
        g[y][0] = 's'
    for c in range(6):
        for r in range(6):
            ch = 'm' if r in (0, 5) or c == 5 else ('K' if (r + c) % 2 else 'W')
            g[1 + r + offs[c]][1 + c] = ch
    return _sp(_rows(g), (0, 10))


CHECKERED_FLAG = Item('checkered_flag', 'hand', "Finish-line flag on a steel pole with a gold knob: black and white "
                      "checks in a silver hem; a wave travels out along the cloth: frames 0-3 loop seamlessly at "
                      "~150 ms (0 is a fine still). rarm='raise' to wave it overhead, 'side' or 'up' to hold.",
                      [_flag([0, 0, 1, 1, 0, 0]), _flag([0, 0, 0, 1, 1, 0]), _flag([0, 0, 0, 0, 1, 1]),
                       _flag([0, 1, 1, 0, 0, 1])], ms=150, tags=('done', 'finish'))


_TROPHY = ['..yyjjJ..',
           '.jyjjjJJ.',
           'j.yjjjJ.J',
           '.jjjjjJJ.',
           '...jjJ...',
           '....j....',
           '...jjJ...',
           '..JJJJJ..']
TROPHY = Item('trophy', 'hand', "Gold cup trophy with two handles, held by the left corner of its base. Frame 0 = "
              "still, frame 1 = a white glint on the cup (flash it ~120 ms every few seconds). rarm='raise' holds "
              "it up beside his head (done!), 'up' to show it off.", [
                  _sp(_TROPHY, (2, 7)),
                  _sp(_TROPHY, (2, 7)).over(_sp(['....', '...W', '...WY'], (0, 0))),
              ], ms=[1600, 120], tags=('done', 'win'))

# Party popper: a cone from the grip (0, 8) up-right to a 45-degree gold lip on x - y = 1, banded pink /
# yellow like the party hat (each band darker along its lower edge).
_POPPER = ['...j......',
           '...pj.....',
           '..yppj....',
           '..yyprJ...',
           '.ppjj.....',
           '.yr.......',
           'j.........']


def _popper(rows, top):
    base = _sp(['..........', '..........'] + _POPPER, (0, 8))
    return _over(base, rows, 0, top)


PARTY_POPPER = Item('party_popper', 'hand', "Striped party-popper cone (pink and yellow bands like the party hat, "
                    "gold lip), tip in his hand, mouth up-right. Frames: 0 = loaded (two streamers peek out, a good "
                    "still); 1 = POP (streamers whip out, confetti specks fly), a one-shot ~90 ms: on the same tick "
                    "spawn the fx 'confetti_burst' with its anchor at the mouth, grip + (5, -5); 2 = spent (limp "
                    "streamers hang out), hold it. rarm='up' or 'raise'.", [
                        _popper(['.....c....',
                                 '.....c....',
                                 '....c.....',
                                 '..........',
                                 '......vv..'], 0),
                        _popper(['....p..c.',
                                 '..y....c.',
                                 '......c..',
                                 '.....c..g',
                                 '....c....',
                                 '......vv.',
                                 '........v'], -2),
                        _popper(['....c.....',
                                 '.....c....',
                                 '......v...',
                                 '.......v..',
                                 '.......v..'], 2),
                    ], ms=[1200, 90, 1200], tags=('done', 'party'))

MICROPHONE = Item('microphone', 'hand', "Handheld mic: silver mesh ball, red band, steel handle = grip. rarm='up' "
                  "(singing, announcing) or 'side'.", _sp([
                      '.mm.',
                      'mSms',
                      'mssN',
                      '.sN.',
                      '.rR.',
                      '.sN.',
                      '.sN.',
                      '..N.',
                  ], (1, 6)), tags=('vibe', 'hello', 'music'))

COWBELL = Item('cowbell', 'hand', "Steel cowbell (phonk!) with a clapper, held out by its short wooden side "
               "handle, mouth down. Frame 0 = still, frame 1 = ring (clapper swings, gold 'ding' rays): play 1 for "
               "~110 ms on each beat. rarm='up' to show it off, or 'side' (the ring rays need 9 cells to the right).", [
                   _sp(['...mmN..',
                        '...mSN..',
                        'TTmSssN.',
                        '..mSssN.',
                        '..mSssN.',
                        '..NnnnN.',
                        '....N...'], (0, 2)),
                   _sp(['...mmN...j',
                        '...mSN..j.',
                        'TTmSssN...',
                        '..mSssN...',
                        '..mSssN.j.',
                        '..NnnnN..j',
                        '.....N....'], (0, 2)),
               ], ms=[320, 110], tags=('vibe', 'music', 'phonk'))

DRUMSTICK = Item('drumstick', 'hand', "Wooden drumstick with a light bead tip. 0 = raised (tip 3 right, 5 up of the "
                 "grip), 1 = strike (tip 5 right, 2 down), 2 = mid-swing (level, tip 5 right, 1 up). Hold 0 ~300 ms, "
                 "then 2 for ~60 ms and 1 for ~110 ms (or 0 -> 1 for a snappier hit). rarm='up' or 'out'.", [
                     _sp(['...t',
                          '..T.',
                          '..T.',
                          '.T..',
                          '.T..',
                          'T...'], (0, 5)),
                     _sp(['TT....',
                          '..TT..',
                          '....Tt'], (0, 0)),
                     _sp(['....Tt',
                          'TTTT..'], (0, 1)),
                 ], ms=[300, 110, 60], tags=('vibe', 'music', 'phonk'))


def _wand(center, spark, sc='l'):
    g = _grid(9, 9)
    star = {(4, 1): 'y', (2, 2): 'y', (3, 2): 'y', (4, 2): center, (5, 2): 'y', (6, 2): 'j',
            (3, 3): 'y', (4, 3): 'y', (5, 3): 'j', (3, 4): 'y', (5, 4): 'j'}
    for (x, y), ch in star.items():
        g[y][x] = ch
    for x, y in [(4, 4), (3, 5), (2, 6), (1, 7), (0, 8)]:
        g[y][x] = 'v'
    for x, y in spark:
        g[y][x] = sc
    return _sp(_rows(g), (0, 8))


WAND = Item('wand', 'hand', "Magic wand: violet stick with a gold star; frames 0-1 twinkle (the star core flashes "
            "and lavender sparkles hop around it) at ~260 ms. rarm='raise' to cast, 'up' or 'side' to hold.",
            [_wand('Y', [(7, 1)]), _wand('W', [(2, 0), (8, 4)])], ms=260,
            tags=('auto', 'magic', 'done'))

UMBRELLA = Item('umbrella', 'hand', "Open violet umbrella for rain: domed canopy 15 wide with a scalloped edge, "
                "shaft = grip. rarm='side' holds the canopy snugly over his head (shelter; 'down' sits a row lower), "
                "'up' a row higher, 'high' raises it well above him (a flourish). It is centred on his hand, so it "
                "covers his right side most.", _sp([
                    '.......N.......',
                    '....llvvvVV....',
                    '..llvvvvvvVVV..',
                    '.llvvvvvvvvVVV.',
                    'llvvvvvvvvvvVVV',
                    'l...v..N..V...V',
                    '.......N.......',
                    '.......N.......',
                    '.......N.......',
                    '.......N.......',
                    '.......T.......',
                ], (7, 10)), tags=('rain', 'rate-limit'))


def _sign(base, shade, glyph):
    g = _grid(7, 11)
    for y in range(7):
        for x in range(7):
            if (x in (0, 6)) and (y in (0, 6)):
                continue
            g[y][x] = shade if (x == 6 or y == 6) else base
    for x, y in glyph:
        g[y][x] = 'W'
    for y in range(7, 11):
        g[y][3] = 'T'
    return _sp(_rows(g), (3, 10))


_GLYPH_BANG = [(3, 1), (3, 2), (3, 3), (3, 5)]
_GLYPH_QUESTION = [(2, 1), (3, 1), (4, 2), (3, 3), (3, 5)]
_GLYPH_HEART = [(1, 1), (2, 1), (4, 1), (5, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (2, 3), (3, 3), (4, 3), (3, 4)]
_GLYPH_CHECK = [(5, 1), (4, 2), (5, 2), (1, 3), (3, 3), (4, 3), (1, 4), (2, 4), (3, 4), (2, 5)]

SIGN_BANG = Item('sign_bang', 'hand', "Red placard on a stick with a white '!' (alert, needs permission). "
                 "rarm='up' or 'raise' to wave it ('side' rests the board on his head corner).",
                 _sign('r', 'R', _GLYPH_BANG), tags=('alert',))
SIGN_QUESTION = Item('sign_question', 'hand', "Blue placard on a stick with a white '?' (question). rarm='up' or "
                     "'raise'. Left hand: place it unmirrored (see module doc).", _sign('b', 'B', _GLYPH_QUESTION),
                     tags=('question',))
SIGN_HEART = Item('sign_heart', 'hand', "Pink placard on a stick with a white heart (thanks, love). rarm='up' or "
                  "'raise'.", _sign('p', 'r', _GLYPH_HEART), tags=('done', 'hello', 'love'))
SIGN_OK = Item('sign_ok', 'hand', "Green placard on a stick with a white check mark (done, approved). rarm='up' "
               "or 'raise'. Left hand: place it unmirrored (see module doc).", _sign('g', 'G', _GLYPH_CHECK),
               tags=('done', 'edits'))


def _stopwatch(hand):
    """Paper face (a white glint top-left, a soft shade bottom-right) in a steel rim, red crown button."""
    rows = ['..rrR..',
            '...s...',
            '..mms..',
            '.mwwws.',
            'mwWwwwN',
            'mwwKwwN',
            'swwwwMN',
            '.swwMN.',
            '..sNN..']
    g = [list(r) for r in rows]
    for x, y in hand:
        g[y][x] = 'r'
    return _sp(_rows(g), (0, 6))


STOPWATCH = Item('stopwatch', 'hand', "Stopwatch with a red hand ticking round (12, 3, 6, 9 o'clock). Frames 0-3 "
                 "loop at ~600 ms (rate limit, waiting). rarm='up' or 'side'. In the left hand (mirrored) play "
                 "0,3,2,1 to keep it clockwise.", [
                     _stopwatch([(3, 4), (3, 3)]),
                     _stopwatch([(4, 5), (5, 5)]),
                     _stopwatch([(3, 6), (3, 7)]),
                     _stopwatch([(2, 5), (1, 5)]),
                 ], ms=600, tags=('rate-limit', 'waiting'))

BROOM = Item('broom', 'hand', "Straw broom held upright with rarm='side' (the bristles rest on the ground row). "
             "Sweep: alternate frames 0-1 at ~200 ms (1 = bristles dragged right, kicking up two specks of dust).", [
                 _sp(['.T....',
                      '.T....',
                      '.T....',
                      '.T....',
                      '.T....',
                      '.T....',
                      '.T....',
                      'RrR...',
                      'yyjJ..',
                      'yyjjJ.',
                      'yyjjjJ'], (1, 6)),
                 _sp(['.T.......',
                      '.T.......',
                      '.T.......',
                      '.T.......',
                      '.T.......',
                      '.T.......',
                      '.T.......',
                      'RrR......',
                      '.yyjJ....',
                      '.yyjjJ.t.',
                      '..yyjjJ.t'], (1, 6)),
             ], ms=200, tags=('compacting', 'clean'))

LOLLIPOP = Item('lollipop', 'hand', "Big pink swirl lollipop on a stick. Hold with rarm='up' (to lick it); in 'side' "
                "the candy brushes his head.", _sp([
                    '..ppp..',
                    '.pPPPp.',
                    'pPrrrPp',
                    'pPrPrPp',
                    'pPrPPPp',
                    '.prrrp.',
                    '..ppp..',
                    '...m...',
                    '...m...',
                    '...m...',
                ], (3, 9)), tags=('idle', 'snack'))

ICE_CREAM = Item('ice_cream', 'hand', "Ice cream cone with a strawberry scoop and a cherry, cone tip = grip. "
                 "Hold with rarm='up' (in 'side' the scoop brushes his head).", _sp([
                     '..r..',
                     '.ppp.',
                     'pPppr',
                     'pppRr',
                     'tpttT',
                     '.ttT.',
                     '.tTT.',
                     '..t..',
                 ], (2, 7)), tags=('idle', 'snack', 'done'))

# =====================================================================================================
# Extras
# =====================================================================================================
_GLYPH_HI = [(1, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3), (1, 4), (3, 4), (1, 5), (3, 5),
             (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]
SIGN_HI = Item('sign_hi', 'hand', "Violet placard on a stick saying 'HI' (hello, session start). rarm='up' or "
               "'raise' to wave it. Left hand: place it unmirrored (see module doc).", _sign('v', 'V', _GLYPH_HI),
               tags=('hello',))

GOLDEN_KEY = Item('golden_key', 'hand', "Big golden key held by its ring bow (permission, unlock). rarm='up' to "
                  "show it, 'out' to offer it to the user.", _sp([
                      '.yj......',
                      'y..j.....',
                      'j..jjjjjj',
                      '.JJ...J.J',
                      '......J..',
                  ], (0, 2)), tags=('alert', 'permission', 'unlock'))

COFFEE_TOGO = Item('coffee_togo', 'hand', "To-go coffee: kraft paper cup with a sleeve and an orange logo, silver sip "
                   "lid overhanging evenly. Held by the sleeve; rarm='side' to hold, 'up' to sip.", _sp([
                       '.NN...',
                       'mmmmmN',
                       '.tttT.',
                       '.ToTT.',
                       '.TTTT.',
                       '.tttT.',
                       '.tttT.',
                   ], (1, 4)), tags=('idle', 'coffee', 'working'))

_MEGAPHONE = _sp(['.....rm',
                  '...rrrm',
                  'Nrrrrrm',
                  '.R.RRRm',
                  '.R...Rm',
                  '.R.....'], (1, 5))
MEGAPHONE = Item('megaphone', 'hand', "Red megaphone pointing right, held by its pistol grip (announcements, "
                 "alerts). Frame 0 = still; frame 1 = shout (gold sound rays burst from the bell, 3 cells right of "
                 "the rim): a one-shot ~120 ms, or alternate 0/1 at ~150 ms while he calls out. rarm='up' or 'side'.", [
                     _MEGAPHONE,
                     _over(_MEGAPHONE, ['.........j',
                                        '........j.',
                                        '..........',
                                        '........jj',
                                        '..........',
                                        '........j.',
                                        '.........j'], 0, -1),
                 ], ms=[600, 120], tags=('alert', 'subagents', 'announce'))


def _sparkler(core, sparks):
    g = _grid(9, 9)
    for x, y in [(0, 8), (1, 7), (2, 6), (3, 5)]:
        g[y][x] = 'N'
    for (x, y), ch in core.items():
        g[y][x] = ch
    for (x, y), ch in sparks.items():
        g[y][x] = ch
    return _sp(_rows(g), (0, 8))


SPARKLER = Item('sparkler', 'hand', "Sparkler fizzing at its tip: frames 0-2 loop at ~110 ms (core twinkles, sparks "
                "jump around). rarm='raise' or 'up' to celebrate.", [
                    _sparkler({(4, 4): 'W', (3, 4): 'y', (5, 4): 'y', (4, 3): 'y', (4, 5): 'y'},
                              {(6, 2): 'y', (2, 2): 'o', (7, 5): 'j', (5, 0): 'j'}),
                    _sparkler({(4, 4): 'Y', (3, 3): 'y', (5, 3): 'y', (5, 5): 'y'},
                              {(4, 1): 'y', (7, 3): 'o', (1, 3): 'j', (7, 7): 'y'}),
                    _sparkler({(4, 4): 'W', (4, 3): 'y', (5, 4): 'y', (3, 4): 'j'},
                              {(6, 1): 'o', (2, 1): 'y', (8, 4): 'y', (6, 6): 'j'}),
                ], ms=110, tags=('done', 'party', 'celebrate'))

# Compact camera seen from the front: silver body, viewfinder bump, red shutter button, a big black lens
# ring around blue glass (glint top-left), and the flash window (yellow) at its top-left.
_CAMERA = _sp(['.NN..rr.',
               'mmmmmmmN',
               'mymKKmmN',
               'mmKCbKmN',
               'mmKbBKmN',
               'mmmKKmNN',
               'NNNNNNNN'], (0, 4))
CAMERA = Item('photo_camera', 'hand', "Compact camera aimed at the viewer (selfie / photo time): silver body, big black "
              "lens ring, red shutter. Frame 0 = ready; frame 1 = flash burst from the window at its top-left, a "
              "one-shot ~100 ms (do not loop the flash). rarm='up' or 'out'.", [
                  _CAMERA,
                  _over(_CAMERA, ['j.y.j',
                                  '..Y..',
                                  '.YWY.',
                                  '..Y..'], -1, 0),
              ], ms=[900, 100], tags=('hello', 'photo'))

RUBBER_DUCK = Item('rubber_duck_held', 'hand', "Yellow rubber duck held in his hand (rubber-duck debugging), facing "
                   "away from Clawd. rarm='up' to show it, 'side' to hold.", _sp([
                       '...yy..',
                       '..ykyo.',
                       'j.yyyoo',
                       'jjyyyj.',
                       '.jjjj..',
                   ], (0, 3)), tags=('thinking', 'error', 'debug', 'idle'))

_WFLAG = ['mmmmm',
          'WWwwm',
          'wwwMm',
          'mmmmm']


def _white_flag(offs):
    g = _grid(6, 11)
    g[0][0] = 't'
    for y in range(1, 11):
        g[y][0] = 'T'
    for c in range(5):
        for r in range(4):
            g[1 + r + offs[c]][1 + c] = _WFLAG[r][c]
    return _sp(_rows(g), (0, 10))


WHITE_FLAG = Item('white_flag', 'hand', "Little white surrender flag on a stick (error, give up), limp wave: frames "
                  "0-2 loop at ~220 ms. rarm='raise' or 'up'; pair with eyes='look_d' and larm='down' (dejected).",
                  [_white_flag([0, 0, 1, 1, 0]), _white_flag([0, 0, 0, 1, 1]), _white_flag([0, 1, 1, 0, 0])],
                  ms=220, tags=('error', 'surrender'))

GIFT_BOX = Item('gift_box', 'hand', "Red gift box with a gold ribbon and bow, held at its side. rarm='side', 'up' "
                "or 'out' (offering it).", _sp([
                    '.j.j.',
                    '..y..',
                    'rryrR',
                    'yyyyJ',
                    'rryrR',
                    'rryRR',
                ], (0, 4)), tags=('done', 'hello', 'gift'))

_KITE = {(6, 0): 'r', (5, 1): 'r', (6, 1): 'r', (7, 1): 'y', (4, 2): 'r', (5, 2): 'r', (6, 2): 'r', (7, 2): 'y',
         (8, 2): 'y', (5, 3): 'y', (6, 3): 'y', (7, 3): 'r', (5, 4): 'y', (6, 4): 'y', (7, 4): 'r', (6, 5): 'y'}


def _kite(tail):
    g = _grid(9, 11)
    for x, y in _line(0, 10, 5, 4):
        g[y][x] = 'm'
    for (x, y), ch in _KITE.items():
        g[y][x] = ch
    for (x, y), ch in tail.items():
        g[y][x] = ch
    return _sp(_rows(g), (0, 10))


KITE = Item('kite', 'hand', "Red-and-yellow diamond kite flying up-right on its string (breezy auto mode); the bow "
            "tail swings: frames 0-1-2 at ~220 ms, ping-pong 0,1,2,1 for a smooth sway. rarm='up' or 'side'.", [
                _kite({(6, 6): 'N', (7, 7): 'b', (7, 8): 'N', (8, 9): 'p'}),
                _kite({(6, 6): 'N', (6, 7): 'b', (7, 8): 'N', (7, 9): 'p'}),
                _kite({(6, 6): 'N', (5, 7): 'b', (6, 8): 'N', (6, 9): 'p'}),
            ], ms=220, tags=('auto', 'breezy', 'play'))

DONUT = Item('donut', 'hand', "Pink frosted donut with sprinkles, held by its edge. rarm='side' or 'up' (snack time).",
             _sp(['.pppp.',
                  'pPpcpp',
                  'pp..pr',
                  'tpyppT',
                  '.tttT.'], (0, 2)), tags=('idle', 'snack'))

PIZZA = Item('pizza_slice', 'hand', "Pepperoni pizza slice held by the crust, tip up. rarm='side' or 'up' (snack time).",
             _sp(['..y..',
                  '.yyj.',
                  '.ryj.',
                  'yyyrj',
                  'yryyj',
                  'ttttT'], (0, 5)), tags=('idle', 'snack'))

ITEMS = [MUG, MUG_HELD, PHONE, BOOK, CLIPBOARD, MAGNIFIER, WRENCH, HAMMER, HAMMER_UP, HAMMER_HIT, FISHING_ROD, FISH,
         CONTROLLER, PENCIL, PAINTBRUSH, BALLOON, CHECKERED_FLAG, TROPHY, PARTY_POPPER, MICROPHONE, COWBELL,
         DRUMSTICK, WAND, UMBRELLA, SIGN_BANG, SIGN_QUESTION, SIGN_HEART, SIGN_OK, STOPWATCH, BROOM, LOLLIPOP,
         ICE_CREAM, SIGN_HI, GOLDEN_KEY, COFFEE_TOGO, MEGAPHONE, SPARKLER, CAMERA, RUBBER_DUCK, WHITE_FLAG,
         GIFT_BOX, KITE, DONUT, PIZZA]
