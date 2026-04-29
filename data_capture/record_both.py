import os
import serial
import csv
import time
import threading
import pyaudio
import wave



SERIAL_PORT = "/dev/ttyUSB0" 
BAUD_RATE = 921600

CSI_DURATION = 10
AUDIO_DURATION = 10
TOTAL_DURATION = 10

CSI_DIR = "csi"
AUDIO_DIR = "audio"



os.makedirs(CSI_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_timestamp():
    return time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())



class CSICapture:
    def __init__(self, port, baud, duration, stop_event, timestamp):
        self.port = port
        self.baud = baud
        self.duration = duration
        self.stop_event = stop_event

        self.ser = serial.Serial(self.port, self.baud, timeout=1)

        self.filepath = os.path.join(CSI_DIR, f"csi_{timestamp}.csv")

    def start(self):
        with open(self.filepath, "w", newline="") as f:
            writer = csv.writer(f)

            start_time = time.time()

            try:
                while not self.stop_event.is_set():

                    if time.time() - start_time > self.duration:
                        break

                    line = self.ser.readline()

                    if not line:
                        continue

                    line = line.decode(errors="ignore").strip()

                    if "CSI_DATA" in line:
                        writer.writerow(line.split(","))
                        f.flush()

            except Exception as e:
                print("CSI ERROR:", e)

            finally:
                self.ser.close()
                print("CSI saved:", self.filepath)



class AudioCapture:
    def __init__(self, duration, stop_event, timestamp):
        self.duration = duration
        self.stop_event = stop_event
        self.filepath = os.path.join(AUDIO_DIR, f"{timestamp}.wav")

    def start(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        frames = []
        start_time = time.time()

        while not self.stop_event.is_set():
            if time.time() - start_time > self.duration:
                break

            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        wf = wave.open(self.filepath, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()

        print("Audio saved:", self.filepath)



def run():
    stop_event = threading.Event()
    timestamp = generate_timestamp()

    csi = CSICapture(SERIAL_PORT, BAUD_RATE, CSI_DURATION, stop_event, timestamp)
    audio = AudioCapture(AUDIO_DURATION, stop_event, timestamp)

    csi_thread = threading.Thread(target=csi.start)
    csi_thread.start()

    audio.start()

    time.sleep(TOTAL_DURATION)
    stop_event.set()

    csi_thread.join()

    print(" Done")



if __name__ == "__main__":
    run()