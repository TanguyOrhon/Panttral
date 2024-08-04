import socket
from .thread_client import *


class Server:
    def __init__(self, host='', port=5566):
        self.active_threads = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        self.data_settings = None
        self.data_get = None
        self.open_file_get()
        self.open_file_settings()
        self.start_json_updater()

    def start(self):
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

    def clean_threads(self):
        """Clean up the list of active threads by removing the ones that have stopped."""
        self.active_threads = [t for t in self.active_threads if t.is_alive()]
        if len(self.active_threads) !=  self.data_settings["nb_active_players"]:
            self.data_settings["nb_active_players"] = len(self.active_threads)
            self.data_settings["active_players"] = [t.id for t in self.active_threads]
            self.handle_json_settings()
            print(f"Active threads : {len(self.active_threads)}")

    def receive_conn(self, conn: socket) -> int:
        id_ = None
        prefix = conn.recv(4)
        if prefix == b'ID  ':
            id_ = int.from_bytes(conn.recv(1), 'big')
        if id_ == 0:
            self.data_settings["nb_players"] += 1
            id_ = self.data_settings["nb_players"]
            print(f"new client : id = {id_}")
        else:
            print(f"id client = {id_}")
        return id_

    def open_file_get(self):
        try:
            with open("game/data_json/data_get.json", 'r') as f:
                self.data_get = json.load(f)
        except:
            print("error")
            pass
    
    def open_file_settings(self):
        try:
            with open("game/data_json/settings.json", 'r') as f:
                self.data_settings = json.load(f)
        except:
            print("error")
            pass
    
    def handle_json_data(self):
        while True:
            try :
                with open(f'game/data_json/data_get.json', 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    json.dump(self.data_get, f, indent=4)
                    f.truncate()
            except:
                print("error")
                pass
            self.clean_threads()

    def handle_json_settings(self):
            try :
                with open(f'game/data_json/settings.json', 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    json.dump(self.data_settings, f, indent=4)
                    f.truncate()
            except:
                print("error")
                pass
    
    def start_json_updater(self):
        """Start a separate thread to update JSON data."""
        updater_thread = threading.Thread(target=self.handle_json_data, daemon=True)
        updater_thread.start()
    
    def send_id(self, conn, id_):
        id_prefix = b'ID  '
        conn.sendall(id_prefix + id_.to_bytes())