import bluetooth
from picamera import PiCamera
from time import sleep
import datetime
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.IN)
serverAddress = 'B8:27:EB:C5:67:60' #Make sure Right Address
port = 1
camera = PiCamera()
camera.resolution = (60,60)

while True:
    print("Checking")
    sleep(3)
    if GPIO.input(36):
        camera.start_preview()
        sleep(5)
        imageName = ('/home/pi/Images/'+str(datetime.datetime.utcnow()) +'.jpg').replace(" ", "_")
        imagesent = 1
        camera.capture(imageName)
        camera.stop_preview()
        print("Opening Image")
        with open(imageName,"rb") as image:
            file = image.read()
            fileBytes = bytearray(file)
            print(len(fileBytes))  
        print("Image Opened and Converted To Bytes")
        while imagesent:
            try:
                print("Connecting")
                Bsocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                Bsocket.connect((serverAddress,port))
                print("Connection Established")
                print("Sending")
                Bsocket.send(imageName)
                print(imageName)
                sleep(3)
                Bsocket.send(str(len(fileBytes)))
                print(str(len(fileBytes)))
                sleep(3)
#                i = 0
                for fileByte in fileBytes:
                    if int(fileByte) <=9:
                        extendedByte = "00" + str(fileByte)
                        Bsocket.send(extendedByte)
   #                     print(extendedByte,i)
                    elif int(fileByte) <=99:
                        extendedByte = "0" + str(fileByte)
                        Bsocket.send(extendedByte)
  #                      print(extendedByte,i)
                    else:
                        Bsocket.send(str(fileByte))
    #                    print(str(fileByte),i)
#                    i = i+1
                imageSent = 0
                Bsocket.close()
                break
            except:
                print("Connection Error")
                imageSent = 0
                break
                Bsocket.close()
                sleep(5)
        
            