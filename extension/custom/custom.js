// Runs inside the Claude Code chat panel (a webview), after the extension's
// own script. Only the DOM is here, no VS Code API.
//
// Clawd stands on the top border of the chat input box and plays the
// animation that fits what's going on (docs/how-it-works.md):
//
//   panel opened ................ hello (or a hello-* version), then idle
//   idle ........................ idle, rotating idle-* variants each cycle
//   idle for 5 minutes .......... sleep (or a sleep-* version)
//   you type while idle ......... typing (or a typing-* version)
//   you switch permission mode .. that mode's animation for one cycle
//   Claude thinking ............. thinking, rotating thinking-* versions
//   Claude running tools/writing  working, rotating working-* versions
//   subagents running ........... subagents
//   compacting .................. compacting
//   asks you a question ......... question (or a question-* version)
//   needs your permission ....... alert (or an alert-* version)
//   rate limited ................ rate-limit
//   turn finished ............... done or a done-* version (done-party after a
//                                 2-minute turn), held until you look at the panel
//   turn failed ................. error
//
// He also moves and can be played with (the "Moving him" section). His world
// is the whole chat column, not just the input box:
//
//   between two animations ...... he walks a few steps first (no hard cut)
//   idle for a while ............ he wanders on the box; near its end he may
//                                 teeter, sit on the edge, or hop off
//   at the bottom of the panel .. he looks up, walks to the box and climbs its side
//   click him ................... his speech bubble opens: the extension's /btw side
//                                 question (talk-listen, talk-think, talk-explain)
//   click him while it's open ... a random click-* reaction (3 quick clicks: dizzy)
//   cursor onto him ............. notice; back and forth over him: pet
//   drag him .................... grabbed (dangling); held still: grabbed-bored;
//                                 shaken: grabbed-dizzy
//   flick and let go ............ thrown: tumble, bounce off the walls, crash
//   let go high up .............. fall, then the parachute opens; land-chute
//   click him under the chute ... chute-pop, he falls
//   let go low .................. land
//
// The SVGs come from ../animations/svg and svg-tx; the build copies them to
// webview/clawd/ and puts `globalThis.CLAWD_CYCLES = {name: ms}` (each
// animation's full cycle) in front of this file.
//
// Further down: the footer's context, usage and agents controls.

const CLAWD_DIR = new URL('./clawd/', import.meta.url)
const CYCLES = globalThis.CLAWD_CYCLES ?? {}
const has = name => name in CYCLES
const cycle = name => CYCLES[name] ?? 6000
const pick = list => list[Math.floor(Math.random() * list.length)]

const IDLE = ['idle', 'idle-moods', 'idle-pet', 'idle-bubbles', 'idle-kite', 'idle-garden', 'idle-game', 'idle-bird']
const MODE = {
  default: ['manual', 'manual-drive', 'manual-craft'],
  plan: ['plan'],
  acceptEdits: ['edits'],
  auto: ['auto', 'auto-robot', 'auto-cloud'],
  bypassPermissions: ['bypass'],
}
const SLEEP_AFTER = 5 * 60_000
const TYPING_HOLD = 2_000
const MIN_SHOW = 1_200 // a busy-state animation stays at least this long
const BUSY_HOLD = 4_000 // ... and a thinking/working scene this long before the other one
const isBusyScene = name => ['thinking', 'working', 'subagents', 'compacting'].includes(name.split('-')[0])

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

const S = {
  busy: false,
  activity: 'thinking', // thinking | working, while busy
  agents: new Set(), // in-flight Task/Agent tool_use ids
  question: '', // tool_use id of an open AskUserQuestion
  alert: false, // a permission prompt is waiting
  compacting: false,
  rateLimited: false,
  turnStart: 0,
  oneShot: null, // { name, until } : hello, done, done-party, error, a mode animation
  typingUntil: 0,
  lastActive: Date.now(),
  idleName: 'idle',
  idleUntil: 0,
  mode: '',
}

function desired(now) {
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
}

// Versions of a state: the state itself plus every installed `<state>-*`
// animation (done-party is its own state).
const POOLS = {}
const PICKS = {}

function poolOf(base) {
  return (POOLS[base] ??= [base, ...Object.keys(CYCLES).filter(n => n.startsWith(`${base}-`) && n !== 'done-party')].filter(has))
}

/**
 * Which version of `base` to show. thinking/working keep one pick until it has played a full cycle, so the
 * thinking <-> working flips in a turn come back to the same scenes; the others (`perShow`) keep their pick
 * while it's on screen and choose again the next time. Never the same one twice in a row; the first pick in
 * a session is the original.
 */
function variant(base, now, perShow = false) {
  const pool = poolOf(base)
  if (pool.length < 2) return base
  const slot = (PICKS[base] ??= { name: base, until: 0, n: 0 })
  const shown = V.shown.replace(/^in-/, '') // its set-up counts as showing it
  if (perShow ? !pool.includes(shown) : now >= slot.until) {
    slot.name = slot.n === 0 ? base : pick(pool.filter(n => n !== slot.name))
    slot.until = now + cycle(slot.name)
    slot.n++
  }
  return slot.name
}

// ---------------------------------------------------------------------------
// Showing it
// ---------------------------------------------------------------------------

const V = { shown: '', shownAt: 0, timer: 0, plays: 0, noQuery: false }

function srcFor(name) {
  const url = new URL(`clawd-${name}.svg`, CLAWD_DIR).href
  // A fresh query restarts the animation from its first frame.
  return V.noQuery ? url : `${url}?p=${++V.plays}`
}

/** Shows animation `name` (from its first frame); `again` restarts it even if it is already showing. */
function show(name, again = false) {
  if (name === V.shown && !again) return
  V.shown = name
  V.shownAt = Date.now()
  for (const img of document.querySelectorAll('img.cx-clawd')) img.src = srcFor(name)
  place() // some clips are drawn somewhere else in the image (ANCHOR)
}

function update() {
  clearTimeout(V.timer)
  const now = Date.now()
  let name = desired(now)
  if (!has(name)) name = 'idle'
  // A walk, a climb, a reaction, a drag or a flight owns him until it ends. Something urgent cuts short his
  // breather at the bottom of the panel; anything but idle gets him up from sitting on the edge.
  if (M.act) {
    const k = M.act.kind
    if ((k === 'wait' || k === 'look') && isUrgent(name)) stopAct()
    else if (k === 'sit' && !isIdle(name)) return standUp()
    else return show(M.act.name)
  }
  // At the bottom of the panel he climbs home first, unless it's urgent or you're talking to him.
  if (M.on === 'floor' && !isUrgent(name) && !T.open) return goHome()

  if (name !== V.shown) {
    // While busy, a scene stays up a moment before the next one; thinking <-> working flips (each with its
    // pack-away and set-up) wait longer, so a quick run of tool calls doesn't become a blur of transitions.
    const hold = isBusyScene(V.shown) && isBusyScene(name) ? BUSY_HOLD : MIN_SHOW
    if (S.busy && isState(V.shown) && now - V.shownAt < hold && !isUrgent(name)) {
      V.timer = setTimeout(update, hold - (now - V.shownAt))
      return
    }
    if (switchScene(V.shown, name, now)) return
    show(name)
  }
  if (!S.busy) planWander(now)

  // Wake up for the next thing that changes on its own.
  const next = [
    S.oneShot?.until,
    S.typingUntil > now ? S.typingUntil : 0,
    !S.busy ? S.idleUntil : 0,
    !S.busy ? S.lastActive + SLEEP_AFTER + 1 : 0,
    S.busy ? PICKS[S.activity]?.until : 0, // the next thinking/working version
    T.open ? T.explainUntil : 0,
    T.open ? T.shrugUntil : 0,
  ].filter(t => t && t > now && t !== Infinity)
  if (next.length > 0) V.timer = setTimeout(update, Math.min(...next) - now + 5)
}

function activity() {
  S.lastActive = Date.now()
}

function oneShot(name, until = Date.now() + cycle(name)) {
  if (!has(name)) return
  S.oneShot = { name, until }
}

// ---------------------------------------------------------------------------
// Reading what Claude does from the messages the extension posts here
// ---------------------------------------------------------------------------

function onSdkMessage(m) {
  if (!m || typeof m !== 'object') return
  activity()
  S.alert = false // any new message means a pending prompt was answered
  const sub = Boolean(m.parent_tool_use_id)

  if (m.type === 'system') {
    if (m.subtype === 'init') {
      S.busy = true
      S.activity = 'thinking'
      S.turnStart = Date.now()
      S.oneShot = null
      S.typingUntil = 0
    } else if (m.subtype === 'status') {
      S.compacting = m.status === 'compacting'
    } else if (m.subtype === 'compact_boundary') {
      S.compacting = false
    }
  } else if (m.type === 'rate_limit_event') {
    S.rateLimited = m.rate_limit_info?.status === 'rejected'
  } else if (m.type === 'stream_event' && !sub) {
    const b = m.event?.type === 'content_block_start' ? m.event.content_block : undefined
    if (b?.type === 'thinking') S.activity = 'thinking'
    else if (b?.type === 'text' || b?.type === 'tool_use') S.activity = 'working'
  } else if (m.type === 'assistant' && Array.isArray(m.message?.content)) {
    if (m.error === 'rate_limit') S.rateLimited = true
    if (!sub) {
      for (const b of m.message.content) {
        if (b?.type !== 'tool_use') continue
        S.activity = 'working'
        if (b.name === 'Task' || b.name === 'Agent') S.agents.add(b.id)
        if (b.name === 'AskUserQuestion') S.question = b.id
      }
    }
  } else if (m.type === 'user' && Array.isArray(m.message?.content)) {
    if (!sub) {
      for (const c of m.message.content) {
        if (c?.type !== 'tool_result') continue
        S.agents.delete(c.tool_use_id)
        if (c.tool_use_id === S.question) S.question = ''
      }
      S.activity = 'thinking'
      S.rateLimited = false
    }
  } else if (m.type === 'result') {
    const secs = (m.duration_ms ?? Date.now() - S.turnStart) / 1000
    S.busy = false
    S.agents.clear()
    S.question = ''
    S.compacting = false
    S.rateLimited = false
    if (m.is_error && m.subtype !== 'error_during_execution') {
      oneShot('error')
    } else if (!m.is_error) {
      // "Finished, unseen": hold it until the panel has focus.
      const name = secs >= 120 ? 'done-party' : variant('done', Date.now(), true)
      oneShot(name, document.hasFocus() ? Date.now() + cycle(name) : Infinity)
    }
    // an Esc interrupt just goes back to idle
  }
  update()
}

