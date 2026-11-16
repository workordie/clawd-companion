'use strict'
/*
 * The two cuts, on the soundtrack's beat grid ("Technology" by Sub_Clair: 125 BPM, beat 0.48 s, bar 1.92 s; bar(k) = bar
 * k's downbeat in video time, bar(k, b) beat b of it). Its 8-bar phrases: intro 0-7, build 8-15, DROP 1 bar 16,
 * breakdown 24-39 (drums out from 24, bass down from 32), lift 40-47, DROP 2 bar 48, outro 56-63, end 64.
 * Captions switch with their scene's first clip (its set-up) or the scene start, whichever is first.
 * STORYBOARD.md is the readable version; keep the two in step.
 *
 * Both cuts mix the two looks (capture with --style mix): they open in A, the real VS Code panel, punch in on the
 * beats (2x, 4x, 6x: hard cuts, whole-number zooms) and land on B, the stage, on the main drop; the body plays on
 * B; they come back to A (4x) for his /btw speech bubble and the input footer's modes; the finale is on B.
 *
 * scene(t0, {...}) holds from t0 on:
 *   look      'A' (the VS Code window), 'A2' (the same panel with the box at its full 680 px: the footer's full set) or
 *             'B' (the stage)
 *   A only    zoom 2 | 4 | 6, at [X, Y] (a world point, cells), anchor [fx, fy] (where it goes, fractions of the
 *             view) or place [px, py] (exact view px); ui: the chat (new | typing | thinking | working | alert |
 *             question | done | error | talk | idle); capPos 'bl' | 'tl' | 'tr' | [left, top] (16:9)
 *   B only    cam 'home' | 'edge' | 'side' | [X, Y]; anchorWide / anchorTall [fx, fy]
 *   both      mode (manual | plan | edits | auto | bypass), ring (the mode ring lit), typing (text typed into the
 *             box from t0), talk (lt => his bubble or null), wall, end
 * cap(t, text, sub)   a caption from t on ('' clears it). Every caption says only what the patch really does.
 * flash(t)            a drop: B flashes and shakes
 */

const ASK = {
  q: 'is the render the slow part?',
  a: 'Partly. The first paint waits on 199 SVG requests; inlining them fixes that.',
}
/** His bubble: closed until openAt, the question typed until sendAt, "Answering…" until answerAt, the answer until closeAt. */
const talkAt = (openAt, sendAt, answerAt, closeAt = Infinity) => lt =>
  lt < openAt || lt >= closeAt
    ? null
    : lt < sendAt
      ? { ...ASK, typed: (lt - openAt) / (sendAt - openAt), state: 'listen' }
      : lt < answerAt
        ? { ...ASK, state: 'think' }
        : { ...ASK, state: 'answer' }

const VARIANTS = ['thinking-chalk', 'working-chef', 'idle-kite', 'thinking-cube', 'working-lab', 'idle-garden', 'thinking-stars',
  'working-knit', 'idle-game', 'thinking-pace', 'working-paint', 'idle-bird', 'thinking-cairn', 'working-mail', 'idle-bubbles', 'working']
const WALL = ['idle', 'typing', 'thinking', 'working', 'subagents', 'compacting', 'hooks', 'question', 'alert', 'done', 'done-party', 'error',
  'rate-limit', 'sleep', 'manual', 'plan', 'edits', 'auto', 'bypass', 'hello', 'vibe', 'idle-moods', 'idle-pet', 'idle-bubbles', 'idle-kite',
  'idle-garden', 'idle-game', 'idle-bird', 'typing-juggle', 'typing-drums', 'thinking-chalk', 'thinking-cube', 'thinking-stars',
  'thinking-gears', 'thinking-pace', 'thinking-cairn', 'working-chef', 'working-forge', 'working-lab', 'working-knit', 'working-paint',
  'working-mail', 'question-lens', 'question-scroll', 'alert-bell', 'alert-flags', 'done-bell', 'done-flag', 'sleep-hammock', 'sleep-camp',
  'manual-drive', 'manual-craft', 'auto-robot', 'auto-cloud', 'hello-peek', 'hello-hat', 'sit-edge-right', 'click-party', 'click-idea']
const MODES = [['plan', 'plan'], ['edits', 'edits'], ['bypass', 'bypass'], ['auto-cloud', 'auto']]

