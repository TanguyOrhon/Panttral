from socket import *

host = '88.183.196.207'
port = 5566

client_socket = socket(AF_INET, SOCK_STREAM)
try:
    client_socket.connect((host, port))
    print("Connected")

    data = "Test 1"
    client_socket.sendall(data.encode("utf8"))

except Exception as e:
    print(f"Connection refused: {e}")
finally:
    client_socket.close()