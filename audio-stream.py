import numpy as np
import pyaudio
import matplotlib.pyplot as plt


# constants
buffer_size = 512  # 1024
read_format = pyaudio.paInt16
num_channels = 1
sample_rate = 22050  # 44100  # Hz

# so we will use this as our sample size! 


print(buffer_size/sample_rate)

p = pyaudio.PyAudio()
stream = p.open(
    format=read_format,
    channels=num_channels,
    rate=sample_rate,
    input=True,
    output=False, # don't play the sounds!
    frames_per_buffer=buffer_size,
    #stream_callback=callback
)




i = 0
data = np.zeros(buffer_size*10)
while i<20:
    audio_data = np.fromstring(stream.read(buffer_size), dtype=np.int16)
    print(data.shape)
    data = np.roll(data, -buffer_size)
    data[-buffer_size:] = audio_data
    # data = stream.read(buffer_size*2)
    # data = np.fromstring(data, dtype=np.int16) 
    # print(data[0], data[-1], len(data))
    i += 1

stream.close()

plt.figure()
plt.plot(data)
plt.show()
