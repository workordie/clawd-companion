"""working - Claude is running tools / editing / writing.  Preview:  python3 gen/preview.py anim working

Storyboard (master loop 9.75 s; every synced layer is cut from ONE beat list, so nothing ever drifts. The
'chunk done' reward, where the CI run stalls and the duck change from loop to loop: 3 loops = 29.3 s
before the whole picture repeats):
  0.00  A  Frame 0: at HOME at his desk, headphones on, mid-keystroke: left hand down on a key glinting
           cyan, eyes on the code, the line he is typing in cyan on the monitor, mug steaming on the books,
           rubber duck on the monitor.
  0.13     Enter with the RIGHT hand (the wide Enter key lights) commits the line in syntax colours and
           scrolls the code; a pause, then a fast burst with his eyes on the keys.
  1.02  C  A key and Enter, a long read of the screen with a quick double blink (2.02 / 2.26 s), two
           bursts (his eyes slide right to find the Enter key), a pause, two more bursts, eyes drifting
           right again.
  3.92  D  Chunk done: the right arm rises (110 ms) and holds raised in the clear air beside the monitor,
           aiming (270 ms), a 60 ms smear ... 4.36 SLAM on Enter: three keys flash, a click spark, a
           reflex blink, the mug hops off the books. The CI bar runs: 2 cells at once, then it stalls
           somewhere different on each loop (near the end / halfway / on a full yellow bar) ...
  4.93  E  ... green. A fist pump (up, raised, easing down) while the reward appears over his head, his
           eyes going up-right to the monitor and then up to it (look_ur, look_u):
           loop 1: "{" then "}" burst out of the monitor's corner and sail up-left on easing arcs to land
                   centred over his head as "{ }";
           loop 2: tests pass: a green tick pops in, overshoots and settles (library check_pop) while the
                   duck squashes, hops, hangs, drops through one cell and lands;
           loop 3: a "/" pops in and "<" ">" spring out of it and bounce back: "</>".
           It holds, then twinkles out in gold sparkles while his eyes go back to the code.
  6.22  B  He reviews the result on the screen (the green bar clears at 6.92), then a same-hand double
           tap with a visible lift.
  7.46  F  Coffee: glances at the mug, reaches (hand on the handle, eyes on it), lifts it, swings it up
           over his raised hand (the cup turns, its handle away from us) to his face (his eye on it), a
           savouring blink, swings it back out over his hand, sets it on the books, his hand lingers.
  9.03  G  Back to the code: right key, pause, left key with his eyes on the screen, lift ... frame 0.
Ambient: steam puffs from the mug, 4 per loop (2.44 s cycle, phase-locked so its pause always covers the
whole time the cup is off the books: the steam never hangs in the air without its cup); the monitor's
amber disk-activity LED blips on its own 2.17 s loop, co-prime with everything else.
Plain face only (open / blink / look_*), normal body size: STYLE.md section 0.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'working'
STATE = 'Claude is running: tools, edits, writing'
DESC = ('Headphones on, Clawd codes at his desk in natural bursts while the code grows on his monitor; '
        'when a chunk is done he slams Enter, the CI bar goes green and a reward pops over his head '
        '({ }, a green check while the duck hops, or </>), then he reviews, types on and sips his coffee.')


# =====================================================================================================
# Local sprites (painted at absolute canvas positions)
# =====================================================================================================
def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


# Monitor x 23..30, y 8..17: silver bezel lit from the top-left, navy screen, blue status bar, green
# power LED, neck + foot standing on the desk top (y 18). Column 22 stays empty so his raised fist and
# the slam's click spark read against the background, not against the bezel.
_MONITOR = [
    'mmmmmmmN',
    'miiiiiin',
    'miiiiiin',
    'miiiiiin',
    'miiiiiin',
    'miiiiiin',
    'mbbbbbbn',
    'NNNNNNgn',
    '...Nn...',
    '.mNNNNn.',
]
_MON_X, _MON_Y = 23, 8
_SCR_X, _SCR_W = 24, 6          # code area x 24..29
_LINE_Y = (9, 11, 13)           # two committed lines + the line being typed
_BAR_Y = 14                     # status / CI bar row

# Desk slab x 1..30 (top surface + front edge); keyboard in front of Clawd (x 9..21) with a wide
# Enter key at its right end (x 20-21).
_DESK = [
    't' * 30,
    'T' * 30,
]
_KEYBOARD = [
    'nmnmnmnmnmnmm',
    'NNNNNNNNNNNNN',
]
_KB_X, _KB_Y = 9, 17

# keys each hand hits (hands strike at x 10 / x 20). Fixed pseudo-random walks, never the same key twice
# in a row for one hand; index 0 = frame 0: right under the left hand.
_LKEYS = [(10, 17), (12, 17), (11, 17), (12, 17), (10, 17), (11, 17)]
_RKEYS = [(19, 17), (18, 17)]
_ENTER = ((20, 17), (21, 17))                   # every Enter: the wide key under his right hand
_SLAM = ((19, 17), (20, 17), (21, 17))          # the big one: Enter + its neighbour flash
_CLICK = ((22, 16), (21, 15))                   # little impact tick beside the Enter key

# Two books lying on the desk; the mug stands on them, so its handle sits exactly where his left hand
# lands when he reaches out (larm='out').
_BOOKS = [
    '.vjjvvV',
    'rrrrrrR',
]
_BOOKS_X, _BOOKS_Y = 2, 16


def _item(name, slot, fallback):
    """Library item; while another artist is mid-save, the same look from a local copy.
    fallback: [(rows, anchor), ...] one per frame."""
    try:
        return get(name)
    except KeyError:
        return Item(name, slot, name, [Sprite(r, anchor=a, name=name) for r, a in fallback])


def _sprite(name, fallback_rows):
    return _item(name, 'hand', [(fallback_rows, (0, 0))]).sprite(0)


# The library mug. Resting on the books / lifted, it is held by its handle with the cup away from him
# ('mug_held' picture: handle on the right, toward Clawd; anchor = the grip). At his face the cup has
# swung round his hand ('mug' picture: handle on the left, in his hand; cup in front of his face).
_MUG_HELD = _sprite('mug_held', ['cTTB..', 'cbbBbb', 'cbbB.b', 'cbbBbb'])
_MUG = _MUG_HELD.with_anchor(_MUG_HELD.x1, _MUG_HELD.y0 + 2)
_MUG_AT = {'rest': (8, 14), 'lift': (9, 13),    # clawd(larm='out' / 'up').at('hand_l')
           'jolt': (8, 13)}                     # hops off the books when he slams Enter
_MUG_FACE = _sprite('mug', ['..cTTB', 'bbcbbB', 'b.cbbB', 'bbcbbB'])
_MUG_FACE = _MUG_FACE.with_anchor(_MUG_FACE.x0, _MUG_FACE.y0)
_FACE_AT = (9, 12)                              # handle in his left hand (x 9-10), cup over x 11-14
# Mid-swing, on the way up and on the way down: the cup alone (its handle turned away from us, hidden
# behind it), upright over his raised hand (larm='raise'), so it travels an arc round his hand instead of
# popping across it: books -> lifted -> over his hand -> his face.
_CUP_COLS = {x for x, y, ch in _MUG_HELD.cells if y == _MUG_HELD.y0}
_MUG_SWING = Sprite(cells=[c for c in _MUG_HELD.cells if c[0] in _CUP_COLS], name='mug_swing')
_MUG_SWING = _MUG_SWING.with_anchor(_MUG_SWING.x0, _MUG_SWING.y0)
_SWING_AT = (7, 9)                              # cup x 7-10, y 9-12, in front of his headphone cup

# His headphones: the library 'headphones' redrawn with the band one row lower, so it hugs his head
# (one clear row) instead of floating over it like a basket handle. The cups stay on rows 10-12, clear of
# everything on row 13 (look_ur's eye, rarm 'up', the fist pump's 'raise').
_PHONES = Item('headphones', 'head', 'over-ear headphones, band hugging his head', [Sprite([
    'lv.mNNNN.vV',
    'vVN.....NvV',
    'vV.......vV',
], anchor=(5, 2), name='headphones')])

# Rubber duck (debugging buddy) sitting on the monitor, facing Clawd; a solid ink eye so it keeps its
# face on the light theme.
_DUCK = [
    '.yy....',
    'okyy..y',
    '.yyyyyj',
    '..jjjj.',
]
_DUCK_SQ = [                     # squashed (take-off / landing): head sinks into the body
    'okyy..y',
    '.yyyyyj',
    '..jjjj.',
]
_DUCK_X, _DUCK_Y = 24, 4

# Steam: one wisp per puff, rising from the coffee and breaking off at the top, then a pause. The
# library 'steam' wisp cut into a single puff (minus its source cell on row 12: that one always sits
# under the rim, since the cup only leaves its spot while the steam pauses).
_PUFF = [
    ((5, 10), (4, 11)),
    ((5, 9), (4, 10), (4, 11)),
    ((5, 8), (4, 9), (4, 10), (5, 11)),
    ((5, 7), (4, 8), (4, 9), (5, 10), (6, 11)),
    ((4, 7), (4, 8), (5, 9), (6, 10)),
    ((4, 7), (5, 8), (6, 9)),
]
_PUFF_MS = (170, 180, 190, 190, 170, 160)
_PUFFS_PER_LOOP = 4

# The monitor's amber disk-activity LED (beside the green power LED) blips "blip-blip" on its own loop,
# co-prime with the master loop: a tiny ambient that never lines up the same way twice.
_LED = (28, 15)
_LED_BLIPS = [(False, 1700), (True, 130), (False, 230), (True, 110)]

# Code the lines are drawn from, by length: keyword violet, names cyan, strings yellow, calls pink.
_CODE = {
    1: ['c'], 2: ['pp', 'cc'], 3: ['v.c', 'ccc', 'p.y'],
    4: ['c.yy', 'pp.c', 'yy.c', 'vv.y'],
    5: ['vv.cc', 'pp.cc', 'c.ppp'],
    6: ['vv.ccc', 'c.y.pp', 'pp.ccc'],
}
_SYNTAX = 'vcyp'
_INDENT = (0, 1, 1, 2, 1, 0, 1, 2)
_TYPED = 'c'                     # colour of the line being typed AND of the key that is hit


# =====================================================================================================
# 'Chunk done': the celebration beats (shared by every loop) and the three rewards (one per loop)
# =====================================================================================================
_LOOPS = 3                       # the reward, the CI run and the duck vary over 3 master loops
_DUCK_LOOP = 1                   # the duck hops for the green check

# One row per beat: ms, his eyes, his right arm (the fist pump), the duck on its hop loop
# (0 sitting, 1/2 cells up, 'sq' squashed).
_CEL = [
    (90,  'look_ur', 'up',    'sq'),   # 0 the bar turns green, "{" pops out of the monitor corner
    (100, 'look_u',  'raise', 1),      # 1 fist pump peak; the duck takes off; the check / "/" pop in
    (110, 'look_u',  'raise', 2),      # 2
    (60,  'look_u',  'up',    2),      # 3 the duck hangs at the top ...
    (60,  'look_u',  'up',    1),      # 4 ... and drops through 1 cell (never pops down)
    (150, 'look_u',  'side',  'sq'),   # 5 the reward lands centred over his head; the duck lands
    (270, 'look_u',  'side',  0),      # 6 hold
    (110, 'look_u',  'side',  0),      # 7 it twinkles out
    (110, 'look_u',  'side',  0),      # 8
    (110, 'look_r',  'side',  0),      # 9 his eyes go back to the code as it fades
    (120, 'look_r',  'side',  0),      # 10 gone
]

# The CI run after the slam: a fast start (2 yellow cells at once, every loop: the 'ci' layer), then it
# stalls somewhere different on each loop before it turns green (the 'chunk' layer): near the end,
# halfway, on a full yellow bar.
_CI_START = 2
_CI_STALL = (5, 3, 6)


def _centred(rows, name):
    s = Sprite(rows, name=name)
    return s.with_anchor((s.x0 + s.x1) // 2, (s.y0 + s.y1) // 2)


_LBRACE = _centred(['.vv', '.v.', 'v..', '.v.', '.vv'], 'brace')            # '{' (violet)
_RBRACE = _LBRACE.flipped()                                                   # '}'
_LT = _centred(['.b', 'b.', '.b'], 'tag')                                     # '<' (blue)
_GT = _LT.flipped()                                                           # '>'
_SLASH = _centred(['..b', '..b', '.b.', 'b..', 'b..'], 'slash')              # '/'
_TICK = _item('check_pop', 'fx', [(['...g', 'g.g.', '.g..'], (1, 0)),
                                  (['.........gG', '........gG.', '.......gG..', 'gG....gG...',
                                    '.gG..gG....', '..gGgG.....', '...gG......'], (5, 3)),
                                  (['......gG', '.....gG.', 'gG..gG..', '.gGgG...', '..gG....'], (3, 2))])
_SPARKLE = _item('sparkle_small', 'fx', [(['j'], (0, 0)), (['.j.', 'jyj', '.j.'], (1, 1)),
                                         (['j.j', '.j.', 'j.j'], (1, 1))])


def _rewards():
    """Per loop, per celebration beat: [(sprite, x, y), ...]. Everything lands centred over his head
    (x 15, rows 1-6), where his look_u is aimed. None = the stalled CI bar stays up one beat longer: on
    that loop the bar turns green in the same instant the reward pops in."""
    sp = _SPARKLE.sprite
    L, R = _LBRACE, _RBRACE
    braces = [                                   # "{" then "}" burst out of the monitor corner and sail
        [(L, 21, 7)],                            # up-left on easing arcs to land as "{ }"
        [(L, 18, 4)],
        [(L, 15, 3), (R, 21, 6)],
        [(L, 14, 3), (R, 19, 4)],
        [(L, 14, 3), (R, 19, 4)],
        [(L, 13, 3), (R, 17, 3)],
        [(L, 13, 3), (R, 17, 3)],
        [(sp(1), 13, 3), (R, 17, 3)],            # they twinkle out, the "{" first
        [(sp(2), 13, 3), (sp(1), 17, 3)],
        [(sp(1), 13, 3), (sp(0), 17, 3)],
        [],
    ]
    t0, t1, t2 = _TICK.sprite(0), _TICK.sprite(1), _TICK.sprite(2)
    check = [                                    # tests pass: a tick pops in, overshoots, settles
        None,                                    # (one row lower than the glyphs: the overshoot
        [(t0, 15, 4)],                           # frame is 7 tall and keeps clear of the top edge)
        [(t1, 15, 4)],
        [(t2, 15, 4)],
        [(t2, 15, 4)],
        [(t2, 15, 4)],
        [(t2, 15, 4)],
        [(t2, 15, 4), (sp(1), 19, 2)],           # a glint runs to its tip ...
        [(sp(2), 14, 5), (sp(1), 18, 3)],        # ... and it breaks into sparkles
        [],
        [],
    ]
    tags = [                                     # a "/" pops in, "<" and ">" spring out of it and
        None,                                    # bounce back: "</>"
        [(_SLASH, 15, 3)],
        [(_SLASH, 15, 3), (_LT, 10, 3), (_GT, 20, 3)],
        [(_SLASH, 15, 3), (_LT, 11, 3), (_GT, 19, 3)],
        [(_SLASH, 15, 3), (_LT, 11, 3), (_GT, 19, 3)],
        [(_SLASH, 15, 3), (_LT, 11, 3), (_GT, 19, 3)],
        [(_SLASH, 15, 3), (_LT, 11, 3), (_GT, 19, 3)],
        [(sp(1), 11, 3), (_SLASH, 15, 3), (sp(1), 19, 3)],
        [(sp(2), 11, 3), (sp(1), 15, 3), (sp(2), 19, 3)],
        [],
        [],
    ]
    for r in (braces, check, tags):
        assert len(r) == len(_CEL)
    return [braces, check, tags]


_REWARDS = _rewards()


# =====================================================================================================
# Master timeline
# =====================================================================================================
class _TL:
    """Beat list: (ms, state). A state holds everything every synced layer needs."""

    def __init__(self):
        self.segs = []
        self.st = dict(eyes='look_d', larm='side', rarm='side', lit=(), click=False,
                       mug='rest', ci=None, cel=None, keys=0)
        self.events = []         # one entry per keystroke: 'char' or 'enter'
        self.count = {'l': 0, 'r': 0}

    def add(self, ms, **kw):
        self.st.update(kw)
        s = dict(self.st)
        s['keys'] = len(self.events)
        self.segs.append((int(ms), s))

    def hold(self, ms, eyes, **kw):
        self.add(ms, eyes=eyes, larm='side', rarm='side', lit=(), **kw)

    def blink(self, back):
        self.add(120, eyes='blink', larm='side', rarm='side', lit=())
        self.st['eyes'] = back

    def key(self, hand, ms, enter=False, eyes=None):
        self.events.append('enter' if enter else 'char')
        if enter:
            hand, lit = 'r', _ENTER
        else:
            tab = _LKEYS if hand == 'l' else _RKEYS
            lit = (tab[self.count[hand] % len(tab)],)
            self.count[hand] += 1
        self.add(ms, eyes=eyes or self.st['eyes'], lit=lit,
                 larm='down' if hand == 'l' else 'side', rarm='down' if hand == 'r' else 'side')

    def burst(self, keys, ms, eyes):
        """keys: l/r = character, R = Enter (always the right hand), '-' = hands up between taps."""
        it = iter(ms)
        for ch in keys:
            if ch == '-':
                self.add(90, larm='side', rarm='side', lit=(), eyes=eyes)
            else:
                self.key(ch.lower(), next(it), enter=ch.isupper(), eyes=eyes)


def _timeline():
    t = _TL()
    # A  frame 0: left hand down on a key, eyes on the code; Enter with the right hand; a burst
    t.burst('l', [132], 'look_r')
    t.burst('R', [128], 'look_d')
    t.hold(270, 'look_d')
    t.burst('lrlr', [112, 126, 108, 140], 'look_d')
    # C  a key and Enter, a long read with a quick double blink, two bursts (eyes find the Enter key on
    #    the right), a pause, two more bursts with his eyes drifting right again
    t.burst('lR', [116, 132], 'look_d')
    t.hold(760, 'look_r')
    t.blink('look_r')
    t.hold(120, 'look_r')
    t.blink('look_r')
    t.hold(320, 'look_r')
    t.burst('lr', [118, 110], 'look_d')
    t.burst('lR', [130, 122], 'look_dr')
    t.hold(240, 'look_d')
    t.burst('rl', [112, 124], 'look_d')
    t.burst('rl', [118, 142], 'look_dr')
    # D  chunk done: the arm rises and holds raised beside the monitor (aiming), a smear, SLAM on
    #    Enter (3 keys + click spark, reflex blink, the mug jolts); the CI bar runs, then stalls
    t.add(110, eyes='look_d', larm='side', rarm='up', lit=())
    t.add(270, rarm='raise')
    t.add(60, rarm='side')
    t.events.append('enter')
    t.add(160, eyes='blink', rarm='down', click=True, lit=_SLAM, ci='run', mug='jolt')   # the desk jolts
    t.add(410, eyes='look_r', rarm='side', click=False, lit=(), mug='rest', ci='stall')
    # E  success: fist pump while the reward appears over his head and his eyes follow it
    for k, (ms, eyes, rarm, _) in enumerate(_CEL):
        t.add(ms, eyes=eyes, rarm=rarm, ci='ok', cel=k)
    t.st['cel'] = None
    # B  he reviews the result on the screen (the green bar clears), then a same-hand double tap
    #    (a visible lift between the taps)
    t.hold(700, 'look_r')
    t.hold(160, 'look_r', ci=None)
    t.burst('r-r', [140, 146], 'look_d')
    # F  coffee: spots the mug, reaches (eyes stay on it), lifts it, swings it up over his hand to his
    #    face, savouring blink, swings it back out and sets it down
    t.hold(300, 'look_l')                                     # spots the mug
    t.add(170, larm='out')                                    # hand on the handle
    t.add(100, eyes='look_ul', larm='up', mug='lift')         # off the books
    t.add(90, eyes='look_u', larm='raise', mug='swing')       # the cup turns over his raised hand ...
    t.add(340, eyes='look_l', larm='up', mug='face')          # ... to his face: sip, his eye on the cup
    t.add(150, eyes='blink')                                  # savouring blink
    t.add(90, eyes='open', larm='raise', mug='swing')         # back out over his hand
    t.add(100, larm='up', mug='lift')
    t.add(230, larm='out', mug='rest')                        # back on the books, hand lingers: "ahh"
    t.hold(170, 'look_r')                                     # back to the code
    # G  back to the keys; his eyes go to the screen and the left hand comes down again in frame 0
    t.burst('r', [126], 'look_d')
    t.hold(230, 'look_d')
    t.burst('l', [120], 'look_r')
    t.hold(80, 'look_r')
    return t


# =====================================================================================================
# Screen model: the text is cut into lines by the loop's own Enter keystrokes (cyclic, seamless)
# =====================================================================================================
def _line_lengths(events):
    """Lengths of the lines between Enters (cyclic). Line 0 is the one in progress at t=0: it was
    started after the loop's last Enter (`carry` characters typed before the loop wraps)."""
    last = max(i for i, e in enumerate(events) if e == 'enter')
    carry = len(events) - 1 - last
    lengths, cur = [], carry
    for e in events:
        if e == 'enter':
            lengths.append(cur)
            cur = 0
        else:
            cur += 1
    return lengths, carry


