import time
import serial
import threading
import queue

NUM_BYTES_EVENT = 1


class SerialCommunicator:
    def __init__(self, port, baudrate):
        # Resets arduino when run
        self.listener = None
        self.is_listening = False
        self.ser = serial.Serial(port, baudrate)
        self.send_queue = queue.Queue()
        self.receive_queue = queue.Queue()

    def queue_command(self, candle_state: bool, candle_id: int):
        byte_command = candle_id
        if candle_state:
            byte_command += 128
        self.send_queue.put(bytes([byte_command]))

    def send_command(self):
        self.ser.write(self.send_queue.get())

    def read_event(self):
        if self.ser.in_waiting >= NUM_BYTES_EVENT:
            self.receive_queue.put(self.ser.read(NUM_BYTES_EVENT))

    def listen_event(self):
        while self.is_listening:
            self.read_event()

    def register_listener(self):
        self.listener = threading.Thread(target=self.listen_event)
        self.is_listening = True
        self.listener.start()

    def de_init(self):
        self.is_listening = False
        if self.listener is not None:
            self.listener.join()
        self.ser.close()


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

