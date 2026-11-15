"""vibe - personal chill-music mode: Clawd the phonk DJ.  Preview:  python3 gen/preview.py anim vibe

STORYBOARD  (140 BPM: beat = 428 ms, 8th = 214, 16th = 107. Master phrase = 32 beats = 8 bars = 13.696 s.
Every layer lasts a whole number of beats and every frame a whole number of 16ths, so it all stays locked;
the layers that follow the chain last a whole number of 2-beat grooves.)
  the groove   felt heavy-light, like the music: beats 1 and 3 are the HEAVY nod (down on the beat, hit and
               hold 321 ms while the headphone cups glow, then a quick 107 ms lift), beats 2 and 4 the light
               bounce (214 down / 214 up). The heavy gold chain is too heavy for the quick lift: it hangs on,
               rises late at the end of the light bounce and lands a 16th after him on the heavy beat, so the
               diamond swings on the 1. The left record turns once every 2 beats and the lantern's tassel
               swings with the bass (a pendulum over the same 2 beats).
  right hand   2-bar scratch groove on the right record (4x per phrase): baby scratch on beats 1 + 3 (push on
               the beat, pull on the "and"), 16th chirps on beat 5, baby scratch on beat 7. The light on the
               grooves moves with his hand.
  left hand    drumstick held over a cowbell mounted on the left deck, now and then: a 16th wind-up, STRIKE
               on the off-beat (gold "ding" rays + sparks where the tip lands on the bell's mouth), then it
               rings on, darker, as the stick rebounds (the left ray travels outward, the top one fades).
     0.00  bar 1  HOME on the heavy downbeat ................................. 1.50 "and" of 4: ding
     1.71  bar 2  (groove) ............................................... 3.21 "and" of 8: ding
     3.42  bar 3  (groove)
     5.14  bar 4  5.03-5.56 his eyes lock on the record for the 16th chirps .... 6.63 "and" of 16: ding
     6.85  bar 5  (groove)
     8.56  bar 6  (groove; the stick rests: a calm bar, the breather that sets up the trick)
    10.27  bar 7  THE TOSS. 10.27 the hand dips a cell (anticipation, opposite to the throw), 10.38 flicks
                  the stick upright and he watches it, 10.49 a drummer's flip: it leaves the hand straight up
                  and spins one full clockwise turn (rises fast, hangs, drops; 6 cells level/upright, 5
                  diagonal = constant length), 10.81 at the apex he looks back at you, 11.13 no-look catch on
                  the heavy downbeat of 27 (the spin carries on into the grip, the hand gives a cell), 11.24
                  wind-up, 11.34 the big DING: the whole bell flares gold and three streaks burst out of its
                  crown (the only full flare: the payoff)
    11.98  bar 8  (groove) -> loops into frame 0
Ambient layers (beat-quantized; co-prime lengths so the picture never repeats exactly):
  EQ 3 beats (three neon bars on the right deck: punch on the beat with a gold peak on the loudest bar,
  settle a cell; capped at row 10 so the notes above always keep a clear row) | notes 11 beats (a note, then
  a beamed pair, take turns: each materializes from a violet speck on the beat, drifts up between the nods
  on the off-16ths, evaporates into a violet twinkle) | blinks 13 beats (3.0 s, 2.35 s + a double) | club
  lights 17 beats (speck, twinkle, speck; 4.5 s / 2.8 s apart) | bling 18 beats (the diamond glints after
  3.0 s, then 4.7 s).
Mood (violet glow): the booth's whole front edge is a deep-violet underglow strip with a lavender neon tube
burning in front of his feet (steady: the one light that never pulses), pads glowing violet under the left
platter and pink under the right, record labels lit to match; the headphone cups glow on every heavy beat.
Red lives only in the paper lantern (the East-Asian half of the user's Asian x Brazilian phonk; the cowbell
is the montagem half), so it reads as the deliberate accent.
Frame 0 (reduced motion): HOME on the heavy downbeat, cups lit, right hand on the record, stick raised over
the cowbell, a note above the EQ (gold peak), a violet club light, the neon underglow and the lantern.

User taste (STYLE.md 0): normal body size (the bob moves his whole body; the legs never shrink, they hide
behind the mixer), plain dot eyes with blinks and glances only, no mouth, no face shading.

Tricks that keep it on the beat AND small (target ~40 KB):
  * The groove is strictly periodic (2 beats), so the body is a 4-frame layer and the chain a 3-frame one.
    The hands are planted on the gear and do not bob: the left forearm stays put while the shoulder rides
    the bob (HOME = the kit's 'raise', up = the elbow folds; no gap ever opens beside his face), and the
    drumstick lives in its own 32-beat layer. His feet behind the mixer are not drawn (always hidden).
  * Eyes: the body is drawn with the holes of every face the state uses (open, look_l, glance) and two
    layers UNDER the body plug the unused ones with body orange. Each face cell lies inside the body in both
    bob positions and never coincides with another face's cell of the other position, so a plug frame is the
    same whatever the bob does: a glance or a blink costs two small frames. The glance is a fixed gaze on
    the record: the same two screen cells in both positions, which is exactly the kit's look_r at HOME and
    look_dr when he is up (his eyes stay on the record while his head bobs). Those cells sit on row 14,
    which the swinging chain never reaches, and (20, 14) is the scratch arm's shoulder in both poses, so
    the face is a clean kit face at every 16th. (look_u/look_d would collide with the bob; look_ul/look_ur
    hide one eye under a cup.) The composite is always a kit face: open, look_l, look_r/look_dr or blink.
Library reuse: dj_decks (split into two turntables, pads re-lit violet/pink), headphones_glow,
gold_chain (+ its glint frames), cowbell (mounted on a post), drumstick (ready / strike frames),
equalizer (its bar levels, re-lit neon), note, note_double, sparkle_small (violet club lights, note
specks/twinkles). Local sprite: _LANTERN (the library has no lantern).
Lint info, by design (light theme): the diamond's ice facet touches the background in the 16ths where the
lagging chain hangs below his belly, between his legs (the chain's open V).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401,F403
from acc import get                          # noqa: E402

NAME = 'vibe'
STATE = 'Personal chill-music mode'
DESC = ('Phonk DJ Clawd nods heavy-light between his turntables: scratches, rings a cowbell on the '
        'off-beats and now and then tosses his drumstick for a no-look catch, headphones glowing on the '
        'one, gold chain swinging, violet neon, EQ and notes.')

Q = 107                 # a 16th note at 140 BPM
E = 2 * Q               # an 8th
BEAT = 4 * Q            # 428 ms
PHRASE = 128            # the master phrase in 16ths: 32 beats = 8 bars = 13696 ms
UP_AT = (HOME[0], HOME[1] - 1)

# The groove, per 16th over 2 beats (heavy beat + light beat). D = down at HOME, U = up a cell.
GROOVE = 8
BOB = 'DDDUDDUU'        # heavy: hit, hold, quick lift | light: 214 down, 214 up
GLOW = 'GGG.....'       # the cups glow through the heavy hit
CHAIN = 'UDDDDDDU'      # the chain ignores the 16th lift, rises late, lands a 16th after him
assert len(BOB) == len(GLOW) == len(CHAIN) == GROOVE


def _paint(f, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch not in '. ':
                f.put(x0 + i, y0 + j, ch)


def _cells(f, cells, ch):
    for x, y in cells:
        f.put(x, y, ch)


def _timed(name, events, total_steps):
    """events: [(16th step, Frame)] sorted; each frame shows until the next one starts."""
    out = []
    for k, (s, f) in enumerate(events):
        end = events[k + 1][0] if k + 1 < len(events) else total_steps
        out.append((f, (end - s) * Q))
    return layer(name, out)


def _part_pose(cells, name):
    """Kit-style Clawd cells (absolute canvas cells, body orange) as a pose for put_clawd at HOME."""
    p = clawd(larm='none', rarm='none')
    spr = Sprite(cells=[(x - HOME[0], y - HOME[1], '#') for x, y in cells], anchor=(0, 0), name=name)
    return Pose(spr, p.anchors, dict(p.spec, part=name))


# =====================================================================================================
# The console: the library dj_decks split into two turntables, a neon mixer strip at Clawd's feet
# =====================================================================================================
_DECK_FALLBACK = [
    'mmmmmmmmmmmmmmmmm',
    'mmKKKKKmNmKKKKKmm',
    'mKKKrKKKyKKKyKKKm',
    'mmKKKKKmNmKKKKKmm',
    'NccNccNNNNNppNppN',
]


def _deck_frames():
    try:
        frames = [spr.rows() for spr in get('dj_decks').frames]
    except KeyError:
        frames = []
    if not frames or any(len(rows) != 5 or any(len(r) != 17 for r in rows) for rows in frames):
        frames = [_DECK_FALLBACK]
    return frames


def _deck_rows():
    """Library deck frame 0 with clean platters: our own layers draw the turning highlight."""
    out = []
    for j, r in enumerate(_deck_frames()[0]):
        r = list(r)
        if 1 <= j <= 3:
            for i in list(range(1, 8)) + list(range(9, 16)):
                if r[i] == 'N':
                    r[i] = 'K'
        out.append(''.join(r))
    return out


TT_L_X, TT_R_X, TT_Y = 2, 20, 15


def _spin_path():
    """Where the library's own spinning mark sits on the left platter in each of its frames."""
    path = []
    for rows in _deck_frames():
        for j in range(1, 4):
            for i in range(1, 8):
                if rows[j][i] == 'N':
                    path.append((TT_L_X + i, TT_Y + j))
    return path if len(path) == 4 else [(6, 16), (8, 17), (6, 18), (4, 17)]


