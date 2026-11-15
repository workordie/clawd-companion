// Builds playground/index.html: the real custom.js + custom.css on a mock of the chat panel, with buttons that
// fake what Claude is doing, so Clawd can be tried without reloading VS Code. Open the file in a browser.
//   npm run playground
// The /btw side question is mocked too: it answers with a canned line after 1.5 s.
import fs from 'node:fs'
import path from 'node:path'

import { ROOT, animationFiles, cycleMs } from './lib.mjs'

const out = path.join(ROOT, 'playground')
const clawdDir = path.join(out, 'clawd')
fs.rmSync(clawdDir, { recursive: true, force: true })
fs.mkdirSync(clawdDir, { recursive: true })

const cycles = {}
for (const { name, file } of animationFiles()) {
  fs.copyFileSync(file, path.join(clawdDir, path.basename(file)))
  cycles[name] = cycleMs(fs.readFileSync(file, 'utf8'))
}
const css = fs.readFileSync(path.join(ROOT, 'custom', 'custom.css'), 'utf8')
const js = fs.readFileSync(path.join(ROOT, 'custom', 'custom.js'), 'utf8')

const page = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clawd playground</title>
<style>
  :root {
    --app-primary-background: #1e1e1e; --app-primary-foreground: #cccccc; --app-widget-border: #3c3c3c;
    --app-input-border: #3c3c3c; --app-input-background: #252526; --app-input-foreground: #dddddd;
    --app-spinner-foreground: #d97757; --app-claude-orange: #d97757; --app-claude-clay-button-orange: #d97757;
    --app-spacing-medium: 8px; --app-spacing-large: 12px; --corner-radius-large: 8px; --corner-radius-medium: 6px;
    --app-monospace-font-size: 12px; --app-monospace-font-family: ui-monospace, monospace;
  }
  html.light {
    --app-primary-background: #ffffff; --app-primary-foreground: #333333; --app-widget-border: #d4d4d4;
    --app-input-border: #cecece; --app-input-background: #f7f7f7; --app-input-foreground: #222222;
  }
  html, body { margin: 0; height: 100%; background: var(--app-primary-background); color: var(--app-primary-foreground);
    font: 13px/1.5 -apple-system, system-ui, sans-serif; }
  #bar { position: fixed; top: 0; left: 0; right: 0; z-index: 100; display: flex; flex-wrap: wrap; gap: 6px; align-items: center;
    padding: 8px 12px; background: #2b2b2b; border-bottom: 1px solid #444; color: #ddd; }
  html.light #bar { background: #ececec; border-color: #ccc; color: #222; }
  #bar b { margin-right: 4px; }
  #bar button { font: inherit; font-size: 12px; color: inherit; background: transparent; border: 1px solid #666; border-radius: 6px; padding: 3px 8px; cursor: pointer; }
  #bar button:hover { border-color: #d97757; }
  #bar .sep { width: 1px; height: 18px; background: #555; margin: 0 4px; }
  #now { margin-left: auto; font: 12px ui-monospace, monospace; opacity: .8; }
  #root { position: fixed; top: 44px; bottom: 0; left: 0; right: 0; display: flex; }
  #frame { display: flex; flex: 1; min-width: 0; margin: 0 auto; max-width: var(--panel, 100%); border-left: 1px dashed #444; border-right: 1px dashed #444; }
  /* the extension's own layout, copied */
  .chatContainer_07S1Yg { display: flex; overflow: hidden; position: relative; flex-direction: column; flex: 1; min-width: 0; line-height: 1.5 }
  .messagesContainer_07S1Yg { overflow-y: auto; display: flex; flex-direction: column; flex: 1; min-width: 0; padding: 20px 20px 140px }
  .inputContainer_07S1Yg { position: absolute; display: flex; z-index: 20; flex-direction: column; max-width: 680px; margin: 0 auto; bottom: 16px; left: 16px; right: 16px }
  .inputContainer_cKsPxg { position: relative; margin: 0; padding: 0; border: 1px solid var(--app-input-border); border-radius: 8px; background: var(--app-input-background); min-inline-size: 0 }
  .messageInput_cKsPxg { outline: none; min-height: 36px; max-height: 160px; overflow-y: auto; padding: 8px 10px; white-space: pre-wrap; color: var(--app-input-foreground) }
  .messageInput_cKsPxg:empty::before { content: 'Type here (Clawd watches); /btw opens his bubble'; opacity: .45 }
  .footer_mock { height: 32px; border-top: 1px solid var(--app-widget-border); font-size: 11px; opacity: .7; padding: 6px 10px; box-sizing: border-box }
  .msg { max-width: 680px; margin: 0 auto 12px; width: 100%; box-sizing: border-box }
  .msg.user { border: 1px solid var(--app-input-border); border-radius: 6px; padding: 4px 8px }
  .panel_TgmhTA { display: flex; overflow: hidden; position: relative; border-left: 1px solid var(--app-widget-border); background: var(--app-primary-background); flex-direction: column; flex: 0 0 clamp(240px, 30%, 420px); min-width: 0 }
  .resizeHandle_TgmhTA { position: absolute; width: 6px; top: 0; bottom: 0; left: 0 }
  .header_TgmhTA { display: flex; padding: 8px 12px; border-bottom: 1px solid var(--app-widget-border); align-items: center; gap: 6px }
  .header_TgmhTA button { background: none; border: none; color: inherit; cursor: pointer; font-size: 14px }
  .title_TgmhTA { flex: 1 }
  .message_TgmhTA { opacity: .6; margin: 0; font-style: italic }
  .thread_UCAeZQ { overflow-y: auto; display: flex; flex-direction: column; flex: 1; gap: 12px; padding: 8px; user-select: text }
  .exchange_UCAeZQ { display: flex; flex-direction: column; gap: 4px }
  .question_UCAeZQ { border: 1px solid var(--app-input-border); border-radius: 6px; background: var(--app-input-background); align-self: flex-start; padding: 4px 6px }
  .pendingGlyph_UCAeZQ { color: #d97757; margin-right: 5px }
  .inputContainer_UCAeZQ { display: flex; margin: 8px; border: 1px solid var(--app-input-border); border-radius: 8px; flex-direction: column }
  .input_UCAeZQ { resize: none; outline: none; color: var(--app-input-foreground); background: none; border: none; padding: 6px 8px 0; font: inherit }
  .inputActions_UCAeZQ { display: flex; justify-content: flex-end; padding: 4px }
  .sendButton_UCAeZQ { background: #d97757; color: #fff; border: none; border-radius: 5px; width: 26px; height: 26px; cursor: pointer }
</style>
<style>
${css}
</style>
</head>
<body>
<div id="bar">
  <b>Clawd playground</b>
  <button data-do="idle">Idle</button>
  <button data-do="thinking">Thinking</button>
  <button data-do="working">Working</button>
  <button data-do="subagents">Subagents</button>
  <button data-do="question">Asks a question</button>
  <button data-do="alert">Needs permission</button>
  <button data-do="done">Done</button>
  <button data-do="party">Done (long turn)</button>
  <button data-do="error">Error</button>
  <button data-do="sleep">Fall asleep</button>
  <span class="sep"></span>
  <button data-do="wander">Wander now</button>
  <button data-do="hop">Hop off the end</button>
  <span class="sep"></span>
  <button data-do="wide">Wide panel</button>
  <button data-do="narrow">Narrow panel</button>
  <button data-do="theme">Light / dark</button>
  <span id="now"></span>
</div>
<div id="root"><div id="frame">
  <div class="chatContainer_07S1Yg">
    <div class="messagesContainer_07S1Yg">
      <div class="msg user">Drag Clawd and throw him around. Drop him beside the box: he falls to the bottom and climbs back up.</div>
      <div class="msg">Click him to open his speech bubble (a mocked /btw: it answers after a moment). Clicks while it's open poke him; three quick clicks make him dizzy. Hover him, or move the cursor back and forth over him to pet him. Hold him still for a few seconds, or shake him.</div>
      <div class="msg user">Use the buttons above to fake what Claude is doing.</div>
      <div class="msg">Thinking and working rotate between their versions; each scene sets up and packs away instead of popping.</div>
    </div>
    <div class="inputContainer_07S1Yg">
      <fieldset class="inputContainer_cKsPxg" data-permission-mode="default">
        <div class="messageInput_cKsPxg" contenteditable="plaintext-only" role="textbox" aria-label="Message input"></div>
        <div class="footer_mock">+  /  95%  ·  56m  ·  Fable 5.2  ·  Auto</div>
      </fieldset>
    </div>
  </div>
</div></div>
<script>
  // --- the extension's /btw, mocked: "/btw" + Enter in the input opens its side-question panel ---
  let PANEL = null
  function openPanel() {
    if (PANEL) return
    PANEL = document.createElement('div')
    PANEL.className = 'panel_TgmhTA'
    PANEL.innerHTML = '<div class="resizeHandle_TgmhTA"></div>'
      + '<div class="header_TgmhTA"><span style="color:#d97757">✦</span><span class="title_TgmhTA">Side question</span>'
      + '<button class="mock-clear" aria-label="Clear side questions from this editor">⟲</button><button class="mock-close" aria-label="Close">✕</button></div>'
      + '<div class="thread_UCAeZQ"><p class="message_TgmhTA">Ask a quick side question below without interrupting the conversation.</p></div>'
      + '<div class="inputContainer_UCAeZQ"><textarea class="input_UCAeZQ" rows="2" placeholder="Ask a side question" aria-label="Ask a side question"></textarea>'
      + '<div class="inputActions_UCAeZQ"><button class="sendButton_UCAeZQ" aria-label="Send side question">↑</button></div></div>'
    document.getElementById('frame').append(PANEL)
    const ta = PANEL.querySelector('textarea')
    ta.focus()
    const send = () => { const q = ta.value.trim(); if (q) { ta.value = ''; ask(q) } }
    PANEL.querySelector('.sendButton_UCAeZQ').onclick = send
    ta.addEventListener('keydown', ev => {
      if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); send() }
      else if (ev.key === 'Escape') { ev.preventDefault(); closePanel() }
    })
    PANEL.querySelector('.mock-close').onclick = closePanel
    PANEL.querySelector('.mock-clear').onclick = () => { PANEL.querySelector('.thread_UCAeZQ').innerHTML = '' }
  }
  function closePanel() { PANEL?.remove(); PANEL = null; document.querySelector('[aria-label="Message input"]').focus() }
  const ANSWERS = ['Short answer: yes. Longer answer: it depends on what the deadline covers; the render is the fixed part.',
    'That command lists the files changed since the last commit, newest first.', 'Probably the cache. Clear it and try again.']
  let nth = 0
  function ask(q) {
    const thread = PANEL.querySelector('.thread_UCAeZQ')
    thread.querySelector(':scope > .message_TgmhTA')?.remove()
    const ex = document.createElement('div')
    ex.className = 'exchange_UCAeZQ'
    ex.innerHTML = '<div class="question_UCAeZQ"></div><p class="message_TgmhTA"><span class="pendingGlyph_UCAeZQ">✻</span>Answering…</p>'
    ex.firstChild.textContent = q
    thread.append(ex)
    thread.scrollTop = thread.scrollHeight
    const fail = /fail|error/i.test(q)
    setTimeout(() => {
      if (!ex.isConnected) return
      ex.lastChild.remove()
      const a = document.createElement(fail ? 'p' : 'div')
      a.className = fail ? 'message_TgmhTA' : 'answer_UCAeZQ'
      a.textContent = fail ? 'Failed to get an answer: (mocked failure)' : ANSWERS[nth++ % ANSWERS.length]
      ex.append(a)
      thread.scrollTop = thread.scrollHeight
    }, 1500)
  }
  document.addEventListener('keydown', ev => {
    const el = ev.target
    if (ev.key !== 'Enter' || ev.shiftKey || !el.matches?.('[aria-label="Message input"]')) return
    ev.preventDefault()
    if (/^\\/btw\\b/.test(el.innerText.trim())) { el.textContent = ''; openPanel() }
    else el.textContent = ''
  })

  // --- fake what Claude is doing, the way the extension tells the panel ---
  const send = message => window.postMessage({ type: 'from-extension', message }, '*')
  const io = m => send({ type: 'io_message', message: m })
  let turnStart = 0
  const startTurn = () => { if (!window.cxClawd?.S.busy) { turnStart = Date.now(); io({ type: 'system', subtype: 'init' }) } }
  const block = type => io({ type: 'stream_event', event: { type: 'content_block_start', content_block: { type } } })
  const ACTIONS = {
    idle: () => io({ type: 'result', subtype: 'error_during_execution', is_error: true }),
    thinking: () => { startTurn(); block('thinking') },
    working: () => { startTurn(); block('tool_use') },
    subagents: () => { startTurn(); io({ type: 'assistant', message: { content: [{ type: 'tool_use', name: 'Task', id: 'task' + Date.now() }] } }) },
    question: () => { startTurn(); io({ type: 'assistant', message: { content: [{ type: 'tool_use', name: 'AskUserQuestion', id: 'q' + Date.now() }] } }) },
    alert: () => { startTurn(); send({ type: 'request', request: { type: 'tool_permission_request' } }) },
    done: () => { startTurn(); io({ type: 'result', duration_ms: 20_000 }) },
    party: () => { startTurn(); io({ type: 'result', duration_ms: 180_000 }) },
    error: () => { startTurn(); io({ type: 'result', subtype: 'error_max_turns', is_error: true }) },
    sleep: () => { const c = window.cxClawd; c.S.lastActive = Date.now() - 5 * 60_000 - 10; c.update() },
    wander: () => { const c = window.cxClawd; c.M.wanderAt = Date.now(); c.update() },
    hop: () => window.cxClawd.hopOffEnd(),
    wide: () => document.documentElement.style.setProperty('--panel', '100%'),
    narrow: () => document.documentElement.style.setProperty('--panel', '520px'),
    theme: () => document.documentElement.classList.toggle('light'),
  }
  document.getElementById('bar').addEventListener('click', ev => {
    const b = ev.target.closest('button[data-do]')
    if (b) ACTIONS[b.dataset.do]()
    setTimeout(() => dispatchEvent(new Event('resize')), 50)
  })
  setInterval(() => {
    const c = window.cxClawd
    if (c) document.getElementById('now').textContent = c.V.shown + (c.M.act ? '  (' + c.M.act.kind + ')' : '')
  }, 200)
</script>
<script type="module">
globalThis.CLAWD_CYCLES = ${JSON.stringify(cycles)};
${js.replace(/<\/script/gi, '<\\/script')}
</script>
</body>
</html>
`
fs.writeFileSync(path.join(out, 'index.html'), page)
console.log(`wrote playground/index.html (${Object.keys(cycles).length} animations): open it in a browser`)
