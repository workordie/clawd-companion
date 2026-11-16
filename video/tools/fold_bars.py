"""Folds band-limited onset strength over a candidate bar length: a real bar gives a crisp, repeating pattern.

  python3 -I tools/fold_bars.py "<track>" <from_s> <to_s> <bar_s> [<bar_s> ...]
Prints, per band (kick < 150 Hz, snare/clap 1.5-5 kHz), the folded profile in 16 (or 24) slots and its contrast.
"""
import sys, subprocess
sys.path.insert(0, __import__('site').getusersitepackages())
import numpy as np
from scipy.signal import butter, sosfiltfilt

SR = 22050
path, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
bars = [float(x) for x in sys.argv[4:]]
raw = subprocess.run([(__import__('shutil').which('ffmpeg') or __import__('os').path.expanduser('~/.local/bin/ffmpeg')), '-v', 'error', '-ss', str(a), '-to', str(b), '-i', path,
                      '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
y = np.frombuffer(raw, dtype='<f4').astype(np.float64)
hop = 64
fps = SR / hop
def onset(lo, hi):
    sos = butter(4, [lo, hi], 'bandpass', fs=SR, output='sos') if lo else butter(4, hi, 'low', fs=SR, output='sos')
    x = sosfiltfilt(sos, y)
    e = np.sqrt(np.convolve(x ** 2, np.ones(256) / 256, 'same'))[::hop]
    d = np.maximum(0, np.diff(20 * np.log10(e + 1e-9), prepend=0))
    return d
bands = {'kick': onset(0, 150), 'snare': onset(1500, 5000)}
for bar in bars:
    print(f'== bar {bar:.4f} s ({240 / bar:.2f} BPM in 4/4)')
    for name, d in bands.items():
        slots = 24
        prof = np.zeros(slots)
        t = np.arange(len(d)) / fps
        idx = ((t % bar) / bar * slots).astype(int) % slots
        np.add.at(prof, idx, d)
        prof /= prof.max()
        contrast = prof.max() / prof.mean()
        print(f'  {name:5s} contrast {contrast:4.2f}  ' + ''.join(' .:-=+*#%@'[min(9, int(v * 9.99))] for v in prof))
