"""Face accessories: eyewear, face marks and little face effects.

Slot 'face' anchors on the point between Clawd's eyes (box (5, 2) when standing). Every sprite in this
module is authored in Clawd's own box coordinates (11 columns, x 0..10) via _f(rows, top, left), so
what you see in the strings is exactly where it lands on him:

    box x:  0 1 2 3 4 5 6 7 8 9 10       body = x 1..9, rows 0..5; eyes = holes at (2,2) and (8,2);
    row 0:  . # # # # # # # # # .        arm stubs at x 0 and 10, rows 2..3 (never cover them).
    row 2:  # # O # # # # # O # #        Face items mostly sit ON his orange body, so they use
    row 3:  # # # # # # # # # # #        colors that contrast with orange; wherever a pixel touches
                                         the background it is a mid-tone (two-theme rule).

Eye cells: his glances (look_*) move each eye hole one cell, so each eye can be anywhere in x 1..3 /
7..9, rows 1..3. Items that leave the eyes visible keep those cells free or say which glances they hide.
Arms: like every face item, these draw over an arm that crosses in front of his face (larm/rarm
'front' or 'chin'); descs only call out the other arm shapes an item touches.
'Screen-left' / 'screen-right' = the side as you look at him (sprite.flipped() via frame.place mirrors).
"""
from clawdlib import Item, Sprite


def _f(rows, top, left=0):
    """Sprite drawn in Clawd's box coordinates: rows[0] is box row `top`, column 0 is box x `left`.
    The anchor is the face point, box (5, 2)."""
    return Sprite(rows, anchor=(5 - left, 2 - top))


def _anim(frames, top, left=0):
    return [_f(r, top, left) for r in frames]


# =============================================================================================
# Eyewear
# =============================================================================================

# Classic dark shades. Flat top bar with gray hinge tips (they keep his outline on the dark theme),
# rounded lens bottoms with a nose notch, one crisp diagonal glint on the left lens and a dim echo
# on the right lens (light from the top-left).
_SHADES = ['.NkkkkkkkN.',
           '.kkWkkkknk.',
           '..Wkk.kkk..']
SUNGLASSES = Item('sunglasses', 'face',
                  'Classic dark shades with a white glint, covering both eyes. Wear after put_clawd; '
                  'eyes open/blink (look_dl/dr peek out under a lens). Peek over them: dy=2 with eyes open/look_u',
                  _f(_SHADES, top=1),
                  tags=('cool', 'bypass', 'vibe'))

# "Deal with it" 8-bit shades: 11 wide (the bar pokes past his head above the arm stubs), blocky
# lenses, a white diagonal glint in each lens. The top bar is graphite with gray tips (lit top edge),
# so the shades keep a visible outline on the dark theme while they drop in from above his head.
PIXEL_SHADES = Item('pixel_shades', 'face',
                    'Meme "deal with it" 8-bit shades, wider than his head, glint in each lens. Wear after put_clawd. '
                    'Drop-in: wear with dy=-6,-4,-2 (~100 ms each), land at dy=0 and hold. Arms up/high: tip covers the arm',
                    _f(['NnnnnnnnnnN',
                        '.kkWkkkkWk.',
                        '.kWkk.kWkk.',
                        '..kk...kk..'], top=1),
                    tags=('cool', 'meme', 'bypass', 'done'))

# Aviators: bright gold brow bar (double bridge), teardrop lenses drooping toward the nose,
# navy-to-cyan gradient tint, darker gold under-rims.
AVIATORS = Item('aviators', 'face',
                'Gold aviators, teardrop lenses with a navy-to-cyan gradient. Wear after put_clawd; '
                'eyes open/blink (look_dl/dr peek out under a lens)',
                _f(['.jyyyyyyyj.',
                    '.jBBBjBBBj.',
                    '..jccjccj..',
                    '...JJ.JJ...'], top=1),
                tags=('cool', 'auto', 'vibe'))

