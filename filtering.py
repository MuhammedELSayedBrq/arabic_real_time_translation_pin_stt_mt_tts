from scipy.io import wavfile
from scipy import signal
import numpy as np


def filter_human(*args):
    if len(args) == 2:
        input_file,output_file = args
        sample_rate, data = wavfile.read(input_file)
        lowcut = 200
        highcut = 3400
        order = 5
        nyquist_freq = 2 * sample_rate
        low = lowcut / nyquist_freq
        high = highcut / nyquist_freq
        b, a = signal.butter(order, [low, high], btype='band')

        filtered_data = signal.filtfilt(b, a, data)

        wavfile.write(output_file, sample_rate, np.int16(filtered_data))

    elif len(args) == 5:
        input_file,output_file , lowcut , highcut , order = args
        sample_rate, data = wavfile.read(input_file)
        nyquist_freq = 2 * sample_rate
        low = lowcut / nyquist_freq
        high = highcut / nyquist_freq
        b, a = signal.butter(order, [low, high], btype='band')

        filtered_data = signal.filtfilt(b, a, data)

        wavfile.write(output_file, sample_rate, np.int16(filtered_data))