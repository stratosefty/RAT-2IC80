
import socket
import os
HOST = "131.155.246.24"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        print(data)
        if data== b's':
            print("Get Fucked")
        if data== b'cmd':
            print("open command promptS")
