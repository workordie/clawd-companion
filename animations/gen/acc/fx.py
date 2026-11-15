"""fx: particles and symbols for Clawd's animations (slot 'fx', anchor = visual center).

Place them with frame.place(item.sprite(i), x, y): the anchor cell lands on (x, y).
Every effect floats over transparency on BOTH themes (#1E1E1E and #FFFFFF), so silhouettes touch the
background with mid-tones only; near-white is kept for enclosed glints and for fills with a mid-tone rim.
Light comes from the top-left. Sizes are relative to Clawd's 9x6 body.
Multi-frame items keep one anchor for every frame, so stepping frames never makes the effect jump.
"""
import math

from clawdlib import Item, Sprite


def _s(rows, anchor):
    return Sprite(rows, anchor=anchor)


def _frames(grids, anchor):
    """Several frames drawn on same-size grids, all sharing one anchor."""
    return [Sprite(g, anchor=anchor) for g in grids]


def _grid(w, h, parts=()):
    """Compose a w x h frame from (rows, x, y) parts; later parts draw on top, '.' is transparent."""
    g = [['.'] * w for _ in range(h)]
    for rows, x, y in parts:
        for yy, r in enumerate(rows):
            for xx, ch in enumerate(r):
                if ch == '.':
                    continue
                if not (0 <= x + xx < w and 0 <= y + yy < h):
                    raise ValueError('fx part pixel (%d, %d) outside %dx%d grid' % (x + xx, y + yy, w, h))
                g[y + yy][x + xx] = ch
    return [''.join(r) for r in g]


# ============================================================================================
# Sleep Zs: lavender face, violet right edge (a chunky italic Z that reads on both themes).
# ============================================================================================
Z_SMALL = Item('z_small', 'fx', 'Small sleep Z (4x4). Spawn just above his head, e.g. (22, 9) at HOME, drift up-right ~1 cell per '
               '300-400 ms and swap to z_medium (~(24, 7)), then z_big (~(27, 4)) as it rises. Anchor = visual center.', _s([
                   'lllv',
                   '..lv',
                   '.lv.',
                   'lllv',
               ], (2, 2)), tags=('sleep',), preview={'at': (22, 9)})

Z_MEDIUM = Item('z_medium', 'fx', 'Medium sleep Z (5x5): middle step of a rising z_small -> z_medium -> z_big trail.', _s([
    'llllv',
    '...lv',
    '..lv.',
    '.lv..',
    'llllv',
], (2, 2)), tags=('sleep',), preview={'at': (24, 7)})

Z_BIG = Item('z_big', 'fx', 'Big sleep Z (6x6): top of the rising Z trail; drop it after ~900 ms (or let it leave the canvas).', _s([
    'lllllv',
    '....lv',
    '...lv.',
    '..lv..',
    '.lv...',
    'lllllv',
], (3, 3)), tags=('sleep',), preview={'at': (27, 4)})

# ============================================================================================
# Sparkles and stars: gold edges (visible on white) around a yellow / white glowing core.
# ============================================================================================
SPARKLE = Item('sparkle', 'fx', 'Twinkle: dot -> plus -> 7x7 star -> long thin plus. One-shot or loop at ~90-120 ms '
               '(put empty gaps between twinkles in your own layer); frame 2 is the best still.', _frames([
                   ['.......',
                    '.......',
                    '.......',
                    '...j...',
                    '.......',
                    '.......',
                    '.......'],
                   ['.......',
                    '.......',
                    '...j...',
                    '..jyj..',
                    '...j...',
                    '.......',
                    '.......'],
                   ['...j...',
                    '...j...',
                    '..jyj..',
                    'jjyWyjj',
                    '..jyj..',
                    '...j...',
                    '...j...'],
                   ['.......',
                    '...j...',
                    '...j...',
                    '.jjyjj.',
                    '...j...',
                    '...j...',
                    '.......'],
               ], (3, 3)), ms=100, tags=('done', 'magic'), preview={'at': (24, 8)})

# sparkle_small never grows past 3x3: its peak is a 45-degree turn (+ -> x), so it twinkles by rotating
# instead of growing like sparkle (scatter both for variety).
SPARKLE_SMALL = Item('sparkle_small', 'fx', 'Small glint (max 3x3): dot -> plus -> diagonal x, a twinkle that turns 45 deg. Play '
                     '0-1-2-1 at ~90-120 ms (or loop 1-2 to keep it turning); scatter several with offset timing. Frame 1 is '
                     'the best still.', _frames([
                         ['.....',
                          '.....',
                          '..j..',
                          '.....',
                          '.....'],
                         ['.....',
                          '..j..',
                          '.jyj.',
                          '..j..',
                          '.....'],
                         ['.....',
                          '.j.j.',
                          '..j..',
                          '.j.j.',
                          '.....'],
                     ], (2, 2)), ms=100, tags=('done', 'magic'), preview={'at': (23, 9)})

_STAR_UP = [
    '...j...',
    '..jyj..',
    'jjWyyjJ',
    '.jyyyJ.',
    '..jjJ..',      # (3,4) gold, not yellow: it touches the notch between the legs and would blur on white
    '.jJ.jJ.',
    '.J...J.',
]
STAR = Item('star', 'fx', 'Little gold star (7x7): yellow body, gold rim, dark-gold shade, white glint. Static; '
            'star_spin twirls the same star. Anchor = center, e.g. (24, 8) at HOME.', _s(_STAR_UP, (3, 3)), tags=('done',), preview={'at': (24, 8)})

# A 5-point star repeats every 72 deg, so exact 90-deg pixel rotations read as 18-deg steps of one
# smooth clockwise twirl. Lighting is re-applied per frame (always from the top-left).
STAR_SPIN = Item('star_spin', 'fx', 'Gold star twirling clockwise in place: 4-frame seamless loop at ~90-140 ms.', _frames([
    _STAR_UP,
    ['....j..',
     'jj.jj..',
     '.jjWyj.',
     '..jyyyJ',
     '.jjyyJ.',
     'jJ.jJ..',
     '....J..'],
    ['.j...j.',
     '.jj.jJ.',
     '..jjj..',
     '.jWyyj.',
     'jjyyyJJ',
     '..jyJ..',
     '...J...'],
    ['..j....',
     '..jj.jJ',
     '.jWyJJ.',
     'jyyyJ..',
     '.jyyJj.',
     '..JJ.JJ',
     '..J....'],
], (3, 3)), ms=110, tags=('done',), preview={'at': (24, 8)})

