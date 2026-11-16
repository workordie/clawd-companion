// The data the video's real panels are made of (src/realpanel.js reads it as REAL): the installed extension's
// CSS, the patch's CSS, VS Code's webview defaults and theme variables, the panel template's own bits, the
// captured DOM states (out/realbox/<panel>/<state>.json) and the spinner's word list.
// It goes into out/showcase.html only (git-ignored): it holds Anthropic's code.
import fs from 'node:fs'
import path from 'node:path'
import { extensionDir, templateParts, vscodeDefaultStyles, FONTS, OUT } from './realbox.mjs'
import { themeStyles, tokenColor } from './theme.mjs'

// the code highlighter's classes (src/engine.js highlight) -> TextMate scopes
const TOKEN_SCOPES = {
  m: 'comment',
  s: 'string',
  k: 'storage.type',
  c: 'keyword.control',
  n: 'constant.numeric',
  o: 'variable.other.constant',
  f: 'entity.name.function',
  v: 'variable',
}

export function realData({ panels } = {}) {
  const ext = extensionDir()
  const W = path.join(ext, 'webview')
  const { css: loadFailure, markup } = templateParts(ext)
  const index = fs.readFileSync(path.join(W, 'index.css'), 'utf8').replace(/url\(\.\/fonts\//g, `url(file://${W}/fonts/`)
  const css = {
    defaults: vscodeDefaultStyles(),
    index,
    custom: fs.readFileSync(path.join(W, 'custom.css'), 'utf8'),
    fonts: `:root {
    --vscode-editor-font-family: ${FONTS.editorFontFamily} !important;
    --vscode-editor-font-size: ${FONTS.editorFontSize}px !important;
    --vscode-editor-font-weight: ${FONTS.editorFontWeight} !important;
    --vscode-chat-font-size: ${FONTS.chatFontSize}px;
    --vscode-chat-font-family: ${FONTS.chatFontFamily};
  }`,
    template: `#claude-error { max-height: 30vh; overflow: auto; }
  #claude-error:empty { min-width: 1px; min-height: 1px; opacity: 0; margin: 0; overflow: hidden; }${loadFailure}`,
    // video only: CSS transitions would run on the wall clock between frames; changes snap instead. Scrollbars
    // never show in a still panel.
    video: '*, *::before, *::after { transition: none !important; } ::-webkit-scrollbar { display: none; }' +
      // Clawd's animation is an inline SVG in his .cx-clawd element (the patch uses an <img> of the same SVG); no
      // will-change, so his pixels are drawn at the zoom the shot uses, not scaled up from a cached layer
      ' .cx-clawd { will-change: auto !important; } .cx-clawd > svg { display: block; width: 100%; height: 100%; }',
  }
  // the template's load-failure markup, without its watchdog script (it only reports a panel that never started)
  const quiet = markup.replace(/<script[\s\S]*?<\/script>/g, '')
  // the user's theme is Default High Contrast Light; Light/Dark Modern stay available (--theme light | dark)
  const themes = {}
  for (const [k, name] of [['hc-light', 'hc_light'], ['light', 'light_modern'], ['dark', 'dark_modern']]) {
    themes[k] = themeStyles(name)
    // the VS Code window's code (look A): its token colours from the theme's own tokenColors
    themes[k].tokens = Object.fromEntries(Object.entries(TOKEN_SCOPES).map(([cls, scope]) => [cls, tokenColor(name, scope)]))
  }
  // the icon the extension gives its own editor tab (setupPanel: iconPath resources/claude-logo.svg)
  const tabIcon = fs.readFileSync(path.join(ext, 'resources', 'claude-logo.svg'), 'utf8').replace(/<title>.*?<\/title>/, '')
  const out = { themes, css, markup: quiet, panels: {}, verbs: spinnerVerbs(W), tabIcon }
  for (const name of panels ?? fs.readdirSync(OUT).filter(d => fs.existsSync(path.join(OUT, d, 'idle.json')))) {
    const dir = path.join(OUT, name)
    const states = {}
    let size = null
    for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort()) {
      const s = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'))
      size ??= s.panel
      states[s.state] = { html: s.html, vars: s.vars, extras: s.extras, focus: s.focus, hover: s.hover, active: s.active, geometry: s.geometry }
    }
    out.panels[name] = { name, width: size.width, height: size.height, states }
  }
  return out
}

/** The panel's own "Claude is working" words (index.js). */
function spinnerVerbs(W) {
  const s = fs.readFileSync(path.join(W, 'index.js'), 'utf8')
  const m = /=\["Accomplishing",[^\]]*\]/.exec(s)
  if (!m) throw new Error('spinner words not found in index.js')
  return JSON.parse(m[0].slice(1))
}

/** JSON for a <script type="application/json"> block. */
export const scriptJson = data => JSON.stringify(data).replace(/<\//g, '<\\/').replace(/<!--/g, '<\\!--')
