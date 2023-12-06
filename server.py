import socket
import os
import time
from tqdm import tqdm
import matplotlib.pyplot as plt

def receive_file(connection, file_size):
    received_size = 0
    start_time = time.time()  # Start time
    transfer_data = []  # List to store timestampled tuples (timestamp, received_size)
     
    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Receiving") as progress_bar:
        with open("ReceivedFile.txt", "wb") as file:
            while received_size < file_size:
                data = connection.recv(1024)
                if not data:
                    break
                file.write(data)
                received_size += len(data)
                progress_bar.update(len(data))  # Update progress bar
                transfer_data.append((time.time() - start_time, received_size))  # Record timestamp and data received
            
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken: {duration:.2f} seconds") # Print total duration of file transfer     
    return transfer_data # Returns transfer_data list to then visualize with matplotlib
    
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

        transfer_data = receive_file(client_socket, file_size)
        plot_transfer_progress(transfer_data)

        print("File received successfully")
        client_socket.close()

def plot_transfer_progress(transfer_data):
    timestamps, data_received = zip(*transfer_data)
    data_received_MB = [bytes / (1024 * 1024) for bytes in data_received] # Convert data received from bytes to MB
    plt.plot(timestamps, data_received_MB)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Data Received (MB)')
    plt.title('File Transfer Progress')
    plt.show()
    
if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    start_server()
