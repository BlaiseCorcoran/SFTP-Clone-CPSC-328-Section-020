#!/usr/bin/env python3

"""
Authors: Blaise Corcoran, Lou Wertman, Michael Colanene
Due Date: December 12th, 4pm
Class: CPSC-328_020
Professor: Dr. Schwesinger
Assignment: Final Project - SFTP Clone
Purpose: To create a concurrent server to respond to client requests for/to give files or directories
"""

# server
import argparse
import socket
import os
import library
import multiprocessing
import time
import shutil
import signal


def parseArgs():
    """
    Description     : Parses the command line arguments
    Return Value    : args - the command line arguments
    """
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument("-p", type=str, help="port number", required=True)
    parser.add_argument(
        "-d", type=str, help="directory to server files from", required=True
    )

    args = parser.parse_args()
    return args


def readSocket(client):
    """
    Description  : Reads from the client
    Parameters   : client - the client socket
    Return Value : socketRead.decode() - the decoded message from the client
    """
    socketRead = b""
    while True:
        buffer = client.recv(1024)
        if not buffer:
            print("client closed connection")
            break
        socketRead += buffer
        if str(socketRead.decode()).endswith("\r\n\r\n"):
            break

    return str(socketRead.decode())


def handleClient(sock, args):
    """
    Description : Parses server commands from the client
    Parameters  : client - client socket
    """
    try:
        # send the BEGIN' packet
        print("sending 'BEGIN'")
        sock.sendall("BEGIN\n\r\n\r\n".encode())
        while True:
            clientMes = readSocket(sock)
            if clientMes == 0:
                return
            clientCmd = (clientMes.split("\n"))[1]
            print(clientCmd)
            userRequest = library.replParse(str(clientCmd))
            baseCMD = userRequest["baseCMD"]
            print(baseCMD)
        # give the expected result
            if baseCMD == "pwd":
                currRemoteDir = str(library.execBash("pwd"))
                message = constructMessage(currRemoteDir, "d", 200)
                sock.send(message.encode())
            if baseCMD == "cd":
                changedRemoteDir = userRequest["fileRequested"]
                #check if the user has access to the file
                base_path = os.path.abspath(args.d)
                file_path = os.path.abspath(args.d + changedRemoteDir)
                is_safe = file_path.startswith(base_path)
                if is_safe:
                    os.chdir(changedRemoteDir)
                    message = constructMessage((userRequest["fileRequested"] + " is the current directory"), "d", 200)
                    sock.send(message.encode())
                elif not is_safe:
                    message = constructMessage(("You do not have Access to this directory"), "d", 403)
                    sock.send(message.encode())
            if baseCMD == "ls":
                result = library.execBash("ls")
                print("STRING IS: " + result)
                message = constructMessage(result, "d", 200)
                print(message)
                sock.send(message.encode())
            if baseCMD == "get":
                handleGet(sock, userRequest)
            if baseCMD == "put":
                handlePut(sock, userRequest)
    except Exception as e:
        print(f"Error: {e}")
        sock.close()
        return
    finally:
        sock.close()

def handlePut(socket, userRequest):
    buffer = readSocket(client)
    #if buffer.startswith("200"):
    response = buffer.splitlines()  # Use splitlines for better newline handling
    #else:
    #    print("Error Occurred \n")
    #    print("Server Response:", buffer)
    #    return

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
        socket.sendall(b"200".encode())

    return

def handleGet(sock, userRequest):
    """
    input: socket, userRequest dictionary
    purpose: handle get command from the client and serve the request
    """
    if (not library.doesExist(userRequest['fileRequested'])):
        type = 'd'
        code = 404
        output = f"{userRequest['fileRequested']}: Resource does not exist"
    elif (os.path.isdir(userRequest['fileRequested']) and userRequest['isRecursive']):
        type = 'c'
        code = 200
        output = str(library.directoryCopy(userRequest['fileRequested']).decode())
        print(output)
    elif (os.path.isdir(userRequest['fileRequested']) and not userRequest['isRecursive']):
        type = 'd'
        code = 400
        output = "Must use Recursive for directories"
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

    message = constructMessage(output, type, code)
    sock.send(message.encode())

def get_dir_path(req):
    """
    Description  : gets the path of the requested directory
    Parameters   : req - the requested directory
    Return Value : the directory path
    """
    s = req.split()
    if len(s) >= 3:
        return s[1]
    return ""

def constructMessage(message, type, errorCode):
    """
    Description  : Constructs the message to be sent to the client
    Parameters   : message - The message as a string 
                   type - the nature of the message
                   errorCode - the HTTP response code
    Return Value : The constructed message
    """
    retMessage = str(errorCode) + "\n"

    if type == "f":
        retMessage += "file\r\n"
    elif type == "d":
        retMessage += "data\r\n"
    elif type == "c":
        retMessage += "directory\r\n"

    return (retMessage + message + "\n\r\n\r\n")


def createServer(port):
    """
    Description  : creates a server
    Parameters   : port - the user input port number
    Return Value : server - the server socket
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()
    return server

def handle_shutdown(signal, frame):
    shutdownTimer = 5
    print(f"\nServer shutting down in {shutdownTimer} seconds...")
    for pid in client_pids:
        os.kill(pid, signal.SIGTERM)  # Terminate child processes
    time.sleep(shutdownTimer)
    os._exit(0)


def reallyRecvall(s, n):
    """
    Description : Ensures all the bytes have been received from the client
    Parameters  : s - the socket
                  n - the number of bytes
    """
    bytes = b""
    while len(bytes) != n:
        bytes += s.recv(n - len(bytes))
        if len(bytes) == 0:
            break
    return bytes


def sigintHandler(signum, frame):
    """
    Description  : handles sigint
    Parameters   : signum - the signal
                   frame - the frame
    """
    mainSocket_G.close()
    print("shutting down new connections now. shutting down current connections in 30 seconds")
    time.sleep(30)
    for s in socketList_G:
        s.close()
    for p in processList_G:
        p.join(0.1)
        if p.exitcode == None:
            p.kill()
    exit(1)
    return


def main():
    """
    Description : Runs the main routine of the server
    """
    args = parseArgs()
    library.userCMD["filePath"] = args.d
    os.chdir(library.userCMD["filePath"])

    signal.signal(signal.SIGINT, handle_shutdown)

    try:
        server = createServer(int(args.p))
        #mainSocket_G=server
        while True:
            client, _ = server.accept()
            #socketList_G.append(client)
            #clientProcess = multiprocessing.Process(target = handleClient, args=(client, args))
            #processList_G.append(clientProcess)
            #clientProcess.start()
            #clientProcess.run()
            # fork a new process
            pid = os.fork()
            # child
            if pid == 0:
                server.close()
                handleClient(client, args)
                os._exit(0)
            #parent
            else:
                os.wait()
                client.close()
    except OSError as e:
        print(f"Error! {e}")
        os._exit(0)



if __name__ == "__main__":
    processList_G = []
    socketList_G = []
    mainSocket_G = None
    main()
