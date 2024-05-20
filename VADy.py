import pyaudio
import webrtcvad
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)

vad = webrtcvad.Vad()

# Configure VAD (set aggressiveness level, 0: least aggressive, 3: most aggressive)
vad.set_mode(3)

audio_in = pyaudio.PyAudio()
audio_out = pyaudio.PyAudio()

stream_in = audio_in.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

stream_out = audio_out.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

print("Listening... Press Ctrl+C to stop.")
speech = b""
try:
    while True:
        audio_data = stream_in.read(CHUNK_SIZE)
        is_speech = vad.is_speech(audio_data, RATE)
       
        if is_speech:
            stream_out.write(audio_data)
            speech += audio_data

except KeyboardInterrupt:
    print("Recording stopped by user.")
    speech_data = np.frombuffer(speech, dtype=np.int16)
    print(type(speech_data))
    """ in the code above i get the data ready for the model
    #in the code below i check the output data
    # Write smaller chunks of speech data to the output stream
    #for i in range(0, len(speech_data), CHUNK_SIZE):
    #    stream_out.write(speech_data[i:i+CHUNK_SIZE].tobytes())
    """

finally:
    stream_in.stop_stream()
    stream_in.close()
    stream_out.stop_stream()
    stream_out.close()
    audio_in.terminate()
    audio_out.terminate()
