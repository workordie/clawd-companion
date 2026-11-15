"""Click reactions, set 1: hop, wave, hug, dizzy, hide, party.  Built through _clicks.py (the registry).
Each is a one-shot that starts and ends at HOME in the plain standing pose.

Local helpers (the kit's API stays frozen):
  _Seq      body track builder that remembers when beats start (to time effects to contacts)
  _track    an effect track from runs placed at absolute times
  _follow   an effect track that steps on the body's own cuts (long beats split into <= step ms), so
            effects that move with him (hearts, stars, confetti) add no sliver frames
  _confetti_path  one confetti piece: fired up and out, air drag, flutters down, slips behind the
                  input box
"""
import math
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims._click_kit import B, FX, TXT, compose, blink, X0, Y0  # noqa: E402,F401
from acc import get                          # noqa: E402


class _Seq:
    """Body track builder: add(B(...), ...) appends beats; mark(name) remembers the current time."""

    def __init__(self):
        self.beats, self.t, self.at = [], 0, {}

    def add(self, *beats):
        for b in beats:
            self.beats.append(b)
            self.t += b[0]
        return self

    def mark(self, name):
        self.at[name] = self.t
        return self.t

    def state(self, t):
        """The body beat's settings at time t (clamped to the track)."""
        for ms, st in self.beats:
            if t < ms:
                return st
            t -= ms
        return self.beats[-1][1]


def _track(*runs):
    """Effect track from (t_start, [FX/TXT beats]) runs at absolute times; gaps show nothing."""
    out, t = [], 0
    for t0, beats in sorted(runs, key=lambda r: r[0]):
        if t0 < t:
            raise ValueError('effect run at %d ms overlaps the previous one (busy until %d ms)' % (t0, t))
        if t0 > t:
            out.append(FX(t0 - t))
        out.extend(beats)
        t = t0 + sum(b[0] for b in beats)
    return out


def _segments(seq, t0, t1, step):
    """[(start, ms)] covering [t0, t1): cut where the body cuts; longer beats split evenly (<= step)."""
    cuts, t = set([t0, t1]), 0
    for ms, _ in seq.beats:
        t += ms
        if t0 < t < t1:
            cuts.add(t)
    cuts = sorted(cuts)
    out = []
    for a, b in zip(cuts, cuts[1:]):
        n = max(1, int(math.ceil((b - a) / float(step))))
        for i in range(n):
            s0, s1 = a + (b - a) * i // n, a + (b - a) * (i + 1) // n
            out.append((s0, s1 - s0))
    return out


def _follow(seq, t0, t1, fn, step=100):
    """Effect track sampled on the body's cuts: fn(t, k) -> (name, frame, x, y) or None, for the
    k-th segment starting at t."""
    out = [FX(t0)] if t0 > 0 else []
    for k, (t, ms) in enumerate(_segments(seq, t0, t1, step)):
        thing = fn(t, k)
        out.append(FX(ms) if thing is None else FX(ms, *thing))
    return out


def _dust(x=15, y=18):
    """Landing dust: start it on the contact beat."""
    return [FX(80, 'dust_puff', 0, x, y), FX(100, 'dust_puff', 1, x, y), FX(130, 'dust_puff', 2, x, y)]


def _bang_small(ms, x, y):
    """A 1x5 red "!" centred on the big exclamation anchored at (x, y): its pop-in / pop-out in-between."""
    return TXT(ms, '!', x - 1, y - 2, 'r')


def _ease_io(u):
    u = min(1.0, max(0.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def _rows_below(item, i):
    """How many rows sprite `item` frame i reaches below its anchor."""
    spr = get(item).sprite(i)
    return max(cy for _, cy, _ in spr.cells) - spr.ay


# confetti pieces and their frame counts
_PIECES = {'confetti_a': 4, 'confetti_b': 4, 'confetti_c': 4, 'confetti_d': 2, 'confetti_e': 4, 'confetti_f': 4}


def _confetti_path(x, y, vx, vy, g=0.45, vmax=1.6, flutter=1.0, phase=0, drag=0.7):
    """Cells of one piece per step: shot up and out, air drag, then a capped flutter fall with a
    side-to-side drift. Ends once it has dropped below row 19 (behind the input box)."""
    fx, fy = float(x), float(y)
    pts, falling = [], 0
    while True:
        ix, iy = int(round(fx)), int(round(fy))
        if iy > GROUND or ix < 0 or ix >= W:
            return pts
        pts.append((ix, iy))
        sway = 0.0
        if vy > 0:
            falling += 1
            sway = flutter * math.sin(falling * 1.25 + phase)
        fx += vx + sway
        fy += vy
        vx *= drag
        vy = min(vy + g, vmax)


# --------------------------------------------------------------------------------------------
def hop():
    """Startled boop: he flinches, the red "!" pops in over his head, a 2-cell hop (legs push off
    long, tuck in the air, reach for the ground), a dust-puff landing with eyes squeezed shut, then he
    looks up at your cursor while the "!" pulses once and pops away."""
    s = _Seq()
    s.add(B(100))
    s.mark('flinch')
    s.add(B(70, 'wide', larm='up', rarm='up'))                             # flinch: eyes pop, arms jump
    s.mark('push')
    s.add(B(60, 'wide', dy=-1, larm='high', rarm='high', legs='long'))     # push-off: feet still down
    s.mark('air')
    s.add(B(70, 'wide', dy=-2, larm='high', rarm='high'))                  # airborne
    s.mark('hang')
    s.add(B(170, 'wide', dy=-2, larm='high', rarm='high', legs='short'))   # hang, legs tucked
    s.mark('fall')
    s.add(B(60, 'wide', dy=-1, larm='up', rarm='up'))                      # legs reach for the ground
    s.mark('land')
    s.add(B(90, 'line', larm='out', rarm='out'))                           # contact: squeeze
    s.add(B(90, 'line', larm='down', rarm='down'))                         # arms follow through
    s.add(B(80, 'half'))
    s.add(B(220, 'open'))
    s.mark('look')
    s.add(B(560, 'look_u'))                                                # ...who did that?
    s.add(B(90, 'open'))
    s.add(*blink(330))
    a = s.at
    bx = 15
    bang = _track(
        (a['flinch'], [_bang_small(70, bx, 5)]),                           # pops in...
        (a['push'], [FX(a['air'] - a['push'], 'exclamation', 1, bx, 5),     # ...overshoots with ticks
                     FX(a['hang'] - a['air'], 'exclamation', 1, bx, 4),     # follows him up, a beat late
                     FX(a['fall'] - a['hang'], 'exclamation', 0, bx, 3),
                     FX(a['land'] - a['fall'], 'exclamation', 0, bx, 3),
                     FX(90, 'exclamation', 0, bx, 4),
                     FX(a['look'] - a['land'] - 90, 'exclamation', 0, bx, 5),
                     FX(130, 'exclamation', 1, bx, 5),                      # one last pulse...
                     FX(200, 'exclamation', 0, bx, 5),
                     _bang_small(70, bx, 5),                                # ...and it pops away
                     FX(80, 'sparkle_small', 2, bx, 5), FX(70, 'sparkle_small', 0, bx, 5)]),
    )
    dust = _track((a['land'], _dust()))
    return compose(s.beats, [bang, dust])


def wave():
    """Friendly: he notices you, dips his arm, and waves back (a real swing: in, through, out, with
    holds at the ends); a heart pops from his waving hand and drifts up; his eyes follow it before it
    pops away."""
    s = _Seq()
    s.add(B(90))
    s.add(B(220, 'look_u'))                                               # notices you
    s.add(B(80, 'open', rarm='down'))                                     # the arm dips first
    s.add(B(60, 'open', rarm='up'))
    s.add(B(60, 'open', rarm='raise'))
    s.mark('hi')
    s.add(B(160, 'open', rarm='wave'))
    for arm, ms, face in [('raise', 60, 'open'), ('high', 130, 'open'), ('raise', 60, 'open'),
                          ('wave', 150, 'open'),
                          ('raise', 60, 'half'), ('high', 120, 'line'), ('raise', 60, 'half'),  # blinks mid-swing
                          ('wave', 170, 'open')]:
        s.add(B(ms, face, rarm=arm))                                     # in-betweens short, ends held
    s.add(B(70, 'open', rarm='raise'), B(60, 'open', rarm='up'))
    s.add(B(150, 'open'))
    s.mark('follow')
    s.add(B(220, 'look_u'))                                               # watches the heart go
    s.mark('pop')
    s.add(B(240, 'look_u'))
    s.add(B(120, 'open'))
    s.add(*blink(300))
    a = s.at
    hx, hy = 25, 9
    t_rise, t_pop = a['hi'] + 400, a['pop']
    path = [(25, 9), (25, 8), (26, 7), (26, 6), (25, 5), (24, 4), (24, 3)]   # drifts up, swaying

    def heart(t, k):
        if t < a['hi'] + 70:
            return ('heart_pop', 0, hx, hy)
        if t < a['hi'] + 160:
            return ('heart_pop', 1, hx, hy)
        if t < t_pop:
            u = _ease_io((t - t_rise) / float(t_pop - t_rise)) if t >= t_rise else 0.0
            x, y = path[int(round(u * (len(path) - 1)))]
            return ('heart', 0, x, y)
        x, y = path[-1]
        if t < t_pop + 50:
            return ('heart_pop', 0, x, y - 1)                              # pops away: tiny heart...
        if t < t_pop + 130:
            return ('sparkle_small', 0, x, y - 1)                          # ...a speck (one segment each)
        return None
    return compose(s.beats, [_follow(s, a['hi'], s.t, heart, step=90)])


def hug():
    """Aww: he opens his arms wide, wraps them round himself and squeezes, eyes shut; a heart pops
    above him with a heartbeat pulse, then drifts up, swaying a beat behind him, and pops away while
    he looks up at it."""
    s = _Seq()
    s.add(B(100))
    s.add(B(60, 'open', larm='up', rarm='up'))
    s.add(B(180, 'sparkle', larm='out', rarm='out'))                       # arms open wide...
    s.add(B(60, 'half'))
    s.mark('squeeze')
    s.add(B(90, 'half', larm='front', rarm='front'))                       # ...and wrap
    s.add(B(260, 'line', larm='front', rarm='front'))                      # squeeze
    for dx, ms in [(1, 300), (0, 130), (-1, 320), (0, 130), (1, 280), (0, 200)]:
        s.add(B(ms, 'line', dx=dx, larm='front', rarm='front'))            # sway, held at the ends
    s.mark('release')
    s.add(B(90, 'half'))
    s.add(B(180, 'open'))
    s.mark('pop')
    s.add(B(260, 'look_u'))                                                # watches the heart go
    s.add(B(240, 'open'))
    a = s.at
    S = a['squeeze']
    hx, hy = 15, 7
    t_rise = S + 550

    def heart(t, k):
        r = t - S
        if r < 90:
            return ('heart_pop', 0, hx, hy)
        if r < 170:
            return ('heart_pop', 1, hx, hy)                                # pops big...
        if r < 350:
            return ('heart_big', 0, hx, hy)
        if r < 450:
            return ('heart', 0, hx, hy)                                     # ...ba-dum
        if r < 550:
            return ('heart_big', 0, hx, hy)
        x = hx + s.state(t - 160)['dx']                                    # sways a beat behind him
        if t < a['pop']:
            u = _ease_io((t - t_rise) / float(a['pop'] - t_rise))
            return ('heart', 0, x, hy - int(round(4 * u)))
        if t < a['pop'] + 50:
            return ('heart_pop', 0, hx, hy - 5)                            # pops away: tiny heart...
        if t < a['pop'] + 130:
            return ('sparkle_small', 0, hx, hy - 5)                        # ...a speck (one segment each)
        return None
    return compose(s.beats, [_follow(s, S, s.t, heart, step=100)])


def dizzy():
    """For rapid clicks: bonk! An impact at his head knocks him a cell aside, the burst's sparks turn
    into stars circling his head while his eyes roll and he sways; he shakes it off, the stars fly away,
    and he gives your cursor a look."""
    s = _Seq()
    s.add(B(60))
    s.mark('bonk')
    s.add(B(50, 'wide'))                                                   # contact
    s.add(B(90, 'line', dx=-1, larm='out', rarm='out'))                    # knocked a cell aside
    s.add(B(90, 'line', dx=-1, larm='out', rarm='out'))
    s.mark('daze')
    roll = ['look_l', 'look_u', 'look_r', 'look_d']                        # eyes roll round
    for k, dx in enumerate([-1, -1, -1, 0, 1, 1, 1, 1, 0, -1]):
        s.add(B(130, roll[k % 4], dx=dx, larm='down', rarm='down'))
    s.add(B(220, 'half', dx=-1, larm='down', rarm='down'))                  # woozy...
    s.add(B(150, 'half', larm='down', rarm='down'))
    s.mark('shake')
    s.add(B(70, 'line', dx=1, larm='out', rarm='out'))                      # shake it off
    s.add(B(60, 'line', dx=-1, larm='out', rarm='out'))
    s.add(B(60, 'line', dx=1, larm='out', rarm='out'))
    s.add(B(80, 'line'))
    s.add(B(90, 'half'))
    s.add(B(220, 'open'))
    s.add(B(300, 'look_u'))                                                # ...hey.
    s.add(*blink(220))
    a = s.at
    bonk = _track((a['bonk'], [FX(50, 'impact_star', 0, 21, 11), FX(90, 'impact_star', 1, 23, 10),
                               FX(90, 'impact_star', 2, 23, 10)]))       # burst flies off his face

    def stars(t, k):
        return ('dizzy_stars', k % 4, 15 + s.state(t - 130)['dx'], 10)     # follows him a beat late
    orbit = _follow(s, a['daze'], a['shake'], stars, step=140)
    fly = []
    for (x, y, vx, vy) in [(10, 10, -2, -1), (15, 8, 0, -2), (21, 10, 2, -1)]:
        fly.append(_track((a['shake'], [FX(70, 'sparkle_small', 1, x, y),
                                        FX(60, 'sparkle_small', 2, x + vx, y + vy),
                                        FX(60, 'sparkle_small', 0, x + 2 * vx, y + 2 * vy)])))
    return compose(s.beats, [orbit, bonk] + fly)


def hide():
    """Peek-a-boo: he spots your cursor, eeps, and ducks behind the input box (never smaller: the box
    edge hides him). His head creeps back up, the eyes peek over the edge and look around, he finds
    you, dips, and pops out with a hop and a dust landing."""
    s = _Seq()
    s.add(B(100))
    s.add(B(160, 'look_u'))                                                # spots the cursor
    s.add(B(90, 'wide', larm='up', rarm='up'))                             # eep!
    s.add(B(60, 'line', dy=1, larm='high', rarm='high'))                   # duck: accelerating
    s.add(B(60, 'line', dy=3, larm='high', rarm='high', legs='none'))      # (legs hidden below the edge)
    s.mark('duck')
    s.add(B(60, 'line', dy=6, larm='high', rarm='high', legs='none'))
    s.add(B(340, turn='gone'))
    hold = dict(larm='up', rarm='up', legs='none')                         # hands on the ledge
    s.add(B(90, 'open', dy=7, **hold))                                     # head creeps up
    s.add(B(110, 'open', dy=6, **hold))
    s.add(B(110, 'look_u', dy=5, **hold))
    s.add(B(200, 'open', dy=4, **hold))                                    # peeking over the edge
    s.add(B(90, 'look_l', dy=4, **hold))                                   # glances lead, the head follows
    s.add(B(280, 'look_l', dx=-1, dy=4, **hold))
    s.add(B(80, 'open', dy=4, **hold))
    s.add(B(90, 'look_r', dy=4, **hold))
    s.add(B(300, 'look_r', dx=1, dy=4, **hold))
    s.add(B(80, 'look_u', dy=4, **hold))
    s.add(B(120, 'look_u', dy=4, **hold))                                  # there you are
    s.add(B(80, 'look_u', dy=5, **hold))                                   # dip
    s.add(B(60, 'wide', dy=2, larm='high', rarm='high', legs='none'))      # pop!
    s.add(B(60, 'wide', dy=-1, larm='high', rarm='high'))
    s.add(B(150, 'sparkle', dy=-2, larm='high', rarm='high', legs='short'))
    s.add(B(60, 'open', dy=-1, larm='up', rarm='up'))
    s.mark('land')
    s.add(B(90, 'line', larm='out', rarm='out'))
    s.add(B(90, 'line', larm='down', rarm='down'))
    s.add(B(80, 'half'))
    s.add(B(260, 'open'))
    a = s.at
    poof = _track((a['duck'], _dust()))
    dust = _track((a['land'], _dust()))
    return compose(s.beats, [dust, poof])


def party():
    """Yay: a wind-up, a big 3-cell jump with both arms high, a confetti fountain pops over his head,
    dust on the landing, sparkly eyes, ta-da arms; the confetti fans out, hangs, flutters down around
    (behind) him and slips out of view behind the input box while his eyes follow it."""
    s = _Seq()
    s.add(B(100))
    s.add(B(90, 'half', larm='down', rarm='down'))                         # wind-up (arms, never a crouch)
    s.add(B(200, 'line', larm='down', rarm='down'))
    s.add(B(60, 'sparkle', dy=-1, larm='up', rarm='up', legs='long'))       # push-off
    s.add(B(60, 'sparkle', dy=-2, larm='high', rarm='high'))
    s.mark('peak')
    s.add(B(240, 'sparkle', dy=-3, larm='high', rarm='high', legs='short'))
    s.add(B(80, 'sparkle', dy=-2, larm='high', rarm='high', legs='short'))
    s.add(B(60, 'sparkle', dy=-1, larm='high', rarm='high'))
    s.mark('land')
    s.add(B(90, 'line', larm='out', rarm='out'))
    s.add(B(70, 'half', larm='up', rarm='up'))
    s.add(B(260, 'sparkle', larm='high', rarm='high'))                       # ta-da
    s.add(B(240, 'look_u', larm='high', rarm='high'))                        # eyes follow the confetti
    s.add(B(80, 'look_u', larm='up', rarm='up'))
    s.add(B(220, 'look_l'))
    s.add(B(240, 'look_r'))
    s.add(B(220, 'look_d'))                                                  # ...as it slips away
    s.add(B(140, 'open'))
    s.add(*blink(280))
    a = s.at
    t_pop = a['peak']
    ex, ey = 15, 5
    pop = _track((t_pop, [FX(80, 'sparkle', 1, ex, ey), FX(80, 'sparkle', 2, ex, ey), FX(80, 'sparkle', 3, ex, ey)]))
    shots = [  # item, vx, vy, fall speed, flutter phase: a dome, the centre pieces highest
        ('confetti_a', -3.4, -0.6, 1.4, 0), ('confetti_b', 3.3, -0.7, 1.5, 2),
        ('confetti_c', -2.4, -1.2, 1.4, 1), ('confetti_d', 2.5, -1.1, 1.4, 3),
        ('confetti_e', -1.3, -1.6, 1.3, 2), ('confetti_f', 1.2, -1.6, 1.4, 0),
        ('confetti_b', -0.4, -1.75, 1.6, 3), ('confetti_a', 0.5, -1.7, 1.5, 1),
    ]
    segs = _segments(s, t_pop, s.t, 110)
    behind = []
    for n, (item, vx, vy, vmax, ph) in enumerate(shots):
        path = _confetti_path(ex, ey, vx, vy, vmax=vmax, phase=ph)
        spin = 1 if n % 2 else -1
        beats = []
        for k, (t, ms) in enumerate(segs):
            if k >= len(path):
                break
            x, y = path[k]
            i = (ph + spin * k) % _PIECES[item]
            if y + _rows_below(item, i) > GROUND:                         # at the edge: lie flat or go
                if _rows_below(item, 0) + y > GROUND:
                    break
                i = 0
            beats.append(FX(ms, item, i, x, y))
        behind.append(_track((t_pop, beats)))
    dust = _track((a['land'], _dust()))
    return compose(s.beats, [pop, dust], behind=behind)
