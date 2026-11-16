"""Quick contact sheet for looking at frames: python3 -I tools/montage.py out.png <height> a.png b.png ..."""
import sys
sys.path.insert(0, __import__('site').getusersitepackages())
from PIL import Image

out, h, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
ims = []
for f in files:
    im = Image.open(f).convert('RGB')
    ims.append(im.resize((round(im.width * h / im.height), h), Image.LANCZOS))
sheet = Image.new('RGB', (sum(i.width for i in ims) + 10 * (len(ims) - 1), h), (60, 60, 60))
x = 0
for im in ims:
    sheet.paste(im, (x, 0))
    x += im.width + 10
sheet.save(out)
print(out, sheet.size)
