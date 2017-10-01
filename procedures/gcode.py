import serial
ser = serial.Serial('/dev/ttyUSB0', baudrate=57600)

def sendGcode(command):
    return ser.write(command + "\n")
