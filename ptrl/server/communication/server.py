import socket
from .thread_client import *


class Server:
    def __init__(self, host='', port=5566):
        self.active_threads = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

    def start(self):
        try:
            while True:
                conn, address = self.server_socket.accept()
                print('Connected by', address)
                id_ = self.receive_conn(conn)
                my_thread = ThreadClient(conn, id_)
                my_thread.start()
                self.active_threads.append(my_thread)
                self.clean_threads()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()
            print("Server stopped")

    def clean_threads(self):
        """Clean up the list of active threads by removing the ones that have stopped."""
        self.active_threads = [t for t in self.active_threads if t.is_alive()]
        print(f"Active threads: {len(self.active_threads)}")

    def receive_conn(self, conn: socket) -> int:
        id_ = None
        prefix = conn.recv(4)
        if prefix == b'ID  ':
            id_ = int.from_bytes(conn.recv(1), 'big')
        if id_ == 0:
            id_ = 1
        return id_