import bluetooth #From PyBluez library
import datetime
from time import sleep
serverAddress = 'B8:27:EB:C5:67:60'#Address of server
port = 1#port client connects too
backlog = 1

while True:    
    imageReceived = 1
    
    while imageReceived:
        try:
            BserverSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM) #Opens Socket with RFCOMM
            BserverSocket.bind((serverAddress,port)) #Binds the socket to specified port and address as server socket
            BserverSocket.listen(backlog)
            print("Accepting Connection")
            Bclient, address = BserverSocket.accept()
            print('Connection Accepted')
            imageName = Bclient.recv(1024)
            imageName = ('/home/pi/Images/' + str(datetime.datetime.utcnow()) +'.jpg').replace(" ","_")
            print(str(imageName))
            fileSize = Bclient.recv(1024)
            print((fileSize))
            fileIntByteArray = [];
            testArray = []

            try:
                while True:
                    fileByte = Bclient.recv(100000)
                    buffer = str(fileByte)[2:len(str(fileByte))-1]
                    for x in range(int(len(buffer)/3)):                     
                        fileIntByteArray.append(int(buffer[3*x:3*x+3]))
            except:
                print("No more Bytes Found/Client Closed Connection")
                BserverSocket.close()#Closes serversocket on server end
                print('closed')
                
                with open(imageName,"wb") as fileReceived:
                    fileReceived.write(bytes(fileIntByteArray))
                    print("File Made")
                    
                imageReceived = 0    
        except:
            print("Connection Error")
            sleep(5)