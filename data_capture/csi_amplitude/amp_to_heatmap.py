import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ====== CONFIG ======
input_file = r"C:\Users\Lenovo\Desktop\Proj\data_capture\csi_amplitude\csi_data_2025-05-07_20-17-52.449.csv"   # <-- put your file name here

# ====== LOAD DATA ======
data = pd.read_csv(input_file, header=None)

# Convert to numpy array
amplitude = data.values

# ====== OPTIONAL CLEANING ======
# Replace NaN or inf if any (safe even if already clean)
amplitude = np.nan_to_num(amplitude)

# ====== PLOT HEATMAP ======
plt.figure(figsize=(10, 6))

plt.imshow(amplitude, aspect='auto')
plt.colorbar(label="Amplitude")

plt.title("CSI Amplitude Heatmap")
plt.xlabel("Subcarriers")
plt.ylabel("Time Samples")

plt.tight_layout()
plt.show()