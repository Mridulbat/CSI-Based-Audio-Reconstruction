import numpy as np
import pandas as pd
import scipy.signal as signal
import matplotlib.pyplot as plt
import soundfile as sf


CSV_FILE = "clap_sample.csv"

CSI_FS = 10          # your sampling rate
PEAK_DISTANCE = 0.5  # seconds between claps
AUDIO_FS = 44100

# ==================

print("[1] Loading data...")

df = pd.read_csv(CSV_FILE, header=None)
csi_data = df.values

print("Shape:", csi_data.shape)



signal_1d = np.std(csi_data, axis=1)


nyq = CSI_FS / 2

if CSI_FS < 30:
    print("⚠ Low sampling rate → using low-pass filter")
    cutoff = nyq * 0.8
    b, a = signal.butter(2, cutoff / nyq, btype='low')
else:
    low = 5
    high = min(80, nyq * 0.9)
    b, a = signal.butter(4, [low/nyq, high/nyq], btype='band')

filtered = signal.filtfilt(b, a, signal_1d)


from scipy.signal import hilbert
envelope = np.abs(hilbert(filtered))


norm = (envelope - envelope.mean()) / (envelope.std() + 1e-9)


window = 3
smooth = np.convolve(norm, np.ones(window)/window, mode='same')

threshold = max(0.8, np.mean(smooth) + 0.8*np.std(smooth))


min_samples = int(PEAK_DISTANCE * CSI_FS)

peaks, _ = signal.find_peaks(
    smooth,
    height=threshold,
    distance=max(1, min_samples),
    prominence=0.3
)

clap_times = peaks / CSI_FS

print("Threshold:", round(threshold, 2))
print("Claps detected:", np.round(clap_times, 3))
print("Number of peaks:", len(peaks))


duration = len(signal_1d) / CSI_FS
n_samples = int(duration * AUDIO_FS)

output = np.zeros(n_samples)

# clap sound
t_env = np.linspace(0, 0.08, int(AUDIO_FS * 0.08))
clap = np.random.randn(len(t_env)) * np.exp(-t_env * 40)

for t in clap_times:
    idx = int(t * AUDIO_FS)
    if idx + len(clap) < n_samples:
        output[idx:idx+len(clap)] += clap

# normalize
if np.max(np.abs(output)) > 0:
    output = output / np.max(np.abs(output)) * 0.9

sf.write("output.wav", output, AUDIO_FS)


time = np.arange(len(smooth)) / CSI_FS

plt.figure(figsize=(10,5))
plt.plot(time, smooth, label="Signal")
plt.axhline(threshold, color='orange', linestyle='--', label="Threshold")
plt.scatter(clap_times, smooth[peaks], color='red', label="Detected")
plt.legend()
plt.title("Clap Detection (CSI)")
plt.savefig("plot.png")

print("DONE")