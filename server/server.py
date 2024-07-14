from socket import *
from thread_client import ThreadClient

host = '0.0.0.0'
port = 5566
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((host, port))

print("The server is started.")

while True:
    server_socket.listen()
    conn, address = server_socket.accept()
    print("Client connected")

    my_thread = ThreadClient(conn)
    my_thread.start()

server_socket.close()