# echo-server.py
import os

import socket

HOST = "145.116.40.250"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print ("Server started")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print (data)
            if not data:
                break
            if data == (b"shutdown"):
                os.system("shutdown /s /t 1")
            conn.sendall(data)