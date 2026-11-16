"""Per-bar energy map on a fixed grid (read-only; ffmpeg pipe).

  python3 -I tools/bar_map.py "<track>" <first downbeat s> <bar s> [<bars>]
"""
import sys, subprocess
sys.path.insert(0, __import__('site').getusersitepackages())
import numpy as np
from scipy.signal import butter, sosfiltfilt

SR = 22050
path, d0, bar = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
raw = subprocess.run([(__import__('shutil').which('ffmpeg') or __import__('os').path.expanduser('~/.local/bin/ffmpeg')), '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                     capture_output=True, check=True).stdout
y = np.frombuffer(raw, dtype='<f4').astype(np.float64)
lo = sosfiltfilt(butter(4, 120, 'low', fs=SR, output='sos'), y)
hi = sosfiltfilt(butter(4, 2000, 'high', fs=SR, output='sos'), y)
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
ref_all, ref_lo, ref_hi = db(y), db(lo), db(hi)
nb = int(sys.argv[4]) if len(sys.argv) > 4 else int((len(y) / SR - d0) / bar) + 1
print(f'{"bar":>4} {"start":>7}  {"all":>5} {"low":>5} {"high":>5}  low-end meter')
for k in range(-1, nb):
    a, b = d0 + k * bar, d0 + (k + 1) * bar
    if k == -1:
        a = 0
    s = y[int(a * SR):int(b * SR)]
    if len(s) < SR // 10:
        break
    l, h = lo[int(a * SR):int(b * SR)], hi[int(a * SR):int(b * SR)]
    L = db(l) - ref_lo
    print(f'{k:4d} {a:7.3f}  {db(s) - ref_all:5.1f} {L:5.1f} {db(h) - ref_hi:5.1f}  ' + '#' * max(0, int(30 + L)))
