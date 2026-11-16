// The real Claude Code panel in the video. Each look puts one in an iframe: the extension's own CSS (index.css),
// the patch's (custom.css), VS Code's webview defaults and theme variables, and DOM snapshots of the panel taken
// from the real extension + patch running in headless Chrome (tools/realbox: capture-states.mjs). Nothing in it is
// drawn by hand: the video only swaps snapshots, puts typed text where the real input keeps it, and sets what the
// real CSS reacts to (focus, hover, pressed: the real :focus/:hover/:active rules, aliased to data-rb-* attributes
// so a frame never depends on where a mouse is), and seeks the real CSS animations.
//
// REAL (from build.mjs): { themes: { light, dark }, css: { defaults, index, custom, fonts, template, video },
//   markup, panels: { name: { width, height, states: { state: { html, vars, extras, focus, hover, active, geometry } } } },
//   verbs }

const REAL = JSON.parse(document.getElementById('real-data').textContent)

const attrEsc = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;')

/** The panel document: VS Code's webview wrapper (theme variables on <html>, the theme class on <body>). */
function realDocHtml(theme) {
  const t = REAL.themes[theme]
  const vars = Object.entries(t.styles).map(([k, v]) => `--${k}: ${v};`).join(' ')
  const c = REAL.css
  return `<!DOCTYPE html><html lang="en" style="${attrEsc(vars)}"><head><meta charset="UTF-8">` +
    `<style id="_defaultStyles">${c.defaults}</style><style>${c.index}</style><style>${c.custom}</style>` +
    `<style id="claude-font-configuration">${c.fonts}</style><style>${c.template}</style><style>${c.video}</style>` +
    `</head><body class="${t.classes.join(' ')}" data-vscode-theme-kind="${t.kind}" data-vscode-theme-name="${attrEsc(t.label)}" ` +
    `data-vscode-theme-id="${attrEsc(t.id)}"><pre id="claude-error"></pre>${REAL.markup}<div id="root"></div></body></html>`
}

/**
 * :hover, :active, :focus, :focus-visible, :focus-within in the real CSS also match data-rb-hover, ... (rewritten
 * in place: `:hover` -> `:is(:hover,[data-rb-hover])`, same specificity). Selectors that can't take it (a pseudo
 * after a pseudo-element) are left as they are.
 */
function aliasPseudo(doc) {
  const re = /:(focus-within|focus-visible|focus|hover|active)(?![-\w])/g
  const walk = rules => {
    for (const r of rules) {
      if (r.selectorText !== undefined && re.test(r.selectorText)) {
        re.lastIndex = 0
        const next = r.selectorText.replace(re, (m, p) => `:is(:${p},[data-rb-${p}])`)
        try {
          r.selectorText = next
        } catch {}
      }
      re.lastIndex = 0
      if (r.cssRules?.length) walk(r.cssRules)
    }
  }
  for (const sheet of doc.styleSheets) walk(sheet.cssRules)
}

// a captured child-index path (the panel had no video Clawd in it): his element doesn't count
const nodeAt = (root, path) => {
  let n = root
  for (const i of path ?? []) n = n ? [...n.children].filter(c => !c.classList.contains('cx-clawd'))[i] : null
  return n ?? null
}

class RealPanel {
  /**
   * A real panel (`name`: a captured panel size) in a new iframe under `parent` (before `before`). The iframe is
   * never moved afterwards: moving one reloads it, blank.
   */
  constructor(parent, name, theme = 'light', before = null) {
    const P = (this.P = REAL.panels[name])
    if (!P) throw new Error(`no real panel ${name}: run tools/realbox/capture-states.mjs`)
    const f = (this.frame = document.createElement('iframe'))
    f.className = 'realpanel'
    f.setAttribute('scrolling', 'no')
    f.style.cssText = `position:absolute;left:0;top:0;width:${P.width}px;height:${P.height}px;border:0;margin:0;` +
      'transform-origin:0 0;background:transparent;pointer-events:none;'
    parent.insertBefore(f, before)
    const doc = (this.doc = f.contentDocument)
    doc.open()
    doc.write(realDocHtml(theme))
    doc.close()
    aliasPseudo(doc)
    this.root = doc.getElementById('root')
    this.state = null
    this.marks = ''
    this.t0 = new WeakMap()
  }

  get width() {
    return this.P.width
  }

