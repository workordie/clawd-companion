"""Headwear: hats, helmets, crowns, horns, headphones... everything in the 'head' slot.

Use:  wear(frame, get('wizard_hat'), pose)  after put_clawd(); animated items take i=<frame index>.
Every anchor is Clawd's head-top-center (box (5, 0)), so jumps and moves just work
(add dy=1 on a landing frame for a little hat lag).

How the art is drawn: every sprite is drawn over a guide of Clawd's head, so placement is exact by
construction:
  '+' = Clawd's body (guide only, transparent)      ':' = his see-through eyes (guide only)
The anchor is derived from the eye guides (head-top-center = left eye + (3, -2)) and every '+' is
checked against the real standing pose, so a misaligned guide fails loudly at import time.

House style for this module: light from the top-left (base tone, shadow on the right/bottom, at most
one highlight); dark items (top hat, mortarboard, pirate hat) keep a gray rim where they touch the
background, light items (chef hat, captain hat, bunny ears, duck, hard hat) keep a mid-tone contour,
so everything reads on the dark AND the light theme. One-pixel alternation is used only where it is
physical structure (knit ribs, pleats).

Resting rows (box y): brims and bands overlap his top row 0 (the bandana covers rows 0-1, cap_back's
strap sits on row 0); perched things (crown, party hat, tiara, cat ears, unicorn horn, rubber duck,
siren) sit on row -1; the halo floats with row -1 empty; the headphones' band arches over row -1.
Things beside his head: nightcap tail, bandana tails, fishing bobber and the cap's bill are on the LEFT;
cap_back's bill, grad_cap's tassel, santa's pom and the bow are on the RIGHT (raised arms on that side
pass under them).

By state: sleep nightcap | vibe headphones, headphones_glow | edits hard_hat | auto propeller_beanie,
unicorn_horn | bypass devil_horns, bandana, pirate_hat | plan wizard_hat, grad_cap, beret, fedora |
alert siren_light | done party_hat, crown, laurel_wreath, tiara, halo | hooks fishing_hat, jester_hat |
manual sprout | subagents captain_hat, antenna | working miner_helmet, chef_hat | thinking rubber_duck |
hello top_hat, cowboy_hat | rate-limit sombrero | seasonal santa_hat, antlers
"""
from clawdlib import Item, Sprite, clawd, HEX

_P = clawd()
_BODY = {(x, y) for x, y, ch in _P.sprite.cells if ch != '_'}


