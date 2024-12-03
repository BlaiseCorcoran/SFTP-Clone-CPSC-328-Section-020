#!/usr/bin/env python3

import argparse
import library

#client
def parseArgs():
    #initialize
    parser = argparse.ArgumentParser(prog='client.py', description='Specify host and port to connect to') 

    #add arguments
    parser.add_argument('-h', type=str, help="Host", required=True) 
    parser.add_argument('-p', type=str, help="Port", required=True) 

    #parse the arguments 
    args = parser.parse_args()

    return args


def replLOOP():
    running = True
    print("Welcome to SFTP Clone\n")
    while running:
        userInput = input("> ")
        handler(userInput)


# massive switch statement, main program logic, returns a bool of successful or not
def handler(userInput):
    userRequest = library.replParse(str(userInput))

def main():
    args = parseArgs()


if __name__ == "__main__":
    main()