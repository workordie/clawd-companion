'use strict'
/*
 * clawd-companion showcase engine.
 *
 * One time value t (seconds of video) decides everything on screen. seek(t) lays the frame out, puts the Clawd SVGs
 * it needs inline (real <svg> elements, so their CSS animations are in document.getAnimations()), pauses every one of
 * those animations and sets its currentTime from t. Nothing runs on its own, so the same t always gives the same
 * picture: capture.mjs steps t frame by frame.
 *
 *   showcase.html?style=A|B|C&cut=wide|tall&t=12.5      a still (scaled to fit the window)
 *   ...&play                                               play in real time (space: play/pause, arrows: +-beat)
 *   ...&audio=<url of the soundtrack>                      with the music, from t = 0 (preview only)
 *   ...&theme=dark                                         the dark version (white mode is the default)
 *   ...&capture                                            the stage at 1:1, no HUD (capture.mjs)
 *
 * The world is measured in Clawd's pixel-art cells (one cell = 3 CSS px in the real chat panel, where he is 96x60).
 * Its origin is the input box's top-right corner: X to the right, Y down, the box's top surface (the inside of its
 * top border, where he stands) at Y = 0. The motion rules are custom.js's ("Moving him"), ported to cells.
 */

// ---------------------------------------------------------------------------------------------------------------
// Clips
// ---------------------------------------------------------------------------------------------------------------

const CLIPS = JSON.parse(document.getElementById('clawd-svgs').textContent)
const has = name => Object.hasOwn(CLIPS, name)
const cycle = name => (CLIPS[name]?.ms ?? 6000) / 1000 // seconds
// played once by the patch: hold the last frame instead of looping
const ONCE = /^(in-|out-|click-|hop-|land|crash|notice$|pet$|look-up-|teeter-|talk-explain$|chute-pop$|hello)/

// ---------------------------------------------------------------------------------------------------------------
// The beat grid of the soundtrack ("Technology" by Sub_Clair, measured with tools/): 125.0 BPM, steady; bar k's downbeat
// at 0.966 + 1.92 k s into the track. A cut's audioStart is where its t = 0 sits in the track (capture.mjs --music-start).
// ---------------------------------------------------------------------------------------------------------------

const MUSIC = { bpm: 125, beat: 0.48, bar: 1.92, bar0: 0.966 }
// the user's VS Code theme, Default High Contrast Light, by default (?theme=light: Light Modern, dark: Dark Modern)
const THEME = (q => (['light', 'dark', 'hc-light'].includes(q) ? q : 'hc-light'))(new URLSearchParams(location.search).get('theme'))
// the looks' classes: HC Light is a white look (light) whose VS Code parts take the theme's own colours (hc)
const THEME_CLASS = THEME === 'hc-light' ? 'light hc' : THEME
// checks (tools/realbox/check-scale.mjs): the panel alone, no Clawd
const NOCLAWD = new URLSearchParams(location.search).has('noclawd')

/** The theme's computed --vscode-* variables and its code token colours (--tok-*) on a look's root. */
function themeVars(el) {
  const t = REAL.themes[THEME]
  for (const [k, v] of Object.entries(t.styles)) el.style.setProperty(`--${k}`, v)
  for (const [k, v] of Object.entries(t.tokens)) el.style.setProperty(`--tok-${k}`, v)
}

// ---------------------------------------------------------------------------------------------------------------
// World (cells)
// ---------------------------------------------------------------------------------------------------------------

// the chat column and the box as the real panel lays them out (the B/A2 panel, tools/realbox): his surface is the
// inside of the box's 1 px top border, the floor the column's bottom, the wall its right side (custom.js world())
const STAGE_GEO = (() => {
  const g = REAL.panels.stage.states['mode-default'].geometry
  return { surface: g.box.y + 1, right: g.box.x + g.box.w, floor: g.column.y + g.column.h, wall: g.column.x + g.column.w, ceil: g.column.y }
})()
const WORLD = {
  F: (STAGE_GEO.floor - STAGE_GEO.surface) / 3, // the bottom of the chat column, below his surface (89 px: 73 + 16)
  BH: 74 / 3, // the box's outer height
  RW: (STAGE_GEO.wall - STAGE_GEO.right) / 3, // the column's right side, right of the box's right end (84 px)
  BW: 150, // the box's width (only its right end matters for the moves)
  CEIL: (STAGE_GEO.ceil - STAGE_GEO.surface) / 3, // the column's top
}
const FEET = [15.5, 20] // his feet's centre in the 32x20 image
const ANCHOR = { 'sit-edge-left': [15.5, 17], 'sit-edge-right': [15.5, 17] }
const HOME = -(1 + 10 + 96 - 46.5) / 3 // his feet at home: 10 px from the box's right end (custom.css)
const EDGE = -2.5 // the edge spot (teeter, sit-edge, hop)
const BODY_HALF = 5.5
const BODY_H = 8
const WALK = 4 // cells/s, the walk SVGs' stride
const CLIMB = 6 // cells/s, the climb SVGs' stride
const G = 160 // cells/s^2
const CHUTE = 9 // cells/s under the parachute
const CAMS = {
  home: [HOME + 1, -3], // Clawd at home, centred
  edge: [-6, 2], // the box's right end
  side: [6, 10], // the box's right side down to the floor (hop, fall, climb)
}

// ---------------------------------------------------------------------------------------------------------------
// Flight: custom.js fly(), fixed step. Thrown ('tumble'), let go high ('fall': the chute opens), let go low
// ('drop'), off the end of the box ('hop'). Returns the path and the clip changes; lands on the box or the floor.
// ---------------------------------------------------------------------------------------------------------------

function simulate(x, y, vx, vy, mode, { cutAt = Infinity } = {}) {
  const dt = 1 / 600
  const path = [[x, y]]
  const ev = []
  let t = 0
  let chute = false
  let cut = false
  for (let i = 0; i < 600 * 30; i++) {
    t = (i + 1) * dt
    const overBox = x <= 0 && x >= -WORLD.BW
    const ground = overBox && y <= 1 / 3 ? 0 : WORLD.F
    if (mode === 'fall' && !chute && !cut && t > 0.38 && ground - y > 8 && has('parachute')) {
      chute = true
      ev.push([t, 'parachute'])
    }
    if (chute && t >= cutAt) {
      chute = false
      cut = true
      vx *= 0.3
      ev.push([t, 'chute-pop'], [t + cycle('chute-pop'), 'fall'])
    }
    if (mode === 'hop' && ev.length === 0 && t > 0.4) ev.push([t, 'fall'])
    if (chute) {
      vy = CHUTE
      vx = Math.sin(t / 0.7) * 2
    } else vy += G * dt
    const py = y
    x += vx * dt
    y += vy * dt
    if (x > WORLD.RW - BODY_HALF) {
      x = WORLD.RW - BODY_HALF
      vx = -Math.abs(vx) * 0.55
    }
    if (y - BODY_H < WORLD.CEIL) {
      y = WORLD.CEIL + BODY_H
      vy = Math.abs(vy) * 0.3
    }
    const over = x <= 0 && x >= -WORLD.BW
    let on = ''
    if (over && vy > 0 && py <= 1 / 3 && y >= 0) on = 'box'
    else if (y > 0 && y - BODY_H < WORLD.BH) {
      if (over) on = 'box'
      else if (x < BODY_HALF && x > 0) {
        x = BODY_HALF
        vx = Math.abs(vx) * 0.55
      }
    }
    if (!on && y >= WORLD.F) on = 'floor'
    if (on) {
      y = on === 'box' ? 0 : WORLD.F
      path.push([x, y])
      const hard = mode === 'tumble' || (mode !== 'hop' && vy > 70)
      const clip = chute ? 'land-chute' : hard ? 'crash' : 'land'
      return { ev: ev.filter(e => e[0] < t), land: { t, X: x, Y: y, on, clip }, at: lt => sample(path, dt, lt) }
    }
    path.push([x, y])
  }
  throw new Error('flight never landed')
}

function sample(path, dt, lt) {
  const f = Math.max(0, lt / dt)
  const i = Math.min(path.length - 1, Math.floor(f))
  const j = Math.min(path.length - 1, i + 1)
  const k = f - i
  return [path[i][0] + (path[j][0] - path[i][0]) * k, path[i][1] + (path[j][1] - path[i][1]) * k]
}

