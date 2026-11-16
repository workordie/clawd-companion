"""Measure a track's tempo, beat phase and drops (read-only: ffmpeg decodes it to a pipe, nothing is written).

  python3 -I tools/measure_music.py "/path/to/Montagem Sombra.m4a"
"""
import sys, subprocess
sys.path.insert(0, __import__('site').getusersitepackages())
import numpy as np

FFMPEG = __import__('shutil').which('ffmpeg') or __import__('os').path.expanduser('~/.local/bin/ffmpeg')
SR, HOP, NFFT = 22050, 256, 2048

path = sys.argv[1]
raw = subprocess.run([FFMPEG, '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                     capture_output=True, check=True).stdout
y = np.frombuffer(raw, dtype='<f4').astype(np.float64)
dur = len(y) / SR
fps = SR / HOP

# STFT magnitude
n = 1 + (len(y) - NFFT) // HOP
win = np.hanning(NFFT)
frames = np.lib.stride_tricks.as_strided(y, shape=(n, NFFT), strides=(y.strides[0] * HOP, y.strides[0]))
spec = np.abs(np.fft.rfft(frames * win, axis=1))
freqs = np.fft.rfftfreq(NFFT, 1 / SR)
logspec = np.log1p(100 * spec)

# onset strength: positive spectral flux (all bands) + a low band (kick/808) envelope
flux = np.maximum(0, np.diff(logspec, axis=0)).sum(axis=1)
flux = np.r_[0, flux]
low = spec[:, (freqs >= 30) & (freqs <= 150)].sum(axis=1)
lowflux = np.r_[0, np.maximum(0, np.diff(np.log1p(low)))]
onset = flux / flux.max() + lowflux / lowflux.max()
onset -= np.convolve(onset, np.ones(32) / 32, 'same')  # remove slow trend
onset = np.maximum(onset, 0)

# tempo: autocorrelation over 70..200 BPM
ac = np.correlate(onset, onset, 'full')[len(onset) - 1:]
lags = np.arange(int(fps * 60 / 200), int(fps * 60 / 70) + 1)
best = lags[np.argmax(ac[lags])]
# refine with parabolic interpolation
a, b, c = ac[best - 1], ac[best], ac[best + 1]
lag = best + 0.5 * (a - c) / (a - 2 * b + c)
bpm = 60 * fps / lag
# prefer the 140-170 octave if the peak landed on a half/double
for mult in (2, 0.5):
    if 140 <= bpm * mult <= 170 and not 140 <= bpm <= 170:
        bpm *= mult
period = 60 / bpm

# refine: comb search over tempo (+-4 BPM around the autocorrelation pick, 0.02 BPM steps) and phase
t_on = np.arange(len(onset)) / fps
def comb(per):
    offs = np.linspace(0, per, 160, endpoint=False)
    sc = [np.interp(np.arange(o, dur, per), t_on, onset).mean() for o in offs]
    k = int(np.argmax(sc))
    return sc[k], offs[k]
grid = np.arange(bpm - 4, bpm + 4, 0.02)
res = [comb(60 / b) for b in grid]
k = int(np.argmax([r[0] for r in res]))
bpm, phase = grid[k], res[k][1]
period = 60 / bpm

# loudness of the low end in 0.1 s steps; drops = big jumps from quiet to loud low end
step = int(round(fps * 0.1))
dt = step * HOP / SR  # seconds per step (~0.1)
lowdb = 20 * np.log10(np.array([low[i:i + step].mean() for i in range(0, len(low) - step, step)]) + 1e-9)
lowdb -= lowdb.max()
w15 = int(round(1.5 / dt))
before = np.array([lowdb[max(0, i - w15):i].mean() if i > 0 else lowdb[0] for i in range(len(lowdb))])
after = np.array([lowdb[i:i + w15].mean() for i in range(len(lowdb))])
jump = after - before
cands = []
for i in np.argsort(-jump):
    if jump[i] < 6:
        break
    if all(abs(i - j) * dt > 4 for j, _ in cands):
        cands.append((i, jump[i]))
drops = sorted((round(i * dt, 2), round(float(j), 1)) for i, j in cands[:8])
snap = lambda t: round(phase + round((t - phase) / period) * period, 2)

print(f'file      {path.split("/")[-1]}')
print(f'duration  {dur:.2f} s')
print(f'tempo     {bpm:.2f} BPM  (beat {period:.4f} s, bar of 4 = {4 * period:.3f} s)')
print(f'phase     first beat at {phase:.3f} s  (beats at {phase:.3f} + n*{period:.4f})')
print('low-end jumps (time s, +dB over 1.5 s, snapped to beat):')
for t, j in drops:
    print(f'   {t:7.2f}  +{j:4.1f} dB   beat {snap(t):.2f}')
print('low-end level per 2 s (dB re max):')
k2 = int(round(2 / dt))
print('  ', ' '.join(f'{i * dt:.0f}:{lowdb[i:i + k2].mean():.0f}' for i in range(0, len(lowdb), k2)))
