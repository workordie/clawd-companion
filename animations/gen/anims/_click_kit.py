"""Click-reaction kit (shared by _clicks_1.py, _clicks_2.py and _drag.py). Keep this API stable:
B, FX, TXT, compose, blink.

Click reactions (DRAFTS, not built yet: files starting with '_' are skipped by make.py).

You click Clawd, he reacts once, then the patch goes back to whatever was playing. Each reaction is a
one-shot that starts and ends at HOME in the plain standing pose, so it can cut in from (and back to)
any state. The patch picks one at random per click; `click-dizzy` is meant for rapid repeated clicks.

Every reaction is one fine layer (half-size face pixels) so body, face and effects never desync.
Timelines are written as tracks: the body track (pose + face) and effect tracks, each a list of
(ms, thing). compose() cuts them into frames wherever any track changes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

X0, Y0 = HOME


def B(ms, face='open', dx=0, dy=0, larm='side', rarm='side', legs='stand', right=None, turn=None):
    """One body beat: Clawd's pose, his box offset from HOME, and his fine-line face.
    turn: None (facing you), 'left' / 'right' (three-quarters, as when walking), 'back' (facing away:
    no eyes), 'gone' (not drawn: hidden by a poof)."""
    return (ms, dict(face=face, right=right, dx=dx, dy=dy, larm=larm, rarm=rarm, legs=legs, turn=turn))


def TXT(ms, s=None, x=0, y=0, ch='o'):
    """An effect beat drawing pixel text `s` (3x5 font) with its top-left at (x, y); s None = nothing."""
    return (ms, None if s is None else ('text:' + s, ch, x, y, False))


def FX(ms, name=None, i=0, x=0, y=0, flip=False):
    """One effect beat: library item `name` frame `i` with its anchor at (x, y); name None = nothing."""
    return (ms, None if name is None else (name, i, x, y, flip))


def _at(track, t):
    for ms, thing in track:
        if t < ms:
            return thing
        t -= ms
    return None


def _len(track):
    return sum(ms for ms, _ in track)


def compose(body, fx_tracks=(), behind=()):
    """body: list of B(...). fx_tracks: lists of FX(...) drawn over him; behind: drawn before him.
    The body track sets the length; effect tracks shorter than it show nothing afterwards."""
    total = _len(body)
    cuts = set([0, total])
    t = 0
    for ms, _ in body:
        t += ms
        cuts.add(t)
    # an effect change closer than 40 ms to another cut snaps to it (no sliver frames)
    extra = []
    for track in list(fx_tracks) + list(behind):
        t = 0
        for ms, _ in track:
            t += ms
            if t < total:
                extra.append(t)
    for t in sorted(extra):
        if all(abs(t - c) >= 40 for c in cuts):
            cuts.add(t)
    cuts = sorted(cuts)
    from anims._walk import standing
    frames = []
    for a, b in zip(cuts, cuts[1:]):
        st = _at(body, a)
        back = Frame()
        for track in behind:
            _draw_fx(back, _at(track, a) if a < _len(track) else None)
        ff = fine(back)
        turn = st['turn']
        if turn in ('left', 'right'):
            him = standing(turn, eyes=st['face'] if st['face'] in ('open', 'half', 'line') else 'open')
            him = him.shifted(2 * st['dx'], 2 * st['dy'])
        elif turn != 'gone':
            f = Frame()
            p = clawd(eyes='blink' if turn == 'back' else 'open', larm=st['larm'], rarm=st['rarm'], legs=st['legs'])
            put_clawd(f, p, X0 + st['dx'], Y0 + st['dy'])
            him = fine(f)
            if turn != 'back':
                fine_face(him, p, X0 + st['dx'], Y0 + st['dy'], st['face'], right=st['right'])
        else:
            him = None
        if him is not None:
            ff.px.update(him.px)
            ff.meta.update(him.meta)
        top = Frame()
        for track in fx_tracks:
            _draw_fx(top, _at(track, a) if a < _len(track) else None)
        ff.px.update(fine(top).px)
        frames.append((ff, b - a))
    return frames


def _draw_fx(f, thing):
    if thing is None:
        return
    name, i, x, y, flip = thing
    if name.startswith('text:'):
        f.text(name[5:], x, y, i)
        return
    f.place(get(name).sprite(i), x, y, flip=flip)


def blink(open_after=300, face='open'):
    """A smooth fine blink: half, line, half, then `face` held."""
    return [B(70, 'half'), B(90, 'line'), B(70, 'half'), B(open_after, face)]

