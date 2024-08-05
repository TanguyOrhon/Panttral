from socket import socket, AF_INET, SOCK_STREAM
import json
import os
import threading

class Client:
    def __init__(self) -> None:
        """
        Initialize the client with server connection details and load necessary files.
        """
        self.host = 'localhost'
        self.port = 5566
        self.data_set = None
        self.data_get = None
        self.data_settings = None
        self.image_data = None
        self.stop_connection = False
        self.lock = threading.Lock()  # Initialize a lock for thread safety
        self.open_file()
        self.id = self.data_settings["id"]

    def calculate_sum(self, a, b):
        """
        Example function to demonstrate locks in non-I/O operations.
        """
        with self.lock:
            return a + b

    def close_socket(self, conn: socket) -> None:
        """
        Close the connection to the server.
        """
        try:
            id_prefix = b'CLS '
            conn.sendall(id_prefix)
            conn.close()
            print("Disconnected")
        except Exception as e:
            print(f"Error closing socket: {e}")

    def connection(self) -> None:
        """
        Establish a connection to the server and handle communication.
        """
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print("Client connected")

            self.send_id(client_socket)
            self.receive_conn(client_socket)
            self.handle_json_settings()

            while not self.stop_connection:
                self.send_data(client_socket)
                self.get_data(client_socket)
                self.handle_json_data()

            self.close_socket(client_socket)

        except Exception as e:
            print(f"Connection refused: {e}")

    def get_data(self, conn: socket) -> None:
        """
        Receive data from the server and handle based on prefix.
        """
        try:
            prefix = conn.recv(4)
            if prefix == b'JSON':
                self.receive_json(conn)
            elif prefix == b'IMG ':
                self.receive_images(conn)
            elif prefix == b'ID  ':
                self.receive_conn(conn)
            else:
                print("Unknown data type prefix received")
        except Exception as e:
            print(f"Error getting data: {e}")

    def handle_json_data(self) -> None:
        """
        Update the local JSON data get file with the latest data received from the server.
        """
        with self.lock:  # Lock the file access
            try:
                with open('game/data_json/data_get.json', 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    json.dump(self.data_get, f, indent=4)
                    f.truncate()
            except Exception as e:
                print(f"Error handling JSON data: {e}")

    def handle_json_settings(self) -> None:
        """
        Update and save the settings JSON file with current data.
        """
        with self.lock:  # Lock the file access
            try:
                with open('game/data_json/settings.json', 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    json.dump(self.data_settings, f, indent=4)
                    f.truncate()
            except Exception as e:
                print(f"Error handling JSON settings: {e}")

    def open_file(self) -> None:
        """
        Load data set, data get, and settings JSON files.
        """
        self.open_file_set()
        self.open_file_get()
        self.open_file_settings()

    def open_file_get(self) -> None:
        """
        Load the JSON data get file.
        """
        with self.lock:  # Lock the file access
            try:
                with open("game/data_json/data_get.json", 'r', encoding='utf-8') as f:
                    self.data_get = json.load(f)
            except Exception as e:
                print(f"Error loading data_get.json: {e}")

    def open_file_set(self) -> None:
        """
        Load the JSON data set file.
        """
        with self.lock:  # Lock the file access
            try:
                with open("game/data_json/data_set.json", 'r', encoding='utf-8') as f:
                    self.data_set = json.load(f)
            except Exception as e:
                print(f"Error loading data_set.json: {e}")

    def open_file_settings(self) -> None:
        """
        Load the settings JSON file.
        """
        with self.lock:  # Lock the file access
            try:
                with open("game/data_json/settings.json", 'r', encoding='utf-8') as f:
                    self.data_settings = json.load(f)
            except Exception as e:
                print(f"Error loading settings.json: {e}")

    def receive_conn(self, conn: socket) -> None:
        """
        Receive client ID from the server and update local settings.
        """
        try:
            prefix = conn.recv(4)
            if prefix == b'ID  ':
                self.id = int.from_bytes(conn.recv(1), 'big')
                self.data_settings["id"] = self.id
                print(f"Client ID = {self.data_settings['id']}")
        except Exception as e:
            print(f"Error receiving connection: {e}")

    def receive_images(self, conn: socket) -> None:
        """
        Receive image data from the server and save it locally.
        """
        try:
            image_size = int.from_bytes(conn.recv(4), 'big')

            image_data = b''
            while len(image_data) < image_size:
                packet = conn.recv(image_size - len(image_data))
                if not packet:
                    break
                image_data += packet

            if image_data:
                with self.lock:  # Lock the file access
                    with open('assets/caracters/main_caracter.png', 'wb') as f:
                        f.write(image_data)

        except Exception as e:
            print(f"Error receiving images: {e}")

    def receive_json(self, conn: socket) -> None:
        """
        Receive JSON data from the server and update local data_get.
        """
        try:
            json_size = int.from_bytes(conn.recv(4), 'big')

            json_data = b''
            while len(json_data) < json_size:
                packet = conn.recv(json_size - len(json_data))
                if not packet:
                    break
                json_data += packet

            if json_data:
                with self.lock:  # Lock the data access
                    self.data_get = json.loads(json_data.decode('utf-8'))

        except Exception as e:
            print(f"Error receiving JSON: {e}")

    def send_data(self, conn: socket) -> None:
        """
        Send current data set to the server.
        """
        self.open_file_set()
        self.send_json(conn)

    def send_id(self, conn: socket) -> None:
        """
        Send client ID to the server.
        """
        try:
            id_prefix = b'ID  '
            conn.sendall(id_prefix + self.id.to_bytes(1, 'big'))
        except Exception as e:
            print(f"Error sending ID: {e}")

    def send_json(self, conn: socket) -> None:
        """
        Send JSON-encoded data to the server.
        """
        try:
            json_prefix = b'JSON'
            data = json.dumps(self.data_set).encode('utf-8')
            json_size = len(data)
            conn.sendall(json_prefix + json_size.to_bytes(4, 'big') + data)
        except Exception as e:
            print(f"Error sending JSON: {e}")
