import serial


def send_command():
    ser = serial.Serial("COM3", 9600)
    command = bytes([255])
    ser.write(command)


if __name__ == '__main__':
    send_command()