# ============================================================================================
# Confetti: 1-4 cell pieces that tumble (front / back faces in two tones). Move them yourself along
# ballistic() arcs, step frames every ~80-120 ms, mix pieces and start frames.
# ============================================================================================
_CF_A = [['rr', '..'], ['.p', 'r.'], ['R.', 'R.'], ['r.', '.R']]          # strip spinning - / | \
_CF_B = [['cc'], ['.b'], ['bb'], ['c.']]                                    # flake: wide / edge / back / edge
_CF_C = [['jo', '.j'], ['.j', 'jo'], ['j.', 'oj'], ['oj', 'j.']]          # curl rotating (orange bend holds on white)
_CF_D = [['g.g.', '.G.G'], ['.g.g', 'G.G.']]                                # ribbon: lit peaks, shaded valleys, wave travels
_CF_E = [['pp', '..'], ['p.', '.r'], ['.r', '.r'], ['.p', 'r.']]          # pink strip spinning the other way
_CF_F = [['lv'], ['.v'], ['vv'], ['l.']]                                    # violet flake

CONFETTI_A = Item('confetti_a', 'fx', 'Red confetti strip spinning (- / | \\): 4 frames at ~90 ms; move it along a ballistic() arc.',
                  _frames(_CF_A, (0, 0)), ms=90, tags=('done', 'confetti'), preview={'at': (24, 8)})
CONFETTI_B = Item('confetti_b', 'fx', 'Blue confetti flake fluttering (wide / edge / back / edge): 4 frames at ~90 ms; move along an arc.',
                  _frames(_CF_B, (0, 0)), ms=90, tags=('done', 'confetti'), preview={'at': (24, 8)})
CONFETTI_C = Item('confetti_c', 'fx', 'Gold confetti curl (3 cells, orange bend) rotating: 4 frames at ~100 ms; move along an arc.',
                  _frames(_CF_C, (0, 0)), ms=100, tags=('done', 'confetti'), preview={'at': (24, 8)})
CONFETTI_D = Item('confetti_d', 'fx', 'Green confetti ribbon (4x2 zigzag, lit peaks / shaded valleys) whose wave travels along it: '
                  '2 frames at ~120 ms; move along an arc.',
                  _frames(_CF_D, (1, 0)), ms=120, tags=('done', 'confetti'), preview={'at': (24, 8)})
CONFETTI_E = Item('confetti_e', 'fx', 'Pink confetti strip spinning (counter to confetti_a): 4 frames at ~90 ms; move along an arc.',
                  _frames(_CF_E, (0, 0)), ms=90, tags=('done', 'confetti'), preview={'at': (24, 8)})
CONFETTI_F = Item('confetti_f', 'fx', 'Violet confetti flake fluttering: 4 frames at ~90 ms; move along an arc.',
                  _frames(_CF_F, (0, 0)), ms=90, tags=('done', 'confetti'), preview={'at': (24, 8)})


# Confetti has a lot of air drag: pieces shoot up and out, their sideways speed dies quickly, they hang at the
# top and then flutter down slowly (terminal speed 1 cell per frame) instead of falling like stones.
_BURST_PIECES = [(-2.6, -2.6, _CF_A, 0), (-1.5, -3.3, _CF_C, 1), (-0.5, -3.6, _CF_B, 2), (0.6, -3.5, _CF_D, 0),
                 (1.6, -3.2, _CF_F, 1), (2.7, -2.5, _CF_E, 2), (-1.9, -1.7, _CF_D, 1), (2.0, -1.9, _CF_C, 3)]
_BURST_N = 8


def _burst_path(vx, vy):
    x = y = 0.0
    pts = []
    for _ in range(_BURST_N):
        pts.append((int(math.floor(x + 0.5)), int(math.floor(y + 0.5))))
        x, y = x + vx, y + vy
        vx, vy = vx * 0.72, min(vy + 0.8, 1.0)
    return pts


def _burst(t):
    """Confetti fountain frame t (0 = pop flash); 21 wide, anchor (10, 11) = the emission point."""
    if t == 0:
        return _grid(21, 14, [(['.j.', 'jWj', '.j.'], 9, 9)])          # its bottom cell is the emission point
    parts = []
    for vx, vy, spr, s0 in _BURST_PIECES:
        x, y = _burst_path(vx, vy)[t]
        parts.append((spr[(s0 + t) % len(spr)], 10 + x, 11 + y))
    return _grid(21, 14, parts)


CONFETTI_BURST = Item('confetti_burst', 'fx', 'One-shot confetti fountain: pop flash, 8 mixed pieces shoot up and out, hang, then '
                      'flutter down, tumbling. 8 frames ~60/80/90/100/110/130/150/170 ms (still: frame 3). Anchor = the emission '
                      'point (bottom center), e.g. a party popper\'s mouth or (15, 11) just above his head at HOME. Every piece is '
                      'falling on the last frame; continue single confetti_* pieces from there (1 cell down per ~170 ms) for a longer fall.',
                      _frames([_burst(t) for t in range(_BURST_N)], (10, 11)), ms=[60, 80, 90, 100, 110, 130, 150, 170],
                      tags=('done', 'confetti'), preview={'at': (15, 11)})

# ============================================================================================
# Hearts: red, white glint top-left, dark-red shade bottom-right.
# ============================================================================================
_HEART = [
    '.r.r.',
    'rWrrr',
    'rrrrR',
    '.rrR.',
    '..r..',
]
_HEART_BIG = [
    '.rr.rr.',
    'rWprrrr',
    'rprrrrR',
    '.rrrrR.',
    '..rrR..',
    '...r...',
]
HEART = Item('heart', 'fx', 'Small red heart (5x5). Float it up with a 1-cell side-to-side sway; spawn it with heart_pop. Anchor = visual center, '
             'e.g. (23, 8) at HOME.',
             _s(_HEART, (2, 2)), tags=('love',), preview={'at': (23, 8)})

HEART_BIG = Item('heart_big', 'fx', 'Big red heart (7x6) for a strong reaction. Anchor = visual center, like heart; (24, 7) at HOME sits it beside his head.',
                 _s(_HEART_BIG, (3, 2)), tags=('love',), preview={'at': (24, 7)})

HEART_POP = Item('heart_pop', 'fx', 'Heart popping in: tiny -> overshoot (heart_big) -> settle (= heart, same spot). One-shot '
                 '~70/90 ms, then hold frame 2 or switch to heart.', _frames([
                     _grid(7, 7, [(['p.p', 'ppp', '.p.'], 2, 2)]),
                     _grid(7, 7, [(_HEART_BIG, 0, 1)]),
                     _grid(7, 7, [(_HEART, 1, 1)]),
                 ], (3, 3)), ms=[70, 90, 400], tags=('love',), preview={'at': (24, 8)})

