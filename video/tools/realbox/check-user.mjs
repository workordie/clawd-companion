// The real box (realbox.mjs, the user's theme) against the user's own screenshot of it (out/realbox/ref-user-box.png:
// 1x, Auto mode, unfocused, the placeholder showing, effort High, a resumed chat, Clawd on top). Renders the box in
// that state at 1x, lines it up on the box's border, and writes out/realbox/check-vs-user.png (the screenshot, the
// render, the difference); prints the colours and every footer item's left/right edge in both.
//   node tools/realbox/check-user.mjs
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { extensionDir, pageHtml, serve, chrome, OUT } from './realbox.mjs'
import { PROMPT, REPLY } from './capture-states.mjs'

const R = path.dirname(new URL(import.meta.url).pathname)
const REF = path.join(OUT, 'ref-user-box.png')
const ext = extensionDir()
const server = await serve(() => pageHtml({ ext, theme: 'hc_light', hostScript: fs.readFileSync(path.join(R, 'host.js'), 'utf8') }), ext)
const c = await chrome({ width: 849, height: 700, dpr: 1, profile: path.join(process.env.TMPDIR ?? '/tmp', 'realbox-profile') })
const live = path.join(OUT, 'check-vs-user-live.png')
let box
try {
  await c.send('Page.navigate', { url: `http://127.0.0.1:${server.address().port}/` })
  await c.sleep(3500)
  const setup = fs.readFileSync(path.join(R, 'setup-screenshot.js'), 'utf8')
  await c.evaluate(fs.readFileSync(path.join(R, 'inpage.js'), 'utf8'))
  await c.evaluate(setup)
  await c.evaluate('RB.dismissNotices(); RB.session().permissionMode.value = "default"')
  // a resumed chat: a turn in it (the user's has history), then their footer state
  const r = await c.evaluate('RB.rect(RB.input())')
  for (const type of ['mousePressed', 'mouseReleased']) await c.send('Input.dispatchMouseEvent', { type, x: r.x + 20, y: r.y + 10, button: 'left', clickCount: 1 })
  await c.send('Input.insertText', { text: PROMPT })
  const d = { key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13, text: '\r' }
  await c.send('Input.dispatchKeyEvent', { type: 'keyDown', ...d })
  await c.send('Input.dispatchKeyEvent', { type: 'keyUp', ...d, text: undefined })
  await c.sleep(1500)
  await c.evaluate(`HOST.reply(${JSON.stringify(REPLY)})`)
  await c.sleep(1500)
  await c.evaluate(setup)
  await c.evaluate('RB.session().permissionMode.value = "auto"')
  // unfocused (a click on the chat), no Clawd, no caret
  await c.evaluate(`document.documentElement.classList.add('rb-noclawd')`)
  for (const type of ['mousePressed', 'mouseReleased']) await c.send('Input.dispatchMouseEvent', { type, x: 424, y: 300, button: 'left', clickCount: 1 })
  await c.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 2, y: 2, button: 'none' })
  await c.sleep(800)
  box = await c.evaluate('RB.rect(RB.box())')
  const items = await c.evaluate(`[...RB.footer().children].filter(n => n.getClientRects().length && getComputedStyle(n).visibility !== 'hidden')
    .map(n => { const r = n.getBoundingClientRect(); return [n.className.split(' ')[0].slice(0, 22) || n.tagName, Math.round(r.left * 10) / 10, Math.round(r.right * 10) / 10] })`)
  fs.writeFileSync(path.join(OUT, 'check-vs-user-items.json'), JSON.stringify({ box, items }))
  await c.shot(null, live)
} finally {
  c.close()
  server.close()
}

