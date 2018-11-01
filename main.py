try:
    print("importing modules...")
    from gdrive.drivePublisher import Gpublisher
    from slack.slackPublisher import Spublisher
    from camera.cam import Camera
    import time
    import os
    print("done")
except Exception as e:
    print("error importing modules")
    print(e)
    exit()

try:
    print("initializing modules...")
    camera = Camera()
    slack = Spublisher()
    drive = Gpublisher()
    print("done")
except Exception as e:
    print("error initializing modules")
    print(e)
    exit()

def closeAll():
    print("stopping MailBot")
    exit()

def Upload(frame):
    imagePath = "camera/image/image.jpg"                    #location for temporary image storage   
    
    camera.saveFrame(frame, imagePath)                      #save frame to disk
    
    fileID = drive.upload(imagePath)                        #upload frame to gdrive
    
    URL = "https://drive.google.com/uc?id=" + str(fileID)   #convert fileID into embeddable URL
    slack.post(URL)                                         #post message to slack
    
    os.remove(imagePath)                                    #remove frame from disk

    print("uploaded image")
    
print("starting main loop")

timer = 0
timerConstant = 1
isOpen = False
doorState1 = False
doorState2 = False
openFrames=[]
startDetection = False
faceDetected = False

while True:
    try:
        frame = camera.getFrame()                               #get frame from camera
        gray = camera.convertGray(frame)                        #convert to grayscale
        
        if timer <= 0:
            average = camera.averageGraySpace(gray)

            if average > 100:                                      #detect if door is open
                doorState1 = True
                openFrames.append(gray)
            else:
                doorState1 = False

            if doorState2 == doorState1 and doorState2 == True:
                isOpen = True
                
            elif doorState2 == doorState1 and doorState2 == False:
                if isOpen == True:
                    startDetection = True
                    
                isOpen = False

            if startDetection == True:
                for f in openFrames:

                    print("searching for faces...")
                    faces = camera.getFaces(f)                      #detect faces in frame
                
                    if len(faces) == 0 or len(faces) > 1:           #only continue with good data
                        pass

                    else:
                        print("face found")
                        f = camera.highlightFace(f, faces)  #draw rectangle around detected face
                        print("uploading image")
                        Upload(f)                               #upload image to the internet
                        timer = 30                                  #wait 30 seconds before attempting to find another face
                        print("delay", timer, " seconds")
                        faceDetected = True
                        break

                if faceDetected == False:
                    print("no face found")
                    median = int(len(openFrames)/2)
                    print("uploading image")
                    Upload(openFrames[median])
                    timer = 30
                    print("delay", timer, " seconds")

                openFrames=[]
                faceDetected = False
                startDetection = False

            doorState2 = doorState1

        else:
            time.sleep(timerConstant)
            timer-=1

    except KeyboardInterrupt:
        print("keyboard interrupt")
        break

    except Exception as e:
        print("error")
        print(e)
        break

closeAll()
