from socket import *

serverIP = ''
serverPort = 12000

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

with open('received_image.png', 'wb') as f:
    print('file opened')
    while True:
        data = clientSocket.recv(1024)
        if not data: break
        else:
            f.write(data)

clientSocket.close()