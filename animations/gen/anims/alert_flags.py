"""alert-flags - Alert variant: Clawd signals you with two little semaphore flags.   Preview:  python3 gen/preview.py anim alert-flags

Clawd as a friendly flag signaller: a little red-and-yellow semaphore flag on a short wooden stick in each
claw.  He wig-wags them (one flag up while the other goes down, never both up: no big arms-up stretch),
then lowers them and waits for your OK, with a polite one-flag "ahem" now and then.

Storyboard (one loop = 8000 ms; every layer is cut from the same beat list, story())
     0  SIGNAL (frame 0, the reduced-motion still): at HOME, right flag up, left flag down: the classic
        semaphore stance, SPARKLE eyes on you.
     0-1610  wig-wag: the flags swap four times (240 ms holds, 70 ms in-betweens: about 1.6 swaps a
        second).  On every in-between both sticks are level and each cloth trails behind its swing (above
        the stick when it sweeps down, below when it sweeps up); on arrival each cloth flutters once.
  1610  he holds the stance a beat (the flags flutter), then lowers both flags to rest low beside him
        (2070), eyes open on you.
  2190  patient wait, flags at rest: a blink (2900), a breath of wind ripples both cloths (3330), and he
        glances at the right flag (4150) ...
  4600  ... a polite "ahem": it pops up (his eyes back on you, wide), flutters twice and comes back down
        (5560).
  5750  waiting again: a slow blink (6200), a glance up at the chat where the prompt is (6700), back to
        you (7250) as the wind ripples the cloths again.
  7600  wind-up: eyes wide, the right flag swings up through level ... into frame 0's stance.
Eye closures: 2.90 s, 6.20 s (a slow one): uneven on purpose.

Face: the fine-line kit only (fine() + fine_face(): open, half, line, look_r, look_u, wide, sparkle).  No
mouth, no blush, his body never changes size or leaves HOME: only his arms, eyes and the flags act.  His
arms are the kit's 'wave' (flag up) and 'out' (level) cells, plus one hand-drawn arm at normal cell size
angled down and out (flag lowered).
Two-theme rule: the cloths are red 'r' and gold 'j' (split on the diagonal, gold at the stick), the sticks
wood 'T': mid-tones on #1E1E1E and on #FFFFFF.
Layers (back to front): trunk (static: Clawd without arms, plain face) | flags (both arms, sticks and
cloths) | face (FINE: only his eye pixels).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401

NAME = 'alert-flags'
STATE = 'alert (variant)'
DESC = ('Waves two little red-and-yellow semaphore flags to catch your eye, one up and one down, then lowers '
        'them and waits for your OK with his eyes on you, giving one flag a polite little wave now and then.')

LOOP = 8000
HX, HY = HOME
MIRROR = 2 * HX + 10                # x -> MIRROR - x mirrors around his center column (15)


def _cells(rows, x0, y0):
    out = {}
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                out[(x0 + i, y0 + j)] = ch
    return out


def _merge(*ds):
    out = {}
    for d in ds:
        out.update(d)
    return out


# ---------------------------------------------------------------------------------------------
# The flags (local).  Right-hand poses: (arm cells, stick + cloth cells).  The left hand is the mirror
# image.  The cloth is a 3 x 3 square split on its diagonal: gold on the stick's side, red on the fly side.
#   up      arm raised out ('wave' cells), stick carrying on up the diagonal, cloth flying above its tip
#   lvl_hi  arm level ('out'), stick level, cloth trailing ABOVE the tip (it is sweeping down)
#   lvl_lo  arm level, cloth trailing BELOW the tip (it is sweeping up)
#   down    arm angled down and out (a hand-drawn arm at normal cell size: (20,14) (21,15)), stick on down
#           the diagonal, cloth hanging from its tip just above the input box
# '_f' = the same with the cloth fluttering (its fly edge rippling out a cell).
# ---------------------------------------------------------------------------------------------
_ARM = {
    'up': [(20, 14), (21, 13), (22, 12)],
    'lvl': [(20, 14), (21, 14)],
    'down': [(20, 14), (21, 15)],
}
_STICK = {
    'up': {(23, 11): 'T', (24, 10): 'T'},
    'lvl': {(22, 14): 'T', (23, 14): 'T'},
    'down': {(22, 16): 'T', (23, 17): 'T'},
}
_CLOTH_UP = ['rrr', 'jrr', 'jjr']        # attached at its bottom-left corner
_CLOTH_UP_F = ['rr.', 'jrrr', 'jjr']
_CLOTH_DN = ['jjr', 'jrr', 'rrr']        # attached at its top-left corner
_CLOTH_DN_F = ['jjr', 'jrrr', 'rr.']
FLAG = {
    'up':       (_ARM['up'], _merge(_STICK['up'], _cells(_CLOTH_UP, 25, 7))),
    'up_f':     (_ARM['up'], _merge(_STICK['up'], _cells(_CLOTH_UP_F, 25, 7))),
    'lvl_hi':   (_ARM['lvl'], _merge(_STICK['lvl'], _cells(_CLOTH_UP, 24, 12))),
    'lvl_lo':   (_ARM['lvl'], _merge(_STICK['lvl'], _cells(_CLOTH_DN, 24, 14))),
    'down':     (_ARM['down'], _merge(_STICK['down'], _cells(_CLOTH_DN, 24, 17))),
    'down_f':   (_ARM['down'], _merge(_STICK['down'], _cells(_CLOTH_DN_F, 24, 17))),
}


# ---------------------------------------------------------------------------------------------
# Clawd
# ---------------------------------------------------------------------------------------------
_P = clawd(eyes='blink', larm='none', rarm='none')


def trunk():
    """Static: Clawd's body and legs with a plain face (the face layer draws his eyes), no arms."""
    f = Frame()
    put_clawd(f, _P)
    return f


