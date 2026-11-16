// Captures out/showcase.html (node build.mjs) with headless Chrome over CDP (no npm installs: Node's own fetch and WebSocket).
// One Chrome at a time, its own profile in out/chrome-profile; every frame is seek(t) + a screenshot, so the
// result does not depend on how fast the machine is.
//
//   stills:  node capture.mjs --style mix --cut wide --still 37.2 --still 12 [--out out/frames]   (style: mix | A | B | C)
//   video:   node capture.mjs --style mix --cut wide --video out/clawd-companion-16x9.mp4 [--music soundtrack.wav]
//            [--fps 30] [--from 0] [--to 88] [--preview]  (--preview: half size, fast x264, a quick look)
//            Without --music the video is silent. With it, the file plays from --music-start (seconds into the file,
//            default 0) at video t = 0, and gets the cut's fade at the end.
//   theme:   --theme hc-light (Default High Contrast Light, the user's; the default) | light (Light Modern) | dark
//   check:   node capture.mjs --style B --cut wide --determinism 37.2   (same t after different histories = same PNG)
//
// The video goes straight into ffmpeg (PNG frames on a pipe, no frame files on disk); --music is muxed in the same
// pass (from t = 0, the cut's own fade at the end).
import { spawn } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'

const HERE = path.dirname(new URL(import.meta.url).pathname)
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
const FFMPEG = path.join(process.env.HOME, '.local/bin/ffmpeg')

const args = process.argv.slice(2)
const opt = (name, def) => {
  const i = args.indexOf(`--${name}`)
  return i >= 0 ? args[i + 1] : def
}
const all = name => args.flatMap((a, i) => (a === `--${name}` ? [args[i + 1]] : []))
const style = (opt('style', 'mix') ?? 'mix').toUpperCase()
const theme = ['light', 'dark', 'hc-light'].includes(opt('theme')) ? opt('theme') : 'hc-light' // the user's: High Contrast Light
const music = opt('music') ? path.resolve(process.cwd(), opt('music')) : null
const musicStart = +opt('music-start', 0)
if (music && !fs.existsSync(music)) {
  console.error(`no such music file: ${music}`)
  process.exit(1)
}
const cutId = opt('cut', 'wide')
const outDir = path.resolve(HERE, opt('out', 'out/frames'))
const preview = args.includes('--preview')
const [W, H] = /tall/.test(cutId) ? [1080, 1920] : [1920, 1080] // tall, footer-tall: 9:16
const port = 9400 + Math.floor(Math.random() * 400)

const profile = path.join(HERE, 'out/chrome-profile')
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--hide-scrollbars',
  '--mute-audio', '--disable-partial-raster', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, `--window-size=${W},${H}`, 'about:blank'], { stdio: 'ignore' })
const sleep = ms => new Promise(r => setTimeout(r, ms))
const quit = code => {
  try {
    ws?.close()
  } catch {}
  chrome.kill()
  process.exit(code)
}
process.on('SIGINT', () => quit(130))

let targets = []
for (let i = 0; i < 100 && !targets.length; i++) {
  try {
    targets = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).filter(t => t.type === 'page')
  } catch {}
  if (!targets.length) await sleep(150)
}
if (!targets.length) {
  console.error('Chrome did not start')
  quit(1)
}
const ws = new WebSocket(targets[0].webSocketDebuggerUrl)
await new Promise(r => ws.addEventListener('open', r, { once: true }))
let id = 0
const waiting = new Map()
const errors = []
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data)
  if (m.id && waiting.has(m.id)) {
    waiting.get(m.id)(m)
    waiting.delete(m.id)
  }
  if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description ?? m.params.exceptionDetails.text)
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map(a => a.value ?? a.description).join(' '))
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
const shot = async () => Buffer.from((await send('Page.captureScreenshot', { format: 'png', fromSurface: true })).result.data, 'base64')

await send('Page.enable')
await send('Runtime.enable')
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: preview ? 0.5 : 1, mobile: false })
const url = `file://${path.join(HERE, 'out/showcase.html')}?style=${style}&cut=${cutId}&theme=${theme}&capture`
await send('Page.navigate', { url })
for (let i = 0; i < 200; i++) {
  if (await evaluate('window.__ready === true').catch(() => false)) break
  await sleep(100)
}
if (errors.length) {
  console.error(errors.join('\n'))
  quit(1)
}
// seek, then wait two frames so layout and the paused animations are painted
const seekTo = t => evaluate(`(() => { const id = seek(${t}); return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => r(id)))) })()`)
const meta = await evaluate('({ duration: SHOW.duration, fps: SHOW.fps, fade: SHOW.fade })')
// warm-up: the first paint after load can differ by a few pixels (text caret, first raster); every frame after
// it depends only on t
await seekTo(0)
await sleep(1000)
await seekTo(0)