# ============================================================================================
# Music notes: violet, lavender highlight and deep-violet shade on the note heads.
# ============================================================================================
NOTE = Item('note', 'fx', 'Single eighth note (5x6). Float up 1 cell every ~200 ms with a side-to-side sway, from about (23, 8) at HOME. '
             'Anchor = visual center.', _s([
    '..vv.',
    '..v.v',
    '..v..',
    '..v..',
    'lvv..',
    'vvV..',
], (2, 3)), tags=('music', 'vibe'), preview={'at': (23, 8)})

NOTE_DOUBLE = Item('note_double', 'fx', 'Beamed pair of eighth notes (7x6). Float up like note; alternate the two for variety.', _s([
    '..lllll',
    '..vvvvv',
    '..v...v',
    '..v...v',
    'lvv.lvv',
    'vvV.vvV',
], (3, 3)), tags=('music', 'vibe'), preview={'at': (24, 8)})

# ============================================================================================
# Steam, smoke, dust, poof
# ============================================================================================
# Steam rises out of one source cell (bottom row, middle) and breaks up: a 1-row gap climbs one row per frame,
# so each puff detaches from the cup, sways up the S-curve and leaves through the top. 5 cells every frame.
_STEAM = [
    ['...', '.m.', 'm..', 'm..', '.m.', '.m.'],
    ['.m.', 'm..', 'm..', '.m.', '..m', '...'],
    ['m..', 'm..', '.m.', '..m', '...', '.m.'],
    ['m..', '.m.', '..m', '...', '.m.', '.m.'],
    ['.m.', '..m', '...', '.m.', 'm..', '.m.'],
    ['..m', '...', '.m.', 'm..', 'm..', '.m.'],
]
STEAM = Item('steam', 'fx', 'Rising steam wisp (3x6): puffs leave one source cell above the cup, sway up an S-curve and break off '
             'at the top. 6-frame seamless loop at ~120-150 ms (still: frame 0). Its bottom row is 2 below the anchor: place '
             'the anchor 3 rows above the cup rim; two wisps with offset frames look rich.',
             _frames(_STEAM, (1, 3)), ms=130, tags=('steam', 'coffee'), preview={'at': (24, 10)})

SMOKE_PUFF = Item('smoke_puff', 'fx', 'Gray smoke puff: a small puff swells into a lumpy cloud (uneven top bumps, rounded '
                  'base), then peels apart into curled wisps. One-shot ~90/110/140/170 ms (still: frame 2); drift it up ~1 cell '
                  'per frame for chimney / exhaust puffs.', _frames([
                      _grid(8, 7, [(['.mm.',
                                     'mMmm',
                                     '.NN.'], 2, 4)]),
                      _grid(8, 7, [(['.mm.m.',
                                     'mMmmMm',
                                     'mmmmmN',
                                     '.NNNN.'], 1, 3)]),
                      _grid(8, 7, [(['.mm.mmm.',
                                     'mMmmMMmm',
                                     'mmmmmmmN',
                                     '.mmmmmN.',
                                     '..NNNN..'], 0, 1)]),
                      _grid(8, 7, [(['.mm',
                                     'mN.'], 0, 0),
                                   (['mm.',
                                     '.mN'], 5, 0),
                                   (['m.',
                                     '.N'], 3, 3)]),
                  ], (3, 3)), ms=[90, 110, 140, 170], tags=('smoke',), preview={'at': (25, 8)})

DUST_PUFF = Item('dust_puff', 'fx', 'Landing dust: two tan puffs roll out from beside his feet. One-shot ~80/100/130 ms. Anchor = '
                 'center between the puffs, one row above the ground: place at (feet center x, GROUND - 1), e.g. (15, 18) at HOME.',
                 _frames([
                     _grid(25, 4, [(['.t.',
                                     'tTT'], 5, 2),
                                   (['.t.',
                                     'tTT'], 17, 2)]),
                     _grid(25, 4, [(['.tt.',
                                     'twtt',
                                     'tTTT'], 2, 1),
                                   (['.tt.',
                                     'twtt',
                                     'tTTT'], 19, 1)]),
                     _grid(25, 4, [(['tt',
                                     'tT'], 0, 0),
                                   (['t'], 3, 2),
                                   (['tt',
                                     'tT'], 23, 0),
                                   (['t'], 21, 2)]),
                 ], (12, 2)), ms=[80, 100, 130], tags=('land', 'jump'), preview={'at': (15, 18)})

_PUFF4 = ['.mm.',
          'mWwm',
          'mwMs',
          '.ss.']
_PUFF3 = ['.m.',
          'mws',
          '.s.']
_PUFF2 = ['mm',
          'ms']
_CLOUD_POOF = [
    '...mmm.mmm...',
    '..mWwwmwwwm..',
    '.mwwwwwwwwwm.',
    'mwwwwwwwwwwwm',
    'mwwwwwwwwwwws',
    'swwMwwwwwwMws',
    '.swwMMwwMMws.',
    '.swwwwwwwwws.',      # flat base resting on the ground: covers all four feet (x 11-19 on row 19 at HOME)
    '..sssssssss..',
]
POOF = Item('poof', 'fx', 'Cartoon poof (appear / disappear): burst -> big cloud that hides his whole box, feet included -> '
            'ring of puffs -> specks. One-shot ~60/110/110/140 ms; swap Clawd in or out on frame 1 (draw the poof after him). '
            'Anchor = his body center, (15, 15) at HOME.', _frames([
                _grid(17, 11, [(['.mmm.',
                                 'mWwwm',
                                 'mwwMs',
                                 '.sss.'], 6, 4),
                               (['m'], 4, 3), (['m'], 12, 3), (['s'], 4, 8), (['s'], 12, 8)]),
                _grid(17, 11, [(_CLOUD_POOF, 2, 2)]),
                _grid(17, 11, [(_PUFF4, 3, 0), (_PUFF4, 10, 0), (_PUFF4, 0, 5), (_PUFF4, 13, 5),
                               (_PUFF3, 4, 8), (_PUFF3, 10, 8)]),
                _grid(17, 11, [(_PUFF2, 2, 0), (_PUFF2, 13, 0), (['m'], 8, 0), (_PUFF2, 0, 8), (_PUFF2, 15, 8),
                               (['s'], 5, 10), (['s'], 11, 10)]),
            ], (8, 6)), ms=[60, 110, 110, 140], tags=('hello', 'magic'), preview={'at': (15, 15)})

