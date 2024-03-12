# .wav is a uncompressed audio file extension

# important audio params:

    # num of channels: mono or stereo ...
    # Sample width: num of bytes for each sample
    # frame rate/ sample rate / sample frequency
    # num of frames
    # values of a frame

import wave
import numpy as np
import matplotlib.pyplot as plt

obj = wave.open("f-s-b-d-n-m.wav","rb")

print("Num of channels: ",obj.getnchannels())
print("Sample Width: ",obj.getsampwidth())
print("Frame rate: ",obj.getframerate())
print("Number of frames: ",obj.getnframes())
print("Parameters: ",obj.getparams())

n_frames = obj.getnframes()
len_audio = n_frames / obj.getframerate()
print("length of wave is ",len_audio , " s")

frames = obj.readframes(-1)
print( type(frames) , type(frames[0]))
print(len(frames)) #num of frames * sample Width

obj.close()


signal_array = np.frombuffer(frames , dtype = np.int16)
time = np.linspace( 0 , len_audio , num = n_frames)

plt.figure(figsize=(15,5) )
plt.plot(time, signal_array)
plt.title("Audio Signal")
plt.xlabel("Time (s)")
plt.ylabel("Signal Wave")
plt.xlim( 0 , len_audio)
plt.show()



# obj_new = wave.open("new_written.wav","wb")
# obj_new.setnchannels(1)
# obj_new.setsampwidth(2)
# obj_new.setframerate(16000.0)
# obj_new.writeframes(frames)
# obj_new.close()