// ---------------------------------------------------------------------------------------------------------------
// Clawd's track: what he plays and where his feet are, as segments in video time. Built with a cursor time `t`
// that each step advances; `at(t)` jumps (a cut), `to(X, Y)` teleports (a jump cut).
// ---------------------------------------------------------------------------------------------------------------

class Track {
  constructor(X = HOME, Y = 0) {
    this.segs = []
    this.t = 0
    this.X = X
    this.Y = Y
  }
  at(t) {
    this.t = t
    return this
  }
  to(X, Y = this.Y) {
    this.X = X
    this.Y = Y
    return this
  }
  add(seg) {
    this.segs.push(seg)
    this.t = seg.t1
    if (seg.end) [this.X, this.Y] = seg.end
    return this
  }
  /** Plays `clip` where he is, for `dur` s (default: one cycle). Options: ct0 (start that far into the clip), rate. */
  play(clip, dur = cycle(clip), o = {}) {
    if (!has(clip)) throw new Error(`no clip ${clip}`)
    return this.add({ t0: this.t, t1: this.t + dur, clip, at: [this.X, this.Y], ...o })
  }
  /** Plays `clip` until video time t. */
  until(t, clip, o) {
    return this.play(clip, Math.max(0, t - this.t), o)
  }
  /** Plays `clip` so that it ENDS at video time t (a set-up landing on a beat). */
  endingAt(t, clip) {
    return this.at(t - cycle(clip)).play(clip)
  }
  /** Scene change the patch's way: pack `from` away (out-*), set `to` up (in-*), `to` starts exactly at t. */
  swap(from, to, t) {
    const inn = has(`in-${to}`) ? `in-${to}` : ''
    const out = from && has(`out-${from}`) ? `out-${from}` : ''
    const tIn = t - (inn ? cycle(inn) : 0)
    const tOut = tIn - (out ? cycle(out) : 0)
    if (from) this.until(tOut, from)
    else this.at(tOut)
    if (out) this.play(out)
    if (inn) this.play(inn)
    return this
  }
  walkTo(X) {
    const x0 = this.X
    const Y = this.Y
    const d = Math.abs(X - x0)
    if (d < 1e-3) return this
    const dir = Math.sign(X - x0)
    return this.add({ t0: this.t, t1: this.t + d / WALK, clip: dir < 0 ? 'walk-left' : 'walk-right', pos: lt => [x0 + dir * Math.min(d, WALK * lt), Y], end: [X, Y] })
  }
  /** Walks so that he arrives at X exactly at video time t. */
  walkArriving(X, t) {
    return this.at(t - Math.abs(X - this.X) / WALK).walkTo(X)
  }
  /** A flight from where he is; `first` is the clip it starts with (ct0: that far into it). Ends with the landing. */
  fly(vx, vy, mode, first, o = {}) {
    const sim = simulate(this.X, this.Y, vx, vy, mode, o)
    const t0 = this.t
    const phases = [[0, first, o.ct0 ?? 0], ...sim.ev.map(([t, c]) => [t, c, 0])]
    phases.forEach(([pt, clip, ct0], i) => {
      const nt = i + 1 < phases.length ? phases[i + 1][0] : sim.land.t
      this.segs.push({ t0: t0 + pt, t1: t0 + nt, clip, ct0, pos: lt => sim.at(pt + lt) })
    })
    this.t = t0 + sim.land.t
    this.X = sim.land.X
    this.Y = sim.land.Y
    this.landed = { ...sim.land, t: t0 + sim.land.t }
    return this.play(sim.land.clip)
  }
  /** Off the end of the box: the hop's wind-up (150 ms on the ground), the arc, the fall, the landing. */
  hopOff(side = 'R') {
    const clip = side === 'R' ? 'hop-right' : 'hop-left'
    this.play(clip, 0.15)
    return this.fly(side === 'R' ? 26 : -26, -36, 'hop', clip, { ct0: 0.15 })
  }
  /** Up the box's right side like a crab (climb-left: the wall on his left), then a quarter turn onto the box. */
  climbUp() {
    const x = BODY_HALF
    const y0 = this.Y
    const top = 8
    this.add({ t0: this.t, t1: this.t + (y0 - top) / CLIMB, clip: 'climb-left', pos: lt => [x, Math.max(top, y0 - CLIMB * lt)], end: [x, top] })
    return this.to(-BODY_HALF, 0)
  }
  /** Picked up by the cursor: from now his feet follow it (custom.js onMove), playing `clip` for `dur` s. */
  drag(cursor, dur, clip, o = {}) {
    if (!this.grip) {
      const [cx, cy] = cursor.at(this.t).p
      this.grip = [this.X - cx, this.Y - cy]
    }
    const [gx, gy] = this.grip
    const t0 = this.t
    const p = lt => {
      const [cx, cy] = cursor.at(t0 + lt).p
      return [cx + gx, cy + gy]
    }
    const end = p(dur)
    return this.add({ t0, t1: t0 + dur, clip, pos: p, end, ...o })
  }
  /** Let go: thrown if the cursor was moving fast, else dropped (custom.js onUp). */
  release(cursor) {
    this.grip = null
    const a = cursor.at(this.t).p
    const b = cursor.at(this.t - 0.09).p
    const vx = (a[0] - b[0]) / 0.09
    const vy = (a[1] - b[1]) / 0.09
    const ground = this.X <= 0 && this.Y <= 0 ? 0 : WORLD.F
    if (Math.hypot(vx, vy) > 45) return this.fly(vx, vy, 'tumble', 'tumble')
    if (ground - this.Y > 9) return this.fly(0, 0, 'fall', 'fall', this.chuteCut ?? {})
    return this.fly(0, 0, 'drop', 'grabbed')
  }
  done() {
    this.segs.sort((a, b) => a.t0 - b.t0)
    return this
  }
}

/** The track at time t: the clip, how far into it, and where his feet are. */
function trackAt(track, t) {
  let s = null
  for (const seg of track.segs) {
    if (seg.t0 <= t + 1e-9) s = seg
    else break
  }
  s ??= track.segs[0]
  if (!s) return null
  const lt = Math.max(0, t - s.t0)
  const [X, Y] = s.pos ? s.pos(Math.min(lt, s.t1 - s.t0)) : s.at
  return { clip: s.clip, ct: (s.ct0 ?? 0) + lt, rate: s.rate ?? 1, X, Y }
}

// ---------------------------------------------------------------------------------------------------------------
// The mouse cursor: keyframes in world cells (it moves with the world), eased; kinds arrow | hand | grab | none.
// ---------------------------------------------------------------------------------------------------------------

class Cursor {
  constructor() {
    this.keys = []
    this.clicks = []
  }
  /** At time t the cursor is at (X, Y), showing `kind`; it eases there from the previous key. */
  key(t, X, Y, kind = 'arrow', ease = 'io') {
    this.keys.push({ t, X, Y, kind, ease })
    this.keys.sort((a, b) => a.t - b.t)
    return this
  }
  click(t) {
    this.clicks.push(t)
    return this
  }
  at(t) {
    const k = this.keys
    if (!k.length || t < k[0].t) return { p: [0, 0], kind: 'none' }
    for (let i = 1; i < k.length; i++) {
      if (t < k[i].t) {
        const a = k[i - 1]
        const b = k[i]
        let u = (t - a.t) / (b.t - a.t)
        if (b.ease === 'io') u = u < 0.5 ? 2 * u * u : 1 - 2 * (1 - u) * (1 - u)
        else if (b.ease === 'out') u = 1 - (1 - u) * (1 - u)
        else if (b.ease === 'step') u = 0
        return { p: [a.X + (b.X - a.X) * u, a.Y + (b.Y - a.Y) * u], kind: a.kind }
      }
    }
    const z = k[k.length - 1]
    return { p: [z.X, z.Y], kind: z.kind }
  }
}

