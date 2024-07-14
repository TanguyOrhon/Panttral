from threading import Thread
from socket import socket
import os

class ThreadClient(Thread):
    def __init__(self, conn: socket) -> None:
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        file_path = "server/image_test.ico"
        file_size = os.path.getsize(file_path)
        self.conn.sendall(file_size.to_bytes(8, 'big'))
        
        with open(file_path, "rb") as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                self.conn.sendall(data)
        self.conn.close()