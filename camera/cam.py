import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

class Camera():
        def __init__(self):                                                                                     #setup Pi Camera and haarcascade classifier
                print("initializing Pi Camera...")

                self.cap = PiCamera()
                self.cap.resolution = (640, 480)
                self.framerate = 60
                self.rawCapture = PiRGBArray(self.cap, size=(640, 480))

                self.faceCascade = cv2.CascadeClassifier('camera/haarcascade_frontalface_default.xml')

                print("done")
    
        def averageGraySpace(self, grayFrame):                                                                  #calculate average light level from frame in gray space
                rows=[]
                for row in grayFrame:
                        rowavg = cv2.mean(grayFrame[row])
                        rows.append(rowavg)
                avgs=[]
                for avg in rows:
                        avgs.append(avg[0])
		
                tavg = sum(avgs)/len(avgs)

                return tavg

        def getFrame(self):                                                                                     #retreive frame from camera as an array
                self.cap.capture(self.rawCapture, format="bgr", use_video_port=True)
                frame = self.rawCapture.array
                self.rawCapture.truncate(0)		

                return frame

        def convertGray(self, frame):                                                                           #convert frame array to gray space
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
                return gray

        def getFaces(self, frame):                                                                              #find faces in frame array with haarcascade
                faces = self.faceCascade.detectMultiScale(frame, 1.3, 5)

                return faces

        def highlightFace(self, frame, faces):                                                                  #draw rectangle around the faces returned by getFaces()
                img = frame
                for (x,y,w,h) in faces:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

                return img

        def saveFrame(self, frame, name="image"):                                                               #save frame array to disk as image
                cv2.imwrite(name, frame)
                
        def __del__(self):
                #self.cap.close() 
                pass
