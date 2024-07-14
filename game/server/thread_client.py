from threading import Thread
import socket
import os
import player
import pickle
import game

class ThreadClient(Thread):
    def __init__(self, conn: socket.socket) -> None:
        super().__init__()
        self.conn = conn


    def run(self) -> None:
        file_path = "game/server/settings_test.py"
        with open(file_path, 'r') as file:
            data = file.read()
        self.conn.sendall(data.encode())
        self.conn.close()