def _code_line(i, length):
    """A code-looking line of exactly `length` characters (syntax-coloured tokens, single spaces)."""
    assert length <= _SCR_W, 'a line of %d characters does not fit the %d-cell screen' % (length, _SCR_W)
    bank = _CODE.get(length) or [_SYNTAX[i % len(_SYNTAX)] * length]
    return bank[i % len(bank)]


# =====================================================================================================
# Layer frames
# =====================================================================================================
def _scene():
    """Everything that never moves, in one static layer under the rest: monitor, books, desk, keyboard
    and his headphones (his head never moves in this loop, so they can never drift off)."""
    f = Frame()
    _paint(f, _MONITOR, _MON_X, _MON_Y)
    _paint(f, _BOOKS, _BOOKS_X, _BOOKS_Y)
    _paint(f, _DESK, 1, 18)
    _paint(f, _KEYBOARD, _KB_X, _KB_Y)
    wear(f, _PHONES, clawd())
    return f


def _body(s, hidden, typed):
    """Clawd + what his keystrokes light up + the mug while it is in his hand (attached to him, so it
    lives in his layer and can never lag behind his arm). The desk/keyboard and the headphones cover
    some of his cells in every frame, so those cells are removed from Clawd here (same picture, smaller
    SVG); the mug is drawn after that, in front of his face and his headphone cup."""
    f = Frame()
    p = clawd(eyes=s['eyes'], larm=s['larm'], rarm=s['rarm'])          # normal body only (STYLE 0)
    put_clawd(f, p)
    for c in hidden:
        f.px.pop(c, None)
    for (x, y) in s['lit'] + (_CLICK if s['click'] else ()):
        f.put(x, y, _TYPED)
    x0, txt = typed
    for i, ch in enumerate(txt):
        if ch != '.':
            f.put(x0 + i, _LINE_Y[-1], _TYPED)
    if s['mug'] == 'face':
        f.place(_MUG_FACE, *_FACE_AT)
    elif s['mug'] == 'swing':
        f.place(_MUG_SWING, *_SWING_AT)
    elif s['mug'] == 'lift':
        f.place(_MUG, *_MUG_AT['lift'])
    return f


