##############################################################################
#Authors       : Lou Wertman, Michael Colanene, Blaise Corcoran                                              
#Due Date      : December 12th, 2024                     
#Course        : CPSC 328                                 
#Professor     : Dr. Schwesinger                          
#Assignment    : Final Project                                                                   
#Purpose       : The purpose of this project was to create an SFTP program
#############################################################################

How to build and run the client and server:  
1. Build the client and server via running the command "make"
2. In one terminal window, run the server via the command "./fileserver -p [port number] -d [directory to serve files from]"
3. In another terminal window, run the client via the command  "./fileclient -h [host name] -p [port number]"

File/Folder Manifest:
server.py - server python script  
client.py - client python script
library.py - the library we created for this project
makefile - the makefile that builds the executables
fileDir - The directory to serve files from

Responsibility List: [if you see any issues with this PLEASE SPEAK UP]
Library - Lou and Michael
Client - Lou and Blaise
Server - Michael and Blaise
Testing - All Group Members

Protocol:
For our protocol, we used a modified version of SFTP that is as follows:
1. The initial handshake begins when the client connects to the server, and a "BEGIN" message is received by the client. 
2. After this, the user sends commands through a REPL (Read Eval Print Loop). 
3. If the client sends a command concerning their local machine, the command does not get sent to the server. 
4. If the client sends a command concerning the server's remote directory, the command is sent over to the server in the form of 
a constructed message containing a main message (the comand) and a type (f - file; d - data; c - directory).
5. When the command gets sent to the server, it is executed, and the result is sent over to the client in the form of 
a constructed message containing a return message (the result), the type (f- file; d - data; c - directory), 
and the HTTP response code (404, 200, 400, 403, or 500)

Assumptions:
Client connects to server with no issues
All commands work properly
[ADD ANY MORE YOU THINK OF]

Development Process Discussion:


Status:
