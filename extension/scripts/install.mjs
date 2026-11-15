// Installs the newest dist/*.vsix into VS Code, replacing the marketplace copy.
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

import { CODE_CLI, ROOT } from './lib.mjs'

const dist = path.join(ROOT, 'dist')
const vsix = fs
  .readdirSync(dist)
  .filter(f => f.endsWith('.vsix'))
  .map(f => path.join(dist, f))
  .sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs)[0]
if (!vsix) throw new Error('No .vsix in dist/. Run npm run build first.')

execFileSync(CODE_CLI, ['--install-extension', vsix, '--force'], { stdio: 'inherit' })
console.log('\nInstalled. In VS Code: Cmd+Shift+P → "Developer: Reload Window".')
console.log('Turn off auto-update for Claude Code (Extensions view → gear → Auto Update) or an update will replace it.')
