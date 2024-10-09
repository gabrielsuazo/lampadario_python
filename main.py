import time
from serial_communicator import SerialCommunicator

if __name__ == '__main__':
    print("Starting test")
    serial_communicator = SerialCommunicator("COM3", 9600)
    serial_communicator.register_listener()
    serial_communicator.queue_command(True, 0)
    serial_communicator.queue_command(False, 0)
    serial_communicator.queue_command(True, 0)
    serial_communicator.queue_command(False, 0)
    time.sleep(5)
    serial_communicator.send_command()
    time.sleep(5)
    serial_communicator.send_command()
    time.sleep(5)
    serial_communicator.send_command()
    time.sleep(5)
    serial_communicator.send_command()
    time.sleep(5)
    while True:
        if not serial_communicator.receive_queue.empty():
            received = serial_communicator.receive_queue.get()
            print(received)

