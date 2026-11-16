// The box in the video against the real one at the same scale: the live panel (realbox.mjs) screenshotted at
// device scale 2, 4 and 6, next to video frames at zoom 2 (A), 4 (A2) and 6 (B) taken with Clawd and the cursor
// hidden. Writes out/realbox/check-<n>x.png (live | video | difference) and prints how many pixels differ.
//   node tools/realbox/check-scale.mjs
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { extensionDir, pageHtml, serve, chrome, OUT, VIDEO } from './realbox.mjs'
import { PROMPT, REPLY } from './capture-states.mjs'

const R = path.dirname(new URL(import.meta.url).pathname)
const profile = path.join(process.env.TMPDIR ?? '/tmp', 'realbox-profile')
const CHECKS = [
  // 1x: the video's own panel code (src/realpanel.js, the verify page) with the captured 'typed' state, at 1x
  { n: 1, verify: 'a-wide', state: 'typed', panel: [600, 453], history: false, mode: 'default', effort: 'high', focus: true, typed: PROMPT },
  // n: the scale; the video frame (cut, t, look); the live panel and how to get it into the same state
  // 2x: the opener's prompt typed (the input focused; the video's caret in its off half-second)
  { n: 2, cut: 'wide', t: 6.3, look: 'A', panel: [600, 453], history: false, mode: 'default', effort: 'high', focus: true, typed: PROMPT },
  { n: 4, cut: 'wide', t: 82.7, look: 'A2', panel: [849, 700], history: true, mode: 'auto', effort: 'medium', focus: true },
  { n: 6, cut: 'wide', t: 31.0, look: 'B', panel: [849, 700], history: true, mode: 'default', effort: 'high', focus: false },
]

async function live(ck) {
  const ext = extensionDir()
  const server = await serve(() => pageHtml({ ext, theme: 'hc_light', hostScript: fs.readFileSync(path.join(R, 'host.js'), 'utf8') }), ext)
  const c = await chrome({ width: ck.panel[0], height: ck.panel[1], dpr: ck.n, profile })
  try {
    await c.send('Page.navigate', { url: `http://127.0.0.1:${server.address().port}/` })
    await c.sleep(3500)
    await c.evaluate(fs.readFileSync(path.join(R, 'inpage.js'), 'utf8'))
    // the opener's panels are a brand-new chat (no history), B and A2 the user's own resumed chat
    const setup = fs.readFileSync(path.join(R, ck.history ? 'setup-screenshot.js' : 'setup-newchat.js'), 'utf8')
    await c.evaluate(setup)
    await c.evaluate('RB.dismissNotices(); RB.session().permissionMode.value = "default"')
    if (ck.history) {
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
    }
    await c.evaluate(`RB.session().permissionMode.value = ${JSON.stringify(ck.mode)}; RB.session().effortLevel.value = ${JSON.stringify(ck.effort)}`)
    if (ck.typed) {
      const r = await c.evaluate('RB.rect(RB.input())')
      for (const type of ['mousePressed', 'mouseReleased']) await c.send('Input.dispatchMouseEvent', { type, x: r.x + 20, y: r.y + 10, button: 'left', clickCount: 1 })
      await c.send('Input.insertText', { text: ck.typed })
    }
    await c.sleep(800)
    // focus as the video shows it; the live caret is hidden (the video draws its own, at its own blink)
    await c.evaluate(`(() => { document.documentElement.classList.add('rb-noclawd')
      const st = document.createElement('style'); st.textContent = '[contenteditable], textarea { caret-color: transparent !important; }'; document.head.append(st)
      ${ck.focus ? 'RB.input().focus()' : ''} })()`)
    if (!ck.focus) {
      // unfocused the way a user does it: a click on the chat's empty space (the panel puts focus back after blur())
      for (const type of ['mousePressed', 'mouseReleased']) await c.send('Input.dispatchMouseEvent', { type, x: Math.round(ck.panel[0] / 2), y: 260, button: 'left', clickCount: 1 })
    }
    await c.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 2, y: 2, button: 'none' })
    await c.sleep(600)
    const box = await c.evaluate('RB.rect(RB.box())')
    const file = path.join(OUT, `check-${ck.n}x-live.png`)
    await c.shot(null, file)
    return { file, box: { x: box.x * ck.n, y: box.y * ck.n, w: box.w * ck.n, h: box.h * ck.n } }
  } finally {
    c.close()
    server.close()
  }
}

