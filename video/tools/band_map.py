"""Energy per frequency band, per group of bars (dB re the loudest group in that band).

  python3 -I tools/band_map.py "<track>" <bar0 s> <bar s> <bars per row>
"""
import sys, subprocess
sys.path.insert(0, __import__('site').getusersitepackages())
import numpy as np

SR = 22050
path, d0, bar, per = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
raw = subprocess.run([(__import__('shutil').which('ffmpeg') or __import__('os').path.expanduser('~/.local/bin/ffmpeg')), '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                     capture_output=True, check=True).stdout
y = np.frombuffer(raw, dtype='<f4').astype(np.float64)
N = 4096
bands = [(20, 60), (60, 120), (120, 300), (300, 2000), (2000, 6000), (6000, 11000)]
rows = []
k = -1
while True:
    a = 0 if k == -1 else d0 + k * bar
    b = d0 + (k + per if k >= 0 else 0) * bar if k >= 0 else d0
    if k >= 0:
        b = d0 + (k + per) * bar
    seg = y[int(a * SR):int(b * SR)]
    if len(seg) < N:
        break
    fr = np.lib.stride_tricks.sliding_window_view(seg, N)[::N // 2]
    P = (np.abs(np.fft.rfft(fr * np.hanning(N), axis=1)) ** 2).mean(axis=0)
    f = np.fft.rfftfreq(N, 1 / SR)
    rows.append((k, a, [10 * np.log10(P[(f >= lo) & (f < hi)].sum() + 1e-12) for lo, hi in bands]))
    k = 0 if k == -1 else k + per
M = np.array([r[2] for r in rows])
M -= M.max(axis=0)
print('bars       start   ' + '  '.join(f'{lo}-{hi}'.rjust(9) for lo, hi in bands))
for (k, a, _), v in zip(rows, M):
    lab = 'pre' if k == -1 else f'{k}-{k + per - 1}'
    print(f'{lab:9s} {a:7.2f}   ' + '  '.join(f'{x:9.1f}' for x in v))
