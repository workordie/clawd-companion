#!/usr/bin/env python3
"""Build everything from the generator:
    gen/anims/*.py  ->  clawd.json  ->  svg/clawd-*.svg   (+ accessories.json and parts.json for the Studio)

    python3 gen/make.py              rebuild all animations
    python3 gen/make.py idle done    rebuild only these; the rest are kept from the current clawd.json

The previous clawd.json is kept as clawd.prev.json (one level of undo). Python 3.9.
"""
import importlib
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
GEN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(GEN)
sys.path.insert(0, GEN)

import clawdlib as L  # noqa: E402

ORDER = ['idle', 'idle-pet', 'idle-bubbles', 'idle-kite', 'idle-garden', 'idle-game', 'idle-bird', 'idle-moods', 'typing', 'typing-juggle', 'typing-drums', 'thinking', 'thinking-chalk', 'thinking-cube', 'thinking-stars', 'thinking-gears', 'thinking-pace',
         'thinking-cairn', 'working', 'working-chef', 'working-forge', 'working-lab', 'working-knit', 'working-paint',
         'working-mail', 'alert', 'alert-bell', 'alert-flags', 'question', 'question-lens', 'question-scroll', 'done', 'done-bell', 'done-flag', 'done-party', 'sleep', 'sleep-hammock', 'sleep-camp', 'compacting',
         'hooks', 'manual', 'manual-drive', 'manual-craft', 'plan', 'edits', 'auto', 'auto-robot', 'auto-cloud',
         'bypass', 'subagents', 'error', 'rate-limit', 'vibe', 'hello', 'hello-peek', 'hello-hat',
         # moving around the panel, talking, playing (custom.js places these; see each module's contract)
         'walk-left', 'walk-right', 'climb-right', 'climb-left', 'look-up-right', 'look-up-left',
         'hop-right', 'hop-left', 'teeter-left', 'teeter-right', 'sit-edge-left', 'sit-edge-right',
         'talk-listen', 'talk-think', 'talk-explain', 'notice', 'pet', 'grabbed', 'grabbed-bored', 'grabbed-dizzy',
         'tumble', 'fall', 'parachute', 'chute-pop', 'land', 'land-chute', 'crash',
         'click-hop', 'click-wave', 'click-hug', 'click-dizzy', 'click-hide', 'click-party', 'click-spin',
         'click-giggle', 'click-shrug', 'click-idea', 'click-poof', 'click-groove']


def names_on_disk():
    d = os.path.join(GEN, 'anims')
    return [f[:-3].replace('_', '-') for f in os.listdir(d) if f.endswith('.py') and not f.startswith('_')]


def build_one(name):
    modname = 'anims.' + name.replace('-', '_')
    sys.modules.pop(modname, None)
    a = importlib.import_module(modname).build()
    for layer in a['layers']:
        layer.pop('_meta', None)
    return a


def sort_key(a):
    n = a['name']
    return (ORDER.index(n) if n in ORDER else len(ORDER), n)


def export_accessories():
    import acc
    items = []
    for it in acc.all_items():
        frames = []
        for spr in it.frames:
            frames.append({'rows': spr.rows(), 'anchor': [spr.ax - spr.x0, spr.ay - spr.y0]})
        items.append({'name': it.name, 'module': it.module, 'slot': it.slot, 'desc': it.desc,
                      'ms': it.ms, 'frames': frames})
    for m, err in acc.errors().items():
        print('!! accessory module %s skipped: %s' % (m, err))
    return {'slots': list(L.SLOTS), 'items': items}


def export_parts():
    def cells(lst):
        return [list(c) for c in lst]
    return {
        'home': list(L.HOME),
        'geom': {k: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in g.items()} for k, g in L.GEOM.items()},
        'arms': {k: cells(v) for k, v in L.ARMS.items()},
        'hand': {k: list(v) for k, v in L.HAND.items()},
        'eyes': {k: [cells(v[0]), cells(v[1])] for k, v in L.EYES.items()},
        'mouths': {('none' if k is None else k): cells(v) for k, v in L.MOUTHS.items()},
        'legs': list(L.LEG_STYLES),
        'fine_eyes': {k: [list(c) for c in v] for k, v in L.FINE_EYES.items()},
        'fine_directional': sorted(L._DIRECTIONAL),
    }


def write_json(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    os.replace(tmp, path)


def main(argv):
    wanted = [a for a in argv if not a.startswith('-')]
    path = os.path.join(ROOT, 'clawd.json')
    if wanted and not os.path.exists(path):
        # A fresh clone has no clawd.json (it's generated, not committed). Building only a few animations now
        # would leave the others out of it, and build.mjs would then delete their SVGs: build everything once.
        print('no clawd.json yet: building every animation first (once)')
        wanted = []
    existing = []
    if wanted and os.path.exists(path):
        old = json.load(open(path))
        if old.get('w') == L.W and old.get('h') == L.H:
            existing = [a for a in old['animations'] if a['name'] not in wanted]
    names = wanted or sorted(names_on_disk(), key=lambda n: (ORDER.index(n) if n in ORDER else 99, n))
    built, failed = [], []
    for n in names:
        try:
            built.append(build_one(n))
        except Exception as e:
            failed.append((n, '%s: %s' % (type(e).__name__, e)))
    anims = sorted(existing + built, key=sort_key)
    if not anims:
        raise SystemExit('nothing built: %s' % failed)
    doc = {'version': 2, 'w': L.W, 'h': L.H, 'scale': L.SCALE, 'home': list(L.HOME),
           'palette': {c: v[1] for c, v in L.PALETTE.items()}, 'animations': anims}
    if os.path.exists(path):
        shutil.copyfile(path, os.path.join(ROOT, 'clawd.prev.json'))
    write_json(path, doc)
    write_json(os.path.join(ROOT, 'accessories.json'), export_accessories())
    write_json(os.path.join(ROOT, 'parts.json'), export_parts())
    r = subprocess.run(['node', 'build.mjs'], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        raise SystemExit('svg build failed')
    sizes = {}
    for a in anims:
        p = os.path.join(ROOT, 'svg', 'clawd-%s.svg' % a['name'])
        sizes[a['name']] = os.path.getsize(p) if os.path.exists(p) else 0
    print('%-12s %-8s %-7s %-9s %s' % ('animation', 'layers', 'frames', 'svg', 'state'))
    for a in anims:
        print('%-12s %-8d %-7d %-9s %s' % (a['name'], len(a['layers']), sum(len(l['frames']) for l in a['layers']),
                                           '%.1f KB' % (sizes[a['name']] / 1000), a.get('state', '')))
    for n, err in failed:
        print('!! %s failed: %s' % (n, err))
    print('wrote clawd.json, accessories.json, parts.json, svg/')


if __name__ == '__main__':
    main(sys.argv[1:])