async function video(ck) {
  if (ck.verify) {
    const c = await chrome({ width: ck.panel[0], height: ck.panel[1], dpr: 1, profile })
    try {
      await c.send('Page.navigate', { url: `file://${path.join(OUT, `verify-${ck.verify}.html`)}` })
      await c.sleep(1500)
      const box = await c.evaluate(`(() => { showState(${JSON.stringify(ck.state)}); const b = panel.rect(panel.box); return { x: b.x, y: b.y, w: b.w, h: b.h, k: 1 } })()`)
      await c.sleep(200)
      const file = path.join(OUT, `check-${ck.n}x-video.png`)
      await c.shot(null, file)
      return { file, box }
    } finally {
      c.close()
    }
  }
  const [W, H] = ck.cut === 'tall' ? [1080, 1920] : [1920, 1080]
  const c = await chrome({ width: W, height: H, dpr: 1, profile })
  try {
    await c.send('Page.navigate', { url: `file://${path.join(VIDEO, 'out/showcase.html')}?style=mix&cut=${ck.cut}&capture&noclawd` })
    for (let i = 0; i < 100 && !(await c.evaluate('window.__ready === true').catch(() => false)); i++) await c.sleep(150)
    await c.evaluate(`(() => { seek(${ck.t}); return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))) })()`)
    const box = await c.evaluate(`(() => { const p = SHOW.looks[${JSON.stringify(ck.look)}].panel, fr = p.frame.getBoundingClientRect(), k = fr.width / p.width, b = p.rect(p.box)
      return { x: fr.left + b.x * k, y: fr.top + b.y * k, w: b.w * k, h: b.h * k, k } })()`)
    const file = path.join(OUT, `check-${ck.n}x-video.png`)
    await c.shot(null, file)
    return { file, box }
  } finally {
    c.close()
  }
}

for (const ck of CHECKS) {
  const L = await live(ck)
  const V = await video(ck)
  // the part of the box (plus 16 px around it, for the focus ring) that the video frame shows, from both
  const out = execFileSync('python3', ['-I', '-c', `
import sys, json
sys.path.insert(0, __import__('site').getusersitepackages())
from PIL import Image, ImageChops
L, V, n, dst = json.loads(sys.argv[1]), json.loads(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
a, b = Image.open(L['file']).convert('RGB'), Image.open(V['file']).convert('RGB')
m = 16 * n
# box-relative window visible in the video frame
x0 = max(-m, -V['box']['x']); y0 = max(-m, -V['box']['y'])
x1 = min(V['box']['w'] + m, b.width - V['box']['x']); y1 = min(V['box']['h'] + m, b.height - V['box']['y'])
x0 = max(x0, -L['box']['x']); y0 = max(y0, -L['box']['y']); x1 = min(x1, a.width - L['box']['x']); y1 = min(y1, a.height - L['box']['y'])
ca = a.crop(tuple(round(v) for v in (L['box']['x'] + x0, L['box']['y'] + y0, L['box']['x'] + x1, L['box']['y'] + y1)))
cb = b.crop(tuple(round(v) for v in (V['box']['x'] + x0, V['box']['y'] + y0, V['box']['x'] + x1, V['box']['y'] + y1)))
cb = cb.resize(ca.size) if cb.size != ca.size else cb
d = ImageChops.difference(ca, cb)
mask = d.convert('L').point(lambda v: 255 if v > 40 else 0)
k = sum(1 for v in mask.getdata() if v)
sheet = Image.new('RGB', (ca.width, ca.height * 3 + 20), 'white')
sheet.paste(ca, (0, 0)); sheet.paste(cb, (0, ca.height + 10)); sheet.paste(d.point(lambda v: min(255, v * 4)), (0, 2 * ca.height + 20))
sheet.save(dst)
print(f'{n}x: compared {ca.width}x{ca.height} px of the box: {k} px differ ({100*k/(ca.width*ca.height):.2f}%), video scale {V["box"]["k"]:.2f}')
`, JSON.stringify(L), JSON.stringify(V), String(ck.n), path.join(OUT, `check-${ck.n}x.png`)], { encoding: 'utf8' })
  process.stdout.write(out)
}
