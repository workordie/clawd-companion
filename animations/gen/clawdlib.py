"""
clawdlib - pixel-art toolkit for the Clawd animations.  Python 3.9 compatible (no match/case, no X|Y types).

Coordinates: x grows right, y grows down, (0, 0) is the top-left cell of the 32 x 20 canvas.
Clawd's body box is 11 x 8 cells; at rest its top-left is HOME = (10, 12) and his feet stand on the
bottom row (y = 19). The Claude Code input box's top border is directly below row 19.

Quick tour (see STYLE.md for the rules and anims/_example.py for a complete animation):

    from clawdlib import *
    from acc import get                      # accessory library: get('party_hat') -> Item
    f = Frame()
    p = clawd(eyes='happy', rarm='raise')    # a Pose: sprite + anchor points (head, face, hand_r ...)
    put_clawd(f, p)                          # at HOME; put_clawd(f, p, x, y) to move him
    wear(f, get('party_hat'), p)             # attaches to his head, follows wherever p was placed
    f.place(get('sparkle').sprite(0), 25, 8) # free placement: sprite anchor lands on (25, 8)
    layer('body', [(f, 400), (f2, 120)])     # frames + durations (ms) -> layer dict
"""
import math

# --------------------------------------------------------------------------------------------
# Canvas
# --------------------------------------------------------------------------------------------
W, H = 32, 20
SCALE = 3                 # default CSS px per cell in the exported SVG (96 x 60 px)
HOME = (10, 12)           # top-left of Clawd's 11x8 box when standing at home
GROUND = H - 1            # bottom row (y = 19): what Clawd stands on

# --------------------------------------------------------------------------------------------
# Palette: one character per color. '.', ' ' (transparent) and '_' (erase) are reserved.
# Never add colors in your own module; use these.
# --------------------------------------------------------------------------------------------
PALETTE = {
    # Clawd
    '#': ('body', '#D97757'),          # official Clawd orange (flat; his body is never shaded by default)
    '@': ('body_shade', '#B65B3E'),    # limb in front of the body / rare shadow on Clawd
    '%': ('body_light', '#EC9A7C'),    # rare highlight on Clawd
    'e': ('ink_brown', '#3A1C13'),     # lines drawn ON Clawd: closed eyes, brows, mouths
    # neutrals
    'k': ('ink', '#17151B'),
    'K': ('charcoal', '#2F2B35'),
    'n': ('graphite', '#4F4A57'),
    'N': ('gray', '#78737F'),
    'm': ('silver', '#A6A2AD'),
    'M': ('light_gray', '#CDC9D3'),
    'w': ('paper', '#ECE7DF'),
    'W': ('white', '#FFFFFF'),
    # reds / pinks
    'r': ('red', '#E5484D'),
    'R': ('dark_red', '#A32A2F'),
    'p': ('pink', '#FF7EA1'),
    'P': ('light_pink', '#FFC4D4'),
    # oranges / yellows / golds
    'o': ('orange', '#F58A35'),
    'O': ('rust', '#B4561B'),
    'y': ('yellow', '#FFCC47'),
    'Y': ('pale_yellow', '#FFEBA6'),
    'j': ('gold', '#E0A42C'),
    'J': ('dark_gold', '#A06C16'),
    # greens
    'g': ('green', '#3FB37A'),
    'G': ('dark_green', '#257352'),
    'h': ('mint', '#9DEBC2'),
    'a': ('lime', '#B8E15A'),
    # blues
    'b': ('blue', '#4D8BF0'),
    'B': ('navy', '#2A4BA3'),
    'c': ('cyan', '#43C6E0'),
    'C': ('ice', '#B8EEF8'),
    'i': ('night', '#1E2756'),
    # purples
    'v': ('violet', '#8B6CFF'),
    'V': ('deep_violet', '#5A3EC2'),
    'l': ('lavender', '#B9A8FF'),
    'L': ('pale_lilac', '#E0D8FF'),
    # browns
    't': ('tan', '#D6A770'),
    'T': ('wood', '#9C6537'),
    'd': ('dark_wood', '#5C3920'),
    # metals
    's': ('steel', '#8C93A3'),
    'S': ('chrome', '#D3D8E2'),
}
HEX = {c: v[1] for c, v in PALETTE.items()}
COLOR = {v[0]: c for c, v in PALETTE.items()}      # COLOR['gold'] -> 'j'
TRANSPARENT = '. '
ERASE = '_'
# USER PREFERENCE: Clawd's eyes are BLACK (ink), not see-through holes. The kit draws eye holes in
# EYE_INK, and layer() fills any small hole enclosed by Clawd's body with EYE_INK as a safety net.
EYES_BLACK = True
EYE_INK = 'k'
STATS = {'clipped': 0}                             # pixels drawn outside the canvas (lint reports it)


def rgb(ch):
    h = HEX[ch]
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


