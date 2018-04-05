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

_offsets = {
    'maj' : [0, 2, 4, 5, 7, 9],
    'min' : [0, 3, 5, 7, 8, 10]
}

_types = {
    'maj' : ['maj', 'min', 'min', 'maj', 'maj', 'min'],
    'min' : ['min', 'maj', 'min', 'min', 'maj', 'maj']
}

def get_random_chord(key):
    key_note, key_type = key
    # try:
    ind = random.randint(0, len(_offsets))
    return (_types[key_type][ind], (key_note + random.choice(_offsets[key_type])[0]) % 12)
    # except:
    #     print("wtf")
    #     return None
