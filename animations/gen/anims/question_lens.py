"""question-lens - Question variant: Clawd studies a little bouncing "?" with a magnifying glass.   Preview:  python3 gen/preview.py anim question-lens

Clawd the curious sleuth: a small blue "?" (his question, with a mind of its own) stands on the input box
beside him and he peers at it through a magnifying glass (library 'magnifier').  It hops onto his head, off
to his left and back over him; he follows it with his eyes and his lens, then turns to you: so, what's the
answer?  Then he waits, patient and polite.

Storyboard (one loop = 11400 ms; every layer is cut from the same beat list, story())
     0  frame 0 (the reduced-motion still): at HOME, the magnifier held out over the little "?" standing on
        the input box at his right, his eyes on it (half-step right).  It wiggles (900), he blinks (1540).
  1970  it crouches ... and HOPS up past the lens onto his head (2090-2490: stretched at take-off and
        landing, round over the top; his eyes follow it up); it lands with a squash and he blinks as he
        feels it (2490).  He lifts the lens up beside his head and peers up at it (2720); it wiggles; a
        blink (3750).
  4110  it crouches and hops off to his left (his eyes lead it there, the lens comes down), landing with a
        squash and a little puff of dust (4630).  He watches it (look_l); a blink (5280).
  5910  it crouches and bounces back over his head in a big arc (6030-6625), his eyes following it left,
        up and right, and lands where it started, under his lens, with a puff and a wobble.
  7200  he looks up from it at YOU, eyes wide: "hm? what do you say?" ... then patient, eyes open on you:
        a blink (8600); the "?" gives a polite little bounce (9500), he glances down at it and back to you
        (10050); a slow blink (10600); and back to studying it (11080) ... frame 0.
Eye closures: 1.54, 2.49 (the landing), 3.75, 5.28, 8.60, 10.60 s: uneven on purpose.

Face: the fine-line kit only (fine() + fine_face(): open, half, line, look_l, look_r, look_u, wide).  No
mouth, no blush, his body never changes size or leaves HOME (the "?" squashes and stretches, he never does):
only his arm, eyes and the props act.
Two-theme rule: the "?" is blue 'b' with a navy 'B' shade and a cyan 'c' highlight; the magnifier is the
library's gold-rimmed lens on a wood handle; the dust is tan 't': mid-tones on #1E1E1E and on #FFFFFF.
Layers (back to front): trunk (static: Clawd without his right arm, plain face) | qmark (the "?", behind the
lens so it hops up past the glass) | lens (his right arm + the magnifier) | face (FINE: only his eye
pixels) | dust.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'question-lens'
STATE = 'question (variant)'
DESC = ('Studies a little bouncing "?" through a magnifying glass as it hops onto his head, off to his left and '
        'back over him, then looks up at you, curious, and waits for your answer.')

LOOP = 11400
HX, HY = HOME

# ---------------------------------------------------------------------------------------------
# The little "?" (local: 5 x 6, the library 'question' glyph one stem row shorter).  Blue with a cyan
# highlight on the top-left of the hook and a navy shade on the right.  Anchor = the left cell of its dot
# (it stands on that cell).  'squash' (landing / crouch) loses the hook's lower right row, 'stretch' (in
# the air) has one more stem row, 'lean_r' / 'lean_l' tip the hook a cell (a curious wiggle).
# ---------------------------------------------------------------------------------------------
_Q = {
    'stand':   ['.cbb.',
                'cb.bB',
                '...bB',
                '..bB.',
                '.....',
                '..bB.'],
    'squash':  ['.cbb.',
                'cb.bB',
                '..bB.',
                '.....',
                '..bB.'],
    'stretch': ['.cbb.',
                'cb.bB',
                '...bB',
                '..bB.',
                '..bB.',
                '.....',
                '..bB.'],
    'lean_r':  ['..cbb.',
                '.cb.bB',
                '...bB.',
                '..bB..',
                '......',
                '..bB..'],
    'lean_l':  ['cbb..',
                'b.bB.',
                '..bB.',
                '..bB.',
                '.....',
                '..bB.'],
}
QM = {k: Sprite(r, anchor=(2, len(r) - 1), name='qmark_' + k) for k, r in _Q.items()}

# perches (where its dot rests)
PERCH = {
    'A': (25, GROUND),        # on the input box at his right, under the lens (glyph x 23-27, rows 14-19)
    'B': (15, HY - 1),        # on his head (glyph x 13-17, rows 6-11)
    'C': (5, GROUND),         # on the input box at his left (glyph x 3-7)
}

DUST = Sprite(['t...t'], anchor=(2, 0), name='hop_dust')     # a tiny puff either side of its dot


def hop(a, b, apex, n):
    """Positions of its dot along a parabola from perch a to perch b, peaking at row `apex`
    (n in-between positions, both ends excluded)."""
    (x0, y0), (x1, y1) = PERCH[a], PERCH[b]
    # y(t) = A t^2 + B t + y0 with y(1) = y1 and min y = apex
    pts = []
    best = None
    for k in range(1, 200):                   # find the peak time tp for which the parabola fits
        tp = k / 200.0
        A = (y0 - apex) / (tp * tp)
        Bc = -2 * A * tp
        if abs(A + Bc + y0 - y1) < 0.5 and (best is None or abs(A + Bc + y0 - y1) < best[0]):
            best = (abs(A + Bc + y0 - y1), A, Bc)
    _, A, Bc = best
    for i in range(1, n + 1):
        t = i / (n + 1.0)
        pts.append((int(round(lerp(x0, x1, t))), int(round(A * t * t + Bc * t + y0))))
    return pts


# ---------------------------------------------------------------------------------------------
# Clawd
# ---------------------------------------------------------------------------------------------
MAG = get('magnifier')                       # gold rim, glass with a glint, wood handle = grip


def _pose(rarm):
    return clawd(eyes='blink', rarm=rarm)


_P_NONE = _pose('none')


def trunk():
    """Static: Clawd's body, legs and left arm, plain face (the face layer draws his eyes)."""
    f = Frame()
    put_clawd(f, _P_NONE)
    return f


