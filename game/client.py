from socket import *

host = '192.168.1.163'
port = 5566

socket = socket(AF_INET, SOCK_STREAM)
try:
    socket.connect((host, port))
    print("Connected")

except:
    print("Connection refused")
    socket.close()
