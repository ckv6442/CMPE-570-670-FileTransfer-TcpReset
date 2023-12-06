# CMPE-570-TCP-RESET
## To run on Windows:
1. Install nmap for Windows. We will use the networking tools, mainly ncat, which are contained within nmap.
2. Install Wireshark. This will not work without Wireshark since Windows does not have a native loopback adapter like Unix systems.
3. Open two command prompt windows. 
4. In one window, enter "ncat -nvl 8000" to start a TCP connection on localhost port 8000.
5. In the other window, enter "ncat 127.0.0.1 8000" to connect to the host.
6. In Wireshark, enter the display filter "tcp.srcport==8000". This will look for tcp connections with the source port of 8000.
7. Wireshark should have captured some kind of handshake packet already, but if it didn't use one of the command prompt windows to send a test packet.
8. In one of the captured packets, look for "Frame #" and expand it. Then look for "Interface id" and expand it. Copy the value for "Interface name". It should be something like "\Device\NPF_Loopback".
9. Use this name for the value of iface in the Python script. (Hint: In Python, a backslash is \\\\).
10. Run the Python script from the command line, and go back to one of the command prompt windows and try to send something.
11. You should see some of the information of the packet in the command prompt window of the Python script, and you should be able to match it up with what Wireshark is capturing.
