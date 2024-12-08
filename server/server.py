#!/usr/bin/env python3

#server
import argparse
import socket
import os
import library

def parseArgs():
    """
    Description     : Parses the command line arguments 
    Return Value    : args - the command line arguments
    """
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-p', type=str, help='port number')
    parser.add_argument('-d', type=str, help='directory to server files from')

    args = parser.parse_args()
    return args

def handleClient(sock):
    """
    Description : Parses server commands from the client
    Parameters  : client - client socket 
    """
    try:
        #send the BEGIN' packet
        print("sending 'BEGIN'")
        sock.sendall("BEGIN".encode())
        sock.sendall("\n".encode())
        #receive the command from the client
        clientCmd = sock.recv(4096).decode()
        library.userCMD['baseCMD'] = clientCmd
        #parse the command
        parsedCmd = library.replParse(library.userCMD)       
        #send the command to the client
        print("SENDING THE RESULT TO THE SERVER")
        sock.sendall(parsedCmd.encode())
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

def main(): 
    """
    Description : Runs the main routine of the server
    """
    args = parseArgs()
    library.userCMD['filePath'] = args.d

    try:
        server = createServer(int(args.p))
        while True:
            client, _ = server.accept()

            #fork a new process
            pid = os.fork() 

            #child
            if pid == 0:
                server.close()
                handleClient(client)
            #parent
            else:
                os.wait()
                client.close()
                os._exit(0)
    except OSError as e:
        print(e)
        os._exit(0)
        print(f"Connection Error {e}")

if __name__ == "__main__":
    main()