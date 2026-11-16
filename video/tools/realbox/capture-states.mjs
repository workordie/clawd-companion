// Takes the real panel's DOM in every state the video shows, by doing what a user does (typing, Enter,
// clicking Clawd, hovering and dragging the effort slider, clicking Ultracode and the context ring) in the real
// extension + patch (realbox.mjs). Each state -> out/realbox/<panel>/<state>.json (the #root HTML, Clawd taken
// out, plus geometry) and a reference screenshot <state>.png (2x).
//
//   node tools/realbox/capture-states.mjs [--panel a-wide|a-tall|stage] [--theme light_modern]
import fs from 'node:fs'
import path from 'node:path'
import { extensionDir, pageHtml, serve, chrome, OUT } from './realbox.mjs'

const args = process.argv.slice(2)
const opt = (n, d) => (args.includes(`--${n}`) ? args[args.indexOf(`--${n}`) + 1] : d)
const theme = opt('theme', 'hc_light')

// the panel sizes the video's looks need (src/engine.js: the A window's chat column; B and A2 share one)
export const PANELS = {
  'a-wide': { width: 600, height: 453, mode: 'default', set: 'chat' }, // 16:9 A: 960x540 window with the editor
  'a-tall': { width: 540, height: 613, mode: 'default', set: 'chat' }, // 9:16 A: 540x700 window, the panel only
  // B (6x) and A2: box 680 on whole px, 84 px to the side, 16 below; tall, so its short chat stays far above the box
  stage: { width: 849, height: 700, mode: 'auto', set: 'footer' },
}
export const PROMPT = 'make the playground load faster'
export const QUESTION = 'is the render the slow part?'
export const ANSWER = 'Partly. The first paint waits on 199 SVG requests; inlining them fixes that.'
export const REPLY = "It fetched all 199 Clawd SVGs one by one before the first paint. They're inlined at build time now, so the playground draws on the first frame."

const AIM_INPUT = '[class*="messageInput_"][contenteditable]'
const ext = extensionDir()
const hostScript = fs.readFileSync(new URL('./host.js', import.meta.url), 'utf8')
const inpage = fs.readFileSync(new URL('./inpage.js', import.meta.url), 'utf8')
const setup = fs.readFileSync(new URL('./setup-screenshot.js', import.meta.url), 'utf8')
const newchat = fs.readFileSync(new URL('./setup-newchat.js', import.meta.url), 'utf8')