_TRUNK = trunk()


def lens(s):
    """His right arm (the whole pose minus the trunk) + the magnifier in his claw."""
    p = _pose(s['rarm'])
    whole = Frame()
    put_clawd(whole, p)
    f = Frame({k: v for k, v in whole.px.items() if k not in _TRUNK.px})
    wear(f, MAG, p)
    return f


def face(s):
    """FINE layer: only the half-size eye pixels (his face under them is plain orange in the trunk)."""
    f = Frame()
    put_clawd(f, _P_NONE)
    base = fine(f)
    ff = fine_face(base.copy(), _P_NONE, HX, HY, s['face'])
    out = Frame(res=2)
    for q, v in ff.px.items():
        if base.px.get(q) != v:
            out.px[q] = v
    out.meta = {'fine_face': [s['face']]}
    return out


def qmark(s):
    f = Frame()
    shape, (x, y) = s['q']
    f.place(QM[shape], x, y)
    return f


def dust(s):
    f = Frame()
    if s['dust']:
        f.place(DUST, *s['dust'])
    return f


# ---------------------------------------------------------------------------------------------
# The story
# ---------------------------------------------------------------------------------------------
def story():
    S = []
    st = dict(rarm='side', face='look_r', q=('stand', PERCH['A']), dust=None)

    def b(ms, **kw):
        kw.setdefault('dust', None)
        st.update(kw)
        S.append((ms, dict(st)))

    def blink(after, eyes=None, lid=90):
        eyes = eyes or st['face']
        b(70, face='half')
        b(lid, face='line')
        b(70, face='half')
        b(after, face=eyes)

    def jump(a, c, apex, n, ms, faces=None, rarm_at=None):
        """crouch (squash, 120 ms) -> n in-air frames of `ms` each (stretched near take-off and landing,
        round over the top) -> the caller lands it (squash)."""
        b(120, q=('squash', PERCH[a]))
        for i, pos in enumerate(hop(a, c, apex, n)):
            kw = {}
            if faces and i in faces:
                kw['face'] = faces[i]
            if rarm_at is not None and i == rarm_at[0]:
                kw['rarm'] = rarm_at[1]
            shape = 'stretch' if i == 0 or i == n - 1 else 'stand'
            b(ms, q=(shape, pos), **kw)

    # ---- frame 0: studying the "?" through his lens ----------------------------------------------------
    b(900)
    b(120, q=('lean_r', PERCH['A']))          # it wiggles (900)
    b(120, q=('lean_l', PERCH['A']))
    b(400, q=('stand', PERCH['A']))
    blink(200)                                # 1540
    # ---- hop onto his head --------------------------------------------------------------------------
    jump('A', 'B', 7, 5, 80, faces={2: 'look_u'})          # 1970: crouch; 2090 up it goes, behind the lens
    b(90, q=('squash', PERCH['B']), face='half')          # 2490: lands on his head; he feels it
    b(70, q=('stand', PERCH['B']), face='line')
    b(70, face='half')
    b(500, face='look_u', rarm='up')          # 2720: lifts the lens beside his head, peers up at it
    b(110, q=('lean_l', PERCH['B']))          # it wiggles (3220)
    b(110, q=('lean_r', PERCH['B']))
    b(310, q=('stand', PERCH['B']))
    blink(130, 'look_u')                      # 3750
    # ---- hop off to his left -------------------------------------------------------------------------
    jump('B', 'C', 7, 5, 80, faces={0: 'look_l'}, rarm_at=(1, 'side'))   # 4110: his eyes lead, the lens comes down
    b(90, q=('squash', PERCH['C']), dust=PERCH['C'])      # 4630: lands, a little puff
    b(560, q=('stand', PERCH['C']))
    blink(400, 'look_l')                      # 5280
    # ---- bounce back over his head ---------------------------------------------------------------------
    jump('C', 'A', 7, 7, 85, faces={2: 'look_u', 5: 'look_r'})   # 5910 crouch, 6030 up and over
    b(90, q=('squash', PERCH['A']), dust=PERCH['A'])      # 6625: lands under his lens, a puff ...
    b(110, q=('lean_r', PERCH['A']))          # ... and a wobble
    b(110, q=('lean_l', PERCH['A']))
    b(265, q=('stand', PERCH['A']))
    # ---- he looks up from it at you: so? ------------------------------------------------------------
    b(500, face='wide')                       # 7200: hm? what do you say?
    b(900, face='open')
    blink(670, 'open')                        # 8600
    b(100, q=('squash', PERCH['A']))          # 9500: the "?" gives a polite little bounce ...
    b(120, q=('stand', (PERCH['A'][0], GROUND - 1)), face='look_r')   # ... he glances down at it ...
    b(80, q=('squash', PERCH['A']))
    b(250, q=('stand', PERCH['A']))
    b(550, face='open')                       # ... and back to you (10050)
    blink(180, 'open', lid=160)               # a slow blink (10600)
    b(320, face='look_r')                     # 11080: back to studying it ... frame 0
    return S


def build():
    S = story()
    total = sum(ms for ms, _ in S)
    assert total == LOOP, total
    return anim(NAME, DESC, [
        static('trunk', _TRUNK),
        layer('qmark', [(qmark(s), ms) for ms, s in S]),     # behind the lens: it hops up past the glass
        layer('lens', [(lens(s), ms) for ms, s in S]),
        layer('face', [(face(s), ms) for ms, s in S]),
        layer('dust', [(dust(s), ms) for ms, s in S]),
    ], state=STATE)
