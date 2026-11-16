# clawd-companion · showcase video · storyboard

**Look:** the A → B mix, in the user's own theme, **Default High Contrast Light**. Each cut opens in VS Code with the
real Claude Code panel (A). It
punches in on the beats and lands on the close-up (B) on the track's first drop. The body plays on B. It comes back to
the panel for the /btw bubble (A, 3x / 9:16 2x) and the input footer (A2: the panel wide enough for its full 680 px
box), and the finale is on B.

**The input box is the real one, everywhere.** Every panel in the video (its box, footer, chat, the /btw bubble) is
the installed extension's own UI with the clawd-companion patch, captured from the real thing, not drawn (see "The
real panel" below). Only Clawd is drawn by the video, with the patch's own animations.

**Music:** "Technology" by Sub_Clair ([Pixabay](https://pixabay.com/music/future-bass-technology-623486/), Pixabay Content License).
- The file is `out/track/sub_clair-technology-623486.mp3`. It stays in `out/`: Pixabay forbids redistributing the
  track, so it must not go into git or be copied anywhere public.
- Previews: `out/preview-16x9.mp4` (960x540) and `out/preview-9x16.mp4` (540x960), with the track.

## The commands

| What | Command |
|---|---|
| the real panel's states (once, and after the extension or the patch changes) | `cd ~/Projects/clawd-companion/video && node tools/realbox/capture-states.mjs` |
| check them against the live panel | `node tools/realbox/verify.mjs` · `node tools/realbox/check-scale.mjs` (1x, 2x, 4x, 6x) |
| check the box against the user's screenshot | `node tools/realbox/check-user.mjs` → `out/realbox/check-vs-user.png` |
| final 16:9 (one line) | `cd ~/Projects/clawd-companion/video && node build.mjs && node capture.mjs --style mix --cut wide --video out/clawd-companion-16x9.mp4 --music out/track/sub_clair-technology-623486.mp3 --music-start 16.326` |
| final 9:16 | `node capture.mjs --style mix --cut tall --video out/clawd-companion-9x16.mp4 --music out/track/sub_clair-technology-623486.mp3 --music-start 29.766` |
| preview (half size) | add `--preview` |
| a still | `node capture.mjs --style mix --cut wide --still 15.36` |
| the timeline | `node capture.mjs --style mix --cut wide --dump` |
| same t twice = same PNG? | `--determinism <t>` |
| other themes | `--theme light` (Light Modern) · `--theme dark` (Dark Modern); default `hc-light` |

`--music-start` is where in the file the video's t = 0 sits; the cut's own fade runs at the end. The track is cut
with `-ss`/`-t` on its input and muxed without `-shortest` (with a seeked MP3, `-shortest` ended the audio about
7 s early). Sync on both previews measures 0 ms at the start, middle and end. Each frame is
`seek(t)` + a screenshot (headless Chrome, one at a time) piped into ffmpeg: x264 CRF 12 for the final, no size target.
Expect about 11 min (16:9) and 5 min (9:16) at full size. `node build.mjs` writes `out/showcase.html` (git-ignored: it
carries the extension's CSS and DOM).

## The real panel (`tools/realbox/`, `src/realpanel.js`)

- **Captured from the real thing.** `capture-states.mjs` runs the installed extension's own webview (`index.js` +
  `index.css`, read only, nothing copied into the repo) with the patch (`custom.js` + `custom.css`) in headless Chrome,
  with a stand-in for the VS Code side (`host.js`: a signed-in user, the model list with "Fable 5.2" and its effort
  levels, Auto and Bypass in the mode menu, Remote Control on). Two footer states, as the stub would have them:
  the user's own resumed chat (`setup-screenshot.js`: cache "cold", context "–", effort High) for B and A2, and a
  brand-new chat (`setup-newchat.js`: no cache record yet, so no clock; context 0%) for the opener.
  It then does what a user does (types the prompt, presses Enter, clicks Clawd for /btw, asks, hovers and drags the
  effort slider, clicks Ultracode and the context ring) and saves the panel's DOM after each step, Clawd taken out.
- **The theme** is VS Code's own, the user's Default High Contrast Light: every `--vscode-*` variable computed like VS
  Code does (`theme.mjs` runs VS Code's colour registry and Color code from its installed bundle over
  `hc_light.json`), its webview default styles, and the body classes its webview host sets (`vscode-high-contrast-light
  vscode-high-contrast`, data-vscode-theme-kind/name/id). Look A's window takes the same computed colours (title bar,
  activity bar, tabs with the red active top border, breadcrumbs, line numbers, the current line's 2 px border, status
  bar, HC's 1 px contrast borders) and the code `hc_light.json`'s tokenColors.
- **In the video,** each look holds the panel in an iframe with the real CSS and swaps those snapshots. The video only
  sets what the real panel's code would: the typed text (in the input and its mention mirror), focus / hover / pressed
  (the real `:focus`, `:hover`, `:active` rules, also matched by `data-rb-*` attributes so a frame never depends on a
  mouse), the spinner's glyph and word (the panel's own sequence), the caret, the bubble's position from Clawd (the
  patch's `placeTalk`), and the times of the real CSS animations (Ultracode, the pops, the agents dot).
- **Panels:** `a-wide` 600x453 (16:9 A, beside the editor: the footer's compact layout), `a-tall` 540x613 (9:16 A: the
  patch's narrow layout), `stage` 849x700 (B at 6x and A2 at 4x: the full 680 px box, 84 px to the column's right side,
  16 px above its bottom, a short chat history far above). The world Clawd moves in is taken from it: the floor is the
  column's bottom, 89 px under his surface (was 90: three of his clip changes in 16:9 come 1-3 frames earlier).
- **Checked:** `verify.mjs` rebuilds every state the video's way and compares it with the live panel (0 px differ, or
  only where something animates: the spinner, the caret). `check-scale.mjs` compares the video's box with the live
  panel rendered at the same scale: **0 px differ at 1x, 2x, 4x and 6x** (sheets in `out/realbox/check-*x.png`).