# ============================================================================================
# Speech bubble (11x9 body, tail down-left) and its variants: all share one bubble and one anchor
# (the bubble center), so you can swap variants frame by frame. Tail tip = anchor + (-5, +6).
# ============================================================================================
_SPEECH = [
    '...NNNNNNN..',
    '..NWwwwwwwN.',
    '.NwwwwwwwwwN',
    '.NwwwwwwwwwN',
    '.NwwwwwwwwwN',
    '.NwwwwwwwwMN',
    '.NwwwwwwwwMN',
    '..NwwwwwwMN.',
    '..NwwNNNNN..',
    '..NwN.......',
    '.NNN........',
]
_SB_AT = {'at': (25, 5)}      # bubble x 20-30, y 1-11 (1-cell canvas margin); tail tip (20, 11) beside his head-top corner


def _speech(*parts):
    return _grid(12, 11, [(_SPEECH, 0, 0)] + list(parts))


# Glyphs sit on paper, so they use a mid face + dark shade (r/R, b/B, g/G) for contrast with the paper,
# all 5 rows tall on rows 2-6 of the bubble (1 row of padding above and below).
_BANG = ['pR',          # 2-wide bar with the pink highlight top-left, like the big exclamation
         'rR',
         'rR',
         '..',
         'rR']
_QUESTION = ['.bbb.',
             'b..bB',
             '..bB.',
             '.....',
             '..bB.']
_CHECK = ['.....gG',
          '....gG.',
          'gG.gG..',
          '.gGG...',
          '..g....']
SPEECH_BUBBLE = Item('speech_bubble', 'fx', 'Empty speech bubble (11x9 + tail down-left; tail tip = anchor + (-5, +6)). Anchor '
                     '(25, 5) at HOME: bubble x 20-30, y 1-11, tip (20, 11) just off his head-top corner.',
                     _s(_speech(), (6, 4)), tags=('talk',), preview=_SB_AT)
BUBBLE_BANG = Item('bubble_bang', 'fx', 'Speech bubble with a bold red "!" (needs attention / permission). Same bubble and anchor '
                   'as speech_bubble: (25, 5) at HOME.', _s(_speech((_BANG, 5, 2)), (6, 4)), tags=('talk', 'alert'), preview=_SB_AT)
BUBBLE_QUESTION = Item('bubble_question', 'fx', 'Speech bubble with a blue "?" (asking you). Same bubble and anchor as '
                       'speech_bubble: (25, 5) at HOME.', _s(_speech((_QUESTION, 4, 2)), (6, 4)), tags=('talk', 'question'), preview=_SB_AT)
BUBBLE_DOTS = Item('bubble_dots', 'fx', 'Speech bubble typing ". .. ...": 3 frames at ~350 ms, loop (or hold frame 2). For '
                   'reduced motion start the layer on frame 2 so the still shows "...". Same bubble/anchor: (25, 5) at HOME.',
                   _frames([_speech((['n'], 4, 4)),
                            _speech((['n.n'], 4, 4)),
                            _speech((['n.n.n'], 4, 4))], (6, 4)), ms=350, tags=('talk', 'typing'), preview=_SB_AT)
BUBBLE_HEART = Item('bubble_heart', 'fx', 'Speech bubble with a red heart. Same bubble and anchor as speech_bubble: (25, 5) at HOME.',
                    _s(_speech((_HEART, 4, 2)), (6, 4)), tags=('talk', 'love'), preview=_SB_AT)
BUBBLE_CHECK = Item('bubble_check', 'fx', 'Speech bubble with a green check (done / approved). Same bubble and anchor as '
                    'speech_bubble: (25, 5) at HOME.', _s(_speech((_CHECK, 3, 2)), (6, 4)), tags=('talk', 'done'), preview=_SB_AT)
_HI = [(['O.O', 'O.O', 'OOO', 'O.O', 'O.O'], 3, 2),       # H   warm rust: friendly, reads on the paper
       (['O', 'O', 'O', 'O', 'O'], 7, 2),                    # I
       (['O', 'O', 'O', '.', 'O'], 9, 2)]                    # !
BUBBLE_HI = Item('bubble_hi', 'fx', 'Speech bubble saying "HI!" (hello / session start). Same bubble and anchor as speech_bubble: '
                 '(25, 5) at HOME; pop it in with a 1-cell bounce while he waves.', _s(_speech(*_HI), (6, 4)),
                 tags=('talk', 'hello'), preview=_SB_AT)

# ============================================================================================
# Thought bubble (cloud) + a trailing bubble ring and dot toward the lower-left; variants share it and its anchor.
# ============================================================================================
_THOUGHT = [
    '...NNN.NNN...',      # two lobes on top, one round bulge per side, three lobes underneath
    '..NWwwNwwwN..',
    '.NwwwwwwwwwN.',
    'NwwwwwwwwwwwN',
    'NwwwwwwwwwwwN',
    'NwwwwwwwwwwMN',
    '.NwwNwwwNwMN.',
    '..NN.NNN.NN..',
    '.............',
    '.....NN......',      # trail: a little bubble ring, then a dot, stepping down-left toward his head
    '....NwwN.....',
    '.....NN......',
    '...N.........',
]
_TB_AT = {'at': (24, 5)}      # cloud x 18-30, y 1-8; ring x 22-25, y 10-12; last dot (21, 13): no cell touches him


def _thought(*parts):
    return _grid(13, 13, [(_THOUGHT, 0, 0)] + list(parts))


# The bulb fills the cloud's rows 1-5, so a row of paper separates its screw base from the cloud's bottom edge.
# (No paper cells are painted over the cloud: animations that diff this variant against thought_bubble get
# only bulb cells, which also sit correctly on a recolored cloud.)
_BULB_MINI = ['.jjj.',
              'jWyyj',
              'jyyyj',
              '.jyj.',
              '.sNs.']
THOUGHT_BUBBLE = Item('thought_bubble', 'fx', 'Empty thought cloud (13x8) with a bubble ring and a dot trailing toward his head '
                      '(last dot = anchor + (-3, +8)). Anchor (24, 5) at HOME: cloud x 18-30, y 1-8, last dot (21, 13) just '
                      'right of his head-top, touching nothing.', _s(_thought(), (6, 4)), tags=('think',), preview=_TB_AT)
THOUGHT_DOTS = Item('thought_dots', 'fx', 'Thought cloud pondering ". .. ...": 3 frames at ~400 ms, loop. For reduced motion '
                    'start the layer on frame 2 so the still shows "...". Same cloud/anchor: (24, 5) at HOME.',
                    _frames([_thought((['n'], 4, 3)),
                             _thought((['n.n'], 4, 3)),
                             _thought((['n.n.n'], 4, 3))], (6, 4)), ms=400, tags=('think',), preview=_TB_AT)
THOUGHT_BULB = Item('thought_bulb', 'fx', 'Thought cloud with a lit idea bulb (glass, neck and screw base). Same cloud/anchor as '
                    'thought_bubble: (24, 5) at HOME. Swap it in after thought_dots for the "got it!" beat.',
                    _s(_thought((_BULB_MINI, 4, 1)), (6, 4)), tags=('think', 'idea'), preview=_TB_AT)

