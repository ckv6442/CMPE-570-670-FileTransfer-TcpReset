import socket
import os

def send_file(connection, file_path):
    file_size = os.path.getsize(file_path)
    connection.send(str(file_size).encode())
    print(f"Sending file of size {file_size} bytes")

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            connection.send(data)

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        file_path = "BigFile.txt"
        send_file(client_socket, file_path)

        print("File sent successfully")

    finally:
        client_socket.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    start_client()
