#!/usr/bin/env python3
"""
Authors: Blaise Corcoran, Lou Wertman, Michael Colanene
Due Date: December 12th, 4pm
Class: CPSC-328_020
Professor: Dr. Schwesinger
Assignment: Final Project - SFTP Clone
Purpose:  To get give the user a REPL interface that sends commands to the server and recieves output from the server
"""
import argparse
import os
import library
import socket

#client
#name: parseArgs()
#purpose: parse cmd line arguments
def parseArgs():
    """
    Description     : Parses the command line arguments
    Return Value    : args - the command line arguments
    """
    #initialize
    parser = argparse.ArgumentParser(prog='client.py', description='Specify host and port to connect to', add_help=False) 

    #add arguments
    parser.add_argument('-h', type=str, help="Host", required=True) 
    parser.add_argument('-p', type=str, help="Port", required=True) 

    #parse the arguments 
    args = parser.parse_args()

    return args


def replLOOP(client):
    """
    Description : Provides the ability of the user to type commands into the prompt
    Parameters  : client - client socket
    """
    running = True
    print("Welcome to SFTP Clone\n")
    while running:
        userInput = input("> ")
        handler(userInput, client)


def handler(userInput, client):
    """
    Description : Handles the user input commands and gives the expected result
    Parameters  : userInput - user input via the command line
                  client - the client socket
    """
    userRequest = library.replParse(str(userInput))
    if userRequest == None:
        print("command fails to exist")
        return
    baseCMD = userRequest['baseCMD']
    try:
        if(baseCMD == "exit"):
            client.close()
            os._exit(0)
        elif(baseCMD == "help"):
            printHelp()
        elif(baseCMD == "lpwd"):
            print("Current Directory: ")
            os.system("pwd")
        elif(baseCMD == "lls"):
            os.system("ls")
        elif(baseCMD == "lcd"):
            directory = userRequest['filePath']
            os.chdir(directory)
        elif(baseCMD == "lmkdir"):
            success = library.createDirectory(userRequest['filePath'])
            print(f"Success Code: + {bool(success)}")
        elif(baseCMD == "mkdir"):
            message = constructMessage(f"mkdir {userRequest['filePath']}", 'd')
            client.sendall(message.encode())
            parsedResp = (readSocket(client)).split('\n')
            print("".join(parsedResp[2:]))
        elif(baseCMD == "ls"):
            message = constructMessage("ls",'d')
            client.sendall(message.encode())
            parsedResp = (readSocket(client)).split('\n')
            print("".join(parsedResp[2:]))
        elif(baseCMD=="pwd"):
            message = constructMessage("pwd", "d")
            client.sendall(message.encode())
            parsedResp = (readSocket(client)).split('\n')
            print("".join(parsedResp[2:]))
        elif(baseCMD == "cd"):
            message = constructMessage(f"cd {userRequest['fileRequested']}", "d")
            client.sendall(message.encode())
            print(readSocket(client))
        elif(baseCMD == "put"):
            handlePut(client, userRequest)
            return
            if(not library.doesExist(userRequest['filePath'])):
                print("Directory does not exist")
            else:
                if(userRequest['isRecursive'] or os.path.isfile(userRequest['filePath'])):
                    if(os.path.isfile(userRequest['filePath'])):
                        fileContents = str(library.fileToByte(userRequest['filePath']))
                        message = constructMessage("touch " + userRequest['fileRequested'] + "; echo " + fileContents + "> " + userRequest['fileRequested'] ,'f')
                    elif(os.path.isdir(userRequest['filePath'])):
                        directory = library.directoryCopy(userRequest['filePath'])
                        command = "cd " + userRequest['fileRequested'] +";" + command
                        message  = constructMessage(command,'c')
                    else:
                        print("unexpected, inexplicable error \n")
                    client.sendall(message.encode())
                else:
                    print("Needs to be Recursive with -R due to directory")
        elif(baseCMD == "get"):
            handleGET(userInput, userRequest['filePath'], userRequest['fileRequested'], client)
        else:
            print("Command Not Found! Enter 'help' For More Info")
    except OSError as e:
        print(f"Error! {e}")



