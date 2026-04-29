import serial
import csv
import time

PORT = "COM3"
BAUD = 115200
DURATION = 30  

ser = serial.Serial(PORT, BAUD, timeout=1)

filename = f"csi_{int(time.time())}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)

    start = time.time()

    while time.time() - start < DURATION:
        line = ser.readline()

        if not line:
            continue  # ignore b''

        try:
            decoded = line.decode("utf-8").strip()
        except:
            continue

        if "CSI_DATA" in decoded:
            print( decoded[:60])  # debug
            writer.writerow([decoded])

print(f"\nSaved to {filename}")
ser.close()