# --------------------------------------------------------------------------------------------
# Sprite
# --------------------------------------------------------------------------------------------
class Sprite:
    """A pixel sprite.

    rows   : list of strings of palette chars; '.' or ' ' = transparent; '_' = erase (punches a hole
             through whatever is already drawn, e.g. Clawd's eyes).
    anchor : (ax, ay) the sprite cell (it may lie outside the drawn pixels) that lands exactly on the
             target point when placed with Frame.place(sprite, x, y) or wear().
    """

    def __init__(self, rows=None, anchor=(0, 0), name='', cells=None):
        self.name = name
        if cells is None:
            cells = []
            for y, row in enumerate(rows or []):
                for x, ch in enumerate(row):
                    if ch in TRANSPARENT:
                        continue
                    if ch != ERASE and ch not in HEX:
                        raise ValueError('%s: unknown color %r at (%d,%d)' % (name or 'sprite', ch, x, y))
                    cells.append((x, y, ch))
        self.cells = list(cells)
        self.ax, self.ay = anchor
        if self.cells:
            xs = [c[0] for c in self.cells]
            ys = [c[1] for c in self.cells]
            self.x0, self.x1, self.y0, self.y1 = min(xs), max(xs), min(ys), max(ys)
        else:
            self.x0 = self.x1 = self.y0 = self.y1 = 0

    @property
    def w(self):
        return self.x1 - self.x0 + 1 if self.cells else 0

    @property
    def h(self):
        return self.y1 - self.y0 + 1 if self.cells else 0

    def flipped(self):
        """Mirror left/right around the sprite's own bounds (anchor mirrors too)."""
        c = self.x0 + self.x1
        return Sprite(cells=[(c - x, y, ch) for x, y, ch in self.cells], anchor=(c - self.ax, self.ay), name=self.name)

    def vflipped(self):
        c = self.y0 + self.y1
        return Sprite(cells=[(x, c - y, ch) for x, y, ch in self.cells], anchor=(self.ax, c - self.ay), name=self.name)

    def recolor(self, mapping):
        """mapping: {old_char: new_char}"""
        return Sprite(cells=[(x, y, mapping.get(ch, ch)) for x, y, ch in self.cells], anchor=(self.ax, self.ay), name=self.name)

    def moved(self, dx, dy):
        """Shift the pixels relative to the anchor (the anchor stays put)."""
        return Sprite(cells=[(x + dx, y + dy, ch) for x, y, ch in self.cells], anchor=(self.ax, self.ay), name=self.name)

    def with_anchor(self, ax, ay):
        return Sprite(cells=self.cells, anchor=(ax, ay), name=self.name)

    def over(self, other):
        """Union with `other` drawn on top (other's coordinates are in this sprite's space)."""
        d = {(x, y): ch for x, y, ch in self.cells}
        for x, y, ch in other.cells:
            d[(x, y)] = ch
        return Sprite(cells=[(x, y, ch) for (x, y), ch in d.items()], anchor=(self.ax, self.ay), name=self.name)

    def rows(self):
        """Back to strings (bounds of the drawn pixels; anchor is not shown)."""
        grid = [['.'] * self.w for _ in range(self.h)]
        for x, y, ch in self.cells:
            grid[y - self.y0][x - self.x0] = ch
        return [''.join(r) for r in grid]

    def __repr__(self):
        return 'Sprite(%r %dx%d anchor=(%d,%d))' % (self.name, self.w, self.h, self.ax, self.ay)


def outlined(spr, ch, diagonal=False):
    """Add a 1-cell outline of color `ch` around the sprite (helps contrast on both themes)."""
    occupied = {(x, y) for x, y, c in spr.cells if c != ERASE}
    ring = set()
    nbrs = [(1, 0), (-1, 0), (0, 1), (0, -1)] + ([(1, 1), (1, -1), (-1, 1), (-1, -1)] if diagonal else [])
    for x, y in occupied:
        for dx, dy in nbrs:
            q = (x + dx, y + dy)
            if q not in occupied:
                ring.add(q)
    return Sprite(cells=[(x, y, ch) for x, y in ring] + list(spr.cells), anchor=(spr.ax, spr.ay), name=spr.name)


