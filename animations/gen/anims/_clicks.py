"""Click reactions registry (DRAFTS; '_' files are skipped by make.py). The reactions live in
_clicks_1.py and _clicks_2.py, the shared kit in _click_kit.py.

You click Clawd, he reacts once, then the patch goes back to whatever was playing. The patch picks one
at random per click; `click-dizzy` is meant for rapid repeated clicks.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims._click_kit import B, FX, TXT, compose, blink  # noqa: E402,F401  (re-exported for _drag.py)
from anims._clicks_1 import hop, wave, hug, dizzy, hide, party  # noqa: E402
from anims._clicks_2 import spin, giggle, shrug, idea, poof, groove  # noqa: E402


REACTIONS = {
    'click-hop': (hop, 'Startled boop: flinch, a hop under a popping red "!", dust landing, looks up at your cursor.'),
    'click-wave': (wave, 'Looks up and waves back; a heart pops from his hand and drifts away, his eyes following it.'),
    'click-hug': (hug, 'Arms open wide, then a big self-hug and sway while a heart beats above him and floats away.'),
    'click-dizzy': (dizzy, 'Rapid clicks: bonk, stars circle his head while his eyes roll, he shakes it off and the stars fly away.'),
    'click-hide': (hide, 'Peek-a-boo: ducks behind the input box, creeps back up to peek over the edge, pops out.'),
    'click-party': (party, 'Wind-up, big jump, a confetti fountain that flutters down behind the input box, sparkly eyes.'),
    'click-spin': (spin, 'Eyes lead into two turns (slow, fast, slow) with whoosh streaks, a skidding stop, a tiptoe ta-da.'),
    'click-giggle': (giggle, 'Eep! Then three shrinking bursts of wriggling, holding his tummy, while rust "HA"s pop out and fizzle.'),
    'click-shrug': (shrug, 'Glances left and right, a "?" pops up, a dip and a shrug with "dunno" eyes; the "?" hops off.'),
    'click-idea': (idea, 'Ponders, a light bulb rises out of his head and switches on, he points at it; it pops into a sparkle.'),
    'click-poof': (poof, 'Magic trick: poofs away, a twinkle hints where, pops up to the right, looks around, poofs home.'),
    'click-groove': (groove, 'Bobs on a steady beat, one arm pumping per beat, notes popping up on the beats.'),
}


def build_reaction(name):
    fn, desc = REACTIONS[name]
    return anim(name, desc, [layer('body', fn())], state='clicked (one-shot)')
