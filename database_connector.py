import mysql.connector


class DatabaseConnector:
    def __init__(self, user, password, host, database):
        self.connexion = mysql.connector.connect(user=user, password=password, host=host, database=database)
        self.cursor = self.connexion.cursor()

    def recover_table_state(self):
        query = "SELECT id, state FROM candles"
        self.cursor.execute(query)

    def turn_candle_on(self, command):
        command_int = int.from_bytes(command, byteorder='big', signed=False)
        candle_id = (command_int - 127)
        query = "UPDATE candles SET state = 1 WHERE id = %(candle_id)s;"
        map_data = {
            'candle_id': candle_id
        }
        self.cursor.execute(query, map_data)
        self.connexion.commit()

    def de_init(self):
        self.cursor.close()
        self.connexion.close()
