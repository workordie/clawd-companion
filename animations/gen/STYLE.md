# Clawd animation art bible

Read this whole file before drawing anything. It is the single source of truth for every accessory
and animation in this project.

## 0. HOUSE RULES (the project owner's taste; highest priority, these override everything below)

Direct feedback from the project's owner, who lives with these animations every day ("the user" below). Their taste is the
**plain, official Clawd**:

- **Clawd keeps his normal body size.** Do not use `body='crouch'`, `body='squash'` or
  `body='stretch'`, or any frame where he gets shorter, narrower or squished. The user dislikes seeing
  him shrink. Anticipate with the arms (`down`), the eyes, or a short pause instead; show a jump by moving
  his whole normal body up, legs `short` (tucked) in the air if you like, and land with a dust puff or a
  1-cell bounce. Lying down to sleep (a hand-drawn lying pose at normal cell size) is fine.
- **Plain face only.** His eyes are the official single-cell dots: `open`, `blink`, and the `look_*`
  glances. `closed` (a 2-cell lid line) only while he is asleep or dozing. NO happy arch eyes, NO sleepy
  arches, NO x / heart / star / wink / tired / angry / sad / wide / squint eyes, NO blush (including the
  library `blush` item), NO mouth (no yawns, no smiles, no gasps). Show emotion with his arms, posture,
  timing, eye direction, props and effects instead. The kit already swaps those features for plain eyes
  and lint reports them: remove them from your code.
- **No big arms-up stretch or yawn moments.**
- **Black eyes.** His eyes are black ink (`k`), not see-through holes. The kit does this automatically,
  and `layer()` fills any small hole enclosed by his body with black, including hand-made eye holes.
- The user liked the idle draft's calm holds, uneven blinks, glances and the firefly he follows with his
  eyes. That level of subtlety is right.

## 0b. Fine-line expressions (half-size pixels): the expressive style

The user loves how expressive Clawd is in their reference emojis. There, his facial expressions use
**half-size pixels**: thin blink lines, small `◠ ◠` happy arcs, `◡ ◡` content cups, winks. Full-size
(1-cell) versions look too big and blocky (the user disliked those), but these delicate fine-line
expressions are welcome. Use them through the kit only:

1. Draw the frame normally (Clawd with `put_clawd`, accessories, props) on a normal `Frame`.
2. Convert it with `ff = fine(frame)`: 64x40 half-size pixels, each cell becomes 2x2.
3. Draw the face: `fine_face(ff, pose, x, y, expr)`, or a wink: `fine_face(ff, p, x, y, expr='line', right='open')`.
4. Put fine frames in their own layer (a layer must not mix normal and fine frames). Scenery and
   particle layers can stay normal.

Expressions (`FINE_EYES`):
- `open`: the official eye hole
- `half`: mid-blink
- `line`: thin closed eye
- `happy`: thin `◠` arch
- `content`: thin `◡` cup
- `wide`: surprised
- `sparkle`: shiny, with a top-left glint
- `look_l`, `look_r`, `look_u`, `look_d`: half-step glances, subtler than the kit's `look_*`

Craft: smooth blinks go open → half → line → half → open (60–90 ms each). Hold the emotional beats
(400–1200 ms). Use expressions with intent and timing, like a character actor.
Rules from section 0 still apply: no mouth, no blush, no full-cell arches, never shrink him.

## 1. What we are making

