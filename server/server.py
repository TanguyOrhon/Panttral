from socket import *

host = '192.168.1.163'
port = 5566
socket = socket(AF_INET, SOCK_STREAM)
socket.bind((host, port))

print("The server is started.")

while True:
    socket.listen()
    conn, address = socket.accept()
    print("Listening")
    conn.close()

socket.close()