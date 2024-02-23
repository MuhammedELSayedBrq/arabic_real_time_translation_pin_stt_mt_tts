import noisereduce as nr
from scipy.io import wavfile

rate , data = wavfile.read("_assets/recorded_audio.wav")

reduced_noise = nr.reduce_noise(data, data[:int(rate * 0.5)] , False)

wavfile.write("_assets/filtered_audio.wav" , rate , reduced_noise)