from threading import Thread, Lock
import socket
import json
import threading

class ThreadClient(Thread):
    def __init__(self, conn: socket.socket, id_: int) -> None:
        """
        Initialize the thread client with a connection and a client ID.
        """
        super().__init__()
        self.conn = conn
        self.data_set = None        
        self.data_get = None
        self.image_data = None
        self.id = id_
        self.running = True
        
        # Initialize lock for thread-safe file access
        self.file_lock = threading.Lock()

        self.open_file_set()

    def run(self) -> None:
        """
        Main thread loop to handle client communication.
        """
        while self.running:
            try:
                self.send_data()            
                self.get_data()
                self.handle_json_data()
            except Exception as e:
                print(f"Error in client thread {self.id}: {e}")
                self.running = False
        self.conn.close()

    def send_data(self) -> None:
        """
        Send JSON data to the client.
        """
        self.open_file_set()
        self.send_json()

    def send_json(self) -> None:
        """
        Send JSON-encoded data to the client with a specific prefix and size.
        """
        json_prefix = b'JSON'
        data = json.dumps(self.data_set).encode('utf-8')
        json_size = len(data)
        try:
            self.conn.sendall(json_prefix + json_size.to_bytes(4, 'big') + data)
        except Exception as e:
            print(f"Error sending JSON data to client {self.id}: {e}")

    def send_image(self) -> None:
        """
        Send image data to the client with a specific prefix and size.
        """
        if self.image_data:
            image_size = len(self.image_data)
            image_prefix = b"IMG "
            try:
                self.conn.sendall(image_prefix + image_size.to_bytes(4, 'big') + self.image_data)
            except Exception as e:
                print(f"Error sending image data to client {self.id}: {e}")
                self.conn.close()

    def get_data(self) -> None:
        """
        Receive data from the client and handle it based on the prefix.
        """
        try:
            prefix = self.conn.recv(4)
            if prefix == b'JSON':
                self.receive_json()
            elif prefix == b'IMG ':
                self.receive_images()
            elif prefix == b'CLS ':
                self.conn.close()
                self.running = False
                print(f"Client {self.id} disconnected")
            else:
                print("Unknown data type prefix received")
        except Exception as e:
            print(f"Error receiving data from client {self.id}: {e}")
            self.running = False

    def handle_json_data(self) -> None:
        """
        Update the client's JSON data file with the latest data received.
        """
        try:
            with self.file_lock:
                with open(f'game/data_json/data_get_{self.id}.json', 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    json.dump(self.data_get, f, indent=4)
                    f.truncate()
        except Exception as e:
            print(f"Error handling JSON data for client {self.id}: {e}")

    def receive_json(self) -> None:
        """
        Receive and process JSON data sent from the client.
        """
        try:
            # Receive the size of the JSON data
            json_size = int.from_bytes(self.conn.recv(4), 'big')
            
            # Receive the JSON data itself
            json_data = b''
            while len(json_data) < json_size:
                packet = self.conn.recv(json_size - len(json_data))
                if not packet:
                    break
                json_data += packet

            # Process the received JSON data
            if json_data:
                json_data = json_data.decode('utf-8')
                self.data_get = json.loads(json_data)
        except Exception as e:
            print(f"Error receiving JSON data from client {self.id}: {e}")
            self.running = False

    def receive_images(self) -> None:
        """
        Receive and process image data sent from the client.
        """
        try:
            # Receive the size of the image
            image_size = int.from_bytes(self.conn.recv(4), 'big')

            # Receive the image data itself
            self.image_data = b''
            while len(self.image_data) < image_size:
                packet = self.conn.recv(image_size - len(self.image_data))
                if not packet:
                    break
                self.image_data += packet

            # Process the received image data
            if self.image_data:
                print(f"Image received from client {self.id}")
                # You can add code here to save or process the image data
        except Exception as e:
            print(f"Error receiving image data from client {self.id}: {e}")

    def open_file_set(self) -> None:
        """
        Load the data_set JSON file into memory.
        """
        try:
            with self.file_lock:
                with open("game/data_json/data_set.json", 'r', encoding='utf-8') as f:
                    self.data_set = json.load(f)
        except Exception as e:
            print(f"Error loading data_set.json for client {self.id}: {e}")
