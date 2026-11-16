// Checks that a captured state, rebuilt the way the video rebuilds it (src/realpanel.js: the real CSS + the DOM
// snapshot in an iframe), looks exactly like the live panel did (the <state>.ref.png taken while capturing, without
// the patch's Clawd). Writes <state>.rebuilt.png and prints how many pixels differ.
//   node tools/realbox/verify.mjs [--panel stage] [--state idle]
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { chrome, OUT, VIDEO } from './realbox.mjs'
import { realData, scriptJson } from './doc.mjs'

const args = process.argv.slice(2)
const opt = (n, d) => (args.includes(`--${n}`) ? args[args.indexOf(`--${n}`) + 1] : d)
const panels = opt('panel') ? [opt('panel')] : ['a-wide', 'a-tall', 'stage']

for (const name of panels) {
  const data = realData({ panels: [name] })
  const P = data.panels[name]
  const page = path.join(OUT, `verify-${name}.html`)
  fs.writeFileSync(page, `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}</style></head><body>
<script id="real-data" type="application/json">${scriptJson(data)}</script>
<script>${fs.readFileSync(path.join(VIDEO, 'src/realpanel.js'), 'utf8')}</script>
<script>window.panel = new RealPanel(document.body, ${JSON.stringify(name)}, 'hc-light')
window.showState = s => { panel.show(s); panel.mark({ focus: 'snap', hover: 'snap', active: 'snap' }); panel.seek(100, 0) } // entrance animations done</script>
</body></html>`)
  const c = await chrome({ width: P.width, height: P.height, dpr: 2, profile: path.join(process.env.TMPDIR ?? '/tmp', 'realbox-profile') })
  try {
    await c.send('Page.navigate', { url: `file://${page}` })
    await c.sleep(1500)
    const states = opt('state') ? [opt('state')] : Object.keys(P.states)
    for (const s of states) {
      await c.evaluate(`showState(${JSON.stringify(s)})`)
      await c.sleep(150)
      await c.shot(null, path.join(OUT, name, `${s}.rebuilt.png`))
    }
    const errs = c.log.filter(l => /^(EXC|error)/.test(l))
    if (errs.length) console.log(errs.slice(0, 5).join('\n'))
    // compare (python, PIL): differing pixels and where they are
    const out = execFileSync('python3', ['-I', '-c', `
import sys, json
sys.path.insert(0, __import__('site').getusersitepackages())
from PIL import Image, ImageChops
d = sys.argv[1]
for s in json.loads(sys.argv[2]):
    a = Image.open(f'{d}/{s}.ref.png').convert('RGB'); b = Image.open(f'{d}/{s}.rebuilt.png').convert('RGB')
    diff = ImageChops.difference(a, b).convert('L').point(lambda v: 255 if v > 24 else 0)
    n = sum(1 for v in diff.getdata() if v)
    print(f'  {s:24s} {n:7d} px differ ({100*n/(a.width*a.height):.3f}%)  where: {diff.getbbox()}')
`, path.join(OUT, name), JSON.stringify(states)], { encoding: 'utf8' })
    console.log(`${name}:\n${out}`)
  } finally {
    c.close()
  }
}