def handlePut(sock, userRequest):
    if (not library.doesExist(userRequest['fileRequested'])):
        type = 'd'
        code = 404
        print( f"{userRequest['fileRequested']}: Resource does not exist")
    elif (os.path.isdir(userRequest['fileRequested']) and userRequest['isRecursive']):
        type = 'c'
        code = 200
        output = str(library.directoryCopy(userRequest['fileRequested']).decode())
        print(output)
    elif (os.path.isdir(userRequest['fileRequested']) and not userRequest['isRecursive']):
        type = 'd'
        code = 400
        print("Must use Recursive for directories")
        print(output)
    elif (os.path.isfile(userRequest['fileRequested'])):
        type = 'f'
        code = 200
        output = str(library.fileToByte(userRequest['fileRequested']).decode())
        print(output)
    else:
        type = 'd'
        code = 500
        output = "Unknown error"

    message = "200\n" + constructMessage(output, type)
    if not(code == 200):
        print (f"error: {code}")
        return
    sock.sendall(message.encode())
    recvstr = readSocket(sock)
    if (recvstr == "200"):
        print("200 ok")
    else:
        print("error from server")





def handleGET(clientCMD, userPath, dirToCopy, client):
    """
    Description : Handles GET commands and receiving commands from the server
    Parameters  : clientCMD - the client command
                  userPath - the user provided path
                  client - the client socket
    """
    request = "GET\n" + clientCMD + "\n" + "\r\n\r\n"
    client.sendall(request.encode())
    buffer = readSocket(client)
    if buffer.startswith("200"):
        response = buffer.splitlines()  # Use splitlines for better newline handling
    else:
        print("Error Occurred \n")
        print("Server Response:", buffer)
        return

    if response[1] == "directory":
        if not os.path.isdir(userPath):
            print("Error: User specified path does not exist.")
            return
        command = "".join(response[2:])
        os.system("mkdir " + dirToCopy +";" + (f"cd {userPath}; "))
        ret = os.system(command)
        print("Command Execution Result:", ret)
    elif response[1] == "file":
        commandRESP = "".join(response[2:])
        if not os.path.exists(userPath):
            command = f"touch {userPath} && echo '{commandRESP}' > {userPath}"
            ret = os.system(command)
        else:
            print("Error: File already exists and cannot be overwritten.")
    elif response[1] == "data":
        print("Received Data:", response[2])


def readSocket(client):
    """
    Description  : Reads from the client
    Parameters   : client - the client socket
    Return Value : socketRead.decode() - the decoded message from the client
    """
    socketRead = b""
    while True:
        buffer = client.recv(1024)
        if buffer == None:
            break
        socketRead += buffer
        if(str(socketRead.decode()).endswith("\r\n\r\n")):
            break

    return str(socketRead.decode())[:-4]
        


#purpose: print the massive help string, just in a seperate function for neatness
def printHelp():
    """
    Description: Prints the help message
    """
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
#        'f' = file, 'd' = data, 'c' - directory
# return: returnString - string to send to server
def constructMessage(mainMessage, messageType):
    """
    Description  : Constructs a message to be sent to the server
    Parameters   : mainMessage - the main message
                   messageType - the nature of the message
    Return Value : returnString - the constructed message
    """
    if messageType == 'f':
        returnString = "File\n"
    elif messageType == 'd':
        returnString = "Data\n"
    elif messageType == 'c':
        returnString = "Directory\n"

    returnString += mainMessage + "\n" + "\r\n\r\n"
    return returnString



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
    """
    Description: Runs the main routine
    """
    args = parseArgs()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((args.h, int(args.p))) #connect to the servers
            bytesrecv = 0
            msgRecv = b''
            while not bytesrecv == 10:
                msgRecv += client.recv(10)
                bytesrecv = len(msgRecv)
            print(msgRecv.decode())
            replLOOP(client) #enter the repl loop
            client.close() #close the client when done
    except OSError as e:
        print(e)



if __name__ == "__main__":
    main()
