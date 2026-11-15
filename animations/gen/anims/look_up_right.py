"""look-up-right: at the bottom of the panel, Clawd sizes up the input box high above him to his right.
Preview:  python3 gen/preview.py anim look-up-right

A one-shot (1950 ms), in place at HOME, standing. The patch plays it after he lands beside the input
box, then starts walk-right toward the box. look-up-left (look_up_left.py) is the mirror image.
Starts and ends in put_clawd's default standing pose with eyes open (the end pose of `land`, and the
pose the walk starts from). Normal body size throughout; the only motion of his whole body is a
1-cell hop.

STORYBOARD (ms)
     0  standing, eyes on you
   160  his eyes slide right (fine look_r): huh?
   360  he turns three-quarters toward the box (the walk's turned stance) and looks up at it (look_u),
        way up there ... 640 a slow, flat blink (half, line, half) ... still looking up
   960  turns back to you, a hand to his chin, eyes still up at the box: hmm
  1280  glances at you (eyes open, hand still at his chin): well then
  1460  determination: both arms drop (anticipation) ...
  1560  ... a tiny hop, his whole body a cell up, legs tucked, both arms pumped up
  1670  lands, arms down
  1750  plain standing, eyes open: ready to walk over there
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clawdlib import *                       # noqa: E402,F401
from anims.hop_right import turned, LEG       # noqa: E402   the walk-style turned body (shared kit)
from anims.walk_left import mirrored as flip  # noqa: E402   mirror about his home box

NAME = 'look-up-right'
STATE = 'looking up at the input box from below'
DESC = ('At the bottom of the panel: turns and looks up at the input box high on his right, hand to chin, '
        'then a determined hop. One-shot, ends standing.')

X0, Y0 = HOME

# Drawn for a box up on his LEFT (that is look-up-left), then mirrored for the right-hand version, so
# the three-quarter turn is the walk's turned body (hop_right.turned) and the glance is fine look_l.


def front(face='open', larm='side', rarm='side', legs='stand', dy=0):
    """Facing you at HOME (+dy rows). face: a FINE_EYES name, or None for the kit's plain eyes."""
    f = Frame()
    p = clawd(larm=larm, rarm=rarm, legs=legs)
    put_clawd(f, p, X0, Y0 + dy)
    ff = fine(f)
    if face:
        fine_face(ff, p, X0, Y0 + dy, face)
    return ff


def turned_up(lid='open'):
    """Turned three-quarters toward the box (left), looking up at it: the walk's turned body standing on
    straight legs, its eyes raised half a cell (look_u), or blinking ('half' / 'line') at that height."""
    return turned(kind='turned', near='rest', far='rest', expr=lid + '/u', legs=[LEG['stand']] * 4)


def frames():
    """The one-shot for a box up on his LEFT."""
    return [
        (front('open'), 160),
        (front('look_l'), 200),                              # huh? (toward the box)
        (turned_up(), 280),                                  # turns toward it, looks way up
        (turned_up('half'), 60),                             # a slow, flat blink
        (turned_up('line'), 80),
        (turned_up('half'), 60),
        (turned_up(), 120),
        (front('look_u', rarm='chin'), 320),                 # hmm (hand to chin, eyes still up)
        (front('open', rarm='chin'), 180),                   # a look at you: well then
        (front('open', larm='down', rarm='down'), 100),      # arms drop: anticipation
        (front('open', larm='up', rarm='up', legs='short', dy=-1), 110),   # hop, arms pumped up
        (front('open', larm='down', rarm='down'), 80),       # lands
        (front(None), 200),                                  # plain standing, eyes open
    ]


def look_up_frames(facing='right'):
    seq = frames()
    if facing == 'right':
        seq = [(flip(f), ms) for f, ms in seq]
    return seq


def build_look_up(facing):
    name = 'look-up-' + facing
    desc = ('At the bottom of the panel: turns and looks up at the input box high on his %s, hand to chin, '
            'then a determined hop. One-shot, ends standing.' % facing)
    return anim(name, desc, [layer('body', look_up_frames(facing))], state=STATE)


def build():
    return build_look_up('right')