const out = execFileSync('python3', ['-I', '-c', `
import sys, json
sys.path.insert(0, __import__('site').getusersitepackages())
from PIL import Image, ImageChops, ImageDraw
ref = Image.open(sys.argv[1]).convert('RGB'); live = Image.open(sys.argv[2]).convert('RGB'); info = json.loads(open(sys.argv[3]).read()); dst = sys.argv[4]
box = info['box']
W, H = ref.size
px = ref.load()
dark = lambda p: sum(p) < 300 and p[2] > p[0] + 25   # the box's dark blue border
# the screenshot's box: its left border is the first dark-blue column mid-height, its bottom border the last dark-blue row
ymid = H - 30
bl = next(x for x in range(W) if dark(px[x, ymid]))
bb = next(y for y in range(H - 1, 0, -1) if dark(px[W // 2, y]))
br = next(x for x in range(W - 1, 0, -1) if dark(px[x, ymid]))
# its top: the first dark-blue row in a column clear of Clawd
bt = next(y for y in range(H) if dark(px[60, y]))
print(f'screenshot box: x {bl}..{br} ({br - bl + 1} px), y {bt}..{bb} ({bb - bt + 1} px)')
print(f'render box:     x {box["x"]:.1f}..{box["x"] + box["w"] - 1:.1f} ({box["w"]:.0f} px), y {box["y"]:.1f} ({box["h"]:.0f} px)')
# the render, cropped to the screenshot's window around the box (same box-relative offsets)
ox, oy = round(box['x']) - bl, round(box['y']) - bt
crop = live.crop((ox, oy, ox + W, oy + H))
diff = ImageChops.difference(ref, crop)
sheet = Image.new('RGB', (W, H * 3 + 24), 'white')
sheet.paste(ref, (0, 0)); sheet.paste(crop, (0, H + 12)); sheet.paste(diff.point(lambda v: min(255, v * 3)), (0, 2 * H + 24))
d = ImageDraw.Draw(sheet)
sheet = sheet.resize((W * 2, sheet.height * 2), Image.NEAREST)
sheet.save(dst)
# colours: the border, the placeholder, cold, the Auto dot, the slider (darkest pixels in each)
def sample(img, x0, y0, x1, y1, pick):
    c = img.crop((x0, y0, x1, y1)).getdata(); return pick(list(c))
darkest = lambda cs: min(cs, key=sum)
reddest = lambda cs: max(cs, key=lambda p: p[0] - p[2])
print('colours (screenshot | render):')
for name, (x0, y0, x1, y1), pick in [('border', (bl, ymid - 3, bl + 2, ymid + 3), darkest), ('placeholder', (bl + 28, bt + 14, bl + 230, bt + 32), darkest),
                                       ('cold', (bl + 120, bt + 42, bl + 165, bt + 62), reddest), ('Auto dot', (bl + 570, bt + 42, bl + 590, bt + 62), reddest),
                                       ('slider', (bl + 500, bt + 46, bl + 565, bt + 58), darkest)]:
    a = sample(ref, x0, y0, x1, y1, pick); b = sample(crop, x0, y0, x1, y1, pick)
    print(f'  {name:12s} #{a[0]:02x}{a[1]:02x}{a[2]:02x} | #{b[0]:02x}{b[1]:02x}{b[2]:02x}')
# the footer row's items: runs of ink along the row (both images), compared edge by edge
def runs(img, y0, y1, x0, x1, gap=5):
    p = img.load(); cols = []
    for x in range(x0, x1):
        ink = any(sum(p[x, y]) < 650 for y in range(y0, y1)); cols.append(ink)  # light greys count (the slider track)
    out = []; start = None; last = None
    for i, ink in enumerate(cols):
        x = x0 + i
        if ink:
            if start is None: start = x
            elif x - last > gap: out.append((start, last)); start = x
            last = x
    if start is not None: out.append((start, last))
    return out
fy0, fy1 = bt + 40, bt + 66
a = runs(ref, fy0, fy1, bl + 6, br - 6); b = runs(crop, fy0, fy1, bl + 6, br - 6)
print(f'footer items: screenshot {len(a)}, render {len(b)} (ink = darker than a light grey)')
# pair each screenshot item with the render item it overlaps most (a faint item can fall either side of the
# ink threshold after the screenshot's colour profile)
worst = 0
used = set()
for ra in a:
    best = max(((min(ra[1], rb[1]) - max(ra[0], rb[0]), j) for j, rb in enumerate(b)), default=(-1, None))
    if best[0] < 0:
        print(f'      screenshot {ra[0]-bl:4d}..{ra[1]-bl:4d}  (no render item over it)'); continue
    rb = b[best[1]]; used.add(best[1])
    dl, dr = rb[0] - ra[0], rb[1] - ra[1]
    worst = max(worst, abs(dl), abs(dr))
    print(f'      screenshot {ra[0]-bl:4d}..{ra[1]-bl:4d}  render {rb[0]-bl:4d}..{rb[1]-bl:4d}  diff {dl:+d} / {dr:+d} px')
for j, rb in enumerate(b):
    if j not in used: print(f'      render {rb[0]-bl:4d}..{rb[1]-bl:4d}  (no screenshot item over it)')
print(f'worst footer edge difference: {worst} px')
pa = runs(ref, bt + 12, bt + 32, bl + 6, br - 6, gap=9); pb = runs(crop, bt + 12, bt + 32, bl + 6, br - 6, gap=9)
print('top row (placeholder, mic):', [(x - bl, y - bl) for x, y in pa], '|', [(x - bl, y - bl) for x, y in pb])
`, REF, live, path.join(OUT, 'check-vs-user-items.json'), path.join(OUT, 'check-vs-user.png')], { encoding: 'utf8' })
console.log(out)