def _screen(committed):
    f = Frame()
    for y, x0, txt in committed:
        for i, ch in enumerate(txt):
            if ch != '.':
                f.put(x0 + i, y, ch)
    return f


def _ci(s):
    """The CI bar's part that is the same every loop: the fast start of the run, then green."""
    f = Frame()
    if s['ci'] in ('run', 'stall'):
        f.hline(_SCR_X, _SCR_X + _CI_START - 1, _BAR_Y, 'y')
    elif s['ci'] == 'ok':
        f.hline(_SCR_X, _SCR_X + _SCR_W - 1, _BAR_Y, 'g')
    return f


def _chunk_loop(segs, k):
    """Master loop k of the 3-loop 'chunk' layer: where the CI run stalls (_CI_STALL[k], drawn over the
    'ci' layer's fast start) and that loop's reward. A reward beat of None keeps the stalled bar up,
    covering the green: on that loop the bar turns green in the instant the reward pops."""
    out = []
    bar = Frame().hline(_SCR_X, _SCR_X + _SCR_W - 1, _BAR_Y, 'b')       # the status bar's own blue:
    bar.hline(_SCR_X, _SCR_X + _CI_STALL[k] - 1, _BAR_Y, 'y')            # masks the green under it
    for ms, s in segs:
        f = Frame()
        if s['ci'] == 'stall':
            f = bar
        elif s['cel'] is not None:
            beat = _REWARDS[k][s['cel']]
            if beat is None:
                f = bar
            else:
                for spr, x, y in beat:
                    f.place(spr, x, y)
        out.append((f, ms))
    return out


