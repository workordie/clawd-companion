# How it works

## The patch

`npm run build` (in `extension/`) copies the Claude Code extension you have installed, and in its `extension.js`
adds two tags to the chat panel's HTML: a `<link>` to `webview/custom.css` and a `<script type="module">` for
`webview/custom.js`. It copies the animations into `webview/clawd/`, puts every animation's cycle length in front
of `custom.js` (`globalThis.CLAWD_CYCLES`), and packs the result as a `.vsix` that `npm run install-vsix` installs.
The patcher finds the HTML template by its structure, not by minified names, so it usually survives extension
updates; if it can't, it stops and says so. `npm run sync` copies `custom/` and the animations straight into the
installed build for quick iteration.

Nothing else in the extension changes, and `custom.js` only reads what the extension already shows its chat panel.

## Knowing what Claude is doing

The extension posts messages to the chat panel (`window` `message` events of type `from-extension`). `custom.js`
listens to the same messages:

| Message | Means |
|---|---|
| `system` / `init` | a turn started: busy, thinking |
| a `thinking` content block | thinking |
| a `text` or `tool_use` block | working |
| `tool_use` of `Task` / `Agent` | subagents running |
| `tool_use` of `AskUserQuestion` | a question for you |
| `tool_permission_request` | needs your permission |
| `status: compacting` | compacting |
| a rejected `rate_limit_event` | rate limited |
| `result` | done (a party after 2 minutes), or an error |

It also watches the input box: typing in it (`typing`), and its `data-permission-mode` attribute (the mode
animations).

## Choosing the animation

`desired()` in `custom.js` picks one, in this order: permission prompt, question, the speech bubble if it's open,
the busy states (rate limit, compacting, subagents, thinking / working), a one-shot (hello, done, error, a mode
change), typing, sleep after 5 minutes, then idle, which rotates through the idle scenes.

Versions rotate on their own: every installed `<state>-*` animation joins its state's pool (`variant()`). Thinking
and working keep one pick until it has played a full cycle, so the frequent thinking <-> working flips in a turn
return to the same two scenes; the others pick again each time they appear. Never the same one twice in a row.

Clawd is an `<img>` inside the input box. Changing its `src` (with a fresh query, so the SVG restarts) changes the
animation. Between two scenes he doesn't cut: the old one packs away (`out-<name>`), he may walk a few steps, the
new one sets up (`in-<name>`). Those clips are generated from each scene's first frame by
`animations/gen/transitions.py`: props drop in and land with a dust puff, or hop and vanish in a poof. While
Claude is busy a scene stays up at least 4 s before the next, so a burst of tool calls isn't a blur.

## Moving him

His world is the whole chat column. He stands on the input box (home) or on the bottom of the panel; the column's
sides and the box's own sides are walls. Positions are his feet's centre: on the box, a distance from its right
end (so he rides the box when it grows taller as you type); elsewhere, panel coordinates. The image stays inside
the input box element (so the extension's menus still draw over him) and is moved with a CSS transform.

- **Walking** clips walk on the spot; the code slides them at the speed they're drawn for (4 cells/s), so planted
  feet don't skate. The walk was traced frame by frame from a reference recording.
- **Physics** (thrown, dropped, hopping off): gravity, bounces off the walls, landing on the box's top or the panel's
  bottom. Where the gap beside the box is too narrow for him, it counts as box.
- **Getting home** from the bottom of the panel: a breather, `look-up`, walk to the box, `climb-left/right` (the
  walk turned a quarter, his feet on the wall, slid up 6 cells/s), and a flip over the top corner.
- **Idle wandering**: every 25-50 s he walks somewhere new; near an end of the box he may teeter, sit on the edge, or
  hop off.

Clips drawn somewhere other than standing at home (sitting on the edge) have an anchor in the `ANCHOR` table.

## Talking to him

Claude Code has a built-in `/btw` side question: a panel where you ask Claude something with the conversation as
context, without adding to it. Clicking Clawd opens that panel; `custom.css` takes it out of its dock and floats it
above his head as a speech bubble (`.cx-talk`, plus a `.cx-talk-tail`), and `custom.js` keeps it pointed at him.
The extension only opens that panel for `/btw` typed in the input box, so `openTalk()` types `/btw`, presses Enter,
and puts back whatever you had typed. While it's open he plays `talk-listen`, `talk-think` while it answers,
`talk-explain` when the answer lands, or a shrug if it failed.

## The footer

The rest of `custom.js` / `custom.css` restyles the input footer (context meter, usage bars, subagents counter,
effort slider, Ultracode switch). Its controls call the panel's own handlers, found through the React props on its
DOM nodes; if they can't be found, the extension's own controls stay.

## Debugging

In VS Code: `Developer: Open Webview Developer Tools`, then in the console `cxClawd.V.shown` (what he shows),
`cxClawd.M` (where he is, what he's doing), `cxClawd.T` (the speech bubble). The playground
(`npm run playground`) runs the same code on a mock panel with buttons for every state.

All new class names in `custom.js` / `custom.css` start with `cx-`; check that a name isn't already used before
adding one (the footer and Clawd share these files).
