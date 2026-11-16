// VS Code's webview theme variables, computed the way VS Code computes them (WebviewThemeDataProvider):
// every registered colour, theme.getColor(id) -> `--vscode-${id.replace('.', '-')}` = color.toString().
//
// Nothing is retyped: the colour registry (976 registerColor calls with their light/dark/hc defaults and
// transforms), the Color class and the transform executor are all read out of the installed VS Code's own
// workbench bundle and run in a vm; the theme comes from VS Code's own theme JSON (with its includes); the
// built-in extensions' contributed colours come from their package.json.
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'

const APP = '/Applications/Visual Studio Code.app/Contents/Resources/app'
const WORKBENCH = path.join(APP, 'out/vs/workbench/workbench.desktop.main.js')
const THEMES = path.join(APP, 'extensions/theme-defaults')

/** End of a JS expression that starts at i: the first top-level ',' or ')' (strings and brackets skipped). */
function exprEnd(s, i) {
  let depth = 0
  for (; i < s.length; i++) {
    const c = s[i]
    if (c === '"' || c === "'" || c === '`') {
      for (i++; i < s.length && s[i] !== c; i++) if (s[i] === '\\') i++
      continue
    }
    if ('([{'.includes(c)) depth++
    else if (')]}'.includes(c)) {
      if (depth === 0) return i
      depth--
    } else if (c === ',' && depth === 0) return i
  }
  throw new Error('unterminated expression')
}

/** Index of the '}' that closes the block opening at i (strings skipped). */
function blockEnd(s, i) {
  let depth = 0
  for (; i < s.length; i++) {
    const c = s[i]
    if (c === '"' || c === "'" || c === '`') {
      for (i++; i < s.length && s[i] !== c; i++) if (s[i] === '\\') i++
      continue
    }
    if (c === '{') depth++
    else if (c === '}' && --depth === 0) return i
  }
  throw new Error('unterminated block')
}

