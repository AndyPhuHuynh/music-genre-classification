import music21
import random
from midiutil import MIDIFile
from pathlib import Path

"""
1. Choose a random key
2. Choose a random chord progression
3. Generate a melody with the chord progression
"""

NUM_TRACKS:   int = 3
CHORD_TRACK:  int = 0
BASS_TRACK:   int = 1
MELODY_TRACK: int = 2

happy_keys: list[music21.key.Key] = [music21.key.Key(k) for k in ["C", "E", "F"]]
sad_keys:   list[music21.key.Key] = [music21.key.Key(k) for k in ["a", "c", "d"]]

major_key_progressions: list[list[str]] = [
    ["I", "IV", "V", "vi"],
    ["I", "IV", "V", "I"],
    ["I", "IV", "vi", "V"],
    ["I", "vi", "IV", "V"],
    ["I", "IV", "ii", "V"],
    ["I", "V", "IV", "V"],
    ["I", "iii", "IV", "V"],
]

minor_key_progressions: list[list[str]] = [
    ["i", "iv", "v", "VI"],
    ["i", "iv", "v", "i"],
    ["i", "VI", "III", "VII"],
    ["i", "VII", "VI", "VII"],
    ["i", "iv", "VII", "III", "VI", "ii°", "V", "i"],
]

RHYTHM_PATTERNS = [
    [1, 1, 1, 1],
    [1.5, 1.5, 1],
    [0.5, 0.5, 1, 2],
    [1.5, 0.5, 1, 1],
]


def write_ending_chord(mf: MIDIFile, chord: music21.chord.Chord, channel: int, chord_start_time: float | int,
                       volume: int):
    for pitch in chord.pitches:
        mf.addNote(CHORD_TRACK, channel, pitch.midi - 12, chord_start_time, 4, volume)
    mf.addNote(BASS_TRACK, channel, chord.root().midi - 24, chord_start_time, 4, volume)
    mf.addNote(MELODY_TRACK, channel, chord.root().midi, chord_start_time, 4, volume)
    return chord_start_time + 4


class Song:
    def __init__(self, is_happy: bool):
        self.is_happy = is_happy
        if self.is_happy:
            self.key: music21.key.Key = random.choice(happy_keys)
            self.one_chord: str = "I"
            self.progression: list[str] = random.choice(major_key_progressions)
        else:
            self.key: music21.key.Key = random.choice(sad_keys)
            self.one_chord: str = "i"
            self.progression: list[str] = random.choice(minor_key_progressions)


    def write(self, filename: Path):
        channel = 0
        volume = 100
        bpm = 120
        mf = MIDIFile(NUM_TRACKS)  # 0: chords, 1: bass, 2: melody
        for track in range(NUM_TRACKS):
            mf.addTempo(track, channel, bpm)

        time = 0
        for roman_numeral in self.progression:
            chord_start_time = time
            chord = music21.roman.RomanNumeral(roman_numeral, self.key)

            for pitch in chord.pitches:
                mf.addNote(0, channel, pitch.midi - 12, chord_start_time, 4, volume)
            mf.addNote(1, channel, chord.root().midi - 24, chord_start_time, 4, volume)
            time = generate_melody_for_chord(chord, self.key.getScale(), time, 2, channel, volume, mf)

        if self.progression[-1] != self.one_chord and random.choice([True, False]):
            write_ending_chord(mf, music21.roman.RomanNumeral(self.one_chord, self.key), channel, time, volume)

        with open(filename, "wb") as f:
            mf.writeFile(f)


def generate_melody_for_chord(chord, scale, start_time, track, channel, volume, midi_file):
    rhythm = random.choice(RHYTHM_PATTERNS)
    beat = 0
    for duration in rhythm:
        if beat in [0, 2]:
            note = random.choice(chord.pitches).midi
        else:
            note = random.choice(scale.pitches).midi
        midi_file.addNote(track, channel, note, start_time + beat, duration, volume)
        beat += duration
    return start_time + beat

