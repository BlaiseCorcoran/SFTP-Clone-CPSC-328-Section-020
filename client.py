"""
DO NOT EDIT THIS VERSION OF CLIENT,
EDIT THE ONE IN THE CLIENT FOLDER
"""

#!/usr/bin/env python3

import argparse
import test.library as library
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



def main():
    args = parseArgs()


if __name__ == "__main__":
    main()