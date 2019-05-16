import bluetooth #From PyBluez library

serverAddress = 'B8:27:EB:C5:67:60'#Address of server
port = 1#port client connects too
backlog = 1
BserverSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM) #Opens Socket with RFCOMM
BserverSocket.bind((serverAddress,port)) #Binds the socket to specified port and address as server socket
BserverSocket.listen(backlog)
try:    
    Bclient, address = BserverSocket.accept() #Accepts connection from client
    print('Connection Accepted')
    fileBytes = Bclient.recv(3)