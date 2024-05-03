import threading
import streamlit as st
import time
from get_ras_ip import get_ip
import numpy as np
import socket
import torch

data = []
def receive(data):
            PORT = 1240
            NUM_SAMPLES = 2048
            Sampling_Rate = 16000
            try :
                get_ip()
                st.success('Microphone Connected')
            except:
                st.error('Microphone Not Connected')
            
            receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            receiving_socket.bind(("0.0.0.0", PORT))

            text_place = st.empty()
        
            NUM_SAMPLES = 2048
            start_time = time.time()
            while True:
                try:
                    audio_bytes, server_addr = receiving_socket.recvfrom(NUM_SAMPLES)
                    audio_sample = np.frombuffer(audio_bytes, dtype=np.uint8)
                    audio_sample = np.array((audio_sample - 128), dtype=np.int8)
                    data.extend(audio_sample.tolist())
                    text_place.text(f"Received {time.time() - start_time} seconds")
                except:
                    receiving_socket.close()
                return data
thread_r = threading.Thread(target=receive(data))
thread_r.start()
