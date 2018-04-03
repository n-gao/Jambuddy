
# base_note from 
# [0, 1,  2,  3, 4, 5,  6, 7,  8, 9, 10, 11]
# [C, C#, D, D#, E, F, F#, G, G#, A, A#,  H]
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
ind_to_note = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
def get_note_name(index):
    if index != -1:
        return note_names[index % len(note_names)] + \
            str((index + len(note_names) - 3)//len(note_names))
    else:
        return ''

class Pentatonic:
    def __init__(self, base_note):
        if type(base_note) == str:
            self.base_note = _base_notes[base_note.upper()]
        elif type(base_note) == int:
            self.base_note = base_note
        else:
            raise ValueError('base_note must be a string or a integer.')
        self.lowest_note = 20
        self.highest_note = 66
        self.offsets = []
        self.notes = []

    def _gen_notes(self):
        self.notes = []
        i = 0
        for i in range(-1, self.highest_note//12):
            for offset in self.offsets:
                note = offset + self.base_note + 3 + i * 12
                if note < self.lowest_note:
                    continue
                if note > self.highest_note:
                    continue
                self.notes.append(note)
        
class MajorPentatonic(Pentatonic):
    def __init__(self, base_note):
        Pentatonic.__init__(self, base_note)
        self.offsets = [0, 2, 4, 7, 9]
        self._gen_notes()


class MinorPentatonic(Pentatonic):
    def __init__(self, base_note):
        Pentatonic.__init__(self, base_note)
        self.offsets = [0, 3, 5, 7, 10]
        self._gen_notes()
        