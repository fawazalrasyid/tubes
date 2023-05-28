#Import packages
import threading
from socket import *
import sys

#Set server address
serverPort = 8081
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

def handle_request(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        
        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
        
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
        
    except IOError:
        #Send response message forfile not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>'.encode())
        
        #Close client socket
        connectionSocket.close()

while True:
    #Establish the connection
    print('Server ready to serve...')
    connectionSocket, addr =  serverSocket.accept()
    
    #Create a new thread for each client
    client_thread = threading.Thread(target=handle_request, args=(connectionSocket,))
    client_thread.start()

serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data