_D = _deck_rows()
# The mood light: the booth's whole front edge is one violet underglow strip (deep violet, so it reads as
# light on the dark theme and as the booth's base on the light one), the pads glow violet on the left deck
# and pink on the right, and a lavender neon tube burns in front of his feet. Record labels re-lit to match.
_UNDERGLOW = {'N': 'V', 'n': 'V', 'c': 'v'}
_LABELS_L, _LABELS_R = {'r': 'l'}, {'y': 'p'}
TT_L = ([''.join(_LABELS_L.get(c, c) for c in r[:8]) + 'm' for r in _D[:4]] +
        [''.join(_UNDERGLOW.get(c, c) for c in _D[4][:8]) + 'V'])                 # x 2..10, rows 15..19
TT_R = (['m' + ''.join(_LABELS_R.get(c, c) for c in r[9:]) for r in _D[:4]] +
        ['V' + ''.join(_UNDERGLOW.get(c, c) for c in _D[4][9:])])                 # x 20..28
MIXER = ['VlllllllV']                       # the neon tube in front of his feet (the brightest, steady)
MIXER_X, MIXER_Y = 11, 19
MARK = 'm'                                  # light catching the grooves: shows the records turning
SPIN_L = _spin_path()                       # left record: a quarter turn per 8th, clockwise
SCRATCH_MARK = {'p': (23, 16), 'l': (22, 16)}   # right record: the grooves move with his hand


