import serial
import io
ser = serial.Serial('/dev/ttyACM0', baudrate=57600, timeout=2)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def sendGcode(command):
    sio.write(str(command + "\n"))
    sio.flush()
    while True:
        output = sio.readline()
        if output == "READY":
            break
        else:
            continue
    print(output)
    return output
