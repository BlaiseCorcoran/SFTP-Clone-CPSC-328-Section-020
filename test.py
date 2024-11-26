#!/usr/bin/env python3

#test python file to make sure the library is working

import library
import argparse


def parseArgs():
    #initialize
    parser = argparse.ArgumentParser(prog='test.py', description='Gets two directories. One that actually exists and one that doesnt') 

    #add arguments
    parser.add_argument('-e', '--exists', type=str, help="Directory That Exists", required=True) 
    parser.add_argument('-f', '--fake', type=str, help="Directory That Doesn't Exist", required=True) 

    #parse the arguments 
    args = parser.parse_args()

    return args


def main():

    #get parsed arguments
    args = parseArgs()

    #testing replParse
    #not yet implemented

    #testing doesExist(pathString)
    existsArg = args.e
    doesItExist = library.doesExist(existsArg)
    print(doesItExist) #should print true
    doesntExistArg = args.f
    itDoesntExist = library.doesExist(doesntExistArg)
    print(itDoesntExist) #should print false

    #testing fileToByte(file)
    #file = "test.txt"


    #testing returnDirectory(path)


    #testing createDirectory(path)


    #testing bufferToFile(buffer, filePath)


    #testing execBash(commandString)


    #testing directoryCopy(filePath)
    #not yet implemented



if __name__ == '__main__':
    main()