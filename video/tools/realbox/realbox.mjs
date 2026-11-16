// The real chat panel, outside VS Code: the installed Claude Code extension's own webview (index.js + index.css)
// plus the clawd-companion patch (custom.js + custom.css), in headless Chrome, with a stand-in for the VS Code
// host. Used to take the input box exactly as it renders, for the video.
//
// Nothing is copied out of the extension into this repo: the page is put together at run time from the
// installed files (read only), and everything it writes goes to out/realbox/ (git-ignored).
//
// The user's VS Code theme is Default High Contrast Light (hc_light), the default here.
import http from 'node:http'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { spawn } from 'node:child_process'
import { themeStyles } from './theme.mjs'

const HERE = path.dirname(new URL(import.meta.url).pathname)
export const VIDEO = path.resolve(HERE, '../..')
export const OUT = path.join(VIDEO, 'out/realbox')
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

/** The Claude Code folder VS Code uses (its extensions.json), like the patch's own scripts find it. */
export function extensionDir() {
  const dir = path.join(os.homedir(), '.vscode', 'extensions')
  const registry = JSON.parse(fs.readFileSync(path.join(dir, 'extensions.json'), 'utf8'))
  const entry = registry.find(x => x.identifier?.id === 'anthropic.claude-code')
  return path.join(dir, entry.relativeLocation ?? path.basename(entry.location.path))
}

