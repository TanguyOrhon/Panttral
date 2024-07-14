from threading import Thread
import socket
from server.settings_test import *
import json

class ThreadClient(Thread):
    def __init__(self, conn: socket.socket) -> None:
        super().__init__()
        self.conn = conn


    def run(self) -> None:
        player_data = json.dumps(PLAYER1)
        self.conn.sendall(player_data.encode('utf-8'))
        self.conn.close()