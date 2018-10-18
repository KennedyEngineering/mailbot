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

timer = 0
timerConstant = 1

def Upload(frame):
    imagePath = "camera/image/image.jpg"                    #location for temporary image storage   
    
    camera.saveFrame(frame, imagePath)                      #save frame to disk
    
    fileID = drive.upload(imagePath)                        #upload frame to gdrive
    
    URL = "https://drive.google.com/uc?id=" + str(fileID)   #convert fileID into embeddable URL
    slack.post(URL)                                         #post message to slack
    
    os.remove(imagePath)                                    #remove frame from disk

    print("uploaded image")
    
print("starting main loop")

while True:
    try:
        frame = camera.getFrame()                               #get frame from camera
        gray = camera.convertGray(frame)                        #convert to grayscale

        if timer <= 0:
            if camera.averageGraySpace(gray) > 100:             #detect if door is open
                print("searching for faces...")
                faces = camera.getFaces(gray)                   #detect faces in frame
                
                if len(faces) == 0 or len(faces) > 1:           #only continue with good data
                    print("no face found")
                else:
                    print("face found")
                    frame = camera.highlightFace(frame, faces)  #draw rectangle around detected face
                    print("uploading image")
                    Upload(frame)                               #upload image to the internet
                    timer = 60                                  #wait 60 seconds before attempting to find another face
                    print("delay", timer, " seconds")
            else:
                timer = 1

        else:
            time.sleep(timerConstant)
            timer-=1

    except KeyboardInterrupt:
        print("stopping MailBot")
        break
    except Exception as e:
        print("error")
        print(e)
        break
exit()