## The track, measured (`tools/`)

- **Tempo.** A steady **125.0 BPM**: beat 0.48 s, bar 1.92 s.
  - The beat-grid fit has contrast 11.3, against 7.1 for the 166.7 BPM octave the autocorrelation first suggested.
  - Every section's onset lands within ±18 ms of the 125 BPM grid.
  - The snare pattern repeats every 0.96 s, half a bar.
- **Bar grid.** Bar k's downbeat is at **0.966 + 1.92·k s** (bar 0 = 0.966 s). There's a short pickup before it.
- **Shape**, in 8-bar phrases:

  | Bars | Time in the track (s) | What happens |
  |---|---|---|
  | 0–7 | 0.97–16.33 | intro: bass, then hats from bar 4 |
  | 8–15 | 16.33–31.69 | build; on bars 14–15 the bass cuts out on beats 3–4 |
  | 16 | **31.686** | **DROP 1**; full to bar 23 |
  | 24 | 47.05 | the drums drop out (breakdown) |
  | 32 | 62.41 | the bass drops too (the calm part) |
  | 40–47 | 77.77–93.13 | lift: everything back and building, the same bass cuts on bar 47 |
  | 48 | **93.126** | **DROP 2**; full to bar 55 |
  | 56–63 | 108.49–123.85 | outro: drums out |
  | 64 | 123.846 | the last hit, then a 1.5 s tail to the end at 125.33 |

## 16:9 cut, 109.0 s

It starts at **16.326 s** in the track (bar 8): the build's 8 bars carry the VS Code opener. It runs to the track's own
ending, with a 0.3 s safety fade. Bar k is at 1.92·(k − 8) s. "Flash" means a blink and shake (B only).