window.addEventListener('message', ev => {
  const d = ev.data
  if (d?.type !== 'from-extension') return
  const msg = d.message
  try {
    if (msg?.type === 'io_message') onSdkMessage(msg.message)
    else if (msg?.type === 'request' && msg.request?.type === 'tool_permission_request') {
      activity()
      S.alert = true
      update()
    }
  } catch (err) {
    console.warn('[custom] clawd', err)
  }
})

// You looked at the panel: a held "done" plays out, then he goes idle.
window.addEventListener('focus', () => {
  if (S.oneShot?.until === Infinity) S.oneShot.until = Date.now() + Math.min(cycle(S.oneShot.name), 4000)
  activity()
  update()
})

// Typing in the input box while Claude is idle.
document.addEventListener(
  'input',
  ev => {
    if (T.issuing) return // that's openTalk() typing /btw, not you
    if (!(ev.target instanceof Element) || !ev.target.matches('[class*="messageInput_"]')) return
    activity()
    if (S.busy) return
    S.oneShot = null
    S.typingUntil = Date.now() + TYPING_HOLD
    update()
  },
  true,
)

// ---------------------------------------------------------------------------
// Moving him. His world is the whole chat column: he stands on the top of the
// input box (home) or on the bottom of the panel, and the column's sides and
// the box's own sides are walls. Thrown, or hopping off the end of the box
// where there's room beside it, he falls to the bottom of the panel and climbs
// back up the box's side (look-up, walk over, walk up the wall like a crab, a quarter turn over the top).
//
// Where he is = his feet's centre: on the box, M.u px left of the box's right
// end (so he rides the box when it grows); otherwise M.fx / M.fy in viewport
// px. The <img> and its hit area stay inside the input box (so the
// extension's popups still draw over him); custom.css moves them by --cx-x /
// --cx-y from his home spot (10px from the box's right end, on its top
// border). While M.act is set (a walk, a climb, a hop, a reaction, a drag, a
// flight, a landing...) it decides what he shows; when it ends, update() goes
// back to what Claude is doing.
// ---------------------------------------------------------------------------

const CELL = 3 // CSS px per pixel-art cell at 96x60
const IMG = { w: 96, h: 60 }
const FEET = [15.5 * CELL, 20 * CELL] // his feet's centre in the image: his 11x8 box is cells 10-20 x 12-19
const BODY_HALF = 5.5 * CELL
const BODY_H = 8 * CELL
const WALK_CPS = 4 // cells per second: the stride the walk SVGs are drawn for
const CLIMB_CPS = 6 // the climb-left/right SVGs are drawn for this
const HOP = { air: 150, land: 550 } // hop-left/right: takes off at 150 ms, touches down at 550 ms
const WALK_GAP = 8_000 // at most one walk between animations per 8 s
const WANDER = [25_000, 50_000] // idle: wander somewhere new every 25-50 s
const EDGE_IN = 2.5 * CELL // the edge spot (teeter, sit-edge): his feet's centre this far in from the box's end
const MIN_GAP = 14 * CELL // a gap beside the box narrower than this is closed: he can't fall down it
const NEAR_EDGE = 40 * CELL // he only wanders to an end of the box from this close
const CLICK_SET = ['click-hop', 'click-wave', 'click-hug', 'click-hide', 'click-party', 'click-spin',
  'click-giggle', 'click-shrug', 'click-idea', 'click-poof', 'click-groove']
const URGENT = new Set(['alert', 'question', 'typing']) // never wait for a walk or the climb home
const STATES = new Set(['idle', 'typing', 'thinking', 'working', 'alert', 'question', 'done', 'sleep', 'compacting',
  'hooks', 'manual', 'plan', 'edits', 'auto', 'bypass', 'subagents', 'error', 'rate', 'vibe', 'hello'])
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)')
const G = 160 * CELL // gravity, px/s^2
const CHUTE_FALL = 9 * CELL // parachute descent, px/s
// Clips not drawn standing at home: where his feet's centre is in the image.
const ANCHOR = {
  'sit-edge-left': [15.5 * CELL, 17 * CELL], // he sits on the box's corner, at cells (13, 17)
  'sit-edge-right': [15.5 * CELL, 17 * CELL], // corner at (18, 17)
}

const baseOf = name => name.split('-')[0]
const isState = name => STATES.has(baseOf(name))
const isUrgent = name => URGENT.has(baseOf(name))
const isIdle = name => baseOf(name) === 'idle'
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v))
const later = ms => new Promise(resolve => setTimeout(resolve, ms))

const M = {
  on: 'box', // what he stands on: 'box', 'floor' (the bottom of the panel), or null (in the air, on a wall)
  u: -1, // on the box: his feet's centre, px left of the box's right end (-1: not placed yet = home)
  fx: 0, // his feet's centre in viewport px (place() keeps them current)
  fy: 0,
  act: null,
  raf: 0,
  timer: 0,
  lastWalk: 0,
  wanderAt: 0,
  wanderTimer: 0,
  clicks: [],
  lastClick: '',
  noticeAt: 0,
  petAt: 0,
  pet: { dir: 0, run: 0, flips: [] },
}

function boxOf() {
  return document.querySelector('img.cx-clawd')?.parentElement ?? null
}

let borders = null

/** His world in viewport px: the chat column's sides, top and bottom, and the input box. */
function world() {
  const box = boxOf()
  if (!box) return null
  const b = box.getBoundingClientRect()
  if (!borders) {
    const cs = getComputedStyle(box)
    borders = { t: parseFloat(cs.borderTopWidth) || 0, r: parseFloat(cs.borderRightWidth) || 0, l: parseFloat(cs.borderLeftWidth) || 0 }
  }
  const c = box.closest('[class*="chatContainer_"]')?.getBoundingClientRect()
  const left = c?.left ?? 0
  const right = c?.right ?? innerWidth
  return {
    b,
    left,
    right,
    ceil: c?.top ?? 0,
    floor: c?.bottom ?? innerHeight,
    top: b.top + borders.t, // he stands on the inside of the box's top border
    homeX: b.right - borders.r - 10 - IMG.w, // the image's top-left at home (custom.css)
    homeY: b.top + borders.t - IMG.h,
    gapL: b.left - left >= MIN_GAP,
    gapR: right - b.right >= MIN_GAP,
  }
}

/** On the box: home and the far end of where he wanders (u), so his whole image stays over the box. */
function range(w) {
  const home = borders.r + 10 + IMG.w - FEET[0]
  return { home, far: Math.max(home, w.b.width - borders.l - 10 - FEET[0]) }
}

/** The stretch of the panel's bottom beside the box that x is in: [from, to] for his feet. */
function floorSpan(w, x = M.fx) {
  return x < w.b.left ? [w.left + BODY_HALF, w.b.left - BODY_HALF] : [w.b.right + BODY_HALF, w.right - BODY_HALF]
}

/** Over the box's top, where he'd land on it (a gap too narrow to fall down counts as box). */
function overBox(w, x) {
  return x >= (w.gapL ? w.b.left : w.left) && x <= (w.gapR ? w.b.right : w.right)
}

function place() {
  const w = world()
  if (!w) return
  if (M.on === 'box') {
    if (M.u < 0) M.u = range(w).home
    M.u = clamp(M.u, EDGE_IN, w.b.width - EDGE_IN)
    M.fx = w.b.right - M.u
    M.fy = w.top
  } else if (M.on === 'floor') {
    const left = M.fx < w.b.left
    if (!(left ? w.gapL : w.gapR)) {
      // the panel got narrower and closed his gap: back up on the box
      M.on = 'box'
      M.u = left ? range(w).far : range(w).home
      return place()
    }
    const [lo, hi] = floorSpan(w)
    M.fx = clamp(M.fx, lo, hi)
    M.fy = w.floor
  }
  const [ax, ay] = ANCHOR[V.shown] ?? FEET
  const x = `${Math.round(M.fx - ax - w.homeX)}px`
  const y = `${Math.round(M.fy - ay - w.homeY)}px`
  for (const el of document.querySelectorAll('.cx-clawd, .cx-clawd-hit')) {
    el.style.setProperty('--cx-x', x)
    el.style.setProperty('--cx-y', y)
  }
  placeTalk(w)
}

/** Ends whatever M.act is doing (its timer and its frame loop). */
function stopAct() {
  cancelAnimationFrame(M.raf)
  clearTimeout(M.timer)
  M.raf = 0
  M.act = null
}

/** Plays one-shot `name` as M.act, then `then` (default: back to update()). */
function playOnce(kind, name, then = update) {
  stopAct()
  if (!has(name)) return void then()
  const a = { kind, name }
  M.act = a
  show(name, true)
  M.timer = setTimeout(() => {
    if (M.act !== a) return
    M.act = null
    then()
  }, cycle(name))
}

/**
 * Walks along what he stands on, at the walk SVGs' own speed, to `to` (on the box: u; on the floor: viewport x),
 * then calls `then`. False (and no `then`) when he's already there.
 */
function walkTo(to, then = update) {
  const w = world()
  const onBox = M.on === 'box'
  if (!w || (!onBox && M.on !== 'floor')) return false
  const [lo, hi] = onBox ? [EDGE_IN, w.b.width - EDGE_IN] : floorSpan(w)
  const from = onBox ? M.u : M.fx
  to = clamp(to, lo, hi)
  if (Math.abs(to - from) < CELL) return false
  stopAct()
  const leftward = onBox ? to > from : to < from
  const a = { kind: 'walk', name: leftward ? 'walk-left' : 'walk-right' }
  M.act = a
  M.lastWalk = Date.now()
  show(a.name, true)
  const speed = (WALK_CPS * CELL) / 1000
  const t0 = performance.now()
  const step = now => {
    if (M.act !== a) return
    const d = Math.min(Math.abs(to - from), speed * (now - t0))
    const v = from + Math.sign(to - from) * d
    if (onBox) M.u = v
    else M.fx = v
    place()
    if (d >= Math.abs(to - from)) {
      M.raf = 0
      M.act = null
      then()
      return
    }
    M.raf = requestAnimationFrame(step)
  }
  M.raf = requestAnimationFrame(step)
  return true
}

/** Back into the stretch he wanders on the box (after landing near an end, getting up, climbing up). */
function settle() {
  const w = world()
  if (!w || M.on !== 'box') return update()
  const { home, far } = range(w)
  if (!walkTo(clamp(M.u, home, far))) update()
}

