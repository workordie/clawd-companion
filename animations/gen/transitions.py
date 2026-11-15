#!/usr/bin/env python3
"""Set-up and pack-away clips for the state animations, generated from each one's frame 0.

Every state animation's frame 0 is a still of its whole scene, set up. Without these, switching from one
animation to another makes a whole scene (laptop, forge, easel...) vanish and the next one appear in a single
frame. custom.js plays out-<A> (A's scene packs away, he ends in the plain pose at home), maybe a short walk,
then in-<B> (B's scene arrives, he takes B's frame-0 pose), then B itself.

in-<name> (about 0.5 s): he stands in the plain pose and the scene's pieces arrive one after another. Pieces
that stand on the ground drop in from above and land with a dust puff (small ones bounce a cell); floating
pieces (stars, notes, sparks) twinkle in. When the first piece lands he takes the frame-0 pose. The last frame
is exactly the animation's frame 0, held.
out-<name> (about 0.45 s): from frame 0 he takes the plain pose, grounded pieces hop up a cell and vanish in a
puff, floating ones twinkle out; the last frame is the plain pose, held.

The pieces are the 8-connected blobs of frame 0 that are not Clawd. Clawd = his body colours connected to his
home box, plus the ink drawn on him inside it. Both clips play once and hold their last frame (`once`).

Run from ~/Projects/clawd-svgs after gen/make.py:
    python3 gen/transitions.py              all state animations in clawd.json
    python3 gen/transitions.py working idle the named ones (and keeps the others already in transitions.json)
    python3 gen/transitions.py --sheet working   also renders gen/out/tx-working.png (contact sheet)
Writes transitions.json and svg-tx/clawd-in-<name>.svg, svg-tx/clawd-out-<name>.svg.
"""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
GEN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(GEN)
sys.path.insert(0, GEN)
import clawdlib as L  # noqa: E402
from preview import composite, anim_res, render, OUT  # noqa: E402

# Same list as custom.js STATES: the animations that are a state (everything else is a move or a reaction).
STATES = {'idle', 'typing', 'thinking', 'working', 'alert', 'question', 'done', 'sleep', 'compacting', 'hooks',
          'manual', 'plan', 'edits', 'auto', 'bypass', 'subagents', 'error', 'rate', 'vibe'}
BODY = {'#', '@', '%'}             # his body colours
ON_HIM = {'k', 'e', 'K'}           # ink drawn on him (eyes, lines): his only inside his box
DUST = ('m', 'w')                  # mid-tone dust that reads on both themes, and a lighter speck
SPARK = ('y', 'w')                 # twinkle: yellow arms, paper core
MS = 50                            # one transition step


def is_state(name):
    return name.split('-')[0] in STATES


def plain_rows(res):
    f = L.Frame()
    L.put_clawd(f, L.clawd())
    L.blacken_eye_holes(f)
    rows = f.rows()
    if res == 1:
        return rows
    return [''.join(ch * res for ch in r) for r in rows for _ in range(res)]


def split(rows, res):
    """frame-0 rows -> (clawd pixel dict, list of pieces); a piece = dict(px={(x, y): ch}, ...)."""
    W, H = len(rows[0]), len(rows)
    px = {(x, y): ch for y, r in enumerate(rows) for x, ch in enumerate(r) if ch != '.'}
    x0, x1 = L.HOME[0] * res, (L.HOME[0] + 11) * res
    y0, y1 = L.HOME[1] * res, (L.HOME[1] + 8) * res
    inbox = lambda x, y: x0 <= x < x1 and y0 <= y < y1
    seeds = [p for p, ch in px.items() if inbox(*p) and ch in BODY]
    him, stack = set(seeds), list(seeds)
    while stack:
        x, y = stack.pop()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = (x + dx, y + dy)
                if q in him or q not in px:
                    continue
                ch = px[q]
                if ch in BODY or (ch in ON_HIM and inbox(*q)):
                    him.add(q)
                    stack.append(q)
    clawd = {p: px[p] for p in him}
    rest = {p: ch for p, ch in px.items() if p not in him}
    pieces, seen = [], set()
    for p in sorted(rest, key=lambda q: (q[1], q[0])):
        if p in seen:
            continue
        comp, stack = {}, [p]
        seen.add(p)
        while stack:
            q = stack.pop()
            comp[q] = rest[q]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    r = (q[0] + dx, q[1] + dy)
                    if r in rest and r not in seen:
                        seen.add(r)
                        stack.append(r)
        xs = [q[0] for q in comp]
        ys = [q[1] for q in comp]
        piece = dict(px=comp, x0=min(xs), x1=max(xs), y0=min(ys), y1=max(ys), n=len(comp))
        piece['grounded'] = piece['y1'] >= H - res      # stands on the box (touches the bottom row)
        piece['cx'] = (piece['x0'] + piece['x1']) // 2
        piece['cy'] = (piece['y0'] + piece['y1']) // 2
        pieces.append(piece)
    return clawd, pieces, (W, H)