// pixel-art cursors (16 px wide), # = black, o = white
const CURSOR_ART = {
  arrow: [
    '#', '##', '#o#', '#oo#', '#ooo#', '#oooo#', '#ooooo#', '#oooooo#', '#ooooooo#', '#oooooooo#', '#ooooo#####',
    '#oo#oo#', '#o# #oo#', '##  #oo#', '#    #oo#', '     #oo#', '      ##',
  ],
  hand: [
    '      ##', '   ## #o###', '  #oo##oo#o#', '  #oo##oo#oo#', '   #oo#oo#oo# #', '   #oo#oo#oo##o#', ' ## #ooooooo#oo#',
    '#oo##oooooooooo#', '#ooo#ooooooooo#', ' #ooooooooooooo#', '  #oooooooooooo#', '  #ooooooooooo#', '   #oooooooooo#',
    '    #oooooooo#', '     #ooooooo#', '     #ooooooo#',
  ],
  grab: [
    '', '', '', '    ## ## ##', '   #oo#oo#oo##', '   #oooooooo#o#', '  ##ooooooooooo#', ' #oo#ooooooooooo#', ' #ooooooooooooo#',
    '  #oooooooooooo#', '   #ooooooooooo#', '    #oooooooooo#', '     #oooooooo#', '      #ooooooo#', '      #ooooooo#',
  ],
}
CURSOR_ART.point = [
  '    ##', '   #oo#', '   #oo#', '   #oo#', '   #oo###', '   #oo#oo##', '   #oo#oo#o##', '## #oo#oo#o#o#', '#oo#oooooooo#o#',
  '#ooooooooooooo#', ' #oooooooooooo#', '  #ooooooooooo#', '  #oooooooooo#', '   #ooooooooo#', '    #ooooooo#', '    #ooooooo#', '    #########',
]
const CURSOR_HOT = { arrow: [0.5, 0.5], hand: [8, 8], grab: [8, 9], point: [4.5, 0.5] } // the hotspot, in cursor pixels

/** Draws the cursor `kind` with its hotspot at (x, y), each cursor pixel `px` screen px. */
function drawCursor(el, kind, x, y, px) {
  if (!kind || kind === 'none') {
    el.classList.add('off')
    return
  }
  el.classList.remove('off')
  if (el.dataset.kind !== kind) {
    el.innerHTML = cursorSvg(kind)
    el.dataset.kind = kind
  }
  const [hx, hy] = CURSOR_HOT[kind]
  el.style.width = `${16 * px}px`
  el.style.height = `${18 * px}px`
  el.style.transform = `translate(${Math.round(x - hx * px)}px, ${Math.round(y - hy * px)}px)`
}

function cursorSvg(kind) {
  const rows = CURSOR_ART[kind]
  let d = ''
  let o = ''
  rows.forEach((r, y) => {
    for (let x = 0; x < r.length; x++) {
      if (r[x] === '#') d += `M${x} ${y}h1v1h-1z`
      else if (r[x] === 'o') o += `M${x} ${y}h1v1h-1z`
    }
  })
  return `<svg viewBox="0 0 16 18" width="100%" height="100%" shape-rendering="crispEdges"><path d="${o}" fill="#fff"/><path d="${d}" fill="#000"/></svg>`
}

// ---------------------------------------------------------------------------------------------------------------
// Cuts. A cut = an aspect, where the music starts, and its scenes, captions, Clawd's track and the cursor, all on
// the music's grid: bar(k) is bar k's downbeat in video time, beat(k, b) beat b (0-3) of it.
// ---------------------------------------------------------------------------------------------------------------

const CUTS = {}

function makeCut(id, o, build) {
  const bar = (k, b = 0) => +(MUSIC.bar0 + k * MUSIC.bar + b * MUSIC.beat - o.audioStart).toFixed(4)
  const cut = { id, ...o, bar, scenes: [], captions: [], flashes: [] }
  cut.track = new Track()
  cut.cursor = new Cursor()
  build(cut)
  cut.track.done()
  cut.scenes.sort((a, b) => a.t0 - b.t0)
  cut.captions.sort((a, b) => a[0] - b[0])
  CUTS[id] = cut
  return cut
}

const lastAt = (list, t, key = x => x.t0) => {
  let r = null
  for (const x of list) {
    if (key(x) <= t + 1e-9) r = x
    else break
  }
  return r
}

// ---------------------------------------------------------------------------------------------------------------
// Putting the SVGs in and seeking them
// ---------------------------------------------------------------------------------------------------------------

/** Shows `clip` in `slot` (an inline <svg>), at `sec` seconds into it. */
function setClip(slot, clip, sec, rate = 1) {
  if (!clip) {
    slot.classList.add('off')
    slot.style.display = 'none'
    return
  }
  slot.classList.remove('off')
  slot.style.display = ''
  if (slot.dataset.clip !== clip) {
    slot.innerHTML = CLIPS[clip].svg
    slot.dataset.clip = clip
    slot._anims = null
  }
  const c = CLIPS[clip]
  let ms = Math.max(0, sec * 1000 * rate)
  if (c.once || ONCE.test(clip)) ms = Math.min(ms, c.ms - 1)
  slot._anims ??= slot.getAnimations({ subtree: true })
  for (const a of slot._anims) {
    a.pause()
    a.currentTime = ms
  }
}

function makeSlot(parent, s) {
  const el = document.createElement('div')
  el.className = 'clawd off'
  el.style.width = `${32 * s}px`
  el.style.height = `${20 * s}px`
  parent.append(el)
  return el
}

/** Places a Clawd image so that his feet's centre (anchor) lands on screen point (fx, fy). */
function placeClawd(el, clip, fx, fy, s) {
  const [ax, ay] = ANCHOR[clip] ?? FEET
  el.style.transform = `translate(${Math.round(fx - ax * s)}px, ${Math.round(fy - ay * s)}px)`
}

// ---------------------------------------------------------------------------------------------------------------
// Shared pieces: captions text, the speech bubble, the wall of Clawds, the end card, the cursor
// ---------------------------------------------------------------------------------------------------------------

const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v))
const esc = s => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c])

function captionAt(cut, t) {
  const c = lastAt(cut.captions, t, x => x[0])
  return c && c[1] ? { text: c[1], sub: c[2] ?? '', t0: c[0] } : null
}

function renderWall(ctx, f, wall) {
  const { el, slots, tiles, s, W, tw, th, rows, cols, y0 } = ctx
  el.classList.toggle('on', Boolean(wall))
  if (!wall) {
    for (const sl of slots) setClip(sl, null)
    return
  }
  const step = Math.max(0, Math.floor((f.t - wall.t0) / MUSIC.beat))
  const x0 = Math.round((W - Math.floor(W / tw) * tw) / 2 + 6)
  let n = 0
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const slot = slots[n]
      const tile = tiles[n++]
      const idx = (step + c) * rows + r
      const clip = wall.clips[idx % wall.clips.length]
      const left = x0 + c * tw
      const top = y0 + r * th
      slot.style.transform = `translate(${left}px, ${top}px)`
      tile.style.transform = `translate(${left}px, ${top}px)`
      tile.lastChild.textContent = clip
      setClip(slot, clip, f.t - wall.t0 + (idx % 7) * 0.9)
    }
  }
  ctx.count.textContent = wall.label ?? ''
  void s
}

function buildWall(stage, s, W, H) {
  const el = document.createElement('div')
  el.className = 'wall'
  stage.append(el)
  const count = document.createElement('div')
  count.className = 'count'
  el.append(count)
  const tw = 32 * s + Math.max(12, s * 2)
  const th = 20 * s + Math.max(46, Math.round(s * 2.8))
  const head = Math.round(H * (H > W ? 0.12 : 0.17))
  const rows = Math.max(1, Math.floor((H - head - 40) / th))
  const cols = Math.floor(W / tw)
  const y0 = Math.round(head + (H - head - rows * th) / 2)
  count.style.cssText = `left:${Math.round((W - cols * tw) / 2 + 6)}px;top:${Math.round(head * (H > W ? 0.25 : 0.3))}px;font-size:${Math.round(head * (H > W ? 0.3 : 0.42))}px`
  const slots = []
  const tiles = []
  for (let i = 0; i < cols * rows; i++) {
    const tile = document.createElement('div')
    tile.className = 'tile'
    tile.style.width = `${32 * s}px`
    tile.style.height = `${20 * s}px`
    tile.innerHTML = `<div class="shelf" style="top:${20 * s}px"></div><div class="nm" style="top:${20 * s + Math.round(s * 1.2)}px"></div>`
    el.append(tile)
    tiles.push(tile)
    slots.push(makeSlot(el, s))
  }
  return { el, slots, tiles, s, W, H, tw, th, rows, cols, y0, count }
}

