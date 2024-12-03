#!/usr/bin/env python3

import argparse
import library
import os

#client

#name: parseArgs
#output: args, the cmd line arguments the user selected
#purpose: to parse the host and port number
def parseArgs():
    #initialize
    parser = argparse.ArgumentParser(prog='client.py', description='Specify host and port to connect to') 

    #add arguments
    parser.add_argument('-h', type=str, help="Host", required=True) 
    parser.add_argument('-p', type=str, help="Port", required=True) 

    #parse the arguments 
    args = parser.parse_args()

    return args

#name:repleLoop 
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
    baseCMD = userRequest.baseCMD
    if(baseCMD == "quit"):
        exit(0)
    elif(baseCMD == "help"):
        printHelp()
    

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


def main():
    args = parseArgs()


if __name__ == "__main__":
    main()