/** A few cells somewhere else on the box: back toward home when far from it, else either way. */
function nextSpot(cells) {
  const { home, far } = range(world())
  const d = cells * CELL
  if (M.u > home + (far - home) * 0.6) return M.u - d
  if (M.u < home + d) return M.u + d
  return M.u + (Math.random() < 0.5 ? -d : d)
}

/** Instead of a hard cut from `from` to `to`: walk 5-9 cells first (when that's not too often). */
function walkBetween(from, to, now, then = update) {
  if (!from || REDUCED.matches || isUrgent(to) || baseOf(from) === 'hello' || M.on !== 'box' || T.open) return false
  if (!isState(from)) return false // not right after a click reaction, a walk or a landing
  const w = world()
  if (!w || now - M.lastWalk < WALK_GAP) return false
  const { home, far } = range(w)
  if (far - home < 12 * CELL) return false
  const cells = 5 + Math.floor(Math.random() * 5)
  return walkTo(clamp(nextSpot(cells), home, far), then)
}

/**
 * From scene `from` to scene `to` without anything popping: out-<from> packs its props away (he ends in the
 * plain pose), maybe a short walk, then in-<to> sets the next scene up and update() shows it. Those clips are
 * generated from each scene's first frame (animations/gen/transitions.py) and play once.
 */
function switchScene(from, to, now) {
  if (!from || REDUCED.matches || from === `in-${to}` || M.on !== 'box') return false
  const out = isState(from) && has(`out-${from}`) ? `out-${from}` : ''
  const setUp = () => {
    const next = desired(Date.now()) // it may have changed meanwhile
    if (isState(next) && has(`in-${next}`) && next !== V.shown) playOnce('scene', `in-${next}`)
    else update()
  }
  const walk = () => {
    if (!walkBetween(from, to, Date.now(), setUp)) setUp()
  }
  if (out) {
    playOnce('scene', out, walk)
    return true
  }
  if (isState(to) && has(`in-${to}`)) {
    walk()
    return true
  }
  return walkBetween(from, to, now)
}

/** While idle, now and then he wanders: somewhere new on the box, or to its end to wobble, sit, or hop off. */
function planWander(now) {
  if (REDUCED.matches) return
  if (!M.wanderAt || M.wanderAt < now - 1000) M.wanderAt = now + WANDER[0] + Math.random() * (WANDER[1] - WANDER[0])
  clearTimeout(M.wanderTimer)
  M.wanderTimer = setTimeout(() => {
    const t = Date.now()
    const asleep = t - S.lastActive > SLEEP_AFTER
    if (M.act || S.busy || S.oneShot || asleep || t < S.typingUntil || t < M.wanderAt || T.open || M.on !== 'box') return
    M.wanderAt = 0
    const w = world()
    if (!w) return
    const { home, far } = range(w)
    // the end of the box he's nearest
    const side = M.u < w.b.width / 2 ? 'R' : 'L'
    const away = side === 'R' ? M.u - EDGE_IN : w.b.width - EDGE_IN - M.u
    const r = Math.random()
    if (away < NEAR_EDGE) {
      if (r < 0.1 && (side === 'L' ? w.gapL : w.gapR)) return toEdge(side, () => teeter(side, () => hopOff(side)))
      if (r < 0.22) return toEdge(side, () => sitEdge(side))
      if (r < 0.3) return toEdge(side, () => teeter(side, settle))
    }
    if (!walkTo(home + Math.random() * (far - home))) update()
  }, M.wanderAt - now + 10)
}

// --- The ends of the box -----------------------------------------------------

function toEdge(side, then) {
  const w = world()
  if (!w) return
  if (!walkTo(side === 'R' ? EDGE_IN : w.b.width - EDGE_IN, then)) then()
}

function teeter(side, then) {
  playOnce('edge', side === 'L' ? 'teeter-left' : 'teeter-right', then)
}

function sitEdge(side) {
  const name = side === 'L' ? 'sit-edge-left' : 'sit-edge-right'
  if (!has(name)) return settle()
  stopAct()
  const a = { kind: 'sit', name }
  M.act = a
  show(name, true)
  M.timer = setTimeout(() => M.act === a && standUp(), 15_000 + Math.random() * 25_000)
}

function standUp() {
  stopAct()
  settle()
}

/** Off the end of the box: the hop's take-off, then a flight down to the bottom of the panel. */
function hopOff(side) {
  const name = side === 'L' ? 'hop-left' : 'hop-right'
  if (!has(name)) return settle()
  stopAct()
  const a = { kind: 'hop', name }
  M.act = a
  show(name, true)
  M.timer = setTimeout(() => {
    if (M.act === a) fly((side === 'L' ? -26 : 26) * CELL, -36 * CELL, 'hop', name)
  }, HOP.air)
}

/** To the nearer end of the box that has room beside it, a wobble at the edge, and off (the playground's button). */
function hopOffEnd() {
  const w = world()
  if (!w || M.on !== 'box' || M.act) return false
  const near = M.u < w.b.width / 2 ? 'R' : 'L'
  const far = near === 'R' ? 'L' : 'R'
  const room = side => (side === 'L' ? w.gapL : w.gapR)
  const side = room(near) ? near : room(far) ? far : ''
  if (!side) return false
  toEdge(side, () => teeter(side, () => hopOff(side)))
  return true
}

// --- Back up from the bottom of the panel ------------------------------------

/** A breather, a look up at the box, a walk over to it, the climb, and back into his stretch. */
function goHome() {
  const w = world()
  if (!w || M.on !== 'floor') return update()
  stopAct()
  const left = M.fx < w.b.left
  const a = { kind: 'wait', name: has('idle') ? 'idle' : V.shown }
  M.act = a
  show(a.name)
  M.timer = setTimeout(() => {
    if (M.act !== a) return
    playOnce('look', left ? 'look-up-right' : 'look-up-left', () => {
      const w2 = world()
      if (!w2 || M.on !== 'floor') return update()
      const wall = left ? w2.b.left - (21 * CELL - FEET[0]) : w2.b.right + (FEET[0] - 10 * CELL)
      const up = () => climb(left)
      if (!walkTo(wall, up)) up()
    })
  }, 900 + Math.random() * 1500)
}

/**
 * Up the box's side, walking on it like a crab (climb-right/-left: the walk turned a quarter, his feet on the wall,
 * his rear at the image's bottom edge). `left`: he's in the gap left of the box, the wall on his right.
 */
function climb(left) {
  const name = left ? 'climb-right' : 'climb-left'
  stopAct()
  M.on = null
  const a = { kind: 'climb', name: has(name) ? name : 'grabbed' }
  M.act = a
  show(a.name, true)
  let last = performance.now()
  const step = now => {
    if (M.act !== a) return
    const w = world()
    if (!w) return
    const dt = Math.max(0, Math.min(0.05, (now - last) / 1000))
    last = now
    M.fx = left ? w.b.left - (21 * CELL - FEET[0]) : w.b.right + (FEET[0] - 10 * CELL)
    const top = w.top + 8 * CELL // his rear 8 cells below the top edge: his head (10.5 cells up) peeks over it
    M.fy = Math.max(top, Math.min(M.fy, w.floor) - CLIMB_CPS * CELL * dt)
    place()
    if (M.fy <= top) {
      M.raf = 0
      M.act = null
      overTop(left)
      return
    }
    M.raf = requestAnimationFrame(step)
  }
  M.raf = requestAnimationFrame(step)
}

/** Over the top: a quarter turn onto the box (his rear at the corner, feet on its top), then on into his stretch. */
function overTop(left) {
  const w = world()
  M.on = 'box'
  M.u = w ? (left ? w.b.width - BODY_HALF : BODY_HALF) : -1
  settle()
}

// --- Clicks and the cursor ---------------------------------------------------

/** A click: the first one opens his speech bubble; clicks while it's open poke him; 3 quick ones: dizzy. */
function click() {
  const now = Date.now()
  M.clicks = M.clicks.filter(t => now - t < 1500)
  M.clicks.push(now)
  if (M.clicks.length >= 3 && has('click-dizzy')) {
    M.clicks = []
    return react('click-dizzy')
  }
  if (T.open) return react()
  activity()
  openTalk().then(ok => ok || react())
}

function react(name) {
  if (M.on !== 'box' && M.on !== 'floor') return // not in the air or on a wall
  if (!name) {
    const pool = CLICK_SET.filter(n => has(n) && n !== M.lastClick && (n !== 'click-hide' || M.on === 'box'))
    if (pool.length === 0) return
    name = pick(pool)
  }
  M.lastClick = name
  activity()
  playOnce('react', name, M.on === 'box' ? settle : update)
}

/** The cursor comes onto him while he's idle or asleep: he notices you (at most every 20 s). */
function onEnter() {
  const now = Date.now()
  if (D.down || M.act || T.open || S.busy || now - M.noticeAt < 20_000 || !has('notice')) return
  if (!isIdle(V.shown) && baseOf(V.shown) !== 'sleep') return
  M.noticeAt = now
  activity()
  playOnce('react', 'notice')
}

/** Petting: the cursor going back and forth over him a few times. */
function hover(ev) {
  const p = M.pet
  const dx = ev.movementX || 0
  if (!dx) return
  const now = performance.now()
  const dir = Math.sign(dx)
  if (dir === p.dir) p.run += Math.abs(dx)
  else {
    if (p.run >= 6) p.flips.push(now)
    p.dir = dir
    p.run = Math.abs(dx)
  }
  p.flips = p.flips.filter(t => now - t < 1600)
  if (p.flips.length < 4 || T.open || !has('pet') || Date.now() - M.petAt < 6000) return
  if (M.act && M.act.name !== 'notice') return
  if (M.on !== 'box' && M.on !== 'floor') return
  p.flips = []
  M.petAt = Date.now()
  activity()
  playOnce('react', 'pet', M.on === 'box' ? settle : update)
}

// --- Grab, throw, drop -------------------------------------------------------

const D = { down: null, samples: [] }

function onDown(ev) {
  if (ev.button !== 0) return
  ev.preventDefault()
  ev.stopPropagation()
  try {
    ev.currentTarget.setPointerCapture(ev.pointerId)
  } catch {}
  D.down = { px: ev.clientX, py: ev.clientY, fx: M.fx, fy: M.fy, moved: false }
  D.samples = []
}