  get height() {
    return this.P.height
  }

  has(state) {
    return Boolean(this.P.states[state])
  }

  /** Puts a captured state in (the whole #root, as the real panel had it). Returns true when it changed. */
  show(state) {
    if (state === this.state) return false
    const s = this.P.states[state]
    if (!s) throw new Error(`real panel ${this.P.name ?? ''}: no state ${state}`)
    const doc = this.doc
    this.root.innerHTML = s.html
    const st = doc.documentElement.style
    for (let i = st.length - 1; i >= 0; i--) if (st[i].startsWith('--cx')) st.removeProperty(st[i])
    for (const [k, v] of Object.entries(s.vars ?? {})) st.setProperty(k, v)
    doc.querySelectorAll('body > .rb-extra').forEach(n => n.remove())
    for (const x of s.extras ?? []) {
      const t = doc.createElement('template')
      t.innerHTML = x
      const n = t.content.firstElementChild
      if (n) {
        n.classList.add('rb-extra')
        doc.body.append(n)
      }
    }
    this.state = state
    this.marks = ''
    this.snap = s
    return true
  }

  q(sel) {
    return this.doc.querySelector(sel)
  }

  qa(sel) {
    return [...this.doc.querySelectorAll(sel)]
  }

  get box() {
    return this.q('fieldset[class*="inputContainer_"]')
  }

  /** An element's box in the panel's own CSS px. */
  rect(el) {
    if (typeof el === 'string') el = this.q(el)
    if (!el) return null
    const r = el.getBoundingClientRect()
    return { x: r.left, y: r.top, w: r.width, h: r.height, r: r.right, b: r.bottom }
  }

  /**
   * What the real CSS reacts to: { focus: el, hover: el, active: el } (elements, selectors or the snapshot's own
   * recorded paths: 'snap'). Focus marks the element (:focus, and :focus-visible for text fields) and its
   * ancestors (:focus-within); hover and active mark the element and its ancestors, as the browser does.
   */
  mark(o = {}) {
    const resolve = v => (v === 'snap' ? null : typeof v === 'string' ? this.q(v) : v ?? null)
    const s = this.snap ?? {}
    const focus = o.focus === 'snap' ? nodeAt(this.root, s.focus) : resolve(o.focus)
    const hover = o.hover === 'snap' ? nodeAt(this.root, s.hover) : resolve(o.hover)
    const active = o.active === 'snap' ? nodeAt(this.root, s.active) : resolve(o.active)
    const key = [focus, hover, active].map(el => (el ? this.qa('*').indexOf(el) : -1)).join(',')
    if (key === this.marks) return
    this.marks = key
    for (const a of ['focus', 'focus-visible', 'focus-within', 'hover', 'active']) {
      for (const n of this.doc.querySelectorAll(`[data-rb-${a}]`)) n.removeAttribute(`data-rb-${a}`)
    }
    const up = (el, a) => {
      for (let n = el; n && n.nodeType === 1; n = n.parentElement) n.setAttribute(`data-rb-${a}`, '')
    }
    if (focus) {
      focus.setAttribute('data-rb-focus', '')
      if (focus.isContentEditable || /^(TEXTAREA|INPUT)$/.test(focus.tagName)) focus.setAttribute('data-rb-focus-visible', '')
      up(focus, 'focus-within')
    }
    if (hover) up(hover, 'hover')
    if (active) up(active, 'active')
  }

  /** The prompt as typed so far: the real input keeps it in the contenteditable and its mention mirror. */
  type(text) {
    const input = this.q('[class*="messageInput_"][contenteditable]')
    const mirror = this.q('[class*="mentionMirror_"]')
    if (input && input.textContent !== text) input.textContent = text
    if (mirror && mirror.textContent !== text) mirror.textContent = text
  }

  /** The side question's textarea, as typed so far. */
  typeSide(text) {
    const ta = this.q('textarea[aria-label="Ask a side question"]')
    if (ta && ta.value !== text) ta.value = text
  }

