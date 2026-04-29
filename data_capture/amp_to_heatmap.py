import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


input_file = r"path to file here"   # <-- put your file name here


data = pd.read_csv(input_file, header=None)


amplitude = data.values


# Replace NaN or inf if any
amplitude = np.nan_to_num(amplitude)


plt.figure(figsize=(10, 6))

plt.imshow(amplitude, aspect='auto')
plt.colorbar(label="Amplitude")

plt.title("CSI Amplitude Heatmap")
plt.xlabel("Subcarriers")
plt.ylabel("Time Samples")

plt.tight_layout()
plt.show()