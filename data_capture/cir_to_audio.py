import numpy as np
import pandas as pd
from scipy.io.wavfile import write


input_file = "cir_output.csv"      # <-- change this
output_file = "cir_audio.wav"
recording_duration_seconds = 10    


TAP_START = 1
TAP_END   = 59

# ====== LOAD CIR DATA ======
df = pd.read_csv(input_file)
tap_cols = [c for c in df.columns if c.startswith('tap_')]
tap_cols = [c for c in tap_cols if TAP_START <= int(c.split('_')[1]) <= TAP_END]

print(f"Packets loaded : {len(df)}")
print(f"Taps used      : {TAP_START} → {TAP_END}  ({len(tap_cols)} taps)")

cir_matrix = df[tap_cols].values.astype(np.float64)  # shape: (packets, taps)


data = cir_matrix.flatten()


total_samples = len(data)
sample_rate = total_samples // recording_duration_seconds
print(f"Total samples  : {total_samples}")
print(f"Sample rate    : {sample_rate} Hz  (matches {recording_duration_seconds}s recording)")

# ====== NORMALIZE to [-1, 1] ======
max_val = np.max(np.abs(data))
if max_val > 0:
    data = data / max_val
else:
    raise ValueError("All CIR values are zero  nothing to convert.")

# ====== CONVERT TO 16-BIT PCM ======
audio = np.int16(data * 32767)

# ====== SAVE AS WAV ======
write(output_file, sample_rate, audio)
print(f"Audio saved    : '{output_file}'  ({len(audio) / sample_rate:.2f} seconds)")

# also save dominant-tap-only version 
dominant = df['tap_1'].values.astype(np.float64)
dominant_sr = len(dominant) // recording_duration_seconds
dominant_norm = dominant / np.max(np.abs(dominant))
dominant_audio = np.int16(dominant_norm * 32767)
write("cir_audio_dominant_tap.wav", dominant_sr, dominant_audio)
print(f"Dominant tap   : 'cir_audio_dominant_tap.wav'  (tap_1 only, {len(dominant_audio)/dominant_sr:.2f}s)")