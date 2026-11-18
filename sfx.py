"""Soft SFX bed that sits under the voiceover (audio/voiceover.wav), on the film's cue frames.
Temp sounds for review; swap for the licensed track + SFX in the final mix.

    python3 sfx.py out.wav
"""
import sys, wave
import numpy as np

SR, FPS, DUR = 48000, 30, 14.4
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
    s = lowpass(rng.standard_normal(n), (0.02 + 0.25 * t) if up else (0.27 - 0.25 * t))
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
    return sum(a * np.sin(2 * np.pi * f * t) for f, a in [(1568, 1), (2349, .6), (3136, .4), (4699, .2)]) * env(n, 0.002, 0.45)


def click():
    return tick(2400) + tick(1800) * .6


put(whoosh(0.45), 18, 0.25)                    # footage shrinks into its card
put(tap(640), 28, 0.25)                        # audience pill
for f in range(52, 78, 2):                     # odometer ticks
    put(tick(), f, 0.16)
put(tap(700), 110, 0.25)                       # shield pops
put(whoosh(0.6, up=False), 132, 0.3)           # scroll to the amount
for i in range(6):                             # digits land
    put(tap(760 + 40 * i), 146 + 3 * i, 0.32)
for f in range(156, 168):                      # coin roll
    put(tick(1400 + 60 * (f % 3)), f, 0.08)
put(chime(), 168, 0.14)
put(whoosh(0.5), 184, 0.22)                    # pull-back into the grid
for f in (198, 204, 210, 222, 262, 274):       # checkbox ticks
    put(click(), f, 0.25)
n = int(SR * 0.4); t = np.linspace(0, 1, n)    # rising swell into the end card
put((lowpass(rng.standard_normal(n), 0.03 + 0.2 * t) * 2 + 0.3 * np.sin(2 * np.pi * np.cumsum(200 + 600 * t) / SR)) * t ** 2, 290, 0.3)
put(tap(520), 350, 0.35)                       # "986" lands
put(chime(), 352, 0.1)

fade = int(SR * 0.25); mix[-fade:] *= np.linspace(1, 0, fade)
mix *= 0.8 / max(1e-9, np.abs(mix).max())
pcm = (np.stack([mix, mix], 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
