"""alert-bell - Alert variant: Clawd rings a little brass handbell for your OK.   Preview:  python3 gen/preview.py anim alert-bell

The town crier's "hear ye!", friendly version: Clawd holds a brass handbell up by its wooden handle in his
raised right claw (the kit's 'wave' arm with one more cell, so the bell hangs clear of him) and rings it;
gold ring-waves pulse out to the right on every "ding".  The ringing is brisk but short; then he simply
waits with the bell up and his eyes on you, with a polite "ding-ding" now and then.

Storyboard (one loop = 7200 ms; every layer is cut from the same beat list, story())
     0  DING (frame 0, the reduced-motion still): at HOME, the bell just struck and hanging straight in his
        raised claw, the first ring-wave popping out on its right, SPARKLE eyes on you, his free left arm
        out ("over here!").
     0-1440  ding-a-ling, four swings of 360 ms (< 3 Hz): the bell swings back left, through the middle and
        out to the right, where his arm flicks up a cell and the clapper strikes (260, 620, 980, 1340).
        Each wave travels out as the bell swings back (inner arc; inner + outer; the outer one alone; its
        tips) and is gone by the next strike.
  1440  it rings out: the last wave travels off as the bell comes to hang still; his left arm drops back to
        his side and his eyes settle on you (1560).
  1800  patient wait, bell up: a blink (2560); the dome catches the light (2900), he glances at it (2990)
        and back to you (3600).
  4300  a polite reminder: "ding-ding" (two strikes, wide eyes on the first), one wave.
  5100  waiting again: a slow blink (5700), a glance up at the chat where the permission prompt is (6150),
        back to you (6600).
  6860  wind-up: a half-lid, then the bell is drawn back, eyes wide, left arm out again (6960) ... his arm
        flicks and the clapper strikes (7100) ... frame 0's ding.
Eye closures: 2.56, 5.70 s (a slow one), plus the half-lid at the wind-up: uneven on purpose.

Face: the fine-line kit only (fine() + fine_face(): open, half, line, look_r, look_u, wide, sparkle).  No
mouth, no blush, his body never changes size or leaves HOME: only his arms, eyes and the bell act.
Two-theme rule: the bell is gold 'j' with a dark-gold 'J' shade and lip (the pale 'y' highlight and the
white gleam only inside the dome), the handle wood 'T', the clapper gray 'N'; the ring-waves are gold 'j'
cooling to orange 'o' as they travel: mid-tones that read on #1E1E1E and on #FFFFFF.
Layers (back to front): trunk (static: Clawd's body and legs, plain face) | larm (his free left arm) |
bell (his bell arm + the bell) | face (FINE: only his eye pixels) | shine (the dome's gleam) | fx (waves).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'alert-bell'
STATE = 'alert (variant)'
DESC = ('Rings a little brass handbell held up in his claw, gold ring-waves pulsing out with every ding, then '
        'waits with the bell up and his eyes on you, giving it a polite "ding-ding" now and then.')

LOOP = 7200
HX, HY = HOME

# ---------------------------------------------------------------------------------------------
# The handbell (local: the library has no handbell).  Wooden handle, brass bell lit from the top-left
# (pale highlight inside the dome only, dark-gold shade on the right and on the lip), gray clapper.
# Anchor = the top of the handle, which sits in his claw, just right of his raised hand (23, 11).
# Swings pivot on that point: 'r' = swung out to the right (the clapper strikes the right lip),
# 'l' = swung back to the left (the clapper on the left lip).  'c' hangs straight down.
# ---------------------------------------------------------------------------------------------
_BELL_ROWS = {
    'c': (['..T..',
           '..T..',
           '.yjJ.',
           '.jjJ.',
           'jjjjJ',
           'JJJJJ',
           '..N..'], (2, 0)),
    'r': (['..T...',
           '...T..',
           '..yjJ.',
           '..jjJ.',
           '.jjjjJ',
           '.JJJJJ',
           '.....N'], (2, 0)),
    'l': (['...T..',
           '..T...',
           '.yjJ..',
           '.jjJ..',
           'jjjjJ.',
           'JJJJJ.',
           'N.....'], (3, 0)),
}
BELL = {k: Sprite(r, anchor=a, name='handbell_' + k) for k, (r, a) in _BELL_ROWS.items()}
GRIP = {False: (24, 11), True: (24, 10)}     # the handle's top, in his claw: arm at rest / flicked up
# His bell arm: the kit's 'wave' with one more cell, reaching up and out so the bell hangs clear of him
# (box cells (10,2) (11,1) (12,0) (13,-1)); the same trick as alert's hand-drawn 'hi' arm.  On a strike
# the whole arm flicks up one cell (the wrist flick that swings the bell out).
EXTRA = (13, -1)

# Ring-waves: ')' arcs to the right of the hanging bell, centred on its body.  Each ding's wave pops out
# as the bell swings back from the strike: inner arc, then inner + outer, then the outer one alone, then
# just its tips.  They are drawn only while the bell hangs straight or swings left, so a wave never
# touches the bell swung out to the right.
_ARC_IN = [(27, 12), (28, 13), (28, 14), (28, 15), (28, 16), (27, 17)]
_ARC_OUT = [(29, 11), (30, 12), (30, 13), (30, 14), (30, 15), (30, 16), (29, 17)]
_ARC_OUT_FADE = [(29, 11), (29, 17)]                 # the outer arc thinning away: only its tips left
_WAVES = {
    None: [],
    'in': [(c, 'j') for c in _ARC_IN],
    'both': [(c, 'o') for c in _ARC_IN] + [(c, 'j') for c in _ARC_OUT],
    'out': [(c, 'o') for c in _ARC_OUT],
    'fade': [(c, 'o') for c in _ARC_OUT_FADE],
}
# The bell catches the light while it hangs still: a gleam at the top of its dome, inside the brass (so it
# never touches the background, where white would vanish on the light theme): pale, white, pale.
_SHINE = [
    {(24, 13): 'Y'},
    {(24, 13): 'W', (24, 14): 'Y'},
]


# ---------------------------------------------------------------------------------------------
# Clawd
# ---------------------------------------------------------------------------------------------
def _pose(larm):
    p = clawd(eyes='blink', larm=larm, rarm='wave')
    cells = list(p.sprite.cells) + [(EXTRA[0], EXTRA[1], '#')]
    return Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors, dict(p.spec, rarm='wave+1'))


def trunk():
    """Static: Clawd's body and legs with a plain face (the face layer draws his eyes); no arms."""
    f = Frame()
    put_clawd(f, clawd(eyes='blink', larm='none', rarm='none'))
    return f


