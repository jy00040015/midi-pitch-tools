# -*- coding: utf-8 -*-
"""From-scratch YIN monophonic pitch tracker (de Cheveigné & Kawahara, 2002).

Pure NumPy + stdlib `wave`. No model download, no TensorFlow. Transparent and
reproducible. This is the same algorithm used to produce accuracy_dataset.csv.

Usage:
    python yin_pitch.py path/to/audio.wav
"""
import sys, json, wave
import numpy as np

F_MIN, F_MAX = 30.0, 2000.0
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def m2n(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def f2m(f):
    return 69 + 12 * np.log2(f / 440.0)


def read_wav(path):
    with wave.open(path, 'r') as w:
        n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
        raw = w.readframes(n)
    sig = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        sig = sig.reshape(-1, ch).mean(axis=1)
    return sig, sr


def harmonic_score(mag, df, f):
    """Harmonic match score used to disambiguate octave (subharmonic) errors."""
    idx0 = int(round(f / df))
    if not (0 <= idx0 < len(mag)):
        return -1.0
    s = 2.0 * mag[idx0]
    for k in range(2, 7):
        ff = k * f
        if ff > F_MAX * 1.5:
            break
        idx = int(round(ff / df))
        if 0 <= idx < len(mag):
            s += mag[idx]
    return s


def yin_pitch(frame, sr, thresh=0.12):
    """Return fundamental frequency (Hz) of a frame, or None for unvoiced."""
    N = len(frame)
    x = frame - frame.mean()
    energy = float(np.dot(x, x))
    if energy < 1e-6:
        return None
    X = np.fft.rfft(x)
    acf = np.fft.irfft(X * np.conj(X))[:N]
    sq = x * x
    prefix = np.concatenate(([0.0], np.cumsum(sq)))
    tau_min = max(2, int(sr / F_MAX))
    tau_max = min(N - 1, int(sr / F_MIN))
    d = np.zeros(tau_max + 1)
    for tau in range(1, tau_max + 1):
        A = prefix[N - tau]; B = energy - prefix[tau]
        d[tau] = A + B - 2.0 * acf[tau]
    cmnd = np.ones(tau_max + 1)
    running = 0.0
    for tau in range(1, tau_max + 1):
        running += d[tau]
        cmnd[tau] = (d[tau] * tau / running) if running > 0 else 1.0
    tau0 = None
    for tau in range(tau_min, tau_max + 1):
        if np.isfinite(cmnd[tau]) and cmnd[tau] < thresh:
            if tau_min < tau < tau_max:
                a, b, c = cmnd[tau - 1], cmnd[tau], cmnd[tau + 1]
                denom = a - 2 * b + c
                if np.isfinite(denom) and denom != 0:
                    tau = tau + 0.5 * (a - c) / denom
            tau0 = tau
            break
    if tau0 is None:
        return None
    f0 = sr / tau0
    mag = np.abs(X)
    freqs = np.fft.rfftfreq(N, 1.0 / sr)
    df = freqs[1] - freqs[0]
    best_f, best_s = f0, -1.0
    for p in range(-1, 6):
        f = f0 * (2 ** p)
        if f < F_MIN or f > F_MAX:
            continue
        s = harmonic_score(mag, df, f)
        if s > best_s:
            best_s, best_f = s, f
    return best_f


def estimate_notes(wav, N=2048, H=512):
    """Return the set of detected MIDI note numbers in a WAV file."""
    sig, sr = read_wav(wav)
    win = np.hanning(N)
    raw = []
    for start in range(0, max(1, len(sig) - N), H):
        raw.append(yin_pitch(sig[start:start + N] * win, sr))
    seq = []
    prev = None
    for f0 in raw:
        if f0 is None:
            seq.append(None); continue
        if prev is None:
            seq.append(f0)
        else:
            best, bestd = f0, 1e18
            for p in range(-2, 3):
                ff = f0 * (2 ** p)
                if F_MIN <= ff <= F_MAX:
                    dd = abs(ff - prev)
                    if dd < bestd:
                        bestd, best = dd, ff
            seq.append(best)
        prev = seq[-1]
    counts = {}
    total = sum(1 for f in seq if f is not None)
    min_frames = max(3, int(0.02 * total)) if total else 0
    for f0 in seq:
        if f0 is None or not np.isfinite(f0) or f0 <= 0:
            continue
        m = int(round(f2m(f0)))
        counts[m] = counts.get(m, 0) + 1
    return sorted(m for m, c in counts.items() if c >= min_frames)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python yin_pitch.py audio.wav"); sys.exit(1)
    notes = estimate_notes(sys.argv[1])
    print(json.dumps({"file": sys.argv[1], "detected_notes": [m2n(m) for m in notes]}))
