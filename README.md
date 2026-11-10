# browser-audio-to-midi-notes

A small, dependency-light toolkit for turning audio into MIDI note data, built to
accompany the research behind [MakeItMidi](https://makeitmidi.com/) — a browser-based
MP3/WAV/voice-to-MIDI converter that runs entirely on the user's device.

This repository is for people who want to understand or reuse the building blocks:

- `yin_pitch.py` — a from-scratch YIN monophonic pitch tracker
  (de Cheveigné & Kawahara, 2002) in pure NumPy. No TensorFlow, no model download.
- `accuracy_dataset.csv` — measured wrong-note counts for 9 audio types, run through
  the tracker above (monophonic baseline, transparent methodology, every number measured).
- `hz_to_note.py` — convert a frequency in Hz to the nearest MIDI note name.

Everything here is plain Python/NumPy so you can read it, run it, and lift what you need.

## Why this exists

Pitch detection is not magic: a MIDI note can only hold a whole semitone, so any pitch
that slides, bends, or vibratos gets rounded — that rounding is what makes
"out-of-tune" conversions sound off. The code and dataset here make that behaviour
observable instead of mysterious. See the converter and its explanations at
[MakeItMidi](https://makeitmidi.com/).
