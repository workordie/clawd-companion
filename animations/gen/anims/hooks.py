"""hooks - Running start-up or prompt hooks.  Pun: Clawd goes fishing (hooks!), and the input box is his pond.

The bottom edge of the canvas is the input box's top border, so here it is the WATER LINE: the bobber
floats on row 19, ripples run along it, and whatever sinks below it is under water (not drawn).

STORYBOARD (ms; one 4360 ms loop, every synced layer is cut from ONE beat list so nothing drifts)
     0  FISHING at HOME (frame 0 = the reduced-motion still): green bucket hat with a red fly on its band,
        rod (red grip, silver reel) held out at 45 deg, the line drops straight into the "pond" where a
        red-white bobber floats with ripples either side; at his left a steel pail with an earlier catch
        lying in it (the library fish: eye, dorsal fin, forked tail hanging over the rim). Eyes on his line.
   430  the catch flaps its tail twice (a drop of water flicks up and arcs away); 510 he glances at it
        (look_l) ... and so he misses the first nibble (790: the bobber dips, the rod tip twitches, a ripple
        ring) ... 1130 a quicker nibble: his eyes snap down onto the bobber (look_d) ...
  1340  BITE! the bobber is yanked under (only its tip shows), splash, his eyes follow it; a gold "!"
        springs up above his hat (short, then full height with burst ticks, holds; one row clear of the
        hat); the fish drags his arm down and arches the rod, the tip tugs up (1430) and is dragged down
        again (1550) = the anticipation for ...
  1660  THE YANK (60/70 ms): arm sweeps up, the rod bends like a crook, the bobber shoots out of the
        water on the taut line with the fish right below it (the line runs tip -> bobber -> fish's mouth);
        eyes snap up-right, then up; his free arm flings out for balance, then up.
  1790  the fish flies off the hook, IN FRONT of the rod: a ballistic arc over his head (fast at the ends,
        hanging at the apex, an even x step of ~3), rotating along the arc (head up -> up-left -> level,
        tail flick at the apex -> down-left -> head down); his eyes track it a beat behind (u, ul, l, dl),
        his free arm up as if reaching for it. Meanwhile the line snaps up over the rod tip, the bobber
        drops and swings out and back (pendulum, 1860-2010) and the bare HOOK dangles under it: a gold
        glint pings off the outside of its bend (1860 plus, 1930 x: "hook!"; neither touches the J).
  2320  it dives head-first into the pail, slipping in BEHIND the catch (its tail pokes up), splash ...
  2390  the catch flaps (drops fly up, fall back) while he lowers the rod: up -> mid (2390) -> rest (2600);
        the bobber swings out past plumb (2600) and back ...
  2600  happy beat: he turns to us ("look!"), free arm swung down (anticipation) ... 2800 HOP (2 cells,
        legs tucked): the bobber swings back to plumb, lagging 2 rows ... 2880 arm waving at the apex,
        slack line: the bobber floats up, a sparkle pops over the pail ... 2990 falling (1 cell): hat and
        bobber float behind ... 3050 lands with a dust puff, hat and bobber still up ... 3150 the hat
        lands, the bobber bounces below its rest, a blink ... 3270 it settles PLUMB under the tip, the
        bare hook dangling in open air (the pun, in the clear); he looks back at the water.
  3460  wind-up: the rod sweeps up and his eyes go up with it (look_u) ... 3530 swung back over his
        shoulder (clear of his hat, his hand keeps the grip; the hook reeled in), the bobber trails over the
        top ... and hangs behind him (3620, 160 ms hold) ... 3780 whip: the rod comes up, the bobber lags
        behind the tip (still overhead: eyes still up) ... 3840 the rod snaps forward, the bobber sails out
        ahead and his eyes follow it (look_r) ... 3910 the line shoots out and tugs the tip down (flex)
        while the bobber falls faster and faster (70, 60 ms) ...
  4040  PLOP: under + splash, the tip springs back; 4120 it pops up too high (overshoot), 4230 dips
        (follow-through) and settles into frame 0 with the ripple ring.
Layers (back to front): pail (static: the pail and the resting catch's body) | line (line, bobber, hook,
ripples, water splashes, the ROD over them, the hooked fish over the rod, and the effects: "!", sparkles,
dust; nothing in it ever overlaps a later layer except the rod, which the flying fish must cover) | fish
(the flying fish: in front of the rod, behind the catch, clipped inside the pail; the catch's flapping
tail; pail splashes) | body | hat. The fish never overlaps him or his hat, so its place before the body
costs nothing.
Local sprites: the rod poses (after the library fishing_rod: grip, reel, wood rod), the bobber, the hook,
the pail, the 45-deg fish (the other fish angles are the library fish rotated), the compact "!", the
dust. Library: fishing_hat, fish (also the catch in the pail), sparkle, sparkle_small.
Plain face only (open / blink / look_*), normal body size (the hop moves his whole normal body). The kit's
edge glances (look_r/dr/ur/l/ul/dl) put an eye hole on his body's edge column, so every edge glance here is
paired with an arm pose that closes that hole (look_r while the rod arm is up, look_l / look_dl with the
free arm at his side, look_dr only while the bite pulls the rod arm down to his side); look_d / look_u are
interior: his eyes always read as holes.
Size: the rod changes only on beats where the line changes anyway, so it lives in the line layer, drawn
in that layer's own colors (red grip = the bobber's red, reel = the line's silver, wood): no rod layer,
no extra colors. The hooked fish rides there too (yank beats). The catch's body is static (only its tail
flaps), the rod's arm changes ride on beats where his eyes change anyway, and on the hop's falling frame
the hat and the bobber keep their apex spots.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from acc import get                          # noqa: E402

NAME = 'hooks'
STATE = 'Running start-up or prompt hooks'
DESC = ('Clawd goes fishing in the input box: the bobber nibbles, bite!, he yanks, the fish flips over his '
        'head into his pail, the bare hook glints, a happy hop, and he casts again.')

BX = 26            # the fishing spot: line + bobber column (row 19 is the water line)
BKX = 4            # pail centre column (stands on row 19 at his left)
CATCH = (BKX, 14)  # where the resting catch's anchor (the library fish's body centre) lies in the pail


# =====================================================================================================
# local sprites
# =====================================================================================================
def _rod(rows, arm):
    """Rod pose drawn around the grip: 'x' = grip, 't' = the rest of the handle, 's' = reel, 'q' = tip.
    The rod shares the line layer, so it is drawn in that layer's own colors and adds none: a red handle
    (the bobber's red: a matching tackle set, and it stays distinct from his orange hand), a reel in the
    line's silver, a wood rod.
    Returns (hand Item anchored on the grip, tip offset from the grip, the arm shape that holds it)."""
    cells, grip, tip = [], None, None
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in '. ':
                continue
            if ch == 'x':
                grip, ch = (x, y), 'r'
            elif ch == 't':
                ch = 'r'
            elif ch == 'q':
                tip, ch = (x, y), 'T'
            elif ch == 's':
                ch = 'm'
            cells.append((x, y, ch))
    spr = Sprite(cells=cells, anchor=grip, name='fishing_rod')
    item = Item('fishing_rod', 'hand', 'local pose of the fishing rod (red grip, silver reel, wood rod)', spr)
    return item, (tip[0] - grip[0], tip[1] - grip[1]), arm


_RODS = {
    # resting: held up at chest height, straight 45 deg, the tip right above the fishing spot
    'rest': _rod(['.....q',
                  '....T.',
                  '...T..',
                  '..T...',
                  '.ts...',
                  'x.....'], 'up'),
    # the same rod flexed: the tip one row lower (a nibble twitch; the cast's follow-through)
    'flex': _rod(['....Tq',
                  '...T..',
                  '..T...',
                  '.ts...',
                  'x.....'], 'up'),
    # a bite: the fish drags his arm down and arches the rod over toward the water ...
    'bite': _rod(['...TT.',
                  '..T..q',
                  '.ts...',
                  'x.....'], 'side'),
    # ... and the tip tugs back up between pulls
    'bite2': _rod(['....Tq',
                   '...T..',
                   '..T...',
                   '.ts...',
                   'x.....'], 'side'),
    # the yank: sweeping up, still bent hard by the fish
    'yank1': _rod(['...TT.',
                   '..T..q',
                   '.T....',
                   '.T....',
                   'ts....',
                   'x.....'], 'up'),
    'yank2': _rod(['..TT.',
                   '.T..q',
                   '.T...',
                   '.T...',
                   '.T...',
                   'ts...',
                   'x....'], 'raise'),
    # held up after the yank (the fish has flown off the hook)
    'up': _rod(['..q',
                '..T',
                '.T.',
                '.T.',
                '.T.',
                'ts.',
                'x..'], 'raise'),
    # lowering it again: the in-between of 'up' and 'rest' (tip (+4, -5) of the grip, on the arc)
    'mid': _rod(['....q',
                 '...T.',
                 '...T.',
                 '..T..',
                 '.ts..',
                 'x....'], 'raise'),
    # wind-up for the cast: swung back over his shoulder. Held with the 'raise' arm, so the hand and grip
    # sit just right of the hat's brim and the shaft runs one cell clear of the hat (behind it).
    'back': _rod(['q.....',
                  '.T....',
                  '..T...',
                  '...T..',
                  '....T.',
                  '....ts',
                  '.....x'], 'raise'),
}

# red-white bobber; anchor = the top nub where the line ties on. Bottom 'mMm': light gray (not white) so
# the white half shows on the light theme, with silver ends as its outline.
_BOB = Sprite(['.r.',
               'rrr',
               'mMm'], anchor=(1, 0), name='bobber')
# the hook: a J in the line's own silver (eye top-right where the leader ties on, shank, bend, point up
# on the left); anchor = the eye. It dangles one line cell below the bobber from the catch until the
# wind-up (during the fast cast it is reeled up flush under the bobber; in the water it is under water).
_HOOK = Sprite(['..m',
                'm.m',
                '.m.'], anchor=(2, 0), name='hook')

# steel bait pail (anchor = bottom centre), split so a fish can lie IN it: the back rim + water, then the
# catch, then the front lip + body. Local: the library has no bucket.
_PAIL_BACK = Sprite(['NmmmmmN',
                     'mcccccm'], anchor=(3, 5), name='pail_back')
_PAIL_FRONT = Sprite(['sSSSSsN',
                      '.ssssN.',
                      '.NNNNN.',
                      '.ssssN.'], anchor=(3, 3), name='pail_front')

# a compact "!" in the library's style (the library one is 8 rows: too tall above the bucket hat), in
# GOLD: a game-like "bite!" cue that cannot be mistaken for the red "!" of the alert (permission) state.
# Anchor = the left cell of its dot (placed one row clear of the hat). It springs up: short, then full.
_BANG_SHORT = Sprite(['jJ',
                      'jJ',
                      '..',
                      'jJ'], anchor=(0, 3), name='bang_short')
_BANG = Sprite(['jJ',
                'jJ',
                'jJ',
                'jJ',
                '..',
                'jJ'], anchor=(0, 5), name='bang')
# burst ticks fanning out from the top of the "!" (same anchor)
_TICKS = Sprite(['j......j',
                 '.j....j.',
                 '........',
                 '........',
                 '........',
                 '........'], anchor=(3, 5), name='bang_ticks')


# landing dust hugging his feet (anchor = feet centre on row 19). Local and narrower than the library
# dust_puff, whose left puff would land on the pail.
_DUST = [
    Sprite(['.t...........t.',
            'tTT.........TTt'], anchor=(7, 1), name='dust_land'),
    Sprite(['t.............t',
            '.t...........t.',
            '...............'], anchor=(7, 2), name='dust_drift'),
]


def _rot_cw(s):
    return Sprite(cells=[(-y, x, ch) for x, y, ch in s.cells], anchor=(-s.ay, s.ax), name=s.name)


def _rot_ccw(s):
    return Sprite(cells=[(y, -x, ch) for x, y, ch in s.cells], anchor=(s.ay, -s.ax), name=s.name)


def _fish_sprites():
    """The library fish turned along its flight arc. It rotates counter-clockwise the whole way, so its
    dorsal fin stays on the outside of the arc and the cyan belly on the inside."""
    lib = get('fish')
    left = [lib.sprite(0), lib.sprite(1)]
    # 45 deg, heading up-left (hand-drawn: a rotated 8x4 sprite loses its head and tail at this size)
    ul = Sprite(['.bb.....',
                 'bkbbB...',
                 'bbbbbB..',
                 '.cbbbb..',
                 '..cbbbB.',
                 '...cbB..',
                 '....B.B.',
                 '.....B..'], anchor=(3, 3), name='fish_ul')
    return {
        'L': left[0], 'L2': left[1],          # level (L2 = the library's tail flick)
        'UP': _rot_cw(left[0]),               # head up (mouth 3 rows above the anchor)
        'UL': ul,
        'DL': _rot_ccw(ul),                   # heading down-left
        'DOWN': _rot_ccw(left[0]),            # head down, diving into the pail
    }


def _catch():
    """The earlier catch lying in the pail: the library fish, level, facing out (eye on the left), its
    forked tail hanging over the rim toward him. Its body is static (pail layer); only the tail flaps
    (fish layer): 'rest' = the library's frame 0 tail, 'flick' = its frame 1 tail (flipped up)."""
    lib = get('fish')
    f0, f1 = lib.sprite(0), lib.sprite(1)
    split = f0.x1 - 1                         # the tail = the fish's two rear columns (it faces left)
    body = Sprite(cells=[c for c in f0.cells if c[0] < split], anchor=(f0.ax, f0.ay), name='catch_body')
    # the tail in the body's blue, not navy: at rest it is the still's key "fish!" cue, and navy is only
    # ~2:1 on the dark theme (in flight the library's navy tail is fine: it is moving and seen whole)
    tails = {k: Sprite(cells=[(x, y, 'b') for x, y, ch in f.cells if x >= split], anchor=(f.ax, f.ay), name='catch_' + k)
             for k, f in (('rest', f0), ('flick', f1))}
    return body, tails


def _hat():
    lib = get('fishing_hat')
    h = lib.sprite(0)
    # keep the green bucket hat, drop the little lure hanging off its brim (anything outside his 11-wide
    # box): the real bobber is on his line, and a second one right above the pail reads as clutter.
    # Instead an angler's fly (red body, steel hook) is pinned on the band, as real anglers do: on the
    # band's (the hat's longest dark-wood row) 3rd and 2nd cells from the right.
    cells = [c for c in h.cells if 0 <= c[0] <= 10]
    rows = {}
    for x, y, ch in cells:
        if ch == 'd':
            rows.setdefault(y, []).append(x)
    if rows:
        by = max(rows, key=lambda y: len(rows[y]))
        band = sorted(rows[by])
        if len(band) >= 5:
            fly = {(band[-3], by): 'r', (band[-2], by): 's'}
            cells = [c for c in cells if (c[0], c[1]) not in fly] + [(x, y, ch) for (x, y), ch in fly.items()]
    return Item('fishing_hat', 'head', lib.desc, Sprite(cells=cells, anchor=(h.ax, h.ay), name='fishing_hat'))


def _mouth_gap(spr):
    """Offset from the anchor to the cell just above the head of a head-up fish (where the line ends)."""
    x, y, _ = min(spr.cells, key=lambda c: (c[1], abs(c[0] - spr.ax)))
    return x - spr.ax, y - spr.ay - 1


# =====================================================================================================
# drawing (one function per layer; every layer is cut from the same beat list, so they stay in sync)
# =====================================================================================================
def _put_clip(f, spr, x, y, ymax=GROUND):
    """Place a sprite but drop its cells below row ymax: below the water line (19) they are under water;
    inside the pail (below its back rim's water, row 15) they are behind the pail's front."""
    for sx, sy, ch in spr.cells:
        X, Y = x + sx - spr.ax, y + sy - spr.ay
        if Y <= ymax:
            f.put(X, Y, ch)


def _seg(x0, y0, x1, y1):
    """Bresenham points from (x0, y0) to (x1, y1), both ends included."""
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def _where(st):
    """(pose, box x, box y, grip, rod tip) for a state."""
    p = clawd(eyes=st['eyes'], larm=st['larm'], rarm=_RODS[st['rod']][2], legs=st['legs'])
    x, y = HOME[0], HOME[1] + st['dy']
    gx, gy = p.at('hand_r', x, y)
    off = _RODS[st['rod']][1]
    return p, x, y, (gx, gy), (gx + off[0], gy + off[1])


def _bob_pos(st, tip):
    """Where the bobber's nub (top) is."""
    b = st['bob']
    k = b[0]
    if k == 'float':
        return (BX, 17)             # resting on the water: its white half sits on row 19
    if k == 'dip':
        return (BX, 18)             # white half under water
    if k == 'under':
        return (BX, 19)             # pulled under: only the nub shows
    if k == 'high':
        return (BX, 16)             # popped up out of the water (overshoot after the plop)
    if k == 'hang':
        return (tip[0] + b[1], tip[1] + b[2])
    if k in ('at', 'hooked'):
        return (b[1], b[2])
    raise ValueError(b)


def _ripple(f, stage):
    """Ripple dashes on the water line around the bobber: A = fresh ring, B = spreading, C = fading."""
    xs = {'A': (BX - 2, BX + 2), 'B': (BX - 4, BX - 3, BX + 3, BX + 4), 'C': (BX - 4, BX + 4)}.get(stage, ())
    for X in xs:
        f.put(X, GROUND, 'c')


# water drops (dx from the fishing spot, y) and pail drops (dx from the pail centre, y)
_WSPLASH = {
    'bite0': [(-2, 18), (2, 18), (-1, 17), (1, 17)],
    'bite1': [(-3, 17), (3, 17), (-2, 16), (2, 16)],
    'yank0': [(-2, 17), (2, 17), (-1, 16), (1, 16), (-3, 18), (3, 18)],
    'yank1': [(-3, 15), (3, 15), (-2, 14), (2, 13), (-4, 17), (4, 17)],
    'yank2': [(-4, 16), (4, 15), (3, 13)],
    'yank3': [(-4, 18), (4, 18)],
    'plop0': [(-1, 18), (1, 18), (0, 17)],
    'plop1': [(-2, 17), (2, 17), (-1, 16), (1, 16)],
    'plop2': [(-3, 18), (3, 18)],
}
_BSPLASH = {                       # around the catch, never on it, so the fish always reads whole
    'flap': [(3, 10)],                                        # the tail flicks a drop up ...
    'flap2': [(4, 9)],                                        # ... it arcs away
    'b0': [(-3, 11), (2, 11)],                                # the dive: drops at the pail's mouth
    'b1': [(-3, 9), (3, 9), (-2, 8), (2, 7), (0, 8)],         # the splash flies up ...
    'b2': [(-3, 11), (4, 10), (-2, 10), (2, 9)],              # ... and falls back
}


def _draw_rod(f, st, p, x, y):
    """The rod, drawn over the line and bobber (so the bobber passes behind it on the wind-up)."""
    wear(f, _RODS[st['rod']][0], p, x, y)


def _line_frame(st, glint, fish, spark):
    """Fishing line, bobber, hook, ripples and water splashes (they always change together), the rod over
    them (it only ever changes on these beats), the hooked fish over the rod, and the one-shot effects
    ("!", sparkles, dust): they change on line beats and never overlap a later layer."""
    f = Frame()
    p, x, y, grip, tip = _where(st)
    _ripple(f, st['rip'])
    for dx, yy in _WSPLASH.get(st['wsplash'], ()):
        f.put(BX + dx, yy, 'c')
    nub = _bob_pos(st, tip)
    for px, py in _seg(tip[0], tip[1], nub[0], nub[1])[1:-1]:        # rod tip -> bobber
        if py <= GROUND:
            f.put(px, py, 'm')
    _put_clip(f, _BOB, nub[0], nub[1])
    kind = st['bob'][0]
    if kind == 'hooked':                     # bobber -> right above the fish's mouth, taut
        _, fx, fy, orient = st['fish']
        mx, my = _mouth_gap(fish[orient])
        for px, py in _seg(nub[0], nub[1] + 3, fx + mx, fy + my):
            f.put(px, py, 'm')
    elif kind == 'hang' and st['hook']:      # the bare hook dangles one line cell under the bobber
        f.put(nub[0], nub[1] + 3, 'm')
        f.place(_HOOK, nub[0], nub[1] + 4)
        if st['glint'] is not None:          # "hook!": a glint pings off the outside of its bend. The plus
            g = st['glint']                  # sits 2 right / 1 below the bend, the x one row lower: neither
            f.place(glint.sprite(g), nub[0] + 1, nub[1] + 6 + g)    # ever touches the J (eye/shank/bend/point)
    _draw_rod(f, st, p, x, y)
    if kind == 'hooked':                     # the hooked fish rides the line (yank beats: the line changes
        _, fx, fy, orient = st['fish']       # anyway), clipped at the water line, in front of the rod
        _put_clip(f, fish[orient], fx, fy)
    # effects
    if st['bang'] is not None:                              # dot on row 6: one clear row above the hat
        f.place(_BANG_SHORT if st['bang'] == 0 else _BANG, 15, 6)
        if st['bang'] == 1:
            f.place(_TICKS, 15, 6)
    if st['spark'] is not None:
        f.place(spark.sprite(st['spark']), BKX, 5)          # over the pail (clear of the catch): nice catch!
    if st['dust'] is not None:
        f.place(_DUST[st['dust']], 15, GROUND)
    return f


def _fish_frame(st, fish, tails, catch_cells):
    f = Frame()
    if st['fish'] and st['fish'][0] == 'fly':           # (the hooked fish is drawn by the line layer)
        kind, x, y, orient = st['fish']
        # head-first into the pail: below its back rim's water the fish is inside, behind the front lip;
        # and it slips in BEHIND the catch lying across the pail's mouth (never over its eye or fins)
        spr = fish[orient]
        _put_clip(f, Sprite(cells=[c for c in spr.cells if (x + c[0] - spr.ax, y + c[1] - spr.ay) not in catch_cells],
                            anchor=(spr.ax, spr.ay)), x, y, 15 if orient == 'DOWN' else GROUND)
    if st['tail']:
        f.place(tails[st['tail']], CATCH[0], CATCH[1])
    for dx, yy in _BSPLASH.get(st['bsplash'], ()):
        f.put(BKX + dx, yy, 'c')
    return f


def _body_frame(st):
    f = Frame()
    p, x, y, grip, tip = _where(st)
    put_clawd(f, p, x, y)
    return f


def _hat_frame(st, hat):
    f = Frame()
    p, x, y, grip, tip = _where(st)
    wear(f, hat, p, x, y, dy=st['hat'])                     # st['hat'] = lag in rows (follow-through)
    return f


# =====================================================================================================
# the master beat list: (ms, changes). State carries over from beat to beat.
# =====================================================================================================
S0 = dict(eyes='look_r', larm='side', legs='stand', dy=0, hat=0, rod='rest', bob=('float',), rip='B',
          hook=False, glint=None, fish=None, tail='rest', bang=None, wsplash=None, bsplash=None, spark=None,
          dust=None)

# the fish's flight: ballistic arc from the fishing spot over his head into the pail (x, y, facing);
# x steps ~3 per frame (vertical spacing ballistic: fast at the ends, hanging at the apex)
_ARC = [(23, 9, 'UL'), (20, 6, 'UL'), (17, 4, 'L'), (14, 3, 'L2'), (11, 4, 'L'), (9, 6, 'DL'),
        (6, 10, 'DL'), (4, 14, 'DOWN')]


def _fly(i):
    return ('fly',) + _ARC[i]


BEATS = [
    # ---- A: calm fishing (frame 0); the catch flaps its tail; two nibbles (rod tip twitches along)
    (430, {}),
    (80, dict(tail='flick', bsplash='flap')),
    (80, dict(tail='rest', bsplash='flap2', eyes='look_l')),  # he glances at it (left arm closes the hole) ...
    (80, dict(tail='flick', bsplash=None)),
    (120, dict(tail='rest')),
    (110, dict(bob=('dip',), rip='A', rod='flex')),           # ... and misses the first nibble entirely ...
    (230, dict(bob=('float',), rip='B', rod='rest')),
    (80, dict(bob=('dip',), rip='A', rod='flex', eyes='look_d')),   # ... nibble: his eyes snap onto the bobber
    (130, dict(bob=('float',), rip='B', rod='rest')),
    # ---- B: BITE!
    (90, dict(bob=('under',), rip='A', rod='bite', wsplash='bite0', bang=0, eyes='look_dr')),   # eyes follow it
    (120, dict(rod='bite2', wsplash='bite1', bang=1, rip='B')),
    (110, dict(rod='bite', wsplash=None, bang=2, rip='C')),
    # ---- C: the yank (the bobber rides the taut line, the fish hangs right below it)
    (60, dict(rod='yank1', bang=None, bob=('hooked', BX, 11), fish=('hook', BX, 18, 'UP'), wsplash='yank0',
              rip='A', eyes='look_ur', larm='out')),          # the free arm flings out for balance
    (70, dict(rod='yank2', bob=('hooked', BX - 1, 7), fish=('hook', BX - 1, 14, 'UP'), wsplash='yank1', rip='B',
              larm='up', eyes='look_u')),
    # ---- D: the flight (the line snaps up over the tip, the bobber drops and swings, the bare hook glints)
    (70, dict(rod='up', fish=_fly(0), wsplash='yank2', bob=('hang', 3, -2))),
    (70, dict(fish=_fly(1), wsplash='yank3', rip='C', bob=('hang', 2, 3), hook=True, glint=1)),   # ping!
    (80, dict(fish=_fly(2), bob=('hang', 3, 3), glint=2)),                       # pendulum: swings out ...
    (90, dict(fish=_fly(3), bob=('hang', 2, 3), glint=None, wsplash=None, rip=None)),   # ... and back
    (80, dict(fish=_fly(4), eyes='look_ul')),
    (70, dict(fish=_fly(5))),
    (70, dict(fish=_fly(6), eyes='look_l', larm='side')),
    (70, dict(fish=_fly(7), eyes='look_dl', bsplash='b0')),                      # dives into the pail
    # ---- E: the catch flaps in the pail while he lowers the rod (the bobber swings past plumb and back),
    #         then the happy hop
    (100, dict(fish=None, tail='flick', bsplash='b1', rod='mid', bob=('hang', 1, 3))),   # rod down: mid ...
    (110, dict(tail='rest', bsplash='b2')),
    (100, dict(tail='flick', bsplash=None, rod='rest', bob=('hang', 1, 3),      # ... rest; the bobber swings
               eyes='open', larm='down')),                    # past plumb; he turns to us, arm down
    (100, dict(tail='rest')),
    (80, dict(dy=-2, legs='short', larm='raise', bob=('hang', 0, 5))),  # hop! the bobber swings back to
                                                                        # plumb, lagging the tip by 2 rows
    (110, dict(larm='wave', spark=1, bob=('hang', 0, 2))),               # apex: slack line, it floats up
    (60, dict(dy=-1, larm='out', hat=-1, bob=('hang', 0, 1))),           # falling: hat + bobber float behind
    (100, dict(dy=0, legs='stand', dust=0, spark=2, bob=('hang', 0, 1))),   # land: hat, bobber still up
    (120, dict(hat=0, larm='side', dust=1, spark=3, eyes='blink', bob=('hang', 0, 4))),  # both drop; bounce
    # ---- F: recast
    (190, dict(dust=None, spark=None, eyes='look_r', bob=('hang', 0, 3))),
    (70, dict(rod='up', eyes='look_u', bob=('hang', 2, 3))),  # wind-up: the rod sweeps up, eyes with it ...
    (90, dict(rod='back', hook=False, bob=('at', 18, 2))),    # ... back (hook reeled in): the bobber trails
                                                              # over the top ...
    (160, dict(bob=('at', 11, 5))),                           # ... and hangs back behind him
    (60, dict(rod='up', bob=('at', 18, 1))),                  # whip: it lags behind the tip (still overhead) ...
    (70, dict(rod='rest', eyes='look_r', bob=('at', 28, 5))),    # ... then sails out ahead: eyes follow it
    (70, dict(rod='flex', bob=('at', 28, 8))),               # the line tugs the tip down; it falls ...
    (60, dict(bob=('at', 27, 13))),                           # ... faster
    (80, dict(rod='rest', bob=('under',), wsplash='plop0', rip='A')),     # plop; the tip springs back
    (110, dict(bob=('high',), wsplash='plop1', rip='B')),     # pops up too high ...
    (130, dict(bob=('dip',), wsplash='plop2', rip='A')),      # ... dips, then floats = frame 0
]


def _states():
    st = dict(S0)
    out = []
    for ms, ch in BEATS:
        st = dict(st, **ch)
        out.append((ms, dict(st)))
    return out


def build():
    hat, fish = _hat(), _fish_sprites()
    body, tails = _catch()
    spark, glint = get('sparkle'), get('sparkle_small')
    seq = _states()
    pail = Frame()
    pail.place(_PAIL_BACK, BKX, GROUND)
    pail.place(body, CATCH[0], CATCH[1])
    pail.place(_PAIL_FRONT, BKX, GROUND)
    catch_cells = {(CATCH[0] + cx - body.ax, CATCH[1] + cy - body.ay) for cx, cy, _ in body.cells}
    layers = [
        static('pail', pail),
        layer('line', [(_line_frame(s, glint, fish, spark), ms) for ms, s in seq]),
        layer('fish', [(_fish_frame(s, fish, tails, catch_cells), ms) for ms, s in seq]),
        layer('body', [(_body_frame(s), ms) for ms, s in seq]),
        layer('hat', [(_hat_frame(s, hat), ms) for ms, s in seq]),
    ]
    return anim(NAME, DESC, layers, state=STATE)
