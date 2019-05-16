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
            i = 0
            try:
                while True:
                    fileByte = Bclient.recv(3)#Receives Byte
                    fileIntByteArray.append(int(fileByte))
                    if(int(fileByte)>255 or int(fileByte)<0):
                        print("Error ", int(fileByte), fileByte, i)
                    if(i%10000 == 0):
                        print(i)
                    i = i + 1
            except:
                print("No more Bytes Found")
                BserverSocket.close()#Closes serversocket on server end
                print('closed')
                with open(imageName,"wb") as fileReceived:
                    fileReceived.write(bytes(fileIntByteArray))
                    print("File Made")
                    sleep(5)
                imageReceive = 0    
        except:
            print("Connection Error")
            sleep(5)