# =====================================================================================================
# Cowbell mounted on the left deck (the library cowbell without its hand grip, on a steel post),
# and a red paper lantern hanging in the corner above it
# =====================================================================================================
_BELL = get('cowbell')
BELL_AT = (0, 10)                           # (removed) grip end: bell body x 2..6, rows 8..13
POST = (4, 14)                              # where the clapper hung: a short post onto the deck
RAYS_A = [(2, 7), (4, 6), (6, 7)]           # "ding" bursts out of the bell's crown ...
RAYS_B = [(1, 6), (4, 6)]                   # ... and rings on, darkening (the left ray travels outward;
                                            # the vertical one fades in place, clear of the lantern)
SPARKS = [(3, 14), (5, 14)]                 # where the tip lands on the bell's mouth
BELL_GLOW = {'S': 'Y', 's': 'y'}            # the big DING: the whole bell flares warm for a 16th
RAYS_BIG = RAYS_A + [(1, 6), (4, 7), (7, 6)]    # the catch DING: three 2-cell streaks out of the crown

_LANTERN = Sprite([
    '.JjJ.',
    'roorR',
    'roorR',
    'rrrRR',
    '.JjJ.',
], anchor=(2, 0), name='paper_lantern')     # round red paper lantern: gold caps, the candle glowing inside
LANTERN_AT = (3, 0)                         # x 1..5, hangs from the top edge
# its tassel swings with the bass, a pendulum over 2 beats (one cell per 8th), out at the right on the
# heavy downbeat. No ding ray or stick cell ever lands on or beside the lantern or tassel (asserted)
TASSEL = [(4, 5), (3, 5), (2, 5), (3, 5)]


