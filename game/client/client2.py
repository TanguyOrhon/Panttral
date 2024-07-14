from socket import *

host = '192.168.208.1'
port = 5566

client_socket = socket(AF_INET, SOCK_STREAM)
try:
    client_socket.connect((host, port))
    print("Connected")

    file_size = int.from_bytes(client_socket.recv(8), 'big')
    save_path = 'received_image_test.ico'
    
    with open(save_path, 'wb') as file:
        bytes_received = 0
        while bytes_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            bytes_received += len(data)

    print("File received successfully")

except Exception as e:
    print(f"Connection refused: {e}")
finally:
    client_socket.close()