def flags(s):
    """Both arms with their flags: the right one as drawn, the left one mirrored."""
    f = Frame()
    for side in ('r', 'l'):
        arm, flag = FLAG[s[side]]
        for x, y in arm:
            f.put(x if side == 'r' else MIRROR - x, y, '#')
        for (x, y), ch in flag.items():
            f.put(x if side == 'r' else MIRROR - x, y, ch)
    return f


def face(s):
    """FINE layer: only the half-size eye pixels (his face under them is plain orange in the trunk)."""
    f = Frame()
    put_clawd(f, _P)
    base = fine(f)
    expr = s['face']
    ff = fine_face(base.copy(), _P, HX, HY, expr)
    out = Frame(res=2)
    for q, v in ff.px.items():
        if base.px.get(q) != v:
            out.px[q] = v
    out.meta = {'fine_face': [expr]}
    return out


# ---------------------------------------------------------------------------------------------
# The story
# ---------------------------------------------------------------------------------------------
def story():
    S = []
    st = dict(r='up', l='down', face='sparkle')

    def b(ms, **kw):
        st.update(kw)
        S.append((ms, dict(st)))

    def swap(to_r_up, face=None):
        """One wig-wag swap: both sticks level, each cloth trailing its swing (70 ms), then the new
        stance, each cloth fluttering on arrival (110 ms) and settling (130 ms)."""
        kw = {'face': face} if face else {}
        if to_r_up:
            b(70, r='lvl_lo', l='lvl_hi', **kw)
            b(110, r='up_f', l='down_f')
            b(130, r='up', l='down')
        else:
            b(70, r='lvl_hi', l='lvl_lo', **kw)
            b(110, r='down_f', l='up_f')
            b(130, r='down', l='up')

    # ---- SIGNAL + wig-wag (frame 0 = the stance) -------------------------------------------------
    b(370)                                    # frame 0: right flag up, left flag down
    swap(False)
    swap(True)
    swap(False)
    swap(True)
    # ---- holds the stance a beat, the flags flutter, then lowers them ----------------------------
    b(120, r='up_f', l='down_f')              # 1610
    b(150, r='up', l='down')
    b(120, r='up_f', l='down_f')
    b(70, r='up', l='down')
    b(70, r='lvl_hi', face='open')            # 2070: right flag comes down, eyes settle on you
    b(50, r='down')                           # (both at rest: the left one was already down)
    # ---- patient wait, flags at rest -------------------------------------------------------------
    b(710)                                    # 2190
    b(70, face='half')                        # blink (2900)
    b(100, face='line')
    b(70, face='half')
    b(190, face='open')
    b(120, r='down_f', l='down_f')            # a breath of wind: both cloths ripple (3330)
    b(510, r='down', l='down')
    b(190)
    b(450, face='look_r')                     # a glance at the right flag (4150) ...
    # ---- a polite "ahem": the right flag pops up --------------------------------------------------
    b(70, r='lvl_lo', face='wide')            # 4600
    b(110, r='up_f')
    b(200, r='up')
    b(110, r='up_f', face='open')
    b(200, r='up')
    b(110, r='up_f')
    b(160, r='up')
    b(70, r='lvl_hi')                         # ... and comes back down (5560)
    b(120, r='down')
    # ---- waiting again ---------------------------------------------------------------------------
    b(450)                                    # 5750
    b(90, face='half')                        # a slow blink (6200)
    b(160, face='line')
    b(90, face='half')
    b(160, face='open')
    b(550, face='look_u')                     # a glance up, where the prompt is (6700)
    b(120, face='open', r='down_f', l='down_f')   # back to you (7250); the wind ripples the cloths
    b(230, r='down', l='down')
    # ---- wind-up -> frame 0 ----------------------------------------------------------------------
    b(330, face='wide')                       # 7600: hey!
    b(70, r='lvl_lo', face='sparkle')         # the right flag swings up through level ... frame 0
    return S


def build():
    S = story()
    total = sum(ms for ms, _ in S)
    assert total == LOOP, total
    return anim(NAME, DESC, [
        static('trunk', trunk()),
        layer('flags', [(flags(s), ms) for ms, s in S]),
        layer('face', [(face(s), ms) for ms, s in S]),
    ], state=STATE)
