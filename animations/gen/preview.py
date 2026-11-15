#!/usr/bin/env python3
"""Render contact sheets (PNG) and lint animations/accessories so you can SEE your pixel art.

  python3 gen/preview.py anim <name> [--from N] [--count N] [--scale S] [--layer NAME]
        -> gen/out/anim-<name>.png  every distinct composite moment of the loop, on the dark AND
           light VS Code backgrounds, with time + duration labels, an orange line for the input
           box border, plus a real-size strip. Prints the lint report.
           --layer NAME shows only that layer's own frames (handy when a fast particle layer
           floods the combined view).
  python3 gen/preview.py frame <name> <index> [--scale S]
        -> gen/out/frame-<name>-<index>.png  one composite moment, big, with a coordinate grid
  python3 gen/preview.py acc <module> [--only a,b,c]
        -> gen/out/acc-<module>.png  each item alone (every frame), worn by / next to Clawd, real size
  python3 gen/preview.py lint [names...]      lint report only (all animations if no names)
  python3 gen/preview.py list                 every library accessory: name, slot, size, frames
  python3 gen/preview.py gif <name>           gen/out/anim-<name>.gif real-time preview for humans
  python3 gen/preview.py states [names...]    frame 0 + mid-loop of every animation side by side (consistency)

All commands accept --out FILE.png (written into gen/out/) so parallel workers never overwrite each other.
Open the PNGs with your image viewer / Read tool. Python 3.9.
"""
import importlib
import json
import os
import sys
from functools import reduce
from math import gcd

sys.dont_write_bytecode = True
GEN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GEN)

import numpy as np                      # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import clawdlib as L                    # noqa: E402

OUT = os.path.join(GEN, 'out')
FONT = ImageFont.load_default()
BORDER = (217, 119, 87)
LABEL = (200, 200, 200)
SHEET_BG = (14, 14, 16)


# ------------------------------------------------------------------ loading
def load_anim(name):
    """Import gen/anims/<name>.py fresh and call build(). Returns (anim_dict, clipped_count)."""
    modname = 'anims.' + name.replace('-', '_')
    for k in list(sys.modules):
        if k == modname or k.startswith('anims.') or k == 'anims':
            del sys.modules[k]
    L.STATS['clipped'] = 0
    mod = importlib.import_module(modname)
    a = mod.build()
    return a, L.STATS['clipped']


def anim_names():
    d = os.path.join(GEN, 'anims')
    return sorted(f[:-3].replace('_', '-') for f in os.listdir(d)
                  if f.endswith('.py') and not f.startswith('_'))


# ------------------------------------------------------------------ timeline
def _lcm(a, b):
    return a * b // gcd(a, b)


def layer_total(layer):
    return sum(f['ms'] for f in layer['frames'])


def frame_index(layer, t):
    T = layer_total(layer)
    tt = t % T
    for i, f in enumerate(layer['frames']):
        if tt < f['ms']:
            return i
        tt -= f['ms']
    return len(layer['frames']) - 1


def anim_res(anim):
    return max(l.get('res', 1) for l in anim['layers'])


def upscale_rows(rows, k):
    if k == 1:
        return rows
    out = []
    for r in rows:
        wide = ''.join(ch * k for ch in r)
        out.extend([wide] * k)
    return out


