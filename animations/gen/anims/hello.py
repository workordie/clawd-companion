# ======================================================================================
# USER FEEDBACK: the user reviewed this fine-face upgrade draft personally and approved it
# ("looks great go"). Keep the scene, beats and fine-line expressions; critics, fixers and judges
# should polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""hello - Session start: the Claude panel just opened.  Preview:  python3 gen/preview.py anim hello

Clawd the dapper host (library top_hat with a little flower tucked in its band) welcomes you: a
cheerful wave, a happy hop that pops his hat off, and a polite hat tip. His heart speech bubble
goes ba-dump along with him; gold sparkles twinkle around the scene. Hello is on screen for only
2-4 s, so the whole story (wave, hop, hat gag, tip) is told by ~2.3 s and the rest of the loop
keeps waving. Clawd is grounded at HOME from 0.97 s to 4.18 s (the second take-off), so the
switch to idle anywhere in the 2-4 s window never catches him mid-air.
EXPRESSIVE STYLE (STYLE.md 0b): his face acts with the fine-line kit (half-size pixels): a big
happy greeting, wide-eyed surprise, a bonk flinch, a friendly wink, twinkling sparkle eyes. No
mouth, no blush, never resized; every face change lands on a body key.

STORYBOARD (ms; every layer shares one 3570 ms timeline, and every accent starts on a body key)
     0  HELLO (frame 0 = the reduced-motion still): at HOME, left arm up in a wave with a steel "("
        swish, HAPPY fine arcs (the big smiling greeting), top hat on, heart bubble beside the hat,
        a big gold star by the hand.
     0  wave / raise / wave (outer holds 220 and 150, inner 90); the swish swings with the hand;
        the star fades (long plus, plus, dot). The heart goes ba- at 310 (outer swing) ...
   460  anticipation (normal body size, user preference): the right arm drops first, then the
        waving arm follows, both down (520) ... -dump (520). The smile opens (half > open): eyes
        on you, "watch this"
   610  take-off: 2 cells up, legs still extended from the push-off, arms swinging up through
        'out'; the hat rides along seated, the flower lags a row; a glint answers bottom right
   680  apex, 3 up, legs tucked, arms up: the hat pops off (rising 2, then 1 row), drifting a cell
        left on its arc; his eyes are still on you ... 780 the gap opens over his head: NOW his
        eyes go WIDE ("whoa, my hat!", held 190 ms: the cause first, then the take)
   910  falls (arms trail up) ... 970 lands (arms out, dust puff) while the hat is 3 rows up: his
        eyes roll up to follow it down (look_u)
  1070  the hat drops (the flower trails above it) ... 1160 PLOP, 190 ms after him: the hat (not
        Clawd) squashes, crown 1 row lower and 2 wider, specks fly off the brim, the flower springs
        up 2, the heart beats, a glint answers on the left; he keeps his full height, but BONK:
        his eyes squeeze shut (thin lines)
  1270  the hat rebounds 1 row (the flower comes down to meet it), the specks fly a cell further
        out, and his eyes ease open where he is about to look (a half lid, raised) ...
  1370  it settles: he glances up (is it back?), a deliberate 260 ms look
  1630  HAT TIP: eyes back on you, the hand rises (up, raise) to the brim ... 1820 he tips it: the
        left half of the hat lifts onto his hand (tilted hat, pulled a cell toward the hand) and the
        crown corner glints (dot, plus, X, plus); the eye under the lifted brim closes (half) ...
  1920  the bow: a friendly WINK (a thin happy arc held 410 ms beside one open eye) and the other
        hand on his belly; ba-dump at 2050 and 2240: on the -dump the open eye's lid comes down
        (half) ...
  2330  the hat drops back onto his head (the flower bobs) and both eyes close (line > half 2420):
        a full smooth blink for the open eye ... 2520 his eyes open SPARKLING (a white glint in
        each black eye) while the hand lingers at the brim; a glint answers at bottom right (2420)
  2620  and waves again, starry-eyed: wave / raise x3 (outer holds 250, 160, 270); at 2870 the
        sparkle TWINKLES (a second glint in each eye) and a glint low on the left answers (2960)
        ... 3060 the sparkle closes (half > line 3120) and curves into the happy arcs (3210) again;
        the star builds again from 3210 (dot, plus, long plus: the mirror of its fade)
  3570  = frame 0 (seamless: the last frame is the inner 'raise' swing, happy arcs, the star at full
        size)
