import socket
import os
from tqdm import tqdm

def receive_file(connection, file_size):
    received_size = 0

    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Receiving") as progress_bar:
        with open("ReceivedFile.txt", "wb") as file:
            while received_size < file_size:
                data = connection.recv(1024)
                if not data:
                    break
                file.write(data)
                received_size += len(data)
                progress_bar.update(len(data))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        file_size = int(client_socket.recv(1024).decode())
        print(f"File size: {file_size} bytes")

        receive_file(client_socket, file_size)

        print("File received successfully")

        client_socket.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    start_server()
