import socket
from .thread_client import *


class Server:
    def __init__(self, host='', port=5566):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        



    def start(self):
        while True:
            conn, address = self.server_socket.accept()
            print('Connected by', address)
            my_thread = ThreadClient(conn)
            my_thread.start()