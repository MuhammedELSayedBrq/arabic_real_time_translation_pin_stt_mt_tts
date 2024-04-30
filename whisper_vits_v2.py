import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio , librosa
import soundfile as sf
import sounddevice as sd
import time
import socket
import numpy as np
import noisereduce as nr
from transformers import VitsTokenizer, VitsModel, set_seed
from scipy.io.wavfile import write
# load the whisper and vits model
processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-eng")
model_whisper = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium").cuda()
model_vits = VitsModel.from_pretrained("facebook/mms-tts-eng").cuda()

########################################################
PORT = 12345
NUM_SAMPLES = 2048
Sampling_Rate = 16000

receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiving_socket.bind(("0.0.0.0", PORT))

print("Receiving now.....");

data = []
data = np.array(data , dtype=np.int8)
start_time=time.time()


stream = sd.OutputStream(channels=1, dtype="int8", samplerate=Sampling_Rate)
stream.start()
start_time=time.time()
while(time.time()-start_time)<30:
    try:
        audio_bytes, server_addr = receiving_socket.recvfrom(NUM_SAMPLES)
        audio_sample = np.frombuffer(audio_bytes, dtype=np.uint8)
        audio_sample = np.array((audio_sample - 128) , dtype=np.int8) 
        audio_sample = nr.reduce_noise(y=audio_sample, sr=Sampling_Rate)
        #audio_sample=process(audio_bytes)
        #print (audio_sample)
        data = np.concatenate((data, audio_sample))
        stream.write(audio_sample)
            
    except:
        receiving_socket.close()
        stream.close()
receiving_socket.close()
stream.close()
        
print("finished talking")
# tokenizer 
forced_decoder_ids = processor.get_decoder_prompt_ids(language="english", task="translate")


new_data=data.reshape(1,data.shape[0])
scaled_data=new_data/127 # to become in range -1 to 1 and will bocome float64
arr=scaled_data.astype(np.float32)  #as whisper recieve float32 not  float 64

sample_rate=16000
input_features = processor(arr, sampling_rate=sample_rate, return_tensors="pt").input_features 
input_features = input_features.to(torch.device('cuda'))


start_time = time.time()  # Record the start time
# generate token ids not text
predicted_ids = model_whisper.generate(input_features, forced_decoder_ids=forced_decoder_ids)

# ouput will be text and not adding special tokens
translation = processor.batch_decode(predicted_ids, skip_special_tokens=True)


end_time = time.time()  # Record the end time
print(translation)
# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"Process took {elapsed_time:.2f} seconds.")


# output waveform
inputs = tokenizer(text=translation, return_tensors="pt")
inputs= inputs.to(torch.device('cuda'))

set_seed(555)  # make deterministic

with torch.no_grad():
   outputs = model_vits(**inputs)

waveform = outputs.waveform[0].to("cpu")

# convert tensor data type into array
float_array = waveform.numpy().astype(float)
sd.play(float_array,samplerate=model_vits.config.sampling_rate)
sd.wait()
sd.play(data,16000)
sd.wait()