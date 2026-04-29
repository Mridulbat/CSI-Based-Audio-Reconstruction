import serial

ser = serial.Serial("COM3", 115200, timeout=1)

while True:
    line = ser.readline()
    print(line)