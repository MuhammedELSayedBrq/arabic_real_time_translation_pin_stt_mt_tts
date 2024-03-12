import socket
import sounddevice as sd
from array import array
import scipy.io.wavfile as wav
import wave
from get_ras_ip import get_ip

duration = 10 
num_channels = 1
sample_width = 2
sample_rate = 33075
file_path = '_assets/recorded_audio.wav'

def receive_audio_data(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")
        """with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(num_channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(sample_rate)

            bytes_received = 0
            while bytes_received < duration * sample_rate * sample_width * num_channels:
                audio_bytes = client_socket.recv(2)
                
                wf.writeframes(audio_bytes)
                
                bytes_received += len(audio_bytes)

    print(f"Audio saved to {file_path}")"""
    # block to listen on output speaker
        stream = sd.OutputStream(channels=1, dtype="int16", samplerate=33075)
        stream.start()

        try:
            while True:
                audio_bytes = client_socket.recv(2)

                audio_value = int.from_bytes(
                    audio_bytes, byteorder="little" 
                ) -  32768
                audio_sample = array("h", [audio_value])
                stream.write(audio_sample)
        finally:
            stream.stop()


if __name__ == "__main__":
    HOST_ip = get_ip() # gets ip from """address resoultion protocol""" reply
    PORT = 49152    # general purpose port numbers from 49152 to 65535

    receive_audio_data(HOST_ip, PORT)
