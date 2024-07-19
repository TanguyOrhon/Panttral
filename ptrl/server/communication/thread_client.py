from threading import Thread
import socket
import json
import pickle
import threading
from typing import List

class ThreadClient(Thread):
    def __init__(self, conn: socket.socket) -> None:
        super().__init__()
        self.conn = conn
        self.data_set = None        
        self.data_get = None
        self.image_data = None
        self.open_file()

    def run(self) -> None:
        while True:
            self.send_data()
            self.get_data()
            self.handle_json_data()

    def send_data(self):
        self.send_json()

    def send_json(self):
        json_prefix = b'JSON'
        data = json.dumps(self.data_set).encode('utf-8')
        json_size = len(data)
        self.conn.sendall(json_prefix + json_size.to_bytes(4, 'big') + data)
        self.conn.sendall(b'')

    def send_image(self):
        image_size = len(self.image_data)
        image_prefix = b"IMG "
        self.conn.sendall(image_prefix + image_size.to_bytes(4, 'big') + self.image_data)
        self.conn.sendall(b'')

    def get_data(self):
            prefix = self.conn.recv(4)
            if prefix == b'JSON':
                self.receive_json()
            elif prefix == b'IMG ':
                self.receive_images()
            else:
                raise ValueError("Unknown data type prefix received")

    def open_file(self) :
        try:
            with open("game/data_json/data_set.json", 'r', encoding='utf-8') as f:
                self.data_set = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de décodage JSON dans le fichier {self.data_player_path}: {e}")
        except IOError as e:
            raise IOError(f"Erreur de lecture du fichier {self.data_player_path}: {e}")
        

        
        try:
            with open("game/data_json/data_get.json", 'r') as data_get:
                self.data_get = json.load(data_get)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de décodage JSON dans le fichier game/data_json/data_get.json : {e}")
        except IOError as e:
            raise IOError(f"Erreur de lecture du fichier game/data_json/data_get.json : {e}")
        
        # try:
        #     with open(self.image_path, 'rb') as data_image:
        #         self.image_data = data_image.read()
        # except json.JSONDecodeError as e:
        #     raise ValueError(f"Erreur de décodage JSON dans le fichier {self.image_path}: {e}")
        # except IOError as e:
            # raise IOError(f"Erreur de lecture du fichier {self.image_path}: {e}")

    def handle_json_data(self):
        lock = threading.Lock()
        with lock:
            with open("game/data_json/data_get.json", 'r+', encoding='utf-8') as f:
                json.dump(self.data_get, f, ensure_ascii=False, indent=4)

    def receive_json(self):
        # Réception de la taille de l'image
        json_size = int.from_bytes(self.conn.recv(4), 'big')
        
        # Réception des données de l'image
        json_data = b''
        while len(json_data) < json_size:
            packet = self.conn.recv(json_size - len(json_data))
            if not packet:
                break
            json_data += packet
            # Sauvegarde de l'image reçue
        if not json_data == b'':
            json_data = json_data.decode('utf-8')
            self.data_get = json.loads(json_data)
            print(json_data)