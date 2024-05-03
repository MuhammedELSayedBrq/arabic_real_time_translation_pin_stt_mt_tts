import wave
import numpy as np
import threading
import socket
import time
import os
def receive():
    PORT = 12345
    NUM_SAMPLES = 2048
    CHUNK_SIZE = 8192  # Define a chunk size for writing to the WAV file
    
    receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiving_socket.bind(("0.0.0.0", PORT))

    data = []  # Define data as an empty list to store audio samples

    while True:
        try:
            audio_bytes, server_addr = receiving_socket.recvfrom(NUM_SAMPLES)
            audio_sample = np.frombuffer(audio_bytes, dtype=np.uint8)
            audio_sample = np.array((audio_sample - 128), dtype=np.int8)
            data.extend(audio_sample.tolist())
            
            # Check if data length exceeds chunk size, if so, save a chunk
            if len(data) >= CHUNK_SIZE:
                save_chunk(data[:CHUNK_SIZE])  # Save the chunk
                data = data[CHUNK_SIZE:]       # Remove the saved chunk from data
        except Exception as e:
            print("An error occurred:", e)
            receiving_socket.close()
            break

    # After receiving all data, save the remaining chunk
    if data:
        save_chunk(data)

def save_chunk(chunk):
    # Scale and convert the chunk, then save it as a WAV file using PCM codec
    new_data = np.array(chunk).reshape(1, len(chunk))
    scaled_data = new_data / 127
    arr = scaled_data.astype(np.float32)
    arr = (arr * 32767).astype(np.int16)  # Convert to 16-bit signed integers
    name = '_assets/mido_part_{}.wav'.format(int(time.time()))
    input_files.append(name)
    input_filesa = [item for index, item in enumerate(input_files) if item not in input_files[:index]]

    save_wav(name, 16000, arr)
    output_file = '_assets/mido.wav'
    merge_wav_files(input_filesa, output_file)
    #os.remove(name)
    #input_files.pop()



def save_wav(filename, sample_rate, data):
    with wave.open(filename, 'w') as wavfile:
        wavfile.setnchannels(1)  # Mono
        wavfile.setsampwidth(2)  # 16-bit
        wavfile.setframerate(sample_rate)
        wavfile.writeframes(data.tobytes())

def merge_wav_files(input_files, output_file):
    # Open the first input file to get parameters
    with wave.open(input_files[0], 'rb') as first_wav:
        # Get parameters from the first WAV file
        num_channels = first_wav.getnchannels()
        sample_width = first_wav.getsampwidth()
        frame_rate = first_wav.getframerate()
        num_frames = first_wav.getnframes()

        # Open the output WAV file for writing
        with wave.open(output_file, 'wb') as output_wav:
            output_wav.setnchannels(num_channels)
            output_wav.setsampwidth(sample_width)
            output_wav.setframerate(frame_rate)

            # Write audio data from each input file to the output file
            for input_file in input_files:
                with wave.open(input_file, 'rb') as input_wav:
                    # Read and write audio data
                    output_wav.writeframes(input_wav.readframes(num_frames))

if __name__ == '__main__':
    input_files = []  # List to store input WAV files
    # Start receiving data in a separate thread
    receive()