def composite(anim, t):
    """Composite at the finest layer resolution (32x20, or 64x40 if any layer uses fine pixels)."""
    R = anim_res(anim)
    grid = [list('.' * (L.W * R)) for _ in range(L.H * R)]
    for layer in anim['layers']:
        rows = upscale_rows(layer['frames'][frame_index(layer, t)]['rows'], R // layer.get('res', 1))
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != '.':
                    grid[y][x] = ch
    return [''.join(r) for r in grid]


def timeline(anim, horizon_cap=40000):
    """Distinct composite moments: list of (t, duration, rows). Covers one full cycle of the layer
    combination (LCM of layer lengths) up to horizon_cap ms."""
    totals = [layer_total(l) for l in anim['layers']]
    lcm = reduce(_lcm, totals)
    horizon = min(lcm, max(max(totals), horizon_cap))
    times = set()
    for layer, T in zip(anim['layers'], totals):
        starts, s = [], 0
        for f in layer['frames']:
            starts.append(s)
            s += f['ms']
        k = 0
        while k * T < horizon:
            for st in starts:
                if k * T + st < horizon:
                    times.add(k * T + st)
            k += 1
    times = sorted(times)
    out = []
    for i, t in enumerate(times):
        end = times[i + 1] if i + 1 < len(times) else horizon
        rows = composite(anim, t)
        if out and out[-1][2] == rows:
            out[-1] = (out[-1][0], out[-1][1] + end - t, rows)
        else:
            out.append((t, end - t, rows))
    return out, {'totals': totals, 'lcm': lcm, 'horizon': horizon}


# ------------------------------------------------------------------ rendering
def render(rows, s, bg, border=True):
    arr = np.zeros((len(rows), len(rows[0]), 3), dtype=np.uint8)
    arr[:, :] = bg
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.':
                arr[y, x] = L.rgb(ch)
    img = Image.fromarray(arr).resize((L.W * s, L.H * s), Image.NEAREST)
    if border:
        out = Image.new('RGB', (L.W * s, L.H * s + max(2, s // 2)), bg)
        out.paste(img, (0, 0))
        d = ImageDraw.Draw(out)
        d.rectangle([0, L.H * s, L.W * s, L.H * s + max(2, s // 2) - 1], fill=BORDER)
        return out
    return img


def both(rows, s):
    a, b = render(rows, s, L.DARK_BG), render(rows, s, L.LIGHT_BG)
    out = Image.new('RGB', (a.width, a.height * 2 + 2), SHEET_BG)
    out.paste(a, (0, 0))
    out.paste(b, (0, a.height + 2))
    return out


def text(d, xy, s, fill=LABEL):
    d.text(xy, s, font=FONT, fill=fill)


# ------------------------------------------------------------------ lint
def svg_size(anim, scale=3):
    """Same algorithm as svgwriter.mjs, to estimate bytes."""
    n = 300
    for li, layer in enumerate(anim['layers']):
        for fi, fr in enumerate(layer['frames']):
            n += 40
            for y, row in enumerate(fr['rows']):
                x = 0
                while x < len(row):
                    if row[x] == '.':
                        x += 1
                        continue
                    c = row[x]
                    x0 = x
                    while x < len(row) and row[x] == c:
                        x += 1
                    n += len('M%d %dh%dv1h-%dz' % (x0, y, x - x0, x - x0))
            n += 60 * len({ch for row in fr['rows'] for ch in row if ch != '.'})
            if len(layer['frames']) > 1:
                n += 140
    return n


def lint(anim, clipped=0):
    out = []
    warn = lambda s: out.append('WARN  ' + s)
    info = lambda s: out.append('info  ' + s)
    for li, layer in enumerate(anim['layers']):
        for fi, fr in enumerate(layer['frames']):
            if fr['ms'] < 40:
                warn('layer %r frame %d lasts %d ms (< 40 ms reads as a glitch)' % (layer['name'], fi, fr['ms']))
            bad = {ch for row in fr['rows'] for ch in row if ch != '.' and ch not in L.HEX}
            if bad:
                warn('layer %r frame %d: unknown colors %s' % (layer['name'], fi, bad))
    if clipped:
        warn('%d pixels were drawn outside the 32x20 canvas and clipped' % clipped)
    resized = {}
    for layer in anim['layers']:
        for meta in layer.get('_meta') or []:
            for _, _, spec in meta.get('clawd', []):
                b = (spec or {}).get('body', 'normal')
                if b in ('crouch', 'squash', 'stretch'):
                    resized[b] = resized.get(b, 0) + 1
    if resized:
        warn('USER PREFERENCE VIOLATION: Clawd changes body size (%s). The user dislikes seeing him shrink: '
             'keep body normal (STYLE.md section 0)' % ', '.join('%s x%d' % kv for kv in sorted(resized.items())))
    face = {}
    for layer in anim['layers']:
        for meta in layer.get('_meta') or []:
            for _, _, spec in meta.get('clawd', []):
                req = (spec or {}).get('requested') or {}
                if req.get('eyes') and req['eyes'] not in L.USER_EYES:
                    face['eyes=' + req['eyes']] = face.get('eyes=' + req['eyes'], 0) + 1
                if req.get('mouth'):
                    face['mouth=' + req['mouth']] = face.get('mouth=' + req['mouth'], 0) + 1
                if req.get('blush'):
                    face['blush'] = face.get('blush', 0) + 1
            for name in meta.get('items', []):
                if name == 'blush':
                    face['blush item'] = face.get('blush item', 0) + 1
    if face:
        warn('USER PREFERENCE VIOLATION: face features the user dislikes (%s). The kit already shows plain eyes '
             'instead; remove them from the code and express the moment with arms, eye direction, timing or effects '
             '(STYLE.md section 0)' % ', '.join('%s x%d' % kv for kv in sorted(face.items())))
    rows0 = composite(anim, 0)
    R = anim_res(anim)
    body0 = sum(r.count('#') for r in rows0) // (R * R)
    if body0 < 30:
        warn('frame 0 shows only %d Clawd-orange cells: frame 0 is the reduced-motion still, Clawd should be clearly visible' % body0)
    homes = []
    for layer in anim['layers']:
        meta = layer.get('_meta') or []
        if meta and meta[0].get('clawd'):
            homes += [(x, y) for x, y, _ in meta[0]['clawd']]
    if not homes:
        warn('no put_clawd() in frame 0 of any layer (always draw Clawd with put_clawd)')
    elif tuple(L.HOME) not in homes:
        warn('frame 0: Clawd is at %s, HOME is %s (ok only if this state is a different resting pose, e.g. lying in bed)' % (homes[0], L.HOME))
    # edge visibility on both themes
    tl, meta = timeline(anim)
    worst = {'dark': {}, 'light': {}}
    edges_total = 0
    for _, _, rows in tl[:40]:
        Hh, Ww = len(rows), len(rows[0])
        for y in range(Hh):
            for x in range(Ww):
                ch = rows[y][x]
                if ch == '.':
                    continue
                edge = any(not (0 <= x + dx < Ww and 0 <= y + dy < Hh) or rows[y + dy][x + dx] == '.'
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if not edge:
                    continue
                edges_total += 1
                for theme, bg in (('dark', L.DARK_BG), ('light', L.LIGHT_BG)):
                    if L.contrast(ch, bg) < 1.5:
                        worst[theme][ch] = worst[theme].get(ch, 0) + 1
    for theme in ('dark', 'light'):
        if worst[theme]:
            n = sum(worst[theme].values())
            parts = ', '.join("'%s' %s x%d" % (c, L.PALETTE[c][0], k) for c, k in sorted(worst[theme].items(), key=lambda kv: -kv[1]))
            msg = '%s theme: %d of %d silhouette-edge pixels are nearly invisible (%s)' % (theme, n, edges_total, parts)
            (warn if n > edges_total * 0.12 else info)(msg)
    size = svg_size(anim)
    (warn if size > 60000 else info)('estimated SVG size %.1f KB' % (size / 1000))
    totals = meta['totals']
    info('layers: %s; loop of the combination: %s ms' % (
        ', '.join('%s=%dms/%df' % (l['name'], t, len(l['frames'])) for l, t in zip(anim['layers'], totals)),
        meta['lcm']))
    return out


# ------------------------------------------------------------------ commands
def cmd_anim(name, start=0, count=30, scale=5, only_layer=None, out=None):
    a, clipped = load_anim(name)
    full = a
    if only_layer is not None:
        keep = [l for l in a['layers'] if l['name'] == only_layer]
        if not keep:
            raise SystemExit('no layer %r; layers: %s' % (only_layer, ', '.join(l['name'] for l in a['layers'])))
        a = dict(a, layers=keep)
    tl, meta = timeline(a)
    if anim_res(full) == 2 and scale % 2:
        scale += 1
    shown = tl[start:start + count]
    cols = 5
    cw, ch_ = L.W * scale, (L.H * scale + max(2, scale // 2)) * 2 + 2
    cell_h = ch_ + 18
    rows_n = (len(shown) + cols - 1) // cols
    strip_n = min(len(shown), 10)
    strip_w = strip_n * (L.W * 3 + 6)
    head = 64
    width = max(cols * (cw + 10) + 10, strip_w + 20, 640)
    height = head + rows_n * (cell_h + 8) + 2 * (L.H * 3 + 6) + 60
    sheet = Image.new('RGB', (width, height), SHEET_BG)
    d = ImageDraw.Draw(sheet)
    text(d, (10, 6), 'anim %s  |  %s' % (a['name'], a.get('state', '')), (255, 255, 255))
    text(d, (10, 20), a.get('desc', '')[:150])
    text(d, (10, 34), 'moments %d-%d of %d (one combined loop = %d ms%s)  |  layers: %s' % (
        start, start + len(shown) - 1, len(tl), meta['lcm'], ', showing first %d ms' % meta['horizon'] if meta['horizon'] < meta['lcm'] else '',
        ', '.join('%s %dms' % (l['name'], t) for l, t in zip(a['layers'], meta['totals']))))
    text(d, (10, 48), 'top = dark theme, bottom = light theme, orange line = input box border; label: #index  t=start  +duration')
    for i, (t, dur, rows) in enumerate(shown):
        cx = 10 + (i % cols) * (cw + 10)
        cy = head + (i // cols) * (cell_h + 8)
        text(d, (cx, cy), '#%d  t=%d  +%dms' % (start + i, t, dur))
        sheet.paste(both(rows, scale), (cx, cy + 14))
    y = head + rows_n * (cell_h + 8) + 6
    text(d, (10, y), 'real size (3 px per cell), first %d moments:' % strip_n)
    for i, (t, dur, rows) in enumerate(shown[:strip_n]):
        sheet.paste(render(rows, 3, L.DARK_BG), (10 + i * (L.W * 3 + 6), y + 14))
        sheet.paste(render(rows, 3, L.LIGHT_BG), (10 + i * (L.W * 3 + 6), y + 14 + L.H * 3 + 6))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out or 'anim-%s%s.png' % (name, '-' + only_layer if only_layer else ''))
    sheet.save(path)
    print(path)
    for line in lint(full, clipped):
        print(line)


def cmd_frame(name, index, scale=16, out=None):
    a, _ = load_anim(name)
    tl, _ = timeline(a)
    t, dur, rows = tl[index]
    if anim_res(a) == 2 and scale % 2:
        scale += 1
    pad = 26
    img = Image.new('RGB', (L.W * scale + pad * 2, (L.H * scale) * 2 + pad * 3), SHEET_BG)
    d = ImageDraw.Draw(img)
    for k, bg in enumerate((L.DARK_BG, L.LIGHT_BG)):
        oy = pad + k * (L.H * scale + pad)
        img.paste(render(rows, scale, bg, border=False), (pad, oy))
        grid = (70, 70, 70) if k == 0 else (215, 215, 215)
        for x in range(L.W + 1):
            d.line([(pad + x * scale, oy), (pad + x * scale, oy + L.H * scale)], fill=grid if x % 5 else (130, 90, 80))
        for y in range(L.H + 1):
            d.line([(pad, oy + y * scale), (pad + L.W * scale, oy + y * scale)], fill=grid if y % 5 else (130, 90, 80))
        for x in range(0, L.W, 5):
            text(d, (pad + x * scale + 2, oy - 12), str(x))
        for y in range(0, L.H, 5):
            text(d, (4, oy + y * scale + 2), str(y))
        hx, hy = L.HOME
        d.rectangle([pad + hx * scale, oy + hy * scale, pad + (hx + 11) * scale, oy + (hy + 8) * scale], outline=(217, 119, 87))
    text(d, (pad, 4), '%s moment #%d  t=%d  +%dms   (orange box = Clawd home box, grid lines every 5 cells)' % (name, index, t, dur))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out or 'frame-%s-%d.png' % (name, index))
    img.save(path)
    print(path)


def item_preview_frames(item, i):
    """Rows of the item worn by/next to Clawd for frame i."""
    f = L.Frame()
    p = L.clawd()
    pv = item.preview or {}
    if item.slot == 'back':
        L.wear(f, item, p, i=i)
        L.put_clawd(f, p)
    elif item.slot in L.SLOT_ANCHOR:
        L.put_clawd(f, p)
        L.wear(f, item, p, i=i)
    else:
        at = pv.get('at') or {'ground': (25, L.GROUND), 'fx': (25, 7), 'scene': (15, L.GROUND)}[item.slot]
        z = pv.get('z') or ('front' if item.slot == 'scene' else 'behind')
        if z == 'behind':
            L.put_clawd(f, p)
            f.place(item.sprite(i), *at)
        else:
            f2 = L.Frame()
            L.put_clawd(f2, p)
            f2.place(item.sprite(i), *at)
            f = f2
    return f.rows()


def alone_rows(spr):
    f = L.Frame()
    f.place(spr.with_anchor(spr.x0, spr.y0), (L.W - spr.w) // 2, (L.H - spr.h) // 2)
    return f.rows()


def cmd_acc(module, only=None, out=None):
    sys.modules.pop('acc', None)
    for k in list(sys.modules):
        if k.startswith('acc.'):
            del sys.modules[k]
    mod = importlib.import_module('acc.' + module)
    items = list(getattr(mod, 'ITEMS'))
    if only:
        items = [it for it in items if it.name in only]
    s_alone, s_worn = 6, 5
    blocks = []
    for it in items:
        n = len(it.frames)
        alone = [both(alone_rows(sp), s_alone) for sp in it.frames]
        worn = [both(item_preview_frames(it, k), s_worn) for k in range(n)]
        real = [both(item_preview_frames(it, k), 3) for k in range(min(n, 4))]
        blocks.append((it, alone, worn, real))
    width = 1500
    y = 10
    rows_layout = []
    for it, alone, worn, real in blocks:
        h = 16 + max(alone[0].height, worn[0].height) + 10
        rows_layout.append((y, it, alone, worn, real))
        y += h
    sheet = Image.new('RGB', (width, y + 10), SHEET_BG)
    d = ImageDraw.Draw(sheet)
    for y0, it, alone, worn, real in rows_layout:
        spr = it.frames[0]
        text(d, (10, y0), '%s  [%s]  %dx%d  %d frame(s)%s  anchor=(%d,%d)  -  %s' % (
            it.name, it.slot, spr.w, spr.h, len(it.frames), ' ms=%s' % (it.ms,) if it.ms else '', spr.ax, spr.ay, it.desc[:110]),
            (255, 255, 255))
        x = 10
        for im in alone[:3]:
            crop = im
            sheet.paste(crop, (x, y0 + 16))
            x += crop.width + 6
        x = max(x, 10) + 10
        for im in worn[:3]:
            sheet.paste(im, (x, y0 + 16))
            x += im.width + 6
        for im in real[:4]:
            sheet.paste(im, (x, y0 + 16))
            x += im.width + 6
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out or 'acc-%s.png' % module)
    sheet.save(path)
    print(path)
    print('%d items: %s' % (len(items), ', '.join(it.name for it in items)))


def cmd_list():
    import acc
    for it in acc.all_items():
        s = it.frames[0]
        print('%-22s %-7s %2dx%-2d %d fr  %-10s %s' % (it.name, it.slot, s.w, s.h, len(it.frames), it.module, it.desc))
    for m, err in acc.errors().items():
        print('!! acc/%s.py failed to import: %s' % (m, err))


def cmd_gif(name, scale=4):
    a, _ = load_anim(name)
    tl, _ = timeline(a)
    frames = [render(rows, scale, L.DARK_BG) for _, _, rows in tl]
    durs = [max(20, int(dur)) for _, dur, _ in tl]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'anim-%s.gif' % name)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durs, loop=0, disposal=1)
    print(path)


def cmd_states(names=None, out=None, scale=5):
    """Frame 0 of every animation side by side (+ the moment halfway through each loop), dark + light."""
    names = names or anim_names()
    cells = []
    for n in names:
        try:
            a, _ = load_anim(n)
        except Exception as e:  # show broken ones instead of crashing
            cells.append((n, None, str(e)[:60]))
            continue
        tl, meta = timeline(a)
        mid = composite(a, max(meta['totals']) // 2)
        cells.append((n, (tl[0][2], mid), ''))
    cols = 4
    cw = L.W * scale * 2 + 16
    chh = (L.H * scale + max(2, scale // 2)) * 2 + 2 + 20
    rows_n = (len(cells) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (cw + 10) + 10, rows_n * (chh + 10) + 30), SHEET_BG)
    d = ImageDraw.Draw(sheet)
    text(d, (10, 8), 'frame 0 (left) and mid-loop (right) of every animation  |  orange box = HOME', (255, 255, 255))
    for i, (n, pair, err) in enumerate(cells):
        x = 10 + (i % cols) * (cw + 10)
        y = 30 + (i // cols) * (chh + 10)
        text(d, (x, y), n + ('  ERROR: ' + err if err else ''))
        if pair:
            for k, rows in enumerate(pair):
                im = both(rows, scale)
                dd = ImageDraw.Draw(im)
                hx, hy = L.HOME
                for oy in (0, im.height // 2 + 1):
                    dd.rectangle([hx * scale, oy + hy * scale, (hx + 11) * scale - 1, oy + (hy + 8) * scale - 1], outline=(217, 119, 87))
                sheet.paste(im, (x + k * (L.W * scale + 8), y + 16))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out or 'states.png')
    sheet.save(path)
    print(path)


def main(argv):
    if not argv:
        print(__doc__)
        return
    opts = {}
    pos = []
    it = iter(argv)
    for a in it:
        if a.startswith('--'):
            opts[a[2:]] = next(it)
        else:
            pos.append(a)
    cmd = pos[0]
    if cmd == 'anim':
        cmd_anim(pos[1], int(opts.get('from', 0)), int(opts.get('count', 30)), int(opts.get('scale', 5)), opts.get('layer'), opts.get('out'))
    elif cmd == 'frame':
        cmd_frame(pos[1], int(pos[2]), int(opts.get('scale', 16)), opts.get('out'))
    elif cmd == 'acc':
        cmd_acc(pos[1], set(opts['only'].split(',')) if 'only' in opts else None, opts.get('out'))
    elif cmd == 'lint':
        for n in (pos[1:] or anim_names()):
            a, clipped = load_anim(n)
            print('== %s' % n)
            for line in lint(a, clipped):
                print('  ' + line)
    elif cmd == 'list':
        cmd_list()
    elif cmd == 'states':
        cmd_states(pos[1:] or None, opts.get('out'))
    elif cmd == 'gif':
        cmd_gif(pos[1], int(opts.get('scale', 4)))
    else:
        print(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
