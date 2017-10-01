import serial
ser = serial.Serial('/dev/ttyUSB0')

def sendGcode(command):
    ser.write(command + "\n")
