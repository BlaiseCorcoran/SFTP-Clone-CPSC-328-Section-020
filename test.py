#!/usr/bin/env python3

#test python file to make sure the library is working

import library
import argparse


def parseArgs():
    #initialize
    parser = argparse.ArgumentParser(prog='test.py', description='Gets two directories. One that actually exists and one that doesnt') 

    #add arguments
    parser.add_argument('-e', type=str, help="Directory That Exists", required=True) 
    parser.add_argument('-f', type=str, help="Directory That Doesn't Exist", required=True) 

    #parse the arguments 
    args = parser.parse_args()

    return args


def main():

    #get parsed arguments - only keep this until we implement replParse
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
    file = "test.txt"
    byteFile = library.fileToByte(file)
    print(type(byteFile))

    #testing returnDirectory(path)
    dir = library.returnDirectory(existsArg)
    print(dir)

    #testing createDirectory(path)
    newDir = "newDirectory"
    library.createDirectory(newDir)

    #testing bufferToFile(buffer, filePath)
    library.bufferToFile(byteFile, newDir)

    #testing execBash(commandString)
    library.execBash("pwd") 

    directorycopy = library.directoryCopy("planning")
    fullCMD = "cd cpinto; " + str(directorycopy)
    library.execBash(fullCMD)

    #testing directoryCopy(filePath)
    #not yet implemented



if __name__ == '__main__':
    main()