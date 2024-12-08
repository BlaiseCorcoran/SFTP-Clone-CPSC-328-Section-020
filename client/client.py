#!/usr/bin/env python3

import argparse
import os
import library
import socket

#client
def parseArgs():
    #initialize
    parser = argparse.ArgumentParser(prog='client.py', description='Specify host and port to connect to', add_help=False) 

    #add arguments
    parser.add_argument('-h', type=str, help="Host", required=True) 
    parser.add_argument('-p', type=str, help="Port", required=True) 

    #parse the arguments 
    args = parser.parse_args()

    return args

#name:replLoop 
#purpose: to provide the ability to use the user to type commands in the prompt
def replLOOP():
    running = True
    print("Welcome to SFTP Clone\n")
    while running:
        userInput = input("> ")
        handler(userInput)


#name: handler
#input: user input string from the REPL
#output: bool - success or not
#purpose: to process the logic of the user argument and package data to send to the server
def handler(userInput):
    userRequest = library.replParse(str(userInput))
    baseCMD = userRequest['baseCMD']
    try:
        if(baseCMD == "exit"):
            os._exit(0)
        elif(baseCMD == "help"):
            printHelp()
        elif(baseCMD == "lpwd"):
            print("Current Directory: ")
            library.execBash("pwd")
        elif(baseCMD == "ls"):
            print(library.execBash("lls"))
        elif(baseCMD == "cd"):
            directory = userRequest['filePath']
            print(library.execBash(str("lcd " + directory)))
        elif(baseCMD == "lmkdir"):
            success = library.createDirectory(userRequest['filePath'])
            print("Succes Code: " + bool(success))
        else:
            print("Command Not Found! Enter 'help' For More Info")
    except OSError as e:
        print(f"Error! {e}")



#purpose: print the massive help string, just in a seperate function for neatness
def printHelp():
    helpString = """
    exit – quit the application.

    cd [path] – Change remote directory to path. If path is not specified, then change directory to the one the session started in.

    get [-R] remote-path [local-path] – Retrieve the remote-path and store it on the local machine. If the local path name is not specified, it is given the same name it has on the remote machine.

    If the -R flag is specified then directories will be copied recursively.

    help – Display help text.

    lcd [path] – Change local directory to path. If path is not specified, then change directory to the local user’s home directory.

    lls [path] – Display local directory listing of either path or current directory if path is not specified.

    lmkdir path – Create local directory specified by path.

    lpwd – Print local working directory.

    ls [path]Display a remote directory listing of either path or the current directory ifpath` is not specified.

    mkdir path – Create remote directory specified by path.

    put [-R] local-path [remote-path] – Upload local-path and store it on the remote machine. If the remote path name is not specified, it is given the same name it has on the local machine.

    If the -R flag is specified then directories will be copied recursively.

    pwd - Display remote working directory.
    """
    print(helpString)

# name: constructMessage
# input: mainMessage - string - what you want to send 
#        messageType - char - type of message
#        'f' = file, 'd' = data
# return: returnString - string to send to server
def constructMessage(mainMessage, messageType):
    pass

#Source    : Dr Schwesinger's public CPSC 328 Directory
#Retreived : November 12th, 2024
#Link      : /export/home/public/schwesin/cpsc328/examples/2024-11-12/Python
def reallyRecvall(s, n):
    """
    Description : Ensures all the bytes have been received from the client
    Parameters  : s - the socket
                  n - the number of bytes
    """
    bytes = b''
    while len(bytes) != n:
        bytes += s.recv(n - len(bytes))
        if len(bytes) == 0: break
    return bytes

def main():
    args = parseArgs()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((args.h, int(args.p))) #connect to the servers
            msgRecv = client.recv(4096)
            print(msgRecv.decode())
            replLOOP() #enter the repl loop
            client.close() #close the client when done
    except OSError as e:
        print(e)



if __name__ == "__main__":
    main()