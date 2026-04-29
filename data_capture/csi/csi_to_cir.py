import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ====== CONFIG ======
input_file = r"C:\Users\Lenovo\Desktop\Proj\data_capture\csi\csi_data_2025-05-07_20-17-52.449.csv"   # <-- change this
output_file = "cir_output.csv"
plot_output = "cir_plot.png"

NUM_SUBCARRIERS = 64  # 128 values = 64 complex pairs (imag, real)

# ====== LOAD DATA ======
df = pd.read_csv(input_file)
print(f"Loaded {len(df)} packets")

# ====== PARSE CSI AND COMPUTE CIR ======
cir_list = []

for idx, row in df.iterrows():
    vals = list(map(int, row['CSI_Data'].strip('[]').split()))

    # Each pair is [imaginary, real] — ESP32 CSI format
    imag = np.array(vals[0::2], dtype=np.float64)  # even indices
    real = np.array(vals[1::2], dtype=np.float64)  # odd indices

    # Build complex CSI vector (frequency domain)
    csi_complex = real + 1j * imag  # shape: (64,)

    # Zero out null/pilot subcarriers (ESP32: indices 0, 27-37 are invalid)
    null_indices = [0] + list(range(27, 38))
    csi_complex[null_indices] = 0 + 0j

    # IFFT to convert frequency domain → time domain (CIR)
    cir = np.fft.ifft(csi_complex, n=NUM_SUBCARRIERS)

    # Take magnitude of CIR (power delay profile)
    cir_magnitude = np.abs(cir)

    cir_list.append(cir_magnitude)

cir_array = np.array(cir_list)  # shape: (num_packets, 64)
print(f"CIR matrix shape: {cir_array.shape}  (packets × delay taps)")

# ====== SAVE CIR TO CSV ======
cir_df = pd.DataFrame(
    cir_array,
    columns=[f"tap_{i}" for i in range(NUM_SUBCARRIERS)]
)
cir_df.insert(0, 'Timestamp', df['Timestamp'].values)
cir_df.to_csv(output_file, index=False)
print(f"CIR saved to '{output_file}'")

# ====== PLOT: CIR HEATMAP OVER TIME ======
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# --- Plot 1: Heatmap (time vs delay tap) ---
ax1 = axes[0]
im = ax1.imshow(
    cir_array.T,
    aspect='auto',
    origin='lower',
    cmap='plasma',
    interpolation='nearest'
)
ax1.set_xlabel('Packet Index (time →)', fontsize=12)
ax1.set_ylabel('Delay Tap', fontsize=12)
ax1.set_title('Channel Impulse Response (CIR) — Heatmap over Time', fontsize=13)
plt.colorbar(im, ax=ax1, label='Magnitude')

# --- Plot 2: Mean CIR (average power delay profile) ---
ax2 = axes[1]
mean_cir = cir_array.mean(axis=0)
ax2.plot(mean_cir, color='cyan', linewidth=1.5)
ax2.fill_between(range(NUM_SUBCARRIERS), mean_cir, alpha=0.3, color='cyan')
ax2.set_xlabel('Delay Tap', fontsize=12)
ax2.set_ylabel('Mean Magnitude', fontsize=12)
ax2.set_title('Mean Power Delay Profile (averaged across all packets)', fontsize=13)
ax2.set_facecolor('#0d0d0d')
ax2.grid(True, alpha=0.2)

fig.patch.set_facecolor('#1a1a2e')
for ax in axes:
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#444')

plt.tight_layout(pad=2.0)
plt.savefig(plot_output, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f"Plot saved to '{plot_output}'")

# ====== SUMMARY ======
print(f"\n--- CIR Summary ---")
print(f"Packets processed : {cir_array.shape[0]}")
print(f"Delay taps        : {cir_array.shape[1]}")
print(f"Max magnitude     : {cir_array.max():.4f}")
print(f"Mean magnitude    : {cir_array.mean():.4f}")
print(f"Dominant tap (avg): tap_{mean_cir.argmax()} (strongest multipath component)")