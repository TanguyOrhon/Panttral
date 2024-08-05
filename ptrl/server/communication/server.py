import socket
import threading
import json
from .thread_client import ThreadClient


class Server:
    def __init__(self, host: str = '', port: int = 5566):
        """
        Initialize the server with the specified host and port.
        Sets up the server socket and loads configuration files.
        """
        self.active_threads = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        
        # Initialize locks for thread-safe file access
        self.data_get_lock = threading.Lock()
        self.data_settings_lock = threading.Lock()

        self.data_settings = None
        self.data_get = None
        self.open_file_get()
        self.open_file_settings()
        self.start_json_updater()

    def start(self) -> None:
        """
        Start accepting connections and create a new thread for each client.
        """
        try:
            while True:
                conn, address = self.server_socket.accept()
                print('Connection from', address)
                id_ = self.receive_conn(conn)
                self.send_id(conn, id_)
                my_thread = ThreadClient(conn, id_)
                my_thread.start()
                self.active_threads.append(my_thread)
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()
            print("Server stopped")

    def clean_threads(self) -> None:
        """
        Clean up the list of active threads by removing the ones that have stopped.
        Updates the settings to reflect the current number of active players.
        """
        self.active_threads = [t for t in self.active_threads if t.is_alive()]
        if len(self.active_threads) != self.data_settings["nb_active_players"]:
            self.data_settings["nb_active_players"] = len(self.active_threads)
            self.data_settings["active_players"] = [t.id for t in self.active_threads]
            print(f"Active threads: {len(self.active_threads)}")

    def create_client_json(self, id_: int) -> None:
        """
        Create a JSON file for the new client with the given ID.
        """
        data = {}
        try:
            with open(f'game/data_json/data_get_{id_}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error creating client JSON: {e}")

    def handle_json_data(self) -> None:
        """
        Continuously update the data JSON file and clean up threads.
        """
        while True:
            try:
                with self.data_get_lock:
                    with open(f'game/data_json/data_get.json', 'r+', encoding='utf-8') as f:
                        f.seek(0)
                        json.dump(self.data_get, f, indent=4)
                        f.truncate()
            except Exception as e:
                print(f"Error handling JSON data: {e}")
            self.clean_threads()
            self.update_data_get()
            self.handle_json_settings()

    def handle_json_settings(self) -> None:
        """
        Update the settings JSON file with current data.
        """
        try:
            with self.data_settings_lock:
                with open(f'game/data_json/settings.json', 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    json.dump(self.data_settings, f, indent=4)
                    f.truncate()
        except Exception as e:
            print(f"Error handling JSON settings: {e}")

    def open_file_get(self) -> None:
        """
        Load the data_get JSON file into memory.
        """
        try:
            with self.data_get_lock:
                with open("game/data_json/data_get.json", 'r') as f:
                    self.data_get = json.load(f)
        except Exception as e:
            print(f"Error loading data_get.json: {e}")

    def open_file_settings(self) -> None:
        """
        Load the settings JSON file into memory.
        """
        try:
            with self.data_settings_lock:
                with open("game/data_json/settings.json", 'r') as f:
                    self.data_settings = json.load(f)
        except Exception as e:
            print(f"Error loading settings.json: {e}")

    def receive_conn(self, conn: socket.socket) -> int:
        """
        Receive a connection from a client and determine the client's ID.
        """
        id_ = None
        try:
            prefix = conn.recv(4)
            if prefix == b'ID  ':
                id_ = int.from_bytes(conn.recv(1), 'big')
            if id_ == 0:
                self.data_settings["nb_players"] += 1
                id_ = self.data_settings["nb_players"]
                print(f"New client: id = {id_}")
                self.create_client_json(id_)
            else:
                print(f"Client ID = {id_}")
        except Exception as e:
            print(f"Error receiving connection: {e}")
        return id_

    def send_id(self, conn: socket.socket, id_: int) -> None:
        """
        Send the client ID back to the client.
        """
        try:
            id_prefix = b'ID  '
            conn.sendall(id_prefix + id_.to_bytes(1, 'big'))
        except Exception as e:
            print(f"Error sending ID: {e}")

    def start_json_updater(self) -> None:
        """
        Start a separate thread to update JSON data.
        """
        updater_thread = threading.Thread(target=self.handle_json_data, daemon=True)
        updater_thread.start()

    def update_data_get(self) -> None:
        """
        Update the data_get dictionary with the latest data from active players.
        """
        data_players = {}
        for i in self.data_settings["active_players"]:
            if i is not None:
                try:
                    with open(f'game/data_json/data_get_{i}.json', 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data_players[f"player_{i}"] = data
                except Exception as e:
                    print(f"Error updating data_get for player {i}: {e}")
        self.data_get["Players"] = data_players
