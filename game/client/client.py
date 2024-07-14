from socket import *
import time
from settings import *
import json

class Client:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.port = 5566


    def connection(self):
        while True:
            client_socket = socket(AF_INET, SOCK_STREAM)
            try:
                client_socket.connect((self.host, self.port))
                print("Connected")

                data = client_socket.recv(1024).decode('utf-8')
                player_data = json.loads(data)
                print(player_data)
                PLAYER1 = player_data

                print("File received successfully")

            except Exception as e:
                print(f"Connection refused: {e}")
            finally:
                time.sleep(1)
                client_socket.close()