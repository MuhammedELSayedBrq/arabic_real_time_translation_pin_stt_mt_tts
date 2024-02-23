from pydub import AudioSegment
from pydub.effects import reduce_noise

audio = AudioSegment.from_file("_assets/recorded_audio.wav")

reduced_noise_audio = reduce_noise(audio)

reduced_noise_audio.export("_assets/filtered_audio.wav" , format = "wav")