function onMove(ev) {
  const d = D.down
  if (!d) return hover(ev)
  const dx = ev.clientX - d.px
  const dy = ev.clientY - d.py
  if (!d.moved && Math.hypot(dx, dy) < 5) return
  const now = performance.now()
  if (!d.moved) {
    d.moved = true
    activity()
    stopAct()
    M.on = null
    M.act = { kind: 'drag', name: has('grabbed') ? 'grabbed' : V.shown, still: now, flips: [], dir: 0, run: 0, dizzy: 0 }
    show(M.act.name, true)
    document.documentElement.classList.add('cx-grabbing')
    M.timer = setTimeout(dragMood, 250)
  }
  const w = world()
  const a = M.act
  if (!w || a?.kind !== 'drag') return
  const nx = clamp(d.fx + dx, w.left + BODY_HALF, w.right - BODY_HALF)
  const ny = clamp(d.fy + dy, w.ceil + BODY_H, w.floor)
  // shaking him: quick back-and-forth
  const step = nx - M.fx
  if (Math.abs(step) > 0.5) {
    const dir = Math.sign(step)
    if (dir === a.dir) a.run += Math.abs(step)
    else {
      if (a.run > 10) a.flips.push(now)
      a.dir = dir
      a.run = Math.abs(step)
    }
    a.flips = a.flips.filter(t => now - t < 900)
    if (a.flips.length >= 4) a.dizzy = now + 1200
  }
  if (Math.hypot(nx - M.fx, ny - M.fy) > 1) a.still = now
  M.fx = nx
  M.fy = ny
  place()
  D.samples.push({ t: now, x: M.fx, y: M.fy })
  if (D.samples.length > 12) D.samples.shift()
}

/** While you hold him: grabbed, grabbed-dizzy while you shake him, grabbed-bored once you've held him still a while. */
function dragMood() {
  const a = M.act
  if (a?.kind !== 'drag') return
  const now = performance.now()
  const want = now < a.dizzy ? 'grabbed-dizzy' : now - a.still > 4000 ? 'grabbed-bored' : 'grabbed'
  if (has(want) && want !== a.name) {
    a.name = want
    show(want, true)
  }
  M.timer = setTimeout(dragMood, 250)
}

function onUp(ev) {
  const d = D.down
  if (!d) return
  D.down = null
  ev.stopPropagation()
  document.documentElement.classList.remove('cx-grabbing')
  if (!d.moved) {
    if (M.act?.kind === 'fly') {
      if (M.act.chute) cutChute()
      return
    }
    click()
    return
  }
  const now = performance.now()
  const old = D.samples.find(s => now - s.t < 90) ?? D.samples[0] ?? { t: now - 16, x: M.fx, y: M.fy }
  const dt = Math.max(0.016, (now - old.t) / 1000)
  const vx = (M.fx - old.x) / dt // px/s in screen directions: +x right, +y down
  const vy = (M.fy - old.y) / dt
  const w = world()
  const ground = !w ? M.fy : overBox(w, M.fx) && M.fy <= w.top ? w.top : w.floor
  if (Math.hypot(vx, vy) / CELL > 45) fly(vx, vy, 'tumble')
  else if (ground - M.fy > 9 * CELL) fly(0, 0, 'fall')
  else fly(0, 0, 'drop')
}

/**
 * A flight: thrown ('tumble'), let go high up ('fall': the parachute opens), let go low ('drop'), or off the end
 * of the box ('hop'). Gravity, the column's walls and top, the box's sides; he lands on the box's top or on the
 * bottom of the panel.
 */
function fly(vx, vy, mode, clip) {
  stopAct()
  M.on = null
  const first = clip ?? (mode === 'tumble' ? 'tumble' : mode === 'fall' ? 'fall' : 'grabbed')
  const a = { kind: 'fly', name: has(first) ? first : V.shown, mode, chute: false, cut: false, vx, vy }
  M.act = a
  show(a.name, true)
  const t0 = performance.now()
  let last = t0
  const step = now => {
    if (M.act !== a) return
    const w = world()
    if (!w) {
      M.act = null
      return
    }
    const dt = Math.max(0, Math.min(0.05, (now - last) / 1000)) // rAF's first timestamp can be before t0
    last = now
    const b = w.b
    const ground = overBox(w, M.fx) && M.fy <= w.top + 1 ? w.top : w.floor
    if (a.mode === 'fall' && !a.chute && !a.cut && now - t0 > 380 && ground - M.fy > 8 * CELL && has('parachute')) {
      a.chute = true
      a.name = 'parachute'
      show('parachute', true)
    }
    if (a.mode === 'hop' && a.name === clip && now - t0 > HOP.land - HOP.air && has('fall')) {
      a.name = 'fall'
      show('fall', true)
    }
    if (a.chute) {
      a.vy = CHUTE_FALL
      a.vx = Math.sin((now - t0) / 700) * 2 * CELL
    } else {
      a.vy += G * dt
    }
    const py = M.fy
    M.fx += a.vx * dt
    M.fy += a.vy * dt
    // the column's sides and top
    if (M.fx < w.left + BODY_HALF) {
      M.fx = w.left + BODY_HALF
      a.vx = Math.abs(a.vx) * 0.55
    }
    if (M.fx > w.right - BODY_HALF) {
      M.fx = w.right - BODY_HALF
      a.vx = -Math.abs(a.vx) * 0.55
    }
    if (M.fy - BODY_H < w.ceil) {
      M.fy = w.ceil + BODY_H
      a.vy = Math.abs(a.vy) * 0.3
    }
    // the box: its top is ground, its sides are walls
    const over = overBox(w, M.fx)
    if (over && a.vy > 0 && py <= w.top + 1 && M.fy >= w.top) { // coming down onto it (a hop starts on it)
      M.fy = w.top
      return touchDown(a, 'box', w)
    }
    if (M.fy > w.top && M.fy - BODY_H < b.bottom) {
      if (over) {
        // let go inside the box: up onto it
        M.fy = w.top
        return touchDown(a, 'box', w)
      }
      if (M.fx > b.left - BODY_HALF && M.fx < b.left) {
        M.fx = b.left - BODY_HALF
        a.vx = -Math.abs(a.vx) * 0.55
      }
      if (M.fx < b.right + BODY_HALF && M.fx > b.right) {
        M.fx = b.right + BODY_HALF
        a.vx = Math.abs(a.vx) * 0.55
      }
    }
    if (M.fy >= w.floor) {
      M.fy = w.floor
      return touchDown(a, 'floor', w)
    }
    place()
    M.raf = requestAnimationFrame(step)
  }
  M.raf = requestAnimationFrame(step)
}

function touchDown(a, on, w) {
  M.raf = 0
  M.on = on
  if (on === 'box') M.u = w.b.right - M.fx
  place()
  const hard = a.mode === 'tumble' || (a.mode !== 'hop' && a.vy / CELL > 70)
  const land = a.chute ? 'land-chute' : hard ? 'crash' : 'land'
  const after = on === 'box' ? settle : update // from the bottom of the panel, update() starts the climb home
  if (has(land)) playOnce('land', land, after)
  else {
    M.act = null
    after()
  }
}

function cutChute() {
  const a = M.act
  a.chute = false
  a.cut = true
  a.vx *= 0.3
  if (!has('chute-pop')) return
  a.name = 'chute-pop'
  show('chute-pop', true)
  setTimeout(() => {
    if (M.act === a && has('fall')) {
      a.name = 'fall'
      show('fall', true)
    }
  }, cycle('chute-pop'))
}

window.addEventListener('resize', place)

// ---------------------------------------------------------------------------
// Talking to him. Clicking him opens the extension's own /btw side-question
// panel, which custom.css restyles as a speech bubble coming out of him
// (.cx-talk, plus the .cx-talk-tail pointing at him): you ask Claude something
// with the conversation as context, without interrupting it. While it's open
// he listens (talk-listen), thinks while it answers (talk-think), presents the
// answer (talk-explain), or shrugs when there's none (click-shrug).
// The extension only opens that panel for "/btw" in the input box, so
// openTalk() types it there and Enter, then puts back what you had typed.
// ---------------------------------------------------------------------------

const T = { open: false, pending: false, answers: 0, explainUntil: 0, shrugUntil: 0, issuing: false, panel: null, tail: null }
const SIDE_INPUT = 'textarea[aria-label="Ask a side question"]'

/** Finds the side-question panel (it comes and goes with React) and follows what happens in it. */
function syncTalk() {
  const panel = document.querySelector(SIDE_INPUT)?.closest('[class*="panel_"]') ?? null
  const now = Date.now()
  if (panel !== T.panel) {
    T.panel = panel
    if (panel) {
      panel.classList.add('cx-talk')
      T.pending = Boolean(panel.querySelector('[class*="pendingGlyph_"]'))
      T.answers = panel.querySelectorAll('[class*="answer_"]').length
    }
  }
  if (Boolean(panel) !== T.open) {
    T.open = Boolean(panel)
    if (T.open) {
      T.tail ??= Object.assign(document.createElement('div'), { className: 'cx-talk-tail' })
      document.body.append(T.tail)
    } else {
      T.tail?.remove()
      T.pending = false
      T.explainUntil = 0
      T.shrugUntil = 0
    }
    activity()
    placeTalk()
    update()
    return
  }
  if (!panel) return
  placeTalk()
  const pending = Boolean(panel.querySelector('[class*="pendingGlyph_"]'))
  const answers = panel.querySelectorAll('[class*="answer_"]').length
  if (pending === T.pending && answers === T.answers) return
  if (T.pending && !pending) {
    // the answer arrived, or the question failed
    if (answers > T.answers) T.explainUntil = now + cycle('talk-explain')
    else T.shrugUntil = now + cycle('click-shrug')
  }
  T.pending = pending
  T.answers = answers
  activity()
  update()
}

/**
 * The bubble sits just above his image (the talk clips draw a spark over his head), up and to his left when
 * there's room (the talk clips look and point that way), inside the chat column, its tail pointing at him.
 */
function placeTalk(w = world()) {
  if (!T.panel || !w) return
  const root = document.documentElement.style
  const width = T.panel.offsetWidth || 360
  const bottom = M.fy - IMG.h + 2 // the bubble's bottom edge: his image's top row is empty
  const left = clamp(M.fx - width * 0.78, w.left + 8, Math.max(w.left + 8, w.right - 8 - width))
  root.setProperty('--cx-bl', `${Math.round(left)}px`)
  root.setProperty('--cx-bb', `${Math.round(innerHeight - bottom)}px`)
  root.setProperty('--cx-bh', `${Math.round(Math.max(120, bottom - w.ceil - 8))}px`)
  root.setProperty('--cx-tl', `${Math.round(clamp(M.fx - 6, left + 16, left + width - 28))}px`)
  root.setProperty('--cx-tt', `${Math.round(bottom - 7)}px`)
}