_TRUNK = trunk()


def _arm_cells(larm):
    """The cells his pose adds to the trunk (drawn whole with put_clawd, minus the trunk)."""
    whole = Frame()
    put_clawd(whole, _pose(larm))
    return {k: v for k, v in whole.px.items() if k not in _TRUNK.px}


_LEFT = {k: {c: v for c, v in _arm_cells(k).items() if c[0] < HX + 5} for k in ('out', 'side')}
_RIGHT = {c: v for c, v in _arm_cells('side').items() if c[0] > HX + 5}


def larm(s):
    """His free left arm."""
    return Frame(_LEFT[s['larm']])


def bell(s):
    """His bell arm (flicked up a cell on a strike) + the bell hanging from his claw."""
    lift = s['lift']
    f = Frame({(x, y - lift): v for (x, y), v in _RIGHT.items()})
    f.place(BELL[s['bell']], *GRIP[bool(lift)])
    return f


_FACE_POSE = _pose('side')


def face(s):
    """FINE layer: only the half-size eye pixels (his face under them is plain orange in the trunk)."""
    f = Frame()
    put_clawd(f, _FACE_POSE)
    base = fine(f)
    expr = s['face']
    ff = fine_face(base.copy(), _FACE_POSE, HX, HY, expr)
    out = Frame(res=2)
    for q, v in ff.px.items():
        if base.px.get(q) != v:
            out.px[q] = v
    out.meta = {'fine_face': [expr]}
    return out