if (args.includes('--dump')) {
  // the cut's timeline as the page computed it: scenes, captions, Clawd's clips (t in video seconds)
  const dump = await evaluate(`(() => {
    const c = SHOW.cut, r = x => Math.round(x * 1000) / 1000
    return {
      duration: r(c.end), audioStart: r(c.audioStart),
      scenes: c.scenes.map(s => [r(s.t0), s.id, s.ui ?? '', s.mode ?? '', Array.isArray(s.cam) ? s.cam.map(r).join(',') : s.cam ?? '']),
      captions: c.captions.map(([t, a, b]) => [r(t), a, b ?? '']),
      clips: c.track.segs.map(s => { const p0 = s.pos ? s.pos(0) : s.at, p1 = s.pos ? s.pos(s.t1 - s.t0) : s.at; return [r(s.t0), r(s.t1), s.clip, r(p0[0]), r(p0[1]), r(p1[0]), r(p1[1])] }),
      flashes: c.flashes.map(r),
    }
  })()`)
  console.log(JSON.stringify(dump))
  quit(0)
}
const stills = all('still')
const video = opt('video')
const det = opt('determinism')

if (stills.length) {
  fs.mkdirSync(outDir, { recursive: true })
  for (const t of stills) {
    const scene = await seekTo(+t)
    const file = path.join(outDir, `${cutId}-${style}-t${(+t).toFixed(2)}.png`)
    fs.writeFileSync(file, await shot())
    console.log(`${file}  (${scene})`)
  }
} else if (det) {
  fs.mkdirSync(outDir, { recursive: true })
  const hashes = []
  const pngs = []
  for (const before of [0, +det + 7.3, +det - 3.1, 2]) {
    await seekTo(Math.max(0, before))
    await seekTo(+det)
    const png = await shot()
    pngs.push(png)
    hashes.push(crypto.createHash('md5').update(png).digest('hex'))
  }
  const same = hashes.every(h => h === hashes[0])
  console.log(hashes.join('\n'), same ? '\nDETERMINISTIC' : '\nDIFFERENT')
  if (!same) pngs.forEach((png, i) => fs.writeFileSync(path.join(outDir, `det-${cutId}-${style}-${i}.png`), png))
} else if (video) {
  const fps = +opt('fps', meta.fps)
  const from = +opt('from', 0)
  const to = +opt('to', meta.duration)
  const frames = Math.round((to - from) * fps)
  const out = path.resolve(HERE, video)
  fs.mkdirSync(path.dirname(out), { recursive: true })
  const fade = Math.min(meta.fade ?? 1.5, to - from) // the cut's own fade-out (it ends on a quiet bar)
  const enc = preview ? ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23'] : ['-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-tune', 'animation']
  const args = ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-']
  if (music) args.push('-ss', String(musicStart + from), '-t', String(to - from), '-i', music) // video t = 0 is musicStart in the file
  args.push('-map', '0:v')
  if (music) args.push('-map', '1:a')
  args.push(...enc, '-pix_fmt', 'yuv420p', '-r', String(fps))
  // no -shortest: with a seeked MP3 it ends the audio ~7 s early; -t above already makes both streams the same length
  if (music) args.push('-af', `afade=t=out:st=${(to - from - fade).toFixed(3)}:d=${fade}`, '-c:a', 'aac', '-b:a', '320k')
  else args.push('-an') // silent
  args.push('-movflags', '+faststart', out)
  const ff = spawn(FFMPEG, args, { stdio: ['pipe', 'inherit', 'inherit'] })
  const t0 = Date.now()
  for (let i = 0; i < frames; i++) {
    await seekTo(from + i / fps)
    const png = await shot()
    if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r))
    if (i % fps === 0) process.stdout.write(`\r${i}/${frames} frames, ${((Date.now() - t0) / 1000).toFixed(0)} s`)
  }
  ff.stdin.end()
  await new Promise(r => ff.on('close', r))
  console.log(`\n${out}`)
} else {
  console.log('nothing to do: --still t, --video file or --determinism t')
}
if (errors.length) console.error(errors.join('\n'))
quit(errors.length ? 1 : 0)