def _bell():
    s = _BELL.sprite(0)
    return Sprite(cells=[(x, y, ch) for x, y, ch in s.cells if ch != 'T'], anchor=(s.ax, s.ay),
                  name='cowbell_mounted')


def _bell_frame():
    f = Frame()
    f.place(_bell(), *BELL_AT)
    f.put(POST[0], POST[1], 's')
    return f


# =====================================================================================================
# Clawd: the bobbing body + headphones + the left shoulder (2 beats, strictly periodic)
# =====================================================================================================
_HP = get('headphones_glow')
_CHAIN = get('gold_chain')
FACES = ('open', 'look_l', 'glance')        # every face this state shows (see the eye trick above)
FOREARM_L = [(9, 12), (9, 13)]              # planted under the drumstick's grip (9, 11), never bobs


def _kit_eye_cells(look, up):
    """Absolute hole cells of the kit eye pattern `look` with Clawd at HOME (up=False) or 1 cell up."""
    g = GEOM['normal']
    x0, y0 = UP_AT if up else HOME
    out = []
    for cx, pat in zip(g['ex'], EYES[look]):
        for dx, dy, ch in pat:
            if ch == '_':
                out.append((x0 + cx + dx, y0 + g['ey'] + dy))
    return out


# the glance: eyes locked on the right record, the same screen cells in both bob positions
GLANCE = _kit_eye_cells('look_r', False)
assert sorted(GLANCE) == sorted(_kit_eye_cells('look_dr', True)) == [(13, 14), (19, 14)]


def _eye_cells(look, up):
    return list(GLANCE) if look == 'glance' else _kit_eye_cells(look, up)


def _plugs(*looks):
    """Body-orange cells that close the holes of these faces in both bob positions."""
    return sorted({c for look in looks for up in (False, True) for c in _eye_cells(look, up)})


def _console_cells():
    f = Frame()
    _paint(f, MIXER, MIXER_X, MIXER_Y)
    return set(f.px)


_HIDDEN = _console_cells()                  # his feet behind the mixer: never visible, not drawn


def _body(up, glow):
    """Down at HOME or up one cell. The left arm: the shoulder rides the bob while the forearm stays
    planted under the stick (HOME = the kit's 'raise'; up = the elbow folds). Cups lit on the heavy hit."""
    f = Frame()
    x, y = UP_AT if up else HOME
    p = clawd(eyes='open', larm='none', rarm='none', legs='long' if up else 'stand')
    holes = {(cx - x, cy - y) for look in FACES for cx, cy in _eye_cells(look, up)}
    cells = [(cx, cy, '_' if (cx, cy) in holes else ch) for cx, cy, ch in p.sprite.cells
             if (x + cx, y + cy) not in _HIDDEN]
    cells.append((0, GEOM['normal']['ay'], '#'))                      # left shoulder
    cells += [(cx - x, cy - y, '#') for cx, cy in FOREARM_L]           # planted forearm
    pose = Pose(Sprite(cells=cells, anchor=(0, 0), name='clawd'), p.anchors,
                dict(p.spec, larm='raise (hand planted)', faces=FACES))
    put_clawd(f, pose, x, y)
    wear(f, _HP, pose, x, y, i=1 if glow else 0)
    return f


def _chain(up):
    """The gold chain where it hangs: from his neck at HOME, or one row higher (where it hangs when he is
    up). Drawn over the console, one 16th behind him (see CHAIN)."""
    f = Frame()
    wear(f, _CHAIN, clawd(), dy=-1 if up else 0)
    return f


def _chain_dy(step):
    return -1 if CHAIN[step % GROOVE] == 'U' else 0


