from socket import *
import sys

serverName = 'localhost'
serverPort = 8081
path = '/index.html'

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(2)
clientSocket.connect((serverName, int(serverPort)))

request = "GET " + path + " HTTP/1.1\r\nHost: " + serverName + "\r\n\r\n"
clientSocket.send(request.encode())

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