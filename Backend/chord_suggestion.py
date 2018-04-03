import random

_base_notes = {
    'C' : 0,
    'C#': 1,
    'Db': 1,
    'D' : 2,
    'D#': 3,
    'Eb': 3,
    'E' : 4,
    'F' : 5,
    'F#': 6,
    'Gb': 6,
    'G' : 7,
    'G#': 8,
    'Ab': 8,
    'A' : 9,
    'A#':10,
    'Bb':10,
    'B' :11
}
_key_to_chords = {
    'maj' : [
        [(0, 'maj'), (2, 'min'), (7, 'maj'), (9, 'maj'), (11, 'min')],
        [],
        [(2, 'maj'), (4, 'min'), (7, 'maj'), (9, 'maj'), (11, 'min')],
        [],
        [(4, 'maj'), (9, 'maj'), (11, 'maj')],
        [(5, 'maj'), (7, 'min'), (9, 'min'), (0, 'maj')],
        [],
        [(7, 'maj'), (9, 'min'), (11, 'min'), (0, 'maj'), (2, 'maj'), (4, 'min')],
        [],
        [(9, 'maj'), (11, 'min'), (2, 'maj'), (4, 'maj')],
        [],
        [(11, 'maj'), (4, 'maj')]
    ],
    'min' : [
        [(0, 'min'), (7, 'min'), (9, 'min')],
        [],
        [(2, 'min'), (5, 'maj'), (7, 'min'), (9, 'min'), (0, 'maj')],
        [],
        [(4, 'min'), (7, 'maj'), (9, 'min'), (11, 'min'), (0, 'maj'), (2, 'maj')],
        [(5, 'min'), (0, 'min')],
        [],
        [(7, 'min'), (0, 'min'), (2, 'min'), (5, 'maj')],
        [],
        [(9, 'min'), (0, 'maj'), (2, 'min'), (4, 'maj'), (5, 'maj'), (7, 'maj')],
        [],
        [(11, 'min'), (2, 'maj'), (4, 'min'), (7, 'maj'), (9, 'maj')]
    ]
}

def get_random_chord(key):
    key_note, key_type = key
    try:
        return random.choice(_key_to_chords[key_type][key_note])
    except:
        return []