# =====================================================================================================
# Left hand: the drumstick (32-beat phrase). The forearm itself is planted in the body layer.
# =====================================================================================================
GRIP = (9, 11)
_STICK = get('drumstick')
LIFT = [(9, 11), (9, 10), (9, 9), (8, 8), (8, 7), (8, 6)]       # wind-up: the stick cocked upright
_DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
# the toss: a drummer's flip, straight up over the hand and back (clear of the lantern), one clockwise
# turn, 45 deg per 16th, from the cocked stick back into the hand. Its centre rises 2.5, 2, 1, hangs
# and drops 1, 2, then 3.5 into the hand; the last airborne tip (6, 6) is the ready tip, so the catch
# reads as the spin continuing into the grip.
TOSS = [((9, 6), 1), ((9, 4), 2), ((9, 3), 3), ((9, 3), 4), ((9, 4), 5), ((9, 6), 6)]

#          beat: 1   2   3   4   |5   6   7   8   |9   10  11  12  |13  14  15  16
SCORE_L = ('uuuuuuuuuuuuuwXx' 'uuuuuuuuuuuuuwXx' 'uuuuuuuuuuuuuuuu' 'uuuuuuuuuuuuuwXx'
           'uuuuuuuuuuuuuuuu' 'uuuuuuuuuuuuuuuu' 'dw012345dwZxuuuu' 'uuuuuuuuuuuuuuuu')
#          beat: 17  18  19  20  |21  22  23  24  |25  26  27  28  |29  30  31  32
# u ready, w wind-up, X strike, x ring, d dip / catch (the hand gives a cell), 0-5 airborne, Z big DING
SCORE_R = ('p.l.H...p.l.H...' 'plplH...p.l.H...')       # 2-bar scratch groove, loops 4x per phrase
# p push, l pull, H hold
EYES_AT = [(0, 'open'), (47, 'glance'), (52, 'open'), (97, 'look_l'), (101, 'open')]
assert len(SCORE_L) == PHRASE and PHRASE % len(SCORE_R) == 0 and PHRASE % GROOVE == 0


def _stick_cells(center, d):
    """A drumstick in the air: 6 cells when level or upright, 5 on the diagonals (same visual length),
    light tip last."""
    dx, dy = _DIRS[d]
    cx, cy = center
    ks = list(range(-2, 3)) if dx and dy else list(range(-2, 4))
    return [(cx + k * dx, cy + k * dy, 't' if k == ks[-1] else 'T') for k in ks]


def _left(tok):
    """The drumstick in his raised left hand (+ what it does to the cowbell)."""
    f = Frame()
    if tok == 'w':
        for i, (x, y) in enumerate(LIFT):
            f.put(x, y, 't' if i == len(LIFT) - 1 else 'T')
    elif tok in '012345':
        for x, y, ch in _stick_cells(*TOSS[int(tok)]):
            f.put(x, y, ch)
    elif tok == 'd':
        # the hand sinks a cell (dip before the toss / give on the catch): the stick's butt covers the
        # planted forearm's top cell and the hand shows one cell lower
        put_clawd(f, _part_pose([(9, 14)], 'hand_l_low'))
        f.place(_STICK.sprite(0).flipped(), GRIP[0], GRIP[1] + 1)
    else:
        f.place(_STICK.sprite(1 if tok in 'XZ' else 0).flipped(), *GRIP)    # library ready / strike
    if tok == 'X':
        _cells(f, RAYS_A + SPARKS, 'j')
    elif tok == 'Z':
        bell = Frame()
        bell.place(_bell(), *BELL_AT)
        for (x, y), ch in bell.px.items():
            if ch in BELL_GLOW and (x, y) not in f.px:
                f.put(x, y, BELL_GLOW[ch])
        _cells(f, RAYS_BIG + SPARKS, 'j')
    elif tok == 'x':
        _cells(f, RAYS_B, 'J')
    return f


R_POSE = {
    'p': [(20, 14), (21, 15), (22, 16)],    # push: hand forward onto the record
    'l': [(20, 14), (20, 15), (21, 16)],    # pull: hand back to the record's edge
}


def _right(pose):
    f = Frame()
    f.put(*SCRATCH_MARK[pose], MARK)
    put_clawd(f, _part_pose(R_POSE[pose], 'arm_r'))
    return f


def _track(score, fn):
    out, last = [], None
    for ch in score:
        if ch == 'H':
            ch = 'l'
        elif ch == '.':
            ch = last
        last = ch
        out.append((fn(ch), Q))
    return out


