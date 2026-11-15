# extension

Patches your installed Claude Code VS Code extension so its chat panel loads `custom/custom.js` and
`custom/custom.css`, with the animations from `../animations`.

```sh
npm run build          # -> dist/claude-code-custom-<version>.vsix, made from YOUR installed Claude Code
npm run install-vsix   # installs it; then Developer: Reload Window
npm run sync           # after editing custom/ or the animations: copy them into the installed build
npm run playground     # -> playground/index.html: the real code on a mock panel, open it in a browser
```

`npm run build -- --from <folder>` patches a specific extension folder. Never share the built `.vsix`: it
contains Anthropic's code. See the main [README](../README.md) for the full install notes.