# --------------------------------------------------------------------------------------------
# Frame
# --------------------------------------------------------------------------------------------
class Frame:
    """One full 32x20 picture. Later drawing goes on top. Pixels outside the canvas are clipped.
    res=2 makes a FINE frame: 64x40 half-size pixels (use fine(frame) to convert a normal frame and
    fine_face() to draw delicate expressions; see STYLE.md section 0b)."""

    def __init__(self, px=None, res=1):
        self.px = dict(px) if px else {}
        self.meta = {}
        self.res = res

    def put(self, x, y, ch):
        if not (0 <= x < W * self.res and 0 <= y < H * self.res):
            STATS['clipped'] += 1
            return self
        if ch == ERASE:
            self.px.pop((x, y), None)
        else:
            if ch not in HEX:
                raise ValueError('unknown color %r' % ch)
            self.px[(x, y)] = ch
        return self

    def get(self, x, y):
        return self.px.get((x, y), '.')

    def place(self, spr, x, y, flip=False):
        """Draw `spr` so that its anchor cell lands on (x, y)."""
        if flip:
            spr = spr.flipped()
        for sx, sy, ch in spr.cells:
            self.put(x + sx - spr.ax, y + sy - spr.ay, ch)
        return self

    def rect(self, x, y, w, h, ch):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, ch)
        return self

    def hline(self, x0, x1, y, ch):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            self.put(x, y, ch)
        return self

    def vline(self, x, y0, y1, ch):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            self.put(x, y, ch)
        return self

    def line(self, x0, y0, x1, y1, ch):
        """Bresenham line (pixel-perfect, no doubles)."""
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.put(x0, y0, ch)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return self

    def text(self, s, x, y, ch, spacing=1):
        """3x5 pixel font (A-Z 0-9 and ! ? : . - + / % < > = ( ) _ space). Returns the width drawn."""
        cx = x
        for c in s.upper():
            g = FONT.get(c)
            if g is None:
                raise ValueError('no glyph for %r' % c)
            for gy, row in enumerate(g):
                for gx, bit in enumerate(row):
                    if bit == '1':
                        self.put(cx + gx, y + gy, ch)
            cx += 3 + spacing
        return cx - x - spacing

    def shifted(self, dx, dy):
        Wr, Hr = W * self.res, H * self.res
        f = Frame({(x + dx, y + dy): c for (x, y), c in self.px.items() if 0 <= x + dx < Wr and 0 <= y + dy < Hr}, res=self.res)
        f.meta = dict(self.meta)
        return f

    def copy(self):
        f = Frame(self.px, res=self.res)
        f.meta = {k: (list(v) if isinstance(v, list) else set(v) if isinstance(v, set) else v) for k, v in self.meta.items()}
        return f

    def over(self, other):
        """New frame: this one with `other` drawn on top (other is converted to this frame's res)."""
        f = self.copy()
        if other.res != f.res:
            other = fine(other) if f.res == 2 else other
        f.px.update(other.px)
        return f

    def rows(self):
        return [''.join(self.px.get((x, y), '.') for x in range(W * self.res)) for y in range(H * self.res)]

    @staticmethod
    def from_rows(rows, res=1):
        f = Frame(res=res)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch not in TRANSPARENT:
                    f.put(x, y, ch)
        return f


# --------------------------------------------------------------------------------------------
# Clawd body kit
# --------------------------------------------------------------------------------------------
# Body geometries (all inside/around the 11x8 box; feet always end on box row 7 except 'stretch').
#   bx: body columns, by: body rows, ey: eye row, ex: eye columns (left, right), ax: arm columns,
#   ay: top row of a resting arm, legs: leg columns, ly: first leg row, ll: leg length.
GEOM = {
    'normal':  dict(bx=(1, 9), by=(0, 5), ey=2, ex=(2, 8), ax=(0, 10), ay=2, legs=(1, 3, 7, 9), ly=6, ll=2),
    'crouch':  dict(bx=(1, 9), by=(1, 6), ey=3, ex=(2, 8), ax=(0, 10), ay=3, legs=(1, 3, 7, 9), ly=7, ll=1),
    'squash':  dict(bx=(0, 10), by=(2, 6), ey=4, ex=(2, 8), ax=(-1, 11), ay=4, legs=(1, 3, 7, 9), ly=7, ll=1),
    'stretch': dict(bx=(2, 8), by=(-1, 5), ey=1, ex=(3, 7), ax=(1, 9), ay=1, legs=(2, 4, 6, 8), ly=6, ll=2),
}

# Arm shapes for the RIGHT arm, relative to (arm column, ay). The left arm mirrors dx.
# A third element is the color (default body '#'; '@' = limb drawn in front of the body).
ARMS = {
    'side':  [(0, 0), (0, 1)],
    'up':    [(0, -1), (0, 0)],
    'down':  [(0, 1), (0, 2)],
    'high':  [(0, 0), (0, -1), (0, -2)],
    'raise': [(0, 0), (1, -1), (1, -2)],
    'wave':  [(0, 0), (1, -1), (2, -2)],
    'out':   [(0, 0), (1, 0)],
    'point': [(0, 0), (1, 0), (2, 0)],
    'chin':  [(0, 1), (-1, 2, '@'), (-2, 2, '@'), (-3, 1, '@')],
    'front': [(0, 1), (-1, 1, '@')],
    'none':  [],
}
# Where a held item's grip lands for each arm shape (relative to (arm column, ay), right arm).
HAND = {
    'side': (1, 1), 'up': (1, -1), 'down': (1, 2), 'high': (0, -3), 'raise': (1, -3), 'wave': (2, -3),
    'out': (2, 0), 'point': (3, 0), 'chin': (-4, 1), 'front': (-2, 1), 'none': (1, 1),
}


def _sym(cells):
    return (list(cells), [(-dx, dy, ch) for dx, dy, ch in cells])


def _same(cells):
    return (list(cells), list(cells))


# Eye patterns: (left-eye cells, right-eye cells), relative to each eye's center. '_' = hole.
EYES = {
    'open':    _sym([(0, 0, '_')]),
    'blink':   _sym([]),
    'closed':  _sym([(-1, 0, 'e'), (0, 0, 'e')]),
    'happy':   _sym([(-1, 1, '@'), (0, 0, 'e'), (1, 1, '@')]),   # user: keep happy eyes small (dark peak, soft sides)
    'sleepy':  _sym([(-1, 0, '@'), (0, 1, 'e'), (1, 0, '@')]),   # same soft treatment as happy
    'tired':   _sym([(-1, -1, 'e'), (0, -1, 'e'), (0, 0, '_')]),
    'wide':    _sym([(0, -1, '_'), (0, 0, '_')]),
    'squint':  _sym([(-1, 0, '_'), (0, 0, '_')]),
    'angry':   _sym([(0, 0, '_'), (1, -1, 'e')]),
    'sad':     _sym([(0, 1, '_'), (-1, -1, 'e')]),
    'look_l':  _same([(-1, 0, '_')]),
    'look_r':  _same([(1, 0, '_')]),
    'look_u':  _sym([(0, -1, '_')]),
    'look_d':  _sym([(0, 1, '_')]),
    'look_ul': _same([(-1, -1, '_')]),
    'look_ur': _same([(1, -1, '_')]),
    'look_dl': _same([(-1, 1, '_')]),
    'look_dr': _same([(1, 1, '_')]),
    'x':       _sym([(-1, -1, 'e'), (1, -1, 'e'), (0, 0, 'e'), (-1, 1, 'e'), (1, 1, 'e')]),
    'hearts':  _sym([(-1, -1, 'p'), (1, -1, 'p'), (-1, 0, 'p'), (0, 0, 'p'), (1, 0, 'p'), (0, 1, 'p')]),
    'stars':   _sym([(0, -1, 'y'), (-1, 0, 'y'), (0, 0, 'Y'), (1, 0, 'y'), (0, 1, 'y')]),
    'wink':    ([(-1, 0, 'e'), (0, 0, 'e')], [(0, 0, '_')]),
}
# Mouths, relative to the mouth point (body center column, eye row + 2). Default: no mouth (official look).
MOUTHS = {
    None:    [],
    'o':     [(0, 0, 'e')],
    'yawn':  [(0, -1, 'e'), (0, 0, 'e')],
    'smile': [(-1, -1, 'e'), (0, 0, 'e'), (1, -1, 'e')],
    'grin':  [(-2, -1, 'e'), (-1, 0, 'e'), (0, 0, 'e'), (1, 0, 'e'), (2, -1, 'e')],
    'flat':  [(-1, 0, 'e'), (0, 0, 'e'), (1, 0, 'e')],
    'frown': [(-1, 0, 'e'), (0, -1, 'e'), (1, 0, 'e')],
    'cat':   [(-2, -1, 'e'), (-1, 0, 'e'), (0, -1, 'e'), (1, 0, 'e'), (2, -1, 'e')],
}
LEG_STYLES = ('stand', 'short', 'long', 'walk_a', 'walk_b', 'none')

# USER PREFERENCE (STYLE.md section 0): the plain, official face only. These eye styles are allowed;
# anything else (happy/sleepy arches, x, hearts, stars, wink, tired, angry, sad, wide, squint) is
# replaced by a plain equivalent, and mouths + blush are switched off. Lint reports the requests.
USER_EYES = ('open', 'blink', 'closed', 'look_l', 'look_r', 'look_u', 'look_d',
             'look_ul', 'look_ur', 'look_dl', 'look_dr')
EYE_FALLBACK = {'happy': 'open', 'sleepy': 'closed', 'tired': 'closed', 'x': 'look_d', 'sad': 'look_d',
                'hearts': 'open', 'stars': 'open', 'wink': 'open', 'angry': 'open', 'wide': 'open',
                'squint': 'open'}


