#!/usr/bin/env python3

# server
import argparse
import socket
import os
import library
import multiprocessing
import subprocess
import time
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
        if buffer == None:
            client.close()
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
        while sock != 0:
            clientMes = readSocket(sock)
            clientCmd = (clientMes.split("\n"))[1]
            print(clientCmd)
            userRequest = library.replParse(str(clientCmd))
            baseCMD = userRequest["baseCMD"]
            print(baseCMD)
        # give the expected result
            if baseCMD == "exit":
                print("Closing Connection")
                sock.close()
                os._exit(0)
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
                if(library.doesExist(userRequest['fileRequested']) == False):
                    type='d'
                    code=404
                    output = userRequest['fileRequested']+": Resource does not exist"
                elif(os.path.isdir(userRequest['fileRequested']) and userRequest['isRecursive'] == True):
                        type='c'
                        code = 200
                        output = library.directoryCopy(userRequest['fileRequested'])
                        print(output)
                elif(os.path.isdir(userRequest['fileRequested']) and userRequest['isRecursive'] == False):
                    type='d'
                    code=400
                    output = "Must use Recursive for directories"
                    print(output)
                elif(os.path.isfile(userRequest['fileRequested'])):
                    type = 'f'
                    code=200
                    output = str(library.fileToByte(userRequest['fileRequested']))
                    print(output)
                message = constructMessage(output, type, code)
                sock.send(message.encode())
            if baseCMD == "mkdir":
                success = library.createDirectory(userRequest["filePath"])
                success = f"Success Code: {success}"
                if success:
                    errorCode = 200
                else:
                    errorCode = 404
                success = constructMessage(success, "c", errorCode)
                sock.send(success.encode())
    except Exception as e:
        print(f"Error: {e}")

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
        retMessage += "file\n"
    elif type == "d":
        retMessage += "data\n"
    elif type == "c":
        retMessage += "directory\n"

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
#    mainSocket_G[0].close()
    print("shutting down new connections now. shutting down current connections in 30 seconds")
#    time.sleep(1)
#    for s in socketList_G:
#        s.close()
#    for p in processList_G:
#        p.join(0.1)
#        if p.exitcode == None:
#            p.kill()
    #
    #
    # DO STUFF TO EXIT GRACEFULLY
    #
    #
    exit(1)
    return


def main():
    """
    Description : Runs the main routine of the server
    """
    args = parseArgs()
    library.userCMD["filePath"] = args.d
    os.chdir(library.userCMD["filePath"])


    try:
        server = createServer(int(args.p))
        mainSocket_G.append(server)
        while True:
            client, _ = server.accept()

            socketList_G.append(client)
            clientProcess = multiprocessing.Process(target = handleClient, args=(client, args))
            processList_G.append(clientProcess)
            clientProcess.run()
            clientProcess.start()

            # fork a new process
    #            pid = os.fork()
    #
    # child
    #           if pid == 0:
    #                server.close()
    #                handleClient(client)
    #            #parent
    #            else:
    #                os.wait()
    #                client.close()
    #                os._exit(0)
    except OSError as e:
        print(f"Error! {e}")
        os._exit(0)



if __name__ == "__main__":
    processList_G = []
    socketList_G = []
    mainSocket_G = []
    main()
