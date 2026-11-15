// Fast loop once the custom build is installed: copies custom/ straight into the
// installed extension, no rebuild. Then reload the VS Code window.
import fs from 'node:fs'
import path from 'node:path'

import { copyCustomFiles, findInstalledExtension, isPatched } from './lib.mjs'

const dir = findInstalledExtension()
if (!isPatched(fs.readFileSync(path.join(dir, 'extension.js'), 'utf8'))) {
  throw new Error(`${dir} is not the custom build. Run npm run build && npm run install-vsix first.`)
}
const n = copyCustomFiles(path.join(dir, "webview"))
console.log(`synced custom/ and ${n} Clawd animations → ${dir}/webview`)
console.log('In VS Code: Cmd+Shift+P → "Developer: Reload Window" (or close and reopen the Claude panel).')