Clawd (Claude Code's pixel mascot) sits **on top of the chat input box** in the Claude Code VS Code
extension. The user patches the extension so Clawd switches SVG animations depending on Claude's
state: idle, typing, thinking, working, needs permission, done, asleep, and more.

- The SVG shows at **96 × 60 CSS px (3 px per cell)**, on the **dark theme (#1E1E1E)** and the
  **light theme (#FFFFFF)**. Everything must read at that size on both themes.
- The bottom edge of the canvas is the input box's top border: Clawd **stands on it**.
- Idle, typing, working and sleep can stay on screen for **minutes or hours**. They must be charming
  but **calm**: no strobing, no constant full-body flailing.
- Each SVG loops forever. Users with reduced motion see **only frame 0 of each layer**, so frame 0
  must be a good still that explains the state.

## 2. Canvas and home spot

- Canvas: **32 × 20 cells** (`W`, `H`). Coordinates are (x right, y down) from the top-left (0, 0).
- **HOME = (10, 12)**: the top-left of Clawd's 11 × 8 box when he stands at rest. His feet are on
  row **19** (`GROUND`), the bottom row.
- **Every animation's frame 0 shows Clawd at HOME** in that state's base pose (exception: states whose
  base pose is different by nature, such as lying in bed for sleep; keep his body roughly centered
  around x 10–20 even then). The patch swaps SVGs instantly, so a shared home spot means Clawd never
  teleports.
- Space: cols 0–9 left of him, cols 21–31 right of him, rows 0–11 above him. Keep a **1-cell margin**
  at the canvas edges unless something deliberately enters or leaves.
- Nothing may hang below row 19 (it would be cut off). Things resting on the input box sit on row 19.

## 3. Clawd's identity (do not break)

- Body: flat official orange `#` (#D97757), 9 × 6 block, 1-cell arm stubs on both sides, 4 leg stubs.
  **No outline. No shading on his body by default.** (`@` and `%` are rare exceptions: an arm crossing in
  front of his body, or a deliberate lighting effect.)
- Eyes are **black ink** (`k`; user preference, see section 0). The kit's `_` eye cells are drawn black. Expressions come from the
  body kit (`clawd(eyes=..., mouth=..., blush=...)`). Lines on his body use `e` (ink_brown).
- He has **no mouth** normally. Use a mouth only for a strong, brief expression (yawn, gasp, big grin).
- Only change his shape through the kit: `body='crouch' | 'squash' | 'stretch'`, the arm and leg shapes,
  `Pose.mirrored()`. For anything else (e.g. lying down), hand-draw a variant with `Pose.from_rows` that
  keeps the same cell size, color and proportions. **Never draw Clawd at a different pixel scale.**
  Mini Clawds for subagents are fine, but at the same 1-cell pixel size, just fewer cells.
- **Always draw Clawd with `put_clawd()`** and accessories with `wear()`, so the tools can track him.

## 4. Palette and contrast (both themes)

Use only the palette in `clawdlib.PALETTE` (40 colors, one char each). Never add colors.

| char | name | | char | name | | char | name |
|---|---|---|---|---|---|---|---|
| `#` | body (Clawd) | | `r` | red | | `b` | blue |
| `@` | body_shade | | `R` | dark_red | | `B` | navy |
| `%` | body_light | | `p` | pink | | `c` | cyan |
| `e` | ink_brown (lines on Clawd) | | `P` | light_pink | | `C` | ice |
| `k` | ink (near-black) | | `o` | orange | | `i` | night (dark blue) |
| `K` | charcoal | | `O` | rust | | `v` | violet |
| `n` | graphite | | `y` | yellow | | `V` | deep_violet |
| `N` | gray | | `Y` | pale_yellow | | `l` | lavender |
| `m` | silver | | `j` | gold | | `L` | pale_lilac |
| `M` | light_gray | | `J` | dark_gold | | `t` | tan |
| `w` | paper (off-white) | | `g` | green | | `T` | wood |
| `W` | white | | `G` | dark_green | | `d` | dark_wood |
| `s` | steel | | `h` | mint | | `S` | chrome |
| | | | `a` | lime | | | |

**The two-theme rule.** The background is either almost black or pure white, so:

- Dark colors (`k K i n d`) **vanish against the dark theme** where they touch transparency.
- Very light colors (`W w Y C L P M S`) **vanish against the light theme** where they touch transparency.
- Shapes should touch the background with **mid-tones**: `# o r g b c v l t T j s N m R G B V O p a y`.
  When a light object (paper, blanket, cloud, bubble) sits on the background, give it a mid-tone or
  darker **contour** (`N m s t`, or a colored rim). When a dark object (sunglasses, a top hat) touches
  the background, add a lighter rim or highlight (`n N m s` or a colored band).
- `W` is for sparkle cores, glints and highlights, not for large areas.
- `lint` reports edge pixels that are nearly invisible per theme. A few are fine; silhouettes that
  disappear are not.

## 5. Pixel-art craft

- **Readability first.** At 3 px per cell, a detail smaller than 1 cell does not exist. Prefer bold,
  simple, iconic shapes. If you squint at the real-size strip and can't tell what an object is, redesign.
- **Light from the top-left.** Each material gets a base tone, a shadow tone (bottom/right) and at most
  one highlight (top/left). No "pillow shading" (darkening all edges equally).
- **Clean lines.** Diagonals step evenly (1:1, 2:1, 1:2). No jaggies (uneven steps), no doubled corners
  ("L-shapes" where a single diagonal step is meant), no orphan single pixels unless they are
  intentional particles or glints.
- **No noise or dithering** at this scale. Use a few large, clear color areas.
- **Silhouette test.** Every object should be recognizable as a solid single-color silhouette.
- **Scale consistency.** Props are sized relative to Clawd (9 × 6 body). A mug is about 3–4 cells, a
  laptop 9–12, a hat 7–11 wide. One cell is one pixel everywhere: no mixed resolutions.
- **Consistent outline policy.** Clawd has no outline. Props use selective contours (darker shade of
  their own color, or a mid-tone where needed for theme contrast), not black outlines everywhere.

## 6. Animation craft

- **Timing.** Motion frames are 60–140 ms. Holds (still poses) are 300–4000 ms. Blinks are 100–160 ms
  closed. Particles step every 80–200 ms. Nothing under 40 ms.
- **Spacing makes easing.** Slow in and out of key poses by putting smaller moves and longer holds
  near the extremes.
- **Anticipation** before big actions (crouch before a jump, wind-up before a throw).
- **Follow-through and overlapping action.** Attached things lag: a hat or pom-pom lands 1 frame after
  the body, an antenna or tassel bounces once. Use `wear(..., dy=1)` on the landing frame, etc.
- **Squash and stretch** with the kit's `crouch`, `squash` and `stretch` bodies, sparingly: one cell of
  squash is a lot.
- **Arcs.** Particles, thrown objects and confetti follow curved paths (`ballistic()`).
- **Secondary motion and life.** Long loops need irregular rhythm: blinks at uneven intervals
  (e.g. 3.1 s, 4.7 s, a quick double blink), an occasional glance or tiny gesture. Avoid metronome
  repetition.
- **Seamless loops.** The last frame must flow into frame 0 with no pop.
- **No strobing.** Never flash large areas. Keep blinking lights small and slower than 3 Hz.
- **Energy matches the state** (table in section 8). Attention states may be bouncy; long states
  must be soothing.

## 7. Layers and file size

- A layer is a list of `(Frame, ms)`. Each layer loops independently. All layers start together at t=0.
- Put **Clawd and everything attached to him in one layer** (or in layers with identical timing).
  Never let a hat drift out of sync with his head.
- **Static scenery goes in its own 1-frame layer** (`static('scene', frame)`): smaller SVGs.
- **Independent effects** (zzz, sparkles, steam, notes, rain) go in their own layers. Choosing
  **co-prime loop lengths** (e.g. 2300 ms vs 3100 ms) makes the combination feel less repetitive.
- Layers draw in order: later layers on top. Think about overlaps (steam in front of a mug, Clawd in
  front of a desk, a blanket in front of Clawd).
- Identical adjacent frames merge automatically. Target an SVG under **40 KB** (lint estimates it;
  it warns above 60 KB).

## 8. States (what each animation is for)

| file (`gen/anims/<name>.py`) | Claude Code state | on screen for | energy |
|---|---|---|---|
| `idle` | session idle, waiting for your prompt | minutes, very often | very calm, alive |
| `idle-pet`, `idle-bubbles`, `idle-kite`, `idle-garden`, `idle-game`, `idle-bird` | idle variants the patch rotates with `idle` | minutes, very often | very calm, alive |
| `typing` | you are typing in the input box | seconds to minutes | calm, attentive |
| `thinking` | Claude is thinking (extended thinking) | 5–90 s | calm, pondering |
| `working` | Claude is running: tools, edits, writing | 10 s to 10 min | steady busy |
| `alert` | needs your permission (`requires_action`) | until you click | friendly attention |
| `question` | Claude asked you a question | until you answer | curious |
| `done` | finished while you weren't looking | until you look | joyful burst, then content |
| `sleep` | idle for a long time | minutes to hours | very calm |
| `compacting` | compacting the conversation | 10–60 s | busy, funny |
| `hooks` | running start-up or prompt hooks | 1–10 s | playful |
| `manual`, `manual-drive`, `manual-craft` | default (manual) permission mode, idle in that mode; 3 variants the patch can rotate between | long | calm, a little funny |
| `plan` | plan mode (idle while in plan mode) | long | calm, studious |
| `edits` | accept-edits mode (idle in that mode) | long | calm builder |
| `auto`, `auto-robot`, `auto-cloud` | auto mode (idle in that mode); 3 variants the patch can rotate between | long | breezy |
| `bypass` | bypass-permissions mode (idle in that mode) | long | cool, daring |
| `subagents` | subagents are running | 10 s to minutes | busy teamwork |
| `error` | something failed | seconds | sad but cute |
| `rate-limit` | rate limited, waiting | minutes | patient |
| `vibe` | personal chill-music mode | any | groovy |
| `hello` | session start / panel opened | 2–4 s | welcoming |

## 9. Accessory anchors (the `Item` slot decides where the sprite's anchor lands)

| slot | anchor lands on | drawn |
|---|---|---|
| `head` | Clawd's head-top-center pixel (x 5 of his box, his top row). A brim that overlaps his top row is anchored on that row; a floating halo is anchored below its lowest pixel. | after Clawd |
| `face` | between his eyes, on the eye row | after Clawd |
| `neck` | center, 2 rows below the eyes (bow tie, chain) | after Clawd |
| `back` | his body center | BEFORE Clawd (`wear` it first) |
| `hand` | the grip point just outside his right hand. Left hand: `side='l'` mirrors automatically. | after Clawd |
| `ground` | bottom-center cell of the prop (rests on row 19 or on another prop) | your choice |
| `fx` | visual center of the effect | your choice |
| `scene` | bottom-center cell (furniture, big props) | your choice |

Animated items are a list of sprites plus suggested `ms`. Design head and face items for the normal
body. With crouch or squash the anchors move automatically, because `wear` uses the pose.

## 10. Tools

```
python3 gen/preview.py anim <name>             # contact sheet PNG (dark + light) + lint
python3 gen/preview.py anim <name> --layer L   # only one layer's frames
python3 gen/preview.py frame <name> <i>        # one moment, huge, with a coordinate grid
python3 gen/preview.py acc <module>            # accessory sheet: alone, worn, real size
python3 gen/preview.py lint <name>             # checks only
python3 gen/preview.py list                    # all library accessories
python3 gen/make.py [names]                    # build clawd.json + SVGs (the coordinator runs this)
```

Look at your PNGs (Read the image file) **every time you change something**. Judge them at real size
and on both themes. The sheets are your eyes.
Python is **3.9**: no `match`, no `X | Y` type unions. Run commands from `~/Projects/clawd-svgs`.