/** Drags him from home: hover, press, lift and move along `path` ([dt, X, Y] from t), playing `clips`. */
function grabAt(a, m, t, path, clips) {
  m.key(t - 0.35, HOME + 0.5, -5.5, 'hand').key(t, HOME + 0.5, -5.5, 'grab', 'step')
  let tt = t
  for (const [dt, X, Y] of path) m.key((tt += dt), X, Y, 'grab')
  a.at(t)
  for (const [dur, clip] of clips) a.drag(m, dur, clip)
}

/** Grab, shake, throw (one bar each from t), as custom.js's drag code would see the cursor. */
function playRough(cut, a, m, t, scene, cap) {
  const { bar } = cut
  const B = MUSIC.bar
  scene(t, { id: 'grab', look: 'B', cam: [HOME + 2, -9], mode: 'manual' })
  a.at(t).to(HOME, 0)
  grabAt(a, m, t, [[0.7, HOME - 4, -14], [0.9, HOME - 2, -13]], [[B, 'grabbed']])
  cap(t, 'grab Clawd.')
  for (let i = 0; i < 14; i++) m.key(t + B + 0.1 + i * 0.1, HOME - 2 + (i % 2 ? -5 : 5), -13 + (i % 3) - 1, 'grab', 'io')
  a.drag(m, B, 'grabbed-dizzy')
  cap(t + B, 'shake Clawd.')
  const th = t + 2 * B
  scene(th, { id: 'throw', look: 'B', cam: [0, 5], anchorTall: [0.42, 0.55], mode: 'manual' })
  m.key(th, HOME - 2, -13, 'grab').key(th + 0.02, HOME - 1.5, -13, 'grab').key(th + 0.22, HOME + 14, -15, 'grab', 'lin')
  m.key(th + 0.221, HOME + 14, -15, 'grab').key(th + 0.32, HOME + 16, -16, 'arrow').key(th + 0.33, HOME + 16, -16, 'none', 'step')
  a.drag(m, 0.22, 'grabbed').release(m)
  cap(th, 'throw Clawd.')
  void bar
}

/** Lifted high and let go (the chute opens), then a click under the chute pops it (one bar each from t). */
function playChute(cut, a, m, t, scene, cap) {
  const B = MUSIC.bar
  scene(t, { id: 'chute', look: 'B', cam: [HOME + 2, -14], mode: 'manual' })
  a.at(t - 0.01).to(HOME, 0).play('idle', 0.01)
  m.key(t - 0.36, HOME + 12, -12, 'arrow')
  grabAt(a, m, t, [[0.55, HOME, -34], [0.45, HOME, -34]], [[1.0, 'grabbed']])
  a.chuteCut = { cutAt: B + 0.2 - 1.0 }
  m.key(t + 1.0, HOME, -34, 'grab').key(t + 1.01, HOME, -34, 'arrow', 'step').key(t + 1.4, HOME + 9, -30, 'arrow')
  a.release(m)
  m.key(t + B + 0.05, HOME + 1, -21, 'hand').click(t + B + 0.2).key(t + B + 0.6, HOME + 6, -26, 'arrow').key(t + B + 0.61, HOME + 6, -26, 'none', 'step')
  cap(t - 0.01, 'drop Clawd\nfrom up high.')
  cap(t + B, 'pop the chute. (sorry)')
}

/** Back in the real panel at 4x: click him, the /btw side question opens as his bubble, the answer lands on `answer`. */
function talkScene(cut, a, m, t, open, send, answer, close, A, scene, cap) {
  scene(t, { id: 'talk', look: 'A', zoom: 3, at: [HOME, 0], ...A, ui: 'talk', mode: 'manual', talk: talkAt(open - t, send - t, answer - t, close - t) })
  a.at(t).to(HOME, 0).until(open, 'idle').until(send, 'talk-listen').until(answer, 'talk-think')
  a.play('talk-explain', Math.min(cycle('talk-explain'), close - answer)).until(close, 'talk-listen')
  m.key(t - 0.01, HOME + 22, -8, 'none').key(t, HOME + 22, -8, 'arrow', 'step').key(open - 0.05, HOME + 0.5, -5, 'hand').click(open)
  m.key(open + 0.35, HOME + 0.5, -5, 'hand').key(open + 0.6, HOME + 14, 4, 'arrow').key(open + 0.61, HOME + 14, 4, 'none', 'step')
  cap(t, 'click Clawd:\nask a side question.')
  cap(answer, 'Claude answers,\nin Clawd’s bubble.', 'it’s the extension’s\n/btw side question')
}

