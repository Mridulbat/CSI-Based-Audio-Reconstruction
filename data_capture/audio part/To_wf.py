import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


file_path = "cir_audio.wav"


sample_rate, data = wavfile.read(file_path)


if len(data.shape) > 1:
    data = data[:, 0]

# Create time axis
duration = len(data) / sample_rate
time = np.linspace(0., duration, len(data))


plt.figure(figsize=(10, 4))
plt.plot(time, data)
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("Audio Waveform")
plt.show()