"""Temp sound bed for review: synthesised SFX on the brief's cue frames plus a quiet
120 BPM guide pulse (beats every 15 frames, so scene changes at f60/135/195/240 land
on beats). Replace with the licensed track + SFX for the master.

    python3 sfx.py out.wav
"""
import sys, wave
import numpy as np

SR, FPS, DUR = 48000, 30, 10.0
N = int(SR * DUR)
mix = np.zeros(N)
rng = np.random.default_rng(3)
fr = lambda f: int(f / FPS * SR)


def put(sig, f, gain=1.0):
    i = fr(f); j = min(N, i + len(sig))
    mix[i:j] += sig[: j - i] * gain


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def lowpass(x, a):
    y = np.zeros_like(x); acc = 0.0
    a = np.broadcast_to(a, x.shape)
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc); y[i] = acc
    return y


def whoosh(dur, up=True):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    sweep = (0.02 + 0.25 * t) if up else (0.27 - 0.25 * t)
    s = lowpass(rng.standard_normal(n), sweep)
    return s * np.sin(np.pi * t) ** 2 * 3


def tick(freq=3200):
    n = int(SR * 0.012); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * freq * t) + 0.5 * rng.standard_normal(n)) * env(n, 0.0005, 0.003)


def tap(freq=820):
    n = int(SR * 0.12); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 1.7 * t)
    return s * env(n, 0.001, 0.025) + 0.3 * rng.standard_normal(n) * env(n, 0.0002, 0.004)


def chime():
    n = int(SR * 1.4); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(1568, 1), (2349, .6), (3136, .4), (4699, .2)])
    return s * env(n, 0.002, 0.45)


def click():
    return tick(2400) + np.concatenate([np.zeros(int(SR * .018)), tick(1800)])[: len(tick(2400))] * 0 + tick(1800) * .6


def kick():
    n = int(SR * 0.3); t = np.arange(n) / SR
    f = 50 + 90 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.12)


def hat():
    n = int(SR * 0.05)
    return np.diff(rng.standard_normal(n + 1)) * env(n, 0.0005, 0.012)


# guide pulse: kick on beats, soft hat on off-beats
for b in range(20):
    put(kick(), b * 15, 0.22)
    put(hat(), b * 15 + 7.5, 0.05)

put(whoosh(0.45), 38, 0.25)                    # f45 footage shrinks into its tile
for f in range(66, 89, 2):                     # f66–88 odometer ticks
    put(tick(), f, 0.18)
put(whoosh(0.6, up=False), 128, 0.3)           # f135 pan
for i in range(6):                             # digits land (140 + 3i + ~6)
    put(tap(760 + 40 * i), 146 + 3 * i, 0.35)
for f in range(156, 168):                      # coin roll
    put(tick(1400 + 60 * (f % 3)), f, 0.08)
put(chime(), 168, 0.16)                        # gleam
put(whoosh(0.5), 190, 0.22)                    # pull-back
for f in (214, 218, 222, 226, 230, 234):       # checkbox ticks
    put(click(), f, 0.25)
n = int(SR * 0.4); t = np.linspace(0, 1, n)    # f240 rising swell into the logo
swell = (lowpass(rng.standard_normal(n), 0.03 + 0.2 * t) * 2 + 0.3 * np.sin(2 * np.pi * np.cumsum(200 + 600 * t) / SR)) * t ** 2
put(swell, 242, 0.3)

fade = int(SR * 0.25); mix[-fade:] *= np.linspace(1, 0, fade)
mix *= 0.8 / max(1e-9, np.abs(mix).max())
pcm = (np.stack([mix, mix], 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
