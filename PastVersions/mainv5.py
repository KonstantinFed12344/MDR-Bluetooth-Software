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
camera.resolution = (400,400)
Images = []

def cameraCapture():
    print ("Taking Picture")
    camera.start_preview()
    sleep(1)
    imageName = ('/home/pi/Images/'+str(datetime.datetime.utcnow()) +'.jpg').replace(" ", "_")
    imagesent = 1
    camera.capture(imageName)
    camera.stop_preview()
    Images.append(imageName)
    sleep(1)
    print("Picture Capturing Complete")
    
    
def imageSending():
    print ("Sending Picture")
    print("Opening Image")
    imagesent = 1
    try:
        with open(Images[0],"rb") as image:
            file = image.read()
            fileBytes = bytearray(file)
            print(len(fileBytes))  
            print("Image Opened and Converted To Bytes")
#        with open('/home/pi/Images/testPerfectCopy.txt',"w") as testFile:
#            fileInt = int(fileBytes)
#            for test in range(len(fileInt)):
#                if fileInt[test] <=9:
#                    testFile.write("00" + str(fileInt[test]) + "\n")
#                elif fileInt[test] <=99:
#                    testFile.write("0"+str(fileInt[test]) + "\n")
#                else:
#                    testFile.write(str(fileInt[test]) + "\n")
    except:
        print("Error: Image unavailable or not convertable")
    while imagesent:
        
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

        sent = 0
        i = 0
        packet = ""
        for fileByte in fileBytes:
#            print("Byte")
#            print(fileByte)
#            print(int(len(fileBytes)))
            newByte = str(fileByte)
#            print(newByte)
            if i==330 or sent == int(len(fileBytes)):
                print(packet)
                print(sent + 1)
                print(int(len(fileBytes)))
                Bsocket.send(packet)
 #               if sent == int(len(fileBytes)) - 1:
 #                   for tByte in packet:
 #               sleep(1)
                i = 0
                packet = ""

            if int(fileByte) <=9:
                extendedByte = "00" + newByte
                packet = packet + extendedByte
            elif int(fileByte) <=99:
                extendedByte = "0"+ newByte
                packet = packet + extendedByte

            else:
                packet = packet + newByte
            i = i + 1
            sent = sent + 1
       
#                Bsocket.send(packet)
                        
        print(packet)
        Bsocket.send(packet)
        
        imageSent = 0
#            Bsocket.close()
        del Images[0]
        break

#        except:
#            print("Connection Error")
#            imageSent = 0
#            break
 #           Bsocket.close()
#            sleep(5)    

#while True:
print("Checking")
#sleep(3)

#    if GPIO.input(37):
#        cameraCapture()
#        
#        _thread.start_new_thread(cameraCapture,())
#cameraCapture()
#Images.append('/home/pi/Images/2019-05-06_22:59:23.926344.jpg')
Images.append('/home/pi/image2.jpg')
#    elif GPIO.input(36):
#        imagesent = 1
#        imageSending()
sleep(1)
imageSending()
print("Done or error")
#        _thread.start_new_thread(imageSending,())