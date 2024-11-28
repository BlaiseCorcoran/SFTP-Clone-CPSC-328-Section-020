#!usr/bin/env python3

import os
import subprocess

#library

userCMD = {
    "baseCMD" : "",
    "fileRequested" : "",
    "filePath" : "",
    "isRecursive" : False
}

#input: commands - string that user types in REPL
#output: userCMD - dictionary with information about the command
def replParse(commands):
    pass

# input: pathString - path to file
# return: bool - true or false if the file exist, will return false if permission is denied
def doesExist(pathString):
    if((os.path.isdir(pathString) or os.path.isfile(pathString)) and os.access(pathString, os.R_OK)):
        return True
    else:
        return False

# input: pathString - file to covert to []byte
# return:  []byte data of file
def fileToByte(file):
    if(doesExist(file) == True){
        file = open(file, "r")
        fileContents = file.read()
        buffer = bytes(fileContents)
        return buffer
    }else{
        print('File does not exist')
        return False;
    }

# input: path - path to return directory from
# return: string - directory where the file resides
def returnDirectory(path):
    return os.path.dirname(path)

# input: path - where to create directory
# return: bool - success
def createDirectory(path):
    if(doesExist == False):
        os.mkdirs(path)
        return True
    else:
        return False

# input: buffer - recieved buffer; filePath - where to create file
# return: bool - success
def bufferToFile(buffer, filePath):
    if(not doesExist(filePath)):
        file = open("file", "wb")
        file.write(buffer)
    else:
        return False


# input: commandString - command to execute
# return: string - return of execution
def execBash(commandString):
    ret = os.system(commandString)
    return ret

# input: filePath; commandBuild string use empty string; right 
# return: string - bash commands to copy directory
def directoryCopy(filePath):
    commandBuild = ""
    if(not doesExist):
        return NULL
    for root, dirs, files in os.walk(".", topdowm=True):
        for name in dirs:
            commandBuild += "mkdir " + root + name + ";"
        for name in files:
            commandBuild += "touch" + root + name
            fileData = fileToByte(name)
            fileData = str(fileData)
            commandBuild += "echo " + fileData + " > " + root+name + ";"
        return commandBuild


def main():
    pass

if __name__ == "__main__":
    main()