class Pose:
    """Clawd's sprite (anchored at his box's top-left) plus named anchor points (relative to the box).

    anchors: head (top-center pixel of his head), face (between the eyes), eye_l, eye_r, mouth,
             neck (center, 2 rows below the eyes), body (center), feet (bottom pixel row, center),
             hand_r / hand_l (where a held item's grip goes).
    """

    def __init__(self, sprite, anchors, spec=None):
        self.sprite = sprite
        self.anchors = dict(anchors)
        self.spec = dict(spec or {})

    def at(self, key, x=None, y=None):
        """Absolute canvas position of an anchor when the box's top-left is at (x, y) (default HOME)."""
        if x is None:
            x, y = HOME
        ax, ay = self.anchors[key]
        return (x + ax, y + ay)

    def mirrored(self):
        """Mirror left/right around the box center. Anchors keep screen meaning:
        hand_r is still the hand on the screen-right side after mirroring."""
        spr = Sprite(cells=[(10 - x, y, ch) for x, y, ch in self.sprite.cells], anchor=(0, 0), name=self.sprite.name)
        a = {k: (10 - ax, ay) for k, (ax, ay) in self.anchors.items()}
        a['hand_r'], a['hand_l'] = a['hand_l'], a['hand_r']
        a['eye_l'], a['eye_r'] = a['eye_r'], a['eye_l']
        return Pose(spr, a, dict(self.spec, mirrored=True))

    @staticmethod
    def from_rows(rows, anchors=None, name='custom'):
        """Hand-drawn Clawd variant (11-wide box rows; may extend outside with care).
        anchors default to the normal standing pose's anchors."""
        base = clawd().anchors
        if anchors:
            base.update(anchors)
        return Pose(Sprite(rows, anchor=(0, 0), name=name), base, {'custom': True})