/** The input footer at 4x: switch modes (Shift+Tab), he switches jobs; the box's ring follows. `beats` each. */
function modesScene(a, t, A, scene, cap, beats = 2) {
  MODES.forEach(([clip, mode], i) => {
    const t0 = t + i * beats * MUSIC.beat
    scene(t0, { id: `mode-${mode}`, look: 'A2', zoom: 4, at: [HOME + 2, 3], ...A, ui: 'idle', mode, ring: true })
    a.at(t0).to(HOME, 0).play(clip, beats * MUSIC.beat)
  })
  cap(t, 'switch modes,\nClawd switches jobs.', 'plan · edits · bypass · auto')
}

/** Props drop in and poof away: a scene change per bar from t, each set up (in-*) to land on its downbeat. */
function transitionsScene(cut, a, t, bars, scene, cap, anchorTall) {
  const B = MUSIC.bar
  scene(t, { id: 'transitions', look: 'B', cam: 'home', anchorTall, mode: 'manual' })
  a.at(t).to(HOME, 0).play('working-chef', 0.3)
  const chain = ['working-chef', 'working-lab', 'thinking-cube', 'done-flag']
  for (let i = 1; i < bars; i++) a.swap(chain[i - 1], chain[i], t + i * B)
  a.until(t + bars * B, chain[bars - 1])
  cap(t, 'props drop in\nand poof away.')
}

// ======================================== The input footer =================================================
// Its own features, in A2 at 4x, on the beat: the effort slider (3 bars), Ultracode (2 bars), the context ring's
// compact confirm + the agents counter (2 bars). The functions get the scene's own time and return the footer's state.

const BT = MUSIC.beat

/** Where the pointer is between keyframes [[t, target], ...]: the two targets and the eased mix. */
function ptrAt(keys, lt) {
  if (lt <= keys[0][0]) return { a: keys[0][1], b: null, k: 0 }
  for (let i = 1; i < keys.length; i++) {
    if (lt < keys[i][0]) {
      const [t0, a] = keys[i - 1]
      const [t1, b] = keys[i]
      const u = (lt - t0) / (t1 - t0)
      return { a, b, k: u < 0.5 ? 2 * u * u : 1 - 2 * (1 - u) * (1 - u) }
    }
  }
  return { a: keys[keys.length - 1][1], b: null, k: 0 }
}

/** Effort, 12 beats: onto the thumb (beat 1: "Medium"), press, then a level per beat: Low, Medium, High, Extra high,
 *  Max (beat 6, its note), release (9.5), away (10.5). Each move's midpoint is on its beat, so the level flips on it. */
function effortFooter(lt) {
  const R = (u, dx, dy) => ({ el: 'range', u, dx, dy })
  const at = b => b * BT
  const step = (b, u0, u1) => [[at(b) - 0.06, R(u0)], [at(b) + 0.06, R(u1)]]
  const P = [[0, R(0.25, 70, 46)], [at(1), R(0.25)], ...step(2, 0.25, 0), ...step(3, 0, 0.25), ...step(4, 0.25, 0.5), ...step(5, 0.5, 0.75),
    ...step(6, 0.75, 1), [at(9.5), R(1)], [at(10.5), R(1, 50, 46)]]
  const p = ptrAt(P, lt)
  const drag = lt >= at(1.5) && lt < at(9.5)
  const hover = lt >= at(1) - 0.05 && lt < at(10)
  const u = p.b && p.b.el === 'range' && !p.b.dx ? p.a.u + (p.b.u - p.a.u) * p.k : p.a.u
  const effort = drag ? Math.round(u * 4) : lt < at(1.5) ? 1 : 4
  return { effort, hover, drag, bubble: hover ? at(1) - 0.05 : 0, ptr: { ...p, kind: hover ? 'point' : 'arrow' } }
}

