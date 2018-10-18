import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

class Camera():
        def __init__(self):
                print("initializing camera...")

                self.cap = PiCamera()
                self.cap.resolution = (640, 480)
                self.framerate = 60
                self.rawCapture = PiRGBArray(self.cap, size=(640, 480))

                self.faceCascade = cv2.CascadeClassifier('camera/haarcascade_frontalface_default.xml')

                print("done")
    
        def averageGraySpace(self, grayFrame):
                rows=[]
                for row in grayFrame:
                        rowavg = cv2.mean(grayFrame[row])
                        rows.append(rowavg)
                avgs=[]
                for avg in rows:
                        avgs.append(avg[0])
		
                tavg = sum(avgs)/len(avgs)

                return tavg

        def getFrame(self):
                self.cap.capture(self.rawCapture, format="bgr")
                frame = self.rawCapture.array
                self.rawCapture.truncate(0)		

                return frame

        def convertGray(self, frame):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
                return gray

        def getFaces(self, frame):
                faces = self.faceCascade.detectMultiScale(frame, 1.3, 5)

                return faces

        def highlightFace(self, frame, faces):
                img = frame
                for (x,y,w,h) in faces:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

                return img

        def saveFrame(self, frame, name="image"):
                cv2.imwrite(name, frame)
                
        def __del__(self):
                self.cap.close()
