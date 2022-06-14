import socket
from tokenize import String

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    msgToSend = input("Enter your message: ")
    clientsocket.send(bytes(msgToSend,"utf-8"))