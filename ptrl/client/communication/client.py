from socket import *
import time
from game.settings import *
import json

class Client:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.port = 5566
        self.filepath = "game/data_json/data_received.json"
        self.backup_filepath = "game/data_json/data_backup.json"
        self.image_path = "assets/caracters/main_caracter.png"
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data_received = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de décodage JSON dans le fichier {self.filepath}: {e}")
        except IOError as e:
            raise IOError(f"Erreur de lecture du fichier {self.filepath}: {e}")



    def connection(self):
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print("Client connected")
            self.receive_data(client_socket)
        except Exception as e:
            print(f"Connection refused: {e}")
        finally:
            time.sleep(0.02)

    def handle_json_data(self):
        # Sauvegarder les données actuelles avant de les écraser
        with open(self.backup_filepath, 'w', encoding='utf-8') as f_backup:
            json.dump(self.data_received, f_backup, ensure_ascii=False, indent=4)

        # Écriture du JSON modifié dans le fichier
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data_received, f, ensure_ascii=False, indent=4)

    def handle_image_data(self):
        with open('received_image.png', 'wb') as image_file:
            image_file.write(self.image_path)


    def receive_data(self, conn: socket):
        while True:
            prefix = conn.recv(4)
            print(prefix)
            if prefix == b'JSON':
                print("test")
                data = self.receive_all_data(conn)  # Implement a method to read all remaining data
                if data:
                        json_data = json.loads(data)
                        self.data_received[0]["content"]["name"] = json_data[0]["content"]["name"]
                        self.data_received[0]["content"]["position_x"] = json_data[0]["content"]["position_x"]
                        self.data_received[0]["content"]["position_y"] = json_data[0]["content"]["position_y"]
                        # Écriture du JSON modifié dans le fichier
                        self.handle_json_data()
                        print(json_data)

            elif prefix == b'IMG':
                image_data = self.receive_all_data(conn)  # Implement a method to read all remaining data
                self. handle_image_data(image_data)
            else:
                raise ValueError("Unknown data type prefix received")
    
    def receive_all_data(self, conn: socket):
        # Read all remaining data from the connection until EOF
        data = b''
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        return data
