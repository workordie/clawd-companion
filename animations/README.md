# animations

The generator for every Clawd animation: one Python file per animation in `gen/anims/`, the pixel toolkit
`gen/clawdlib.py`, an accessory library in `gen/acc/`, and the art rules in `gen/STYLE.md`.

```sh
python3 gen/make.py                 # build everything -> svg/ (about a minute)
python3 gen/make.py idle working    # only these
python3 gen/transitions.py          # set-up / pack-away clips -> svg-tx/
python3 gen/preview.py anim idle    # contact sheet + lint -> gen/out/
```

`svg/` and `svg-tx/` are committed, so the extension works without Python. To add one, see
[../docs/add-an-animation.md](../docs/add-an-animation.md).