def clawd(eyes='open', larm='side', rarm='side', legs='stand', body='normal', mouth=None,
          blush=False, holes=True, color='#'):
    """Build a Clawd pose.

    eyes : see EYES (open blink closed happy sleepy tired wide squint angry sad look_* x hearts stars wink)
    larm, rarm : see ARMS (side up down high raise wave out point chin front none)
    legs : stand short long walk_a walk_b none
    body : normal crouch squash stretch   (crouch/squash keep his feet on the box's bottom row)
    mouth: None o yawn smile grin flat frown cat
    blush: pink cheeks
    holes: True = eyes are see-through (official look). False = eyes drawn in ink 'k'
           (use when something is directly behind his face).
    color: body color char (e.g. '@' for a silhouette/shadow Clawd)
    """
    requested = dict(eyes=eyes, mouth=mouth, blush=blush)
    if eyes not in USER_EYES:
        eyes = EYE_FALLBACK.get(eyes, 'open')
    mouth, blush = None, False
    g = GEOM[body]
    cells = {}
    bx0, bx1 = g['bx']
    by0, by1 = g['by']
    for yy in range(by0, by1 + 1):
        for xx in range(bx0, bx1 + 1):
            cells[(xx, yy)] = color
    axl, axr = g['ax']
    for side, shape, base in (('r', rarm, axr), ('l', larm, axl)):
        for item in ARMS[shape]:
            dx, dy = item[0], item[1]
            ch = item[2] if len(item) > 2 else color
            if ch == '@' and color != '#':
                ch = color
            xx = base + dx if side == 'r' else base - dx
            cells[(xx, g['ay'] + dy)] = ch
    lcols = g['legs']
    ll, ly = g['ll'], g['ly']
    lengths = {
        'stand': [ll] * 4, 'short': [1] * 4, 'long': [ll + 1] * 4,
        'walk_a': [1, ll, 1, ll], 'walk_b': [ll, 1, ll, 1], 'none': [0] * 4,
    }[legs]
    for c, n in zip(lcols, lengths):
        for i in range(n):
            cells[(c, ly + i)] = color
    exl, exr = g['ex']
    ey = g['ey']
    left, right = EYES[eyes]
    for (cx, pattern) in ((exl, left), (exr, right)):
        for dx, dy, ch in pattern:
            if ch == '_' and (EYES_BLACK or not holes):
                ch = EYE_INK
            elif ch == 'e' and EYES_BLACK:
                ch = EYE_INK
            cells[(cx + dx, ey + dy)] = ch
    cxm = (bx0 + bx1) // 2
    for dx, dy, ch in MOUTHS[mouth]:
        cells[(cxm + dx, ey + 2 + dy)] = ch
    if blush:
        cells[(exl - 1, ey + 1)] = 'p'
        cells[(exr + 1, ey + 1)] = 'p'
    hr, hl = HAND[rarm], HAND[larm]
    leg_bottom = ly + max(lengths) - 1 if max(lengths) else by1
    anchors = {
        'head': (cxm, by0), 'face': (cxm, ey), 'eye_l': (exl, ey), 'eye_r': (exr, ey),
        'mouth': (cxm, ey + 2), 'neck': (cxm, by1 - 1), 'body': (cxm, (by0 + by1 + 1) // 2),
        'feet': (cxm, leg_bottom),
        'hand_r': (axr + hr[0], g['ay'] + hr[1]), 'hand_l': (axl - hl[0], g['ay'] + hl[1]),
    }
    spec = dict(eyes=eyes, larm=larm, rarm=rarm, legs=legs, body=body, mouth=mouth, blush=blush,
                requested=requested)
    return Pose(Sprite(cells=[(x, y, ch) for (x, y), ch in cells.items()], anchor=(0, 0), name='clawd'), anchors, spec)


def put_clawd(frame, pose, x=None, y=None):
    """Draw Clawd with his box's top-left at (x, y) (default HOME). Always use this for Clawd
    (tools track where he is, e.g. lint's home-spot check)."""
    if x is None:
        x, y = HOME
    frame.place(pose.sprite, x, y)
    frame.meta.setdefault('clawd', []).append((x, y, pose.spec))
    return frame


# --------------------------------------------------------------------------------------------
# Accessories
# --------------------------------------------------------------------------------------------
SLOTS = ('head', 'face', 'neck', 'back', 'hand', 'ground', 'fx', 'scene')
SLOT_ANCHOR = {'head': 'head', 'face': 'face', 'neck': 'neck', 'back': 'body', 'hand': 'hand_r'}


class Item:
    """A library accessory. frames: one Sprite or a list (animated). ms: suggested frame duration(s).

    Anchor convention per slot (the sprite's anchor lands on this point):
      head   -> Clawd's head-top-center pixel  (hat brims usually overlap his top row or sit on it)
      face   -> the point between his eyes, on the eye row
      neck   -> center, two rows below the eyes (bow ties, chains)
      back   -> his body center; drawn BEFORE Clawd (capes, wings, jetpacks)
      hand   -> the grip point just outside his right hand (left hand = automatically mirrored)
      ground -> bottom-center cell of the prop (it rests on a surface, usually y = GROUND)
      fx     -> visual center of the effect
      scene  -> bottom-center cell (furniture, big props)
    preview: optional dict for the contact sheet: {'at': (x, y), 'z': 'front' or 'behind'}
    """

    def __init__(self, name, slot, desc, frames, ms=None, tags=(), preview=None):
        if slot not in SLOTS:
            raise ValueError('%s: unknown slot %r' % (name, slot))
        if isinstance(frames, Sprite):
            frames = [frames]
        self.name, self.slot, self.desc = name, slot, desc
        self.frames = list(frames)
        self.ms = ms
        self.tags = tuple(tags)
        self.preview = preview or {}
        self.module = None
        for s in self.frames:
            s.name = s.name or name

    def sprite(self, i=0):
        return self.frames[i % len(self.frames)]

    def __len__(self):
        return len(self.frames)

    def __repr__(self):
        return 'Item(%r, %s, %d frame(s))' % (self.name, self.slot, len(self.frames))


def wear(frame, item, pose, x=None, y=None, i=0, side='r', dx=0, dy=0):
    """Attach an accessory to Clawd (pose placed with its box at (x, y), default HOME).
    i = which animation frame of the item, side = 'r'/'l' for hand items, dx/dy = nudge
    (e.g. a hat lagging one pixel behind a jump). Back items must be worn BEFORE put_clawd()."""
    if x is None:
        x, y = HOME
    spr = item.sprite(i)
    if item.slot == 'hand':
        key = 'hand_l' if side == 'l' else 'hand_r'
        if side == 'l':
            spr = spr.flipped()
    elif item.slot in SLOT_ANCHOR:
        key = SLOT_ANCHOR[item.slot]
    else:
        raise ValueError('%s (%s) is not wearable; place it with frame.place()' % (item.name, item.slot))
    px, py = pose.at(key, x, y)
    frame.place(spr, px + dx, py + dy)
    frame.meta.setdefault('slots', []).append(item.slot)
    frame.meta.setdefault('items', []).append(item.name)
    return frame


# --------------------------------------------------------------------------------------------
# Fine-line expressions (half-size pixels) - STYLE.md section 0b
# --------------------------------------------------------------------------------------------
def fine(frame):
    """Convert a normal frame to a FINE frame (res=2): every cell becomes 2x2 half-size pixels.
    Draw Clawd, his accessories and props as usual on a normal Frame, then fine(it), then fine_face()."""
    if frame.res == 2:
        return frame.copy()
    f = Frame(res=2)
    for (x, y), c in frame.px.items():
        for dy in (0, 1):
            for dx in (0, 1):
                f.px[(2 * x + dx, 2 * y + dy)] = c
    f.meta = {k: (list(v) if isinstance(v, list) else v) for k, v in frame.meta.items()}
    return f


# Patterns for the LEFT eye in fine pixels, relative to the top-left fine pixel of his eye cell
# (the eye cell is fine (0,0)-(1,1)). The right eye is mirrored automatically. '_' = see-through hole
# (the official eye), 'e' = ink line, 'W' = glint. Everything else in the eye area is body orange.
_HOLE = [(0, 0, '_'), (1, 0, '_'), (0, 1, '_'), (1, 1, '_')]
FINE_EYES = {
    'open':      _HOLE,                                               # the official eye
    'half':      [(0, 1, '_'), (1, 1, '_')],                          # mid-blink / relaxed lid (bottom half open)
    'line':      [(-1, 1, 'e'), (0, 1, 'e'), (1, 1, 'e'), (2, 1, 'e')],   # thin closed eye (blink, sleep, wink)
    'happy':     [(0, 0, 'e'), (1, 0, 'e'), (-1, 1, 'e'), (2, 1, 'e')],   # thin arch: smiling eyes  (like ^ ^)
    'content':   [(-1, 0, 'e'), (2, 0, 'e'), (0, 1, 'e'), (1, 1, 'e')],   # thin cup: cozy/content  (like u u)
    'wide':      [(0, -1, '_'), (1, -1, '_')] + _HOLE,                # surprised: a taller eye
    'sparkle':   [(0, 0, 'k'), (1, 0, 'k'), (0, 1, 'k'), (1, 1, 'k'), (0, 0, 'W')],  # shiny eye with a glint
    'look_l':    [(-1, 0, '_'), (0, 0, '_'), (-1, 1, '_'), (0, 1, '_')],  # half-step glances (subtler than kit look_*)
    'look_r':    [(1, 0, '_'), (2, 0, '_'), (1, 1, '_'), (2, 1, '_')],
    'look_u':    [(0, -1, '_'), (1, -1, '_'), (0, 0, '_'), (1, 0, '_')],
    'look_d':    [(0, 1, '_'), (1, 1, '_'), (0, 2, '_'), (1, 2, '_')],
    'squint':    [(-1, 0, 'e'), (0, 1, 'e'), (1, 1, 'e'), (2, 0, 'e')],   # alias-ish of content, slightly flatter
}
_DIRECTIONAL = {'look_l', 'look_r', 'sparkle'}   # not mirrored for the right eye (direction / top-left glint)


def fine_face(ff, pose, x=None, y=None, expr='open', right=None, color='#'):
    """Draw a fine-line expression on a FINE frame `ff` for Clawd placed with put_clawd(f, pose, x, y).
    expr: a FINE_EYES name for both eyes (or the left eye if `right` is given, e.g. a wink:
    fine_face(ff, p, expr='line', right='open')). Clears his normal eye cells first."""
    if ff.res != 2:
        raise ValueError('fine_face needs a fine frame: ff = fine(frame)')
    if x is None:
        x, y = HOME
    exprs = (expr, right if right is not None else expr)
    for side, key in ((0, 'eye_l'), (1, 'eye_r')):
        ex, ey = pose.anchors[key]
        fx0, fy0 = 2 * (x + ex), 2 * (y + ey)
        for dy in (-1, 0, 1, 2):            # clear the eye area back to body color
            for dx in (-1, 0, 1, 2):
                if (fx0 + dx, fy0 + dy) in ff.px or (0 <= dx <= 1 and 0 <= dy <= 1):
                    ff.put(fx0 + dx, fy0 + dy, color)
        name = exprs[side]
        mirror = side == 1 and name not in _DIRECTIONAL
        for dx, dy, ch in FINE_EYES[name]:
            px = fx0 + (1 - dx if mirror else dx)
            ff.put(px, fy0 + dy, EYE_INK if (ch in '_e' and EYES_BLACK) else ch)
    ff.meta.setdefault('fine_face', []).append(exprs)
    return ff


# --------------------------------------------------------------------------------------------
# Layers / animations
# --------------------------------------------------------------------------------------------
_BODY_COLORS = set('#@%')


def blacken_eye_holes(frame):
    """Fill small transparent holes fully enclosed by Clawd's body (his eyes) with EYE_INK, in place."""
    if not EYES_BLACK:
        return frame
    Wr, Hr, px = W * frame.res, H * frame.res, frame.px
    outside = set()
    stack = [(x, y) for x in range(Wr) for y in (0, Hr - 1)] + [(x, y) for y in range(Hr) for x in (0, Wr - 1)]
    while stack:                                   # everything transparent that reaches the canvas edge
        x, y = stack.pop()
        if (x, y) in outside or (x, y) in px or not (0 <= x < Wr and 0 <= y < Hr):
            continue
        outside.add((x, y))
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    seen = set()
    limit = 8 * frame.res * frame.res
    for y in range(Hr):
        for x in range(Wr):
            if (x, y) in px or (x, y) in outside or (x, y) in seen:
                continue
            comp, edge, body, todo = [], 0, 0, [(x, y)]
            while todo:                                # one enclosed hole
                c = todo.pop()
                if c in seen:
                    continue
                seen.add(c)
                comp.append(c)
                for n in ((c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)):
                    if n in px:
                        edge += 1
                        body += px[n] in _BODY_COLORS
                    elif n not in seen:
                        todo.append(n)
            if len(comp) <= limit and edge and body * 10 >= edge * 6:
                for c in comp:
                    px[c] = EYE_INK
    # eye lines drawn by hand in ink_brown on his face (closed eyes, arcs) become black too
    for (x, y), c in list(px.items()):
        if c == 'e' and any(px.get(n) in _BODY_COLORS for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
            px[(x, y)] = EYE_INK
    return frame


def layer(name, frames, merge=True):
    """frames: list of (Frame, ms). Adjacent identical frames are merged (their ms add up).
    Each layer loops on its own; layers that must stay in sync need identical frame timing."""
    out, metas = [], []
    res = frames[0][0].res if frames else 1
    for f, ms in frames:
        if f.res != res:
            raise ValueError('layer %r mixes resolutions; use fine() on every frame of a fine layer' % name)
        ms = int(round(ms))
        if ms < 20:
            raise ValueError('layer %r: frame shorter than 20 ms (%d)' % (name, ms))
        blacken_eye_holes(f)
        rows = f.rows()
        if merge and out and out[-1]['rows'] == rows:
            out[-1]['ms'] += ms
            continue
        out.append({'ms': ms, 'rows': rows})
        metas.append(f.meta)
    if not out:
        raise ValueError('layer %r has no frames' % name)
    d = {'name': name, 'frames': out, '_meta': metas}
    if res != 1:
        d['res'] = res
    return d


def static(name, frame):
    """A one-frame layer (scenery that never changes)."""
    return layer(name, [(frame, 1000)])


def anim(name, desc, layers, state=''):
    return {'name': name, 'desc': desc, 'state': state, 'layers': layers}


# --------------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------------
def ballistic(x, y, vx, vy, g=0.35, steps=10, drag=1.0):
    """Integer positions of a thrown particle over `steps` ticks (y grows down; g pulls down)."""
    pts = []
    fx, fy = float(x), float(y)
    for _ in range(steps):
        pts.append((int(round(fx)), int(round(fy))))
        fx += vx
        fy += vy
        vx *= drag
        vy += g
    return pts


def ease(n, kind='inout'):
    """n fractions in [0, 1] (inclusive ends) with easing: 'in', 'out', 'inout', 'linear'."""
    out = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 1.0
        if kind == 'in':
            v = t * t
        elif kind == 'out':
            v = 1 - (1 - t) * (1 - t)
        elif kind == 'inout':
            v = 0.5 - 0.5 * math.cos(math.pi * t)
        else:
            v = t
        out.append(v)
    return out


def lerp(a, b, t):
    return a + (b - a) * t


def total_ms(frames):
    return sum(int(round(ms)) for _, ms in frames)


# 3x5 pixel font
_F = {
    '0': '111101101101111', '1': '010110010010111', '2': '111001111100111', '3': '111001111001111',
    '4': '101101111001001', '5': '111100111001111', '6': '111100111101111', '7': '111001010010010',
    '8': '111101111101111', '9': '111101111001111', 'A': '010101111101101', 'B': '110101110101110',
    'C': '011100100100011', 'D': '110101101101110', 'E': '111100110100111', 'F': '111100110100100',
    'G': '011100101101011', 'H': '101101111101101', 'I': '111010010010111', 'J': '001001001101010',
    'K': '101101110101101', 'L': '100100100100111', 'M': '101111101101101', 'N': '110101101101101',
    'O': '010101101101010', 'P': '110101110100100', 'Q': '010101101110011', 'R': '110101110101101',
    'S': '011100010001110', 'T': '111010010010010', 'U': '101101101101111', 'V': '101101101101010',
    'W': '101101111111101', 'X': '101101010101101', 'Y': '101101010010010', 'Z': '111001010100111',
    '!': '010010010000010', '?': '110001010000010', ':': '000010000010000', '.': '000000000000010',
    '-': '000000111000000', '+': '000010111010000', '/': '001001010100100', '%': '101001010100101',
    '<': '001010100010001', '>': '100010001010100', '=': '000111000111000', '(': '010100100100010',
    ')': '010001001001010', '_': '000000000000111', ' ': '000000000000000',
}
FONT = {k: [v[i:i + 3] for i in range(0, 15, 3)] for k, v in _F.items()}


def contrast(ch, bg):
    """WCAG contrast ratio between palette color `ch` and an (r, g, b) background."""
    def lum(c):
        def ch_(v):
            v = v / 255.0
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        r, g_, b = c
        return 0.2126 * ch_(r) + 0.7152 * ch_(g_) + 0.0722 * ch_(b)
    a, b = lum(rgb(ch)), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


DARK_BG = (30, 30, 30)      # VS Code dark theme panel
LIGHT_BG = (255, 255, 255)  # VS Code light theme panel
