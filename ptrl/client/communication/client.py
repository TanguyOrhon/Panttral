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

    def handle_json_data(self, data_received):
        # Sauvegarder les données actuelles avant de les écraser
        with open(self.backup_filepath, 'w', encoding='utf-8') as f_backup:
            json.dump(data_received, f_backup, ensure_ascii=False, indent=4)

        # Écriture du JSON modifié dans le fichier
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data_received, f, ensure_ascii=False, indent=4)

    def receive_data(self, conn: socket):
        while True:
            prefix = conn.recv(4)
            print(prefix)
            if prefix == b'JSON':
                self.receive_json(conn)
                # print("test_prefix")
                # data = self.receive_all_data(conn)  # Implement a method to read all remaining data
                # print(data)
                # if data:
                #         json_data = json.loads(data)
                #         self.data_received[0]["content"]["name"] = json_data[0]["content"]["name"]
                #         self.data_received[0]["content"]["position_x"] = json_data[0]["content"]["position_x"]
                #         self.data_received[0]["content"]["position_y"] = json_data[0]["content"]["position_y"]
                #         # Écriture du JSON modifié dans le fichier
                #         self.handle_json_data(self.data_received)
                #         print(json_data)

            elif prefix == b'IMG ':
                self.receive_images(conn)
            else:
                raise ValueError("Unknown data type prefix received")
    
    def receive_images(self, conn):
        print("test_image")
        # Réception de la taille de l'image
        image_size = int.from_bytes(conn.recv(4), 'big')
        
        # Réception des données de l'image
        image_data = b''
        while len(image_data) < image_size:
            packet = conn.recv(image_size - len(image_data))
            if not packet:
                break
            image_data += packet
            # Sauvegarde de l'image reçue
        if not image_data == b'':
            with open(f'assets/caracters/main_caracter.png', 'wb') as f:
                f.write(image_data)

    def receive_json(self, conn):
        # Réception de la taille de l'image
        json_size = int.from_bytes(conn.recv(4), 'big')
        
        # Réception des données de l'image
        json_data = b''
        while len(json_data) < json_size:
            packet = conn.recv(json_size - len(json_data))
            if not packet:
                break
            json_data += packet
            # Sauvegarde de l'image reçue
        if not json_data == b'':
            json_data = json_data.decode('utf-8')
            json_data = json.loads(json_data)
            print(json_data)
            self.handle_json_data(json_data)

    def receive_all_data(self, conn):
        data = b""
        while True:
            part = conn.recv(1024)
            data += part
            if len(part) < 1024:
                break
        return data

