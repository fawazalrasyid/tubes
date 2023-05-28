#Import packages
from socket import *
import sys

#Set server address
serverName = 'localhost'
serverPort = 8081
path = '/index.html'

clientSocket = socket(AF_INET, SOCK_STREAM) #Create socket cleint
clientSocket.settimeout(2) #Set timeout to 2 seconds
clientSocket.connect((serverName, int(serverPort))) #Connect to server

request = "GET " + path + " HTTP/1.1\r\nHost: " + serverName + "\r\n\r\n" #Request string with the GET method
clientSocket.send(request.encode()) #Sends the request to the server by converting the string to bytes using the encode() method.

#Starts an infinite loop to receive and print the server's response.
while True:
    try:
        response = clientSocket.recv(1024)
        if response:
            print(response.decode(), end = "")
        else:
            break
    except socket.timeout:
        print("Timeout np more TCP packages, closing the connection...")
        break

clientSocket.close()