function buildEnd(stage, s, W, H, aspect) {
  const el = document.createElement('div')
  el.className = 'endcard'
  const tall = aspect === '9x16'
  // he stands centred on a shelf (like the wall's): no drawn input box; the real one is in every other shot
  const shelfW = Math.round(-2 * HOME * s)
  const shelfL = Math.round((W - shelfW) / 2)
  const shelfT = Math.round(tall ? H * 0.52 : H * 0.6)
  el.innerHTML = `
    <div class="ttl" style="top:${tall ? 320 : 110}px;${tall ? 'font-size:112px' : ''}">clawd-companion</div>
    <div class="sub" style="top:${tall ? 470 : 285}px">${tall ? 'Clawd lives on your<br>Claude Code input box.' : 'Clawd lives on your Claude Code input box.'}</div>
    <div class="eshelf" style="left:${shelfL}px;top:${shelfT}px;width:${shelfW}px"></div>
    <div class="url" style="top:${shelfT + (tall ? 180 : 130)}px">github.com/workordie/clawd-companion</div>
    <div class="fine" style="top:${H - (tall ? 250 : 110)}px">${tall ? 'Unofficial fan project, not affiliated with Anthropic.<br>Clawd and Claude belong to Anthropic.' : 'Unofficial fan project, not affiliated with Anthropic. Clawd and Claude belong to Anthropic.'}</div>`
  stage.append(el)
  const slot = makeSlot(el, s)
  return { el, slot, s, fx: shelfL + shelfW / 2, fy: shelfT }
}

function renderEnd(ctx, f, end) {
  ctx.el.classList.toggle('on', Boolean(end))
  if (!end) return setClip(ctx.slot, null)
  const clip = f.t - end.t0 < cycle(end.clip) ? end.clip : end.then ?? end.clip
  const ct = clip === end.clip ? f.t - end.t0 : f.t - end.t0 - cycle(end.clip)
  placeClawd(ctx.slot, clip, ctx.fx, ctx.fy, ctx.s)
  setClip(ctx.slot, clip, ct)
}

function renderCursor(el, cur, f, toScreen, px) {
  const c = cur.at(f.t)
  if (c.kind === 'none') {
    el.classList.add('off')
    return
  }
  el.classList.remove('off')
  if (el.dataset.kind !== c.kind) {
    el.innerHTML = cursorSvg(c.kind)
    el.dataset.kind = c.kind
  }
  const [hx, hy] = CURSOR_HOT[c.kind]
  const [x, y] = toScreen(c.p[0], c.p[1])
  el.style.width = `${16 * px}px`
  el.style.height = `${18 * px}px`
  el.style.transform = `translate(${Math.round(x - hx * px)}px, ${Math.round(y - hy * px)}px)`
}

// ---------------------------------------------------------------------------------------------------------------
// The real panel (src/realpanel.js) in the looks: which captured state a frame shows, what the real CSS reacts to,
// and when each of its animations started.
// ---------------------------------------------------------------------------------------------------------------

const LEVELS = ['low', 'medium', 'high', 'xhigh', 'max']
// the scenes' modes -> the panel's permission modes (it names them Manual, Plan, Auto-edit, Bypass, Auto)
const MODE_STATE = { manual: 'default', plan: 'plan', edits: 'acceptEdits', bypass: 'bypassPermissions', auto: 'auto' }
// Claude is busy (the box says "Queue another message…", send is a stop button) while Clawd plays one of these
const BUSY = /^(?:in-|out-)?(?:thinking|working|subagents|compacting|hooks|question|alert)\b/
// what the camera and the cursor aim at in the panel
const AIM = {
  range: '.cx-effort input',
  uc: '.cx-uc',
  ctx: '.cx-ctx',
  cancel: '.cx-pop .cx-btn-secondary',
  agents: '.cx-agents',
  input: '[class*="messageInput_"][contenteditable]',
  side: 'textarea[aria-label="Ask a side question"]',
}

/**
 * When a panel animation started (video time): the Ultracode layers at its click, the pops when they open, the
 * empty chat when the panel opened, the spinner row when Claude started. Loops run on the video's own clock (so a
 * state swap never makes them jump); anything else finished long ago.
 */
function animStart(a, el, ps) {
  const name = a.animationName ?? ''
  const cls = typeof el?.className === 'string' ? el.className : ''
  if (/^cx-uc-/.test(name)) return ps.ucAt ?? -100
  if (name === 'cx-pop-in') return /\bcx-bubble\b/.test(cls) ? ps.bubbleAt ?? -100 : ps.popAt ?? -100
  if (name === 'cx-pulse') return ps.agentsAt ?? 0
  if (/^fadeIn_/.test(name) && /spinnerRow_/.test(cls)) return ps.spinAt ?? -100
  if (/^fadeIn_/.test(name) && /emptyState_/.test(cls)) return ps.openAt ?? -100
  if (a.effect?.getTiming().iterations === Infinity) return 0
  return -100
}

/** What the panel's own JS keeps changing: its spinner (glyph and word) and the Ultracode button's 500 ms pop. */
function panelLive(panel, t, ps) {
  if (ps.spinAt !== undefined) {
    const row = panel.q('[class*="spinnerRow_"] [data-permission-mode]')
    if (row) {
      const sp = spinnerAt(t - ps.spinAt)
      const [icon, text] = row.children
      if (icon && icon.textContent !== sp.glyph) icon.textContent = sp.glyph
      if (text && text.textContent !== sp.text) text.textContent = sp.text
    }
  }
  const uc = panel.q('.cx-uc.cx-pop')
  if (uc && (ps.ucAt === undefined || t - ps.ucAt >= 0.5)) uc.classList.remove('cx-pop')
}

let measureCtx = null

/**
 * The text caret where the browser draws it: after the text in the focused field, 1 px wide, in the field's
 * caret-color (the frame's own one is off: it would blink on the wall clock). Solid while typing, then it blinks.
 */
