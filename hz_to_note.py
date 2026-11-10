# -*- coding: utf-8 -*-
"""Convert a frequency in Hz to the nearest MIDI note name.

Usage:
    python hz_to_note.py 440 261.63 432
"""
import sys, math

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def hz_to_note(f):
    m = round(69 + 12 * math.log2(f / 440.0))
    return f"{NAMES[m % 12]}{m // 12 - 1}"


if __name__ == '__main__':
    for a in sys.argv[1:]:
        try:
            print(f"{a} Hz -> {hz_to_note(float(a))}")
        except ValueError:
            print(f"{a}: not a number")
