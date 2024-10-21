import time

from database_connector import DatabaseConnector
from serial_communicator import SerialCommunicator


if __name__ == '__main__':
    print("Starting test")
    serial_communicator = SerialCommunicator("COM3", 9600)
    time.sleep(3)
    database_connector = DatabaseConnector("root", "", "localhost", "lampadario")
    database_connector.recover_table_state()

    for (candle_id, state) in database_connector.cursor:
        bool_state = (state == 1)
        serial_communicator.queue_command(bool_state, int(candle_id) - 1)
    database_connector.de_init()
    serial_communicator.register_listener()

    while True:
        if not serial_communicator.send_queue.empty():
            serial_communicator.send_command()

        elif not serial_communicator.receive_queue.empty():
            received = serial_communicator.receive_queue.get()
            database_connector = DatabaseConnector("root", "", "localhost", "lampadario")
            database_connector.turn_candle_on(received)
            database_connector.de_init()

        else:
            database_connector = DatabaseConnector("root", "", "localhost", "lampadario")
            database_connector.recover_table_state()

            for (candle_id, state) in database_connector.cursor:
                bool_state = (state == 1)
                serial_communicator.queue_command(bool_state, int(candle_id) - 1)
            database_connector.de_init()
            time.sleep(3)
