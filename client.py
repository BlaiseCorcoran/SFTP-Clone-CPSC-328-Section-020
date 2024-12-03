#!/usr/bin/env python3

import argparse
import library

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
    if(userRequest.baseCMD == "quit"):
        exit(0)
        if(user):



def main():
    args = parseArgs()


if __name__ == "__main__":
    main()