# =====================================================================================================
# Eyes: plug layers drawn UNDER the body (see the module docstring)
# =====================================================================================================
def _plug_frame(cells, name):
    f = Frame()
    put_clawd(f, _part_pose(cells, name))
    return f


def _eyes_layer():
    """Glances on the phrase: the unused faces' holes are plugged; frame 0 = plain open eyes."""
    events = []
    for s, look in EYES_AT:
        events.append((s, _plug_frame(_plugs(*[k for k in FACES if k != look]), 'eyes_' + look)))
    return _timed('eyes', events, PHRASE)


def _blink_layer(beats, at):
    """Blinks (one 16th each) at uneven steps: every hole plugged, whatever the bob or a glance does."""
    lids = [(x, y) for x in range(11, 20) for y in range(13, 16)]     # covers every hole, any bob
    assert set(_plugs(*FACES)) <= set(lids)
    events = [(0, Frame())]
    for s in at:
        events += [(s, _plug_frame(lids, 'blink')), (s + 1, Frame())]
    return _timed('blink', events, beats * 4)


# =====================================================================================================
# Static scene
# =====================================================================================================
def _scene():
    f = Frame()
    _paint(f, TT_L, TT_L_X, TT_Y)
    _paint(f, TT_R, TT_R_X, TT_Y)
    _paint(f, MIXER, MIXER_X, MIXER_Y)
    f.px.update(_bell_frame().px)
    f.place(_LANTERN, *LANTERN_AT)
    return f


# =====================================================================================================
# Effects
# =====================================================================================================
_EQ = get('equalizer')
EQ_BARS = {2: 23, 4: 25, 6: 27}             # library bars 1..3 -> three bars on the right deck's back edge
EQ_FLOOR, EQ_MAX = 14, 5                    # they stand on row 14, at most 5 cells tall (top row 10), so
                                            # the notes above always keep a clear row
EQ_LEVELS = 'vvppj'                         # neon level colors from the floor up; gold = the peak


