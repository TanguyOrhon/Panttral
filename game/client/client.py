from socket import *

class Client:
    def __init__(self) -> None:
        self.host = '192.168.1.163'
        self.port = 5566


    def connection(self):
        client_socket = socket(AF_INET, SOCK_STREAM)
        try:
            client_socket.connect((self.host, self.port))
            print("Connected")

            data = client_socket.recv(1024).decode()
            
            settings_path = 'game/settings.py'
            with open(settings_path, 'w') as file:
                file.write(data)

            print("File received successfully")

        except Exception as e:
            print(f"Connection refused: {e}")
        finally:
            client_socket.close()