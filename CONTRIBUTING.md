# Contributing

Thanks for wanting to make Clawd better.

## Ideas

Open an issue with the **Animation idea** template: what's happening in Claude Code at that moment, and what Clawd
should do. A rough sketch or a reference clip helps a lot (walking was traced from a screen recording).

## New animations

Follow [docs/add-an-animation.md](docs/add-an-animation.md). Before you open a pull request:

- it follows [animations/gen/STYLE.md](animations/gen/STYLE.md): Clawd never shrinks, plain black eyes, no mouth, frame 0
  at HOME, readable on dark and light;
- `python3 gen/preview.py anim <name>` shows no lint warnings you can't explain;
- you rebuilt it (`python3 gen/make.py <name>`, and `python3 gen/transitions.py <name>` if it has props) and the
  pull request includes the new `svg/` (and `svg-tx/`) files;
- you tried it in the playground (`cd extension && npm run playground`).

## Code changes

`extension/custom/custom.js` and `custom.css` hold both Clawd and the footer controls. Test in the playground and in
VS Code (`npm run sync`, then Developer: Reload Window). Start new class names with `cx-` and check the name isn't
taken (`grep -n "cx-yourname" extension/custom/*`).

## Never commit

The built `.vsix` (it contains Anthropic's code), anything from your installed extension, `build/`, `dist/`, or the
generated `animations/clawd.json`: `.gitignore` covers them.
