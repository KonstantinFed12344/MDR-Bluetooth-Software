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
    fileSize = Bclient.recv(1024)#First string recived is file size
    print(int(fileSize))
    fileIntByteArray = [];   
    with open("imageReceived.jpg","wb") as fileReceived: #Opens a file on server end to read bytes into        
        print('Image Opened')
        fileByte = Bclient.recv(3)#Reads first byte
        print('First Byte Received')
#        fileReceived.write(bytes(int(fileByte)))
        print(fileByte, 0)
        i = 1
        fileIntByteArray.append(int(fileByte))
#        fileByte = Bclient.recv(3)
#        print(fileByte, 1)
        while True:
#           fileReceived.write(bytes(fileByte))#Writes byte to file
            
            fileByte = Bclient.recv(3) #Receives next byte
            fileIntByteArray.append(int(fileByte))
 #           print(bytes(int(fileByte)),i)
            i = i + 1
            if(int(fileByte)>255 or int(fileByte)<0):
                print("Error ", int(fileByte), fileByte, i)
#            else:
#                print(int(fileByte), fileByte, i)
#            if i  == 16:
#                print(i)
#                print("Printing Array")
#                print(bytes(fileIntByteArray[:16]))
#                break

            if(i%10000 == 0):
                print(i)       
except:
    #Bclient.close()#Closes socket on client end
    BserverSocket.close()#Closes serversocket on server end
    print('closed')
    with open("imageReceived.jpg","wb") as fileReceived:
        fileReceived.write(bytes(fileIntByteArray))    
