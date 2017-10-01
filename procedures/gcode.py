import serial
import io
ser = serial.Serial('/dev/ttyUSB0', baudrate=57600)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def sendGcode(command):
    sio.write(unicode(command + "\n"))
    sio.flush()
    return sio.readline()
