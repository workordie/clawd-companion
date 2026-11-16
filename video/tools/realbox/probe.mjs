// Opens the real panel (realbox.mjs) and reports what it did: console, messages it posted, requests nobody
// answered, and a screenshot. A tool for getting the harness right.
//   node tools/realbox/probe.mjs [--width 935] [--height 700] [--theme light_modern] [--wait 4000] [--js 'expr']
import fs from 'node:fs'
import path from 'node:path'
import { extensionDir, pageHtml, serve, chrome, OUT } from './realbox.mjs'

const args = process.argv.slice(2)
const opt = (n, d) => (args.includes(`--${n}`) ? args[args.indexOf(`--${n}`) + 1] : d)
const width = +opt('width', 935)
const height = +opt('height', 700)
const theme = opt('theme', 'hc_light')
const name = opt('name', 'probe')
const ext = extensionDir()
const hostScript = fs.readFileSync(new URL('./host.js', import.meta.url), 'utf8') + (opt('host') ? '\n' + fs.readFileSync(opt('host'), 'utf8') : '')
const server = await serve(() => pageHtml({ ext, theme, hostScript }), ext)
const url = `http://127.0.0.1:${server.address().port}/`
const profile = path.join(process.env.TMPDIR ?? '/tmp', 'realbox-profile')
const c = await chrome({ width, height, dpr: +opt('dpr', 2), profile })
try {
  await c.send('Page.navigate', { url })
  await c.sleep(+opt('wait', 4000))
  await c.evaluate(fs.readFileSync(new URL('./inpage.js', import.meta.url), 'utf8'))
  if (opt('setup')) {
    await c.evaluate(fs.readFileSync(opt('setup'), 'utf8'))
    await c.sleep(+opt('settle', 1500))
  }
  fs.mkdirSync(OUT, { recursive: true })
  await c.shot(null, path.join(OUT, `${name}.png`))
  const report = await c.evaluate(`({
    sent: __sent.map(m => m.type + (m.request ? ':' + m.request.type : '')),
    unhandled: HOST.unhandled,
    fieldset: !!document.querySelector('fieldset'),
    root: document.getElementById('root')?.innerHTML.length,
    failure: document.getElementById('claude-load-failure')?.textContent.slice(0, 300),
    error: document.getElementById('claude-error')?.textContent.slice(0, 300),
    extra: ${opt('js') ?? 'null'},
  })`)
  console.log(JSON.stringify(report, null, 1))
  console.log('--- console:')
  for (const l of c.log.slice(0, 60)) console.log(l.slice(0, 400))
  console.log(`screenshot: ${path.join(OUT, `${name}.png`)}`)
} finally {
  c.close()
  server.close()
}
