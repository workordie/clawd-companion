"""Tempo check over a section: autocorrelation peaks of the onset envelope, and the period refined over long lags.

  python3 -I tools/tempo_check.py "<track>" <from_s> <to_s> <beat guess s>
"""
import sys, subprocess
sys.path.insert(0, __import__('site').getusersitepackages())
import numpy as np

SR, HOP, NFFT = 22050, 64, 1024
path, a, b, guess = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
raw = subprocess.run([(__import__('shutil').which('ffmpeg') or __import__('os').path.expanduser('~/.local/bin/ffmpeg')), '-v', 'error', '-ss', str(a), '-to', str(b), '-i', path,
                      '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
y = np.frombuffer(raw, dtype='<f4').astype(np.float64)
n = 1 + (len(y) - NFFT) // HOP
fr = np.lib.stride_tricks.as_strided(y, shape=(n, NFFT), strides=(y.strides[0] * HOP, y.strides[0]))
spec = np.log1p(100 * np.abs(np.fft.rfft(fr * np.hanning(NFFT), axis=1)))
on = np.r_[0, np.maximum(0, np.diff(spec, axis=0)).sum(axis=1)]
on -= np.convolve(on, np.ones(64) / 64, 'same')
on = np.maximum(on, 0)
fps = SR / HOP
ac = np.correlate(on, on, 'full')[len(on) - 1:]
ac /= ac[0]
lags = np.arange(int(0.2 * fps), int(3.2 * fps))
seg = ac[lags]
peaks = [i for i in range(1, len(seg) - 1) if seg[i] > seg[i - 1] and seg[i] >= seg[i + 1]]
top = sorted(peaks, key=lambda i: -seg[i])[:8]
print(f'{path.split("/")[-1]} {a}-{b} s: strongest autocorrelation lags:',
      ', '.join(f'{lags[i] / fps:.4f}s ({seg[i]:.2f})' for i in sorted(top)))
for k in (1, 2, 4, 8, 16, 32):
    c = guess * k * fps
    w = int(0.03 * k * fps) + 3
    lo, hi = int(c - w), int(c + w) + 1
    if hi >= len(ac):
        break
    j = lo + int(np.argmax(ac[lo:hi]))
    p, q, r = ac[j - 1], ac[j], ac[j + 1]
    off = 0.5 * (p - r) / (p - 2 * q + r) if (p - 2 * q + r) != 0 else 0
    lag = (j + off) / fps
    print(f'  {k:2d} beats: lag {lag:.4f} s -> beat {lag / k:.5f} s = {60 * k / lag:.3f} BPM')
