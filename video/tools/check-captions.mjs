// No caption may touch or cross a UI edge or line. For every caption of a cut, over all the time it's on screen
// (every 0.2 s and right after each scene change), this measures the caption's box (plus 6 px) against every visible
// line in the frame: borders in the VS Code window and in the real panel (its box, bubbles, popups, the chat's
// boxes), the active tabs' top lines, the current line's box, B's floor and wall. Seeks only: no screenshots.
//   node tools/check-captions.mjs [--cut wide]      (out/showcase.html: node build.mjs first)
import path from 'node:path'
import { chrome, VIDEO } from './realbox/realbox.mjs'

const args = process.argv.slice(2)
const cuts = args.includes('--cut') ? [args[args.indexOf('--cut') + 1]] : ['wide', 'tall']
const profile = path.join(process.env.TMPDIR ?? '/tmp', 'captions-profile')
const PAGE_FN = `(() => {
  const M = 6
  const SKIP = '.capA, .topText, .capC, .cursor, .clawd, .cx-clawd, .wall, .endcard, .flash, .note, .lead, .corner, #hud'
  const name = el => (el.className && typeof el.className === 'string' ? el.className.split(' ')[0] : el.tagName).slice(0, 28)
  const visible = (cs) => cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.05
  const segs = []
  const clipRect = (r, c) => ({ l: Math.max(r.l, c.l), t: Math.max(r.t, c.t), r: Math.min(r.r, c.r), b: Math.min(r.b, c.b) })
  const add = (x1, y1, x2, y2, src, clip) => {
    if (x1 === x2) { const t = Math.max(y1, clip.t), b = Math.min(y2, clip.b); if (x1 >= clip.l && x1 <= clip.r && b > t) segs.push([x1, t, x1, b, src]) }
    else { const l = Math.max(x1, clip.l), r = Math.min(x2, clip.r); if (y1 >= clip.t && y1 <= clip.b && r > l) segs.push([l, y1, r, y1, src]) }
  }
  const borders = (doc, root, map, clip) => {
    for (const el of root.querySelectorAll('*')) {
      if (el.closest(SKIP)) continue
      const cs = doc.defaultView.getComputedStyle(el)
      if (!visible(cs)) continue
      const q = el.getBoundingClientRect()
      if (q.width < 1 && q.height < 1) continue
      const [x1, y1] = map(q.left, q.top), [x2, y2] = map(q.right, q.bottom)
      for (const [side, a, b, c, d] of [['Top', x1, y1, x2, y1], ['Bottom', x1, y2, x2, y2], ['Left', x1, y1, x1, y2], ['Right', x2, y1, x2, y2]]) {
        const w = parseFloat(cs['border' + side + 'Width'])
        const col = cs['border' + side + 'Color']
        if (!(w > 0) || cs['border' + side + 'Style'] === 'none' || /,\\s*0\\)$/.test(col) || col === 'transparent') continue
        add(a, b, c, d, name(el) + ' ' + side.toLowerCase(), clip)
      }
    }
  }
  const look = SHOW.styleId === 'MIX' ? (SHOW.cut.scenes.findLast(s => s.t0 <= SHOW.t + 1e-9) ?? SHOW.cut.scenes[0]).look ?? 'B' : SHOW.styleId
  const L = SHOW.looks[look]
  const stage = { l: 0, t: 0, r: SHOW.W, b: SHOW.H }
  const view = L.root.querySelector('.view')
  const clip = view ? clipRect((r => ({ l: r.left, t: r.top, r: r.right, b: r.bottom }))(view.getBoundingClientRect()), stage) : stage
  borders(document, L.root, (x, y) => [x, y], clip)
  // lines drawn without borders: the window's outline, the active tabs' top line, the current line's box
  for (const el of L.root.querySelectorAll('.vsc')) { const q = el.getBoundingClientRect(); for (const [a, b, c, d] of [[q.left, q.top, q.right, q.top], [q.left, q.bottom, q.right, q.bottom], [q.left, q.top, q.left, q.bottom], [q.right, q.top, q.right, q.bottom]]) add(a, b, c, d, 'window outline', clip) }
  for (const el of L.root.querySelectorAll('.vsc-tabs > span.on')) { const q = el.getBoundingClientRect(); add(q.left, q.top, q.right, q.top, 'active tab top', clip) }
  for (const el of L.root.querySelectorAll('.vsc-code .cur')) { const q = el.getBoundingClientRect(); const k = q.height / 18; const x0 = q.left + 56 * k
    for (const [a, b, c, d] of [[x0, q.top, q.right, q.top], [x0, q.bottom, q.right, q.bottom], [x0, q.top, x0, q.bottom], [q.right, q.top, q.right, q.bottom]]) add(a, b, c, d, 'current line', clip) }
  // the real panel (its own borders), in the stage's px
  const P = L.panel
  if (P) {
    const fr = P.frame.getBoundingClientRect(), k = fr.width / P.width
    const pclip = clipRect({ l: fr.left, t: fr.top, r: fr.right, b: fr.bottom }, clip)
    borders(P.doc, P.doc.body, (x, y) => [fr.left + x * k, fr.top + y * k], pclip)
  }
  // the caption on screen
  const capEl = [...L.root.querySelectorAll('.capA, .topText, .capC')].find(e => !e.classList.contains('off') && getComputedStyle(e).display !== 'none' && e.textContent.trim())
  if (!capEl) return null
  // a card (a background or border) is its box; bare text (B's caption, 9:16's band) is its text's own extent
  const ccs = getComputedStyle(capEl)
  const card = !/,\\s*0\\)$|transparent/.test(ccs.backgroundColor) || parseFloat(ccs.borderTopWidth) > 0
  const range = document.createRange()
  range.selectNodeContents(capEl)
  const q = card ? capEl.getBoundingClientRect() : range.getBoundingClientRect()
  const R = { l: q.left - M, t: q.top - M, r: q.right + M, b: q.bottom + M }
  const hits = segs.filter(([x1, y1, x2, y2]) => x1 <= R.r && x2 >= R.l && y1 <= R.b && y2 >= R.t).map(s => s[4])
  return { look, cap: capEl.textContent.replace(/\\s+/g, ' ').slice(0, 44), rect: [Math.round(q.left), Math.round(q.top), Math.round(q.right), Math.round(q.bottom)],
    out: q.left < 0 || q.top < 0 || q.right > SHOW.W || q.bottom > SHOW.H, hits: [...new Set(hits)] }
})()`

