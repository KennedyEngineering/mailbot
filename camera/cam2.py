import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def averageGraySpace(grayArray):
	rows=[]
	for row in gray:
		rowavg = cv2.mean(gray[row])
		rows.append(rowavg)
	avgs=[]
	for avg in rows:
		avgs.append(avg[0])
	tavg = sum(avgs)/len(avgs)

	return tavg

while True:
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	timer = 0
	timerConstant = 1 # amount of seconds per 'tick'
	if timer == 0:

		if averageGraySpace(gray) > 100: #light is abundantly present
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)

			if len(faces) == 0 or len(faces) > 1:
				pass
			else:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
				cv2.imwrite("face.jpg", frame)
				timer = 60
		else:
			print("no")

	else:   #tick
		time.sleep(timerConstant)
		timer-=1
