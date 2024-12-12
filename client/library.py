#!/usr/bin/env python3

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

#name: replParse
#purpose: parses the Read-Eval-Print loop user arguments.
#when requesting or sending files the fileRequested value is used
#when changing or listing directories the filePath value is used
#for certain commands where the default dir is the current dir, instead
#of being left blank the filePath will be './'
#return value: returns a userCMD dictionary containing the values.
def replParse(userCommandString):
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
    if(os.path.isfile(file) == True):
        file = open(file, "r")
        fileContents = file.read()
        buffer = bytes(fileContents.encode())
        return buffer
    else:
        print('File does not exist')
        return False
    

# input: path - path to return directory from
# return: string - directory where the file resides
def returnDirectory(path):
    return os.path.dirname(path)

# input: path - where to create directory
# return: bool - success
def createDirectory(path):
    if(doesExist(path) == False):
        os.mkdir(path)
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
# found https://docs.python.org/3/library/subprocess.html#subprocess.check_output
def execBash(commandString):
    ret = subprocess.check_output(commandString, shell=True, stderr=subprocess.STDOUT)
    return str(ret.decode())

# input: filePath; commandBuild string use empty string; right 
# return: string - bash commands to copy directory
def directoryCopy(filePath):
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
