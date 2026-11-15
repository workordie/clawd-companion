"""Click reactions, set 2: spin, giggle, shrug, idea, poof, groove.  Built through _clicks.py (the registry).
Each is a one-shot that starts and ends at HOME in the plain standing pose.

Effects never just vanish: text and props pop in along an eased path and leave by shrinking, fizzling
(checkered, then a few specks) or twinkling out. Local sprites (SPR beats) sit in the same effect tracks
as the kit's FX/TXT beats; comp() draws them (see its docstring)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402
from anims._click_kit import B, FX, TXT, compose, blink, X0, Y0  # noqa: E402,F401


# ------------------------------------------------------------------ local helpers
def SPR(ms, spr=None, x=0, y=0):
    """An effect beat drawing a local Sprite with its anchor at (x, y); spr None = nothing."""
    return (ms, None if spr is None else ('spr', spr, x, y, False))


def _tlen(track):
    return sum(ms for ms, _ in track)


def _tat(track, t):
    for ms, thing in track:
        if t < ms:
            return thing
        t -= ms
    return None


def _draw(f, thing):
    if thing is None:
        return
    if thing[0] == 'spr':
        f.place(thing[1], thing[2], thing[3])
        return
    name, i, x, y, flip = thing
    if name.startswith('text:'):
        f.text(name[5:], x, y, i)
    else:
        f.place(get(name).sprite(i), x, y, flip=flip)


def _fit(track, cuts, total):
    """Move each change of an effect track onto a frame cut when it falls within 40 ms of one (as
    compose() would), but never let a beat get squeezed out: it moves on to the next cut instead.
    `cuts` (a set) grows with the changes that become cuts of their own."""
    out, prev, t = [], 0, 0
    for ms, thing in track:
        t += ms
        b = t
        if b < total:
            near = min(cuts, key=lambda c: abs(c - b))
            if abs(near - b) < 40:
                b = near
            if b <= prev:
                b = min(c for c in cuts if c > prev)
            cuts.add(b)
        out.append((b - prev, thing))
        prev = b
    return out


def comp(body, front=(), behind=()):
    """compose() with tracks that may also hold SPR beats. Every effect change is first fitted to the
    frame cuts (_fit: no beat is lost to the kit's 40 ms snapping), the kit cuts the frames from blank
    copies of the tracks, and the effects are drawn here at each frame's start time: `behind` only
    where Clawd isn't, `front` on top."""
    total = _tlen(body)
    cuts, t = set([0, total]), 0
    for ms, _ in body:
        t += ms
        cuts.add(t)
    front = [_fit(tr, cuts, total) for tr in front]
    behind = [_fit(tr, cuts, total) for tr in behind]
    frames = compose(body, [[(ms, None) for ms, _ in tr] for tr in front + behind])
    out, t = [], 0
    for ff, ms in frames:
        back, top = Frame(), Frame()
        for tr in behind:
            _draw(back, _tat(tr, t) if t < _tlen(tr) else None)
        for tr in front:
            _draw(top, _tat(tr, t) if t < _tlen(tr) else None)
        for k, c in fine(back).px.items():
            ff.px.setdefault(k, c)
        ff.px.update(fine(top).px)
        out.append((ff, ms))
        t += ms
    return out


def now(track):
    """Current length of a track being built (the start time of the next beat)."""
    return _tlen(track)


def after(t0, beats):
    """An effect track that waits t0 ms, then plays `beats`."""
    return ([(t0, None)] if t0 > 0 else []) + list(beats)


def cells(spec, ch, anchor=(0, 0)):
    """A sprite from (x, y) cells in one color."""
    return Sprite(cells=[(x, y, ch) for x, y in spec], anchor=anchor)


def text_sprite(s, ch):
    f = Frame()
    f.text(s, 0, 0, ch)
    return Sprite(cells=[(x, y, c) for (x, y), c in f.px.items()])


def checkered(spr, parity=0):
    """Every other pixel: a sprite fizzling out (or fading in) for one frame."""
    return Sprite(cells=[(x, y, c) for x, y, c in spr.cells if (x + y) % 2 == parity],
                  anchor=(spr.ax, spr.ay))


def twinkle(name, x, y, seq, ms):
    return [FX(m, name, i, x, y) for i, m in zip(seq, ms)]


# ------------------------------------------------------------------ spin
# Whoosh: short steel streaks on alternating sides of him (an orbit read at 3 px per cell), with a
# fading tail. Absolute cells: his box spans x 10-20, arms on x 10 and 20, body rows 12-17.
_WHOOSH = [
    cells([(22, 13), (23, 13), (24, 13), (26, 13), (6, 16), (7, 16), (8, 16), (4, 16)], 's'),
    cells([(22, 16), (23, 16), (24, 16), (26, 16), (6, 13), (7, 13), (8, 13), (4, 13)], 's'),
]
_WHOOSH_START = cells([(22, 13), (23, 13), (7, 16), (8, 16)], 's')     # first, slower turn: short
_WHOOSH_FADE = [
    cells([(23, 14), (24, 14), (6, 15), (7, 15)], 's'),     # it slows: shorter, closing in
    cells([(25, 13), (5, 16)], 's'),                         # last wisps drift off
]


def spin():
    """Twirl: the eyes lead, he spins round twice on the spot (front, three-quarters, back,
    three-quarters), slow-fast-slow with a whoosh trailing him, skids to a stop (eyes overshoot, a puff
    of dust), then a ta-da on tiptoe, arms out and a twinkle in his eyes, while two sparkles twinkle out."""
    body = [B(200),
            B(150, 'look_r', larm='down', rarm='down'),          # wind-up: eyes and arms counter the turn
            B(100, 'look_l'),                                   # the eyes lead the turn
            B(120, turn='left')]
    t_whoosh = now(body)
    fast = [B(90, turn='back'), B(80, turn='right'), B(70, 'look_l'),     # (facing us for a blink of time)
            B(60, turn='left'), B(60, turn='back'), B(70, turn='right')]
    body += fast
    t_stop = now(body)
    body += [B(180, 'look_l'),                                  # stop: the eyes overshoot
             B(130, 'open', larm='down', rarm='down'),          # dip before the ta-da
             B(70, 'open', larm='out', rarm='out')]
    t_tada = now(body)
    body += [B(140, 'sparkle', dy=-1, legs='long', larm='wave', rarm='wave'),   # ta-da, up on his toes
             B(560, 'sparkle', larm='wave', rarm='wave'),
             B(100, 'open', larm='up', rarm='up'),
             B(320)] + blink(330)

    whoosh = [SPR(ms, _WHOOSH_START if k == 0 else _WHOOSH[k % 2])          # one streak pair per spin frame
              for k, (ms, _) in enumerate(fast)]
    whoosh += [SPR(80, _WHOOSH_FADE[0]), SPR(100, _WHOOSH_FADE[1])]
    dust = twinkle('dust_puff', 15, 18, [0, 1, 2], [80, 100, 130])
    big = twinkle('sparkle', 25, 8, [0, 1, 2, 3, 1, 0], [60, 80, 160, 110, 90, 70])
    small = twinkle('sparkle_small', 5, 10, [0, 1, 2, 1, 0], [70, 90, 120, 100, 80])
    return comp(body, [after(t_whoosh, whoosh), after(t_stop, dust), after(t_tada, big),
                       after(t_tada + 160, small)])


# ------------------------------------------------------------------ giggle
_HA_INK = 'O'                                     # rust: a warm mid-tone that reads on both themes
_HA = text_sprite('HA', _HA_INK)


def _specks(spr, ch):
    """Three specks spread over a sprite's top edge: what is left when it fizzles away."""
    return cells([(spr.x0, spr.y0 + 1), ((spr.x0 + spr.x1) // 2, spr.y0), (spr.x1, spr.y0 + 1)], ch)


def _ha(t0, pts):
    """A "HA" that pops out of him along `pts` [(x, y, ms)] (big steps first: ease out), drifts up,
    then fizzles away: checkered one row up, then three specks one more row up."""
    x, y = pts[-1][:2]
    return after(t0, [SPR(ms, _HA, px, py) for px, py, ms in pts] +
                 [SPR(90, checkered(_HA), x, y - 1), SPR(90, _specks(_HA, _HA_INK), x, y - 2)])


def giggle():
    """Tickled: eep! then he wriggles in giggly bursts, eyes squeezed shut, arms flapping and feet
    shuffling, holding his tummy between bursts, while "HA"s pop out of him and fizzle away; he
    calms down, opens his eyes and blinks."""
    tilt_r, tilt_l = ('up', 'down'), ('down', 'up')

    def wriggle(steps):
        out = []
        for ms, dx, arms in steps:
            legs = 'walk_a' if dx > 0 else 'walk_b' if dx < 0 else 'stand'
            out.append(B(ms, 'line', dx=dx, larm=arms[0], rarm=arms[1], legs=legs))
        return out

    side = ('side', 'side')
    body = [B(150),
            B(130, 'wide', larm='up', rarm='up'),                 # eep!
            B(70, 'half', larm='front', rarm='front')]
    t1 = now(body)
    body += wriggle([(80, 1, tilt_r), (70, 0, side), (80, -1, tilt_l), (70, 0, side), (80, 1, tilt_r),
                     (90, 0, side)])
    body += [B(170, 'line', larm='front', rarm='front')]        # holds his tummy
    t2 = now(body)
    body += wriggle([(80, -1, tilt_l), (70, 0, side), (80, 1, tilt_r), (70, 0, side), (80, -1, tilt_l),
                     (90, 0, side)])
    body += [B(140, 'line', larm='front', rarm='front')]
    t3 = now(body)
    body += wriggle([(80, 0, tilt_r), (80, 0, side), (80, 0, tilt_l), (100, 0, side)])   # last chuckles
    body += [B(170, 'line', larm='front', rarm='front'), B(90, 'half'), B(360, 'open')] + blink(300)

    ha1 = _ha(t1, [(22, 9, 60), (23, 7, 70), (24, 6, 140), (24, 5, 200)])
    ha2 = _ha(t2, [(2, 9, 60), (1, 7, 70), (1, 6, 140), (1, 5, 230)])
    ha3 = _ha(t3, [(17, 6, 60), (19, 5, 70), (20, 4, 140), (20, 3, 160)])
    return comp(body, [ha1, ha2, ha3])


# ------------------------------------------------------------------ shrug
_Q_INK = 'b'
_Q_SMALL = text_sprite('?', _Q_INK)               # 3x5 font "?": the big one's pop-in / pop-out size
_Q_DOT = cells([(1, 4)], _Q_INK)


def shrug():
    """Huh? He glances left, then right; a blue "?" pops up over his head, he looks up at it and shrugs,
    hands up, rising on his toes with heavy-lidded "dunno" eyes; he drops back, looks up as the "?"
    shrinks away, and blinks."""
    body = [B(170), B(420, 'look_l'), B(80, 'open'), B(360, 'look_r'), B(110, 'open')]
    t_q = now(body)
    body += [B(170, 'look_u'),                                   # notices the "?"
             B(90, 'open', larm='down', rarm='down'),            # shoulders drop (anticipation)
             B(70, 'open', larm='up', rarm='up')]
    t_up = now(body)
    body += [B(100, 'half', dy=-1, legs='long', larm='wave', rarm='wave'),     # shrug: hands overshoot out
             B(460, 'half', dy=-1, legs='long', larm='raise', rarm='raise')]   # ...and settle: dunno
    up_ms = now(body) - t_up
    body += [B(90, 'half', larm='up', rarm='up'),                # drops back
             B(110, 'open')]
    t_out = now(body)
    body += [B(330, 'look_u'), B(120, 'open')] + blink(300)

    def big(ms, up):
        return FX(ms, 'question', 1 if up else 0, 15, 7)
    q = after(t_q, [SPR(60, _Q_SMALL, 14, 6), big(90, True), big(t_up - t_q - 150, False),
                    big(up_ms, True), big(t_out - t_up - up_ms, False),  # pushed up while he's up
                    big(150, True),                                       # a last hop, then it shrinks away
                    SPR(90, _Q_SMALL, 14, 4), SPR(80, _Q_DOT, 14, 3)])
    return comp(body, [q])


# ------------------------------------------------------------------ idea
def idea():
    """Aha! He ponders (a glance aside), a light bulb rises out of his head and his eyes follow it up;
    it switches on (wide eyes!), glows, and he points at it with a twinkle in his eyes. Then the bulb
    floats up and pops into a twinkle."""
    body = [B(180), B(330, 'look_l'), B(90, 'open')]
    t_bulb = now(body)
    body += [B(70, 'open'), B(300, 'look_u')]                 # the eyes follow it up
    t_on = now(body)
    body += [B(220, 'wide'),                                    # it lights: surprise
             B(80, 'look_u', rarm='up'),
             B(700, 'sparkle', rarm='raise'),                    # points up at the bulb
             B(100, 'open', rarm='up')]
    t_off = now(body)
    body += [B(320, 'look_u'), B(90, 'open')] + blink(320)

    def bulb(ms, i, y=6):
        return FX(ms, 'lightbulb', i, 15, y)
    glow = [bulb(110, 1), bulb(330, 2), bulb(140, 1)]                     # on, rays, a flicker...
    b = after(t_bulb, [bulb(70, 0, 7), bulb(80, 0, 5), bulb(t_on - t_bulb - 150, 0)] + glow +
              [bulb(t_off - t_on - _tlen(glow), 2),                         # ...rays while he points
               bulb(110, 1, 5)])                                            # it lifts...
    b += twinkle('sparkle', 15, 5, [2, 3, 1, 0], [110, 100, 80, 70])    # ...and pops into a twinkle
    tw = after(t_on + 110, twinkle('sparkle_small', 24, 3, [0, 1, 2, 1, 0], [80, 100, 120, 100, 80]))
    return comp(body, [b, tw])


# ------------------------------------------------------------------ poof
_POOF_TAIL = cells([(3, -1), (13, -1), (8, 0)], 's', anchor=(8, 6))   # the last specks drift up


def poof():
    """Magic trick: arms up, eyes squeezed (abracadabra), poof! he vanishes in a cloud; a sparkle hints
    where he'll be, poof, there he is a few cells to the right; he looks back where he was, then
    around, and poofs home the same way (ta-da eyes)."""
    R = 7                                                        # cells to the right
    body = [B(150),
            B(80, 'half', larm='up', rarm='up'),
            B(200, 'line', larm='raise', rarm='raise')]          # abracadabra
    t_out1 = now(body)
    body += [B(60, 'line', larm='raise', rarm='raise'),          # burst over him
             B(460, turn='gone')]
    t_in1 = now(body)
    body += [B(60, dx=R, turn='gone'),                          # burst on the right
             B(220, dx=R),                                      # there he is (the cloud clears)
             B(340, 'look_l', dx=R), B(90, dx=R), B(240, 'look_r', dx=R), B(100, dx=R),
             B(70, 'half', dx=R, larm='up', rarm='up'),
             B(160, 'line', dx=R, larm='raise', rarm='raise')]
    t_out2 = now(body)
    body += [B(60, 'line', dx=R, larm='raise', rarm='raise'),
             B(300, turn='gone')]
    t_in2 = now(body)
    body += [B(60, turn='gone'),
             B(220, 'sparkle')] + blink(280)                    # home, ta-da

    def cloud(at, x):
        return after(at, [FX(ms, 'poof', i, x, 15) for i, ms in enumerate([60, 110, 110, 140])] +
                     [SPR(100, _POOF_TAIL, x, 15)])

    def hint(t_in, x, ms):
        # a twinkle over the far top corner of where he'll appear (clear of the other cloud's ring); it
        # grows until the new cloud billows up beside it and takes over (timed on the clouds' frames)
        return after(t_in + 60 - sum(ms), twinkle('sparkle_small', x, 11, [0, 1, 2], ms))
    return comp(body, [cloud(t_out1, 15), cloud(t_in1, 15 + R), cloud(t_out2, 15 + R), cloud(t_in2, 15),
                       hint(t_in1, 18 + R, [110, 140, 160]), hint(t_in2, 12, [110, 80, 60])])


# ------------------------------------------------------------------ groove
_NOTE_SMALL = Sprite(['.vl', '.v.', 'vV.'], anchor=(1, 1))      # a 3x3 eighth note: pop-in / drift-off size
_NOTE_DOT = cells([(0, 0)], 'v')


def _note(t0, name, x, y, sway, durs):
    """A note that pops in small, floats up 1 cell per step with a side-to-side sway, then shrinks
    and drifts off (small note, then a dot). durs: [pop-in, steps..., shrink, dot]."""
    tr = [SPR(durs[0], _NOTE_SMALL, x, y + 1)]
    steps = durs[1:-2]
    for k, ms in enumerate(steps):
        tr.append(FX(ms, name, 0, x + sway[k % len(sway)], y - k))
    n = len(steps)
    tr += [SPR(durs[-2], _NOTE_SMALL, x + sway[n % len(sway)], y - n),
           SPR(durs[-1], _NOTE_DOT, x + sway[(n + 1) % len(sway)], y - n - 1)]
    return after(t0, tr)


def groove():
    """Little dance on a steady beat: up on his toes on the off-beat, landing on the beat, one arm
    pumping up each beat (it comes down a beat later), eyes following it, eyes shut on the third beat;
    notes pop in on the beats and bob up in time, then shrink away. He ends with a pose and a blink."""
    UP, DOWN = 160, 260                                          # one beat = 420 ms
    beat = UP + DOWN
    body = [B(170), B(110, 'open', larm='down', rarm='down')]   # catches the beat
    t_beats = now(body)
    for k, s in enumerate(['l', 'r', 'l', 'r']):
        look = 'look_l' if s == 'l' else 'look_r'
        pump = ('raise', 'side') if s == 'l' else ('side', 'raise')
        lag = ('up', 'side') if s == 'l' else ('side', 'up')
        body.append(B(UP, 'line' if k == 2 else look, dy=-1, legs='long', larm=pump[0], rarm=pump[1]))
        body.append(B(DOWN, 'half' if k == 2 else look, larm=lag[0], rarm=lag[1]))
    body += [B(90, 'open', larm='up', rarm='up'),
             B(380, 'sparkle', larm='raise', rarm='raise'),      # and... pose
             B(100, 'open', larm='up', rarm='up'), B(220)] + blink(260)

    life = [UP, DOWN, UP, DOWN, UP, 130, 110]                   # pop in on the off-beat, bob up in time
    n1 = _note(t_beats, 'note', 25, 10, [0, 1, 0, -1], life)
    n2 = _note(t_beats + beat, 'note_double', 5, 10, [0, -1, 0, 1], life)
    n3 = _note(t_beats + 3 * beat, 'note', 26, 9, [0, -1, 0, 1], [UP, DOWN, 90, 190, 190, 130, 110])
    return comp(body, [n1, n2, n3])