function panelCaret(panel, caret, t) {
  const doc = panel.doc
  let c = panel.caretEl
  if (!c) {
    c = panel.caretEl = doc.createElement('div')
    c.style.cssText = 'position:fixed;width:1px;pointer-events:none;z-index:2147483647;display:none;'
    doc.body.append(c)
  }
  const el = caret && (typeof caret.el === 'string' ? panel.q(caret.el) : caret.el)
  const since = caret ? t - caret.from : 0
  if (!el || !(since <= 0 || Math.floor(since / 0.5) % 2 === 0)) {
    c.style.display = 'none'
    return
  }
  const cs = doc.defaultView.getComputedStyle(el)
  let x
  let y
  let h
  if (el.tagName === 'TEXTAREA') {
    measureCtx ??= document.createElement('canvas').getContext('2d')
    measureCtx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`
    const r = el.getBoundingClientRect()
    const fs = parseFloat(cs.fontSize)
    const lh = parseFloat(cs.lineHeight) || fs * 1.2
    h = Math.round(fs * 1.2)
    x = r.left + parseFloat(cs.borderLeftWidth) + parseFloat(cs.paddingLeft) + measureCtx.measureText(el.value).width
    y = r.top + parseFloat(cs.borderTopWidth) + parseFloat(cs.paddingTop) + (lh - h) / 2
  } else {
    let tmp = null
    if (!el.firstChild) el.append((tmp = doc.createTextNode('​')))
    const node = el.lastChild
    const range = doc.createRange()
    range.setStart(node, node.length)
    range.collapse(true)
    const rects = range.getClientRects()
    const r = rects[rects.length - 1] ?? range.getBoundingClientRect()
    x = r.left
    y = r.top
    h = r.height
    tmp?.remove()
  }
  c.style.display = ''
  c.style.background = cs.caretColor
  c.style.left = `${Math.round(x)}px`
  c.style.top = `${Math.round(y)}px`
  c.style.height = `${Math.round(h)}px`
}

/** A frame's panel state for the chat looks (A): the opener, Claude on it, the /btw bubble. */
function chatState(f, sc, spinAt) {
  const lt = f.t - sc.t0
  const ui = sc.ui ?? 'idle'
  const base = { spinAt, openAt: 0 }
  if (ui === 'new' || (ui === 'idle' && !sc.talk)) {
    if (sc.typing) {
      const cps = sc.cps ?? 18
      const n = Math.max(0, Math.min(sc.typing.length, Math.floor(lt * cps)))
      const text = sc.typing.slice(0, n)
      const lastKey = n < sc.typing.length ? f.t : sc.t0 + sc.typing.length / cps
      return { ...base, state: text ? 'typed' : 'idle', type: text, since: 0, marks: { focus: AIM.input }, caret: { el: AIM.input, from: lastKey } }
    }
    return { ...base, state: 'idle', since: 0, marks: sc.ring ? { focus: AIM.input } : {}, caret: sc.ring ? { el: AIM.input, from: sc.t0 } : null }
  }
  // Claude is on it: the prompt in the chat and his spinner; the box says "Queue another message…"
  const talk = sc.talk ? sc.talk(lt) : null
  if (!talk) return { ...base, state: 'thinking', since: spinAt }
  if (talk.state === 'listen') {
    const q = talk.q.slice(0, Math.round(talk.q.length * Math.max(0, Math.min(1, talk.typed ?? 1))))
    const typing = q.length > 0 && talk.typed < 1
    return { ...base, state: q ? 'talk-typed' : 'talk-open', side: q, since: sc.t0, marks: { focus: 'snap' }, caret: { el: AIM.side, from: typing ? f.t : sc.t0 } }
  }
  return { ...base, state: talk.state === 'think' ? 'talk-pending' : 'talk-answer', since: sc.t0, marks: { focus: 'snap' }, caret: { el: AIM.side, from: sc.t0 } }
}

/** A frame's panel state for the footer close-ups (A2): the modes, the effort slider, Ultracode, the tour. */
function footerState(f, sc, FS) {
  const lt = f.t - sc.t0
  if (!sc.footer) {
    // the modes: the mode menu's own label, the box's ring in the mode's colour
    const st = `mode-${MODE_STATE[sc.mode ?? 'auto']}`
    return { state: st, since: sc.t0, marks: sc.ring ? { focus: AIM.input } : {}, caret: sc.ring ? { el: AIM.input, from: sc.t0 } : null }
  }
  const level = LEVELS[FS.effort ?? 3]
  const ucAt = FS.ucAt !== undefined ? sc.t0 + FS.ucAt : undefined
  const ucOn = ucAt !== undefined && f.t >= ucAt
  const ps = { since: sc.t0, ucAt }
  if (FS.confirm && lt >= FS.confirm[0] && lt < FS.confirm[1]) {
    ps.state = 'confirm'
    ps.popAt = sc.t0 + FS.confirm[0]
  } else if (FS.agents?.n) {
    ps.state = 'agents-2'
    ps.agentsAt = sc.t0 + (FS.agents.at ?? 0)
  } else if (ucOn) ps.state = f.t - ucAt < 3.3 ? 'uc-on' : 'uc-hold' // custom.js drops the wave's layers at 3.3 s
  else if (FS.bubble) {
    ps.state = `effort-${level}-bubble`
    ps.bubbleAt = sc.t0 + FS.bubble
  } else ps.state = `effort-${level}`
  // focus as the real panel had it in that state; hover and pressed where this cursor is
  const hover = FS.drag || FS.hover ? AIM.range : FS.ptrOn ? AIM[FS.ptrOn] : null
  ps.marks = { focus: 'snap', hover, active: FS.drag ? AIM.range : null }
  return ps
}

/**
 * His /btw bubble (the panel's side question, which custom.css styles as a speech bubble): placed by custom.js
 * placeTalk from where his feet are (fx, fy in the panel's px), inside the chat column, its tail pointing at him.
 */
function placeTalk(panel, fx, fy) {
  const bubble = panel.q('.cx-talk')
  if (!bubble) return
  const col = panel.snap.geometry.column
  const IMG_H = 60
  const width = bubble.offsetWidth || 360
  const bottom = fy - IMG_H + 2 // the bubble's bottom edge: his image's top row is empty
  const lo = col.x + 8
  const left = clamp(fx - width * 0.78, lo, Math.max(lo, col.x + col.w - 8 - width))
  const st = panel.doc.documentElement.style
  st.setProperty('--cx-bl', `${Math.round(left)}px`)
  st.setProperty('--cx-bb', `${Math.round(panel.height - bottom)}px`)
  st.setProperty('--cx-bh', `${Math.round(Math.max(120, bottom - col.y - 8))}px`)
  st.setProperty('--cx-tl', `${Math.round(clamp(fx - 6, left + 16, left + width - 28))}px`)
  st.setProperty('--cx-tt', `${Math.round(bottom - 7)}px`)
}

/** Applies a panel state to a panel at video time t (`layout`: what places things in it, before the caret is measured). */
function showPanel(panel, ps, t, layout = null) {
  panel.show(ps.state)
  if (ps.type !== undefined) panel.type(ps.type)
  if (ps.side !== undefined) panel.typeSide(ps.side)
  panelLive(panel, t, ps)
  panel.mark(ps.marks ?? {})
  layout?.()
  panel.seek(t, ps.since ?? t, (a, el) => animStart(a, el, ps))
  // the caret: where the state says, or in the text field the real panel had focused
  let caret = ps.caret
  if (caret === undefined && ps.marks?.focus === 'snap') {
    const el = panel.doc.querySelector('[data-rb-focus]')
    if (el && (el.isContentEditable || el.tagName === 'TEXTAREA')) caret = { el, from: ps.since ?? t }
  }
  panelCaret(panel, caret, t)
}

// ---------------------------------------------------------------------------------------------------------------
// Style A: in VS Code. A VS Code window with the real Claude Code panel in it, drawn at 2x like a Retina screen
// recording: Clawd at his real size in it (96x60 CSS px = 192x120 on screen, 6 px a cell).
// ---------------------------------------------------------------------------------------------------------------

const PROMPT = 'make the playground load faster' // typed into the box in the opener, then the first chat message

const CODE = `function desired(now) {
  if (S.alert) return variant('alert', now, true)
  if (S.busy && S.question && !S.rateLimited) return variant('question', now, true)
  // talking to him (his speech bubble is open)
  if (T.open) {
    if (T.pending) return 'talk-think'
    if (now < T.explainUntil) return 'talk-explain'
    if (now < T.shrugUntil) return 'click-shrug'
    return 'talk-listen'
  }
  if (S.busy) {
    if (S.rateLimited) return 'rate-limit'
    if (S.compacting) return 'compacting'
    if (S.agents.size > 0) return 'subagents'
    return variant(S.activity, now)
  }
  if (S.oneShot && now < S.oneShot.until) return S.oneShot.name
  S.oneShot = null
  if (now < S.typingUntil) return variant('typing', now, true)
  if (now - S.lastActive > SLEEP_AFTER) return variant('sleep', now, true)
  if (now >= S.idleUntil) {
    // next idle animation, never the same one twice in a row
    const pool = IDLE.filter(n => has(n) && n !== S.idleName)
    S.idleName = S.idleUntil === 0 || pool.length === 0 ? 'idle' : pick(pool)
    S.idleUntil = now + cycle(S.idleName)
  }
  return S.idleName
}`

function highlight(line) {
  const re = /(\/\/.*$)|('[^']*')|\b(function|const|let|null|true|false)\b|\b(if|return|else)\b|\b(\d+)\b|\b([A-Z][A-Z_]+)\b|\b([a-zA-Z_]\w*)(?=\()|\b([a-zA-Z_]\w*)\b/g
  const cls = ['m', 's', 'k', 'c', 'n', 'o', 'f', 'v']
  let out = ''
  let last = 0
  for (const m of line.matchAll(re)) {
    out += esc(line.slice(last, m.index))
    const k = m.slice(1).findIndex(Boolean)
    out += `<span class="${cls[k]}">${esc(m[0])}</span>`
    last = m.index + m[0].length
  }
  return out + esc(line.slice(last))
}

// an editor tab's close button (VS Code shows it on the active tab)
const TAB_X = '<i class="x"><svg viewBox="0 0 16 16"><path d="M4.5 4.5l7 7M11.5 4.5l-7 7"/></svg></i>'

const ACT_ICONS = [
  '<path d="M6 3h7l4 4v14H6z M13 3v4h4"/>', // files
  '<circle cx="10" cy="10" r="5.5"/><path d="M14 14l5 5"/>', // search
  '<circle cx="7" cy="6" r="2"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="9" r="2"/><path d="M7 8v8M17 11c0 4-6 3-9 6"/>', // git
  '<path d="M4 4h7v7H4zM13 13h7v7h-7zM4 13h7v7H4zM15 3l5 5-5 5-5-5z"/>', // extensions
  '<path d="M12 3l2.2 6.3L21 12l-6.8 2.7L12 21l-2.2-6.3L3 12l6.8-2.7z"/>', // a spark: the Claude panel
]

/**
 * Look A's camera works like a screen recording that cuts between zooms: the window is drawn at a whole-number
 * zoom z (2 = the whole window, 4, 6), so Clawd is 3z px a cell and the UI stays crisp; between cuts it can sit
 * anywhere over the window (clamped so the frame never shows past its edges). A scene sets zoom, at (a world point,
 * in cells), and either anchor (where that point goes, as fractions of the view) or place (exact view px).
 */
function buildA(root, cut, W, H, wideBox = false) {
  const tall = cut.aspect === '9x16'
  const FL = wideBox || Boolean(cut.footerLayout) // footer close-ups: the panel as wide as its box gets (680 px)
  const pname = FL ? 'stage' : tall ? 'a-tall' : 'a-wide'
  const { width: PW, height: PH } = REAL.panels[pname]
  root.className = `look A ${tall ? 'tall' : 'wide'} ${THEME_CLASS}`
  themeVars(root)
  const editor = !tall && !FL
  const lw = editor ? 44 + 316 + PW : PW // the window's own (logical) size: activity bar + editor + the panel
  const lh = 30 + 35 + PH + 22 // title bar, the panel's editor tab, the panel, status bar
  const VT = tall ? H - 1400 : 0 // the view's top (9:16: under the caption band)
  const VW = W
  const VH = H - VT
  const code = CODE.split('\n').map((l, i) => `<span class="${i === 21 ? 'cur' : ''}"><span class="ln">${82 + i}</span>${highlight(l)}</span>`).join('')
  root.innerHTML = `
    <div class="view" style="top:${VT}px;width:${VW}px;height:${VH}px">
      <div class="vsc" style="width:${lw}px;height:${lh}px">
        <div class="vsc-title"><span class="dots"><i></i><i></i><i></i></span>${editor ? 'custom.js — clawd-companion' : 'clawd-companion'}</div>
        <div class="vsc-body">
          ${editor ? `<div class="vsc-act">${ACT_ICONS.map((p, i) => `<b class="${i === 4 ? 'on' : ''}"><svg viewBox="0 0 24 24">${p}</svg></b>`).join('')}</div>
          <div class="vsc-editor">
            <div class="vsc-tabs"><span class="on"><i class="ic js">JS</i>custom.js${TAB_X}</span><span><i class="ic css">#</i>custom.css${TAB_X}</span></div>
            <div class="vsc-crumbs">custom › <span class="js" style="color:#CBCB41;font:600 9px var(--ui)">JS</span> custom.js › desired</div>
            <pre class="vsc-code">${code}</pre>
          </div>` : ''}
          <div class="vsc-chat">
            <div class="vsc-tabs"><span class="on"><i class="ic">${REAL.tabIcon}</i>Claude Code${TAB_X}</span></div>
            <div class="vsc-panel" style="width:${PW}px;height:${PH}px"></div>
          </div>
        </div>
        <div class="vsc-status"><span>⎇ main</span><span>⊗ 0 ⚠ 0</span><span class="sp"></span><span>Ln 103, Col 5</span><span>Spaces: 2</span><span>UTF-8</span><span>JavaScript</span></div>
      </div>
    </div>
    <div class="capA"></div>`
  const view = root.querySelector('.view')
  const vsc = root.querySelector('.vsc')
  const cap = root.querySelector('.capA')
  // the real Claude Code panel (src/realpanel.js)
  const panel = new RealPanel(root.querySelector('.vsc-panel'), pname, THEME)
  const cursor = document.createElement('div')
  cursor.className = 'cursor off'
  view.append(cursor)
  const wall = buildWall(root, 6, W, H)
  const end = buildEnd(root, 12, W, H, cut.aspect)
  // where the panel and its box are in the window's own px (window at scale 1): he stands on the inside of the
  // box's 1 px top border, his home 10 px from its right end (custom.css)
  vsc.style.transform = 'scale(1)'
  const wr = vsc.getBoundingClientRect()
  const fr = panel.frame.getBoundingClientRect()
  const PX = fr.left - wr.left
  const PY = fr.top - wr.top
  panel.show(FL ? 'mode-auto' : 'idle')
  const boxR = panel.rect(panel.box)
  const bx = Math.round(PX + boxR.r)
  const by = Math.round(PY + boxR.y) + 1
  // the footer's controls (same place in every state), the confirm's Cancel
  const AT = { box: boxR }
  for (const k of ['range', 'uc', 'ctx', 'agents']) {
    const r = panel.rect(AIM[k])
    if (r) AT[k] = r
  }
  if (panel.has('confirm')) {
    panel.show('confirm')
    AT.cancel = panel.rect(AIM.cancel)
  }
  const FOCUS = Object.fromEntries(Object.entries(AT).map(([k, r]) => [k, { x: PX + r.x, y: PY + r.y, w: r.w, h: r.h }]))
  // when Claude got the prompt (his spinner starts): the opener's send; a cut that opens mid-thought started earlier
  const think = cut.scenes.find(s => s.look === 'A' && s.ui === 'thinking')
  const typedFirst = cut.scenes.some(s => s.typing && think && s.t0 < think.t0)
  const spinAt = think ? (typedFirst ? think.t0 : think.t0 - 6.3) : -6.3
  const home = panel.clawdHome() // his image's top left at home, in the panel's px (custom.js world())
  return {
    root,
    panel,
    camera(sc) {
      const z = sc.zoom ?? 2
      const [X, Y] = sc.at ?? [HOME, -4]
      const fo = sc.focus && FOCUS[sc.focus]
      const lx = fo ? fo.x + fo.w / 2 : bx + 3 * X
      const ly = fo ? fo.y + fo.h / 2 : by + 3 * Y
      const [px, py] = sc.place ?? [(sc.anchor ?? [0.5, 0.5])[0] * VW, (sc.anchor ?? [0.5, 0.5])[1] * VH]
      const tx = Math.round(clamp(px - lx * z, VW - lw * z, 0))
      const ty = Math.round(clamp(py - ly * z, VH - lh * z, 0))
      return { z, tx, ty, toScreen: (X2, Y2) => [tx + (bx + 3 * X2) * z, ty + (by + 3 * Y2) * z] }
    },
    render(f) {
      const sc = f.scene
      const { z, tx, ty, toScreen } = this.camera(sc)
      const s = 3 * z
      vsc.style.transform = `translate(${tx}px, ${ty}px) scale(${z})`
      const lt = f.t - sc.t0
      const FS = sc.footer ? sc.footer(lt) : {}
      // the panel; his bubble is the panel's own, placed from his feet (before the caret in it is measured)
      const a = f.actor
      showPanel(panel, FL ? footerState(f, sc, FS) : chatState(f, sc, spinAt), f.t, () => {
        if (a && sc.talk) placeTalk(panel, bx + 3 * a.X - PX, by + 3 * a.Y - PY)
      })
      // Clawd: in the panel's box as the patch mounts him, so the panel's own bubbles and popups draw over him.
      // His image's top left on screen (whole px, as always), back in the panel's px: --cx-x/--cx-y from home.
      if (a && !sc.wall && !sc.end && !NOCLAWD) {
        const [fx, fy] = toScreen(a.X, a.Y)
        const [ax, ay] = ANCHOR[a.clip] ?? FEET
        const L = Math.round(fx - ax * s)
        const T = Math.round(fy - ay * s)
        setClip(panel.clawd((L - tx) / z - PX - home.x, (T - ty) / z - PY - home.y), a.clip, a.ct, a.rate)
      } else if (panel.clawdEl) setClip(panel.clawdEl, null)
      // the cursor: on a footer control (FS.ptr: el, u along the slider, dx/dy), or the cut's own track
      if (FS.ptr) {
        const at = tg => {
          const r = AT[tg.el]
          const x = tg.el === 'range' ? r.x + 6 + (r.w - 12) * (tg.u ?? 0) : r.x + r.w / 2 // thumb radius 6 (custom.js)
          return [tx + (PX + x + (tg.dx ?? 0)) * z, ty + (PY + r.y + r.h / 2 + (tg.dy ?? 0)) * z]
        }
        const [ax, ay] = at(FS.ptr.a)
        const [bx2, by2] = FS.ptr.b ? at(FS.ptr.b) : [ax, ay]
        const u = FS.ptr.k ?? 0
        drawCursor(cursor, FS.ptr.kind ?? 'arrow', ax + (bx2 - ax) * u, ay + (by2 - ay) * u, z)
      } else renderCursor(cursor, f.cut.cursor, f, toScreen, z)
      // caption: 9:16 in the band above the view; 16:9 a card over the editor (2x) or top left (closer shots)
      const c = captionAt(f.cut, f.t)
      cap.classList.toggle('off', !c || Boolean(sc.end) || Boolean(sc.wall))
      if (c) cap.innerHTML = `${esc(c.text)}${c.sub ? `<small>${esc(c.sub)}</small>` : ''}`
      if (!tall) {
        // 2x: on the editor's code, under its breadcrumbs, clear of the current line and the panel's edge
        const pos = sc.capPos ?? (z === 2 ? [110, 196] : 'tl')
        cap.style.cssText = Array.isArray(pos) ? `left:${pos[0]}px;top:${pos[1]}px` : pos === 'bl' ? 'left:104px;bottom:92px' : pos === 'tr' ? 'right:64px;top:64px' : 'left:64px;top:64px'
      }
      renderWall(wall, f, sc.wall)
      renderEnd(end, f, sc.end)
    },
  }
}

// ---------------------------------------------------------------------------------------------------------------
// Styles B and C: the real panel blown up 6x (3 CSS px a cell, 18 screen px), its box's right end at X = 0 and
// the inside of its top border at Y = 0; the chat column's bottom (the floor) and right side (the wall) are the
// panel's own edges. A camera that never zooms follows Clawd. B: plain, the captions above. C: on Clawd's own
// pixel grid, with notes like a sprite sheet.
// ---------------------------------------------------------------------------------------------------------------

function buildStage(stage, cut, W, H, style) {
  const tall = cut.aspect === '9x16'
  stage.className = `look ${style} ${tall ? 'tall' : 'wide'} ${THEME_CLASS}`
  themeVars(stage)
  const s = 18
  const k = s / 3 // the real panel's CSS px, blown up
  stage.innerHTML = `${style === 'C' ? '<div class="grid"></div>' : ''}
    <div class="w-floor"></div><div class="w-wall"></div>
    ${style === 'C' ? '<div class="capC"></div><div class="note"></div><div class="lead"></div><div class="corner"></div>' : '<div class="topText off"></div>'}
    <div class="flash"></div>`
  const $ = sel => stage.querySelector(sel)
  const grid = $('.grid')
  const floor = $('.w-floor')
  const wallEl = $('.w-wall')
  const cap = $('.capC')
  const note = $('.note')
  const lead = $('.lead')
  const corner = $('.corner')
  const topText = $('.topText')
  const flash = $('.flash')
  // the real panel, under the floor and wall edges, Clawd, the captions
  const panel = new RealPanel(stage, 'stage', THEME, floor)
  panel.show('mode-default')
  const g = panel.rect(panel.box)
  const home = panel.clawdHome() // his image's top left at home, in the panel's px (custom.js world())
  const cursor = document.createElement('div')
  cursor.className = 'cursor off'
  stage.append(cursor)
  const wall = buildWall(stage, s, W, H)
  const end = buildEnd(stage, s, W, H, cut.aspect)
  const root = stage
  const light = THEME !== 'dark'
  return {
    root,
    s,
    panel,
    render(f) {
      const sc = f.scene
      const cam = typeof sc.cam === 'string' ? CAMS[sc.cam] : sc.cam ?? CAMS.home
      // where the camera's world point goes on screen (C leaves the top left to its big captions)
      const anchor = (tall ? sc.anchorTall : sc.anchorWide) ?? (tall ? [0.5, 0.56] : style === 'C' ? [0.63, 0.54] : [0.56, 0.52])
      // a short shake on the drops (B), whole pixels only
      let sx = 0
      let sy = 0
      if (style === 'B') {
        for (const ft of f.cut.flashes) {
          const d = f.t - ft
          if (d >= 0 && d < 0.25) {
            const a = (1 - d / 0.25) * 10
            sx += Math.round(Math.sin(d * 97) * a)
            sy += Math.round(Math.cos(d * 83) * a)
          }
        }
      }
      const ox = Math.round(W * anchor[0] - cam[0] * s) + sx
      const oy = Math.round(H * anchor[1] - cam[1] * s) + sy
      const toScreen = (X, Y) => [ox + X * s, oy + Y * s]
      if (grid) {
        grid.style.backgroundSize = `${8 * s}px ${8 * s}px, ${8 * s}px ${8 * s}px, ${s}px ${s}px, ${s}px ${s}px`
        const gx = ((ox % s) + s) % s
        const gy = ((oy % s) + s) % s
        const Gx = ((ox % (8 * s)) + 8 * s) % (8 * s)
        const Gy = ((oy % (8 * s)) + 8 * s) % (8 * s)
        grid.style.backgroundPosition = `${Gx}px ${Gy - 1}px, ${Gx - 1}px ${Gy}px, ${gx}px ${gy}px, ${gx}px ${gy}px`
      }
      // the panel: its box's right end on X = 0, the inside of the box's top border on Y = 0
      const PL = Math.round(ox - g.r * k)
      const PT = Math.round(oy - (g.y + 1) * k)
      panel.frame.style.transform = `translate(${PL}px, ${PT}px) scale(${k})`
      const a = f.actor
      // Claude is on it while Clawd shows it (the states scene); otherwise idle, in the scene's mode
      const busy = sc.id === 'states' && BUSY.test(a?.clip ?? '')
      showPanel(panel, busy ? { state: 'thinking', since: sc.t0, spinAt: sc.t0 } : { state: `mode-${MODE_STATE[sc.mode ?? 'manual']}`, since: sc.t0 }, f.t)
      floor.style.transform = `translate(0, ${oy + WORLD.F * s}px)`
      wallEl.style.transform = `translate(${ox + WORLD.RW * s}px, 0)`
      const c = captionAt(f.cut, f.t)
      if (style === 'B') {
        // the caption types itself above the panel's box, never in it; the caret blinks on the beat
        topText.classList.toggle('off', !c || Boolean(sc.end) || Boolean(sc.wall))
        if (c && !sc.end && !sc.wall) {
          const n = Math.max(0, Math.floor((f.t - c.t0) * 45) + 1)
          const blink = n >= c.text.length && Math.floor((f.t - c.t0) / MUSIC.beat) % 2 === 1
          topText.innerHTML = `${esc(c.text.slice(0, n))}<span class="caret" style="opacity:${blink ? 0 : 1}"></span>${c.sub ? `<small>${esc(c.sub)}</small>` : ''}`
          topText.style.transform = `translate(${tall ? 72 : 96}px, ${tall ? 150 : 88}px)`
        }
      } else {
        cap.classList.toggle('off', !c || Boolean(sc.end) || Boolean(sc.wall))
        if (c) {
          cap.innerHTML = `${esc(c.text)}${c.sub ? `<small>${esc(c.sub)}</small>` : ''}`
          cap.style.transform = `translate(${tall ? 72 : 96}px, ${tall ? 150 : 88}px)`

        }
      }
      // Clawd: in the panel's box as the patch mounts him (its popups draw over him); his image's top left on
      // screen in whole px, back in the panel's px as --cx-x/--cx-y from his home spot
      if (a && !sc.wall && !sc.end) {
        const [fx, fy] = toScreen(a.X, a.Y)
        const [ax, ay] = ANCHOR[a.clip] ?? FEET
        const L = Math.round(fx - ax * s)
        const T = Math.round(fy - ay * s)
        if (!NOCLAWD) setClip(panel.clawd((L - PL) / k - home.x, (T - PT) / k - home.y), a.clip, a.ct, a.rate)
        if (note) {
          // C: his 32x20 canvas outlined like a sprite sheet frame, labelled with the clip
          note.classList.remove('off')
          lead.classList.remove('off')
          lead.style.transform = `translate(${L}px, ${T}px)`
          lead.style.width = `${32 * s}px`
          lead.style.height = `${20 * s}px`
          note.innerHTML = `<b>${esc(a.clip)}</b>  ${esc(clipInfo(a.clip))}`
          const nw = note.offsetWidth || 600
          note.style.transform = `translate(${Math.max(24, Math.min(W - 24 - nw, L))}px, ${T - 46}px)`
        }
      } else {
        if (panel.clawdEl) setClip(panel.clawdEl, null)
        note?.classList.add('off')
        lead?.classList.add('off')
      }
      if (corner) {
        corner.textContent = `clawd-companion  ·  ${(f.t).toFixed(2)} s  ·  bar ${barLabel(f.cut, f.t)}`
        corner.style.transform = `translate(${W - 72 - 760}px, ${tall ? 64 : 40}px)`
        corner.style.width = '760px'
        corner.style.textAlign = 'right'
      }
      renderCursor(cursor, f.cut.cursor, f, toScreen, 4)
      // flash on the drops (B only): two frames, fading; on white a short dark blink
      let fl = 0
      if (style === 'B') for (const ft of f.cut.flashes) if (f.t >= ft && f.t < ft + 0.12) fl = Math.max(fl, 0.55 * (1 - (f.t - ft) / 0.12))
      flash.style.opacity = light ? fl * 0.4 : fl
      flash.style.background = light ? '#000000' : '#FFFFFF'
      renderWall(wall, f, sc.wall)
      renderEnd(end, f, sc.end)
    },
  }
}

function barLabel(cut, t) {
  const b = (t - cut.bar(0)) / MUSIC.bar
  const k = Math.floor(b)
  const beat = Math.floor((b - k) * 4) + 1
  return `${k}.${beat}`
}

const STATE_OF = {
  idle: 'idle', typing: 'you are typing', thinking: 'Claude is thinking', working: 'Claude is working', alert: 'needs your permission',
  question: 'asked you a question', done: 'turn finished', sleep: 'idle for 5 minutes', compacting: 'compacting', hooks: 'running hooks',
  subagents: 'subagents running', error: 'turn failed', rate: 'rate limited', manual: 'mode: manual', plan: 'mode: plan', edits: 'mode: accept edits',
  auto: 'mode: auto', bypass: 'mode: bypass', hello: 'panel opened', vibe: 'just for fun', walk: 'moving', climb: 'climbing the box',
  hop: 'hopping off', fall: 'falling', land: 'landing', teeter: 'at the edge', look: 'at the bottom', grabbed: 'dragged', tumble: 'thrown',
  crash: 'hard landing', parachute: 'dropped from high up', chute: 'chute clicked', notice: 'cursor on him', pet: 'petted', talk: 'speech bubble (/btw)',
  click: 'clicked', in: 'set-up', out: 'pack-away', sit: 'idle', done_party: 'long turn finished',
}

function clipInfo(clip) {
  const base = clip.split('-')[0]
  const st = clip === 'done-party' ? STATE_OF.done_party : STATE_OF[base] ?? ''
  const c = CLIPS[clip]
  const loop = c.once || ONCE.test(clip) ? `once, ${(c.ms / 1000).toFixed(2)} s` : `loop ${(c.ms / 1000).toFixed(2)} s`
  return `${st}  ·  ${loop}`
}

// ---------------------------------------------------------------------------------------------------------------
// The frame at t, seek(t), boot
// ---------------------------------------------------------------------------------------------------------------

let SHOW = null

function frameAt(t) {
  const cut = SHOW.cut
  const scene = lastAt(cut.scenes, t) ?? cut.scenes[0]
  return { t, cut, scene, actor: trackAt(cut.track, t) }
}

/** Shows the frame at video time t (seconds). Deterministic: no animation runs on its own. */
function seek(t) {
  const f = frameAt(t)
  SHOW.style.render(f)
  SHOW.t = t
  return f.scene.id
}

function boot() {
  const Q = new URLSearchParams(location.search)
  const cut = CUTS[Q.get('cut') ?? 'wide']
  const style = (Q.get('style') ?? 'B').toUpperCase()
  if (!cut) throw new Error(`unknown cut "${Q.get('cut')}" (cuts: ${Object.keys(CUTS).join(', ')})`)
  if (!['A', 'B', 'C', 'MIX'].includes(style)) throw new Error(`unknown style "${style}" (A, B, C or mix)`)
  const [W, H] = cut.aspect === '9x16' ? [1080, 1920] : [1920, 1080]
  const stage = document.getElementById('stage')
  stage.style.width = `${W}px`
  stage.style.height = `${H}px`
  const capture = Q.has('capture')
  document.body.classList.toggle('capture', capture)
  // checks (tools/realbox/check-scale.mjs): the panel alone, no Clawd or cursor over it
  document.body.classList.toggle('noclawd', Q.has('noclawd'))
  if (!capture) {
    const fit = () => {
      const k = Math.min(innerWidth / W, innerHeight / H)
      stage.style.transform = `translate(${(innerWidth - W * k) / 2}px, ${(innerHeight - H * k) / 2}px) scale(${k})`
    }
    addEventListener('resize', fit)
    fit()
  }
  SHOW = { cut, styleId: style, W, H, t: 0, fps: 30, duration: cut.end, fade: cut.fade ?? 1.5 }
  const layer = () => stage.appendChild(document.createElement('div'))
  const looks = {}
  if (style === 'MIX' || style === 'A') looks.A = buildA(layer(), cut, W, H)
  if (style === 'MIX') looks.A2 = buildA(layer(), cut, W, H, true) // the same panel, wider: the footer's full set
  if (style === 'MIX' || style === 'B') looks.B = buildStage(layer(), cut, W, H, 'B')
  if (style === 'C') looks.C = buildStage(layer(), cut, W, H, 'C')
  SHOW.looks = looks
  SHOW.style = {
    render(f) {
      const id = style === 'MIX' ? f.scene.look ?? 'B' : style
      for (const [k, L] of Object.entries(looks)) L.root.style.visibility = k === id ? '' : 'hidden'
      looks[id].render(f)
    },
  }
  window.SHOW = SHOW
  window.seek = seek
  seek(+(Q.get('t') ?? 0))
  if (!capture) preview(Q)
  window.__ready = true
}

function preview(Q) {
  const hud = document.getElementById('hud')
  const audio = Q.get('audio') ? Object.assign(new Audio(Q.get('audio')), { preload: 'auto' }) : null
  let playing = false
  let useAudio = false // the music is the clock once it really plays (a key press may be needed: autoplay rules)
  let t0 = 0
  let w0 = 0
  const show = () => {
    const f = frameAt(SHOW.t)
    hud.textContent = `${SHOW.cut.id} ${SHOW.styleId}  t ${SHOW.t.toFixed(2)} / ${SHOW.duration.toFixed(1)}  bar ${barLabel(SHOW.cut, SHOW.t)}  ${f.scene.id}  ${f.actor?.clip ?? ''}\nspace play  ←/→ beat  ⇧←/→ bar  [/] frame${audio && !useAudio && playing ? '  (no sound yet: press space twice)' : ''}`
  }
  let lastA = -1
  let lastAWall = 0
  const loop = () => {
    if (!playing) return
    const now = performance.now()
    // the music is the clock while its time is really moving; otherwise (blocked, still loading, no sound
    // device) the wall clock
    if (useAudio && audio.currentTime !== lastA) {
      lastA = audio.currentTime
      lastAWall = now
    }
    const fromAudio = useAudio && !audio.paused && now - lastAWall < 300
    const t = fromAudio ? lastA + (now - lastAWall) / 1000 : t0 + (now - w0) / 1000
    if (!fromAudio && useAudio) {
      t0 = t
      w0 = now
    }
    seek(Math.min(t, SHOW.duration))
    show()
    if (t >= SHOW.duration) {
      playing = false
      audio?.pause()
    } else requestAnimationFrame(loop)
  }
  const go = t => {
    seek(Math.max(0, Math.min(SHOW.duration, t)))
    show()
  }
  addEventListener('keydown', ev => {
    if (ev.key === ' ') {
      ev.preventDefault()
      playing = !playing
      if (playing) {
        t0 = SHOW.t
        w0 = performance.now()
        useAudio = false
        if (audio) {
          audio.currentTime = SHOW.t
          audio.play().then(() => (useAudio = true), () => (useAudio = false))
        }
        loop()
      } else audio?.pause()
    } else if (ev.key === 'ArrowRight') go(SHOW.t + (ev.shiftKey ? MUSIC.bar : MUSIC.beat))
    else if (ev.key === 'ArrowLeft') go(SHOW.t - (ev.shiftKey ? MUSIC.bar : MUSIC.beat))
    else if (ev.key === ']') go(SHOW.t + 1 / 30)
    else if (ev.key === '[') go(SHOW.t - 1 / 30)
  })
  show()
  if (Q.has('play')) dispatchEvent(new KeyboardEvent('keydown', { key: ' ' }))
}