let cached
function registry() {
  if (cached) return cached
  const src = fs.readFileSync(WORKBENCH, 'utf8')

  // VS Code's Color module (round helper, RGBA, HSLA, HSVA, Color + Color.Format.CSS), verbatim
  const round = /function (\w+)\(s,o\)\{let e=Math\.pow\(10,o\);return Math\.round\(s\*e\)\/e\}var (\w+)=class\{constructor\(o,e,t,i=1\)\{this\._rgbaBrand/.exec(src)
  const colorName = /(\w+)=class s\{static fromHex\(o\)\{return s\.Format/.exec(src.slice(round.index))[1]
  const close = `})(${colorName}||={})`
  const colorModule = src.slice(round.index, src.indexOf(close, round.index) + close.length)

  // the transform executor (darken, lighten, transparent, opaque, oneOf, ifDefinedThenElse, lessProminent, mix)
  const exec = /function (\w+)\(s,o\)\{switch\(s\.op\)\{case 0:return (\w+)\(s\.value,o\)\?\.darken\(s\.factor\)/.exec(src)
  const resolverName = exec[2]
  const resolverAt = src.indexOf(`function ${resolverName}(s,o){`, exec.index)
  const execModule = src.slice(exec.index, blockEnd(src, src.indexOf('{', resolverAt)) + 1)

  const ctx = vm.createContext({})
  vm.runInContext(`var __throw = x => { throw new Error('unknown op ' + JSON.stringify(x)) };\n${colorModule}\n` +
    execModule.replace(/default:throw \w+\(s\)/, 'default:__throw(s)') +
    `\nglobalThis.__Color = ${colorName}; globalThis.__resolve = ${resolverName};`, ctx)

  // every registerColor call: VAR=ue("id",SPEC,...) (ue = the registry's registerColor shorthand)
  const reg = /function (\w+)\(s,o,e,t,i\)\{return \w+\.registerColor\(s,o,e,t,i\)\}/.exec(src)[1]
  const callRe = new RegExp(`(?:([\\w$]+)=)?\\b${reg.replace('$', '\\$')}\\("([^"]+)",`, 'g')
  const entries = []
  const names = {}
  for (const m of src.matchAll(callRe)) {
    const at = m.index + m[0].length
    const spec = src.slice(at, exprEnd(src, at))
    if (m[1]) names[m[1]] = m[2]
    entries.push({ id: m[2], spec })
  }
  // the transform constructors' minified names, so the specs can call them
  const transforms = [...src.matchAll(/function ([\w$]+)\(([\w,.]*)\)\{return\{op:\d+[^}]*\}\}/g)].map(m => m[0])
  vm.runInContext(transforms.join('\n'), ctx)
  // colour variables resolve to their ids (registerColor returns the id)
  vm.runInContext(Object.entries(names).map(([k, v]) => `var ${k} = ${JSON.stringify(v)};`).join('\n'), ctx)
  vm.runInContext(`var nt = __Color;`, ctx) // the specs say nt.white, nt.black ... (colorName)
  if (colorName !== 'nt') vm.runInContext(`var ${colorName} = __Color;`, ctx)

  const defaults = new Map()
  const failed = []
  for (const e of entries) {
    try {
      defaults.set(e.id, vm.runInContext(`(${e.spec})`, ctx))
    } catch (err) {
      failed.push(`${e.id}: ${err.message}`)
    }
  }
  // colours the built-in extensions contribute (git decorations, ...)
  for (const dir of fs.readdirSync(path.join(APP, 'extensions'))) {
    const pj = path.join(APP, 'extensions', dir, 'package.json')
    if (!fs.existsSync(pj)) continue
    for (const c of JSON.parse(fs.readFileSync(pj, 'utf8')).contributes?.colors ?? []) {
      const d = c.defaults
      defaults.set(c.id, { light: d.light, dark: d.dark, hcDark: d.highContrast ?? d.dark, hcLight: d.highContrastLight ?? d.light })
    }
  }
  cached = { ctx, defaults, failed, Color: ctx.__Color, resolve: ctx.__resolve }
  return cached
}

const stripJsonc = raw => raw.replace(/("(?:[^"\\]|\\.)*")|\/\/[^\n]*|\/\*[\s\S]*?\*\//g, (m, str) => str ?? '').replace(/,(\s*[}\]])/g, '$1')

/** A theme's own colours, includes first (ColorThemeData._loadColorTheme). */
function themeColors(file) {
  const json = JSON.parse(stripJsonc(fs.readFileSync(file, 'utf8')))
  const base = json.include ? themeColors(path.join(path.dirname(file), json.include)) : {}
  for (const [k, v] of Object.entries(json.colors ?? {})) if (typeof v === 'string') base[k] = v
  return base
}

const KINDS = { vs: ['light', 'vscode-light'], 'vs-dark': ['dark', 'vscode-dark'], 'hc-black': ['hcDark', 'vscode-high-contrast'],
  'hc-light': ['hcLight', 'vscode-high-contrast-light'] }

/**
 * themeStyles('light_modern') -> { kind, id, label, styles: { 'vscode-editor-background': '#ffffff', ... } }
 * (the theme file's base name, as in theme-defaults/themes).
 */
export function themeStyles(name = 'light_modern') {
  const { defaults, Color, resolve } = registry()
  const pkg = JSON.parse(fs.readFileSync(path.join(THEMES, 'package.json'), 'utf8'))
  const nls = JSON.parse(fs.readFileSync(path.join(THEMES, 'package.nls.json'), 'utf8'))
  const contrib = pkg.contributes.themes.find(t => path.basename(t.path, '.json') === name)
  if (!contrib) throw new Error(`no such theme: ${name}`)
  const [type, kind] = KINDS[contrib.uiTheme]
  const own = themeColors(path.join(THEMES, contrib.path))
  const colorMap = Object.fromEntries(Object.entries(own).map(([k, v]) => [k, Color.fromHex(v)]))
  const theme = {
    type,
    defines: id => Object.prototype.hasOwnProperty.call(colorMap, id),
    getColor(id) {
      if (colorMap[id] !== undefined) return colorMap[id]
      if (!defaults.has(id)) return undefined
      const d = defaults.get(id)
      const isDefaults = d !== null && typeof d === 'object' && 'light' in d && 'dark' in d
      return resolve(isDefaults ? d[type] : d, theme) ?? undefined
    },
  }
  const styles = {
    'vscode-font-family': '-apple-system, BlinkMacSystemFont, sans-serif', // tO on macOS
    'vscode-font-weight': 'normal',
    'vscode-font-size': '13px',
    'vscode-editor-font-family': "Menlo, Monaco, 'Courier New', monospace", // editor defaults on macOS (fLr)
    'vscode-editor-font-weight': 'normal',
    'vscode-editor-font-size': '12px',
    'text-link-decoration': 'none',
  }
  for (const id of defaults.keys()) {
    const c = theme.getColor(id)
    if (c) styles['vscode-' + id.replace('.', '-')] = c.toString()
  }
  const label = (nls[contrib.label.replace(/%/g, '')] ?? contrib.id)
  // VS Code's webview host (pre/index.html applyStyles): the kind as a body class; HC Light also gets
  // vscode-high-contrast "for backwards compatibility"
  const classes = kind === 'vscode-high-contrast-light' ? [kind, 'vscode-high-contrast'] : [kind]
  return { kind, classes, id: contrib.id, label, type, styles }
}

/**
 * A TextMate scope's colour in a theme's tokenColors (with its includes), the way VS Code picks it: the rule whose
 * selector is the longest prefix of the scope; a later rule wins a tie. Falls back to editor.foreground.
 */
export function tokenColor(name, scope) {
  const pkg = JSON.parse(fs.readFileSync(path.join(THEMES, 'package.json'), 'utf8'))
  const contrib = pkg.contributes.themes.find(t => path.basename(t.path, '.json') === name)
  const rules = []
  const load = file => {
    const json = JSON.parse(stripJsonc(fs.readFileSync(file, 'utf8')))
    if (json.include) load(path.join(path.dirname(file), json.include))
    for (const r of json.tokenColors ?? []) {
      const sc = r.scope ?? ''
      for (const sel of (Array.isArray(sc) ? sc : String(sc).split(',')).map(x => x.trim())) rules.push([sel, r.settings ?? {}])
    }
  }
  load(path.join(THEMES, contrib.path))
  let best = null
  for (const [sel, st] of rules) {
    if (!st.foreground) continue
    const last = sel.split(' ').pop()
    const len = last === '' ? 0 : scope === last || scope.startsWith(last + '.') ? last.length : -1
    if (len >= 0 && (!best || len >= best[0])) best = [len, st.foreground]
  }
  return best?.[1] ?? themeStyles(name).styles['vscode-editor-foreground']
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const name = process.argv[2] ?? 'light_modern'
  const t = themeStyles(name)
  const { failed, defaults } = registry()
  console.log(`${t.label} (${t.type}): ${Object.keys(t.styles).length} variables from ${defaults.size} registered colours; ${failed.length} specs failed`)
  for (const f of failed.slice(0, 12)) console.log('  failed:', f)
  for (const k of process.argv.slice(3)) console.log(`  --${k}: ${t.styles[k]}`)
}