Face beats (fine kit, black eyes): happy 0-460 | half 460 | open 520-780 | WIDE 780-970 | look_u
970 | line 1160 (bonk) | raised half 1270 | look_u 1370 | open 1630 | wink 1820-2330 (half, then a
thin arc for 410 ms; the open eye's lid starts down at 2240) | blink 2330 (line, half) | SPARKLE
2520-3060 (twinkle 2870) | half 3060 | line 3120 | happy 3210 -> loop. Lids close and open through
an in-between (half or line); only the surprise (wide) and the bonk flinch snap, on purpose.
Layers (back to front): bubble (static) | trunk (the kit body with no arms; it only changes in the
hop: 5 frames) | limbs (the rest of his body: arms, swish, dust; trunk + limbs = the kit pose, see
body()) | face (FINE: only the half-size eye pixels: black eyes, arcs, lines, glints; his eye
window stays plain orange in the body, so body frames merge while only his face acts; see _split)
| hat (own layer with the body's timing, so its frames merge while it rests) | fx (heartbeat
overlay + sparkles + the hat's "ting", one layer on the same loop: hello lives for 2-4 s, so the
accents are choreographed, not drifting; see fx()).
Trunk, limbs, face and hat are cut from the same KEYS, so the face never drifts off his body.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'hello'
STATE = 'Session start: the Claude panel just opened'
DESC = ('Waves hello in a top hat with happy smiling eyes, hops so high his hat pops off (wide-eyed '
        'whoa) and bonks back a beat late, then tips it to you with a wink and waves on, starry-eyed, '
        'while his heart bubble beats.')

HAT = get('top_hat')
DUST = get('dust_puff')
SPK = get('sparkle')
SPS = get('sparkle_small')

# ---------------------------------------------------------------------------------------------
# Compact heart bubble (local): the library bubble_heart is 11 wide; beside the top hat's 11-wide
# brim it would touch the brim or the canvas edge. Same style (gray contour, paper fill, white
# glint top-left, light-gray shade bottom-right, same tail), 9 wide. Anchor = the tail tip.
# ---------------------------------------------------------------------------------------------
_BUB_ROWS = [
    '..NNNNN..',
    '.NWwwwwN.',
    'NwwrwrwwN',
    'NwrWrrrwN',
    'NwrrrrRwN',
    'NwwrrRwMN',
    'NwwwrwwMN',
    '.NwwwwMN.',
    '.NwwNNN..',
    '.NwN.....',
    'NNN......',
]
_BEAT_ROWS = [                 # the heart swells to fill the bubble (heart_big shape)
    '..NNNNN..',
    '.NrrwrrN.',
    'NrWprrrrN',
    'NrprrrrRN',
    'NwrrrrRwN',
    'NwwrrRwMN',
    'NwwwrwwMN',
    '.NwwwwMN.',
    '.NwwNNN..',
    '.NwN.....',
    'NNN......',
]
BUB = Sprite(_BUB_ROWS, anchor=(0, 10), name='bubble_heart_compact')
BUB_BEAT = Sprite(_BEAT_ROWS, anchor=(0, 10), name='bubble_heart_beat')
TIP = (22, 11)       # tail tip: one empty column right of the hat brim; bubble spans x 22-30, y 1-11


def _diff(a, b):
    """Frame with only the cells where b differs from a (an overlay drawn on top of a)."""
    f = Frame()
    for (x, y), ch in b.px.items():
        if a.px.get((x, y)) != ch:
            f.put(x, y, ch)
    return f


def _bubble(spr):
    f = Frame()
    f.place(spr, TIP[0], TIP[1])
    return f


BUBBLE = _bubble(BUB)
BEAT = _diff(BUBBLE, _bubble(BUB_BEAT))

# ---------------------------------------------------------------------------------------------
# The hat and its local variants, all derived from the library top_hat (box coordinates: brim
# bottom row y=0 on his top row, brim x 0-10, crown x 2-8, band y=-2, crown top y=-6).
# ---------------------------------------------------------------------------------------------
_H0 = HAT.sprite(0)
# Graphite underside in EVERY frame: on his head it sits fine on orange, and in the air (or over
# look_u eye holes) a charcoal underside would vanish on the dark theme. One underside = no shade pops.
_HAT = Sprite(cells=[(x, y, ('n' if (y == 0 and ch == 'K') else ch)) for x, y, ch in _H0.cells],
              anchor=(_H0.ax, _H0.ay), name='top_hat_rimmed')


def _lift_cols(spr, cols, name):
    """Tilt: the given box columns move up one row (the rest stays put as the pivot)."""
    return Sprite(cells=[(x, y - (1 if x in cols else 0), ch) for x, y, ch in spr.cells],
                  anchor=(spr.ax, spr.ay), name=name)


def _squash(spr, name):
    """Impact squash: the crown loses a body row (y=-4) and gets one column wider on each side
    (the centre column is repeated); brim unchanged, so it still sits on his top row."""
    cells = []
    for x, y, ch in spr.cells:
        if y == -4:
            continue
        yy = y + 1 if y < -4 else y
        if y > -2:                                   # brim rows stay as they are
            cells.append((x, yy, ch))
        elif x < 5:
            cells.append((x - 1, yy, ch))
        elif x > 5:
            cells.append((x + 1, yy, ch))
        else:
            cells += [(4, yy, ch), (5, yy, ch), (6, yy, ch)]
    return Sprite(cells=cells, anchor=(spr.ax, spr.ay), name=name)


# Hat tip: the left 6 columns lift a row, so the crown top, band and brim each get one clean step;
# the right half of the brim stays seated on his head (the pivot). Worn with hdx=-1 the raised left
# brim end lands right on the 'raise' hand at (9,12), and the crown's top-left corner is (11,5).
_HAT_TIP = _lift_cols(_HAT, set(range(0, 6)), 'top_hat_tipped')
_HAT_SQUASH = _squash(_HAT, 'top_hat_squashed')

# a little flower tucked into the hat band (local): pink petals, yellow heart, a green leaf
_FLOWER = Sprite([
    '.p.',
    'pyp',
    'gp.',
], anchor=(1, 1), name='hat_flower')
_FLOWER_AT = (3, -3)          # relative to the hat anchor (his head-top center): right end of the band

# impact specks flicking off both brim ends on the plop (clear of the bubble tail at (22, 11)), and
# one cell further out on the rebound (they travel, then they are gone); the upper-right speck stops
# there, because one cell further it would touch the bubble tail
_SPECKS = {1: [(9, 10), (8, 12), (21, 10), (22, 13)],
           2: [(8, 9), (7, 12), (23, 13)]}

# steel "(" swish just outside the waving hand; it swings with the hand (outer 'wave' hand at
# (8, 12), inner 'raise' hand at (9, 12))
_SWISH = {'wave': [(6, 10), (5, 11), (5, 12), (6, 13)],
          'raise': [(7, 10), (6, 11), (6, 12), (7, 13)]}


# ---------------------------------------------------------------------------------------------
# Clawd (trunk + limbs layers), his fine-line face (face layer) and his hat (hat layer): same keys,
# same timing
# ---------------------------------------------------------------------------------------------
def pose(k):
    """His body for key k. The eye cells are drawn plain orange (kit 'blink'): his eyes and every
    expression live in the fine face layer (_split)."""
    return clawd(eyes='blink', larm=k.get('larm', 'wave'), rarm=k.get('rarm', 'side'),
                 legs=k.get('legs', 'stand'))


def _expr(k):
    """(left eye, right eye) names for key k (FINE_EYES or _LOCAL_EYES); 'face' is one name or a
    (left, right) pair."""
    e = k.get('face', 'open')
    return e if isinstance(e, tuple) else (e, e)


# Two local fine expressions, each drawn as a kit expression plus a few fine-pixel edits (relative
# to the eye cell's top-left fine pixel, the same for both eyes; '_' = the eye's ink, '#' = lid):
#   glint  : sparkle + a second white glint at the bottom-right: the sparkle TWINKLES (the same
#            'glint' face as the user-approved done-party)
#   half_u : the kit's half lid raised one fine pixel (the half-open eye looking up). It shares its
#            pixels with look_u, so the bonk's line > half_u > look_u opens the eyes upward, where
#            he is about to look, instead of jumping from the bottom of the eye to the top.
_LOCAL_EYES = {
    'glint': ('sparkle', [(1, 1, 'W')]),
    'half_u': ('half', [(0, 1, '#'), (1, 1, '#'), (0, 0, '_'), (1, 0, '_')]),
}


def _fine_eyes(ff, p, x, y, left, right):
    """fine_face() for both eyes, with the local expressions above."""
    fine_face(ff, p, x, y, *[_LOCAL_EYES.get(e, (e,))[0] for e in (left, right)])
    for e, key in ((left, 'eye_l'), (right, 'eye_r')):
        ex, ey = p.at(key, x, y)
        for dx, dy, ch in _LOCAL_EYES.get(e, (e, []))[1]:
            if ch == '_':
                ch = EYE_INK if EYES_BLACK else ERASE
            ff.put(2 * ex + dx, 2 * ey + dy, ch)
    return ff


_SPLIT = {}


def _split(k):
    """Clawd drawn the normal way, his face drawn with the fine-line kit (fine + fine_face, via
    _fine_eyes for the local expressions), split into a normal-res body and a fine overlay holding
    only the half-size eye pixels.
    His body is drawn with plain filled eye cells (pose() uses the kit's 'blink'), so the body's eye
    window stays plain orange (each body row is one run, and the body frames merge while only his
    face acts); the overlay holds just the pixels the expression draws: the black eyes, arcs and
    lines, the sparkle glints. (Measured: 1.5 KB smaller than putting whole black eye cells in the
    body.) Body + face composite exactly to fine(frame) + fine_face(...), except that fine_face's
    eye-area clear (a 4x4 half-pixel square per eye) never repaints his front arm: in the bow
    ('front' arm) its shaded cell sits inside that square, and would lose a half-pixel corner."""
    key = id(k)
    if key not in _SPLIT:
        p, x, y = pose(k), HOME[0], k.get('y', HOME[1])
        left, right = _expr(k)
        f = Frame()
        put_clawd(f, p, x, y)
        ff0 = fine(f)
        ff = _fine_eyes(ff0.copy(), p, x, y, left, right)
        for q, c in list(ff.px.items()):                # undo the clear where it hit a non-orange cell
            if c == '#' and ff0.px.get(q, '#') != '#':   # (eye patterns never draw orange)
                ff.px[q] = ff0.px[q]
        face = Frame(res=2)
        face.meta = {'fine_face': [(left, right)]}
        for eye in ('eye_l', 'eye_r'):
            ex, ey = p.at(eye, x, y)
            for cy in range(ey - 1, ey + 2):            # fine_face only touches this 3x3-cell window
                for cx in range(ex - 1, ex + 2):
                    quad = [ff.px.get((2 * cx + i % 2, 2 * cy + i // 2)) for i in range(4)]
                    b = f.px.get((cx, cy))
                    if None in quad:                     # see-through (only if the kit's eyes are holes)
                        f.px.pop((cx, cy), None)
                        keep = [q is not None for q in quad]
                    else:                                # the body keeps its own cell (orange, or
                        keep = [q != b for q in quad]    # the shaded front arm); overlay = the rest
                    for i, q in enumerate(quad):
                        if keep[i]:
                            face.px[(2 * cx + i % 2, 2 * cy + i // 2)] = q
        _SPLIT[key] = (f, face)
    return _SPLIT[key]


def face(k):
    return _split(k)[1]


def body(k):
    f = _split(k)[0].copy()
    if k.get('swish'):
        for x, y in _SWISH[k.get('larm', 'wave')]:
            f.put(x, y, 's')
    if k.get('dust') is not None:
        f.place(DUST.sprite(k['dust']), 15, GROUND - 1)
    return f


def hat(k):
    """k['hat'] = the brim's bottom row in WORLD space (None = seated on his head);
    k['hdx'] = sideways shift; k['tilt'] = tipped hat; k['squash'] = impact squash;
    k['fdy'] = the flower's lag/lead relative to the hat (overlapping action)."""
    y = k.get('y', HOME[1])
    f = Frame()
    hx, hy = pose(k).at('head', HOME[0], y)
    dy = 0 if k.get('hat') is None else k['hat'] - y
    dx = k.get('hdx', 0)
    spr = _HAT_TIP if k.get('tilt') else _HAT_SQUASH if k.get('squash') else _HAT
    f.place(spr, hx + dx, hy + dy)
    f.place(_FLOWER, hx + dx + _FLOWER_AT[0], hy + dy + _FLOWER_AT[1] + k.get('fdy', 0))
    for x, yy in _SPECKS.get(k.get('specks'), []):
        f.put(x, yy, 's')
    f.meta.setdefault('items', []).append(HAT.name)
    return f


WINK = ('happy', 'open')        # the eye under the lifted brim (screen left) closes in a thin arc
WINK_IN = ('half', 'open')      # the lid comes down first
WINK_OUT = ('happy', 'half')    # ... and the open eye's lid starts down into the blink
KEYS = [
    # WAVE (frame 0 = 'hi'): the big happy greeting (fine arcs); the swish swings with the hand
    ('hi',      dict(swish=1, face='happy'), 220),
    ('w1',      dict(larm='raise', swish=1, face='happy'), 90),
    ('w2',      dict(swish=1, face='happy'), 150),
    # HOP. Anticipation with the arms only (the right arm leads, the left follows), no crouch; the
    # smile opens (half > open): eyes on you
    ('ant1',    dict(larm='side', rarm='down', face='half'), 60),
    ('ant2',    dict(larm='down', rarm='down'), 90),
    # take-off: legs still extended from the push-off, arms swinging up through 'out' (clear of the
    # brim), hat seated, the flower lags
    ('launch',  dict(larm='out', rarm='out', y=10, fdy=1), 70),
    # apex: legs tucked, the hat pops off (rising 2 then 1) and drifts a cell left on its arc. The
    # cause comes first: his eyes stay on you while the brim still touches his head, and go WIDE
    # ("whoa, my hat!") when the gap opens (apex2), held through the fall; on landing they roll up
    # to follow it down
    ('apex',    dict(larm='wave', rarm='up', legs='short', y=9, hat=8, fdy=1), 100),
    ('apex2',   dict(larm='wave', rarm='up', legs='short', y=9, hat=7, hdx=-1, face='wide'), 130),
    ('fall',    dict(larm='raise', rarm='up', y=10, hat=7, hdx=-1, face='wide'), 60),
    ('land',    dict(larm='out', rarm='out', hat=8, hdx=-1, face='look_u', dust=0), 100),
    ('settle',  dict(larm='side', hat=10, face='look_u', dust=1, fdy=-1), 90),
    # PLOP: the hat lands a beat late and squashes (not him); the flower springs up 2, and comes
    # down to meet the hat as it rebounds (flower centre y 7, 8, 9 while the crown top goes 7, 5, 6);
    # the specks fly a cell further out on the rebound. BONK: his eyes squeeze shut (thin lines),
    # ease open upward (the raised half lid), then a deliberate look above (is it back?)
    ('plop',    dict(larm='side', squash=1, specks=1, dust=2, fdy=-2, face='line'), 110),
    ('rebound', dict(larm='side', hat=11, specks=2, face='half_u'), 100),
    ('check',   dict(larm='side', face='look_u'), 260),             # is it back?
    # HAT TIP: eyes back on you; the hand rises to the brim and tips the hat (left half lifted onto
    # the hand) while the eye under it starts to close
    ('reach',   dict(larm='up'), 90),
    ('grab',    dict(larm='raise'), 100),
    ('tip',     dict(larm='raise', tilt=1, hdx=-1, face=WINK_IN), 100),
    # ... a beat later the bow: a friendly WINK + the other hand on his belly (kit 'front' arm);
    # on the heart's -dump the open eye's lid starts down (half), so the blink below is a smooth one
    ('tip_b',   dict(larm='raise', rarm='front', tilt=1, hdx=-1, face=WINK), 130),
    ('tip_h',   dict(larm='raise', rarm='front', tilt=1, hdx=-1, face=WINK), 190),
    ('tip_h2',  dict(larm='raise', rarm='front', tilt=1, hdx=-1, face=WINK_OUT), 90),
    # back on: the flower bobs and he blinks (a gentle echo of the bonk) ... his eyes ease open
    # (half; body and hat frames merge, the cut lands on the fx glint's turn) and SPARKLE
    ('down',    dict(larm='raise', fdy=-1, face='line'), 90),
    ('down2',   dict(larm='raise', face='half'), 100),
    ('down3',   dict(larm='raise', face='sparkle'), 100),
    # ... and waves again, starry-eyed: on the inner swing the sparkle TWINKLES (a second glint in
    # each eye, answered by the glint low on the left), then closes smoothly (half > line) into the
    # happy arcs of frame 0
    ('w3',      dict(swish=1, face='sparkle'), 250),
    ('w4',      dict(larm='raise', swish=1, face='glint'), 90),
    ('w5',      dict(swish=1, face='sparkle'), 100),
    ('w5b',     dict(swish=1, face='half'), 60),
    ('w6',      dict(larm='raise', swish=1, face='line'), 90),
    ('w7',      dict(swish=1, face='happy'), 270),
    ('w8',      dict(larm='raise', swish=1, face='happy'), 90),
]

T, LOOP = {}, 0
for _name, _, _ms in KEYS:
    T[_name] = LOOP
    LOOP += _ms


def trunk(k):
    """His trunk for key k: the kit body with no arms (eye cells plain orange) at his height. It
    only changes during the hop, so this layer is 5 frames instead of redrawing him 22 times."""
    f = Frame()
    put_clawd(f, clawd(eyes='blink', larm='none', rarm='none', legs=k.get('legs', 'stand')),
              HOME[0], k.get('y', HOME[1]))
    full = body(k).px
    f.px = {q: c for q, c in f.px.items() if q in full}   # (a no-op unless the kit's eyes are holes)
    return f


def limbs(k):
    """The rest of body(k): his arms (the bow's shaded front hand is drawn over the trunk), the
    swish and the dust. trunk + limbs composite exactly to body(k)."""
    t = trunk(k).px
    b = body(k)
    f = Frame()
    f.px = {q: c for q, c in b.px.items() if t.get(q) != c}
    f.meta = b.meta
    return f


def build():
    tr = [(trunk(k), ms) for _, k, ms in KEYS]
    lb = [(limbs(k), ms) for _, k, ms in KEYS]
    fc = [(face(k), ms) for _, k, ms in KEYS]
    h = [(hat(k), ms) for _, k, ms in KEYS]
    return anim(NAME, DESC, [static('bubble', BUBBLE), layer('trunk', tr), layer('limbs', lb),
                             layer('face', fc), layer('hat', h), layer('fx', fx())],
                state=STATE)


# ---------------------------------------------------------------------------------------------
# fx layer: heartbeats, sparkles and the hat's "ting", all on the body's loop length. Hello is on
# screen for 2-4 s, so instead of drifting co-prime loops every accent is choreographed against
# the story on every pass, and one shared layer saves the empty frames three layers would need
# (the heartbeat overlay only touches the bubble, which nothing else overlaps). Every accent
# starts and ends on a body key, so the composite has no stray 10-30 ms moments.
#   heart: ba-dump on the opening wave, a beat on the plop, ba-dump on the hat tip.
#   sparkles: the big star by the waving hand fades as the wave starts; small glints answer the
#   take-off (bottom right) and the plop (left); during the tip only the crown corner of the tipped
#   hat (11, 5) glints (dot, plus, X, plus); two glints keep the closing wave alive (the second
#   answers his twinkling eyes), and the star builds again into the loop point through the same
#   sizes it faded through (dot, plus, long plus, STAR). Side glints are impact flashes: they pop
#   straight in as a plus, turn (plus, X, plus) and fade out through a dot that lasts until the
#   next accent's cut (no extra fx frames: each dot fills what was an empty stretch).
# ---------------------------------------------------------------------------------------------
_BEAT_SPR = Sprite(cells=[(x, y, ch) for (x, y), ch in BEAT.px.items()], anchor=(0, 0), name='heart_swell')
BEATS = [
    (T['w2'], T['w2'] + 90),             # ba- (outer wave swing)
    (T['ant2'], T['launch']),            # -dump (arms down, about to jump)
    (T['plop'], T['rebound']),           # plop!
    (T['tip_h'], T['tip_h'] + 90),       # ba- (in the bow)
    (T['tip_h2'], T['down']),            # -dump (the open eye's lid starts down)
]
# Each twinkle: (start ms, item, x, y, [(frame, ms), ...]); a twinkle may wrap past the loop end.
TW_LOOP = LOOP
TWINKLES = [
    # big star: dot (w7), plus, long plus, STAR from w8 through frame 0, long plus (w1), plus (w2), dot
    (T['w7'], SPK, 4, 5, [(0, 90), (1, 90), (3, 90), (2, 310), (3, 90), (1, 90), (0, 210)]),  # -> 610
    (T['w8'] - 90, SPS, 8, 2, [(0, 90), (1, 400), (0, 90)]),                              # -> 400
    # take-off, apex, fall ... the dot fades until the plop
    (T['launch'], SPS, 27, 15, [(1, 70), (2, 100), (1, 130), (0, T['plop'] - T['fall'])]),
    # plop, rebound, check ... the dot fades while the hand rises to the brim
    (T['plop'], SPS, 2, 12, [(1, 110), (2, 100), (1, 260), (0, T['tip'] - T['reach'])]),
    # the tip's "ting" on the crown corner, fading before the hat drops back on
    (T['tip'], SPS, 11, 5, [(0, 100), (1, 130), (2, 90), (1, 100), (0, T['down'] - T['tip_h2'])]),
    # the hat is back on ... the dot fades until its answer on the left
    (T['down2'], SPS, 25, 16, [(1, 100), (2, 100), (1, 110), (0, T['w5'] - T['w3'] - 110)]),
    (T['w5'], SPS, 4, 16, [(1, 160), (2, 90), (1, 90), (0, 90)]),        # the twinkle's answer, fades
]


def fx():
    spans = [(t0, t1, _BEAT_SPR, 0, 0) for t0, t1 in BEATS]   # (t0, t1, sprite, x, y) in [0, TW_LOOP)
    for t0, item, x, y, seq in TWINKLES:
        t = t0
        for i, ms in seq:
            a, b = t % TW_LOOP, t % TW_LOOP + ms
            if b <= TW_LOOP:
                spans.append((a, b, item.sprite(i), x, y))
            else:                                # wraps: split at the loop point
                spans.append((a, TW_LOOP, item.sprite(i), x, y))
                spans.append((0, b - TW_LOOP, item.sprite(i), x, y))
            t += ms
    cuts = sorted({0, TW_LOOP} | {s[0] for s in spans} | {s[1] for s in spans})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        f = Frame()
        for s0, s1, spr, x, y in spans:
            if s0 <= a < s1:
                f.place(spr, x, y)
        out.append((f, b - a))
    return out
