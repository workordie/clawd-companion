"""Beat phase at a fixed BPM, and the exact onsets of the drops on that grid (read-only; ffmpeg pipe).

  python3 -I tools/drops_on_grid.py "<track>" <bpm> <approx drop s> [<approx drop s> ...]
"""
import sys, subprocess
sys.path.insert(0, __import__('site').getusersitepackages())
import numpy as np
from scipy.signal import butter, sosfiltfilt

SR, HOP, NFFT = 22050, 64, 1024
path, bpm = sys.argv[1], float(sys.argv[2])
approx = [float(x) for x in sys.argv[3:]]
raw = subprocess.run([(__import__('shutil').which('ffmpeg') or __import__('os').path.expanduser('~/.local/bin/ffmpeg')), '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                     capture_output=True, check=True).stdout
y = np.frombuffer(raw, dtype='<f4').astype(np.float64)
dur = len(y) / SR
fps = SR / HOP
n = 1 + (len(y) - NFFT) // HOP
fr = np.lib.stride_tricks.as_strided(y, shape=(n, NFFT), strides=(y.strides[0] * HOP, y.strides[0]))
spec = np.log1p(100 * np.abs(np.fft.rfft(fr * np.hanning(NFFT), axis=1)))
on = np.r_[0, np.maximum(0, np.diff(spec, axis=0)).sum(axis=1)]
on -= np.convolve(on, np.ones(64) / 64, 'same')
on = np.maximum(on, 0)
t = (np.arange(len(on)) * HOP + NFFT / 2) / SR
per = 60 / bpm
offs = np.arange(0, per, 0.002)
sc = np.array([np.interp(np.arange(o, dur, per), t, on).mean() for o in offs])
ph = offs[int(np.argmax(sc))]
# 16th-note check: the phase of the strongest 16th
print(f'{path.split("/")[-1]}: {bpm} BPM, beat {per:.4f} s, grid phase {ph:.3f} s (contrast max/mean {sc.max() / sc.mean():.2f})')
# low-band envelope for the drop onsets
lowp = sosfiltfilt(butter(4, 120, 'low', fs=SR, output='sos'), y)
e = np.sqrt(np.convolve(lowp ** 2, np.ones(256) / 256, 'same'))[::HOP]
edb = 20 * np.log10(e + 1e-9)
te = np.arange(len(edb)) * HOP / SR
for d in approx:
    m = (te > d - 1.0) & (te < d + 1.0)
    rise = np.diff(edb[m], prepend=edb[m][0])
    rise = np.convolve(rise, np.ones(4), 'same')
    k = int(np.argmax(rise))
    onset = te[m][k]
    beat = round((onset - ph) / per)
    g = ph + beat * per
    print(f'  drop ~{d:6.2f}: low-end onset {onset:7.3f} s -> beat #{beat} at {g:7.3f} s (off {1000 * (onset - g):+.0f} ms), bar {beat // 4} beat {beat % 4 + 1}')
