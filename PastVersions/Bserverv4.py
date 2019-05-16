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
            i = 330
            a = 0
            try:
                while True:
                    fileByte = Bclient.recv(990)#Receives Byte
 #                   if a == 0:
                        
                    buffer = str(fileByte)[2:len(str(fileByte))-1]
                    print(buffer)
                    print(int(len(buffer)/3))
                    for x in range(int(len(buffer)/3)):
                        if(int(len(buffer)) != 990):
                            print("Test")
                            if a == 0:
                                print(int(len(buffer)/3))
                                print(len(buffer)/3)
                                print(len(buffer))
                                a = 1
                            print(buffer[x*3:x*3+3])
                            testArray.append(int(buffer[3*x:3*x+3]))
                            print("Added")
                            print(int(buffer[3*x:3*x+3]))
                     
                        fileIntByteArray.append(int(buffer[3*x:3*x+3]))
                        
#                    print("Packet Done")    
#                    sleep(3)    
  #                  print(buffer[0:3])
 #                   print(buffer[3:6])
                    
#                        fileIntByteArray.append(buffer[3*x:3*x+3])

#                    fileIntByteArray.append(int(fileByte))
#                    if(int(fileByte)>255 or int(fileByte)<0):
#                        print("Error ", int(fileByte), fileByte, i)
#                    if(i%10000 == 0):
                    print(i)
                    i = i + 330
            except:
                print("No more Bytes Found")
                print(testArray)
                print(bytes(testArray))
                BserverSocket.close()#Closes serversocket on server end
                print('closed')
                with open('/home/pi/Images/test.txt',"w") as testFile:
                    for test in range(len(fileIntByteArray)):
                        if fileIntByteArray[test] <=9:
                            testFile.write("00"+str(fileIntByteArray[test]) +"\n")
                        elif fileIntByteArray[test] <= 99:
                            testFile.write("0"+str(fileIntByteArray[test]) +"\n")
                        else:
                            testFile.write(str(fileIntByteArray[test]) +"\n")
                with open(imageName,"wb") as fileReceived:
#                    print(bytes(fileIntByteArray[11:]))
                    fileReceived.write(bytes(fileIntByteArray))
#                    print(bytes(fileIntByteArray))
                    print("File Made")
#                    sleep(5)
                imageReceive = 0    
        except:
            print("Connection Error")
            sleep(5)