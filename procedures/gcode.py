import serial
import io
ser = serial.Serial('/dev/ttyACM0', baudrate=57600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def sendGcode(command):
    sio.write(str(command + "\n"))
    sio.flush()
    output = sio.readline()
    print(output)
    return output
