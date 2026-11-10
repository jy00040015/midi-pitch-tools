# Standard MIDI File (SMF) field reference

The MakeItMidi converters emit a **Format 0 Standard MIDI File**: a single track
holding the detected notes. This is a short reference to the fields involved.

## Header chunk — `MThd`

| Field      | Bytes | Meaning                     |
|------------|-------|-----------------------------|
| chunk type | 4     | `MThd`                      |
| length     | 4     | 6                           |
| format     | 2     | 0 = single track            |
| ntracks    | 2     | 1                           |
| division   | 2     | ticks per quarter note (e.g. 480) |

## Track chunk — `MTrk`

A stream of variable-length events. The ones this converter writes:

| Status          | Bytes | Meaning                                          |
|-----------------|-------|--------------------------------------------------|
| `0x90` note on  | 3     | note number, velocity                            |
| `0x80` note off | 3     | note number, velocity                            |
| `0xE0` pitch bend | 3  | 14-bit bend value (keeps expressive pitch drifts)|

## Note numbers

MIDI note 60 = C4, 69 = A4 (440 Hz). Frequency of note `m`:

`f = 440 * 2 ^ ((m - 69) / 12)` Hz.

See the live converter and its explanations at [MakeItMidi](https://makeitmidi.com/).
