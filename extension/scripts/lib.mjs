import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

export const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..')
export const MARK = 'clawd-companion'
const OLD_MARKS = ['vsix-claude-ext'] // builds patched before the rename
export const EXT_DIR = path.join(os.homedir(), '.vscode', 'extensions')
const MAC_CODE = '/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code'
/** The `code` command: $CODE_CLI if set, the macOS app's copy if it's there, else `code` on your PATH. */
export const CODE_CLI = process.env.CODE_CLI || (fs.existsSync(MAC_CODE) ? MAC_CODE : 'code')

/**
 * The Claude Code folder VS Code is using (from its extensions.json), or the
 * one passed with --from. Leftover folders VS Code has marked obsolete are
 * never picked.
 */
export function findInstalledExtension(argv = process.argv) {
  const i = argv.indexOf('--from')
  if (i !== -1 && argv[i + 1]) return path.resolve(argv[i + 1])

  const registry = JSON.parse(fs.readFileSync(path.join(EXT_DIR, 'extensions.json'), 'utf8'))
  const entry = registry.find(x => x.identifier?.id === 'anthropic.claude-code')
  if (!entry) throw new Error('Claude Code is not installed in VS Code.')
  const dir = path.join(EXT_DIR, entry.relativeLocation ?? path.basename(entry.location?.path ?? ''))
  if (!fs.existsSync(path.join(dir, 'extension.js'))) throw new Error(`Claude Code's folder is missing: ${dir}`)
  return dir
}

export const isPatched = extensionJs => [MARK, ...OLD_MARKS].some(m => extensionJs.includes(`<!--${m}:css-->`))

/** Where the animations come from: the generator's output in ../animations (svg/ and the set-up clips in svg-tx/). */
export const ANIM_DIRS = [path.join(ROOT, '..', 'animations', 'svg'), path.join(ROOT, '..', 'animations', 'svg-tx')]

/** Every animation file: [{ name, file }] across ANIM_DIRS. */
export function animationFiles() {
  const out = []
  for (const dir of ANIM_DIRS) {
    if (!fs.existsSync(dir)) continue
    for (const f of fs.readdirSync(dir)) if (/^clawd-.*\.svg$/.test(f)) out.push({ name: f.slice(6, -4), file: path.join(dir, f) })
  }
  if (out.length === 0) throw new Error('No animations found in ../animations/svg. Run: cd ../animations && python3 gen/make.py')
  return out
}

/**
 * Adds two tags to the chat webview's HTML template inside extension.js:
 * a <link> to webview/custom.css after the extension's own stylesheet, and a
 * <script type="module"> for webview/custom.js before </body>. Identifiers in
 * the minified code change every release, so they're read from the code.
 */
export function patchExtensionJs(src) {
  if (isPatched(src)) return src

  const anchor =
    /let (\w+)=([\w$]+)\.Uri\.joinPath\(this\.extensionUri,"webview","index\.js"\),[\w$]+=([\w$]+)\.asWebviewUri\(\1\)/
  const m = anchor.exec(src)
  if (!m) throw new Error('Could not find where the webview loads index.js. The extension changed; the patcher needs updating.')
  const [, , ns, webview] = m

  const start = m.index
  const end = src.indexOf('</html>', start)
  if (end === -1) throw new Error('Could not find the end of the webview HTML template.')
  let tpl = src.slice(start, end)

  const nonce = /script-src 'nonce-\$\{([\w$]+)\}'/.exec(tpl)?.[1]
  if (!nonce) throw new Error('Could not find the script nonce in the webview template.')

  const uri = file => `\${${webview}.asWebviewUri(${ns}.Uri.joinPath(this.extensionUri,"webview","${file}"))}`
  const cssTag = `<!--${MARK}:css--><link href="${uri('custom.css')}" rel="stylesheet">`
  const jsTag = `<!--${MARK}:js--><script nonce="\${${nonce}}" src="${uri('custom.js')}" type="module"></script>`

  const link = /<link href="\$\{[\w$]+\}" rel="stylesheet">/
  if (!link.test(tpl)) throw new Error('Could not find the main stylesheet <link> in the webview template.')
  if (!tpl.includes('</body>')) throw new Error('Could not find </body> in the webview template.')

  tpl = tpl.replace(link, found => found + cssTag)
  tpl = tpl.replace('</body>', () => jsTag + '</body>')

  return src.slice(0, start) + tpl + src.slice(end)
}

/**
 * Puts our files into the extension's webview folder:
 *   custom/custom.css, custom/custom.js  → webview/
 *   ../animations/svg + svg-tx/*.svg      → webview/clawd/
 * webview/clawd is emptied first so nothing stale is left behind.
 */
export function copyCustomFiles(webviewDir) {
  for (const f of ['custom.css', 'custom.js']) {
    const from = path.join(ROOT, 'custom', f)
    if (!fs.existsSync(from)) throw new Error(`custom/${f} is missing`)
    fs.copyFileSync(from, path.join(webviewDir, f))
  }

  const clawdDir = path.join(webviewDir, 'clawd')
  fs.rmSync(clawdDir, { recursive: true, force: true })
  fs.mkdirSync(clawdDir)
  const svgs = animationFiles()
  const cycles = {}
  for (const { name, file } of svgs) {
    fs.copyFileSync(file, path.join(clawdDir, path.basename(file)))
    cycles[name] = cycleMs(fs.readFileSync(file, 'utf8'))
  }

  // How long each animation's full cycle runs, so custom.js knows when one
  // has played through. The webview can't fetch files (no connect-src), so
  // this rides at the top of custom.js.
  const js = fs.readFileSync(path.join(webviewDir, 'custom.js'), 'utf8')
  fs.writeFileSync(path.join(webviewDir, 'custom.js'), `globalThis.CLAWD_CYCLES = ${JSON.stringify(cycles)};\n${js}`)
  return svgs.length
}

/** The longest CSS animation duration in an SVG, in ms: its full cycle. */
export function cycleMs(svg) {
  let max = 0
  for (const [, v, unit] of svg.matchAll(/animation:[^;}]*?\s(\d+(?:\.\d+)?)(ms|s)\b/g)) {
    max = Math.max(max, Number(v) * (unit === 's' ? 1000 : 1))
  }
  return Math.round(max) || 6000
}
