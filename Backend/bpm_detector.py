import aubio
import pyaudio
import numpy as np
from collections import deque

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 512
BATCH_SECONDS = 15

class BpmDetector:
    def __init__(self):
        self.tempo_detector = aubio.tempo('specdiff', samplerate=RATE, hop_size=CHUNK)
        self.audio = pyaudio.PyAudio()
        self.in_stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                    rate=RATE, input=True,
                                    frames_per_buffer=CHUNK)
        self.beats = deque([], 30)
        self.bpm = -1

    def get_bpm(self):
        return self.bpm

    def beats_to_bpm(self, beats):
        if len(beats) > 1:
            if len(beats) < 4:
                return -1
            bpms = 60/np.diff(beats)
            return np.median(bpms)
        return -1

    def continously_detect_bpm(self):
        while True:
            data = self.in_stream.read(CHUNK, exception_on_overflow=False)
            numpydata = np.fromstring(data, dtype=np.float32)
            is_beat = self.tempo_detector(numpydata)
            if is_beat:
                this_beat = self.tempo_detector.get_last_s()
                self.beats.append(this_beat)
            self.bpm = self.beats_to_bpm(list(self.beats))

if __name__ == '__main__':
    BpmDetector().continously_detect_bpm()
