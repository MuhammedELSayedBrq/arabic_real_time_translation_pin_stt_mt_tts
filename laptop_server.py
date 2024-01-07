import socket
import sounddevice as sd
from array import array


def receive_audio_data(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        stream = sd.OutputStream(channels=1, dtype="int16", samplerate=44100)
        stream.start()

        try:
            while True:
                audio_bytes = client_socket.recv(2)
                if not audio_bytes:
                    break

                audio_value = int.from_bytes(
                    audio_bytes, byteorder="little", signed=True
                )
                audio_sample = array("h", [audio_value])
                stream.write(audio_sample)
        finally:
            stream.stop()


if __name__ == "__main__":
    HOST = "192.168.0.102"  # Replace with the actual IP of your Raspberry Pi
    PORT = 89

    receive_audio_data(HOST, PORT)