# Thick nerd frames around each eye. Each rim is bevelled like a real frame: gray on the lit top and
# left edges, graphite on the bottom and right, a charcoal corner, and the bridge in the same
# graphite. The gray inner edge keeps his eye holes readable on the dark theme.
_NERD = ['.NNn...NNn.',
         '.N.nnnnN.n.',
         '.nnK...nnK.']
NERD_GLASSES = Item('nerd_glasses', 'face',
                    'Thick nerd frames, his eyes show inside the rims. Wear after put_clawd; '
                    'eyes open/blink only (look_*/closed hide under the rims)',
                    _f(_NERD, top=1),
                    tags=('smart', 'thinking', 'plan'))

# Tortoiseshell half-moon reading glasses perched low on his face: he peeks over them. Two small
# cyan-tinted lenses (no white highlight: near-white glass read as teeth at real size), dark-wood
# rims below, lighter wood frame ends right under his eyes so the eye holes stay crisp on both themes.
READING_GLASSES = Item('reading_glasses', 'face',
                       'Tortoiseshell half-moon reading glasses below his eyes, he peeks over them. '
                       'Wear after put_clawd; eyes open/blink/look_l/r/u; for look_d* wear with dy=1',
                       _f(['..TccdccT..',
                           '...dd.dd...'], top=3),
                       tags=('plan', 'thinking', 'calm'))

# Monocle on his screen-left eye: gold ring bevelled from the top-left (pale-gold glint on the
# outer corner, dark gold on the shadow side), the eye visible inside, and a short chain draped
# across his cheek.
MONOCLE = Item('monocle', 'face',
               'Gold monocle around his screen-left eye (eye stays visible) + chain draped on his cheek. '
               'Wear after put_clawd; eyes open/blink (look_* hide that eye); avoid larm front/chin',
               _f(['.yjj..',
                   '.j.J..',
                   '.jJJ..',
                   '....J.',
                   '.....J'], top=1),
               tags=('fancy', 'thinking'))

# Cardboard 3D glasses: rounded paper frame (shaded underside with a nose notch), red and cyan gels
# with a gloss pixel each.
GLASSES_3D = Item('glasses_3d', 'face',
                  'Red/cyan cardboard 3D glasses. Wear after put_clawd (covers both eyes, any eyes)',
                  _f(['..wwwwwww..',
                      '.wprrwCccw.',
                      '.wrrrwcccw.',
                      '..MMM.MMM..'], top=1),
                  tags=('fun', 'vibe'))

# VR headset: chunky charcoal visor (nose notch) on a graphite head band whose gray strap ends show
# at both sides. The eye strip glows cyan; every couple of seconds an ice highlight scans across it.
_VR_TOP = 'NnnnnnnnnnN'
_VR_LOW = ['.KKKKKKKKK.',
           '..KKK.KKK..']
VR_HEADSET = Item('vr_headset', 'face',
                  'VR headset: charcoal visor with a glowing eye strip and a scan sweep. Wear after put_clawd. '
                  'Loop 0 (hold ~2.2 s) then 1-3 (~90 ms each); still = 0. Arms up/high: strap covers the arm',
                  _anim([[_VR_TOP, '.KbcccccbK.'] + _VR_LOW,
                         [_VR_TOP, '.KbCccccbK.'] + _VR_LOW,
                         [_VR_TOP, '.KbccCccbK.'] + _VR_LOW,
                         [_VR_TOP, '.KbccccCbK.'] + _VR_LOW], top=1),
                  ms=[2200, 90, 90, 90], tags=('working', 'auto', 'vibe'))