def _mug(s):
    """The mug while it stands on the books (or hops when he slams Enter). In his hand it is drawn
    with him, in the body layer."""
    f = Frame()
    if s['mug'] in _MUG_AT and s['mug'] != 'lift':
        f.place(_MUG, *_MUG_AT[s['mug']])
    return f


def _duck(s, k):
    f = Frame()
    d = _CEL[s['cel']][3] if (k == _DUCK_LOOP and s['cel'] is not None) else 0
    if d == 'sq':
        _paint(f, _DUCK_SQ, _DUCK_X, _DUCK_Y + 1)
    else:
        _paint(f, _DUCK, _DUCK_X, _DUCK_Y - d)
    return f


def _steam(total, away):
    """Steam puffs, _PUFFS_PER_LOOP per master loop, each followed by a pause. The cycle divides the
    master loop exactly, so the pause always falls on `away` (the window when the cup is off the
    books): the steam never hangs in the air without its cup. Frame 0 shows a full wisp."""
    period = total // _PUFFS_PER_LOOP
    assert period * _PUFFS_PER_LOOP == total, 'master loop %d ms is not a multiple of %d' % (total, _PUFFS_PER_LOOP)
    gap = period - sum(_PUFF_MS)
    a, b = away
    for first in (3, 2, 4, 1, 5, 0):           # which puff frame frame 0 shows (fullest wisps first)
        gap_start = sum(_PUFF_MS[first:])      # where the pause starts in every cycle
        if (a - gap_start) % period + (b - a) <= gap:
            break
    else:
        raise ValueError('no steam phase puts the pause on the sip window %d..%d (period %d)' % (a, b, period))
    order = list(range(first, len(_PUFF))) + [None] + list(range(first))
    durs = [(_PUFF_MS[i] if i is not None else gap) for i in order]
    frames = []
    for i, ms in zip(order, durs):
        f = Frame()
        if i is not None:
            for (x, y) in _PUFF[i]:
                f.put(x, y, 'm')
        frames.append((f, ms))
    return frames


