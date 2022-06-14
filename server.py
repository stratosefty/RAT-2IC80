import socket
from tokenize import String

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)
clientsocket, address = s.accept()
# now our endpoint knows about the OTHER endpoint.s
print(f"Connection from {address} has been established.")

# Server sends message and waits for reply

# To ensure that the person knows what to use there could be a help option
while True:

    msgToSend = input("Enter your message: ")
    clientsocket.send(bytes(msgToSend,"utf-8"))
    #this does not work currently since it gets an error
    msg = clientsocket.recv(1024)
    decodedMsg = msg.decode("utf-8")
    print(decodedMsg)

