import bluetooth
from picamera import PiCamera
from time import sleep
import datetime
import RPi.GPIO as GPIO
import _thread

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.IN)
GPIO.setup(37,GPIO.IN)
serverAddress = 'B8:27:EB:C5:67:60' #Make sure Right Address
port = 1
camera = PiCamera()
camera.resolution = (60,60)
Images = []

def cameraCapture():
    camera.start_preview()
    sleep(5)
    imageName = ('/home/pi/Images/'+str(datetime.datetime.utcnow()) +'.jpg').replace(" ", "_")
    imagesent = 1
    camera.capture(imageName)
    camera.stop_preview()
    Images.append(imageName)
    sleep(3)
    print("Picture Capturing Complete")
    
    
def imageSending():
    print("Opening Image")
    try:
        with open(Images[0],"rb") as image:
            file = image.read()
            fileBytes = bytearray(file)
            print(len(fileBytes))  
            print("Image Opened and Converted To Bytes")
    except:
        print("Error: Image unavailable or not convertable")
    while imagesent:
        try:
            print("Connecting")
            Bsocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            Bsocket.connect((serverAddress,port))
            print("Connection Established")
            print("Sending")
            Bsocket.send(Images[0])
            print(Images[0])
            sleep(3)
            Bsocket.send(str(len(fileBytes)))
            print(str(len(fileBytes)))
            sleep(3)

            for fileByte in fileBytes:
                if int(fileByte) <=9:
                    extendedByte = "00" + str(fileByte)
                    Bsocket.send(extendedByte)
                elif int(fileByte) <=99:
                    extendedByte = "0" + str(fileByte)
                    Bsocket.send(extendedByte)
                else:
                    Bsocket.send(str(fileByte))

            imageSent = 0
            Bsocket.close()
            del Images[0]
            break

        except:
            print("Connection Error")
            imageSent = 0
            break
            Bsocket.close()
            sleep(5)    

while True:
    print("Checking")
    sleep(3)

    if GPIO.input(37):
#        cameraCapture()
        print ("Taking Picture")
        _thread.start_new_thread(cameraCapture,())

    elif GPIO.input(36):
        imagesent = 1
#        imageSending()
        print ("Sending Picture")
        _thread.start_new_thread(imageSending,())
        
        
