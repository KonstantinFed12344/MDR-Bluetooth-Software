import bluetooth

serverAddress = 'B8:27:EB:C5:67:60'#Address of server
port = 1#port client connects too
backlog = 1
BserverSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM) #Opens Socket with RFCOMM
BserverSocket.bind(('B8:27:EB:D7:1B:CE',1)) #Binds the socket to specified port and address as server socket
BserverSocket.listen(backlog)

Bclient, address = BserverSocket.accept() #Accepts connection from client
print('Connection Accepted')
fileSize = Bclient.recv(1024)#First string recived is file size
print(int(fileSize))

with open("imageReceived.jpg","wb") as fileReceived: #Opens a file on server end to read bytes into        
        print('Image Opened')
        fileByte = Bclient.recv(1024)#Reads first byte
        print('First Byte Received')
        fileReceived.write(bytes(fileByte))
        print(bytes(fileByte), 0)
        while True:
            fileReceived.write(fileByte)#Writes byte to file
            fileByte = Bclient.recv(1024)


BserverSocket.close()#Closes serversocket on server end
print('closed')