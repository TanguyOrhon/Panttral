import socket
import threading
import time

class Server:
    def __init__(self, host='0.0.0.0', port=5566):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        self.game_data = {}  # Shared game data

    def handle_client(self, client_socket, client_address):
        print(f"Connection from {client_address}")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received {data} from {client_address}")
                self.modify_game_data(client_address, data)
                response = f"Data received: {data.decode('utf-8')}"
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print(f"Connection closed from {client_address}")
            client_socket.close()

    def modify_game_data(self, client_address, data):
        # Modify shared game data based on client data
        self.game_data[client_address] = data.decode('utf-8')
        print(f"Game data updated: {self.game_data}")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()