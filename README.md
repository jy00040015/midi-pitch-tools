# midi-pitch-tools

Small, dependency-light tools that turn audio into MIDI note data, built alongside
[MakeItMidi](https://makeitmidi.com/) — a browser-based MP3/WAV/voice-to-MIDI converter
that runs entirely on the user's device.

- `yin_pitch.py` — a from-scratch YIN monophonic pitch tracker
  (de Cheveigné & Kawahara, 2002) in pure NumPy. No model download, no TensorFlow.
- `hz_to_note.py` — convert a frequency in Hz to the nearest MIDI note name.
- `note_frequency_table.csv` — reference table of MIDI note numbers, names and frequencies.
- `midi-smf-notes.md` — short field reference for the Standard MIDI File format this
  converter emits.

Everything is plain Python/NumPy so you can read it, run it, and lift what you need.
The converter and its explanations live at [MakeItMidi](https://makeitmidi.com/).
