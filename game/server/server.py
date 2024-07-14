import socket
import threading
import time
import server.thread_client as thr
import game

class Server:
    def __init__(self, host='0.0.0.0', port=5566):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        self.game_data = {}  # Shared game data



    def start(self):
        while True:
            conn, address = self.server_socket.accept()
            print('Connected by', address)
            my_thread = thr.ThreadClient(conn)
            my_thread.start()