/** Opens the side-question panel: types /btw in the input box and Enter, then puts your text back. */
async function openTalk() {
  if (T.panel) {
    T.panel.querySelector(SIDE_INPUT)?.focus()
    return true
  }
  const input = document.querySelector('[class*="messageInput_"][contenteditable]')
  if (!input) return false
  const draft = input.innerText.replace(/\n+$/, '')
  const opened = () => Boolean(document.querySelector(SIDE_INPUT))
  T.issuing = true
  try {
    typeInto(input, '/btw')
    await later(40)
    let ok = false
    // Enter, and Ctrl+Enter for "Ctrl+Enter to send"
    for (const mods of [{}, { ctrlKey: true }]) {
      if (!/^\/btw\s*$/.test(input.innerText.trim())) break
      pressEnter(input, mods)
      ok = await waitFor(opened, 700)
      if (ok) break
    }
    if (input.innerText.replace(/\n+$/, '') !== draft) typeInto(input, draft)
    syncTalk()
    document.querySelector(SIDE_INPUT)?.focus()
    return ok || opened()
  } catch (err) {
    console.warn('[custom] talk', err)
    return false
  } finally {
    T.issuing = false
  }
}

function typeInto(el, text) {
  el.focus()
  const range = document.createRange()
  range.selectNodeContents(el)
  const sel = getSelection()
  sel.removeAllRanges()
  sel.addRange(range)
  if (text) document.execCommand('insertText', false, text)
  else document.execCommand('delete', false)
}

function pressEnter(el, mods) {
  for (const type of ['keydown', 'keyup']) {
    el.dispatchEvent(new KeyboardEvent(type, { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true, ...mods }))
  }
}

async function waitFor(test, ms) {
  const end = Date.now() + ms
  while (Date.now() < end) {
    if (test()) return true
    await later(30)
  }
  return test()
}

// ---------------------------------------------------------------------------
// Mounting: Clawd is an <img> inside the input box (a <fieldset> the
// extension's React UI re-renders), put back whenever it goes missing.
// His hit area is a <div> over his body, so clicks on the empty parts of the
// image still reach the chat underneath.
// ---------------------------------------------------------------------------

let mounted = false
const resized = new ResizeObserver(() => place())

function mount() {
  for (const box of document.querySelectorAll('fieldset[class*="inputContainer_"]')) {
    watchMode(box)
    if (box.querySelector(':scope > .cx-clawd') && box.querySelector(':scope > .cx-clawd-hit')) continue
    box.querySelectorAll(':scope > .cx-clawd, :scope > .cx-clawd-hit').forEach(el => el.remove())
    const img = document.createElement('img')
    img.className = 'cx-clawd'
    img.alt = ''
    img.setAttribute('aria-hidden', 'true')
    img.addEventListener('error', () => {
      if (V.noQuery) return
      V.noQuery = true
      img.src = img.src.replace(/\?p=\d+$/, '')
    })
    if (V.shown) img.src = srcFor(V.shown)
    const hit = document.createElement('div')
    hit.className = 'cx-clawd-hit'
    hit.setAttribute('aria-hidden', 'true')
    hit.addEventListener('pointerdown', onDown)
    hit.addEventListener('pointermove', onMove)
    hit.addEventListener('pointerup', onUp)
    hit.addEventListener('pointercancel', onUp)
    hit.addEventListener('pointerenter', onEnter)
    hit.addEventListener('click', ev => ev.stopPropagation())
    // First children, so the extension's popups (later in the box) draw over him.
    box.prepend(img, hit)
    borders = null
    resized.observe(box)
    place()
    if (!mounted) {
      mounted = true
      oneShot(variant('hello', Date.now(), true))
      update()
    }
  }
}

// For poking at him from the webview's developer tools: cxClawd.M (where he is), .T (his bubble), .V (what he shows).
globalThis.cxClawd = { S, V, M, T, world, update, place, hopOff, hopOffEnd, goHome }

// The input box carries the permission mode as data-permission-mode.
function watchMode(box) {
  const mode = box.dataset.permissionMode ?? ''
  if (mode === S.mode) return
  const changed = S.mode !== ''
  S.mode = mode
  if (changed && !S.busy && MODE[mode]) {
    activity()
    oneShot(pick(MODE[mode].filter(has)) ?? 'idle')
    update()
  }
}

// ===========================================================================
// Footer controls (a redesigned input footer)
//
//   context .. ring + "34%", always shown (the extension's own ring only
//              appears past 50%, so it's hidden in favour of this one).
//              Click opens a small "Compact this chat?" confirm; Compact
//              runs the extension's own compact.
//   usage .... two 16x3 bars: session (5-hour) on top, weekly below; the
//              top one turns yellow past 80%, red past 95%. Click opens
//              "Account & usage…".
//   agents ... agents icon + how many subagents are working, always shown
//              (the extension's own pill only exists while a chat has
//              agents). A dot shows their state: green running, yellow
//              waiting for you, red failed. Click opens the agent map.
//   Ultracode  fan-out icon + "Ultracode", right of the spacer. Toggles the
//              mode menu's own Ultracode switch; only shown when that switch
//              is. Switching on sends a purple dot wave through the box,
//              then a purple edge with a slow glint stays while it's on.
//   effort ... "Effort" + a slider with one step per level the model
//              offers; hidden when the model has no effort setting.
//
// Clicks go through the panel's own handlers, read from the footer's React
// props (the panel is React; each DOM node links to its fiber). If those
// can't be found, the extension's own controls stay as they were.
// The controls carry data-footer-overlay: the footer re-measures itself on
// any DOM change inside it except under that attribute, so updating them
// doesn't make it collapse and expand.
// ===========================================================================

const FOOT = {
  windows: null, // plan limits: { five_hour, seven_day, ... }: { utilization 0-1, resetsAt (s) }
}

/** Props of the nearest React component above `node` that passes `test`. */
function fiberProps(node, test, depth = 40) {
  const key = node && Object.keys(node).find(k => k.startsWith('__reactFiber$'))
  for (let f = key ? node[key] : null, i = 0; f && i < depth; f = f.return, i++) {
    const p = f.memoizedProps
    if (p && typeof p === 'object' && test(p)) return p
  }
  return null
}

/** The footer component's props: session, onCompact, modelSelector.commandRegistry, … */
function footerProps(footer) {
  return fiberProps(footer, p => p.session && 'onCompact' in p)
}

/**
 * The mode menu's props (the "Manual ▾" button): effortLevel,
 * supportedEffortLevels, onSetEffort, ultracodeAvailable, ultracodeOn,
 * onSetUltracode. The panel only fills the effort ones in when the model
 * supports effort, and its Ultracode switch only shows when
 * ultracodeAvailable — the footer controls follow the same rules.
 */
function modeProps(footer) {
  const btn = footer.querySelector('button[title*="Shift+Tab"]')
  return fiberProps(btn, p => 'availableModes' in p && 'supportedEffortLevels' in p, 8)
}

function runCommand(footer, id) {
  const registry = footerProps(footer)?.modelSelector?.commandRegistry
  if (typeof registry?.executeCommand === 'function') registry.executeCommand(id)
  else console.warn('[custom] footer: command registry not found for', id)
}

// Same merge the panel does (VPe): null removes a window, an update without
// a reset time doesn't replace one that has it.
function mergeWindows(update) {
  if (!update || typeof update !== 'object') return
  const next = { ...(FOOT.windows ?? {}) }
  for (const k of ['five_hour', 'seven_day', 'seven_day_overage_included']) {
    const w = update[k]
    if (w === null) {
      delete next[k]
      continue
    }
    if (!w || (w.resetsAt === undefined && next[k]?.resetsAt !== undefined)) continue
    next[k] = w
  }
  FOOT.windows = Object.keys(next).length > 0 ? next : null
}

function windowPct(w, now) {
  if (!w) return null
  if (w.resetsAt !== undefined && w.resetsAt * 1000 <= now) return 0
  return Math.max(0, Math.min(100, Math.round((w.utilization ?? 0) * 100)))
}

function resetsIn(w, now) {
  if (!w?.resetsAt) return ''
  const mins = Math.max(0, Math.round((w.resetsAt * 1000 - now) / 60_000))
  if (mins >= 48 * 60) return ` · resets in ${Math.round(mins / 1440)}d`
  if (mins >= 60) return ` · resets in ${Math.floor(mins / 60)}h ${mins % 60}m`
  return ` · resets in ${mins}m`
}

/** % of context used, measured the way the panel's own ring does (DPt). */
function contextPct(session) {
  const u = session?.usageData?.value
  if (!u) return null
  if (!u.totalTokens) return 0
  // auto-compact point: the window minus room for the reply (≤20k) and a 13k buffer
  const limit = u.contextWindow - Math.min(u.maxOutputTokens ?? 0, 20_000) - 13_000
  if (!(u.contextWindow > 0) || limit <= 0) return null // not known until the first reply
  return Math.min(100, Math.round((u.totalTokens / limit) * 100))
}

function h(tag, className, attrs = {}) {
  const n = document.createElement(tag)
  if (className) n.className = className
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v)
  return n
}

function setText(node, text) {
  if (node.textContent !== text) node.textContent = text
}

function setAttr(node, name, value) {
  if (value === null || value === undefined) {
    if (node.hasAttribute(name)) node.removeAttribute(name)
  } else if (node.getAttribute(name) !== value) node.setAttribute(name, value)
}

// ---------------------------------------------------------------------------
// Compact asks first: clicking context opens a small confirm above it.
// ---------------------------------------------------------------------------

const CONFIRM = { pop: null, anchor: null, off: null }

function closeConfirm(refocus = false) {
  const { pop, anchor, off } = CONFIRM
  CONFIRM.pop = CONFIRM.anchor = CONFIRM.off = null
  off?.()
  pop?.remove()
  anchor?.setAttribute('aria-expanded', 'false')
  if (refocus && anchor?.isConnected) anchor.focus({ preventScroll: true })
}