# =====================================================================================================
def build():
    t = _timeline()
    lengths, carry = _line_lengths(t.events)
    n = len(lengths)
    lines = [_code_line(i, L_) for i, L_ in enumerate(lengths)]
    indent = [min(_INDENT[i % len(_INDENT)], _SCR_W - len(lines[i])) for i in range(n)]
    scene = _scene()
    hidden = set(scene.px)
    led = [(Frame().put(_LED[0], _LED[1], 'o') if on else Frame(), ms) for on, ms in _LED_BLIPS]
    body, screen, mug, ci = [], [], [], []
    clock, away = 0, None
    for ms, s in t.segs:
        li, typed = 0, carry                  # replay the keystrokes up to this beat
        for e in t.events[:s['keys']]:
            if e == 'enter':
                li, typed = li + 1, 0
            else:
                typed += 1
        cur = li % n
        committed = [(_LINE_Y[slot], _SCR_X + indent[k % n], lines[k % n])
                     for slot, k in enumerate(range(li - 2, li))]
        body.append((_body(s, hidden, (_SCR_X + indent[cur], lines[cur][:typed])), ms))
        screen.append((_screen(committed), ms))
        mug.append((_mug(s), ms))
        ci.append((_ci(s), ms))
        if s['mug'] not in ('rest', 'jolt'):  # cup off the books: the steam must pause
            away = (away[0] if away else clock, clock + ms)
        clock += ms
    # The CI run + reward ('chunk') and the duck last exactly _LOOPS master loops (so they never drift):
    # a different reward each loop, the CI bar stalls somewhere else each time, the duck hops on one.
    chunk, duck = [], []
    for k in range(_LOOPS):
        chunk += _chunk_loop(t.segs, k)
        for ms, s in t.segs:
            duck.append((_duck(s, k), ms))
    return anim(NAME, DESC, [
        static('scene', scene),
        layer('led', led),
        layer('steam', _steam(clock, away)),
        layer('screen', screen),
        layer('ci', ci),
        layer('duck', duck),
        layer('body', body),
        layer('mug', mug),
        layer('chunk', chunk),
    ], state=STATE)
