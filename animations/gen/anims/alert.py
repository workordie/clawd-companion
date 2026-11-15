# ======================================================================================
# USER FEEDBACK: the user reviewed this fine-face upgrade draft personally and approved it
# ("looks great go"). Keep the scene, beats and fine-line expressions; critics, fixers and judges
# should polish the execution (timing, readability, craft, size), not redesign it.
# ======================================================================================
"""alert -- Claude needs your permission (requires_action).  Preview:  python3 gen/preview.py anim alert

Clawd as a polite little bellhop (local navy-and-gold pillbox cap) who needs your OK. He holds a
golden key out to you next to a closed brass padlock (both local props), so the scene reads "may I
open this? Your permission, please". The red '!' bubble is the library bubble_bang; its '!' is drawn
here so the rest, pulse, squash and stretch shapes always match. Library: bubble_bang, dust_puff,
sparkle_small.

Expressive face (STYLE.md section 0b): his eyes act with the fine-line kit (fine() + fine_face(),
half-size pixels): sparkle eyes that twinkle, thin squeezed lines, a half-lid flinch, smooth blinks,
half-step glances, wide eyes. No mouth, no blush, and his body keeps its normal size in every frame
(the hop moves the whole normal body, legs tucked in the air). Anticipation and impact are carried by
the arms, the eyes, timing and the props (cap, key, bubble).

The wave: his forearm swings between 'wave' (out, with a swish arcing over the hand) and 'hi', a
hand-drawn variant of the kit's 'raise' at normal cell size whose hand clears his head by one row,
like a hand raised in class ("may I?"). The 60 ms in-between is 'sweep', the kit's 'wave' with the
hand turned up a cell: it keeps the hand out on the arc around his elbow, so the wave sweeps instead
of the hand ducking in and back out. All three stand clear of his body, so the arm never melts into
his head.

Storyboard (one loop = 3800 ms; the bubble, trunk, limbs, face, gear and pop layers share this timing
table T)

  t (ms)      beat
  0           HEY! (frame 0): at HOME, SPARKLE eyes on you (a white glint in each black eye), left
              arm out in 'wave' with a swish over the hand, key held out in his right hand. The '!'
              bubble has just popped: orange ticks burst from it.
  0-820       two waves, sparkle eyes on you all along: wave -> sweep -> hi -> sweep -> wave -> sweep
              -> hi. The longest holds sit on the extremes. The accents alternate: the swish shows
              with the hand on the 'wave' extremes (shorter on the second one), and his eyes twinkle
              (a second glint, bottom-right) each time the hand is up high (280, 700). The ticks fly
              out (220) and vanish (340).
  820-990     anticipation, a 170 ms hold: his eyes squeeze shut (thin lines, held through the
              push-off), the raised arm dips ('up') and the key hand swings down.
  990-1380    hop: take-off 1 cell, eyes still squeezed, legs still reaching, cap pressed down, arm
              swinging up. Then 2 cells up with legs tucked and the hand held high ('hi'), the key
              dangling behind, and his sparkle eyes pop open a beat after the push-off (1060). A
              170 ms hang (the cap floats a row off his head), then 1 cell down, the arm swinging out
              ('wave'). The bubble lifts its tail out of his way the moment he leaves the ground and
              is tugged narrow while he is up.
  1380-1700   thump at HOME with a half-lid flinch (1380), free arm out, the key dips, dust_puff
              rolls out (behind the padlock) and thins to a wisp on the ground. The bubble's tail
              snaps back down; the cap lands a frame late and is pressed onto his head (the hat takes
              the squash, not Clawd), and the bubble squashes a frame late. His eyes are open on you
              again a beat later (1480) as he settles, key offered. The take-off squeeze stays the
              hop's only full closure, so the sparkle at the apex keeps its contrast and the wait's
              blink is the next time his eyes shut.
  1700-3450   patient wait, key offered, eyes on you: a quiet beat, the key glints (1860), the '!'
              swells gently (2300). A smooth fine blink (2600: half, line, and then the half lid opens
              up and to the right, where he is about to look) lifts into a hopeful half-step glance
              up at his bubble (2800-3120), and the '!' swells on the very frame his eyes reach it;
              it settles as his eyes come back to you for a 330 ms still hold.
              Every other loop the wait plays out differently (the wait_face layer runs 2 x 3800 ms):
              he glances at the key as it glints (1950, half-step right), then on to the padlock
              (2210, half-step left: "this key... that lock...") while the '!' swells, and back to
              you as it settles (2540: "may I?"). Then a slow blink while the '!' swells again
              (2800-3120: half 80, line 160, half 80 ms), his eyes opening as it settles. The wait's
              blinks come 4.0 s and 3.6 s apart, never on a metronome.
  3450-3800   restart with a cause: the bubble gathers to pop again (squash, held 170 ms) and his
              eyes go WIDE ("hey!": the upper lids lift one fine row), held 350 ms through the pop
              (stretch + ticks 3620) while his arm rises (up -> raise); they light up into frame 0's
              sparkle and wave.

  glint layer (10600 ms; 10600 and 3800 only meet every ~3.4 minutes): the padlock catches the light
  now and then. Its first twinkle lands in the first loop's still hold (3180-3450) and its white
  shine in the second loop's (6980-7250); each starts a beat after his eyes settle on you and is gone
  as the bubble gathers to pop, so the busy first seconds after the switch stay clean. Later passes
  drift ~800 ms against the body loop and the glints turn up in new places. It is pinned to a prop
  that never moves, so it can run out of sync with the body. The shine's plus has no left arm: that
  cell is the lock's left edge, which stays gold so it never vanishes on the light theme.

Face technique: Clawd is drawn whole at normal resolution with the kit's black eyes (STYLE.md
section 0); the face layers (FINE, half-size pixels) only hold the pixels his fine-line expression
changes (a glint, a lid, a thin line, an eye moved half a step), so they are empty while his eyes are
the plain official ones and the body frames never change with his face. The composite is exactly
fine(frame) + fine_face(...) (asserted, also after layer()'s eye-ink pass). His face is split over two
fine layers that never draw at the same time (asserted): 'face' (3800 ms: the burst and the re-pop,
the same every loop) and 'wait_face' (7600 ms: the two versions of the patient wait). Both are cut at
every body beat of the same clock T, so his face never drifts off his body. Local expressions, built
on the kit's shapes: 'look_ur' (at the bubble, up and to his right) is the kit's half-step look_r
lifted one fine row; 'half_ur' is its bottom half (the blink's half lid at that gaze); 'glint' is the
kit's sparkle with done_party's second glint.

Layers, back to front: bubble | trunk (Clawd's body, legs and black eyes, no arms: it only changes
with the hop) | limbs (his arm cells, the swish, the dust) | face + wait_face (fine eyes) | gear (cap +
key) | pop (ticks, '!' pulse, key glint) | lock (static) | glint (co-prime). Trunk, limbs and gear
come from the same pose on the same clock (the trunk + limbs composite is asserted to be exactly
Clawd drawn whole); they are separate layers only so each one's frames merge while it stands still
(smaller SVG).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'alert'
STATE = 'Claude needs your permission'
DESC = ('A little bellhop with a golden key beside a closed padlock: his red "!" bubble pops and Clawd '
        'goes wide-eyed, waves sparkle-eyed with his hand raised high and hops, then holds the key out '
        'and waits politely, glancing hopefully at his bubble, the key and the lock and back at you for '
        'your OK.')

LOOP = 3800
TIP = (20, 11)          # the bubble's tail tip (library anchor (25, 5)); at rest it spans x 20-30, y 1-11

# ---------------------------------------------------------------------------------------------
# Bubble: library bubble_bang outline + tail; our own '!' so all the shapes match.
# Every shape is anchored on the resting tail tip. The rest, swell and squash shapes sit on the
# library's own tail. The short-tail shapes (the stretch, and the rest shape while he is in the air)
# pull their tail up into a stub a row higher and a column further right (tip (21, 10)), so it always
# keeps an empty cell from his rising head; on the re-pop the stretch's tail springs up the same way.
# ---------------------------------------------------------------------------------------------
_LIB_ROWS = get('bubble_bang').sprite(0).rows()
_TAIL = _LIB_ROWS[-2:]
_TIP_COL = next(i for i, ch in enumerate(_TAIL[-1]) if ch not in '. ')
_PLAIN = set('NwWMm.')                      # bubble colors; anything else is the library's glyph
_REST_ROWS = [''.join(ch if ch in _PLAIN else 'w' for ch in row) for row in _LIB_ROWS[:-2]]
_SHORT_TAIL = ['NN']                        # the retracted stub under the bubble's bottom-left corner

# the '!': a straight 2-wide bar with a pink highlight on top, a gap, and the dot (rest-bubble cells)
_BANG = {(4, 2): 'p', (5, 2): 'R', (4, 3): 'r', (5, 3): 'R', (4, 4): 'r', (5, 4): 'R',
         (4, 6): 'r', (5, 6): 'R'}
_BANG_TALL = dict(_BANG)                    # the gentle pulse: the bar one row longer (no sideways shift)
_BANG_TALL.update({(4, 1): 'p', (5, 1): 'R', (4, 2): 'r'})


def _paint(rows, cells):
    g = [list(r) for r in rows]
    for (c, r), ch in cells.items():
        g[r][c] = ch
    return [''.join(r) for r in g]


def _close_tail(rows):
    """The bubble's bottom row with the tail opening narrowed to one cell (the cell right of the
    left outline stays paper, the next one becomes outline): the mouth of the short tail."""
    last = list(rows[-1])
    col = next(c for c, ch in enumerate(last) if ch not in '. ')
    last[col + 2] = 'N'
    return rows[:-1] + [''.join(last)]


def _bubble(body_rows, dx, name, short=False):
    """A bubble body (its left column `dx` cells right of the tail tip, its bottom row 2 rows above
    the tip) on the library tail (or the short stub), anchored on the resting tip."""
    nb, cells = len(body_rows), []
    for r, row in enumerate(body_rows):
        for c, ch in enumerate(row):
            if ch not in '. ':
                cells.append((dx + c, r - nb - 1, ch))
    if short:                                # stub under the bottom-left outline cell
        left = next(c for c, ch in enumerate(body_rows[-1]) if ch not in '. ')
        for c, ch in enumerate(_SHORT_TAIL[0]):
            cells.append((dx + left + c, -1, ch))
    else:
        for r, row in enumerate(_TAIL):
            for c, ch in enumerate(row):
                if ch not in '. ':
                    cells.append((c - _TIP_COL, r - 1, ch))
    return Sprite(cells=cells, anchor=(0, 0), name=name)


_REST = _paint(_REST_ROWS, _BANG)
_BUB = _bubble(_REST, -_TIP_COL, 'bubble_bang')
_BUB_SWELL = _bubble(_paint(_REST_ROWS, _BANG_TALL), -_TIP_COL, 'bubble_swell')
_BUB_SHORT = _bubble(_close_tail(_REST), -_TIP_COL, 'bubble_short', short=True)
_BUB_SQUASH = _bubble([                      # 13 wide (x 18-30), 2 rows shorter, squashed '!'
    '..NNNNNNNNN..',
    '.NWwwwwwwwwN.',
    'NwwwwwpRwwwwN',
    'NwwwwwrRwwwMN',
    'NwwwwwwwwwwMN',
    '.NwwwwrRwwMN.',
    '..NNwwNNNNN..',
], -2, 'bubble_squash')
_STRETCH_ROWS = [                            # 9 wide (x 21-29), same height, '!' one row longer
    '..NNNNN..',
    '.NWwwwwN.',
    'NwwpRwwwN',
    'NwwrRwwwN',
    'NwwrRwwwN',
    'NwwrRwwMN',
    'NwwwwwwMN',
    'NwwrRwwMN',
    'NwwNNNNN.',
]
_BUB_STRETCH = _bubble(_close_tail(_STRETCH_ROWS), 1, 'bubble_stretch', short=True)

# "pop!" ticks radiating from the bubble's left side: they shoot out (inner) -> full -> fly away
# (outer). Every cell keeps an empty cell from the bubble and from his cap.
_TICKS_IN = [(19, 2), (17, 4), (18, 6)]
_TICKS_BIG = [(18, 1), (19, 2), (16, 4), (17, 4), (17, 7), (18, 6)]
_TICKS_OUT = [(18, 1), (16, 4), (17, 7)]


def bubble(spr=None):
    f = Frame()
    f.place(spr or _BUB, TIP[0], TIP[1])
    return f


def swell_overlay():
    """Only the cells where the pulsing '!' differs from the resting bubble (drawn on top of it)."""
    rest, sw = bubble().px, bubble(_BUB_SWELL).px
    f = Frame()
    for (x, y), ch in sw.items():
        if rest.get((x, y)) != ch:
            f.put(x, y, ch)
    return f


def ticks(cells):
    f = Frame()
    for x, y in cells:
        f.put(x, y, 'o')
    return f


# ---------------------------------------------------------------------------------------------
# Props
# ---------------------------------------------------------------------------------------------
SPARK = get('sparkle_small').frames          # gold glint (reads on both themes): dot, plus, x
# Golden key (local, in the style of the library golden_key): ring bow, shaft, two teeth, dark-gold
# shadow on the bottom right. The library key is 5 rows tall; between the bubble's tail (row 11)
# and the landing dust (rows 17-19) only 3 rows are free, so this one is 9 x 3. All mid-tones (no
# pale highlight on its edge, which would vanish on the light theme). Held by its bow in his right
# hand: 'out' offers it to you (x 22-30, rows 13-15), 'down' lets it dangle in the air.
_KEY = Item('bellhop_key', 'hand', 'Golden key held by its ring bow (permission).',
           Sprite([
               '.jj......',
               'j..jjjjjj',
               '.jJ...J.J',
           ], anchor=(0, 1)))
def _no_left_arm(s):
    """The sprite without the cell just left of its anchor (the plus frame's left arm)."""
    return Sprite(cells=[c for c in s.cells if (c[0] - s.ax, c[1] - s.ay) != (-1, 0)],
                  anchor=(s.ax, s.ay), name=s.name)


# a white shine for the middle of a gold surface, where a gold glint would not show. Its plus has no
# left arm: on the padlock that cell is the brass body's left edge, where pale yellow would vanish on
# the light theme (the lock's own gold edge stays there instead).
_SHINE = [_no_left_arm(s).recolor({'j': 'Y', 'y': 'W'}) for s in SPARK]
# swish: a short arc over the waving hand (hand tip at (8, 12) in 'wave'), tracing where the hand
# just swung down from. Orange like the bubble's pop ticks (one color for every action mark, clear
# on both themes, a tone the padlock doesn't use) and two columns clear of its shackle (x 2-6), with
# an empty row between it and the hand. Listed far end first: the fading swish keeps only the cells
# nearest the hand.
_SWISH = [(10, 9), (9, 9), (8, 10)]
_SWISH_INK = 'o'

# Bellhop pillbox cap (local): navy drum with a blue top, gold band and button, light from the
# top-left (dark-gold shadow cell on the band's right end). Head slot: the band sits on the row just
# above his head.
_CAP = Item('bellhop_cap', 'head', 'Bellhop pillbox cap: navy drum, blue top, gold band and button.',
           Sprite([
               '..j..',
               '.bbb.',
               'BBBBB',
               'jjjjJ',
           ], anchor=(2, 4)))

# Closed brass padlock (local), standing on the input box at his left: steel shackle (silver
# highlight top-left, gray shadow on the right leg), gold body with a dark-gold right side and
# base, a shine streak and the keyhole. Anchor = bottom-center cell.
_LOCK = Sprite([
    '..mss..',
    '.m...s.',
    '.s...N.',
    'jjjjjjJ',
    'jyjkjjJ',
    'jjjkjjJ',
    'JJJJJJJ',
], anchor=(3, 6), name='padlock')
LOCK_AT = (4, GROUND)                         # x 1-7, rows 13-19

# Landing dust: library dust_puff frames 0-1 roll out from his feet; the last beat is our own
# thinning wisp that stays on the ground just past the second puff (x 22-25), instead of the
# library's rising third frame (it would float into the key he holds out). The left side of every
# frame is behind the padlock.
DUST = get('dust_puff')
_WISP = Sprite([
    '.tt',
    't..',
], anchor=(0, 1), name='dust_wisp')            # anchor = its lowest-left cell, on the ground
_WISP_AT = (24, GROUND)


def _dust(f, i):
    if i < 2:
        f.place(DUST.sprite(i), 15, GROUND - 1)
    else:
        f.place(_WISP, *_WISP_AT)


# ---------------------------------------------------------------------------------------------
# Clawd: body (normal resolution, the kit's black eyes) + face (fine overlay)
# ---------------------------------------------------------------------------------------------
# Two hand-drawn left arms at normal cell size: a kit arm plus one cell (box coords), and its grip point.
#   'hi'    the wave's high extreme: the kit's 'raise' with one more cell on top, so the hand clears
#           his head by one row while the forearm stays a column clear of his body
#           (box cells (0,2) (-1,1) (-1,0) (-1,-1)).
#   'sweep' the wave's in-between: the kit's 'wave' with the hand turned up a cell
#           (box cells (0,2) (-1,1) (-2,0) (-2,-1)). Its hand sits on the arc around his elbow
#           between 'wave' (hand out) and 'hi' (hand up), so the wave sweeps instead of the hand
#           ducking in to the kit's short 'raise' and back out.
_ARM_PLUS = {'hi': ('raise', (-1, -1), (-1, -2)), 'sweep': ('wave', (-2, -1), (-2, -2))}


def pose(larm='side', rarm='out', legs='stand'):
    """A kit pose with the official open eyes (the face layer does the acting); larm may also be one of
    the hand-drawn wave arms in _ARM_PLUS."""
    if larm not in _ARM_PLUS:
        return clawd(larm=larm, rarm=rarm, legs=legs)
    kit, (cx, cy), hand = _ARM_PLUS[larm]
    p = clawd(larm=kit, rarm=rarm, legs=legs)
    anchors = dict(p.anchors)
    anchors['hand_l'] = hand
    return Pose(Sprite(cells=list(p.sprite.cells) + [(cx, cy, '#')], anchor=(0, 0), name='clawd'),
                anchors, dict(p.spec, larm=larm, custom=True))


# local fine expressions, each built on a kit FINE_EYES shape (see _eyes)
_LOCAL_EYES = {'look_ur': 'look_r', 'half_ur': 'look_r', 'glint': 'sparkle'}


def _eyes(ff, p, x, y, left, right):
    """fine_face() on a fine frame, plus three local expressions built on the kit's shapes:
      'look_ur' (up at his bubble): the kit's half-step look_r lifted one fine row;
      'half_ur': the bottom half of look_ur, the half lid of a blink that opens where he is about to
                 look (the line -> half_ur -> look_ur lid lifts up and over, no jump);
      'glint'  : sparkle with a second glint at the bottom-right (done_party's twinkle)."""
    names = (left, right)
    fine_face(ff, p, x, y, *[_LOCAL_EYES.get(n, n) for n in names])
    for n, key in zip(names, ('eye_l', 'eye_r')):
        ex, ey = p.at(key, x, y)
        if n in ('look_ur', 'half_ur'):
            for dx in (1, 2):
                ff.put(2 * ex + dx, 2 * ey + 1, '#')
                if n == 'look_ur':
                    ff.put(2 * ex + dx, 2 * ey - 1, EYE_INK)
        elif n == 'glint':
            ff.put(2 * ex + 1, 2 * ey + 1, 'W')
    ff.meta['fine_face'] = [names]
    return ff


def _split(p, x, y, face):
    """Clawd drawn the normal way (the kit's black eyes) -> (body frame, fine face overlay). The
    overlay holds only the half-size pixels his fine-line expression (fine + fine_face) changes, so
    it is empty while his eyes are the plain official ones and the body frames never change with
    his face. Body + overlay composite to exactly the fine frame, also after layer()'s eye-ink pass
    (asserted)."""
    left, right = face if isinstance(face, tuple) else (face, face)
    f = Frame()
    put_clawd(f, p, x, y)
    base = fine(f)
    ff = _eyes(base.copy(), p, x, y, left, right)
    assert set(ff.px) == set(base.px), face             # no see-through pixels: ink only
    lay = Frame({k: v for k, v in ff.px.items() if base.px[k] != v}, res=2)
    lay.meta = {'fine_face': [(left, right)]}
    assert base.over(blacken_eye_holes(lay.copy())).px == ff.px, face
    return f, lay


def body(face='open', larm='side', rarm='out', legs='stand', dy=0, cap=0, swish=0, dust=None):
    """One moment of Clawd -> (trunk, limbs, face, gear) frames. All four come from the same pose and
    the same clock, so nothing can drift from him. Clawd is drawn whole with put_clawd and split by
    what changes, for a smaller SVG (the composite is asserted to be exactly the whole Clawd):
      trunk: the kit body + legs + black eyes with no arms (it only changes with the hop: 5 frames),
      limbs: his arm cells (the whole pose minus the trunk) plus the swish and the landing dust,
      face : the fine overlay (see _split),
      gear : cap + key, in their own layer so their frames merge while he stands still.
    face = a fine expression (FINE_EYES name or one of _LOCAL_EYES; a (left, right) pair for two
    different eyes), dy = whole-body lift (normal body size always), cap = the cap's offset from its
    seat (+1 pressed onto his head, -1 floating a row up), swish = swish cells shown (3 full,
    2 fading), dust = frame."""
    p = pose(larm=larm, rarm=rarm, legs=legs)
    x, y = HOME[0], HOME[1] + dy
    whole, ff = _split(p, x, y, face)
    trunk = Frame()
    put_clawd(trunk, clawd(larm='none', rarm='none', legs=legs), x, y)
    limbs = Frame({k: v for k, v in whole.px.items() if k not in trunk.px})
    limbs.meta = whole.copy().meta
    assert all(whole.px.get(k) == v for k, v in trunk.px.items()), (larm, rarm, legs)
    assert trunk.over(limbs).px == whole.px, (larm, rarm, legs)
    for sx, sy in _SWISH[len(_SWISH) - swish:]:
        limbs.put(sx, sy + dy, _SWISH_INK)
    if dust is not None:
        _dust(limbs, dust)
    fg = Frame()
    wear(fg, _CAP, p, x, y, dy=cap)
    wear(fg, _KEY, p, x, y)
    return trunk, limbs, ff, fg


def _at(track, t):
    """The value of a sorted [(start_ms, value), ...] track at time t."""
    return [v for s, v in track if s <= t][-1]


def at_times(events, total):
    """[(start_ms, Frame), ...] (sorted, first at 0) -> [(Frame, ms), ...] filling `total`."""
    out = []
    for i, (t, f) in enumerate(events):
        end = events[i + 1][0] if i + 1 < len(events) else total
        out.append((f, end - t))
    return out


def glints(events, total):
    """A glint layer: [(start, sprite or None, (x, y)), ...] -> layer frames."""
    ev = []
    for t, spr, xy in events:
        f = Frame()
        if spr is not None:
            f.place(spr, xy[0], xy[1])
        ev.append((t, f))
    return at_times(ev, total)


def build():
    WAIT = dict(larm='side', rarm='out')      # free arm relaxed, key held out to you
    keys = [
        # A. HEY! + two waves (frame 0 = first key): out ('wave' + swish) <-> up ('hi'), 'sweep' between
        ('hey', dict(larm='wave', swish=3), 220),
        ('w1', dict(larm='sweep'), 60),
        ('w2', dict(larm='hi'), 140),
        ('w3', dict(larm='sweep'), 60),
        ('w4', dict(larm='wave', swish=2), 160),
        ('w5', dict(larm='sweep'), 60),
        ('w6', dict(larm='hi'), 120),
        # B. hop with the normal body: the arms anticipate, the cap and key follow through
        ('antic', dict(larm='up', rarm='down'), 170),
        ('launch', dict(larm='raise', rarm='down', dy=-1, cap=1), 70),            # cap pressed
        ('rise', dict(larm='hi', rarm='down', legs='short', dy=-2), 80),
        ('apex', dict(larm='hi', rarm='down', legs='short', dy=-2, cap=-1), 170),  # cap floats
        ('fall', dict(larm='wave', rarm='side', dy=-1, cap=-1), 70),
        ('land', dict(larm='out', rarm='side', dust=0, cap=-1), 100),   # thump: cap still up, key dips
        ('recover', dict(larm='side', rarm='out', dust=1, cap=1), 100),  # cap lands, pressed on
        ('settle', dict(dust=2, **WAIT), 120),
        # C. patient wait (the wait_face track does the blinks and the glances)
        ('wait', dict(**WAIT), 900),
        ('blink', dict(**WAIT), 120),
        ('wait2', dict(**WAIT), 80),
        ('glance', dict(**WAIT), 320),
        ('wait3', dict(**WAIT), 330),
        # D. the bubble pops again: it gathers (squash), his eyes go wide, it pops, his arm rises
        ('notice', dict(**WAIT), 170),
        ('lift', dict(larm='up', rarm='out'), 90),
        ('reach', dict(larm='raise', rarm='out'), 90),
    ]
    T, t = {}, 0
    for k, _, ms in keys:
        T[k] = t
        t += ms
    assert t == LOOP, t

    BODY = [(T[k], kw) for k, kw, _ in keys]
    trunk, limbs, gear = [], [], []
    for k, kw, ms in keys:
        ft, fl, _, fg = body(**kw)
        trunk.append((ft, ms))
        limbs.append((fl, ms))
        gear.append((fg, ms))

    # his face (expression from that moment on), in two fine layers that never draw at the same time:
    # the burst and the re-pop are the same every loop ...
    FACE = [
        (0, 'sparkle'),                    # HEY! sparkle eyes on you through both waves ...
        (T['w2'], 'glint'),                # ... twinkling each time his hand goes up high
        (T['w3'], 'sparkle'),
        (T['w6'], 'glint'),
        (T['antic'], 'line'),              # squeezed shut: winding up, through the push-off ...
        (T['rise'], 'sparkle'),            # ... eager eyes pop open a beat after take-off
        (T['land'], 'half'),               # thump: a half-lid flinch ...
        (T['recover'], 'open'),            # ... on you, key offered (the wait layer acts from here)
        (T['notice'], 'wide'),             # the bubble gathers to pop: WIDE eyes, "hey!" (350 ms,
                                           # through the pop, into frame 0's sparkle)
    ]
    # ... and the patient wait alternates between two loops (a quick blink into a glance at the
    # bubble; then glances at the key and the padlock and a slow blink), so the long wait never ticks
    # like a metronome
    WAIT_FACE = [
        (0, 'open'),
        (T['blink'], 'half'),              # loop 1: a smooth fine blink (half, line, half: 60/80/60) ...
        (T['blink'] + 60, 'line'),
        (T['blink'] + 140, 'half_ur'),     # ... its lid lifting where he is about to look ...
        (T['glance'], 'look_ur'),          # ... a hopeful glance up at his bubble: the '!' swells
        (T['wait3'], 'open'),              # back to you as it settles: still hold
        (LOOP + T['wait'] + 250, 'look_r'),   # loop 2: the key glints, he glances at it ...
        (LOOP + T['wait'] + 510, 'look_l'),   # ... on to the padlock ("this key, that lock") ...
        (LOOP + T['wait'] + 840, 'open'),     # ... the '!' swells, and as it settles: back to you
        (LOOP + T['glance'], 'half'),         # a slow blink while the '!' swells again ...
        (LOOP + T['glance'] + 80, 'line'),
        (LOOP + T['glance'] + 240, 'half'),
        (LOOP + T['wait3'], 'open'),          # ... eyes open as it settles: still hold
    ]

    def face_frames(track, total):
        """The fine overlay for a face track, cut at its own beats and at every body beat."""
        cuts = sorted({s + n * LOOP for s, _ in BODY for n in range(total // LOOP)} | {s for s, _ in track})
        out = []
        for i, ct in enumerate(cuts):
            ms = (cuts[i + 1] if i + 1 < len(cuts) else total) - ct
            out.append((body(face=_at(track, ct), **_at(BODY, ct % LOOP))[2], ms))
        return out

    face, face_wait = face_frames(FACE, LOOP), face_frames(WAIT_FACE, 2 * LOOP)
    for t in range(0, 2 * LOOP, 10):
        assert _at(FACE, t % LOOP) == 'open' or _at(WAIT_FACE, t) == 'open', t

    # the bubble's shape (follow-through + the re-pop); same timing table as the body
    bub = at_times([
        (0, bubble()),                         # frame 0: settled right after the pop
        (T['launch'], bubble(_BUB_SHORT)),     # lifts its tail out of the way of his rising head ...
        (T['rise'], bubble(_BUB_STRETCH)),     # ... tugged narrow while he is up ...
        (T['fall'], bubble(_BUB_SHORT)),       # ... relaxes as he comes down ...
        (T['land'], bubble()),                 # ... tail snaps back down on his impact ...
        (T['recover'], bubble(_BUB_SQUASH)),   # ... and the bubble squashes a frame late
        (T['settle'], bubble()),
        (T['notice'], bubble(_BUB_SQUASH)),    # pop again: squash ...
        (T['lift'], bubble(_BUB_STRETCH)),     # ... stretch ...
        (T['reach'], bubble()),                # ... settle (ticks burst, frame 0)
    ], LOOP)

    # on top: pop ticks, the gentle '!' pulse and the key's glint (same timing table)
    swell = swell_overlay()
    kx, ky = (26, 12)                         # just above the key's shaft, next to the bow (key held out)
    key_glint = []
    for dt, i in ((0, 0), (90, 1), (200, 0)):
        f = Frame()
        f.place(SPARK[i], kx, ky)
        key_glint.append((T['wait'] + 160 + dt, f))
    pop = at_times([
        (0, ticks(_TICKS_BIG)),                # frame 0: the ticks burst out ...
        (T['w1'], ticks(_TICKS_OUT)),          # ... and fly away
        (T['w2'] + 60, Frame()),
    ] + key_glint + [                          # after a quiet beat, the key he offers glints ("ting")
        (T['wait'] + 440, Frame()),
        (T['wait'] + 600, swell),              # gentle pulse 1
        (T['wait'] + 840, Frame()),
        (T['glance'], swell),                  # pulse 2, on the very frame his eyes reach it (loop 1) ...
        (T['wait3'], Frame()),                 # ... it settles as his eyes come back to you
        (T['lift'], ticks(_TICKS_IN)),         # ticks shoot out of the stretching bubble
        (T['reach'], ticks(_TICKS_BIG)),
    ], LOOP)

    lock = Frame()
    lock.place(_LOCK, *LOCK_AT)

    # the padlock catches the light on its own long loop (it never moves, so the glints can run out
    # of sync with the body): a turning gold twinkle on the shackle's top-left curve in the first
    # loop's still hold, and a quick white shine on the brass body's highlight in the second loop's.
    # Each starts a beat after his eyes settle on you and is gone as the bubble gathers to pop.
    sh, bd = (3, 13), (2, 17)
    t1, t2 = T['wait3'] + 60, LOOP + T['wait3'] + 60
    tw1 = [(0, SPARK[0], sh), (60, SPARK[1], sh), (130, SPARK[2], sh), (210, SPARK[1], sh), (270, None, None)]
    tw2 = [(0, _SHINE[0], bd), (90, _SHINE[1], bd), (200, _SHINE[0], bd), (270, None, None)]
    assert t1 + 270 == T['notice'] and t2 + 270 == LOOP + T['notice']
    glint = glints([(0, None, None)] + [(t1 + dt, s, xy) for dt, s, xy in tw1]
                   + [(t2 + dt, s, xy) for dt, s, xy in tw2], 10600)
    return anim(NAME, DESC, [layer('bubble', bub), layer('trunk', trunk), layer('limbs', limbs),
                             layer('face', face), layer('wait_face', face_wait), layer('gear', gear),
                             layer('pop', pop), layer('lock', [(lock, LOOP)]), layer('glint', glint)],
                state=STATE)