function openCompactConfirm(footer, anchor) {
  if (CONFIRM.anchor === anchor) return closeConfirm()
  closeConfirm()
  const box = footer.closest('fieldset')
  if (!box) return
  const pct = contextPct(footerProps(footer)?.session)
  const pop = h('div', 'cx-pop cx-confirm', { role: 'dialog', 'aria-label': 'Compact this chat?', 'data-footer-overlay': '' })
  const title = h('div', 'cx-pop-title')
  title.textContent = 'Compact this chat?'
  const body = h('div', 'cx-pop-body')
  body.textContent =
    'Claude summarizes the conversation so far to free up context' +
    (pct === null ? '.' : `. ${pct}% is used now.`)
  const row = h('div', 'cx-pop-actions')
  const yes = h('button', 'cx-btn cx-btn-primary', { type: 'button' })
  yes.textContent = 'Compact'
  const no = h('button', 'cx-btn cx-btn-secondary', { type: 'button' })
  no.textContent = 'Cancel'
  row.append(yes, no)
  pop.append(title, body, row)
  yes.addEventListener('click', ev => {
    ev.preventDefault()
    closeConfirm()
    try {
      footerProps(footer)?.onCompact?.()
    } catch (err) {
      console.warn('[custom] compact', err)
    }
  })
  no.addEventListener('click', ev => {
    ev.preventDefault()
    closeConfirm(true)
  })

  // above the context control, its left edge lined up with it
  const r = box.getBoundingClientRect()
  const b = anchor.getBoundingClientRect()
  const scale = box.offsetWidth ? r.width / box.offsetWidth : 1
  const left = Math.max(4, Math.round((b.left - r.left) / scale - box.clientLeft) - 2)
  pop.style.left = `${left}px`
  pop.style.bottom = `${Math.round((r.bottom - b.top) / scale - box.clientTop) + 6}px`
  pop.style.maxWidth = `${Math.max(180, box.clientWidth - left - 4)}px`
  box.append(pop)

  const onDown = ev => {
    if (!pop.contains(ev.target) && !anchor.contains(ev.target)) closeConfirm()
  }
  const onKey = ev => {
    if (ev.key !== 'Escape') return
    ev.preventDefault()
    ev.stopPropagation()
    closeConfirm(true)
  }
  document.addEventListener('pointerdown', onDown, true)
  document.addEventListener('keydown', onKey, true)
  CONFIRM.pop = pop
  CONFIRM.anchor = anchor
  CONFIRM.off = () => {
    document.removeEventListener('pointerdown', onDown, true)
    document.removeEventListener('keydown', onKey, true)
  }
  anchor.setAttribute('aria-expanded', 'true')
  yes.focus({ preventScroll: true })
}

// ---------------------------------------------------------------------------
// Effort slider and Ultracode
// ---------------------------------------------------------------------------

const LEVEL_NAME = { low: 'Low', medium: 'Medium', high: 'High', xhigh: 'Extra high', max: 'Max' }
const UC_TITLE = 'Ultracode: run dynamic workflows on every task (this session only)'

/** What the effort slider shows: { levels, level, index } or null when the model has no effort. */
function effortState(footer, session) {
  const mp = modeProps(footer)
  const levels = mp?.supportedEffortLevels
  if (!Array.isArray(levels) || levels.length === 0 || typeof mp.onSetEffort !== 'function') return null
  const level = session?.effortLevel?.value ?? mp.effortLevel
  const index = levels.indexOf(level)
  return { levels, level: index === -1 ? undefined : level, index: Math.max(0, index), set: mp.onSetEffort }
}

function paintEffort(eff, levels, index, level) {
  const name = level ? (LEVEL_NAME[level] ?? level) : 'Auto'
  setAttr(eff, 'data-level', level ?? 'auto')
  const f = levels.length > 1 ? (index / (levels.length - 1)).toFixed(3) : '0'
  if (eff.style.getPropertyValue('--f') !== f) eff.style.setProperty('--f', f)
  const range = eff.querySelector('input')
  setAttr(range, 'max', String(levels.length - 1))
  if (range.value !== String(index)) range.value = String(index)
  setAttr(range, 'aria-valuetext', name)
  placeBubble(eff)
}

// The level bubble lives in the input box, not the footer: anything that
// sticks out of a footer control makes the footer think it's clipped, and
// it re-measures exactly when effort changes (mid-drag, bubble showing), so
// it would drop to its narrowest layout and everything would jump.
function placeBubble(eff) {
  const box = eff.closest('fieldset')
  if (!box) return
  let bubble = box.querySelector(':scope > .cx-bubble')
  const show = eff.isConnected && !eff.hidden && eff.hasAttribute('data-show')
  if (!show) {
    bubble?.remove()
    return
  }
  if (!bubble) {
    bubble = h('div', 'cx-bubble', { 'aria-hidden': 'true', 'data-footer-overlay': '' })
    const row = h('span', 'cx-bubble-row')
    row.append(h('i', 'cx-dot'), h('span', 'cx-name'))
    const note = h('span', 'cx-bubble-note')
    note.textContent = 'uses many more tokens'
    bubble.append(row, note)
    box.append(bubble)
  }
  const range = eff.querySelector('input')
  setAttr(bubble, 'data-level', eff.getAttribute('data-level'))
  setText(bubble.querySelector('.cx-name'), range.getAttribute('aria-valuetext') ?? '')
  // 6px above the control, centred on the thumb (thumb radius 6)
  const r = box.getBoundingClientRect()
  const t = range.getBoundingClientRect()
  const scale = box.offsetWidth ? r.width / box.offsetWidth : 1
  const max = Number(range.max) || 1
  const thumbX = t.left + (6 + (t.width / scale - 12) * (Number(range.value) / max)) * scale
  bubble.style.left = `${Math.round((thumbX - r.left) / scale - box.clientLeft)}px`
  bubble.style.bottom = `${Math.round((r.bottom - t.top) / scale - box.clientTop) + 6}px`
}

const UC = new WeakMap() // fieldset -> { on, timer }

/** Where the wave starts: the centre of the Ultracode button (or the mode button), in box px. */
function ucOrigin(box, footer) {
  const el = [footer.querySelector(':scope > .cx-uc'), footer.querySelector('button[title*="Shift+Tab"]')].find(
    e => e && e.getClientRects().length > 0,
  )
  if (!el) return { ox: box.clientWidth - 60, oy: box.clientHeight - 20 }
  const r = box.getBoundingClientRect()
  const b = el.getBoundingClientRect()
  const scale = box.offsetWidth ? r.width / box.offsetWidth : 1
  return {
    ox: Math.round((b.left + b.width / 2 - r.left) / scale - box.clientLeft),
    oy: Math.round((b.top + b.height / 2 - r.top) / scale - box.clientTop),
  }
}

/**
 * The Ultracode layers in the input box.
 *   'on' ... the switch-on wave, then the holding edge and glow
 *   'hold' . just the holding edge and glow (already on when the panel loads)
 *   'off' .. edge and glow fading out
 *   'none' . nothing
 * The edge and glow go before Clawd and the box's background, so Clawd
 * still stands on top of the edge; the dots go right after the background,
 * under the text and the footer.
 */
function ucLayers(box, kind, origin) {
  box.querySelectorAll(':scope > .cx-uc-fx').forEach(n => n.remove())
  if (kind === 'none') return
  const at = origin ? `--ox:${origin.ox}px;--oy:${origin.oy}px;` : ''
  const fx = (cls, style = '') => h('span', `cx-uc-fx ${cls}`, { 'aria-hidden': 'true', style: at + style })
  const ringIn = cls => {
    const n = fx(cls)
    n.append(h('span', 'cx-uc-ring'))
    return n
  }
  const edge = []
  const dots = []
  if (kind === 'off') {
    edge.push(fx('cx-uc-under cx-uc-off'), fx('cx-uc-ring cx-uc-offring cx-uc-off'))
  } else {
    const still = kind === 'hold' ? ' cx-uc-still' : ''
    edge.push(fx('cx-uc-under' + still))
    if (kind === 'on') {
      dots.push(
        fx('cx-uc-bloom'),
        fx('cx-uc-dots cx-uc-wave', '--d:0s'),
        fx('cx-uc-dots cx-uc-hot cx-uc-wave cx-uc-front', '--d:0s'),
        fx('cx-uc-dots cx-uc-wave', '--d:.35s'),
        fx('cx-uc-dots cx-uc-hot cx-uc-wave cx-uc-front', '--d:.35s'),
        fx('cx-uc-dots cx-uc-wave', '--d:.7s'),
      )
      edge.push(ringIn('cx-uc-reveal'), ringIn('cx-uc-hit'))
    }
    edge.push(fx('cx-uc-ring cx-uc-hold' + still))
  }
  const bg = box.querySelector(':scope > [class*="inputContainerBackground_"]')
  const first = box.querySelector(':scope > .cx-clawd') ?? bg
  if (first) first.before(...edge)
  else box.prepend(...edge)
  if (bg) bg.after(...dots)
  else box.prepend(...dots)
}

function syncUltracode(box, footer, on) {
  const st = UC.get(box)
  if (!st) {
    UC.set(box, { on, timer: 0 })
    if (on) ucLayers(box, 'hold')
    return
  }
  if (st.on === on) {
    if (on && !box.querySelector(':scope > .cx-uc-hold')) ucLayers(box, 'hold')
    return
  }
  st.on = on
  clearTimeout(st.timer)
  if (on) {
    ucLayers(box, 'on', ucOrigin(box, footer))
    // the wave is over by ~3s: drop its layers, keep the edge and glow running
    st.timer = setTimeout(() => {
      if (UC.get(box)?.on) {
        box.querySelectorAll(':scope > :is(.cx-uc-bloom, .cx-uc-dots, .cx-uc-reveal, .cx-uc-hit)').forEach(n => n.remove())
      }
    }, 3300)
    const btn = footer.querySelector(':scope > .cx-uc')
    if (btn) {
      btn.classList.remove('cx-pop')
      void btn.offsetWidth // restart the animation
      btn.classList.add('cx-pop')
      setTimeout(() => btn.classList.remove('cx-pop'), 500)
    }
  } else {
    ucLayers(box, 'off')
    st.timer = setTimeout(() => {
      if (!UC.get(box)?.on) ucLayers(box, 'none')
    }, 380)
  }
}

// Effort and Ultracode can change from the mode menu or a slash command too:
// follow the panel's own state (Preact signals) instead of polling.
const WATCHED = new WeakSet()
function watchSession(session) {
  if (!session || WATCHED.has(session)) return
  WATCHED.add(session)
  for (const k of ['effortLevel', 'ultracodeActive', 'ultracodeAvailable', 'modelSelection', 'usageData', 'claudeConfig', 'agentMapAgents', 'permissionRequests']) {
    const sig = session[k]
    if (typeof sig?.subscribe !== 'function') continue
    try {
      let first = true
      sig.subscribe(() => {
        queueFooterRefresh()
        setTimeout(queueFooterRefresh, 120) // after React has re-rendered with it
        if (first) return void (first = false)
        if (k === 'effortLevel' || k === 'ultracodeActive' || k === 'ultracodeAvailable') {
          setTimeout(() => sendDiag(k + '+200ms'), 200)
          setTimeout(() => sendDiag(k + '+1500ms'), 1500)
        }
      })
    } catch (err) {
      console.warn('[custom] footer: watch', k, err)
    }
  }
}

