import numpy as np
import pandas as pd
from scipy.io.wavfile import write

input_file = r"C:\Users\Lenovo\Desktop\Proj\data_capture\csi\csi_data_2025-05-07_20-17-52.449.csv"
output_file = "output.wav"
sample_rate = 100

# Load CSV
df = pd.read_csv(input_file)

# Convert everything to numeric (VERY IMPORTANT)
df = df.apply(pd.to_numeric, errors='coerce')

# Now flatten
data = df.values.flatten()

# Remove NaNs (now it will work)
data = data[~np.isnan(data)]

# Normalize
data = data / np.max(np.abs(data))

# Convert to audio
audio = np.int16(data * 32767)

write(output_file, sample_rate, audio)

print("Done")