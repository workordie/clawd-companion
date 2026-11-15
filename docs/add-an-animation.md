# Add your own animation

Every animation is one small Python file in `animations/gen/anims/`. It draws pixel frames with the toolkit in
`animations/gen/clawdlib.py` and returns them as layers; the build turns that into an animated SVG (pure CSS, no
JavaScript), and the extension shows it on the input box.

You need Python 3.9+ with Pillow (`pip3 install pillow`) and Node 18+. Run everything from `animations/`.

## 1. Read the rules (5 minutes)

[`gen/STYLE.md`](../animations/gen/STYLE.md) is the art bible. The short version:

- One canvas: 32 x 20 cells (shown at 3 px per cell, 96 x 60 px). The bottom edge is the input box's top border.
- Clawd's 11 x 8 box stands at `HOME = (10, 12)`. **Frame 0 is Clawd at HOME in a good still**: reduced-motion users
  only ever see frame 0, and every scene starts there, so switching never makes him jump.
- **Clawd never shrinks**: no crouch, squash or stretch. Jumps move his whole body.
- **Plain black eyes**, no mouth, no blush. The fine-line faces (`fine_face`: open, half, line, look_l/r/u/d, wide,
  sparkle) are the only expressions. Emotion comes from arms, timing, eye direction, props and effects.
- It must read on both the dark and the light theme, and stay under ~50 KB.

## 2. Start from the example

```sh
cp gen/anims/_example.py gen/anims/working_dj.py
```

Edit the top of the new file:

```python
NAME = 'working-dj'            # the file name is NAME with '-' -> '_'
STATE = 'working (variant)'    # shown in the gallery
DESC = 'Spins records while Claude works: ...'
```

`build()` returns `anim(NAME, DESC, layers, state=STATE)`. A layer is a list of `(Frame, ms)`; layers loop on
their own, so a steam puff can loop every 1.2 s while the body loops every 8 s. Draw Clawd with
`put_clawd(frame, clawd(...))`, give him accessories with `wear(frame, item, pose)` (`python3 gen/preview.py list`
shows all 225), and put fine-line faces on a `fine(frame)` copy in their own layer. The existing animations in
`gen/anims/` are good references: `idle_bird.py` is a simple one, `working_forge.py` a busy one.

## 3. Look at it

```sh
python3 gen/preview.py anim working-dj      # contact sheet: every frame, dark + light, real size, and lint
python3 gen/preview.py frame working-dj 4   # one frame, big
python3 gen/preview.py gif working-dj       # a GIF to check the motion
```

Pictures go to `gen/out/`. Lint warns about shrinking, eyes that aren't allowed, frame 0 away from HOME, size and
contrast. Fix every warning or know why it's fine.

## 4. Build it

```sh
python3 gen/make.py working-dj              # -> svg/clawd-working-dj.svg
python3 gen/transitions.py working-dj       # -> svg-tx/: its set-up and pack-away clips (for scenes with props)
```

Add the name to `ORDER` in `gen/make.py` if you want it sorted with its state (optional). The first build on a
fresh clone builds everything once (about a minute).

## 5. Hook it up

- **A new version of an existing state** needs nothing: name it `<state>-<anything>` and `custom.js` adds it to the
  rotation for `thinking`, `working`, `typing`, `done`, `hello`, `sleep`, `question` and `alert`.
- **A new idle scene**: add its name to the `IDLE` list at the top of `extension/custom/custom.js`.
- **A permission-mode scene**: add it to `MODE` there.
- **Something new** (a new state, a new reaction): see [how-it-works.md](how-it-works.md); `desired()` in
  `custom.js` decides what he shows.

## 6. Try it

```sh
cd ../extension
npm run playground      # then open extension/playground/index.html and use the buttons
npm run sync            # into your installed build; then Developer: Reload Window in VS Code
```

## Moving clips

Clips that the patch moves around (walk, climb, hop, teeter, sit-edge) are drawn "on the spot" and follow exact
contracts (where the wall or the edge is in the canvas, how fast the patch slides them). Each module's docstring
spells its contract out; keep to it, or change the matching numbers in `custom.js` ("Moving him").