// The footer measures its children to decide when to shorten itself (its
// "fit stage"), but ignores changes to data-footer-overlay nodes. When one of
// ours appears, hides or changes width, nudge it with a throwaway text node
// so it measures again.
const FIT = new WeakMap()
function remeasure(footer, signature) {
  if (FIT.get(footer) === signature) return
  FIT.set(footer, signature)
  const t = document.createTextNode('')
  footer.append(t)
  t.remove()
}

// ---------------------------------------------------------------------------
// Diagnostics. A report of the footer's state goes into the extension's own
// log ("Received message from webview: {"type":"cx_diag","channelId":…}" in
// the Claude VSCode log file), which the extension writes for every message
// the panel sends; it ignores this type. Sent when the footer looks broken
// (its own + or send button missing) and shortly after effort or Ultracode
// changes, at most 24 times per load. Nothing leaves the machine.
// ---------------------------------------------------------------------------

const DIAG = { sent: 0, lastBroken: 0, stages: [], ops: [] } // stages: recent fit-stage changes, 't:stage'; ops: removals from the footer

// Record anything that takes an element out of the footer (or wipes it),
// with the call stack, so a report can say who did it. Our own controls
// (data-footer-overlay) are left out; the panel moving its model pill in
// and out at fit stage 2 shows up here too, which is normal.
const isFooter = n => n?.nodeType === 1 && typeof n.className === 'string' && n.className.includes('inputFooterV2_')
function noteOp(op, target, child) {
  if (child?.nodeType === 1 && child.hasAttribute('data-footer-overlay')) return
  const stack = (new Error().stack ?? '').split('\n').slice(2, 9).map(l => l.trim().replace(/\(?(vscode-webview|https?|file):\/\/[^)]*\/([^/)]+)\)?/, '$2')).join(' < ')
  DIAG.ops.push(`${Math.round(performance.now())} ${op} ${describeEl(child ?? target)} :: ${stack}`.slice(0, 700))
  if (DIAG.ops.length > 12) DIAG.ops.shift()
}
try {
  const wrap = (proto, name, check) => {
    const orig = proto[name]
    if (typeof orig !== 'function') return
    proto[name] = function (...args) {
      try {
        check(this, args)
      } catch {}
      return orig.apply(this, args)
    }
  }
  wrap(Node.prototype, 'removeChild', (self, [child]) => isFooter(self) && noteOp('removeChild', self, child))
  wrap(Element.prototype, 'remove', self => isFooter(self.parentNode) && noteOp('remove', self.parentNode, self))
  wrap(Element.prototype, 'replaceChildren', self => isFooter(self) && noteOp('replaceChildren', self, null))
  // moved somewhere else while still in the footer
  wrap(Node.prototype, 'insertBefore', (self, [node]) => isFooter(node?.parentNode) && node.parentNode !== self && noteOp('moved-out', node.parentNode, node))
  wrap(Node.prototype, 'appendChild', (self, [node]) => isFooter(node?.parentNode) && node.parentNode !== self && noteOp('moved-out', node.parentNode, node))
  for (const prop of ['textContent', 'innerHTML']) {
    const proto = prop === 'textContent' ? Node.prototype : Element.prototype
    const d = Object.getOwnPropertyDescriptor(proto, prop)
    if (!d?.set) continue
    Object.defineProperty(proto, prop, {
      ...d,
      set(v) {
        try {
          if (isFooter(this)) noteOp('set-' + prop, this, null)
        } catch {}
        return d.set.call(this, v)
      },
    })
  }
} catch (err) {
  console.warn('[custom] diag hooks', err)
}

function describeEl(el) {
  if (!el || el.nodeType !== 1) return String(el)
  const cs = getComputedStyle(el)
  const r = el.getBoundingClientRect()
  const raw = typeof el.className === 'string' ? el.className : el.getAttribute('class') ?? ''
  const cls = raw.split(/\s+/).filter(Boolean).map(c => c.replace(/_[A-Za-z0-9]{6}$/, '_')).slice(0, 3).join('.')
  const bits = [el.tagName.toLowerCase() + (cls ? '.' + cls : ''), cs.display, cs.position, cs.visibility]
  bits.push(`${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.width)}x${Math.round(r.height)}`)
  if (cs.order !== '0') bits.push('o' + cs.order)
  if (el.hidden) bits.push('hidden')
  if (cs.opacity !== '1') bits.push('op' + cs.opacity)
  if (cs.zIndex !== 'auto') bits.push('z' + cs.zIndex)
  return bits.join('|')
}

function sendDiag(why, footer) {
  if (DIAG.sent >= 24) return
  try {
    footer ??= document.querySelector('fieldset[class*="inputContainer_"] [class*="inputFooterV2_"]')
    const box = footer?.closest('fieldset') ?? document.querySelector('fieldset[class*="inputContainer_"]')
    const s = footer ? footerProps(footer)?.session : undefined
    const out = {
      why,
      t: Math.round(performance.now()),
      stage: footer?.getAttribute('data-fit-stage'),
      w: footer?.getAttribute('data-cx-w'),
      ready: footer?.hasAttribute('data-cx-ready'),
      effort: s?.effortLevel?.value,
      uc: [s?.ultracodeAvailable?.value, s?.ultracodeActive?.value],
      busy: s?.busy?.value,
      focus: describeEl(document.activeElement),
      footers: document.querySelectorAll('[class*="inputFooterV2_"]').length,
      adds: document.querySelectorAll('[class*="addButtonContainer_"]').length,
      footer: describeEl(footer),
      kids: footer ? [...footer.childNodes].map(n => (n.nodeType === 1 ? describeEl(n) : `#${n.nodeType}`)) : null,
      box: box ? [...box.children].map(describeEl) : null,
      rows: [...document.querySelectorAll('[class*="modelPillRow_"]')].map(r => describeEl(r) + ' in ' + describeEl(r.parentElement)),
      boxes: [...document.querySelectorAll('fieldset[class*="inputContainer_"]')].map(describeEl),
      stages: DIAG.stages.slice(-16),
      ops: DIAG.ops.slice(-12),
    }
    const api = s?.connection?.value?.api
    if (typeof api?.postMessage !== 'function') return console.warn('[custom] diag', out)
    DIAG.sent++
    api.postMessage({ type: 'cx_diag', channelId: JSON.stringify(out) })
  } catch (err) {
    console.warn('[custom] diag', err)
  }
}

// The footer's own + and send buttons should always be there and visible.
function checkFooter(footer) {
  const add = footer.querySelector(':scope > [class*="addButtonContainer_"]')
  const send = footer.querySelector(':scope > [class*="sendButton_"]')
  const ok = add && send && add.getBoundingClientRect().width > 0 && send.getBoundingClientRect().width > 0
  if (ok) return
  const now = Date.now()
  if (now - DIAG.lastBroken < 3000) return
  DIAG.lastBroken = now
  sendDiag('broken', footer)
}

const footerSize = typeof ResizeObserver === 'function' ? new ResizeObserver(() => queueFooterRefresh()) : null

function ensureControls(footer) {
  if (footer.querySelector(':scope > .cx-ctx')) return
  footerSize?.observe(footer)
  const ctl = (kind, onClick) => {
    const b = h('button', `cx-ctl cx-${kind}`, { type: 'button', 'data-footer-overlay': '' })
    b.addEventListener('click', ev => {
      ev.preventDefault()
      try {
        onClick()
      } catch (err) {
        console.warn('[custom] footer', kind, err)
      }
    })
    return b
  }

  const ctx = ctl('ctx', () => openCompactConfirm(footer, ctx))
  ctx.setAttribute('aria-haspopup', 'dialog')
  ctx.setAttribute('aria-expanded', 'false')
  ctx.append(h('span', 'cx-ring', { 'aria-hidden': 'true' }), h('span', 'cx-num'))

  const usage = ctl('usage', () => runCommand(footer, 'account-usage'))
  const bars = h('span', 'cx-bars', { 'aria-hidden': 'true' })
  for (let i = 0; i < 2; i++) {
    const bar = h('span', 'cx-bar')
    bar.append(h('i'))
    bars.append(bar)
  }
  usage.append(bars, h('span', 'cx-num'))

  const agents = ctl('agents', () => footerProps(footer)?.onOpenAgentMap?.())
  agents.append(h('span', 'cx-icon cx-icon-agents', { 'aria-hidden': 'true' }), h('span', 'cx-num'))

  // Right after "/", so keyboard order roughly follows what you see; the
  // visual order is set in custom.css.
  const slash = footer.querySelector(':scope > [class*="menuButton_"]')
  if (slash) slash.after(ctx, usage, agents)
  else footer.append(ctx, usage, agents)

  // Ultracode: fan-out icon + label; drives the mode menu's own switch.
  const uc = ctl('uc', () => {
    const mp = modeProps(footer)
    const on = footerProps(footer)?.session?.ultracodeActive?.value ?? mp?.ultracodeOn ?? false
    mp?.onSetUltracode?.(!on)
  })
  uc.setAttribute('aria-pressed', 'false')
  uc.setAttribute('title', UC_TITLE)
  uc.hidden = true
  const ucLabel = h('span', 'cx-label', { 'data-text': 'Ultracode' })
  ucLabel.textContent = 'Ultracode'
  uc.append(h('span', 'cx-icon cx-icon-fan', { 'aria-hidden': 'true' }), ucLabel)

  // Effort: "Effort" + a native range, one step per level the model offers.
  // The bubble over the thumb names the level on hover, focus or drag.
  const eff = h('label', 'cx-ctl cx-effort', { 'data-footer-overlay': '', title: 'Effort: set how hard the model tries' })
  eff.hidden = true
  const effLabel = h('span', 'cx-effort-label', { 'aria-hidden': 'true' })
  effLabel.textContent = 'Effort'
  const track = h('span', 'cx-track')
  const range = h('input', 'cx-range', { type: 'range', min: '0', max: '4', step: '1', value: '0', 'aria-label': 'Effort' })
  track.append(range)
  eff.append(effLabel, track)
  const pickedLevel = () => {
    const st = effortState(footer, footerProps(footer)?.session)
    return st ? { st, level: st.levels[Number(range.value)] } : null
  }
  range.addEventListener('input', () => {
    const p = pickedLevel() // preview while dragging; the panel is told on release
    if (p) paintEffort(eff, p.st.levels, Number(range.value), p.level)
  })
  range.addEventListener('change', () => {
    const p = pickedLevel()
    if (!p?.level) return
    try {
      p.st.set(p.level)
    } catch (err) {
      console.warn('[custom] effort', err)
    }
  })
  // bubble: on hover, keyboard focus, or while dragging
  let hover = false
  let dragging = false
  const bubbleNow = () => {
    let keyboard = false
    try {
      keyboard = range.matches(':focus-visible')
    } catch {}
    setAttr(eff, 'data-show', hover || dragging || keyboard ? '' : null)
    placeBubble(eff)
  }
  eff.addEventListener('pointerenter', () => {
    hover = true
    bubbleNow()
  })
  eff.addEventListener('pointerleave', () => {
    hover = false
    bubbleNow()
  })
  range.addEventListener('pointerdown', () => {
    dragging = true
    eff.setAttribute('data-dragging', '')
    bubbleNow()
  })
  const endDrag = () => {
    dragging = false
    eff.removeAttribute('data-dragging')
    bubbleNow()
    queueFooterRefresh()
  }
  range.addEventListener('pointerup', endDrag)
  range.addEventListener('pointercancel', endDrag)
  range.addEventListener('blur', endDrag)
  range.addEventListener('focus', bubbleNow)
  range.addEventListener('keyup', bubbleNow)

  // just before the mode button, so Tab follows what you see
  const modeHost = footer.querySelector(':scope > :has(> button[title*="Shift+Tab"])')
  if (modeHost) modeHost.before(uc, eff)
  else footer.append(uc, eff)
}

