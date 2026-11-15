#!/usr/bin/env node
// Builds svg/clawd-<name>.svg for every animation in clawd.json.   Usage: node build.mjs
import { readFileSync, writeFileSync, mkdirSync, readdirSync, unlinkSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg, fileName, validate } from './svgwriter.mjs';

export const ROOT = dirname(fileURLToPath(import.meta.url));

export function writeAll(doc) {
  const errs = validate(doc);
  if (errs.length) throw new Error(errs.join('\n'));
  const dir = join(ROOT, 'svg');
  mkdirSync(dir, { recursive: true });
  const written = doc.animations.map((a) => {
    writeFileSync(join(dir, fileName(a)), buildSvg(doc, a));
    return fileName(a);
  });
  // remove SVGs of animations that were deleted or renamed
  for (const f of readdirSync(dir)) {
    if (/^clawd-.*\.svg$/.test(f) && !written.includes(f)) unlinkSync(join(dir, f));
  }
  return written;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const doc = JSON.parse(readFileSync(join(ROOT, 'clawd.json'), 'utf8'));
  for (const f of writeAll(doc)) console.log('svg/' + f);
}
