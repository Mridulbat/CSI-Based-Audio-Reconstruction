# WiFi-CSI-Based Activity Recognition

This project explores the capabilities of WiFi based device-free sensing by leveraging Channel State
Information (CSI) and Channel Impulse Response (CIR) to detect environmental patterns. The work
begins with a focus on research into CSI data collection methodologies and software frameworks,
followed by a hardware implementation using the ESP32 platform While exploring possible
Hardware and software for WiFi 6/7 Standards.
The technical core of the work involves a multi-stage data processing pipeline. Raw CSI data is
captured by reading data from the serial port and then converted into Amplitude and Phase for each
sub carrier allowing us to get a better picture of our data. The CSI signal is converted into CIR
using IFFT to get an idea about the data in the time domain. This process allowed for a direct
magnitude and pattern comparison between signal-derived "audio" and actual acoustic recordings.
The later part of the work focused on mapping specific physical activities and environmental
disturbances to signal fluctuations. This included collecting data under controlled noise conditions,
such as background clapping, to test the system’s sensitivity. By comparing the waveforms of actual
audio against those generated from CSI/CIR data, and then attempting to find conclusive patterns
by comparing the waveforms using techniques like Cosine Similarity.


An ESP32 captures CSI at 100 Hz over a standard WiFi link and sends it over USB serial at a baud rate of 921600 . A microphone records in parallel. Both streams are timestamped and aligned.

<div align="center">
  <img src="data_capture/csi_plot/csi_data_2024-09-25_22-01-04.590_amp_all_subcarriers.png?raw=true" width="45%" alt="CSI amplitude — all subcarriers">
  <img src="data_capture/csi_plot/csi_data_2024-09-25_16-27-42.805_heatmap.png?raw=true" width="45%" alt="CSI amplitude + phase heatmap">
</div>
<div align="center">
  <img src="data_capture/audio_plot/2024-09-25_22-01-04.590_spectrogram.png?raw=true" width="45%" alt="Mel-spectrogram of synchronized audio">
  <img src="data_capture/audio_plot/2024-09-25_22-01-04.590_time_series.png?raw=true" width="45%" alt="Audio time-series">
</div>
<div align="center"><em>Top row: CSI amplitude time-series (left) and amplitude/phase heatmap (right). Bottom row: Synchronized audio mel-spectrogram (left) and audio time-series (right).</em></div>





### 1. Flash ESP32 Firmware

Flash the [ESP32 CSI Toolkit](https://github.com/StevenMHernandez/esp32-csi-tool) (`active_sta` mode) using ESP-IDF v4.3. Full instructions: [Flashing Firmware](https://github.com/Cryio/Wifi-CSI-Based-Activity-Recognition/wiki/Flashing-Firmware).

### 2. Capture Data

```bash
cd data_capture
python record_both.py
```

Captures CSI from `/dev/ttyUSB0` at 1 Mbaud and audio from the default microphone simultaneously for 10 seconds, saving timestamped CSV and WAV files.

```

## Hardware

| Component | Details |
|-----------|---------|
| ESP32 DevKit | CSI capture via USB serial at 1 Mbaud |
| Router | Standard 2.4 GHz WiFi AP |
| Microphone | Any USB or 3.5 mm mic supported by PyAudio |
| Host PC / Raspberry Pi | Runs `record_both.py` |



## References

See the [References](https://github.com/Cryio/Wifi-CSI-Based-Activity-Recognition/wiki/References) wiki page for the full list of academic papers and tools this project builds on.
