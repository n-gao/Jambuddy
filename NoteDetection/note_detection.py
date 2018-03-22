import pyaudio
import aubio
import audioop
import numpy as np
import inspect
import operator

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 256
BATCH_SECONDS = 0.1

BATCH_SIZE = RATE/CHUNK * BATCH_SECONDS

pitch_detector = aubio.pitch('yinfft', samplerate=RATE, hop_size=CHUNK)
pitch_detector.set_unit('Hz')
pitch_detector.set_tolerance(0.8)

note_detector = aubio.notes('default', samplerate=RATE, hop_size=CHUNK)

reference_frequency = 27.5 # frequency of A0
note_frequencies = []
for i in range(88):
    note_frequencies.append(reference_frequency * pow(2, i/12))
note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
def get_most_likely_note(frequency):
    for i in range(len(note_frequencies)):
        if note_frequencies[i] > frequency:
            if abs(note_frequencies[i-1] - frequency) < abs(note_frequencies[i] - frequency):
                return i-1
            else:
                return i
    return -1

def get_note_name(index):
    if index != -1:
        return note_names[index % len(note_names)] + \
            str((index + len(note_names) - 3)//len(note_names))
    else:
        return ''

def main():
    audio = pyaudio.PyAudio()
    frames = []
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    out_stream = audio.open(format=FORMAT, channels=CHANNELS,
             rate=RATE, output=True, frames_per_buffer=CHUNK)
    
    batch = []
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        # frames.append(data)
        numpydata = np.fromstring(data, dtype=np.float32)
        # numpydata = np.float32(numpydata)
        pitch = pitch_detector(numpydata)[0]
        confidence = pitch_detector.get_confidence()
        if pitch:
            batch.append(pitch)
        if len(batch) >= BATCH_SIZE:
            notes = {}
            for p in batch:
                note = get_most_likely_note(p) 
                notes[note] = (notes[note] if note in notes else 0) + 1
            note = max(notes.items(), key=operator.itemgetter(1))[0]
            print(get_note_name(note))
            print(notes)
            print(pitch)
            batch = []
        # if pitch:
        #     note = get_note_name(get_most_likely_note(pitch))
        #     print('%s %f' % (note, pitch))
        # for f in note_frequencies:
        # out_stream.write(data)

if __name__ == '__main__':
    main()