async function run(name) {
  const P = PANELS[name]
  const dir = path.join(OUT, name)
  fs.rmSync(dir, { recursive: true, force: true })
  fs.mkdirSync(dir, { recursive: true })
  const server = await serve(() => pageHtml({ ext, theme, hostScript }), ext)
  const profile = path.join(process.env.TMPDIR ?? '/tmp', 'realbox-profile')
  const c = await chrome({ width: P.width, height: P.height, dpr: 2, profile })
  const ev = c.evaluate
  const mouse = async (type, x, y, extra = {}) => c.send('Input.dispatchMouseEvent', { type, x, y, button: 'left', ...extra })
  const center = async sel => {
    const r = await ev(`RB.rect(${JSON.stringify(sel)})`)
    if (!r) throw new Error(`not found: ${sel}`)
    return [r.x + r.w / 2, r.y + r.h / 2]
  }
  const click = async sel => {
    const [x, y] = await center(sel)
    await mouse('mouseMoved', x, y, { button: 'none' })
    await mouse('mousePressed', x, y, { clickCount: 1 })
    await mouse('mouseReleased', x, y, { clickCount: 1 })
  }
  const away = () => mouse('mouseMoved', 4, 4, { button: 'none' })
  const key = async k => {
    const d = { Enter: { key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13, text: '\r' } }[k]
    await c.send('Input.dispatchKeyEvent', { type: 'keyDown', ...d })
    await c.send('Input.dispatchKeyEvent', { type: 'keyUp', ...d, text: undefined })
  }
  const done = []
  const shot = async (state, settle = 600) => {
    await c.sleep(settle)
    const snap = await ev('RB.snapshot()')
    snap.state = state
    snap.panel = { name, width: P.width, height: P.height, theme }
    fs.writeFileSync(path.join(dir, `${state}.json`), JSON.stringify(snap))
    await c.shot(null, path.join(dir, `${state}.png`))
    // the same without the patch's Clawd (the video draws him): what the snapshot must reproduce exactly
    await ev(`document.documentElement.classList.add('rb-noclawd')`)
    await c.sleep(50)
    await c.shot(null, path.join(dir, `${state}.ref.png`))
    await ev(`document.documentElement.classList.remove('rb-noclawd')`)
    done.push(state)
  }
  const setMode = m => ev(`RB.session().permissionMode.value = ${JSON.stringify(m)}`)
  try {
    await c.send('Page.navigate', { url: `http://127.0.0.1:${server.address().port}/` })
    for (let i = 0; i < 60 && !(await ev('!!document.querySelector("fieldset [class*=inputFooter_]")').catch(() => false)); i++) await c.sleep(150)
    await c.sleep(2500)
    await ev(inpage)
    // the opener's panels are a brand-new chat; B and the footer close-ups the user's own (resumed) chat
    await ev(P.set === 'chat' ? newchat : setup)
    await ev('RB.dismissNotices()')
    if (P.set === 'footer') {
      // B and the footer close-ups show a chat with history (the user's own footer is a resumed chat's: context
      // "–", cache cold): the prompt, Claude busy on it (B's busy box: Manual, the user's Extra high), his reply
      await setMode('default')
      await click(AIM_INPUT)
      await c.send('Input.insertText', { text: PROMPT })
      await key('Enter')
      await away()
      await shot('thinking', 1500)
      await ev(`HOST.reply(${JSON.stringify(REPLY)})`)
      await c.sleep(1500)
      await ev(setup)
      await ev(`document.activeElement?.blur?.(); RB.input().focus()`)
    }
    await setMode(P.mode)
    await away()
    await shot('idle', 1500)

    if (P.set === 'footer') {
      // the stage panel also shows Manual (B's scenes) and every mode the modes scene steps through
      for (const m of ['default', 'plan', 'acceptEdits', 'bypassPermissions', 'auto']) {
        await setMode(m)
        await shot(`mode-${m}`)
      }
      // effort: each level, without and with its bubble (hovering the slider shows it)
      for (const L of ['low', 'medium', 'high', 'xhigh', 'max']) {
        await ev(`RB.session().effortLevel.value = ${JSON.stringify(L)}`)
        await shot(`effort-${L}`, 500)
      }
      const [ex, ey] = await center('.cx-effort input')
      await mouse('mouseMoved', ex, ey, { button: 'none' })
      for (const L of ['low', 'medium', 'high', 'xhigh', 'max']) {
        await ev(`RB.session().effortLevel.value = ${JSON.stringify(L)}`)
        await shot(`effort-${L}-bubble`, 500)
      }
      // and pressed on the thumb (dragging)
      await mouse('mousePressed', ex, ey, { clickCount: 1 })
      await shot('effort-max-drag', 400)
      await mouse('mouseReleased', ex, ey, { clickCount: 1 })
      await ev(`RB.session().effortLevel.value = "max"`)
      await away()
      await shot('effort-max-after', 500)
      // Ultracode: click it; the wave's layers right away, then the edge that stays
      await click('.cx-uc')
      await shot('uc-on', 60)
      await away()
      await shot('uc-hold', 3600)
      // the context ring's compact confirm
      await click('.cx-ctx')
      await shot('confirm', 500)
      await click('.cx-pop .cx-btn-secondary, .cx-pop button:last-child').catch(async () => ev('document.querySelector(".cx-pop")?.remove()'))
      await away()
      // two subagents working
      const ok = await ev(`(() => { try {
        RB.session().agentMapAgents.value = new Map([['t1', { status: 'working', taskId: 't1' }], ['t2', { status: 'working', taskId: 't2' }]])
        return true } catch (e) { return String(e) } })()`)
      if (ok !== true) console.warn('agents:', ok)
      await shot('agents-2', 600)
      await ev(`RB.session().agentMapAgents.value = new Map()`)
      await ev(`(() => { const s = RB.session(); s.ultracodeEnabled.value = false })()`)
      await shot('uc-off', 800)
    }

    if (P.set === 'chat') {
      // the opener: typing the prompt, sending it (Claude is busy: the panel's own "thinking" state)
      await setMode(P.mode)
      await click(AIM_INPUT)
      await c.send('Input.insertText', { text: PROMPT })
      await away()
      await shot('typed', 600)
      await key('Enter')
      await shot('thinking', 1500)
      // his /btw bubble: click him (custom.js opens the extension's side question), ask, the answer comes later
      await ev(`HOST.answers.side_question = (r, msg) => { HOST.sidePending = msg.requestId; return undefined }`)
      await click('.cx-clawd-hit')
      await c.sleep(1200)
      await away()
      await shot('talk-open', 600)
      await click('textarea[aria-label="Ask a side question"]')
      await c.send('Input.insertText', { text: QUESTION })
      await away()
      await shot('talk-typed', 500)
      await click('textarea[aria-label="Ask a side question"]')
      await key('Enter')
      await away()
      await shot('talk-pending', 800)
      await ev(`HOST.respond(HOST.sidePending, { type: 'side_question_response', response: ${JSON.stringify(ANSWER)}, synthetic: false })`)
      await shot('talk-answer', 1200)
    }
    const log = c.log.filter(l => /^(EXC|error)/.test(l))
    console.log(`${name}: ${done.length} states -> ${dir}${log.length ? `\n  console errors:\n  ${log.slice(0, 8).join('\n  ').slice(0, 2000)}` : ''}`)
    console.log('  ' + done.join(' '))
  } finally {
    c.close()
    server.close()
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  for (const name of opt('panel') ? [opt('panel')] : Object.keys(PANELS)) await run(name)
}