# Workshop goggles: round brass rims (highlight top-left, dark gold bottom-right), cyan-tinted
# lenses with a glint, leather bridge + strap peeking out at both sides of his head.
GOGGLES = Item('goggles', 'face',
               'Brass workshop goggles over his eyes, strap peeking out at both sides. Wear after put_clawd; '
               'eyes open/blink (look_dl/dr peek out). Edits. Arms up/high: strap covers the arm',
               _f(['..jj...jj..',
                   'TyWcJTyWcJT',
                   '.jccJ.jccJ.',
                   '..JJ...JJ..'], top=0),
               tags=('edits', 'working', 'building'))

# =============================================================================================
# Face marks
# =============================================================================================

# Pirate eye patch over his screen-left eye: shield-shaped patch with a graphite sheen, strap
# running diagonally up over his head; where the strap crosses his head's top edge it catches the
# light (gray), so it reads on the dark theme too.
EYE_PATCH = Item('eye_patch', 'face',
                 'Pirate eye patch over his screen-left eye, strap running up over his head. Wear after put_clawd; '
                 'the free eye can glance (avoid look_u*: the hidden eye would peek over the patch)',
                 _f(['......NN...',
                     '....kk.....',
                     '.nkk.......',
                     '.kkk.......',
                     '..k........'], top=0),
                 tags=('pirate', 'bypass', 'fun'))

# Curly handlebar mustache: thick lobes under the nose (each lit on its top-left), thin sweeps,
# tips curling up.
MUSTACHE = Item('mustache', 'face',
                'Curly handlebar mustache under his eyes. Wear after put_clawd; '
                'eyes open/blink/look_l/r/u (downward glances land in it)',
                _f(['.e.deede.e.',
                    '..eee.eee..'], top=3),
                tags=('fancy', 'fun'))

# Soft pink cheeks (a bigger, softer version of the kit's blush pixel), low enough to clear every
# glance.
BLUSH = Item('blush', 'face',
             'Soft pink cheek pads under both eyes. Wear after put_clawd. Not for the plain-face user set '
             '(STYLE section 0: lint flags it)',
             _f(['..pp...pp..'], top=4),
             tags=('cute', 'happy', 'shy'))

# Big round clown nose between his eyes: pink lit rim and a white glint on the top-left, red body,
# dark-red shadow crescent on the bottom-right that also outlines it against his orange.
CLOWN_NOSE = Item('clown_nose', 'face',
                  'Big shiny red clown nose between his eyes. Wear after put_clawd; '
                  'eyes open/blink/look_l/r/u/d (look_dl/dr hide one eye behind it)',
                  _f(['.prr.',
                      'pWrrR',
                      'rrrRR',
                      '.RRR.'], top=2, left=3),
                  tags=('fun', 'silly'))

# Cheek band-aid on his lower screen-right cheek: paper strip lit from the top-left (white -> light
# gray -> silver on the shadow corner), tan pad in the middle. It sits below every eye cell, so all
# glances (also look_d) stay visible, and off-center so it never reads as teeth.
BANDAID = Item('bandaid', 'face',
               'Band-aid on his lower screen-right cheek (ouch / error). Wear after put_clawd; works with every eye '
               '(incl. look_d)',
               _f(['wttM',
                   'MTTm'], top=4, left=6),
               tags=('error', 'ouch'))

# =============================================================================================
# Face effects (animated)
# =============================================================================================

# Anime sweat drop beside the top-right of his head (slot 'face' so it follows him). A plump
# teardrop with its tip leaning toward his head: cyan body, ice/white glint top-left, blue shadow
# bottom-right. Loop: it rests, slides down, stretches, drips off, is gone for a beat, and a new
# bead wells up. It stays at x 11..14, clear of his head and arm stub.
_DROP = ['c...',
         'cc..',
         'cWcb',
         'cCcb',
         '.bb.']
