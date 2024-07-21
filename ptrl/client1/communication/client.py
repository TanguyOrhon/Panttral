from socket import *
import time
from game.settings import *
import json
import pickle

class Client:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.port = 5566
        self.data_set = None
        self.data_get = None
        self.image_data = None
        self.open_file()
        self.stop_connection = False

    def connection(self):
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print("Client connected")
            while not self.stop_connection:
                self.get_data(client_socket)
                self.send_data(client_socket)
                self.handle_json_data()
            client_socket.close()
        except Exception as e:
            print(f"Connection refused: {e}")
            pass

    def handle_json_data(self):
        with open('game/data_json/data_get.json', 'r+', encoding='utf-8') as f:
            f.seek(0)
            json.dump(self.data_get, f, indent=4)
            f.truncate()

    def get_data(self, conn: socket):
            prefix = conn.recv(4)
            if prefix == b'JSON':
                self.receive_json(conn)
            elif prefix == b'IMG ':
                self.receive_images(conn)
            else:
                print("Unknown data type prefix received")
            
    def send_data(self, conn: socket):
        self.open_file_set()
        self.send_json(conn)
    
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
            self.data_get = json.loads(json_data)

    def send_json(self, conn):
        json_prefix = b'JSON'
        data = json.dumps(self.data_set).encode('utf-8')
        json_size = len(data)
        conn.sendall(json_prefix + json_size.to_bytes(4, 'big') + data)
        conn.sendall(b'')

    def open_file(self) :
        self.open_file_set()
        self.open_file_get()    

    def open_file_get(self):
        try:
            with open("game/data_json/data_get.json", 'r') as f:
                self.data_get = json.load(f)
        except:
            print("error")
            pass

    def open_file_set(self): 
        try :
            with open("game/data_json/data_set.json", 'r', encoding='utf-8') as f:
                self.data_set = json.load(f)
        except:
            print("error")
            pass