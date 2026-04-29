import numpy as np
import pandas as pd
from scipy.io.wavfile import write

# ====== CONFIG ======
input_file =r"C:\Users\Lenovo\Desktop\Proj\data_capture\csi\csi_data_2025-05-07_20-17-52.449.csv"   # <-- change this
output_file = "output.wav"
recording_duration_seconds = 10  # <-- change if your recording was different

# ====== LOAD DATA ======
df = pd.read_csv(input_file)

# ====== PARSE CSI_Data COLUMN ======
# Each row's CSI_Data is a string like "[94 -32 5 0 ...]"
csi_values = []
for row in df['CSI_Data']:
    vals = list(map(int, row.strip('[]').split()))
    csi_values.extend(vals)

data = np.array(csi_values, dtype=np.float64)

# ====== CALCULATE SAMPLE RATE TO MATCH RECORDING DURATION ======
total_samples = len(data)
sample_rate = total_samples // recording_duration_seconds
print(f"Total CSI samples : {total_samples}")
print(f"Recording duration: {recording_duration_seconds}s")
print(f"Sample rate set to: {sample_rate} Hz")

# ====== NORMALIZE to [-1, 1] ======
max_val = np.max(np.abs(data))
if max_val > 0:
    data = data / max_val
else:
    raise ValueError("All CSI values are zero — nothing to convert.")

# ====== CONVERT TO 16-BIT PCM ======
audio = np.int16(data * 32767)

# ====== SAVE AS WAV ======
write(output_file, sample_rate, audio)
print(f"Audio saved as '{output_file}' ({len(audio) / sample_rate:.2f} seconds)")