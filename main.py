from gdrive.drivePublisher import Gpublisher
from slack.slackPublisher import Spublisher
from camera.cam import Camera
import time
import os

camera = Camera()
slack = Spublisher()
drive = Gpublisher()

timer = 0
timerConstant = 1

def Upload(frame):
    imagePath = "camera/image/image.jpg"   
    
    camera.saveFrame(frame, imagePath)                      #save frame to disk
    
    fileID = drive.upload(imagePath)                        #upload frame to gdrive
    
    URL = "https://drive.google.com/uc?id=" + str(fileID)   #convert fileID into embeddable URL
    slack.post(URL)                                         #post message to slack
    
    os.remove(imagePath)                                    #remove frame from disk

    exit()
    
while True:
    frame = camera.getFrame()
    gray = camera.convertGray(frame)

    if timer == 0:
        if camera.averageGraySpace(gray) > 100:
            faces = camera.getFaces(gray)

            if len(faces) == 0 or len(faces) > 1:
                pass
            else:
                frame = camera.highlightFace(frame, faces)
                Upload(frame)
                timer = 60

        else:
            timer = 1

    else:
        time.sleep(timerConstant)
        timer-=1

exit()
