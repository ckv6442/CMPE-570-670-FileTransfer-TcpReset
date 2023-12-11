import socket
import os

file_size = 14

sizes = {
    0 : "FileSizes\\SmallFile.txt", # Approx 50 bytes
    1 : "FileSizes\\1KB.txt",
    2 : "FileSizes\\5KB.txt",
    3 : "FileSizes\\10KB.txt",
    4 : "FileSizes\\25KB.txt",
    5 : "FileSizes\\50KB.txt",
    6 : "FileSizes\\100KB.txt",
    7 : "FileSizes\\1MB.txt",
    8 : "FileSizes\\5MB.txt",
    9 : "FileSizes\\10MB.txt",
    10 : "FileSizes\\25MB.txt",
    11 : "FileSizes\\50MB.txt",
    12 : "FileSizes\\100MB.txt",
    13 : "FileSizes\\250MB.txt",
    14 : "FileSizes\\BigFile.txt" # Approx 9 GB
}

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

        file_path = sizes[file_size]
        send_file(client_socket, file_path)

        print("File sent successfully")

    finally:
        client_socket.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    start_client()