def _eq_heights(k):
    """Bar heights of library equalizer frame k (bars 1..3), scaled from its 7 rows to our 5."""
    spr = _EQ.sprite(k)
    full = spr.y1 - spr.y0 + 1
    out = {}
    for sx, x in EQ_BARS.items():
        ys = [cy for cx, cy, ch in spr.cells if cx == sx]
        h = spr.y1 - min(ys) + 1 if ys else 1
        out[x] = max(1, -(-h * EQ_MAX // full))
    return out


def _eq_frame(heights, sag):
    """The bars (instant attack on the beat, then they settle `sag` cells)."""
    f = Frame()
    for x, h in heights.items():
        for i in range(max(1, h - sag)):
            f.put(x, EQ_FLOOR - i, EQ_LEVELS[i])
    return f


_NOTE = get('note')
_NOTE2 = get('note_double')
_TWINKLE = get('sparkle_small')
_VIOLET = {'j': 'V', 'y': 'v'}              # sparkle_small re-lit as a violet club light


def _spark(fr, x, y):
    f = Frame()
    f.place(_TWINKLE.sprite(fr).recolor(_VIOLET), x, y)
    return f


def _notes_layer(beats, rises):
    """One layer, the two notes take turns (never tangled). Each: a violet speck one 16th before, then
    the note on the beat, held 3 16ths, drifting up a cell on the off-16ths 3, 5, 7, evaporating into
    a violet twinkle on 9 (two 16ths), gone. rises: [(start step, item, path, speck)]"""
    total = beats * 4
    events = []
    for start, item, path, speck in rises:
        assert start % 4 == 0, 'a note is born on the beat'
        events.append(((start - 1) % total, _spark(0, *speck)))
        for k, (x, y) in enumerate(path):
            f = Frame()
            f.place(item.sprite(0), x, y)
            events.append((start + (0 if k == 0 else 2 * k + 1), f))
        x, y = path[-1]
        events.append((start + 2 * len(path) + 1, _spark(1, x, y - 1)))
        events.append((start + 2 * len(path) + 3, Frame()))
    events.sort(key=lambda e: e[0])
    assert events[0][0] == 0, 'frame 0 must show a note (the reduced-motion still)'
    return _timed('notes', events, total)


def _chain_glint_cells(i):
    """White cells of the library gold_chain glint frame i (1 or 2), chain at its HOME hang."""
    p = clawd()
    base, g = Frame(), Frame()
    wear(base, _CHAIN, p, i=0)
    wear(g, _CHAIN, p, i=i)
    return [c for c, ch in g.px.items() if base.px.get(c) != ch]


def _gem():
    """The diamond's bright table facet ('C') with the chain at its HOME hang."""
    f = Frame()
    wear(f, _CHAIN, clawd(), i=0)
    found = [c for c, ch in f.px.items() if ch == 'C']
    return found[0] if found else (15, 18)


GEM = _gem()


def _glint_layer(beats, at):
    """Bling on the beat: library glint sweep -> a white star on the gem -> the library's last twinkle,
    stretched into a 2-cell streak up the chain's V. Every cell follows the swinging chain (the layer
    lasts whole grooves, so it stays locked to it); no white touches the background on either theme."""
    assert (beats * 4) % GROOVE == 0
    gx, gy = GEM
    star = [(gx, gy - 1), (gx - 1, gy), (gx, gy), (gx + 1, gy)]
    fade = _chain_glint_cells(2)
    fade = fade + [(x, y - 1) for x, y in fade]
    events = [(0, Frame())]
    for s in at:
        assert s % 4 == 0, 'the glint starts on a beat'
        for k, cells in enumerate((_chain_glint_cells(1), star, fade)):
            off = _chain_dy(s + k)
            f = Frame()
            _cells(f, [(x, y + off) for x, y in cells], 'W')
            events.append((s + k, f))
        events.append((s + 3, Frame()))
    return _timed('glint', events, beats * 4)


def _lights_layer(beats, events_at):
    """Violet club lights twinkling in the sky: speck, plus (2 16ths), speck, gone. events: (step of
    the plus, x, y); the first one is lit in frame 0 (the still) and fades in at the end of the loop."""
    total = beats * 4
    events = []
    for s, x, y in events_at:
        events += [((s - 1) % total, _spark(0, x, y)), (s, _spark(1, x, y)), (s + 2, _spark(0, x, y)),
                   (s + 3, Frame())]
    events.sort(key=lambda t: t[0])
    assert events[0][0] == 0
    return _timed('lights', events, total)


def build():
    body = [(_body(BOB[s] == 'U', GLOW[s] == 'G'), Q) for s in range(GROOVE)]
    chain = [(_chain(CHAIN[s] == 'U'), Q) for s in range(GROOVE)]
    lantern = Frame().place(_LANTERN, *LANTERN_AT)
    for s, tok in enumerate(SCORE_L):           # rays and stick stay clear of the lantern + swinging tassel
        near = set(lantern.px) | {TASSEL[(s // 2) % len(TASSEL)]}
        near |= {(x + dx, y + dy) for x, y in near for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
        assert not near & set(_left(tok).px), 'the left hand touches the lantern at step %d' % s
    spin = []                                   # the left record's turn + the lantern's tassel, per 8th
    for c, t in zip(SPIN_L, TASSEL):
        f = Frame()
        f.put(c[0], c[1], MARK)
        f.put(t[0], t[1], 'r')
        spin.append((f, E))
    eq = []
    for k in (0, 2, 4):
        h = _eq_heights(k)
        eq += [(_eq_frame(h, 0), Q), (_eq_frame(h, 1), 3 * Q)]
    layers = [
        _eyes_layer(),
        _blink_layer(13, [8, 36, 38]),
        layer('body', body),
        layer('eq', eq),
        _notes_layer(11, [(0, _NOTE, [(26, 6), (26, 5), (27, 5), (27, 4)], (25, 7)),
                          (24, _NOTE2, [(25, 6), (25, 5), (26, 5), (26, 4)], (25, 6))]),
        static('scene', _scene()),
        layer('chain', chain),
        layer('spin', spin),
        layer('right', _track(SCORE_R, _right)),
        layer('left', _track(SCORE_L, _left)),
        _glint_layer(18, [24, 52]),             # uneven holds: 3.0 s, then 4.7 s
        _lights_layer(17, [(0, 14, 3), (42, 20, 2)]),   # 4.5 s, then 2.8 s apart
    ]
    return anim(NAME, DESC, layers, state=STATE)
