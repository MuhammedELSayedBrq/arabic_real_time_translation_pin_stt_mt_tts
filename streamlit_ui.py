import streamlit as st
from transformers import WhisperProcessor, WhisperForConditionalGeneration, VitsTokenizer, VitsModel, set_seed
from get_ras_ip import get_ip
import numpy as np
import socket
import torch
import time
import noisereduce as nr
#import threading

@st.cache_resource
def load_models():
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
    tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-eng")

    if torch.cuda.is_available():
        model_whisper = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium").cuda()
        model_vits = VitsModel.from_pretrained("facebook/mms-tts-eng").cuda()
    else:
        model_whisper = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")
        model_vits = VitsModel.from_pretrained("facebook/mms-tts-eng")

    return processor, tokenizer, model_whisper, model_vits, str(model_whisper.device)

processor, tokenizer, model_whisper, model_vits, device = load_models()
st.success("Ready, Running on " + device)

if 'duration' not in st.session_state:
    st.session_state.duration = 0

duration = st.slider('Choose duration (seconds) ', 1, 30, st.session_state.duration)
st.session_state.duration = int(duration)
st.text(duration)


if 'start_button' not in st.session_state:
    st.session_state.start_button = 0


data = []

start_button_c = st.button('Start receiving')

if start_button_c:
    with st.spinner(text='Running'):
        #def receive(data):
        PORT = 12345
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
        while time.time() - start_time < duration:
            try:
                audio_bytes, server_addr = receiving_socket.recvfrom(NUM_SAMPLES)
                audio_sample = np.frombuffer(audio_bytes, dtype=np.uint8)
                audio_sample = np.array((audio_sample - 128), dtype=np.int8)
                data.extend(audio_sample.tolist())
                text_place.text(f"Received {time.time() - start_time} seconds")
            except:
                receiving_socket.close()

        #thread_r = threading.Thread(target=receive(data))
        #thread_r.start()
        
        chu = st.button('chunk')
        if chu:
            with st.spinner(text='translating'):
                st.text("here")
                forced_decoder_ids = processor.get_decoder_prompt_ids(language="english", task="translate")
                new_data = np.array(data).reshape(1, len(data))

                data = data[len(new_data[0]):]
                scaled_data = new_data / 127
                arr = scaled_data.astype(np.float32)
                sample_rate = 16000
                arr = nr.reduce_noise(y=arr, sr=sample_rate)
                st.audio(arr, sample_rate=sample_rate)

                input_features = processor(arr, sampling_rate=sample_rate, return_tensors="pt").input_features

                if torch.cuda.is_available():
                    input_features = input_features.to(torch.device('cuda'))

                start_time = time.time()
                predicted_ids = model_whisper.generate(input_features, forced_decoder_ids=forced_decoder_ids)
                translation = processor.batch_decode(predicted_ids, skip_special_tokens=True)

                st.text_area("Translation", translation , height = 170)

                end_time = time.time()

                inputs = tokenizer(text=translation, return_tensors="pt")

                if torch.cuda.is_available():
                    inputs = inputs.to(torch.device('cuda'))

                set_seed(555)

                with torch.no_grad():
                    outputs = model_vits(**inputs)

                waveform = outputs.waveform[0].to("cpu")

                float_array = waveform.numpy().astype(np.float32)
                st.audio(float_array, format='audio/wav', sample_rate=sample_rate)
