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
    socketRead = b""
    while True:
        buffer = client.recv(1024)
        if buffer == None:
            client.close()
        socketRead += buffer
        if str(socketRead.decode()).endswith("\r\n\r\n"):
            break

    return str(socketRead.decode())


def handleClient(sock):
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
            if baseCMD == "pwd":
                currRemoteDir = library.execBash("pwd")
                message = constructMessage((currRemoteDir + " "), "d", 200)
                sock.send(message.encode())
            if baseCMD == "cd":
                changedRemoteDir = userRequest["fileRequested"]
                #check if the user has access to the file
                base_path = os.path.abspath(os.getcwd())
                file_path = os.path.abspath(os.getcwd() + get_file_path(changedRemoteDir))
                is_safe = file_path.startswith(base_path)
                if is_safe:
                    os.chdir(changedRemoteDir)
                    message = constructMessage((userRequest["fileRequested"] + " is the current directory"), "d", 200)
                    sock.send(message.encode())
                if not is_safe:
                    message = constructMessage(("You do not have Access to this directory"), "d", 403)
            if baseCMD == "ls":
                result = library.execBash("ls")
                message = constructMessage(result, "d", 200)
                print(message)
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

def get_file_path(req):
    s = req.split()
    if len(s) >= 3:
        return s[1]
    return ""

def constructMessage(message, type, errorCode):
    retMessage = str(errorCode) + "\n"

    if type == "f":
        retMessage += "file\n"
    elif type == "d":
        retMessage += "data\n"
    elif type == "c":
        retMessage += "directory\n"

    return retMessage + message + "\r\n\r\n"


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
    mainSocket_G.close()
    print("shutting down new connections now. shutting down current connections in 30 seconds")
    time.sleep(30)
    for s in socketList_G:
        s.close()
    for p in processList_G:
        p.kill()
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

    signal.signal(signal.SIGINT, sigintHandler)

    try:
        server = createServer(int(args.p))
        while True:
            client, _ = server.accept()

            socketList_G.append(client)
            processList_G.append(
                multiprocessing.Process(target=handleClient, args=(client,))
            )
            processList_G[-1].run()

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
        print(e)
        os._exit(0)
        print(f"Connection Error {e}")


if __name__ == "__main__":
    processList_G = []
    socketList_G = []
    mainSocket_G
    main()
