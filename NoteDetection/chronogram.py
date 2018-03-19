
class Chronogram:
    
    def __init__(self, frame_size, frequency):
        self.reference_frequency = 130.81278265
        self.buffer_size = 8192
        self.num_harmonics = 2
        self.num_octaves = 2
        self.num_bins_to_search = 2
        self.note_frequencies = []
        for i in range(12):
            self.note_frequencies.append(
                self.reference_frequency * pow(2, i/12)
            )
        self.setup_fft()
        self.buffer = []
        self.chromogram = []
        self.magnitude_spectrum = []
        self.make_hamming_window()
        self.set_frequency(frequency)
        self.set_frame_size(frame_size)
        self.num_samples_since_last_calculation = 0
        self.chroma_calculation_interval = 4096
        self.chroma_ready = False

    def process_audio_frame(self, sample):
        self.chroma_ready = False
        # downsample the input frame by 4
        self.down_sample_frame(sample)
        self.buffer = []
        # move samples back
        for i in range(self.buffer_size - self.down_sampled_audio_frame_size):
            self.buffer.append[i + self.down_sampled_audio_frame_size]
        n = 0
        # add new sample to buffer
        for i in range(self.buffer_size - self.down_sampled_audio_frame_size, self.buffer_size):
            self.buffer[i] = self.down_sampled_audio_frame[n]
            n += 1
        #add new number of samples from calculation
        self.num_samples_since_last_calculation += self.frame_size
        #if we have had enough samples
        if self.num_samples_since_last_calculation >= self.chroma_calculation_interval:
            self.calculate_chromogram()
            self.num_samples_since_last_calculation = 0

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size
        self.down_sampled_audio_frame = []
        self.down_sampled_audio_frame_size = frame_size//4

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_chroma_calculation_interval(self, num_samples):
        self.num_samples = num_samples

    def get_chromogram(self):
        return []

    def is_ready(self):
        return self.chroma_ready

    def setup_fft(self):

    def calculate_chromogram(self):

    def calculate_magnitude_spectrum(self):

    def down_sample_frame(self):

    def make_hamming_window(self):

    