def merge_small(pieces, res):
    """Specks of 1-3 cells next to a bigger floating piece travel with it (fewer, calmer arrivals)."""
    big = [p for p in pieces if p['n'] > 3 * res * res or p['grounded']]
    small = [p for p in pieces if p not in big]
    out = list(big)
    for s in small:
        out.append(s)
    return out


class Canvas:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.px = {}

    def put(self, x, y, ch):
        if 0 <= x < self.W and 0 <= y < self.H:
            self.px[(x, y)] = ch

    def piece(self, p, dx=0, dy=0, dither=None, res=1):
        for (x, y), ch in p['px'].items():
            if dither is not None and ((x // res + y // res) % 2) != dither:
                continue
            self.put(x + dx, y + dy, ch)

    def cell(self, cx, cy, ch, res):
        """One cell-sized dot (res x res pixels) with its top-left at pixel (cx, cy)."""
        for a in range(res):
            for b in range(res):
                self.put(cx + a, cy + b, ch)

    def rows(self):
        return [''.join(self.px.get((x, y), '.') for x in range(self.W)) for y in range(self.H)]


def sparkle(c, x, y, res, big=True):
    s = res
    c.cell(x, y, SPARK[1], s)
    if big:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            c.cell(x + dx * s, y + dy * s, SPARK[0], s)


def puff(c, p, res, k):
    """Dust at a landing piece's feet: k = 0 (burst) or 1 (settling)."""
    y = p['y1']
    if k == 0:
        for x, ch in ((p['x0'] - res, DUST[0]), (p['x1'] + 1, DUST[0]), (p['x0'] - 2 * res, DUST[1]),
                      (p['x1'] + 1 + res, DUST[1])):
            c.cell(x, y - res + 1, ch, res)
    else:
        for x in (p['x0'] - 2 * res, p['x1'] + 1 + res):
            c.cell(x, y - 2 * res + 1, DUST[0], res)


def poof(c, p, res, k):
    """A piece vanishing: k = 0 (cloud over it), 1 (cloud breaking up)."""
    cx, cy = p['cx'], p['cy']
    rx = max(res, (p['x1'] - p['x0']) // 2)
    ry = max(res, (p['y1'] - p['y0']) // 2)
    pts = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]
    for i, (dx, dy) in enumerate(pts):
        if k == 1 and i % 2:
            continue
        r = 1.0 if k == 0 else 1.4
        x = cx + int(dx * rx * r)
        y = cy + int(dy * ry * r)
        c.cell(x - res // 2, y - res // 2, DUST[i % 2] if k == 0 else DUST[0], res)


def build_in(anim):
    res = anim_res(anim)
    f0 = composite(anim, 0)
    clawd, pieces, (W, H) = split(f0, res)
    plain = plain_rows(res)
    grounded = sorted([p for p in pieces if p['grounded']], key=lambda p: (-p['n'], p['x0']))
    floating = sorted([p for p in pieces if not p['grounded']], key=lambda p: (p['y0'], p['x0']))
    # schedule: grounded pieces start one step apart (at most 4 waves), floating ones after the first landing
    DROP = 4
    start = {}
    for i, p in enumerate(grounded):
        start[id(p)] = min(i, 3)
    first_land = DROP if grounded else 1
    for j, p in enumerate(floating):
        start[id(p)] = first_land - 1 + min(j // 2, 4)
    end = max([start[id(p)] + DROP + 3 for p in grounded] + [start[id(p)] + 3 for p in floating] + [first_land + 1])
    frames = []
    for k in range(end + 1):
        c = Canvas(W, H)
        pose = plain if k < first_land else None
        if pose:
            for y, r in enumerate(pose):
                for x, ch in enumerate(r):
                    if ch != '.':
                        c.put(x, y, ch)
        else:
            for (x, y), ch in clawd.items():
                c.put(x, y, ch)
        for p in grounded:
            t = k - start[id(p)]
            if t < 0:
                continue
            if t < DROP:
                lift = p['y1'] + 1                      # fully above the canvas at t = 0
                dy = -int(round(lift * (1 - (t / DROP) ** 2)))
                c.piece(p, 0, dy, res=res)
            else:
                bounce = -res if (t == DROP + 1 and p['n'] <= 40 * res * res) else 0
                c.piece(p, 0, bounce, res=res)
                if t == DROP:
                    puff(c, p, res, 0)
                elif t == DROP + 1:
                    puff(c, p, res, 1)
        for p in floating:
            t = k - start[id(p)]
            if t < 0:
                continue
            if t == 0:
                sparkle(c, p['cx'], p['cy'], res)
            elif t == 1:
                c.piece(p, dither=0, res=res)
                sparkle(c, p['cx'], p['cy'], res, big=False)
            else:
                c.piece(p, res=res)
        frames.append(c.rows())
    frames.append(f0)
    out = []
    for i, rows in enumerate(frames):
        ms = 300 if i == len(frames) - 1 else MS
        if out and out[-1]['rows'] == rows:
            out[-1]['ms'] += ms
        else:
            out.append({'ms': ms, 'rows': rows})
    if len(out) < 2:
        return None                                     # nothing to set up: frame 0 is the plain pose
    layer = {'name': 'scene', 'frames': out}
    if res != 1:
        layer['res'] = res
    return {'name': 'in-' + anim['name'], 'desc': 'Set-up for %s: its scene arrives, ending on its first frame.' % anim['name'],
            'state': 'transition (set-up)', 'once': True, 'layers': [layer]}


def build_out(anim):
    res = anim_res(anim)
    f0 = composite(anim, 0)
    clawd, pieces, (W, H) = split(f0, res)
    plain = plain_rows(res)
    grounded = sorted([p for p in pieces if p['grounded']], key=lambda p: (p['n'], p['x0']))
    floating = sorted([p for p in pieces if not p['grounded']], key=lambda p: (p['y0'], p['x0']))
    start = {}
    for j, p in enumerate(floating):
        start[id(p)] = 1 + min(j // 2, 3)
    for i, p in enumerate(grounded):
        start[id(p)] = 1 + min(i, 3)
    end = max([start[id(p)] + 4 for p in pieces] + [2])
    frames = [f0]
    for k in range(1, end + 1):
        c = Canvas(W, H)
        for y, r in enumerate(plain):
            for x, ch in enumerate(r):
                if ch != '.':
                    c.put(x, y, ch)
        for p in grounded:
            t = k - start[id(p)]
            if t < 0:
                c.piece(p, res=res)
            elif t == 0:
                c.piece(p, 0, -res, res=res)            # a hop
            elif t == 1:
                c.piece(p, 0, -res, dither=0, res=res)
                poof(c, p, res, 0)
            elif t == 2:
                poof(c, p, res, 1)
        for p in floating:
            t = k - start[id(p)]
            if t < 0:
                c.piece(p, res=res)
            elif t == 0:
                c.piece(p, dither=1, res=res)
            elif t == 1:
                sparkle(c, p['cx'], p['cy'], res)
            elif t == 2:
                sparkle(c, p['cx'], p['cy'], res, big=False)
        frames.append(c.rows())
    frames.append(plain)
    out = []
    for i, rows in enumerate(frames):
        ms = 200 if i == len(frames) - 1 else MS
        if out and out[-1]['rows'] == rows:
            out[-1]['ms'] += ms
        else:
            out.append({'ms': ms, 'rows': rows})
    if len(out) < 2:
        return None
    layer = {'name': 'scene', 'frames': out}
    if res != 1:
        layer['res'] = res
    return {'name': 'out-' + anim['name'], 'desc': 'Pack-away for %s: its scene leaves, ending on the plain pose.' % anim['name'],
            'state': 'transition (pack-away)', 'once': True, 'layers': [layer]}


def sheet(tx, name):
    """A contact sheet of in-/out- for one animation: every frame at 4x, dark and light."""
    from PIL import Image, ImageDraw
    clips = [a for a in tx if a['name'] in ('in-' + name, 'out-' + name)]
    rows_ = []
    for a in clips:
        rows_.append((a['name'], [(f['ms'], f['rows'], a['layers'][0].get('res', 1)) for f in a['layers'][0]['frames']]))
    s = 4
    cw, chh = L.W * s, L.H * s
    width = 10 + max(len(fr) for _, fr in rows_) * (cw + 6)
    height = sum(2 * chh + 40 for _ in rows_) + 10
    im = Image.new('RGB', (width, height), (14, 14, 16))
    d = ImageDraw.Draw(im)
    y = 6
    for label, frames in rows_:
        d.text((10, y), label, fill=(230, 230, 230))
        y += 14
        for i, (ms, rows, res) in enumerate(frames):
            x = 10 + i * (cw + 6)
            for j, bg in enumerate((L.DARK_BG, L.LIGHT_BG)):
                im.paste(render(rows, s // res if res > 1 else s, bg, border=True), (x, y + j * (chh + 2)))
            d.text((x, y + 2 * chh + 4), '%dms' % ms, fill=(160, 160, 160))
        y += 2 * chh + 26
    path = os.path.join(OUT, 'tx-%s.png' % name)
    im.save(path)
    return path


def main(argv):
    sheets = '--sheet' in argv
    wanted = [a for a in argv if not a.startswith('-')]
    doc = json.load(open(os.path.join(ROOT, 'clawd.json')))
    pool = [a for a in doc['animations'] if is_state(a['name']) and (not wanted or a['name'] in wanted)]
    path = os.path.join(ROOT, 'transitions.json')
    keep = []
    if wanted and os.path.exists(path):
        keep = [a for a in json.load(open(path))['animations'] if a['name'].split('-', 1)[1] not in wanted]
    tx = list(keep)
    for a in pool:
        tx.extend(c for c in (build_in(a), build_out(a)) if c)
    tx.sort(key=lambda a: (a['name'].split('-', 1)[1], a['name']))
    out = dict(doc, animations=tx)
    with open(path, 'w') as fh:
        json.dump(out, fh, separators=(',', ':'))
    r = subprocess.run(['node', '-e', '''
import('./svgwriter.mjs').then(({ buildSvg, fileName }) => {
  const fs = require('node:fs');
  const doc = JSON.parse(fs.readFileSync('transitions.json', 'utf8'));
  fs.mkdirSync('svg-tx', { recursive: true });
  for (const f of fs.readdirSync('svg-tx')) if (f.endsWith('.svg')) fs.unlinkSync('svg-tx/' + f);
  for (const a of doc.animations) fs.writeFileSync('svg-tx/' + fileName(a), buildSvg(doc, a));
  console.log(doc.animations.length);
})'''], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    total = sum(os.path.getsize(os.path.join(ROOT, 'svg-tx', f)) for f in os.listdir(os.path.join(ROOT, 'svg-tx')))
    print('wrote transitions.json and svg-tx/: %s clips, %.0f KB' % (r.stdout.strip(), total / 1000))
    if sheets:
        for a in pool:
            print(sheet(tx, a['name']))


if __name__ == '__main__':
    main(sys.argv[1:])