# ============================================================================================
# Lightbulb, lightning, rain cloud, flame
# ============================================================================================
_BULB_OFF = ['.mmm.',     # cold glass: rim lit top-left (silver), shaded bottom-right (steel)
             'mWMMs',
             'mMMMs',
             'sMMMs',
             '.sMs.',
             '.mmm.',     # screw base: two horizontal thread bands
             '.NNN.']
_BULB_ON = ['.jjj.',
            'jWyyj',
            'jyYyj',
            'jyyyj',
            '.jyj.',
            '.mmm.',
            '.NNN.']
_RAYS = ['j....j....j',
         '.j...j...j.',
         '...........',
         '...........',
         '...........',
         'jj.......jj']
LIGHTBULB = Item('lightbulb', 'fx', 'Idea bulb: 0 off, 1 on, 2 on + glow rays. E.g. 0 (300 ms) -> 1 (120) -> 2, then hold or alternate '
                 '1/2 at ~300 ms (still: frame 2). Anchor = glass center, base bottom = anchor + 4: (15, 6) at HOME floats it '
                 'above his head (rays from y 1, base ends on y 10, one clear row above him).', _frames([
                     _grid(11, 10, [(_BULB_OFF, 3, 3)]),
                     _grid(11, 10, [(_BULB_ON, 3, 3)]),
                     _grid(11, 10, [(_RAYS, 0, 0), (_BULB_ON, 3, 3)]),
                 ], (5, 5)), ms=[300, 120, 300], tags=('idea', 'think'), preview={'at': (15, 6)})

_BOLT = ['...jjo',
         '..jyo.',
         '.jyo..',
         'jjyyjo',      # the jog's end cells are gold: pale yellow there would touch the background and blur on white
         '..jyo.',
         '..jo..',
         '.jo...',
         '.o....']
LIGHTNING = Item('lightning', 'fx', 'Small lightning bolt that crackles now and then: plain (700 ms) -> white glint + two sparks '
                 '(80) -> plain (520) -> glint + sparks elsewhere (80). Loop as given (crackles stay well under 3 Hz); still: '
                 'frame 0. (25, 7) at HOME puts it beside his head.', _frames([
                     _grid(8, 10, [(_BOLT, 1, 1)]),
                     _grid(8, 10, [(_BOLT, 1, 1), (['W'], 3, 4), (['j'], 0, 9), (['j'], 6, 6)]),
                     _grid(8, 10, [(_BOLT, 1, 1)]),
                     _grid(8, 10, [(_BOLT, 1, 1), (['W'], 4, 2), (['j'], 0, 2), (['j'], 6, 8)]),
                 ], (4, 4)), ms=[700, 80, 520, 80], tags=('zap', 'bypass'), preview={'at': (25, 7)})


def _rain(k):
    """4 rows of falling streaks (cyan tail, blue head) below an 11-wide cloud; period 3 rows."""
    g = [['.'] * 11 for _ in range(4)]
    for c, p in ((1, 0), (4, 2), (7, 1), (9, 0)):
        for y in range(4):
            v = (y - k + p) % 3
            if v < 2:
                g[y][c] = 'cb'[v]
    return [''.join(r) for r in g]


_RAIN_CLOUD = [
    '..mmm..mm..',      # a big lobe and a small lobe on top, lit top-left; flat dark underside
    '.mMMMmmMmm.',
    'mMMmmmmmmmm',
    'mmmmmmmmmmN',
    '.NNNNNNNNN.',
]
RAIN_CLOUD = Item('rain_cloud', 'fx', 'Little gray rain cloud with falling drops: 3-frame loop at ~120 ms. Anchor = the cloud\'s '
                  'bottom-center row; rain falls in the 4 rows below it. Over his head: anchor (15, 7) at HOME (cloud y 3-7, '
                  'rain y 8-11 stops right above him). Anchor it lower only if you draw it BEFORE Clawd so drops hide behind him.',
                  _frames([_RAIN_CLOUD + _rain(k) for k in range(3)], (5, 4)), ms=120,
                  tags=('error', 'sad'), preview={'at': (15, 7)})

# Flame: the red rim, orange body and yellow / pale-yellow core stay nested and centered in every frame; only the
# tip sways (x 2, 1, 2, 3) and the core breathes by one cell on a slower 2-frame beat. 24 cells every frame.
_FLAME_TIPS = [['..r..', '..rr.'], ['.r...', '.rr..'], ['..r..', '.rr..'], ['...r.', '..rr.']]
_FLAME_TALL = ['.ror.', 'royor', 'royor', 'ryYyr', '.rrr.']
_FLAME_LOW = ['.ror.', 'rooor', 'royor', 'ryYyr', '.rrr.']
FLAME = Item('flame', 'fx', 'Small flame flickering: the tip sways left / right while the hot core breathes. 4-frame loop at '
             '~100-130 ms. Bottom row = anchor + 2: set it on a wick or prop top (e.g. a candle); (25, 10) at HOME floats it '
             'beside his head.', _frames([_FLAME_TIPS[k] + (_FLAME_TALL if k < 2 else _FLAME_LOW) for k in range(4)], (2, 4)),
             ms=110, tags=('fire', 'bypass'), preview={'at': (25, 10)})

# ============================================================================================
# Motion and impact
# ============================================================================================
MOTION_LINES = Item('motion_lines', 'fx', 'Speed lines trailing to the LEFT of something moving right (place(..., flip=True) for '
                    'leftward motion): 2 frames at ~80-100 ms. Anchor (5, 15) at HOME streams them off his left side, across '
                    'his body rows; move the anchor with him (box x - 5, box y + 3).', _frames([
                        ['..ssssss',
                         '........',
                         'sssss...',
                         '........',
                         '...sssss'],
                        ['...sssss',
                         '........',
                         '.ssssss.',
                         '........',
                         '.ssssss.'],
                    ], (4, 2)), ms=90, tags=('move',), preview={'at': (5, 15)})

