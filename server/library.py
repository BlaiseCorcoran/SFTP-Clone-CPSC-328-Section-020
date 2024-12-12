#!/usr/bin/env python3

import os
import subprocess

"""
Authors: Blaise Corcoran, Lou Wertman, Michael Colanene
Due Date: December 12th, 4pm
Class: CPSC-328_020
Professor: Dr. Schwesinger
Assignment: Final Project - SFTP Clone
Purpose:  To provide a set of libraries to the client and to the server regarding file manipulation
"""

#library

userCMD = {
    "baseCMD" : "",
    "fileRequested" : "",
    "filePath" : "",
    "isRecursive" : False
}




def replParse(userCommandString):
    """
    input: commands - string that user types in REPL
    output: userCMD - dictionary with information about the command

    name: replParse
    purpose: parses the Read-Eval-Print loop user arguments.
    when requesting or sending files the fileRequested value is used
    when changing or listing directories the filePath value is used
    for certain commands where the default dir is the current dir, instead
    of being left blank the filePath will be './'
    return value: returns a userCMD dictionary containing the values.   
    """
    retval = userCMD
    commandArgs = userCommandString.rsplit(" ")
    retval["baseCMD"] = commandArgs[0]
    baseCommand = retval["baseCMD"]
    #no match statement acad's python3 is too old :'(
    try:
        if baseCommand == "exit" :
            return retval
        elif baseCommand == "cd" :
            retval["fileRequested"] = commandArgs[1]
            return retval
        elif baseCommand == "get" :
            if commandArgs.count("-R") > 0:
                commandArgs.remove("-R")
                retval["isRecursive"] = True
            retval["fileRequested"] = commandArgs[1]
            if len(commandArgs) > 2 :
                retval["filePath"] = commandArgs[2]
            return retval
        elif baseCommand == "help" :
            return retval
        elif baseCommand == "lcd" :
            if len(commandArgs) > 1:
                retval["filePath"] = commandArgs[1]
                return retval
            else:
                return retval
        elif baseCommand == "lls" :
            if len(commandArgs) > 1 :
                retval["filePath"] = commandArgs[1]
                return retval
            else :
                return retval
        elif baseCommand == "lmkdir" :
            retval["filePath"] = commandArgs[1]
            return retval
        elif baseCommand == "lpwd" :
            return retval
        elif baseCommand == "ls" :
            if len(commandArgs) > 1:
                retval["filePath"] = commandArgs[1]
                return retval
            else :
                retval["filePath"] = "./"
                return retval
        elif baseCommand == "mkdir":
            retval["filePath"] = commandArgs[1]
            return retval
        elif baseCommand == "put":
            if(commandArgs.count("-R") > 0) :
                commandArgs.remove("-R")
                retval["isRecursive"] = True
            retval["fileRequested"] = commandArgs[1]
            if len(commandArgs) > 2:
                retval["filePath"] = commandArgs[2]
            return retval
        elif baseCommand == "pwd":
            return retval
    except Exception as e:
        print(f"Error! {e}")


def doesExist(pathString):
    """
    input: pathString - path to file
    return: bool - true or false if the file exist, will return false if permission is denied
    """
    if((os.path.isdir(pathString) or os.path.isfile(pathString)) and os.access(pathString, os.R_OK)):
        return True
    else:
        return False


def fileToByte(file):
    """
    input: pathString - file to covert to []byte
    return:  []byte data of file
    """
    if(os.path.isfile(file) == True):
        file = open(file, "r")
        fileContents = file.read()
        buffer = bytes(fileContents.encode())
        return buffer
    else:
        print('File does not exist')
        return False
    


def returnDirectory(path):
    """
    input: path - path to return directory from
    return: string - directory where the file resides
    """
    return os.path.dirname(path)


def createDirectory(path):
    """
    input: path - where to create directory
    return: bool - success
    """
    if(doesExist(path) == False):
        os.mkdir(path)
        return True
    else:
        return False


def bufferToFile(buffer, filePath):
    """
    input: buffer - recieved buffer; filePath - where to create file
    return: bool - success
    """
    if(not doesExist(filePath)):
        file = open("file", "wb")
        file.write(buffer)
    else:
        return False



def execBash(commandString):
    """
    input: commandString - command to execute
    return: string - return of execution
    found https://docs.python.org/3/library/subprocess.html#subprocess.check_output
    """
    ret = subprocess.check_output(commandString, shell=True, stderr=subprocess.STDOUT)
    return str(ret.decode())


def directoryCopy(filePath):
    """
    input: commandString - command to execute
    return: string - return of execution
    found https://docs.python.org/3/library/os.html 
    """
    commandBuild = ""
    if(not doesExist):
        return NULL
    for root, dirs, files in os.walk(filePath):
        for name in dirs:
            dirPath = os.path.join(root, name)
            commandBuild += f"mkdir -p '{dirPath}';\n" 
        for name in files:
            pathFile = os.path.join(root, name)
            filebytes = str(fileToByte(pathFile))
            fileString= filebytes.replace("'", "'\\''")  
            fileString= filebytes.replace("'", "'\\#'")
            commandBuild += f"echo '{fileString}' > '{pathFile}';\n" 

    return commandBuild

def main():
    pass

if __name__ == "__main__":
    main()