function refreshFooter() {
  const now = Date.now()
  for (const footer of document.querySelectorAll('fieldset[class*="inputContainer_"] [class*="inputFooterV2_"]')) {
    ensureControls(footer)
    const props = footerProps(footer)
    setAttr(footer, 'data-cx-ready', props ? '' : null)
    if (!props) continue

    // context
    const ctx = footer.querySelector(':scope > .cx-ctx')
    const pct = contextPct(props.session)
    if (ctx.style.getPropertyValue('--cx-p') !== String(pct ?? 0)) ctx.style.setProperty('--cx-p', String(pct ?? 0))
    setText(ctx.querySelector('.cx-num'), pct === null ? '–' : `${pct}%`)
    setAttr(ctx, 'aria-label', pct === null ? 'Context used: shows after the next reply. Compact…' : `Context ${pct}% used. Compact…`)
    setAttr(
      ctx,
      'title',
      pct === null
        ? 'Context used shows after the next reply\nClick to compact…'
        : `${pct}% of context used\n${100 - pct}% left before auto-compact\nClick to compact…`,
    )

    // usage
    const usage = footer.querySelector(':scope > .cx-usage')
    const W = FOOT.windows
    const s = windowPct(W?.five_hour, now)
    const w = windowPct(W?.seven_day, now)
    const [sBar, wBar] = usage.querySelectorAll('.cx-bar > i')
    if (sBar.style.width !== `${s ?? 0}%`) sBar.style.width = `${s ?? 0}%`
    if (wBar.style.width !== `${w ?? 0}%`) wBar.style.width = `${w ?? 0}%`
    setAttr(usage, 'data-level', s === null ? 'none' : s >= 95 ? 'crit' : s >= 80 ? 'warn' : 'ok')
    setText(usage.querySelector('.cx-num'), s === null ? '' : `${s}%`)
    const lines = []
    if (s !== null) lines.push(`Session (5hr) ${s}%${resetsIn(W.five_hour, now)}`)
    if (w !== null) lines.push(`Weekly (7 day) ${w}%${resetsIn(W.seven_day, now)}`)
    const extra = windowPct(W?.seven_day_overage_included, now)
    if (extra !== null) lines.push(`Model limit ${extra}%${resetsIn(W.seven_day_overage_included, now)}`)
    setAttr(usage, 'title', `${lines.length > 0 ? lines.join('\n') : 'Plan usage shows after the first reply'}\nClick for Account & usage`)
    setAttr(usage, 'aria-label', s === null ? 'Usage. Open Account and usage' : `Usage: session ${s}%${w !== null ? `, weekly ${w}%` : ''}. Open Account and usage`)

    // agents: working count + state, like the extension's own pill
    const agents = footer.querySelector(':scope > .cx-agents')
    const map = props.session?.agentMapAgents?.value
    const all = map && typeof map.values === 'function' ? [...map.values()] : []
    const asking = new Set()
    for (const r of props.session?.permissionRequests?.value ?? []) if (r?.agentId !== undefined) asking.add(r.agentId)
    const working = all.filter(x => x?.status === 'working')
    const state = working.some(x => asking.has(x.taskId))
      ? 'waiting'
      : working.length > 0
        ? 'running'
        : all.some(x => x?.status === 'failed')
          ? 'failed'
          : null
    setAttr(agents, 'hidden', typeof props.onOpenAgentMap === 'function' ? null : '')
    setAttr(agents, 'data-dot', state)
    setText(agents.querySelector('.cx-num'), String(working.length))
    const STATE = { waiting: 'An agent is waiting for your permission', running: 'Agents are working', failed: 'An agent failed' }
    const head = `${working.length} ${working.length === 1 ? 'agent' : 'agents'} working` + (all.length > working.length ? ` · ${all.length} in this chat` : '')
    setAttr(agents, 'title', `${head}${state ? `\n${STATE[state]}` : ''}\nClick to open the agent map`)
    setAttr(agents, 'aria-label', `${head}. Open the agent map`)

    // effort
    const session = props.session
    watchSession(session)
    const eff = footer.querySelector(':scope > .cx-effort')
    const est = effortState(footer, session)
    setAttr(eff, 'hidden', est ? null : '')
    if (est && !eff.hasAttribute('data-dragging')) paintEffort(eff, est.levels, est.index, est.level)

    // Ultracode: shown when the panel would show its own switch
    const uc = footer.querySelector(':scope > .cx-uc')
    const mp = modeProps(footer)
    const ucAvail = Boolean(est && (session?.ultracodeAvailable?.value ?? mp?.ultracodeAvailable) && typeof mp?.onSetUltracode === 'function')
    const ucOn = ucAvail && Boolean(session?.ultracodeActive?.value ?? mp?.ultracodeOn)
    setAttr(uc, 'hidden', ucAvail ? null : '')
    setAttr(uc, 'aria-pressed', ucOn ? 'true' : 'false')
    const box = footer.closest('fieldset')
    if (box) syncUltracode(box, footer, ucOn)

    // the compact set for this width (custom.css), from the width alone
    const fs = getComputedStyle(footer)
    const inner = footer.clientWidth - parseFloat(fs.paddingLeft) - parseFloat(fs.paddingRight)
    const tier = inner >= 656 ? 'full' : inner >= 501 ? 'compact' : inner >= 381 ? 'narrow' : 'tiny'
    if (inner > 0) setAttr(footer, 'data-cx-w', tier)

    remeasure(footer, [agents.hidden, eff.hidden, uc.hidden, ucOn, footer.getAttribute('data-cx-w')].map(String).join('|'))
    placeModelRow(footer)
    checkFooter(footer)
  }
}

// When the footer runs out of room (fit stage 2) the panel moves the model
// pill to a second row under it. Keep the box one line: lay that row over
// the gap in the footer (between the left and right groups); the pill
// truncates its label to fit.
function placeModelRow(footer) {
  const box = footer.closest('fieldset')
  const row = box?.querySelector(':scope > [class*="modelPillRow_"]')
  if (!row) return
  const b = box.getBoundingClientRect()
  const f = footer.getBoundingClientRect()
  const scale = box.offsetWidth ? b.width / box.offsetWidth : 1
  const fs = getComputedStyle(footer)
  let left = f.left + parseFloat(fs.paddingLeft) * scale
  let right = f.right - parseFloat(fs.paddingRight) * scale
  for (const c of footer.children) {
    if (c.matches('[class*="spacer_"]')) continue
    const cs = getComputedStyle(c)
    const r = c.getBoundingClientRect()
    if (cs.display === 'none' || r.width === 0) continue
    if (Number(cs.order) < 30) left = Math.max(left, r.right)
    else right = Math.min(right, r.left)
  }
  const px = v => `${Math.round(v)}px`
  const set = (k, v) => {
    if (row.style.getPropertyValue(k) !== v) row.style.setProperty(k, v)
  }
  set('--cx-row-left', px((left - b.left) / scale - box.clientLeft + 4))
  set('--cx-row-right', px((b.right - right) / scale - box.clientLeft + 2))
  set('--cx-row-top', px((f.top - b.top) / scale - box.clientTop + parseFloat(fs.paddingTop)))
  setAttr(row, 'data-cx-placed', '')
}

let footerQueued = false
function queueFooterRefresh() {
  if (footerQueued) return
  footerQueued = true
  requestAnimationFrame(() => {
    footerQueued = false
    try {
      refreshFooter()
    } catch (err) {
      console.warn('[custom] footer', err)
    }
  })
}

window.addEventListener('message', ev => {
  const d = ev.data
  if (d?.type !== 'from-extension') return
  const msg = d.message
  try {
    if (msg?.type === 'io_message') {
      const m = msg.message
      if (m?.type === 'rate_limit_event') mergeWindows(m.rate_limit_info?.unifiedWindows)
    } else if (msg?.type === 'request' && msg.request?.type === 'panel_usage_update') {
      mergeWindows(msg.request.unifiedWindows)
    }
  } catch (err) {
    console.warn('[custom] footer', err)
  }
  // after the panel's own listener has updated its state
  queueFooterRefresh()
})
// reset times and expiring windows move on their own
setInterval(queueFooterRefresh, 15_000)

let queued = false
new MutationObserver(records => {
  for (const r of records) {
    if (r.attributeName === 'data-fit-stage') {
      DIAG.stages.push(`${Math.round(performance.now())}:${r.target.getAttribute('data-fit-stage')}`)
      if (DIAG.stages.length > 40) DIAG.stages.shift()
    }
  }
  if (queued) return
  queued = true
  requestAnimationFrame(() => {
    queued = false
    mount()
    syncTalk()
    queueFooterRefresh()
  })
}).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['data-permission-mode', 'data-fit-stage'] })
mount()
queueFooterRefresh()