/** Ultracode, 8 beats: onto the button, click on beat 2 (the pop, the dot wave, then the edge and its glint), away. */
function ucFooter(lt) {
  const P = [[0, { el: 'uc', dx: -70, dy: 44 }], [BT * 1.4, { el: 'uc' }], [BT * 2.6, { el: 'uc' }], [BT * 3.6, { el: 'uc', dx: 46, dy: 52 }]]
  const p = ptrAt(P, lt)
  const on = lt >= BT * 1.3 && lt < BT * 2.8
  return { effort: 4, ucAt: BT * 2, ptrOn: on ? 'uc' : null, ptr: { ...p, kind: on ? 'point' : 'arrow' } }
}

/** The context ring, 8 beats: click on beat 2 (the "Compact this chat?" confirm), Cancel on beat 4; then two subagents
 *  start on beat 6: the counter and its pulsing dot. Ultracode stays on. */
function tourFooter(lt) {
  const P = [[0, { el: 'ctx', dx: 64, dy: 46 }], [BT * 1.4, { el: 'ctx' }], [BT * 2.4, { el: 'ctx' }], [BT * 3.5, { el: 'cancel' }],
    [BT * 4.4, { el: 'cancel' }], [BT * 5.4, { el: 'agents', dx: 34, dy: 44 }]]
  const p = ptrAt(P, lt)
  const onCtx = lt >= BT * 1.3 && lt < BT * 2.6
  const onCancel = lt >= BT * 3.4 && lt < BT * 4.6
  return {
    effort: 4, ucAt: -10, confirm: [BT * 2, BT * 4], ptrOn: onCtx ? 'ctx' : onCancel ? 'cancel' : null,
    agents: lt >= BT * 6 ? { n: 2, dot: 'running', at: BT * 6 } : { n: 0 },
    ptr: { ...p, kind: onCtx || onCancel ? 'point' : 'arrow' },
  }
}

/** The footer segment from t (A2, 4x, Auto mode): effort, Ultracode and (opts.tour) the ring's confirm. Returns its end. */
function footerScenes(cut, a, t, A, scene, cap, opts = {}) {
  const B = MUSIC.bar
  const base = { look: 'A2', zoom: 4, ui: 'idle', mode: 'auto' }
  scene(t, { id: 'effort', ...base, focus: 'effort', anchor: A.effort, footer: effortFooter })
  cap(t, 'drag the effort slider.', 'low · medium · high · extra high · max')
  const tu = t + 3 * B
  scene(tu, { id: 'ultracode', ...base, focus: 'uc', anchor: A.uc, footer: ucFooter })
  cap(tu, 'turn on Ultracode.', 'dynamic workflows on every task\n(this session only)')
  let end = tu + 2 * B
  if (opts.tour) {
    scene(end, { id: 'tour', ...base, focus: 'ctx', anchor: A.ctx, footer: tourFooter })
    cap(end, 'click the context ring\nto compact.')
    cap(end + 6 * BT, 'usage and subagents,\nat a glance.')
    end += 2 * B
  }
  a.at(t).to(HOME, 0).play('idle', end - t)
  return end
}

const TRACK_END = 125.328 // the track's length (its last hit is bar 64, then a short tail)

// ======================================== 16:9, 109 s ======================================================
// From bar 8 of the track (16.326 s): the build's 8 bars for the VS Code opener (its bass cuts on bars 14-15 for the
// punch-ins), DROP 1 on the stage at 15.36 s, and on to the track's own ending.

