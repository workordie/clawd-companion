// Builds out/showcase.html: src/page.html with src/realpanel.js, src/engine.js, src/scenes.js, every Clawd SVG and the
// real Claude Code panel (tools/realbox: run capture-states.mjs first) inlined.
//   node build.mjs
// The SVGs are inlined as text (a JSON block) and put into the DOM as real inline <svg> when a frame needs them,
// so all their CSS animations show up in document.getAnimations() and seek() can set every one's currentTime.
import fs from 'node:fs'
import path from 'node:path'
import { realData, scriptJson } from './tools/realbox/doc.mjs'

const HERE = path.dirname(new URL(import.meta.url).pathname)
const SVG_DIR = path.join(process.env.HOME, 'Projects/vsix-claude-ext/clawd-animations/svg')

const clips = {}
for (const file of fs.readdirSync(SVG_DIR).sort()) {
  const m = /^clawd-(.+)\.svg$/.exec(file)
  if (!m) continue
  const svg = fs.readFileSync(path.join(SVG_DIR, file), 'utf8').trim()
  // its full cycle: the longest animation in it (every layer loops inside that)
  let ms = 0
  let once = false
  for (const a of svg.matchAll(/animation:[\w-]+ (\d+)ms step-end (infinite|1)/g)) {
    ms = Math.max(ms, +a[1])
    if (a[2] === '1') once = true
  }
  clips[m[1]] = { ms: ms || 1000, once, svg }
}

const json = JSON.stringify(clips).replace(/<\//g, '<\\/')
// the real Claude Code panel: the installed extension's CSS + the captured DOM states (tools/realbox). It holds
// Anthropic's code, so the page goes to out/ (git-ignored), never into the repo.
const real = realData()
const page = fs.readFileSync(path.join(HERE, 'src/page.html'), 'utf8')
const out = page
  .replace('/*CLAWD-SVGS*/', () => json)
  .replace('/*REAL-DATA*/', () => scriptJson(real))
  .replace('/*REALPANEL*/', () => fs.readFileSync(path.join(HERE, 'src/realpanel.js'), 'utf8'))
  .replace('/*ENGINE*/', () => fs.readFileSync(path.join(HERE, 'src/engine.js'), 'utf8'))
  .replace('/*SCENES*/', () => fs.readFileSync(path.join(HERE, 'src/scenes.js'), 'utf8'))
fs.mkdirSync(path.join(HERE, 'out'), { recursive: true })
fs.writeFileSync(path.join(HERE, 'out/showcase.html'), out)
fs.rmSync(path.join(HERE, 'showcase.html'), { force: true }) // older builds wrote it next to src/
const states = Object.values(real.panels).reduce((n, p) => n + Object.keys(p.states).length, 0)
console.log(`out/showcase.html: ${Object.keys(clips).length} clips, ${Object.keys(real.panels).length} real panels (${states} states), ${(out.length / 1e6).toFixed(2)} MB`)