SWEAT_DROP = Item('sweat_drop', 'face',
                  'Sweat drop beside his head (follows him): 0 rest, 1-2 slide, 3 stretch, 4 drip, 5 gone, 6 new bead. '
                  'Loop ~[700,180,140,100,100,450,160] ms or hold 0. Right arm not raise/wave/point',
                  [_f(_DROP, top=-4, left=11),
                   _f(_DROP, top=-3, left=11),
                   _f(_DROP, top=-2, left=11),
                   _f(['c...',
                       'cc..',
                       'cWc.',
                       'cCcb',
                       '.cbb',
                       '..b.'], top=-2, left=11),
                   _f(['c',
                       'b'], top=4, left=13),
                   _f(['.'], top=0, left=11),
                   _f(['cc',
                       'cb'], top=-2, left=11)],
                  ms=[700, 180, 140, 100, 100, 450, 160], tags=('nervous', 'error', 'rate-limit'))

# Tear running down his screen-left cheek: the stream starts one cell below the eye (so look_d
# makes it flow straight out of the eye instead of covering it). Frame 0 (the still): a drop gathers
# under his body; 1: it falls between his legs; 2: a fresh ice glint at the top, which slides down
# into frame 0 again.
TEAR = Item('tear', 'face',
            'Tear running down his screen-left cheek, dripping between his legs. Loop 0-2 ~[450,130,200] ms. '
            'Wear after put_clawd; any eyes (look_d: flows from the eye); dx=6 for the other eye',
            _anim([['c',
                    'C',
                    'c'],
                   ['c',
                    'c',
                    '.',
                    'c'],
                   ['C',
                    'c']], top=4, left=2),
            ms=[450, 130, 200], tags=('sad', 'error'))

# Anime anger vein (cross-popping vein) floating off the top-left of his head, one clean cell away
# from it. Frame 0 = relaxed 5x5 mark, frame 1 = throbbing 7x7; both have dark-red bends.
_ANGER0 = ['.......',
           '..r.r..',
           '.rR.Rr.',
           '.......',
           '.rR.Rr.',
           '..r.r..',
           '.......']
_ANGER1 = ['..r.r..',
           '..r.r..',
           'rrR.Rrr',
           '.......',
           'rrR.Rrr',
           '..r.r..',
           '..r.r..']
ANGER_MARK = Item('anger_mark', 'face',
                  'Anime anger vein off the top-left of his head (slot face, follows him). '
                  'Frames 0-1 throb ~[380,160] ms. Left arm not high/raise/wave',
                  _anim([_ANGER0, _ANGER1], top=-6, left=-5),
                  ms=[380, 160], tags=('angry', 'error'))

# =============================================================================================
# Extras
# =============================================================================================

# The workshop goggles pushed up onto his forehead (calm "edits" idle: eyes stay expressive).
# Squashed 3-row rims; the top rims peek over his head (gold, not yellow, where they touch the
# background), strap stubs at both top corners.
GOGGLES_UP = Item('goggles_up', 'face',
                  'Brass goggles pushed up on his forehead, eyes free (calm edits idle). Wear after put_clawd; '
                  'any eyes. Arm high: strap covers the arm',
                  _f(['..jj...jj..',
                      'TjWcJTjWcJT',
                      '..JJ...JJ..'], top=-1),
                  tags=('edits', 'building', 'calm'))

# Lavender sleep mask with embroidered closed eyes (a 'v' lash line centered on each eye), elastic
# strap peeking out at both sides.
SLEEP_MASK = Item('sleep_mask', 'face',
                  'Lavender sleep mask with embroidered closed eyes. Wear after put_clawd (eyes closed). Sleep. '
                  'Arms up/high: strap covers the arm',
                  _f(['vlLLLLLLLlv',
                      '.VlVlllVlV.',
                      '.lVll.llVl.'], top=1),
                  tags=('sleep', 'calm'))