makeCut('wide', { aspect: '16x9', audioStart: MUSIC.bar0 + 8 * MUSIC.bar, fade: 0.3 }, cut => {
  const { bar, track: a, cursor: m } = cut
  const scene = (t0, o) => cut.scenes.push({ t0, ...o })
  const cap = (t, text, sub) => cut.captions.push([t, text, sub])
  const flash = t => cut.flashes.push(t)
  cut.end = +(TRACK_END - cut.audioStart).toFixed(3)

  // ---- A: the real panel ----
  // Panel opened: he peeks up from behind the box. Bars 8-9
  scene(0, { id: 'hello', look: 'A', zoom: 2, ui: 'new', mode: 'manual' })
  a.at(0).play('hello-peek', bar(10))
  cap(0, 'meet Clawd.', 'Claude Code’s mascot,\non your input box')
  // A prompt typed into the real box. Bars 10-11
  scene(bar(10), { id: 'typing', look: 'A', zoom: 2, ui: 'new', mode: 'manual', ring: true, typing: PROMPT, cps: 18 })
  a.play('in-typing-juggle')
  cap(bar(10), 'you type,\nClawd juggles\nthe letters.')
  // Sent: Claude thinks (set up to land on bar 12). Bars 12-13
  const sent = bar(12) - cycle('in-thinking-gears') - cycle('out-typing-juggle')
  a.until(sent, 'typing-juggle').play('out-typing-juggle').play('in-thinking-gears')
  scene(sent, { id: 'thinking', look: 'A', zoom: 2, ui: 'thinking', mode: 'manual' })
  cap(sent, 'Claude thinks.\nso does Clawd.')
  // The build's bass cuts: punch in on the downbeats, 4x then 6x; the gears pack away, the forge drops in for the drop.
  scene(bar(14), { id: 'punch-4x', look: 'A', zoom: 4, at: [HOME + 4, -10], anchor: [0.5, 0.5], ui: 'thinking', mode: 'manual' })
  scene(bar(15), { id: 'punch-6x', look: 'A', zoom: 6, at: [HOME, 0], place: [1057, 616], ui: 'thinking', mode: 'manual' })
  a.swap('thinking-gears', 'working-forge', bar(16))

  // ---- B: the stage (the 6x shot cuts to it with Clawd on the same pixels) ----
  // DROP 1: what Claude does, a state every 2 bars, each packed away and the next set up. Bars 16-23
  scene(bar(16), { id: 'states', look: 'B', cam: 'home', mode: 'manual' })
  flash(bar(16))
  cap(bar(16) - cycle('in-working-forge'), 'Claude works.\nso does Clawd.')
  a.swap('working-forge', 'alert-bell', bar(18))
  cap(bar(18) - cycle('in-alert-bell'), 'needs your OK?\nClawd rings.')
  a.swap('alert-bell', 'question-lens', bar(20))
  cap(bar(20) - cycle('in-question-lens'), 'a question for you?\nClawd waits.')
  a.swap('question-lens', 'done', bar(22)).until(bar(24), 'done')
  cap(bar(22) - cycle('in-done'), 'done? party.')
  // The breakdown (drums out): he wanders to the edge, teeters, hops off on bar 25 beat 4. Bars 24-25
  const takeoff = bar(25, 3)
  const teeter = takeoff - 0.15 - cycle('teeter-right')
  a.at(bar(24)).to(EDGE - (teeter - bar(24)) * WALK, 0).walkTo(EDGE).play('teeter-right')
  scene(bar(24), { id: 'wander', look: 'B', cam: 'edge', mode: 'manual' })
  cap(bar(24), 'nothing to do?\nClawd wanders off.')
  cap(bar(25), 'uh oh.')
  scene(takeoff, { id: 'hop', look: 'B', cam: 'side', mode: 'manual' })
  a.hopOff('R')
  cap(takeoff - 0.15, 'Clawd hops off.')
  // A look up, over to the wall, up it like a crab; over the top on bar 32 (the bass drops). Bars 26-31
  const climbAt = bar(32) - (WORLD.F - 8) / CLIMB
  const walkAt = climbAt - Math.abs(BODY_HALF - a.X) / WALK
  a.until(walkAt - cycle('look-up-left'), 'idle').play('look-up-left').walkTo(BODY_HALF).climbUp()
  cap(walkAt, '…and walks back\nup the wall.')
  cap(climbAt, 'like a crab.')
  scene(bar(32), { id: 'over', look: 'B', cam: 'edge', mode: 'manual' })
  a.walkTo(HOME)
  cap(bar(32), 'home again.')
  // Every state has versions: one a beat. Bars 33-35
  scene(bar(33), { id: 'versions', look: 'B', cam: 'home', mode: 'manual' })
  VARIANTS.slice(0, 12).forEach((clip, i) => a.at(bar(33) + i * BT).to(HOME, 0).play(clip, BT))
  cap(bar(33), 'every state has versions.')
  // Set-up and pack-away: a scene a bar. Bars 36-39
  transitionsScene(cut, a, bar(36), 4, scene, cap)
  // The lift: playing with him. Bars 40-45
  scene(bar(40), { id: 'notice', look: 'B', cam: 'home', mode: 'manual' })
  a.at(bar(40)).to(HOME, 0).play('idle', 0.45).play('notice')
  m.key(bar(40) - 0.01, HOME + 26, -16, 'none').key(bar(40), HOME + 26, -16, 'arrow', 'step').key(bar(40) + 0.45, HOME + 0.5, -5.5, 'hand', 'out')
  cap(bar(40), 'hover over Clawd:\nClawd notices you.')
  playRough(cut, a, m, bar(41), scene, cap)
  flash(bar(43))
  playChute(cut, a, m, bar(44), scene, cap)

  // ---- A: the real panel at 4x: his bubble; "Answering…" through the bass cuts, the answer on DROP 2. Bars 46-48 ----
  // 2x: the whole window: the real bubble and Clawd in the panel, the caption on the editor
  talkScene(cut, a, m, bar(46), bar(46, 2), bar(47), bar(48), bar(49), { zoom: 2 }, scene, cap)
  // ---- A2: the input footer: modes, effort, Ultracode, the ring's confirm. Bars 49-57 ----
  modesScene(a, bar(49), { anchor: [0.62, 0.55] }, scene, cap)
  const fEnd = footerScenes(cut, a, bar(51), { effort: [0.5, 0.62], uc: [0.45, 0.62], ctx: [0.3, 0.66] }, scene, cap, { tour: true })

  // ---- B: the outro ----
  // All of them. Bars 58-59
  scene(fEnd, { id: 'wall', look: 'B', wall: { t0: fEnd, clips: WALL, label: '199 pixel-art animations.' } })
  cap(fEnd, '')
  a.at(fEnd).to(HOME, 0).until(bar(60) - cycle('in-sleep-camp'), 'idle').play('in-sleep-camp')
  // Nap time. Bars 60-61
  scene(bar(60), { id: 'sleep', look: 'B', cam: 'home', mode: 'manual' })
  a.until(bar(62), 'sleep-camp')
  cap(bar(60) - cycle('in-sleep-camp'), 'away a while?\nnap time.')
  // The end card, to the track's own ending. Bar 62-
  scene(bar(62), { id: 'end', look: 'B', end: { t0: bar(62), clip: 'hello-hat', then: 'idle' } })
  cap(bar(62), '')
})