IMPACT_STAR = Item('impact_star', 'fx', 'Comic impact burst: flash -> jagged burst -> spike tips flung one cell further out. '
                   'One-shot ~50/90/90 ms; frame 1 is the best still. Anchor = the point of contact (burst center); 13x13 at most, '
                   'e.g. (25, 7) at HOME for a bonk beside his head.', _frames([
    _grid(13, 13, [(['...........',
                     '...........',
                     '...........',
                     '.....o.....',
                     '....oyo....',
                     '...oyWyo...',
                     '....oyo....',
                     '.....o.....'], 1, 1)]),
    _grid(13, 13, [(['....r......',      # irregular comic spikes (long / short), hot white-yellow core
                     '....rr...r.',
                     '.r..ror.rr.',
                     '..rrooorr..',
                     '...royyor..',
                     'rrooyWyoorr',
                     '..royyyor..',
                     '..rrooorr..',
                     '.rr.ror.r..',
                     '.r...r.....',
                     '.....r.....'], 1, 1)]),
    ['.....r.......',      # the burst is gone; its spike tips fly on, one cell further out along each spike
     '...........r.',
     '.r.........r.',
     '.............',
     '.............',
     '.............',
     'rr.........rr',
     '.............',
     '.............',
     '.............',
     '.r........r..',
     '.r....r......',
     '......r......'],
], (6, 6)), ms=[50, 90, 90], tags=('hit', 'error'), preview={'at': (25, 7)})

# ============================================================================================
# Big symbols
# ============================================================================================
_EXCL = ['pR',
         'rR',
         'rR',
         'rR',
         'rR',
         '..',
         'pR',
         'rR']
EXCLAMATION = Item('exclamation', 'fx', 'Big red "!" with a 2-frame pulse (plain / with burst ticks) at ~300 ms; frame 0 is a '
                   'good still. Anchor = center; (15, 6) at HOME floats it just above his head.', _frames([
                       _grid(8, 9, [(_EXCL, 3, 1)]),
                       _grid(8, 9, [(_EXCL, 3, 1), (['o.', '.o'], 0, 0), (['.o', 'o.'], 6, 0)]),
                   ], (3, 4)), ms=300, tags=('alert',), preview={'at': (15, 6)})

_QMARK = ['.cbb.',
          'cb.bb',
          '...bb',
          '..bb.',
          '..bb.',
          '.....',
          '..bb.']
QUESTION = Item('question', 'fx', 'Big blue "?" bobbing 1 cell on an uneven, curious rhythm: rest 600 ms, hop 240, rest 380, '
                'hop 260 (frames 0/2 = rest, 1/3 = up). Anchor = center; (15, 7) at HOME floats it just above his head.', _frames([
                    _grid(5, 8, [(_QMARK, 0, 1)]),
                    _grid(5, 8, [(_QMARK, 0, 0)]),
                    _grid(5, 8, [(_QMARK, 0, 1)]),
                    _grid(5, 8, [(_QMARK, 0, 0)]),
                ], (2, 4)), ms=[600, 240, 380, 260], tags=('question',), preview={'at': (15, 7)})

CHECK_POP = Item('check_pop', 'fx', 'Green check popping in: tiny -> overshoot -> settle. One-shot ~60/80 ms, then hold frame 2 '
                 '(the still). (25, 6) at HOME pops it beside his head.', _frames([
    _grid(11, 7, [(['...g',
                    'g.g.',
                    '.g..'], 4, 3)]),
    _grid(11, 7, [(['.........gG',
                    '........gG.',
                    '.......gG..',
                    'gG....gG...',
                    '.gG..gG....',
                    '..gGgG.....',
                    '...gG......'], 0, 0)]),
    _grid(11, 7, [(['......gG',
                    '.....gG.',
                    'gG..gG..',
                    '.gGgG...',
                    '..gG....'], 2, 1)]),
], (5, 3)), ms=[60, 80, 400], tags=('done',), preview={'at': (25, 6)})

CROSS_POP = Item('cross_pop', 'fx', 'Red X popping in: tiny -> overshoot -> settle. One-shot ~60/80 ms, then hold frame 2 '
                 '(the still). (25, 6) at HOME pops it beside his head.', _frames([
    _grid(10, 9, [(['r.r',
                    '.r.',
                    'r.r'], 3, 3)]),
    _grid(10, 9, [(['rR......rR',
                    '.rR....rR.',
                    '..rR..rR..',
                    '...rRrR...',
                    '....rR....',
                    '...rRrR...',
                    '..rR..rR..',
                    '.rR....rR.',
                    'rR......rR'], 0, 0)]),
    _grid(10, 9, [(['rR....rR',
                    '.rR..rR.',
                    '..rRrR..',
                    '...rR...',
                    '..rRrR..',
                    '.rR..rR.',
                    'rR....rR'], 1, 1)]),
], (4, 4)), ms=[60, 80, 400], tags=('error',), preview={'at': (25, 6)})

# ============================================================================================
# Loaders and music
# ============================================================================================
_RING = [(2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4),
         (2, 4), (1, 4), (0, 3), (0, 2), (0, 1), (1, 0)]      # the 12 cells of a round 5x5 track, clockwise from the top


def _spinner(k):
    """Frame k: the head is ring cell k; 3 orange cells + 1 rust tail = a constant 4-cell arc, 1 cell per frame."""
    g = [['.'] * 5 for _ in range(5)]
    for i, (x, y) in enumerate(_RING):
        d = (k - i) % 12
        g[y][x] = 'o' if d < 3 else ('O' if d == 3 else 'N')
    return [''.join(r) for r in g]


SPINNER = Item('spinner', 'fx', 'Loading ring (5x5): a 4-cell orange arc (rust tail) glides clockwise round a gray track, one '
               'cell per frame. 12-frame seamless loop at ~70-90 ms (~1 turn per second).',
               _frames([_spinner(k) for k in range(12)], (2, 2)), ms=80, tags=('working', 'loading'), preview={'at': (24, 9)})

_EQ_H = [   # bar heights (1-7) per frame: every bar bounces on its own phase
    [3, 6, 4, 2, 5, 7, 3],
    [5, 7, 2, 4, 3, 5, 5],
    [7, 5, 3, 6, 2, 3, 6],
    [5, 3, 5, 7, 4, 2, 4],
    [3, 2, 7, 5, 6, 4, 2],
    [2, 4, 6, 3, 7, 6, 3],
]


def _eq(hs):
    g = [['.'] * 13 for _ in range(7)]
    for b, h in enumerate(hs):
        for i in range(h):
            g[6 - i][2 * b] = 'g' if i < 3 else ('j' if i < 5 else 'r')
    return [''.join(r) for r in g]


EQUALIZER = Item('equalizer', 'fx', 'Music equalizer: 7 bars bouncing (green / gold / red levels). 6-frame loop at ~110-140 ms. '
                 'Anchor = center; bars grow up from the bottom row (anchor + 3), so set that row on a speaker or desk top. '
                 '(24, 7) at HOME floats all 7 bars (x 18-30) up-right of him, one clear row above his head.',
                 _frames([_eq(h) for h in _EQ_H], (6, 3)), ms=120, tags=('music', 'vibe'), preview={'at': (24, 7)})