# Black domino mask with white hero lenses and flared gray-tipped wings (bypass: daring).
HERO_MASK = Item('hero_mask', 'face',
                 'Black domino hero mask with white lens eyes. Wear after put_clawd; eyes open/blink '
                 '(look_dl/dr peek out). Bypass / daring. Arms up/high: wing tip covers the arm',
                 _f(['Nkkkk.kkkkN',
                     '.kWWkkkWWk.',
                     '..kkk.kkk..'], top=1),
                 tags=('bypass', 'cool', 'hero'))

# Spa cucumber slices over both eyes: dark green skin, pale flesh, glossy seed highlight.
CUCUMBER_SLICES = Item('cucumber_slices', 'face',
                       'Spa cucumber slices over both eyes (pair with a towel on his head). '
                       'Wear after put_clawd; eyes open/blink/closed (look_dl/dr peek out). Vibe',
                       _f(['..gg...gg..',
                           '.gYhG.gYhG.',
                           '.ghhG.ghhG.',
                           '..GG...GG..'], top=0),
                       tags=('vibe', 'chill', 'calm'))

# Party blowout from his mouth: a navy mouthpiece, a striped paper tube (red + yellow on his body,
# red + gold past it so the stripes hold on both themes). Frame 0: the rest is rolled into a red
# coil ring (lit top-left, open center); 1: half unrolled, the end still hooked under; 2: blown out
# straight with a pink fringe.
PARTY_BLOWER = Item('party_blower', 'face',
                    'Party blowout in his mouth: 0 rolled coil, 1 unrolling, 2 blown with fringe. '
                    'Play 0,1,2,1 ~[300,80,500,80] ms (still: 2). Wear after put_clawd; right arm not down',
                    _anim([['.............',
                            '.............',
                            'BRyRyRrR.....',
                            '.....r.R.....',
                            '.....RRR.....'],
                           ['.............',
                            '.............',
                            'BRyRyRjRjR...',
                            '........rR...',
                            '.............'],
                           ['...........p.',
                            '...........pp',
                            'BRyRyRjRjRjpp',
                            '...........p.',
                            '.............']], top=2, left=5),
                    ms=[300, 80, 500, 80], tags=('done', 'hello', 'party'))

# Bubblegum: a round pink bubble (white glint top-left, pale fill, pink rim) blown from his mouth.
# 0 = big bubble (the still), 1 = pop: bits fly out (kept off his eye row and his legs), 2 = the gum
# left at his mouth, 3 = small bubble, 4 = medium bubble, back to 0.
GUM_BUBBLE = Item('gum_bubble', 'face',
                  'Bubblegum: 0 big bubble (still), 1 pop, 2 gum, 3 small, 4 medium. Loop ~[900,110,700,260,300] ms; '
                  'for idle hold 0 or 2 for 2-4 s. Wear after put_clawd',
                  [_f(['.ppp.',
                       'pWPPp',
                       'pPPPp',
                       'pPPPp',
                       '.ppp.'], top=2, left=3),
                   _f(['...p.p...',
                       '.........',
                       '.........',
                       'p.......p',
                       '.........',
                       '...p.p...'], top=1, left=1),
                   _f(['p'], top=4, left=5),
                   _f(['.p.',
                       'pPp',
                       '.p.'], top=3, left=4),
                   _f(['.ppp.',
                       'pWPPp',
                       'pPPPp',
                       '.ppp.'], top=3, left=3)],
                  ms=[900, 110, 700, 260, 300], tags=('vibe', 'idle', 'fun'))

