// Builds dist/claude-code-custom-<version>.vsix from the installed Claude Code
// extension plus everything in custom/.
//
//   npm run build                 newest installed version
//   npm run build -- --from <dir> a specific extension folder
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

import { MARK, ROOT, copyCustomFiles, findInstalledExtension, isPatched, patchExtensionJs } from './lib.mjs'

const source = findInstalledExtension()
const stage = path.join(ROOT, 'build', 'stage')
const ext = path.join(stage, 'extension')
const dist = path.join(ROOT, 'dist')

console.log(`source  ${source}`)
fs.rmSync(stage, { recursive: true, force: true })
fs.mkdirSync(ext, { recursive: true })
fs.cpSync(source, ext, { recursive: true, verbatimSymlinks: true })

// The installed folder's .vsixmanifest becomes the package's root manifest.
const manifestPath = path.join(ext, '.vsixmanifest')
let manifest = fs.readFileSync(manifestPath, 'utf8')
fs.rmSync(manifestPath)

// Patch the webview HTML template.
const jsPath = path.join(ext, 'extension.js')
const original = fs.readFileSync(jsPath, 'utf8')
const wasPatched = isPatched(original)
fs.writeFileSync(jsPath, patchExtensionJs(original))
execFileSync(process.execPath, ['--check', jsPath]) // throws if the patch broke the syntax
console.log(wasPatched ? 'patch   already present, kept' : 'patch   webview now loads custom.css + custom.js')

console.log(`clawd   ${copyCustomFiles(path.join(ext, "webview"))} animations`)

// Mark the display name so the custom build is recognisable in the Extensions view.
const pkgPath = path.join(ext, 'package.json')
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'))
if (!pkg.displayName.endsWith('(custom)')) pkg.displayName += ' (custom)'
fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2))
manifest = manifest.replace(/<DisplayName>(.*?)( \(custom\))?<\/DisplayName>/, '<DisplayName>$1 (custom)</DisplayName>')
fs.writeFileSync(path.join(stage, 'extension.vsixmanifest'), manifest)

// [Content_Types].xml: one Default per file extension in the package.
const exts = new Set(['.vsixmanifest'])
const walk = dir => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name)
    if (e.isDirectory()) walk(p)
    else if (path.extname(e.name)) exts.add(path.extname(e.name).toLowerCase())
  }
}
walk(ext)
const types = {
  '.json': 'application/json', '.js': 'application/javascript', '.css': 'text/css',
  '.md': 'text/markdown', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.vsixmanifest': 'text/xml', '.html': 'text/html', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.ttf': 'font/ttf', '.wasm': 'application/wasm', '.txt': 'text/plain',
}
fs.writeFileSync(
  path.join(stage, '[Content_Types].xml'),
  `<?xml version="1.0" encoding="utf-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">` +
    [...exts].sort().map(x => `<Default Extension="${x}" ContentType="${types[x] ?? 'application/octet-stream'}"/>`).join('') +
    `</Types>\n`,
)

// Zip it. `zip` keeps file modes, so the bundled claude binary stays executable.
fs.mkdirSync(dist, { recursive: true })
const out = path.join(dist, `claude-code-custom-${pkg.version}.vsix`)
fs.rmSync(out, { force: true })
execFileSync('zip', ['-q', '-r', '-X', out, '.'], { cwd: stage, stdio: 'inherit' })

const mb = (fs.statSync(out).size / 1024 / 1024).toFixed(0)
console.log(`built   ${path.relative(ROOT, out)} (${mb} MB, ${MARK})`)
console.log('next    npm run install-vsix')
