#!/usr/bin/env python3

#server
import argparse
import socket
import os
import library
import multiprocessing
import subprocess
import signal

def parseArgs():
    """
    Description     : Parses the command line arguments 
    Return Value    : args - the command line arguments
    """
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-p', type=str, help='port number', required = True)
    parser.add_argument('-d', type=str, help='directory to server files from', required = True)

    args = parser.parse_args()
    return args

def readSocket(client):
    socketRead = b""
    while True:
        buffer = client.recv(1024)
        if buffer == None:
            break
        socketRead += buffer
        if(str(socketRead.decode()).endswith("\r\n\r\n")):
            break

    return str(socketRead.decode())
 
def handleClient(sock):
    """
    Description : Parses server commands from the client
    Parameters  : client - client socket 
    """
    try:

        #send the BEGIN' packet
        print("sending 'BEGIN'")
        sock.sendall("BEGIN\n".encode())
        sock.sendall("\r\n\r\n".encode())
        clientMes = readSocket(sock)
        clientCmd = (clientMes.split('\n'))[1]
        print(clientCmd)
        userRequest = library.replParse(str(clientCmd))
        baseCMD = userRequest['baseCMD']    
        print(baseCMD)
        #give the expected result
        if baseCMD == "pwd":
            currRemoteDir = library.execBash("pwd")
            print(currRemoteDir)
            sock.sendall(currRemoteDir.encode())
        if baseCMD == "cd":
            changedRemoteDir = userRequest['filePath']
            os.chdir(changedRemoteDir)
        if baseCMD == "ls":
            result = library.execBash("ls")
            result += "\n\r\n\r\n"
            print(result)
            sock.sendall(result.encode())
        if baseCMD == "mkdir":
            success = library.createDirectory(userRequest['filePath'])
            success = f"Success Code: {bool(success)}"
            sock.sendall(success.encode())
    except Exception as e:
        print(f"Error: {e}")
        
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
    bytes = b''
    while len(bytes) != n:
        bytes += s.recv(n - len(bytes))
        if len(bytes) == 0: break
    return bytes



def sigintHandler(signum, frame):
    #
    #
    #DO STUFF TO EXIT GRACEFULLY
    #
    #
    exit(1)
    return


def main(): 
    """
    Description : Runs the main routine of the server
    """
    args = parseArgs()
    library.userCMD['filePath'] = args.d
    os.chdir(library.userCMD['filePath'])

    signal.signal(signal.SIGINT, sigintHandler)

    
    try:
        server = createServer(int(args.p))
        while True:
            client, _ = server.accept()

            socketList.append(client)
            processList.append( multiprocessing.Process(target = handleClient, args = (client,) ))
            processList[-1].run()

            
            #fork a new process
#            pid = os.fork() 
#
            #child
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
    processList = []
    socketList = []
    main()
