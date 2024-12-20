import serial
import socket
import time

SERIAL_PORT = 'COM3'  # Adjust for your Teensy
SERIAL_BAUD = 9600

UDP_IP = "0.0.0.0"
UDP_PORT = 8284

try:
    ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")
    ser = None

print("Connected to Teensy on", SERIAL_PORT)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Listening on {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    command = data.decode('utf-8').strip()
    print(f"Received UDP command: {command} from {addr}")

    # Forward to Teensy over serial
    if ser and ser.is_open:
        ser.write((command + "\n").encode('utf-8'))
        time.sleep(0.05)
        response = ser.readline().decode('utf-8').strip()
        if response:
            print("Teensy response:", response)