def _art(rows, name=''):
    """Head-slot sprite from rows drawn over the Clawd guide. Cells end up in Clawd-box
    coordinates (his top-left body corner = (1, 0)) with the anchor on his head-top-center (5, 0)."""
    eyes = [(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch == ':']
    if len(eyes) != 2 or eyes[0][1] != eyes[1][1] or eyes[1][0] - eyes[0][0] != 6:
        raise ValueError('%s: need exactly two eye guides 6 apart on one row, got %r' % (name, eyes))
    ox, oy = eyes[0][0] - 2, eyes[0][1] - 2          # art position of box (0, 0)
    cells = []
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            bx, by = x - ox, y - oy
            if ch == '+':
                if (bx, by) not in _BODY:
                    raise ValueError('%s: body guide at box (%d,%d) is not on Clawd' % (name, bx, by))
            elif ch in '.: ':
                pass
            elif ch in HEX:
                cells.append((bx, by, ch))
            else:
                raise ValueError('%s: unknown char %r' % (name, ch))
    return Sprite(cells=cells, anchor=(5, 0), name=name)


def _frames(name, *arts):
    return [_art(a, name) for a in arts]


def _striped(rows, a, b, name='', period=2, fixed=None):
    """Like _art, but '#' cells become diagonal stripes of colours a/b (computed in box coordinates,
    so the stripes stay put when a frame moves part of the shape). fixed = {(box x, box y): colour}
    pins single cells (a swinging tail keeps its own colours instead of crawling through the stripes)."""
    base = _art([r.replace('#', 'W') for r in rows], name)
    mask = _art([''.join(c if c in '#+:' else '.' for c in r).replace('#', 'W') for r in rows], name)
    m = {(x, y) for x, y, c in mask.cells}
    fixed = fixed or {}
    cells = [(x, y, fixed.get((x, y)) or ((a if ((x + y) // period) % 2 == 0 else b) if (x, y) in m else c))
             for x, y, c in base.cells]
    return Sprite(cells=cells, anchor=(5, 0), name=name)


# =============================================================================================
# beanie: knit dome, ribbed cuff over his top row, pom-pom
# =============================================================================================
#  box x: -2-1 0 1 2 3 4 5 6 7 8 9 0 1 2
BEANIE = _art([
    '......lll......',
    '......lLV......',
    '....vlvvvvV....',
    '...vlvvvvvvV...',
    '...vvvvvvvVV...',
    '..lvlvlvlvvVv..',
    '..lvlvlvlvvVv..',
    '...+++++++++...',
    '..++:+++++:++..',
], 'beanie')

# =============================================================================================
# caps: 3/4 view so the bill reads at 3 px per cell. The front cap's bill pokes out LEFT at his top
# row (its navy underside hangs beside his forehead, never over it); worn backwards the bill sticks out
# behind on the RIGHT, a row higher, and the strap's gold snap sits on his top row.
# =============================================================================================
#  box x: -3-2-1 0 1 2 3 4 5 6 7 8 9 0 1 2
CAP = _art([
    '........b.......',
    '......cbbbB.....',
    '.....cbWbbbB....',
    '....cbbbbbbbB...',
    'cbbbbbbbbBBBB...',
    'BBBB.+++++++....',
    '...++:+++++:++..',
], 'cap')

#  box x: -2-1 0 1 2 3 4 5 6 7 8 9 0 1 2 3
CAP_BACK = _art([
    '.......b........',
    '.....cbbbB......',
    '....cbbbbbB.....',
    '...cbbbbbbbBbbbb',
    '...bbBBjBBBBBBB.',
    '...+++++++++....',
    '..++:+++++:++...',
], 'cap_back')

# =============================================================================================
# crown
# =============================================================================================
CROWN = _art([
    '.......j.......',
    '...j..jyj..j...',
    '...yj.jjj.jJ...',
    '...jWjjjjjjJ...',
    '...jJrJbJrJJ...',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'crown')

# =============================================================================================
# party hat: cone tilted right, 2-cell stripes that follow the lean, violet pom
# =============================================================================================
PARTY_HAT = _art([
    '.........v.....',
    '........vLv....',
    '........vvV....',
    '........pr.....',
    '.......ppj.....',
    '......ppyyr....',
    '.....ppyypr....',
    '....ppyyppj....',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'party_hat')

# =============================================================================================
# wizard hat: two stars trade their twinkle (frame 0: top star bright, frame 1: bottom star bright)
# =============================================================================================
_WIZ = [
    '.......VV......',
    '......vVYV.....',
    '......vVVVV....',
    '......vVV.VV...',
    '.....vjVV..y...',
    '.....vVVVV.j...',
    '....vVVVVVV....',
    '.vvvjjjjjjjvvv.',
    '.vVVVVVVVVVVVV.',
    '...+++++++++...',
    '..++:+++++:++..',
]
WIZARD_HAT = _frames('wizard_hat', _WIZ, [r.replace('vVYV.....', 'vVjV.....').replace('vjVV..y', 'vYVV..y') for r in _WIZ])

# =============================================================================================
# top hat
# =============================================================================================
TOP_HAT = _art([
    '....NmmmmmN....',
    '....NnKKKKn....',
    '....NnKKKKn....',
    '....NnKKKKn....',
    '....rrrrrrR....',
    '..NNnKKKKKnnn..',
    '..nKKKKKKKKKn..',
    '...+++++++++...',
    '..++:+++++:++..',
], 'top_hat')

# =============================================================================================
# hard hat
# =============================================================================================
HARD_HAT = _art([
    '.....jjjjj.....',
    '....jYyYyyj....',
    '...jYyyYyyjj...',
    '...jyyyYyyjJ...',
    '..jjjjjjjJJJJ..',
    '...+++++++++...',
    '..++:+++++:++..',
], 'hard_hat')

# =============================================================================================
# chef hat: rounded two-lobed puff (11 wide, lit top-left) over a pleated band
# =============================================================================================
CHEF_HAT = _art([
    '....mmm.mm.....',
    '...mWwwmwwmm...',
    '..mWwwwwwwwwm..',
    '..mwwwwwwwwMm..',
    '...mMwwwwMMm...',
    '...mwMwMwMwm...',
    '...mwMwMwMwm...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'chef_hat')

# =============================================================================================
# nightcap: droops to the left; 3 frames = rest / swing out / swing in (sleep.py relies on this order).
# The two tail cells below the dome keep their colours (blue, lavender) in every frame.
# =============================================================================================
NIGHTCAP = [_striped(r, 'b', 'l', 'nightcap', fixed=f) for r, f in ((
    [
        '......####.......',
        '....########.....',
        '...##.########...',
        '...#.##########..',
        '...#.BBBBBBBBBBB.',
        '..yj..+++++++++..',
        '..jJ.++:+++++:++.',
    ], {(-2, -1): 'b', (-2, 0): 'l'}), (
    [
        '......####.......',
        '....########.....',
        '...##.########...',
        '..#..##########..',
        '..#..BBBBBBBBBBB.',
        '.yj...+++++++++..',
        '.jJ..++:+++++:++.',
    ], {(-3, -1): 'b', (-3, 0): 'l'}), (
    [
        '......####.......',
        '....########.....',
        '...##.########...',
        '...#.##########..',
        '....#BBBBBBBBBBB.',
        '...yj.+++++++++..',
        '...jJ++:+++++:++.',
    ], {(-2, -1): 'b', (-1, 0): 'l'}))]

# =============================================================================================
# headphones: band arches one row over his head, violet cups on his top corners (lit from the left).
# The glow frame keeps the exact same cells and only lights the cups (no size pop on the beat).
# =============================================================================================
_HP = [
    '.....mNNNN.....',
    '..lvN.....NvV..',
    '..vV+++++++vV..',
    '..vV+++++++vV..',
    '..++:+++++:++..',
]
HEADPHONES = _art(_HP, 'headphones')
HEADPHONES_GLOW = _frames('headphones_glow', _HP, [
    '.....mNNNN.....',
    '..llN.....NlV..',
    '..lv+++++++lv..',
    '..lv+++++++lv..',
    '..++:+++++:++..',
])

# =============================================================================================
# propeller beanie: 4 frames of spin seen edge-on (blade 7, 5, 3, 5 wide). In the two 5-wide frames the
# receding half is shaded, so the blade turns one way instead of breathing. auto.py splits this item:
# blade = top row, hub 'm' on the anchor column; keep that structure and the 4-frame count.
# =============================================================================================
_DOME = [
    '.....pygbv.....',
    '....ryygbbv....',
    '...rryygbbvv...',
    '...RRjjGBBVV...',
    '...+++++++++...',
    '..++:+++++:++..',
]
PROPELLER_BEANIE = _frames(
    'propeller_beanie',
    ['....rrrmrrr....', '.......s.......'] + _DOME,
    ['.....rrmRR.....', '.......s.......'] + _DOME,
    ['......rmr......', '.......s.......'] + _DOME,
    ['.....RRmrr.....', '.......s.......'] + _DOME,
)

# =============================================================================================
# graduation cap: graphite board (gray far rim) on a charcoal skull cap with light side rims; the tassel
# hangs off the board's right corner and swings: rest, out, rest, in
# =============================================================================================
_GC_TOP = [
    '....NNNNNNN....',
    '.NnnnnnjnnnnnN.',
    '.nnnnnnnnnnnnn.',
]
GRAD_CAP = _frames('grad_cap', _GC_TOP + [
    '...NKKKKKKKn.J.',
    '...nKKKKKKKn.j.',
    '...+++++++++.j.',
    '..++:+++++:++..',
], _GC_TOP + [
    '...NKKKKKKKn.J.',
    '...nKKKKKKKn..j',
    '...+++++++++..j',
    '..++:+++++:++..',
], _GC_TOP + [
    '...NKKKKKKKn.J.',
    '...nKKKKKKKn.j.',
    '...+++++++++.j.',
    '..++:+++++:++..',
], _GC_TOP + [
    '...NKKKKKKKn.J.',
    '...nKKKKKKKn.j.',
    '...+++++++++j..',
    '..++:+++++:++..',
])

# =============================================================================================
# cowboy hat: band sits right on the 13-wide brim, brim ends curl up
# =============================================================================================
COWBOY_HAT = _art([
    '.....tt.tT.....',
    '....tttttTT....',
    '....tttttTT....',
    't...tttttTT...T',
    'tt..ddddddd..TT',
    '.ttttttttttTTT.',
    '...+++++++++...',
    '..++:+++++:++..',
], 'cowboy_hat')

# =============================================================================================
# halo: floats with a 1-row gap; gold ring shaded on the right, a glint sweeps across the front
# =============================================================================================
_HALO_GAP = [
    '...............',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
]
HALO = _frames('halo', [
    '.....jjjjj.....',
    '...jj.....JJ...',
    '.....jyjJJ.....',
] + _HALO_GAP, [
    '.....jjjjj.....',
    '...jj.....JJ...',
    '.....jjjyJ.....',
] + _HALO_GAP, [
    '.....jjjjj.....',
    '...jj.....yJ...',
    '.....jjjJJ.....',
] + _HALO_GAP, [
    '.....jjjjj.....',
    '...jj.....JJ...',
    '.....jjjJJ.....',
] + _HALO_GAP)

# =============================================================================================
# devil horns: short curved horns, 2 cells thick at the base, growing out of his top corners
# =============================================================================================
DEVIL_HORNS = _art([
    '..p.........r..',
    '..pr.......rR..',
    '...rR.....rR...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'devil_horns')

# =============================================================================================
# antenna: 5-wide ball centred on the stalk; ball tip blinks (2 frames)
# =============================================================================================
_STALK = [
    '.......s.......',
    '.......s.......',
    '......NsN......',
    '...+++++++++...',
    '..++:+++++:++..',
]
ANTENNA = _frames('antenna', [
    '......rrr......',
    '.....pWrrR.....',
    '.....rrrrR.....',
    '......RRR......',
] + _STALK, [
    '......RRR......',
    '.....rRRRR.....',
    '.....RRRRR.....',
    '......RRR......',
] + _STALK)

# =============================================================================================
# bow: two loops fanning out from a pinched red knot, two little ribbon tails
# =============================================================================================
BOW = _art([
    '......pp.....pp',
    '......pPpprppPp',
    '......ppprRrppr',
    '......pp.R.R.pr',
    '...+++++++++...',
    '..++:+++++:++..',
], 'bow')

# =============================================================================================
# flower: sways rest, right, rest, left (the stem bends right; leaning left only the head tips, so the
# stem never runs into the leaf)
# =============================================================================================
_FLOWER_STEM = [
    '......Gg.......',
    '.......g.......',
    '...+++++++++...',
    '..++:+++++:++..',
]
FLOWER = _frames('flower', [
    '......p.p......',
    '.....ppypp.....',
    '......rpr......',
    '.......g.......',
] + _FLOWER_STEM, [
    '.......p.p.....',
    '......ppypp....',
    '.......rpr.....',
    '........g......',
] + _FLOWER_STEM, [
    '......p.p......',
    '.....ppypp.....',
    '......rpr......',
    '.......g.......',
] + _FLOWER_STEM, [
    '.....p.p.......',
    '....ppypp......',
    '.....rpr.......',
    '.......g.......',
] + _FLOWER_STEM)

# =============================================================================================
# viking helmet
# =============================================================================================
VIKING_HELMET = _art([
    '.t...........t.',
    '.tT.........tT.',
    '..tT.sssss.TT..',
    '...TsSSsssNT...',
    '...ssssssssN...',
    '...JJyJJJyJJ...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'viking_helmet')

# =============================================================================================
# bandana: cloth band round his head (red over dark red, rows 0-1), knot at his left temple, two tails
# streaming left. The tails keep their length; a bend travels along them (a ripple), so a gust reads
# as cloth, not as specks.
# =============================================================================================
_BAND = [(x, 0, 'r') for x in range(0, 10)] + [(x, 1, 'R') for x in range(0, 10)]


def _tail(n, y0, bend, rise, ch):
    """n cells leftwards from box x -1 on row y0; the cells from index `bend` on are `rise` rows off."""
    return [(-1 - i, y0 + (rise if i >= bend else 0), ch) for i in range(n)]


BANDANA = [Sprite(cells=_BAND + _tail(5, 0, ub, -1, 'r') + _tail(4, 1, lb, 1, 'R'), anchor=(5, 0), name='bandana')
           for ub, lb in ((3, 2), (4, 3), (2, 1))]

# =============================================================================================
# miner helmet: headlamp = gray housing ring around a warm lens; frame 1 brightens the lens only
# =============================================================================================
_MINER_LAMP = [
    ['...ghNyWyNgG...', '...ggNyYyNgG...'],
    ['...ghNYWYNgG...', '...ggNYWYNgG...'],
]
MINER_HELMET = [_art([
    '.....ggggg.....',
    '....ghNNNgG....',
    lamp[0],
    lamp[1],
    '...nnnNNNnnn...',
    '..GGGGGGGGGGG..',
    '...+++++++++...',
    '..++:+++++:++..',
], 'miner_helmet') for lamp in _MINER_LAMP]


# =============================================================================================
# extras
# =============================================================================================
SANTA_HAT = _art([
    '......rrr.......',
    '.....prrrRR.....',
    '....prrrrrRR....',
    '...prrrrrrRRR...',
    '..mWWwwwwwwwmRm.',
    '..mwwwwwwwwwmWWm',
    '...+++++++++.mm.',
    '..++:+++++:++...',
], 'santa_hat')

PIRATE_HAT = _art([
    '....nNNNNNn....',
    '.j.nKKWWWKKn.j.',
    '.njKKWkWkWKKjn.',
    '.nKjKKWWWKKjKn.',
    '..nKjKWKWKjKn..',
    '...nKjjjjjKn...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'pirate_hat')

BERET = _art([
    '......R........',
    '...prrrrrr.....',
    '..prrrrrrrrrr..',
    '..rrrrrrrrrrrR.',
    '...RRRRRRRRRR..',
    '...+++++++++...',
    '..++:+++++:++..',
], 'beret')

TIARA = _art([
    '.......s.......',
    '......sPs......',
    '....s..p..s....',
    '...smmmSmmms...',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'tiara')

SIREN_LIGHT = _frames('siren_light', [
    '.......r.......',
    '......rrR......',
    '......rRR......',
    '.....nNNNn.....',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], [
    '...p...r.......',
    '....p.pWr......',
    '...p..pRR......',
    '.....nNNNn.....',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], [
    '....p..p..p....',
    '......pWp......',
    '......rpr......',
    '.....nNNNn.....',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], [
    '.......r...p...',
    '......rWp.p....',
    '......rRp..p...',
    '.....nNNNn.....',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
])

CAPTAIN_HAT = _art([
    '....mmmmmmm....',
    '..mmWwwwwwwmm..',
    '..mWwwwwwwwwm..',
    '..mMMMMMMMMMm..',
    '...BBBBjBBBB...',
    '...nKjjjjjKn...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'captain_hat')

FEDORA = _art([
    '.....TT.TT.....',
    '....TtTTTTd....',
    '....tTTTTTd....',
    '....nKKKKKn....',
    '..TtTTTTTTTTd..',
    '...dd+++++dd...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'fedora')

LAUREL_WREATH = _art([
    '.a...........a.',
    '.gaa.......aag.',
    '..gGaa...aaGg..',
    '...GGGGrGGGG...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'laurel_wreath')

BUNNY_EARS = _frames('bunny_ears', [
    '...mm.....mm...',
    '..mwPm...mPwm..',
    '..mwPm...mPwm..',
    '..mwPm...mPwm..',
    '...mwm...mwm...',
    '...+++++++++...',
    '..++:+++++:++..',
], [
    '...mm..........',
    '..mwPm...mmm...',
    '..mwPm...mPwmm.',
    '..mwPm...mPwm..',
    '...mwm...mwm...',
    '...+++++++++...',
    '..++:+++++:++..',
])

CAT_EARS = _art([
    '...m.......m...',
    '...Nm.....mN...',
    '...NpN...NpN...',
    '...NppN.NppN...',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'cat_ears')

FISHING_HAT = _art([
    '.......ggggg....',
    '......ghgggGG...',
    '......ddddddd...',
    '...sgggggggggG..',
    '..s.GGG+++++GGG.',
    '.rr..+++++++++..',
    '.mN.++:+++++:++.',
], 'fishing_hat')

_SPROUT_STEM = [
    '.......G.......',
    '.......G.......',
    '...+++++++++...',
    '..++:+++++:++..',
]
SPROUT = _frames('sprout', [
    '.....ag.ga.....',
    '......gGg......',
] + _SPROUT_STEM, [
    '......ag.ga....',
    '.......gGg.....',
] + _SPROUT_STEM, [
    '.....ag.ga.....',
    '......gGg......',
] + _SPROUT_STEM, [
    '....ag.ga......',
    '.....gGg.......',
] + _SPROUT_STEM)

UNICORN_HORN = _art([
    '.......p.......',
    '.......l.......',
    '.......pv......',
    '......ppV......',
    '......plV......',
    '......llv......',
    '.....llppV.....',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'unicorn_horn')

RUBBER_DUCK = _art([
    '.....jj........',
    '....oYkj...j...',
    '.....jyyjjjyj..',
    '.....jyyyyyyj..',
    '......jjjjjj...',
    '...+++++++++...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'rubber_duck')

FEZ = _art([
    '.......JJ......',
    '......prRJ.....',
    '......rrRJ.....',
    '.....prrrRj....',
    '.....RRRRR.....',
    '...+++++++++...',
    '..++:+++++:++..',
], 'fez')

SOMBRERO = _art([
    '.......t.......',
    '......tTT......',
    '.....tttTT.....',
    '.....rgryr.....',
    't...tttttTT...T',
    'TttttttttttTTTT',
    '..TTTTTTTTTTT..',
    '...+++++++++...',
    '..++:+++++:++..',
], 'sombrero')

JESTER_HAT = _art([
    '.j...........j.',
    '.rr....j....bb.',
    '..Rr..rrb..bB..',
    '...rrrrbbbbb...',
    '...rrrrbbbbB...',
    '...jjyyjjyyj...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'jester_hat')

MUSHROOM_CAP = _art([
    '.....rrrrr.....',
    '...rrWWrrrrR...',
    '..rrrWrrrWWrR..',
    '.rWWrrrrrrrrRR.',
    '..RRRRRRRRRRR..',
    '...+++++++++...',
    '..++:+++++:++..',
], 'mushroom_cap')

ANTLERS = _art([
    't..t.......t..T',
    '.t.t.......t.T.',
    '..TT.......TT..',
    '...T.......T...',
    '...TT.....TT...',
    '...+++++++++...',
    '..++:+++++:++..',
], 'antlers')

ITEMS = [
    Item('beanie', 'head', 'Cozy violet knit beanie: ribbed cuff hugs his top row, pom-pom on top. Static; wear after put_clawd',
         BEANIE, tags=('hat', 'cozy')),
    Item('cap', 'head', 'Blue baseball cap in 3/4 view: bill pokes out left at his top row, eyes stay clear. Static; a raised left arm (up/high) passes under the bill',
         CAP, tags=('hat',)),
    Item('cap_back', 'head', 'The blue cap worn backwards: strap + gold snap on his top row, bill sticks out behind on the right. Static; right high/raise/wave pass under it',
         CAP_BACK, tags=('hat', 'cool')),
    Item('crown', 'head', 'Gold crown perched on his head: 3 points, red/blue gems, white glint. Static (done, victory)',
         CROWN, tags=('hat', 'done')),
    Item('party_hat', 'head', 'Pink/yellow party cone tilted right, 2-cell stripes along the lean, violet pom-pom. Static (done; add confetti)',
         PARTY_HAT, tags=('hat', 'done')),
    Item('wizard_hat', 'head', 'Deep violet wizard hat: gold band, floppy tip with gold tassel, two stars that trade a twinkle: frames 0-1 loop at ~900 ms (plan)',
         WIZARD_HAT, ms=900, tags=('hat', 'plan')),
    Item('top_hat', 'head', 'Charcoal top hat with red band and gray rims (reads on dark). Static; hello: lift it with dy=-1 and rarm=high (the arm tip meets the brim)',
         TOP_HAT, tags=('hat', 'hello')),
    Item('hard_hat', 'head', 'Yellow construction hard hat: center ridge, gold contour, brim shaded on the right. Static (edits / accept-edits mode)',
         HARD_HAT, tags=('hat', 'edits')),
    Item('chef_hat', 'head', 'Puffy two-lobed chef toque (11 wide) on a pleated band, paper white with a silver contour. Static (working)',
         CHEF_HAT, tags=('hat', 'working')),
    Item('nightcap', 'head', 'Blue/lavender striped nightcap drooping left, gold pom. Frames 0 rest, 1 tail out, 2 tail in: play 0,1,0,2 at ~500 ms (sleep)',
         NIGHTCAP, ms=500, tags=('hat', 'sleep')),
    Item('headphones', 'head', 'Over-ear headphones: gray band arched just over his head, violet cups on his top corners. Static; side/out/raise/wave arms stay clear, up/high pass behind the cups',
         HEADPHONES, tags=('music', 'vibe')),
    Item('headphones_glow', 'head', 'Headphones whose cups light up on the beat (same cells, lighter colors): frame 0 ~300 ms + frame 1 ~130 ms = one beat at 140 BPM (vibe)',
         HEADPHONES_GLOW, ms=[300, 130], tags=('music', 'vibe')),
    Item('propeller_beanie', 'head', 'Rainbow-panel beanie with a red propeller: frames 0-3 loop (blade 7-5-3-5 wide, far half shaded); ~100 ms spins, 160-220 ms idles (auto)',
         PROPELLER_BEANIE, ms=110, tags=('hat', 'auto')),
    Item('grad_cap', 'head', 'Mortarboard with gold button; tassel hangs at box x 11 (rows -1..1) and swings: frames 0-3 = rest, out, rest, in at [1100, 450, 900, 450] ms; cheer with the left arm (plan, done)',
         GRAD_CAP, ms=[1100, 450, 900, 450], tags=('hat', 'plan')),
    Item('cowboy_hat', 'head', 'Tan cowboy hat: pinched crown, dark band on a wide brim that curls up at both ends. Static (hello)',
         COWBOY_HAT, tags=('hat', 'hello')),
    Item('halo', 'head', 'Golden halo floating one row above his head, a glint sweeps across it: frames 0-3 at [1200, 110, 110, 900] ms (done, innocent)',
         HALO, ms=[1200, 110, 110, 900], tags=('fx', 'done')),
    Item('devil_horns', 'head', 'Two short curved red horns growing from his top corners. Static (mischief / bypass mode)',
         DEVIL_HORNS, tags=('bypass',)),
    Item('antenna', 'head', 'Robot antenna whose red ball blinks: frame 0 lit ~500 ms, frame 1 dim ~700 ms (alien, subagents)',
         ANTENNA, ms=[500, 700], tags=('tech',)),
    Item('bow', 'head', 'Big pink hair bow on his top-right corner: two loops, red knot, little tails. Static; a raised right arm (high/raise) tucks under it',
         BOW, tags=('cute',)),
    Item('flower', 'head', 'Pink flower growing from his head; sways: frames 0-3 = rest, right, rest, left at [900, 600, 900, 600] ms (idle, happy)',
         FLOWER, ms=[900, 600, 900, 600], tags=('cute', 'idle')),
    Item('viking_helmet', 'head', 'Steel viking helmet: gold riveted band, diagonal tan horns. Static',
         VIKING_HELMET, tags=('hat',)),
    Item('bandana', 'head', 'Red ninja bandana tied round his head (rows 0-1, so no dy landing lag), tails stream left: frame 0 rest, 1-2 a ripple at [1200, 180, 180] ms; or hold 0 for 1.5-3 s between gusts',
         BANDANA, ms=[1200, 180, 180], tags=('bypass', 'cool')),
    Item('miner_helmet', 'head', 'Green miner helmet with a headlamp (gray housing, warm lens); frame 1 brightens the lamp: pulse at [600, 300] ms (working, search)',
         MINER_HELMET, ms=[600, 300], tags=('hat', 'working')),
    # ---- extras
    Item('santa_hat', 'head', 'Red Santa hat with a fluffy white cuff, tip flops right into a white pom. Static (seasonal); right raise/wave pass under the pom',
         SANTA_HAT, tags=('hat', 'seasonal')),
    Item('pirate_hat', 'head', 'Black pirate bicorn with gold trim and a white skull & jaw. Static (bypass mode, daring)',
         PIRATE_HAT, tags=('hat', 'bypass')),
    Item('beret', 'head', 'Red artist beret slouched to the right, little stem on top. Static (plan, creative)',
         BERET, tags=('hat', 'plan')),
    Item('tiara', 'head', 'Small silver tiara with a pink center gem, perched on his head. Static (cute, done)',
         TIARA, tags=('cute', 'done')),
    Item('siren_light', 'head', 'Red rotating beacon on his head: frames 0-3 loop at ~160 ms (alert: needs permission)',
         SIREN_LIGHT, ms=160, tags=('alert',)),
    Item('captain_hat', 'head', 'White captain hat, navy band with gold badge, black visor + gold braid. Static (subagents lead)',
         CAPTAIN_HAT, tags=('hat', 'subagents')),
    Item('fedora', 'head', 'Brown detective fedora with pinched crown and black band. Static (plan, search; pair with magnifier)',
         FEDORA, tags=('hat', 'plan')),
    Item('laurel_wreath', 'head', 'Green laurel wreath round his top row: leaves fan up and out from a red front berry. Static (done, victory)',
         LAUREL_WREATH, tags=('done',)),
    Item('bunny_ears', 'head', 'White bunny ears with pink insides; frame 1 = right ear tip flops: hold frame 0 ~2 s, twitch ~160 ms',
         BUNNY_EARS, ms=[2000, 160], tags=('cute',)),
    Item('cat_ears', 'head', 'Gray cat ears with pink insides on his top corners. Static (cute)',
         CAT_EARS, tags=('cute',)),
    Item('fishing_hat', 'head', 'Green bucket hat with a red/gray bobber on a line hanging left. Static (hooks; pair with fishing_rod)',
         FISHING_HAT, tags=('hat', 'hooks')),
    Item('sprout', 'head', 'Tiny two-leaf sprout growing from his head; sways: frames 0-3 = rest, right, rest, left at [1000, 600, 800, 600] ms (manual, new idea)',
         SPROUT, ms=[1000, 600, 800, 600], tags=('cute', 'idle')),
    Item('unicorn_horn', 'head', 'Slim pastel unicorn horn with pink/lavender spiral bands, perched on his head. Static (magic, auto)',
         UNICORN_HORN, tags=('cute', 'magic')),
    Item('rubber_duck', 'head', 'Yellow rubber duck with a gold contour sitting on his head (rubber-duck debugging!). Static (thinking, debugging)',
         RUBBER_DUCK, tags=('cute', 'thinking')),
    Item('fez', 'head', 'Small red fez with a gold tassel falling to the right. Static',
         FEZ, tags=('hat',)),
    Item('sombrero', 'head', 'Wide straw sombrero with a colorful band and upturned brim. Static (siesta / rate-limit wait)',
         SOMBRERO, tags=('hat', 'rate-limit')),
    Item('jester_hat', 'head', 'Red/blue three-point jester hat with gold bells and a gold band. Static (hooks, playful)',
         JESTER_HAT, tags=('hat', 'hooks')),
    Item('mushroom_cap', 'head', 'Red mushroom cap worn as a hat: white spots, dark rim. Static (cute, idle)',
         MUSHROOM_CAP, tags=('hat', 'cute')),
    Item('antlers', 'head', 'Branching reindeer antlers growing from his top corners. Static (seasonal, winter)',
         ANTLERS, tags=('seasonal',)),
]