/** The bits of the panel's HTML template that aren't ours to retype: the load-failure CSS and markup. */
export function templateParts(ext) {
  const s = fs.readFileSync(path.join(ext, 'extension.js'), 'utf8')
  const cssAt = s.search(/\w+=`\s*#claude-load-failure:not\(:empty\)/)
  const css = s.slice(s.indexOf('`', cssAt) + 1, s.indexOf('`', s.indexOf('`', cssAt) + 1))
  const fn = /function (\w+)\(e\)\{return`<div id="claude-load-failure"/.exec(s)
  const start = fn.index + fn[0].length - '<div id="claude-load-failure"'.length
  let markup = s.slice(start, s.indexOf('`}', start))
  markup = markup.replace(/\$\{"([^"]*)"\}/g, '$1').replace(/\$\{e\}/g, 'harness')
  if (/\$\{/.test(markup)) throw new Error('load-failure markup has template expressions the harness does not know')
  return { css, markup }
}

/** VS Code's own webview default styles (prepended to every webview's <head>). */
export function vscodeDefaultStyles() {
  const pre = '/Applications/Visual Studio Code.app/Contents/Resources/app/out/vs/workbench/contrib/webview/browser/pre/index.html'
  const s = fs.readFileSync(pre, 'utf8')
  const i = s.indexOf('defaultStyles.textContent = `') + 'defaultStyles.textContent = `'.length
  return s.slice(i, s.indexOf('`;', i))
}

/** Chat font settings as the extension reads them (Fh in extension.js), at their defaults: the user sets none. */
export const FONTS = {
  editorFontFamily: 'monospace',
  editorFontSize: 12,
  editorFontWeight: 'normal',
  chatFontSize: 13,
  chatFontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
}

export function pageHtml({ ext, theme, hostScript, sidebar = false }) {
  const { css, markup } = templateParts(ext)
  const t = themeStyles(theme)
  // the host sets these on <html> and <body> (applyStyles in VS Code's webview pre/index.html)
  const htmlStyle = Object.entries(t.styles).map(([k, v]) => `--${k}: ${v};`).join(' ').replace(/"/g, '&quot;')
  const auth = JSON.stringify({ authMethod: 'claudeai', email: null, subscriptionType: 'max' }).replace(/"/g, '&quot;')
  return `<!DOCTYPE html>
<html lang="en" style="${htmlStyle}">
<head>
<style id="_defaultStyles">${vscodeDefaultStyles()}</style>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="/webview/index.css" rel="stylesheet"><link href="/webview/custom.css" rel="stylesheet">
<style id="claude-font-configuration">
  :root {
    --vscode-editor-font-family: ${FONTS.editorFontFamily} !important;
    --vscode-editor-font-size: ${FONTS.editorFontSize}px !important;
    --vscode-editor-font-weight: ${FONTS.editorFontWeight} !important;
    --vscode-chat-font-size: ${FONTS.chatFontSize}px;
    --vscode-chat-font-family: ${FONTS.chatFontFamily};
  }
</style>
<style>html.rb-noclawd :is(.cx-clawd, .cx-clawd-hit) { visibility: hidden !important; }</style>
<style>
  #claude-error { max-height: 30vh; overflow: auto; }
  #claude-error:empty { min-width: 1px; min-height: 1px; opacity: 0; margin: 0; overflow: hidden; }${css}
</style>
</head>
<body class="${t.classes.join(' ')}" data-vscode-theme-kind="${t.kind}" data-vscode-theme-name="${t.label}" data-vscode-theme-id="${t.id}">
<pre id="claude-error"></pre>
${markup}
<div id="root" data-initial-auth-status="${auth}"></div>
<script>
  window.IS_SIDEBAR = ${sidebar}
  window.IS_FULL_EDITOR = false
  window.IS_SESSION_LIST_ONLY = false
</script>
<script>${hostScript}</script>
<script id="claude-panel-script" src="/webview/index.js" type="module"></script>
<script src="/webview/custom.js" type="module"></script>
</body>
</html>`
}

const TYPES = { '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2',
  '.woff': 'font/woff', '.ttf': 'font/ttf', '.json': 'application/json', '.html': 'text/html' }

/** Serves the page at / and the installed extension's webview/ folder (read only) at /webview/. */
export function serve(page, ext) {
  const root = path.join(ext, 'webview')
  const server = http.createServer((req, res) => {
    const url = decodeURIComponent(new URL(req.url, 'http://x').pathname)
    if (url === '/') {
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' })
      return res.end(page())
    }
    if (url.startsWith('/webview/')) {
      const file = path.join(root, url.slice('/webview/'.length))
      if (file.startsWith(root + path.sep) && fs.existsSync(file) && fs.statSync(file).isFile()) {
        res.writeHead(200, { 'content-type': TYPES[path.extname(file)] ?? 'application/octet-stream' })
        return fs.createReadStream(file).pipe(res)
      }
    }
    res.writeHead(404)
    res.end()
  })
  return new Promise(r => server.listen(0, '127.0.0.1', () => r(server)))
}

/** Headless Chrome over CDP (Node's own fetch and WebSocket), one at a time. */
export async function chrome({ width, height, dpr, profile }) {
  const port = 9800 + Math.floor(Math.random() * 150)
  const proc = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--hide-scrollbars',
    '--mute-audio', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, `--window-size=${width},${height}`, 'about:blank'],
  { stdio: 'ignore' })
  const sleep = ms => new Promise(r => setTimeout(r, ms))
  let targets = []
  for (let i = 0; i < 100 && !targets.length; i++) {
    try {
      targets = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).filter(t => t.type === 'page')
    } catch {}
    if (!targets.length) await sleep(150)
  }
  if (!targets.length) throw new Error('Chrome did not start')
  const ws = new WebSocket(targets[0].webSocketDebuggerUrl)
  await new Promise(r => ws.addEventListener('open', r, { once: true }))
  let id = 0
  const waiting = new Map()
  const log = []
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data)
    if (m.id && waiting.has(m.id)) {
      waiting.get(m.id)(m)
      waiting.delete(m.id)
    }
    if (m.method === 'Runtime.exceptionThrown') log.push('EXC ' + (m.params.exceptionDetails.exception?.description ?? m.params.exceptionDetails.text))
    if (m.method === 'Runtime.consoleAPICalled') log.push(m.params.type + ' ' + m.params.args.map(a => a.value ?? a.description).join(' '))
  })
  const send = (method, params = {}) => new Promise(r => {
    const i = ++id
    waiting.set(i, r)
    ws.send(JSON.stringify({ id: i, method, params }))
  })
  const evaluate = async expr => {
    const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true })
    if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description ?? 'evaluate failed')
    return r.result?.result?.value
  }
  const shot = async (clip, file) => {
    const p = { format: 'png', fromSurface: true, captureBeyondViewport: false }
    if (clip) p.clip = { ...clip, scale: 1 }
    const b = Buffer.from((await send('Page.captureScreenshot', p)).result.data, 'base64')
    if (file) fs.writeFileSync(file, b)
    return b
  }
  await send('Page.enable')
  await send('Runtime.enable')
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: dpr, mobile: false })
  const close = () => {
    try {
      ws.close()
    } catch {}
    proc.kill()
  }
  return { send, evaluate, shot, log, close, sleep }
}
