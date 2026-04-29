import soundfile as sf
import numpy as np
from scipy.signal import resample

file1 = r"C:\Users\Lenovo\Desktop\cir_audio.wav"
file2 = r"C:\Users\Lenovo\Desktop\drums.wav"
output_file = r"C:\Users\Lenovo\Desktop\output_mixed_cir_drums.wav"

audio1, sr1 = sf.read(file1)
audio2, sr2 = sf.read(file2)

# Ensure 2D
if audio1.ndim == 1:
    audio1 = audio1[:, None]
if audio2.ndim == 1:
    audio2 = audio2[:, None]

# Resample if needed
if sr1 != sr2:
    new_len = int(len(audio2) * sr1 / sr2)
    audio2 = np.stack([resample(audio2[:, ch], new_len) for ch in range(audio2.shape[1])], axis=1)

# Match channels
channels = max(audio1.shape[1], audio2.shape[1])
audio1 = np.tile(audio1, (1, channels)) if audio1.shape[1] != channels else audio1
audio2 = np.tile(audio2, (1, channels)) if audio2.shape[1] != channels else audio2

# Match length
max_len = max(len(audio1), len(audio2))
audio1 = np.pad(audio1, ((0, max_len - len(audio1)), (0, 0)))
audio2 = np.pad(audio2, ((0, max_len - len(audio2)), (0, 0)))

# Weighted mix (KEY FIX)
mixed = 0.4 * audio1 + 1.0 * audio2

# Normalize safely
mixed = mixed / (np.max(np.abs(mixed)) + 1e-8)

sf.write(output_file, mixed, sr1)

print(" Better mix saved")