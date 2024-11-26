#!usr/bin/env python3

#test python file to make sure the library is working

import library

def main():
    #testing doesExist(pathString)
    existsArg = input(print("Enter A Directory That Works: "))
    doesItExist = library.doesExist(existsArg)
    print(doesItExist) #should print true
    doesntExistArg = input(print("Enter A Directory That Doesn't Work: "))
    itDoesntExist = library.doesExist(doesntExistArg)
    print(itDoesntExist) #should print false

    #testing fileToByte(file)
    file = "test.txt"


    #testing returnDirectory(path)


    #testing createDirectory()



if __name__ == '__main__':
    main()