// ======================================== 9:16, 48 s =======================================================
// From bar 15 of the track (29.766 s), the last bar of the build: DROP 1 at 1.92 s; it ends as the breakdown's calm
// bar 39 fades out (bar 40 = 48.0 s).

makeCut('tall', { aspect: '9x16', audioStart: MUSIC.bar0 + 15 * MUSIC.bar, fade: MUSIC.bar }, cut => {
  const { bar, track: a, cursor: m } = cut
  const scene = (t0, o) => cut.scenes.push({ t0, ...o })
  const cap = (t, text, sub) => cut.captions.push([t, text, sub])
  const flash = t => cut.flashes.push(t)
  cut.end = bar(40)
  const HOME_TALL = [0.5, 0.621875] // B's home framing in 9:16: Clawd on the same pixels as A's 6x shot

  // ---- A: the real panel, one bar: 2x, 4x on beat 3, 6x on beat 4 (the build's bass cuts) ----
  scene(0, { id: 'panel', look: 'A', zoom: 2, ui: 'thinking', mode: 'manual' })
  scene(bar(15, 2), { id: 'punch-4x', look: 'A', zoom: 4, at: [HOME + 3, -8], anchor: [0.5, 0.55], ui: 'thinking', mode: 'manual' })
  scene(bar(15, 3), { id: 'punch-6x', look: 'A', zoom: 6, at: [HOME, 0], place: [522, 728], ui: 'thinking', mode: 'manual' })
  cap(0, 'Clawd lives on your\ninput box now.', 'Claude Code · VS Code')

  // ---- B: DROP 1 (match cut); the gears pack away and the forge drops in on beat 4, then a state a bar ----
  const forge = bar(16, 3)
  const tIn = forge - cycle('in-working-forge')
  const tOut = tIn - cycle('out-thinking-gears')
  a.at(0).play('thinking-gears', tOut, { ct0: 2 }).play('out-thinking-gears').play('in-working-forge')
  scene(bar(16), { id: 'states', look: 'B', cam: 'home', anchorTall: HOME_TALL, mode: 'manual' })
  flash(bar(16))
  cap(tIn, 'Claude works.\nso does Clawd.')
  a.play('working-forge', bar(18) - forge).play('alert-bell', MUSIC.bar).play('done', MUSIC.bar)
  cap(bar(18), 'needs your OK?\nClawd rings.')
  cap(bar(19), 'done? party.')
  // Nothing to do: to the edge, a teeter, off on bar 21 beat 3. Bars 20-22
  const takeoff = bar(21, 2)
  const teeter = takeoff - 0.15 - cycle('teeter-right')
  a.at(bar(20)).to(EDGE - (teeter - bar(20)) * WALK, 0).walkTo(EDGE).play('teeter-right')
  scene(bar(20), { id: 'wander', look: 'B', cam: 'edge', mode: 'manual' })
  cap(bar(20), 'nothing to do?\nClawd wanders off.')
  cap(bar(21), 'uh oh.')
  scene(takeoff, { id: 'hop', look: 'B', cam: 'side', anchorTall: [0.42, 0.55], mode: 'manual' })
  a.hopOff('R')
  cap(takeoff - 0.15, 'Clawd hops off.')
  // Jump cut (reframed) to the wall: up it like a crab, over the top on bar 24 beat 3. Bars 23-24
  const top = bar(24, 2)
  const climbFrom = bar(23)
  scene(climbFrom, { id: 'climb', look: 'B', cam: [4, 14], anchorTall: [0.36, 0.5], mode: 'manual' })
  a.at(climbFrom).to(BODY_HALF, 8 + (top - climbFrom) * CLIMB).climbUp()
  cap(climbFrom, '…and walks up\nthe wall,\nlike a crab.') // three lines: clear of the panel's edge in this shot
  scene(top, { id: 'over', look: 'B', cam: 'edge', mode: 'manual' })
  a.walkTo(HOME)
  // Grab, shake, throw. Bars 25-27
  playRough(cut, a, m, bar(25), scene, cap)
  flash(bar(27))

  // ---- A: his bubble, the answer on bar 29 ----
  // 2x: the panel fills the view's width, the real bubble (382 px) fits over Clawd and the box under him
  talkScene(cut, a, m, bar(28), bar(28, 1), bar(28, 3), bar(29), bar(30), { zoom: 2, place: [800, 1180] }, scene, cap)
  // ---- A2: modes (a beat each), effort, Ultracode. Bars 30-35 ----
  modesScene(a, bar(30), { anchor: [0.55, 0.45] }, scene, cap, 1)
  const fEnd = footerScenes(cut, a, bar(31), { effort: [0.42, 0.62], uc: [0.7, 0.62], ctx: [0.115, 0.66] }, scene, cap)

  // ---- B: all of them, the end card (the fade runs over bar 39) ----
  scene(fEnd, { id: 'wall', look: 'B', wall: { t0: fEnd, clips: WALL, label: '199 pixel-art\nanimations.' } })
  cap(fEnd, '')
  scene(bar(38), { id: 'end', look: 'B', end: { t0: bar(38), clip: 'hello-hat', then: 'idle' } })
  a.at(fEnd).to(HOME, 0).play('idle', bar(40) - fEnd)
  cap(bar(38), '')
})

// ======================================== Footer close-ups (for review) =========================================
// The footer segment on its own, in A (the full footer), as rendered for review into out/footer/.

function footerCut(id, aspect, A) {
  makeCut(id, { aspect, audioStart: 0, footerLayout: true }, cut => {
    const scene = (t0, o) => cut.scenes.push({ t0, ...o.look === 'A2' ? { ...o, look: 'A' } : o })
    const cap = (t, text, sub) => cut.captions.push([t, text, sub])
    cut.end = footerScenes(cut, cut.track, 0, A, scene, cap, { tour: true })
  })
}
footerCut('footer-wide', '16x9', { effort: [0.5, 0.62], uc: [0.45, 0.62], ctx: [0.3, 0.66] })
footerCut('footer-tall', '9x16', { effort: [0.42, 0.62], uc: [0.7, 0.62], ctx: [0.115, 0.66] }) // the confirm (260 px) fits the 270 px view
