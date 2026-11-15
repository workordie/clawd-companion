// Turns one animation from clawd.json into an animated SVG.
// Shared by the Studio (live preview) and build.mjs (files on disk), so what you preview is what you get.
//
// How the SVG animates: every frame is a <g>. Each <g> gets a CSS keyframe that makes it visible
// (opacity 1) only during its time slot, with step-end timing so frames snap like pixel art.
// Layers loop independently. Works when the SVG is loaded via <img>, CSS background or inlined
// (class names are prefixed per animation so several can live on one page).

export const slug = (name) => String(name).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'clawd';
export const fileName = (anim) => `clawd-${slug(anim.name)}.svg`;

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const pct = (v) => `${+v.toFixed(3)}%`;

export function framePaths(rows, palette) {
  const byColor = new Map();
  rows.forEach((row, y) => {
    let x = 0;
    while (x < row.length) {
      const c = row[x];
      if (c === '.' || !palette[c]) { x++; continue; }
      const x0 = x;
      while (x < row.length && row[x] === c) x++;
      const w = x - x0;
      if (!byColor.has(c)) byColor.set(c, []);
      byColor.get(c).push(`M${x0} ${y}h${w}v1h-${w}z`);
    }
  });
  return [...byColor].map(([c, d]) => `<path fill="${palette[c]}" d="${d.join('')}"/>`).join('');
}

export function buildSvg(doc, anim) {
  const id = `clawd-${slug(anim.name)}-`;
  const css = [];
  const groups = [];
  anim.layers.forEach((layer, li) => {
    const total = layer.frames.reduce((s, f) => s + f.ms, 0);
    const res = layer.res || 1;   // res 2 = fine layer: half-size pixels (64x40 rows), drawn at scale 1/2
    const tf = res === 1 ? '' : ` transform="scale(${1 / res})"`;
    let t = 0;
    layer.frames.forEach((fr, fi) => {
      const cls = `${id}${li}-${fi}`;
      groups.push(`<g class="${cls}"${tf}>${framePaths(fr.rows, doc.palette)}</g>`);
      if (layer.frames.length > 1) {
        const s = (t / total) * 100;
        const e = ((t + fr.ms) / total) * 100;
        const kf = t === 0 ? ['0%{opacity:1}'] : ['0%{opacity:0}', `${pct(s)}{opacity:1}`];
        if (e < 99.9995) kf.push(`${pct(e)}{opacity:0}`, '100%{opacity:0}');
        else kf.push('100%{opacity:1}');
        css.push(`@keyframes ${cls}{${kf.join('')}}`);
        // `once`: a one-shot that plays a single time and holds its last frame (set-up/pack-away clips)
        css.push(`.${cls}{opacity:${fi === 0 ? 1 : 0};animation:${cls} ${total}ms step-end ${anim.once ? '1 forwards' : 'infinite'}}`);
      }
      t += fr.ms;
    });
  });
  css.push(`@media (prefers-reduced-motion:reduce){[class^="${id}"]{animation:none!important}}`);
  const s = doc.scale || 3;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${doc.w * s}" height="${doc.h * s}" viewBox="0 0 ${doc.w} ${doc.h}" shape-rendering="crispEdges">`
    + `<title>Clawd ${esc(anim.name)}</title><desc>${esc(anim.desc || '')}</desc>`
    + `<style>${css.join('')}</style>${groups.join('')}</svg>\n`;
}

// Returns a list of problems (empty = valid). Used by the server before writing anything.
export function validate(doc) {
  const errs = [];
  if (!doc || typeof doc !== 'object') return ['not an object'];
  const { w, h, palette, animations } = doc;
  if (!Number.isInteger(w) || w < 1 || w > 128 || !Number.isInteger(h) || h < 1 || h > 128) errs.push('w/h must be integers 1-128');
  if (!palette || typeof palette !== 'object') errs.push('palette missing');
  else for (const [k, v] of Object.entries(palette)) {
    if (k.length !== 1 || k === '.') errs.push(`bad palette key "${k}"`);
    if (!/^#[0-9a-fA-F]{3,8}$/.test(v)) errs.push(`bad color for "${k}"`);
  }
  if (!Array.isArray(animations) || !animations.length) return [...errs, 'no animations'];
  const seen = new Set();
  animations.forEach((a, ai) => {
    const where = `animation ${ai + 1}`;
    if (!a.name || typeof a.name !== 'string') errs.push(`${where}: name missing`);
    else if (seen.has(slug(a.name))) errs.push(`${where}: duplicate name "${a.name}"`);
    else seen.add(slug(a.name));
    if (!Array.isArray(a.layers) || !a.layers.length) { errs.push(`${where}: no layers`); return; }
    a.layers.forEach((l, li) => {
      if (!Array.isArray(l.frames) || !l.frames.length) { errs.push(`${where} layer ${li + 1}: no frames`); return; }
      const res = l.res || 1;
      if (res !== 1 && res !== 2) errs.push(`${where} layer ${li + 1}: res must be 1 or 2`);
      l.frames.forEach((f, fi) => {
        const at = `${where} layer ${li + 1} frame ${fi + 1}`;
        if (!Number.isInteger(f.ms) || f.ms < 20 || f.ms > 60000) errs.push(`${at}: ms must be 20-60000`);
        if (!Array.isArray(f.rows) || f.rows.length !== h * res || f.rows.some((r) => typeof r !== 'string' || r.length !== w * res)) errs.push(`${at}: rows must be ${h * res} strings of ${w * res} chars`);
      });
    });
  });
  return errs;
}
