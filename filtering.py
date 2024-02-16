from scipy.io import wavfile
from scipy import signal
import numpy as np

sample_rate, data = wavfile.read('f-s-b-d-n-m.wav')

lowcut = 200
highcut = 1000
order = 4
nyquist_freq = 0.5 * sample_rate
low = lowcut / nyquist_freq
high = highcut / nyquist_freq
b, a = signal.butter(order, [low, high], btype='band')

filtered_data = signal.filtfilt(b, a, data)

wavfile.write('filtered_audio.wav', sample_rate, np.int16(filtered_data))
