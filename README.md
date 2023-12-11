# TCP Reset
## To run on Windows:
1. Install nmap for Windows. We will use the networking tools, mainly ncat, which are contained within nmap.
2. Install Wireshark. This will not work without Wireshark since Windows does not have a native loopback adapter like Unix systems.
3. Open three command prompt windows. 
4. Ensure that all Python packages are installed. Use "python -m pip install {package}" to install it.
5. In the first window, enter "ncat -nvl 12345" to start a TCP connection on localhost port 8000.
6. In the second window, enter "ncat 127.0.0.1 12345" to connect to the host.
7. In Wireshark, enter the display filter "tcp.srcport==12345". This will look for tcp connections with the source port of 12345.
8. Wireshark should have captured some kind of handshake packet already, but if it didn't use one of the command prompt windows to send a test packet.
9. In one of the captured packets, look for "Frame #" and expand it. Then look for "Interface id" and expand it. Copy the value for "Interface name". It should be something like "\Device\NPF_Loopback".
10. Use this name for the value of iface in the Python script. (Hint: In Python, a backslash is \\\\).
11. In the third window, run the attack using "python .\\tcp_reset.py", and go back to one of the command prompt windows and try to send something.
12. You should see some of the information of the packet in the command prompt window of the Python script, and you should be able to match it up with what Wireshark is capturing.


# File Transfer
1. Download the FileSizes folder from Google Drive: https://drive.google.com/drive/folders/1EfWqXiebljur1QqctUcUz20LPKGXy4fi?usp=sharing.
2. Move this folder into the project folder. (We could not updload all these files to GitHub).
3. Open two command prompt windows.
4. Ensure that all Python packages are installed. Use "python -m pip install {package}" to install it.
5. In one window, run the server script from the using "python .\\server.py".
6. In the other window, run the client script from theusing "python .\\client.py".
7. You can view and change the file size to be sent by going into client.py and changing the value of "file_size".


# File Transfer + TCP Reset
1. Make sure both the TCP reset and file transfer work using the steps above.
2. Open three command prompt windows.
3. In the first window, run the server script using "python .\\server.py".
4. In the second window, run the client script using "python .\\client.py".
5. In the third window, run the attack using "python .\\tcp_reset.py". It should work for the majority of file sizes, but ultimately depends on your system.
6. For larger file sizes such as the 9 GB file, you can wait for the progress bar to fill up to whatever percentage you want, and then run the attack.
7. For smaller file sizes, they send the file too quickly. If this is the case, then you have to pre-empt the attack by running it before running the client.
8. This still works because the attack is designed to listen for ACKs, but obviously in a real scenario, that wouldn't be the case.