def fx(s):
    f = Frame()
    for (x, y), ch in _WAVES[s['wave']]:
        f.put(x, y, ch)
    return f


def shine(s):
    """The dome's shine, drawn over the bell (same beat list)."""
    f = Frame()
    if s['shine'] is not None:
        for (x, y), ch in _SHINE[s['shine']].items():
            f.put(x, y, ch)
    return f


# ---------------------------------------------------------------------------------------------
# The story
# ---------------------------------------------------------------------------------------------
def story():
    S = []
    st = dict(larm='out', bell='c', lift=0, face='sparkle', wave='in', shine=None)

    def b(ms, **kw):
        kw.setdefault('wave', None)
        kw.setdefault('shine', None)
        kw.setdefault('lift', 0)
        st.update(kw)
        S.append((ms, dict(st)))

    def ding():
        """One swing, starting just after a strike (360 ms, < 3 Hz): the wave pops out as the bell swings
        back through the middle, both arcs as it swings left, the outer one as it comes back, and the
        next strike out on the right, his arm flicking up (only the old wave's tips are left by then)."""
        b(80, bell='c', wave='in')
        b(120, bell='l', wave='both')
        b(60, bell='c', wave='out')
        b(100, bell='r', lift=1, wave='fade')

    # ---- DING-A-LING: frame 0 = just struck, the bell swinging back, the first wave out -------------
    for _ in range(4):
        ding()
    # ---- it rings out: the last wave travels off as the bell comes to hang still -------------------
    b(120, bell='c', wave='in')               # 1440
    b(100, wave='both', larm='side', face='open')   # left arm back down, eyes settle on you
    b(140, wave='out')
    # ---- patient wait, bell up ----------------------------------------------------------------
    b(760)                                    # 1800
    b(70, face='half')                        # blink (2560)
    b(100, face='line')
    b(70, face='half')
    b(100, face='open')
    b(90, shine=0)                            # the dome catches the light (2900) ...
    b(110, shine=1, face='look_r')            # ... he glances at it (2990) ...
    b(100, shine=0, face='look_r')
    b(400, face='look_r')
    b(700, face='open')                       # ... and back to you (3600)
    # ---- a polite reminder: ding-ding ----------------------------------------------------------
    b(100, bell='r', lift=1, face='wide')     # 4300: strike ...
    b(80, bell='c', wave='in')
    b(120, bell='l', wave='both', face='open')
    b(60, bell='c', wave='out')
    b(100, bell='r', lift=1, wave='fade')     # ... strike
    b(100, bell='c', wave='in')
    b(100, wave='both')
    b(140, wave='out')
    # ---- waiting again ---------------------------------------------------------------------------
    b(600)                                    # 5100
    b(90, face='half')                        # a slow blink (5700)
    b(160, face='line')
    b(90, face='half')
    b(110, face='open')
    b(450, face='look_u')                     # a glance up, where the prompt is (6150)
    b(260, face='open')                       # back to you (6600)
    # ---- wind-up -> strike -> frame 0 ----------------------------------------------------------
    b(100, face='half')                       # 6860: a half-lid as he gets ready ...
    b(140, bell='l', face='wide', larm='out')  # ... the bell drawn back, wide eyes: hey!
    b(100, bell='r', lift=1)                  # ... flick, DING (frame 0: the wave pops out)
    return S


def build():
    S = story()
    total = sum(ms for ms, _ in S)
    assert total == LOOP, total
    return anim(NAME, DESC, [
        static('trunk', _TRUNK),
        layer('larm', [(larm(s), ms) for ms, s in S]),
        layer('bell', [(bell(s), ms) for ms, s in S]),
        layer('face', [(face(s), ms) for ms, s in S]),
        layer('shine', [(shine(s), ms) for ms, s in S]),
        layer('fx', [(fx(s), ms) for ms, s in S]),
    ], state=STATE)
