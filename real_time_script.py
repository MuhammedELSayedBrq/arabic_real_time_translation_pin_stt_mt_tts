from transformers import WhisperProcessor, WhisperForConditionalGeneration, VitsTokenizer, VitsModel, set_seed
import torch , torchaudio , librosa
import soundfile as sf
import sounddevice as sd
import time
import socket
import numpy as np
import noisereduce as nr
from scipy.io.wavfile import write
import threading
import queue

def load_models():
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
    tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-eng")
    model_whisper = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")
    model_vits = VitsModel.from_pretrained("facebook/mms-tts-eng")
    return processor, tokenizer, model_whisper, model_vits, str(model_whisper.device)

def rec(q):
    PORT = 12345
    NUM_SAMPLES = 2048
    Sampling_Rate = 16000

    receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiving_socket.bind(("0.0.0.0", PORT))

    print("Receiving now.....")

    data = []
    data_to_share = np.array(data , dtype=np.int8)

    stream = sd.OutputStream(channels=1, dtype="int8", samplerate=Sampling_Rate)
    stream.start()
    while True:        
        try:
            audio_bytes, server_addr = receiving_socket.recvfrom(NUM_SAMPLES)
            audio_sample = np.frombuffer(audio_bytes, dtype=np.uint8)
            audio_sample = np.array((audio_sample - 128) , dtype=np.int8) 
            audio_sample = nr.reduce_noise(y=audio_sample, sr=Sampling_Rate)
            stream.write(audio_sample)

            data = np.concatenate((data, audio_sample))
            for _ in range(2048):
                q.put(data[0])
                data=data[1:]

        except:
            receiving_socket.close()
            #stream.close()
    #print(list(q.queue),"1")

            

q=queue.Queue()
processor, tokenizer, model_whisper, model_vits, device = load()

receive=threading.Thread(target=rec, args=(q,))
#receive.daemon=True
receive.start()
if __name__=='__main__':
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="english", task="translate")
    sample_rate=16000
    try:
        while True:
            shared_list=[]   
        
            for _ in range (80000):
                shared_list.append(q.get())
            data=np.array(shared_list,dtype=np.int8)
        
            new_data  = data.reshape(1,data.shape[0])
            norm_data = new_data/127
            arr = norm_data.astype(np.float32)

            
            input_features = processor(arr, sampling_rate=sample_rate, return_tensors="pt").input_features 

            start_time = time.time()
            predicted_ids = model_whisper.generate(input_features, forced_decoder_ids=forced_decoder_ids)

            translation = processor.batch_decode(predicted_ids, skip_special_tokens=True)


            end_time = time.time()
            print(translation,end='')
            elapsed_time = end_time - start_time

            print(f"Process took {elapsed_time:.2f} seconds.")

            inputs = tokenizer(text=translation, return_tensors="pt")

            set_seed(555) 

            with torch.no_grad():
                outputs = model_vits(**inputs)

            waveform = outputs.waveform[0].to("cpu")

            float_array = waveform.numpy().astype(float)
            sd.play(float_array , samplerate=model_vits.config.sampling_rate)
            sd.wait()

    except KeyboardInterrupt:
        print("Exiting...")