# ============================================================================================
# Dizzy stars: three tiny stars on a flat orbit; back stars shrink to dots for depth.
# 4 frames x 30 deg = 120 deg = the gap between stars, so the loop is seamless.
# ============================================================================================
_ORBIT = ['...v.v.v...',      # violet orbit (rx 5, ry 2): the back arc is dashed, the front arc solid, so it reads as a
          '.v.......v.',      # tilted ring in perspective (not a halo); violet stays a mid-tone on both themes
          'v.........v',
          '.vv.....vv.',
          '...vvvvv...']
_DZ = [   # (x, y) of the three stars on the orbit per frame, relative to its center; y > 0 = in front of his head.
    [(-2, 2), (-2, -2), (5, 0)],       # frame 0 is an off-balance phase: a still that reads as circling, not as horns
    [(-4, 1), (0, -2), (4, 1)],
    [(-5, 0), (2, -2), (2, 2)],
    [(0, 2), (-4, -1), (4, -1)],
]


def _dizzy(pts):
    parts = [(_ORBIT, 1, 1)]
    for x, y in sorted(pts, key=lambda p: p[1]):
        if y <= -2:
            parts.append((['j'], 6 + x, 3 + y))                     # far behind his head: a tiny dot
        elif y == -1:
            parts.append((['.j.', 'j.j'], 5 + x, 2 + y))            # just behind: a small 3-cell twinkle
        else:
            parts.append((['.j.', 'jyj', 'j.j'], 5 + x, 2 + y))     # side / front: a little 5-point star
    return _grid(13, 7, parts)


DIZZY_STARS = Item('dizzy_stars', 'fx', 'Dazed: three tiny stars circling his head on a tilted violet orbit (dashed behind, solid '
                   'in front); stars shrink to dots as they pass behind. 4-frame seamless loop at ~100-130 ms; frame 0 is the '
                   'still. Anchor = orbit center: 2 rows above his head-top, (15, 10) at HOME; the front arc crosses his forehead, '
                   'the stars never cover his eyes.', _frames([_dizzy(p) for p in _DZ], (6, 3)), ms=110,
                   tags=('error', 'dizzy'), preview={'at': (15, 10)})

# ============================================================================================
# Code bits, paper plane
# ============================================================================================
def _ink(rows, ch):
    return [r.replace('x', ch) for r in rows]


_TAG = _grid(11, 5, [(['..x', '.x.', 'x..', '.x.', '..x'], 0, 0),      # <
                     (['..x', '..x', '.x.', 'x..', 'x..'], 4, 0),      # /
                     (['x..', '.x.', '..x', '.x.', 'x..'], 8, 0)])     # >
_BRACES = _grid(8, 5, [(['.xx', '.x.', 'x..', '.x.', '.xx'], 0, 0),   # {   two empty columns between the braces,
                       (['xx.', '.x.', '..x', '.x.', 'xx.'], 5, 0)])  # }   so their tips never close into an "O"
_SEMI = ['.x',
         '..',
         '.x',
         'x.']


def _code(k):
    bob = [0, 1, 1, 0]
    a, b, c = bob[k % 4], bob[(k + 1) % 4], bob[(k + 2) % 4]
    return _grid(11, 13, [
        (_ink(_TAG, 'b'), 0, a),
        (_ink(_BRACES, 'v'), 1, 7 + b),     # always >= 1 clear row below the bobbing </>
        (_ink(_SEMI, 'g'), 9, 8 + c),       # bottom-aligned with the braces
    ])


CODE_BITS = Item('code_bits', 'fx', 'Floating code glyphs: blue </>, violet { } and a green ; each bobbing on its own beat. '
                 '4-frame loop at ~200-250 ms (working). 11x13, anchor = center: (25, 7) at HOME floats it up-right of him '
                 '(x 20-30, y 1-13) without touching his head or arm.', _frames([_code(k) for k in range(4)], (5, 6)),
                 ms=220, tags=('working', 'code'), preview={'at': (25, 7)})

_PLANE = ['mm.....',     # near wing lit (paper), far wing shaded, silver contour all round, notched tail
          'mWmm...',
          '.mwwmm.',
          '.mwwwwm',
          '.sMMss.',
          'sMss...',
          'ss.....']
PAPER_PLANE = Item('paper_plane', 'fx', 'Little paper airplane flying right (flip=True for left): 2-frame bob at ~200 ms; glide it '
                   'along a gentle arc. Anchor = visual center, e.g. (25, 6) at HOME.', _frames([
                       _grid(7, 8, [(_PLANE, 0, 1)]),
                       _grid(7, 8, [(_PLANE, 0, 0)]),
                   ], (3, 4)), ms=200, tags=('send', 'auto'), preview={'at': (25, 6)})


# ============================================================================================
# Extras: firework, thinking dots (sweat drop / anger mark / tear live in the face module, they follow his head)
# ============================================================================================
def _firework(t):
    """Pink / gold chrysanthemum: rocket rises (0-1), flash (2), ring of 8 sparks grows and droops (3-5), embers (6)."""
    cx, cy = 6, 6
    if t < 2:
        return _grid(13, 15, [(['y', 'o', 'O'], cx, cy + 6 - 3 * t)])
    if t == 2:
        return _grid(13, 15, [(['.j.', 'jWj', '.j.'], cx - 1, cy - 1)])
    r, droop = {3: (2, 0), 4: (4, 0), 5: (5, 1), 6: (6, 2)}[t]
    parts = []
    for k in range(8):
        a = math.radians(45 * k)
        dx, dy = math.sin(a), -math.cos(a)
        head, tail = ('p', 'r') if k % 2 == 0 else ('j', 'o')
        x, y = int(math.floor(cx + r * dx + 0.5)), int(math.floor(cy + r * dy + 0.5)) + droop
        if t == 6:
            parts.append(([tail], x, y))          # cooling embers
            continue
        if t >= 4:
            tx, ty = int(math.floor(cx + (r - 1) * dx + 0.5)), int(math.floor(cy + (r - 1) * dy + 0.5)) + droop
            parts.append(([tail], tx, ty))
        parts.append(([head], x, y))
    if t == 3:
        parts.append((['y'], cx, cy))
    return _grid(13, 15, parts)


FIREWORK = Item('firework', 'fx', 'One-shot firework: rocket streak rises (0-1), white flash (2), pink / gold spark ring bursts, '
                'grows and droops (3-5), embers fade (6). ~80/80/60/70/90/110/140 ms (still: frame 4). Anchor = burst center; the rocket starts '
                '6 rows below it. 13x15.', _frames([_firework(t) for t in range(7)], (6, 6)), ms=[80, 80, 60, 70, 90, 110, 140],
                tags=('done', 'celebrate'), preview={'at': (24, 6)})