| # | Bars | Video (s) | Look | What's on screen | Clawd's clips | Captions |
|---|---|---|---|---|---|---|
| 1 | 8–9 | 0.00–3.84 | A 2x | The whole window, an empty session. He peeks up from behind the box. | hello-peek | 0.00 "meet Clawd." · *Claude Code’s mascot, / on your input box* |
| 2 | 10–11 | 3.84–6.68 | A 2x | The prompt is typed into the real box, with the mode ring lit. | in-typing-juggle → **typing-juggle** | 3.84 "you type, / Clawd juggles / the letters." |
| 3 | 12–13 | 6.68–11.52 | A 2x | Sent: "Thinking…". | out/in → **thinking-gears** (7.68) | 6.68 "Claude thinks. so does Clawd." |
| 4 | 14 | 11.52–13.44 | **A 4x** | Punch in on the build's bass cuts. | thinking-gears | |
| 5 | 15 | 13.44–15.36 | **A 6x** | Punch in close: the gears pack away and the forge sets up for the drop. | out-thinking-gears → in-working-forge (14.61) | 14.61 "Claude works. so does Clawd." |
| 6 | 16–23 | 15.36–30.72 | **B** | **DROP 1: match cut to the stage** (flash). A state every 2 bars, each set up and packed away. | **working-forge** → alert-bell (19.20) → question-lens (23.04) → done (26.88) | 18.65 "needs your OK? Clawd rings." · 22.34 "a question for you? Clawd waits." · 26.03 "done? party." |
| 7 | 24–25 | 30.72–34.08 | B | **The drums drop out.** He wanders to the edge and teeters. | walk-right → teeter-right (32.33) | 30.72 "nothing to do? Clawd wanders off." · 32.64 "uh oh." |
| 8 | 25–31 | 34.08–46.08 | B | Off he hops (bar 25, beat 4), falls, lands, looks up, walks to the wall and **climbs it like a crab**. | hop-right → fall → land → look-up-left (36.77) → walk-left (38.72) → **climb-left** (42.41) | 33.93 "Clawd hops off." · 38.72 "…and walks back up the wall." · 42.41 "like a crab." |
| 9 | 32 | 46.08–48.00 | B | **Over the top as the bass drops.** He walks home. | walk-left | 46.08 "home again." |
| 10 | 33–35 | 48.00–53.76 | B | Flip-book: a version a beat (12). | thinking-chalk, working-chef, idle-kite, … | 48.00 "every state has versions." |
| 11 | 36–39 | 53.76–61.44 | B | Set-up and pack-away, a scene a bar. | working-chef → working-lab → thinking-cube → done-flag | 53.76 "props drop in and poof away." |
| 12 | 40–45 | 61.44–72.96 | B | **The lift:** hover, grab, shake, throw (flash), drop from high, pop the chute. | notice · grabbed · grabbed-dizzy · tumble/crash · fall/parachute/chute-pop | 61.44 "hover over Clawd: Clawd notices you." · 63.36 "grab Clawd." · 65.28 "shake Clawd." · 67.20 "throw Clawd." · 69.11 "drop Clawd / from up high." · 71.04 "pop the chute. (sorry)" |
| 13 | 46–48 | 72.96–78.72 | **A 2x** | Back in the real panel: click, the /btw bubble (the panel's own side question), the question, "Answering…" through the bass cuts. **The answer lands on DROP 2 (76.80).** | talk-listen → talk-think → **talk-explain** | 72.96 "click Clawd: ask a side question." · 76.80 "Claude answers, in Clawd’s bubble." |
| 14 | 49–50 | 78.72–82.56 | **A2 4x** | The footer's mode, 2 beats each: Plan, Auto-edit, Bypass, Auto (ring, dot and name). | plan · edits · bypass · auto-cloud | 78.72 "switch modes, Clawd switches jobs." |
| 15 | 51–53 | 82.56–88.32 | A2 4x | **Effort slider:** a level per beat, Low → Medium → High → Extra high → Max, with Max's "uses many more tokens". | idle | 82.56 "drag the effort slider." |
| 16 | 54–55 | 88.32–92.16 | A2 4x | **Ultracode:** a click on beat 3, the dot wave, then the purple edge and glint. | idle | 88.32 "turn on Ultracode." |
| 17 | 56–57 | 92.16–96.00 | A2 4x | **The outro starts.** The ring's "Compact this chat?" confirm, then Cancel; agents go 0 → 2. | idle | 92.16 "click the context ring to compact." · 95.04 "usage and subagents, at a glance." |
| 18 | 58–59 | 96.00–99.84 | B | The wall of animations. | — | "199 pixel-art animations." |
| 19 | 60–61 | 99.84–103.68 | B | Nap time. | in-sleep-camp → sleep-camp | 99.14 "away a while? nap time." |
| 20 | 62– | 103.68–109.00 | B | **End card** to the track's own ending (he stands on a shelf: no drawn box). | hello-hat → idle | clawd-companion · `github.com/workordie/clawd-companion` · unofficial fan project |

## 9:16 cut, 48.0 s

It starts at **29.766 s** in the track (bar 15), so **DROP 1 hits at 1.92 s**. It ends as the calm bar 39 fades out
(bar 40 = 48.0 s; the fade runs 1.92 s). Bar k is at 1.92·(k − 15) s.

| # | Bars | Video (s) | Look | What's on screen | Clawd's clips | Captions |
|---|---|---|---|---|---|---|
| 1 | 15 | 0.00–1.92 | **A 2x → 4x (0.96) → 6x (1.44)** | The real panel, Claude thinking. Punch-ins on beats 3 and 4 (the build's bass cuts). | thinking-gears | 0.00 "Clawd lives on your input box now." · *Claude Code · VS Code* |
| 2 | 16–19 | 1.92–9.60 | **B** | **DROP 1: match cut** (flash). The gears pack away and the forge drops in on beat 4; then a state a bar. | out (2.11) → in-working-forge (2.61) → **working-forge** (3.36) → alert-bell (5.76) → done (7.68) | 2.61 "Claude works. so does Clawd." · 5.76 "needs your OK? Clawd rings." · 7.68 "done? party." |
| 3 | 20–22 | 9.60–15.36 | B | To the edge, a teeter, off (bar 21, beat 3), a fall and a landing. | walk-right → teeter-right → hop-right → fall → land | 9.60 "nothing to do? Clawd wanders off." · 11.52 "uh oh." · 12.33 "Clawd hops off." |
| 4 | 23–24 | 15.36–19.20 | B | Jump cut to the wall: up it like a crab, over the top on bar 24, beat 3 (the drums are out). | **climb-left** → walk-left | 15.36 "…and walks up / the wall, / like a crab." |
| 5 | 25–27 | 19.20–24.96 | B | Grab, shake, throw (flash). | grabbed → grabbed-dizzy → tumble/crash | 19.20 "grab Clawd." · 21.12 "shake Clawd." · 23.04 "throw Clawd." |
| 6 | 28–29 | 24.96–28.80 | **A 2x** | The /btw bubble (the whole bubble fits at 2x); the answer lands on bar 29. | talk-* | 24.96 "click Clawd: ask a side question." · 26.88 "Claude answers, in Clawd’s bubble." |
| 7 | 30 | 28.80–30.72 | **A2 4x** | The footer's mode, a beat each. | plan · edits · bypass · auto-cloud | 28.80 "switch modes, Clawd switches jobs." |
| 8 | 31–33 | 30.72–36.48 | A2 4x | **Effort slider**, a level per beat, with Max's note. | idle | 30.72 "drag the effort slider." |
| 9 | 34–35 | 36.48–40.32 | A2 4x | **Ultracode** (the bass is down: a calm wave). | idle | 36.48 "turn on Ultracode." |
| 10 | 36–37 | 40.32–44.16 | B | The wall. | — | "199 pixel-art animations." |
| 11 | 38–39 | 44.16–48.00 | B | **End card**; the fade runs over bar 39. | hello-hat → idle | end card |

To fit 48 s, the 9:16 cut leaves out the look-up and walk to the wall (jump cut), the parachute, the versions
flip-book, the props scene changes, nap time and the footer tour. Set-up and pack-away still show in the drop's
gears → forge change.

## Footer segment (step 4; now inside both cuts, A2, on the beat)

These are the input footer's own features, in look A (light), at 4x on the footer. They are their own cuts,
`footer-wide` (16:9) and `footer-tall` (9:16), 16 s each, until the edit is re-timed to the new track.

- **Layout.** The window is wide and the box is at its real full width (680 px), so the footer shows its full set,
  left to right: + · / · context ring "–" · clock "cold" (cache) · usage bars · agents "0" · Remote (phone, blue
  dot) · spacer · "Fable 5.2 ⌄" · Ultracode · effort slider · "● Auto ⌄" · send.
- **The real footer.** Since step 6 every footer state is the real panel's own (captured, see "The real panel"):
  the extension's +, /, cache clock, Remote Control and send, the patch's ring, usage, agents, Ultracode and slider,
  in their real places and colours. The smaller panels use the patch's own compact and narrow layouts.

| Scene | Footer t (s) | Camera | What happens (as the patch draws it) | Caption |
|---|---|---|---|---|
| Effort | 0.0–5.6 | 4x on the slider | See below. | "drag the effort slider." · *low · medium · high · extra high · max* |
| Ultracode | 5.6–10.4 | 4x on the button | See below. | "turn on Ultracode." · *dynamic workflows on every task (this session only)* (the patch's own tooltip) |
| Tour | 10.4–16.0 | 4x on the left half | See below. | "click the context ring to compact." · 13.3 "usage and subagents, at a glance." |

- **Effort.**
  - The pointing hand goes onto the thumb, and the level bubble pops in 6 px above it: "● Medium".
  - It presses (thumb 1.3x), then drags down to Low and up a level at a time: Medium, High, Extra high, Max. The
    track fill, thumb and dot take each level's colour: purple, blue, green, yellow, red.
  - On Max the bubble adds "uses many more tokens". Then it releases and moves away.
- **Ultracode.**
  - A click on Ultracode: the button pops and turns purple.
  - A bloom, then three waves of purple dots run through the box, with its border lighting where they reach.
  - From 1.6 s the purple edge fades in, with one glint circling every 9 s and a soft glow under the box breathing
    every 5 s.
- **Tour.**
  - A click on the context ring opens the "Compact this chat?" confirm above it ("Claude summarizes the conversation so
    far to free up context.", Compact / Cancel), then Cancel closes it.
  - Then subagents start: the agents counter goes 0 → 2 with its pulsing green dot. Ultracode stays on.

Files are in `out/footer/`:

| What | Files |
|---|---|
| stills | `{effort,ultracode,tour}-{16x9,9x16}-*.png` |
| silent half-size clips | `{effort,ultracode,tour}-{16x9,9x16}.mp4` |
| a clip again | `node capture.mjs --style mix --cut footer-wide --video out/footer/effort-16x9.mp4 --from 0 --to 5.6 --preview` |

## Changed in step 8 (layering, tabs, captions)

- **Clawd is mounted in the real panel** the way the patch mounts him: a `.cx-clawd` element first in the input box
  (after the Ultracode edge layers, before the box's background), placed by the patch's own CSS (top -60px, right
  10px) and moved by `--cx-x` / `--cx-y`. So the effort bubble and the compact confirm (z-index 60 in the box), the /btw
  bubble (fixed, z-index 40) and the extension's menus draw over him, as in the real panel; he stays inside the chat
  column. His image still lands on whole screen pixels.
- **The editor tabs** are VS Code's: file icon, name, a close button on the active tab, HC's right borders and the
  active tab's 1 px red top line; the Claude Code tab has the extension's own icon (`resources/claude-logo.svg`).
- **Captions call Clawd by name** (never he / him / his), break only where they're written (no automatic wrapping,
  no one-word lines, no line starting with "·"), and never touch a UI edge or line: `tools/check-captions.mjs`
  measures each caption against every visible line (window parts, the panel's boxes and popups, B's floor and wall)
  over its whole time on screen. A's cards sit on the editor's code at 2x; the 16:9 /btw shot is 2x (was 3x) so its
  caption can sit there too. Every typed caption finishes typing at least 0.7 s before the next one.

## Changed in step 7 (the user's theme)

- **Default High Contrast Light everywhere** (the user's `settings.json`), computed from VS Code's own theme files:
  the panel (every state re-captured in it), look A's whole window, and B's surround (the panel's white, its edges in
  the contrast border).
- **Checked against the user's screenshot** (`out/realbox/check-vs-user.png`: theirs, ours, the difference): the box
  680 x 74 px in both, colours within the screenshot's display-profile shift (border #0c427a / #0f4a85, cold and Auto
  #ad1d12 / #b5200d, placeholder #666 / #696969, slider #2c3a0e / #30400c), every footer item within 1 px.
- **Effort High**, as in the screenshot (the slider's middle step, charts-green); their Claude settings say Extra
  high, the screenshot's session ran High.
- **The opener's chat is brand new**: the real footer has no cache clock before Claude's first reply and the ring
  says 0%. B and the footer close-ups keep the screenshot's state ("–", cold).

## Changed in step 6 (the real input box)

- **Every box is the real one** (see "The real panel"). Gone: captions typed into the box (B), the clip-name pill and
  the "● Manual" chip (B), the hand-made footer, the hand-made /btw bubble and the end card's drawn box. Captions sit
  above the box (B) or on the editor / in the band (A).
- **What the box shows follows the story:** idle ("⌘ Esc to focus or unfocus Claude"); the prompt typed, focused;
  Claude on it ("Queue another message…", the stop button) in the opener, the /btw scene and B's states scene while
  Clawd works, rings or waits; the footer's own states in A2. A's chat is the real one too: the prompt, Claude's
  spinner, Remote Control's line, and (A2, B) his finished reply.
- **Talk framing:** the real bubble is bigger than the old drawn one, so the /btw shot is 3x in 16:9 (was 4x) and 2x
  in 9:16 (was 4x), with the whole bubble and Clawd in frame. Timing unchanged.
- **build.mjs** writes `out/showcase.html` (it now carries the extension's CSS and DOM: never in git).

## Changed in step 3 (white mode, the soundtrack)

- **White mode everywhere:** A in Light Modern, B a white stage, the wall and end card white. Clawd is unchanged. On
  white, the drop flash became a short dark blink.
- **Captions.** They now switch with their scene's set-up clip or the scene start, whichever is first. They used to lag
  the picture, for example "a question for you?" while in-done was already setting up. The moved times are in the
  tables (16:9: 10 captions; 9:16: 4).
  - Kept: "uh oh." stays mid-teeter (27.2 / 9.6). Moving it to the teeter's start would leave "nothing to do? he
    wanders off." up for 0.65 s, shorter than it takes to type in.
  - Unchanged: scenes, clip segments and flashes are identical to `out/timeline-*.json` (checked with `--dump`).
- **capture.mjs.** `--music <file>` (from t = 0, with the cut's fade); no file means silent. The placeholder track is
  out of the code.

## Changed from the step-1 storyboard

- **Look.** It was one look per video; now it's the A → B → A → B mix. A gained camera zooms (2x/4x/6x hard cuts) and a
  real empty-session opener (hello, a typed prompt, thinking).
- **16:9 start.** It now starts on grid bar 9 (15.948 s) instead of 0 s, so the A opener is about 10 s and the
  punch-ins sit in the hush right before the main drop. The drop is now the match cut to the stage (Claude works), and the hop-off
  moved to bar 26.
- **16:9 length and ending.** It's 88.0 s and ends on the end card at bar 60 (the plan's biggest section), with a
  two-bar fade.
- **9:16 length and ending.** It's 54.4 s (was 45 s) and ends on the bar-48 break instead of fading mid-groove. It gains
  the real-panel bubble and modes and drops vibe.
- **Captions** rechecked against `custom.js`:
  - "he even vibes to your phonk" is gone: nothing in the patch triggers vibe. It only appears in the wall.
  - "he answers" became "Claude answers, in his bubble".
  - "199 hand-made…" became "199 pixel-art animations" (the set-up and pack-away clips are generated).
  - The done state shows `done` (confetti), not `done-party`, which needs a 2-minute turn.
- **Repo URL:** `github.com/workordie/clawd-companion`.

## Open

- In 9:16 the Ultracode shot keeps Clawd off-frame (the camera is on the button), as in the approved footer clip.
- The cursor is pixel art. The wall pans one column per beat.
- In 9:16, the modes shot sits near the window's right edge (the camera is clamped to the window).
