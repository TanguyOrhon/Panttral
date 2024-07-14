from threading import Thread
from socket import socket

class ThreadClient(Thread):
    def __init__(self, conn: socket) -> None:
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        data = self.conn.recv(1024)
        data = data.decode("utf8")
        print(data)
        self.conn.close()