def _dots(k):
    """Gray dots; the one hopping up lights orange, so the wave reads at a glance (and never blends into his head)."""
    lift = [(0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, 1)][k]
    return _grid(5, 2, [(['N' if lift[i] else 'o'], 2 * i, lift[i]) for i in range(3)])


DOTS_WAVE = Item('dots_wave', 'fx', 'Thinking dots "..." (gray) with a wave hopping through them; the hopping dot lights orange '
                 '(no bubble). 4-frame loop at ~150-180 ms; frame 3 (all resting) is the calmest still. Anchor = middle dot; '
                 '(15, 10) at HOME floats it just above his head.', _frames([_dots(k) for k in range(4)], (2, 1)),
                 ms=160, tags=('think', 'working'), preview={'at': (15, 10)})


# ============================================================================================
# More extras for the states that have no props of their own yet: rate-limit, error, hello, idle / vibe.
# ============================================================================================
_BATT = ['mmmmmmmm.',      # steel shell lit on top, darker terminal nub on the right; bars sit inside rows 1-3
         's......sN',
         's......sN',
         's......sN',
         'ssssssss.']
_BATT_BAR = {'r': ['pr', 'rr', 'RR'], 'j': ['yj', 'jj', 'JJ'], 'g': ['ag', 'gg', 'GG']}   # highlight top-left, shade bottom


def _battery(n, col):
    return _grid(9, 5, [(_BATT, 0, 0)] + [(_BATT_BAR[col], 1 + 2 * i, 1) for i in range(n)])


BATTERY_CHARGE = Item('battery_charge', 'fx', 'Little battery slowly recharging: 1 red bar (low) -> 2 gold -> 3 green (full), '
                      'then back to low. Loop as given (1000/1000/1400 ms) for rate-limit / "waiting for capacity"; frame 0 (low) '
                      'is the still. Anchor = battery center, e.g. (25, 8) at HOME beside his head.',
                      _frames([_battery(1, 'r'), _battery(2, 'j'), _battery(3, 'g')], (4, 2)), ms=[1000, 1000, 1400],
                      tags=('rate-limit', 'waiting'), preview={'at': (25, 8)})

_WARN = ['....o....',      # orange rim lit on the left, rust on the right and bottom; ink "!" on a yellow face
         '...oyO...',
         '...okO...',
         '..oykyO..',
         '..oykyO..',
         '.oyyyyyO.',
         '.oyykyyO.',
         'oOOOOOOOO']
WARNING_SIGN = Item('warning_sign', 'fx', 'Warning triangle with a bold "!" (error / risky action / permission). 2 frames: plain '
                    '(the still, ~500 ms) and with two burst ticks off its tip (~250 ms); loop for a calm pulse under 3 Hz. '
                    'Anchor = triangle center; (25, 7) at HOME floats it beside his head (ticks on y 1-2).', _frames([
                        _grid(13, 10, [(_WARN, 2, 2)]),
                        _grid(13, 10, [(_WARN, 2, 2), (['o.', '.o'], 2, 0), (['.o', 'o.'], 9, 0)]),
                    ], (6, 6)), ms=[500, 250], tags=('error', 'alert'), preview={'at': (25, 7)})

SHOOTING_STAR = Item('shooting_star', 'fx', 'Shooting star falling down-left: white-hot head with a gold-to-rust trail on a 2:1 '
                     'slope (frame 1 = the tail flickers). Move it 2 cells left + 1 down per ~80 ms frame, alternating frames, '
                     'and let it leave the canvas; place(..., flip=True) to fall down-right. Anchor = the white head.', _frames([
                         ['.......OO',
                          '.....oo..',
                          '..jjj....',
                          '.jWj.....',
                          '..j......'],
                         ['........O',
                          '.....oO..',
                          '..jjj....',
                          '.jWj.....',
                          '..j......'],
                     ], (2, 3)), ms=80, tags=('done', 'sleep', 'magic'), preview={'at': (24, 7)})

_RING12 = [(2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (1, 4), (0, 3), (0, 2), (0, 1), (1, 0)]
_SHEEN = 'llccccccppll'      # iridescent film: lavender -> cyan -> pink round the ring


def _soap(k):
    """Bubble frame k (0-3): the sheen swirls a quarter turn per frame; the white glint stays top-left."""
    g = [['.'] * 7 for _ in range(7)]
    for i, (x, y) in enumerate(_RING12):
        g[y + 1][x + 1] = _SHEEN[(i - 3 * k) % 12]
    g[2][2] = 'W'
    return [''.join(r) for r in g]


SOAP_BUBBLE = Item('soap_bubble', 'fx', 'Soap bubble (5x5 ring) with a swirling rainbow sheen and a white glint. Frames 0-3 loop '
                   'at ~180-220 ms while you drift it up ~1 cell per 2 frames with a 1-cell sway; frame 4 = pop (4 specks, '
                   '~120 ms, then remove it). Calm enough for idle / vibe: let his eyes follow it. Anchor = bubble center.',
                   _frames([_soap(k) for k in range(4)] + [_grid(7, 7, [(['l.....c', '.......', '.......', '.......', '.......',
                                                                         '.......', 'p.....c'], 0, 0)])], (3, 3)),
                   ms=[200, 200, 200, 200, 120], tags=('idle', 'vibe', 'magic'), preview={'at': (24, 8)})


ITEMS = [
    Z_SMALL, Z_MEDIUM, Z_BIG,
    SPARKLE, SPARKLE_SMALL, STAR, STAR_SPIN,
    CONFETTI_A, CONFETTI_B, CONFETTI_C, CONFETTI_D, CONFETTI_E, CONFETTI_F, CONFETTI_BURST,
    HEART, HEART_BIG, HEART_POP,
    NOTE, NOTE_DOUBLE,
    STEAM, SMOKE_PUFF, DUST_PUFF, POOF,
    SPEECH_BUBBLE, BUBBLE_BANG, BUBBLE_QUESTION, BUBBLE_DOTS, BUBBLE_HEART, BUBBLE_CHECK, BUBBLE_HI,
    THOUGHT_BUBBLE, THOUGHT_DOTS, THOUGHT_BULB,
    LIGHTBULB, LIGHTNING, RAIN_CLOUD, FLAME,
    MOTION_LINES, IMPACT_STAR,
    EXCLAMATION, QUESTION, CHECK_POP, CROSS_POP,
    SPINNER, EQUALIZER, DIZZY_STARS,
    CODE_BITS, PAPER_PLANE,
    FIREWORK, DOTS_WAVE,
    BATTERY_CHARGE, WARNING_SIGN, SHOOTING_STAR, SOAP_BUBBLE,
]