  /**
   * Clawd, mounted the way the patch mounts him (custom.js mount): a .cx-clawd element inside the box, before its
   * background (after the Ultracode edge layers, which draw under him), placed by custom.css (top -60px, right 10px)
   * and moved by --cx-x / --cx-y (px from that home spot). So whatever the extension and the patch draw later in
   * the box (the effort bubble, the compact confirm) or over it (the /btw bubble, menus) covers him, as it does in
   * the real panel. Returns the element; the video puts his animation in it.
   */
  clawd(x, y) {
    let el = this.clawdEl
    if (!el) {
      el = this.clawdEl = this.doc.createElement('div')
      el.className = 'cx-clawd'
      el.setAttribute('aria-hidden', 'true')
    }
    const box = this.box
    if (box && el.parentNode !== box) box.insertBefore(el, box.querySelector(':scope > [class*="inputContainerBackground_"]') ?? box.firstChild)
    el.style.setProperty('--cx-x', `${x}px`)
    el.style.setProperty('--cx-y', `${y}px`)
    return el
  }

  /** His home spot's offset (custom.js world(): homeX / homeY), in the panel's px: his image's top left at home. */
  clawdHome() {
    const box = this.box
    const r = box.getBoundingClientRect()
    const cs = this.doc.defaultView.getComputedStyle(box)
    return { x: r.right - parseFloat(cs.borderRightWidth) - 10 - 96, y: r.top + parseFloat(cs.borderTopWidth) - 60 }
  }

  /**
   * Seeks every CSS animation in the panel: t0(anim) gives the video time its element started (default: `base`,
   * when the state came in), `t` is now. Looping ones use the same clock, so they never jump on a state swap.
   * Clawd's own animation is the video's (setClip), not the panel's.
   */
  seek(t, base, t0 = () => undefined) {
    for (const a of this.doc.getAnimations()) {
      const el = a.effect?.target
      if (el?.closest?.('.cx-clawd')) continue
      a.pause()
      const start = t0(a, el) ?? base
      a.currentTime = Math.max(0, (t - start) * 1000)
    }
  }
}

// ---------------------------------------------------------------------------------------------------------------
// The panel's "Claude is working" spinner (its own JS in the extension: the glyph steps every 120 ms through
// · ✢ * ✶ ✻ ✽ and back; the word changes after 2 s, 3 s, then every 5 s, wiping in 40 ms a letter with a ▌ and two
// scrambled letters behind it). The same rules here, with a seeded random, so a frame only depends on its time.
// ---------------------------------------------------------------------------------------------------------------

const SPIN_GLYPHS = ['·', '✢', '*', '✶', '✻', '✽']
const SPIN = [...SPIN_GLYPHS, ...[...SPIN_GLYPHS].reverse()]

function rng(seed) {
  let s = seed | 0
  return () => {
    s = (s + 0x6d2b79f5) | 0
    let t = Math.imul(s ^ (s >>> 15), 1 | s)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

/** The spinner's glyph and text `dt` seconds after it appeared (words picked from the panel's own list). */
function spinnerAt(dt, seed = 7) {
  const verbs = REAL.verbs
  const maxLen = Math.max(...verbs.map(v => v.length))
  const glyph = SPIN[Math.floor(Math.max(0, dt) / 0.12) % SPIN.length]
  // when the word changes: 0 (first), +2 s, +3 s, then every 5 s
  const at = [0, 2, 5]
  while (at[at.length - 1] <= dt) at.push(at[at.length - 1] + 5)
  let k = 0
  while (k + 1 < at.length && at[k + 1] <= dt) k++
  const r = rng(seed)
  const words = []
  for (let i = 0; i <= k; i++) words.push(verbs[Math.floor(r() * verbs.length)])
  const pad = s => s + ' '.repeat(Math.max(0, maxLen + 3 - s.length))
  const target = pad(words[k] + '...')
  let prev = k === 0 ? ' '.repeat(target.length) : pad(words[k - 1] + '...')
  // the wipe: index u advances every 40 ms; at u, positions u-3..u are [final, scramble, scramble, ▌]
  const u = Math.floor((dt - at[k]) / 0.04)
  if (u - 3 >= target.length) return { glyph, text: target }
  const sr = rng(seed * 31 + k * 977 + u)
  let out = ''
  for (let g = 0; g < target.length; g++) {
    const f = u - g // 0: the ▌, 1-2: scrambled, 3+: final, <0: still the old text
    out += f < 0 ? prev[g] ?? ' ' : f >= 3 || target[g] === ' ' ? target[g] : f === 0 ? '▌' : ['.', '_', target[g]][Math.floor(sr() * 3)]
  }
  return { glyph, text: out }
}