for (const cutId of cuts) {
  const [W, H] = cutId === 'tall' ? [1080, 1920] : [1920, 1080]
  const c = await chrome({ width: W, height: H, dpr: 0.25, profile })
  try {
    await c.send('Page.navigate', { url: `file://${path.join(VIDEO, 'out/showcase.html')}?style=mix&cut=${cutId}&capture` })
    for (let i = 0; i < 100 && !(await c.evaluate('window.__ready === true').catch(() => false)); i++) await c.sleep(150)
    const plan = await c.evaluate(`(() => { const cut = SHOW.cut, out = []
      cut.captions.forEach((cp, i) => { if (!cp[1]) return; const t0 = cp[0], t1 = Math.min(cut.end, (cut.captions[i + 1] ?? [cut.end])[0])
        const ts = new Set(); for (let t = t0 + 0.04; t < t1 - 0.02; t += 0.2) ts.add(+t.toFixed(3)); ts.add(+(t1 - 0.04).toFixed(3))
        for (const s of cut.scenes) if (s.t0 > t0 && s.t0 < t1) ts.add(+(s.t0 + 0.02).toFixed(3))
        out.push({ text: cp[1], t0, t1, ts: [...ts].sort((a, b) => a - b), typed: (cp[1].length + 1) / 45 }) })
      return out })()`)
    let bad = 0
    for (const cp of plan) {
      const issues = new Map()
      for (const t of cp.ts) {
        const r = await c.evaluate(`(() => { seek(${t}); return ${PAGE_FN} })()`)
        if (!r) continue
        if (r.hits.length || r.out) {
          const key = r.look + ' ' + (r.out ? 'OUTSIDE THE FRAME ' : '') + r.hits.join(', ')
          if (!issues.has(key)) issues.set(key, { from: t, to: t, rect: r.rect })
          else issues.get(key).to = t
        }
      }
      const head = `${cp.t0.toFixed(2)}–${cp.t1.toFixed(2)}  "${cp.text.replace(/\n/g, ' / ')}"`
      if (issues.size) {
        bad++
        console.log(`✗ ${head}`)
        for (const [k, v] of issues) console.log(`    ${v.from.toFixed(2)}–${v.to.toFixed(2)} s  rect ${v.rect.join(',')}  ${k}`)
      } else console.log(`✓ ${head}`)
    }
    console.log(`${cutId}: ${plan.length} captions, ${bad} touch a UI line`)
  } finally {
    c.close()
  }
}
