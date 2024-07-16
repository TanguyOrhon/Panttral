from threading import Thread
import socket
import json

class ThreadClient(Thread):
    def __init__(self, conn: socket.socket) -> None:
        super().__init__()
        self.conn = conn
        self.data_player_path = "game/data_json/data_serv.json"
        self.backup_data_player_path = "game/data_json/data_backup.json"
        self.image_path = "assets/caracters/main_caracter.png"
        self.data_sent = None
        self.image_data = None

    def run(self) -> None:
        self.open_file()
        self.send_json()
        #self.send_image()

    def send_json(self):
        json_prefix = b'JSON'
        data = json.dumps(self.data_sent).encode('utf-8')
        json_size = len(data)
        self.conn.sendall(json_prefix + json_size.to_bytes(4, 'big') + data)
        self.conn.sendall(b'')

    def send_image(self):
        image_size = len(self.image_data)
        image_prefix = b"IMG "
        self.conn.sendall(image_prefix + image_size.to_bytes(4, 'big') + self.image_data)
        self.conn.sendall(b'')

    
    def open_file(self) :
        try:
            with open(self.data_player_path, 'r', encoding='utf-8') as data_player:
                self.data_sent = json.load(data_player)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de décodage JSON dans le fichier {self.data_player_path}: {e}")
        except IOError as e:
            raise IOError(f"Erreur de lecture du fichier {self.data_player_path}: {e}")
        
        try:
            with open(self.image_path, 'rb') as data_image:
                self.image_data = data_image.read()
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de décodage JSON dans le fichier {self.image_path}: {e}")
        except IOError as e:
            raise IOError(f"Erreur de lecture du fichier {self.image_path}: {e}")

    def send_file(self, filename, prefix):
        with open(filename, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                self.conn.sendall(prefix + data)
        # Send a zero-length message to indicate the end of the file
        self.conn.sendall(b'')