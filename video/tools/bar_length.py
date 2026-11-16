"""Bar length from long-lag autocorrelation of the onset envelope (read-only; ffmpeg decodes to a pipe).

  python3 -I tools/bar_length.py "<track>" <from_s> <to_s>
"""
import sys, subprocess
sys.path.insert(0, __import__('site').getusersitepackages())
import numpy as np

SR, HOP, NFFT = 22050, 64, 1024
path, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
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
out = []
for k in (1, 2, 4, 8, 16):
    c = int(1.6 * k * fps)
    w = int(0.06 * k * fps) + 3
    seg = ac[c - w:c + w + 1]
    j = int(np.argmax(seg))
    if 0 < j < len(seg) - 1:
        p, q, r = seg[j - 1], seg[j], seg[j + 1]
        off = 0.5 * (p - r) / (p - 2 * q + r)
    else:
        off = 0
    lag = (c - w + j + off) / fps
    out.append((k, lag, 240 * k / lag))
print(f'{path.split("/")[-1]}  {a}-{b} s')
for k, lag, bpm in out:
    print(f'  {k:2d} bar(s): lag {lag:.4f} s -> bar {lag / k:.4f} s = {bpm:.2f} BPM')
