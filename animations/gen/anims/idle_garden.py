"""idle-garden - Idle variant: tending a little plant.

STORYBOARD (s; ONE master beat list drives every synced layer, so nothing can drift; loop 23.07 s)
  0.00  HOLD at HOME, official open eyes (frame 0 = the reduced-motion still).  Left: a violet butterfly
        basks, wings spread, on a red toadstool.  Right: his blue watering can (arched handle, spout with
        a cyan rose, navy shade at the front-bottom) parked beside a terracotta pot with a two-leaf sprout.
  2.40  blink .. 3.41 a glance at the butterfly (the eyes lead); 3.71 it closes its wings up and opens
        them again (hello) .. 4.54 a blink on the big eye turn .. 4.64 he checks his sprout .. 5.20 his
        eyes drop to the can
  5.50  GRIP: his hand closes on the handle (a straight contact) .. LIFT (ease out: 110 / 150 / 180 ms):
        the can hangs from his hand, then up on his toes (left arm out for balance) he holds it out, then
        tips it forward on his raised hand
  6.07  POUR: three drops leave the rose one at a time; each falls with gravity (130 ms under the rose,
        90 ms a row lower) and bursts in cyan on the stem tip or the seed leaf; the last bursts as the can
        tips back (6.73) .. upright .. off his toes .. 7.09 it hovers a row above the ground .. 7.23 set
        down (3-2-1 rows: ease in) and he lets go
  7.73  GROW 1, one row per frame (ease out): the stem pokes up, a folded leaf pair, it unfolds with a
        1-row overshoot and settles (8.13) .. he double-blinks (huh?) and admires it
  9.17  the butterfly takes one slow wing-breath on its toadstool (a long perch never goes dead)
 10.40  GROW 2: the tip rises a row as a green bud .. the pink shows a row too tall (overshoot) .. and
        settles (10.65) .. 10.96 the bud sways toward him (slow) .. 11.58 and back
 12.30  the butterfly raises its wings (anticipation) and lifts off: an arc over his head with 1-3-cell
        steps, eased in and out, the wings flapping open / up with an uneven 1-row bob.  He notices it with
        a blink on the turn (12.60), his eyes trail it a beat behind: left .. up (12.96) .. right (13.22),
        where it slows by the bud, which swells, cups and BLOOMS (13.57: a glint pings, + then x); it
        touches down on the open flower (13.72), which dips a row under it as its wings settle (13.86)
 14.12  ADMIRE: a blink on the eye turn with the arm down (anticipation) .. 14.22 a hand up, eyes up-right
        on the visitor; a tiny library heart pops from his hand (dot, heart) and floats up with a sway ..
        fades (14.91)
 15.11  TABLEAU: the hand comes down; he gazes at the flower and its visitor (look_r, arms at his sides);
        16.01 the butterfly takes a slow wing-breath on the flower; 16.82 he blinks
 17.87  the butterfly raises its wings, his hand comes up and his eyes go up-right; lift-off (18.02):
        the flower springs back past rest and settles; it flutters out over the top-right edge while he
        waves bye (up / high / up / high); gone at 18.43, the hand lingers .. 18.85 down, eyes back on the
        flower
 19.11  the flower closes (cup, bud) .. 19.77 the bud nods off with his slow blink .. 20.07 a SEED hangs
        from it for a beat, then drops (1 row, then 2: gravity) as the leaves fold up and the plant tucks
        itself back into its pot (1 row, then 2: ease in) .. 20.44 the seed lands on the rim and rolls
        into the hole the stem left (20.75)
 20.99  a nub, the two leaves unfold: the sprout again (21.34); meanwhile the butterfly flutters back in
        from the left edge, slowing, and lands on its toadstool (21.54 wings up, 21.77 open); he looks
        back to you
 22.07  HOLD -> loop (1.3 s + frame 0's 2.4 s = 3.7 s of calm across a pixel-identical seam)
Eye closures: 2.40, 4.54, 8.13 + 8.41, 12.60, 14.12, 16.82, 19.77 s (gaps 2.1 / 3.6 / 0.3 / 4.2 / 1.5 /
2.7 / 3.0 / 5.7).  Holds of 400 ms or more: ~54% of the loop.

Layers, back to front: can | stalk + head (the plant split at the head's bottom row: a sway, a dip or the
bloom redraws only its own part; drawn behind the pot so the plant can tuck itself back in; the seed
rides in the stalk layer on the same steps) | scene (static: toadstool, pot) | trunk + arm + eyes (Clawd
drawn whole with put_clawd every beat, then split by what changes: the trunk moves only when he rises onto
his toes, the arm layer holds the kit's right-arm cells, the eye layer only the kit's black eye pixels
over plain orange; the composite is exactly the put_clawd frame) | fx (drops, bursts, heart) | butterfly
(+ the bloom glint, which rides on its flight steps at no extra frames).
Face: kit eyes only (black ink per STYLE section 0), and every glance keeps both eyes inside his body:
look_ur only with the right arm 'up' / 'high', look_dr only with it 'side' / 'down', look_l / look_r with
the arms out to that side.  Normal body size; on his toes = kit legs 'long' with the whole normal body one
row up (taller, never shorter), to reach over the plant for the pour.
Local sprites (none in the library): can, pot, toadstool, plant stages, butterfly, seed.
Library: sparkle_small (the bloom glint), heart_pop (the tiny heart).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'idle-garden'
STATE = 'Idle variant: tending a little plant'
DESC = ('Tends a potted sprout: tips his little blue watering can over it on tiptoe, watches it grow '
        'leaves, a bud and a pink flower, admires it while a butterfly visits and waves it goodbye, then '
        'the flower drops a seed that becomes the sprout again.')

HX, HY = HOME
PX = 28            # pot / plant column
BASE = 16          # the plant's bottom row (the stem stands on the pot rim, row 17)
HEADY = 11         # bottom row of the bud / flower head
MX = 5             # toadstool column
PERCH = (MX, 13)   # butterfly on its toadstool (anchor = centre of its middle row)
BLOOM = (PX, 6)    # butterfly on top of the open flower: its hind wings on the two top petals
GLINT = (23, 10)   # the bloom glint, left of the petals


def _S(rows, anchor, name=''):
    return Sprite(rows, anchor=anchor, name=name)


def _put(f, spr, x, y):
    """frame.place, but cells outside the canvas are skipped (entering / leaving at an edge)."""
    for sx, sy, ch in spr.cells:
        px, py = x + sx - spr.ax, y + sy - spr.ay
        if 0 <= px < W and 0 <= py < H:
            f.put(px, py, ch)


# ================================================================ scenery (static layer)
_POT = _S(['OoooO',
           '.oOR.',
           '.ORR.'], (2, 2), 'pot')
_TOADSTOOL = _S(['.rrr.',
                 'rWrrR',
                 'RRRRR',
                 '.ttT.',
                 '.ttT.'], (2, 4), 'toadstool')

# ================================================================ watering can
# Blue tin lit from the top-left: one navy shade at the front-bottom, a spout with a cyan rose, an arched
# handle.  The body is 4 cells wide in every pose (rows of 4 + 3); the tilts stagger its rows.
# 'carry' anchor = the handle's top-left cell (his grip); 'half' / 'pour' anchor = the rear-bottom cell
# that sits on his raised hand (right above it: a straight contact, not a corner touch).
_CAN = {
    'carry': _S(['bb..c',
                 'b.bb.',
                 'bbbb.',
                 'bbB..'], (0, 0), 'can'),
    'half': _S(['.bb...',
                '.b.bbc',
                'bbbb..',
                '.bbB..'], (1, 3), 'can_half'),
    'pour': _S(['.bb....',
                '.b.b...',
                'bbbb...',
                '.bbBb..',
                '.....bc'], (1, 3), 'can_pour'),
}
CAN_REST = (21, 16)     # the handle's top-left when the can stands on the ground (no cell touches the pot)

# ================================================================ butterfly (anchor = centre of its middle row)
# Seen from above: four wing lobes splayed around its body (a notch at the top and between the hind
# wings), so the silhouette reads as a butterfly at 3 px.  One violet (a darker body dot vanishes at real
# size anyway, and each colour costs every frame bytes): mid-tone, 4.5:1 on dark, 3.7:1 on white.
_BF = {
    'rest': _S(['vv.vv',            # wings open: perched, gliding
                'vvvvv',
                '.v.v.'], (2, 1), 'bfly_rest'),
    'up': _S(['v...v',              # wings raised in a V: a flap, a slow wing-breath, take-off
              '.vvv.',
              '..v..'], (2, 1), 'bfly_up'),
    'fold': _S(['v.v',              # wings closing up over its back, a narrow Y (hello)
                '.v.',
                '.v.'], (1, 1), 'bfly_fold'),
}

# ================================================================ plant
# Stalk stages: rows listed top -> bottom, the last row on BASE (stem column = the middle one).
_STALK = {
    'sprout': ['gg.gg',
               '.gGg.',
               '..G..'],
    'tip1': ['..g..',
             'ggGgg',
             '.gGg.',
             '..G..'],
    'tip2': ['..g..',
             '..G..',
             'ggGgg',
             '.gGg.',
             '..G..'],
    'fold': ['..g..',               # the new leaf pair, still folded against the stem
             '.gGg.',
             '..G..',
             'ggGgg',
             '.gGg.',
             '..G..'],
    'over': ['..g..',               # unfolds with a 1-row overshoot ..
             'g.G.g',
             '.gGg.',
             '..G..',
             'ggGgg',
             '.gGg.',
             '..G..'],
    'leaves': ['..g..',             # .. and settles
               'g.G.g',
               '.gGg.',
               'ggGgg',
               '.gGg.',
               '..G..'],
    'folded': ['.p...',             # end: the leaves fold up against the stem under the nodding bud
               'gpg..',
               '.gGg.',
               '..G..',
               '.gGg.',
               '..G..',
               '..G..'],
    'nub': ['..g..'],               # the seed sprouts ..
    'unfold': ['.g.g.',             # .. its two leaves unfold
               '..G..'],
}
# Head stages: rows top -> bottom, the last row on HEADY.
_HEAD = {
    'gbud': ['..g..',               # the tip rises a row as a green bud ..
             '.gGg.'],
    'pover': ['..p..',              # .. the pink shows, a row too tall (overshoot) ..
              '..p..',
              '.gpg.'],
    'bud': ['..p..',                # .. and settles
            '.gpg.'],
    'swell': ['..p..',
              '.ppp.',
              '.gpg.'],
    'cup': ['p.p.p',
            'ppjpp',
            '.ppp.'],
    'flower': ['.p.p.',
               'ppjpp',
               'pjjjp',
               '.ppp.'],
    'nod': ['.p...',                # the closed bud nods off to the left
            'gpg..'],
}


def _rows_sprite(rows, name):
    """Sprite whose anchor is the middle column of its bottom row."""
    return _S(rows, (len(rows[0]) // 2, len(rows) - 1), name)


_STALK_S = {k: _rows_sprite(v, 'stalk_' + k) for k, v in _STALK.items()}
_HEAD_S = {k: _rows_sprite(v, 'head_' + k) for k, v in _HEAD.items()}

# ================================================================ fx
_GLINT = get('sparkle_small')            # frames: 0 dot, 1 plus, 2 diagonal x (play 0-1-2-1)
_TINY_HEART = get('heart_pop').sprite(0)  # the 3x3 pink pop-in heart
_DOT = _S(['p'], (0, 0), 'heart_dot')
_DROP = _S(['b'], (0, 0), 'drop')        # blue: 5.0:1 on dark, 3.4:1 on white
_SPLASH = _S(['c'], (0, 0), 'splash')    # one-frame cyan burst where a drop lands
_FX = {'drop': _DROP, 'splash': _SPLASH, 'heart': _TINY_HEART, 'dot': _DOT}

# The pour (the rose is at (27, 11)): one drop at a time, each falls with gravity (a long frame just under
# the rose, a short one a row lower) and bursts on the stem tip (col 28) or on the seed leaf (col 27).
_POUR = [   # (ms, drops)
    (130, [('drop', 28, 12)]),
    (90, [('drop', 28, 13)]),
    (130, [('splash', 28, 14), ('drop', 27, 12)]),
    (90, [('splash', 27, 13)]),
    (130, [('drop', 28, 12)]),
    (90, [('drop', 28, 13)]),
]
_POUR_TAIL = [('splash', 28, 14)]       # the last one lands while the can tips back up


# ================================================================ beats
def _beats():
    B = []

    def beat(ms, **kw):
        B.append((ms, kw))

    def fly(path):
        """path: (pose, x, y, ms, extra-state) steps of the butterfly."""
        for k, x, y, ms, kw in path:
            beat(ms, bf=(k, x, y), **kw)

    perch = lambda k: (k,) + PERCH                 # noqa: E731
    bloom = lambda k, dy=0: (k, BLOOM[0], BLOOM[1] + dy)   # noqa: E731

    # ---------------------------------------------------------------- A. opening calm
    beat(2400, eyes='open', larm='side', rarm='side', tip=False, can='rest', stalk='sprout', head=None,
         hdx=0, hdy=0, sdy=0, fx=[], bf=perch('rest'), glint=None, seed=None)
    beat(110, eyes='blink')
    beat(900, eyes='open')
    beat(300, eyes='look_l')                         # the eyes lead ..
    beat(450, bf=perch('fold'))                      # .. it closes its wings up once: hello
    beat(380, bf=perch('rest'))
    beat(100, eyes='blink')                          # a blink on the big eye turn
    beat(560, eyes='look_r')                         # how is my sprout?
    beat(300, eyes='look_dr')                        # eyes lead: the can
    # ---------------------------------------------------------------- B. lift, pour, lower
    beat(130, rarm='down')                           # grip: his hand closes on the handle
    beat(110, rarm='up', can='lift', eyes='look_r')  # lift (ease out: quick start, longer frames
    beat(150, rarm='raise', tip=True, larm='out', can='raise')   # toward the top) .. up on his toes,
    beat(180, rarm='wave', can='half')               # the left arm out for balance .. it tips forward
    for i, (ms, drops) in enumerate(_POUR):          # POUR
        beat(ms, can='pour', fx=drops)
    beat(120, can='half', fx=_POUR_TAIL)             # tipping back while the last drop bursts ..
    beat(120, rarm='raise', can='raise', fx=[])      # .. upright
    beat(120, rarm='up', tip=False, larm='side', can='lift')   # off his toes (ease in)
    beat(140, rarm='side', can='hover')              # the can hovers a row above the ground ..
    beat(500, can='rest')                            # .. and settles: a held beat
    # ---------------------------------------------------------------- C. grow 1 (1 row per frame, ease out)
    beat(90, stalk='tip1')
    beat(90, stalk='tip2')
    beat(120, stalk='fold')
    beat(100, stalk='over')                          # unfolds with an overshoot ..
    beat(140, stalk='leaves', eyes='blink')          # .. settles; he double-blinks (huh?)
    beat(140, eyes='look_r')
    beat(110, eyes='blink')
    beat(650, eyes='look_r')
    beat(430, bf=perch('up'))                        # the butterfly takes one slow wing-breath
    beat(800, bf=perch('rest'))
    # ---------------------------------------------------------------- D. grow 2: a bud
    beat(130, head='gbud')                           # the tip rises a row as a green bud ..
    beat(120, head='pover')                          # .. the pink shows, a row too tall ..
    beat(310, head='bud')                            # .. and settles
    beat(620, hdx=-1)                                # the bud sways toward him (slow) ..
    beat(720, hdx=0)                                 # .. and back
    # ---------------------------------------------------------------- E. the butterfly comes; the bloom
    beat(150, bf=perch('up'))                        # wings up: anticipation
    fly([  # varied steps (1-3 cells), ease out / in, an uneven 1-row bob on the flaps (open = higher)
        ('rest', 6, 11, 150, {}),
        ('up', 8, 10, 130, dict(eyes='blink')),      # he notices: a blink on the big eye turn ..
        ('rest', 11, 8, 120, dict(eyes='look_l')),   # .. and follows it, a beat behind
        ('up', 14, 7, 110, {}),
        ('rest', 17, 4, 120, dict(eyes='look_u')),   # over his head now
        ('up', 20, 4, 140, {}),
        ('rest', 22, 2, 170, dict(eyes='look_r', head='swell')),   # it slows by the bud, which swells,
        ('up', 24, 4, 180, dict(head='cup')),                      # cups,
        ('rest', 26, 4, 150, dict(head='flower', glint=1)),        # and BLOOMS: a glint pings (+ .. x)
        bloom('up') + (140, dict(glint=2)),                        # touch down on the open flower ..
        bloom('rest', 1) + (260, dict(hdy=1, glint=None)),         # .. which dips a row under it
    ])
    # ---------------------------------------------------------------- F. admire
    beat(100, eyes='blink', rarm='down')             # anticipation: arm down, a blink on the eye turn
    beat(110, rarm='up', eyes='look_ur', fx=[('dot', 20, 11)])   # a hand up ("ooh"), eyes on the visitor
    beat(140, fx=[('heart', 20, 10)])                # a tiny heart pops from his hand, floats up, sways
    beat(190, fx=[('heart', 21, 9)])
    beat(250, fx=[('heart', 20, 8)])
    beat(200, fx=[('dot', 20, 6)])                   # .. and fades; the hand stays up a beat longer
    # ---------------------------------------------------------------- G. tableau
    beat(900, rarm='side', eyes='look_r', fx=[])     # the hand comes down: he admires it
    beat(430, bf=bloom('up', 1))                     # a slow wing-breath on the flower
    beat(380, bf=bloom('rest', 1))
    beat(110, eyes='blink')
    beat(940, eyes='look_r')
    # ---------------------------------------------------------------- H. it leaves; he waves bye
    beat(150, bf=bloom('up', 1), rarm='up', eyes='look_ur')   # wings up .. his hand comes up
    fly([
        ('rest', 29, 4, 130, dict(hdy=-1, rarm='high')),   # lift-off: the flower springs back (overshoot) ..
        ('up', 30, 4, 150, dict(hdy=0, rarm='up')),        # .. and settles; bye, bye
        ('rest', 32, 1, 130, dict(rarm='high')),
    ])
    beat(420, bf=None, rarm='up')                    # gone .. the hand lingers ..
    beat(260, rarm='side', eyes='look_r')            # .. and comes down
    # ---------------------------------------------------------------- I. the flower closes; the seed
    beat(240, head='cup')
    beat(420, head='bud')
    beat(300, head='nod', eyes='blink')              # the bud nods off with his slow blink ..
    beat(130, stalk='folded', head=None, seed=(26, 12), eyes='look_dr')   # .. a seed hangs from it ..
    beat(130, seed=(26, 13))                         # .. and drops (1 row,
    beat(110, sdy=1, seed=(26, 15))                  # then 2: gravity); the plant tucks itself back in
    beat(160, sdy=3, seed=(26, 16))                  # .. the seed lands on the rim ..
    beat(150, stalk=None, sdy=0, seed=(27, 16))      # .. and rolls into the hole the stem left
    beat(240, seed=(28, 16))
    # ---------------------------------------------------------------- J. sprout again; the butterfly is back
    beat(170, seed=None, stalk='nub', bf=('rest', 1, 9))      # a nub; the butterfly flutters in ..
    beat(180, stalk='unfold', bf=('up', 3, 11))
    beat(200, stalk='sprout', bf=('rest', 4, 11))    # (slowing down: ease in)
    beat(230, bf=perch('up'))                        # .. lands on its toadstool, wings up ..
    beat(300, bf=perch('rest'), eyes='open')         # .. and opens them; he looks back to you
    beat(1000)                                       # HOLD (flows into frame 0's hold)
    return B


def _expand(B):
    out, state = [], {}
    for ms, kw in B:
        state = dict(state, **kw)
        out.append((ms, dict(state)))
    return out


# ================================================================ frames
def _pose(s):
    return clawd(eyes=s['eyes'], larm=s['larm'], rarm=s['rarm'], legs='long' if s['tip'] else 'stand')


def _box(s):
    return (HX, HY - 1) if s['tip'] else (HX, HY)


def _can_frame(s):
    f = Frame()
    c = s['can']
    if c == 'rest':
        f.place(_CAN['carry'], *CAN_REST)
    elif c == 'hover':
        f.place(_CAN['carry'], CAN_REST[0], CAN_REST[1] - 1)   # still in his hand at his side
    else:
        x, y = _box(s)
        gx, gy = _pose(s).at('hand_r', x, y)
        if c == 'lift':
            f.place(_CAN['carry'], gx, gy)            # hangs from his raised hand by the handle
        elif c == 'raise':
            f.place(_CAN['carry'], gx + 1, gy)        # held out by the handle beside his hand
        else:
            f.place(_CAN[c], gx, gy)                  # tipped forward on his raised hand
    return f


def _clawd_frames(s):
    """Clawd drawn once with put_clawd (kit pose), then split by what changes, so each part pays only for
    its own changes: the trunk (body, legs, left arm; it moves only when he rises onto his toes), his
    right arm (the kit's arm cells: grip, lift, pour, the hand up, the wave) and his eyes (only the kit's
    black eye pixels; under them the trunk is plain orange).  The composite is exactly the put_clawd
    frame, every beat."""
    x, y = _box(s)
    whole, bare = Frame(), Frame()
    put_clawd(whole, _pose(s), x, y)
    put_clawd(bare, clawd(eyes='blink', larm=s['larm'], rarm='none', legs='long' if s['tip'] else 'stand'),
              x, y)
    trunk, rarm, eyes = Frame(), Frame(), Frame()
    for xy, ch in whole.px.items():
        if ch == EYE_INK:
            trunk.px[xy] = '#'
            eyes.px[xy] = ch
        elif xy in bare.px:
            trunk.px[xy] = ch
        else:
            rarm.px[xy] = ch
    trunk.meta = whole.copy().meta
    return trunk, rarm, eyes


def _stalk_frame(s):
    f = Frame()
    if s['stalk']:
        spr = _STALK_S[s['stalk']]
        dy = s['sdy']
        for sx, sy, ch in spr.cells:
            px, py = PX + sx - spr.ax, BASE + dy + sy - spr.ay
            if py <= BASE:              # below the soil line it is hidden by the pot anyway
                f.put(px, py, ch)
    if s['seed']:                       # the seed lives in this layer: its steps line up with the plant's
        f.put(s['seed'][0], s['seed'][1], 'T')
    return f


def _head_frame(s):
    f = Frame()
    if s['head']:
        f.place(_HEAD_S[s['head']], PX + s['hdx'], HEADY + s['hdy'])
    return f


def _fx_frame(s):
    f = Frame()
    for k, x, y in s['fx']:
        _put(f, _FX[k], x, y)
    return f


def _bf_frame(s):
    f = Frame()
    if s['bf']:
        k, x, y = s['bf']
        _put(f, _BF[k], x, y)
    if s['glint'] is not None:          # the bloom glint rides on the butterfly's steps (no extra frames)
        _put(f, _GLINT.sprite(s['glint']), *GLINT)
    return f


def build():
    seq = _expand(_beats())
    total = sum(ms for ms, _ in seq)
    scene = Frame()
    scene.place(_TOADSTOOL, MX, GROUND)
    scene.place(_POT, PX, GROUND)
    split = [(_clawd_frames(s), ms) for ms, s in seq]
    layers = [
        layer('can', [(_can_frame(s), ms) for ms, s in seq]),
        layer('stalk', [(_stalk_frame(s), ms) for ms, s in seq]),
        layer('head', [(_head_frame(s), ms) for ms, s in seq]),
        layer('scene', [(scene, total)]),
        layer('trunk', [(t, ms) for (t, a, e), ms in split]),
        layer('arm', [(a, ms) for (t, a, e), ms in split]),
        layer('eyes', [(e, ms) for (t, a, e), ms in split]),
        layer('fx', [(_fx_frame(s), ms) for ms, s in seq]),
        layer('butterfly', [(_bf_frame(s), ms) for ms, s in seq]),
    ]
    return anim(NAME, DESC, layers, state=STATE)
