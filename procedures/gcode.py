import serial
import io
ser = serial.Serial('/dev/ttyACM0', baudrate=57600, timeout=2)

def sendGcode(command):
    ser.write(bytes(command + "\n", "utf-8"))
    while True:
        output = str(ser.readline(), "utf-8")
        print(output)
        if output.strip() == "READY":
            ser.reset_input_buffer()
            break
        else:
            print("WAITING")
            continue
    print(output)
    return output
