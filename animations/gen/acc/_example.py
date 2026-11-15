"""Example accessory module (files starting with '_' are NOT loaded into the library).
Preview it with:  python3 gen/preview.py acc _example
"""
from clawdlib import Item, Sprite

# head slot: the anchor cell lands on Clawd's head-top-center pixel. Here the cuff row (row 3) is
# anchored at its center column, so the cuff overlaps his top row and the hat sits snugly.
BEANIE = Item('example_beanie', 'head', 'Example knit beanie with pom-pom (cuff overlaps his top row)', Sprite([
    '....W....',
    '...rrr...',
    '..rrrrr..',
    'RrRrRrRrR',
], anchor=(4, 3)))

# hand slot: the anchor is the grip (the handle), it lands just outside his right hand.
MUG = Item('example_mug', 'hand', 'Example mug; handle is the grip', Sprite([
    '.RdR',
    '.rrR',
    'rrrR',
    '.rrR',
], anchor=(0, 2)))

# fx slot, animated: list of sprites + suggested ms. Anchor = visual center.
STEAM = Item('example_steam', 'fx', 'Example 3-frame steam wisp', [
    Sprite(['.m.', 'm..', '.m.'], anchor=(1, 1)),
    Sprite(['..m', '.m.', 'm..'], anchor=(1, 1)),
    Sprite(['m..', '.m.', '..m'], anchor=(1, 1)),
], ms=180)

ITEMS = [BEANIE, MUG, STEAM]