# The classic shades with an anime "ting!": frame 0 is exactly SUNGLASSES; the glint sweeps across
# to the right lens, then a cyan-white twinkle pops just off his head's top-right corner and fades.
_TING_SKY = ['.............', '.............', '.............']
_TING_PLUS = ['...........c.', '..........cWc', '...........c.']
_TING_DOT = ['.............', '...........c.', '.............']
_TING_R = ['.NkkkkkkkN...', '.kkkkkkkWk...', '..kkk.kWk....']
SUNGLASSES_GLINT = Item('sunglasses_glint', 'face',
                        'Sunglasses with a "ting" shine: 0 rest (= sunglasses), 1-2 glint sweeps right, 3 twinkle, 4 fade. '
                        '~[4200,60,60,180,110] ms; vary the rest 3-6 s per cycle. Bypass / done. Right arm not raise/wave',
                        _anim([_TING_SKY + [r + '..' for r in _SHADES],
                               _TING_SKY + ['.NkkkkkkkN...', '.kkkkWkkkk...', '..kkW.kkk....'],
                               _TING_SKY + _TING_R,
                               _TING_PLUS + _TING_R,
                               _TING_DOT + _TING_R], top=-2),
                        ms=[4200, 60, 60, 180, 110], tags=('cool', 'bypass', 'done'))

# Party star glasses: a 5-point star over each eye (pale highlight top-left, gold tips where they
# touch the background, dark-gold shadow), joined by a dark-gold bridge so they read as glasses.
STAR_GLASSES = Item('star_glasses', 'face',
                    'Yellow star-shaped party glasses over both eyes. Wear after put_clawd; eyes open/blink '
                    '(look_d* peek out under the stars). Done / celebrate. Arms up/high: star tip covers the arm',
                    _f(['..j.....j..',
                        'jYyyjJyYyyj',
                        '.yyj...yyj.',
                        '.j.J...j.J.'], top=0),
                    tags=('done', 'party', 'fun'))

# A red rose held in his mouth: dark green stem with a two-tone leaf hanging under it, the bloom
# just past his body, one cell below his arm stub (so it does not look held in his hand).
MOUTH_ROSE = Item('mouth_rose', 'face',
                  'Red rose held in his mouth, stem out to the right, bloom below his arm. Wear after put_clawd. '
                  'Hello / charming',
                  _f(['GGGGG.pr',
                      '..aG.rRr',
                      '......RR'], top=4, left=5),
                  tags=('hello', 'charming', 'vibe'))

# Groucho disguise: the bevelled nerd frames (eyes visible), big pink nose lit from the top-left,
# bushy mustache.
DISGUISE_GLASSES = Item('disguise_glasses', 'face',
                        'Groucho disguise: thick glasses + big pink nose + mustache, eyes show. Wear after put_clawd; '
                        'eyes open/blink only',
                        _f(['.NNn...NNn.',
                            '.N.nnPnN.n.',
                            '.nnKPPpnnK.',
                            '..eeepeee..'], top=1),
                        tags=('fun', 'silly', 'incognito'))

# Outlaw bandana tied over his lower face (bypass: cool, daring): red cloth with white polka dots,
# shadowed on the right, its point hanging into the gap between his legs. Eyes stay free above it.
OUTLAW_BANDANA = Item('outlaw_bandana', 'face',
                      'Red polka-dot outlaw bandana over his lower face, point hanging between his legs. '
                      'Wear after put_clawd; eyes open/blink/look_l/r/u (look_d* land in it). Bypass / daring',
                      _f(['.rrrrrrrrr.',
                          '.rrWrrrWrR.',
                          '..rrrWrrR..',
                          '....rRR....',
                          '.....R.....'], top=3),
                      tags=('bypass', 'cool', 'daring'))

ITEMS = [
    SUNGLASSES, PIXEL_SHADES, AVIATORS, NERD_GLASSES, READING_GLASSES, MONOCLE, GLASSES_3D,
    VR_HEADSET, GOGGLES, EYE_PATCH, MUSTACHE, BLUSH, CLOWN_NOSE, SWEAT_DROP, TEAR, BANDAID,
    ANGER_MARK,
    GOGGLES_UP, SLEEP_MASK, HERO_MASK, CUCUMBER_SLICES, PARTY_BLOWER, GUM_BUBBLE,
    SUNGLASSES_GLINT, STAR_GLASSES, MOUTH_ROSE, DISGUISE_GLASSES, OUTLAW_BANDANA,
]
