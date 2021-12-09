from socket import *
serverIP = ''
serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverIP,serverPort))
serverSocket.listen(1)
print('server ready to receive:')



while True:
    connectionSocket, clientAddr = serverSocket.accept()
    f = open('server_input.png', 'rb')
    l = f.read(1024)
    while l:
        connectionSocket.send(l)
        l = f.read(1024)

    f.close()
    print('done sending!')
    connectionSocket.close()