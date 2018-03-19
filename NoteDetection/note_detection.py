import pyaudio
import aubio
import audioop
import numpy as np

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 512

pitch_detector = aubio.pitch('yin', samplerate=RATE)
pitch_detector.set_unit('Hz')
pitch_detector.set_tolerance(0.8)

pv = aubio.pvoc(512, 512)
f = aubio.filterbank(40, 512)

def main():
    audio = pyaudio.PyAudio()
    frames = []
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    out_stream = audio.open(format=FORMAT, channels=CHANNELS,
             rate=RATE, output=True, frames_per_buffer=CHUNK)
    
    while True:
        data = stream.read(CHUNK)
        # frames.append(data)
        numpydata = np.fromstring(data, dtype=np.float32)
        # numpydata = np.float32(numpydata)
        pitch = pitch_detector(numpydata)
        confidence = pitch_detector.get_confidence()
        if pitch:
            print('%f' % (pitch))
        energy = audioop.rms(data, 1)
        out_stream.write(data)

if __name__ == '__main__':
    main()